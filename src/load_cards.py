"""Scryfall loader — populates cards, cards_fts, card_prints, rulings, rulings_fts.

Source: the Scryfall *bulk data* endpoint (https://api.scryfall.com/bulk-data).
The dated download URI is discovered every run — never hardcoded.

Owned tables (the only ones this module ever deletes from):
    cards, cards_fts, card_prints, rulings, rulings_fts

Zero third-party imports by design (constraint C6). Zero LLM/embedding calls (C1).

Usage:
    python3 src/load_cards.py            # reuse data/raw/*.json if present
    python3 src/load_cards.py --force    # re-download and reload
"""
from __future__ import annotations

import argparse
import gzip
import json
import shutil
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402  (shared helpers live next to this file)

BULK_INDEX_URL = "https://api.scryfall.com/bulk-data"
ORACLE_RAW = db.RAW / "oracle-cards.json"
RULINGS_RAW = db.RAW / "rulings.json"

BATCH = 5000

# The tables this loader owns, in FK-safe delete order (children before parent).
OWNED_TABLES = ("card_prints", "cards_fts", "rulings_fts", "rulings", "cards")


# --------------------------------------------------------------- http helpers
def _request(url: str, accept: str = "*/*") -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": db.USER_AGENT,
            "Accept": accept,
            # Ask for gzip explicitly; _open_body() transparently decodes it.
            "Accept-Encoding": "gzip",
        },
    )


def _fetch_json(url: str):
    """Small JSON GET (used for the bulk-data index)."""
    with urllib.request.urlopen(_request(url, "application/json"), timeout=60) as resp:
        raw = resp.read()
        if (resp.headers.get("Content-Encoding") or "").lower() == "gzip":
            raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def download(url: str, dest: Path, force: bool = False) -> dict:
    """Stream `url` to `dest` in chunks. Reuses a non-empty existing file."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0 and not force:
        return {"path": str(dest), "bytes": dest.stat().st_size, "reused": True}

    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(_request(url), timeout=300) as resp:
        body = resp
        if (resp.headers.get("Content-Encoding") or "").lower() == "gzip":
            body = gzip.GzipFile(fileobj=resp)
        with open(tmp, "wb") as fh:
            shutil.copyfileobj(body, fh, length=1024 * 1024)
    tmp.replace(dest)  # atomic: a partial download is never reused
    return {"path": str(dest), "bytes": dest.stat().st_size, "reused": False}


def discover_bulk_uris() -> dict:
    """Return {'oracle_cards': uri, 'rulings': uri} from the live bulk-data index."""
    payload = _fetch_json(BULK_INDEX_URL)
    wanted = {"oracle_cards": None, "rulings": None}
    for entry in payload.get("data", []):
        if entry.get("type") in wanted:
            wanted[entry["type"]] = entry.get("download_uri")
    missing = [k for k, v in wanted.items() if not v]
    if missing:
        raise RuntimeError(f"bulk-data index missing type(s): {missing}")
    return wanted


# ------------------------------------------------------------- row extraction
def _oracle_text(card: dict) -> str | None:
    """DFC/split cards carry text on faces; join so FTS still finds it."""
    text = card.get("oracle_text")
    if text:
        return text
    faces = card.get("card_faces") or []
    parts = [f.get("oracle_text") for f in faces if f.get("oracle_text")]
    if parts:
        return "\n//\n".join(parts)
    return text  # None or ''


def _image_normal(card: dict) -> str | None:
    uris = card.get("image_uris") or {}
    img = uris.get("normal")
    if img:
        return img
    faces = card.get("card_faces") or []
    if faces:
        face_uris = faces[0].get("image_uris") or {}
        return face_uris.get("normal")
    return None


def _price_usd(card: dict) -> float | None:
    raw = (card.get("prices") or {}).get("usd")
    if raw in (None, ""):
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _as_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def card_row(card: dict) -> tuple:
    faces = card.get("card_faces")
    return (
        card["oracle_id"],
        card["name"],
        card.get("mana_cost"),
        _as_float(card.get("cmc")),
        card.get("type_line"),
        _oracle_text(card),
        json.dumps(card.get("colors", [])),
        json.dumps(card.get("color_identity", [])),
        json.dumps(card.get("keywords", [])),
        card.get("power"),
        card.get("toughness"),
        card.get("loyalty"),
        card.get("rarity"),
        card.get("layout"),
        json.dumps(faces) if faces else None,
        (card.get("legalities") or {}).get("commander"),
        _as_int(card.get("edhrec_rank")),
        _price_usd(card),
        card.get("scryfall_uri"),
        _image_normal(card),
    )


CARD_INSERT = """
INSERT OR REPLACE INTO cards (
    oracle_id, name, mana_cost, cmc, type_line, oracle_text,
    colors, color_identity, keywords, power, toughness, loyalty,
    rarity, layout, card_faces_json, legal_commander, edhrec_rank,
    price_usd, scryfall_uri, image_normal
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""


# ------------------------------------------------------------------ db helpers
def _batched_insert(conn: sqlite3.Connection, sql: str, rows, batch: int = BATCH) -> int:
    """executemany in chunks, committing each chunk so write locks stay short."""
    total = 0
    chunk: list = []
    for row in rows:
        chunk.append(row)
        if len(chunk) >= batch:
            conn.executemany(sql, chunk)
            conn.commit()
            total += len(chunk)
            chunk = []
    if chunk:
        conn.executemany(sql, chunk)
        conn.commit()
        total += len(chunk)
    return total


def _truncate_owned(conn: sqlite3.Connection) -> dict:
    """Delete ONLY our five tables, children first.

    `deck_cards` (owned by the deck loader) also FK-references cards. If it
    already holds rows, enforcement is suspended for the reload window and a
    PRAGMA foreign_key_check is run afterwards to prove nothing was orphaned.
    """
    try:
        deck_rows = conn.execute("SELECT COUNT(*) FROM deck_cards").fetchone()[0]
    except sqlite3.OperationalError:
        deck_rows = 0

    fk_suspended = deck_rows > 0
    if fk_suspended:
        conn.commit()  # PRAGMA foreign_keys is a no-op inside a transaction
        conn.execute("PRAGMA foreign_keys=OFF")

    for table in OWNED_TABLES:
        conn.execute(f"DELETE FROM {table}")
    conn.commit()
    return {"fk_suspended": fk_suspended, "deck_cards_rows": deck_rows}


def _restore_fk(conn: sqlite3.Connection, state: dict) -> list:
    if not state.get("fk_suspended"):
        return []
    conn.commit()
    conn.execute("PRAGMA foreign_keys=ON")
    return [tuple(r) for r in conn.execute("PRAGMA foreign_key_check").fetchall()]


# ------------------------------------------------------------------- main load
def load(conn: sqlite3.Connection, force: bool = False) -> dict:
    """Download (or reuse) the Scryfall bulk files and rebuild the card tables."""
    stats: dict = {"skipped": {}, "downloads": {}}

    db.apply_schema(conn)

    uris = discover_bulk_uris()
    stats["cards_bulk_uri"] = uris["oracle_cards"]
    stats["rulings_bulk_uri"] = uris["rulings"]
    stats["downloads"]["oracle_cards"] = download(uris["oracle_cards"], ORACLE_RAW, force)
    stats["downloads"]["rulings"] = download(uris["rulings"], RULINGS_RAW, force)

    # ---- parse oracle cards -------------------------------------------------
    with open(ORACLE_RAW, "r", encoding="utf-8") as fh:
        oracle_data = json.load(fh)
    stats["oracle_records_in_file"] = len(oracle_data)

    cards_by_oracle: dict[str, tuple] = {}
    fts_by_oracle: dict[str, tuple] = {}
    prints_by_id: dict[str, tuple] = {}
    skipped_no_oracle_id = 0
    skipped_no_name = 0
    duplicate_oracle_ids = 0

    for card in oracle_data:
        oid = card.get("oracle_id")
        if not oid:
            skipped_no_oracle_id += 1
            continue
        if not card.get("name"):
            skipped_no_name += 1
            continue
        if oid in cards_by_oracle:
            duplicate_oracle_ids += 1
        cards_by_oracle[oid] = card_row(card)
        fts_by_oracle[oid] = (
            oid,
            card["name"],
            _oracle_text(card),
            card.get("type_line"),
        )
        print_id = card.get("id")
        if print_id:
            prints_by_id[print_id] = (print_id, oid)

    del oracle_data  # release ~1.5GB before we start writing

    # ---- parse rulings ------------------------------------------------------
    with open(RULINGS_RAW, "r", encoding="utf-8") as fh:
        rulings_data = json.load(fh)
    stats["ruling_records_in_file"] = len(rulings_data)

    ruling_rows: list[tuple] = []
    ruling_fts_rows: list[tuple] = []
    skipped_rulings_no_oracle_id = 0
    for r in rulings_data:
        oid = r.get("oracle_id")
        if not oid:
            skipped_rulings_no_oracle_id += 1
            continue
        ruling_rows.append((oid, r.get("published_at"), r.get("comment"), r.get("source")))
        ruling_fts_rows.append((oid, r.get("comment")))

    del rulings_data

    # ---- rebuild ------------------------------------------------------------
    fk_state = _truncate_owned(conn)

    stats["cards"] = _batched_insert(conn, CARD_INSERT, cards_by_oracle.values())
    stats["cards_fts"] = _batched_insert(
        conn,
        "INSERT INTO cards_fts (oracle_id, name, oracle_text, type_line) VALUES (?,?,?,?)",
        fts_by_oracle.values(),
    )
    stats["card_prints"] = _batched_insert(
        conn,
        "INSERT OR REPLACE INTO card_prints (scryfall_id, oracle_id) VALUES (?,?)",
        prints_by_id.values(),
    )
    stats["rulings"] = _batched_insert(
        conn,
        "INSERT INTO rulings (oracle_id, published_at, comment, source) VALUES (?,?,?,?)",
        ruling_rows,
    )
    stats["rulings_fts"] = _batched_insert(
        conn,
        "INSERT INTO rulings_fts (oracle_id, comment) VALUES (?,?)",
        ruling_fts_rows,
    )

    fk_violations = _restore_fk(conn, fk_state)
    stats["fk_enforcement_suspended"] = fk_state["fk_suspended"]
    stats["fk_violations_after_reload"] = fk_violations

    stats["skipped"] = {
        "cards_missing_oracle_id": skipped_no_oracle_id,
        "cards_missing_name": skipped_no_name,
        "duplicate_oracle_ids_collapsed": duplicate_oracle_ids,
        "rulings_missing_oracle_id": skipped_rulings_no_oracle_id,
    }

    # ---- build_meta ---------------------------------------------------------
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    db.set_meta(conn, "cards_loaded_at", now)
    db.set_meta(conn, "cards_bulk_uri", uris["oracle_cards"])
    db.set_meta(conn, "rulings_bulk_uri", uris["rulings"])
    db.set_meta(conn, "cards_count", str(stats["cards"]))
    db.set_meta(conn, "rulings_count", str(stats["rulings"]))
    stats["cards_loaded_at"] = now

    return stats


# ------------------------------------------------------------------ standalone
def _verify(conn: sqlite3.Connection) -> None:
    q = lambda sql, args=(): conn.execute(sql, args).fetchall()  # noqa: E731
    print("\n--- verification ---")
    for label, sql in (
        ("cards", "SELECT COUNT(*) FROM cards"),
        ("rulings", "SELECT COUNT(*) FROM rulings"),
        ("card_prints", "SELECT COUNT(*) FROM card_prints"),
        ("cards_fts", "SELECT COUNT(*) FROM cards_fts"),
        ("rulings_fts", "SELECT COUNT(*) FROM rulings_fts"),
    ):
        print(f"{label:14} {q(sql)[0][0]}")

    row = q("SELECT name, mana_cost, type_line FROM cards WHERE name='Sol Ring'")
    print("\nSol Ring:", [tuple(r) for r in row])

    hits = q("SELECT COUNT(*) FROM cards_fts WHERE cards_fts MATCH 'lifelink'")[0][0]
    print("cards_fts MATCH 'lifelink':", hits)

    cmds = q(
        "SELECT name, color_identity FROM cards WHERE name IN "
        "(?, ?, ?)",
        ("Tidus, Yuna's Guardian", "Ms. Bumbleflower", "Dogmeat, Ever Loyal"),
    )
    print("commanders:", [tuple(r) for r in cmds])


def main() -> int:
    ap = argparse.ArgumentParser(description="Load Scryfall bulk data into mtg-brain.")
    ap.add_argument("--force", action="store_true", help="re-download raw bulk files")
    ap.add_argument("--db", default=None, help="override DB path")
    args = ap.parse_args()

    conn = db.connect(args.db)
    try:
        stats = load(conn, force=args.force)
        print(json.dumps(stats, indent=2))
        _verify(conn)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
