# Counter Blitz — Card-by-Card Study Guide

**Deck slug:** `tidus` · **Commander:** Tidus, Yuna's Guardian · **Colors:** Bant (Green/White/Blue, `WUG`)
**Format:** Commander (EDH) only. 100 cards, singleton (one copy of each card except basic lands),
**no sideboard** — Commander does not have one.
**Set:** FIC (FINAL FANTASY Commander), released 2025-06-13 · **Estimated bracket:** 3 (Upgraded)

> Every card fact in this document was pulled from the local database this session.
> Re-check anything yourself with `./bin/mtg card "<name>"` (that also shows official rulings),
> or look up a keyword with `./bin/mtg glossary <term>`.
> Companion document: `PRIMER.md` (how the deck plays); this file is *what each card does*.

---

## How to read this file

Cards are grouped by **the job they do in this deck**, not alphabetically. Each card appears
exactly once, under its main job; secondary jobs are mentioned in its entry.

| Section | Cards | What the section is for |
|---|---|---|
| [Commander](#1-commander) | 1 | The card that starts in your command zone |
| [Ramp & Mana](#2-ramp--mana) | 10 | Getting more mana, faster |
| [Card Draw & Selection](#3-card-draw--selection) | 11 | Refilling your hand |
| [Removal & Interaction](#4-removal--interaction) | 11 | Answering one thing an opponent has |
| [Board Wipes](#5-board-wipes) | 4 | Answering *everything* at once |
| [Threats & Beaters](#6-threats--beaters) | 7 | Big bodies that end games |
| [Synergy Pieces](#7-synergy-pieces--the-actual-engine) | 13 | The +1/+1 counter engine — the real deck |
| [Utility & Protection](#8-utility--protection) | 6 | Keeping your board alive |
| [Lands](#9-lands) | 31 entries / 37 cards | Mana base |

**Total: 94 distinct cards = 100 cards** (the three basic land names are 3 copies each).

### Five words you need before you start

- **+1/+1 counter** — a marker you put on a creature. A `+X/+Y` counter adds X to the creature's
  power and Y to its toughness (Comprehensive Rules **122.1a**). It is permanent — it stays until
  something removes it. It is *not* a token and *not* an object (CR **122.1**).
- **Proliferate** — a keyword action: *"choose any number of permanents and/or players that have a
  counter, then give each one additional counter of each kind that permanent or player already has"*
  (CR **701.34a**). It only adds counters to things that **already** have one, and you choose which
  ones — "any number" includes zero.
- **Mana value (MV)** — the total amount of mana in a card's mana cost, ignoring color (CR **202.3**).
  `{2}{G}{W}` has mana value 4. Older players call this "converted mana cost."
- **Permanent** — anything on the battlefield: creature, artifact, enchantment, land.
- **Instant speed** — you can do it during any player's turn, including in response to something.
  Instants and abilities with **flash** work at instant speed; sorceries, creatures, artifacts and
  enchantments normally only work on your own turn when nothing else is happening.

### Three Commander rules that affect nearly every entry below

- You start at **40 life** and draw seven cards (CR **903.7**).
- Your commander can be cast from the command zone, and **costs an additional {2} for each previous
  time you cast it from there this game** — the "commander tax" (CR **903.8**).
- A player dealt **21 or more combat damage by the same commander** over the game loses (CR **903.10a**).
  With this commander that basically never comes up — Tidus is a 3/3 and is not your win route.

---

## 1. Commander

#### Tidus, Yuna's Guardian — {G}{W}{U} — Legendary Creature — Human Warrior · 3/3

Your commander, and the card the deck is named around. He does two things. **First**, at the
beginning of combat on each of your turns (the step between your first main phase and declaring
attackers), you *may* move one counter from one creature you control onto another creature you
control. That is a free counter shuffle every turn — you use it to consolidate counters onto the
creature that is about to get through, or to trigger everything in the deck that cares about
"whenever you put a counter on a creature." **Second**, his ability called **Cheer**: whenever one
or more creatures you control that have counters on them deal combat damage to a player, you may
draw a card and proliferate — but only **once each turn**, no matter how many creatures connect.

Note the wording is "creatures... with **counters**", not "+1/+1 counters". A shield counter or a
flying counter also switches Cheer on.

**When to play it:** Not on turn 3 into an empty board — a 3/3 with no counters on your side does
nothing and just eats a removal spell, making the next cast cost {2} more (CR **903.8**). Cast him
once you already have one or two creatures with counters that can attack, ideally turn 4–6.

**Watch out:** The move ability says "target creature you control" **and** "a second target creature
you control" — you need **two** different creatures you control for it to do anything. With only one
creature out, the ability has no legal targets and simply does nothing.

**Rulings:**
- *"To move a counter from one permanent to another, the counter is removed from the first permanent
  and put on the second. Any abilities that care about a counter being removed from or put onto a
  permanent will apply."* — this is why the move is an engine, not just a shuffle: it triggers
  Rikku, Fathom Mage, Lord Jyscal Guado, etc.
- *"You don't have to choose every permanent or player that has a counter — only the ones you want to
  add counters to. Since 'any number' includes zero, you don't have to choose any permanents at all."*
- *"When you proliferate, you can choose any permanent that has a counter, including ones controlled
  by opponents. You can choose any player who has a counter, including opponents."* (You normally
  will not want to — but you may need to if an opponent has a counter you can safely grow.)
- *"If a player or permanent has more than one kind of counter on it, and you choose for it to get
  additional counters, it must get one of each kind of counter it already has."* Careful: proliferating
  a creature of yours that has both a +1/+1 counter **and** a stun counter gives it another of each.
- *"Players can respond to a spell or ability whose effect includes proliferating. Once that spell or
  ability starts to resolve, however, and its controller chooses which permanents and players will get
  new counters, it's too late for anyone to respond."*

---

## 2. Ramp & Mana

"Ramp" means anything that gets you extra mana ahead of schedule, or fixes which colors you have.
This deck runs 10 of them plus 37 lands.

#### Sol Ring — {1} — Artifact

Costs one mana, taps for two colorless mana (`{T}: Add {C}{C}`). It pays for itself the turn after
you play it and never stops. The single most powerful cheap card in Commander.

**When to play it:** Turn 1, always, no exceptions. If it is in your opening hand, that hand is fine.

**Watch out:** It makes **colorless** mana. Colorless mana cannot pay for the `{G}`, `{W}` or `{U}`
in a cost — only for generic amounts like the `{2}` in `{2}{G}{W}`. Sol Ring does not fix your colors.

#### Arcane Signet — {2} — Artifact

Two mana, taps for one mana of any color in your commander's color identity — so green, white, or
blue for you. Colour identity is defined in CR **903.4**.

**When to play it:** Turn 2 if you have nothing better; it makes your awkward three-colour costs
(`{G}{W}{U}` on Tidus, `{1}{G}{W}{U}` on Yuna) reachable a turn early.

**Rulings:** *"If you don't have a commander, Arcane Signet's ability produces no mana."* Irrelevant in
practice — but it is why the card is only good in this format.

#### Everflowing Chalice — {0} — Artifact

Costs zero mana base, but has **Multikicker {2}** — an optional additional cost you may pay any
number of times as you cast it (a variant of kicker, CR **702.33**). It enters with one charge
counter for each time you kicked it, and taps for `{C}` per charge counter.

**When to play it:** Pay {4} for a two-mana rock on turn 4, or {2} for a one-mana rock. Cast it for
{0} only if you are desperate for an artifact on the battlefield for some other reason.

**Watch out:** *"You can cast Everflowing Chalice without kicking it at all if you wish. However, if
Everflowing Chalice has no charge counters on it, activating its last ability won't produce any mana."*
A {0} Chalice is literally a blank. Also — charge counters **are counters**, so proliferate grows it,
and it dies to `Bane of Progress` / `Farewell` alongside your own artifacts.

#### Farseek — {1}{G} — Sorcery

Search your library for a Plains, Island, Swamp, or Mountain card, put it onto the battlefield
**tapped**, then shuffle.

**When to play it:** Turn 2. Prefer fetching a dual land over a basic — see the ruling.

**Watch out:** Farseek **cannot find a Forest**. Read the list again: Plains, Island, Swamp, Mountain.
In this deck it finds a basic Plains or Island, or better, one of your nonbasic lands that *has* one
of those land types.

**Rulings:** *"Farseek can find any land with any of the listed land types, including nonbasic ones,
even if that land is a Forest in addition to one or more of those types."* So Farseek can grab
`Canopy Vista` (Land — Forest Plains), `Prairie Stream` (Land — Plains Island), `Idyllic Beachfront`
(Land — Plains Island) or `Tangled Islet` (Land — Forest Island). Those are strictly better than a basic.

#### Three Visits — {1}{G} — Sorcery

Search your library for a Forest card, put it onto the battlefield (**untapped**), then shuffle.

**When to play it:** Turn 2. It is better than Farseek in the one way that matters most — the land
comes in untapped, so on turn 2 you can still use it.

**Rulings:** *"Three Visits allows you to search your library for any card with the land type Forest,
not just a card with the name Forest."* So it can fetch `Canopy Vista`, `Radiant Grove` or
`Tangled Islet` (all have the Forest type) — but those three all enter tapped anyway, so grabbing a
basic Forest is often correct if you need the mana this turn.

#### Gyre Sage — {1}{G} — Creature — Elf Druid · 1/2

A mana creature that scales with the deck's theme. It has **evolve**: *"Whenever a creature you
control enters, if that creature's power is greater than this creature's power and/or that creature's
toughness is greater than this creature's toughness, put a +1/+1 counter on this creature"*
(CR **702.100a**). Then `{T}: Add {G} for each +1/+1 counter on this creature` — note **zero counters
means zero mana**.

**When to play it:** Turn 2, but only if you expect to play bigger creatures soon. In a deck with
`Hardened Scales`, `Tromell` and proliferate, it routinely taps for 3–5 green.

**Watch out:** The turn it lands it taps for **nothing**. It needs a counter first.

**Rulings:** *"Gyre Sage's last ability is a mana ability. It doesn't use the stack and can't be
responded to."* (Meaning: nobody can kill it "in response" to you tapping it for mana.)

#### Incubation Druid — {1}{G} — Creature — Elf Druid · 0/2

`{T}: Add one mana of any type that a land you control could produce. If this creature has a +1/+1
counter on it, add **three** mana of that type instead.` It also has `{3}{G}{G}: Adapt 3` — adapt N
means *"If this permanent has no +1/+1 counters on it, put N +1/+1 counters on it"* (CR **701.46a**).

**When to play it:** Turn 2. Get any counter onto it — via Tidus's move ability, `Duskshell Crawler`,
`Shelinda`, proliferate, anything — and it becomes a three-mana land that also fixes colors.

**Watch out:** **Adapt does nothing if it already has a +1/+1 counter** (CR 701.46a). So never pay
{3}{G}{G} for adapt on a Druid that already has one counter — use a cheaper counter source instead.

**Rulings:** *"Incubation Druid checks the effects of all mana-producing abilities of lands you
control, but it doesn't check their costs or legality."* It copies what your lands *could* make, so
with `Command Tower` out it effectively taps for any of your three colors.

#### Scholar of New Horizons — {1}{W} — Creature — Human Scout · 1/1

Enters with a +1/+1 counter already on it. Then: `{T}, Remove a counter from a permanent you control:
Search your library for a Plains card and reveal it. If an opponent controls more lands than you, you
may put that card onto the battlefield tapped. If you don't put the card onto the battlefield, put it
into your hand. Then shuffle.`

**When to play it:** Turn 2. It is a land-fetcher that is also a legal target for every counter
effect you own.

**Watch out:** You only get the land onto the battlefield **if an opponent controls more lands than
you**. Otherwise it just goes to your hand — still fine, but it is not ramp that turn. Also note the
cost **removes** a counter, which shrinks the creature you take it from.

**Rulings:** *"You may choose to put the card into your hand rather than onto the battlefield even if
an opponent controls more lands than you."*

#### Rampant Rejuvenator — {3}{G} — Creature — Plant Hydra · 0/0

Enters with **two** +1/+1 counters on it (so it is normally a 2/2). When it dies, search your library
for up to X basic land cards, where X is its power, put them onto the battlefield, then shuffle.

**When to play it:** Turn 4 when you already have counter-doublers out. With `Hardened Scales` it
enters as a 3/3; grow it with proliferate and its death becomes a 4–6 land payoff.

**Watch out:** This is a 0/0 creature — without counters it dies immediately as a state-based action
(CR **704.5f**). Anything that removes all its counters kills it. Also, it fetches **basic** lands
only, and this deck runs just 9 basics (3 Forest, 3 Island, 3 Plains) — you will run out fast.

**Rulings:** *"Use Rampant Rejuvenator's power as it last existed on the battlefield to determine the
value of X for its last ability."* So growing it right before it dies still counts.

#### Yuna, Grand Summoner — {1}{G}{W}{U} — Legendary Creature — Human Cleric · 1/5

Two abilities. **Grand Summon** — `{T}: Add one mana of any color. When you next cast a creature spell
this turn, that creature enters with two additional +1/+1 counters on it.` And: *"Whenever another
permanent you control is put into a graveyard from the battlefield, if it had one or more counters on
it, you may put that number of +1/+1 counters on target creature."*

**When to play it:** Turn 4 as a mana creature that pre-loads your next creature with counters. A 1/5
body blocks well and survives most early attacks.

**Watch out:** The counter bonus only applies to *the next creature spell you cast that turn* — tap
Yuna **before** casting the creature you want to grow, not after.

**Rulings:** *"Yuna's last ability counts all counters that were on the permanent, not just +1/+1
counters."* A creature with a stun counter and two +1/+1 counters that dies gives you **three** +1/+1
counters on the target. That is a real upside when your board gets wiped.

---

## 3. Card Draw & Selection

Twelve cards were tagged "draw" by the deck tool; eleven of them live here (`Inspiring Call` is in
[Utility & Protection](#8-utility--protection) because its main job is saving your board).

#### Blitzball Stadium — {X}{U} — Artifact

When it enters, **support X** — support N on a permanent means *"Put a +1/+1 counter on each of up to
N other target creatures"* (CR **701.41a**). Then: `Go for the Goal! — {3}, {T}: Until end of turn,
target creature gains "Whenever this creature deals combat damage to a player, draw a card for each
kind of counter on it" and it can't be blocked this turn.`

**When to play it:** Cast it for X = 2 or 3 mid-game so it spreads counters as it lands, then use the
activated ability on your biggest counter-carrier the turn you want a big draw.

**Watch out:** Read the draw clause carefully — it draws a card for each **kind** of counter, not each
counter. A creature with twelve +1/+1 counters and nothing else draws you **one** card. To draw more
you need different *kinds* — e.g. a +1/+1 counter plus a shield counter (from `Protection Magic`) plus
a flying counter (from `Luminous Broodmoth`).

#### Bred for the Hunt — {1}{G}{U} — Enchantment

*"Whenever a creature you control with a +1/+1 counter on it deals combat damage to a player, you may
draw a card."* Unlike your commander's Cheer, this is **not** limited to once per turn — every
creature that connects draws a card.

**When to play it:** Turn 3 on a board that already has two or more countered creatures. This is the
deck's best repeatable draw engine.

**Watch out:** Combat damage **to a player** only. Damage to a blocking creature draws nothing.

**Rulings:** *"A creature that deals combat damage to a player must have a +1/+1 counter on it at the
time damage is dealt in order for Bred for the Hunt's ability to trigger."* So if you use your
commander's move ability to strip a counter off an attacker before damage, that attacker no longer draws.

#### Chasm Skulker — {2}{U} — Creature — Squid Horror · 1/1

*"Whenever you draw a card, put a +1/+1 counter on this creature."* And when it dies, create X 1/1
blue Squid creature tokens with islandwalk (they can't be blocked as long as the defending player
controls an Island), where X is the number of +1/+1 counters on it.

**When to play it:** Turn 3, ideally before you deploy your draw engines. It grows every single draw —
including your normal draw step each turn.

**Watch out:** It is a 1/1 to start and dies to almost anything early. That is mostly fine, because
dying converts it into a squad of tokens.

**Rulings:**
- *"If you draw multiple cards, the first ability will trigger that many times."* `Pull from Tomorrow`
  for X=5 puts five counters on it.
- *"If enough -1/-1 counters are put on Chasm Skulker at the same time to make its toughness 0 or
  less, the number of +1/+1 counters on it before it got any -1/-1 counters will be used to determine
  how many Squid tokens you get."*

#### Fathom Mage — {2}{G}{U} — Creature — Human Wizard · 1/1

Has **evolve** (see `Gyre Sage`, CR **702.100a**), plus: *"Whenever a +1/+1 counter is put on this
creature, you may draw a card."*

**When to play it:** Turn 4 when you have counter-movers online. Every time Tidus moves a counter onto
her, or you proliferate, or `Hardened Scales` adds one — you draw.

**Watch out:** A 1/1 body. She is the card opponents most want to kill; expect to lose her and plan
to get value the turn she lands.

**Rulings:**
- *"If multiple +1/+1 counters are placed on Fathom Mage simultaneously, its last ability will trigger
  once for each of those counters."* Three counters at once = three draws.
- *"Fathom Mage's last ability will trigger whenever any +1/+1 counter is placed on it, not just ones
  due to the evolve ability."*

#### Generous Patron — {2}{G} — Creature — Elf Advisor · 1/4

When it enters, **support 2** (a +1/+1 counter on each of up to two *other* target creatures — CR
**701.41a**). Plus: *"Whenever you put one or more counters on a creature you don't control, draw a card."*

**When to play it:** Turn 3. The 1/4 body blocks early aggression well.

**Watch out:** The draw trigger is for creatures you **don't** control. That reads like a downside but
it is a deliberate combo: support can target opponents' creatures, so you can hand an opponent a
harmless +1/+1 counter to draw a card. Do this on a creature that cannot punish you for it.

**Rulings:**
- *"Support can target a creature another player controls."*
- *"If you put one or more counters on multiple creatures you don't control at the same time, such as
  by supporting two different creatures you don't control, Generous Patron's last ability triggers for
  each of those creatures."* Two opposing creatures supported = **two** cards.
- *"Generous Patron's last ability triggers even if the counters you put on another player's creatures
  aren't +1/+1 counters."* A stun counter from `Lulu` on an opposing attacker also draws you a card.
- *"You can't put more than one +1/+1 counter on any one target using the support action."*

#### Lord Jyscal Guado — {1}{W} — Legendary Creature — Spirit Cleric · 2/1

Flying (can't be blocked except by creatures with flying and/or reach — CR **702.9b**). *"At the
beginning of each end step, if you put a counter on a creature this turn, **investigate**."* To
investigate is to create a Clue token (CR **701.16a**) — an artifact with `{2}, Sacrifice this token:
Draw a card`.

**When to play it:** Turn 2. Note "each end step" — that includes **opponents' turns**, so in a
four-player game this can make up to four Clues per turn cycle if you keep putting counters down.

**Watch out:** You must have actually put a counter on a creature *during that turn*. To get value on an
opponent's turn you need an instant-speed counter source: `Protection Magic`, `Gatta and Luzzu` (flash),
`Yuna's Whistle`, or `Lulu`'s stun-counter trigger when someone attacks you. `Nesting Grounds` and
`Rikku`'s Steal are **sorcery-speed only** and cannot help on an opponent's turn.

**Rulings:** *"Lord Jyscal Guado's last ability checks at the moment it would trigger to see if you put
a counter on a creature this turn. If you didn't, the ability won't trigger at all. Once your end step
begins, it's too late to put a counter on a creature in order to cause this ability to trigger."*

#### O'aka, Traveling Merchant — {1}{U} — Legendary Creature — Human Citizen · 1/2

`{T}, Remove a counter from a nonland permanent you control: Draw a card.`

**When to play it:** Turn 2 in a hand with lots of counter production. It converts surplus counters
into cards, once per turn.

**Watch out:** It **removes** a counter — you are shrinking a creature to draw. Only do it when the
counter is not doing work (e.g. a lore counter is not removable this way; a spare +1/+1 counter on a
creature that is not attacking is). Note "nonland permanent," so charge counters on `Everflowing
Chalice` also work — but that shrinks your mana.

#### Pull from Tomorrow — {X}{U}{U} — Instant

Draw X cards, then discard a card.

**When to play it:** At the end of an opponent's turn (their end step), so your mana was not wasted
and you untap with a full hand. X = 4 or more is where it gets good.

**Watch out:** The discard is **not optional** and happens even if X is 0. Also, drawing a big pile
does not help if your hand is already full at end of turn — you discard down to seven at your cleanup
step, so cast it on the turn cycle you can actually deploy the cards.

#### Tireless Tracker — {2}{G} — Creature — Human Scout · 3/2

*Landfall* — whenever a land you control enters, investigate (make a Clue). ("Landfall" is an **ability
word**: it has no rules meaning of its own, it just labels the trigger — CR **207.2c**.) Plus:
*"Whenever you sacrifice a Clue, put a +1/+1 counter on this creature."*

**When to play it:** Turn 3, ideally before your land drop that turn. Every land after that is a card.

**Watch out:** Each Clue costs `{2}` to cash in. You need mana to convert Clues into cards; don't hoard
six Clues you can never crack.

**Rulings:**
- *"A landfall ability triggers whenever a land you control enters for any reason. It triggers whenever
  you play a land, as well as whenever a spell or ability puts a land onto the battlefield under your
  control."* — so `Farseek`, `Three Visits`, `Evolving Wilds` and `Scholar of New Horizons` all trigger it.
- *"Some abilities trigger 'whenever you sacrifice a Clue'. Those abilities trigger whenever you
  sacrifice a Clue for any reason, not just to activate a Clue's activated ability."*
- *"You can't sacrifice a Clue to pay multiple costs."*

#### Yuna's Decision — {3}{G} — Sorcery

Choose one — **Continue the Pilgrimage:** sacrifice a creature; if you do, draw a card, then you may
put a creature card and/or a land card from your hand onto the battlefield. Or **Find Another Way:**
return one or two target permanent cards from your graveyard to your hand.

This is the deck's **only recursion** card (the tool counts `recursion 1`), and it doubles as ramp and draw.

**When to play it:** Mode 2 after a board wipe, to rebuild — two permanents back is a real swing.
Mode 1 when you have a dying or already-worthless creature and an expensive creature stuck in hand.

**Watch out:** Mode 1 makes you sacrifice **first**; if you have no creature you cannot choose it
usefully. Sacrificing a creature with counters also turns on `Yuna, Grand Summoner`'s death trigger,
which is a genuine two-card combo worth remembering.

**Rulings:** *"Putting a land card onto the battlefield with the first mode of Yuna's Decision doesn't
count as playing a land. You can put a land card onto the battlefield this way even if you've already
played a land for the turn."*

#### Yuna's Whistle — {1}{G}{G} — Instant

Reveal cards from the top of your library until you reveal a creature card. Put that card into your
hand and the rest on the bottom of your library in a random order. When you reveal a creature card this
way, put X +1/+1 counters on target creature you control, where X is the mana value of that card.

**When to play it:** At instant speed in combat, as a surprise pump. With 34 creatures in the deck you
will hit quickly, and the average non-land mana value is 3.03, so expect roughly +3/+3 **and** a card.

**Watch out:** You do not choose which creature you find — it is the first one off the top. And the
counters go on **a creature you control**, targeted separately.

**Rulings:**
- *"You don't choose a target for Yuna's Whistle at the time you cast it. Rather, a second 'reflexive'
  ability triggers when you reveal a creature card this way. You choose a target for that ability as it
  goes on the stack. Each player may respond to this triggered ability as normal."* (So an opponent can
  kill your intended target after they see the size of the pump.)
- *"If the revealed card has {X} in its mana cost, X is 0 for the purpose of determining its mana value."*
  Revealing `Walking Ballista` ({X}{X}) gives you **zero** counters.

---

## 4. Removal & Interaction

Answers to a single problem permanent. The deck has 8 tool-tagged removal spells plus the Sagas;
only **4 of these work at instant speed** (`Path to Exile`, `An Offer You Can't Refuse`,
`Destroy Evil`, `Endless Detour`). That is the deck's biggest structural weakness — most of your
answers only work on your own turn.

#### Path to Exile — {W} — Instant

Exile target creature. Its controller may search their library for a basic land card, put that card
onto the battlefield tapped, then shuffle.

**When to play it:** One mana, instant speed, exiles anything — the best removal spell in the deck.
Save it for a genuine threat (a commander, a creature about to kill you), not the first 3/3 you see.

**Watch out:** You are **ramping your opponent** — they get a land. Against a player who is already
short on lands this is a real gift; consider a different answer if you have one.

**Rulings:**
- *"The controller of the exiled creature isn't required to search their library for a basic land."*
- *"If the target creature is an illegal target by the time Path to Exile tries to resolve, it won't
  resolve and none of its effects will happen. The creature's controller won't search for a basic land."*

#### An Offer You Can't Refuse — {U} — Instant

Counter target **noncreature** spell. Its controller creates two Treasure tokens (artifacts with
`{T}, Sacrifice this token: Add one mana of any color`). To "counter" a spell means to cancel it so
it never resolves.

**When to play it:** Hold one blue mana up when you suspect a board wipe or a game-winning artifact/
enchantment. This is the cheapest interaction in the deck.

**Watch out:** **It cannot counter a creature spell.** In a format full of creatures that is a big
restriction. Also, the two Treasures are real mana for the opponent — they may just recast something.

**Rulings:** *"If the target is still legal as it resolves but the spell can't be countered for some
reason, its controller will still create two Treasure tokens."* (Worst case: you gave them mana for free.)

#### Destroy Evil — {1}{W} — Instant

Choose one — destroy target creature with toughness 4 or greater; **or** destroy target enchantment.

**When to play it:** Instant speed, two mana, flexible. The enchantment mode matters — this deck has
few other ways to handle an opposing enchantment.

**Watch out:** The creature mode requires **toughness 4 or greater**, current toughness as it resolves.
It cannot kill a 5/2, a 3/3, or most small utility creatures. Check the toughness, not the power.

#### Endless Detour — {G}{W}{U} — Instant

The owner of target spell, nonland permanent, or card in a graveyard puts it on their choice of the
top or bottom of their library.

**When to play it:** As a catch-all. It handles a spell on the stack (a pseudo-counterspell), a
resolved permanent of any type, **or** a card in a graveyard someone is trying to reanimate.

**Watch out:** Costs one of each of your three colors — you often physically cannot cast it early.
And the **owner** chooses top or bottom, so a savvy opponent puts it on top and redraws it.

**Rulings:**
- *"Endless Detour doesn't counter spells. A spell that can't be countered can still be put on the top
  or bottom of its owner's library this way."* Useful against "can't be countered" threats.
- *"If Endless Detour targets a token, that token is put into the library, then ceases to exist."*
- *"The card's owner chooses whether to put it on the top or bottom of their library."*

#### Collective Effort — {1}{W}{W} — Sorcery

**Escalate — Tap an untapped creature you control.** Escalate means *"For each mode you choose beyond
the first as you cast this spell, you pay an additional [cost]"* (CR **702.120a**). Modes: destroy
target creature with power 4 or greater; destroy target enchantment; put a +1/+1 counter on each
creature target player controls.

**When to play it:** On a wide board, tap two spare creatures and take all three modes for {1}{W}{W} —
kill a big creature, kill an enchantment, and pump your whole team.

**Watch out:** Sorcery speed. Tapping creatures to escalate means they can't block that turn cycle,
and if you do it on your own turn *before* attacking, those creatures can't attack either. Also, the
third mode targets a **player** — pick yourself.

**Rulings:**
- *"You can tap any untapped creature you control to pay the escalate cost, including one you haven't
  controlled continuously since the beginning of the turn."* (No "summoning sickness" restriction here.)
- *"If you choose the first and third modes, and destroying the creature ends an 'exile until' effect…,
  the creature will return to the battlefield before you put +1/+1 counters on creatures."*

#### Walking Ballista — {X}{X} — Artifact Creature — Construct · 0/0

Enters with X +1/+1 counters on it. `{4}: Put a +1/+1 counter on this creature.` `Remove a +1/+1
counter from this creature: It deals 1 damage to any target.`

**When to play it:** Any time you have spare mana — it is a mana sink at every stage of the game. It
is the deck's only way to kill a creature at instant speed without a spell, and it can throw damage at
a player's face.

**Watch out:** `{X}{X}` means you pay **twice X** — for a 3/3 you pay {6}. Also, it is a 0/0: with no
counters it dies instantly (CR **704.5f**), so removing its last counter kills it. That is often fine.
Every counter you add via `Hardened Scales`, proliferate, or Tidus's move makes it a bigger gun.

**Rulings:**
- *"A casting cost of {X}{X} means that you pay twice X. If you want X to be 3, you pay {6}."*
- *"If Walking Ballista has been dealt damage or had its toughness reduced by an effect, this limits
  how many times you'll be able to remove +1/+1 counters from it in a single turn."*

#### Auron, Venerated Guardian — {3}{W} — Legendary Creature — Human Spirit Samurai · 2/5

Vigilance (attacking doesn't cause it to tap — CR **702.20**). **Shooting Star** — whenever Auron
attacks, put a +1/+1 counter on it. When you do, exile target creature the defending player controls
with power **less than Auron's power**, until Auron leaves the battlefield.

**When to play it:** Turn 4. This is your most repeatable removal: every attack exiles something. With
vigilance he still blocks after attacking.

**Watch out:** The exile is tied to Auron — **if Auron dies or is removed, the exiled creature comes
back**. And the power comparison happens when the reflexive trigger goes on the stack, after the +1/+1
counter, so an attacking Auron is at least a 3/6 for that check.

**Rulings:**
- *"You don't choose a target for Auron's last ability at the time it triggers. Rather, a second
  'reflexive' ability triggers when you put a +1/+1 counter on it this way. You choose a target for
  that ability as it goes on the stack. Each player may respond to this triggered ability as normal."*
- *"Once a creature is exiled by the reflexive triggered ability, it doesn't matter what happens to
  Auron's power. Reducing Auron's power below the exiled creature's power won't cause the exiled
  creature to return."*
- *"If a token is exiled this way, it will cease to exist and won't return to the battlefield."*
- *"Any counters on the exiled creature will cease to exist. When the card returns to the battlefield,
  it will be a new object."*

#### Summon: Ixion — {2}{W} — Enchantment Creature — Saga Unicorn · 3/3

A **Saga**: as it enters and after each of your draw steps, add a lore counter; the chapter with that
number triggers (CR **714.2b**). It is sacrificed after chapter III. It also has first strike (deals
combat damage before creatures without first strike — CR **702.7**).
- **I — Aerospark:** Exile target creature an opponent controls until this Saga leaves the battlefield.
- **II, III:** Put a +1/+1 counter on each of up to two target creatures you control. You gain 2 life.

**When to play it:** Turn 3. It is removal on turn one, a 3/3 first-strike body the whole time, and
two rounds of counters after that.

**Watch out:** The Saga **sacrifices itself after chapter III** — and when it leaves, the exiled
creature comes back. You get roughly three turns of removal, not permanent removal.

**Rulings:**
- *"If Summon: Ixion leaves the battlefield before its first chapter ability resolves, the target
  permanent won't be exiled."*
- *"If a token is exiled this way, it will cease to exist and won't return."*
- *"You don't have to choose any targets for Summon: Ixion's second or third chapter ability. However,
  if you do and all of the targets are illegal when the ability tries to resolve, it won't resolve and
  none of its effects will happen. You won't gain life."*

#### Summon: Yojimbo — {3}{W} — Enchantment Creature — Saga Samurai · 5/5

A Saga with vigilance, sacrificed after chapter IV.
- **I:** Exile target artifact, enchantment, **or tapped creature** an opponent controls.
- **II, III:** Until your next turn, creatures can't attack you unless their controller pays {2} for
  each of those creatures.
- **IV:** Create X Treasure tokens, where X is the number of opponents who control a creature with
  power 4 or greater.

**When to play it:** Turn 4. A 5/5 vigilance body for four mana is already a fine rate; the chapters
are pure profit. Chapter I is your only clean answer to an opposing artifact or enchantment outside of
`Destroy Evil`, `Collective Effort`, `Bane of Progress` and `Farewell`.

**Watch out:** Chapter I can only hit a **tapped** creature — untapped blockers are safe. Chapters II
and III are a defensive tax, not a hard lock; a determined opponent can just pay.

**Rulings:**
- *"On turns where the effect of Summon: Yojimbo's second or third chapter ability is applying, your
  opponents can choose not to attack with a creature that must attack if able as long as there is no
  other player, planeswalker, or battle for that creature to attack that wouldn't require a cost."*
- *"The value of X is determined only once, as Summon: Yojimbo's fourth chapter ability resolves."*

#### Summon: Valefor — {4}{U} — Enchantment Creature — Saga Drake · 5/4

A Saga with flying, sacrificed after chapter IV.
- **I — Sonic Wings:** Each opponent chooses a creature with the greatest mana value among creatures
  they control. Return those creatures to their owners' hands.
- **II, III, IV:** Tap up to one target creature and put a **stun counter** on it. A stun counter means
  *"If a permanent with a stun counter on it would become untapped, instead remove a stun counter from
  it"* (CR **122.1d**) — so the creature misses its next untap.

**When to play it:** Turn 5 when the table has expensive bombs out. Chapter I is a one-sided sweeper of
the biggest thing each opponent has, and a 5/4 flier is a real clock.

**Watch out:** Chapter I is a **bounce**, not removal — they can recast. And each opponent chooses,
so they will pick the greatest-mana-value creature they least mind losing if there is a tie.

**Rulings:**
- *"While resolving Valefor's first chapter ability, the next opponent in turn order chooses a
  creature with the greatest mana value among creatures they control, then each other opponent in turn
  order does the same. Then the chosen creatures are returned to their owners' hands simultaneously."*
- *"If a creature on the battlefield has {X} in its mana cost, X is 0 for the purpose of determining
  its mana value."*

#### Lulu, Stern Guardian — {2}{U} — Legendary Creature — Human Wizard · 2/3

*"Whenever an opponent attacks you, choose target creature attacking you. Put a stun counter on that
creature."* Plus `{3}{U}: Proliferate.`

**When to play it:** Turn 3 when you are the table's punching bag, or any time you want a repeatable
proliferate outlet — that second ability is genuinely one of the deck's better mana sinks.

**Watch out:** The stun counter goes on **one** attacker, and it does not stop this attack — it stops
that creature untapping next turn. Also, a stun counter is a counter, so proliferating it gives that
opposing creature *another* stun counter (good) — but if that opposing creature also has +1/+1
counters, proliferate grows those too (bad). Read CR **122.1** carefully before proliferating an
opponent's stuff.

**Rulings:**
- *"Lulu's first ability only cares about creatures attacking you, not planeswalkers you control or
  battles you protect."*
- *"When you proliferate, you can choose any permanent that has a counter, including ones controlled
  by opponents."*
- *"If a player or permanent has more than one kind of counter on it, and you choose for it to get
  additional counters, it must get one of each kind of counter it already has."*

---

## 5. Board Wipes

Four cards that destroy or exile many permanents at once. Two of them (`Damning Verdict`,
`Promise of Loyalty`) are built to spare your board and wreck everyone else's — that asymmetry is one
of the best things this deck does.

#### Damning Verdict — {3}{W}{W} — Sorcery

*"Destroy all creatures with no counters on them."*

**When to play it:** This is your signature card. Your creatures have counters; theirs almost never do.
Cast it when the table has developed and you have two or more countered creatures out — you keep your
board and everyone else starts over.

**Watch out:** It says **counters**, not +1/+1 counters — but it also means **your** counter-less
creatures die too. Before casting, walk your board and make sure every creature you care about has at
least one counter of some kind. Use Tidus's beginning-of-combat move, `Together Forever`'s support, or
`Protection Magic` to top up first. Note a token creature with no counters dies like anything else.

#### Promise of Loyalty — {4}{W} — Sorcery

*"Each player puts a vow counter on a creature they control and sacrifices the rest. Each of those
creatures can't attack you or planeswalkers you control for as long as it has a vow counter on it."*

**When to play it:** When you are behind on board. Everyone keeps exactly one creature — and the ones
they keep cannot attack **you**. It resets a runaway table without leaving you defenceless.

**Watch out:** You sacrifice too — you keep only one creature. Also, sacrifice **bypasses
indestructible and shield counters**, so `Inspiring Call` and `Protection Magic` will not save your
extra creatures. And because the survivors now have a vow counter, `Damning Verdict` afterwards will
no longer kill them.

**Rulings:**
- *"Each player, including you, must put a vow counter on a creature they control if able. They can't
  choose to opt out and sacrifice all of their creatures."*
- *"If the vow counter is removed from the creature, it can attack as normal."*
- *"If the vow counter is moved to another creature, it won't prevent the second creature from
  attacking normally."* — note `Rikku`'s Steal and `Nesting Grounds` can move a vow counter off an
  opposing creature, which is usually pointless, but moving one **onto** your own is a way to give a
  creature a counter for `Damning Verdict`.

#### Farewell — {4}{W}{W} — Sorcery

Choose one or more — exile all artifacts; exile all creatures; exile all enchantments; exile all
graveyards. **Exile**, not destroy, so indestructible and regeneration do not help anyone.

**When to play it:** The full reset when you are losing badly and no asymmetric answer will do. Pick
only the modes you need — if your board is enchantments and theirs is creatures, choose creatures only.

**Watch out:** This is the deck's single **Game Changer** card — `./bin/mtg deck bracket tidus` reports
`Game Changers: 1 — Farewell`, and that is what drives the Bracket 3 rating. It is completely symmetrical
if you choose everything, and it exiles **your** Sagas, `Sphere Grid`, `Hardened Scales` and Clues too.
Most of the time you should be casting `Damning Verdict` instead.

**Rulings:** *"If you choose more than one mode for Farewell, you perform the actions in the order
written."* (Artifacts, then creatures, then enchantments, then graveyards.)

#### Bane of Progress — {4}{G}{G} — Creature — Elemental · 2/2

When it enters, destroy **all** artifacts and enchantments. Put a +1/+1 counter on it for each
permanent destroyed this way.

**When to play it:** Against a table full of mana rocks, equipment, or enchantment engines. It often
lands as a 6/6 or bigger.

**Watch out:** It destroys **your** artifacts and enchantments too — `Hardened Scales`, `Sphere Grid`,
`Bred for the Hunt`, `Sol Ring`, `Arcane Signet`, your Clues, and all four of your Sagas (Sagas are
enchantments). Read your own board before casting this. It is frequently a bad card in this deck.

**Rulings:**
- *"Bane of Progress's ability destroys all artifacts and enchantments, including those you control."*
- *"If an artifact or enchantment isn't destroyed (perhaps because it has indestructible or it
  regenerated), it won't count toward the number of +1/+1 counters put on Bane of Progress."*

---

## 6. Threats & Beaters

The bodies that actually end games. The deck tool reports `wincon 0` — there is no card here that says
"you win." These are how you win anyway: attacking, repeatedly, with something too big to block.

#### Chocobo Knights — {3}{W} — Creature — Human Knight · 3/3

*"Whenever you attack, creatures you control with counters on them gain double strike until end of turn."*
Double strike means the creature deals its combat damage **twice** — once in a first-strike damage
step, once in the normal one (CR **702.4b**).

**When to play it:** Turn 4, and then attack. This is the closest thing the deck has to a finisher: it
doubles your entire attack step, and because your commander's Cheer is "once each turn," the first
strike damage step is when Cheer triggers and the second step is free extra damage.

**Watch out:** Read the wording precisely — the card says "Whenever **you** attack", and it pumps
"**creatures you control** with counters on them", not "attacking creatures". It also only sees counters
that are already there when the ability resolves, so **put your counters on before you declare
attackers**. The sequencing works in your favour: Tidus's counter-move happens at the beginning of
combat, and attackers are declared later, in the declare attackers step (CR **508.1a**).

#### Wakka, Devoted Guardian — {2}{G}{W} — Legendary Creature — Human Warrior · 4/4

Reach (can block fliers — CR **702.17**) and trample (excess combat damage past blockers hits the
player — CR **702.19b**). *"Whenever Wakka deals combat damage to a player, destroy up to one target
artifact that player controls and put a +1/+1 counter on Wakka."* And **Blitzball Captain** — *"At the
beginning of your end step, if a counter was put on Wakka this turn, put a +1/+1 counter on each other
creature you control."*

**When to play it:** Turn 4. A 4/4 trampler for four is a fine rate on its own, and Blitzball Captain
is a **team-wide counter engine** every single turn — this is one of the deck's three or four best cards.

**Watch out:** Blitzball Captain needs a counter to have been put on Wakka **that turn**, and it checks
at the beginning of your end step. Tidus's move ability puts a counter on Wakka, which is a clean way
to turn it on every turn even when Wakka doesn't connect.

**Rulings:**
- *"Wakka's last ability checks at the moment it would trigger to see if a counter was put on Wakka
  this turn. If none were, the ability won't trigger at all. Once your end step begins, it's too late
  to put a counter on Wakka in order to cause this ability to trigger."*
- *"You don't have to choose a target for Wakka's second ability. However, if you do and the target is
  illegal as the ability tries to resolve, it won't resolve and none of its effects will happen. You
  won't put a counter on Wakka."* — **important**: if you target an artifact and it is gone by
  resolution, you lose the counter too. If there is no artifact worth destroying, choose no target.

#### Sunscorch Regent — {3}{W}{W} — Creature — Dragon · 4/3

Flying. *"Whenever an opponent casts a spell, put a +1/+1 counter on this creature and you gain 1 life."*

**When to play it:** Turn 5 in a game with three opponents — in a normal four-player game this grows
several times per turn cycle for free, with no work from you.

**Watch out:** 4/3 is a fragile body for five mana until it grows. It grows on **opponents'** spells
only, not yours.

#### Kimahri, Valiant Guardian — {2}{G}{U} — Legendary Creature — Cat Warrior · 3/3

Vigilance. **Ronso Rage** — at the beginning of combat on your turn, put a +1/+1 counter on Kimahri and
tap target creature an opponent controls. Then you may have Kimahri become a copy of that creature,
except its name is Kimahri, Valiant Guardian and it has vigilance and this ability.

**When to play it:** Turn 4. Every turn it taps down a potential blocker *and* grows, which is already
good; the copy mode lets you steal the best creature on the board (as a copy) while keeping the ability.

**Watch out:** Copying is a trap as often as it is a bonus. Kimahri **keeps** the +1/+1 counters already
on it — counters live on the permanent and copy effects do not touch them — but its **base** power and
toughness become the copied creature's, and it does **not** gain the counters the copied creature had.
So copying a 2/2 while Kimahri has four counters turns your 7/7 into a 6/6. Only copy something whose
printed abilities you actually want. And if the copy target becomes illegal, you get nothing at all —
not even the counter.

**Rulings:**
- *"If the target creature is an illegal target as Kimahri's last ability tries to resolve, it won't
  resolve and none of its effects will happen. You won't put a counter on Kimahri, and Kimahri won't
  become a copy of anything."*
- *"Kimahri copies exactly what was printed on the original creature, with the listed exceptions... It
  doesn't copy whether that creature is tapped or untapped, whether it has any counters on it or any
  Auras or Equipment attached to it."*
- *"If the copied creature has {X} in its mana cost, X is 0."*

#### Altered Ego — {X}{2}{G}{U} — Creature — Shapeshifter · 0/0

*"This spell can't be countered."* You may have it enter as a copy of any creature on the battlefield,
except it enters with X **additional** +1/+1 counters on it.

**When to play it:** Late, with X = 3 or more, copying the strongest creature on the table (yours or an
opponent's). Copying your own `Wakka` or an opponent's bomb are both fine.

**Watch out:** If you copy nothing it enters as a 0/0 and dies immediately (CR **704.5f**). Also, if you
copy one of **your** legendary creatures you must immediately put one of them in the graveyard — the
legend rule (CR **704.5j**). Copy an opponent's legend, or a nonlegendary creature.

**Rulings:**
- *"You can choose not to copy anything. In that case, Altered Ego enters as a 0/0 creature and is
  probably put into the graveyard immediately. It won't have +1/+1 counters placed on it by its ability."*
- *"X can be 0. Altered Ego won't enter with any additional +1/+1 counters."*
- *"Altered Ego copies exactly what was printed on the original creature... It doesn't copy whether
  that creature is tapped or untapped, whether it has any counters on it."*
- *"Any 'enters' abilities of the copied creature will trigger when Altered Ego enters the battlefield."*
- *"If Altered Ego somehow enters at the same time as another creature, Altered Ego can't become a copy
  of that creature."*

#### Summon: Magus Sisters — {4}{G} — Enchantment Creature — Saga Faerie · 5/5

A Saga with **haste** (it can attack the turn it arrives), sacrificed after chapter III. Chapters I, II
and III each **choose one at random**:
- **Combine Powers!** — Put three +1/+1 counters on target creature.
- **Defense!** — Put a shield counter on target creature. You gain 3 life. (A shield counter replaces
  the next destruction or damage: *"If this permanent would be destroyed as the result of an effect,
  instead remove a shield counter from it"* and *"If damage would be dealt to this permanent, prevent
  that damage and remove a shield counter from it"* — CR **122.1c**.)
- **Fight!** — This creature fights up to one target creature an opponent controls (each deals damage
  equal to its power to the other).

**When to play it:** Turn 5 as a hasty 5/5 that immediately starts attacking, with three rounds of
random value on top.

**Watch out:** You do **not** choose the mode — it is random, and the mode is picked before targets.
"Fight!" can get your 5/5 killed by a bigger creature. If the board is dangerous, consider whether you
want to commit it at all.

**Rulings:**
- *"As you put one of Summon: Magus Sisters's chapter abilities on the stack, you choose a mode at
  random. Players can respond to the ability knowing which mode was chosen."*
- *"The random choice of mode for Summon: Magus Sisters's chapter abilities is made before targets are
  chosen."*
- *"In the incredibly rare case where there is no legal target for the first or second mode, those
  modes can't be chosen at random. Since the third mode doesn't require a target, it is always eligible."*

#### Sin, Unending Cataclysm — {5}{G}{U} — Legendary Creature — Leviathan Avatar · 5/5

Flying, trample. *"As Sin enters, remove all counters from any number of artifacts, creatures, and
enchantments. Sin enters with X +1/+1 counters on it, where X is **twice** the number of counters
removed this way."* And when it dies, put its counters on target creature you control, then shuffle
this card into its owner's library.

**When to play it:** The deck's top of the curve at 7 mana — the only card above mana value 6. Cast it
when your board is loaded with counters; strip them all off and Sin arrives at double the size, with
flying and trample. A 5/5 that eats 8 counters becomes a 21/21 flier.

**Watch out:** You are gutting your own board to do it. Every creature you strip loses its counters —
which means they now die to your own `Damning Verdict`, lose `Sphere Grid`'s reach and trample, and
stop triggering `Bred for the Hunt`. Only do this when one huge flying trampler wins the game.

**Rulings:**
- *"Sin's last ability puts all counters that were on Sin onto the target creature, not just its +1/+1
  counters."*
- *"Sin's last ability doesn't cause you to move counters from Sin onto the target creature. Rather, you
  put the same number of each kind of counter Sin had when it died onto the target creature."*
- *"If the target creature is an illegal target as Sin's last ability tries to resolve, it won't resolve
  and none of its effects will happen. Sin will remain in the zone it went to when it died."*

---

## 7. Synergy Pieces — the actual engine

This is the deck. Everything here either **makes** counters, **multiplies** counters, or **converts**
counters into an advantage. If you have to keep one section, keep this one.

#### Hardened Scales — {G} — Enchantment

*"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1
counters are put on it instead."*

**When to play it:** Turn 1, every time. One mana, and it silently upgrades every counter effect in the
deck for the rest of the game. `Generous Patron`'s support 2 becomes two +2/+2 hand-outs.
`Duskshell Crawler` puts two counters. Proliferate is **not** affected (see below), but almost
everything else is.

**Watch out:** Two things beginners get wrong.
1. It only affects **+1/+1** counters, and only on **creatures you control** — not shield counters, not
   stun counters, not lore counters, not charge counters on `Everflowing Chalice`.
2. It says "that many **plus one**," not "twice as many." Three counters become four, not six.

Also: proliferate adds *one counter of each kind already there*; that is still "one or more +1/+1
counters put on a creature you control," so Hardened Scales **does** upgrade proliferate to two.

**Rulings:**
- *"If a creature you control would enter the battlefield with a number of +1/+1 counters on it, it
  enters with that many plus one instead."* — `Walking Ballista` cast for X=2 arrives as a 3/3.
- *"If two or more effects attempt to modify how many counters would be put on a creature you control,
  you choose the order to apply those effects, no matter who controls the sources of those effects."*
- *"Each additional Hardened Scales you control will increase the number of +1/+1 counters placed on a
  creature you control by one."* (Singleton deck — you will only ever have one.)

#### Sphere Grid — {1}{G} — Enchantment

*"Whenever a creature you control deals combat damage to a player, put a +1/+1 counter on that
creature."* Plus **Unlock Ability** — *"Creatures you control with +1/+1 counters on them have reach and
trample."*

**When to play it:** Turn 2. It is the deck's best two-mana card. It turns every connection into
permanent growth, and it hands your whole team **trample** — which is exactly what a counters deck
needs, because trample means a 9/9 blocked by a 1/1 still sends 8 damage to the player (CR **702.19b**).

**Watch out:** Combat damage **to a player** only. Also, the reach/trample grant requires a **+1/+1**
counter specifically — a creature with only a shield counter gets nothing.

**Rulings:** *"Once a creature that has reach because of Sphere Grid's last ability has blocked a
creature, removing all +1/+1 counters from that creature or causing Sphere Grid to leave the
battlefield won't cause that creature to stop blocking."*

#### Duskshell Crawler — {1}{G} — Creature — Insect · 0/3

When it enters, put a +1/+1 counter on target creature. *"Each creature you control with a +1/+1 counter
on it has trample."*

**When to play it:** Turn 2, targeting whichever creature most wants to be bigger. The static trample
grant is the real value — it stacks in function with `Sphere Grid` and means your growing creatures
cannot be chump-blocked into irrelevance by a 1/1.

**Watch out:** It is a 0/3 and can target *itself* with the enters trigger, making it a 1/4 with trample
— usually correct if you have nothing better.

#### Grateful Apparition — {1}{W} — Creature — Spirit · 1/1

Flying. *"Whenever this creature deals combat damage to a player or planeswalker, proliferate."*

**When to play it:** Turn 2. A 1/1 flier is very hard for most decks to block, so this is close to a
guaranteed proliferate every turn — and unlike your commander's Cheer it has **no once-per-turn limit**.

**Watch out:** It has no counter of its own at first, so proliferating does not grow it until someone
gives it a counter. Give it one (Tidus's move, `Together Forever`, `Blitzball Stadium`) and it snowballs.

**Rulings:**
- *"To proliferate, you can choose any permanent that has a counter, including ones controlled by
  opponents."*
- *"An ability that triggers 'Whenever you proliferate' triggers even if you chose no permanents or
  players while doing so."*
- *"If a permanent ever has both +1/+1 counters and -1/-1 counters on it at the same time, they're
  removed in pairs as a state-based action so that the permanent has only one of those kinds of counters
  on it."* (Also CR **122.3**.)

#### Shelinda, Yevon Acolyte — {G}{W} — Legendary Creature — Human Cleric · 2/2

Lifelink (damage it deals also gains you that much life — CR **702.15**). *"Whenever another creature
you control enters, put a +1/+1 counter on that creature if its power is less than Shelinda's power.
Otherwise, put a +1/+1 counter on Shelinda."*

**When to play it:** Turn 2. It is a free +1/+1 counter on **every** creature you play for the rest of
the game, in one direction or the other — there is no "nothing happens" case.

**Watch out:** The comparison is against Shelinda's **current** power, which grows. Once Shelinda is
large, small creatures get the counter; while she is small, she absorbs them. That is fine either way,
but it means you cannot always choose where the counter lands.

#### Maester Seymour — {2}{G} — Legendary Creature — Human Elf Cleric · 1/3

*"At the beginning of combat on your turn, put a number of +1/+1 counters equal to Maester Seymour's
power on **another** target creature you control."* Plus `{3}{G}{G}: Monstrosity X, where X is the
number of counters among creatures you control` — monstrosity N means *"If this permanent isn't
monstrous, put N +1/+1 counters on it and it becomes monstrous"* (CR **701.37a**).

**When to play it:** Turn 3. It starts small (power 1 = one counter per turn) but the monstrosity
ability is a huge one-shot: count every counter across your creatures and add that many to Seymour.

**Watch out:**
- It must target **another** creature — Seymour cannot grow itself with the combat trigger.
- **Monstrosity only works once ever** (CR **701.37b**). Do not fire it early for 3; wait until your
  board has 8+ counters.
- Its combat trigger and Tidus's combat trigger both happen at the beginning of combat — you choose the
  order they go on the stack, and the last one you put on the stack resolves first.

**Rulings:**
- *"The value of X is determined only once, as Maester Seymour's last ability resolves."*
- *"If Maester Seymour is no longer on the battlefield when its first ability resolves, use its power as
  it last existed on the battlefield to determine how many +1/+1 counters to put on the target creature."*
- *"Once a creature becomes monstrous, it can't become monstrous again. If the creature is already
  monstrous when the monstrosity ability resolves, nothing happens."*
- *"Monstrous isn't an ability that a creature has. It's just something true about that creature."*

#### Rikku, Resourceful Guardian — {2}{U} — Legendary Creature — Human Artificer · 2/3

*"Whenever you put one or more counters on a creature, until end of turn, that creature can't be blocked
by creatures your opponents control."* Plus **Steal** — `{1}, {T}: Move a counter from target creature
an opponent controls onto target creature you control. Activate only as a sorcery.`

**When to play it:** Turn 3, and then never let her die. Rikku is the card that converts "my creatures
are big" into "my creatures connect." Any counter — including one Tidus **moves** at the beginning of
combat — makes that creature unblockable for the turn. Combined with `Sphere Grid`, `Bred for the Hunt`
and Cheer, this is the deck's actual value loop.

**Watch out:**
- Order matters: put the counters on **before** blockers are declared. Once a creature has been blocked,
  making it unblockable does nothing.
- "Can't be blocked by creatures **your opponents** control" — it does not grant evasion against
  anything else, and it lasts only until end of turn.
- Steal is sorcery-speed only (your main phase, empty stack).

**Rulings:**
- *"To move a counter from one permanent to another, the counter is removed from the first permanent and
  put on the second. Any abilities that care about a counter being removed from or put onto a permanent
  will apply."* — this is why Tidus's move triggers Rikku.
- *"Once a creature has been blocked, Rikku's first ability won't cause it to become unblocked."*

#### Tromell, Seymour's Butler — {2}{G} — Legendary Creature — Elf Advisor · 2/3

*"Each other nontoken creature you control enters with an additional +1/+1 counter on it."* Plus
`{1}, {T}: Proliferate X times, where X is the number of nontoken creatures you control that entered
this turn.`

**When to play it:** Turn 3, before you deploy the rest of your creatures — the static ability is a
permanent upgrade to every creature you cast after it.

**Watch out:** **Nontoken** only. Your Squid tokens from `Chasm Skulker` and Spirit tokens from
`Summoner's Sending` do not benefit. And the proliferate ability counts creatures that entered **this
turn** — activate it late in a turn where you deployed two or three creatures, not on an empty turn
(X = 0 means you proliferate zero times).

**Rulings:**
- *"The value of X is determined only once, as Tromell's last ability resolves. To determine that value,
  look at the nontoken creatures you control and count each one that entered this turn."*
- *"If you proliferate multiple times, you don't have to choose the same set of players and/or permanents
  to get additional counters each time."*
- *"While proliferating multiple times, players can't respond between proliferating the first time and
  proliferating the second time, and so on."*

#### Forgotten Ancient — {3}{G} — Creature — Elemental · 0/3

*"Whenever a player casts a spell, you may put a +1/+1 counter on this creature."* Plus *"At the
beginning of your upkeep, you may move any number of +1/+1 counters from this creature onto other
creatures."*

**When to play it:** Turn 4. In a four-player game it collects a counter off **every** spell anyone
casts — it is routinely a 6/9 or bigger by your next turn — and then redistributes those counters across
your whole team each upkeep.

**Watch out:** It is a 0/3 until it accumulates counters. And redistribution happens at your **upkeep**,
which is before your draw step and long before combat — plan a turn ahead.

**Rulings:**
- *"Forgotten Ancient's first ability will resolve before the spell that caused it to trigger. Putting a
  +1/+1 counter on Forgotten Ancient is optional."*
- *"Forgotten Ancient's last ability doesn't target any creatures. You choose how many +1/+1 counters
  will be moved (and onto which creatures) as the ability resolves. Notably, once the ability starts
  resolving and you make these choices, no player may take actions until the ability has finished
  resolving."* — this means the redistribution **cannot be responded to** once it starts.

#### Path of Discovery — {3}{G} — Enchantment

*"Whenever a creature you control enters, it **explores**."* To explore: reveal the top card of your
library; if it is a land card, put it into your hand; otherwise put a +1/+1 counter on the exploring
creature and you may put the revealed card into your graveyard (CR **701.44a**).

**When to play it:** Turn 4 in a creature-heavy hand. With 34 creatures and 37 lands, every creature you
play is either a free land or a free counter — never nothing.

**Watch out:** Putting the revealed non-land card in the graveyard is **optional and usually wrong** —
you normally want to leave it on top and draw it. Read carefully before shipping a good card to the bin.

**Rulings:** *"Path of Discovery's triggered ability triggers along with any other abilities that say
that the creature explores when it enters the battlefield... You may take actions between each resolving
ability's exploration."*

#### Fight Rigging — {2}{G} — Enchantment

**Hideaway 5** — when it enters, look at the top five cards of your library, exile one face down, then
put the rest on the bottom in a random order (CR **702.75a**). Then: *"At the beginning of combat on
your turn, put a +1/+1 counter on target creature you control. Then if you control a creature with power
7 or greater, you may play the exiled card without paying its mana cost."*

**When to play it:** Turn 3. Even if you never unlock the free card, "a free +1/+1 counter at the
beginning of every combat" is worth three mana in this deck.

**Watch out:** The free-cast condition needs a creature with **power 7 or greater** — that is a real
ask; realistically it comes online around turn 7+ with `Wakka`, `Maester Seymour` post-monstrosity, or
a grown `Forgotten Ancient`. Pick the most expensive card you see when you hideaway, since you get it
for free. Also, "put the rest on the bottom in a **random** order" — you cannot stack your library.

**Rulings:**
- *"Any player who has controlled a permanent with a hideaway ability since a card was exiled with it
  may look at that card."*
- *"Hideaway now causes you to put the rest of the cards on the bottom of your library in a random order
  instead of any order."*

#### Resourceful Defense — {2}{W} — Enchantment

*"Whenever a permanent you control leaves the battlefield, if it had counters on it, put those counters
on target permanent you control."* Plus `{4}{W}: Move any number of counters from target permanent you
control onto a second target permanent you control.`

**When to play it:** Turn 3 as insurance. It makes removal and board wipes far less painful — every
countered creature that dies hands its counters to something else. Together with `Yuna, Grand Summoner`
you get **both** effects off the same death.

**Watch out:** The counters go on a **permanent**, not necessarily a creature. Putting +1/+1 counters on
a land does nothing (CR **122.1a** only adds power/toughness to creatures) — but a **keyword counter**
would still grant the keyword (CR **122.1b**), and the counter still counts for `Damning Verdict`.
The `{4}{W}` ability is expensive; treat it as a late-game mana sink.

#### Inexorable Tide — {3}{U}{U} — Enchantment

*"Whenever you cast a spell, proliferate."*

**When to play it:** Turn 5 when you still have cheap spells left to cast. Every instant, sorcery,
creature, artifact and enchantment you cast afterwards proliferates your whole board.

**Note:** playing a **land does not** trigger it. *"Playing a land is a special action; it doesn't use
the stack... Since the land doesn't go on the stack, it is never a spell"* (CR **305.1**).

**Watch out:** Five mana and it does nothing by itself the turn it lands. It is at its best in a
mid-game with a wide countered board, not as a topdeck when you are behind.

**Rulings:** *"Whenever you cast a spell, Inexorable Tide's ability triggers and goes on the stack on
top of it. It will resolve (and you'll proliferate) before the spell resolves."*

---

## 8. Utility & Protection

Cards whose job is to keep your board — and therefore your counters — alive.

#### Inspiring Call — {2}{G} — Instant

*"Draw a card for each creature you control with a +1/+1 counter on it. Those creatures gain
indestructible until end of turn."* Indestructible means the permanent can't be destroyed by damage or
by an effect that says "destroy" (CR **702.12**).

**When to play it:** This is the single best instant in the deck. Cast it **in response to** an
opponent's board wipe (while their `Wrath`-style spell is on the stack but before it resolves) — your
countered creatures survive **and** you draw four or five cards. Also fine as a combat trick to blow out
a block.

**Watch out:** Only creatures with **+1/+1 counters** are protected and only they draw cards.
Indestructible does **not** stop exile (`Farewell`, `Path to Exile`), sacrifice
(`Promise of Loyalty`), or -X/-X effects that reduce toughness to 0.

**Rulings:**
- *"Creatures you control that have +1/+1 counters put on them after Inspiring Call resolves won't gain
  indestructible."*
- *"Once a creature gains indestructible, it will have it for the turn, even if it loses all its +1/+1
  counters."*

#### Protection Magic — {1}{W} — Instant

Put a **shield counter** on each of up to three target creatures. A shield counter creates *"If this
permanent would be destroyed as the result of an effect, instead remove a shield counter from it"* and
*"If damage would be dealt to this permanent, prevent that damage and remove a shield counter from it"*
(CR **122.1c**).

**When to play it:** Two mana at instant speed to save three creatures from a wipe or a removal spell.
Equally important in this deck: it is a cheap way to put **counters** on three creatures right before
you cast `Damning Verdict`, or to switch on your commander's Cheer.

**Watch out:** Each shield counter absorbs exactly **one** event, then is gone.

**Rulings:**
- *"If a permanent that would be dealt damage has more than one shield counter on it, that damage is
  prevented and only one shield counter is removed."*
- *"Shield counters don't prevent players from sacrificing creatures."*
- *"A creature with a shield counter on it may still be destroyed by state-based actions if it has
  damage marked on it equal to its toughness or has been dealt unpreventable damage by a source with
  deathtouch."*
- *"'Shield' is not an ability that creatures have and shield counters are not keyword counters."*

#### Gatta and Luzzu — {2}{W} — Legendary Creature — Human Soldier · 1/1

**Flash** — you may cast it any time you could cast an instant (CR **702.8**). When it enters, choose
target creature you control; if damage would be dealt to that creature this turn, prevent that damage
and put that many +1/+1 counters on it instead.

**When to play it:** Flash it in **during combat**, after blockers are declared. Your 4/4 blocked by a
6/6 takes no damage and becomes a 10/10. It is a combat trick, a removal answer (against damage-based
removal), and a counter engine in one card.

**Watch out:** It only prevents **damage**, not "destroy" effects. And it is a 1/1 body, so it is not
holding the ground itself.

**Rulings:** *"If damage that can't be prevented is dealt to the target creature after Gatta and Luzzu's
last ability resolves, you still put that many +1/+1 counters on it."*

#### Together Forever — {W}{W} — Enchantment

When it enters, **support 2** (a +1/+1 counter on each of up to two target creatures — CR **701.41a**).
Then `{1}: Choose target creature with a counter on it. When that creature dies this turn, return that
card to its owner's hand.`

**When to play it:** Turn 2. The enters trigger alone is fine; the activated ability is the important
part — one mana to make any countered creature "die, come back to hand, recast later."

**Watch out:** It returns the creature to your **hand**, not the battlefield, and only for creatures
that die **this turn**. It also works on creature **cards** only — token creatures cease to exist.

**Rulings:**
- *"Together Forever's activated ability checks whether the target creature has a counter on it as the
  ability is activated and as the ability resolves. If the creature loses its counters later in the
  turn, the delayed triggered ability will still return it to its owner's hand when it dies."*
- *"You can't put more than one +1/+1 counter on any one target using the support action."*
- *"Support can target a creature another player controls."*
- *"If a creature without counters receives enough -1/-1 counters to reduce its toughness to 0 or less,
  Together Forever's ability can't be activated before state-based actions put that creature into its
  owner's graveyard."*

#### Luminous Broodmoth — {2}{W}{W} — Creature — Insect · 3/4

Flying. *"Whenever a creature you control without flying dies, return it to the battlefield under its
owner's control with a **flying counter** on it."* A keyword counter grants that keyword (CR **122.1b**).

**When to play it:** Turn 4. It makes your entire ground board effectively die-once-for-free, and every
creature that comes back has a **counter** on it — which means it survives your `Damning Verdict`,
switches on Cheer, and triggers `Rikku`.

**Watch out:** Only creatures **without flying**, and the returned creature comes back **fresh** — it
loses all the +1/+1 counters it had. Broodmoth itself has flying, so it does not recur itself (unless it
somehow loses flying first).

**Rulings:**
- *"If Luminous Broodmoth dies at the same time as a creature without flying, its ability triggers for
  that creature."*
- *"Luminous Broodmoth's ability triggers if a token creature without flying dies, but the token won't
  be returned to the battlefield."*
- *"If Luminous Broodmoth dies after losing flying but not losing its triggered ability, its ability
  will trigger for itself."*

#### Summoner's Sending — {1}{W} — Enchantment

*"At the beginning of your end step, you may exile target creature card from a graveyard. If you do,
create a 1/1 white Spirit creature token with flying. Put a +1/+1 counter on it if the exiled card's
mana value is 4 or greater."*

**When to play it:** Turn 2. It is graveyard hate (stopping opponents reanimating creatures) that also
builds you a free 1/1 flier every single turn, forever.

**Watch out:** "**a** graveyard" includes yours — do not exile your own good creature when an opponent's
graveyard has a better target. The token only gets a counter if the exiled card had mana value 4 or
more; the average non-land mana value in this deck is 3.03, so aim at opponents' expensive creatures.
Note tokens are **not** helped by `Tromell` (which says nontoken).

**Rulings:** *"If the exiled card has {X} in its mana cost, X is 0 for the purpose of determining its
mana value."*

---

## 9. Lands

37 lands total (31 distinct entries below). **16 of them can enter tapped** (8 always, 8 conditionally)
— that is 43% of your mana base and the main reason this deck's early turns can feel slow. Sequencing
matters: play your always-tapped lands on turns where you were not going to use all your mana anyway.

### Basic lands — 9 total

#### Forest ×3 · Island ×3 · Plains ×3 — Basic Land

`Forest` taps for `{G}`, `Island` for `{U}`, `Plains` for `{W}`. Nine basics is a low count for a
three-colour deck, which matters because several of your own cards look for them:
`Farseek` (Plains/Island only — it cannot find a Forest), `Three Visits` (Forest),
`Evolving Wilds`, `Ash Barrens`, `Rampant Rejuvenator`, and `Path to Exile` when an opponent uses it.
It also matters for `Canopy Vista` and `Prairie Stream`, which check whether you control **two or more
basic lands**.

**Watch out:** Cards with basic land **types** — `Canopy Vista` (Land — Forest Plains), `Prairie Stream`
(Land — Plains Island), `Idyllic Beachfront` (Land — Plains Island), `Radiant Grove` (Land — Forest
Plains), `Tangled Islet` (Land — Forest Island) — are **not** basic lands. Per the official ruling on
Canopy Vista: *"Even though these lands have basic land types, they are not basic lands because 'basic'
doesn't appear on their type line."*

### Any-colour and fixing lands

#### Command Tower — Land

`{T}: Add one mana of any color in your commander's color identity` — green, white, or blue for you.
Enters untapped. The single best land in the deck; there is no downside.

#### Exotic Orchard — Land

`{T}: Add one mana of any color that a land an opponent controls could produce.`

**Watch out:** It depends entirely on your **opponents'** lands. In a three-opponent game it is
usually excellent; against a mono-colour opponent whose colour you don't need, it can be dead.

**Rulings:** *"Exotic Orchard checks the effects of all mana-producing abilities of lands your opponents
control, but it doesn't check their costs."* / *"Exotic Orchard can't be tapped for colorless mana, even
if a land an opponent controls could produce colorless mana."*

#### Seaside Citadel — Land

`This land enters tapped. {T}: Add {G}, {W}, or {U}.` Perfect fixing, always a turn late.

**When to play it:** On a turn where you are not spending all your mana, or turn 1 off a hand with no
one-drop.

#### Path of Ancestry — Land

Enters tapped. `{T}: Add one mana of any color in your commander's color identity. When that mana is
spent to cast a creature spell that shares a creature type with your commander, scry 1` (scry 1 = look
at the top card of your library and you may put it on the bottom — CR **701.22**).

**Watch out:** Your commander is a **Human Warrior**. The scry only happens for creature spells sharing
one of those types. In this deck that is a fairly narrow set — check the type line before expecting it.

**Rulings:** *"Your commander's creature types are checked immediately after you cast a creature spell
spending mana from Path of Ancestry's last ability."*

### Lands that check a condition to enter untapped

These eight are the "conditional tapped" lands. Read each condition — sequencing your lands correctly is
free value.

#### Canopy Vista — Land — Forest Plains

`({T}: Add {G} or {W}.) This land enters tapped unless you control two or more basic lands.`

**Watch out:** You only run 9 basics, so this often enters tapped. It **has** the Forest and Plains
types, so `Three Visits` and `Farseek` can both fetch it.

**Rulings:** *"If one of these lands enters the battlefield at the same time as any number of basic
lands, those other lands are not counted when determining if this land enters the battlefield tapped."*

#### Prairie Stream — Land — Plains Island

`({T}: Add {W} or {U}.) This land enters tapped unless you control two or more basic lands.`
Same condition and same caveats as `Canopy Vista`. Fetchable with `Farseek`.

#### Glacial Fortress — Land

`This land enters tapped unless you control a Plains or an Island. {T}: Add {W} or {U}.`

**Rulings:** *"This checks for lands you control with the land type Plains or Island, not for lands named
Plains or Island. The lands it checks for don't have to be basic lands."* So `Prairie Stream` or
`Idyllic Beachfront` turn it on. *"As this is entering, it checks for lands that are already on the
battlefield."*

#### Hinterland Harbor — Land

`This land enters tapped unless you control a Forest or an Island. {T}: Add {G} or {U}.`
Same style of check as `Glacial Fortress` — any land with the Forest or Island **type** counts.

#### Sunpetal Grove — Land

`This land enters tapped unless you control a Forest or a Plains. {T}: Add {G} or {W}.`

**Rulings:** *"This checks for lands you control with the land type Forest or Plains, not for lands named
Forest or Plains. The lands it checks for don't have to be basic lands."*

#### Fortified Village — Land

`As this land enters, you may reveal a Forest or Plains card from your hand. If you don't, this land
enters tapped. {T}: Add {G} or {W}.`

**Watch out:** You reveal from **hand** — this is the "reveal" style, not the "control" style. Holding a
basic Forest in hand is what makes it untapped.

**Rulings:** *"Lands don't have a subtype just because they can produce mana of the corresponding color.
Fortified Village itself is neither a Forest nor a Plains, even though it produces green and white mana,
so you can't reveal one to satisfy the ability of another."*

#### Port Town — Land

`As this land enters, you may reveal a Plains or Island card from your hand. If you don't, this land
enters tapped. {T}: Add {W} or {U}.` Same reveal-from-hand mechanic as `Fortified Village`.

**Rulings:** *"You may reveal any land card with either or both of the appropriate subtypes. It doesn't
have to be a basic land."*

#### Vineglimmer Snarl — Land

`As this land enters, you may reveal a Forest or Island card from your hand. If you don't, this land
enters tapped. {T}: Add {G} or {U}.`

**Rulings:** *"The 'Snarl' itself doesn't have any land subtypes. You can't reveal one to satisfy the
ability of another."*

### Lands that always enter tapped

#### Idyllic Beachfront — Land — Plains Island

`({T}: Add {W} or {U}.) This land enters tapped.` Always tapped, but it carries the Plains and Island
types, so `Farseek` can fetch it straight onto the battlefield.

#### Radiant Grove — Land — Forest Plains

`({T}: Add {G} or {W}.) This land enters tapped.` Carries the Forest and Plains types — fetchable with
`Three Visits` (Forest) or `Farseek` (Plains).

#### Tangled Islet — Land — Forest Island

`({T}: Add {G} or {U}.) This land enters tapped.` Carries the Forest and Island types — fetchable with
`Three Visits` or `Farseek`.

#### Temple of Enlightenment — Land

`This land enters tapped. When this land enters, scry 1. {T}: Add {W} or {U}.`

**Rulings:** *"When you scry, you may put all the cards you look at back on top of your library, you may
put all of those cards on the bottom of your library, or you may put some of those cards on top and the
rest of them on the bottom."*

#### Temple of Mystery — Land

`This land enters tapped. When this land enters, scry 1. {T}: Add {G} or {U}.` Same as above.

#### Temple of Plenty — Land

`This land enters tapped. When this land enters, scry 1. {T}: Add {G} or {W}.` Same as above.
**When to play it:** These three Temples are your best turn-1 plays when your hand has no one-mana spell
— the scry smooths your draws and the tapped land costs you nothing on turn 1.

### Pain, filter, and utility lands

#### Brushland — Land

`{T}: Add {C}.` or `{T}: Add {G} or {W}. This land deals 1 damage to you.` Untapped, always. The 1
damage is a real cost but small against a 40-life starting total (CR **903.7**).

#### Flooded Grove — Land

`{T}: Add {C}.` or `{G/U}, {T}: Add {G}{G}, {G}{U}, or {U}{U}.`

**Watch out:** The second ability is a **filter**: you must spend a green or blue mana to get two mana
back. It does not fix from nothing — you need another green or blue source already.

#### Overflowing Basin — Land

`{1}, {T}: Add {G}{U}.` Costs a generic mana to make two coloured ones — net zero mana, pure fixing.
Useless as your only land on turn 1 (you have no mana to pay the {1}).

#### Skycloud Expanse — Land

`{1}, {T}: Add {W}{U}.` Same shape as `Overflowing Basin`, for white and blue.

#### Sungrass Prairie — Land

`{1}, {T}: Add {G}{W}.` Same shape, for green and white.

#### Temple of the False God — Land

`{T}: Add {C}{C}. Activate only if you control five or more lands.`

**Watch out:** This is the most dangerous land in the deck for a new player. Until you have **five**
lands it produces **nothing at all** — it is a blank card that does not even tap for one colourless.
And it never makes coloured mana. Play it late, not early.

#### Forge of Heroes — Land

`{T}: Add {C}.` or `{T}: Choose target commander that entered this turn. Put a +1/+1 counter on it if
it's a creature and a loyalty counter on it if it's a planeswalker.`

**When to play it:** Hold it for the turn you cast Tidus — he arrives with a +1/+1 counter, which
immediately makes him a legal source for his own move ability and turns on everything that cares about
counters.

**Watch out:** The commander must have entered **this turn**, and it can target any player's commander.

**Rulings:** *"If the target commander is somehow neither a creature nor a planeswalker…, it receives no
counters."*

#### Nesting Grounds — Land

`{T}: Add {C}.` or `{1}, {T}: Move a counter from target permanent you control onto a second target
permanent. Activate only as a sorcery.`

**When to play it:** This is a genuine engine land — a second, repeatable version of your commander's
move ability, on a land, that survives creature removal.

**Watch out:** Sorcery-speed only. Also note the **second** target is just "a permanent," not
"a permanent you control" — so you can move a bad counter (a stun counter, a vow counter from
`Promise of Loyalty`) off your creature and onto an opponent's permanent.

**Rulings:**
- *"You choose the two target permanents as Nesting Grounds's second ability is put onto the stack. You
  choose which kind of counter to move as that ability resolves."*
- *"If either permanent becomes an illegal target, no counter is removed or put."*
- *"The two target permanents don't have to share a type, which can result in some counters on permanents
  that would not occur normally... +1/+1 counters won't affect the permanent unless it's a creature."*
- *"To move a counter from one creature to another, the counter is removed from the first permanent and
  put on the second. Any abilities that care about a counter being removed from or put onto a permanent
  will apply."* — so moving a counter with Nesting Grounds triggers `Rikku` and `Fathom Mage` too.

### Land-fetching lands

#### Evolving Wilds — Land

`{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield
tapped, then shuffle.`

**When to play it:** Turn 1 when you can afford the tempo loss, or any turn you need a specific colour.
It also triggers `Tireless Tracker`'s landfall a second time (once when Evolving Wilds enters, once when
the fetched land enters).

**Watch out:** It produces **no mana itself** and the fetched land arrives **tapped** — playing this on a
turn you need all your mana costs you a full land drop's worth of mana.

#### Ash Barrens — Land

`{T}: Add {C}.` plus **Basic landcycling {1}** — `{1}, Discard this card: Search your library for a basic
land card, reveal it, put it into your hand, then shuffle.`

**When to play it:** Two modes. Play it as a colourless land when you just need a land drop, or pay {1}
to discard it from hand and fetch the exact basic colour you are missing — that fetched land goes to
your **hand**, so you still get to play it untapped as your land for the turn.

**Watch out:** Landcycling is done from your hand, not the battlefield. Once Ash Barrens is on the
battlefield it is just a colourless land, and colourless mana cannot pay `{G}`, `{W}` or `{U}`.

---

## Completeness check

Every card in `./bin/mtg deck tidus` appears exactly once above, in exactly one section:

| Section | Distinct cards |
|---|---|
| Commander | 1 |
| Ramp & Mana | 10 |
| Card Draw & Selection | 11 |
| Removal & Interaction | 11 |
| Board Wipes | 4 |
| Threats & Beaters | 7 |
| Synergy Pieces | 13 |
| Utility & Protection | 6 |
| Lands | 31 (28 nonbasic + 3 basic names ×3 copies = 37 land cards) |
| **Total distinct** | **94** |
| **Total cards** | **100** (99 maindeck + commander) |

Re-run the check yourself any time:

```bash
cd /Users/omaralatas/Work/personal/mtg-brain
./bin/mtg deck tidus --json | python3 -c "
import json,sys,re
d=json.load(sys.stdin)['groups']
names=[c['name'] for v in d.values() for c in v]
txt=open('decks/tidus/CARDS.md').read()
missing=[n for n in names if n not in txt]
print('cards in deck:',len(names),'| missing from CARDS.md:',missing or 'none')
"
```
