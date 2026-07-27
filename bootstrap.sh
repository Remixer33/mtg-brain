#!/usr/bin/env bash
# Bring a fresh clone of MTG Brain to a fully working state.
#
# The database, the raw downloads, the card art and the dashboard payloads are
# all derived artifacts (~470MB) and are deliberately NOT in git. This script
# rebuilds every one of them from free public sources. That is the whole point
# of constraint C5: one command, no secrets, no manual steps.
#
#   ./bootstrap.sh              full build (data + dashboard + art)
#   ./bootstrap.sh --data-only  skip the dashboard build
#
# Needs the network ONCE. After this finishes, everything runs offline.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

DATA_ONLY=0
[ "${1:-}" = "--data-only" ] && DATA_ONLY=1

say() { printf '\n\033[1;32m▸ %s\033[0m\n' "$1"; }

say "Python"
python3 --version

# pytest is the ONLY dependency, and it is test-only — the runtime is pure
# stdlib. Skip the venv entirely if you never intend to run the tests.
if [ ! -d .venv ]; then
  say "Creating .venv (pytest only — test harness, not a runtime dep)"
  python3 -m venv .venv
  ./.venv/bin/pip install -q --upgrade pip
  ./.venv/bin/pip install -q -r requirements.txt
fi

say "Building the database (Scryfall + Wizards CR + MTGJSON + EDHREC)"
echo "  ~227MB of downloads on a cold run; cached in data/raw/ afterwards."
./bin/mtg rebuild

if [ "$DATA_ONLY" -eq 0 ]; then
  say "Building Remy's Lair (data payloads + card art + webfonts)"
  ./bin/mtg dashboard --build
fi

say "Verifying"
./bin/mtg status | head -20
echo
./.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3

cat <<'DONE'

────────────────────────────────────────────────────────────────
MTG Brain is ready. Everything below runs offline, at zero cost.

  ./bin/mtg card "Sol Ring"
  ./bin/mtg deck stats tidus
  ./bin/mtg deck goldfish dogmeat --seed 42
  ./bin/mtg rule 903.10a
  ./bin/mtg dashboard --serve      # then open the printed URL

Open a Claude Code session in this directory and CLAUDE.md turns it into
the MTG Brain orchestrator — just ask a normal question, e.g.
"Teach me how to play my Tidus deck".
────────────────────────────────────────────────────────────────
DONE
