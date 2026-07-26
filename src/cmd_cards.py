"""Card, search, rule and glossary lookups — the reference half of MTG Brain.

Everything here is deterministic SQLite retrieval. No network, no inference:
the four commands below are the agents' only source of card/rules truth, and
when the data is not present they say so (via output.fail) instead of guessing.

Subcommands registered:
    mtg card <name...>        full card + every official ruling
    mtg search "<query>"      FTS5 + structured filters (Commander-scoped)
    mtg rule <number|query>   exact rule lookup w/ children, or full-text search
    mtg glossary <term...>    glossary entry + the rules it points at

Stdlib only (constraint C6).
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3

import db
import output

# --------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------

# Printings that are not "the card". 219 names in the corpus map to more than
# one oracle_id purely because a token/art-card shares the name; resolving to
# one of those would hand an agent a card that cannot legally be played.
NON_CARD_LAYOUTS = ("token", "art_series", "double_faced_token")

CARD_COLUMNS = (
    "oracle_id", "name", "mana_cost", "cmc", "type_line", "oracle_text",
    "colors", "color_identity", "keywords", "power", "toughness", "loyalty",
    "rarity", "layout", "card_faces_json", "legal_commander", "edhrec_rank",
    "price_usd", "scryfall_uri", "image_normal",
)

COLOR_NAMES = {"W": "white", "U": "blue", "B": "black", "R": "red", "G": "green"}
WUBRG = "WUBRG"

RULE_NUMBER_RE = re.compile(r"^\d+(\.\d+)?[a-z]?$")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

# "See rule 702.2." / "see rules 903.8 and 903.9" / "rule 903, "Commander.""
RULE_REF_RE = re.compile(r"\brules?\s+(\d+(?:\.\d+)?[a-z]?)", re.I)
# Bare fully-qualified references that skip the word "rule" (e.g. "(see 104.3b)").
BARE_RULE_REF_RE = re.compile(r"\b(\d{3}\.\d+[a-z]?)\b")

TEXT_WIDTH = 76


# --------------------------------------------------------------------------
# small shared helpers
# --------------------------------------------------------------------------

def _open(as_json: bool):
    """Open the DB, or emit a 'not in my data' failure and return None."""
    if not db.DB_PATH.exists():
        output.fail(f"database at {db.DB_PATH} (run 'mtg rebuild' to build it)", as_json)
        return None
    conn = db.connect()
    try:
        conn.execute("SELECT 1 FROM cards LIMIT 1").fetchone()
    except sqlite3.OperationalError:
        conn.close()
        output.fail(f"card data in {db.DB_PATH} (run 'mtg rebuild')", as_json)
        return None
    return conn


def _fts_query(terms) -> str:
    """Build a MATCH string that FTS5 can never choke on.

    User text routinely contains ", *, -, :, NEAR, AND ... all of which are FTS5
    syntax. Wrapping every term in double quotes (with internal quotes doubled)
    turns each one into an inert literal/phrase. Raw user input is NEVER
    interpolated into a MATCH expression.
    """
    parts = []
    for term in terms:
        term = (term or "").strip()
        if not term:
            continue
        parts.append('"' + term.replace('"', '""') + '"')
    return " AND ".join(parts)


def _fts_column_query(column: str, terms) -> str:
    """Same sanitization, restricted to one FTS column (e.g. name)."""
    parts = []
    for term in terms:
        term = (term or "").strip()
        if not term:
            continue
        parts.append('%s : "%s"' % (column, term.replace('"', '""')))
    return " AND ".join(parts)


def _like(value: str) -> str:
    """Lowercased %contains% pattern with LIKE wildcards escaped."""
    esc = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return "%" + esc.lower() + "%"


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _clamp_limit(value: int) -> int:
    """Keep LIMIT sane.

    Two traps this closes: SQLite reads a negative LIMIT as *unlimited* (so
    `--limit -1` would dump all 38k cards), and LIMIT 0 returns no rows, which
    would make us print "not in my data" for a query that actually matched
    thousands — a false negative is the one thing this CLI must never emit.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return 25
    return max(1, value)


def _row_to_card(row: sqlite3.Row) -> dict:
    """Full card row as JSON-ready data: JSON-array columns become real arrays."""
    card = {key: row[key] for key in CARD_COLUMNS if key in row.keys()}
    card["colors"] = output.json_list(row["colors"])
    card["color_identity"] = output.json_list(row["color_identity"])
    card["keywords"] = output.json_list(row["keywords"])
    faces = row["card_faces_json"] if "card_faces_json" in row.keys() else None
    parsed = []
    if faces:
        try:
            loaded = json.loads(faces)
            parsed = loaded if isinstance(loaded, list) else []
        except (json.JSONDecodeError, TypeError):
            parsed = []
    card.pop("card_faces_json", None)
    card["card_faces"] = parsed
    return card


def _identity_str(identity: list) -> str:
    if not identity:
        return "colorless"
    letters = "".join(c for c in WUBRG if c in identity)
    extra = [c for c in identity if c not in WUBRG]
    letters += "".join(extra)
    names = ", ".join(COLOR_NAMES.get(c, c) for c in letters)
    return f"{letters} ({names})"


def _pt_str(row) -> str:
    """P/T or loyalty, whichever the card actually has."""
    power = row["power"] if "power" in row.keys() else None
    tough = row["toughness"] if "toughness" in row.keys() else None
    loyal = row["loyalty"] if "loyalty" in row.keys() else None
    if not _blank(power) or not _blank(tough):
        return f"{power or '?'}/{tough or '?'}"
    if not _blank(loyal):
        return f"Loyalty {loyal}"
    return ""


def _face_pt(face: dict) -> str:
    power, tough, loyal = face.get("power"), face.get("toughness"), face.get("loyalty")
    if power is not None or tough is not None:
        return f"{power if power is not None else '?'}/{tough if tough is not None else '?'}"
    if loyal is not None:
        return f"Loyalty {loyal}"
    return ""


def _ambiguous(kind: str, candidates: list, lines: list, as_json: bool) -> int:
    """Several distinct cards matched — show them all, never pick one silently."""
    if as_json:
        print(json.dumps(
            {"ok": False, "error": kind, "ambiguous": True, "candidates": candidates},
            indent=2, ensure_ascii=False,
        ))
    else:
        print("\n".join(lines))
    return 1


# --------------------------------------------------------------------------
# card resolution
# --------------------------------------------------------------------------

def _select_cards(conn, where: str, params: tuple) -> list:
    cols = ", ".join(CARD_COLUMNS)
    sql = f"SELECT {cols} FROM cards WHERE {where}"
    return conn.execute(sql, params).fetchall()


def _prefer_real_cards(rows: list) -> list:
    """Drop token / art-series / non-legal-data printings unless that is all we have."""
    preferred = [
        r for r in rows
        if r["layout"] not in NON_CARD_LAYOUTS and r["legal_commander"] is not None
    ]
    return preferred or rows


def _narrow_same_name(rows: list) -> list:
    """Rows that share one name are variant printings (Un-set variants, planes).

    Prefer the one the Commander world actually plays: an EDHREC rank means the
    printing is the one people register. If the variants are textually identical
    they are interchangeable, so pick deterministically. Otherwise stay ambiguous.
    """
    if len(rows) <= 1:
        return rows
    if len({r["name"] for r in rows}) != 1:
        return rows
    ranked = [r for r in rows if r["edhrec_rank"] is not None]
    if len(ranked) == 1:
        return ranked
    if ranked:
        rows = ranked
    signatures = {(r["mana_cost"], r["type_line"], r["oracle_text"]) for r in rows}
    if len(signatures) == 1:
        return [sorted(rows, key=lambda r: (r["edhrec_rank"] or 10 ** 9, r["oracle_id"]))[0]]
    return rows


def _resolve_card(conn, name: str):
    """(row, candidates, how) — exactly one of row/candidates is meaningful.

    Resolution order: oracle_id -> exact (case-sensitive) -> exact
    (case-insensitive) -> unique prefix -> FTS name match.
    """
    query = name.strip()
    if not query:
        return None, [], "empty"

    if UUID_RE.match(query):
        rows = _select_cards(conn, "oracle_id = ?", (query,))
        if rows:
            return rows[0], [], "oracle_id"

    attempts = (
        ("exact", "name = ?", (query,)),
        ("exact-ci", "name = ? COLLATE NOCASE", (query,)),
        ("prefix", "name LIKE ? ESCAPE '\\' COLLATE NOCASE",
         (query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%",)),
    )
    for how, where, params in attempts:
        rows = _select_cards(conn, where, params)
        if not rows:
            continue
        rows = _narrow_same_name(_prefer_real_cards(rows))
        if len(rows) == 1:
            return rows[0], [], how
        return None, rows, how

    match = _fts_column_query("name", query.split())
    if match:
        ids = [
            r["oracle_id"] for r in
            conn.execute(
                "SELECT oracle_id FROM cards_fts WHERE cards_fts MATCH ? LIMIT 50", (match,)
            ).fetchall()
        ]
        if ids:
            placeholders = ",".join("?" * len(ids))
            rows = _select_cards(conn, f"oracle_id IN ({placeholders})", tuple(ids))
            rows = _narrow_same_name(_prefer_real_cards(rows))
            if len(rows) == 1:
                return rows[0], [], "fts"
            if rows:
                return None, rows, "fts"
    return None, [], "none"


def _candidate_dict(row) -> dict:
    return {
        "oracle_id": row["oracle_id"],
        "name": row["name"],
        "mana_cost": row["mana_cost"],
        "type_line": row["type_line"],
        "layout": row["layout"],
        "edhrec_rank": row["edhrec_rank"],
        "oracle_text": row["oracle_text"],
    }


# --------------------------------------------------------------------------
# mtg card
# --------------------------------------------------------------------------

def _fetch_rulings(conn, oracle_id: str) -> list:
    rows = conn.execute(
        "SELECT published_at, comment, source FROM rulings WHERE oracle_id = ? "
        "ORDER BY COALESCE(published_at, ''), rowid",
        (oracle_id,),
    ).fetchall()
    return [
        {"published_at": r["published_at"], "comment": r["comment"], "source": r["source"]}
        for r in rows
    ]


def _render_card(row, rulings: list, show_rulings: bool) -> str:
    card = _row_to_card(row)
    lines = [output.rule(card["name"], TEXT_WIDTH)]

    if not _blank(card["mana_cost"]):
        lines.append(f"Mana cost      : {card['mana_cost']}")
    cmc = card["cmc"]
    if cmc is not None:
        lines.append(f"Mana value     : {int(cmc) if float(cmc).is_integer() else cmc}")
    lines.append(f"Type           : {card['type_line'] or '—'}")

    if not _blank(card["oracle_text"]):
        lines.append("")
        lines.append(output.wrap(card["oracle_text"], TEXT_WIDTH))

    pt = _pt_str(row)
    if pt:
        lines.append("")
        lines.append(f"P/T            : {pt}" if "/" in pt else f"Loyalty        : {pt.split()[-1]}")

    lines.append("")
    lines.append(f"Color identity : {_identity_str(card['color_identity'])}")
    if card["keywords"]:
        lines.append(f"Keywords       : {', '.join(card['keywords'])}")
    lines.append(f"Rarity         : {card['rarity'] or 'unknown'}")
    lines.append(f"Commander      : {card['legal_commander'] or 'unknown'}")
    rank = card["edhrec_rank"]
    lines.append(f"EDHREC rank    : {'#' + str(rank) if rank is not None else 'not in my data'}")
    price = card["price_usd"]
    lines.append(f"Price (USD)    : {'$%.2f' % price if price is not None else 'not in my data'}")

    faces = card["card_faces"]
    if faces:
        lines.append("")
        lines.append(output.rule(f"Faces ({len(faces)})", TEXT_WIDTH))
        for i, face in enumerate(faces, 1):
            if i > 1:
                lines.append("")
            head = f"[{i}] {face.get('name') or '(unnamed face)'}"
            cost = face.get("mana_cost")
            if cost:
                head += f"   {cost}"
            lines.append(head)
            if face.get("type_line"):
                lines.append(f"    {face['type_line']}")
            if face.get("oracle_text"):
                lines.append(output.wrap(face["oracle_text"], TEXT_WIDTH - 4, indent="    "))
            fpt = _face_pt(face)
            if fpt:
                lines.append(f"    {fpt}")

    if show_rulings:
        lines.append("")
        lines.append(output.rule(f"Rulings ({len(rulings)})", TEXT_WIDTH))
        if not rulings:
            lines.append("not in my data: no official rulings recorded for this card")
        for ruling in rulings:
            date = ruling["published_at"] or "undated"
            src = ruling["source"] or "?"
            lines.append(f"[{date}] ({src})")
            lines.append(output.wrap(ruling["comment"] or "", TEXT_WIDTH - 2, indent="  "))
            lines.append("")
        if rulings:
            lines.pop()

    if card["scryfall_uri"]:
        lines.append("")
        lines.append(card["scryfall_uri"])
    return "\n".join(lines)


def cmd_card(args) -> int:
    as_json = args.json
    name = " ".join(args.name).strip()
    conn = _open(as_json)
    if conn is None:
        return 1
    try:
        row, candidates, how = _resolve_card(conn, name)

        if row is None and candidates:
            cands = [_candidate_dict(c) for c in candidates]
            lines = [
                f"'{name}' matches {len(cands)} distinct cards ({how} match) — "
                "not guessing. Re-run with the full name or the oracle_id:",
                "",
            ]
            for c in cands:
                lines.append(f"  {c['name']}  [{c['oracle_id']}]")
                lines.append(f"      {c['mana_cost'] or ''} {c['type_line'] or ''}".rstrip())
                snippet = (c["oracle_text"] or "").replace("\n", " ")
                if snippet:
                    lines.append(f"      {snippet[:100]}{'…' if len(snippet) > 100 else ''}")
            return _ambiguous(
                f"'{name}' is ambiguous — {len(cands)} distinct cards match",
                cands, lines, as_json,
            )

        if row is None:
            return output.fail(f"card '{name}'", as_json)

        rulings = _fetch_rulings(conn, row["oracle_id"])
        show = not args.no_rulings
        card = _row_to_card(row)
        payload = {"ok": True, **card, "rulings": rulings if show else [],
                   "ruling_count": len(rulings), "matched_by": how}
        return output.emit(payload, _render_card(row, rulings, show), as_json)
    finally:
        conn.close()


# --------------------------------------------------------------------------
# mtg search — structured query language + FTS5
# --------------------------------------------------------------------------

FILTER_RE = re.compile(r"^(?P<key>[A-Za-z_]+)(?P<op><=|>=|!=|:|<|>|=)(?P<val>.*)$", re.S)

TYPE_KEYS = {"type", "t", "is"}
COLOR_KEYS = {"color", "colors", "c", "id", "ci", "identity"}
CMC_KEYS = {"cmc", "mv"}
RARITY_KEYS = {"rarity", "r"}
DECK_KEYS = {"deck", "d"}
LEGAL_KEYS = {"legal", "legality"}
NAME_KEYS = {"name", "n"}
TEXT_KEYS = {"oracle", "o", "text"}
KEYWORD_KEYS = {"kw", "keyword", "keywords"}
ALL_KEYS = (TYPE_KEYS | COLOR_KEYS | CMC_KEYS | RARITY_KEYS | DECK_KEYS
            | LEGAL_KEYS | NAME_KEYS | TEXT_KEYS | KEYWORD_KEYS)

LEGAL_VALUES = {
    "commander": "legal", "legal": "legal", "edh": "legal",
    "banned": "banned", "restricted": "restricted",
    "not_legal": "not_legal", "notlegal": "not_legal", "illegal": "not_legal",
}


def _split_tokens(text: str) -> list:
    """Whitespace split that keeps "quoted phrases" (and type:"legendary creature") whole."""
    tokens, cur, in_quote = [], [], False
    for ch in text or "":
        if ch == '"':
            in_quote = not in_quote
            continue
        if ch.isspace() and not in_quote:
            if cur:
                tokens.append("".join(cur))
                cur = []
        else:
            cur.append(ch)
    if cur:
        tokens.append("".join(cur))
    return tokens


class QueryError(Exception):
    pass


def parse_query(text: str):
    """-> (where_clauses, params, bare_terms, needs_deck_join, filters_described)

    Structured tokens are pulled OUT first; whatever is left is bare text that
    goes to FTS5 MATCH.
    """
    where, params, bare, described = [], [], [], []
    deck_slug = None

    for token in _split_tokens(text):
        match = FILTER_RE.match(token)
        key = match.group("key").lower() if match else None
        if not match or key not in ALL_KEYS:
            bare.append(token)
            continue
        op, val = match.group("op"), match.group("val").strip()
        if not val:
            bare.append(token)
            continue

        if key in TYPE_KEYS:
            where.append("lower(c.type_line) LIKE ? ESCAPE '\\'")
            params.append(_like(val))
            described.append(f"type~{val}")
        elif key in COLOR_KEYS:
            letters = {ch.upper() for ch in val if ch.isalpha()}
            if "C" in letters:
                where.append("(c.color_identity = '[]' OR c.color_identity IS NULL)")
                described.append("colorless")
                letters.discard("C")
            for letter in sorted(letters):
                where.append("c.color_identity LIKE ?")
                params.append(f'%"{letter}"%')
            if letters:
                described.append("id>=" + "".join(sorted(letters)))
        elif key in CMC_KEYS:
            try:
                number = float(val)
            except ValueError:
                raise QueryError(f"cmc filter '{token}' (value must be a number)")
            sql_op = "=" if op == ":" else ("<>" if op == "!=" else op)
            where.append(f"c.cmc {sql_op} ?")
            params.append(number)
            described.append(f"cmc{sql_op}{val}")
        elif key in RARITY_KEYS:
            where.append("lower(c.rarity) = ?")
            params.append(val.lower())
            described.append(f"rarity={val.lower()}")
        elif key in DECK_KEYS:
            deck_slug = val.lower()
            described.append(f"deck={deck_slug}")
        elif key in LEGAL_KEYS:
            mapped = LEGAL_VALUES.get(val.lower())
            if mapped is None:
                raise QueryError(
                    f"legality '{val}' (known: {', '.join(sorted(set(LEGAL_VALUES)))})"
                )
            where.append("c.legal_commander = ?")
            params.append(mapped)
            described.append(f"legal={mapped}")
        elif key in NAME_KEYS:
            where.append("lower(c.name) LIKE ? ESCAPE '\\'")
            params.append(_like(val))
            described.append(f"name~{val}")
        elif key in TEXT_KEYS:
            where.append("lower(c.oracle_text) LIKE ? ESCAPE '\\'")
            params.append(_like(val))
            described.append(f"text~{val}")
        elif key in KEYWORD_KEYS:
            where.append("lower(c.keywords) LIKE ?")
            params.append(f'%"{val.lower()}"%')
            described.append(f"keyword={val}")

    return where, params, bare, deck_slug, described


ORDER_SQL = {
    # NULL EDHREC ranks are cards nobody registers — they sort last, always.
    "edhrec": "(c.edhrec_rank IS NULL), c.edhrec_rank, c.name COLLATE NOCASE",
    "name": "c.name COLLATE NOCASE",
    "cmc": "(c.cmc IS NULL), c.cmc, c.name COLLATE NOCASE",
}


def _truncate(value: str, width: int) -> str:
    value = value or ""
    return value if len(value) <= width else value[: width - 1] + "…"


def _render_table(rows: list, total: int, query: str) -> str:
    if not rows:
        return f"0 matches for: {query}"
    cells = []
    for r in rows:
        cells.append((
            _truncate(r["name"], 38),
            _truncate(r["mana_cost"] or "", 16),
            _truncate((r["type_line"] or "").replace("—", "-"), 34),
            _pt_str(r),
        ))
    widths = [max(len(c[i]) for c in cells) for i in range(4)]
    headers = ("NAME", "COST", "TYPE", "P/T")
    widths = [max(widths[i], len(headers[i])) for i in range(4)]

    def line(vals):
        return " | ".join(v.ljust(widths[i]) for i, v in enumerate(vals)).rstrip()

    out = [line(headers), "-+-".join("-" * w for w in widths)]
    out.extend(line(c) for c in cells)
    out.append("")
    shown = len(rows)
    out.append(f"{total} match{'' if total == 1 else 'es'}"
               + (f" (showing {shown})" if shown < total else ""))
    return "\n".join(out)


def cmd_search(args) -> int:
    as_json = args.json
    query = " ".join(args.query).strip()
    args.limit = _clamp_limit(args.limit)
    if not query:
        return output.fail("search query (nothing to search for)", as_json)
    conn = _open(as_json)
    if conn is None:
        return 1
    try:
        try:
            where, params, bare, deck_slug, described = parse_query(query)
        except QueryError as exc:
            return output.fail(str(exc), as_json)

        joins = ""
        if deck_slug:
            known = conn.execute(
                "SELECT deck_id FROM decks WHERE deck_id = ? COLLATE NOCASE", (deck_slug,)
            ).fetchone()
            if not known:
                slugs = [r[0] for r in conn.execute("SELECT deck_id FROM decks ORDER BY 1")]
                return output.fail(
                    f"deck '{deck_slug}' (known decks: {', '.join(slugs) or 'none'})", as_json
                )
            joins = " JOIN deck_cards dc ON dc.oracle_id = c.oracle_id"
            where.append("dc.deck_id = ?")
            params.append(known[0])

        match = _fts_query(bare)
        if match:
            where.append("c.oracle_id IN (SELECT oracle_id FROM cards_fts WHERE cards_fts MATCH ?)")
            params.append(match)

        if not where:
            return output.fail(
                "usable search terms (try: type:creature color:g cmc<=2)", as_json
            )

        clause = " AND ".join(where)
        cols = ", ".join(f"c.{col}" for col in CARD_COLUMNS)
        order = ORDER_SQL[args.order]
        try:
            total = conn.execute(
                f"SELECT COUNT(DISTINCT c.oracle_id) FROM cards c{joins} WHERE {clause}",
                tuple(params),
            ).fetchone()[0]
            rows = conn.execute(
                f"SELECT DISTINCT {cols} FROM cards c{joins} WHERE {clause} "
                f"ORDER BY {order} LIMIT ?",
                tuple(params) + (args.limit,),
            ).fetchall()
        except sqlite3.OperationalError as exc:
            return output.fail(f"searchable data ({exc})", as_json)

        if not rows:
            return output.fail(f"any card matching '{query}'", as_json)

        payload = {
            "ok": True,
            "count": total,
            "returned": len(rows),
            "query": query,
            "filters": described,
            "text_terms": bare,
            "order": args.order,
            "results": [_row_to_card(r) for r in rows],
        }
        return output.emit(payload, _render_table(rows, total, query), as_json)
    finally:
        conn.close()


# --------------------------------------------------------------------------
# mtg rule
# --------------------------------------------------------------------------

def _rule_dict(row) -> dict:
    return {
        "rule_number": row["rule_number"],
        "section": row["section"],
        "parent_number": row["parent_number"],
        "text": row["text"],
    }


def cmd_rule(args) -> int:
    as_json = args.json
    query = " ".join(args.query).strip()
    args.limit = _clamp_limit(args.limit)
    if not query:
        return output.fail("rule number or search text", as_json)
    conn = _open(as_json)
    if conn is None:
        return 1
    try:
        if RULE_NUMBER_RE.match(query):
            return _rule_exact(conn, query, as_json)
        return _rule_search(conn, query, args.limit, as_json)
    finally:
        conn.close()


def _rule_exact(conn, number: str, as_json: bool) -> int:
    row = conn.execute(
        "SELECT rule_number, section, parent_number, text FROM rules WHERE rule_number = ?",
        (number,),
    ).fetchone()
    if row is None:
        return output.fail(f"rule {number}", as_json)

    children = [
        _rule_dict(r) for r in conn.execute(
            "SELECT rule_number, section, parent_number, text FROM rules "
            "WHERE parent_number = ? ORDER BY LENGTH(rule_number), rule_number",
            (number,),
        ).fetchall()
    ]
    parent = None
    if row["parent_number"]:
        prow = conn.execute(
            "SELECT rule_number, section, parent_number, text FROM rules WHERE rule_number = ?",
            (row["parent_number"],),
        ).fetchone()
        if prow:
            parent = _rule_dict(prow)

    lines = [output.rule(f"Rule {row['rule_number']}", TEXT_WIDTH)]
    if parent:
        head = (parent["text"] or "").replace("\n", " ")
        lines.append(f"parent: {parent['rule_number']} — {_truncate(head, 60)}")
    else:
        lines.append("parent: (top-level section)")
    lines.append("")
    lines.append(output.wrap(row["text"], TEXT_WIDTH))
    lines.append("")
    lines.append(output.rule(f"Subrules ({len(children)})", TEXT_WIDTH))
    if not children:
        lines.append("(none — this rule has no subrules)")
    for child in children:
        lines.append(f"{child['rule_number']}")
        lines.append(output.wrap(child["text"], TEXT_WIDTH - 2, indent="  "))
        lines.append("")
    if children:
        lines.pop()

    payload = {
        "ok": True, "mode": "exact", "rule": _rule_dict(row),
        "parent": parent, "children": children,
    }
    return output.emit(payload, "\n".join(lines), as_json)


def _rule_search(conn, query: str, limit: int, as_json: bool) -> int:
    match = _fts_query(_split_tokens(query))
    if not match:
        return output.fail(f"searchable rule text in '{query}'", as_json)
    try:
        hits = conn.execute(
            "SELECT rule_number FROM rules_fts WHERE rules_fts MATCH ? ORDER BY rank LIMIT ?",
            (match, limit),
        ).fetchall()
        total = conn.execute(
            "SELECT COUNT(*) FROM rules_fts WHERE rules_fts MATCH ?", (match,)
        ).fetchone()[0]
    except sqlite3.OperationalError as exc:
        return output.fail(f"searchable rules ({exc})", as_json)
    if not hits:
        return output.fail(f"any rule mentioning '{query}'", as_json)

    numbers = [h["rule_number"] for h in hits]
    placeholders = ",".join("?" * len(numbers))
    by_number = {
        r["rule_number"]: _rule_dict(r) for r in conn.execute(
            f"SELECT rule_number, section, parent_number, text FROM rules "
            f"WHERE rule_number IN ({placeholders})", tuple(numbers)
        ).fetchall()
    }
    results = [by_number[n] for n in numbers if n in by_number]

    lines = [output.rule(f"Rules matching '{query}'", TEXT_WIDTH)]
    for res in results:
        lines.append(res["rule_number"])
        lines.append(output.wrap(res["text"], TEXT_WIDTH - 2, indent="  "))
        lines.append("")
    lines.append(f"{total} matching rule{'' if total == 1 else 's'}"
                 + (f" (showing {len(results)})" if len(results) < total else ""))

    payload = {"ok": True, "mode": "search", "query": query,
               "count": total, "returned": len(results), "results": results}
    return output.emit(payload, "\n".join(lines), as_json)


# --------------------------------------------------------------------------
# mtg glossary
# --------------------------------------------------------------------------

def _related_rules(conn, definition: str) -> list:
    """Rule numbers referenced by a definition, verified to exist in our rules."""
    found, seen = [], set()
    for candidate in RULE_REF_RE.findall(definition or "") + BARE_RULE_REF_RE.findall(definition or ""):
        if candidate in seen:
            continue
        seen.add(candidate)
        found.append(candidate)
    if not found:
        return []
    placeholders = ",".join("?" * len(found))
    real = {
        r[0] for r in conn.execute(
            f"SELECT rule_number FROM rules WHERE rule_number IN ({placeholders})", tuple(found)
        ).fetchall()
    }
    return [f for f in found if f in real]


def _glossary_lines(conn, term: str, definition: str, related: list) -> list:
    lines = [output.rule(term, TEXT_WIDTH), output.wrap(definition, TEXT_WIDTH)]
    if related:
        lines.append("")
        lines.append("Related rules:")
        for number in related:
            row = conn.execute("SELECT text FROM rules WHERE rule_number = ?", (number,)).fetchone()
            snippet = _truncate((row["text"] or "").replace("\n", " "), 58) if row else ""
            lines.append(f"  {number:<10} {snippet}")
        lines.append("")
        lines.append(f"  (chase them with: mtg rule {related[0]})")
    return lines


def cmd_glossary(args) -> int:
    as_json = args.json
    term = " ".join(args.term).strip()
    args.limit = _clamp_limit(args.limit)
    if not term:
        return output.fail("glossary term", as_json)
    conn = _open(as_json)
    if conn is None:
        return 1
    try:
        row = conn.execute(
            "SELECT term, definition FROM glossary WHERE term = ? COLLATE NOCASE", (term,)
        ).fetchone()
        if row:
            related = _related_rules(conn, row["definition"])
            payload = {"ok": True, "mode": "exact", "term": row["term"],
                       "definition": row["definition"], "related_rules": related}
            return output.emit(
                payload, "\n".join(_glossary_lines(conn, row["term"], row["definition"], related)),
                as_json,
            )

        # No exact term. Widen in stages, narrowest first, so the most literal
        # interpretation always outranks the loosest. glossary_fts indexes only
        # `definition` (term is UNINDEXED), so term matching has to be LIKE.
        hits, seen = [], set()

        def collect(sql, params):
            if len(hits) >= args.limit:
                return None
            try:
                rows = conn.execute(sql, params).fetchall()
            except sqlite3.OperationalError as exc:
                return exc
            for row in rows:
                if row["term"] not in seen:
                    seen.add(row["term"])
                    hits.append(row)
            return None

        words = [w for w in _split_tokens(term) if w]

        # 1. term contains the whole phrase          ("combat damage" -> Combat Damage Step)
        collect(
            "SELECT term, definition FROM glossary WHERE lower(term) LIKE ? ESCAPE '\\' "
            "ORDER BY LENGTH(term), term LIMIT ?", (_like(term), args.limit),
        )
        # 2. definitions mention every word           (full-text, ranked)
        match = _fts_query(words)
        if match:
            err = collect(
                "SELECT g.term, g.definition FROM glossary_fts f "
                "JOIN glossary g ON g.term = f.term "
                "WHERE glossary_fts MATCH ? ORDER BY rank LIMIT ?", (match, args.limit),
            )
            if err is not None:
                return output.fail(f"searchable glossary ({err})", as_json)
        # 3. term contains every word, in any order
        # 4. term contains any word                   ("commander damage" -> Commander, Damage, …)
        if len(words) > 1:
            all_words = " AND ".join(["lower(term) LIKE ? ESCAPE '\\'"] * len(words))
            any_words = " OR ".join(["lower(term) LIKE ? ESCAPE '\\'"] * len(words))
            patterns = [_like(w) for w in words]
            for clause in (all_words, any_words):
                collect(
                    f"SELECT term, definition FROM glossary WHERE {clause} "
                    f"ORDER BY LENGTH(term), term LIMIT ?", tuple(patterns) + (args.limit,),
                )

        if not hits:
            return output.fail(f"glossary term '{term}'", as_json)

        hits = hits[: args.limit]
        results = []
        lines = [output.rule(f"Glossary matches for '{term}'", TEXT_WIDTH),
                 f"(no exact glossary term '{term}' — closest entries below)", ""]
        for row in hits:
            related = _related_rules(conn, row["definition"])
            results.append({"term": row["term"], "definition": row["definition"],
                            "related_rules": related})
            lines.extend(_glossary_lines(conn, row["term"], row["definition"], related))
            lines.append("")
        lines.append(f"{len(results)} glossary entr{'y' if len(results) == 1 else 'ies'} matched")

        payload = {"ok": True, "mode": "search", "query": term,
                   "count": len(results), "results": results}
        if len(results) == 1:
            # Single hit: also expose the flat shape agents expect from an
            # exact lookup, while `mode` still says this was a fuzzy match.
            payload.update(results[0])
        return output.emit(payload, "\n".join(lines), as_json)
    finally:
        conn.close()


# --------------------------------------------------------------------------
# registration
# --------------------------------------------------------------------------

def _add_json_flag(parser) -> None:
    """Accept --json AFTER the subcommand too.

    cli.py puts --json on the root parser, so `mtg card X --json` (the order an
    agent naturally types) would die with argparse exit 2 and print no JSON at
    all — the worst possible failure for a machine caller. default=SUPPRESS is
    load-bearing: without it the subparser's False would overwrite a --json
    already parsed by the root parser.
    """
    parser.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS,
        help="emit machine-readable JSON (also accepted before the subcommand)",
    )


def register(subparsers) -> None:
    card = subparsers.add_parser(
        "card", help="full card text + every official ruling",
        description=(
            "Look up one card. When a name is shared by a real card and a "
            "token/art printing, the real card wins; a token is only returned "
            "when nothing else carries that name."
        ),
    )
    card.add_argument("name", nargs="+", help="card name (unquoted words are joined) or oracle_id")
    card.add_argument("--no-rulings", action="store_true", help="suppress the rulings section")
    _add_json_flag(card)
    card.set_defaults(func=cmd_card)

    search = subparsers.add_parser(
        "search", help="search cards: type: color: cmc<= rarity: deck: legal: is: + free text",
        description=(
            "Structured filters combine with AND; leftover words go to full-text search. "
            "Examples: 'type:creature color:g cmc<=2', 'deck:tidus draw', 'is:land id:gw'."
        ),
    )
    search.add_argument("query", nargs="+", help="query string")
    search.add_argument("--limit", type=int, default=25, help="max rows (default 25)")
    search.add_argument("--order", choices=("name", "cmc", "edhrec"), default="edhrec",
                        help="sort order (default edhrec, NULL ranks last)")
    _add_json_flag(search)
    search.set_defaults(func=cmd_search)

    rules = subparsers.add_parser(
        "rule", help="exact rule number (601.2) or full-text rules search",
        description="A bare rule number does an exact lookup and lists its subrules.",
    )
    rules.add_argument("query", nargs="+", help="rule number (e.g. 601.2) or search text")
    rules.add_argument("--limit", type=int, default=10, help="max search results (default 10)")
    _add_json_flag(rules)
    rules.set_defaults(func=cmd_rule)

    glossary = subparsers.add_parser(
        "glossary", help="official glossary entry + the rules it references",
    )
    glossary.add_argument("term", nargs="+", help="glossary term")
    glossary.add_argument("--limit", type=int, default=10, help="max fallback results (default 10)")
    _add_json_flag(glossary)
    glossary.set_defaults(func=cmd_glossary)
