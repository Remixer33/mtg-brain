"""Depth tests for `mtg deck`, `mtg deck stats`, `mtg deck bracket`, `mtg edhrec`.

Covers requirements 9 and 13. Commander decks are 100 cards — 99 + commander —
and every number the CLI prints is re-derived here straight from SQL.
"""
from __future__ import annotations

import pytest

from conftest import DECK_SLUGS, assert_json_ok, identity

BRACKET_NAMES = {1, 2, 3, 4, 5}


# ------------------------------------------------------------------ requirement 9
@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_total_is_exactly_100(cli, sql, slug):
    payload = assert_json_ok(cli("--json", "deck", slug))
    assert payload["total"] == 100, f"{slug}: deck total is {payload['total']}, expected 100"

    sql_total = sql.execute(
        "SELECT SUM(count) FROM deck_cards WHERE deck_id = ?", (slug,)
    ).fetchone()[0]
    assert sql_total == 100, f"{slug}: SQL says {sql_total} cards"
    assert payload["deck"]["total_cards"] == 100


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_stats_totals_match_sql(cli, sql, slug):
    payload = assert_json_ok(cli("--json", "deck", "stats", slug))
    totals = payload["totals"]

    expected_total = sql.execute(
        "SELECT SUM(count) FROM deck_cards WHERE deck_id = ?", (slug,)
    ).fetchone()[0]
    expected_main = sql.execute(
        "SELECT SUM(count) FROM deck_cards WHERE deck_id = ? AND board = 'main'", (slug,)
    ).fetchone()[0]
    expected_cmd = sql.execute(
        "SELECT SUM(count) FROM deck_cards WHERE deck_id = ? AND board = 'commander'", (slug,)
    ).fetchone()[0]

    assert totals["cards"] == expected_total == 100
    assert totals["maindeck"] == expected_main == 99
    assert totals["commander"] == expected_cmd == 1


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_stats_land_count_matches_direct_sql(cli, sql, slug):
    """Requirement 9: the reported land count must equal a direct SQL count of
    type_line LIKE '%Land%'."""
    payload = assert_json_ok(cli("--json", "deck", "stats", slug))
    expected = sql.execute(
        "SELECT SUM(dc.count) FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ? AND c.type_line LIKE '%Land%'",
        (slug,),
    ).fetchone()[0]
    assert payload["totals"]["lands"] == expected, (
        f"{slug}: stats says {payload['totals']['lands']} lands, SQL says {expected}"
    )
    # lands/nonlands partition the 99-card maindeck; the commander is counted
    # separately (it is always available and would skew the curve).
    assert payload["totals"]["lands"] + payload["totals"]["nonlands"] == 99
    assert (
        payload["totals"]["lands"]
        + payload["totals"]["nonlands"]
        + payload["totals"]["commander"]
        == 100
    )
    # ...which is only equal to the all-boards SQL count because no commander in
    # these decks is a land. Assert that rather than assume it.
    commander_lands = sql.execute(
        "SELECT COUNT(*) FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ? AND dc.board = 'commander' AND c.type_line LIKE '%Land%'",
        (slug,),
    ).fetchone()[0]
    assert commander_lands == 0


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_stats_land_count_visible_in_text_mode(cli, sql, slug):
    expected = sql.execute(
        "SELECT SUM(dc.count) FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ? AND c.type_line LIKE '%Land%'",
        (slug,),
    ).fetchone()[0]
    result = cli("deck", "stats", slug)
    assert result.returncode == 0
    assert str(expected) in result.stdout, f"{slug}: land count {expected} not shown in text output"


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_decklist_names_all_exist_in_the_database(cli, sql, slug):
    """Nothing in a decklist may be invented: every printed name must be a card
    that is actually in that deck."""
    payload = assert_json_ok(cli("--json", "deck", slug))
    in_deck = {
        r["name"]
        for r in sql.execute(
            "SELECT c.name FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
            "WHERE dc.deck_id = ?",
            (slug,),
        )
    }
    listed, copies = set(), 0
    for group in payload["groups"].values() if isinstance(payload["groups"], dict) else payload["groups"]:
        entries = group if isinstance(group, list) else group.get("cards", [])
        for entry in entries:
            listed.add(entry["name"])
            copies += entry.get("count", 1)
    assert listed, "decklist JSON contained no cards"
    unknown = listed - in_deck
    assert not unknown, f"{slug}: names not in the deck: {sorted(unknown)}"
    assert copies == 100, f"{slug}: listed copies sum to {copies}, expected 100"


# ----------------------------------------------------------------- requirement 13
@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_bracket_is_1_to_5_with_reasoning(cli, slug):
    payload = assert_json_ok(cli("--json", "deck", "bracket", slug))
    bracket = payload["estimated_bracket"]
    assert isinstance(bracket, int), f"{slug}: bracket is {type(bracket).__name__}, expected int"
    assert bracket in BRACKET_NAMES, f"{slug}: bracket {bracket} outside 1..5"

    reasoning = payload["reasoning"]
    assert isinstance(reasoning, list), f"{slug}: reasoning is {type(reasoning).__name__}"
    assert reasoning, f"{slug}: bracket returned with empty reasoning"
    for line in reasoning:
        assert isinstance(line, str) and line.strip(), f"{slug}: blank reasoning line"
    assert payload["bracket_name"], f"{slug}: bracket has no name"


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_bracket_text_mode_shows_bracket_and_reasoning(cli, slug):
    result = cli("deck", "bracket", slug)
    assert result.returncode == 0
    payload = assert_json_ok(cli("--json", "deck", "bracket", slug))
    assert str(payload["estimated_bracket"]) in result.stdout
    # at least one reasoning line must reach the human, not just the JSON
    first = payload["reasoning"][0].split(".")[0][:40]
    assert first.split()[0] in result.stdout


def test_bracket_game_changers_are_real_cards_in_the_deck(cli, sql):
    """A Game Changer can only be counted if that card is genuinely in the deck."""
    for slug in DECK_SLUGS:
        payload = assert_json_ok(cli("--json", "deck", "bracket", slug))
        in_deck = {
            r["name"]
            for r in sql.execute(
                "SELECT c.name FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
                "WHERE dc.deck_id = ?",
                (slug,),
            )
        }
        for found in payload["game_changers_found"]:
            name = found if isinstance(found, str) else found.get("name")
            assert name in in_deck, f"{slug}: game changer {name!r} is not in the deck"


# --------------------------------------------------------------------- edhrec
@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_edhrec_is_served_from_the_local_cache(cli, sql, slug):
    payload = assert_json_ok(cli("--json", "edhrec", slug))
    assert payload["cardlists"], f"{slug}: no cached cardlists"
    cached = {r["slug"] for r in sql.execute("SELECT slug FROM edhrec_cache")}
    assert payload["commander"]["slug"] in cached, (
        f"{slug}: answered for {payload['commander']['slug']!r}, which is not in edhrec_cache"
    )
    assert "cache" in (payload.get("source") or "").lower(), (
        f"{slug}: source={payload.get('source')!r} — must state it came from the local cache"
    )


def test_deck_list_reports_all_three_decks(cli, sql):
    payload = assert_json_ok(cli("--json", "deck"))
    slugs = {d["slug"] for d in payload["decks"]}
    expected = {r["deck_id"] for r in sql.execute("SELECT deck_id FROM decks")}
    assert slugs == expected == set(DECK_SLUGS)
    for deck in payload["decks"]:
        assert deck["cards"] == 100, f"{deck['slug']}: {deck['cards']} cards"


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_deck_colour_identity_is_the_commanders(cli, sql, slug):
    """C3/EDH: the deck's stated identity must be exactly the commander's."""
    payload = assert_json_ok(cli("--json", "deck", slug))
    row = sql.execute(
        "SELECT c.color_identity FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ? AND dc.board = 'commander'",
        (slug,),
    ).fetchone()
    assert set(payload["deck"]["color_identity"]) == identity(row["color_identity"])
