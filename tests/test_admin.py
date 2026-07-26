"""Depth tests for `mtg status`, `mtg log game`, `mtg log rule`, `mtg rebuild`.

The write paths (`log game` / `log rule` without --list) are exercised
IN-PROCESS with db.DB_PATH and the two markdown targets monkeypatched into a
tmp_path, so running the suite can never append junk to Omar's real game log or
his RULES-I-KEEP-MISSING.md.

`mtg rebuild` is the only command in the system allowed to touch the network
(constraint C1), so its happy path is deliberately never executed here — that
would re-download the Scryfall bulk files. Its argument handling and its
guard-rails are asserted instead.
"""
from __future__ import annotations

import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

from conftest import ROOT, SRC, assert_json_ok

sys.path.insert(0, str(SRC))

import cli as cli_module  # noqa: E402
import cmd_admin  # noqa: E402
import db  # noqa: E402


@pytest.fixture()
def sandboxed_writes(monkeypatch, tmp_path, sandbox_db):
    """Point the learning loop at throwaway files and a throwaway database copy."""
    work_db = tmp_path / "mtg.sqlite"
    source = sqlite3.connect(f"file:{sandbox_db}?mode=ro", uri=True)
    target = sqlite3.connect(str(work_db))
    try:
        with target:
            source.backup(target)
    finally:
        target.close()
        source.close()

    game_md = tmp_path / "GAME-LOG.md"
    rules_md = tmp_path / "RULES-I-KEEP-MISSING.md"
    monkeypatch.setattr(db, "DB_PATH", work_db)
    monkeypatch.setattr(cmd_admin, "LEARNING_DIR", tmp_path)
    monkeypatch.setattr(cmd_admin, "GAME_LOG_MD", game_md)
    monkeypatch.setattr(cmd_admin, "RULES_MISSED_MD", rules_md)
    return {"db": work_db, "game_md": game_md, "rules_md": rules_md}


# ---------------------------------------------------------------------- status
def test_status_reports_real_row_counts(cli, sql):
    payload = assert_json_ok(cli("--json", "status"))
    tables = payload["tables"]
    assert isinstance(tables, dict) and tables

    for table in ("cards", "rulings", "rules", "glossary", "decks", "edhrec_cache"):
        assert table in tables, f"status does not report table {table!r}"
        reported = tables[table] if not isinstance(tables[table], dict) else tables[table].get("rows")
        actual = sql.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert reported == actual, f"status says {table}={reported}, SQL says {actual}"


def test_status_lists_the_three_decks(cli):
    payload = assert_json_ok(cli("--json", "status"))
    slugs = {d["deck_id"] for d in payload["decks"]}
    assert {"tidus", "bumbleflower", "dogmeat"} <= slugs
    for deck in payload["decks"]:
        assert deck["main_total"] == 99 and deck["commander_total"] == 1


def test_status_text_mode_is_human_readable(cli, sql):
    result = cli("status")
    assert result.returncode == 0
    assert "cards" in result.stdout
    cards = sql.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    assert f"{cards:,}" in result.stdout, "status text does not show the real card count"


def test_status_says_it_is_offline(cli):
    """C1's user-visible promise: status states the DB is local."""
    payload = assert_json_ok(cli("--json", "status"))
    assert payload["database"]["offline"] is True


# -------------------------------------------------------------------- log read
def test_log_game_list_reads_the_database_back(cli, sql):
    payload = assert_json_ok(cli("--json", "log", "game", "--list"))
    expected = sql.execute("SELECT COUNT(*) FROM game_log").fetchone()[0]
    assert payload["count"] == expected
    assert payload["games"], "game log read back empty despite rows in game_log"
    assert set(payload["record"]) == {"win", "loss", "draw"}


def test_log_game_list_filters_by_deck(cli):
    good = cli("--json", "log", "game", "--list", "--deck", "tidus")
    assert good.returncode == 0
    payload = good.json()
    assert all(g["deck_id"] == "tidus" for g in payload["games"])

    bad = cli("--json", "log", "game", "--list", "--deck", "notadeck")
    assert bad.returncode != 0
    assert_json_ok(bad, expect_ok=False)


def test_log_game_list_rejects_a_meaningless_limit(cli):
    """LIMIT 0 / negative would silently masquerade as 'nothing logged'."""
    result = cli("--json", "log", "game", "--list", "--limit", "0")
    assert result.returncode != 0
    assert_json_ok(result, expect_ok=False)


def test_log_rule_list_groups_by_rule(cli, sql):
    payload = assert_json_ok(cli("--json", "log", "rule", "--list"))
    expected_total = sql.execute("SELECT COUNT(*) FROM rules_missed").fetchone()[0]
    assert payload["total_misses"] == expected_total
    for entry in payload["most_missed"]:
        row = sql.execute(
            "SELECT text FROM rules WHERE rule_number = ?", (entry["rule_number"],)
        ).fetchone()
        if entry.get("in_rules_table"):
            assert row is not None
            assert entry["rule_text"] == row["text"], "logged rule text is not verbatim"


# ------------------------------------------------------------------- log write
def test_log_game_writes_a_row_and_a_markdown_entry(sandboxed_writes, capsys):
    code = cli_module.main(
        [
            "--json",
            "log",
            "game",
            "--deck",
            "tidus",
            "--result",
            "win",
            "--opponents",
            "pytest",
            "--notes",
            "written by the test suite",
        ]
    )
    out = capsys.readouterr().out
    assert code == 0, out

    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["logged"]["deck_id"] == "tidus"
    assert payload["logged"]["result"] == "win"

    conn = sqlite3.connect(str(sandboxed_writes["db"]))
    try:
        rows = conn.execute(
            "SELECT deck_id, result, notes FROM game_log WHERE notes = ?",
            ("written by the test suite",),
        ).fetchall()
    finally:
        conn.close()
    assert len(rows) == 1, "the game was not persisted"
    assert sandboxed_writes["game_md"].exists(), "GAME-LOG.md was not written"
    assert "tidus" in sandboxed_writes["game_md"].read_text(encoding="utf-8")

    # the write landed in the sandbox, never in the repo's learning/ directory
    assert ROOT not in sandboxed_writes["game_md"].parents
    assert payload["file"] == str(sandboxed_writes["game_md"])


def test_log_rule_refuses_a_citation_it_cannot_back_up(sandboxed_writes, capsys):
    code = cli_module.main(["--json", "log", "rule", "--rule", "999.999", "--note", "nope"])
    out = capsys.readouterr().out
    assert code != 0, "a rule number that is not in the corpus must not be logged"

    assert json.loads(out)["ok"] is False
    assert not sandboxed_writes["rules_md"].exists(), "markdown written for a non-existent rule"


def test_log_rule_writes_a_row_and_quotes_the_rule(sandboxed_writes, capsys):
    code = cli_module.main(
        ["--json", "log", "rule", "--rule", "903.4", "--note", "hybrid pips count as both colours"]
    )
    out = capsys.readouterr().out
    assert code == 0, out

    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["rule"]["rule_number"] == "903.4"

    conn = sqlite3.connect(str(sandboxed_writes["db"]))
    try:
        expected = conn.execute(
            "SELECT text FROM rules WHERE rule_number = '903.4'"
        ).fetchone()[0]
        logged = conn.execute(
            "SELECT COUNT(*) FROM rules_missed WHERE what_i_got_wrong = ?",
            ("hybrid pips count as both colours",),
        ).fetchone()[0]
    finally:
        conn.close()
    assert logged == 1
    assert payload["rule"]["text"] == expected, "the quoted rule text was not verbatim"
    assert sandboxed_writes["rules_md"].exists()


def test_log_rule_normalizes_a_cited_number(sandboxed_writes, capsys):
    code = cli_module.main(["--json", "log", "rule", "--rule", "rule 601.2a.", "--note", "x"])
    out = capsys.readouterr().out
    assert code == 0, out

    assert json.loads(out)["rule"]["rule_number"] == "601.2a"


# --------------------------------------------------------------------- rebuild
def test_rebuild_is_registered_but_never_run_by_the_suite(cli):
    """`rebuild` is the ONLY networked command (C1). We assert the parser, not
    the download."""
    result = cli("rebuild", "--help")
    assert result.returncode == 0
    for loader in ("cards", "rules", "edhrec", "decks"):
        assert loader in result.stdout, f"rebuild --only is missing '{loader}'"
    assert "--force" in result.stdout


def test_rebuild_rejects_an_unknown_loader(cli):
    result = cli("rebuild", "--only", "bogus")
    assert result.returncode != 0
    assert "invalid choice" in result.combined


def test_rebuild_loaders_are_imported_lazily():
    """The loaders are what pull in urllib. Keeping them out of cmd_admin's
    import path is what makes 'no network at query time' verifiable."""
    module = importlib.import_module("cmd_admin")
    source = Path(module.__file__).read_text(encoding="utf-8")
    top_level = [
        line
        for line in source.splitlines()
        if line.startswith("import load_") or line.startswith("from load_")
    ]
    assert not top_level, f"loaders imported at module level in cmd_admin: {top_level}"
