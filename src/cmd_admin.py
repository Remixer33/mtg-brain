"""Admin + learning-loop commands.

    mtg rebuild [--only cards|rules|edhrec|decks] [--force]
    mtg log game --deck <slug> --result <win|loss|draw> [--opponents T] [--notes T]
    mtg log game --list [--deck slug] [--limit N]
    mtg log rule --rule <number> --note "<what I got wrong>"
    mtg log rule --list
    mtg status

`rebuild` is the ONLY command in the whole CLI permitted to touch the network
(constraint C1). It orchestrates the four existing loaders — it never
re-implements them — in the one order that is safe:

    apply_schema -> cards -> rules -> edhrec -> decks

`deck_cards.oracle_id` is a foreign key into `cards`, so cards must exist before
decks are written, and the card loader is the one that knows how to suspend FK
enforcement while it truncates and reloads.

Zero third-party imports by design (constraint C6). Commander/EDH only (C3).
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import db  # noqa: E402  shared connect/apply_schema/get_meta
import output  # noqa: E402  emit/fail/rule/wrap

# --------------------------------------------------------------------------- paths
LEARNING_DIR = db.ROOT / "learning"
GAME_LOG_MD = LEARNING_DIR / "GAME-LOG.md"
RULES_MISSED_MD = LEARNING_DIR / "RULES-I-KEEP-MISSING.md"
BRACKETS_PATH = db.DATA / "brackets.json"

# --------------------------------------------------------------------------- rebuild
#: The only safe order. cards MUST precede decks (FK), rules/edhrec are
#: independent but are run in the middle so a slow card load fails fast.
STEP_ORDER = ("cards", "rules", "edhrec", "decks")

RESULTS = ("win", "loss", "draw")

#: FTS5 keeps four/five shadow tables per virtual table; `mtg status` hides them.
_SHADOW_SUFFIXES = ("_data", "_idx", "_content", "_docsize", "_config")

#: Omar's own learning-loop tables. Empty is the correct initial state for these,
#: so they never count as a degraded build.
LEARNING_TABLES = ("game_log", "rules_missed")


# --------------------------------------------------------------------------- helpers
def utc_now() -> str:
    """UTC ISO-8601, second precision. Every timestamp this module writes."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _pretty_ts(iso: str | None) -> str:
    """'2026-07-26T16:20:11+00:00' -> '2026-07-26 16:20 UTC' for humans."""
    if not iso:
        return "—"
    try:
        moment = datetime.fromisoformat(iso)
    except ValueError:
        return iso
    if moment.tzinfo is not None:
        moment = moment.astimezone(timezone.utc)
    return moment.strftime("%Y-%m-%d %H:%M UTC")


def _human_bytes(n: int | None) -> str:
    if n is None:
        return "—"
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{int(size)} B" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def _as_json(args) -> bool:
    return bool(getattr(args, "json", False))


def _usage_error(message: str, as_json: bool) -> int:
    """A wrong-invocation error. Distinct from output.fail(), which means the
    data does not exist — mixing the two would teach agents to guess."""
    if as_json:
        print(json.dumps({"ok": False, "error": message}, indent=2, ensure_ascii=False))
    else:
        print(f"error: {message}", file=sys.stderr)
    return 2


def _real_tables(conn: sqlite3.Connection) -> list[str]:
    """Every user table, minus SQLite internals and FTS5 shadow tables."""
    names = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    known = set(names)
    keep = []
    for name in names:
        shadow = any(
            name.endswith(suf) and name[: -len(suf)] in known for suf in _SHADOW_SUFFIXES
        )
        if not shadow:
            keep.append(name)
    return keep


def _row_counts(conn: sqlite3.Connection) -> dict:
    counts = {}
    for table in _real_tables(conn):
        try:
            counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        except sqlite3.DatabaseError as exc:  # a corrupt FTS index must not hide the rest
            counts[table] = f"error: {exc}"
    return counts


# Public alias: `mtg dashboard --build` reports the same table inventory that
# `mtg status` prints, from the same query.
table_counts = _row_counts


def _loader(name: str):
    """Import a loader lazily. Loaders pull in urllib; keeping them out of the
    import path of every other command is what makes 'zero network at query
    time' verifiable, not just intended."""
    if name == "cards":
        import load_cards

        return load_cards.load
    if name == "rules":
        import load_rules

        return load_rules.load
    if name == "edhrec":
        import load_edhrec

        return load_edhrec.load
    if name == "decks":
        import load_decks

        return load_decks.load
    raise ValueError(f"unknown loader {name!r}")


def _summarize(name: str, stats: dict) -> str:
    """One dense line per loader for the text summary table."""
    g = stats.get
    if name == "cards":
        downloads = stats.get("downloads") or {}
        reused = sum(1 for d in downloads.values() if isinstance(d, dict) and d.get("reused"))
        return (
            f"cards={g('cards')} fts={g('cards_fts')} prints={g('card_prints')} "
            f"rulings={g('rulings')} raw_files_reused={reused}/{len(downloads)}"
        )
    if name == "rules":
        return (
            f"rules={g('rules_count')} glossary={g('glossary_count')} "
            f"sections={g('sections')} effective={g('effective_date')}"
        )
    if name == "edhrec":
        return (
            f"edhrec_rows={g('edhrec_rows')} downloaded={g('edhrec_downloaded')} "
            f"game_changers={g('game_changers')}"
        )
    if name == "decks":
        return (
            f"decks={g('deck_rows')} deck_cards={g('deck_card_rows')} "
            f"orphans={g('orphans')} ci_violations="
            f"{len(stats.get('color_identity_violations') or [])}"
        )
    return ""


def cmd_rebuild(args) -> int:
    as_json = _as_json(args)
    only = getattr(args, "only", None)
    force = bool(getattr(args, "force", False))
    steps = [only] if only else list(STEP_ORDER)

    conn = db.connect()
    try:
        # Schema first: every loader calls apply_schema too, but doing it here
        # means `--only decks` on a fresh file still has tables to check.
        db.apply_schema(conn)

        if "decks" in steps and "cards" not in steps:
            have_cards = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
            if not have_cards:
                return output.fail(
                    "cards — the cards table is empty, so decks cannot load "
                    "(deck_cards.oracle_id is a foreign key into cards). "
                    "Run 'mtg rebuild --only cards' first, or plain 'mtg rebuild'.",
                    as_json,
                )

        done: list[dict] = []
        started = time.perf_counter()
        failure = None

        for name in steps:
            t0 = time.perf_counter()
            try:
                stats = _loader(name)(conn, force=force)
            except Exception as exc:  # noqa: BLE001 — reported, then we stop
                elapsed = round(time.perf_counter() - t0, 2)
                done.append(
                    {
                        "name": name,
                        "ok": False,
                        "seconds": elapsed,
                        "error": f"{type(exc).__name__}: {exc}",
                        "stats": {},
                    }
                )
                failure = f"{name} failed after {elapsed}s — {type(exc).__name__}: {exc}"
                break
            done.append(
                {
                    "name": name,
                    "ok": True,
                    "seconds": round(time.perf_counter() - t0, 2),
                    "stats": stats,
                }
            )

        total_seconds = round(time.perf_counter() - started, 2)
        totals = _row_counts(conn)
        if failure is None:
            db.set_meta(conn, "last_rebuild_at", utc_now())

        payload = {
            "ok": failure is None,
            "forced": force,
            "only": only,
            "db": str(db.DB_PATH),
            "steps": done,
            "totals": totals,
            "total_seconds": total_seconds,
        }
        if failure:
            payload["error"] = failure

        lines = [output.rule("rebuild"), ""]
        lines.append(f"{'step':<10} {'seconds':>9}  detail")
        lines.append(f"{'-' * 10} {'-' * 9}  {'-' * 46}")
        for step in done:
            detail = (
                _summarize(step["name"], step["stats"])
                if step["ok"]
                else f"FAILED — {step['error']}"
            )
            lines.append(f"{step['name']:<10} {step['seconds']:>9.2f}  {detail}")
        lines.append(f"{'TOTAL':<10} {total_seconds:>9.2f}")
        lines.append("")
        lines.append(output.rule("row counts"))
        for table, count in totals.items():
            lines.append(f"  {table:<16} {count:>8}")
        lines.append("")
        lines.append(f"  database   {db.DB_PATH}")
        lines.append(f"  size       {_human_bytes(_db_bytes())}")
        lines.append(f"  mode       {'--force (re-downloaded)' if force else 'cached raw files reused'}")
        if failure:
            lines.append("")
            lines.append(f"  REBUILD FAILED: {failure}")

        code = output.emit(payload, "\n".join(lines), as_json)
        return code if failure is None else 1
    finally:
        conn.close()


def _db_bytes() -> int | None:
    try:
        return db.DB_PATH.stat().st_size
    except OSError:
        return None


# --------------------------------------------------------------------------- log game
def _deck_row(conn: sqlite3.Connection, slug: str):
    return conn.execute(
        "SELECT deck_id, name, commander_name FROM decks WHERE deck_id = ? COLLATE NOCASE",
        (slug,),
    ).fetchone()


def _known_decks(conn: sqlite3.Connection) -> list[str]:
    return [r[0] for r in conn.execute("SELECT deck_id FROM decks ORDER BY deck_id")]


def _game_dict(row: sqlite3.Row, commander: str | None = None) -> dict:
    data = {
        "id": row["id"],
        "played_at": row["played_at"],
        "deck_id": row["deck_id"],
        "result": row["result"],
        "opponents": row["opponents"],
        "notes": row["notes"],
    }
    if commander is not None:
        data["commander"] = commander
    return data


def _game_entry_md(conn: sqlite3.Connection, game: dict) -> str:
    deck = _deck_row(conn, game["deck_id"])
    deck_name = deck["name"] if deck else game["deck_id"]
    commander = deck["commander_name"] if deck else "—"
    return "\n".join(
        [
            f"### {_pretty_ts(game['played_at'])} — {game['deck_id']} — "
            f"{(game['result'] or '').upper()}",
            f"- **Deck:** {deck_name} (`{game['deck_id']}`) — commander: {commander}",
            f"- **Result:** {game['result']}",
            f"- **Opponents:** {game['opponents'] or '—'}",
            f"- **Notes:** {game['notes'] or '—'}",
            f"- **Log id:** {game['id']}",
        ]
    )


GAME_LOG_HEADER = """# Game Log

Commander games logged with `mtg log game`. Newest first.

Written by the MTG Brain CLI: each new game is inserted directly under the
`## Games` heading, so anything you add by hand elsewhere in this file survives.
The database (`game_log`) is the source of truth — delete this file and the next
`mtg log game` rebuilds it in full.

## Games
"""


def _render_game_log_md(conn: sqlite3.Connection) -> str:
    """Full file, rebuilt from the database. Used when the file is missing or
    someone removed the '## Games' heading this command writes under."""
    rows = conn.execute(
        "SELECT id, played_at, deck_id, opponents, result, notes FROM game_log "
        "ORDER BY played_at DESC, id DESC"
    ).fetchall()
    body = [GAME_LOG_HEADER]
    if not rows:
        body.append("_No games logged yet._\n")
    for row in rows:
        body.append(_game_entry_md(conn, _game_dict(row)) + "\n")
    return "\n".join(body)


def _insert_under_heading(path: Path, heading: str, entry: str, fallback: str) -> str:
    """Insert `entry` immediately under `heading`; rebuild the whole file from
    the database if the heading is gone. Returns inserted|created|rebuilt."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    if existed:
        lines = path.read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(lines):
            if line.strip() == heading:
                tail = lines[i + 1:]
                while tail and not tail[0].strip():
                    tail.pop(0)
                merged = lines[: i + 1] + ["", entry.rstrip("\n"), ""] + tail
                path.write_text("\n".join(merged), encoding="utf-8")
                return "inserted"
    path.write_text(fallback, encoding="utf-8")
    return "rebuilt" if existed else "created"


def cmd_log_game(args) -> int:
    as_json = _as_json(args)
    conn = db.connect()
    try:
        if getattr(args, "list", False):
            return _list_games(conn, args, as_json)

        if not args.deck or not args.result:
            return _usage_error(
                "mtg log game needs --deck <slug> and --result <win|loss|draw> "
                "(or --list to read the log back)",
                as_json,
            )

        deck = _deck_row(conn, args.deck)
        if deck is None:
            known = _known_decks(conn)
            return output.fail(
                f"deck {args.deck!r}"
                + (f" — known decks: {', '.join(known)}" if known else ""),
                as_json,
            )

        played_at = utc_now()
        cur = conn.execute(
            "INSERT INTO game_log(played_at, deck_id, opponents, result, notes) "
            "VALUES (?,?,?,?,?)",
            (played_at, deck["deck_id"], args.opponents or "", args.result, args.notes or ""),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, played_at, deck_id, opponents, result, notes FROM game_log WHERE id=?",
            (cur.lastrowid,),
        ).fetchone()
        game = _game_dict(row, commander=deck["commander_name"])

        written = _insert_under_heading(
            GAME_LOG_MD,
            "## Games",
            _game_entry_md(conn, game),
            _render_game_log_md(conn),
        )

        total = conn.execute("SELECT COUNT(*) FROM game_log").fetchone()[0]
        payload = {
            "ok": True,
            "logged": game,
            "file": str(GAME_LOG_MD),
            "file_action": written,
            "total_games": total,
        }
        text = "\n".join(
            [
                output.rule("game logged"),
                f"  #{game['id']}  {_pretty_ts(game['played_at'])}",
                f"  deck       {deck['name']} ({game['deck_id']}) — {deck['commander_name']}",
                f"  result     {(game['result'] or '').upper()}",
                f"  opponents  {game['opponents'] or '—'}",
                f"  notes      {game['notes'] or '—'}",
                "",
                f"  {written} {GAME_LOG_MD}   ({total} game(s) on record)",
            ]
        )
        return output.emit(payload, text, as_json)
    finally:
        conn.close()


def _list_games(conn: sqlite3.Connection, args, as_json: bool) -> int:
    limit = getattr(args, "limit", None)
    limit = 20 if limit is None else int(limit)
    if limit < 1:
        # SQLite reads a negative LIMIT as "no limit" and 0 as "no rows", either
        # of which would masquerade as an empty log. (`or 20` would swallow 0.)
        return _usage_error("--limit must be 1 or more", as_json)
    sql = "SELECT id, played_at, deck_id, opponents, result, notes FROM game_log"
    params: list = []
    if getattr(args, "deck", None):
        deck = _deck_row(conn, args.deck)
        if deck is None:
            known = _known_decks(conn)
            return output.fail(
                f"deck {args.deck!r}"
                + (f" — known decks: {', '.join(known)}" if known else ""),
                as_json,
            )
        sql += " WHERE deck_id = ?"
        params.append(deck["deck_id"])
    sql += " ORDER BY played_at DESC, id DESC LIMIT ?"
    params.append(int(limit))

    rows = [_game_dict(r) for r in conn.execute(sql, params)]
    if not rows:
        scope = f" for deck {args.deck!r}" if getattr(args, "deck", None) else ""
        return output.fail(f"game_log is empty{scope} — nothing logged yet", as_json)

    tally = {"win": 0, "loss": 0, "draw": 0}
    for row in rows:
        if row["result"] in tally:
            tally[row["result"]] += 1

    payload = {
        "ok": True,
        "count": len(rows),
        "deck": getattr(args, "deck", None),
        "limit": int(limit),
        "record": tally,
        "games": rows,
    }
    lines = [
        output.rule(
            f"games ({len(rows)} shown — {tally['win']}W/{tally['loss']}L/{tally['draw']}D)"
        ),
        "",
    ]
    for row in rows:
        lines.append(
            f"  #{row['id']:<4} {_pretty_ts(row['played_at']):<20} "
            f"{row['deck_id']:<14} {(row['result'] or '').upper():<5} "
            f"vs {row['opponents'] or '—'}"
        )
        if row["notes"]:
            lines.append(output.wrap(row["notes"], width=66, indent="        "))
    return output.emit(payload, "\n".join(lines), as_json)


# --------------------------------------------------------------------------- log rule
def _normalize_rule_number(raw: str) -> str:
    """'rule 601.2a' / 'CR 601.2a' / '601.2a.' -> '601.2a'."""
    text = (raw or "").strip()
    text = re.sub(r"^(?:cr|rule)\s+", "", text, flags=re.IGNORECASE)
    return text.strip().rstrip(".")


def _rule_row(conn: sqlite3.Connection, number: str):
    return conn.execute(
        "SELECT rule_number, section, parent_number, text FROM rules WHERE rule_number = ?",
        (number,),
    ).fetchone()


RULES_MD_HEADER = """# Rules I Keep Missing

Study file for MTG Brain — Commander only. Every entry comes from
`mtg log rule`, and every rule quotation is pulled verbatim from the
Comprehensive Rules stored in the local database. Nothing here is typed from
memory.

**This file is regenerated in full from the `rules_missed` table on every
write** (that is how the "Most missed" table below stays honest), so keep your
notes in the log itself: `mtg log rule --rule 903.4 --note "..."`.
"""


def _md_cell(text: str, width: int = 110) -> str:
    """Squash a rule's text onto one markdown table line."""
    flat = " ".join((text or "").split()).replace("|", "\\|")
    return flat if len(flat) <= width else flat[: width - 1].rstrip() + "…"


def _render_rules_md(conn: sqlite3.Connection) -> str:
    grouped = _grouped_misses(conn)
    effective = db.get_meta(conn, "rules_effective_date")
    source = db.get_meta(conn, "rules_source_uri", "")

    out = [RULES_MD_HEADER]
    out.append(
        f"_Rules corpus: Comprehensive Rules effective {effective or 'unknown'}"
        + (f" — {source}_" if source else "_")
    )
    out.append("")
    out.append("## Most missed")
    out.append("")
    if grouped:
        out.append("| Misses | Rule | Last missed | Rule text |")
        out.append("|---:|---|---|---|")
        for entry in grouped:
            out.append(
                f"| {entry['misses']} | `{entry['rule_number']}` | "
                f"{_pretty_ts(entry['last_logged_at'])} | {_md_cell(entry['rule_text'])} |"
            )
    else:
        out.append("_Nothing logged yet._")
    out.append("")
    out.append("## Log")
    out.append("")

    rows = conn.execute(
        "SELECT id, logged_at, rule_number, what_i_got_wrong FROM rules_missed "
        "ORDER BY logged_at DESC, id DESC"
    ).fetchall()
    if not rows:
        out.append("_Nothing logged yet._")
        out.append("")
    for row in rows:
        out.append(_rule_entry_md(conn, dict(row)))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def _rule_entry_md(conn: sqlite3.Connection, entry: dict) -> str:
    rule = _rule_row(conn, entry["rule_number"])
    text = rule["text"] if rule else ""
    parent = rule["parent_number"] if rule else None
    quoted = "\n".join(f"> {line}" for line in output.wrap(text, width=88).split("\n"))
    head = f"### {_pretty_ts(entry['logged_at'])} — rule {entry['rule_number']}"
    meta = f"**CR {entry['rule_number']}**" + (f" (parent {parent})" if parent else "")
    return "\n".join(
        [
            head,
            f"**What I got wrong:** {entry['what_i_got_wrong']}",
            "",
            meta + ":",
            quoted if text else "> _rule text unavailable_",
        ]
    )


def _grouped_misses(conn: sqlite3.Connection) -> list[dict]:
    """Rule numbers by miss count, most-missed first, with the real rule text."""
    rows = conn.execute(
        "SELECT rule_number, COUNT(*) AS misses, MAX(logged_at) AS last_logged_at "
        "FROM rules_missed GROUP BY rule_number "
        "ORDER BY misses DESC, last_logged_at DESC, rule_number"
    ).fetchall()
    grouped = []
    for row in rows:
        rule = _rule_row(conn, row["rule_number"])
        entries = [
            dict(e)
            for e in conn.execute(
                "SELECT id, logged_at, what_i_got_wrong FROM rules_missed "
                "WHERE rule_number = ? ORDER BY logged_at DESC, id DESC",
                (row["rule_number"],),
            )
        ]
        grouped.append(
            {
                "rule_number": row["rule_number"],
                "misses": row["misses"],
                "last_logged_at": row["last_logged_at"],
                "rule_text": rule["text"] if rule else None,
                "in_rules_table": rule is not None,
                "entries": entries,
            }
        )
    return grouped


def cmd_log_rule(args) -> int:
    as_json = _as_json(args)
    conn = db.connect()
    try:
        if getattr(args, "list", False):
            return _list_rule_misses(conn, as_json)

        if not args.rule or not args.note:
            return _usage_error(
                'mtg log rule needs --rule <number> and --note "<what I got wrong>" '
                "(or --list to read the log back)",
                as_json,
            )

        number = _normalize_rule_number(args.rule)
        rule = _rule_row(conn, number)
        if rule is None:
            # Never log a citation the rules corpus cannot back up.
            return output.fail(f"rule {number}", as_json)

        logged_at = utc_now()
        cur = conn.execute(
            "INSERT INTO rules_missed(logged_at, rule_number, what_i_got_wrong) "
            "VALUES (?,?,?)",
            (logged_at, rule["rule_number"], args.note),
        )
        conn.commit()

        entry = {
            "id": cur.lastrowid,
            "logged_at": logged_at,
            "rule_number": rule["rule_number"],
            "what_i_got_wrong": args.note,
        }
        RULES_MISSED_MD.parent.mkdir(parents=True, exist_ok=True)
        existed = RULES_MISSED_MD.exists()
        RULES_MISSED_MD.write_text(_render_rules_md(conn), encoding="utf-8")

        misses = conn.execute(
            "SELECT COUNT(*) FROM rules_missed WHERE rule_number = ?", (rule["rule_number"],)
        ).fetchone()[0]

        payload = {
            "ok": True,
            "logged": entry,
            "rule": {
                "rule_number": rule["rule_number"],
                "section": rule["section"],
                "parent_number": rule["parent_number"],
                "text": rule["text"],
            },
            "misses_for_this_rule": misses,
            "file": str(RULES_MISSED_MD),
            "file_action": "updated" if existed else "created",
        }
        text = "\n".join(
            [
                output.rule(f"rule {rule['rule_number']} logged (miss #{misses})"),
                f"  when       {_pretty_ts(logged_at)}",
                f"  got wrong  {args.note}",
                "",
                f"  CR {rule['rule_number']}"
                + (f"  (parent {rule['parent_number']})" if rule["parent_number"] else ""),
                output.wrap(rule["text"], width=68, indent="    "),
                "",
                f"  {'updated' if existed else 'created'} {RULES_MISSED_MD}",
            ]
        )
        return output.emit(payload, text, as_json)
    finally:
        conn.close()


def _list_rule_misses(conn: sqlite3.Connection, as_json: bool) -> int:
    grouped = _grouped_misses(conn)
    if not grouped:
        return output.fail("rules_missed is empty — nothing logged yet", as_json)

    total = sum(g["misses"] for g in grouped)
    payload = {
        "ok": True,
        "rules": len(grouped),
        "total_misses": total,
        "most_missed": grouped,
    }
    lines = [output.rule(f"rules I keep missing ({len(grouped)} rules, {total} misses)"), ""]
    for entry in grouped:
        lines.append(f"  {entry['misses']}x  CR {entry['rule_number']}")
        if entry["rule_text"]:
            lines.append(output.wrap(entry["rule_text"], width=66, indent="      "))
        for miss in entry["entries"]:
            lines.append(f"      • [{_pretty_ts(miss['logged_at'])}] {miss['what_i_got_wrong']}")
        lines.append("")
    return output.emit(payload, "\n".join(lines).rstrip(), as_json)


# --------------------------------------------------------------------------- status
META_TIMESTAMPS = (
    ("cards", "cards_loaded_at"),
    ("rules", "rules_loaded_at"),
    ("edhrec", "edhrec_loaded_at"),
    ("decks", "decks_loaded_at"),
    ("last_rebuild", "last_rebuild_at"),
)


def cmd_status(args) -> int:
    as_json = _as_json(args)
    db_path = db.DB_PATH
    if not db_path.exists():
        return output.fail(
            f"database {db_path} — run 'mtg rebuild' to build it", as_json
        )

    conn = db.connect()
    try:
        counts = _row_counts(conn)
        meta = {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM build_meta")}
        loaded_at = {label: meta.get(key) for label, key in META_TIMESTAMPS}

        decks = []
        for row in conn.execute(
            "SELECT deck_id, name, set_code, release_date, commander_name FROM decks "
            "ORDER BY deck_id"
        ):
            deck = dict(row)
            deck["main_total"] = conn.execute(
                "SELECT COALESCE(SUM(count),0) FROM deck_cards WHERE deck_id=? AND board='main'",
                (row["deck_id"],),
            ).fetchone()[0]
            deck["commander_total"] = conn.execute(
                "SELECT COALESCE(SUM(count),0) FROM deck_cards "
                "WHERE deck_id=? AND board='commander'",
                (row["deck_id"],),
            ).fetchone()[0]
            decks.append(deck)

        brackets = {"path": str(BRACKETS_PATH), "exists": BRACKETS_PATH.exists()}
        if brackets["exists"]:
            brackets["bytes"] = BRACKETS_PATH.stat().st_size
            try:
                doc = json.loads(BRACKETS_PATH.read_text(encoding="utf-8"))
                brackets["game_changers"] = len(doc.get("game_changers") or [])
                brackets["brackets"] = sorted((doc.get("brackets") or {}).keys())
                brackets["fetched_at"] = doc.get("fetched_at")
            except (ValueError, OSError) as exc:
                brackets["error"] = str(exc)

        learning = {
            name: {"path": str(path), "exists": path.exists(),
                   "bytes": path.stat().st_size if path.exists() else 0}
            for name, path in (("game_log_md", GAME_LOG_MD),
                               ("rules_missed_md", RULES_MISSED_MD))
        }

        raw_cache = {}
        if db.RAW.exists():
            for item in sorted(db.RAW.iterdir()):
                if item.is_file():
                    raw_cache[item.name] = item.stat().st_size
                elif item.is_dir():
                    raw_cache[item.name + "/"] = sum(
                        f.stat().st_size for f in item.iterdir() if f.is_file()
                    )

        size = db_path.stat().st_size
        empty = [t for t, n in counts.items()
                 if isinstance(n, int) and n == 0 and t not in LEARNING_TABLES]
        payload = {
            "ok": not empty,
            "database": {
                "path": str(db_path),
                "bytes": size,
                "human": _human_bytes(size),
                "offline": True,
            },
            "tables": counts,
            "loaded_at": loaded_at,
            "build_meta": meta,
            "decks": decks,
            "brackets": brackets,
            "learning_files": learning,
            "raw_cache": raw_cache,
            "empty_tables": empty,
            "checked_at": utc_now(),
        }

        lines = [output.rule("mtg brain status"), ""]
        lines.append(f"  database   {db_path}")
        lines.append(f"  size       {_human_bytes(size)}  ({size:,} bytes)")
        lines.append("")
        lines.append(output.rule("tables"))
        for table, count in counts.items():
            if not isinstance(count, int):
                lines.append(f"  {table:<16} {count}")
                continue
            flag = ""
            if count == 0:
                # game_log/rules_missed start empty by design — that is Omar's
                # own data, not a broken build.
                flag = "  (nothing logged yet)" if table in LEARNING_TABLES else "  <- EMPTY"
            lines.append(f"  {table:<16} {count:>9,}{flag}")
        lines.append("")
        lines.append(output.rule("last loaded"))
        for label, _key in META_TIMESTAMPS:
            lines.append(f"  {label:<14} {_pretty_ts(loaded_at.get(label))}")
        if meta.get("rules_effective_date"):
            lines.append(f"  {'rules as of':<14} {meta['rules_effective_date']}")
        lines.append("")
        lines.append(output.rule("decks"))
        if decks:
            for deck in decks:
                lines.append(
                    f"  {deck['deck_id']:<14} {deck['name']:<34} {deck['commander_name']}"
                )
                lines.append(
                    f"  {'':<14} {deck['main_total']} main + "
                    f"{deck['commander_total']} commander   [{deck['set_code']} "
                    f"{deck['release_date']}]"
                )
        else:
            lines.append("  none — run 'mtg rebuild'")
        lines.append("")
        lines.append(output.rule("files"))
        lines.append(
            f"  {'brackets.json':<15} {'yes' if brackets['exists'] else 'MISSING'}"
            + (f"  ({brackets.get('game_changers')} game changers, "
               f"{_human_bytes(brackets.get('bytes'))})" if brackets["exists"] else "")
        )
        for name, info in learning.items():
            lines.append(
                f"  {name:<15} {'yes' if info['exists'] else 'not yet'}"
                + (f"  ({_human_bytes(info['bytes'])})" if info["exists"] else "")
            )
        lines.append("")
        lines.append(
            "  STATUS: OK — all core tables populated, query path is fully offline."
            if not empty
            else f"  STATUS: DEGRADED — empty table(s): {', '.join(empty)}. Run 'mtg rebuild'."
        )
        code = output.emit(payload, "\n".join(lines), as_json)
        return code if not empty else 1
    finally:
        conn.close()


# --------------------------------------------------------------------------- wiring
def _add_json_flag(parser: argparse.ArgumentParser) -> None:
    """Accept --json after the subcommand too. SUPPRESS is load-bearing: a real
    default here would overwrite the root parser's --json with False."""
    parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="emit machine-readable JSON",
    )


def register(subparsers) -> None:
    # ---------------------------------------------------------------- rebuild
    rebuild = subparsers.add_parser(
        "rebuild",
        help="download/refresh the local data (the ONLY networked command)",
        description=(
            "Rebuild the local database from source. Runs the loaders in the only "
            "safe order: cards -> rules -> edhrec -> decks (deck_cards has a foreign "
            "key into cards). Without --force, cached files in data/raw/ are reused."
        ),
    )
    rebuild.add_argument(
        "--only",
        choices=STEP_ORDER,
        help="run a single loader instead of the full pipeline",
    )
    rebuild.add_argument(
        "--force", action="store_true", help="re-download raw sources instead of reusing data/raw/"
    )
    _add_json_flag(rebuild)
    rebuild.set_defaults(func=cmd_rebuild)

    # ---------------------------------------------------------------- status
    status = subparsers.add_parser(
        "status",
        help="database health + inventory (rows, load times, decks, brackets)",
    )
    _add_json_flag(status)
    status.set_defaults(func=cmd_status)

    # ------------------------------------------------------------------- log
    log = subparsers.add_parser(
        "log",
        help="learning loop: record games played and rules you got wrong",
    )
    _add_json_flag(log)
    log.set_defaults(func=_log_help)
    log_sub = log.add_subparsers(dest="log_command", metavar="<game|rule>")

    game = log_sub.add_parser("game", help="log a Commander game, or --list past games")
    game.add_argument("--deck", help="deck slug (see 'mtg status')")
    game.add_argument("--result", choices=RESULTS, type=lambda s: s.lower(), help="win|loss|draw")
    game.add_argument("--opponents", default="", help="who/what you played against")
    game.add_argument("--notes", default="", help="what happened, what to do differently")
    game.add_argument("--list", action="store_true", help="show past games instead of logging one")
    game.add_argument("--limit", type=int, default=20, help="rows for --list (default 20)")
    _add_json_flag(game)
    game.set_defaults(func=cmd_log_game)

    rule = log_sub.add_parser(
        "rule", help="log a rule you got wrong, or --list the most-missed rules"
    )
    rule.add_argument("--rule", help="rule number, e.g. 903.4 or 601.2a")
    rule.add_argument("--note", help="what you got wrong")
    rule.add_argument("--list", action="store_true", help="show the log grouped by rule")
    _add_json_flag(rule)
    rule.set_defaults(func=cmd_log_rule)

    # Keep a handle so _log_help can print real usage.
    log.set_defaults(_log_parser=log)


def _log_help(args) -> int:
    as_json = _as_json(args)
    if as_json:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "mtg log needs a subcommand: 'game' or 'rule'",
                    "usage": [
                        'mtg log game --deck <slug> --result <win|loss|draw> '
                        '--opponents "<text>" --notes "<text>"',
                        "mtg log game --list [--deck <slug>] [--limit N]",
                        'mtg log rule --rule <number> --note "<what I got wrong>"',
                        "mtg log rule --list",
                    ],
                },
                indent=2,
            )
        )
    else:
        parser = getattr(args, "_log_parser", None)
        if parser is not None:
            parser.print_help()
        else:
            print("usage: mtg log <game|rule> ...", file=sys.stderr)
    return 2
