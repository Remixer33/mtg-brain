# MTG Brain

A local Magic: The Gathering **Commander** reference and coach, built around three preconstructed
decks you actually own. It holds every Magic card, every official ruling, and the entire
Comprehensive Rules in one SQLite file on this machine, so you can ask "what does this card do?"
or "can I respond to that?" and get a real, cited answer in under a second. It costs nothing to
run and, after one initial download, works with the wifi off.

**Commander (EDH) only.** No Standard, no Modern, no Limited, no sideboards.

---

## Setup — one command

```bash
cd /Users/omaralatas/Work/personal/mtg-brain
./bin/mtg rebuild
```

That downloads the card database from Scryfall, the Comprehensive Rules from Wizards, the three
decklists from MTGJSON, and the EDHREC recommendation pages — then builds `data/mtg.sqlite`.

**This is the only time you need the internet.** Every other command reads the local database and
never opens a socket. Re-run `rebuild` when a new set comes out or the rules get updated.
Add `--force` to re-download instead of reusing the cached files in `data/raw/`, or
`--only cards|rules|decks|edhrec` to refresh just one piece.

You need Python 3 and nothing else. The runtime imports only the Python standard library — there
are no packages to install and no API keys anywhere. (`requirements.txt` exists, but it holds
`pytest` and is for running the tests.)

### Confirm it's alive

```bash
./bin/mtg status
```

Real output:

```
── mtg brain status ──────────────────────────────────────────────────

  database   /Users/omaralatas/Work/personal/mtg-brain/data/mtg.sqlite
  size       149.7 MB  (156,946,432 bytes)

── tables ────────────────────────────────────────────────────────────
  cards               38,351
  glossary               735
  rules                3,309
  rulings             77,999
  ...

── last loaded ───────────────────────────────────────────────────────
  cards          2026-07-26 16:15 UTC
  rules          2026-07-26 16:14 UTC
  rules as of    2026-06-19

  STATUS: OK — all core tables populated, query path is fully offline.
```

If `STATUS` says anything other than OK, run `./bin/mtg rebuild`.

---

## Your first five minutes

Real commands, real output (trimmed for length — nothing invented).

### 1. What do I own?

```bash
./bin/mtg deck
```

```
── decks ─────────────────────────────────────────────────────────────
  bumbleflower   Peace Offering                   Ms. Bumbleflower         100 cards
  dogmeat        Scrappy Survivors                Dogmeat, Ever Loyal      100 cards
  tidus          Counter Blitz (FINAL FANTASY X)  Tidus, Yuna's Guardian   100 cards

  mtg deck <slug> | mtg deck stats <slug> | mtg deck bracket <slug>
```

`tidus`, `bumbleflower`, `dogmeat` are the **slugs** — the short names every command takes.
Any prefix of the deck name or the commander name works too (`./bin/mtg deck peace`).

### 2. What does my commander actually do?

```bash
./bin/mtg card "Tidus, Yuna's Guardian"
```

```
── Tidus, Yuna's Guardian ────────────────────────────────────────────────
Mana cost      : {G}{W}{U}
Mana value     : 3
Type           : Legendary Creature — Human Warrior

At the beginning of combat on your turn, you may move a counter from target
creature you control onto a second target creature you control.
Cheer — Whenever one or more creatures you control with counters on them
deal combat damage to a player, you may draw a card and proliferate. Do this
only once each turn.

P/T            : 3/3

Color identity : WUG (white, blue, green)
Keywords       : Proliferate, Cheer
Rarity         : mythic
Commander      : legal
EDHREC rank    : #3942
Price (USD)    : $2.60

── Rulings (5) ───────────────────────────────────────────────────────────
[2025-06-06] (wotc)
  Players can respond to a spell or ability whose effect includes
  proliferating. Once that spell or ability starts to resolve, however,
  and its controller chooses which permanents and players will get new
  counters, it's too late for anyone to respond.
  ...
```

Those rulings are the **official** Wizards rulings, not commentary. There are 77,999 of them in
the database. Add `--no-rulings` when you only want the card.

### 3. What bracket is my deck? (You get asked this before every game.)

```bash
./bin/mtg deck bracket tidus
```

```
ESTIMATED BRACKET 3 — Upgraded
  A precon that has been deliberately tuned, or a deck built to beat
  one. Stronger cards and tighter curve, still not cutthroat.

── SIGNALS ───────────────────────────────────────────────────────────
  Game Changers        : 1 (checked against 53 listed cards)
      • Farewell
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review

── REASONING ─────────────────────────────────────────────────────────
  - 1 Game Changer(s) found: Farewell. Brackets 1-2 both state 'No
    Game Changers.', while Bracket 3 (Upgraded) allows 'Up to 3
    Game Changers.' — so a single listed card lifts an otherwise
    precon-level deck to 3.
```

One card is the entire reason Counter Blitz is Bracket 3. Cut Farewell and it's Bracket 2.

### 4. Practice a hand without shuffling anything

```bash
./bin/mtg goldfish dogmeat --seed 7 --turns 4
```

```
── OPENING HAND (7) ──────────────────────────────────────────────────
  Explorer's Scope                 {1}                 1  Artifact
  Chaos Warp                       {2}{R}              3  Instant
  Junktown                         —                   0  Land
  Champion's Helm                  {3}                 3  Artifact
  Path to Exile                    {W}                 1  Instant
  Preston Garvey, Minuteman        {2}{R}{G}{W}        5  Legendary Creature
  Clifftop Retreat                 —                   0  Land

  lands in opener: 2

── RECOMMENDATION: KEEP ──────────────────────────────────────────────
  - 2 lands in the seven (deck runs 38; 2-5 is the keepable band).
  - Ramp/fixing at 3 or less: 0.
  - Interaction: 1 (Path to Exile).
  - Curve: 5 spells, average cmc 2.6, cheapest 1.
  - Heuristic advice from card counts only — not a rules ruling.

── TURNS ─────────────────────────────────────────────────────────────
T1  draw: Temple of the False God (land)
     lands seen 3 · in play 1 [W,R] · played Clifftop Retreat · hand 7
     castable: Explorer's Scope {1}, Path to Exile {W}
...
```

The **seed** makes it repeatable — `--seed 7` always deals that exact hand, so you can practice the
same decision twice. Leave `--seed` off and it picks a random one and prints it. Add
`--mulligans 1` to practice mulliganing.

### 5. Settle a rules argument

```bash
./bin/mtg rule 903.10a
```

```
── Rule 903.10a ──────────────────────────────────────────────────────────
parent: 903.10 — The Commander variant includes the following specification …

A player who's been dealt 21 or more combat damage by the same commander
over the course of the game loses the game. (This is a state-based action.
See rule 704.)
```

Don't know the number? Search the text instead: `./bin/mtg rule "deathtouch trample"`.
Don't know the word? `./bin/mtg glossary proliferate` gives the official definition plus the rule
numbers to chase.

---

## Your three decks

| Slug | Deck | Commander | Colors | Bracket |
|---|---|---|---|---|
| `tidus` | Counter Blitz (FINAL FANTASY X) | Tidus, Yuna's Guardian | Bant — green/white/blue | **3 — Upgraded** |
| `bumbleflower` | Peace Offering | Ms. Bumbleflower | Bant — green/white/blue | **2 — Core** |
| `dogmeat` | Scrappy Survivors | Dogmeat, Ever Loyal | Naya — green/red/white | **2 — Core** |

`tidus` is Bracket 3 only because of **Farewell**, a listed Game Changer. Both other decks are
Bracket 2, which is where a precon out of the box belongs.

`tidus` and `bumbleflower` are the same three colors, which is why you can physically build one
better deck out of both boxes without buying a single card. That merge is written up in
`decks/merged-bant/` — `MERGED-BANT.md` explains the choices, `DECKLIST.md` is the clean 100.

> Note: `merged-bant` is **documents only** — it is not loaded into the database, so
> `./bin/mtg deck merged-bant` will tell you it's not in the data. To work with the merge live,
> use `./bin/mtg merge tidus bumbleflower --commander "Tidus, Yuna's Guardian"`.

Each deck folder has three documents:

- `decks/<slug>/PRIMER.md` — the game plan. What the deck is trying to do, turn by turn.
- `decks/<slug>/CARDS.md` — card-by-card study guide.
- `decks/<slug>/UPGRADES.md` — what to change, what it costs, what it does to your bracket.

---

## The learning documents

These are the point of the whole system. They get better every time you play.

**`learning/RULES-I-KEEP-MISSING.md`** — every rule you've gotten wrong, ranked by how many times
you've gotten it wrong, with the official rule text. Add to it after a misplay:

```bash
./bin/mtg log rule --rule 903.4 --note "Forgot hybrid mana symbols count as both colors."
```

The command checks that the rule number is real before it writes, then rebuilds the whole file
from the database. Today it looks like this:

```
| Misses | Rule    | Last missed          |
|-------:|---------|----------------------|
|      2 | 903.4   | 2026-07-26 16:11 UTC |
|      1 | 903.10a | 2026-07-26 16:11 UTC |
```

That table is your study plan.

**`learning/GAME-LOG.md`** — what you played, against what, and what you'd do differently:

```bash
./bin/mtg log game --deck tidus --result loss --opponents "Bumbleflower, Dogmeat" \
                   --notes "Held counterspell mana all game and never used it."
```

Review either one with `./bin/mtg log rule --list` or `./bin/mtg log game --list`.

**`learning/GLOSSARY.md`** — a hand-written beginner's glossary of the terms you'll hit in your
first ten games (the stack, priority, instant speed, mana value, and so on). Every rule number in
it was pulled from the database, not written from memory. Start here if the jargon is what's
actually blocking you.

---

## PATH tip — running `mtg` from anywhere

Everything above says `./bin/mtg`, which only works from the project folder. To type just `mtg`
from any directory, add a **shell function** to `~/.zshrc`:

```bash
mtg() { /Users/omaralatas/Work/personal/mtg-brain/bin/mtg "$@"; }
```

Then `source ~/.zshrc`. Now `mtg status` works from anywhere. (An `alias` line works the same way.)

If you'd rather have it on your `PATH` as a real command, create a small **wrapper script** —
for example `~/bin/mtg`:

```bash
#!/usr/bin/env bash
exec /Users/omaralatas/Work/personal/mtg-brain/bin/mtg "$@"
```

`chmod +x ~/bin/mtg` and make sure `~/bin` is on your `PATH`.

**Do not use a bare symlink.** `ln -s .../bin/mtg /usr/local/bin/mtg` looks like it should work but
breaks: the launcher finds the project folder relative to its own location, and through a symlink
that resolves to the wrong place. Use the function or the wrapper script.

---

## Running the tests

```bash
./.venv/bin/python -m pytest tests/ -q
```

```
........................................................................ [ 24%]
........................................................................ [ 48%]
........................................................................ [ 72%]
........................................................................ [ 96%]
...........                                                              [100%]
299 passed in 14.78s
```

If you don't have the virtualenv, `python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt`
creates it. The tests cover the loaders, every CLI command, the simulator, and the two hard
constraints below — including a test that greps the source to prove no network or paid dependency
has snuck into the runtime.

---

## How this stays free

There is no API key anywhere in this repository, and there is no per-query cost. The split is:

- **SQLite FTS5 does the retrieval.** Full-text search over 38,351 cards, 77,999 rulings, 3,309
  rules, and 735 glossary entries runs locally, in milliseconds, on a 150 MB file. No embeddings,
  no vector database, no inference to find the right card.
- **Claude Code does the reasoning.** The model reads what SQLite returned and explains it. It
  never has to *remember* a card, which is also why the answers are trustworthy.
- **The runtime is pure Python standard library.** Nothing to install, nothing to pay for, nothing
  that phones home.
- **The network is touched exactly once**, by `mtg rebuild`, against free public sources (Scryfall,
  Wizards, MTGJSON, EDHREC).

Two constraints are enforced by the test suite so this can't quietly stop being true:

- **C1 — zero API spend.** No inference, embedding, or vector dependency may enter the runtime.
- **C2 — never hallucinate a card.** Every card fact and rules claim must come from the database.
  When something isn't there, the CLI says exactly that:

  ```
  $ ./bin/mtg card "Blastoise, Shellfire Titan"
  not in my data: card 'Blastoise, Shellfire Titan'
  ```

---

## Full command list

```
mtg card <name...> [--no-rulings]           card text + every official ruling
mtg search "<query>" [--limit N]            type: color: cmc<=N rarity: deck:<slug>
       [--order name|cmc|edhrec]            legal:commander is:<type> + free text
mtg rule <number> | "<query>"               exact rule lookup, or full-text search
mtg glossary <term...>                      official definition + related rules

mtg deck                                    list your decks
mtg deck <slug> [--group type|cmc|color]    the decklist
mtg deck stats <slug> [-v]                  curve, colors, mana sources, roles, assessment
mtg deck bracket <slug>                     estimated bracket 1-5 with reasoning
mtg goldfish <slug> [--seed N] [--turns N]  practice draws
       [--mulligans M] [--bottom highest-cmc|worst-lands]

mtg edhrec <commander> [--missing]          what other players run, from cache
       [--list "<header>"] [--limit N]
mtg merge <A> <B> --commander "<name>"      legal card pool for combining two decks

mtg log game --deck <slug> --result win|loss|draw --opponents "..." --notes "..."
mtg log rule --rule <number> --note "..."
mtg log game --list  |  mtg log rule --list

mtg status                                  database health
mtg rebuild [--only cards|rules|decks|edhrec] [--force]    the only networked command
```

Every command also takes `--json`.
