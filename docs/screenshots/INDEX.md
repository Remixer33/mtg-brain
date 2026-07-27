# Remy's Lair — screenshots

Captured 2026-07-27 from a live local run (`mtg dashboard --serve`, Chrome, 1456×829).
Every number, card and rule in these images came out of the local database — nothing is mocked
or hand-edited.

| # | File | What it shows |
|---|------|---------------|
| 01 | `01-lair-overview.jpg` | The shelf: all three precons side by side with commander, bracket, land count, average mana value and ramp — plus the Bant merge as a fourth tile. |
| 02 | `02-deck-header.jpg` | A single deck (Counter Blitz / Tidus): commander art, type line, verbatim oracle text, bracket chip, colour identity, set and release date. |
| 03 | `03-deck-charts-manabase.jpg` | The analysis: mana curve, colour sources by land, role counts — and the mana-base verdict, which shows its arithmetic and labels itself a heuristic, not a rule. |
| 04 | `04-deck-card-grid.jpg` | All 100 cards as real card images, grouped by type, filterable and sortable. |
| 05 | `05-cards-search-detail.jpg` | The card search across all 38,351 cards using the same query language as the terminal (`t:creature c:g cmc<=3` → 2,171 matches), with the detail pane open. |
| 06 | `06-rules-search.jpg` | The Comprehensive Rules, verbatim, full-text searchable ("commander damage" → 7 matches), with a curated "start here" list of the rules that actually decide a Commander game. |
| 07 | `07-glossary-priority.jpg` | The 735 official glossary terms. Rule references inside a definition become working links (here, "rule 117"). |
| 08 | `08-merge-bant.jpg` | The Bant merge — one 100-card deck built from two boxes with nothing bought, priced from local data. |
| 09 | `09-learning-loop.jpg` | The learning loop: games logged, rules missed ranked by frequency, the verbatim rule text, and the dated notes for each miss. |
| 10 | `10-cli-transcript.txt` | The other half of the system — real terminal output for `mtg card` and `mtg deck bracket`. Text, not an image. |

## Two things worth noticing

**Nothing is paraphrased.** Card text, rulings and rule text are inserted verbatim. Where the data
has a gap the page prints "not in my data" instead of guessing — screenshot 05 shows this: the
detail pane says the rulings are not in that payload rather than inventing them.

**It is fully offline.** No API keys, no inference, no per-query cost. The page makes zero network
requests — card art and fonts are cached locally, and the data ships as `.js` files so it runs
straight from `file://`.
