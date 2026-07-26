"""Requirement 1 + 2: every command exits 0 on a good call, non-zero on a bad
one, and every --json response is valid JSON carrying the 'ok' contract key.

This is the breadth pass over the whole CLI surface. The depth tests for each
command live in test_cards.py / test_decks.py / test_sim.py / test_admin.py.

`rebuild` is the one command whose happy path is deliberately NOT executed here:
it is the only networked command in the system (constraint C1) and running it
would re-download ~500MB of bulk data. Its failure path is asserted below, and
test_constraints.py asserts that it is the only command that can reach the
network at all.
"""
from __future__ import annotations

import pytest

from conftest import assert_json_ok, assert_no_traceback

COMMANDER = "Tidus, Yuna's Guardian"

# (test id, argv) — one valid invocation per command / sub-command.
VALID = [
    ("card", ["card", "Sol Ring"]),
    ("card-no-rulings", ["card", "--no-rulings", "Rhystic Study"]),
    ("search-filters", ["search", "type:creature", "color:g", "cmc<=2"]),
    ("search-text", ["search", "draw a card"]),
    ("rule-exact", ["rule", "601.2"]),
    ("rule-search", ["rule", "commander damage"]),
    ("glossary-exact", ["glossary", "Commander"]),
    ("glossary-search", ["glossary", "commander damage"]),
    ("deck-list", ["deck"]),
    ("deck-show", ["deck", "tidus"]),
    ("deck-show-group-cmc", ["deck", "tidus", "--group", "cmc"]),
    ("deck-stats", ["deck", "stats", "bumbleflower"]),
    ("deck-bracket", ["deck", "bracket", "dogmeat"]),
    ("edhrec", ["edhrec", "tidus"]),
    ("edhrec-missing", ["edhrec", "tidus", "--missing", "--limit", "5"]),
    ("deck-goldfish", ["deck", "goldfish", "tidus", "--seed", "42"]),
    ("goldfish-alias", ["goldfish", "dogmeat", "--seed", "7", "--turns", "3"]),
    ("goldfish-mulligan", ["goldfish", "bumbleflower", "--seed", "9", "--mulligans", "2"]),
    ("merge", ["merge", "tidus", "bumbleflower", "--commander", COMMANDER]),
    ("merge-legal-only", ["merge", "tidus", "dogmeat", "--commander", COMMANDER, "--show", "legal"]),
    ("status", ["status"]),
    ("log-game-list", ["log", "game", "--list"]),
    ("log-rule-list", ["log", "rule", "--list"]),
]

# (test id, argv, emits_json) — emits_json is False when argparse itself rejects
# the call before any handler runs (argparse prints usage to stderr, by design).
INVALID = [
    ("card-missing", ["card", "Zzzznotacard Fakename"], True),
    ("card-no-arg", ["card"], False),
    ("search-no-match", ["search", "zzzznotacardtext qqqq"], True),
    ("search-bad-cmc", ["search", "cmc<=notanumber"], True),
    ("rule-missing", ["rule", "999.999"], True),
    ("glossary-missing", ["glossary", "zzzznotaterm"], True),
    ("deck-missing", ["deck", "notadeck"], True),
    ("deck-stats-missing", ["deck", "stats", "notadeck"], True),
    ("deck-bracket-missing", ["deck", "bracket", "notadeck"], True),
    ("edhrec-missing-slug", ["edhrec", "notadeck"], True),
    ("goldfish-missing-deck", ["goldfish", "notadeck", "--seed", "1"], True),
    ("goldfish-no-deck", ["deck", "goldfish"], True),
    ("merge-missing-deck", ["merge", "tidus", "notadeck", "--commander", COMMANDER], True),
    ("merge-missing-commander", ["merge", "tidus", "bumbleflower", "--commander", "Nobody At All"], True),
    ("merge-no-commander-flag", ["merge", "tidus", "bumbleflower"], False),
    ("log-no-subcommand", ["log"], True),
    ("log-game-incomplete", ["log", "game", "--deck", "tidus"], True),
    ("log-game-bad-deck", ["log", "game", "--deck", "notadeck", "--result", "win"], True),
    ("log-game-bad-result", ["log", "game", "--deck", "tidus", "--result", "victory"], False),
    ("log-rule-incomplete", ["log", "rule", "--rule", "903.4"], True),
    ("log-rule-missing-rule", ["log", "rule", "--rule", "999.999", "--note", "x"], True),
    ("rebuild-bad-only", ["rebuild", "--only", "bogus"], False),
    ("no-command", [], False),
    ("unknown-command", ["definitelynotacommand"], False),
]


@pytest.mark.parametrize("argv", [a for _, a in VALID], ids=[i for i, _ in VALID])
def test_valid_invocation_exits_zero(cli, argv):
    result = cli(*argv)
    assert result.returncode == 0, (
        f"{result.label} exited {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    assert result.stdout.strip(), f"{result.label} printed nothing on stdout"


@pytest.mark.parametrize("argv", [a for _, a in VALID], ids=[i for i, _ in VALID])
def test_valid_invocation_json_is_valid_and_ok(cli, argv):
    result = cli("--json", *argv)
    assert result.returncode == 0, (
        f"{result.label} exited {result.returncode}\n{result.stdout}\n{result.stderr}"
    )
    payload = assert_json_ok(result, expect_ok=True)
    assert payload["ok"] is True


@pytest.mark.parametrize(
    "argv", [a for _, a, _ in INVALID], ids=[i for i, _, _ in INVALID]
)
def test_invalid_invocation_exits_nonzero(cli, argv):
    result = cli(*argv)
    assert result.returncode != 0, (
        f"{result.label} exited 0 but should have failed\n{result.stdout}\n{result.stderr}"
    )


@pytest.mark.parametrize(
    "argv",
    [a for _, a, emits in INVALID if emits],
    ids=[i for i, _, emits in INVALID if emits],
)
def test_invalid_invocation_json_reports_not_ok(cli, argv):
    result = cli("--json", *argv)
    assert result.returncode != 0, f"{result.label} exited 0 but should have failed"
    payload = assert_json_ok(result, expect_ok=False)
    assert payload["ok"] is False
    assert payload.get("error"), f"{result.label}: failure JSON carries no error message"


@pytest.mark.parametrize("argv", [a for _, a in VALID], ids=[i for i, _ in VALID])
def test_no_command_ever_leaks_a_traceback(cli, argv):
    assert_no_traceback(cli(*argv))


def test_help_lists_every_command(cli):
    result = cli("--help")
    assert result.returncode == 0
    for command in (
        "card",
        "search",
        "rule",
        "glossary",
        "deck",
        "edhrec",
        "goldfish",
        "merge",
        "rebuild",
        "status",
        "log",
    ):
        assert f"  {command}" in result.stdout, f"'{command}' missing from mtg --help"
