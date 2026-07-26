# Counter Blitz — Upgrade Path

**Deck:** Counter Blitz (FINAL FANTASY X) · slug `tidus`
**Commander:** Tidus, Yuna's Guardian — `{G}{W}{U}` — Bant (green/white/blue)
**Current estimated bracket:** **3 — Upgraded** (see *Bracket, honestly* below — it's a technicality)
**Format:** Commander / EDH only. Commander has **no sideboard** — the 100 cards you register are the whole deck (CR 903.5a: *"Each deck must contain exactly 100 cards, including its commander."*).

Every card fact, price and rules number in this file was pulled from the local database in the
session that wrote it. Prices are the `price_usd` field the database holds; where the database has
no price the file says **"price not in my data."**

---

## Table of contents

1. [What this deck actually needs](#1--what-this-deck-actually-needs)
2. [How the engine works (read this before swapping anything)](#2--how-the-engine-works)
3. [Tier 0 — Free (cards Omar already owns)](#3--tier-0--free)
4. [Tier 1 — Under $5 total](#4--tier-1--under-5-total)
5. [Tier 2 — Under $20 total](#5--tier-2--under-20-total)
6. [Tier 3 — Under $50 total](#6--tier-3--under-50-total)
7. [Do NOT buy these yet](#7--do-not-buy-these-yet)
8. [Bracket, honestly](#8--bracket-honestly)
9. [Running totals & the full swap ledger](#9--running-totals--the-full-swap-ledger)
10. [Verbatim CLI receipts](#10--verbatim-cli-receipts)
11. [A closing note](#11--a-closing-note)

---

## 1 · What this deck actually needs

Run this yourself any time: `./bin/mtg deck stats tidus -v`

Here are the numbers that matter, straight out of that command:

| Measurement | Number | What it means |
|---|---|---|
| Total cards | 100 (99 maindeck + 1 commander) | Legal. |
| Lands | 37 | The tool's verdict: **"land count: SANE."** |
| Lands that enter **tapped** | **16 of 37 (43%)** | Nearly half your lands cost you a turn of speed. |
| Average mana value, non-lands | **3.03** | *Mana value* = the total mana in a card's cost (CR 202.3). 3.03 is a normal EDH curve. |
| Ramp | 12 | Healthy. |
| Draw | 12 | Healthy. |
| Removal | 8 | Only **4** of those work at instant speed. |
| Board wipes | 4 | Cards that sweep many permanents at once. |
| **Interaction** | **3** | Counterspells + defensive protection. Out of 62 non-land cards, that is **4.8%**. |
| Recursion | 1 | |
| **Tutors** | **0** | A *tutor* is a card that searches your library for a specific non-land card. You have none. |
| **Win conditions** | **0** | No alternate-win card, no extra-combat, no damage doubler, no "you just win" big body. |

### The diagnosis, in plain language

**Problem 1 — the deck cannot protect what it builds. This is the big one.**
Your whole plan lives on the battlefield as counters sitting on creatures. Counters are physical
markers on a permanent (CR 122.1: *"A counter is a marker placed on an object or player that modifies
its characteristics…"*), and when the creature dies, the counters die with it. You have **3**
interaction cards out of 62 non-lands. One opposing *board wipe* (a spell that destroys or exiles all
creatures at once) erases three turns of work and you have almost nothing to say about it.

**Problem 2 — 8 removal spells, but only 4 answer anything on an opponent's turn.**
"Instant speed" means you can cast it whenever you have priority, including during someone else's
turn (CR 117.1a: *"A player may cast an instant spell any time they have priority."*). Your four
instant-speed answers are `Path to Exile`, `An Offer You Can't Refuse`, `Destroy Evil` and
`Endless Detour` — and `An Offer You Can't Refuse` reads *"Counter target noncreature spell,"* so it
cannot touch a creature spell at all. Everything else you own only works on your own main phase,
which means opponents get to untap and use their stuff first.

**Problem 3 — you have no clean answer to an artifact.**
Your artifact answers are: `Wakka, Devoted Guardian` (needs to connect in combat first),
`Summon: Yojimbo` chapter I (a Saga — it only fires when the chapter arrives), and
`Bane of Progress` / `Farewell` (huge sweepers that blow up **your own** `Hardened Scales`,
`Sphere Grid`, `Bred for the Hunt` and `Inexorable Tide` too). Nothing surgical, nothing instant.

**Problem 4 — 0 win conditions and 0 tutors means you cannot find or force anything.**
Tidus's Cheer ability only rewards **combat damage to a player**. If a board stalls behind blockers,
the deck has no button to press.

**Problem 5 — the top of the curve is bloated.**
9 cards cost 5 mana or more (6 at MV 5, 2 at MV 6, 1 at MV 7). In a deck whose engine wants to
deploy cheap creatures and attack, those are the cards you're stuck holding.

**A concrete illustration** — `./bin/mtg deck goldfish tidus --seed 7 --turns 8` (deterministic, no
opponents) draws a hand that hits 3 lands on turn 4 and then **misses its land drop on turns 5, 6 and
7**, ending turn 7 with **11 cards in hand** and only `Sphere Grid`-tier plays available. The deck's
bad draws are "I sit there." That is what the low curve and untapped-land fixes below are for.
(Caveat: the goldfish model ignores whether lands enter tapped, so it's actually *flattering* here.)

### Priority order for every dollar and every swap

1. **Protection** — keep the engine alive through a wipe.
2. **Evasion / a way to actually close the game** — Cheer needs damage to a *player*.
3. **Instant-speed, unconditional answers** — especially to artifacts and enchantments.
4. **Counter multipliers** — you own exactly one (`Hardened Scales`). Each extra one makes every
   other card in the deck better.
5. **Curve and mana smoothing** — cut the 5-, 6- and 7-drops; add lands that do something.

---

## 2 · How the engine works

Do not swap anything until you can see the loop. Deck names are flavour — "Counter Blitz" is not
about counterspells at all. Here is what the actual cards say.

**Your commander**, from `./bin/mtg card "Tidus, Yuna's Guardian"`:

> `{G}{W}{U}` · Legendary Creature — Human Warrior · 3/3
> *"At the beginning of combat on your turn, you may move a counter from target creature you control
> onto a second target creature you control."*
> *"Cheer — Whenever one or more creatures you control with counters on them deal combat damage to a
> player, you may draw a card and proliferate. Do this only once each turn."*

Two things a beginner will miss:

- Both abilities say **"a counter"** and **"counters"**, not "+1/+1 counters." Shield counters from
  `Protection Magic`, stun counters from `Lulu, Stern Guardian`, flying counters from
  `Luminous Broodmoth` — all of them switch Cheer on.
- **Proliferate** means *"choose any number of permanents and/or players that have a counter, then
  give each one additional counter of each kind that permanent or player already has"*
  (CR 701.34a). It only adds to things that **already** have a counter. It never starts one.
  Look it up any time with `./bin/mtg glossary proliferate`.

**The loop:**

1. Put a +1/+1 counter on something cheap. A **+1/+1 counter** adds +1 power and +1 toughness
   (CR 122.1a).
2. `Hardened Scales` — *"If one or more +1/+1 counters would be put on a creature you control, that
   many plus one +1/+1 counters are put on it instead"* — makes every single one of those bigger.
3. `Rikku, Resourceful Guardian` — *"Whenever you put one or more counters on a creature, until end
   of turn, that creature can't be blocked by creatures your opponents control"* — turns the act of
   adding a counter into evasion.
4. You connect. `Sphere Grid` — *"Whenever a creature you control deals combat damage to a player,
   put a +1/+1 counter on that creature"* — pays you again. Its Unlock Ability gives your countered
   creatures **reach and trample** (trample lets excess combat damage spill through to the player,
   CR 702.19a–b).
5. `Bred for the Hunt` and Tidus's Cheer refill your hand; Cheer also proliferates, growing
   everything at once.
6. `Wakka, Devoted Guardian`'s Blitzball Captain: *"At the beginning of your end step, if a counter
   was put on Wakka this turn, put a +1/+1 counter on each other creature you control."*
7. `Damning Verdict` — *"Destroy all creatures with no counters on them"* — is the payoff. Your board
   has counters. Theirs doesn't. It is a one-sided board wipe. **Never cut this card.**

Everything below is chosen to feed that loop, protect it, or finish with it.

---

## 3 · Tier 0 — Free

### Read this first: the honest cost

Omar owns three preconstructed decks:

| Slug | Deck | Colours |
|---|---|---|
| `tidus` | Counter Blitz | Bant — G/W/U |
| `bumbleflower` | Peace Offering | Bant — G/W/U |
| `dogmeat` | Scrappy Survivors | Naya — G/R/W |

A card is legal in a Commander deck only if its **colour identity** — the colours of every mana
symbol in its cost and rules text — fits inside the commander's (CR 903.4, CR 903.5c; try
`./bin/mtg glossary "color identity"`). `bumbleflower` is the same three colours as `tidus`, so
**anything** in it is legal here. `dogmeat` is Naya, so only its **white, green and colourless**
cards can move across — its red cards cannot.

**Physical cards exist in one place at a time.** Every swap in this tier makes another deck worse.
That is the real price, and it isn't zero. Two mitigations:

- **It's a trade, not a strip-mine.** Six of the seven cards leaving `tidus` in this tier
  (`Yuna's Whistle`, `Summoner's Sending`, `Scholar of New Horizons`, `Path of Discovery`,
  `Destroy Evil`, `Altered Ego`) are legal in `bumbleflower`, so they can slot straight into the hole
  you just made. `Sunscorch Regent` cannot — `bumbleflower` already runs a copy, and Commander is
  singleton (CR 903.5b: *"Other than basic lands, each card in a Commander deck must have a different
  English name"*).
- **If you only do three, do 0-1, 0-2 and 0-3.** They fix the two worst problems in section 1.

> ### ⚠️ Read this before you start moving cards: the other two upgrade paths exist
> `decks/bumbleflower/UPGRADES.md` and `decks/dogmeat/UPGRADES.md` have their own Tier 0 sections,
> written from their own deck's point of view, and **the three documents are not automatically
> compatible.** Each of these cards exists as exactly **one** physical copy (verified with
> `./bin/mtg deck <slug> --json`, count 1 for each), and two documents each tell you to take it:
>
> | Card | Lives in | Also claimed by | Effect |
> |---|---|---|---|
> | `Swords to Plowshares` | `bumbleflower` | tidus **0-1** vs dogmeat **T0-1** | mutually exclusive |
> | `Loran of the Third Path` | `bumbleflower` | tidus **0-4** vs dogmeat **T0-3** | mutually exclusive |
> | `Heroic Intervention` | `dogmeat` | tidus **0-2** vs bumbleflower **T0-3** | mutually exclusive |
> | `Rogue's Passage` | `dogmeat` | tidus **1-6** vs bumbleflower **T0-6** | this file prices it as a $0.38 buy so both can have one — see 1-6 |
>
> **And the traffic runs both ways.** `bumbleflower`'s Tier 0 takes `Damning Verdict`,
> `Hardened Scales` and `Inexorable Tide` **out of this deck**; `dogmeat`'s Tier 0 takes
> `Collective Effort`, `Brushland` and `Fortified Village`. That includes `Damning Verdict`, which
> section 2 above tells you to **never cut** — it is the single most on-theme card in the list and
> the reason the deck can wipe a board one-sidedly. **If you follow all three documents literally
> you will gut this deck.** Decide which deck is your main deck first, run *that* deck's path in
> full, and treat the other two as shopping lists.

---

### Swap 0-1 · Swords to Plowshares

- **IN:** `Swords to Plowshares` — `{W}` — Instant — **$1.30** — from `bumbleflower`
  > *"Exile target creature. Its controller gains life equal to its power."*
  > Official ruling (2022-12-08): *"Use the power of the creature from when it was last on the
  > battlefield to determine how much life is gained."*
- **OUT:** `Yuna's Whistle` — `{1}{G}{G}` — Instant. Three mana to dig for a random creature and put
  counters equal to its mana value on something. It's a coin flip that does nothing to the board, and
  it's the weakest instant you own. EDHREC has it in 31.3% of Tidus decks — the lowest of your
  instants that isn't already a cut.
- **Why:** One mana, exiles *anything*, at instant speed. This takes your instant-speed answer count
  from **4 → 5** and, unlike `Path to Exile`, doesn't hand an opponent a land. `Exile` also beats
  `destroy` — it dodges indestructible and recursion. It is the #11 most-played card in all of EDHREC
  and appears in 44.0% of Tidus decks.
- **Cost to `bumbleflower`:** significant. This is that deck's single best removal spell.
- **⚠️ Two upgrade paths want this same physical card.** `bumbleflower` contains exactly **one**
  `Swords to Plowshares` (verified: `./bin/mtg deck bumbleflower --json`, count 1), and
  `decks/dogmeat/UPGRADES.md` swap **T0-1** also moves that same copy into `dogmeat`. **These two
  swaps are mutually exclusive — you can do one of them, not both.** Pick the deck you play more,
  or buy a second copy for $1.30 and do both (the same framing used for `Heroic Intervention` in
  swap 0-2 below).
- **Bracket impact:** none. Not on the Game Changers list in `data/brackets.json`.

### Swap 0-2 · Heroic Intervention

- **IN:** `Heroic Intervention` — `{1}{G}` — Instant — **$16.17** — from `dogmeat`
  > *"Permanents you control gain hexproof and indestructible until end of turn."*
  > Official ruling (2020-06-23): *"The set of permanents affected by Heroic Intervention is
  > determined as the spell resolves. Permanents you begin to control later in the turn won't gain
  > hexproof and indestructible."*
- **OUT:** `Summoner's Sending` — `{1}{W}` — Enchantment. It exiles one creature card from a
  graveyard each end step for a 1/1 flier. Slow, and it does nothing for the counters loop.
  EDHREC: 25.7%.
- **Why:** This is the single biggest hole in the deck. **Hexproof** means *"This permanent can't be
  the target of spells or abilities your opponents control"* (CR 702.11b). **Indestructible** means
  the permanent *"can't be destroyed… aren't destroyed by lethal damage"* (CR 702.12b). For two mana
  at instant speed, your whole board survives a wipe. It takes interaction from **3 → 4** and is the
  most expensive card in this tier at $16.17 — which you get for free.
- **Cost to `dogmeat`:** **the highest cost of any swap in this document, and you should think about
  it.** `dogmeat` is an Aura and Equipment deck (`Rancor`, `All That Glitters`, `Mantle of the
  Ancients`, `Behemoth Sledge`…). When its creature dies, every Aura on it dies too. `Heroic
  Intervention` is that deck's only blanket protection spell. **Decide by which deck you play more.**
  If you play both equally, buy a second copy at Tier 3 money instead and leave `dogmeat` alone.
- **⚠️ Two upgrade paths want this same physical card.** `dogmeat` contains exactly **one**
  `Heroic Intervention` (verified: `./bin/mtg deck dogmeat --json`, count 1), and
  `decks/bumbleflower/UPGRADES.md` swap **T0-3** claims that same copy. So this one card is wanted
  by all three decks. Buying a second copy is the only way two of them get it.
- **Bracket impact:** none.

### Swap 0-3 · Rishkar, Peema Renegade

- **IN:** `Rishkar, Peema Renegade` — `{2}{G}` — Legendary Creature — Elf Druid — 2/2 — **$0.18** —
  from `bumbleflower`
  > *"When Rishkar enters, put a +1/+1 counter on each of up to two target creatures."*
  > *"Each creature you control with a counter on it has '{T}: Add {G}.'"*
  > Official ruling (2017-02-09): *"Each creature you control has Rishkar's mana ability as long as
  > that creature has **any kind of counter** on it. The effect isn't limited to those with +1/+1
  > counters."*
- **OUT:** `Scholar of New Horizons` — `{1}{W}` — Creature. Its ability reads *"{T}, Remove a counter
  from a permanent you control: Search your library for a Plains card…"* — it **removes** counters to
  find a land. That is backwards in a deck whose commander and payoffs all check for counters
  *staying on* creatures. EDHREC: 37.5%.
- **Why:** That ruling is the whole reason. Every creature with any counter — including shield and
  stun counters — becomes a mana source. It is both **ramp** and a **counter enabler** in one
  three-mana card, and it turns the wide board the deck naturally builds into real mana. Ramp goes
  **12 → 12** but the *quality* changes: this ramp scales with your board instead of sitting there.
- **Cost to `bumbleflower`:** moderate. That deck still has `Faeburrow Elder`, `Selvala, Explorer
  Returned` and `Coiling Oracle` doing similar work.
- **Bracket impact:** none.

### Swap 0-4 · Loran of the Third Path

- **IN:** `Loran of the Third Path` — `{2}{W}` — Legendary Creature — Human Artificer — 2/1 —
  **$3.81** — from `bumbleflower`
  > *"Vigilance"*
  > *"When Loran enters, destroy up to one target artifact or enchantment."*
  > *"{T}: You and target opponent each draw a card."*
- **OUT:** `Path of Discovery` — `{3}{G}` — Enchantment. Four mana that does absolutely nothing on the
  turn you cast it, and then gives a small bonus per creature afterwards. EDHREC: 19.6% — the lowest
  of your enchantments.
- **Why:** Problem 3. Your only surgical artifact/enchantment answers are attached to combat damage
  or to Sagas. This is a body **and** an answer, and it replaces a do-nothing four-drop with a
  three-drop. Removal goes **8 → 9**.
- **Cost to `bumbleflower`:** low. That deck also runs `Broken Wings` and `Wear Down` for the same job.
- **⚠️ Two upgrade paths want this same physical card.** `bumbleflower` contains exactly **one**
  `Loran of the Third Path` (verified: `./bin/mtg deck bumbleflower --json`, count 1), and
  `decks/dogmeat/UPGRADES.md` swap **T0-3** claims that same copy. **Mutually exclusive — do one,
  not both**, or buy a second copy for $3.81.
- **Bracket impact:** none.

### Swap 0-5 · Generous Gift

- **IN:** `Generous Gift` — `{2}{W}` — Instant — **$0.69** — from `bumbleflower`
  > *"Destroy target permanent. Its controller creates a 3/3 green Elephant creature token."*
- **OUT:** `Destroy Evil` — `{1}{W}` — Instant. *"Choose one — Destroy target creature with toughness
  4 or greater. • Destroy target enchantment."* Both modes are conditional; against a deck of small
  creatures the first mode is dead. EDHREC: 38.1%.
- **Why:** `Generous Gift` answers **any permanent type at instant speed** — creature, artifact,
  enchantment, planeswalker, even a land. It is a strict upgrade on `Destroy Evil` for one more mana,
  and it is the only card in the whole upgrade path that can answer a problem land. Note the
  downside honestly: the 3/3 Elephant they get is a real creature. Against your `Damning Verdict`
  that Elephant has no counters on it and dies, so the drawback is smaller here than in most decks.
- **Cost to `bumbleflower`:** moderate — it's that deck's catch-all.
- **Bracket impact:** none.

### Swap 0-6 · Kalonian Hydra

- **IN:** `Kalonian Hydra` — `{3}{G}{G}` — Creature — Hydra — 0/0 — **$6.37** — from `bumbleflower`
  > *"Trample"* · *"This creature enters with four +1/+1 counters on it."*
  > *"Whenever this creature attacks, double the number of +1/+1 counters on each creature you
  > control."*
  > Official ruling (2013-07-01): *"To double the number of +1/+1 counters on a creature, determine how
  > many +1/+1 counters are on the creature and put that many more on it."*
- **OUT:** `Sunscorch Regent` — `{3}{W}{W}` — Creature. A five-mana flier that grows when opponents
  cast spells. Fine, but it's a five-drop that does nothing the turn it lands and does not interact
  with the counters loop at all. EDHREC: 29.3%.
- **Why:** Because that ruling plus `Hardened Scales` is a real number: it *doubles* every counter on
  every creature, every attack. It is a genuine finisher in a deck the stats tool says has
  **0 win conditions**. It also swaps a five-drop for a five-drop, so the curve doesn't move.
- **Cost to `bumbleflower`:** high. That deck has a counters sub-theme (`Managorger Hydra`,
  `Forgotten Ancient`, `Simic Ascendancy`) and this is its top end. **If you take both this and
  swap 0-7, that sub-theme is basically gone.** Pick one, or buy a copy at Tier 3 money.
- **Bracket impact:** none.

### Swap 0-7 · Simic Ascendancy

- **IN:** `Simic Ascendancy` — `{G}{U}` — Enchantment — **$0.44** — from `bumbleflower`
  > *"{1}{G}{U}: Put a +1/+1 counter on target creature you control."*
  > *"Whenever one or more +1/+1 counters are put on a creature you control, put that many growth
  > counters on this enchantment."*
  > *"At the beginning of your upkeep, if this enchantment has twenty or more growth counters on it,
  > you win the game."*
- **OUT:** `Altered Ego` — `{X}{2}{G}{U}` — Creature — Shapeshifter. A clone. Copying an opponent's
  best creature is fine, but it costs at least four mana to do nothing on its own, and it is the
  least-played creature in your deck at **18.8%** on EDHREC.
- **Why:** `mtg deck stats tidus -v` says **wincon 0**. This is a literal, stated win condition that
  charges itself off the thing your deck already does more than anything else — and `Hardened Scales`,
  `Conclave Mentor` and the doublers below all make it charge faster. Twenty growth counters sounds
  like a lot; with a wide board and Cheer proliferating each turn it isn't.
- **Cost to `bumbleflower`:** low-to-moderate — it's a cute card there, a real plan here.
- **Bracket impact:** **none.** An alternate-win card is *not* a Game Changer and is not restricted at
  Bracket 2 — the Bracket 1/2 restrictions in `data/brackets.json` are "No Game Changers. No mass land
  denial. No chaining extra turns. No two-card infinite combos." A slow alt-win is fine.

**Tier 0 running total: $0.00 spent.** Value moved into the deck: **$28.96** at database prices
($1.30 + $16.17 + $0.18 + $3.81 + $0.69 + $6.37 + $0.44).

---

## 4 · Tier 1 — Under $5 total

Eight swaps, **$3.77 total.** This tier is the best value in the entire document — it is almost all
sub-$1 cards that do exactly what section 1 says the deck is missing.

| # | IN | Price | Running |
|---|---|---|---|
| 1-1 | Thrummingbird | $0.26 | $0.26 |
| 1-2 | Metastatic Evangel | $0.40 | $0.66 |
| 1-3 | Conclave Mentor | $0.71 | $1.37 |
| 1-4 | Luminarch Aspirant | $0.37 | $1.74 |
| 1-5 | Beast Within | $0.48 | $2.22 |
| 1-6 | Rogue's Passage | $0.38 | $2.60 |
| 1-7 | Ezuri, Stalker of Spheres | $0.92 | $3.52 |
| 1-8 | Return to Nature | $0.25 | **$3.77** |

---

### Swap 1-1 · Thrummingbird

- **IN:** `Thrummingbird` — `{1}{U}` — Creature — Phyrexian Bird Horror — 1/1 — **$0.26**
  > *"Flying"*
  > *"Whenever this creature deals combat damage to a player, proliferate."*
- **OUT:** `Lord Jyscal Guado` — `{1}{W}` — Legendary Creature — Spirit Cleric. It investigates
  (makes a Clue token) at each end step if you put a counter on a creature that turn. That's a
  two-mana-per-card draw engine, which is slow. It is the **least-played card in your entire deck**
  at **17.9%** on EDHREC.
- **Why:** A two-mana flier that proliferates every time it connects. Flying is the cheapest evasion
  in the deck, and this triggers Tidus's Cheer *and* proliferates in the same swing. EDHREC has it in
  34.3% of Tidus decks. Beginner note: proliferate only adds counters to things that already have
  one, so play it *after* you've started putting counters out, not before.
- **Bracket impact:** none.

### Swap 1-2 · Metastatic Evangel

- **IN:** `Metastatic Evangel` — `{1}{W}` — Creature — Phyrexian Human Cleric — 3/1 — **$0.40**
  > *"Whenever another nontoken creature you control enters, proliferate."*
- **OUT:** `Summon: Valefor` — `{4}{U}` — Enchantment Creature — Saga Drake. A five-mana Saga whose
  chapter I bounces one creature per opponent back to hand — temporary, and it hands them their
  creature back to recast. EDHREC: 37.2%. It's one of the nine 5-plus-mana cards clogging your top end.
- **Why:** Free proliferate on **every creature you cast** for two mana. In a deck with 34 creatures
  this fires constantly, and each trigger grows your whole counter-laden board. It also swaps a
  five-drop for a two-drop, which is the curve fix Problem 5 asks for.
- **Bracket impact:** none.

### Swap 1-3 · Conclave Mentor

- **IN:** `Conclave Mentor` — `{G}{W}` — Creature — Centaur Cleric — 2/2 — **$0.71**
  > *"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1
  > counters are put on that creature instead."*
  > *"When this creature dies, you gain life equal to its power."*
  > Official ruling (2020-06-23): *"If two or more effects attempt to modify how many counters would
  > be put onto a creature you control, **you choose the order** to apply those effects, no matter who
  > controls the sources of those effects."*
- **OUT:** `Summon: Magus Sisters` — `{4}{G}` — Enchantment Creature — Saga Faerie. Each chapter picks
  one of three modes **at random**. Five mana for a coin flip is not a plan. EDHREC: 29.2%.
- **Why:** This is a second `Hardened Scales` on a body. You own exactly one counter multiplier today;
  this doubles that count for 71 cents. The ruling above is the important beginner lesson: when you
  have several of these, **apply the "plus one" effects first and the doubling effects last** — 1
  counter → +1 (Mentor) = 2 → +1 (Scales) = 3 → doubled (Branching Evolution, Tier 3) = 6. Applying
  the doubler first would only give you 4.
- **Bracket impact:** none.

### Swap 1-4 · Luminarch Aspirant

- **IN:** `Luminarch Aspirant` — `{1}{W}` — Creature — Human Cleric — 1/1 — **$0.37**
  > *"At the beginning of combat on your turn, put a +1/+1 counter on target creature you control."*
  > Official ruling (2020-09-25): *"Luminarch Aspirant can be the target of its own ability."*
- **OUT:** `Chasm Skulker` — `{2}{U}` — Creature — Squid Horror. It grows on draws and leaves Squid
  tokens when it dies — but those tokens have no counters, so `Damning Verdict` kills them and Cheer
  ignores them. EDHREC: 33.6%.
- **Why:** A free counter every single combat, on *any* creature you control, for two mana. It fires at
  the beginning of combat — the same step as Tidus's counter-moving trigger and `Maester Seymour`'s —
  so you get to sequence them. Crucially, putting that counter on a creature switches on
  `Rikku, Resourceful Guardian`'s unblockable trigger for that creature that turn.
- **Bracket impact:** none.

### Swap 1-5 · Beast Within

- **IN:** `Beast Within` — `{2}{G}` — Instant — **$0.48**
  > *"Destroy target permanent. Its controller creates a 3/3 green Beast creature token."*
- **OUT:** `Yuna's Decision` — `{3}{G}` — Sorcery. The stats tool credits this card in four role
  columns (ramp, draw, removal, recursion) but it says **"Choose one"** — it only ever does one of
  those things, and its first mode makes you **sacrifice a creature**, which is actively bad when your
  value is stored as counters on creatures. EDHREC: 32.4%.
- **Why:** The green half of `Generous Gift`. Three mana, instant speed, destroys **any permanent**.
  Together with swaps 0-1, 0-5 and 1-8, your instant-speed answers go from 4 to 7 by the end of
  Tier 1 — and for the first time you can answer an opposing artifact or enchantment on their turn.
- **Bracket impact:** none.

### Swap 1-6 · Rogue's Passage

- **IN:** `Rogue's Passage` — Land — **$0.38**
  > *"{T}: Add {C}."* · *"{4}, {T}: Target creature can't be blocked this turn."*
  > Official ruling (2018-12-07): *"Activating the second ability of Rogue's Passage after a creature
  > has become blocked won't cause that creature to become unblocked."* (So use it **before** blockers
  > are declared.)
- **OUT:** `Temple of the False God` — Land. *"{T}: Add {C}{C}. Activate only if you control five or
  more lands."* Before your fifth land it produces **nothing at all** — it is not even a land that
  taps for one. It is the single worst land in the deck.
- **Why:** Land-for-land, so your land count stays at 37 and the stats tool's "land count: SANE"
  verdict holds. But this land is a **win condition** in a deck the tool scores at **wincon 0**: point
  it at a creature carrying half your counters, and Tidus's Cheer + `Bred for the Hunt` fire for free.
  It also enters untapped, chipping at the 43%-tapped problem.
- **You may not have to buy this at all — it's a Tier 0 candidate.** `dogmeat` already runs a copy
  (verified: `./bin/mtg deck dogmeat --json`, count 1), and `Rogue's Passage` has an **empty colour
  identity** — it is a colourless land, so it is legal in every deck you own (CR 903.4). Move it and
  this swap costs $0.00, exactly like swap 0-2. It is priced here as a purchase for two reasons:
  `decks/bumbleflower/UPGRADES.md` swap **T0-6** claims that same single copy, and `dogmeat` is a
  Voltron deck that genuinely wants it. **If you'd rather not spend, move `dogmeat`'s copy and drop
  Tier 1 to $3.39; if you want it in two decks, $0.38 is the cheapest second copy in this document.**
- **Bracket impact:** none.

### Swap 1-7 · Ezuri, Stalker of Spheres

- **IN:** `Ezuri, Stalker of Spheres` — `{2}{G}{U}` — Legendary Creature — Phyrexian Elf Warrior —
  3/3 — **$0.92**
  > *"When Ezuri enters, you may pay {3}. If you do, proliferate twice."*
  > *"Whenever you proliferate, draw a card."*
  > Official ruling (2023-02-04): *"If you proliferate twice, you don't have to choose the same set of
  > players and/or permanents to get additional counters each time."*
- **OUT:** `Rampant Rejuvenator` — `{3}{G}` — Creature — Plant Hydra. Its ramp only happens **when it
  dies**, which means you have to want your own creature dead — the opposite of the deck's plan.
  EDHREC: 27.8%.
- **Why:** Your deck proliferates a *lot* — Tidus's Cheer, `Inexorable Tide` (*"Whenever you cast a
  spell, proliferate"*), `Grateful Apparition`, `Tromell`, `Lulu`, and now `Thrummingbird`,
  `Metastatic Evangel` and (Tier 2) `Evolution Sage`. This turns every one of those into a card. Note
  the ruling above: proliferating twice lets you pick different targets each time.
- **Bracket impact:** none.

### Swap 1-8 · Return to Nature

- **IN:** `Return to Nature` — `{1}{G}` — Instant — **$0.25**
  > *"Choose one — • Destroy target artifact. • Destroy target enchantment. • Exile target card from a
  > graveyard."*
- **OUT:** `Promise of Loyalty` — `{4}{W}` — Sorcery. *"Each player puts a vow counter on a creature
  they control and sacrifices the rest."* Read that again: **you** sacrifice down to one creature too.
  In a deck that wins by having a wide board of countered creatures, that is a five-mana card that
  destroys your own game plan. EDHREC: 33.9%. It is your weakest of the four board wipes by a mile.
- **Why:** Two mana, instant speed, hits the two permanent types you currently cannot answer cleanly.
  Cutting a symmetrical wipe drops board wipes 4 → 3, which is correct: `Damning Verdict` is
  one-sided in your favour and `Farewell` is discussed in Tier 3.
- **Bracket impact:** none.

**Tier 1 running total: $3.77.** Under the $5 cap.
**Cumulative spend after Tier 1: $3.77.**

---

## 5 · Tier 2 — Under $20 total

Seven swaps, **$18.01 total.** This tier buys the engine pieces — multipliers and repeatable
proliferate — plus real protection.

| # | IN | Price | Running |
|---|---|---|---|
| 2-1 | Ozolith, the Shattered Spire | $5.20 | $5.20 |
| 2-2 | Kami of Whispered Hopes | $2.94 | $8.14 |
| 2-3 | Ripples of Potential | $2.94 | $11.08 |
| 2-4 | Karn's Bastion | $2.26 | $13.34 |
| 2-5 | Evolution Sage | $2.25 | $15.59 |
| 2-6 | Tekuthal, Inquiry Dominus | $1.24 | $16.83 |
| 2-7 | Unbreakable Formation | $1.18 | **$18.01** |

---

### Swap 2-1 · Ozolith, the Shattered Spire

- **IN:** `Ozolith, the Shattered Spire` — `{1}{G}` — Legendary Artifact — **$5.20**
  > *"If one or more +1/+1 counters would be put on an artifact or creature you control, that many plus
  > one +1/+1 counters are put on it instead."*
  > *"{1}{G}, {T}: Put a +1/+1 counter on target artifact or creature you control. Activate only as a
  > sorcery."*
  > *"Cycling {2} ({2}, Discard this card: Draw a card.)"*
  > Official ruling (2023-04-14): *"If another artifact or creature you control would enter the
  > battlefield with a number of +1/+1 counters on it, it enters with that many plus one instead."*
- **OUT:** `Blitzball Stadium` — `{X}{U}` — Artifact. Its unblockable-and-draw mode costs **{3} and a
  tap** on top of the X you already paid to cast it. Too many mana, too slow, and `Rikku` and
  `Rogue's Passage` do the unblockable job cheaper.
- **Why:** Multiplier number three. It is also the only one that grows on `Walking Ballista` (an
  Artifact Creature) *and* has **cycling** — a keyword meaning you may pay {2} and discard it to draw
  a card, so it is never a dead card in a slow hand. Its own activated ability means it makes counters
  by itself with no creatures at all, which matters after a wipe.
- **Bracket impact:** none.

### Swap 2-2 · Kami of Whispered Hopes

- **IN:** `Kami of Whispered Hopes` — `{2}{G}` — Creature — Spirit — 1/1 — **$2.94**
  > *"If one or more +1/+1 counters would be put on a permanent you control, that many plus one +1/+1
  > counters are put on that permanent instead."*
  > *"{T}: Add X mana of any one color, where X is this creature's power."*
- **OUT:** `Sin, Unending Cataclysm` — `{5}{G}{U}` — Legendary Creature. Your only seven-drop, in a
  deck with an average non-land mana value of **3.03**. Its enter effect *removes* all counters from
  permanents to convert them, which fights the deck's own payoffs (`Damning Verdict` wants counters
  to still be there). EDHREC: 41.1%.
- **Why:** Multiplier number four **and** ramp that scales — because its mana ability keys off its own
  power, and its own +1/+1 counters get the "plus one" from `Hardened Scales`, `Conclave Mentor` and
  `Ozolith`. It appears in **46.5%** of Tidus decks on EDHREC, the highest-played card you don't own.
  Cutting the seven-drop takes your MV-5-and-up count from 9 to 8 on the way to 3.
- **Bracket impact:** none.

### Swap 2-3 · Ripples of Potential

- **IN:** `Ripples of Potential` — `{1}{U}` — Instant — **$2.94**
  > *"Proliferate, then choose any number of permanents you control that had a counter put on them
  > this way. Those permanents phase out."*
- **OUT:** `Pull from Tomorrow` — `{X}{U}{U}` — Instant. *"Draw X cards, then discard a card."* It's
  fine, but it's a pure X-spell in a deck that already runs 12 draw pieces and wants its mana on the
  battlefield. EDHREC: 20.3% — the second-lowest instant in your deck.
- **Why:** Two mana at instant speed that **proliferates and then saves your board from a wipe**.
  *Phasing out* means the permanents are treated as though they don't exist until your untap step —
  so a board wipe, a targeted removal spell, or a big attack simply misses them, and they come back
  with the counters intact. This is protection #2 (after `Heroic Intervention`) and takes interaction
  from **4 → 5**. EDHREC: 33.0% of Tidus decks.
- **Bracket impact:** none.

### Swap 2-4 · Karn's Bastion

- **IN:** `Karn's Bastion` — Land — **$2.26**
  > *"{T}: Add {C}."* · *"{4}, {T}: Proliferate."*
- **OUT:** `Skycloud Expanse` — Land. Its **only** ability is *"{1}, {T}: Add {W}{U}."* It cannot tap
  for a single mana on its own, so if it's your first or second land it produces nothing. That is a
  serious liability in a deck already carrying 16 tapped lands.
- **Why:** Land-for-land — count stays 37. This is a **repeatable proliferate from a land**, which
  means late-game flood turns into board growth. It also feeds `Ezuri` (draw a card whenever you
  proliferate) and `Tekuthal` below. EDHREC: 30.2%, the highest-played utility land you don't own.
- **Bracket impact:** none.

### Swap 2-5 · Evolution Sage

- **IN:** `Evolution Sage` — `{2}{G}` — Creature — Elf Druid — 3/2 — **$2.25**
  > *"Landfall — Whenever a land you control enters, proliferate."*
- **OUT:** `Fight Rigging` — `{2}{G}` — Enchantment. The free counter each combat is real, but its
  Hideaway payoff requires *"a creature with power 7 or greater"*, which this deck reaches
  inconsistently, so most games it's a worse `Luminarch Aspirant`. EDHREC: 35.8%.
- **Why:** **Landfall** means "whenever a land you control enters." You play a land almost every turn,
  and you run `Farseek`, `Three Visits`, `Ash Barrens` and `Evolving Wilds` to trigger it more than
  once. That is a free proliferate most turns for three mana, and another `Ezuri` trigger.
  EDHREC: 27.1%.
- **Bracket impact:** none.

### Swap 2-6 · Tekuthal, Inquiry Dominus

- **IN:** `Tekuthal, Inquiry Dominus` — `{2}{U}{U}` — Legendary Creature — Phyrexian Horror — 3/5 —
  **$1.24**
  > *"Flying"*
  > *"If you would proliferate, proliferate twice instead."*
  > *"{1}{U/P}{U/P}, Remove three counters from among other artifacts, creatures, and planeswalkers you
  > control: Put an indestructible counter on Tekuthal."*
- **OUT:** `O'aka, Traveling Merchant` — `{1}{U}` — Legendary Creature. *"{T}, Remove a counter from a
  nonland permanent you control: Draw a card."* Like `Scholar of New Horizons`, it pays you by
  **removing** counters — the resource `Damning Verdict`, Cheer, `Bred for the Hunt` and `Rikku` all
  need to stay put. It's popular in the precon crowd (54.9%) mostly because it shipped in the box.
- **Why:** This is the highest-synergy creature you don't own on EDHREC (**52.3%** of Tidus decks,
  +47.9% synergy). Doubling every proliferate doubles Cheer, `Inexorable Tide`, `Grateful Apparition`,
  `Thrummingbird`, `Evolution Sage`, `Metastatic Evangel` and `Karn's Bastion` all at once. A 3/5
  flier also blocks well.
- **Caution, stated plainly:** `{2}{U}{U}` needs **two blue mana**. `mtg deck stats tidus -v` counts
  **19 blue sources**. That's castable but not free — expect to sometimes hold it a turn.
- **Bracket impact:** none.

### Swap 2-7 · Unbreakable Formation

- **IN:** `Unbreakable Formation` — `{2}{W}` — Instant — **$1.18**
  > *"Creatures you control gain indestructible until end of turn."*
  > *"Addendum — If you cast this spell during your main phase, put a +1/+1 counter on each of those
  > creatures and they gain vigilance until end of turn."*
- **OUT:** `Collective Effort` — `{1}{W}{W}` — Sorcery. Its escalate cost (tap an untapped creature per
  extra mode) competes directly with attacking, and its creature mode only kills *"target creature with
  power 4 or greater."* Sorcery speed, conditional. EDHREC: 48.2%.
- **Why:** Protection #3, and a flexible one — **Addendum** means that if you cast it on your own main
  phase it *also* puts a +1/+1 counter on every creature you control, which with `Hardened Scales` +
  `Conclave Mentor` + `Ozolith` is a genuine board pump that turns on `Rikku`'s unblockable trigger for
  your whole team. Held up on an opponent's turn instead, it's an anti-wipe. Interaction goes
  **5 → 6**.
- **Bracket impact:** none.

**Tier 2 running total: $18.01.** Under the $20 cap.
**Cumulative spend after Tiers 1+2: $21.78.**

---

## 6 · Tier 3 — Under $50 total

Nine swaps, **$40.99 total** — $9.01 of headroom left under the cap. This tier converts the engine
into a deck that closes games, and includes the one swap that changes the deck's bracket.

| # | IN | Price | Running |
|---|---|---|---|
| 3-1 | Herald of Secret Streams | $8.81 | $8.81 |
| 3-2 | Innkeeper's Talent | $7.99 | $16.80 |
| 3-3 | Branching Evolution | $6.85 | $23.65 |
| 3-4 | Gavony Township | $5.42 | $29.07 |
| 3-5 | Champion of Lambholt | $4.20 | $33.27 |
| 3-6 | Kutzil, Malamet Exemplar | $3.93 | $37.20 |
| 3-7 | Swiftfoot Boots | $1.99 | $39.19 |
| 3-8 | Krosan Grip | $1.51 | $40.70 |
| 3-9 | Skyclave Apparition | $0.29 | **$40.99** |

---

### Swap 3-1 · Herald of Secret Streams

- **IN:** `Herald of Secret Streams` — `{3}{U}` — Creature — Merfolk Warrior — 2/3 — **$8.81**
  > *"Creatures you control with +1/+1 counters on them can't be blocked."*
  > Official ruling (2017-09-29): *"Once a creature you control has become blocked, putting a +1/+1
  > counter on it won't cause it to become unblocked."*
- **OUT:** `Generous Patron` — `{2}{G}` — Creature — Elf Advisor. Its draw trigger reads *"Whenever you
  put one or more counters on a creature **you don't control**, draw a card."* You essentially never
  put counters on opponents' creatures, so half this card is dead text. It is the second-lowest
  EDHREC creature in your deck at **14.0%** — and at **$7.05** it is worth more traded away than
  played.
- **Why:** This is the answer to **wincon 0**. Your entire board has +1/+1 counters on it by design;
  this makes your entire board unblockable, permanently, from turn four onward. Every unblocked
  creature triggers Tidus's Cheer, `Sphere Grid` and `Bred for the Hunt`. `Rikku` does a smaller
  version of this one creature at a time — this does it for the team. EDHREC: 40.9%.
  Read the ruling: declare the counters **before** blockers, not after.
- **Bracket impact:** none.

### Swap 3-2 · Innkeeper's Talent (and the Farewell decision)

- **IN:** `Innkeeper's Talent` — `{1}{G}` — Enchantment — Class — **$7.99**
  > *"(Gain the next level as a sorcery to add its ability.)"*
  > *"At the beginning of combat on your turn, put a +1/+1 counter on target creature you control."*
  > *"{G}: Level 2 / Permanents you control with counters on them have ward {1}."*
  > *"{3}{G}: Level 3 / If you would put one or more counters on a permanent or player, put twice that
  > many of each of those kinds of counters on that permanent or player instead."*
- **OUT:** `Farewell` — `{4}{W}{W}` — Sorcery. *"Choose one or more — • Exile all artifacts. • Exile
  all creatures. • Exile all enchantments. • Exile all graveyards."* Six mana, and every relevant mode
  destroys **your** side too: your creatures with all their counters, and `Hardened Scales`,
  `Sphere Grid`, `Bred for the Hunt`, `Inexorable Tide`, `Sol Ring` and `Arcane Signet`.
- **Why:** A **Class** enchantment is one you can pay to level up over multiple turns. Level 1 is a
  second `Luminarch Aspirant` for two mana. Level 2 gives everything with counters **ward {1}** — a
  triggered ability that counters an opponent's spell or ability targeting it unless they pay the ward
  cost (CR 702.21). That is *taxing protection on every permanent you own*. Level 3 is a counter
  doubler. One card, three of your five priorities.
- **Bracket impact — this is the important one.** `./bin/mtg deck bracket tidus` currently returns
  **Bracket 3 — Upgraded** for exactly one reason: *"1 Game Changer(s) found: Farewell."* `Farewell` is
  on the 53-card Game Changers list in `data/brackets.json`. Bracket 1 and 2 both say "No Game
  Changers," Bracket 3 allows up to 3 — so this single card is what lifts the deck. **Cutting
  `Farewell` returns the deck to Bracket 2 — Core**, which is the honest home for a precon and the
  friendliest place for a new player to sit down. `Innkeeper's Talent` is **not** on the Game Changers
  list. If your regular table plays Bracket 3, keep `Farewell` and cut `Together Forever` for
  `Innkeeper's Talent` instead — your call, not mine.

### Swap 3-3 · Branching Evolution

- **IN:** `Branching Evolution` — `{2}{G}` — Enchantment — **$6.85**
  > *"If one or more +1/+1 counters would be put on a creature you control, twice that many +1/+1
  > counters are put on that creature instead."*
  > Official ruling (2020-06-23): *"If a creature you control would enter the battlefield with a number
  > of +1/+1 counters on it, it enters with twice that many instead."*
- **OUT:** `Together Forever` — `{W}{W}` — Enchantment. Support 2 on arrival, then *"{1}: Choose target
  creature with a counter on it. When that creature dies this turn, return that card to its owner's
  hand."* Returning a creature to **hand** loses every counter on it and costs you the mana to recast
  — it's damage control, not protection, and `Heroic Intervention`, `Ripples of Potential` and
  `Unbreakable Formation` all do the job better.
- **Why:** The strongest multiplier in your colours that isn't a $60 card. Remember the stacking
  ruling from swap 1-3: apply `Hardened Scales`, `Conclave Mentor`, `Kami of Whispered Hopes` and
  `Ozolith` **first**, then double. One counter becomes 5 → 10. EDHREC: 30.7%.
- **Bracket impact:** none.

### Swap 3-4 · Gavony Township

- **IN:** `Gavony Township` — Land — **$5.42**
  > *"{T}: Add {C}."* · *"{2}{G}{W}, {T}: Put a +1/+1 counter on each creature you control."*
- **OUT:** `Sungrass Prairie` — Land. Same flaw as `Skycloud Expanse`: its only ability is
  *"{1}, {T}: Add {G}{W}."* It cannot make a single mana on its own.
- **Why:** Land-for-land — count stays 37. This is a **mana sink that is also your entire game plan**:
  it puts a counter on every creature, which with your multipliers is a large pump, and which turns on
  `Rikku`'s unblockable trigger for the whole team at instant speed on an opponent's end step.
  EDHREC: 17.8%.
- **Bracket impact:** none.

### Swap 3-5 · Champion of Lambholt

- **IN:** `Champion of Lambholt` — `{1}{G}{G}` — Creature — Human Warrior — 1/1 — **$4.20**
  > *"Creatures with power less than this creature's power can't block creatures you control."*
  > *"Whenever another creature you control enters, put a +1/+1 counter on this creature."*
- **OUT:** `Summon: Ixion` — `{2}{W}` — Enchantment Creature — Saga Unicorn. Chapter I reads *"Exile
  target creature an opponent controls **until this Saga leaves the battlefield**"* — and the Saga
  sacrifices itself after chapter III. The exile is temporary **by design**; you hand the creature
  back two turns later. EDHREC: 44.7%.
- **Why:** A second team-wide evasion effect that grows itself. Between this, `Herald of Secret
  Streams`, `Rikku` and `Rogue's Passage`, the deck stops getting walled by a wide board — which is
  the failure mode of every counters deck.
- **Bracket impact:** none.

### Swap 3-6 · Kutzil, Malamet Exemplar

- **IN:** `Kutzil, Malamet Exemplar` — `{1}{G}{W}` — Legendary Creature — Cat Warrior — 3/3 — **$3.93**
  > *"Your opponents can't cast spells during your turn."*
  > *"Whenever one or more creatures you control each with power greater than its base power deals
  > combat damage to a player, draw a card."*
- **OUT:** `Tireless Tracker` — `{2}{G}` — Creature — Human Scout. This is a **good card** and cutting
  it is the closest call in the document. It's here because it is the least *synergistic* good card
  left: its Clues cost {2} each to cash, and the counters only ever land on Tracker itself.
  EDHREC: 16.5% in Tidus decks.
- **Why:** Two effects the deck badly wants. *"Your opponents can't cast spells during your turn"*
  means your alpha strike cannot be broken up by an instant-speed removal spell or a board wipe — it is
  protection that costs no mana. And the draw trigger is free with `Hardened Scales` on board, since
  any creature with a +1/+1 counter has power greater than its base power. EDHREC: 37.6%.
- **Bracket impact:** none. (`Drannith Magistrate` and `Grand Arbiter Augustin IV` are the Game
  Changers in this space; `Kutzil` is not on the list.)

### Swap 3-7 · Swiftfoot Boots

- **IN:** `Swiftfoot Boots` — `{2}` — Artifact — Equipment — **$1.99**
  > *"Equipped creature has hexproof and haste."*
  > *"Equip {1}"*
- **OUT:** `Everflowing Chalice` — `{0}` — Artifact. Multikicker ramp: you pay {2} per charge counter,
  then tap it for that much colourless. Paying 2 to make 1 is the worst rate of any ramp in the deck,
  and it makes **colourless** mana in a three-colour deck.
- **Why:** Tidus costs `{G}{W}{U}` and every single one of his triggers requires him to be on the
  battlefield. Hexproof (CR 702.11b) means opponents can't target him at all. Note the free option:
  `bumbleflower` **and** `dogmeat` each already run a copy (count 1 each) — if you'd rather not
  spend, move one and this swap is Tier 0 instead, dropping Tier 3 to **$39.00**. Because there are
  two copies out there, this is the one "already owned" card with no contention at all.
- **Bracket impact:** none.

### Swap 3-8 · Krosan Grip

- **IN:** `Krosan Grip` — `{2}{G}` — Instant — **$1.51**
  > *"Split second (As long as this spell is on the stack, players can't cast spells or activate
  > abilities that aren't mana abilities.)"*
  > *"Destroy target artifact or enchantment."*
- **OUT:** `Bane of Progress` — `{4}{G}{G}` — Creature — Elemental. *"When this creature enters,
  destroy all artifacts and enchantments."* Count what you'd be destroying on your own side:
  `Hardened Scales`, `Sphere Grid`, `Bred for the Hunt`, `Inexorable Tide`, `Sol Ring`,
  `Arcane Signet`, plus (after these upgrades) `Ozolith`, `Branching Evolution`, `Innkeeper's Talent`
  and `Simic Ascendancy`. It is a six-mana card that reads "destroy your own deck." EDHREC: 32.1%.
- **Why:** Surgical instead of nuclear, at instant speed, and **split second** (CR 702.61a) means the
  opponent cannot respond by sacrificing the target or countering the Grip. This is the clean answer
  Problem 3 asked for, and swapping a six-drop for a three-drop drops your MV-5-and-up count to 3.
- **Bracket impact:** none.

### Swap 3-9 · Skyclave Apparition

- **IN:** `Skyclave Apparition` — `{1}{W}{W}` — Creature — Kor Spirit — 2/2 — **$0.29**
  > *"When this creature enters, exile up to one target nonland, nontoken permanent you don't control
  > with mana value 4 or less."*
  > *"When this creature leaves the battlefield, the exiled card's owner creates an X/X blue Illusion
  > creature token, where X is the mana value of the exiled card."*
- **OUT:** `Gatta and Luzzu` — `{2}{W}` — Legendary Creature. A one-shot damage-prevention-into-counters
  trigger on arrival. It's cute, but it's a single defensive trigger with no ongoing effect, and
  you now have three dedicated protection instants that do it better.
- **Why:** Removal on a body, and it hits the permanent types you're thin on — an opposing mana rock,
  an `Aura`, a two-drop that's causing problems. The Illusion drawback only happens if the Apparition
  leaves the battlefield, and if it does, that Illusion has no counters on it and dies to your
  `Damning Verdict`. Removal ends the path at **11** — up from 8 — and **every one** of the 11 is
  either an instant or attached to a creature that does something else, with **6** at instant speed.
  (This swap also drops interaction back from 6 to 5 by cutting `Gatta and Luzzu`; that's the right
  trade, because a one-shot prevention trigger is not protection.)
- **Bracket impact:** none.

**Tier 3 running total: $40.99.** Under the $50 cap, with $9.01 unspent.
**Cumulative spend across Tiers 1+2+3: $62.77** — for a full 31-card overhaul.

---

## 7 · Do NOT buy these yet

These are all real, popular, powerful cards. EDHREC will happily show them to you. They are still
the wrong purchase for a first Commander deck at Bracket 2, and here is the kind version of why.

### Because they change what bracket you're allowed to play

`data/brackets.json` holds the official 53-card **Game Changers** list. Bracket 1 and Bracket 2 both
say **"No Game Changers."** Every card below is on it. Buying any one of them moves your deck out of
the pod you're most likely sitting in.

| Card | Price | Why not yet |
|---|---|---|
| `Rhystic Study` | **$69.85** | *"Whenever an opponent casts a spell, you may draw a card unless that player pays {1}."* Great card, but it makes every opponent do arithmetic on every spell all game. It is the classic "new player accidentally becomes the archenemy" purchase. |
| `Smothering Tithe` | **$63.65** | Same social problem, plus it costs more than this entire upgrade path. |
| `Fierce Guardianship` | **$56.48** | A free counterspell — it's genuinely strong, but *"Counter target noncreature spell"* doesn't protect you from the creature-based decks you'll actually face. |
| `Teferi's Protection` | **$52.60** | `Heroic Intervention` (free, Tier 0), `Ripples of Potential` ($2.94) and `Unbreakable Formation` ($1.18) cover 90% of this for 2% of the price. |
| `Cyclonic Rift` | **$40.76** | The overload mode bounces every nonland permanent your opponents control. It ends games out of nowhere and is the least fun way to lose. |
| `Enlightened Tutor` | **$38.71** | A tutor is worth more the more broken your best card is. Your best card is `Damning Verdict`. |
| `Worldly Tutor` | **$27.13** | Same reasoning. Spend $27 on *eight* new creatures instead. |

### Because there is a cheap version that does nearly the same thing

| Card | Price | Buy this instead |
|---|---|---|
| `The Ozolith` | **$65.37** | `Ozolith, the Shattered Spire` — **$5.20** (Tier 2). The $65 one banks counters from dying creatures; the $5 one multiplies counters every turn, which is what your deck actually does. |
| `The Great Henge` | **$63.41** | `Innkeeper's Talent` — **$7.99** (Tier 3). |
| `Bristly Bill, Spine Sower` | **$42.23** | `Evolution Sage` — **$2.25** (Tier 2) triggers on the same landfall condition. |
| `Sword of Truth and Justice` | **$35.89** | `Swiftfoot Boots` — **$1.99**, or free from another deck. |
| `Agatha's Soul Cauldron` | **$37.94** | Nothing — this card is a puzzle box for experienced players and does very little in a straightforward counters deck. |
| `Esper Sentinel` | **$57.50** | You have 12 draw pieces. You don't need a 13th at $57. |
| `Kodama of the West Tree` | **$22.73** | `Sphere Grid` (already in your deck) gives trample to the same creatures for free. |
| `Ouroboroid` | **$31.38** | `Kalonian Hydra` — free from `bumbleflower`, or $6.37. |
| `Anointed Procession` | **$57.52** | Wrong deck entirely — you make almost no tokens. |
| `Boseiju, Who Endures` | **$49.35** | `Krosan Grip` — **$1.51** (Tier 3). |
| `Danny Pink` | **$16.30** | `Bred for the Hunt` (already in your deck) does the same job. |

### Because you already own it

- **`Heroic Intervention` — $16.17.** It's in `dogmeat`. Move it (swap 0-2) before you buy one. If you
  decide `dogmeat` can't spare it, then and only then is $16.17 a fair price.
- **`Rogue's Passage` — $0.38.** It's in `dogmeat` too, and being a colourless land it is legal in
  every deck you own. Move it and swap **1-6** becomes free (Tier 1 drops to $3.39). Note that
  `decks/bumbleflower/UPGRADES.md` swap **T0-6** wants the same copy — at $0.38 a second copy is
  the cheapest purchase in this whole document, so this is the one contested card not worth
  agonising over.
- **`Swiftfoot Boots` — $1.99.** Both `bumbleflower` **and** `dogmeat` run a copy (see swap 3-7).
  Move one and swap 3-7 becomes free, dropping Tier 3 to $39.00.

### The mana base — the trap everyone falls into

EDHREC will show you `Breeding Pool`, `Temple Garden` and `Hallowed Fountain` in 37–40% of Tidus
decks. **Their price is not in my data** — the local database has no `price_usd` for any of the three.
What I can tell you from the card text is what they do: *"As this land enters, you may pay 2 life. If
you don't, it enters tapped."* That is worth real money to a tournament player and almost nothing to
you: it saves you roughly one turn of tempo, occasionally.

`Spara's Headquarters` — **$13.64** — is the same story: *"This land enters tapped."* You are paying
$13.64 for a land that enters tapped exactly like the eight you already have. **The correct mana-base
fix at your budget is free**: cut the three lands that cannot produce mana on their own
(`Skycloud Expanse`, `Sungrass Prairie`, `Overflowing Basin`) for lands that do something —
which is exactly what swaps 1-6, 2-4 and 3-4 do. `Overflowing Basin` is the next one on the chopping
block if you ever add a fourth utility land.

---

## 8 · Bracket, honestly

Straight from `./bin/mtg deck bracket tidus`:

```
ESTIMATED BRACKET 3 — Upgraded
  Game Changers        : 1 (checked against 53 listed cards)
      • Farewell
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review
```

**Read that carefully: the deck is at Bracket 3 because of one card.** Out of the box it plays like a
Bracket 2 deck in every other respect — the tool found no mass land denial and no extra turns.

**Every single one of the 31 cards recommended in this document was checked against the 53-card Game
Changers list in `data/brackets.json`. None of them is on it.** So the entire path — all four tiers —
adds **zero** Game Changers.

That gives you two clean endpoints:

- **Take swap 3-2 (cut `Farewell`)** → 0 Game Changers → **Bracket 2 — Core.** The rules text `data/brackets.json`
  carries for that bracket ends *"…games typically end around turn 9 or later."* This is where a new
  player should be.
  The deck will be much stronger than it is today and still legal at any Bracket 2 table.
- **Keep `Farewell`** → 1 Game Changer → **Bracket 3 — Upgraded.** Bracket 3 allows up to 3, so you
  have room. Choose this if your regular pod is already playing tuned decks.

One caveat the tool states about itself and I'll repeat: it does not detect two-card infinite combos.
I checked the additions by hand and none of them loop. `Ezuri` + `Inexorable Tide` draws you a card
per spell, and `Tekuthal` doubles proliferates — those are strong, not infinite. `Simic Ascendancy`
is an alternate win condition, which is permitted at every bracket; it is not a combo.

---

## 9 · Running totals & the full swap ledger

| Tier | Swaps | Spend | Cumulative |
|---|---|---|---|
| Tier 0 — Free | 7 | **$0.00** | $0.00 |
| Tier 1 — Under $5 | 8 | **$3.77** | $3.77 |
| Tier 2 — Under $20 | 7 | **$18.01** | $21.78 |
| Tier 3 — Under $50 | 9 | **$40.99** | **$62.77** |
| **Total** | **31** | | |

**The deck stays at exactly 100 cards at every stage.** Each tier swaps the same number of cards in as
out, and lands are only ever swapped for lands (`Temple of the False God` → `Rogue's Passage`,
`Skycloud Expanse` → `Karn's Bastion`, `Sungrass Prairie` → `Gavony Township`), so the land count
holds at **37** and the stats tool's *"land count: SANE"* verdict survives the whole path.

### What the numbers look like at the end

| Measure | Before | After all four tiers | The maths |
|---|---|---|---|
| Interaction (the tool's own count: counterspells + protection) | 3 | **5** | keep `An Offer You Can't Refuse` + `Inspiring Call`; cut `Gatta and Luzzu`; add `Heroic Intervention`, `Ripples of Potential`, `Unbreakable Formation` |
| Instant-speed answers to a permanent or spell | 4 | **8** | keep `Path to Exile`, `An Offer You Can't Refuse`, `Endless Detour`; cut `Destroy Evil`; add `Swords to Plowshares`, `Generous Gift`, `Beast Within`, `Return to Nature`, `Krosan Grip` |
| Removal (the tool's role count) | 8 | **11** | |
| Counter multipliers | 1 (`Hardened Scales`) | **5** | + `Conclave Mentor`, `Ozolith, the Shattered Spire`, `Kami of Whispered Hopes`, `Branching Evolution` (a conditional 6th at `Innkeeper's Talent` level 3) |
| Stated win conditions | 0 | **2** | `Simic Ascendancy`, `Herald of Secret Streams` |
| Cards at mana value 5 or more | 9 | **3** | cut 7 of the 9; only `Kalonian Hydra` added back — leaving `Damning Verdict`, `Inexorable Tide`, `Kalonian Hydra` |
| Lands | 37 | **37** | 3 lands in, 3 lands out |
| Game Changers | 1 (`Farewell`) | **0** | if you take swap 3-2 |

### Ledger — every card leaving, and when

| Tier | OUT | EDHREC play rate in Tidus decks |
|---|---|---|
| 0 | Yuna's Whistle | 31.3% |
| 0 | Summoner's Sending | 25.7% |
| 0 | Scholar of New Horizons | 37.5% |
| 0 | Path of Discovery | 19.6% |
| 0 | Destroy Evil | 38.1% |
| 0 | Sunscorch Regent | 29.3% |
| 0 | Altered Ego | 18.8% |
| 1 | Lord Jyscal Guado | 17.9% |
| 1 | Summon: Valefor | 37.2% |
| 1 | Summon: Magus Sisters | 29.2% |
| 1 | Chasm Skulker | 33.6% |
| 1 | Yuna's Decision | 32.4% |
| 1 | Temple of the False God *(land)* | 32.6% |
| 1 | Rampant Rejuvenator | 27.8% |
| 1 | Promise of Loyalty | 33.9% |
| 2 | Blitzball Stadium | 58.2% |
| 2 | Sin, Unending Cataclysm | 41.1% |
| 2 | Skycloud Expanse *(land)* | not on EDHREC's Tidus lists |
| 2 | Fight Rigging | 35.8% |
| 2 | Pull from Tomorrow | 20.3% |
| 2 | O'aka, Traveling Merchant | 54.9% |
| 2 | Collective Effort | 48.2% |
| 3 | Generous Patron | 14.0% |
| 3 | Farewell *(Game Changer)* | 60.3% |
| 3 | Together Forever | 53.6% |
| 3 | Sungrass Prairie *(land)* | not on EDHREC's Tidus lists |
| 3 | Summon: Ixion | 44.7% |
| 3 | Tireless Tracker | 16.5% |
| 3 | Everflowing Chalice | 61.7% |
| 3 | Bane of Progress | 32.1% |
| 3 | Gatta and Luzzu | 60.1% |

**One honest caveat about those percentages.** EDHREC's Tidus page is built from 19,181 decks, and
most of them **are** this precon with a few cards changed. So a precon card showing 58% or 61% partly
means "most people never cut it," not "most people chose it." Use the percentage as a tiebreaker,
never as the whole argument — the reason written next to each swap above is the real argument.

---

## 10 · Verbatim CLI receipts

Everything above is checkable. Here is the unedited output for four of the recommendations, prices
included, so you can see the source. Run any of these yourself.

**`./bin/mtg card "Swords to Plowshares"`**
```
── Swords to Plowshares ──────────────────────────────────────────────────
Mana cost      : {W}
Mana value     : 1
Type           : Instant

Exile target creature. Its controller gains life equal to its power.

Color identity : W (white)
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #11
Price (USD)    : $1.30

── Rulings (1) ───────────────────────────────────────────────────────────
[2022-12-08] (wotc)
  Use the power of the creature from when it was last on the battlefield
  to determine how much life is gained.
```

**`./bin/mtg card "Rishkar, Peema Renegade"`**
```
── Rishkar, Peema Renegade ───────────────────────────────────────────────
Mana cost      : {2}{G}
Mana value     : 3
Type           : Legendary Creature — Elf Druid

When Rishkar enters, put a +1/+1 counter on each of up to two target
creatures.
Each creature you control with a counter on it has "{T}: Add {G}."

P/T            : 2/2

Color identity : G (green)
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #834
Price (USD)    : $0.18

── Rulings (3) ───────────────────────────────────────────────────────────
[2017-02-09] (wotc)
  Each creature you control has Rishkar's mana ability as long as that
  creature has any kind of counter on it. The effect isn't limited to
  those with +1/+1 counters.
```

**`./bin/mtg card "Ozolith, the Shattered Spire"`**
```
── Ozolith, the Shattered Spire ──────────────────────────────────────────
Mana cost      : {1}{G}
Mana value     : 2
Type           : Legendary Artifact

If one or more +1/+1 counters would be put on an artifact or creature you
control, that many plus one +1/+1 counters are put on it instead.
{1}{G}, {T}: Put a +1/+1 counter on target artifact or creature you control.
Activate only as a sorcery.
Cycling {2} ({2}, Discard this card: Draw a card.)

Color identity : G (green)
Keywords       : Cycling
Rarity         : rare
Commander      : legal
EDHREC rank    : #637
Price (USD)    : $5.20

── Rulings (4) ───────────────────────────────────────────────────────────
[2023-04-14] (wotc)
  If another artifact or creature you control would enter the battlefield
  with a number of +1/+1 counters on it, it enters with that many plus one
  instead.
[2023-04-14] (wotc)
  If two or more effects attempt to modify how many counters would be put
  onto a permanent you control, you choose the order to apply those
  effects, no matter who controls the sources of those effects.
```

**`./bin/mtg card "Herald of Secret Streams"`**
```
── Herald of Secret Streams ──────────────────────────────────────────────
Mana cost      : {3}{U}
Mana value     : 4
Type           : Creature — Merfolk Warrior

Creatures you control with +1/+1 counters on them can't be blocked.

P/T            : 2/3

Color identity : U (blue)
Rarity         : rare
Commander      : legal
EDHREC rank    : #1053
Price (USD)    : $8.81

── Rulings (1) ───────────────────────────────────────────────────────────
[2017-09-29] (wotc)
  Once a creature you control has become blocked, putting a +1/+1 counter
  on it won't cause it to become unblocked.
```

### Rules and terms used in this document

| Term | Where to look it up |
|---|---|
| counter (the marker) | `./bin/mtg rule 122.1` |
| +1/+1 counter | `./bin/mtg rule 122.1` → subrule 122.1a |
| proliferate | `./bin/mtg glossary proliferate` · `./bin/mtg rule 701.34` |
| hexproof | `./bin/mtg glossary hexproof` · `./bin/mtg rule 702.11` |
| indestructible | `./bin/mtg glossary indestructible` · `./bin/mtg rule 702.12` |
| trample | `./bin/mtg glossary trample` · `./bin/mtg rule 702.19` |
| ward | `./bin/mtg glossary ward` · `./bin/mtg rule 702.21` |
| split second | `./bin/mtg rule 702.61` |
| mana value | `./bin/mtg glossary "mana value"` · `./bin/mtg rule 202.3` |
| instant timing | `./bin/mtg rule 117.1` → subrule 117.1a |
| colour identity | `./bin/mtg glossary "color identity"` · `./bin/mtg rule 903.4` |
| Commander deck rules | `./bin/mtg rule 903.5` |

---

## 11 · A closing note

**None of this is required.** `Counter Blitz` is a finished, playable, genuinely good Commander deck
exactly as it came out of the box. It has a real engine — Tidus moving counters, `Rikku` turning those
counters into unblockable attackers, `Sphere Grid` paying you for connecting, `Damning Verdict`
sweeping a board that your creatures walk away from. Plenty of people play this precon unchanged for
a year and win games with it.

The best first move is not a purchase. It is **playing ten games and noticing what actually goes
wrong.** If you keep losing your board to a wipe, section 3 swap 0-2 is your card. If you keep getting
chump-blocked forever, it's swap 3-1. If you keep drawing five-drops on turn three, it's Tier 1. The
list above is ordered by what the numbers say is weakest — but your own games are better evidence than
any EDHREC percentage.

And when you do upgrade, go **one tier at a time and play between tiers.** Changing 31 cards at once
means you learn nothing about which change helped. Changing seven means you find out.

Finally: **Tier 0 is not free.** Every card you move out of `bumbleflower` or `dogmeat` makes that deck
worse, and having three decks that are all fun to play is worth more than having one deck that is 15%
stronger. If you only ever do Tier 1 — eight cards, $3.77 — you will have fixed the two real problems
in this deck for less than the price of a coffee, and all three of your decks will still be intact.
