# Counter Blitz — Tidus, Yuna's Guardian

**Format:** Commander (EDH) only — 100 cards, singleton, no sideboard.
**Colors:** Bant (Green / White / Blue — `WUG`)
**Deck slug:** `tidus` · **Set:** FIC (FINAL FANTASY Commander), released 2025-06-13
**Estimated bracket:** 3 (Upgraded)

> Everything in this document was pulled from the local card database this session.
> If you want to re-check any card while reading, run `./bin/mtg card "<name>"`.
> If you hit a word you don't know, run `./bin/mtg glossary <term>`.

---

## 1. What this deck is trying to do

This is a **+1/+1 counter combat deck**. You put small permanent "power boosters" called
**+1/+1 counters** on your creatures (a +1/+1 counter makes a creature 1 bigger in both power
and toughness, permanently, for as long as the counter stays on it), you attack with those
creatures, and connecting with them draws you cards and puts *more* counters out.

The deck has no two-card "I win" combination it can assemble (players call that **comboing off**),
and it has no cards that point damage straight at a player's face (players call that **burn**). It
builds a board of medium creatures, grows them past what the table can block profitably, and then
converts that into card advantage and eventually a lethal attack. **Its two real engines are (a) creatures with
counters dealing combat damage to a player, and (b) proliferate** — a keyword action that means
"choose any number of permanents and/or players that have a counter, then give each one
additional counter of each kind that it already has" (Comprehensive Rules **701.34a**;
`./bin/mtg glossary proliferate`).

The deck's single biggest asymmetry is that **your creatures have counters and your opponents'
usually do not.** That is why the list runs `Damning Verdict` ({3}{W}{W}, Sorcery): *"Destroy all
creatures with no counters on them."* You blow up the table and keep your entire board.

Honest framing: this deck is a **fair, grinding, mid-speed deck** — in player shorthand, a
**grindy midrange** deck. Those three words each mean something specific:

- **Fair** — it wins by casting creatures and attacking, the way the game is designed to be played,
  rather than by exploiting a loop or a shortcut.
- **Grindy** — it wins slowly, by accumulating more resources than the table until they run out of
  answers. Its games go long.
- **Midrange** — the middle of the three speed archetypes. An **aggro** deck races to kill you
  early with cheap creatures; a **control** deck answers everything and wins at its leisure;
  **midrange** does neither, deploying efficient medium-sized threats and out-valuing both.

The role-scoring tool literally reports `wincon 0` and `tutor 0` — there is no card in here that
just says "you win," and no card that searches your library for a specific nonland card. You win by
attacking, repeatedly, with a board that got too big.

---

## 2. Your commander

### Tidus, Yuna's Guardian — {G}{W}{U} — Legendary Creature — Human Warrior — 3/3

Exact text from the database:

```
At the beginning of combat on your turn, you may move a counter from target
creature you control onto a second target creature you control.

Cheer — Whenever one or more creatures you control with counters on them
deal combat damage to a player, you may draw a card and proliferate. Do this
only once each turn.
```

**Mana cost:** {G}{W}{U} — three mana, one of each of your three colors. Mana value 3.

### What it actually means in play

**Ability 1 — the counter shuffle.** Every turn, for free, at "the beginning of combat on your
turn" (the step right after your main phase, before you declare attackers — see CR **507**), you
may pick up **one counter** from one of your creatures and drop it on another of your creatures.

Three things beginners miss here:

- It says **"a counter"**, not "a +1/+1 counter." Any kind of counter is legal: shield counters,
  flying counters, vow counters, lore counters on your Saga creatures. Both targets must be
  **creatures you control**.
- It is a **move**, and a move is two events. Per the official ruling on this card
  (2025-06-06): *"To move a counter from one permanent to another, the counter is removed from
  the first permanent and put on the second. Any abilities that care about a counter being
  removed from or put onto a permanent will apply."* This is the whole reason the ability is
  good — see the Rikku and Wakka entries in §6.
- **It does nothing on an empty board.** You need a creature that already has a counter, and a
  second creature to move it to. Tidus himself enters with no counters.

**Ability 2 — "Cheer".** When your creatures that have counters on them hit an *opponent*
(a player — not a creature) with combat damage, you draw a card and proliferate. Note the
restriction: **"Do this only once each turn."** If you attack with six countered creatures and
four get through, you still only draw one and proliferate once. That is fine — the proliferate
adds a counter to *every* countered permanent you choose, so one trigger already pumps your
whole team.

Also note it says **"creatures you control with counters on them"** — again, *any* counters.
Your four Saga creatures (`Summon: Ixion`, `Summon: Yojimbo`, `Summon: Valefor`,
`Summon: Magus Sisters`) naturally carry **lore counters**, so they turn on Cheer just by
existing and attacking.

> **What a Saga is** (CR **714**; `./bin/mtg glossary saga` — *"An enchantment subtype. Sagas have
> a number of chapter abilities that take effect over a number of turns to tell a story."*). A Saga
> tracks its progress with **lore counters** (CR 714.3). It enters with one lore counter on it
> (CR 714.3a), and you add another as each of your precombat main phases begins (CR 714.3c — the
> card's own reminder text words this as *"after your draw step,"* which is the same moment). Each
> Roman-numeral **chapter ability** is a triggered ability that fires when the lore counters reach
> that number (CR 714.2b), and once the counters reach the Saga's final chapter number you
> **sacrifice it** (CR 714.4). All four `Summon:` cards above are **Enchantment Creature — Saga**,
> so they are creatures *and* Sagas: they attack, they block, and they have a lore counter on them
> from the moment they hit the battlefield. That last part is why they switch Cheer on for free.
> (Their reminder text spells out the ending: `Summon: Ixion` says *"Sacrifice after III,"*
> `Summon: Yojimbo` says *"Sacrifice after IV."*)

### The cost if it dies — commander tax

Your commander starts in a special zone called the **command zone** and you may cast it from
there. If it dies, you may put it back in the command zone instead of leaving it in the
graveyard — CR **903.9a**: *"If a commander is in a graveyard or in exile and that object was put
into that zone since the last time state-based actions were checked, its owner may put it into
the command zone."* Same for going to hand or library (903.9b).

But recasting is not free. CR **903.8**:

> A player may cast a commander they own from the command zone. A commander cast from the
> command zone costs an additional {2} for each previous time the player casting it has cast it
> from the command zone that game. This additional cost is informally known as the "commander
> tax."

So Tidus costs {G}{W}{U} the first time, **{2}{G}{W}{U} (5 mana)** the second time,
**{4}{G}{W}{U} (7 mana)** the third. Budget for this.

### Cast early or hold?

**Hold him until you have a board.** This is the opposite of most 3-mana commanders. Tidus on
turn 3 with nothing else out does literally nothing — both of his abilities require creatures
that already have counters. He is also a 3/3 for 3 with no protection, so casting him into an
open table just invites someone to kill him and start the tax clock.

**The right turn to cast Tidus is the turn he immediately generates value** — usually turn 4-6,
once you already control two or more creatures and at least one of them has a counter. If you
have a counter-producer like `Shelinda, Yevon Acolyte` ({G}{W}) or `Duskshell Crawler` ({1}{G})
already down, Tidus becomes live the moment he resolves.

**Commander damage note:** CR **903.10a** — *"A player who's been dealt 21 or more combat damage
by the same commander over the course of the game loses the game."* Tidus is a 3/3 with no
evasion. Killing someone with 21 Tidus damage is possible if you stack counters onto him, but it
is not a plan — treat it as a bonus, not a route.

---

## 3. The turn-by-turn shape

### The mana reality you are playing around

From `mtg deck stats tidus -v`:

- **37 lands**, average mana value of the 62 nonland cards is **3.03**. The tool grades the land
  count "SANE" — 37 lands is exactly right for this curve.
- **16 of the 37 lands can enter tapped (43%)** — 8 always, 8 conditionally.
- Curve: `0→2 · 1→5 · 2→17 · 3→16 · 4→13 · 5→6 · 6→2 · 7+→1`. The deck is heaviest at 2 and 3.
- Color sources: White 20, Blue 19, Green 20 (`Command Tower`, `Exotic Orchard`, `Path of
  Ancestry` count for all three).

Because nearly half your lands enter tapped, **land sequencing is a real skill in this deck.**
Play your tapped lands on turns where you weren't going to spend all your mana anyway.

### Turns 1-3 — set up mana, land a counter-producer

**What good looks like:** two or three lands, and by turn 2-3 a cheap creature or enchantment
that starts making counters.

The cards you most want to see here (all 1-2 mana, verified):

| Card | Cost | Why it's a great turn 1-3 play |
|---|---|---|
| `Sol Ring` | {1} | Artifact. *"{T}: Add {C}{C}."* Two colorless mana from a one-mana rock. Always cast it turn 1 if you have it. |
| `Hardened Scales` | {G} | Enchantment. *"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1 counters are put on it instead."* Upgrades every single counter effect in the deck for one mana. |
| `Shelinda, Yevon Acolyte` | {G}{W} | 2/2 Lifelink. *"Whenever another creature you control enters, put a +1/+1 counter on that creature if its power is less than Shelinda's power. Otherwise, put a +1/+1 counter on Shelinda."* A counter on essentially every creature you play. |
| `Sphere Grid` | {1}{G} | Enchantment. *"Whenever a creature you control deals combat damage to a player, put a +1/+1 counter on that creature. Unlock Ability — Creatures you control with +1/+1 counters on them have reach and trample."* |
| `Duskshell Crawler` | {1}{G} | 0/3. *"When this creature enters, put a +1/+1 counter on target creature. Each creature you control with a +1/+1 counter on it has trample."* |
| `Gyre Sage` | {1}{G} | 1/2 with Evolve. *"{T}: Add {G} for each +1/+1 counter on this creature."* Ramp that scales with your theme. |
| `Incubation Druid` | {1}{G} | 0/2. *"{T}: Add one mana of any type that a land you control could produce. If this creature has a +1/+1 counter on it, add three mana of that type instead."* One counter turns it into a 3-mana land. |
| `Farseek` / `Three Visits` | {1}{G} each | Sorceries that fetch a land onto the battlefield. `Three Visits` fetches a **Forest card** untapped; `Farseek` fetches a *"Plains, Island, Swamp, or Mountain"* **tapped**. |
| `Arcane Signet` | {2} | *"{T}: Add one mana of any color in your commander's color identity."* Perfect fixing for a three-color deck. |

**"Evolve"** on `Gyre Sage` and `Fathom Mage` means: *"Whenever a creature you control enters, if
that creature has greater power or toughness than this creature, put a +1/+1 counter on this
creature."* (`./bin/mtg glossary evolve`.)

**If turns 1-3 go badly** (you're on two lands, no green source, nothing to cast): do not panic and
dump your whole hand out for no reason. Prioritize hitting land drops, cast `Everflowing Chalice`
for whatever you can afford, and use `Ash Barrens` — *"Basic landcycling {1} ({1}, Discard this
card: Search your library for a basic land card, reveal it, put it into your hand, then shuffle.)"*
— to fix the color you're missing.

**`Everflowing Chalice` costs `{0}` and has "Multikicker {2}."** From the card: *"Multikicker {2}
(You may pay an additional {2} any number of times as you cast this spell.) This artifact enters
with a charge counter on it for each time it was kicked. {T}: Add {C} for each charge counter on
this artifact."* **Kicker** is an optional extra cost you choose to pay as you cast a spell to get
more out of it; **multikicker** means you may pay it as many times as you like. So Chalice for {0}
is a blank artifact that taps for nothing; for {2} it taps for {C}; for {4} it taps for {C}{C}.
Official ruling (2021-03-19): *"You can cast Everflowing Chalice without kicking it at all if you
wish. However, if Everflowing Chalice has no charge counters on it, activating its last ability
won't produce any mana."* Pay for at least one counter unless you have a reason not to.

### Turns 4-6 — deploy the engine, cast Tidus, start connecting

This is the deck's real gear. You want two or three creatures out, counters on them, Tidus in
play, and you want to start attacking the **least defended player** so Cheer turns on.

Cards you're aiming to resolve in this window:

- `Maester Seymour` ({2}{G}, 1/3) — *"At the beginning of combat on your turn, put a number of
  +1/+1 counters equal to Maester Seymour's power on another target creature you control."*
  Starts at 1 counter/turn but compounds fast, because counters you put on *him* raise his power.
- `Tromell, Seymour's Butler` ({2}{G}, 2/3) — *"Each other nontoken creature you control enters
  with an additional +1/+1 counter on it."* Every creature after this arrives pre-loaded.
- `Rikku, Resourceful Guardian` ({2}{U}, 2/3) — turns counters into unblockable damage (see §6).
- `Bred for the Hunt` ({1}{G}{U}) — *"Whenever a creature you control with a +1/+1 counter on it
  deals combat damage to a player, you may draw a card."* Unlike Cheer, this triggers **per
  creature**, so a wide attack draws multiple cards.
- `Wakka, Devoted Guardian` ({2}{G}{W}, 4/4 reach trample) — your best turn-4 body.
- `Chocobo Knights` ({3}{W}, 3/3) — *"Whenever you attack, creatures you control with counters on
  them gain double strike until end of turn."* This is the card that turns a board into lethal.

**A key habit to build now:** each turn, at the beginning of combat, you get *three* separate
"beginning of combat" triggers if you have Tidus + Maester Seymour + `Fight Rigging`. You control
the order they go on the stack — and **the stack resolves last-in-first-out, so whichever trigger
you put on the stack LAST is the one that resolves FIRST.** Work backwards from the order you want
things to happen in. Sequence them so the counters land where you want *before* you declare
attackers. (Worked example in §7, Mistake 7.)

**If turns 4-6 go badly** (someone wiped your board, or you're stuck on lands): this deck is
resilient here in a way most aggro decks aren't. `Yuna, Grand Summoner` ({1}{G}{W}{U}, 1/5) —
*"Whenever another permanent you control is put into a graveyard from the battlefield, if it had
one or more counters on it, you may put that number of +1/+1 counters on target creature"* —
recovers counters from a wipe. So does `Resourceful Defense` ({2}{W}). And
`Luminous Broodmoth` ({2}{W}{W}, 3/4 flying) — *"Whenever a creature you control without flying
dies, return it to the battlefield under its owner's control with a flying counter on it"* —
makes a board wipe a temporary inconvenience *and* the returned creatures come back **with a
counter on them**, which turns Cheer back on immediately.

### Turns 7+ — convert to a kill

By now a normal Bracket 3 game is deciding itself. Your job is to find the turn where the whole
team swings and someone dies.

The pieces that end games:

- **`Chocobo Knights` + a wide board.** Double strike means the creature deals its combat damage
  twice (CR **702.4b** — first-strike damage step, then a second combat damage step). Every
  creature with a counter effectively doubles.
- **`Maester Seymour`'s monstrosity:** *"{3}{G}{G}: Monstrosity X, where X is the number of
  counters among creatures you control."*
  **Monstrosity X is a keyword action, and it is the thing that makes him a finisher: it puts X
  +1/+1 counters on the creature and the creature becomes *monstrous*** (CR **701.37a** —
  *"'Monstrosity N' means 'If this permanent isn't monstrous, put N +1/+1 counters on it and it
  becomes monstrous'"*; `./bin/mtg glossary monstrosity`). The card even prints the reminder text:
  *"(If this creature isn't monstrous, put X +1/+1 counters on it and it becomes monstrous.)"*
  **"Monstrous" is not an ability — it is just a flag** meaning this permanent has already done
  this once (CR 701.37b), which is exactly why he can only go monstrous once. Ruling (2025-06-06):
  *"The value of X is determined only once, as Maester Seymour's last ability resolves."* Late game
  with 12+ counters on board, one activation turns a 1/3 into a 13/15 or bigger.
- **`Sin, Unending Cataclysm`** ({5}{G}{U}, 5/5 flying trample) — *"As Sin enters, remove all
  counters from any number of artifacts, creatures, and enchantments. Sin enters with X +1/+1
  counters on it, where X is twice the number of counters removed this way."* Vacuum up your own
  board and get double back. A 5/5 flier that becomes a 20/20+ flier ends a player quickly.
- **`Blitzball Stadium`** ({X}{U}) — *"Go for the Goal! — {3}, {T}: Until end of turn, target
  creature gains 'Whenever this creature deals combat damage to a player, draw a card for each
  kind of counter on it' and it can't be blocked this turn."* Guaranteed damage through, plus
  cards.
- **`Damning Verdict`** ({3}{W}{W}) as the *setup* for the kill: clear every blocker at the table
  that lacks a counter, then attack into nothing.

**If turns 7+ go badly:** you have four board wipes (`Farewell`, `Damning Verdict`,
`Promise of Loyalty`, `Bane of Progress`) and they are not symmetric in the same way.
`Damning Verdict` favors you heavily. `Promise of Loyalty` ({4}{W}, *"Each player puts a vow
counter on a creature they control and sacrifices the rest"*) leaves everyone one creature —
and yours keeps its counters, plus a **vow counter**, which keeps Cheer live. `Farewell`
({4}{W}{W}) is the nuclear option and it **exiles your stuff too** — only cast it when you're
behind.

---

## 4. How you actually win

**You win by attacking.** That is the honest answer. There is no alternate win condition, no
infinite combo detected, no "deal 20 damage from nowhere" card in the list.

The clock is **medium, not fast**. (A deck's **clock** is how many turns it needs to kill somebody
once it gets going — a "fast clock" kills in two or three attacks, a slow one takes many. Not a
rules term; it's how players talk.) Bracket 3 guidance from the tool says games "typically end
around turn 7 or later," and that matches this deck: you're realistically killing your first
opponent somewhere around turn 8-11 in a four-player pod.

The concrete finishers, all verified this session:

1. **`Chocobo Knights` ({3}{W}, 3/3)** — *"Whenever you attack, creatures you control with
   counters on them gain double strike until end of turn."* This is your single best "the game
   ends now" card. Six creatures with counters becomes twelve attacks worth of damage.
2. **`Maester Seymour` ({2}{G}, 1/3)** monstrosity — one activation of {3}{G}{G} puts X +1/+1
   counters on him, where X is every counter on your creatures (CR 701.37a; see §3), converting
   your whole board's counter count into a single huge threat.
3. **`Sin, Unending Cataclysm` ({5}{G}{U}, 5/5 flying, trample)** — the biggest single body you
   can build, and it flies, so blockers mostly don't matter.
4. **`Wakka, Devoted Guardian` ({2}{G}{W}, 4/4 reach, trample)** — *"Blitzball Captain — At the
   beginning of your end step, if a counter was put on Wakka this turn, put a +1/+1 counter on
   each other creature you control."* This is a team-wide pump **every turn**, which is what
   actually turns a stalled board into lethal.
5. **`Walking Ballista` ({X}{X}, 0/0 Artifact Creature)** — *"Remove a +1/+1 counter from this
   creature: It deals 1 damage to any target."* Your only way to deal damage without attacking.
   It's a mana sink and a way to finish a player at 3 life through a wall of blockers. Note the
   cost: *"A casting cost of {X}{X} means that you pay twice X. If you want X to be 3, you pay
   {6}"* (official ruling).
6. **Evasion as the enabler.** Damage only matters if it connects. Your ways through:
   - `Rikku, Resourceful Guardian` — *"Whenever you put one or more counters on a creature,
     until end of turn, that creature can't be blocked by creatures your opponents control."*
   - `Duskshell Crawler` — grants trample to all your +1/+1-countered creatures. **Trample** means
     excess combat damage past the blockers hits the player (CR **702.19b**).
   - `Sphere Grid` — grants reach *and* trample to countered creatures.
   - `Blitzball Stadium` — makes one creature unblockable for a turn.
   - Fliers: `Grateful Apparition`, `Lord Jyscal Guado`, `Luminous Broodmoth`,
     `Sunscorch Regent`, `Summon: Valefor`, `Sin, Unending Cataclysm`.

**What you are NOT:** you are not a deck that kills on turn 4, and you are not a deck that can
race a combo deck. If the table has a fast combo player, your removal (`Path to Exile`,
`Destroy Evil`, `Endless Detour`, `An Offer You Can't Refuse`) is the only brake you have — see
§7.

---

## 5. What to mulligan for

### The 10-second checklist

Look at your seven cards and ask, in this order:

1. **How many lands? Two to five.** Below 2 is a mulligan almost always. Six or seven lands is
   also a mulligan (you'll flood out). **Flooding out** = drawing far more lands than spells, so
   you have plenty of mana and nothing left to spend it on; the opposite is being **screwed** —
   spells in hand and no lands to cast them with. Neither word is official rules vocabulary, it's
   just how players talk.
2. **Can I cast something on turn 2 or turn 3?** You have 5 one-drops and 17 two-drops, so a
   normal keep should contain a play by turn 3.
3. **Do I have green?** Green is your densest color (47 cards carry green; `Hardened Scales`,
   `Sphere Grid`, `Maester Seymour`, `Farseek`, `Three Visits`, `Gyre Sage`, `Incubation Druid`
   are all green). A hand with three white lands and no green source is worse than it looks.
4. **Is there a way to make a counter?** You do not need Tidus in your opener — you need
   *something that makes counters* so Tidus is live when he arrives.

**Mulligan rule reminder** (CR **103.5** and CR **103.5c**): a mulligan means shuffling your hand
back into your library, drawing a new seven, then **putting a number of cards equal to how many
mulligans you've taken on the bottom of your library.**

But Commander is a multiplayer game, and CR **103.5c** says: *"In a multiplayer game and in any
Brawl game, the first mulligan a player takes doesn't count toward the number of cards that player
will put on the bottom of their library or the number of mulligans that player may take. Subsequent
mulligans are counted toward these numbers as normal."*

**So your first mulligan is a completely free fresh seven — you bottom nothing.** Only from the
second mulligan on do you start paying: mull #2 = draw 7, bottom 1; mull #3 = draw 7, bottom 2.
Take the first one freely — a hand that fails the checklist above is never worth keeping when the
re-draw costs you zero cards.

### Real hands, generated this session

**Seed 42 → KEEP (the tool agrees, and so do I)**

```
  Sin, Unending Cataclysm          {5}{G}{U}           7  Legendary Creature
  Port Town                        —                   0  Land
  Tireless Tracker                 {2}{G}              3  Creature
  Canopy Vista                     —                   0  Land
  Generous Patron                  {2}{G}              3  Creature
  Forest                           —                   0  Basic Land
  An Offer You Can't Refuse        {U}                 1  Instant
```

3 lands, green available, a turn-3 play (`Tireless Tracker` or `Generous Patron`), and a piece of
interaction. **Keep.** But study what actually happened: the simulation drew **zero more lands
until turn 8**, and the hand ballooned to 11 cards while stuck on 3 lands. This is the honest
lesson — a "keep" is a probability bet, not a promise. Note also there's **no ramp** in this hand
at 3 mana or less, which is what made the flood-out so punishing.

**Seed 7 → MULLIGAN**

```
  Gatta and Luzzu                  {2}{W}              3  Legendary Creature
  Farseek                          {1}{G}              2  Sorcery
  Lord Jyscal Guado                {1}{W}              2  Legendary Creature
  Farewell                         {4}{W}{W}           6  Sorcery
  Plains                           —                   0  Basic Land
  Resourceful Defense              {2}{W}              3  Enchantment
  Fight Rigging                    {2}{G}              3  Enchantment
```

**One land.** It is tempting — `Farseek` is right there, and the spells are good. Don't. You need
a second land *before* `Farseek` does anything, and the sim shows the punishment: nothing castable
on turn 1, and by turn 8 you have 11 cards in hand and 4 lands. **Mulligan.**

**Seed 13 → MULLIGAN (this is the trap hand)**

```
  Lulu, Stern Guardian             {2}{U}              3  Legendary Creature
  Path to Exile                    {W}                 1  Instant
  Fight Rigging                    {2}{G}              3  Enchantment
  Sol Ring                         {1}                 1  Artifact
  Forest                           —                   0  Basic Land
  Bane of Progress                 {4}{G}{G}           6  Creature
  Summon: Valefor                  {4}{U}              5  Enchantment Creature
```

`Sol Ring` makes this look keepable and it is still **one land**. `Sol Ring` needs a land to cast
off. This particular sim got bailed out by drawing five lands across its first seven draw steps —
you will not always be that lucky. **Mulligan.** The rule holds: `Sol Ring` does not count as your
second land.

**Seed 99 → KEEP**

```
  Together Forever                 {W}{W}              2  Enchantment
  Destroy Evil                     {1}{W}              2  Instant
  Maester Seymour                  {2}{G}              3  Legendary Creature
  Exotic Orchard                   —                   0  Land
  Everflowing Chalice              {0}                 0  Artifact
  Plains                           —                   0  Basic Land
  Summon: Magus Sisters            {4}{G}              5  Enchantment Creature
```

Only 2 lands, but: a **0-mana ramp card** (`Everflowing Chalice`), a 2-drop, a 3-drop that is a
genuine engine (`Maester Seymour`), and removal. The average cost of the hand is 2.4. This is the
shape you want. **Keep.**

**Seed 3 → KEEP, with a warning**

```
  Auron, Venerated Guardian        {3}{W}              4  Legendary Creature
  Plains                           —                   0  Basic Land
  Chocobo Knights                  {3}{W}              4  Creature
  Destroy Evil                     {1}{W}              2  Instant
  Prairie Stream                   —                   0  Land
  Altered Ego                      {X}{2}{G}{U}        4  Creature
  Idyllic Beachfront               —                   0  Land
```

3 lands, so the tool says keep — but look at the colors. All three lands make **White and Blue
only**. The sim confirms the danger: nothing castable on turn 1, and **green never arrived through
turn 8** — the run stalls on 4 lands `[W,U]` from turn 4 onward with 11 cards in hand, and both
`Altered Ego` and the `Bred for the Hunt` drawn on turn 7 sit dead. This is a **marginal keep** —
it works only because `Destroy Evil`, `Auron, Venerated Guardian`, and `Chocobo Knights` are all
castable off White.
If this hand's spells were green-heavy instead, the same three lands would make it a mulligan.
**Check colors, not just land count.**

**Seed 21 → MULLIGAN**

```
  Endless Detour                   {G}{W}{U}           3  Instant
  Walking Ballista                 {X}{X}              0  Artifact Creature
  Incubation Druid                 {1}{G}              2  Creature
  Together Forever                 {W}{W}              2  Enchantment
  Blitzball Stadium                {X}{U}              1  Artifact
  Yuna's Decision                  {3}{G}              4  Sorcery
  Idyllic Beachfront               —                   0  Land
```

Beautifully cheap (average cost 2.0) and it is **one land**. `Walking Ballista` at X=0 dies
immediately as a 0/0 and `Blitzball Stadium` at X=0 does nothing. **Mulligan.**

---

## 6. The 8-10 cards that matter most

Ranked by how much they change the game.

### 1. `Hardened Scales` — {G} — Enchantment

> *"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1
> counters are put on it instead."*

**Why:** it upgrades every counter effect in the deck for one mana, including creatures entering
with counters — official ruling: *"If a creature you control would enter the battlefield with a
number of +1/+1 counters on it, it enters with that many plus one instead."* EDHREC has it in
**89.1% of 19,181 Tidus decks**, the highest inclusion rate of any synergy card. Play it turn 1
whenever you can.

### 2. `Sphere Grid` — {1}{G} — Enchantment

> *"Whenever a creature you control deals combat damage to a player, put a +1/+1 counter on that
> creature.*
> *Unlock Ability — Creatures you control with +1/+1 counters on them have reach and trample."*

**Why:** it is a counter engine *and* an evasion engine in one two-mana card. **Trample** means
excess damage past blockers goes to the player (CR 702.19b); **reach** lets the creature block
fliers. One ruling to know (2025-06-06): once a creature has blocked using Sphere Grid's reach,
removing its counters later *"won't cause that creature to stop blocking."*

### 3. `Rikku, Resourceful Guardian` — {2}{U} — 2/3 Legendary Creature — Human Artificer

> *"Whenever you put one or more counters on a creature, until end of turn, that creature can't be
> blocked by creatures your opponents control.*
> *Steal — {1}, {T}: Move a counter from target creature an opponent controls onto target creature
> you control. Activate only as a sorcery."*

**Why:** this is the card that makes Tidus's move ability into a weapon. Because moving a counter
counts as *putting* a counter on the destination creature (Tidus ruling, 2025-06-06), **Tidus's
beginning-of-combat move makes the receiving creature unblockable that turn.** Free, every turn.
Note the limit (Rikku ruling): *"Once a creature has been blocked, Rikku's first ability won't
cause it to become unblocked"* — you must do this **before** blockers are declared, which is
exactly when Tidus's trigger happens.

### 4. `Wakka, Devoted Guardian` — {2}{G}{W} — 4/4 Legendary Creature — Human Warrior

> *"Reach, trample*
> *Whenever Wakka deals combat damage to a player, destroy up to one target artifact that player
> controls and put a +1/+1 counter on Wakka.*
> *Blitzball Captain — At the beginning of your end step, if a counter was put on Wakka this turn,
> put a +1/+1 counter on each other creature you control."*

**Why:** the Blitzball Captain trigger is a free team-wide pump every single turn — but only *"if
a counter was put on Wakka this turn."* Official ruling: *"Once your end step begins, it's too
late to put a counter on Wakka in order to cause this ability to trigger."*
**So: use Tidus's beginning-of-combat move to put a counter on Wakka every turn.** That guarantees
Blitzball Captain fires even on turns you don't attack. This is the deck's most reliable engine
loop.

### 5. `Maester Seymour` — {2}{G} — 1/3 Legendary Creature — Human Elf Cleric

> *"At the beginning of combat on your turn, put a number of +1/+1 counters equal to Maester
> Seymour's power on another target creature you control.*
> *{3}{G}{G}: Monstrosity X, where X is the number of counters among creatures you control.
> (If this creature isn't monstrous, put X +1/+1 counters on it and it becomes monstrous.)"*

**Why:** free counters every turn that scale with his own power, plus a late-game finisher button.
**Monstrosity X** = put X +1/+1 counters on this creature and it becomes *monstrous* (CR 701.37a;
`./bin/mtg glossary monstrosity`), and *monstrous* is only a marker recording that it already
happened (CR 701.37b) — which is why it is once-only. Two rulings to know: X for monstrosity *"is
determined only once, as Maester Seymour's last ability resolves,"* and *"Once a creature becomes
monstrous, it can't become monstrous again."*
Save the monstrosity for the turn you're attacking for lethal.

### 6. `Damning Verdict` — {3}{W}{W} — Sorcery

> *"Destroy all creatures with no counters on them."*

**Why:** a one-sided board wipe. Your creatures have counters; almost nobody else's do. This is
the card you hold when the table is ahead of you on board. **EDHREC: 85.8% of Tidus decks.**
Before you cast it, take one second to check that every creature you care about actually has a
counter — a fresh `Chocobo Knights` with no counter will die to your own spell.

### 7. `Chocobo Knights` — {3}{W} — 3/3 Creature — Human Knight

> *"Whenever you attack, creatures you control with counters on them gain double strike until end
> of turn."*

**Why:** double strike means the creature deals its combat damage **twice** (CR 702.4b). This
doubles your whole board's damage output in one card. It is your most common "and that's the
game" card. The database has **no official rulings** for this card yet — the text is the whole
story.

### 8. `Inexorable Tide` — {3}{U}{U} — Enchantment

> *"Whenever you cast a spell, proliferate."*

**Why:** every spell you cast — including lands? No: **spells**, so not lands — adds a counter to
every countered permanent you choose. In a deck averaging 3.03 mana value, you cast 1-3 spells a
turn, which is 1-3 free team-wide pumps. Ruling (2011-01-01): *"Whenever you cast a spell,
Inexorable Tide's ability triggers and goes on the stack on top of it. It will resolve (and you'll
proliferate) before the spell resolves."*

### 9. `Inspiring Call` — {2}{G} — Instant

> *"Draw a card for each creature you control with a +1/+1 counter on it. Those creatures gain
> indestructible until end of turn."*

**Why:** this is your best card in the deck and it does two jobs — it refills your hand *and* it
blanks an opposing board wipe. **Indestructible** means damage and "destroy" effects don't kill
it (CR 702.12). Rulings: *"Creatures you control that have +1/+1 counters put on them after
Inspiring Call resolves won't gain indestructible"* and *"Once a creature gains indestructible, it
will have it for the turn, even if it loses all its +1/+1 counters."* Hold this up whenever you
suspect a wipe. Note: indestructible does **not** stop exile or sacrifice — it won't save you from
`Farewell` or a "each player sacrifices" effect.

### 10. `Yuna, Grand Summoner` — {1}{G}{W}{U} — 1/5 Legendary Creature — Human Cleric

> *"Grand Summon — {T}: Add one mana of any color. When you next cast a creature spell this turn,
> that creature enters with two additional +1/+1 counters on it.*
> *Whenever another permanent you control is put into a graveyard from the battlefield, if it had
> one or more counters on it, you may put that number of +1/+1 counters on target creature."*

**Why:** ramp, fixing, and counter-generation on one 5-toughness body, plus insurance against
removal — ruling: *"Yuna's last ability counts all counters that were on the permanent, not just
+1/+1 counters."* Note that includes **lore counters from your Sagas** when they sacrifice
themselves, which is free value every time a Summon finishes its story.

### Also worth learning early

- **`Tromell, Seymour's Butler` ({2}{G}, 2/3)** — *"Each other nontoken creature you control
  enters with an additional +1/+1 counter on it."* Plus *"{1}, {T}: Proliferate X times, where X is
  the number of nontoken creatures you control that entered this turn."*
- **`Resourceful Defense` ({2}{W})** — *"Whenever a permanent you control leaves the battlefield,
  if it had counters on it, put those counters on target permanent you control."* Your counters
  become nearly impossible to remove permanently.
- **`Fathom Mage` ({2}{G}{U}, 1/1)** — *"Whenever a +1/+1 counter is put on this creature, you may
  draw a card."* Ruling: *"If multiple +1/+1 counters are placed on Fathom Mage simultaneously,
  its last ability will trigger once for each of those counters."* With `Hardened Scales` out,
  every counter effect on Fathom Mage draws an extra card.

---

## 7. Common mistakes with this deck

Each of these is tied to a number the deck actually has.

### Mistake 1 — Casting Tidus on turn 3 into an empty board

His move ability targets *"target creature you control"* twice, and Cheer requires creatures with
counters. With no board, Tidus is a vanilla 3/3 that eats a removal spell and starts your
commander tax (CR 903.8: +{2} per recast). **Wait until he's immediately profitable.**

### Mistake 2 — Expecting to "hold up interaction" — you basically can't

**Interaction** (the role name `mtg deck stats` uses, and player slang rather than a rules term)
means *cards you can cast in response to what an opponent is doing* — counterspells,
instant-speed removal, protection spells, fogs. It is narrower than **removal**: removal is any
answer at all, including sorceries and creatures with enter-the-battlefield abilities; interaction
specifically means answers you can deploy on somebody else's turn.

The role scan reports **interaction: 3** (`An Offer You Can't Refuse`, `Gatta and Luzzu`,
`Inspiring Call`). Counting every instant that answers something, you have exactly **four**
instant-speed answers in the whole deck:

| Card | Cost | What it answers |
|---|---|---|
| `Path to Exile` | {W} | *"Exile target creature."* (Its controller may search for a basic land.) |
| `Destroy Evil` | {1}{W} | *"Destroy target creature with toughness 4 or greater"* OR *"Destroy target enchantment."* |
| `Endless Detour` | {G}{W}{U} | *"The owner of target spell, nonland permanent, or card in a graveyard puts it on their choice of the top or bottom of their library."* |
| `An Offer You Can't Refuse` | {U} | *"Counter target **noncreature** spell. Its controller creates two Treasure tokens."* |

That is it. **The mistake is not tapping out — the mistake is *planning* around holding up
interaction you don't have.** Play proactively. Deploy your board. The one exception: if you
actually hold `Inspiring Call` or `Protection Magic` and you suspect a board wipe, leaving 2-3
mana up is correct.

### Mistake 3 — Casting `Farewell` because it's the flashy rare

`Farewell` ({4}{W}{W}) is the deck's only card flagged as a **Game Changer** — it's the single
reason the bracket estimate is 3 instead of 2. Its text: *"Choose one or more — Exile all
artifacts. / Exile all creatures. / Exile all enchantments. / Exile all graveyards."* It **exiles
your board too**, and exile bypasses `Luminous Broodmoth` and `Yuna, Grand Summoner` recovery
(those need permanents going to a *graveyard*). Cast `Damning Verdict` instead whenever the choice
exists. `Farewell` is for when you are genuinely losing.

### Mistake 4 — Playing your tapped lands on the wrong turns

**16 of 37 lands (43%) can enter tapped.** With a curve peaking at 2 and 3 mana, a tapped land on
turn 2 costs you a whole turn of development. Plan two turns ahead: if you know turn 3 is a
`Maester Seymour` turn, play the tapped land on turn 2 alongside a 1-drop, not on turn 3.
Also remember `Temple of the False God` — *"{T}: Add {C}{C}. Activate only if you control five or
more lands"* — produces **nothing** until you have five lands. It is not a turn-1 play.

### Mistake 5 — Keeping a greedy hand because there are no tutors

The role scan reports **tutor: 0**. You cannot go find your `Hardened Scales` or your
`Chocobo Knights`. That means the *shape* of your opening hand is the whole game. A 6-card hand
with 3 lands and a 2-drop beats a 7-card hand with 1 land and three bombs, every time. See §5.

### Mistake 6 — Forgetting Cheer is once per turn, but the other payoffs aren't

Tidus's Cheer says *"Do this only once each turn."* But `Bred for the Hunt` and `Sphere Grid`
trigger **per creature**. So the correct attack pattern is **wide, not tall** — five small
countered creatures connecting is five `Bred for the Hunt` draws and five `Sphere Grid` counters;
one huge creature connecting is one of each.

### Mistake 7 — Not stacking your beginning-of-combat triggers

By mid-game you can have three or four abilities that all trigger *"at the beginning of combat on
your turn"*: Tidus, `Maester Seymour`, `Fight Rigging`, `Kimahri, Valiant Guardian`.

**You choose the order they go on the stack, and the stack resolves last-in-first-out — so the
trigger you want to happen FIRST is the one you put on the stack LAST.** This inversion is where
the mistake actually lives: "resolve Seymour first" and "put Seymour on the stack first" are
*opposite* instructions, and a beginner who does the second gets the wrong play.

Common correct sequence, stated as physical actions in order:

1. Put **Tidus's** move trigger on the stack **first** (bottom of the stack).
2. Put **`Maester Seymour`'s** trigger on the stack **on top of it** (last on).
3. `Maester Seymour` resolves **first**, putting counters on a creature.
4. **Tidus** resolves **second**, moving a counter — which counts as *putting* a counter on the
   destination, triggering `Rikku`'s unblockable and feeding Wakka's Blitzball Captain.
5. Only then declare attackers.

One targeting note that makes step 1 legal: Tidus's trigger just says *"target creature you
control"* — it does **not** require that creature to have a counter when you target it. So you may
point Tidus's move at the creature `Maester Seymour` is about to pump, even though it is empty at
the moment you put the trigger on the stack. If it still has no counter when Tidus's trigger
resolves, nothing moves and you have lost nothing.

### Mistake 8 — Proliferating without looking at the whole board

Proliferate (CR 701.34a) lets you *"choose any number of permanents and/or players that have a
counter."* Rulings on Tidus spell out both traps:

- *"You don't have to choose every permanent or player that has a counter — only the ones you want
  to add counters to."* You are **never forced** to proliferate an opponent's stuff.
- *"If a player or permanent has more than one kind of counter on it, and you choose for it to get
  additional counters, it must get one of each kind of counter it already has."* So if your own
  creature has a +1/+1 counter **and** a stun counter (a stun counter stops it untapping — CR
  122.1d), proliferating it gives it another stun counter too. Sometimes you skip that creature.

**Saga warning:** your four Saga creatures — `Summon: Ixion`, `Summon: Yojimbo`,
`Summon: Valefor`, `Summon: Magus Sisters` — carry **lore counters**. Proliferating
them adds a lore counter, which advances their chapters faster (CR 714.2b) — usually good, more
triggers — but it also gets them to their final chapter sooner, and CR **714.4** makes you
sacrifice a Saga once its lore counters reach its final chapter number. Choose deliberately.

### Mistake 9 — Attacking with your 0-power utility creatures

`Duskshell Crawler` is a **0/3**, `Incubation Druid` is **0/2**, `Forgotten Ancient` is **0/3**,
`Walking Ballista` is **0/0**. These are engines, not attackers. Leave them home unless they've
actually accumulated counters.

---

## 8. Bracket and table expectations

`mtg deck bracket tidus` estimates **Bracket 3 — "Upgraded."**

In plain language, the Commander bracket system sorts decks 1-5 by how hard they're trying to
win. Bracket 3 means: *"A precon that has been deliberately tuned, or a deck built to beat one.
Stronger cards and tighter curve, still not cutthroat."*

**Why this deck lands at 3 and not 2:** exactly one card. The tool checks your list against the
53 officially listed "Game Changers" (cards strong enough to bump a deck's bracket) and found
**one: `Farewell`**. Brackets 1 and 2 both require *zero* Game Changers; Bracket 3 allows up to
three. So one card lifts an otherwise precon-level deck into 3.

The rest of the signals are clean:
- **Mass land denial: 0** — nothing in here destroys everyone's lands.
- **Extra turns: 0** — nothing takes extra turns.
- **Two-card infinite combos:** the tool cannot detect these automatically and flags it for human
  review. Nothing obvious appeared while reading the list, but treat this as unverified.

### What this means at a table

- **Games run long.** Bracket 3 guidance: *"games typically end around turn 7 or later."* Expect
  turn 9-12 in a four-player pod. This deck does not race.
- **You are a fair deck.** You should be comfortable sitting down with other upgraded precons or
  lightly tuned decks. Against a genuine Bracket 4/5 deck you will lose to combo before your board
  matters.
- **You will look scary before you are scary.** A board of creatures covered in counters draws
  attention. Be aware that at a Commander table, the player with the visibly biggest board eats
  the removal. Consider deploying just enough to be threatening, and holding a creature or two in
  hand to rebuild.
- **Say what your deck does at the start.** Standard etiquette at a Bracket 3 table is to name
  your bracket and flag anything spicy. "Bracket 3, +1/+1 counters, one Game Changer —
  `Farewell`" is a complete and honest table pitch.

---

## Quick reference — the whole plan on one screen

```
T1-3   Land. Sol Ring / Hardened Scales / Arcane Signet / Gyre Sage / Incubation Druid.
       Get ONE creature with a counter down. Sequence tapped lands here, not later.

T4-6   Cast Tidus once you have a board. Deploy Maester Seymour / Tromell / Rikku / Wakka.
       Every combat: put Tidus's trigger on the stack FIRST, Seymour's on TOP of it —
       last on = first to resolve. Seymour's counters land, then Tidus moves a counter
       onto Wakka (guarantees Blitzball Captain) or onto your attacker (Rikku makes it
       unblockable). Attack the least-defended player. Cheer draws + proliferates.

T7+    Find the ALPHA STRIKE — the turn you attack with your entire board at once
       because the damage finally adds up to lethal.
       Chocobo Knights = double strike on everything with a counter.
       Damning Verdict clears blockers without touching your team.
       Maester Seymour monstrosity (X +1/+1 counters on him, once only), or Sin,
       as the single huge threat.
       Blitzball Stadium's {3},{T} pushes the last damage through.

HOLD   Inspiring Call (draw + indestructible) when you fear a wipe.
       Path to Exile / Destroy Evil / Endless Detour — you only get four instant answers.
```

---

*All card text, mana costs, type lines, power/toughness, and rulings in this document were
retrieved from the local MTG Brain database. Rules citations are Comprehensive Rules numbers
retrieved via `mtg rule`. Re-verify anything with `./bin/mtg card "<name>"`.*
