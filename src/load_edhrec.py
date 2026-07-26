"""Loader: EDHREC commander pages -> edhrec_cache, and the Commander Brackets
reference file -> data/brackets.json.

Two independent jobs live here because they answer the same question from two
sides: "what do people actually play with this commander" (EDHREC) and "how
strong am I allowed to be" (Brackets / Game Changers).

Owned table: edhrec_cache. Nothing else in the DB is touched (other loaders
write the same file concurrently).

Zero third-party imports by design (constraint C6). No LLM/embedding calls
anywhere (constraint C1).

Standalone:
    python3 src/load_edhrec.py            # reuse cached raw files if present
    python3 src/load_edhrec.py --force    # re-download everything
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import db

# --------------------------------------------------------------------------- config

EDHREC_URL = "https://json.edhrec.com/pages/commanders/{slug}.json"
EDHREC_SLEEP = 0.20  # json.edhrec.com is a static CDN, but be polite anyway.

SCRYFALL_GAMECHANGERS_URL = (
    "https://api.scryfall.com/cards/search?q=is%3Agamechanger&format=json"
)
SCRYFALL_SOURCE_LABEL = "https://api.scryfall.com/cards/search?q=is:gamechanger"
SCRYFALL_SLEEP = 0.10  # api.scryfall.com asks for <= ~10 req/s.

# VERIFIED slugs for the three decks this brain is being built around.
# Do not re-derive these from card names at runtime; EDHREC's own slugs win.
COMMANDER_SLUGS = (
    "tidus-yunas-guardian",
    "ms-bumbleflower",
    "dogmeat-ever-loyal",
)

RAW_EDHREC_DIR = db.RAW / "edhrec"
RAW_GAMECHANGERS = db.RAW / "scryfall-gamechangers.json"
BRACKETS_PATH = db.DATA / "brackets.json"

# Punctuation EDHREC drops entirely when building a slug (apostrophes, commas,
# periods -- straight and typographic variants).
_SLUG_DROP = re.compile(r"[’'`,\.\!\?\:\;\"“”\(\)\[\]]")
# Anything else that is not a letter/digit becomes a separator.
_SLUG_SEP = re.compile(r"[^a-z0-9]+")


# --------------------------------------------------------------------------- helpers


def utc_now() -> str:
    """UTC ISO-8601 timestamp, second precision, with explicit Z-style offset."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(name: str) -> str:
    """Commander name -> EDHREC page slug.

    Rule: lowercase, strip punctuation (apostrophes, commas, periods), spaces
    become hyphens.

        "Tidus, Yuna's Guardian" -> "tidus-yunas-guardian"
        "Ms. Bumbleflower"       -> "ms-bumbleflower"
        "Dogmeat, Ever Loyal"    -> "dogmeat-ever-loyal"

    Split cards ("A // B") keep only the front face, which is how EDHREC pages
    for partner/MDFC commanders are addressed.
    """
    text = (name or "").strip().lower()
    if "//" in text:
        text = text.split("//", 1)[0].strip()
    text = _SLUG_DROP.sub("", text)   # punctuation vanishes, no separator left behind
    text = _SLUG_SEP.sub("-", text)   # everything else collapses to single hyphens
    return text.strip("-")


def cardlists(payload) -> list:
    """Safely dig container.json_dict.cardlists out of an EDHREC payload.

    Returns [] for anything unexpected (missing keys, None, wrong types) so CLI
    code can iterate without guarding. Accepts either the parsed dict or a raw
    JSON string.
    """
    if isinstance(payload, (str, bytes, bytearray)):
        try:
            payload = json.loads(payload)
        except (ValueError, TypeError):
            return []
    if not isinstance(payload, dict):
        return []
    container = payload.get("container")
    if not isinstance(container, dict):
        return []
    json_dict = container.get("json_dict")
    if not isinstance(json_dict, dict):
        return []
    lists = json_dict.get("cardlists")
    if not isinstance(lists, list):
        return []
    return [entry for entry in lists if isinstance(entry, dict)]


def cardlist_headers(payload) -> list[str]:
    """Just the section headers of an EDHREC payload, in page order."""
    return [str(entry.get("header") or entry.get("tag") or "?") for entry in cardlists(payload)]


def _http_get(url: str, timeout: int = 60, accept: str | None = None) -> bytes:
    headers = {"User-Agent": db.USER_AGENT}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _read_cached(path: Path) -> bytes | None:
    """Return raw bytes if the cache file exists and is non-empty, else None."""
    try:
        if path.is_file() and path.stat().st_size > 0:
            return path.read_bytes()
    except OSError:
        pass
    return None


# --------------------------------------------------------------------------- part 1: edhrec


def fetch_commander(slug: str, force: bool = False) -> tuple[bytes, bool]:
    """Fetch one EDHREC commander page. Returns (raw_bytes, downloaded?).

    Cached raw JSON in data/raw/edhrec/ is reused unless force=True, which keeps
    rebuilds fast and lets the whole thing run offline.
    """
    RAW_EDHREC_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_EDHREC_DIR / f"{slug}.json"

    if not force:
        cached = _read_cached(path)
        if cached is not None:
            return cached, False

    url = EDHREC_URL.format(slug=slug)
    raw = _http_get(url)
    # Validate before persisting -- a truncated/HTML error body must never land
    # in the cache and poison later offline runs.
    payload = json.loads(raw)
    if not cardlists(payload):
        raise RuntimeError(
            f"EDHREC page for {slug!r} has no container.json_dict.cardlists "
            f"({len(raw)} bytes) -- refusing to cache it."
        )
    path.write_bytes(raw)
    return raw, True


def load_edhrec(conn: sqlite3.Connection, force: bool = False) -> dict:
    """Cache every commander page in COMMANDER_SLUGS into edhrec_cache."""
    rows = []
    per_slug = {}
    downloaded = 0

    for index, slug in enumerate(COMMANDER_SLUGS):
        raw, was_downloaded = fetch_commander(slug, force=force)
        if was_downloaded:
            downloaded += 1
            if index != len(COMMANDER_SLUGS) - 1:
                time.sleep(EDHREC_SLEEP)

        payload = json.loads(raw)
        text = raw.decode("utf-8")
        rows.append((slug, utc_now(), text))
        per_slug[slug] = {
            "bytes": len(text),
            "cardlists": len(cardlists(payload)),
            "headers": cardlist_headers(payload),
            "downloaded": was_downloaded,
        }

    # Upsert, never DELETE: another slug someone else cached earlier stays put.
    conn.executemany(
        "INSERT INTO edhrec_cache(slug, fetched_at, payload_json) VALUES (?, ?, ?) "
        "ON CONFLICT(slug) DO UPDATE SET "
        "  fetched_at=excluded.fetched_at, payload_json=excluded.payload_json",
        rows,
    )
    conn.commit()

    return {"slugs": len(rows), "downloaded": downloaded, "detail": per_slug}


# --------------------------------------------------------------------------- part 2: brackets

BRACKET_DEFINITIONS = {
    "1": {
        "name": "Exhibition",
        "summary": (
            "Ultra-casual. The deck exists to show off a theme or a joke, not to win. "
            "Games go long and everyone gets to do their thing."
        ),
        "allows_game_changers": False,
        "rules": [
            "No Game Changers.",
            "No mass land denial.",
            "No chaining extra turns.",
            "No two-card infinite combos.",
            "Games are expected to go long; winning is not the point.",
        ],
    },
    "2": {
        "name": "Core",
        "summary": (
            "Precon-level. The baseline Commander experience -- a modern preconstructed "
            "deck out of the box lands here."
        ),
        "allows_game_changers": False,
        "rules": [
            "No Game Changers.",
            "No mass land denial.",
            "No chaining extra turns.",
            "No two-card infinite combos.",
            "Power level of a modern precon; games typically end around turn 9 or later.",
        ],
    },
    "3": {
        "name": "Upgraded",
        "summary": (
            "A precon that has been deliberately tuned, or a deck built to beat one. "
            "Stronger cards and tighter curve, still not cutthroat."
        ),
        "allows_game_changers": True,
        "max_game_changers": 3,
        "rules": [
            "Up to 3 Game Changers.",
            "No mass land denial.",
            "No chaining extra turns.",
            "Late-game two-card infinite combos are tolerated.",
            "Noticeably stronger than a precon; games typically end around turn 7 or later.",
        ],
    },
    "4": {
        "name": "Optimized",
        "summary": (
            "High power. The strongest version of the deck you want to play, built "
            "without deck-construction restrictions but not aimed at a tournament metagame."
        ),
        "allows_game_changers": True,
        "rules": [
            "No restrictions: any number of Game Changers.",
            "Mass land denial, extra-turn chains and two-card infinite combos are all allowed.",
            "Built to be as strong as possible within its own strategy.",
            "Not tuned for a competitive metagame -- that is Bracket 5.",
        ],
    },
    "5": {
        "name": "cEDH",
        "summary": (
            "Competitive EDH. Tournament-tuned and metagame-driven: every card is chosen "
            "to win, and to win as fast as possible."
        ),
        "allows_game_changers": True,
        "rules": [
            "No restrictions: any number of Game Changers.",
            "Deckbuilding is driven by the competitive metagame, not by the pilot's preference.",
            "Wins as fast as possible; free interaction and fast mana are expected.",
            "Only the banned list constrains construction.",
        ],
    },
}


def fetch_game_changers(force: bool = False) -> tuple[list[str], bool]:
    """Fetch the CURRENT Game Changers list from Scryfall. Returns (names, downloaded?).

    Never falls back to a remembered list: if Scryfall returns nothing or errors,
    this raises. A silently-stale Game Changers list would mis-bracket decks.
    """
    if not force:
        cached = _read_cached(RAW_GAMECHANGERS)
        if cached is not None:
            names = json.loads(cached)
            if isinstance(names, list) and names:
                return [str(n) for n in names], False

    names: list[str] = []
    url: str | None = SCRYFALL_GAMECHANGERS_URL
    pages = 0

    while url:
        try:
            raw = _http_get(url, accept="application/json")
        except urllib.error.HTTPError as exc:
            body = exc.read()[:400].decode("utf-8", "replace")
            raise RuntimeError(
                f"Scryfall is:gamechanger search failed with HTTP {exc.code} at {url}: {body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Scryfall is:gamechanger search unreachable at {url}: {exc.reason}"
            ) from exc

        page = json.loads(raw)
        if page.get("object") == "error":
            raise RuntimeError(
                f"Scryfall returned an error object for is:gamechanger: {page.get('details')!r}"
            )

        data = page.get("data") or []
        names.extend(str(card["name"]) for card in data if card.get("name"))
        pages += 1

        url = page.get("next_page") if page.get("has_more") else None
        if url:
            time.sleep(SCRYFALL_SLEEP)

    if not names:
        raise RuntimeError(
            "Scryfall is:gamechanger returned 0 cards. Refusing to fall back to a "
            "hardcoded list -- the Game Changers list must come from the live source."
        )

    # De-duplicate defensively (a card could appear twice across pages) but keep
    # Scryfall's ordering stable.
    seen = set()
    unique = [n for n in names if not (n in seen or seen.add(n))]

    RAW_GAMECHANGERS.parent.mkdir(parents=True, exist_ok=True)
    RAW_GAMECHANGERS.write_text(json.dumps(unique, indent=2, ensure_ascii=False), encoding="utf-8")
    return unique, True


def write_brackets(force: bool = False) -> dict:
    """Build data/brackets.json from the live Game Changers list + published criteria."""
    game_changers, downloaded = fetch_game_changers(force=force)

    document = {
        "fetched_at": utc_now(),
        "source": SCRYFALL_SOURCE_LABEL,
        "game_changers": sorted(game_changers, key=str.casefold),
        "brackets": BRACKET_DEFINITIONS,
    }

    BRACKETS_PATH.parent.mkdir(parents=True, exist_ok=True)
    BRACKETS_PATH.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {
        "path": str(BRACKETS_PATH),
        "game_changers": len(document["game_changers"]),
        "downloaded": downloaded,
        "bytes": BRACKETS_PATH.stat().st_size,
    }


# --------------------------------------------------------------------------- entrypoint


def load(conn: sqlite3.Connection, force: bool = False) -> dict:
    """Populate edhrec_cache and write data/brackets.json. Returns a stats dict."""
    db.apply_schema(conn)

    edhrec_stats = load_edhrec(conn, force=force)
    bracket_stats = write_brackets(force=force)

    db.set_meta(conn, "edhrec_loaded_at", utc_now())
    db.set_meta(conn, "edhrec_slugs", str(edhrec_stats["slugs"]))
    db.set_meta(conn, "brackets_game_changers", str(bracket_stats["game_changers"]))

    return {
        "edhrec_rows": edhrec_stats["slugs"],
        "edhrec_downloaded": edhrec_stats["downloaded"],
        "edhrec_detail": edhrec_stats["detail"],
        "brackets_path": bracket_stats["path"],
        "game_changers": bracket_stats["game_changers"],
        "game_changers_downloaded": bracket_stats["downloaded"],
        "brackets_bytes": bracket_stats["bytes"],
    }


def _report(conn: sqlite3.Connection, stats: dict) -> None:
    print("== edhrec_cache ==")
    print(f"{'slug':<24} {'bytes':>8}  fetched_at")
    for row in conn.execute(
        "SELECT slug, length(payload_json) AS n, fetched_at FROM edhrec_cache ORDER BY slug"
    ):
        print(f"{row['slug']:<24} {row['n']:>8}  {row['fetched_at']}")

    print("\n== cardlist headers ==")
    for row in conn.execute("SELECT slug, payload_json FROM edhrec_cache ORDER BY slug"):
        headers = cardlist_headers(row["payload_json"])
        print(f"\n{row['slug']}  ({len(headers)} cardlists)")
        for header in headers:
            print(f"   - {header}")

    document = json.loads(BRACKETS_PATH.read_text(encoding="utf-8"))
    names = document["game_changers"]
    print(f"\n== brackets.json ==\n{BRACKETS_PATH}  ({stats['brackets_bytes']} bytes)")
    print(f"game_changers: {len(names)}")
    print("first 10 alphabetically:")
    for name in names[:10]:
        print(f"   - {name}")
    print("brackets: " + ", ".join(f"{k}={v['name']}" for k, v in document["brackets"].items()))


def main() -> None:
    parser = argparse.ArgumentParser(description="Load EDHREC pages + Commander Brackets.")
    parser.add_argument(
        "--force", action="store_true", help="re-download instead of reusing data/raw/"
    )
    parser.add_argument("--db", default=None, help="override database path")
    args = parser.parse_args()

    conn = db.connect(args.db)
    try:
        stats = load(conn, force=args.force)
        _report(conn, stats)
        print(
            f"\nOK: {stats['edhrec_rows']} edhrec rows "
            f"({stats['edhrec_downloaded']} downloaded), "
            f"{stats['game_changers']} game changers."
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
