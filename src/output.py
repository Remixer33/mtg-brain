"""Shared output helpers so every command formats consistently.

Text mode is for Omar reading a terminal. JSON mode is for agents.
"""
from __future__ import annotations

import json
import sys
from typing import Any

# Mana symbol rendering stays as-is ({2}{G}{U}) — it is already the clearest
# plain-text form and matches what is printed on the card.


def emit(data: Any, text: str, as_json: bool) -> int:
    """Emit either the JSON payload or the human text. Returns exit code 0."""
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(text)
    return 0


def fail(message: str, as_json: bool = False, code: int = 1) -> int:
    """Emit a 'not in my data' style failure. Agents must surface this verbatim
    rather than guessing — see constraint C2."""
    if as_json:
        print(json.dumps({"ok": False, "error": message}, indent=2, ensure_ascii=False))
    else:
        print(f"not in my data: {message}", file=sys.stderr)
    return code


def rule(title: str = "", width: int = 72) -> str:
    if not title:
        return "─" * width
    pad = width - len(title) - 3
    return f"── {title} " + "─" * max(pad - 3, 0)


def wrap(text: str, width: int = 72, indent: str = "") -> str:
    """Wrap preserving intentional newlines (card oracle text is line-sensitive)."""
    import textwrap

    out = []
    for line in (text or "").split("\n"):
        if not line.strip():
            out.append("")
            continue
        out.extend(
            textwrap.wrap(
                line, width=width, initial_indent=indent, subsequent_indent=indent
            )
            or [""]
        )
    return "\n".join(out)


def json_list(value: str | None) -> list:
    """Columns like colors/color_identity/keywords are stored as JSON arrays."""
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (json.JSONDecodeError, TypeError):
        return []
