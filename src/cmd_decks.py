"""Deck inspection commands: `mtg deck`, `mtg deck stats`, `mtg deck bracket`,
`mtg edhrec`.

Everything here is offline and deterministic (constraints C1/C6): sqlite3 + the
stdlib only, no network, no third-party imports. EDHREC data is read from the
`edhrec_cache` table that `mtg rebuild` populated — this module never fetches.

Commander (EDH) is the only format modelled (C3): a deck is 99 maindeck cards
plus exactly one commander, and the bracket system is the Commander bracket
system from data/brackets.json.

Role classification is regex-based and lives in ROLE_PATTERNS below so it is
auditable and tunable. It is a heuristic, not an oracle — a card can hold
several roles at once, so the role counts are deliberately NOT a partition of
the deck.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

import db
import output

BRACKETS_PATH = db.DATA / "brackets.json"

# ---------------------------------------------------------------- card types
# Priority order matters: the FIRST match wins, so 'Artifact Creature' is a
# Creature and 'Enchantment Creature — Saga' is a Creature, not an Enchantment.
TYPE_ORDER = (
    "Commander",
    "Creature",
    "Planeswalker",
    "Instant",
    "Sorcery",
    "Artifact",
    "Enchantment",
    "Battle",
    "Land",
)
# 'Commander' is a board, not a type_line word, so it is not probed here.
TYPE_PROBES = TYPE_ORDER[1:]

COLOR_ORDER = ("W", "U", "B", "R", "G")
COLOR_NAMES = {
    "W": "White",
    "U": "Blue",
    "B": "Black",
    "R": "Red",
    "G": "Green",
}
BASIC_TYPE_COLOR = {
    "Plains": "W",
    "Island": "U",
    "Swamp": "B",
    "Mountain": "R",
    "Forest": "G",
}

# --------------------------------------------------------------- mana / land
# "{T}: Add {G} or {W}."  /  "Add {G}{G}, {G}{U}, or {U}{U}."  /  "Add {C}{C}."
# Captures the run of mana symbols + separators that follows the word "Add",
# stopping at the first period.
ADD_CLAUSE_RE = re.compile(
    r"\badd\b((?:\s*\{[^}]{1,8}\}|\s*,|\s+or\b|\s+and\b)+)", re.I
)
MANA_SYMBOL_RE = re.compile(r"\{([^}]{1,8})\}")
# Command Tower / Path of Ancestry / Exotic Orchard style: colour is decided at
# resolution, so it is scored against the deck's own colour identity.
ANY_COLOR_RE = re.compile(r"\badd\b[^.\n]{0,60}?\bany color\b", re.I)
ENTERS_TAPPED_RE = re.compile(r"enters (?:the battlefield )?tapped", re.I)
CONDITIONAL_TAP_RE = re.compile(r"\bunless\b|\bif you don'?t\b", re.I)


def _c(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.I)


# ------------------------------------------------------------------- roles
# EDIT THIS DICT to retune role detection — nothing else needs to change.
#
#   include : if ANY regex hits, the card holds the role.
#   exclude : these phrases are BLANKED OUT of the oracle text before the
#             include patterns run, so a card whose only "match" was an
#             excluded phrase does not score (e.g. "can't be countered" must
#             not read as interaction; "double strike" must not read as a
#             wincon).
#   predicate : optional non-textual test (card stats) OR'd with the regexes.
#
# Deliberate deviation from a naive reading of the brief, documented so it is
# auditable: 'each creature' as a boardwipe signal is narrowed to destructive
# contexts ("destroy each creature", "each creature gets -X/-X", ...). The bare
# phrase would score every anthem ("each creature you control gets +1/+1") as a
# wipe, which would mislead the Deck Doctor in the opposite direction.
#
# Roles are scored over NON-LAND cards only (plus the commander). A land that
# taps for mana is mana base, not ramp.
#
# Two further precision fixes, both learned by auditing the real precons:
#   * reminder text (anything in parentheses) is stripped before matching, so
#     "An Offer You Can't Refuse" is not scored as ramp merely because the
#     Treasure reminder says "Add one mana of any color";
#   * "land" is not the only word for a land — Farseek and Three Visits never
#     say it, they name basic land TYPES. LAND_WORD covers both.
LAND_WORD = r"(?:land|plains|island|swamp|mountain|forest)"
REMINDER_RE = re.compile(r"\([^)]*\)")

ROLE_PATTERNS = {
    "ramp": {
        "blurb": "accelerates or fixes mana (land fetch, mana rocks, dorks, Treasure)",
        "include": [
            # "your library" matters: Path to Exile ramps the OPPONENT.
            _c(rf"search your library for[^.\n]{{0,40}}{LAND_WORD}"),
            _c(r"\badd \{[wubrgc]"),
            _c(r"\badd (?:one|two|three|four|five|x|\d+) mana\b"),
            _c(r"\btreasure tokens?\b"),
            _c(rf"\b{LAND_WORD} card[^.\n]{{0,30}}from your hand onto the battlefield"),
            _c(r"\bplay an additional land\b"),
            _c(r"\bmana of any (?:one )?color\b"),
        ],
        # Treasures handed to an opponent are not your ramp.
        "exclude": [
            _c(r"(?:its controller|that player|each opponent|target (?:player|opponent))"
               r"[^.\n]{0,60}treasure tokens?")
        ],
    },
    "draw": {
        "blurb": "refills the hand",
        "include": [
            _c(r"\bdraws? (?:a|one|two|three|four|five|six|seven|x|\d+) cards?\b"),
            _c(r"\bdraws? that many cards?\b"),
            _c(r"\bdraw cards? equal to\b"),
            # Clues ARE draw, but the "Draw a card" only appears in the
            # reminder text this module strips, so match the keyword itself.
            _c(r"\binvestigates?\b"),
            _c(r"\bclue tokens?\b"),
        ],
        "exclude": [],
    },
    "removal": {
        "blurb": "answers a single permanent or player",
        "include": [
            _c(r"\bdestroy target\b"),
            _c(r"\bexile target\b"),
            _c(r"\bdeals? (?:\d+|x) damage to target\b"),
            _c(r"\bdeals? (?:\d+|x) damage to any target\b"),
            _c(r"\btarget creature gets [-−]"),
            _c(r"\bsacrifices? a creature\b"),
            _c(r"\btarget (?:player|opponent) sacrifices\b"),
            _c(r"\bfights? target\b"),
        ],
        # Exiling a card out of a graveyard is graveyard hate, not removal.
        "exclude": [_c(r"exile target[^.\n]{0,40}from a(?:ny)? graveyard")],
    },
    "boardwipe": {
        "blurb": "sweeps multiple permanents at once",
        "include": [
            _c(r"\bdestroy all\b"),
            _c(r"\bexile all\b"),
            _c(r"\bdestroy each\b"),
            _c(r"\bexile each\b"),
            _c(r"\ball creatures get [-−]"),
            _c(r"\beach creature gets [-−]"),
            _c(r"\beach player[^.\n]{0,60}sacrifices\b"),
            _c(r"\beach opponent[^.\n]{0,60}sacrifices\b"),
            _c(r"\ball creatures? (?:are|is) (?:destroyed|sacrificed)\b"),
        ],
        "exclude": [],
    },
    "interaction": {
        "blurb": "counterspells and defensive protection",
        "include": [
            _c(r"\bcounter target\b"),
            _c(r"\bprotection from\b"),
            _c(r"\bhexproof\b"),
            _c(r"\bindestructible\b"),
            _c(r"\bprevent[^.\n]{0,30}damage\b"),
            _c(r"\bphases? out\b"),
        ],
        # "can't be countered" is explicitly NOT interaction.
        "exclude": [_c(r"can[’']?t be countered")],
    },
    "recursion": {
        "blurb": "brings cards back from the graveyard",
        "include": [
            _c(r"\breturn target [^.\n]{0,40}from your graveyard\b"),
            _c(r"\bfrom your graveyard to your hand\b"),
            _c(r"\breturn[^.\n]{0,40}from your graveyard to the battlefield\b"),
            _c(r"\bfrom your graveyard to the battlefield\b"),
        ],
        "exclude": [],
    },
    "tutor": {
        "blurb": "searches the library for a NON-land card",
        # Negative lookahead keeps land-fetch out of the tutor column; those
        # cards are already counted as ramp. LAND_WORD, not just "land", so
        # Farseek ("a Plains, Island, Swamp, or Mountain card") is excluded too.
        "include": [
            _c(rf"search your library for (?:a|an)\b(?![^.\n]{{0,40}}{LAND_WORD})")
        ],
        "exclude": [],
    },
    "wincon": {
        "blurb": "closes the game (alt-win, extra combats, doublers, big bodies)",
        "include": [
            _c(r"\byou win the game\b"),
            _c(r"\bloses the game\b"),
            _c(r"\binfinite\b"),
            _c(r"\btake an extra turn\b"),
            _c(r"\ban additional combat phase\b"),
            _c(r"\bextra combat phase\b"),
            _c(r"\bdoubl(?:e|es|ed|ing)\b"),
            _c(r"\btwice that many\b"),
        ],
        # "double strike" is a keyword, not a payoff doubler.
        "exclude": [_c(r"double strike")],
        # Big finisher: a 6+ MV creature with 6+ power.
        "predicate": lambda card: (
            "creature" in (card["type_line"] or "").lower()
            and (card["cmc"] or 0) >= 6
            and _int_or_none(card["power"]) is not None
            and _int_or_none(card["power"]) >= 6
        ),
    },
}

ROLE_ORDER = (
    "ramp",
    "draw",
    "removal",
    "boardwipe",
    "interaction",
    "recursion",
    "tutor",
    "wincon",
)

ROLES_NOTE = (
    "Roles overlap by design — one card can be counted in several columns "
    "(Cultivate is ramp AND tutor-shaped), so these numbers do NOT sum to the "
    "deck size and are not a partition. Scored over non-land cards only, "
    "commander included."
)

# --------------------------------------------------------- bracket heuristics
MASS_LAND_DENIAL_RE = [
    _c(r"\bdestroy all lands\b"),
    _c(r"\beach player sacrifices a land\b"),
    _c(r"\beach opponent sacrifices a land\b"),
    _c(r"\bdestroy all nonbasic lands\b"),
    _c(r"\blands? (?:don'?t|doesn'?t) untap\b"),
]
EXTRA_TURNS_RE = [
    _c(r"\btake an extra turn\b"),
    _c(r"\btakes? (?:an|two|three|\d+) extra turns?\b"),
]
# "Perch Protection" GIFTS the extra turn to an opponent — that is not an
# extra-turn chain, it is a drawback. Blanked before the patterns above run.
EXTRA_TURNS_EXCLUDE_RE = [
    _c(r"(?:they|that player|target (?:player|opponent)|each opponent|an opponent)"
       r"[^.\n]{0,30}takes? an extra turn"),
]

INFINITE_COMBO_VERDICT = (
    "not detected by this tool; requires human/agent review"
)


# =============================================================== small helpers
def _int_or_none(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _slugify(name: str) -> str:
    """Commander name -> EDHREC page slug (same rule as the loader)."""
    text = (name or "").strip().lower()
    if "//" in text:
        text = text.split("//", 1)[0].strip()
    text = re.sub(r"[’'`,\.\!\?\:\;\"“”\(\)\[\]]", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _norm_name(name: str) -> str:
    """Normalised card name for cross-referencing lists against a decklist."""
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def _name_keys(name: str) -> set:
    """Full name plus the front face, so 'A // B' matches either spelling."""
    keys = {_norm_name(name)}
    if "//" in (name or ""):
        keys.add(_norm_name(name.split("//", 1)[0]))
    return {k for k in keys if k}


def _fmt_mv(value) -> str:
    value = float(value or 0)
    return str(int(value)) if value == int(value) else f"{value:g}"


def _trunc(text: str, width: int) -> str:
    """Pad to width, marking a cut with '…' so a clipped mana cost like
    '{5}{W}{W} // {' never reads as real data."""
    text = text or ""
    if len(text) > width:
        text = text[: width - 1] + "…"
    return f"{text:<{width}}"


def _card_type_group(type_line: str) -> str:
    tl = type_line or ""
    for probe in TYPE_PROBES:
        if probe.lower() in tl.lower():
            return probe
    return "Other"


def _cmc_bucket(cmc) -> str:
    value = int(float(cmc or 0))
    return "7+" if value >= 7 else str(value)


CURVE_BUCKETS = ("0", "1", "2", "3", "4", "5", "6", "7+")


def _color_group(identity: list) -> str:
    if not identity:
        return "Colorless"
    if len(identity) > 1:
        return "Multicolor"
    return COLOR_NAMES.get(identity[0], identity[0])


COLOR_GROUP_ORDER = [COLOR_NAMES[c] for c in COLOR_ORDER] + ["Multicolor", "Colorless"]


# ============================================================ deck resolution
def _all_decks(conn: sqlite3.Connection) -> list:
    return conn.execute(
        "SELECT deck_id, name, set_code, release_date, commander_name, source_file "
        "FROM decks ORDER BY deck_id"
    ).fetchall()


def _valid_slugs(rows) -> str:
    return ", ".join(f"'{r['deck_id']}'" for r in rows) or "(none loaded)"


def resolve_deck(conn: sqlite3.Connection, token: str):
    """Slug, or a case-insensitive prefix of the deck / commander name.

    Returns (deck_row, error_message). Exactly one of the two is None.
    """
    rows = _all_decks(conn)
    needle = (token or "").strip().lower()
    if not needle:
        return None, f"no deck given — valid slugs: {_valid_slugs(rows)}"

    for row in rows:  # exact slug
        if row["deck_id"].lower() == needle:
            return row, None
    for row in rows:  # exact deck name / commander name
        if needle in {row["name"].lower(), (row["commander_name"] or "").lower()}:
            return row, None

    hits = [
        row
        for row in rows
        if row["deck_id"].lower().startswith(needle)
        or row["name"].lower().startswith(needle)
        or (row["commander_name"] or "").lower().startswith(needle)
    ]
    if not hits:  # last resort: substring anywhere
        hits = [
            row
            for row in rows
            if needle in row["deck_id"].lower()
            or needle in row["name"].lower()
            or needle in (row["commander_name"] or "").lower()
        ]

    if len(hits) == 1:
        return hits[0], None
    if len(hits) > 1:
        names = ", ".join(f"'{r['deck_id']}'" for r in hits)
        return None, f"deck '{token}' is ambiguous — matches {names}"
    return None, f"deck '{token}' — valid slugs: {_valid_slugs(rows)}"


def deck_rows(conn: sqlite3.Connection, deck_id: str) -> list:
    """Every card in the deck, both boards, with the fields the commands need."""
    return conn.execute(
        """
        SELECT dc.count, dc.board, c.oracle_id, c.name, c.mana_cost, c.cmc,
               c.type_line, c.oracle_text, c.colors, c.color_identity, c.keywords,
               c.power, c.toughness, c.layout, c.rarity, c.edhrec_rank, c.price_usd
        FROM deck_cards dc
        JOIN cards c ON c.oracle_id = dc.oracle_id
        WHERE dc.deck_id = ?
        ORDER BY c.cmc, c.name
        """,
        (deck_id,),
    ).fetchall()


def _deck_meta(deck, cards) -> dict:
    identity = set()
    for card in cards:
        identity.update(output.json_list(card["color_identity"]))
    return {
        "slug": deck["deck_id"],
        "name": deck["name"],
        "set_code": deck["set_code"],
        "release_date": deck["release_date"],
        "commander": deck["commander_name"],
        "color_identity": [c for c in COLOR_ORDER if c in identity],
        "total_cards": sum(r["count"] for r in cards),
    }


def _is_land(card) -> bool:
    return "land" in (card["type_line"] or "").lower()


# =================================================================== mtg deck
def _entry(card, board) -> dict:
    return {
        "count": card["count"],
        "name": card["name"],
        "mana_cost": card["mana_cost"] or "",
        "cmc": float(card["cmc"] or 0),
        "type_line": card["type_line"] or "",
        "color_identity": output.json_list(card["color_identity"]),
        "board": board,
    }


def _build_groups(cards, mode: str):
    """-> (ordered list of (group_name, [entry,...]), subtotal dict)."""
    buckets: dict[str, list] = {}
    for card in cards:
        entry = _entry(card, card["board"])
        if card["board"] == "commander":
            key = "Commander"
        elif mode == "cmc":
            # Lands get their own bucket rather than piling into MV 0, so this
            # view matches the curve `mtg deck stats` reports.
            key = "Land" if _is_land(card) else f"MV {_cmc_bucket(card['cmc'])}"
        elif mode == "color":
            key = _color_group(entry["color_identity"])
        else:
            key = _card_type_group(card["type_line"])
        buckets.setdefault(key, []).append(entry)

    for entries in buckets.values():
        entries.sort(key=lambda e: (e["cmc"], e["name"]))

    if mode == "cmc":
        order = ["Commander"] + [f"MV {b}" for b in CURVE_BUCKETS] + ["Land"]
    elif mode == "color":
        order = ["Commander"] + COLOR_GROUP_ORDER
    else:
        order = list(TYPE_ORDER) + ["Other"]

    ordered = [(name, buckets[name]) for name in order if name in buckets]
    placed = {name for name, _ in ordered}
    ordered += [(name, entries) for name, entries in buckets.items() if name not in placed]
    subtotals = {name: sum(e["count"] for e in entries) for name, entries in ordered}
    return ordered, subtotals


def _render_deck(meta, ordered, subtotals, total) -> str:
    lines = [output.rule(meta["name"])]
    lines.append(f"Commander : {meta['commander']}")
    lines.append(
        f"Set       : {meta['set_code']}   released {meta['release_date']}   "
        f"identity {''.join(meta['color_identity']) or 'C'}"
    )
    lines.append("")
    for name, entries in ordered:
        lines.append(output.rule(f"{name} ({subtotals[name]})"))
        for e in entries:
            lines.append(
                f"  {e['count']}x {_trunc(e['name'], 32)} {_trunc(e['mana_cost'], 20)} "
                f"{e['type_line']}"
            )
        lines.append("")
    lines.append(output.rule())
    widest = max((len(n) for n, _ in ordered), default=10)
    for name, _entries in ordered:
        lines.append(f"  {name:<{widest}} {subtotals[name]:>3}")
    lines.append(f"  {'TOTAL':<{widest}} {total:>3}" + ("  ✓ 99 + commander" if total == 100 else "  ⚠ expected 100"))
    return "\n".join(lines)


def cmd_deck_list(args, conn, deck) -> int:
    cards = deck_rows(conn, deck["deck_id"])
    meta = _deck_meta(deck, cards)
    ordered, subtotals = _build_groups(cards, args.group)
    total = sum(subtotals.values())
    payload = {
        "ok": True,
        "deck": meta,
        "grouped_by": args.group,
        "groups": {name: entries for name, entries in ordered},
        "subtotals": subtotals,
        "total": total,
    }
    return output.emit(payload, _render_deck(meta, ordered, subtotals, total), args.json)


# ============================================================= mtg deck stats
def land_color_sources(card, deck_colors) -> dict:
    """What colours THIS land can produce, plus how it enters.

    Detection is textual: mana symbols in an "Add ..." clause, basic land types
    in the type line, and 'any color' wording scored against the deck's own
    colour identity.
    """
    text = card["oracle_text"] or ""
    type_line = card["type_line"] or ""
    colors, colorless, flexible = set(), False, False

    for basic, color in BASIC_TYPE_COLOR.items():
        if re.search(rf"\b{basic}\b", type_line):
            colors.add(color)

    for clause in ADD_CLAUSE_RE.findall(text):
        for symbol in MANA_SYMBOL_RE.findall(clause):
            for char in symbol.upper():
                if char in COLOR_ORDER:
                    colors.add(char)
                elif char == "C":
                    colorless = True

    if ANY_COLOR_RE.search(text):
        flexible = True
        colors.update(deck_colors)

    tapped = bool(ENTERS_TAPPED_RE.search(text))
    conditional = False
    if tapped:
        for sentence in re.split(r"(?<=\.)\s+", text):
            if ENTERS_TAPPED_RE.search(sentence):
                conditional = bool(CONDITIONAL_TAP_RE.search(sentence))
                break
    return {
        "colors": [c for c in COLOR_ORDER if c in colors],
        "colorless": colorless,
        "any_color": flexible,
        "enters_tapped": tapped,
        "enters_tapped_conditional": conditional,
    }


def classify_roles(card) -> list:
    """Which ROLE_PATTERNS keys this card satisfies (a card may hold several).

    Reminder text (parenthesised) is dropped first: it restates rules that are
    not this card's own effect and is a large source of false positives.
    """
    text = REMINDER_RE.sub(" ", card["oracle_text"] or "")
    held = []
    for role in ROLE_ORDER:
        spec = ROLE_PATTERNS[role]
        scrubbed = text
        for pattern in spec.get("exclude", []):
            scrubbed = pattern.sub(" ", scrubbed)
        hit = any(pattern.search(scrubbed) for pattern in spec["include"])
        if not hit:
            predicate = spec.get("predicate")
            hit = bool(predicate and predicate(card))
        if hit:
            held.append(role)
    return held


def _recommended_lands(avg_mv: float, ramp: int):
    """Transparent EDH land heuristic. ~37-38 lands at avg MV 3.0-3.3."""
    if avg_mv < 2.80:
        low, high, band = 33, 35, "avg MV under 2.8 (very low curve)"
    elif avg_mv < 3.00:
        low, high, band = 35, 37, "avg MV 2.8-3.0 (low curve)"
    elif avg_mv <= 3.30:
        low, high, band = 37, 38, "avg MV 3.0-3.3 (the usual EDH band)"
    elif avg_mv <= 3.60:
        low, high, band = 38, 39, "avg MV 3.3-3.6 (high curve)"
    else:
        low, high, band = 39, 41, "avg MV above 3.6 (very high curve)"
    ramp_adjust = -1 if ramp >= 10 else 0
    return low + ramp_adjust, high + ramp_adjust, band, ramp_adjust


def _bullet(text: str, width: int = 70) -> str:
    """'- text' with a hanging indent, so wrapped lines line up under the text."""
    body = output.wrap(text, width - 4, "    ")
    return "  - " + body[4:] if body.startswith("    ") else "  - " + body


def _bar(count: int, peak: int, width: int = 34) -> str:
    if peak <= 0:
        return ""
    return "█" * max(1, round(count * width / peak)) if count else ""


def compute_stats(conn, deck) -> dict:
    cards = deck_rows(conn, deck["deck_id"])
    meta = _deck_meta(deck, cards)
    deck_colors = meta["color_identity"]

    commander = [c for c in cards if c["board"] == "commander"]
    main = [c for c in cards if c["board"] == "main"]
    lands = [c for c in main if _is_land(c)]
    nonlands = [c for c in main if not _is_land(c)]

    n_lands = sum(c["count"] for c in lands)
    n_nonlands = sum(c["count"] for c in nonlands)
    n_commander = sum(c["count"] for c in commander)

    # ---- curve (maindeck non-lands; the commander is always available and is
    # reported separately rather than skewing the curve).
    curve = {bucket: 0 for bucket in CURVE_BUCKETS}
    for card in nonlands:
        curve[_cmc_bucket(card["cmc"])] += card["count"]

    mv_nonland = sum(float(c["cmc"] or 0) * c["count"] for c in nonlands)
    mv_all = mv_nonland + sum(float(c["cmc"] or 0) * c["count"] for c in lands)
    avg_nonland = round(mv_nonland / n_nonlands, 2) if n_nonlands else 0.0
    avg_all = round(mv_all / (n_lands + n_nonlands), 2) if (n_lands + n_nonlands) else 0.0

    # ---- colour breakdown over every card (commander included)
    card_colors = {c: 0 for c in COLOR_ORDER}
    colorless_cards = 0
    for card in cards:
        identity = output.json_list(card["color_identity"])
        if not identity:
            colorless_cards += card["count"]
        for color in identity:
            if color in card_colors:
                card_colors[color] += card["count"]

    sources = {c: {"lands": 0, "cards": []} for c in COLOR_ORDER}
    colorless_sources, any_color_lands = 0, []
    tapped_total = tapped_uncond = tapped_cond = 0
    tapped_cards = []
    for card in lands:
        info = land_color_sources(card, deck_colors)
        for color in info["colors"]:
            sources[color]["lands"] += card["count"]
            sources[color]["cards"].append(card["name"])
        if info["colorless"]:
            colorless_sources += card["count"]
        if info["any_color"]:
            any_color_lands.append(card["name"])
        if info["enters_tapped"]:
            tapped_total += card["count"]
            tapped_cards.append(card["name"])
            if info["enters_tapped_conditional"]:
                tapped_cond += card["count"]
            else:
                tapped_uncond += card["count"]

    # ---- roles (non-lands + commander)
    role_cards = nonlands + [c for c in commander if not _is_land(c)]
    roles = {role: {"count": 0, "cards": []} for role in ROLE_ORDER}
    for card in role_cards:
        label = card["name"] + (" (commander)" if card["board"] == "commander" else "")
        if card["count"] > 1:
            label = f"{card['count']}x {label}"
        for role in classify_roles(card):
            roles[role]["count"] += card["count"]
            roles[role]["cards"].append(label)
    for role in roles:
        roles[role]["cards"].sort()
        roles[role]["blurb"] = ROLE_PATTERNS[role]["blurb"]

    # ---- assessment
    low, high, band, ramp_adjust = _recommended_lands(avg_nonland, roles["ramp"]["count"])
    if n_lands < low:
        verdict, ok = "LIGHT on lands", False
    elif n_lands > high:
        verdict, ok = "HEAVY on lands", False
    else:
        verdict, ok = "SANE", True
    notes = [
        f"Average mana value of the {n_nonlands} maindeck non-lands is {avg_nonland:.2f} — {band}.",
        f"The usual EDH heuristic puts that at {low}-{high} lands"
        + (f" (adjusted -1 for {roles['ramp']['count']} ramp pieces)" if ramp_adjust else "")
        + f". This deck runs {n_lands}.",
    ]
    if ok:
        notes.append(f"{n_lands} lands is inside {low}-{high}: the mana base matches the curve.")
    elif n_lands < low:
        notes.append(
            f"{n_lands} lands is {low - n_lands} below the {low}-{high} band — expect to miss land "
            f"drops unless the {roles['ramp']['count']} ramp pieces come down early."
        )
    else:
        notes.append(
            f"{n_lands} lands is {n_lands - high} above the {low}-{high} band — expect flood; "
            f"consider trimming for card advantage (deck has {roles['draw']['count']} draw pieces)."
        )
    notes.append(
        f"Total mana sources = {n_lands} lands + {roles['ramp']['count']} ramp = "
        f"{n_lands + roles['ramp']['count']}."
    )
    if tapped_total:
        notes.append(
            f"{tapped_total} lands can enter tapped ({tapped_uncond} always, "
            f"{tapped_cond} conditionally) — {round(100 * tapped_total / n_lands)}% of the mana base."
        )
    thin = [
        c for c in deck_colors
        if sources[c]["lands"] < 10 and card_colors[c] >= 10
    ]
    if thin:
        notes.append(
            "Colour-source warning: "
            + "; ".join(
                f"{COLOR_NAMES[c]} has {sources[c]['lands']} sources for {card_colors[c]} cards"
                for c in thin
            )
            + "."
        )

    return {
        "ok": True,
        "deck": meta,
        "totals": {
            "cards": n_lands + n_nonlands + n_commander,
            "maindeck": n_lands + n_nonlands,
            "commander": n_commander,
            "lands": n_lands,
            "nonlands": n_nonlands,
        },
        "curve": {
            "buckets": curve,
            "note": "maindeck non-lands only; the commander is listed separately",
            "peak_bucket": max(curve, key=lambda b: curve[b]) if n_nonlands else None,
            "peak_count": max(curve.values()) if n_nonlands else 0,
        },
        "mana_value": {
            "avg_nonland": avg_nonland,
            "avg_including_lands": avg_all,
            "total_mv_nonland": round(mv_nonland, 2),
            "commander_mv": float(commander[0]["cmc"] or 0) if commander else None,
        },
        "colors": {
            "identity": deck_colors,
            "cards_per_color": card_colors,
            "colorless_cards": colorless_cards,
            "sources_per_color": {c: sources[c]["lands"] for c in COLOR_ORDER},
            "source_lands": {c: sorted(set(sources[c]["cards"])) for c in COLOR_ORDER},
            "colorless_sources": colorless_sources,
            "any_color_lands": sorted(set(any_color_lands)),
            "lands_enter_tapped": tapped_total,
            "lands_enter_tapped_always": tapped_uncond,
            "lands_enter_tapped_conditional": tapped_cond,
            "lands_enter_tapped_cards": sorted(set(tapped_cards)),
        },
        "roles": roles,
        "roles_note": ROLES_NOTE,
        "assessment": {
            "recommended_lands_low": low,
            "recommended_lands_high": high,
            "actual_lands": n_lands,
            "ramp_adjustment": ramp_adjust,
            "curve_band": band,
            "land_count_ok": ok,
            "verdict": verdict,
            "total_mana_sources": n_lands + roles["ramp"]["count"],
            "notes": notes,
        },
    }


def _render_stats(stats, verbose: bool) -> str:
    meta, totals = stats["deck"], stats["totals"]
    curve, mv, colors = stats["curve"], stats["mana_value"], stats["colors"]
    lines = [output.rule(f"{meta['name']} — stats")]
    lines.append(f"Commander : {meta['commander']}   identity {''.join(colors['identity']) or 'C'}")
    lines.append(
        f"Cards     : {totals['cards']} total = {totals['maindeck']} maindeck "
        f"+ {totals['commander']} commander   ({totals['lands']} lands / "
        f"{totals['nonlands']} nonlands)"
    )
    lines.append("")

    lines.append(output.rule("MANA CURVE (non-land maindeck cards)"))
    peak = curve["peak_count"]
    for bucket in CURVE_BUCKETS:
        count = curve["buckets"][bucket]
        lines.append(f"  {bucket:>2}  {count:>3}  {_bar(count, peak)}")
    lines.append("")
    lines.append(f"  average MV, non-lands       : {mv['avg_nonland']:.2f}")
    lines.append(f"  average MV, including lands : {mv['avg_including_lands']:.2f}")
    if mv["commander_mv"] is not None:
        lines.append(f"  commander MV                : {_fmt_mv(mv['commander_mv'])} (excluded from the curve)")
    lines.append("")

    lines.append(output.rule("COLORS"))
    lines.append(f"  {'':<10}{'cards':>6}{'sources':>9}")
    for color in colors["identity"] or COLOR_ORDER:
        lines.append(
            f"  {COLOR_NAMES[color]:<10}{colors['cards_per_color'][color]:>6}"
            f"{colors['sources_per_color'][color]:>9}"
        )
    lines.append(
        f"  {'Colorless':<10}{colors['colorless_cards']:>6}{colors['colorless_sources']:>9}"
    )
    if colors["any_color_lands"]:
        lines.append(
            "  any-colour lands counted toward every colour: "
            + ", ".join(colors["any_color_lands"])
        )
    lines.append(
        f"  lands entering tapped: {colors['lands_enter_tapped']} "
        f"({colors['lands_enter_tapped_always']} always, "
        f"{colors['lands_enter_tapped_conditional']} conditional)"
    )
    if verbose and colors["lands_enter_tapped_cards"]:
        lines.append(output.wrap(" · ".join(colors["lands_enter_tapped_cards"]), 68, "    "))
    lines.append("")

    lines.append(output.rule("ROLES"))
    for role in ROLE_ORDER:
        entry = stats["roles"][role]
        lines.append(f"  {role:<12}{entry['count']:>3}   {entry['blurb']}")
        if verbose and entry["cards"]:
            lines.append(output.wrap(" · ".join(entry["cards"]), 68, "        "))
    lines.append("")
    lines.append(output.wrap(ROLES_NOTE, 72, "  "))
    lines.append("")

    lines.append(output.rule("ASSESSMENT"))
    assessment = stats["assessment"]
    lines.append(f"  land count: {assessment['verdict']}")
    for note in assessment["notes"]:
        lines.append(_bullet(note))
    return "\n".join(lines)


def cmd_deck_stats(args, conn, deck) -> int:
    stats = compute_stats(conn, deck)
    return output.emit(stats, _render_stats(stats, args.verbose), args.json)


# =========================================================== mtg deck bracket
def _load_brackets():
    try:
        return json.loads(Path(BRACKETS_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def compute_bracket(conn, deck) -> dict:
    data = _load_brackets()
    if data is None:
        return {"error": f"brackets.json at {BRACKETS_PATH}"}

    game_changers = data.get("game_changers", [])
    brackets = data.get("brackets", {})
    gc_lookup = {}
    for name in game_changers:
        for key in _name_keys(name):
            gc_lookup[key] = name

    cards = deck_rows(conn, deck["deck_id"])
    meta = _deck_meta(deck, cards)

    found, mld, extra_turns = [], [], []
    for card in cards:
        for key in _name_keys(card["name"]):
            if key in gc_lookup:
                found.append(gc_lookup[key])
                break
        # Reminder text is stripped here for the same reason as in the role
        # scan: it restates rules that are not this card's own effect.
        text = REMINDER_RE.sub(" ", card["oracle_text"] or "")
        if any(p.search(text) for p in MASS_LAND_DENIAL_RE):
            mld.append(card["name"])
        turn_text = text
        for pattern in EXTRA_TURNS_EXCLUDE_RE:
            turn_text = pattern.sub(" ", turn_text)
        if any(p.search(turn_text) for p in EXTRA_TURNS_RE):
            extra_turns.append(card["name"])
    found = sorted(set(found))
    mld, extra_turns = sorted(set(mld)), sorted(set(extra_turns))

    signals = {
        "game_changers": len(found),
        "mass_land_denial": len(mld),
        "mass_land_denial_cards": mld,
        "extra_turns": len(extra_turns),
        "extra_turns_cards": extra_turns,
        "two_card_infinite_combo": INFINITE_COMBO_VERDICT,
    }

    max_gc = brackets.get("3", {}).get("max_game_changers", 3)
    reasoning, caveats = [], []

    # Mass land denial is an unconditional "no" in brackets 1-3, so it forces 4.
    # Extra turns are NOT: the rule bans *chaining*, and whether a card chains is
    # no more decidable here than a two-card combo is — it is raised as a caveat.
    if mld:
        bracket = 4
        reasoning.append(
            f"Mass land denial detected ({', '.join(mld)}). Brackets 1-3 all state "
            f"'No mass land denial.', so the deck cannot sit below Bracket 4."
        )
    elif len(found) == 0:
        bracket = 2
        reasoning.append(
            "Zero Game Changers found. Brackets 1 and 2 both require 'No Game Changers.'"
        )
        reasoning.append(
            "Bracket 2 (Core) is described as 'Precon-level ... a modern preconstructed deck "
            "out of the box lands here', which is exactly what this deck is. Bracket 1 "
            "(Exhibition) is about intent — a joke or theme deck that is not trying to win — "
            "so it is not assigned automatically."
        )
    elif len(found) <= max_gc:
        bracket = 3
        reasoning.append(
            f"{len(found)} Game Changer(s) found: {', '.join(found)}. Brackets 1-2 both state "
            f"'No Game Changers.', while Bracket 3 (Upgraded) allows 'Up to {max_gc} Game "
            f"Changers.' — so a single listed card lifts an otherwise precon-level deck to 3."
        )
    else:
        bracket = 4
        reasoning.append(
            f"{len(found)} Game Changers found: {', '.join(found)}. That exceeds Bracket 3's "
            f"limit of {max_gc}, so Bracket 4 (Optimized), which states "
            f"'No restrictions: any number of Game Changers.'"
        )

    if not mld:
        reasoning.append(
            "No mass land denial detected (searched for 'destroy all lands' / "
            "'each player sacrifices a land' wording)."
        )
    if extra_turns:
        caveats.append(
            f"{len(extra_turns)} extra-turn effect(s) found: {', '.join(extra_turns)}. "
            f"Brackets 1-3 ban CHAINING extra turns, not owning one. Whether these chain is "
            f"a judgement call this tool does not make — review by hand. If they chain, "
            f"the deck is Bracket 4."
        )
    else:
        reasoning.append("No extra-turn effects detected (searched for 'take an extra turn').")
    caveats.append(f"Two-card infinite combos: {INFINITE_COMBO_VERDICT}. A combo would raise this estimate.")

    info = brackets.get(str(bracket), {})
    return {
        "ok": True,
        "deck": meta,
        "estimated_bracket": bracket,
        "bracket_name": info.get("name"),
        "bracket_summary": info.get("summary"),
        "bracket_rules": info.get("rules", []),
        "game_changers_found": found,
        "game_changers_checked": len(game_changers),
        "signals": signals,
        "reasoning": reasoning,
        "caveats": caveats,
        "needs_human_review": bool(caveats),
        "source": str(BRACKETS_PATH),
    }


def _render_bracket(result) -> str:
    meta, signals = result["deck"], result["signals"]
    lines = [output.rule(f"{meta['name']} — bracket")]
    lines.append(f"Commander : {meta['commander']}")
    lines.append("")
    lines.append(
        f"ESTIMATED BRACKET {result['estimated_bracket']} — {result['bracket_name']}"
    )
    lines.append(output.wrap(result["bracket_summary"] or "", 70, "  "))
    lines.append("")
    lines.append(output.rule("SIGNALS"))
    lines.append(
        f"  Game Changers        : {signals['game_changers']} "
        f"(checked against {result['game_changers_checked']} listed cards)"
    )
    for name in result["game_changers_found"]:
        lines.append(f"      • {name}")
    lines.append(f"  Mass land denial     : {signals['mass_land_denial']}"
                 + (f" — {', '.join(signals['mass_land_denial_cards'])}" if signals["mass_land_denial_cards"] else ""))
    lines.append(f"  Extra turns          : {signals['extra_turns']}"
                 + (f" — {', '.join(signals['extra_turns_cards'])}" if signals["extra_turns_cards"] else ""))
    lines.append(f"  Two-card infinite    : {signals['two_card_infinite_combo']}")
    lines.append("")
    lines.append(output.rule("REASONING"))
    for note in result["reasoning"]:
        lines.append(_bullet(note))
    lines.append("")
    lines.append(output.rule("NEEDS HUMAN / AGENT REVIEW"))
    for note in result["caveats"]:
        lines.append(_bullet(note))
    lines.append("")
    lines.append(output.rule(f"BRACKET {result['estimated_bracket']} RULES"))
    for item in result["bracket_rules"]:
        lines.append(_bullet(item))
    return "\n".join(lines)


def cmd_deck_bracket(args, conn, deck) -> int:
    result = compute_bracket(conn, deck)
    if "error" in result:
        return output.fail(result["error"], args.json)
    return output.emit(result, _render_bracket(result), args.json)


# ================================================================ mtg deck (router)
def cmd_deck(args) -> int:
    target = list(args.target or [])
    sub = None
    if target and target[0].lower() in {"stats", "bracket"}:
        sub = target.pop(0).lower()
    token = " ".join(target).strip()

    conn = db.connect()
    try:
        if not token and sub is None:
            rows = _all_decks(conn)
            payload = {
                "ok": True,
                "decks": [
                    {
                        "slug": r["deck_id"],
                        "name": r["name"],
                        "set_code": r["set_code"],
                        "release_date": r["release_date"],
                        "commander": r["commander_name"],
                        "cards": conn.execute(
                            "SELECT COALESCE(SUM(count), 0) FROM deck_cards WHERE deck_id=?",
                            (r["deck_id"],),
                        ).fetchone()[0],
                    }
                    for r in rows
                ],
            }
            text = [output.rule("decks")]
            for d in payload["decks"]:
                text.append(
                    f"  {d['slug']:<14} {_trunc(d['name'], 32)} "
                    f"{_trunc(d['commander'], 24)} {d['cards']:>3} cards"
                )
            text.append("")
            text.append("  mtg deck <slug> | mtg deck stats <slug> | mtg deck bracket <slug>")
            return output.emit(payload, "\n".join(text), args.json)

        deck, error = resolve_deck(conn, token)
        if deck is None:
            return output.fail(error, args.json)
        if sub == "stats":
            return cmd_deck_stats(args, conn, deck)
        if sub == "bracket":
            return cmd_deck_bracket(args, conn, deck)
        return cmd_deck_list(args, conn, deck)
    finally:
        conn.close()


# ================================================================= mtg edhrec
def _resolve_edhrec_slug(conn, token: str):
    """deck slug | commander name | EDHREC slug  ->  (row, deck_row, error)."""
    cached = conn.execute(
        "SELECT slug, fetched_at, payload_json FROM edhrec_cache ORDER BY slug"
    ).fetchall()
    if not cached:
        return None, None, "edhrec_cache is empty — run 'mtg rebuild --only edhrec'"

    slugs = [r["slug"] for r in cached]
    decks = _all_decks(conn)
    # commander slug -> deck row, so --missing knows which decklist to diff.
    by_commander = {_slugify(d["commander_name"]): d for d in decks}

    needle = (token or "").strip().lower()
    if not needle:
        return None, None, (
            "no commander given — cached: " + ", ".join(f"'{s}'" for s in slugs)
        )

    candidate = None
    direct = _slugify(needle)
    for row in cached:  # exact edhrec slug, or the slugified spelling of it
        if row["slug"].lower() in {needle, direct}:
            candidate = row
            break
    if candidate is None:  # a deck slug / deck name / commander name
        deck, _err = resolve_deck(conn, token)
        if deck is not None:
            wanted = _slugify(deck["commander_name"])
            for row in cached:
                if row["slug"] == wanted:
                    candidate = row
                    break
    if candidate is None:  # prefix of a cached slug
        hits = [r for r in cached if r["slug"].startswith(direct) or r["slug"].startswith(needle)]
        if len(hits) == 1:
            candidate = hits[0]
    if candidate is None:
        return None, None, (
            f"'{token}' not in my data — run 'mtg rebuild --only edhrec' "
            f"(cached: {', '.join(slugs)})"
        )
    return candidate, by_commander.get(candidate["slug"]), None


def _deck_name_set(conn, deck) -> set:
    if deck is None:
        return set()
    names = set()
    for row in conn.execute(
        "SELECT c.name FROM deck_cards dc JOIN cards c ON c.oracle_id = dc.oracle_id "
        "WHERE dc.deck_id = ?",
        (deck["deck_id"],),
    ):
        names |= _name_keys(row["name"])
    return names


def _fmt_synergy(value):
    if value is None:
        return "     —"
    return f"{value * 100:+6.1f}%"


def cmd_edhrec(args) -> int:
    conn = db.connect()
    try:
        row, deck, error = _resolve_edhrec_slug(conn, args.commander)
        if row is None:
            return output.fail(error, args.json)

        payload = json.loads(row["payload_json"])
        container = payload.get("container") or {}
        json_dict = container.get("json_dict") or {}
        lists = [cl for cl in (json_dict.get("cardlists") or []) if isinstance(cl, dict)]
        if not lists:
            return output.fail(
                f"{row['slug']} has no container.json_dict.cardlists — "
                f"run 'mtg rebuild --only edhrec'",
                args.json,
            )

        commander_card = json_dict.get("card") or {}
        headers = [str(cl.get("header") or cl.get("tag") or "?") for cl in lists]

        if args.list_header:
            wanted = args.list_header.strip().lower()
            lists = [
                cl
                for cl in lists
                if str(cl.get("header", "")).lower() == wanted
                or str(cl.get("tag", "")).lower() == wanted
                or str(cl.get("header", "")).lower().startswith(wanted)
            ]
            if not lists:
                return output.fail(
                    f"cardlist '{args.list_header}' for {row['slug']} — "
                    f"available: {', '.join(headers)}",
                    args.json,
                )

        deck_names = _deck_name_set(conn, deck)
        if args.missing and deck is None:
            return output.fail(
                f"a local decklist for {commander_card.get('name') or row['slug']} — "
                f"--missing needs one to cross-reference",
                args.json,
            )

        limit = args.limit if args.limit and args.limit > 0 else None
        out_lists = []
        for cl in lists:
            cards = []
            for view in cl.get("cardviews") or []:
                if not isinstance(view, dict):
                    continue
                name = view.get("name") or ""
                in_deck = bool(_name_keys(name) & deck_names) if deck_names else None
                if args.missing and in_deck:
                    continue
                num_decks = view.get("num_decks")
                potential = view.get("potential_decks")
                inclusion = (
                    round(100 * num_decks / potential, 1)
                    if isinstance(num_decks, int) and isinstance(potential, int) and potential
                    else None
                )
                cards.append(
                    {
                        "name": name,
                        "synergy": view.get("synergy"),
                        "synergy_pct": (
                            round(view["synergy"] * 100, 1)
                            if isinstance(view.get("synergy"), (int, float))
                            else None
                        ),
                        "num_decks": num_decks,
                        "potential_decks": potential,
                        "inclusion_pct": inclusion,
                        "in_deck": in_deck,
                    }
                )
            shown = cards[:limit] if limit else cards
            out_lists.append(
                {
                    "header": str(cl.get("header") or cl.get("tag") or "?"),
                    "tag": cl.get("tag"),
                    "total_cards": len(cl.get("cardviews") or []),
                    "matched": len(cards),
                    "shown": len(shown),
                    "cards": shown,
                }
            )

        result = {
            "ok": True,
            "commander": {
                "name": commander_card.get("name") or row["slug"],
                "slug": row["slug"],
                "num_decks": commander_card.get("num_decks"),
                "rank": commander_card.get("rank"),
                "color_identity": commander_card.get("color_identity"),
                "type_line": commander_card.get("type_line"),
            },
            "source": "edhrec_cache (offline)",
            "fetched_at": row["fetched_at"],
            "local_deck": deck["deck_id"] if deck is not None else None,
            "filters": {
                "list": args.list_header,
                "limit": limit,
                "missing_only": bool(args.missing),
            },
            "available_cardlists": headers,
            "cardlists": out_lists,
        }

        lines = [output.rule(f"EDHREC — {result['commander']['name']}")]
        lines.append(
            f"slug {row['slug']}   cached {row['fetched_at']}   "
            f"{result['commander']['num_decks'] or '?'} decks   rank #{result['commander']['rank'] or '?'}"
        )
        if deck is not None:
            lines.append(f"cross-referenced against local deck '{deck['deck_id']}'")
        if args.missing:
            lines.append("showing ONLY cards not already in that deck")
        lines.append("")
        for cl in out_lists:
            if args.missing:
                caption = (
                    f"{cl['header']} ({cl['shown']} of {cl['matched']} missing — "
                    f"{cl['total_cards']} in list)"
                )
            else:
                caption = f"{cl['header']} ({cl['shown']} of {cl['total_cards']})"
            lines.append(output.rule(caption))
            if not cl["cards"]:
                lines.append(
                    "  (all of this list is already in your deck)"
                    if args.missing and cl["total_cards"]
                    else "  (nothing to show)"
                )
            for card in cl["cards"]:
                mark = "" if card["in_deck"] is None else ("✓" if card["in_deck"] else " ")
                inclusion = (
                    f"{card['inclusion_pct']:>5.1f}% of {card['potential_decks']} decks"
                    if card["inclusion_pct"] is not None
                    else ""
                )
                lines.append(
                    f"  {mark} {_trunc(card['name'], 32)} "
                    f"syn {_fmt_synergy(card['synergy'])}   {inclusion}"
                )
            lines.append("")
        if deck is not None and not args.missing:
            lines.append("  ✓ = already in your deck")
        return output.emit(result, "\n".join(lines), args.json)
    finally:
        conn.close()


# ================================================================== register
def _add_json_flag(parser) -> None:
    """Accept --json AFTER the subcommand as well as before it.

    cli.py defines --json on the root parser only. Whether a trailing --json
    survives depends on the subparser's positional nargs, which is an argparse
    implementation detail, not a contract: `mtg deck tidus --json` happened to
    work while `mtg edhrec tidus --json` died with exit 2 and printed no JSON —
    the worst possible failure for a machine caller. Declaring it explicitly
    removes the accident.

    default=SUPPRESS is load-bearing: a plain store_true would default to False
    and overwrite a --json already parsed by the root parser.
    """
    parser.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS,
        help="emit machine-readable JSON instead of formatted text",
    )


def register(subparsers) -> None:
    deck = subparsers.add_parser(
        "deck",
        help="show a decklist, its stats, or its Commander bracket",
        description=(
            "mtg deck                     list the loaded decks\n"
            "mtg deck <slug>              full decklist grouped by card type\n"
            "mtg deck stats <slug>        curve, colours, mana sources, roles\n"
            "mtg deck bracket <slug>      estimated Commander bracket (1-5)\n"
            "\n<slug> is 'tidus' | 'bumbleflower' | 'dogmeat', or any "
            "case-insensitive prefix of the deck or commander name."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    deck.add_argument(
        "target",
        nargs="*",
        metavar="[stats|bracket] <deck>",
        help="deck slug / name prefix, optionally preceded by 'stats' or 'bracket'",
    )
    deck.add_argument(
        "--group",
        choices=["type", "cmc", "color"],
        default="type",
        help="how to group the decklist (default: type)",
    )
    deck.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="list the card names behind each role / signal",
    )
    _add_json_flag(deck)
    deck.set_defaults(func=cmd_deck)

    edhrec = subparsers.add_parser(
        "edhrec",
        help="cached EDHREC recommendations for a commander (offline)",
        description=(
            "Reads the cached EDHREC payload from the local database. Never "
            "touches the network. Accepts a deck slug, a commander name, or an "
            "EDHREC slug."
        ),
    )
    edhrec.add_argument("commander", nargs="?", help="deck slug, commander name, or edhrec slug")
    edhrec.add_argument(
        "--list",
        dest="list_header",
        metavar="HEADER",
        help='show one cardlist, e.g. --list "High Synergy Cards"',
    )
    edhrec.add_argument("--limit", type=int, default=15, help="cards per list (default 15, 0 = all)")
    edhrec.add_argument(
        "--missing",
        action="store_true",
        help="show only cards NOT already in that commander's local deck",
    )
    _add_json_flag(edhrec)
    edhrec.set_defaults(func=cmd_edhrec)
