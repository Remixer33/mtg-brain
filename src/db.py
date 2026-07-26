"""Shared DB helpers. Every loader and CLI command uses THIS module to connect.

Zero third-party imports by design (constraint C6).
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
DB_PATH = Path(os.environ.get("MTG_BRAIN_DB", DATA / "mtg.sqlite"))
SCHEMA_PATH = ROOT / "src" / "schema.sql"

USER_AGENT = "mtg-brain/1.0"


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Open the database with sane pragmas and Row access."""
    path = Path(db_path) if db_path else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    # Parallel loaders share this file; WAL permits one writer at a time, so
    # wait rather than raising SQLITE_BUSY.
    conn.execute("PRAGMA busy_timeout=120000")
    return conn


def apply_schema(conn: sqlite3.Connection) -> None:
    """Idempotently create every table/index/FTS defined in schema.sql."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO build_meta(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None):
    row = conn.execute("SELECT value FROM build_meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default
