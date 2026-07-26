"""MTGJSON precon deck loader — populates decks, deck_cards.

Owned tables (the ONLY tables this module ever writes or truncates):

    decks, deck_cards

`cards` and `card_prints` are read-only here; they are populated by
src/load_cards.py (Scryfall). This loader joins onto them.

Usage:
    python3 src/load_decks.py            # load (reuses cached raw JSON)
    python3 src/load_decks.py --force    # re-download deck JSON, then load
    python3 src/load_decks.py --verify   # re-run the gate queries only

Zero third-party imports by design (constraint C6). Zero LLM/embedding calls
by design (constraint C1).
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import db  # noqa: E402  (shared helpers: connect / apply_schema / set_meta)

# --------------------------------------------------------------------------
# The three precons. VERIFIED — file names are exact, do not "fix" them.
# --------------------------------------------------------------------------
DECKS = (
    # slug,            mtgjson fileName,                  expected commander
    ("tidus", "CounterBlitzFinalFantasyX_FIC", "Tidus, Yuna's Guardian"),
    ("bumbleflower", "PeaceOffering_BLC", "Ms. Bumbleflower"),
    ("dogmeat", "ScrappySurvivors_PIP", "Dogmeat, Ever Loyal"),
)

MTGJSON_DECK_URL = "https://mtgjson.com/api/v5/decks/{file_name}.json"

# Truncate order matters: deck_cards is the FK child of decks.
OWNED_TABLES = ("deck_cards", "decks")

EXPECTED_MAIN_TOTAL = 99
EXPECTED_COMMANDER_TOTAL = 1

# Resolution methods, in the order they are attempted.
METHODS = (
    "scryfall_id",   # 1. identifiers.scryfallId -> card_prints -> oracle_id
    "name_exact",    # 2. exact, case-sensitive cards.name
    "name_nocase",   # 3. cards.name COLLATE NOCASE
    "dfc_front",     # 4a. MTGJSON "Fear"        -> Scryfall "Fear // Loathing"
    "dfc_split",     # 4b. MTGJSON "A // B"      -> Scryfall "A"
)


class UnresolvedCards(RuntimeError):
    """Raised when any deck card cannot be mapped to a cards.oracle_id.

    The Phase 1 gate demands ZERO orphans, so an unresolved card is a hard
    failure — never a silent drop and never an invented oracle_id.
    """


# --------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------
def download_deck(slug: str, file_name: str, force: bool = False) -> dict:
    """Fetch one MTGJSON deck to data/raw/deck_<slug>.json, reusing the cache.

    Reuse keeps rebuilds fast and lets the whole pipeline run offline.
    """
    dest = db.RAW / f"deck_{slug}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and dest.stat().st_size > 0 and not force:
        return {"path": str(dest), "bytes": dest.stat().st_size, "cached": True}

    url = MTGJSON_DECK_URL.format(file_name=file_name)
    req = urllib.request.Request(url, headers={"User-Agent": db.USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = resp.read()

    # Validate before overwriting a good cache file.
    parsed = json.loads(payload)
    if "data" not in parsed:
        raise RuntimeError(f"{url} returned no 'data' key")
    dest.write_bytes(payload)
    return {"path": str(dest), "bytes": len(payload), "cached": False}


def read_deck(slug: str) -> dict:
    return json.loads((db.RAW / f"deck_{slug}.json").read_text(encoding="utf-8"))["data"]


# --------------------------------------------------------------------------
# resolution
# --------------------------------------------------------------------------
def resolve_oracle_id(conn: sqlite3.Connection, card: dict):
    """Map one MTGJSON card object to (oracle_id, method) or (None, None).

    Ordered best-first. `card_prints` currently holds only the oracle-
    representative printing per card, so a set-specific scryfallId often
    misses and name matching carries most of the load — hence the fallbacks.
    """
    name = card.get("name") or ""
    scryfall_id = (card.get("identifiers") or {}).get("scryfallId")

    # 1. scryfallId -> card_prints
    if scryfall_id:
        row = conn.execute(
            "SELECT oracle_id FROM card_prints WHERE scryfall_id = ?", (scryfall_id,)
        ).fetchone()
        if row:
            return row["oracle_id"], "scryfall_id"

    # 2. exact, case-sensitive name
    row = conn.execute("SELECT oracle_id FROM cards WHERE name = ?", (name,)).fetchone()
    if row:
        return row["oracle_id"], "name_exact"

    # 3. case-insensitive name
    row = conn.execute(
        "SELECT oracle_id FROM cards WHERE name = ? COLLATE NOCASE", (name,)
    ).fetchone()
    if row:
        return row["oracle_id"], "name_nocase"

    # 4a. MTGJSON front face only -> Scryfall combined "Front // Back".
    #     LIKE is case-insensitive for ASCII; escape wildcards in the name.
    escaped = name.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    row = conn.execute(
        "SELECT oracle_id FROM cards WHERE name LIKE ? ESCAPE '\\' ORDER BY name LIMIT 1",
        (escaped + " // %",),
    ).fetchone()
    if row:
        return row["oracle_id"], "dfc_front"

    # 4b. MTGJSON combined "A // B" -> Scryfall front face only, or Scryfall
    #     holding a differently-named back ("A // B" vs "A // B-prime").
    if " // " in name:
        front = name.split(" // ")[0]
        row = conn.execute(
            "SELECT oracle_id FROM cards WHERE name = ? COLLATE NOCASE", (front,)
        ).fetchone()
        if row:
            return row["oracle_id"], "dfc_split"
        front_escaped = (
            front.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        row = conn.execute(
            "SELECT oracle_id FROM cards WHERE name LIKE ? ESCAPE '\\' "
            "ORDER BY name LIMIT 1",
            (front_escaped + " // %",),
        ).fetchone()
        if row:
            return row["oracle_id"], "dfc_split"

    return None, None


def resolve_deck(conn: sqlite3.Connection, slug: str, data: dict) -> dict:
    """Resolve every card in one deck. Pure read — writes nothing.

    Returns a fully-resolved plan so that resolution can be validated across
    ALL decks before a single row is written.
    """
    methods: dict[str, int] = {m: 0 for m in METHODS}
    unresolved: list[dict] = []
    # (board, oracle_id) -> count. Basics legitimately appear as several
    # mainBoard entries sharing one oracle_id; the PK is
    # (deck_id, oracle_id, board), so counts must be SUMMED, not inserted twice.
    counts: dict[tuple[str, str], int] = {}

    boards = (("commander", data.get("commander") or []),
              ("main", data.get("mainBoard") or []))

    for board, cards in boards:
        for card in cards:
            oracle_id, method = resolve_oracle_id(conn, card)
            if oracle_id is None:
                unresolved.append({
                    "deck": slug,
                    "board": board,
                    "name": card.get("name"),
                    "scryfall_id": (card.get("identifiers") or {}).get("scryfallId"),
                    "set_code": card.get("setCode"),
                })
                continue
            methods[method] += 1
            key = (board, oracle_id)
            counts[key] = counts.get(key, 0) + int(card.get("count") or 0)

    return {
        "slug": slug,
        "row": (
            slug,
            data.get("name"),
            data.get("code"),
            data.get("releaseDate"),
            ", ".join(c.get("name", "") for c in (data.get("commander") or [])),
            f"{slug}.json",
        ),
        "counts": counts,
        "methods": methods,
        "unresolved": unresolved,
        "main_total": sum(v for (b, _), v in counts.items() if b == "main"),
        "commander_total": sum(v for (b, _), v in counts.items() if b == "commander"),
        "main_rows": sum(1 for (b, _) in counts if b == "main"),
    }


# --------------------------------------------------------------------------
# color identity
# --------------------------------------------------------------------------
def _identity(raw) -> set:
    if not raw:
        return set()
    try:
        return set(json.loads(raw))
    except (TypeError, ValueError):
        return set()


def check_color_identity(conn: sqlite3.Connection) -> list[dict]:
    """Every main-board card's color identity must fit its commander's.

    A legal precon has zero violations; any hit is a real data or resolution
    bug worth surfacing loudly.
    """
    violations = []
    for (deck_id,) in conn.execute("SELECT deck_id FROM decks ORDER BY deck_id").fetchall():
        commander = set()
        for row in conn.execute(
            "SELECT c.color_identity FROM deck_cards dc "
            "JOIN cards c ON c.oracle_id = dc.oracle_id "
            "WHERE dc.deck_id = ? AND dc.board = 'commander'",
            (deck_id,),
        ):
            commander |= _identity(row["color_identity"])

        for row in conn.execute(
            "SELECT c.name, c.color_identity FROM deck_cards dc "
            "JOIN cards c ON c.oracle_id = dc.oracle_id "
            "WHERE dc.deck_id = ? AND dc.board = 'main'",
            (deck_id,),
        ):
            card_ci = _identity(row["color_identity"])
            if not card_ci <= commander:
                violations.append({
                    "deck_id": deck_id,
                    "card": row["name"],
                    "card_identity": sorted(card_ci),
                    "commander_identity": sorted(commander),
                    "illegal_colors": sorted(card_ci - commander),
                })
    return violations


# --------------------------------------------------------------------------
# load
# --------------------------------------------------------------------------
def _truncate_owned(conn: sqlite3.Connection) -> dict:
    """Delete ONLY this module's tables, child-first. Never touches cards."""
    deleted = {}
    for table in OWNED_TABLES:
        cur = conn.execute(f"DELETE FROM {table}")
        deleted[table] = cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0
    conn.commit()
    return deleted


def load(conn: sqlite3.Connection, force: bool = False) -> dict:
    """Load the three precon decks into decks + deck_cards.

    Raises UnresolvedCards if ANY card fails to map to an oracle_id — the
    Phase 1 gate requires zero orphans, so a partial load is worse than none.
    """
    db.apply_schema(conn)

    stats: dict = {
        "downloads": {},
        "decks": {},
        "resolution_methods": {m: 0 for m in METHODS},
        "unresolved": [],
    }

    # ---- Phase A: fetch + resolve everything BEFORE writing anything, so a
    # resolution failure can never leave a half-populated deck behind.
    plans = []
    for slug, file_name, expected_commander in DECKS:
        stats["downloads"][slug] = download_deck(slug, file_name, force=force)
        data = read_deck(slug)

        commanders = [c.get("name") for c in (data.get("commander") or [])]
        if expected_commander not in commanders:
            raise RuntimeError(
                f"{slug}: expected commander {expected_commander!r}, got {commanders!r}"
            )

        plan = resolve_deck(conn, slug, data)
        plan["source_file"] = f"{file_name}.json"
        plan["row"] = plan["row"][:5] + (f"{file_name}.json",)
        plans.append(plan)

        stats["unresolved"].extend(plan["unresolved"])
        for method, n in plan["methods"].items():
            stats["resolution_methods"][method] += n

    if stats["unresolved"]:
        lines = "\n".join(
            f"  - [{u['deck']}/{u['board']}] {u['name']!r} "
            f"(scryfallId={u['scryfall_id']}, set={u['set_code']})"
            for u in stats["unresolved"]
        )
        raise UnresolvedCards(
            f"{len(stats['unresolved'])} deck card(s) could not be resolved to an "
            f"oracle_id — refusing to load (zero-orphan gate):\n{lines}"
        )

    # ---- Phase B: write. Small payload (~288 rows), so one short transaction.
    stats["truncated"] = _truncate_owned(conn)

    deck_rows = [p["row"] for p in plans]
    card_rows = [
        (p["slug"], oracle_id, count, board)
        for p in plans
        for (board, oracle_id), count in p["counts"].items()
    ]

    conn.executemany(
        "INSERT INTO decks (deck_id, name, set_code, release_date, commander_name, "
        "source_file) VALUES (?,?,?,?,?,?)",
        deck_rows,
    )
    conn.executemany(
        "INSERT INTO deck_cards (deck_id, oracle_id, count, board) VALUES (?,?,?,?)",
        card_rows,
    )
    conn.commit()

    stats["deck_rows"] = len(deck_rows)
    stats["deck_card_rows"] = len(card_rows)

    # ---- Phase C: assert the gate against what is actually ON DISK.
    for p in plans:
        slug = p["slug"]
        main_total = conn.execute(
            "SELECT COALESCE(SUM(count),0) FROM deck_cards WHERE deck_id=? AND board='main'",
            (slug,),
        ).fetchone()[0]
        cmd_total = conn.execute(
            "SELECT COALESCE(SUM(count),0) FROM deck_cards WHERE deck_id=? AND board='commander'",
            (slug,),
        ).fetchone()[0]
        stats["decks"][slug] = {
            "main_total": main_total,
            "commander_total": cmd_total,
            "main_rows": p["main_rows"],
            "methods": p["methods"],
        }
        if main_total != EXPECTED_MAIN_TOTAL:
            raise RuntimeError(
                f"{slug}: mainBoard sums to {main_total}, expected {EXPECTED_MAIN_TOTAL}"
            )
        if cmd_total != EXPECTED_COMMANDER_TOTAL:
            raise RuntimeError(
                f"{slug}: commander sums to {cmd_total}, expected {EXPECTED_COMMANDER_TOTAL}"
            )

    orphans = conn.execute(
        "SELECT COUNT(*) FROM deck_cards dc "
        "LEFT JOIN cards c ON c.oracle_id = dc.oracle_id WHERE c.oracle_id IS NULL"
    ).fetchone()[0]
    stats["orphans"] = orphans
    if orphans:
        raise RuntimeError(f"{orphans} orphan deck_cards row(s) — zero-orphan gate FAILED")

    stats["color_identity_violations"] = check_color_identity(conn)

    # ---- build_meta
    db.set_meta(conn, "decks_loaded_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    for slug, info in stats["decks"].items():
        db.set_meta(conn, f"{slug}_main_total", str(info["main_total"]))

    return stats


# --------------------------------------------------------------------------
# verification (the Phase 1 gate, printed)
# --------------------------------------------------------------------------
def verify(conn: sqlite3.Connection) -> dict:
    out: dict = {}
    print("\n=== decks ===")
    rows = conn.execute(
        "SELECT deck_id, name, commander_name, set_code, release_date FROM decks "
        "ORDER BY deck_id"
    ).fetchall()
    for r in rows:
        print(f"  {r['deck_id']:<14} | {r['name']:<32} | {r['commander_name']:<24} "
              f"| {r['set_code']} | {r['release_date']}")
    out["decks"] = [dict(r) for r in rows]

    print("\n=== main board totals (MUST be 99) ===")
    main = conn.execute(
        "SELECT deck_id, SUM(count) AS total FROM deck_cards WHERE board='main' "
        "GROUP BY deck_id ORDER BY deck_id"
    ).fetchall()
    for r in main:
        print(f"  {r['deck_id']:<14} {r['total']:>4}   {'OK' if r['total'] == 99 else 'FAIL'}")
    out["main_totals"] = {r["deck_id"]: r["total"] for r in main}

    print("\n=== commander totals (MUST be 1) ===")
    cmd = conn.execute(
        "SELECT deck_id, SUM(count) AS total FROM deck_cards WHERE board='commander' "
        "GROUP BY deck_id ORDER BY deck_id"
    ).fetchall()
    for r in cmd:
        print(f"  {r['deck_id']:<14} {r['total']:>4}   {'OK' if r['total'] == 1 else 'FAIL'}")
    out["commander_totals"] = {r["deck_id"]: r["total"] for r in cmd}

    orphans = conn.execute(
        "SELECT COUNT(*) FROM deck_cards dc "
        "LEFT JOIN cards c ON c.oracle_id = dc.oracle_id WHERE c.oracle_id IS NULL"
    ).fetchone()[0]
    print(f"\n=== orphans (MUST be 0) === {orphans}   {'OK' if orphans == 0 else 'FAIL'}")
    out["orphans"] = orphans

    violations = check_color_identity(conn)
    print(f"\n=== color-identity violations (MUST be 0) === {len(violations)}")
    for v in violations:
        print(f"  {v['deck_id']}: {v['card']} {v['card_identity']} "
              f"illegal={v['illegal_colors']} vs commander {v['commander_identity']}")
    out["color_identity_violations"] = violations

    ok = (all(t == 99 for t in out["main_totals"].values())
          and all(t == 1 for t in out["commander_totals"].values())
          and len(out["main_totals"]) == 3
          and orphans == 0
          and not violations)
    out["gate_pass"] = ok
    print(f"\n=== GATE: {'PASS' if ok else 'FAIL'} ===")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Load MTGJSON precon decks into MTG Brain.")
    ap.add_argument("--force", action="store_true", help="re-download the deck JSON files")
    ap.add_argument("--verify", action="store_true", help="only run the gate queries")
    ap.add_argument("--json", action="store_true", help="emit stats as JSON")
    args = ap.parse_args(argv)

    conn = db.connect()
    try:
        if args.verify:
            result = verify(conn)
            return 0 if result["gate_pass"] else 1

        stats = load(conn, force=args.force)

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("resolution methods:", stats["resolution_methods"])
            print("deck rows:", stats["deck_rows"], "| deck_card rows:", stats["deck_card_rows"])

        result = verify(conn)
        return 0 if result["gate_pass"] else 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
