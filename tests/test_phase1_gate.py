"""Phase 1 integrity gate for MTG Brain.

Adversarial, read-only verification of data/mtg.sqlite. This file NEVER writes to
the database and never mutates the repo -- it only asserts truths about the build.

Runs two ways:
    pytest tests/test_phase1_gate.py -v      (if pytest is installed)
    python3 tests/test_phase1_gate.py        (stdlib-only fallback runner)

Constraint C6 is respected: stdlib imports only (sqlite3, json, re, pathlib,
subprocess for the grep audit). No venv, no requirements.txt, no pip.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("MTG_BRAIN_DB", ROOT / "data" / "mtg.sqlite"))
SRC = ROOT / "src"

BASIC_NAMES = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}

EXPECTED_COMMANDERS = {
    "Tidus, Yuna's Guardian": {"G", "U", "W"},
    "Ms. Bumbleflower": {"G", "U", "W"},
    "Dogmeat, Ever Loyal": {"G", "R", "W"},
}

BANNED_TOKENS = [
    "openai",
    "anthropic",
    "api_key",
    "API_KEY",
    "embedding",
    "sentence_transformers",
    "langchain",
    "chromadb",
    "faiss",
    "pinecone",
]


# ------------------------------------------------------------------ helpers
def conn() -> sqlite3.Connection:
    """Read-only-ish connection. We never issue a write statement."""
    assert DB_PATH.exists(), f"database missing: {DB_PATH}"
    c = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def one(sql: str, args=()):
    c = conn()
    try:
        return c.execute(sql, args).fetchone()[0]
    finally:
        c.close()


def rows(sql: str, args=()):
    c = conn()
    try:
        return c.execute(sql, args).fetchall()
    finally:
        c.close()


def identity(raw) -> set:
    """color_identity is stored as a JSON array string."""
    if not raw:
        return set()
    try:
        return set(json.loads(raw))
    except (ValueError, TypeError):
        return set()


# ------------------------------------------------------------------- tests
def test_01_cards_rowcount():
    n = one("SELECT COUNT(*) FROM cards")
    assert n > 25_000, f"cards has {n} rows, expected > 25000"


def test_02_cards_fts_matches_cards():
    n_cards = one("SELECT COUNT(*) FROM cards")
    n_fts = one("SELECT COUNT(*) FROM cards_fts")
    assert n_fts == n_cards, f"cards_fts={n_fts} != cards={n_cards}"
    # stronger than a count: the key sets must align
    missing = one("SELECT COUNT(*) FROM cards WHERE oracle_id NOT IN (SELECT oracle_id FROM cards_fts)")
    assert missing == 0, f"{missing} cards have no cards_fts row"


def test_03_rulings():
    n = one("SELECT COUNT(*) FROM rulings")
    assert n > 50_000, f"rulings has {n} rows, expected > 50000"
    n_fts = one("SELECT COUNT(*) FROM rulings_fts")
    assert n_fts == n, f"rulings_fts={n_fts} != rulings={n}"


def test_04_rules():
    n = one("SELECT COUNT(*) FROM rules")
    assert n > 2_500, f"rules has {n} rows, expected > 2500"
    n_fts = one("SELECT COUNT(*) FROM rules_fts")
    assert n_fts == n, f"rules_fts={n_fts} != rules={n}"
    missing = one("SELECT COUNT(*) FROM rules WHERE rule_number NOT IN (SELECT rule_number FROM rules_fts)")
    assert missing == 0, f"{missing} rules have no rules_fts row"


def test_05_rule_numbers_normalized():
    bad = rows("SELECT rule_number FROM rules WHERE rule_number LIKE '%.'")
    assert not bad, f"{len(bad)} rule_numbers end in '.': {[r[0] for r in bad[:10]]}"


def test_06_rules_parent_linkage():
    orphans = rows(
        "SELECT r.rule_number, r.parent_number FROM rules r "
        "WHERE r.parent_number IS NOT NULL AND r.parent_number <> '' "
        "AND NOT EXISTS (SELECT 1 FROM rules p WHERE p.rule_number = r.parent_number)"
    )
    sample = [(r[0], r[1]) for r in orphans[:10]]
    assert not orphans, f"{len(orphans)} rules point at a missing parent; e.g. {sample}"


def test_07_glossary():
    n = one("SELECT COUNT(*) FROM glossary")
    assert n > 300, f"glossary has {n} rows, expected > 300"


def test_08_exactly_three_decks():
    n = one("SELECT COUNT(*) FROM decks")
    assert n == 3, f"decks has {n} rows, expected exactly 3"


def test_09_main_board_is_99():
    got = {
        r["deck_id"]: r["s"]
        for r in rows("SELECT deck_id, SUM(count) s FROM deck_cards WHERE board='main' GROUP BY deck_id")
    }
    all_decks = [r[0] for r in rows("SELECT deck_id FROM decks ORDER BY deck_id")]
    bad = [f"{d}={got.get(d)}" for d in all_decks if got.get(d) != 99]
    assert not bad, f"main board must sum to exactly 99; got {bad}"


def test_10_commander_board_is_1():
    got = {
        r["deck_id"]: r["s"]
        for r in rows("SELECT deck_id, SUM(count) s FROM deck_cards WHERE board='commander' GROUP BY deck_id")
    }
    all_decks = [r[0] for r in rows("SELECT deck_id FROM decks ORDER BY deck_id")]
    bad = [f"{d}={got.get(d)}" for d in all_decks if got.get(d) != 1]
    assert not bad, f"commander board must sum to exactly 1; got {bad}"


def test_11_no_orphan_deck_cards():
    orphans = rows(
        "SELECT dc.deck_id, dc.oracle_id, dc.board FROM deck_cards dc "
        "LEFT JOIN cards c ON c.oracle_id = dc.oracle_id WHERE c.oracle_id IS NULL"
    )
    assert not orphans, f"{len(orphans)} deck_cards have no cards row; e.g. {[tuple(r) for r in orphans[:10]]}"


def test_12_color_identity_subset_of_commander():
    cmd_identity = {}
    for r in rows(
        "SELECT dc.deck_id, c.name, c.color_identity FROM deck_cards dc "
        "JOIN cards c ON c.oracle_id = dc.oracle_id WHERE dc.board='commander'"
    ):
        cmd_identity[r["deck_id"]] = (r["name"], identity(r["color_identity"]))

    violations = []
    for r in rows(
        "SELECT dc.deck_id, dc.board, c.name, c.color_identity FROM deck_cards dc "
        "JOIN cards c ON c.oracle_id = dc.oracle_id"
    ):
        ci = identity(r["color_identity"])
        cname, cci = cmd_identity.get(r["deck_id"], ("<none>", set()))
        if not ci <= cci:
            violations.append(
                f"{r['deck_id']}/{r['board']}: {r['name']} {sorted(ci)} "
                f"not subset of commander {cname} {sorted(cci)}"
            )
    assert not violations, "color identity violations:\n" + "\n".join(violations)


def test_13_no_duplicate_nonbasics():
    violations = []
    for r in rows(
        "SELECT dc.deck_id, dc.board, dc.count, c.name, c.type_line FROM deck_cards dc "
        "JOIN cards c ON c.oracle_id = dc.oracle_id WHERE dc.count > 1"
    ):
        is_basic = r["name"] in BASIC_NAMES or "Basic Land" in (r["type_line"] or "")
        if not is_basic:
            violations.append(f"{r['deck_id']}/{r['board']}: {r['name']} x{r['count']} ({r['type_line']})")
    assert not violations, "non-basic duplicates:\n" + "\n".join(violations)


def test_14_commanders_present_with_expected_identity():
    problems = []
    for name, expected in EXPECTED_COMMANDERS.items():
        found = rows("SELECT color_identity FROM cards WHERE name = ?", (name,))
        if not found:
            problems.append(f"{name!r} not found in cards")
            continue
        got = identity(found[0]["color_identity"])
        if got != expected:
            problems.append(f"{name!r} identity {sorted(got)} != expected {sorted(expected)}")
    assert not problems, "; ".join(problems)


def test_15_brackets_json():
    p = ROOT / "data" / "brackets.json"
    assert p.exists(), f"missing {p}"
    data = json.loads(p.read_text(encoding="utf-8"))
    gc = data.get("game_changers")
    assert isinstance(gc, list), f"game_changers is {type(gc).__name__}, expected list"
    assert len(gc) > 0, "game_changers is empty"


def test_16_edhrec_cache():
    n = one("SELECT COUNT(*) FROM edhrec_cache")
    assert n == 3, f"edhrec_cache has {n} rows, expected exactly 3"
    small = [
        (r["slug"], r["n"])
        for r in rows("SELECT slug, LENGTH(payload_json) n FROM edhrec_cache")
        if (r["n"] or 0) <= 10 * 1024
    ]
    assert not small, f"edhrec payloads under 10KB: {small}"


def test_17_no_llm_dependencies_in_src():
    """C1: no LLM / embedding / hosted-vector-DB code anywhere in src/.

    Comments that merely *mention* a banned word while disclaiming it are
    tolerated; actual imports, package references, or key handling are not.
    """
    pattern = "|".join(re.escape(t) for t in BANNED_TOKENS)
    proc = subprocess.run(
        ["grep", "-rInE", pattern, str(SRC)],
        capture_output=True,
        text=True,
    )
    hits = [ln for ln in proc.stdout.splitlines() if ln.strip()]

    code_hits = []
    for ln in hits:
        try:
            _path, _lineno, body = ln.split(":", 2)
        except ValueError:
            code_hits.append(ln)
            continue
        stripped = body.strip()
        is_comment = stripped.startswith("#") or stripped.startswith("*") or stripped.startswith('"""')
        # A docstring/comment body that only disclaims is fine. Real code is not.
        looks_like_code = bool(
            re.search(r"^\s*(import|from)\s", body)
            or re.search(r"\b(import|require)\s*\(", body)
            or re.search(r"(api_key|API_KEY)\s*=", body)
        )
        if looks_like_code or not (is_comment or "constraint" in body.lower() or "C1" in body or "C6" in body):
            code_hits.append(ln)

    assert not code_hits, "C1 violations (real code references):\n" + "\n".join(code_hits)


def _requirement_name(line: str) -> str:
    """'pytest==9.1.1' -> 'pytest'. Extras/markers/versions all stripped."""
    text = line.split("#", 1)[0].strip()
    text = re.split(r"[<>=!~;\[]", text, maxsplit=1)[0]
    return text.strip().lower().replace("_", "-")


def test_18_stdlib_only():
    """C6: pytest is the ONLY dependency allowed to exist, and only for tests.

    (This assertion used to demand that no requirements.txt / .venv existed at
    all. pytest is now an explicitly sanctioned test-only dependency, so the
    rule is stated the way it actually is: requirements may name pytest and
    nothing else, and the runtime in src/ must import nothing third-party.)
    """
    skip_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
    reqs = [
        p
        for p in ROOT.rglob("requirements*.txt")
        if not skip_dirs & set(p.parts)
    ]
    for path in reqs:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            name = _requirement_name(line)
            if not name:
                continue
            assert name == "pytest", (
                f"{path}:{lineno} declares {name!r}; pytest is the only dependency "
                f"constraint C6 permits (and only for tests)"
            )

    # The real rule behind the old assertion: nothing in src/ may import a
    # third-party package, whether or not a venv happens to be sitting there.
    import ast

    local = {p.stem for p in SRC.glob("*.py")}
    offenders = {}
    for path in sorted(SRC.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module.split(".")[0]]
            for name in names:
                if name in local or name == "__future__" or name in sys.stdlib_module_names:
                    continue
                offenders.setdefault(path.name, set()).add(name)
    assert not offenders, f"third-party imports in src/: { {k: sorted(v) for k, v in offenders.items()} }"


# ------------------------------------------------------ stdlib fallback run
def _main() -> int:
    tests = sorted(
        (name, fn)
        for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    failures = []
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except AssertionError as exc:
            print(f"FAIL  {name}: {exc}")
            failures.append(name)
        except Exception as exc:  # noqa: BLE001 - gate must report, not crash
            print(f"ERROR {name}: {type(exc).__name__}: {exc}")
            failures.append(name)
    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_main())
