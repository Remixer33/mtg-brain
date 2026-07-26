#!/usr/bin/env python3
"""MTG Brain CLI — the agents' hands. Deterministic retrieval, zero AI.

Command modules live beside this file and each expose:

    register(subparsers) -> None     # add its argparse subcommands
                                     # set  parser.set_defaults(func=handler)

    handler(args) -> int             # print output, return an exit code

Every command must support --json (global flag) and emit machine-readable JSON
when it is set, so agents parse rather than scrape.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make sibling modules importable whether invoked as a script or a module.
sys.path.insert(0, str(Path(__file__).resolve().parent))

COMMAND_MODULES = (
    "cmd_cards",   # card, search, rule, glossary
    "cmd_decks",   # deck, deck stats, deck bracket, edhrec
    "cmd_sim",     # deck goldfish, merge
    "cmd_admin",   # rebuild, log
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mtg",
        description="MTG Brain — local Commander reference. Runs entirely offline.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of formatted text",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    for mod_name in COMMAND_MODULES:
        try:
            mod = __import__(mod_name)
        except ImportError:
            # A command module that isn't written yet must not break the others.
            continue
        register = getattr(mod, "register", None)
        if register:
            register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 1

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1

    return func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
