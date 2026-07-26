# MERGED BANT — one deck out of two boxes

**Commander (EDH) only.** 100 cards, singleton (one copy of everything except basic lands),
no sideboard — Commander does not have one.

| | |
|---|---|
| **Commander** | Tidus, Yuna's Guardian |
| **Colors** | Bant — green / white / blue (`WUG`) |
| **Built from** | `tidus` (Counter Blitz) + `bumbleflower` (Peace Offering) |
| **Cards you must buy** | **zero** — every card is already in one of your two boxes |
| **Estimated bracket** | **2 — Core**, playing at the top of that band (see §9) |
| **New deck folder** | `decks/merged-bant/` · clean list in `DECKLIST.md` |

> Every mana cost, type line, power/toughness, and rules quote below was pulled from the local
> card database in this session. Re-check anything yourself with `./bin/mtg card "<name>"`.
> Rules citations are Comprehensive Rules numbers pulled with `./bin/mtg rule <number>`.
> The full verification output is pasted at the bottom (§11). Nothing here is from memory.

---

## Jargon key (read this first if you are new)

Each of these is also defined again where it matters. Anything marked ⌕ has an official
entry — `./bin/mtg glossary <term>`. **Pip** and **pillowfort** are player slang with no official
entry at all, which is exactly why they are spelled out in full below.

- **Mana value** ⌕ — the total amount of mana in a cost, ignoring color. `{2}{G}` has mana value 3.
  Written "MV" below.
- **Pip** — one coloured mana symbol inside a cost. `{3}{W}{W}` has **two** white pips and mana
  value 5; `{G}{W}{U}` has one pip of each colour. Counting every pip in the deck is how you work
  out how many *sources* of each colour you need — that is the whole argument in §3. (Slang: the
  rules only ever say "mana symbol", CR **107.4a**.)
- **+1/+1 counter** — a permanent marker that makes a creature 1 bigger in power and toughness for
  as long as it stays on (CR **122.1a**: *"A +X/+Y counter on a creature … adds X to that object's
  power and Y to that object's toughness."*).
- **Counter (the noun) vs. counter (the verb)** — a *counter* is the marker above. To *counter a
  spell* is to stop it resolving. This deck cares about the marker almost all the time.
- **Ramp** — anything that gives you extra mana. A **mana rock** is an artifact that taps for mana.
- **Trigger / triggered ability** ⌕ — an ability starting "Whenever…", "When…", or "At the beginning
  of…". It happens on its own; you do not choose to activate it.
- **The stack** ⌕ — the queue spells and triggers sit in before they take effect. The last thing added
  resolves first.
- **Proliferate** ⌕ — CR **701.34a**: *"To proliferate means to choose any number of permanents
  and/or players that have a counter, then give each one additional counter of each kind that
  permanent or player already has."* You are never forced to pick an opponent's stuff.
- **Scry N** ⌕ — CR **701.22a**: *"To 'scry N' means to look at the top N cards of your library, then
  put any number of them on the bottom of your library in any order and the rest on top of your
  library in any order."* It does **not** draw you a card — it improves the card you draw next. Three
  of this deck's lands (the Temples, §2) have scry 1 as their whole upside.
- **Investigate** ⌕ — CR **701.16a**: *"'Investigate' means 'Create a Clue token.'"* A **Clue token**
  is *"a colorless Clue artifact token with '{2}, Sacrifice this token: Draw a card.'"* (CR
  **111.10f**). So an investigate trigger is not a card now — it is a card you buy later for `{2}`,
  and it sits on the battlefield as an artifact until you do.
- **Hideaway N** ⌕ — CR **702.75a**: *"When this permanent enters, look at the top N cards of your
  library. Exile one of them face down and put the rest on the bottom of your library in a random
  order."* A condition printed on the same card then lets you play the exiled card, usually for free.
- **Trample** ⌕ — excess combat damage past the blockers hits the defending player (CR **702.19b**).
- **Double strike** ⌕ — the creature deals its combat damage **twice**, in two separate damage steps
  (CR **702.4b**).
- **Indestructible** ⌕ — CR **702.12b**: *"A permanent with indestructible can't be destroyed. Such
  permanents aren't destroyed by lethal damage…"* It does **not** stop exile or sacrifice.
- **Vigilance** ⌕ — attacking doesn't tap the creature, so it can attack and still block later.
- **Board wipe** — a spell that destroys or exiles most creatures at once.
- **Pillowfort** — cards that make it expensive or pointless to attack *you*, steering the table at
  somebody else. In the final 100 that is `Baird, Steward of Argive` and `Summon: Yojimbo`; the
  alternate Bumbleflower build in §1 is mostly built out of them.
- **Commander tax** — CR **903.8**: a commander cast from the command zone *"costs an additional
  {2} for each previous time the player casting it has cast it from the command zone that game."*
- **Singleton** — you may only run one copy of each card. **Basic lands are the exception** — you can
  run as many Forests, Plains and Islands as you like.

---

## 1. Which commander, and why

Both of your Bant boxes are legal to lead this deck. They are not close.

### The two cards, exactly as printed

```
Tidus, Yuna's Guardian — {G}{W}{U} — Legendary Creature — Human Warrior — 3/3

At the beginning of combat on your turn, you may move a counter from target
creature you control onto a second target creature you control.
Cheer — Whenever one or more creatures you control with counters on them
deal combat damage to a player, you may draw a card and proliferate. Do this
only once each turn.
```

```
Ms. Bumbleflower — {1}{G}{W}{U} — Legendary Creature — Rabbit Citizen — 1/5

Vigilance
Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter
on target creature. It gains flying until end of turn. If this is the second
time this ability has resolved this turn, you draw two cards.
```

### The decision: **Tidus, Yuna's Guardian.**

Here is the reasoning, from the actual contents of the merged pool rather than from either
deck's name.

**The pool is overwhelmingly a +1/+1-counter pool, and it is that way from *both* boxes.**
People assume the counters live in the FINAL FANTASY box and the "group hug" lives in the
Peace Offering box. That is not what the card list says. The Peace Offering box independently
contributes `Kalonian Hydra` ({3}{G}{G}, enters with four +1/+1 counters, *"Whenever this creature
attacks, double the number of +1/+1 counters on each creature you control"*), `Simic Ascendancy`
({G}{U}, *"Whenever one or more +1/+1 counters are put on a creature you control, put that many
growth counters on this enchantment"* → win at twenty), `Managorger Hydra` ({2}{G}, a counter off
every spell any player casts), `Rishkar, Peema Renegade` ({2}{G}), `Steelburr Champion` ({2}{W}),
`Chasm Skulker` ({2}{U}) and `Sunscorch Regent` ({3}{W}{W}). Every one of those is a Tidus card.
Merging the boxes does not blend two strategies — it **deepens one strategy**.

**Tidus is the payoff for what the pool already does; Bumbleflower is a payoff for something the
pool mostly doesn't do.** Bumbleflower rewards *casting lots of cheap spells and having a huge
hand*. The cards that convert that into a win — `Psychosis Crawler` ({5}, power and toughness equal
to your hand size, *"Whenever you draw a card, each opponent loses 1 life"*), `Body of Knowledge`
({3}{U}{U}), `Twenty-Toed Toad` ({3}{U}), `Triskaidekaphile` ({1}{U}), `Kwain, Itinerant Meddler`
({W}{U}), `Secret Rendezvous` ({1}{W}{W}) — are **all in one box only**, all in blue and white, and
there are about a dozen of them. The counter package is roughly forty cards across both boxes. You
build toward your deepest resource, not your shallowest.

**Tidus costs three mana; Bumbleflower costs four, and this deck's mana is genuinely three-colored.**
`{G}{W}{U}` on turn 3 is hard enough. `{1}{G}{W}{U}` on turn 4 is harder, and it is the single most
demanding cast in either box.

**Bumbleflower's drawback fights the merged plan directly.** Her trigger is *mandatory* and says
*"target opponent draws a card"* on **every spell you cast** — no "may." A merged Bant counters deck
is the aggressor at the table: it builds a visible, growing board and asks the other three players
to answer it. Handing those three players roughly two extra cards per turn cycle is literally
funding the removal that answers you. In her own box she pays for that with `Baird, Steward of
Argive`, `Mangara, the Diplomat`, `Spore Frog`, `Riot Control`, `Illusionist's Gambit` and
`Perch Protection` — a defensive shell that makes the table's fresh cards point elsewhere. This
merged deck keeps only one of those (`Baird`). Without the shell, the drawback is just a drawback.

**The community data agrees, for whatever that is worth.** `mtg edhrec "Tidus, Yuna's Guardian"`
reports 19,181 decks, and eight of my picks appear in more than 70% of them — `Hardened Scales`
89.1%, `Sphere Grid` 88.7%, `Damning Verdict` 85.8%, `Yuna, Grand Summoner` 85.2%,
`Rikku, Resourceful Guardian` 83.2%, `Wakka, Devoted Guardian` 80.5%, `Gyre Sage` 78.8%,
`Incubation Druid` 79.6%. That is not proof, but it does mean the shape I'm handing you is the
shape thousands of people converged on.

### The alternate build: Ms. Bumbleflower

If you ever want it, it is a genuinely different deck, not a reskin. You would keep the ramp and
the fixing, keep `Forgotten Ancient` / `Managorger Hydra` / `Sunscorch Regent` (they grow off the
*whole table's* spells, so the extra cards you hand out actually feed them), and then swap the
entire attack package — `Chocobo Knights`, `Wakka`, `Auron`, `Kalonian Hydra`, `Sin`,
`Damning Verdict` — for the hand-size payoffs and the **pillowfort** (cards that tax or block
attacks *on you* so the table swings at someone else — jargon key): `Psychosis Crawler`,
`Body of Knowledge`, `Twenty-Toed Toad`, `Triskaidekaphile`, `Baird`, `Mangara, the Diplomat`,
`Spore Frog`, `Riot Control`, `Illusionist's Gambit`, `Perplexing Test`, `Tamiyo, Field
Researcher`. You would go up to about 38 lands and 25+ draw pieces, drop the average mana value
work entirely, and win at turn 10-13 by flying over a stalled board or by hitting an alternate
win condition. It is slower, safer, more political, and much more bookkeeping per turn. It is a
fine deck. It is not the deck this card pool wants to be.

---

## 2. The final 100

**99 + commander. Programmatic count is in §11 — it says 100.**

Format below: `Name` — cost — one-line reason. All costs and text verified this session.

### Commander (1)

| Card | Cost | Why |
|---|---|---|
| **Tidus, Yuna's Guardian** | `{G}{W}{U}` | 3/3. Free counter-move every combat, and *"Cheer — Whenever one or more creatures you control with counters on them deal combat damage to a player, you may draw a card and proliferate."* Turns the deck's forty counter cards into card advantage. |

**Two things a new player must internalise about him.** First, his move ability says *"a counter"*,
not "a +1/+1 counter" — shield counters, flying counters and lore counters all move. Second, the
official ruling (2025-06-06) says *"To move a counter from one permanent to another, the counter is
removed from the first permanent and put on the second. Any abilities that care about a counter
being removed from or put onto a permanent will apply."* That is why `Rikku` and `Wakka` below are
so strong — a *move* counts as *putting* a counter on the destination.

### Ramp — 12 cards

Mana acceleration and colour fixing. Twelve is high on purpose: this is a three-colour deck and
the merged pool gave us far better rocks than either box had alone.

| Card | Cost | Why it's in |
|---|---|---|
| Sol Ring | `{1}` | *"{T}: Add {C}{C}."* Two mana off a one-mana artifact. Best turn-1 play in either box. |
| Arcane Signet | `{2}` | *"{T}: Add one mana of any color in your commander's color identity."* Perfect three-colour fixing. |
| Fellwar Stone | `{2}` | *"{T}: Add one mana of any color that a land an opponent controls could produce."* In a four-player pod this is nearly always a colour you want. |
| Mind Stone | `{2}` | Ramp early; *"{1}, {T}, Sacrifice this artifact: Draw a card"* late. Never a dead draw. |
| Farseek | `{1}{G}` | *"Search your library for a Plains, Island, Swamp, or Mountain card…"* — in **this** mana base that legally includes `Canopy Vista` and `Prairie Stream`, because those cards have the land types Forest Plains / Plains Island. |
| Three Visits | `{1}{G}` | *"Search your library for a Forest card, put it onto the battlefield, then shuffle."* No "tapped" — this one comes in untapped. |
| Cultivate | `{2}{G}` | Two basics: one onto the battlefield tapped, one to hand. Fixes colour and guarantees next turn's land drop. |
| Gyre Sage | `{1}{G}` | 1/2 with Evolve. *"{T}: Add {G} for each +1/+1 counter on this creature."* Ramp that scales with the entire deck theme. |
| Incubation Druid | `{1}{G}` | 0/2. Taps for one mana of any type a land you control could produce — **three** if it has a +1/+1 counter on it. |
| Rishkar, Peema Renegade | `{2}{G}` | 2/2, two counters on entry, and *"Each creature you control with a counter on it has '{T}: Add {G}.'"* Ruling (2017-02-09): *"The effect isn't limited to those with +1/+1 counters"* — shield and lore counters turn creatures into mana too. |
| Faeburrow Elder | `{1}{G}{W}` | 0/0 vigilance, +1/+1 per colour among your permanents. Official ruling: *"usually gives it at least +2/+2 and its last ability usually produces at least {G}{W}."* With a blue permanent out, a 3/3 tapping for `{G}{W}{U}`. |
| Yuna, Grand Summoner | `{1}{G}{W}{U}` | 1/5. Taps for any colour **and** makes your next creature spell that turn enter with two extra +1/+1 counters. Also recovers counters from anything of yours that dies. |

### Draw — 8 cards

| Card | Cost | Why it's in |
|---|---|---|
| Bred for the Hunt | `{1}{G}{U}` | *"Whenever a creature you control with a +1/+1 counter on it deals combat damage to a player, you may draw a card."* Unlike Cheer, this triggers **per creature** — the reason you attack wide. |
| Fathom Mage | `{2}{G}{U}` | 1/1 Evolve. *"Whenever a +1/+1 counter is put on this creature, you may draw a card."* With `Hardened Scales` out, every counter effect on it draws extra. |
| Inspiring Call | `{2}{G}` | Instant. *"Draw a card for each creature you control with a +1/+1 counter on it. Those creatures gain indestructible until end of turn."* Note the wording: specifically **+1/+1** counters — a creature carrying only a shield or lore counter draws you nothing and is not protected. Your single best card: refuel plus board-wipe insurance in one. |
| Tireless Tracker | `{2}{G}` | 3/2. Investigate on every land you play — a **Clue** token, i.e. an artifact reading *"{2}, Sacrifice this token: Draw a card"*; when you pay that `{2}` and sacrifice it, Tracker also gets a +1/+1 counter. |
| Chasm Skulker | `{2}{U}` | 1/1. *"Whenever you draw a card, put a +1/+1 counter on this creature."* When it dies it leaves X 1/1 Squids. |
| Lord Jyscal Guado | `{1}{W}` | 2/1 flier. *"At the beginning of each end step, if you put a counter on a creature this turn, investigate."* Investigate = make a Clue (`{2}`, sacrifice it, draw a card). In this deck that condition is met almost every turn — including opponents' turns. Ruling (2025-06-06): the check happens **when the end step begins**, so putting a counter on afterwards is too late. |
| Pull from Tomorrow | `{X}{U}{U}` | Instant. *"Draw X cards, then discard a card."* Your reset button when the board stalls. |
| Blitzball Stadium | `{X}{U}` | Support X on entry (a counter on each of up to X creatures), then *"{3}, {T}"* makes one creature unblockable **and** gives it *"Whenever this creature deals combat damage to a player, draw a card for each kind of counter on it."* The cards arrive when it connects, not when you activate. |

### Removal & interaction — 11 cards

The old Tidus list had **8 removal / 3 interaction** and the old Bumbleflower list had
**4 removal / 6 interaction** (`mtg deck stats`, both run this session). This is the single biggest
upgrade the merge buys — see §5.

| Card | Cost | Why it's in |
|---|---|---|
| Swords to Plowshares | `{W}` | *"Exile target creature. Its controller gains life equal to its power."* One mana, exiles anything, no conditions. The most efficient removal in either box. |
| Path to Exile | `{W}` | The second copy of that effect. Exile beats destroy — it gets past indestructible and regeneration. |
| An Offer You Can't Refuse | `{U}` | *"Counter target **noncreature** spell."* Your one-mana answer to an opposing board wipe or combo piece. |
| Destroy Evil | `{1}{W}` | Modal instant: a creature with toughness 4+, **or** an enchantment. |
| Generous Gift | `{2}{W}` | *"Destroy target permanent."* The only card here that can answer a problem land, artifact, planeswalker or enchantment at instant speed. They get a 3/3 Elephant — pay it. |
| Broken Wings | `{2}{G}` | Instant. Artifact, enchantment, **or** creature with flying — green's answer to the things green can't normally touch. |
| Endless Detour | `{G}{W}{U}` | Instant. Puts *"target spell, nonland permanent, or card in a graveyard"* on top or bottom of its owner's library. Answers a commander permanently-ish (they must redraw it), and it hits things on the stack. |
| Collective Effort | `{1}{W}{W}` | Escalate — tap an untapped creature per extra mode. Late game one card destroys a big creature **and** an enchantment **and** puts a +1/+1 counter on each creature you control. |
| Loran of the Third Path | `{2}{W}` | 2/1 vigilance. *"When Loran enters, destroy up to one target artifact or enchantment."* Removal stapled to a body. |
| Damning Verdict | `{3}{W}{W}` | *"Destroy all creatures with no counters on them."* In this deck it is a one-sided board wipe. Check every creature you own actually has a counter before you cast it. |
| Promise of Loyalty | `{4}{W}` | Everyone keeps one creature and sacrifices the rest; yours keeps its counters **and** gains a vow counter (another Cheer enabler), and every surviving creature *"can't attack you."* Ruling: nobody may opt out. |

### Synergy — the counter engines — 14 cards

| Card | Cost | Why it's in |
|---|---|---|
| Hardened Scales | `{G}` | *"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1 counters are put on it instead."* One mana that upgrades every other card in this section. In 89.1% of the 19,181 Tidus decks EDHREC tracks. |
| Sphere Grid | `{1}{G}` | A +1/+1 counter whenever a creature of yours connects, **and** *"Creatures you control with +1/+1 counters on them have reach and trample."* An engine and an evasion package for two mana. |
| Shelinda, Yevon Acolyte | `{G}{W}` | 2/2 lifelink. Puts a +1/+1 counter on essentially every creature you play (on the new creature if its power is lower, otherwise on Shelinda). |
| Duskshell Crawler | `{1}{G}` | 0/3. *"When this creature enters, put a +1/+1 counter on target creature"* — any creature you like, usually a better body than this one — and *"Each creature you control with a +1/+1 counter on it has trample."* |
| Together Forever | `{W}{W}` | Support 2 on entry, then *"{1}: Choose target creature with a counter on it. When that creature dies this turn, return that card to its owner's hand."* Cheap insurance for your best creature. |
| Protection Magic | `{1}{W}` | *"Put a shield counter on each of up to three target creatures."* A shield counter absorbs damage or destruction — and it is a **counter**, so those creatures now switch on Cheer and survive `Damning Verdict`. |
| Tromell, Seymour's Butler | `{2}{G}` | *"Each other nontoken creature you control enters with an additional +1/+1 counter on it,"* plus a proliferate activation. Every creature after this arrives pre-loaded. |
| Rikku, Resourceful Guardian | `{2}{U}` | *"Whenever you put one or more counters on a creature, until end of turn, that creature can't be blocked by creatures your opponents control."* Tidus's beginning-of-combat move makes a creature unblockable for free, every turn. Ruling: it must happen **before** blockers are declared. |
| Simic Ascendancy | `{G}{U}` | Banks a growth counter for every +1/+1 counter you place; at twenty growth counters you win at your upkeep. A genuine second route to victory that the Tidus box did not have. |
| Fight Rigging | `{2}{G}` | Hideaway 5 — on entry you look at your top five, exile one face down and bottom the rest in a random order. Then a free +1/+1 counter at the beginning of combat every turn, and *"if you control a creature with power 7 or greater, you may play the exiled card without paying its mana cost."* The hidden card is dead weight until you get to power 7, so treat it as a bonus, not a plan. |
| Resourceful Defense | `{2}{W}` | *"Whenever a permanent you control leaves the battlefield, if it had counters on it, put those counters on target permanent you control."* Makes your counters nearly impossible to remove for good. |
| Forgotten Ancient | `{3}{G}` | 0/3. A +1/+1 counter off a spell cast by **any** player, then move any number of them onto other creatures at your upkeep. In a four-player pod this is the best mana-to-counters rate in the deck. |
| Path of Discovery | `{3}{G}` | Every creature you play explores: a land goes to your hand, or the creature gets a +1/+1 counter. Card selection and counters at once. |
| Inexorable Tide | `{3}{U}{U}` | *"Whenever you cast a spell, proliferate."* Lands, remember, are not spells — but at ~2.9 average mana value you are casting one to three spells a turn, and each one pumps your whole team. |

### Threats — 16 cards

| Card | Cost | Why it's in |
|---|---|---|
| Grateful Apparition | `{1}{W}` | 1/1 **flying**, proliferates whenever it connects. Your cheapest reliable way to turn Cheer on — it flies, so it gets through early. |
| Steelburr Champion | `{2}{W}` | 1/1 vigilance that grows off opponents' noncreature spells; Offspring `{1}{W}` gives you a 1/1 token copy on top. |
| Managorger Hydra | `{2}{G}` | 1/1 trample. *"Whenever a player casts a spell, put a +1/+1 counter on this creature."* Not optional and not just your spells — it snowballs fast at a four-player table. |
| Maester Seymour | `{2}{G}` | 1/3. *"At the beginning of combat on your turn, put a number of +1/+1 counters equal to Maester Seymour's power on another target creature you control,"* plus `{3}{G}{G}` monstrosity as a late-game finisher. |
| Kimahri, Valiant Guardian | `{2}{G}{U}` | 3/3 vigilance. Every combat it gains a counter, taps a blocker, and may become a copy of that creature. Removal, growth, and a body. |
| Wakka, Devoted Guardian | `{2}{G}{W}` | 4/4 reach trample. *"Blitzball Captain — At the beginning of your end step, if a counter was put on Wakka this turn, put a +1/+1 counter on each other creature you control."* Use Tidus's move to guarantee it. Ruling: *"Once your end step begins, it's too late to put a counter on Wakka in order to cause this ability to trigger."* |
| Summon: Ixion | `{2}{W}` | 3/3 first strike Saga. Chapter I exiles an opponent's creature *"until this Saga leaves the battlefield"* — and the Saga sacrifices itself after chapter III, so **the creature comes back**. Treat it as a two-turn Time Out, not removal. II and III put counters on up to two of yours and gain 2 life. Its lore counters also switch on Cheer by themselves. |
| Chocobo Knights | `{3}{W}` | 3/3. *"Whenever you attack, creatures you control with counters on them gain double strike until end of turn."* Your most common "and that's the game" card. |
| Auron, Venerated Guardian | `{3}{W}` | 2/5 vigilance. *"Shooting Star — Whenever Auron attacks, put a +1/+1 counter on it. When you do, exile target creature defending player controls with power less than Auron's power until Auron leaves the battlefield."* It clears its own blocker — but the exile lasts only as long as Auron does, so killing Auron hands the creature back. |
| Summon: Yojimbo | `{3}{W}` | 5/5 vigilance Saga, four chapters. I exiles an opponent's artifact, enchantment, or tapped creature (permanently — no "until" clause); II and III tax attacks against you `{2}` per creature; IV makes a Treasure per opponent with a power-4-or-greater creature, then it is sacrificed. Defence and offence in one card. |
| Luminous Broodmoth | `{2}{W}{W}` | 3/4 flying. *"Whenever a creature you control without flying dies, return it to the battlefield under its owner's control with a flying counter on it."* Your creatures come back **evasive and countered** — a board wipe becomes a delay. |
| Sunscorch Regent | `{3}{W}{W}` | 4/3 flying that gains a +1/+1 counter and 1 life on every opponent's spell. In both boxes; a flier that grows without your help. |
| Kalonian Hydra | `{3}{G}{G}` | 0/0 trample that enters with four +1/+1 counters, and *"Whenever this creature attacks, double the number of +1/+1 counters on each creature you control."* The single biggest swing card in the merged pool, and it came out of the Peace Offering box. |
| Summon: Magus Sisters | `{4}{G}` | 5/5 **haste** Saga. Each chapter randomly does one of: three +1/+1 counters, a shield counter and 3 life, or a fight. A 5/5 that attacks the turn it lands. |
| Sin, Unending Cataclysm | `{5}{G}{U}` | 5/5 flying trample. *"As Sin enters, remove all counters from any number of artifacts, creatures, and enchantments. Sin enters with X +1/+1 counters on it, where X is twice the number of counters removed this way."* Vacuum your own board, get double back on an evasive body. |
| Walking Ballista | `{X}{X}` | 0/0 artifact creature. *"Remove a +1/+1 counter from this creature: It deals 1 damage to any target."* The only damage in the deck that doesn't need to attack — how you finish someone at 3 life through a wall of blockers. Note `{X}{X}` means you pay X **twice**. |

### Utility — 2 cards

| Card | Cost | Why it's in |
|---|---|---|
| Swiftfoot Boots | `{2}` | Equip `{1}`. Hexproof and haste. Hexproof means *"It can't be the target of spells or abilities your opponents control"* — the cheapest way to stop the commander tax spiral on Tidus. |
| Baird, Steward of Argive | `{2}{W}{W}` | 2/4 vigilance. *"Creatures can't attack you or planeswalkers you control unless their controller pays {1} for each of those creatures."* The Tidus box had **no permanent** attack taxer — only `Summon: Yojimbo`'s chapters II-III, which tax *"until your next turn"* and then run out. Baird never runs out. This is the card that buys you the turns 5-8 you need to assemble a board. |

### Lands — 36 cards

**23 non-basic + 13 basic (5 Forest, 4 Plains, 4 Island).**

| Land | Role |
|---|---|
| Command Tower | *"Add one mana of any color in your commander's color identity."* Untapped, perfect. |
| Exotic Orchard | Any colour an opponent's land could produce — in practice a dual or better at a four-player table. |
| Seaside Citadel | Enters tapped, taps for `{G}`, `{W}` **or** `{U}`. The only true tri-land in the pool. |
| Brushland | Untapped `{G}`/`{W}` for 1 damage to you. |
| Adarkar Wastes | Untapped `{W}`/`{U}` for 1 damage to you. |
| Yavimaya Coast | Untapped `{G}`/`{U}` for 1 damage to you. |
| Glacial Fortress | `{W}`/`{U}`, untapped if you control a Plains or an Island. |
| Hinterland Harbor | `{G}`/`{U}`, untapped if you control a Forest or an Island. |
| Sunpetal Grove | `{G}`/`{W}`, untapped if you control a Forest or a Plains. |
| Fortified Village | `{G}`/`{W}`, untapped if you reveal a Forest or Plains from hand. |
| Port Town | `{W}`/`{U}`, untapped if you reveal a Plains or Island from hand. |
| Vineglimmer Snarl | `{G}`/`{U}`, untapped if you reveal a Forest or Island from hand. |
| Razorverge Thicket | `{G}`/`{W}`, untapped while you control two or fewer other lands — a turn 1-3 land. |
| Seachrome Coast | `{W}`/`{U}`, same early-game clause. |
| Canopy Vista | `{G}`/`{W}` dual with the Forest and Plains land types — untapped once you control two basics, and a legal `Farseek` target. |
| Prairie Stream | `{W}`/`{U}` with the Plains and Island types — same, and also a `Farseek` target. |
| Flooded Grove | Filter land: `{G/U}, {T}` turns one mana into `{G}{G}`, `{G}{U}` or `{U}{U}`. |
| Temple of Plenty | Tapped, **scry 1** on entry, then `{G}`/`{W}`. Scry 1 = look at your top card and either leave it or put it on the bottom (CR **701.22a**) — it is not a draw, it is a filter. That one look is the whole reason you accept the tapped turn. |
| Temple of Mystery | Tapped, scry 1, `{G}`/`{U}`. |
| Temple of Enlightenment | Tapped, scry 1, `{W}`/`{U}`. |
| Nesting Grounds | *"{1}, {T}: Move a counter from target permanent you control onto a second target permanent."* A second Tidus ability that lives on a land. |
| Forge of Heroes | *"{T}: Choose target commander that entered this turn. Put a +1/+1 counter on it if it's a creature and a loyalty counter on it if it's a planeswalker."* Tidus lands with a counter already on him, so his move ability is live immediately. |
| Ash Barrens | Taps for `{C}`, or basic landcycling `{1}` fetches whichever basic colour you're short. |
| 5 × Forest, 4 × Plains, 4 × Island | Basics are not singleton-limited. They're also what makes `Canopy Vista`, `Prairie Stream`, `Cultivate` and `Ash Barrens` work. |

---

## 3. The land count, defended

This is the number people get wrong, so here is the actual arithmetic rather than a vibe.

**What the parents run** (`mtg deck stats <slug> -v`, both run this session):

| | Tidus (Counter Blitz) | Bumbleflower (Peace Offering) |
|---|---|---|
| Lands | 37 | 38 |
| Non-lands | 62 | 61 |
| Average MV of non-lands | **3.03** | **3.21** |
| Ramp pieces | 12 | 14 |
| Tool verdict | land count **SANE** | land count **HEAVY on lands** |
| Lands entering tapped | 16 of 37 = **43%** | 14 of 38 = **37%** |

The heuristic the tool uses (`_recommended_lands` in `src/cmd_decks.py`, read this session) is
transparent: avg MV under 2.80 → 33-35 lands; 2.80-3.00 → 35-37; 3.00-3.30 → 37-38; and it
subtracts 1 from both ends of the band once you have 10 or more ramp pieces. That is where the
"roughly 37-38 lands at avg MV 3.0-3.3" rule of thumb comes from.

**What the merged deck actually is:**

```
non-land cards            : 63
average mana value        : 2.90   → band "avg MV 2.8-3.0 (low curve)" → 35-37 lands
ramp pieces               : 12     → 10 or more, so the band shifts down 1 → 34-36 lands
LANDS RUN                 : 36     → top of the recommended band
curve  0:1  1:6  2:18  3:20  4:11  5:6  7:1
```

**So: 36 lands, not 37.** The merge let us cut the expensive, off-plan cards from both boxes
(`Coveted Jewel` `{6}`, `Realm-Cloaked Giant` MV 7, `Bane of Progress` `{4}{G}{G}`,
`Farewell` `{4}{W}{W}`, `Sphinx of Enlightenment` `{4}{U}{U}`, `Perch Protection` `{4}{W}{W}`,
`Ghirapur Orrery` `{4}`, `Intellectual Offering` `{4}{U}`), which pulled the average mana value
from 3.03 / 3.21 down to **2.90**. A cheaper deck wants fewer lands. Running 37 here would put you
one above the band — the same "expect flood" flag the tool raises on Peace Offering today. I took
the top of the band rather than the bottom because this is a three-colour deck where missing a
colour is as bad as missing a land.

**Colour sources** (counted from the actual land list; `Exotic Orchard` excluded because its output
depends on your opponents). A **pip** is one coloured mana symbol in a cost — `{3}{W}{W}` is two
white pips, `{G}{W}{U}` is one of each — so the pip count is a demand curve: it says how badly the
deck wants each colour, and the source count says how well the lands supply it.

```
colored pips in the 63 non-lands   W:32   U:15   G:31
colored sources in the 36 lands    W:18   U:17   G:18   (+ Exotic Orchard, + Arcane Signet,
                                                          Faeburrow Elder, Yuna, Ash Barrens)
```

Note what that says about the deck: **it is a green-white deck with a blue splash.** Blue is 15 of
78 coloured pips. The only cards that ask for two blue in a hurry are `Pull from Tomorrow`
(`{X}{U}{U}`) and `Inexorable Tide` (`{3}{U}{U}`), both of which you cast late. That is why 17 blue
sources is enough here and would not be in a blue-primary deck.

**Lands entering tapped: 14 of 36 = 39%** — 4 always (`Seaside Citadel` and the three Temples),
10 conditionally. Slightly worse than Peace Offering's 37%, meaningfully better than Tidus's 43%.
With a curve peaking at 2 and 3 mana, sequencing matters: play the tapped land on a turn you were
not going to spend all your mana anyway.

---

## 4. The cut list — 67 cards, and why

The two boxes offer 157 distinct cards. 90 of those names made the deck (63 spells + 23 non-basic
lands + 3 basic land names + the commander). Here is every card that did not, grouped by the reason
it lost its slot. Knowing *why* is the part that makes you a better deckbuilder.

### 4a. Off-plan — they support the Bumbleflower deck, not this one (24)

These are good cards. They are good at *handing the table cards and getting paid for having a huge
hand*, which is not what this deck does. Once Bumbleflower is not the commander, most of them stop
being worth a card.

`Body of Knowledge` `{3}{U}{U}` · `Psychosis Crawler` `{5}` · `Triskaidekaphile` `{1}{U}` ·
`Twenty-Toed Toad` `{3}{U}` · `Wizard Class` `{U}` · `Jolrael, Mwonvuli Recluse` `{1}{G}` ·
`Kwain, Itinerant Meddler` `{W}{U}` · `Jolly Gerbils` `{1}{W}` · `Secret Rendezvous` `{1}{W}{W}` ·
`Intellectual Offering` `{4}{U}` · `Tenuous Truce` `{1}{W}` · `Tempt with Bunnies` `{2}{W}` ·
`Sphinx of Enlightenment` `{4}{U}{U}` · `Mr. Foxglove` `{2}{G}{W}{U}` · `Coveted Jewel` `{6}` ·
`Ghirapur Orrery` `{4}` · `Rites of Flourishing` `{2}{G}` · `Fisher's Talent` `{2}{G}{U}` ·
`Communal Brewing` `{2}{G}` · `Selvala, Explorer Returned` `{1}{G}{W}` ·
`Tamiyo, Field Researcher` `{1}{G}{W}{U}` · `Ms. Bumbleflower` `{1}{G}{W}{U}` ·
`Octomancer` `{3}{G}{U}` · `Martial Impetus` `{2}{W}`

Worked examples so this isn't hand-waving:
- **`Secret Rendezvous`** is literally *"You and target opponent each draw three cards."* Three cards
  for you and three for a player who is trying to kill you is a bad trade when you're the one with
  the scary board.
- **`Coveted Jewel`** (`{6}`) draws three and taps for three, but *"Whenever one or more creatures an
  opponent controls attack you and aren't blocked, that player draws three cards and gains control
  of this artifact."* You are the aggressor; you will be attacked back.
- **`Rites of Flourishing`** gives *every* player an extra draw and an extra land each turn. You are
  ahead on board — symmetric effects help whoever is behind.
- **`Selvala, Explorer Returned`** makes green mana but *"each player draws a card"* every time you
  tap it. Three opponents, three cards, once per turn.
- **`Martial Impetus`** is an Aura that goads an opponent's creature — *"Enchanted creature gets
  +1/+1 and is goaded"*, meaning it must attack, and must attack somebody other than you. Pure
  table politics. It doesn't build your board and it hands an opponent a permanent +1/+1.

### 4b. Redundant — a worse copy of something already in the 100 (18)

`Long River's Pull` `{U}{U}` (counters creature spells only; `An Offer You Can't Refuse` `{U}` is
cheaper and hits the board wipes) · `Wear Down` `{1}{G}` (sorcery; `Broken Wings` `{2}{G}` is an
instant and also kills fliers) · `Peerless Recycling` `{1}{G}` (recursion for a deck with almost
nothing worth recurring) · `Riot Control` `{2}{W}` and `Spore Frog` `{G}` (one-shot fogs; the deck
would rather have a threat) · `Perplexing Test` `{3}{U}{U}` and `Illusionist's Gambit` `{2}{U}{U}`
(defensive resets that also undo *your* board) · `Realm-Cloaked Giant // Cast Off` (its `Cast Off`
half destroys all non-Giant creatures — including all of yours; `Damning Verdict` `{3}{W}{W}` does
the same job one-sidedly) · `Mangara, the Diplomat` `{3}{W}` (`Baird` taxes attacks for one less
mana) · `Everflowing Chalice` `{0}` and `Thought Vessel` `{2}` (rocks 13 and 14 in a deck that
already has 12) · `Gatta and Luzzu` `{2}{W}` (damage prevention that turns into counters — real, but
`Protection Magic` `{1}{W}` covers three creatures for the same effect) ·
`Scholar of New Horizons` `{1}{W}` (a worse `Ash Barrens` on a 1/1) · `Summoner's Sending` `{1}{W}` ·
`O'aka, Traveling Merchant` `{1}{U}` (turns counters into cards, but this deck wants counters to
*stay on* creatures) · `Yuna's Whistle` `{1}{G}{G}` · `Generous Patron` `{2}{G}` (a 1/4 whose
"support 2" is real, but its draw trigger only fires *"Whenever you put one or more counters on a
creature you don't control"* — you almost never do) · `Lulu, Stern Guardian` `{2}{U}` (a
`{3}{U}` proliferate outlet and a stun counter on one attacker per opponent's attack — much slower
than `Grateful Apparition` `{1}{W}` and `Tromell, Seymour's Butler` `{2}{G}`, both already in)

### 4c. Too expensive for a 2.90-curve deck (7)

Every card here is fine in a vacuum and each one would push the average mana value up, which would
force a 37th and 38th land, which would make the deck slower again. That is the actual cost.

`Farewell` `{4}{W}{W}` · `Bane of Progress` `{4}{G}{G}` · `Perch Protection` `{4}{W}{W}` ·
`Summon: Valefor` `{4}{U}` · `Tempt with Discovery` `{3}{G}` · `Rampant Rejuvenator` `{3}{G}` ·
`Altered Ego` `{X}{2}{G}{U}`

Two of these deserve a sentence each:
- **`Farewell`** is the only card in either box on the official **Game Changers** list — see §9. Its
  text is *"Choose one or more — Exile all artifacts. / Exile all creatures. / Exile all
  enchantments. / Exile all graveyards."* It **exiles your board too**, and exile dodges your
  `Luminous Broodmoth` and `Yuna, Grand Summoner` recovery, both of which need permanents to hit a
  *graveyard*. It is anti-synergy at six mana and it is the sole reason the parent Tidus deck is
  rated a bracket above this one.
- **`Bane of Progress`** destroys all artifacts and enchantments — including your `Hardened Scales`,
  `Sphere Grid`, `Simic Ascendancy`, `Fight Rigging`, `Path of Discovery`, `Inexorable Tide`,
  `Together Forever`, `Resourceful Defense`, and all four Saga creatures. It is a six-mana way to
  blow up your own deck.

### 4d. Weaker version of a card in the 100, specifically among engines (3)

`Bloodroot Apothecary` `{2}{G}` (toxic/poison and Treasure-sacrifice payoffs; this deck has no
poison plan and gives an opponent a Treasure on entry) · `Hoofprints of the Stag` `{1}{W}` (four
draws for one 4/4 — slower than `Chasm Skulker`, which is already in) · `Coiling Oracle` `{G}{U}`
(a 1/1 that flips one card; `Path of Discovery` does that for every creature)

### 4e. Lands that lost the mana-base cut (14)

`Idyllic Beachfront`, `Radiant Grove`, `Tangled Islet`, `Thriving Grove`, `Thriving Heath`,
`Thriving Isle` — six duals that **always** enter tapped, and I was already carrying four of those.
`Skycloud Expanse`, `Sungrass Prairie`, `Overflowing Basin` — these need `{1}` **plus** the tap to
make two mana, so they are a net gain only on turns you have spare mana. `Evolving Wilds` and
`Terramorphic Expanse` — fetch a basic **tapped**; `Ash Barrens` does the same job while still being
able to tap for `{C}` on a turn you don't need it. `Reliquary Tower` (no maximum hand size — this
deck does not hoard cards) and `Path of Ancestry` (always tapped; the scry only happens on a
creature spell that shares a type with Tidus, i.e. Human or Warrior). `Temple of the False God` was
cut too — *"Activate only if you control five or more lands"* means it produces literally nothing
before turn 5, and in a three-colour deck a land that never makes coloured mana is a liability.

### 4f. One deliberate cut you should know about: `Yuna's Decision` `{3}{G}`

It is a fine card (*"Sacrifice a creature. If you do, draw a card, then you may put a creature card
and/or a land card from your hand onto the battlefield"* or *"Return one or two target permanent
cards from your graveyard to your hand"*) and the role tool counts it as ramp, draw, removal **and**
recursion at once. It lost to `Cultivate` and `Inspiring Call` on raw rate at four mana. If you find
yourself wanting one more flexible card, this is the first one I'd put back — over `Blitzball
Stadium`.

---

## 5. What the merged deck does that neither parent did

Being honest first: **this is fundamentally the Tidus plan.** You attack with creatures covered in
+1/+1 counters, Cheer draws and proliferates, and around turn 8-11 someone dies to a wide attack.
The merge did not invent a strategy.

But do **not** just carry Counter Blitz's piloting over unchanged — the two decks are close, not
identical, and every difference points the same way (faster, leaner, less insurance):

| | Counter Blitz | This deck |
|---|---|---|
| Lands | 37 | **36** |
| Average MV of the non-lands | 3.03 | **2.90** |
| Lands entering tapped | 16 of 37 = 43% | **14 of 36 = 39%** |
| Board wipes you own | 4 (`Farewell`, `Bane of Progress`, `Damning Verdict`, `Promise of Loyalty`) | **2** — `Damning Verdict` and `Promise of Loyalty`; `Farewell` and `Bane of Progress` are cut (§4c) |
| Removal / interaction | 8 / 3 | **11** combined |
| Alternate win condition | none (`wincon 0`) | `Simic Ascendancy` |
| Permanent attack taxer | none — only `Summon: Yojimbo`'s chapters II-III, which last until your next turn and then the Saga is gone | `Baird, Steward of Argive`, always on, plus Yojimbo |

Practical consequences: you have **no answer that resets a board you are losing** — `Farewell` is
gone, so there is no "wipe it and rebuild" button, and `Damning Verdict` only works while your own
creatures all carry counters. You have one fewer land and a cheaper curve, so hands that Counter
Blitz could keep on 3 lands and expensive spells are now keeps on 2-3 lands and cheap ones. And you
have a second way to win that changes what you do with a stalled board. §7 and §8 below are written
for *this* list — read them instead of, not after, Counter Blitz's.

What it actually bought you is four specific things, and they are all measurable.

**1. Real removal. This is the big one.** The parent decks ran 8 and 4 removal spells respectively.
This deck runs 11 removal/interaction cards *and they are better cards*, because the two boxes'
answers had almost no overlap. Peace Offering supplied `Swords to Plowshares` `{W}`,
`Generous Gift` `{2}{W}`, `Broken Wings` `{2}{G}` and `Loran of the Third Path` `{2}{W}`; the FINAL
FANTASY box supplied `Path to Exile` `{W}`, `Destroy Evil` `{1}{W}`, `Endless Detour` `{G}{W}{U}`,
`Collective Effort` `{1}{W}{W}` and `Damning Verdict` `{3}{W}{W}`. Neither deck alone could answer
an artifact, an enchantment, a land, a creature, and a spell on the stack. This one can.

**2. A second way to win.** The Tidus box's own primer says it plainly — the role tool reports
`wincon 0` for that deck. `Simic Ascendancy` `{G}{U}` came out of the Peace Offering box and reads
*"At the beginning of your upkeep, if this enchantment has twenty or more growth counters on it, you
win the game."* Every +1/+1 counter you put on your own creature also puts a growth counter on it.
Read the ruling before you rely on it: *"If Simic Ascendancy doesn't have twenty or more growth
counters on it as your upkeep begins, its last ability won't trigger."* You must already be at 20
when the upkeep starts — plan the turn before.

**3. One card that is a bigger swing than anything in the Tidus box.** `Kalonian Hydra` `{3}{G}{G}`
doubles the +1/+1 counters on *each creature you control* every time it attacks. On a board of four
countered creatures that is more raw stats than any single card in Counter Blitz produces. It was
sitting in the Peace Offering box, where a deck that wins by flying over a stall barely used it.

**4. It is genuinely more consistent, and it is faster.** Average mana value dropped from 3.03 /
3.21 to **2.90**. Lands entering tapped dropped from 43% to 39%. Ramp went to 12 with three real
mana rocks plus `Fellwar Stone` and `Mind Stone` that the Tidus box didn't have. And you finally
have an attack-taxer — `Baird, Steward of Argive` `{2}{W}{W}` — so the turns you spend assembling a
board are turns you're less likely to just die.

**What the merge did NOT do, so you're not surprised at the table:** it did not add a tutor (a card
that searches your library for a specific nonland card) — there are zero in either box, so the shape
of your opening hand is still the whole game. It did not add a combo. It did not make you fast: this
is still a turn 8-11 deck in a four-player pod. And it is still, at heart, a fair creature deck that
loses to a genuine combo deck if that deck goes off before turn 8.

---

## 6. The physical build — a checklist you can work through at the table

You own two boxes. **21 of the 100 cards exist in both boxes**, so you own two physical copies of
each of those. That is the lever that makes this build cheap: for every one of those 21 you only
have to gut *one* parent deck.

### The strategy for pulling cards

**Pull all 21 shared cards out of the FINAL FANTASY (Tidus) box.** That box is losing its commander
anyway, so Counter Blitz stops existing either way. Peace Offering then only loses its 19 unique
donations and stays mostly intact. Details in §10.

### Checklist A — from the FINAL FANTASY box (`Counter Blitz`): the commander + 46 cards

```
COMMANDER
[ ] Tidus, Yuna's Guardian

CREATURES & SAGAS  (22)
[ ] Auron, Venerated Guardian       [ ] Chocobo Knights
[ ] Duskshell Crawler               [ ] Fathom Mage
[ ] Grateful Apparition             [ ] Gyre Sage
[ ] Incubation Druid                [ ] Kimahri, Valiant Guardian
[ ] Lord Jyscal Guado               [ ] Luminous Broodmoth
[ ] Maester Seymour                 [ ] Rikku, Resourceful Guardian
[ ] Shelinda, Yevon Acolyte         [ ] Sin, Unending Cataclysm
[ ] Summon: Ixion                   [ ] Summon: Magus Sisters
[ ] Summon: Yojimbo                 [ ] Tireless Tracker
[ ] Tromell, Seymour's Butler       [ ] Wakka, Devoted Guardian
[ ] Walking Ballista                [ ] Yuna, Grand Summoner

ENCHANTMENTS  (8)
[ ] Bred for the Hunt               [ ] Fight Rigging
[ ] Hardened Scales                 [ ] Inexorable Tide
[ ] Path of Discovery               [ ] Resourceful Defense
[ ] Sphere Grid                     [ ] Together Forever

INSTANTS / SORCERIES  (9)
[ ] Collective Effort               [ ] Damning Verdict
[ ] Destroy Evil                    [ ] Endless Detour
[ ] Inspiring Call                  [ ] Path to Exile
[ ] Protection Magic                [ ] Pull from Tomorrow
[ ] Three Visits

ARTIFACT  (1)
[ ] Blitzball Stadium

LANDS  (6)
[ ] Ash Barrens                     [ ] Forge of Heroes
[ ] Fortified Village               [ ] Nesting Grounds
[ ] Port Town                       [ ] Vineglimmer Snarl
```

*(22 + 8 + 9 + 1 + 6 = 46, plus Tidus himself = 47 cards leaving this box before you touch
Checklist C.)*

### Checklist B — from the Peace Offering box, 19 unique cards

```
CREATURES  (7)
[ ] Baird, Steward of Argive        [ ] Faeburrow Elder
[ ] Kalonian Hydra                  [ ] Loran of the Third Path
[ ] Managorger Hydra                [ ] Rishkar, Peema Renegade
[ ] Steelburr Champion

ENCHANTMENT  (1)
[ ] Simic Ascendancy

INSTANTS / SORCERIES  (4)
[ ] Broken Wings                    [ ] Cultivate
[ ] Generous Gift                   [ ] Swords to Plowshares

ARTIFACTS  (3)
[ ] Fellwar Stone                   [ ] Mind Stone
[ ] Swiftfoot Boots

LANDS  (4)
[ ] Adarkar Wastes                  [ ] Razorverge Thicket
[ ] Seachrome Coast                 [ ] Yavimaya Coast
```

*(7 + 1 + 4 + 3 + 4 = 19.)*

### Checklist C — ⚠️ the 21 cards you own TWO of, one in each box

**This is the trade you need to understand.** You own two physical copies of each card below — one
sleeved in Counter Blitz, one in Peace Offering. The merged deck only needs one. Take it from the
**FINAL FANTASY box** (Counter Blitz is being disassembled anyway) and the Peace Offering copy stays
where it is.

```
NON-LANDS  (8)
[ ] An Offer You Can't Refuse       [ ] Arcane Signet
[ ] Chasm Skulker                   [ ] Farseek
[ ] Forgotten Ancient               [ ] Promise of Loyalty
[ ] Sol Ring                        [ ] Sunscorch Regent

LANDS  (13)
[ ] Brushland                       [ ] Canopy Vista
[ ] Command Tower                   [ ] Exotic Orchard
[ ] Flooded Grove                   [ ] Glacial Fortress
[ ] Hinterland Harbor               [ ] Prairie Stream
[ ] Seaside Citadel                 [ ] Sunpetal Grove
[ ] Temple of Enlightenment         [ ] Temple of Mystery
[ ] Temple of Plenty
```

*(8 + 13 = 21.)*

**If you ever want both parents playable at once**, these 21 are exactly the cards you'd need a
second copy of — and you already have it. Nothing on this list forces you to break two decks.

### Checklist D — basic lands (13)

Basic lands are **not** singleton-limited — that's why the merged deck runs five Forests. Both boxes
supply them and you have far more than you need:

| Basic | Merged deck needs | Counter Blitz has | Peace Offering has | Combined |
|---|---|---|---|---|
| Forest | 5 | 3 | 4 | 7 |
| Plains | 4 | 3 | 4 | 7 |
| Island | 4 | 3 | 4 | 7 |

```
[ ] 5 Forest   — take all 3 from Counter Blitz + 2 from Peace Offering
[ ] 4 Plains   — take all 3 from Counter Blitz + 1 from Peace Offering
[ ] 4 Island   — take all 3 from Counter Blitz + 1 from Peace Offering
```

(If you have loose basics from anywhere else — the `Scrappy Survivors` box has 4 Forest and 4 Plains,
for instance — use those instead and leave Peace Offering's basics alone.)

### Order of operations at the table

1. Lay out both decks face up, sorted by type.
2. Work Checklist C first (the 21 shared cards) — pull the **Counter Blitz** copy of each. Peace
   Offering is untouched so far.
3. Work Checklist A — everything else out of Counter Blitz. That box is now empty of anything the
   merge wants.
4. Work Checklist B — 19 cards out of Peace Offering.
5. Work Checklist D — basics.
6. Count the pile. **It must be 100.** Then count the lands: **36.**
7. Sleeve it. Put Tidus in a separate spot — he starts the game in the **command zone**, not the deck.

---

## 7. What to mulligan for

Counter Blitz's primer has a mulligan section, but it is written for a 37-land, 3.03-MV deck with
`Farewell` in it. Every number below was recomputed over **this** 100-card list.

### The rule, stated correctly

**London mulligan (CR 103.5):** shuffle your hand into your library, draw a fresh seven, then put a
number of cards equal to *the number of mulligans you have taken* on the bottom in any order.

**Your first mulligan in Commander is free.** CR **103.5c**: *"In a multiplayer game and in any
Brawl game, the first mulligan a player takes doesn't count toward the number of cards that player
will put on the bottom of their library or the number of mulligans that player may take."* So
mulligan #1 is a clean new seven — you bottom nothing. Mulligan #2 bottoms one, #3 bottoms two.
New players hoard bad sevens because they think every mulligan costs a card. The first one doesn't.
**Take it.**

Tidus is **not** in your opening hand. He starts in the command zone, so you are drawing seven from
a 99-card library that contains 36 lands.

### The numbers, for this deck

Hypergeometric over the real list — 36 lands in 99 cards, draw 7:

| Lands in your opening seven | Chance |
|---|---|
| 0 | 3.7% |
| 1 | 16.4% |
| 2 | 29.8% |
| 3 | 28.6% |
| 4 | 15.7% |
| 5 | 5.0% |
| 6 or more | 0.9% |

**2-5 lands = 79% of hands. 0-1 lands = 20%.** One opening seven in five is an automatic mulligan on
land count alone, and the free first mulligan exists precisely for it.

### The 10-second checklist

Keep the hand if all four are true.

1. **2 to 5 lands.** Not 1 — this deck has **zero tutors** (§5) and only 8 draw spells, so there is
   no digging your way out. Not 6+ either; at 2.90 average mana value a 6-land seven is a hand with
   one spell in it.
2. **A green *or* a white source.** The cheap half of the deck is `{G}` and `{W}`: `Hardened Scales`
   `{G}`, `Swords to Plowshares` `{W}`, `Path to Exile` `{W}`, `Sphere Grid` `{1}{G}`,
   `Duskshell Crawler` `{1}{G}`, `Shelinda, Yevon Acolyte` `{G}{W}`. Blue is a splash — 15 of the 78
   coloured pips (§3) — so a hand with no blue source is fine. A hand with neither green nor white
   is not.
3. **Something to do on turn 2 or turn 3.** Ramp counts: **8 of the 12 ramp pieces cost 2 or less** —
   `Sol Ring` `{1}`, `Arcane Signet` `{2}`, `Fellwar Stone` `{2}`, `Mind Stone` `{2}`, `Farseek`
   `{1}{G}`, `Three Visits` `{1}{G}`, `Gyre Sage` `{1}{G}`, `Incubation Druid` `{1}{G}`. So does any
   of the 25 non-lands at mana value 2 or less (the whole `0:1 1:6 2:18` end of the curve, §3).
4. **A creature or a counter engine in it somewhere.** A hand of lands and removal is not a keep in a
   deck that wins by attacking — and Tidus does nothing on an empty board (§8, mistake 1).

Two adjustments specific to this build:

- **Count untapped lands, not lands.** 14 of the 36 enter tapped — 4 always (`Seaside Citadel` and
  the three Temples), 10 conditionally (§3). A "three-land" hand of `Seaside Citadel` +
  `Temple of Plenty` + `Temple of Mystery` casts its first two-drop on turn 3. Downgrade it to a
  two-lander and judge it as one.
- **Do not mulligan chasing `{G}{W}{U}` on turn 3.** The commander is a bonus, not the plan. Among
  the 36 lands there are 18 white, 17 blue and 18 green sources (§3), before `Exotic Orchard`,
  `Arcane Signet`, `Faeburrow Elder`, `Yuna, Grand Summoner` and `Ash Barrens` — the colours turn
  up. A turn-5 Tidus onto a board of two countered creatures beats a turn-3 Tidus onto nothing.

---

## 8. Common mistakes with this deck

Nine ways to lose a game you had won. Every card quote here is from the local database.

**1. Casting Tidus into an empty board.** His combat trigger needs *two* creatures — one holding a
counter and a second to move it to — and Cheer needs a creature with a counter to connect with a
player. On an empty board he is a 3/3 that eats a removal spell, and every recast costs `{2}` more
(CR **903.8**, commander tax). Build first, then cast him.

**2. Casting `Damning Verdict` without auditing your own side.** It reads *"Destroy all creatures
with no counters on them"* — **all**, including yours. The ones that quietly die: `Walking Ballista`
after you have shot off its last +1/+1 counter, `Chasm Skulker`'s Squid tokens, the 1/1 Offspring
token copy of `Steelburr Champion`, and anything you cast this turn that hasn't been given a counter
yet. The flip side is the useful half: *any* counter saves a creature, not just +1/+1 — which is
what `Protection Magic`'s shield counters, the Sagas' lore counters and `Promise of Loyalty`'s vow
counters are quietly for.

**3. Forgetting Cheer is once a turn but the other payoffs are not.** Tidus says *"you may draw a
card and proliferate. Do this only once each turn."* `Bred for the Hunt` `{1}{G}{U}` says *"Whenever
a creature you control with a +1/+1 counter on it deals combat damage to a player, you may draw a
card"* — that one is **per creature**. Attacking with five countered creatures draws one card off
Tidus and five off Bred for the Hunt. Attack wide, not tall.

**4. Missing an end-step check.** `Wakka, Devoted Guardian` and `Lord Jyscal Guado` both look back at
the turn *as the end step begins*. Wakka's ruling (2025-06-06): *"Once your end step begins, it's too
late to put a counter on Wakka in order to cause this ability to trigger."* Jyscal has the same
ruling. If you want Blitzball Captain, move the counter onto Wakka during combat — not after.

**5. Proliferating your own Sagas to death.** A Saga is sacrificed as a state-based action the moment
its lore counters reach its final chapter (CR **714.4**). `Summon: Ixion` and
`Summon: Magus Sisters` finish at III, `Summon: Yojimbo` at IV. `Inexorable Tide`,
`Grateful Apparition` and `Tromell, Seymour's Butler` will happily push them over the edge. And
Ixion's chapter I exiles a creature *"until this Saga leaves the battlefield"* — so proliferating
Ixion to death **hands the creature straight back**, untapped, to an opponent who is now free to
block with it.

**6. Treating Auron's exile as removal.** Same trap: *"exile target creature defending player
controls with power less than Auron's power **until Auron leaves the battlefield**."* Kill Auron —
or chump-block him into a bigger creature — and the exiled creature returns. Only `Swords to
Plowshares`, `Path to Exile` and `Summon: Yojimbo`'s chapter I exile permanently.

**7. Moving counters after blockers are declared.** `Rikku, Resourceful Guardian` reads *"Whenever
you put one or more counters on a creature, until end of turn, that creature can't be blocked by
creatures your opponents control"*, and her ruling is explicit: *"Once a
creature has been blocked, Rikku's first ability won't cause it to become unblocked."* Tidus's move
happens at the beginning of combat, which is before attackers are even declared — that is the whole
reason it works. `Maester Seymour`, `Fight Rigging` and `Kimahri, Valiant Guardian` all fire in the
same step. Stack every beginning-of-combat trigger you have, resolve them all, *then* declare
attackers.

**8. Playing the tapped land on the wrong turn.** 39% of your lands can enter tapped. With the curve
peaking at 2 and 3 mana, the tapped land goes down on a turn you were not going to empty your mana
anyway — typically the turn you cast nothing, or the turn you cast a one-drop. Getting this wrong is
worth about a full turn of tempo per game and it costs nothing to get right.

**9. Attacking with a creature whose power is *currently* 0.** `Incubation Druid` (0/2),
`Duskshell Crawler` (0/3) and `Forgotten Ancient` (0/3) are printed at 0 power, and a 0-power
creature that gets through deals **no** combat damage — so it triggers nothing: not Cheer, not
`Bred for the Hunt`, not `Sphere Grid` (*"Whenever a creature you control deals combat damage to a
player, put a +1/+1 counter on that creature"*), not `Blitzball Stadium`'s draw. It just dies for
free. `Forgotten Ancient` is the specific trap: the way you use it is its upkeep ability,
*"move any number of +1/+1 counters from this creature onto other creatures"* — which leaves it back
at 0 power by the time you declare attackers. Read the counters on the card, not the ones you
remember putting there. (`Faeburrow Elder` and `Kalonian Hydra` are also printed 0/0 but are
essentially never 0 power in play: the Elder *"gets +1/+1 for each color among permanents you
control"* and the Hydra enters with four +1/+1 counters.)

**And one timing rule that wins games:** `Simic Ascendancy` reads *"At the beginning of your upkeep,
if this enchantment has twenty or more growth counters on it, you win the game."* Its ruling: *"If Simic
Ascendancy doesn't have twenty or more growth counters on it as your upkeep begins, its last ability
won't trigger."* You cannot get to 20 during your upkeep and win on the spot — you must already be
at 20 when the upkeep starts. Count on the turn before.

---

## 9. Estimated bracket

`data/brackets.json` (fetched 2026-07-26 from Scryfall's `is:gamechanger` search) lists **53 Game
Changers** — cards strong enough that including them raises the bracket a deck is honestly presented
as. I scanned the final 100 against that list programmatically (§11, check f).

```
GAME CHANGERS in the final 100: NONE
```

The only Game Changer in either box is `Farewell` `{4}{W}{W}`, and it is cut — for deck reasons, not
bracket reasons (it exiles your own board; see §4c).

**Estimated bracket: 2 — Core.** Brackets 1 and 2 both require zero Game Changers. The other
automatic signals are clean too: no mass land denial (nothing here destroys everyone's lands), no
extra-turn effects, and I found no two-card infinite combo while reading the list — though that last
one is a human judgement, not a tool output, so treat it as "checked, not proven."

**For comparison, run this session:** `mtg deck bracket tidus` → **Bracket 3 (Upgraded)**, entirely
because of the single `Farewell`. `mtg deck bracket bumbleflower` → **Bracket 2 (Core)**.

**The honest caveat.** This deck is a *tuned* Bracket 2, and it plays noticeably above a precon out
of the box: better removal, a lower curve, a second win route in `Simic Ascendancy`, and
`Kalonian Hydra` as a genuine swing card. Bracket 3's description is *"a precon that has been
deliberately tuned"* — which is literally what this is. The Game Changer count says 2 and the
construction says "top of 2, knocking on 3."

**What to say when you sit down.** Something like: *"Bracket 2, upgraded — it's my two Bant precons
merged into one. +1/+1 counters, one alternate win condition on Simic Ascendancy, no Game Changers,
no combo. Games go long."* That is a complete and honest pitch, and it is exactly the etiquette a
bracket-aware table expects.

**If you ever want it to be a real Bracket 3:** put `Farewell` back in and cut `Blitzball Stadium`.
One card, one bracket.

---

## 10. What this does to the parent decks

Plain answer: **Counter Blitz ceases to exist. Peace Offering survives, wounded but real.**

### Counter Blitz (Tidus) — gone

It loses its commander, plus the **46** other cards that only it has (Checklist A), plus its copy of
each of the 21 shared cards (Checklist C), plus its 9 basics: 1 + 46 + 21 + 9 = **77 cards out of
100**. Only **23 of its 100 cards** are not wanted by the merge, and one of the things it loses is
`Tidus, Yuna's Guardian` himself, which is the whole deck. There is no version of this where you
build the merged deck and still have Counter Blitz. Accept that going in — it is the price of the
project, and the merged deck is strictly the better Tidus deck.

**To make it whole again** you would need to buy 77 cards, including a second `Tidus, Yuna's
Guardian` `{G}{W}{U}`. That is a real purchase, not a rounding error. Don't plan on it.

### Peace Offering (Ms. Bumbleflower) — still a deck

**48 of its 100 cards are untouched by the merge.** It keeps its commander (`Ms. Bumbleflower`
`{1}{G}{W}{U}` is not in the merged 100), and it keeps its entire identity: `Psychosis Crawler`,
`Body of Knowledge`, `Twenty-Toed Toad`, `Triskaidekaphile`, `Wizard Class`, `Kwain`, `Jolly
Gerbils`, `Jolrael`, `Secret Rendezvous`, `Tenuous Truce`, `Tempt with Bunnies`, `Tempt with
Discovery`, `Intellectual Offering`, `Sphinx of Enlightenment`, `Mr. Foxglove`, `Coveted Jewel`,
`Ghirapur Orrery`, `Rites of Flourishing`, `Fisher's Talent`, `Communal Brewing`, `Selvala`,
`Tamiyo, Field Researcher`, `Spore Frog`, `Riot Control`, `Perplexing Test`, `Illusionist's Gambit`,
`Perch Protection`, `Realm-Cloaked Giant // Cast Off`, `Mangara, the Diplomat`, `Long River's Pull`,
`Wear Down`, `Peerless Recycling`, `Hoofprints of the Stag`, `Bloodroot Apothecary`,
`Coiling Oracle`, `Octomancer`, `Martial Impetus`, `Thought Vessel` and its own lands.

**What it actually loses: 19 cards** (Checklist B) **plus 4 basics.** It ends up around 77 cards.
Because you pulled all 21 shared cards from the Counter Blitz box instead, it keeps its own
`Sol Ring`, `Arcane Signet`, `Command Tower`, `Farseek`, `Forgotten Ancient`, `Sunscorch Regent`,
`Chasm Skulker`, `Promise of Loyalty`, `An Offer You Can't Refuse` and 13 of its lands.

**To make it whole again** you need 23 cards, and the cheapest honest fix is:
- **Lands (4 + 4 basics = 8 slots):** it loses `Adarkar Wastes`, `Razorverge Thicket`,
  `Seachrome Coast`, `Yavimaya Coast` and 4 basics. Replace all eight with **basic lands** — you
  almost certainly have spares, they cost nothing, and a slightly worse mana base is the least
  painful compromise for a slow Bracket 2 deck. That closes 8 of the 23.
- **The other 15** are real cards (`Kalonian Hydra`, `Swords to Plowshares`, `Generous Gift`,
  `Cultivate`, `Simic Ascendancy`, `Rishkar`, `Managorger Hydra`, `Faeburrow Elder`, `Baird`,
  `Loran`, `Steelburr Champion`, `Broken Wings`, `Fellwar Stone`, `Mind Stone`, `Swiftfoot Boots`).
  Any 15 reasonable Bant cards fill those slots. If you have a `Scrappy Survivors` box, its white and
  green cards are legal here as long as each one's colour identity is inside `WUG` — check with
  `./bin/mtg card "<name>"` and look at the `Color identity` line.

**Simplest read:** build the merged deck, keep Peace Offering as your second deck with basics
plugging the land holes, and treat Counter Blitz as retired into the merge.

---

## 11. Verification (run programmatically, output pasted verbatim)

Every check below was run over the final 100 against the local database and the `mtg merge` output.

```
==========================================================================
MERGED BANT — VERIFICATION
==========================================================================
(a) COUNT
   commander            : 1
   nonland spells       : 63
   nonbasic lands       : 23
   basic lands          : 13 {'Forest': 5, 'Plains': 4, 'Island': 4}
   total lands          : 36
   TOTAL                : 100
   -> exactly 100  PASS

(b) COLOR IDENTITY subset of Tidus WUG
   violations: none  PASS

(c) EVERY CARD PRESENT IN THE MERGED POOL from `mtg merge`
   not in merge pool: none  PASS

(d) NO NON-BASIC APPEARS TWICE
   duplicate non-basics: none  PASS
   basics in the singleton section: none  PASS

(e) COMMANDER-LEGAL
   not commander-legal: none  PASS

(f) GAME CHANGERS in the final 100 (53-card list, data/brackets.json)
   found: NONE  -> Bracket 2 ceiling on this signal

(g) MANA MATH
   avg mana value of the 63 non-lands: 2.90
   curve: 0:1 1:6 2:18 3:20 4:11 5:6 7:1
   colored pips  W:32 U:15 G:31
   colored sources (excl. Exotic Orchard's variable output)  W:18 U:17 G:18
   always tapped (4): Seaside Citadel, Temple of Plenty, Temple of Mystery, Temple of Enlightenment
   conditionally tapped (10): Glacial Fortress, Hinterland Harbor, Sunpetal Grove, Fortified
       Village, Port Town, Vineglimmer Snarl, Razorverge Thicket, Seachrome Coast, Canopy Vista,
       Prairie Stream
   tapped share: 14/36 = 39%

(h) CUT LIST — pool cards not in the final 100
   pool unique names: 157  used: 90  cut: 67

(i) PHYSICAL BUILD — which box each card comes from
   from tidus box only      : 47
   from bumbleflower only   : 19
   available in BOTH boxes  : 24  (21 non-basic + Forest/Plains/Island)
```

(Note on **(i)**: the 47 "from tidus box only" **includes Tidus himself**. That is why Checklist A in
§6 is "the commander + 46 cards" and why §10 counts 1 + 46 + 21 + 9 = 77 cards leaving that box —
do not add the commander to the 47 a second time.)

**Source of the merged pool** (`./bin/mtg merge tidus bumbleflower --commander "Tidus, Yuna's
Guardian" --json`), run this session:

```
pool                    : 156 cards
legal                   : 156
illegal                 : 0
in_both                 : 28
copies_available        : 174
legal_copies_available  : 174
slots_to_fill           : 99
```

(The merge tool's 156 excludes the commander itself; my 157 "pool unique names" counts both
commanders as pool entries. 156 + Tidus = 157. `in_both` is 28 there and 24 in my build because
exactly four cards that exist in both boxes did not make the final 100 — all four are lands:
`Evolving Wilds`, `Overflowing Basin`, `Skycloud Expanse` and `Sungrass Prairie`. See §4e.)

---

## 12. One-screen pilot summary

```
MULL   Keep 2-5 lands (79% of sevens), with green or white, something to cast on
       turn 2-3, and at least one creature. Your FIRST mulligan in Commander is
       free — you bottom nothing (CR 103.5c). Take it. Full checklist in §7.

T1-3   Land every turn. Sol Ring / Hardened Scales / Arcane Signet / Sphere Grid /
       Shelinda / Gyre Sage / Incubation Druid. Get ONE creature with a counter down.
       Play your tapped lands on turns you weren't spending all your mana.

T4-6   Cast Tidus only when he immediately does something — you need a creature that
       already has a counter plus a second creature. Deploy Maester Seymour, Tromell,
       Rikku, Managorger Hydra, Forgotten Ancient, Wakka, Baird.
       Every combat: stack your beginning-of-combat triggers → Seymour's counters first,
       then Tidus moves a counter onto Wakka (guarantees Blitzball Captain) or onto your
       attacker (Rikku makes it unblockable). Attack the least-defended player.

T7+    Find the alpha strike. Kalonian Hydra attacking doubles every counter you own.
       Chocobo Knights gives everything with a counter double strike.
       Damning Verdict clears blockers without touching your team.
       Or just count Simic Ascendancy's growth counters and win at your upkeep.

HOLD   Inspiring Call when you fear a board wipe (draw + indestructible).
       Swords to Plowshares / Path to Exile / Generous Gift / An Offer You Can't Refuse
       are your instant-speed answers. You have seven. Don't plan around holding more.

NEVER  Cast Tidus into an empty board. Proliferate without checking whether your Sagas
       are one lore counter from sacrificing themselves (CR 714.4) — Ixion dying gives
       back the creature it exiled. Cast Damning Verdict before checking that every
       creature you own has a counter on it. Full list of traps in §8.
```

---

*All card names, mana costs, type lines, power/toughness and quoted rules text in this document were
retrieved from the local MTG Brain database during the session that wrote it. Rules citations are
Comprehensive Rules numbers retrieved with `mtg rule`. Re-verify anything with
`./bin/mtg card "<name>"`.*
