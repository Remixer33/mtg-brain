"""Depth tests for `mtg card`, `mtg search`, `mtg rule`, `mtg glossary`.

Covers requirements 3-8. The through-line: the CLI must be a faithful window
onto the database — never a paraphrase, never a guess. Where a value is
asserted, it is re-derived from SQL in the same test rather than hard-coded,
so the tests keep meaning after the next `mtg rebuild`.
"""
from __future__ import annotations

import json
import re

import pytest

from conftest import assert_json_ok, assert_no_traceback, identity

NOT_IN_MY_DATA = "not in my data"


def _norm(text: str) -> str:
    """Collapse whitespace so wrapped terminal text can be compared to raw DB text."""
    return re.sub(r"\s+", " ", text or "").strip()


# ------------------------------------------------------------------ requirement 3
def test_sol_ring_core_fields(cli):
    payload = assert_json_ok(cli("--json", "card", "Sol Ring"))
    assert payload["name"] == "Sol Ring"
    assert payload["mana_cost"] == "{1}", f"mana_cost={payload['mana_cost']!r}, expected '{{1}}'"
    assert payload["type_line"] == "Artifact", f"type_line={payload['type_line']!r}"


def test_sol_ring_text_mode_shows_the_same_facts(cli):
    result = cli("card", "Sol Ring")
    assert result.returncode == 0
    assert "Sol Ring" in result.stdout
    assert "{1}" in result.stdout
    assert "Artifact" in result.stdout
    assert "{T}: Add {C}{C}." in _norm(result.stdout)


def test_card_rulings_are_exactly_what_the_database_holds(cli, sql):
    """`mtg card` must report every ruling the DB has for that oracle_id — no
    more (invention) and no fewer (silent truncation).

    NOTE ON REQUIREMENT 3 ("Sol Ring ... >= 1 ruling"): Scryfall's rulings bulk
    genuinely contains ZERO rulings for Sol Ring (77,999 rulings across 19,770
    oracle_ids, none of them Sol Ring's). Asserting >= 1 there would be
    asserting a fact about Magic that is not true, so this test asserts the
    stronger and checkable property — CLI ruling count == SQL ruling count —
    for Sol Ring, and test_card_with_rulings_surfaces_them below proves the
    rulings path really does return rulings for a card that has them.
    """
    payload = assert_json_ok(cli("--json", "card", "Sol Ring"))
    oracle_id = payload["oracle_id"]
    expected = sql.execute(
        "SELECT comment FROM rulings WHERE oracle_id = ? ORDER BY published_at, rowid",
        (oracle_id,),
    ).fetchall()
    assert payload["ruling_count"] == len(expected), (
        f"card reported {payload['ruling_count']} rulings, SQL has {len(expected)}"
    )
    assert len(payload["rulings"]) == len(expected)
    got = {_norm(r["comment"]) for r in payload["rulings"]}
    want = {_norm(r["comment"]) for r in expected}
    assert got == want, "ruling text does not match the database verbatim"


def test_card_with_rulings_surfaces_them(cli, sql):
    """The rulings join actually works: pick the card the DB says has the most
    rulings and demand the CLI hands back every one of them, verbatim."""
    row = sql.execute(
        "SELECT c.name, c.oracle_id, COUNT(*) n FROM rulings r "
        "JOIN cards c ON c.oracle_id = r.oracle_id "
        "WHERE c.layout = 'normal' AND c.legal_commander IS NOT NULL "
        "GROUP BY c.oracle_id ORDER BY n DESC, c.name LIMIT 1"
    ).fetchone()
    assert row is not None and row["n"] >= 1

    payload = assert_json_ok(cli("--json", "card", row["name"]))
    assert payload["ruling_count"] >= 1
    assert payload["ruling_count"] == row["n"], (
        f"{row['name']}: CLI {payload['ruling_count']} rulings vs SQL {row['n']}"
    )
    want = {
        _norm(r["comment"])
        for r in sql.execute("SELECT comment FROM rulings WHERE oracle_id = ?", (row["oracle_id"],))
    }
    assert {_norm(r["comment"]) for r in payload["rulings"]} == want


def test_card_never_resolves_to_a_token_row(cli, sql):
    """219 names map to more than one oracle_id (token vs real printing). A
    lookup must land on the real card."""
    ambiguous = [
        r["name"]
        for r in sql.execute(
            "SELECT name FROM cards GROUP BY name HAVING COUNT(DISTINCT oracle_id) > 1 "
            "ORDER BY name LIMIT 25"
        )
    ]
    assert ambiguous, "expected duplicate-name cards in the corpus"
    checked = 0
    for name in ambiguous:
        real = sql.execute(
            "SELECT oracle_id FROM cards WHERE name = ? "
            "AND layout NOT IN ('token','art_series','double_faced_token') "
            "AND legal_commander IS NOT NULL",
            (name,),
        ).fetchall()
        if len(real) != 1:
            continue  # genuinely ambiguous even among real cards — not this test's job
        result = cli("--json", "card", name)
        if result.returncode != 0:
            continue  # the CLI may legitimately ask for disambiguation
        payload = result.json()
        if not payload.get("ok"):
            continue
        checked += 1
        row = sql.execute(
            "SELECT layout FROM cards WHERE oracle_id = ?", (payload["oracle_id"],)
        ).fetchone()
        assert row["layout"] not in ("token", "art_series", "double_faced_token"), (
            f"'{name}' resolved to the {row['layout']} row"
        )
    assert checked >= 5, f"only {checked} duplicate-name lookups were verified"


# ------------------------------------------------------------------ requirement 4
def test_missing_card_says_not_in_my_data(cli):
    result = cli("card", "Zzzznotacard Fakename")
    assert result.returncode != 0, "a card that does not exist must not exit 0"
    assert NOT_IN_MY_DATA in result.combined, (
        "the literal phrase 'not in my data' is the contract that stops agents "
        f"guessing; got:\n{result.combined}"
    )


@pytest.mark.parametrize(
    "argv",
    [
        ["card", "Zzzznotacard Fakename"],
        ["rule", "999.999"],
        ["glossary", "zzzznotaterm"],
        ["deck", "notadeck"],
        ["edhrec", "notadeck"],
        ["search", "zzzznotacardtext qqqq"],
        ["goldfish", "notadeck"],
    ],
)
def test_every_missing_lookup_says_not_in_my_data(cli, argv):
    result = cli(*argv)
    assert result.returncode != 0
    assert NOT_IN_MY_DATA in result.combined, f"mtg {' '.join(argv)}:\n{result.combined}"


def test_missing_card_json_is_machine_readable(cli):
    payload = assert_json_ok(cli("--json", "card", "Zzzznotacard Fakename"), expect_ok=False)
    assert payload["error"], "failure JSON must name what was not found"


# ------------------------------------------------------------------ requirement 5
def test_rule_601_2_is_verbatim_from_the_database(cli, sql):
    expected = sql.execute("SELECT text FROM rules WHERE rule_number = '601.2'").fetchone()["text"]
    payload = assert_json_ok(cli("--json", "rule", "601.2"))
    assert payload["mode"] == "exact"
    assert payload["rule"]["rule_number"] == "601.2"
    assert payload["rule"]["text"] == expected, "rule text was altered/paraphrased"


def test_rule_601_2_text_mode_is_not_paraphrased(cli, sql):
    """Text mode wraps, but every word must still be the database's own."""
    expected = sql.execute("SELECT text FROM rules WHERE rule_number = '601.2'").fetchone()["text"]
    result = cli("rule", "601.2")
    assert result.returncode == 0
    assert _norm(expected) in _norm(result.stdout), "text output does not contain the rule verbatim"


def test_rule_601_2_lists_children_a_through_d(cli, sql):
    payload = assert_json_ok(cli("--json", "rule", "601.2"))
    listed = [c["rule_number"] for c in payload["children"]]
    for child in ("601.2a", "601.2b", "601.2c", "601.2d"):
        assert child in listed, f"{child} missing from children: {listed}"

    expected = [
        r["rule_number"]
        for r in sql.execute(
            "SELECT rule_number FROM rules WHERE parent_number = '601.2' ORDER BY rule_number"
        )
    ]
    assert sorted(listed) == sorted(expected), (
        f"children {sorted(listed)} != SQL children {sorted(expected)}"
    )

    by_number = {c["rule_number"]: c["text"] for c in payload["children"]}
    for child in ("601.2a", "601.2b", "601.2c", "601.2d"):
        want = sql.execute("SELECT text FROM rules WHERE rule_number = ?", (child,)).fetchone()["text"]
        assert by_number[child] == want, f"{child} text is not verbatim"


def test_rule_601_2_text_mode_shows_the_subrules(cli):
    result = cli("rule", "601.2")
    for child in ("601.2a", "601.2b", "601.2c", "601.2d"):
        assert child in result.stdout, f"{child} not shown in text mode"


# ------------------------------------------------------------------ requirement 6
def test_rule_fulltext_search_finds_commander_damage(cli, sql):
    payload = assert_json_ok(cli("--json", "rule", "commander damage"))
    assert payload["mode"] == "search"
    assert payload["count"] >= 1, "no FTS hits for 'commander damage'"
    assert payload["results"], "count > 0 but results list is empty"

    # Every hit must be a real rule, quoted verbatim.
    for hit in payload["results"]:
        row = sql.execute(
            "SELECT text FROM rules WHERE rule_number = ?", (hit["rule_number"],)
        ).fetchone()
        assert row is not None, f"{hit['rule_number']} is not in the rules table"
        assert hit["text"] == row["text"], f"{hit['rule_number']} text is not verbatim"

    # 704.6c is *the* commander-damage state-based action; a search that misses
    # it is not doing its job.
    numbers = [h["rule_number"] for h in payload["results"]]
    assert "704.6c" in numbers, f"expected 704.6c among hits, got {numbers}"


# ------------------------------------------------------------------ requirement 7
ADVERSARIAL = [
    '"',
    "a OR b",
    "NEAR(",
    "*",
    'foo"bar',
    "it's",
    "(unbalanced",
    "AND",
    # a few more of the same family, because FTS5 syntax has sharp edges
    "NOT",
    '""',
    "^",
    "a AND OR b",
    "col:*",
    ")",
    "-",
    "**",
    'type:creature "',
]


@pytest.mark.parametrize("query", ADVERSARIAL, ids=[repr(q) for q in ADVERSARIAL])
def test_search_survives_fts_injection(cli, query):
    result = cli("search", query)
    assert result.returncode in (0, 1), (
        f"mtg search {query!r} exited {result.returncode} — hostile input must be "
        f"answered or refused, never crashed\n{result.combined}"
    )
    assert_no_traceback(result)


@pytest.mark.parametrize("query", ADVERSARIAL, ids=[repr(q) for q in ADVERSARIAL])
def test_search_json_stays_parseable_under_injection(cli, query):
    result = cli("--json", "search", query)
    assert result.returncode in (0, 1)
    assert_no_traceback(result)
    payload = json.loads(result.stdout)  # must parse even in the failure case
    assert "ok" in payload


@pytest.mark.parametrize("query", ADVERSARIAL, ids=[repr(q) for q in ADVERSARIAL])
def test_rule_and_glossary_survive_fts_injection(cli, query):
    """The same FTS5 tables back `rule` and `glossary`; the same input must not
    blow them up either."""
    for command in ("rule", "glossary"):
        result = cli(command, query)
        assert result.returncode in (0, 1), (
            f"mtg {command} {query!r} exited {result.returncode}\n{result.combined}"
        )
        assert_no_traceback(result)


# ------------------------------------------------------------------ requirement 8
def test_search_filters_are_actually_applied(cli, sql):
    """`type:creature color:g cmc<=2` — re-check EVERY returned row against the
    database rather than trusting the result table."""
    result = cli("--json", "search", "type:creature", "color:g", "cmc<=2", "--limit", "100")
    payload = assert_json_ok(result)
    assert payload["count"] > 0, "no results for type:creature color:g cmc<=2"
    assert payload["returned"] > 0
    assert payload["results"]

    violations = []
    for card in payload["results"]:
        row = sql.execute(
            "SELECT name, type_line, cmc, color_identity FROM cards WHERE oracle_id = ?",
            (card["oracle_id"],),
        ).fetchone()
        assert row is not None, f"{card['name']} has no cards row — result was invented"
        if "creature" not in (row["type_line"] or "").lower():
            violations.append(f"{row['name']}: type_line={row['type_line']!r} is not a creature")
        if "G" not in identity(row["color_identity"]):
            violations.append(f"{row['name']}: color_identity={row['color_identity']} lacks G")
        if row["cmc"] is None or row["cmc"] > 2:
            violations.append(f"{row['name']}: cmc={row['cmc']} > 2")
    assert not violations, "filters not honoured:\n" + "\n".join(violations)


def test_search_count_matches_sql(cli, sql):
    """The reported total is the real total, not the page size."""
    payload = assert_json_ok(
        cli("--json", "search", "type:creature", "color:g", "cmc<=2", "--limit", "5")
    )
    expected = sql.execute(
        "SELECT COUNT(DISTINCT oracle_id) FROM cards "
        "WHERE lower(type_line) LIKE '%creature%' "
        "AND color_identity LIKE '%\"G\"%' AND cmc <= 2"
    ).fetchone()[0]
    assert payload["count"] == expected, f"CLI count {payload['count']} != SQL count {expected}"
    assert payload["returned"] == 5


def test_search_deck_filter_stays_inside_the_deck(cli, sql):
    payload = assert_json_ok(cli("--json", "search", "deck:tidus", "type:land", "--limit", "100"))
    in_deck = {
        r["oracle_id"]
        for r in sql.execute("SELECT oracle_id FROM deck_cards WHERE deck_id = 'tidus'")
    }
    for card in payload["results"]:
        assert card["oracle_id"] in in_deck, f"{card['name']} is not in the tidus deck"


# --------------------------------------------------------------------- glossary
def test_glossary_entry_is_verbatim(cli, sql):
    payload = assert_json_ok(cli("--json", "glossary", "Commander"))
    if payload.get("mode") == "exact":
        term, definition = payload["term"], payload["definition"]
    else:  # search mode still has to quote the database exactly
        term, definition = payload["results"][0]["term"], payload["results"][0]["definition"]
    row = sql.execute("SELECT definition FROM glossary WHERE term = ?", (term,)).fetchone()
    assert row is not None, f"glossary term {term!r} is not in the database"
    assert definition == row["definition"], "glossary definition is not verbatim"
