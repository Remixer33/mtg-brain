"""Shared fixtures for the MTG Brain test suite.

Design rules for this suite:

* End-to-end tests shell out to ``bin/mtg`` so we exercise the real entry point
  (and so PYTHONHASHSEED / process-boundary bugs cannot hide).
* Every subprocess runs against a **sandbox copy** of ``data/mtg.sqlite`` made
  with sqlite3's backup API. The copy is byte-faithful real data, but it means a
  test can never corrupt Omar's database or depend on how many games he happened
  to log. The default (real) DB is still exercised explicitly by
  ``test_constraints.py``.
* Only ``pytest`` is used on top of the stdlib — constraint C6 permits pytest as
  a test-only dependency and nothing else.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
BIN = ROOT / "bin" / "mtg"
REAL_DB = Path(os.environ.get("MTG_BRAIN_DB", ROOT / "data" / "mtg.sqlite"))

#: Every subprocess call gets this ceiling. The CLI answers in ~40ms; a command
#: that takes a minute is a hung command, and the suite should say so.
TIMEOUT = 60

DECK_SLUGS = ("tidus", "bumbleflower", "dogmeat")

#: Seeded into the sandbox so the learning-loop read-back commands have a
#: deterministic, non-empty log regardless of the real database's contents.
SEED_GAME = ("2026-01-01T00:00:00+00:00", "tidus", "test opponents", "win", "seeded by the test suite")
SEED_MISS = ("2026-01-01T00:00:00+00:00", "903.4", "seeded by the test suite")


# --------------------------------------------------------------------------- db
@pytest.fixture(scope="session")
def sandbox_db(tmp_path_factory) -> Path:
    """A writable, byte-faithful copy of the real database.

    sqlite3's backup API is used rather than a file copy so any content still
    sitting in the WAL comes along.
    """
    assert REAL_DB.exists(), f"database missing: {REAL_DB} (run 'mtg rebuild')"
    dst = tmp_path_factory.mktemp("mtg-brain-db") / "mtg.sqlite"

    source = sqlite3.connect(f"file:{REAL_DB}?mode=ro", uri=True)
    target = sqlite3.connect(str(dst))
    try:
        with target:
            source.backup(target)
        target.execute("DELETE FROM game_log")
        target.execute("DELETE FROM rules_missed")
        target.execute(
            "INSERT INTO game_log(played_at, deck_id, opponents, result, notes) VALUES (?,?,?,?,?)",
            SEED_GAME,
        )
        target.execute(
            "INSERT INTO rules_missed(logged_at, rule_number, what_i_got_wrong) VALUES (?,?,?)",
            SEED_MISS,
        )
        target.commit()
    finally:
        target.close()
        source.close()
    return dst


@pytest.fixture(scope="session")
def sql(sandbox_db):
    """Direct read-only SQL against the same data the CLI is answering from.

    Tests use this to re-derive the truth independently instead of trusting the
    CLI's own numbers.
    """
    conn = sqlite3.connect(f"file:{sandbox_db}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


# -------------------------------------------------------------------- cli runner
class CliResult:
    """A finished ``bin/mtg`` invocation, with JSON parsing that fails loudly."""

    def __init__(self, argv: list[str], proc: subprocess.CompletedProcess):
        self.argv = argv
        self.returncode = proc.returncode
        self.stdout = proc.stdout
        self.stderr = proc.stderr

    @property
    def combined(self) -> str:
        return self.stdout + self.stderr

    @property
    def label(self) -> str:
        return "mtg " + " ".join(self.argv)

    def json(self):
        try:
            return json.loads(self.stdout)
        except json.JSONDecodeError as exc:  # pragma: no cover - failure path
            raise AssertionError(
                f"{self.label} did not emit valid JSON ({exc})\n"
                f"--- stdout ---\n{self.stdout}\n--- stderr ---\n{self.stderr}"
            ) from None

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<CliResult {self.label!r} rc={self.returncode}>"


def _run(argv, db_path, extra_env=None, timeout=TIMEOUT) -> CliResult:
    env = dict(os.environ)
    env["MTG_BRAIN_DB"] = str(db_path)
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [str(BIN), *argv],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        cwd=str(ROOT),
    )
    return CliResult(list(argv), proc)


@pytest.fixture(scope="session")
def cli(sandbox_db):
    """Run ``bin/mtg`` against the sandbox DB. Returns a CliResult."""

    def run(*argv, env=None, timeout=TIMEOUT, db=None) -> CliResult:
        return _run(list(argv), db or sandbox_db, extra_env=env, timeout=timeout)

    return run


@pytest.fixture(scope="session")
def real_cli():
    """Run ``bin/mtg`` against the real shipped database (read-only commands)."""

    def run(*argv, env=None, timeout=TIMEOUT) -> CliResult:
        return _run(list(argv), REAL_DB, extra_env=env, timeout=timeout)

    return run


# ------------------------------------------------------------------- assertions
def assert_json_ok(result: CliResult, expect_ok=True):
    """Every --json response must parse and carry the 'ok' contract key."""
    payload = result.json()
    assert isinstance(payload, dict), f"{result.label}: JSON root is {type(payload).__name__}, expected object"
    assert "ok" in payload, f"{result.label}: JSON payload has no 'ok' key: {sorted(payload)}"
    if expect_ok is not None:
        assert payload["ok"] is expect_ok, f"{result.label}: ok={payload['ok']}, expected {expect_ok}"
    return payload


def assert_no_traceback(result: CliResult):
    """A crash is never an acceptable answer — not even for hostile input."""
    for needle in ("Traceback (most recent call last)", "OperationalError", "sqlite3."):
        assert needle not in result.combined, (
            f"{result.label}: leaked {needle!r}\n"
            f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
        )


def identity(raw) -> set:
    """color_identity / colors / keywords are JSON arrays stored as TEXT."""
    if not raw:
        return set()
    try:
        value = json.loads(raw)
    except (ValueError, TypeError):
        return set()
    return set(value) if isinstance(value, list) else set()
