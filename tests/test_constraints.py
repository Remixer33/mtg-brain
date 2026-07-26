"""The constraints, as executable tests.

Requirement 14 — OFFLINE GUARANTEE (constraint C1): with socket construction
made impossible, every query-time command must still answer correctly. This is
the teeth behind "everything runs locally"; a command that quietly reached for
the network would raise here instead of silently costing money or breaking on a
plane. `rebuild` is the one exemption — it is the only networked command.

Requirement 15 — CONSTRAINT AUDIT (constraints C1 + C6): src/ is parsed with
`ast` and every imported top-level module is checked against an allowlist of
stdlib + local modules, so a third-party dependency cannot creep in unnoticed.
The LLM/vector-database ban is enforced on the *code*, via the AST — a docstring
that merely disclaims "no OpenAI here" is fine, an actual reference is not.

The audit does not stop at src/. `bin/mtg` — the shell script that *is* the
`mtg` command, and the entry point conftest shells out to — is scanned as text
as well, because an AST guard over src/*.py can never see a `curl` sitting in
the wrapper that launches it.
"""
from __future__ import annotations

import ast
import os
import socket
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT, SRC, TIMEOUT

sys.path.insert(0, str(SRC))

import cli as cli_module  # noqa: E402
import db  # noqa: E402

#: Recursive on purpose. src/ is flat today, but a plain glob("*.py") would let
#: a violation hide one directory down (src/helpers/__init__.py) where every AST
#: audit below is blind to it.
SRC_FILES = sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)
LOCAL_MODULES = {p.stem for p in SRC_FILES}

#: The runtime surface is bigger than src/. `bin/mtg` is what actually runs when
#: you type `mtg`, it is the only executable file in the tree, and every other
#: guard here globs src/*.py — so this is the one place it gets checked. The
#: glob is deliberate: anything dropped into bin/ later is covered on arrival.
BIN_DIR = ROOT / "bin"
ENTRY_POINT = BIN_DIR / "mtg"
BIN_FILES = sorted(p for p in BIN_DIR.glob("*") if p.is_file())

#: Stdlib modules this project is allowed to use. Constraint C6 names the core
#: set; the rest are stdlib helpers already in use by the loaders. Anything not
#: on this list has to be argued for — that is the point of the list.
STDLIB_ALLOWLIST = {
    "__future__",
    "argparse",
    "collections",
    "datetime",
    "gzip",
    "json",
    "os",
    "pathlib",
    "random",
    "re",
    "shutil",
    "sqlite3",
    "sys",
    "textwrap",
    "time",
    "typing",
    "urllib",  # rebuild path only — asserted below
}

#: Modules that make a network call possible. Only the loaders (the `rebuild`
#: path) may import them.
NETWORK_MODULES = {"urllib", "socket", "http", "ftplib", "requests", "httpx", "aiohttp"}
REBUILD_ONLY_FILES = {"load_cards", "load_rules", "load_edhrec", "load_decks"}

#: C1: no LLM / embedding / hosted-vector-store anything, as executable code.
BANNED_TOKENS = (
    "openai",
    "anthropic",
    "claude",
    "embedding",
    "embeddings",
    "langchain",
    "chromadb",
    "faiss",
    "pinecone",
    "sentence_transformers",
    "transformers",
    "torch",
    "tiktoken",
    "cohere",
    "ollama",
    "llama_cpp",
)

#: Shell has no `import` statement, so BANNED_TOKENS alone would not catch the
#: obvious way to break C1 from a wrapper script: one fetch command, or one
#: credential handed to it. Checked in bin/ only, on top of BANNED_TOKENS.
SHELL_BANNED_TOKENS = (
    "curl",
    "wget",
    "api.openai.com",
    "api.anthropic.com",
    "api_key",
    "apikey",
    "secret_key",
    "access_token",
    "authorization:",
    "pip install",
    # A wrapper does not need curl to reach the network — it can inline an
    # interpreter (`python3 -c "import urllib.request; ..."`) or open a raw
    # socket. Blocking only fetch *binaries* left that door open, so the
    # transport names and URL schemes are banned in bin/ too.
    "requests",
    "urllib",
    "socket",
    "http://",
    "https://",
    "nc ",
    "netcat",
    "ssh ",
    "scp ",
)

QUERY_COMMANDS = [
    ["card", "Sol Ring"],
    ["--json", "card", "Sol Ring"],
    ["search", "type:creature", "color:g", "cmc<=2"],
    ["search", "draw a card"],
    ["rule", "601.2"],
    ["rule", "commander damage"],
    ["glossary", "Commander"],
    ["deck"],
    ["deck", "tidus"],
    ["deck", "stats", "tidus"],
    ["deck", "bracket", "tidus"],
    ["edhrec", "tidus"],
    ["deck", "goldfish", "tidus", "--seed", "42"],
    ["goldfish", "dogmeat", "--seed", "1"],
    ["merge", "tidus", "bumbleflower", "--commander", "Tidus, Yuna's Guardian"],
    ["status"],
    ["log", "game", "--list"],
    ["log", "rule", "--list"],
]


# ------------------------------------------------------------------ helpers
def _imports_of(path: Path) -> set[str]:
    """Top-level module names imported by a file, per the AST."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                found.add(node.module.split(".")[0])
    return found


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """ids() of the Constant nodes that are docstrings, so they can be excused."""
    excused = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", None)
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                excused.add(id(body[0].value))
    return excused


# ------------------------------------------------------------- requirement 14
@pytest.fixture()
def no_network(monkeypatch):
    """Make any attempt to open a socket an immediate, loud failure."""

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "NETWORK ACCESS ATTEMPTED AT QUERY TIME — this breaks constraint C1 "
            "(the CLI must work fully offline)"
        )

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    monkeypatch.setattr(socket, "gethostbyname", forbidden, raising=False)
    return forbidden


@pytest.mark.parametrize("argv", QUERY_COMMANDS, ids=[" ".join(a) for a in QUERY_COMMANDS])
def test_query_commands_work_with_networking_disabled(no_network, monkeypatch, capsys, sandbox_db, argv):
    monkeypatch.setattr(db, "DB_PATH", sandbox_db)
    code = cli_module.main(list(argv))
    captured = capsys.readouterr()
    assert code == 0, (
        f"mtg {' '.join(argv)} failed with sockets disabled (exit {code})\n"
        f"{captured.out}\n{captured.err}"
    )
    assert captured.out.strip(), f"mtg {' '.join(argv)} produced no output offline"


def test_the_offline_guard_actually_bites(no_network):
    """Guard against a false-negative test: prove the monkeypatch really blocks."""
    with pytest.raises(AssertionError):
        socket.socket()


def test_query_modules_never_import_the_network_stack(monkeypatch, sandbox_db):
    """Stronger than 'it did not connect': the modules that answer queries must
    not even be able to — urllib/http must not be in sys.modules after a query
    runs in a clean interpreter."""
    script = (
        "import sys; sys.path.insert(0, %r)\n"
        "import cli\n"
        "rc = cli.main(['--json', 'card', 'Sol Ring'])\n"
        "leaked = sorted(m for m in ('urllib.request', 'http.client', 'ssl', 'socket') "
        "if m in sys.modules)\n"
        "sys.stderr.write('LEAKED=' + ','.join(leaked))\n"
        "sys.exit(rc)\n"
    ) % str(SRC)
    proc = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        cwd=str(ROOT),
        env={**os.environ, "MTG_BRAIN_DB": str(sandbox_db)},
    )
    assert proc.returncode == 0, proc.stderr
    marker = proc.stderr.rsplit("LEAKED=", 1)
    assert len(marker) == 2, f"probe did not report: {proc.stderr!r}"
    leaked = [m for m in marker[1].strip().split(",") if m]
    assert not leaked, (
        f"a plain `mtg card` query pulled the network stack into sys.modules: {leaked}"
    )


# ------------------------------------------------------------- requirement 15
def test_src_imports_are_stdlib_or_local_only():
    offenders = {}
    for path in SRC_FILES:
        for module in _imports_of(path):
            if module in LOCAL_MODULES or module in STDLIB_ALLOWLIST:
                continue
            offenders.setdefault(str(path.relative_to(SRC)), set()).add(module)
    assert not offenders, (
        "third-party (or unvetted) imports in src/ — constraint C6 is stdlib only:\n"
        + "\n".join(f"  {name}: {sorted(mods)}" for name, mods in offenders.items())
    )


def test_allowlist_itself_is_really_stdlib():
    """Belt and braces: nothing on the allowlist may be a package that happens to
    be installed in the venv."""
    not_stdlib = sorted(
        m for m in STDLIB_ALLOWLIST if m not in sys.stdlib_module_names and m != "__future__"
    )
    assert not not_stdlib, f"allowlist contains non-stdlib modules: {not_stdlib}"


def test_only_the_rebuild_loaders_import_the_network():
    offenders = {}
    for path in SRC_FILES:
        if path.stem in REBUILD_ONLY_FILES:
            continue
        network = _imports_of(path) & NETWORK_MODULES
        if network:
            offenders[str(path.relative_to(SRC))] = sorted(network)
    assert not offenders, (
        "C1: only the rebuild loaders may import networking:\n"
        + "\n".join(f"  {name}: {mods}" for name, mods in offenders.items())
    )


def test_no_llm_or_vector_code_anywhere_in_src():
    """AST-based, so a docstring that disclaims a banned tool stays legal while
    any executable reference to one fails."""
    offenders = []
    for path in SRC_FILES:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        excused = _docstring_nodes(tree)

        def flag(node, what):
            offenders.append(f"{path.relative_to(SRC)}:{getattr(node, 'lineno', '?')}  {what}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0].lower()
                    if any(token in root for token in BANNED_TOKENS):
                        flag(node, f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                root = (node.module or "").split(".")[0].lower()
                if node.level == 0 and any(token in root for token in BANNED_TOKENS):
                    flag(node, f"from {node.module} import ...")
            elif isinstance(node, ast.Name):
                if node.id.lower() in BANNED_TOKENS:
                    flag(node, f"name {node.id}")
            elif isinstance(node, ast.Attribute):
                if node.attr.lower() in BANNED_TOKENS:
                    flag(node, f"attribute .{node.attr}")
            elif isinstance(node, ast.keyword):
                if (node.arg or "").lower() in BANNED_TOKENS:
                    flag(node, f"keyword argument {node.arg}=")
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, str) and id(node) not in excused:
                    lowered = node.value.lower()
                    for token in BANNED_TOKENS:
                        # 'claude' inside a path/comment-ish string is still code
                        if token in lowered:
                            flag(node, f"string literal contains {token!r}")
                            break
    assert not offenders, (
        "C1 violations — LLM/embedding/vector references as executable code:\n"
        + "\n".join(offenders)
    )


def test_no_api_key_handling_in_src():
    """Zero LLM spend also means zero credential plumbing to spend it with."""
    offenders = []
    for path in SRC_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Name):
                names.append(node.id)
            elif isinstance(node, ast.Attribute):
                names.append(node.attr)
            elif isinstance(node, ast.keyword) and node.arg:
                names.append(node.arg)
            for name in names:
                lowered = name.lower()
                if "api_key" in lowered or lowered in {"apikey", "secret_key", "access_token"}:
                    offenders.append(f"{path.relative_to(SRC)}:{node.lineno}  {name}")
    assert not offenders, "credential handling found in src/:\n" + "\n".join(offenders)


def test_the_bin_scan_is_pointed_at_something_real():
    """Anti-false-negative, the same idea as `test_the_offline_guard_actually_bites`:
    a scan over an empty (or renamed, or moved) bin/ would pass forever while
    guarding nothing. Pin it to the entry point the test suite actually runs."""
    assert BIN_FILES, (
        f"no files found in {BIN_DIR} — the C1 scan below would pass vacuously"
    )
    assert ENTRY_POINT in BIN_FILES, (
        f"{ENTRY_POINT} is missing or is not a file; conftest shells out to it as "
        "the real CLI, so it is exactly the file that must stay clean"
    )


@pytest.mark.parametrize("path", BIN_FILES, ids=[p.name for p in BIN_FILES])
def test_no_llm_or_network_calls_in_the_shell_entry_point(path):
    """C1 outside src/: the wrapper script must not fetch, spend, or install.

    Unlike the src/ audits this is a literal text scan, not an AST walk — shell
    has no import graph to reason about, and a one-line `curl` is the whole
    attack. Consequence for whoever edits bin/ next: do not write these words
    here at all, not even in a comment. Say "no hosted-model calls" instead.
    """
    offenders = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        lowered = line.lower()
        for token in BANNED_TOKENS + SHELL_BANNED_TOKENS:
            if token in lowered:
                offenders.append(f"{path.relative_to(ROOT)}:{lineno}  {token!r} in {line.strip()!r}")
    assert not offenders, (
        "C1 violation in the CLI entry point — bin/ must stay offline and free of "
        "LLM/credential plumbing:\n" + "\n".join(offenders)
    )


def test_every_src_file_parses():
    """A syntax error in a command module is silently swallowed by cli.py's
    try/except ImportError, so it would show up as a *missing command* rather
    than a crash. Catch it here instead."""
    for path in SRC_FILES:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_all_command_modules_are_actually_registered():
    """cli.py skips a module that fails to import. That must never happen
    silently — every declared command module has to register something."""
    parser = cli_module.build_parser()
    choices = set()
    for action in parser._actions:  # noqa: SLF001 - argparse has no public accessor
        if hasattr(action, "choices") and isinstance(action.choices, dict):
            choices.update(action.choices)
    for command in ("card", "search", "rule", "glossary", "deck", "edhrec", "merge", "rebuild", "status", "log"):
        assert command in choices, f"'{command}' is not registered — did its module fail to import?"
