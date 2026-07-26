"""Comprehensive Rules + Glossary loader for MTG Brain.

Downloads the current Magic: The Gathering Comprehensive Rules TXT from
magic.wizards.com (discovered dynamically -- the filename carries a release
date that changes every set), parses the numbered rules body and the glossary,
and loads them into the ``rules`` / ``rules_fts`` / ``glossary`` /
``glossary_fts`` tables.

Owns EXACTLY these four tables. Never touches anything else.

Constraints honoured:
  * C1 -- no LLM / embedding / vector-DB calls anywhere. Search is FTS5 only.
  * C6 -- Python stdlib only (re, sqlite3, urllib, pathlib, datetime, ...).

Standalone:
    python3 src/load_rules.py            # load (reuses cached raw file)
    python3 src/load_rules.py --force    # re-download + reload
    python3 src/load_rules.py --verify   # load, then print verification queries
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:  # imported as a package module (``from src import load_rules``)
    from . import db
except ImportError:  # run standalone (``python3 src/load_rules.py``)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import db  # type: ignore[no-redef]


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

RULES_INDEX_URL = "https://magic.wizards.com/en/rules"
MIRROR_URL = "https://yawgatog.com/resources/magic-rules/"

RAW_PATH = db.RAW / "comprehensive-rules.txt"
#: Sidecar recording which URL produced RAW_PATH, so a cached rebuild can still
#: report an accurate ``rules_source_uri`` without touching the network.
RAW_SOURCE_PATH = db.RAW / "comprehensive-rules.source.txt"

#: Matches the leading rule-number token of a rules-body line, e.g.
#:   '1. Game Concepts'      -> '1.'        (section header)
#:   '100. General'          -> '100.'      (subsection header)
#:   '100.1. These Magic ...'-> '100.1.'    (rule)
#:   '601.2a To propose ...' -> '601.2a'    (subrule)
RULE_TOKEN_RE = re.compile(r"^(\d{3}\.\d+[a-z]?\.?|\d{3}\.|\d\.)\s")

#: Robust link matcher for the WotC media host (note the LITERAL SPACE in the
#: real filename -- it must be percent-encoded before the request).
COMP_RULES_TXT_RE = re.compile(
    r"https://media\.wizards\.com/[^\"'<>]*?MagicCompRules[^\"'<>]*?\.txt"
)

EFFECTIVE_RE = re.compile(r"These rules are effective as of\s+([A-Z][a-z]+ \d{1,2}, \d{4})\.")

#: Locale-independent month lookup (``strptime('%B')`` is locale-sensitive).
_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}

# Loud sanity floors -- a structural change upstream must fail, not silently
# load a half-empty table.
MIN_RULES = 2000
MIN_GLOSSARY = 300


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #

def _fetch(url: str, timeout: int = 120) -> bytes:
    """GET ``url`` with the project User-Agent, percent-encoding the path."""
    parts = urllib.parse.urlsplit(url)
    safe = urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            urllib.parse.quote(parts.path),
            parts.query,
            parts.fragment,
        )
    )
    req = urllib.request.Request(safe, headers={"User-Agent": db.USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def discover_rules_url() -> str:
    """Find the current Comprehensive Rules .txt URL. Never hardcodes the date.

    Primary source is the official rules page; the yawgatog mirror is the
    fallback. If neither yields a link this raises -- we never silently proceed
    with a stale or guessed URL.
    """
    errors: list[str] = []

    try:
        html = _fetch(RULES_INDEX_URL, timeout=60).decode("utf-8", "replace")
        hits = COMP_RULES_TXT_RE.findall(html)
        if hits:
            # De-duplicate while preserving order; the page repeats the link in
            # both raw HTML and an escaped JSON blob.
            return list(dict.fromkeys(hits))[0]
        errors.append(f"{RULES_INDEX_URL}: no MagicCompRules .txt link found")
    except Exception as exc:  # noqa: BLE001 - reported via the raise below
        errors.append(f"{RULES_INDEX_URL}: {exc!r}")

    try:
        html = _fetch(MIRROR_URL, timeout=60).decode("utf-8", "replace")
        hits = COMP_RULES_TXT_RE.findall(html)
        if not hits:
            # The mirror may host its own copy with a relative href.
            rel = re.findall(r'href=[\'"]([^\'"<>]*?\.txt)[\'"]', html, re.I)
            rel = [r for r in rel if "rule" in r.lower()]
            hits = [urllib.parse.urljoin(MIRROR_URL, r) for r in rel]
        if hits:
            return list(dict.fromkeys(hits))[0]
        errors.append(f"{MIRROR_URL}: no rules .txt link found")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{MIRROR_URL}: {exc!r}")

    raise RuntimeError(
        "Could not discover the Comprehensive Rules .txt URL from any source:\n  - "
        + "\n  - ".join(errors)
    )


def ensure_raw(force: bool = False) -> tuple[Path, str]:
    """Return ``(path_to_raw_txt, source_uri)``, downloading only when needed.

    A present, non-empty cached file is reused (fast, offline-capable rebuilds)
    unless ``force`` is set.
    """
    if not force and RAW_PATH.exists() and RAW_PATH.stat().st_size > 0:
        if RAW_SOURCE_PATH.exists():
            source = RAW_SOURCE_PATH.read_text(encoding="utf-8").strip()
        else:
            source = RAW_PATH.resolve().as_uri()
        return RAW_PATH, source

    url = discover_rules_url()
    payload = _fetch(url)
    if not payload:
        raise RuntimeError(f"Downloaded an empty body from {url}")

    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_bytes(payload)
    RAW_SOURCE_PATH.write_text(url + "\n", encoding="utf-8")
    return RAW_PATH, url


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #

def parse_effective_date(text: str) -> tuple[str | None, str | None]:
    """Return ``(iso_date, raw_phrase)`` from the 'effective as of' line."""
    m = EFFECTIVE_RE.search(text)
    if not m:
        return None, None
    raw = m.group(1)
    month_name, day, year = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})", raw).groups()
    month = _MONTHS.get(month_name.lower())
    if not month:
        return None, raw
    return f"{int(year):04d}-{month:02d}-{int(day):02d}", raw


def find_boundaries(lines: list[str]) -> tuple[int, int, int, int]:
    """Locate the rules body and glossary spans.

    The document is: intro, a table of Contents (which itself contains lines
    that look exactly like section headers, plus its own 'Glossary'/'Credits'
    entries), 'Credits', the numbered rules body, 'Glossary', the glossary, and
    a final 'Credits'. Anchoring on the standalone 'Credits'/'Glossary' lines
    is what keeps the Contents block out of the parsed rules.

    Returns ``(body_start, body_end, gloss_start, gloss_end)`` as half-open
    line-index ranges.
    """
    glossary_idx = [i for i, l in enumerate(lines) if l.strip() == "Glossary"]
    credits_idx = [i for i, l in enumerate(lines) if l.strip() == "Credits"]
    if not glossary_idx:
        raise RuntimeError("No standalone 'Glossary' line found in the rules file")
    if not credits_idx:
        raise RuntimeError("No standalone 'Credits' line found in the rules file")

    gloss_header = glossary_idx[-1]  # the real section, not the Contents entry
    before = [i for i in credits_idx if i < gloss_header]
    after = [i for i in credits_idx if i > gloss_header]
    if not before:
        raise RuntimeError("No 'Credits' line precedes the Glossary section")
    if not after:
        raise RuntimeError("No trailing 'Credits' line follows the Glossary section")

    body_start = before[-1] + 1
    body_end = gloss_header
    gloss_start = gloss_header + 1
    gloss_end = after[0]
    if not (body_start < body_end < gloss_start < gloss_end):
        raise RuntimeError(
            f"Nonsensical section boundaries: {body_start=} {body_end=} "
            f"{gloss_start=} {gloss_end=}"
        )
    return body_start, body_end, gloss_start, gloss_end


def section_of(rule_number: str) -> str:
    """'601.2a' -> '6';  '100.1' -> '1';  '1' -> '1'."""
    return rule_number[0]


def parent_of(rule_number: str) -> str | None:
    """Trim the last component: letter suffix first, then the last dotted segment.

    '601.2a' -> '601.2'   '601.2' -> '601'   '601' -> '6'   '6' -> None
    """
    if re.fullmatch(r"\d{3}\.\d+[a-z]", rule_number):
        return rule_number[:-1]
    if "." in rule_number:
        return rule_number.rsplit(".", 1)[0]
    if len(rule_number) > 1:  # '601' -> '6'
        return rule_number[0]
    return None  # top-level section


def parse_rules(lines: list[str], start: int, end: int) -> list[tuple[str, str, str | None, str]]:
    """Parse the numbered rules body into ``(number, section, parent, text)`` rows.

    A rule's text wraps onto following lines (indented paragraphs and
    'Example:' lines) until the next numbered line or a blank line; those
    continuations are joined with a single space. Note that some "blank"
    separators in the source are a single space, hence ``.strip()``.
    """
    rows: list[tuple[str, str, str | None, str]] = []
    number: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if number is None:
            return
        text = " ".join(p for p in buf if p).strip()
        rows.append((number, section_of(number), parent_of(number), text))

    for raw in lines[start:end]:
        line = raw.rstrip()
        if not line.strip():          # blank (or whitespace-only) separator
            flush()
            number, buf = None, []
            continue

        m = RULE_TOKEN_RE.match(line)
        if m:
            flush()
            # '100.1.' -> '100.1', '601.2a' -> '601.2a', '1.' -> '1'
            number = m.group(1).rstrip(".")
            buf = [line[m.end():].strip()]
        elif number is not None:
            buf.append(line.strip())  # continuation of the current rule
        # else: stray prose outside any rule -- ignored by design
    flush()
    return rows


def parse_glossary(lines: list[str], start: int, end: int) -> list[tuple[str, str]]:
    """Parse ``(term, definition)`` pairs: a term line, then its definition lines.

    Blocks are separated by blank lines. Multi-line definitions (numbered
    senses, trailing 'See rule ...' pointers) are joined with a single space.
    The term is stored verbatim.
    """
    rows: list[tuple[str, str]] = []
    block: list[str] = []

    def flush() -> None:
        if len(block) < 2:
            return  # a lone line is a stray heading, not a term/definition pair
        term = block[0].strip()
        definition = " ".join(p.strip() for p in block[1:]).strip()
        if term and definition:
            rows.append((term, definition))

    for raw in lines[start:end]:
        if raw.strip():
            block.append(raw)
        else:
            flush()
            block = []
    flush()
    return rows


# --------------------------------------------------------------------------- #
# Load
# --------------------------------------------------------------------------- #

def _executemany_batched(
    conn: sqlite3.Connection, sql: str, rows: list[tuple], batch: int = 500
) -> None:
    """Insert in batches, committing between them so write locks are held briefly."""
    for i in range(0, len(rows), batch):
        conn.executemany(sql, rows[i:i + batch])
        conn.commit()


def load(conn: sqlite3.Connection, force: bool = False) -> dict:
    """Populate rules, rules_fts, glossary, glossary_fts. Returns a stats dict."""
    db.apply_schema(conn)

    raw_path, source_uri = ensure_raw(force=force)
    text = raw_path.read_text(encoding="utf-8-sig")  # BOM-aware; keeps curly quotes
    lines = text.splitlines()

    effective_iso, effective_raw = parse_effective_date(text)
    body_start, body_end, gloss_start, gloss_end = find_boundaries(lines)

    rule_rows = parse_rules(lines, body_start, body_end)
    gloss_rows = parse_glossary(lines, gloss_start, gloss_end)

    # ---- structural guards: fail loudly rather than load a broken corpus ----
    if len(rule_rows) < MIN_RULES:
        raise RuntimeError(f"Only parsed {len(rule_rows)} rules (expected >= {MIN_RULES})")
    if len(gloss_rows) < MIN_GLOSSARY:
        raise RuntimeError(
            f"Only parsed {len(gloss_rows)} glossary terms (expected >= {MIN_GLOSSARY})"
        )
    numbers = {r[0] for r in rule_rows}
    if len(numbers) != len(rule_rows):
        seen, dupes = set(), set()
        for r in rule_rows:
            (dupes if r[0] in seen else seen).add(r[0])
        raise RuntimeError(f"Duplicate rule numbers parsed: {sorted(dupes)[:10]}")
    for canary in ("100.1", "601.2a", "903.1"):
        if canary not in numbers:
            raise RuntimeError(f"Canary rule {canary!r} missing -- parse is wrong")
    if any(n.endswith(".") for n in numbers):
        raise RuntimeError("A rule_number retained a trailing period")

    # ---- write: only the four tables this module owns --------------------
    conn.execute("DELETE FROM rules_fts")
    conn.execute("DELETE FROM rules")
    conn.execute("DELETE FROM glossary_fts")
    conn.execute("DELETE FROM glossary")
    conn.commit()

    _executemany_batched(
        conn,
        "INSERT INTO rules(rule_number, section, parent_number, text) VALUES (?,?,?,?)",
        rule_rows,
    )
    _executemany_batched(
        conn,
        "INSERT INTO rules_fts(rule_number, text) VALUES (?,?)",
        [(r[0], r[3]) for r in rule_rows],
    )
    _executemany_batched(
        conn,
        "INSERT INTO glossary(term, definition) VALUES (?,?)",
        gloss_rows,
    )
    _executemany_batched(
        conn,
        "INSERT INTO glossary_fts(term, definition) VALUES (?,?)",
        gloss_rows,
    )

    orphans = conn.execute(
        "SELECT COUNT(*) FROM rules r WHERE r.parent_number IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM rules p WHERE p.rule_number = r.parent_number)"
    ).fetchone()[0]

    loaded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    db.set_meta(conn, "rules_loaded_at", loaded_at)
    db.set_meta(conn, "rules_source_uri", source_uri)
    if effective_iso:
        db.set_meta(conn, "rules_effective_date", effective_iso)
    db.set_meta(conn, "rules_count", str(len(rule_rows)))
    db.set_meta(conn, "glossary_count", str(len(gloss_rows)))

    return {
        "source_uri": source_uri,
        "raw_path": str(raw_path),
        "raw_bytes": raw_path.stat().st_size,
        "effective_date": effective_iso,
        "effective_date_raw": effective_raw,
        "rules_count": len(rule_rows),
        "rules_fts_count": len(rule_rows),
        "glossary_count": len(gloss_rows),
        "sections": len({r[1] for r in rule_rows}),
        "orphan_parents": orphans,
        "loaded_at": loaded_at,
        "forced": force,
    }


# --------------------------------------------------------------------------- #
# Standalone verification
# --------------------------------------------------------------------------- #

VERIFY_QUERIES: list[tuple[str, str]] = [
    ("rules row count", "SELECT COUNT(*) FROM rules"),
    ("glossary row count", "SELECT COUNT(*) FROM glossary"),
    ("rules_fts row count", "SELECT COUNT(*) FROM rules_fts"),
    ("glossary_fts row count", "SELECT COUNT(*) FROM glossary_fts"),
    (
        "rule 601.2",
        "SELECT rule_number, section, parent_number, substr(text,1,120) "
        "FROM rules WHERE rule_number='601.2'",
    ),
    ("rule 601.2a parent", "SELECT rule_number, parent_number FROM rules WHERE rule_number='601.2a'"),
    ("rule 509.1b text", "SELECT text FROM rules WHERE rule_number='509.1b'"),
    (
        "glossary Deathtouch",
        "SELECT term, substr(definition,1,100) FROM glossary WHERE term LIKE 'Deathtouch%'",
    ),
    (
        "FTS 'commander damage'",
        "SELECT COUNT(*) FROM rules_fts WHERE rules_fts MATCH 'commander damage'",
    ),
    ("rule_numbers ending in '.' (must be 0)", "SELECT COUNT(*) FROM rules WHERE rule_number LIKE '%.'"),
    (
        "orphan parent_number (must be 0)",
        "SELECT COUNT(*) FROM rules r WHERE r.parent_number IS NOT NULL "
        "AND NOT EXISTS (SELECT 1 FROM rules p WHERE p.rule_number = r.parent_number)",
    ),
    (
        "build_meta",
        "SELECT key, value FROM build_meta WHERE key LIKE 'rules_%' OR key='glossary_count' "
        "ORDER BY key",
    ),
]


def verify(conn: sqlite3.Connection) -> None:
    for label, sql in VERIFY_QUERIES:
        print(f"\n-- {label}\n   {sql}")
        for row in conn.execute(sql).fetchall():
            print("   ->", tuple(row))


def main() -> int:
    ap = argparse.ArgumentParser(description="Load the MTG Comprehensive Rules + Glossary.")
    ap.add_argument("--force", action="store_true", help="re-download the source txt and reload")
    ap.add_argument("--verify", action="store_true", help="print verification queries after loading")
    ap.add_argument("--db", default=None, help="override the database path")
    args = ap.parse_args()

    conn = db.connect(args.db)
    try:
        stats = load(conn, force=args.force)
        print("load_rules stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        if args.verify:
            verify(conn)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
