"""Dashboard export: `mtg dashboard`.

The bridge from SQLite to Remy's Lair — the static dashboard in `dashboard/`.
This module is the ONLY writer of `dashboard/data/`; the renderer never queries
anything, it just draws what is written here.

Three subcommands:

    mtg dashboard --build       export data/*.js, cache card images + fonts
    mtg dashboard --serve       serve dashboard/ over http on 127.0.0.1
    mtg dashboard               where it is, whether it is built, how stale

WHY .js AND NOT .json (constraint C5, offline-first)
----------------------------------------------------
The page has to work from `file://` with the network off. Under a `file://`
origin, `fetch()` of a sibling file is blocked by CORS in every modern browser
— there is no flag-free way around it. A `<script src>` is not. So every data
file is JavaScript that ends in a call to the renderer's registry:

    window.RL.register("core", { ... });

That is the whole trick, and it is why nothing here emits .json.

ONE SOURCE OF TRUTH FOR THE NUMBERS
-----------------------------------
Curve, colours, colour sources, role counts, the land assessment and the
bracket all come from `cmd_decks.compute_stats()` / `compute_bracket()` — the
exact functions behind `mtg deck stats` and `mtg deck bracket`. Per-card roles
come from `cmd_decks.classify_roles()`. Nothing is recomputed locally, because
a dashboard that quietly disagreed with the CLI would be worse than no
dashboard: Omar would have two answers and no way to tell which is real.
`--build` re-checks that agreement and warns loudly if it ever breaks.

Consequences of reusing the CLI code path, worth knowing before reading a chart:

  * Roles overlap on purpose and do NOT sum to the deck size (see
    `cmd_decks.ROLES_NOTE`). A card carries every role it satisfies; `role` is
    just the first of those in `ROLE_ORDER`, offered for one-glance colouring.
  * Roles are scored over non-land cards plus the commander. Lands therefore
    get `role: null` and `roles: []` — a land that taps for mana is mana base,
    not ramp, and the CLI counts it the same way.
  * The curve covers maindeck non-lands only; the commander is always
    available so it is reported separately rather than skewing the shape.

NETWORK
-------
`--build` is a networked command, like `mtg rebuild`: it downloads card art and
the two webfont families so that the finished page needs neither.

But the socket does not live here. Every fetch, and the `--serve` file server,
is in `load_dashboard`, which this module imports LAZILY inside the two
functions that need it — the same trick `cmd_admin._loader` uses for the
rebuild loaders. So `cmd_dashboard` imports neither urllib nor http at any
nesting level, and `mtg card` cannot pull the network stack into sys.modules
just because the dashboard command exists. The C1 constraint tests assert this
against the AST, not against behaviour, which is the stronger guarantee.

IDEMPOTENCE
-----------
Running `--build` twice produces byte-identical files, except for the single
`generated_at` field in core.js, which is written LAST so a diff of two builds
is one readable line. Every collection that comes out of a set is sorted before
it is emitted, and card images are skipped when already cached (unless
--force), so a rebuild is cheap and quiet.

stdlib only (C6). Zero AI, zero inference, zero API keys (C1).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import cmd_admin
import cmd_cards
import cmd_decks
import db
import output

# ------------------------------------------------------------------- layout
DASHBOARD = db.ROOT / "dashboard"
DATA_DIR = DASHBOARD / "data"
IMG_DIR = DATA_DIR / "img"
ASSETS_DIR = DASHBOARD / "assets"
FONT_DIR = ASSETS_DIR / "fonts"
FONTS_CSS = FONT_DIR / "fonts.css"
INDEX_HTML = DASHBOARD / "index.html"

DECKS_DIR = db.ROOT / "decks"
MERGED_DIR = DECKS_DIR / "merged-bant"
LEARNING_DIR = db.ROOT / "learning"

#: Files that make the dashboard "built". Everything else is optional polish.
REQUIRED_DATA = ("core.js", "merged.js", "rules.js", "cards.js")


# ============================================================ emit primitives
def _as_json(args) -> bool:
    return bool(getattr(args, "json", False))


def _json_text(payload) -> str:
    """Compact JSON, safe to drop inside a <script> element.

    `</script>` anywhere in a card's oracle text or a rules paragraph would end
    the script early and blank the page. Escaping the three HTML-significant
    characters (plus the two line separators that are newlines to a JS parser
    but not to JSON) makes that structurally impossible. The result is still
    valid JSON — these are ordinary \\uXXXX escapes — so nothing downstream has
    to know.
    """
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        text.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _write_data(filename: str, key: str, payload, rows: int, note: str) -> dict:
    """Write one `window.RL.register(...)` file and describe it for the table."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    body = f"window.RL.register({json.dumps(key)}, {_json_text(payload)});\n"
    path = DATA_DIR / filename
    path.write_text(body, encoding="utf-8")
    return {
        "file": filename,
        "key": key,
        "rows": rows,
        "rows_of": note,
        "bytes": path.stat().st_size,
        "path": str(path),
    }


def _read_doc(path: Path):
    """Markdown off disk, embedded verbatim. Missing file -> None, never a stub:
    the view can then say 'no primer yet' instead of rendering a lie."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _rows(cursor) -> list:
    return [dict(row) for row in cursor]


# =================================================================== core.js
def _role_counts(stats) -> dict:
    return {role: stats["roles"][role]["count"] for role in cmd_decks.ROLE_ORDER}


def _deck_core(conn, deck) -> tuple:
    """-> (payload, warnings). One entry of core.decks[]."""
    warnings = []
    stats = cmd_decks.compute_stats(conn, deck)
    bracket = cmd_decks.compute_bracket(conn, deck)

    if "error" in bracket:
        warnings.append(f"bracket unavailable for '{deck['deck_id']}': {bracket['error']}")
        bracket_no, game_changers, bracket_detail = None, [], None
    else:
        bracket_no = bracket["estimated_bracket"]
        game_changers = bracket["game_changers_found"]
        bracket_detail = {
            "name": bracket["bracket_name"],
            "summary": bracket["bracket_summary"],
            "rules": bracket["bracket_rules"],
            "game_changers_checked": bracket["game_changers_checked"],
            "signals": bracket["signals"],
            "reasoning": bracket["reasoning"],
            "caveats": bracket["caveats"],
            "needs_human_review": bracket["needs_human_review"],
        }

    meta = stats["deck"]
    return (
        {
            "slug": meta["slug"],
            "name": meta["name"],
            "set_code": meta["set_code"],
            "release_date": meta["release_date"],
            "commander": meta["commander"],
            "color_identity": meta["color_identity"],
            "bracket": bracket_no,
            "game_changers": game_changers,
            "totals": stats["totals"],
            "mana_value": stats["mana_value"],
            "curve": stats["curve"],
            "colors": stats["colors"],
            "roles": _role_counts(stats),
            # The names behind each count, so the roles chart can answer
            # "which cards?" without the Deck view being loaded.
            "roles_detail": stats["roles"],
            "roles_note": stats["roles_note"],
            "assessment": stats["assessment"],
            "bracket_detail": bracket_detail,
        },
        warnings,
    )


def _learning(conn) -> dict:
    """The learning loop, straight out of the DB, newest first.

    Each missed rule carries the verbatim CR text so the view never has to
    guess at it — and cannot show a rule number with invented wording (C2).
    """
    missed = _rows(
        conn.execute(
            "SELECT id, logged_at, rule_number, what_i_got_wrong FROM rules_missed "
            "ORDER BY logged_at DESC, id DESC"
        )
    )
    for row in missed:
        hit = conn.execute(
            "SELECT text FROM rules WHERE rule_number=?", (row["rule_number"],)
        ).fetchone()
        row["rule_text"] = hit["text"] if hit else None

    games = _rows(
        conn.execute(
            "SELECT id, played_at, deck_id, opponents, result, notes FROM game_log "
            "ORDER BY played_at DESC, id DESC"
        )
    )
    return {
        "rules_missed": missed,
        "game_log": games,
        # The two generated study documents. GLOSSARY.md is large and lives in
        # rules.js instead, beside the official glossary it complements.
        "docs": {
            "game_log": _read_doc(LEARNING_DIR / "GAME-LOG.md"),
            "rules_missed": _read_doc(LEARNING_DIR / "RULES-I-KEEP-MISSING.md"),
        },
    }


def build_core(conn) -> tuple:
    """-> (record, warnings, deck_rows, by_slug). core.js: what the shell needs.

    `by_slug` is handed back so `--build` can check each deck-<slug>.js against
    the very objects that went into core.js, rather than recomputing (and
    possibly disagreeing with) them.
    """
    warnings = []
    decks, deck_list = [], cmd_decks.all_decks(conn)
    for deck in deck_list:
        payload, warns = _deck_core(conn, deck)
        decks.append(payload)
        warnings.extend(warns)

    brackets = cmd_decks.load_brackets()
    if brackets is None:
        warnings.append(f"brackets.json unreadable at {cmd_decks.BRACKETS_PATH}")

    size = db.DB_PATH.stat().st_size if db.DB_PATH.exists() else 0
    payload = {
        "db": {
            "path": str(db.DB_PATH),
            "size_bytes": size,
            "tables": cmd_admin.table_counts(conn),
        },
        "decks": decks,
        "brackets": brackets,
        "learning": _learning(conn),
        # LAST on purpose: it is the only field that changes between two builds
        # of the same database, so a diff stays one readable line.
        "generated_at": cmd_admin.utc_now(),
    }
    record = _write_data("core.js", "core", payload, len(decks), "decks")
    return record, warnings, deck_list, {d["slug"]: d for d in decks}


# ============================================================= deck-<slug>.js
#: Deck cards need loyalty + art, which `cmd_decks.deck_rows` does not select
#: (the CLI never prints either). Same join, same ORDER BY, two more columns.
DECK_CARD_SQL = """
    SELECT dc.count, dc.board, c.oracle_id, c.name, c.mana_cost, c.cmc,
           c.type_line, c.oracle_text, c.colors, c.color_identity, c.keywords,
           c.power, c.toughness, c.loyalty, c.rarity, c.layout, c.edhrec_rank,
           c.price_usd, c.image_normal, c.scryfall_uri
    FROM deck_cards dc
    JOIN cards c ON c.oracle_id = dc.oracle_id
    WHERE dc.deck_id = ?
    ORDER BY c.cmc, c.name, dc.board
"""


def _image_path(oracle_id: str) -> str:
    """Where the view looks for the art, relative to dashboard/index.html.

    Always emitted, even when the download failed or --skip-images was used:
    making it conditional would mean two builds of the same database disagreed
    depending on network luck. A missing file is the view's problem to handle,
    and it is a visible one.
    """
    return f"data/img/{oracle_id}.jpg"


def _rulings_by_oracle(conn, oracle_ids: list) -> dict:
    """Every official ruling for these cards, oldest first."""
    out = {oid: [] for oid in oracle_ids}
    if not oracle_ids:
        return out
    marks = ",".join("?" * len(oracle_ids))
    for row in conn.execute(
        f"SELECT oracle_id, published_at, comment FROM rulings "
        f"WHERE oracle_id IN ({marks}) ORDER BY oracle_id, published_at, comment",
        oracle_ids,
    ):
        out[row["oracle_id"]].append(
            {"published_at": row["published_at"], "comment": row["comment"]}
        )
    return out


def _deck_card(card, rulings) -> dict:
    land = cmd_decks.is_land(card)
    # Lands are excluded from role scoring by the CLI (a land that taps for
    # mana is mana base, not ramp) — mirror that exactly or the per-card roles
    # would not add up to the role counts in core.js.
    roles = [] if land else cmd_decks.classify_roles(card)
    return {
        "oracle_id": card["oracle_id"],
        "name": card["name"],
        "mana_cost": card["mana_cost"] or "",
        "cmc": float(card["cmc"] or 0),
        "type_line": card["type_line"] or "",
        "oracle_text": card["oracle_text"] or "",
        "colors": output.json_list(card["colors"]),
        "color_identity": output.json_list(card["color_identity"]),
        "keywords": output.json_list(card["keywords"]),
        "power": card["power"],
        "toughness": card["toughness"],
        "loyalty": card["loyalty"],
        "rarity": card["rarity"],
        "price_usd": card["price_usd"],
        "edhrec_rank": card["edhrec_rank"],
        "image": _image_path(card["oracle_id"]),
        "scryfall_uri": card["scryfall_uri"],
        "role": roles[0] if roles else None,
        "roles": roles,
        "type_group": cmd_decks.card_type_group(card["type_line"]),
        "cmc_bucket": cmd_decks.cmc_bucket(card["cmc"]),
        "is_land": land,
        "board": card["board"],
        "count": card["count"],
        "rulings": rulings,
    }


def _verify_role_parity(slug: str, cards: list, core_deck: dict) -> list:
    """Per-card roles must sum to the role counts core.js took from the CLI.

    Same functions, same rows — so a mismatch means this exporter drifted, and
    the dashboard is about to show two different answers to one question. Warn;
    never silently publish it.
    """
    tally = {role: 0 for role in cmd_decks.ROLE_ORDER}
    for card in cards:
        for role in card["roles"]:
            tally[role] += card["count"]
    bad = [r for r in cmd_decks.ROLE_ORDER if tally[r] != core_deck["roles"][r]]
    return [
        f"role parity broken for '{slug}': "
        + ", ".join(f"{r} cards={tally[r]} vs stats={core_deck['roles'][r]}" for r in bad)
    ] if bad else []


def build_deck(conn, deck, core_deck) -> tuple:
    """-> (record, warnings, oracle_ids). One deck-<slug>.js."""
    slug = deck["deck_id"]
    rows = list(conn.execute(DECK_CARD_SQL, (slug,)))
    oracle_ids = [r["oracle_id"] for r in rows]
    rulings = _rulings_by_oracle(conn, oracle_ids)
    cards = [_deck_card(r, rulings.get(r["oracle_id"], [])) for r in rows]

    warnings = _verify_role_parity(slug, cards, core_deck)
    missing_art = [c["name"] for c in rows if not (c["image_normal"] or "").strip()]
    if missing_art:
        warnings.append(
            f"{len(missing_art)} card(s) in '{slug}' have no image_normal in the DB: "
            + ", ".join(sorted(missing_art)[:5])
        )

    doc_dir = DECKS_DIR / slug
    payload = {
        "slug": slug,
        "cards": cards,
        "docs": {
            "primer": _read_doc(doc_dir / "PRIMER.md"),
            "cards": _read_doc(doc_dir / "CARDS.md"),
            "upgrades": _read_doc(doc_dir / "UPGRADES.md"),
        },
    }
    record = _write_data(
        f"deck-{slug}.js", f"deck:{slug}", payload, len(cards), "distinct cards"
    )
    return record, warnings, oracle_ids


# ================================================================= merged.js
#: The Bant merge is documents, not a database deck — `mtg deck merged-bant`
#: correctly answers "not in my data". Its canonical list is the copy-paste
#: block at the end of DECKLIST.md (90 lines = 100 cards, commander first),
#: which is the one place in that file guaranteed to be machine-readable.
MERGED_BLOCK_RE = re.compile(r"##\s*PLAIN COPY-PASTE.*?```(.*?)```", re.S)
MERGED_LINE_RE = re.compile(r"^(\d+)\s+(.+?)\s*$")


def _lookup_card(conn, name: str):
    """Exact name, then front-face — 'A // B' is filed under its full name."""
    row = conn.execute(
        "SELECT oracle_id, name, mana_cost, cmc, type_line, color_identity, "
        "rarity, price_usd, edhrec_rank FROM cards WHERE name = ? COLLATE NOCASE",
        (name,),
    ).fetchone()
    if row is None:
        row = conn.execute(
            "SELECT oracle_id, name, mana_cost, cmc, type_line, color_identity, "
            "rarity, price_usd, edhrec_rank FROM cards "
            "WHERE name LIKE ? COLLATE NOCASE ORDER BY name LIMIT 1",
            (name + " // %",),
        ).fetchone()
    return row


def build_merged(conn) -> tuple:
    """-> (record or None, warnings, oracle_ids)."""
    doc_path = MERGED_DIR / "MERGED-BANT.md"
    list_path = MERGED_DIR / "DECKLIST.md"
    raw = _read_doc(list_path)
    if raw is None:
        return None, [f"merged deck skipped: {list_path} not found"], []

    block = MERGED_BLOCK_RE.search(raw)
    if not block:
        return None, [
            f"merged deck skipped: no 'PLAIN COPY-PASTE' code block in {list_path}"
        ], []

    warnings, decklist, oracle_ids = [], [], []
    lands = nonlands = total = 0
    by_type: dict = {}
    for line in block.group(1).strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = MERGED_LINE_RE.match(line)
        if not match:
            warnings.append(f"merged decklist: unparsable line {line!r}")
            continue
        count, name = int(match.group(1)), match.group(2)
        card = _lookup_card(conn, name)
        if card is None:
            # C2: never invent the card. Record it as unresolved and let the
            # view show the gap rather than a plausible-looking row.
            warnings.append(f"merged decklist: '{name}' is not in the cards table")
            decklist.append(
                {"count": count, "name": name, "oracle_id": None, "unresolved": True}
            )
            total += count
            continue

        group = "Commander" if not decklist else cmd_decks.card_type_group(card["type_line"])
        is_land = "land" in (card["type_line"] or "").lower()
        decklist.append(
            {
                "count": count,
                "name": card["name"],
                "oracle_id": card["oracle_id"],
                "mana_cost": card["mana_cost"] or "",
                "cmc": float(card["cmc"] or 0),
                "type_line": card["type_line"] or "",
                "color_identity": output.json_list(card["color_identity"]),
                "rarity": card["rarity"],
                "price_usd": card["price_usd"],
                "edhrec_rank": card["edhrec_rank"],
                "type_group": group,
                "image": _image_path(card["oracle_id"]),
            }
        )
        oracle_ids.append(card["oracle_id"])
        by_type[group] = by_type.get(group, 0) + count
        total += count
        if is_land:
            lands += count
        else:
            nonlands += count

    ordered_types = [t for t in cmd_decks.TYPE_ORDER if t in by_type]
    ordered_types += sorted(t for t in by_type if t not in cmd_decks.TYPE_ORDER)

    payload = {
        "slug": "merged-bant",
        "name": "Merged Bant",
        "source": str(list_path),
        "decklist": decklist,
        "doc": _read_doc(doc_path),
        "decklist_doc": raw,
        "totals": {
            "cards": total,
            "entries": len(decklist),
            "lands": lands,
            "nonlands": nonlands,
        },
        "by_type": {t: by_type[t] for t in ordered_types},
    }
    record = _write_data(
        "merged.js", "merged", payload, len(decklist), "decklist entries"
    )
    return record, warnings, oracle_ids


# ================================================================== rules.js
def _rule_sort_key(number: str) -> tuple:
    """Comprehensive Rules order, which is NOT lexicographic: '100.1' sorts
    after '2', and '601.2a' after '601.2'."""
    head, _, tail = (number or "").partition(".")
    try:
        section = int(head)
    except ValueError:
        section = 0
    match = re.match(r"(\d*)(.*)", tail)
    digits, suffix = match.group(1), match.group(2)
    return (section, int(digits) if digits else -1, suffix, number or "")


def build_rules(conn) -> dict:
    rules = [
        [r["rule_number"], r["section"], r["parent_number"], r["text"]]
        for r in conn.execute(
            "SELECT rule_number, section, parent_number, text FROM rules"
        )
    ]
    rules.sort(key=lambda row: _rule_sort_key(row[0]))
    glossary = [
        [r["term"], r["definition"]]
        for r in conn.execute("SELECT term, definition FROM glossary ORDER BY term")
    ]
    payload = {
        "fields": {"rules": ["number", "section", "parent", "text"],
                   "glossary": ["term", "definition"]},
        "rules": rules,
        "glossary": glossary,
        # Omar's hand-written beginner glossary. It sits here rather than in
        # core.js because it is large and belongs beside the official one.
        "docs": {"glossary": _read_doc(LEARNING_DIR / "GLOSSARY.md")},
    }
    return _write_data(
        "rules.js", "rules", payload, len(rules) + len(glossary), "rules + glossary"
    )


# ================================================================== cards.js
#: Array-of-arrays, not array-of-objects: 38k rows of repeated key names is
#: several megabytes of nothing. `fields` is the header.
#:
#: `pt` and `legal_commander` are here because the Cards view reimplements the
#: `mtg search` query language in the browser, and two of its filters cannot be
#: derived from anything else in the payload:
#:   * `legal:commander` — 6,729 of the 38,351 cards are banned or not_legal,
#:     and legality is NOT predictable from the type line (795 plain "Creature"
#:     rows are not_legal against 12,964 that are). Guessing it would break C2.
#:   * P/T — 19,730 cards have power/toughness or loyalty and nothing else in
#:     the row carries it.
#: `pt` is precomputed with the same `_pt_str` the CLI prints, so the dashboard
#: and the terminal never disagree about a card's box. Both are appended at the
#: END of the tuple: `fields` is the header, so readers that index by name keep
#: working unchanged.
CARD_FIELDS = (
    "name", "mana_cost", "type_line", "cmc", "color_identity",
    "rarity", "edhrec_rank", "oracle_text", "price_usd",
    "pt", "legal_commander",
)


def build_cards(conn) -> dict:
    rows = [
        [
            r["name"],
            r["mana_cost"] or "",
            r["type_line"] or "",
            float(r["cmc"] or 0),
            output.json_list(r["color_identity"]),
            r["rarity"],
            r["edhrec_rank"],
            r["oracle_text"] or "",
            r["price_usd"],
            cmd_cards._pt_str(r),
            r["legal_commander"],
        ]
        for r in conn.execute(
            "SELECT name, mana_cost, type_line, cmc, color_identity, rarity, "
            "edhrec_rank, oracle_text, price_usd, power, toughness, loyalty, "
            "legal_commander FROM cards ORDER BY name, oracle_id"
        )
    ]
    payload = {"fields": list(CARD_FIELDS), "rows": rows}
    return _write_data("cards.js", "cards", payload, len(rows), "cards")


# =================================================================== --build
def _fmt_bytes(value: int) -> str:
    step = float(value)
    for unit in ("B", "KB", "MB", "GB"):
        if step < 1024 or unit == "GB":
            return f"{step:.0f} {unit}" if unit == "B" else f"{step:.1f} {unit}"
        step /= 1024
    return f"{value} B"


def _render_build(payload) -> str:
    files = payload["files"]
    name_w = max([len(f["file"]) for f in files] + [len("FILE")])
    note_w = max([len(f["rows_of"]) for f in files] + [len("ROWS ARE")])
    lines = [output.rule("mtg dashboard --build")]
    lines.append(f"  {'FILE':<{name_w}}  {'ROWS':>7}  {'ROWS ARE':<{note_w}}  {'BYTES':>10}")
    lines.append(f"  {'-' * name_w}  {'-' * 7}  {'-' * note_w}  {'-' * 10}")
    for item in files:
        lines.append(
            f"  {item['file']:<{name_w}}  {item['rows']:>7,}  "
            f"{item['rows_of']:<{note_w}}  {_fmt_bytes(item['bytes']):>10}"
        )
    total_rows = sum(f["rows"] for f in files)
    total_bytes = sum(f["bytes"] for f in files)
    lines.append(f"  {'-' * name_w}  {'-' * 7}  {'-' * note_w}  {'-' * 10}")
    lines.append(
        f"  {'TOTAL':<{name_w}}  {total_rows:>7,}  {'':<{note_w}}  "
        f"{_fmt_bytes(total_bytes):>10}"
    )
    lines.append("")

    images = payload["images"]
    if images.get("skipped"):
        lines.append("  Images  : skipped (--skip-images)")
    else:
        lines.append(
            f"  Images  : {images['downloaded']} downloaded, {images['cached']} already cached, "
            f"{images['failed']} failed, {images['no_url']} without a URL "
            f"— {_fmt_bytes(images['bytes'])} in {IMG_DIR.name}/"
        )
    fonts = payload["fonts"]
    if fonts.get("skipped"):
        lines.append("  Fonts   : skipped (--skip-fonts)")
    elif fonts["ok"]:
        lines.append(
            f"  Fonts   : {fonts['downloaded']} downloaded, {fonts['cached']} already cached "
            f"({', '.join(fonts['families'])}) — {_fmt_bytes(fonts['bytes'])}, "
            f"fonts.css written"
        )
    else:
        lines.append(
            "  Fonts   : NOT cached — fonts.css written as a no-op. The page falls "
            "back to the system stacks in tokens.css and still looks right."
        )
    lines.append(f"  Elapsed : {payload['seconds']}s")
    lines.append("")
    lines.append(f"  Open    : file://{INDEX_HTML}")
    lines.append("            or `mtg dashboard --serve`")

    if payload["warnings"]:
        lines.append("")
        lines.append(output.rule("WARNINGS"))
        for note in payload["warnings"]:
            lines.append(f"  ! {note}")
    return "\n".join(lines)


def cmd_build(args) -> int:
    as_json = _as_json(args)
    if not db.DB_PATH.exists():
        return output.fail(
            f"database {db.DB_PATH} — run 'mtg rebuild' to build it", as_json
        )

    started = time.monotonic()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = db.connect()
    try:
        files, warnings, oracle_ids = [], [], []

        core, warns, decks, core_by_slug = build_core(conn)
        files.append(core)
        warnings.extend(warns)

        for deck in decks:
            record, deck_warns, ids = build_deck(
                conn, deck, core_by_slug[deck["deck_id"]]
            )
            files.append(record)
            warnings.extend(deck_warns)
            oracle_ids.extend(ids)

        merged, merged_warns, merged_ids = build_merged(conn)
        if merged:
            files.append(merged)
        warnings.extend(merged_warns)
        oracle_ids.extend(merged_ids)

        files.append(build_rules(conn))
        files.append(build_cards(conn))

        if args.skip_images:
            images = {"skipped": True, "wanted": 0, "downloaded": 0, "cached": 0,
                      "no_url": 0, "failed": 0, "bytes": 0, "errors": []}
        else:
            import load_dashboard  # lazy: keeps urllib out of every other command

            images = load_dashboard.cache_images(
                conn, oracle_ids, IMG_DIR, force=args.force
            )
            images["skipped"] = False
            if images["failed"]:
                warnings.append(
                    f"{images['failed']} card image(s) failed to download: "
                    + "; ".join(images["errors"][:3])
                )
    finally:
        conn.close()

    if args.skip_fonts:
        fonts = {"skipped": True, "ok": False, "faces": 0, "downloaded": 0,
                 "cached": 0, "failed": 0, "bytes": 0, "families": [], "errors": []}
    else:
        import load_dashboard

        fonts = load_dashboard.cache_fonts(FONT_DIR, FONTS_CSS, force=args.force)
        fonts["skipped"] = False
        if not fonts["ok"]:
            warnings.append(
                "webfonts not cached (" + "; ".join(fonts["errors"][:2] or ["unknown"])
                + ") — the page falls back to the system stacks in tokens.css"
            )

    payload = {
        "ok": True,
        "dashboard": str(DASHBOARD),
        "data_dir": str(DATA_DIR),
        "files": files,
        "total_bytes": sum(f["bytes"] for f in files),
        "images": images,
        "fonts": fonts,
        "warnings": warnings,
        "seconds": round(time.monotonic() - started, 2),
        "open": f"file://{INDEX_HTML}",
    }
    return output.emit(payload, _render_build(payload), as_json)


# =================================================================== --serve
def cmd_serve(args) -> int:
    """Static file server on the loopback interface only.

    The page is a dumb renderer of files already on disk, so this exists purely
    for the convenience of a real http:// origin during development. Binding
    127.0.0.1 (not 0.0.0.0) keeps Omar's card collection off his LAN.
    """
    as_json = _as_json(args)
    if not DASHBOARD.exists():
        return output.fail(f"dashboard directory {DASHBOARD}", as_json)

    import load_dashboard  # lazy: `http.server` is a socket, and lives there

    try:
        server = load_dashboard.make_server(DASHBOARD, args.port)
    except OSError as exc:
        return output.fail(f"cannot bind 127.0.0.1:{args.port} — {exc}", as_json)

    url = f"http://127.0.0.1:{server.server_port}/"
    if as_json:
        print(json.dumps({"ok": True, "url": url, "root": str(DASHBOARD)}, indent=2))
    else:
        print(f"Remy's Lair — serving {DASHBOARD}")
        print(f"  {url}")
        print("  Ctrl-C to stop. Bound to 127.0.0.1 only.")
    sys.stdout.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        if not as_json:
            print("\nstopped.")
    finally:
        server.server_close()
    return 0


# ============================================================ status (no flags)
def _file_state(path: Path) -> dict:
    exists = path.exists()
    return {
        "path": str(path),
        "exists": exists,
        "bytes": path.stat().st_size if exists else 0,
        "mtime": path.stat().st_mtime if exists else None,
    }


def cmd_dashboard(args) -> int:
    """No flags: where it is, whether it is built, how stale, how to open it."""
    as_json = _as_json(args)

    data_files = [_file_state(DATA_DIR / name) for name in REQUIRED_DATA]
    deck_files = sorted(DATA_DIR.glob("deck-*.js")) if DATA_DIR.exists() else []
    data_files += [_file_state(p) for p in deck_files]
    built = all(f["exists"] for f in data_files[: len(REQUIRED_DATA)]) and bool(deck_files)

    db_mtime = db.DB_PATH.stat().st_mtime if db.DB_PATH.exists() else None
    stamps = [f["mtime"] for f in data_files if f["mtime"]]
    oldest = min(stamps) if stamps else None
    if not built:
        freshness = "NOT BUILT"
    elif db_mtime and oldest and db_mtime > oldest:
        freshness = "STALE — the database is newer than the exported data"
    else:
        freshness = "FRESH — exported data is newer than the database"

    images = sorted(IMG_DIR.glob("*.jpg")) if IMG_DIR.exists() else []
    fonts = sorted(FONT_DIR.glob("*.woff2")) if FONT_DIR.exists() else []

    payload = {
        "ok": True,
        "dashboard": str(DASHBOARD),
        "index": str(INDEX_HTML),
        "index_exists": INDEX_HTML.exists(),
        "built": built,
        "freshness": freshness,
        "data_dir": str(DATA_DIR),
        "files": data_files,
        "total_bytes": sum(f["bytes"] for f in data_files),
        "images_cached": len(images),
        "fonts_cached": len(fonts),
        "fonts_css": FONTS_CSS.exists(),
        "db": {"path": str(db.DB_PATH), "exists": db.DB_PATH.exists()},
        "open": f"file://{INDEX_HTML}",
        "serve": "mtg dashboard --serve",
        "build": "mtg dashboard --build",
    }

    lines = [output.rule("Remy's Lair — dashboard")]
    lines.append(f"  Path      : {DASHBOARD}")
    lines.append(
        f"  index.html: {'present' if INDEX_HTML.exists() else 'MISSING — the renderer has not been written yet'}"
    )
    lines.append(f"  Built     : {'yes' if built else 'no — run: mtg dashboard --build'}")
    lines.append(f"  Freshness : {freshness}")
    lines.append("")
    if data_files:
        width = max(len(Path(f["path"]).name) for f in data_files)
        for item in data_files:
            name = Path(item["path"]).name
            state = _fmt_bytes(item["bytes"]) if item["exists"] else "missing"
            lines.append(f"    {name:<{width}}  {state:>10}")
        lines.append(f"    {'total':<{width}}  {_fmt_bytes(payload['total_bytes']):>10}")
    lines.append("")
    lines.append(f"  Card art  : {len(images)} cached in {IMG_DIR}")
    lines.append(
        f"  Webfonts  : {len(fonts)} cached"
        + (" + fonts.css" if FONTS_CSS.exists() else " (no fonts.css)")
    )
    lines.append("")
    lines.append("  Open it:")
    lines.append(f"    file://{INDEX_HTML}")
    lines.append("    mtg dashboard --serve        (http://127.0.0.1:8765)")
    lines.append("")
    lines.append("  Rebuild the data:")
    lines.append("    mtg dashboard --build")
    return output.emit(payload, "\n".join(lines), as_json)


# ================================================================== argparse
def _add_json_flag(parser) -> None:
    """Accept --json after the subcommand too. See cmd_decks._add_json_flag —
    default=SUPPRESS stops it overwriting a --json parsed by the root parser."""
    parser.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS,
        help="emit machine-readable JSON instead of formatted text",
    )


def cmd_dashboard_router(args) -> int:
    if args.build and args.serve:
        return output.fail(
            "--build and --serve are separate steps; run --build first", _as_json(args)
        )
    if args.build:
        return cmd_build(args)
    if args.serve:
        return cmd_serve(args)
    return cmd_dashboard(args)


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "dashboard",
        help="build / serve Remy's Lair, the offline dashboard",
        description=(
            "mtg dashboard                 where it is, whether it is built, how stale\n"
            "mtg dashboard --build         export dashboard/data/*.js + cache art & fonts\n"
            "mtg dashboard --serve         serve dashboard/ on 127.0.0.1\n"
            "\n"
            "--build is a NETWORKED command (card art + webfonts), like 'mtg rebuild'.\n"
            "The page it produces is not: it runs from file:// with the network off."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--build", action="store_true", help="export the data files the page reads"
    )
    parser.add_argument(
        "--serve", action="store_true", help="serve dashboard/ over http (127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="port for --serve (default 8765)"
    )
    parser.add_argument(
        "--skip-images", action="store_true", help="--build: do not download card art"
    )
    parser.add_argument(
        "--skip-fonts", action="store_true", help="--build: do not download webfonts"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="--build: re-download art/fonts that are already cached",
    )
    _add_json_flag(parser)
    parser.set_defaults(func=cmd_dashboard_router)
