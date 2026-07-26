"""cmd_sim.py — goldfish simulator (`mtg deck goldfish`) and deck merger (`mtg merge`).

Two deterministic tools for Commander (EDH) only:

  mtg deck goldfish <slug> --seed N --turns 8
      Shuffle a 99-card library with a dedicated random.Random(seed), draw an
      opening seven, optionally take London mulligans, then draw one card per
      turn while tracking lands, colours available and what is castable.
      Same seed  ->  byte-identical output, forever, on any machine.

  mtg merge <slugA> <slugB> --commander "<name>"
      The legal candidate pool for mixing two decks: union of both main boards
      plus the non-chosen commander, each card marked LEGAL/ILLEGAL against the
      chosen commander's colour identity, de-duplicated with in_both flags.
      This is a set operation, not a deckbuilding opinion.

Determinism contract (why this file is written the way it is)
------------------------------------------------------------
* The library is built as an EXPLICIT ORDERED LIST sorted by (name, oracle_id),
  with count>1 cards expanded into repeated entries. SQLite row order is never
  trusted — it is not stable across rebuilds.
* All randomness comes from one dedicated ``random.Random(seed)`` instance.
  The global ``random`` module is never touched.
* Every tie-break in every heuristic (which land to play, which card to bottom)
  sorts on a total order that ends in the card name, so there are no ties left
  to resolve non-deterministically.

Stdlib only (constraint C6). No network at query time (constraint C1).
"""
from __future__ import annotations

import argparse
import random
import re
import sqlite3
from collections import Counter, OrderedDict

import db
import output

# --------------------------------------------------------------------------- #
# constants
# --------------------------------------------------------------------------- #

COLORS = ("W", "U", "B", "R", "G")
COLOR_ORDER = {c: i for i, c in enumerate(COLORS)}

# Priority order used to bucket a type_line into ONE primary type.
# Land wins over everything (an artifact land is a land you play, not a spell),
# then permanents by how they are usually counted in a Commander deck list.
TYPE_PRIORITY = (
    "Land",
    "Planeswalker",
    "Battle",
    "Creature",
    "Artifact",
    "Enchantment",
    "Instant",
    "Sorcery",
)

_SYMBOL_RE = re.compile(r"\{([^}]+)\}")
# "Add {G} or {W}." / "Add one mana of any color..." — capture up to the clause end.
_ADD_RE = re.compile(r"\badd\b([^.;]*)", re.IGNORECASE)
_ANY_NUMBER_RE = re.compile(r"any number of cards named", re.IGNORECASE)

_RAMP_RE = re.compile(
    r"(search your library for (?:a|up to \w+)[^.]*land"
    r"|add \{"
    r"|put (?:a|two|that) land[^.]*onto the battlefield)",
    re.IGNORECASE,
)
_INTERACTION_RE = re.compile(
    r"(destroy target|destroy all|exile target|exile all|counter target"
    r"|return target[^.]*to (?:its owner|their owner)|deals? \d+ damage to target"
    r"|fights? target|sacrifices? a creature)",
    re.IGNORECASE,
)

GOLDFISH_NOTES = [
    "Mana model: lands only (one land drop per turn, tapped/untapped ignored).",
    "'Any color' lands (Command Tower, Exotic Orchard, Path of Ancestry) are "
    "counted as producing the commander's colours.",
    "Castable = cmc <= lands in play AND every coloured pip has a source among "
    "those lands. No board state, no opponents, no interaction.",
]

# --------------------------------------------------------------------------- #
# small shared helpers
# --------------------------------------------------------------------------- #


def _as_json(args) -> bool:
    return bool(getattr(args, "json", False))


def _row_to_card(row: sqlite3.Row, count: int = 1, board: str = "main") -> dict:
    """Normalise a cards row into the dict shape every function here passes around."""
    type_line = row["type_line"] or ""
    return {
        "oracle_id": row["oracle_id"],
        "name": row["name"],
        "mana_cost": row["mana_cost"] or "",
        "cmc": float(row["cmc"] or 0.0),
        "type_line": type_line,
        "oracle_text": row["oracle_text"] or "",
        "colors": output.json_list(row["colors"]),
        "color_identity": output.json_list(row["color_identity"]),
        "layout": row["layout"] or "",
        "legal_commander": row["legal_commander"],
        "is_land": "Land" in type_line,
        "is_basic": "Basic Land" in type_line,
        "count": count,
        "board": board,
    }


_CARD_SELECT = (
    "SELECT c.oracle_id, c.name, c.mana_cost, c.cmc, c.type_line, c.oracle_text, "
    "       c.colors, c.color_identity, c.layout, c.legal_commander "
    "FROM cards c"
)


def _deck_row(conn, slug: str):
    return conn.execute("SELECT * FROM decks WHERE deck_id = ?", (slug,)).fetchone()


def _resolve_deck(conn, slug: str):
    """Exact slug, else an unambiguous case-insensitive prefix of slug/name/commander.

    Matches how `mtg deck <slug>` resolves, so `mtg deck goldfish counter` and
    `mtg deck counter` mean the same deck. Returns (row, error_message).
    """
    row = _deck_row(conn, slug)
    if row is not None:
        return row, None
    q = (slug or "").strip().lower()
    if q:
        hits = {}
        for r in conn.execute("SELECT * FROM decks ORDER BY deck_id"):
            haystack = (r["deck_id"], r["name"] or "", r["commander_name"] or "")
            if any(h.lower().startswith(q) for h in haystack):
                hits[r["deck_id"]] = r
        if len(hits) == 1:
            return next(iter(hits.values())), None
        if len(hits) > 1:
            return None, (
                f"deck '{slug}' is ambiguous — matches {', '.join(sorted(hits))}"
            )
    return None, (
        f"deck '{slug}' — no such deck slug (known: {', '.join(_known_slugs(conn))})"
    )


def _known_slugs(conn) -> list:
    return [r["deck_id"] for r in conn.execute("SELECT deck_id FROM decks ORDER BY deck_id")]


def _deck_cards(conn, slug: str, board: str = "main") -> list:
    """Deck contents as a DETERMINISTICALLY ORDERED list (name, oracle_id)."""
    rows = conn.execute(
        _CARD_SELECT + " JOIN deck_cards dc ON dc.oracle_id = c.oracle_id "
        "WHERE dc.deck_id = ? AND dc.board = ?",
        (slug, board),
    ).fetchall()
    counts = {
        r["oracle_id"]: r["count"]
        for r in conn.execute(
            "SELECT oracle_id, count FROM deck_cards WHERE deck_id = ? AND board = ?",
            (slug, board),
        )
    }
    cards = [_row_to_card(r, counts.get(r["oracle_id"], 1), board) for r in rows]
    cards.sort(key=lambda c: (c["name"], c["oracle_id"]))
    return cards


def _resolve_card_by_name(conn, name: str):
    """Resolve a card name to ONE oracle row.

    219 names map to more than one oracle_id (token vs normal printings), so
    real cards are preferred over tokens and Commander-legal rows over the rest.
    """
    rows = conn.execute(
        _CARD_SELECT + " WHERE c.name = ? COLLATE NOCASE", (name,)
    ).fetchall()
    if not rows:
        return None
    tokenish = ("token", "art_series", "double_faced_token", "emblem")

    def rank(r):
        return (
            0 if (r["layout"] or "") not in tokenish else 1,
            0 if r["legal_commander"] is not None else 1,
            0 if r["legal_commander"] == "legal" else 1,
            r["oracle_id"],
        )

    return sorted(rows, key=rank)[0]


def _short_type(type_line: str) -> str:
    return (type_line or "").split(" — ")[0].strip()


def _primary_type(type_line: str) -> str:
    tl = type_line or ""
    for t in TYPE_PRIORITY:
        if t in tl:
            return t
    return "Other"


def _sorted_colors(colors) -> list:
    return sorted(set(colors), key=lambda c: COLOR_ORDER.get(c, 99))


def _cmc_bucket(cmc: float) -> str:
    n = int(cmc)
    return "7+" if n >= 7 else str(n)


# --------------------------------------------------------------------------- #
# mana logic
# --------------------------------------------------------------------------- #


def _pip_requirements(mana_cost: str) -> list:
    """Coloured requirements of a mana cost, as a list of option-sets.

    Each entry is the set of colours that can pay that pip. Symbols payable
    without a coloured source ({2}, {X}, {C}, {S}, {2/W} generic side,
    {W/P} phyrexian life) contribute no requirement.
    """
    reqs = []
    for sym in _SYMBOL_RE.findall(mana_cost or ""):
        parts = sym.upper().split("/")
        if any(p.isdigit() or p in ("X", "Y", "Z", "C", "S", "P") for p in parts):
            continue  # payable without a specific colour
        opts = {p for p in parts if p in COLORS}
        if opts:
            reqs.append(opts)
    return reqs


def _required_colors(card: dict) -> list:
    """Colours the card's own mana cost demands (falls back to colour identity)."""
    reqs = _pip_requirements(card["mana_cost"])
    if reqs:
        seen = set()
        for opts in reqs:
            seen |= opts
        return _sorted_colors(seen)
    return _sorted_colors(card["color_identity"])


def _land_sources(card: dict, commander_identity) -> set:
    """Colours a land can produce, approximated from its oracle text.

    'any color' clauses resolve to the commander's identity — that covers
    Command Tower, Path of Ancestry and (optimistically) Exotic Orchard.
    """
    text = card["oracle_text"] or ""
    produced: set = set()
    for clause in _ADD_RE.findall(text):
        low = clause.lower()
        if "any color" in low or "any colour" in low:
            produced |= set(commander_identity)
        for sym in _SYMBOL_RE.findall(clause):
            for part in sym.upper().split("/"):
                if part in COLORS:
                    produced.add(part)
    if not produced:
        # Fetch lands and utility lands legitimately produce nothing coloured;
        # colour identity is the safe fallback for anything the regex missed.
        produced = set(card["color_identity"])
    return produced


def _castable(card: dict, mana: int, sources: set) -> bool:
    if card["is_land"]:
        return False
    if card["cmc"] > mana:
        return False
    for opts in _pip_requirements(card["mana_cost"]):
        if not (opts & sources):
            return False
    if not _pip_requirements(card["mana_cost"]):
        # No pips in the cost — still respect colour identity for split/adventure
        # style costs the symbol parser cannot see.
        for c in card["color_identity"]:
            if c not in sources:
                return False
    return True


# --------------------------------------------------------------------------- #
# goldfish
# --------------------------------------------------------------------------- #


def _card_public(card: dict) -> dict:
    """The JSON shape used for every card the goldfish reports."""
    return {
        "name": card["name"],
        "oracle_id": card["oracle_id"],
        "mana_cost": card["mana_cost"],
        "cmc": card["cmc"],
        "type_line": card["type_line"],
        "color_identity": card["color_identity"],
        "is_land": card["is_land"],
    }


def _build_library(cards: list) -> list:
    """Explicit ordered list: sorted by (name, oracle_id), counts expanded."""
    library = []
    for card in sorted(cards, key=lambda c: (c["name"], c["oracle_id"])):
        for _ in range(max(1, int(card["count"]))):
            library.append(card)
    return library


def _choose_bottom(hand: list, n: int, strategy: str) -> list:
    """Pick n cards to put on the bottom. Total order -> fully deterministic."""
    if n <= 0:
        return []
    chosen: list = []
    remaining = list(hand)

    if strategy == "worst-lands":
        lands = [c for c in remaining if c["is_land"]]
        excess = max(0, len(lands) - 4)
        if excess:
            # Worst first: fewest colours produced, then basics, then by name.
            ranked = sorted(
                lands,
                key=lambda c: (
                    len(_land_sources(c, COLORS)),
                    0 if c["is_basic"] else 1,
                    c["name"],
                    c["oracle_id"],
                ),
            )
            for card in ranked[: min(excess, n)]:
                chosen.append(card)
                remaining.remove(card)

    # Fill the rest (or the whole quota for 'highest-cmc') with the top end.
    need = n - len(chosen)
    if need > 0:
        ranked = sorted(
            remaining,
            key=lambda c: (-c["cmc"], 1 if c["is_land"] else 0, c["name"], c["oracle_id"]),
        )
        for card in ranked[:need]:
            chosen.append(card)
            remaining.remove(card)
    return chosen


def _pick_land_to_play(hand: list, sources: set, commander_identity) -> dict | None:
    """Play the land that adds the most new colours; ties break on name."""
    lands = [c for c in hand if c["is_land"]]
    if not lands:
        return None

    def key(card):
        produced = _land_sources(card, commander_identity)
        new = produced - sources
        return (-len(new), -len(produced), card["name"], card["oracle_id"])

    return sorted(lands, key=key)[0]


def _recommendation(hand: list, deck_land_count: int, mulligans: int) -> dict:
    """Heuristic keep/mull advice. Explicitly NOT a rules ruling."""
    lands = [c for c in hand if c["is_land"]]
    spells = [c for c in hand if not c["is_land"]]
    n_lands = len(lands)
    reasons = []

    keepable = 2 <= n_lands <= 5
    reasons.append(
        f"{n_lands} land{'' if n_lands == 1 else 's'} in the seven "
        f"(deck runs {deck_land_count}; 2-5 is the keepable band)."
    )
    if n_lands < 2:
        reasons.append("Under two lands is a mulligan in almost every Commander pod.")
    elif n_lands > 5:
        reasons.append("Six or more lands means too few spells — flood risk.")

    ramp = [c for c in spells if c["cmc"] <= 3 and _RAMP_RE.search(c["oracle_text"])]
    interaction = [c for c in spells if _INTERACTION_RE.search(c["oracle_text"])]
    early = [c for c in spells if c["cmc"] <= 2]

    reasons.append(
        f"Ramp/fixing at 3 or less: {len(ramp)}"
        + (f" ({', '.join(c['name'] for c in ramp)})." if ramp else ".")
    )
    reasons.append(
        f"Interaction: {len(interaction)}"
        + (f" ({', '.join(c['name'] for c in interaction)})." if interaction else ".")
    )

    if spells:
        avg = round(sum(c["cmc"] for c in spells) / len(spells), 2)
        cheapest = min(c["cmc"] for c in spells)
        reasons.append(
            f"Curve: {len(spells)} spells, average cmc {avg}, cheapest {cheapest:g}."
        )
        if not early:
            reasons.append("Nothing castable before turn 3 — the hand is slow.")
        if cheapest > n_lands + 2:
            reasons.append("Cheapest spell needs more lands than this hand can find soon.")
    else:
        reasons.append("No spells at all — this hand does nothing.")

    verdict = "keep" if keepable and spells else "mulligan"
    evaluated_on = "the seven as drawn, before any cards go to the bottom"
    if verdict == "keep" and n_lands in (2, 5) and not ramp and not early:
        reasons.append("Borderline: keepable land count but no early action to use it.")
    if mulligans:
        reasons.append(
            f"Already at {mulligans} mulligan{'' if mulligans == 1 else 's'} — "
            f"the next hand costs another card, so the bar to ship drops."
        )
    reasons.append("Heuristic advice from card counts only — not a rules ruling.")
    return {
        "verdict": verdict,
        "reasons": reasons,
        "evaluated_on": evaluated_on,
        "lands": n_lands,
        "spells": len(spells),
        "ramp": [c["name"] for c in ramp],
        "interaction": [c["name"] for c in interaction],
        "heuristic": True,
    }


def _bullet(text: str, width: int = 72) -> str:
    """'  - text' with a hanging indent on the wrapped continuation lines."""
    wrapped = output.wrap(text, width=width - 4, indent="    ")
    return "  - " + (wrapped[4:] if wrapped.startswith("    ") else wrapped)


def _hand_lines(cards: list, indent: str = "  ") -> list:
    lines = []
    for card in cards:
        cost = card["mana_cost"] or ("—" if card["is_land"] else "")
        lines.append(
            f"{indent}{card['name'][:32]:<32} {cost:<16} "
            f"{card['cmc']:>4.0f}  {_short_type(card['type_line'])}"
        )
    return lines


def cmd_goldfish(args) -> int:
    as_json = _as_json(args)
    # getattr with defaults: this handler is reachable three ways (nested
    # subcommand, top-level alias, grafted onto cmd_decks' `deck` parser) and
    # not every route is guaranteed to have defined every flag.
    slug = getattr(args, "slug", None)
    if not slug:
        return output.fail("goldfish — no deck slug given (try: mtg deck goldfish tidus)", as_json)
    turns = max(0, int(getattr(args, "turns", 8) or 0))
    mulligans = max(0, int(getattr(args, "mulligans", 0) or 0))
    strategy = getattr(args, "bottom", "highest-cmc") or "highest-cmc"

    if mulligans >= 7:
        return output.fail(
            f"--mulligans {mulligans} — a London mulligan to zero cards is not simulated "
            "(use 0-6)",
            as_json,
        )

    conn = db.connect()
    try:
        deck, err = _resolve_deck(conn, slug)
        if deck is None:
            return output.fail(err, as_json)
        slug = deck["deck_id"]

        main = _deck_cards(conn, slug, "main")
        if not main:
            return output.fail(f"deck '{slug}' has no main-board cards", as_json)

        cmd_rows = _deck_cards(conn, slug, "commander")
        commander = cmd_rows[0] if cmd_rows else None
        commander_identity = (
            _sorted_colors(commander["color_identity"]) if commander else list(COLORS)
        )

        seed = getattr(args, "seed", None)
        if seed is None:
            seed = random.SystemRandom().randrange(1, 2**31 - 1)
        seed = int(seed)

        rng = random.Random(seed)  # dedicated instance — never the global module
        library = _build_library(main)
        deck_size = len(library)
        deck_land_count = sum(1 for c in library if c["is_land"])

        if deck_size < 7:
            return output.fail(f"deck '{slug}' has only {deck_size} cards to shuffle", as_json)

        rng.shuffle(library)

        # ---- London mulligans: always draw a full seven, bottom M on the keep
        hand = library[:7]
        library = library[7:]
        mulligan_records = []
        for i in range(1, mulligans + 1):
            mulligan_records.append(
                {
                    "number": i,
                    "hand": [_card_public(c) for c in hand],
                    "lands": sum(1 for c in hand if c["is_land"]),
                }
            )
            library = hand + library          # hand shuffles back into the library
            rng.shuffle(library)
            hand = library[:7]
            library = library[7:]

        kept_seven = list(hand)
        recommendation = _recommendation(kept_seven, deck_land_count, mulligans)
        lands_in_opener = sum(1 for c in kept_seven if c["is_land"])

        bottomed = _choose_bottom(hand, mulligans, strategy)
        for card in bottomed:
            hand.remove(card)
        library.extend(bottomed)  # bottom of the library
        opening_hand = list(hand)  # what is actually kept and played

        # ---- turns
        sources: set = set()
        lands_played: list = []
        lands_seen = sum(1 for c in hand if c["is_land"])
        draws = []
        turn_records = []
        decked = False

        for turn in range(1, turns + 1):
            if not library:
                decked = True
                break
            drawn = library.pop(0)
            hand.append(drawn)
            if drawn["is_land"]:
                lands_seen += 1
            draws.append({"turn": turn, "card": _card_public(drawn)})

            land = _pick_land_to_play(hand, sources, commander_identity)
            played_name = None
            if land is not None:
                hand.remove(land)
                lands_played.append(land)
                sources |= _land_sources(land, commander_identity)
                played_name = land["name"]

            mana = len(lands_played)
            # One pass, so a duplicate card can never land in both lists
            # (dicts compare by value — membership tests are not safe here).
            castable, stuck = [], []
            for card in hand:
                if card["is_land"]:
                    continue
                (castable if _castable(card, mana, sources) else stuck).append(card)
            castable.sort(key=lambda c: (-c["cmc"], c["name"], c["oracle_id"]))
            stuck.sort(key=lambda c: (c["cmc"], c["name"], c["oracle_id"]))

            turn_records.append(
                {
                    "turn": turn,
                    "drew": _card_public(drawn),
                    "land_played": played_name,
                    "lands_in_play": mana,
                    "lands_seen": lands_seen,
                    "colors_available": _sorted_colors(sources),
                    "hand_size": len(hand),
                    "castable": [_card_public(c) for c in castable],
                    "uncastable_in_hand": [_card_public(c) for c in stuck],
                }
            )

        payload = {
            "ok": True,
            "deck": {
                "slug": slug,
                "name": deck["name"],
                "commander": deck["commander_name"],
                "commander_color_identity": commander_identity,
                "library_size": deck_size,
                "land_count": deck_land_count,
            },
            "seed": seed,
            "turns_simulated": len(turn_records),
            "mulligans_taken": mulligans,
            "bottom_strategy": strategy,
            "opening_hand": [_card_public(c) for c in opening_hand],
            "kept_seven": [_card_public(c) for c in kept_seven],
            "bottomed": [_card_public(c) for c in bottomed],
            "mulligans": mulligan_records,
            "draws": draws,
            "lands_in_opener": lands_in_opener,
            "lands_in_hand": lands_in_opener - sum(1 for c in bottomed if c["is_land"]),
            "recommendation": recommendation,
            "turn_detail": turn_records,
            "library_remaining": len(library),
            "decked": decked,
            "notes": GOLDFISH_NOTES,
        }

        lines = []
        lines.append(output.rule(f"GOLDFISH · {deck['name']}"))
        lines.append(
            f"deck: {slug}   commander: {deck['commander_name']} "
            f"({'/'.join(commander_identity) or 'C'})"
        )
        lines.append(
            f"seed: {seed}   library: {deck_size} cards ({deck_land_count} lands)   "
            f"turns: {len(turn_records)}   mulligans: {mulligans} ({strategy})"
        )
        lines.append("")

        for rec in mulligan_records:
            n = rec["lands"]
            lines.append(
                output.rule(
                    f"MULLIGAN #{rec['number']} — SHIPPED ({n} land{'' if n == 1 else 's'})"
                )
            )
            lines.extend(_hand_lines(rec["hand"]))
            lines.append("")

        lines.append(output.rule(f"OPENING HAND ({len(opening_hand)})"))
        lines.extend(_hand_lines(opening_hand))
        if bottomed:
            lines.append("")
            lines.append(f"  bottomed ({strategy}):")
            lines.extend(_hand_lines(bottomed, indent="    - "))
        lines.append("")
        lines.append(f"  lands in opener: {lands_in_opener}")
        lines.append("")

        lines.append(output.rule(f"RECOMMENDATION: {recommendation['verdict'].upper()}"))
        if bottomed:
            lines.append("  (judged on the seven you kept, before bottoming)")
        for reason in recommendation["reasons"]:
            lines.append(_bullet(reason))
        lines.append("")

        lines.append(output.rule("TURNS"))
        for rec in turn_records:
            lines.append(
                f"T{rec['turn']}  draw: {rec['drew']['name']}"
                f"{' (land)' if rec['drew']['is_land'] else ''}"
            )
            lines.append(
                f"     lands seen {rec['lands_seen']} · in play {rec['lands_in_play']}"
                f" [{','.join(rec['colors_available']) or '-'}]"
                + (f" · played {rec['land_played']}" if rec["land_played"] else " · no land drop")
                + f" · hand {rec['hand_size']}"
            )
            if rec["castable"]:
                names = ", ".join(
                    f"{c['name']} {c['mana_cost']}".strip() for c in rec["castable"]
                )
                lines.append(output.wrap(f"castable: {names}", width=72, indent="     "))
            else:
                lines.append("     castable: (nothing)")
        if decked:
            lines.append("  library empty — simulation stopped early.")
        lines.append("")
        lines.append(output.rule("NOTES"))
        for note in GOLDFISH_NOTES:
            lines.append(_bullet(note))

        return output.emit(payload, "\n".join(lines), as_json)
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
# merge
# --------------------------------------------------------------------------- #


def _illegal_reason(card: dict, identity: set) -> str | None:
    """Every reason the card cannot go in the deck, or None if it is legal.

    Both checks run — a card can be off-colour AND banned, and the merge agent
    should see both rather than only the first one we happened to test.
    """
    reasons = []
    ci = set(card["color_identity"])
    off = _sorted_colors(ci - identity)
    if off:
        reasons.append(
            f"colour identity {{{','.join(_sorted_colors(ci))}}} is not within the "
            f"commander's {{{','.join(_sorted_colors(identity)) or 'C'}}} — off-colour: "
            f"{','.join(off)}"
        )
    legality = card["legal_commander"]
    if legality != "legal":
        reasons.append(f"not legal in Commander (legality={legality or 'unknown'})")
    return "; ".join(reasons) if reasons else None


def cmd_merge(args) -> int:
    as_json = _as_json(args)
    slug_a, slug_b = args.deck_a, args.deck_b

    conn = db.connect()
    try:
        deck_a, err_a = _resolve_deck(conn, slug_a)
        if deck_a is None:
            return output.fail(err_a, as_json)
        deck_b, err_b = _resolve_deck(conn, slug_b)
        if deck_b is None:
            return output.fail(err_b, as_json)
        slug_a, slug_b = deck_a["deck_id"], deck_b["deck_id"]
        if slug_a == slug_b:
            return output.fail(
                f"deck '{slug_a}' merged with itself — pass two different deck slugs", as_json
            )
        main_a = _deck_cards(conn, slug_a, "main")
        main_b = _deck_cards(conn, slug_b, "main")
        cmd_a = _deck_cards(conn, slug_a, "commander")
        cmd_b = _deck_cards(conn, slug_b, "commander")

        # ---- resolve the chosen commander
        wanted = args.commander.strip()
        chosen = None
        source = None
        for slug, pile in ((slug_a, cmd_a), (slug_b, cmd_b)):
            for card in pile:
                if card["name"].lower() == wanted.lower():
                    chosen, source = card, f"{slug} (commander)"
                    break
            if chosen:
                break
        if chosen is None:
            for slug, pile in ((slug_a, main_a), (slug_b, main_b)):
                for card in pile:
                    if card["name"].lower() == wanted.lower():
                        chosen, source = card, f"{slug} (main board)"
                        break
                if chosen:
                    break
        if chosen is None:
            row = _resolve_card_by_name(conn, wanted)
            if row is None:
                return output.fail(
                    f"commander '{wanted}' — no card by that name in either deck or in cards",
                    as_json,
                )
            chosen = _row_to_card(row, 1, "commander")
            source = "cards table (not in either deck)"

        tl = chosen["type_line"]
        can_be = "can be your commander" in (chosen["oracle_text"] or "").lower()
        if not (("Legendary" in tl and "Creature" in tl) or can_be):
            return output.fail(
                f"commander '{chosen['name']}' — type is '{tl}', which is not a legendary "
                "creature and has no 'can be your commander' clause",
                as_json,
            )
        if chosen["legal_commander"] != "legal":
            return output.fail(
                f"commander '{chosen['name']}' — legality is "
                f"'{chosen['legal_commander'] or 'unknown'}', not legal in Commander",
                as_json,
            )

        identity = set(chosen["color_identity"])

        # ---- pool: both main boards + every non-chosen commander
        pool: "OrderedDict[str, dict]" = OrderedDict()

        def add(card: dict, slug: str, board: str):
            entry = pool.get(card["oracle_id"])
            singleton_exempt = card["is_basic"] or bool(
                _ANY_NUMBER_RE.search(card["oracle_text"] or "")
            )
            if entry is None:
                pool[card["oracle_id"]] = {
                    "card": card,
                    "from": [slug],
                    "boards": [board],
                    # Singleton applies even to a single deck: if a rebuild ever
                    # hands us 2x of a non-basic, only 1 is legally playable.
                    "count": card["count"] if singleton_exempt else 1,
                    "counts": {slug: card["count"]},
                    "singleton_exempt": singleton_exempt,
                }
                return
            if slug not in entry["from"]:
                entry["from"].append(slug)
            if board not in entry["boards"]:
                entry["boards"].append(board)
            entry["counts"][slug] = card["count"]
            # Basics (and 'any number' cards) stack across decks; everything
            # else is singleton-limited no matter how many copies you own.
            entry["count"] = (
                sum(entry["counts"].values()) if entry["singleton_exempt"] else 1
            )

        for card in main_a:
            add(card, slug_a, "main")
        for card in main_b:
            add(card, slug_b, "main")
        for slug, pile in ((slug_a, cmd_a), (slug_b, cmd_b)):
            for card in pile:
                if card["oracle_id"] != chosen["oracle_id"]:
                    add(card, slug, "commander")

        # The chosen commander is the commander, not a pool candidate.
        pool.pop(chosen["oracle_id"], None)

        entries = sorted(pool.values(), key=lambda e: (e["card"]["name"], e["card"]["oracle_id"]))

        pool_json = []
        legal_cards = []
        illegal_cards = []
        in_both = 0
        for entry in entries:
            card = entry["card"]
            reason = _illegal_reason(card, identity)
            is_legal = reason is None
            both = len(entry["from"]) > 1
            if both:
                in_both += 1
            rec = {
                "name": card["name"],
                "oracle_id": card["oracle_id"],
                "mana_cost": card["mana_cost"],
                "cmc": card["cmc"],
                "type_line": card["type_line"],
                "color_identity": card["color_identity"],
                "legal": is_legal,
                "reason": reason,
                "in_both": both,
                "from": entry["from"],
                "boards": entry["boards"],
                "count": entry["count"],
            }
            pool_json.append(rec)
            (legal_cards if is_legal else illegal_cards).append(rec)

        by_type: Counter = Counter()
        curve: Counter = Counter()
        for rec in legal_cards:
            by_type[_primary_type(rec["type_line"])] += rec["count"]
            if _primary_type(rec["type_line"]) != "Land":
                curve[_cmc_bucket(rec["cmc"])] += rec["count"]

        by_type_out = OrderedDict(
            (t, by_type[t]) for t in TYPE_PRIORITY + ("Other",) if by_type.get(t)
        )
        curve_out = OrderedDict(
            (b, curve[b]) for b in ("0", "1", "2", "3", "4", "5", "6", "7+") if curve.get(b)
        )

        payload = {
            "ok": True,
            "decks": [
                {"slug": slug_a, "name": deck_a["name"], "commander": deck_a["commander_name"]},
                {"slug": slug_b, "name": deck_b["name"], "commander": deck_b["commander_name"]},
            ],
            "commander": {
                "name": chosen["name"],
                "oracle_id": chosen["oracle_id"],
                "mana_cost": chosen["mana_cost"],
                "cmc": chosen["cmc"],
                "type_line": chosen["type_line"],
                "color_identity": _sorted_colors(chosen["color_identity"]),
                "source": source,
            },
            "color_identity": _sorted_colors(identity),
            "pool": pool_json,
            "totals": {
                "pool": len(pool_json),
                "legal": len(legal_cards),
                "illegal": len(illegal_cards),
                "in_both": in_both,
                "copies_available": sum(r["count"] for r in pool_json),
                "legal_copies_available": sum(r["count"] for r in legal_cards),
                "slots_to_fill": 99,
            },
            "by_type": dict(by_type_out),
            "curve": dict(curve_out),
            "notes": [
                "Set operation only — legality by colour identity and Commander "
                "legality. Deck-quality judgement belongs to the Deck Merger agent.",
                "Basics and 'any number of cards named' cards stack across both "
                "decks; everything else is singleton-limited to 1 copy.",
            ],
        }

        # ---- text
        show = args.show
        limit = args.limit
        ci_txt = "/".join(_sorted_colors(identity)) or "C"
        lines = []
        lines.append(output.rule(f"MERGE POOL · {slug_a} + {slug_b}"))
        lines.append(
            f"commander: {chosen['name']}  {chosen['mana_cost']}  "
            f"identity {ci_txt}   [{source}]"
        )
        lines.append(f"  {deck_a['name']} ({slug_a})  +  {deck_b['name']} ({slug_b})")
        lines.append("")
        t = payload["totals"]
        lines.append(
            f"pool {t['pool']} distinct  ·  legal {t['legal']}  ·  illegal {t['illegal']}"
            f"  ·  in both decks {t['in_both']}  ·  {t['legal_copies_available']} legal "
            f"copies available for 99 slots"
        )
        lines.append("")

        lines.append(output.rule("LEGAL POOL BY TYPE"))
        for typ, n in by_type_out.items():
            lines.append(f"  {typ:<14} {n:>4}")
        lines.append("")
        lines.append(output.rule("LEGAL POOL CURVE (non-land)"))
        peak = max(curve_out.values()) if curve_out else 1
        for bucket, n in curve_out.items():
            bar = "█" * max(1, round(n * 32 / peak))
            lines.append(f"  {bucket:>2}  {bar} {n}")
        lines.append("")

        def card_line(rec):
            mark = "✓" if rec["legal"] else "✗"
            tag = " [both]" if rec["in_both"] else ""
            base = (
                f"  {mark} {rec['count']}x {rec['name'][:30]:<30} "
                f"{rec['mana_cost'] or '—':<14} {_short_type(rec['type_line'])[:20]:<20}{tag}"
            )
            if rec["reason"]:
                base += f"\n        ↳ {rec['reason']}"
            return base

        buckets = []
        if show in ("legal", "both"):
            buckets.append(("LEGAL", legal_cards))
        if show in ("illegal", "both"):
            buckets.append(("ILLEGAL", illegal_cards))
        for title, recs in buckets:
            lines.append(output.rule(f"{title} ({len(recs)})"))
            if not recs:
                lines.append("  (none)")
            shown = recs if limit <= 0 else recs[:limit]
            for rec in shown:
                lines.append(card_line(rec))
            if limit > 0 and len(recs) > limit:
                lines.append(f"  … {len(recs) - limit} more (use --limit 0 for all)")
            lines.append("")

        lines.append(output.rule("NOTES"))
        for note in payload["notes"]:
            lines.append(_bullet(note))

        return output.emit(payload, "\n".join(lines), as_json)
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
# registration
# --------------------------------------------------------------------------- #


def _add_goldfish_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("slug", help="deck slug, e.g. tidus")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="shuffle seed — the same seed always yields the identical game "
        "(default: a fresh random seed, reported in the output so you can replay it)",
    )
    parser.add_argument("--turns", type=int, default=8, help="turns to draw for (default 8)")
    parser.add_argument(
        "--mulligans",
        type=int,
        default=0,
        help="London mulligans to take before keeping (default 0)",
    )
    parser.add_argument(
        "--bottom",
        choices=("highest-cmc", "worst-lands"),
        default="highest-cmc",
        help="which cards go to the bottom after a mulligan (default highest-cmc)",
    )
    # Same flag as the global --json, accepted after the subcommand too.
    # SUPPRESS is essential: without it the subparser default would clobber the
    # value the root parser already stored for `mtg --json deck goldfish ...`.
    parser.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="emit machine-readable JSON (same as the global --json)",
    )
    parser.set_defaults(func=cmd_goldfish)


def _find_subparsers_action(parser: argparse.ArgumentParser):
    for action in parser._actions:  # noqa: SLF001 — argparse has no public accessor
        if isinstance(action, argparse._SubParsersAction):  # noqa: SLF001
            return action
    return None


def _positional_dest(parser: argparse.ArgumentParser):
    """dest of the positional that carries the sub-word, if the parser has one.

    Prefers a multi-value positional (nargs '*' or '+') because that is what a
    `mtg deck stats tidus` style parser uses to collect its words.
    """
    positionals = [a for a in parser._actions if not a.option_strings]  # noqa: SLF001
    for action in positionals:
        if action.nargs in ("*", "+"):
            return action.dest
    return positionals[0].dest if positionals else None


def _safe_add(parser: argparse.ArgumentParser, *flags, **kwargs) -> bool:
    """Add an optional only if none of its flags are already taken.

    We are decorating a parser another module owns; a name clash would raise at
    import time and take the whole CLI down, so check first.
    """
    taken = set()
    for action in parser._actions:  # noqa: SLF001
        taken.update(action.option_strings)
    if any(flag in taken for flag in flags):
        return False
    parser.add_argument(*flags, **kwargs)
    return True


def _graft_goldfish(deck_parser: argparse.ArgumentParser) -> None:
    """Make `mtg deck goldfish <slug>` work on a `deck` parser we do not own.

    cmd_decks registers `deck` with a free-form positional (`mtg deck stats
    tidus`), so there is no sub-command group to hang `goldfish` off and adding
    one would break its existing commands. Instead we add the goldfish flags to
    that parser and wrap its handler: if the first word is 'goldfish' we take
    the call, otherwise we hand straight back to cmd_decks.
    """
    dest = _positional_dest(deck_parser)
    if dest is None:
        return

    _safe_add(deck_parser, "--seed", type=int, default=None, help="[goldfish] shuffle seed")
    _safe_add(deck_parser, "--turns", type=int, default=8, help="[goldfish] turns to draw")
    _safe_add(
        deck_parser, "--mulligans", type=int, default=0, help="[goldfish] London mulligans to take"
    )
    _safe_add(
        deck_parser,
        "--bottom",
        choices=("highest-cmc", "worst-lands"),
        default="highest-cmc",
        help="[goldfish] which cards go to the bottom after a mulligan",
    )
    _safe_add(
        deck_parser,
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="emit machine-readable JSON (same as the global --json)",
    )

    inner = deck_parser.get_default("func")

    def dispatch(args, _inner=inner, _dest=dest):
        words = getattr(args, _dest, None) or []
        if isinstance(words, str):
            words = [words]
        if words and str(words[0]).lower() == "goldfish":
            rest = [w for w in words[1:] if w]
            if not rest:
                return output.fail(
                    "deck goldfish — no deck slug given (try: mtg deck goldfish tidus)",
                    _as_json(args),
                )
            if len(rest) > 1:
                return output.fail(
                    f"deck goldfish takes one deck, got {len(rest)}: {' '.join(rest)}",
                    _as_json(args),
                )
            args.slug = rest[0]
            return cmd_goldfish(args)
        if _inner is None:
            return output.fail("deck — no handler registered for this command", _as_json(args))
        return _inner(args)

    deck_parser.set_defaults(func=dispatch)
    if deck_parser.description:
        deck_parser.description += (
            "\nmtg deck goldfish <slug>     deterministic seeded goldfish "
            "(--seed --turns --mulligans)"
        )


def register(subparsers) -> None:
    # `deck` belongs to cmd_decks, which registers before us. Three cases:
    #   1. no `deck` parser yet     -> create one with a real sub-command group
    #   2. `deck` has subcommands   -> add `goldfish` to it
    #   3. `deck` takes positionals -> graft onto its handler (never bolt a
    #      subparser onto a parser that already has a positional; that breaks it)
    deck_parser = getattr(subparsers, "choices", {}).get("deck")
    if deck_parser is None:
        deck_parser = subparsers.add_parser("deck", help="deck tools")
        nested = deck_parser.add_subparsers(dest="deck_command", metavar="<subcommand>")
    else:
        nested = _find_subparsers_action(deck_parser)

    if nested is not None:
        if "goldfish" not in nested.choices:
            gp = nested.add_parser(
                "goldfish",
                help="deterministic seeded goldfish: opening hand, mulligans, draws, curve",
                description="Deterministic goldfish sim. Same --seed, same game, forever.",
            )
            _add_goldfish_args(gp)
    else:
        _graft_goldfish(deck_parser)

    # Top-level alias, always available, so the simulator stays reachable no
    # matter how `deck` is shaped by whoever owns it.
    if "goldfish" not in subparsers.choices:
        alias = subparsers.add_parser(
            "goldfish",
            help="alias for `deck goldfish` — deterministic seeded goldfish sim",
        )
        _add_goldfish_args(alias)

    mp = subparsers.add_parser(
        "merge",
        help="legal candidate pool for mixing two decks under one commander",
        description="Deterministic set operation: union of two main boards, "
        "marked legal/illegal against the chosen commander's colour identity.",
    )
    mp.add_argument("deck_a", help="first deck slug")
    mp.add_argument("deck_b", help="second deck slug")
    mp.add_argument("--commander", required=True, help='the commander to build under')
    mp.add_argument(
        "--show", choices=("legal", "illegal", "both"), default="both", help="which cards to list"
    )
    mp.add_argument(
        "--limit", type=int, default=40, help="max cards per section in text mode (0 = all)"
    )
    mp.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="emit machine-readable JSON (same as the global --json)",
    )
    mp.set_defaults(func=cmd_merge)
