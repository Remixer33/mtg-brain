"""Depth tests for `mtg deck goldfish` and `mtg merge`.

Covers requirements 10, 11 and 12.

Requirement 10 is the load-bearing one: a seeded simulation that is only stable
inside one process is not deterministic. Every determinism assertion here runs
the CLI in a SEPARATE process, with a DIFFERENT PYTHONHASHSEED each time, so any
reliance on set/dict iteration order shows up as a diff.
"""
from __future__ import annotations

import pytest

from conftest import DECK_SLUGS, assert_json_ok, identity

TIDUS = "Tidus, Yuna's Guardian"
BUMBLE = "Ms. Bumbleflower"
DOGMEAT = "Dogmeat, Ever Loyal"


# ----------------------------------------------------------------- requirement 10
def test_goldfish_is_byte_identical_across_three_processes(cli):
    runs = []
    for hashseed in ("0", "1", "12345"):
        result = cli(
            "deck", "goldfish", "tidus", "--seed", "42", env={"PYTHONHASHSEED": hashseed}
        )
        assert result.returncode == 0, result.combined
        assert result.stdout.strip(), "goldfish printed nothing"
        runs.append(result.stdout)

    assert runs[0] == runs[1] == runs[2], (
        "goldfish --seed 42 is NOT deterministic across processes.\n"
        "--- run 1 (PYTHONHASHSEED=0) ---\n" + runs[0] +
        "\n--- run 2 (PYTHONHASHSEED=1) ---\n" + runs[1] +
        "\n--- run 3 (PYTHONHASHSEED=12345) ---\n" + runs[2]
    )


def test_goldfish_json_is_byte_identical_across_processes(cli):
    runs = [
        cli("--json", "deck", "goldfish", "tidus", "--seed", "42",
            env={"PYTHONHASHSEED": seed}).stdout
        for seed in ("0", "7", "99999")
    ]
    assert runs[0] == runs[1] == runs[2], "goldfish --json --seed 42 differs between processes"


def test_different_seeds_produce_different_games(cli):
    a = cli("deck", "goldfish", "tidus", "--seed", "42")
    b = cli("deck", "goldfish", "tidus", "--seed", "43")
    assert a.returncode == 0 and b.returncode == 0
    assert a.stdout != b.stdout, "seed 42 and seed 43 produced the identical game — seed is ignored"


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_determinism_holds_for_every_deck(cli, slug):
    first = cli("deck", "goldfish", slug, "--seed", "1234", env={"PYTHONHASHSEED": "0"})
    second = cli("deck", "goldfish", slug, "--seed", "1234", env={"PYTHONHASHSEED": "31337"})
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout, f"{slug}: seeded goldfish is not reproducible"


def test_mulligans_are_deterministic_too(cli):
    a = cli("goldfish", "tidus", "--seed", "5", "--mulligans", "2", env={"PYTHONHASHSEED": "0"})
    b = cli("goldfish", "tidus", "--seed", "5", "--mulligans", "2", env={"PYTHONHASHSEED": "4242"})
    assert a.returncode == 0
    assert a.stdout == b.stdout, "mulligan handling is not deterministic"


def test_seed_is_reported_so_a_random_game_can_be_replayed(cli):
    random_run = assert_json_ok(cli("--json", "goldfish", "tidus"))
    seed = random_run["seed"]
    assert isinstance(seed, int), f"seed is {type(seed).__name__}, expected int"
    replay = assert_json_ok(cli("--json", "goldfish", "tidus", "--seed", str(seed)))
    assert [c["oracle_id"] for c in replay["opening_hand"]] == [
        c["oracle_id"] for c in random_run["opening_hand"]
    ], "replaying the reported seed did not reproduce the hand"


# ----------------------------------------------------------------- requirement 11
@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_opening_hand_is_seven_cards_from_that_deck(cli, sql, slug):
    payload = assert_json_ok(cli("--json", "deck", "goldfish", slug, "--seed", "42"))
    hand = payload["opening_hand"]
    assert len(hand) == 7, f"{slug}: opening hand has {len(hand)} cards, expected 7"

    in_deck = {
        r["oracle_id"]
        for r in sql.execute(
            "SELECT oracle_id FROM deck_cards WHERE deck_id = ? AND board = 'main'", (slug,)
        )
    }
    for card in hand:
        assert card["oracle_id"] in in_deck, (
            f"{slug}: '{card['name']}' is in the opening hand but not in the deck's main board"
        )


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_goldfish_never_draws_a_card_twice_beyond_its_copies(cli, sql, slug):
    """The library is a real 99-card shuffle: no card may appear more often than
    the deck actually runs it (basics excepted, which run many copies)."""
    payload = assert_json_ok(cli("--json", "deck", "goldfish", slug, "--seed", "42", "--turns", "8"))
    copies = {
        r["oracle_id"]: r["count"]
        for r in sql.execute(
            "SELECT oracle_id, count FROM deck_cards WHERE deck_id = ? AND board = 'main'", (slug,)
        )
    }
    seen: dict[str, int] = {}
    for card in payload["opening_hand"]:
        seen[card["oracle_id"]] = seen.get(card["oracle_id"], 0) + 1
    for draw in payload["draws"]:
        oid = draw["card"]["oracle_id"]
        seen[oid] = seen.get(oid, 0) + 1

    for oid, count in seen.items():
        assert oid in copies, "goldfish drew a card that is not in the deck"
        assert count <= copies[oid], (
            f"{slug}: drew {count} of {oid} but the deck runs {copies[oid]}"
        )
    assert len(payload["opening_hand"]) + len(payload["draws"]) + payload["library_remaining"] == 99


@pytest.mark.parametrize("slug", DECK_SLUGS)
def test_goldfish_land_count_matches_the_deck(cli, sql, slug):
    payload = assert_json_ok(cli("--json", "deck", "goldfish", slug, "--seed", "3"))
    expected = sql.execute(
        "SELECT SUM(dc.count) FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ? AND dc.board = 'main' AND c.type_line LIKE '%Land%'",
        (slug,),
    ).fetchone()[0]
    assert payload["deck"]["land_count"] == expected
    assert payload["deck"]["library_size"] == 99


def test_london_mulligan_draws_seven_and_bottoms_n(cli, sql):
    """London mulligan: always draw seven, then put N on the bottom. So the kept
    seven is 7, the bottomed pile is N, and the hand you actually play is 7-N."""
    payload = assert_json_ok(cli("--json", "goldfish", "tidus", "--seed", "11", "--mulligans", "2"))
    assert payload["mulligans_taken"] == 2
    assert len(payload["kept_seven"]) == 7, "the London mulligan still draws seven"
    assert len(payload["bottomed"]) == 2, "two mulligans put two cards on the bottom"
    assert len(payload["opening_hand"]) == 5, "hand after bottoming must be 7 - mulligans"
    assert len(payload["mulligans"]) == 2, "each thrown-back hand should be reported"

    in_deck = {
        r["oracle_id"]
        for r in sql.execute(
            "SELECT oracle_id FROM deck_cards WHERE deck_id = 'tidus' AND board = 'main'"
        )
    }
    for card in payload["kept_seven"] + payload["bottomed"] + payload["opening_hand"]:
        assert card["oracle_id"] in in_deck, f"'{card['name']}' is not in the tidus deck"


# ----------------------------------------------------------------- requirement 12
def test_merge_pool_legality_is_colour_identity_correct(cli):
    payload = assert_json_ok(
        cli("--json", "merge", "tidus", "bumbleflower", "--commander", TIDUS)
    )
    assert set(payload["color_identity"]) == set("GUW")
    assert payload["pool"], "merge produced an empty pool"

    violations = [
        f"{c['name']} {sorted(c['color_identity'])}"
        for c in payload["pool"]
        if c["legal"] and not set(c["color_identity"]) <= set("GUW")
    ]
    assert not violations, "cards marked legal that break GUW identity:\n" + "\n".join(violations)


def test_merge_legality_re_checked_against_the_database(cli, sql):
    """Do not trust the colour identity the CLI echoed back — re-read it."""
    payload = assert_json_ok(
        cli("--json", "merge", "tidus", "bumbleflower", "--commander", TIDUS)
    )
    commander_identity = identity(
        sql.execute("SELECT color_identity FROM cards WHERE name = ?", (TIDUS,)).fetchone()[
            "color_identity"
        ]
    )
    assert commander_identity == set("GUW")

    for card in payload["pool"]:
        row = sql.execute(
            "SELECT color_identity, legal_commander FROM cards WHERE oracle_id = ?",
            (card["oracle_id"],),
        ).fetchone()
        assert row is not None, f"{card['name']} is not a real card"
        ci = identity(row["color_identity"])
        if card["legal"]:
            assert ci <= commander_identity, (
                f"{card['name']} {sorted(ci)} marked legal under {sorted(commander_identity)}"
            )
            assert row["legal_commander"] != "banned", f"{card['name']} is banned but marked legal"
        else:
            assert not (ci <= commander_identity) or row["legal_commander"] in ("banned", "not_legal"), (
                f"{card['name']} {sorted(ci)} marked illegal without a reason"
            )
            assert card.get("reason"), f"{card['name']} marked illegal with no reason given"


def test_merge_pool_is_the_union_of_both_main_boards(cli, sql):
    payload = assert_json_ok(
        cli("--json", "merge", "tidus", "bumbleflower", "--commander", TIDUS)
    )
    expected = {
        r["oracle_id"]
        for r in sql.execute(
            "SELECT DISTINCT oracle_id FROM deck_cards WHERE deck_id IN ('tidus','bumbleflower')"
        )
    }
    main_only = {
        r["oracle_id"]
        for r in sql.execute(
            "SELECT DISTINCT oracle_id FROM deck_cards "
            "WHERE deck_id IN ('tidus','bumbleflower') AND board = 'main'"
        )
    }
    got = {c["oracle_id"] for c in payload["pool"]}
    invented = got - expected
    assert not invented, f"merge invented cards not in either deck: {sorted(invented)[:5]}"
    assert main_only <= got, (
        f"merge dropped {len(main_only - got)} main-board cards from the union"
    )
    # Only the chosen commander may be held out of its own candidate pool.
    held_out = expected - got
    assert len(held_out) <= 1, f"merge dropped {len(held_out)} cards from the union"
    assert payload["totals"]["pool"] == len(payload["pool"])
    assert payload["totals"]["slots_to_fill"] == 99


def test_merge_under_a_narrower_commander_marks_cards_illegal(cli, sql):
    """Bumbleflower is GUW too, so use Dogmeat (RGW) over the tidus/bumbleflower
    pool: blue cards must then be rejected, with a stated reason."""
    payload = assert_json_ok(
        cli("--json", "merge", "tidus", "bumbleflower", "--commander", DOGMEAT)
    )
    assert set(payload["color_identity"]) == set("RGW")
    illegal = [c for c in payload["pool"] if not c["legal"]]
    assert illegal, "a GUW pool under an RGW commander must produce illegal cards"
    for card in illegal[:20]:
        ci = set(card["color_identity"])
        assert not ci <= set("RGW") or card.get("reason"), (
            f"{card['name']} rejected without a reason"
        )
    for card in payload["pool"]:
        if card["legal"]:
            assert set(card["color_identity"]) <= set("RGW"), (
                f"{card['name']} {card['color_identity']} marked legal under Dogmeat"
            )
