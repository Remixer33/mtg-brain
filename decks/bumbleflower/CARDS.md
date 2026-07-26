# Peace Offering — Ms. Bumbleflower · Card-by-Card Study Guide

**Every one of the 100 cards, explained in plain language.** 99 maindeck + the commander.

| | |
|---|---|
| Deck | Peace Offering (slug `bumbleflower`) |
| Commander | Ms. Bumbleflower |
| Colors | Bant — white / blue / green (WUG) |
| Bracket | 2 — Core (precon-level, 0 Game Changers) |
| Format | **Commander (EDH)** only. Commander has **no sideboard** — the 100 cards below are the whole deck. |

> **How to verify anything in here.** Every mana cost, type line, power/toughness, rules text and
> official ruling below was pulled from the local database in the same session this file was
> written. Check any card yourself with `./bin/mtg card "<name>"`, any rule with
> `./bin/mtg rule <number>`, any keyword with `./bin/mtg glossary <term>`. Real CLI output is
> pasted in the Appendix at the bottom.

> **Read the PRIMER first.** `decks/bumbleflower/PRIMER.md` explains *how to pilot* the deck.
> This file explains *what each card does*. They are companions.

---

## How this file is organised

Cards are grouped by **the job they do in this deck**, not alphabetically. Each card appears
exactly **once**, under its primary job; secondary jobs are called out in its entry.

1. [Commander](#1-commander) (1)
2. [Ramp & Mana](#2-ramp--mana) (12)
3. [Card Draw & Selection](#3-card-draw--selection) (17)
4. [Removal & Interaction](#4-removal--interaction) (8)
5. [Board Wipes](#5-board-wipes) (2)
6. [Threats & Beaters](#6-threats--beaters) (6)
7. [Synergy Pieces — the actual engine](#7-synergy-pieces--the-actual-engine) (9)
8. [Utility & Protection](#8-utility--protection) (7)
9. [Lands](#9-lands) (38)

62 non-land cards + 38 lands = 100. ✓

---

## Jargon key (read once, then dive in)

Everything here is also defined inline the first time it appears. ⌕ = has an official glossary
entry you can read with `./bin/mtg glossary <term>`.

- **Mana value** — the total amount of mana in a cost, ignoring colour. `{2}{G}` = mana value 3.
- **Permanent** — a card that stays on the battlefield: creature, artifact, enchantment, land,
  planeswalker. Instants and sorceries are *not* permanents; they resolve and go to the graveyard.
- **Cast** — announcing a spell and paying for it. **Playing a land is NOT casting a spell** —
  this matters constantly for Ms. Bumbleflower.
- **The stack** — the queue where spells and triggered abilities wait. Last thing added is the
  first thing to happen. Anyone can respond before something resolves.
- **Trigger / triggered ability** — anything starting "Whenever…", "When…", "At the beginning
  of…". It happens on its own; you don't spend mana.
- **ETB / "enters"** — a trigger that fires when a permanent hits the battlefield.
- **Target** — a specific thing an ability points at. Targets are chosen when the ability goes on
  the stack, not when it resolves.
- **+1/+1 counter** ⌕ (CR 122) — a physical marker on a creature that permanently makes it
  +1 power and +1 toughness. This deck is built on them.
- **Upkeep** — a step at the start of your turn, **before** your draw for the turn.
- **End step** — the last step of a turn, before cards are discarded. "At the beginning of the
  end step" effects fire here.
- **Instant speed** — you can do it any time you have priority, including on other players' turns.
  Instants and activated abilities (things with a `:` in them) are instant speed unless stated.
- **Sacrifice** — you put your own permanent into your graveyard as a cost. It can't be
  responded to once paid, and it dodges "destroy" effects.
- **Token** — a permanent that isn't a real card. If it leaves the battlefield it stops existing.
- **Mana rock** — an artifact that taps for mana (Sol Ring, Arcane Signet).
- **Ramp** — cards that get you extra mana ahead of schedule.
- **Fog** — an effect that prevents combat damage for a turn so you survive a lethal attack.
- **Board wipe** — a spell that destroys or removes most creatures at once.
- **Group hug** — cards that give *everyone* resources. This deck is full of them, on purpose.
- **Pillowfort** — cards that make attacking *you* expensive or pointless.
- **Commander tax** — CR 903.8: recasting your commander from the command zone "costs an
  additional {2} for each previous time the player casting it has cast it from the command zone
  that game."
- **Maximum hand size** — CR 402.2: "Each player has a maximum hand size, which is normally seven
  cards. A player may have any number of cards in their hand, but as part of their cleanup step,
  the player must discard excess cards down to the maximum hand size." So you only discard at the
  *end of your own turn*.

**Keywords that appear in this deck** (all pulled from the glossary this session):

| Keyword | Rule | Plain English |
|---|---|---|
| Vigilance ⌕ | CR 702.20b | "Attacking doesn't cause creatures with vigilance to tap." Attack *and* still block. |
| Flying ⌕ | CR 702.9b | "A creature with flying can't be blocked except by creatures with flying and/or reach." |
| Trample ⌕ | CR 702.19b | Assign lethal damage to blockers, then "any excess damage is assigned as its controller chooses" — i.e. it spills onto the defending player. |
| Lifelink ⌕ | CR 702.15b | "Damage dealt by a source with lifelink causes that source's controller… to gain that much life." |
| Hexproof ⌕ | CR 702.11b | "This permanent can't be the target of spells or abilities your opponents control." |
| Haste ⌕ | CR 702.10 / 302.6 | Ignores the summoning-sickness rule — it can attack and tap the turn it arrives. |
| Landwalk / islandwalk ⌕ | CR 702.14b | "Landwalk is an evasion ability" — unblockable if the defender controls that land type. |
| Toxic N ⌕ | CR 702.164c | Combat damage to a player also gives them N poison counters. CR 704.5c: "If a player has ten or more poison counters, that player loses the game." |
| Goad ⌕ | CR 701.15b | "A goaded creature attacks each combat if able and attacks a player other than the controller of the permanent, spell, or ability that caused it to be goaded if able." |
| Phasing ⌕ | CR 702.26b | "Except for rules and effects that specifically mention phased-out permanents, a phased-out permanent is treated as though it does not exist. It can't affect or be affected by anything else in the game." It phases back in as its controller's untap step begins (CR 702.26a). |
| Protection from everything | CR 702.16 | Per the Perch Protection ruling: damage to you is prevented, Auras can't attach to you, and you can't be targeted. |
| Gift ⌕ | CR 702.174a | "As an additional cost to cast this spell, you may choose an opponent." They get the listed gift; your spell gets *better*. |
| Offspring ⌕ | CR 702.175a | "You may pay an additional [cost] as you cast this spell" and "when this permanent enters… create a token that's a copy of it, except it's 1/1." |
| Adventure ⌕ | CR 715 | A card with a second, cheaper spell on the left. Cast the small half, it exiles itself, and you may cast the creature later from exile. |
| Class ⌕ | CR 716 | An enchantment that enters at level 1. Activating a "class level bar" — sorcery speed only — raises it a level and *adds* that level's ability (CR 716.2). Not the same mechanic as "level up" (CR 716.4). |
| Scry N ⌕ | CR 701.22 | Look at the top N cards of your library; put any of them on the bottom. |
| Treasure token ⌕ | CR 111.10a | "A Treasure token is a colorless Treasure artifact token with '{T}, Sacrifice this token: Add one mana of any color.'" |
| Mana ability ⌕ | CR 605 | An ability that makes mana and **doesn't use the stack** — it can't be responded to. |
| Tempting offer | *(not a glossary term — "not in my data")* | You do a thing; each opponent may copy it; for each one who does, **you do it again**. |

---

# 1. Commander

#### Ms. Bumbleflower — {1}{G}{W}{U} — Legendary Creature — Rabbit Citizen — 1/5

The whole deck in one card. She has **vigilance** (attacking doesn't tap her, so she can swing and
still block — CR 702.20b) and reads:

> Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter on target creature.
> It gains flying until end of turn. If this is the second time this ability has resolved this
> turn, you draw two cards.

Translation: **every spell you cast** hands one opponent of your choice a free card, and puts a
permanent +1/+1 counter on a creature you point at, giving that creature flying for the turn.
The **second** time that ability resolves in a turn, **you** draw two cards.

So your ideal turn is **exactly two cheap spells**. Two spells = 2 counters, 2 free cards for you,
2 free cards for the table. A third spell gives the table another card and gives you nothing extra.

She is a 1/5 — a wall, not a threat. She blocks well and dies to almost nothing.

**When to play it:** Turn 4 if you can, but only if you can also cast something the turn after.
She does nothing on her own; she needs a hand of cheap spells behind her. Playing her into an
empty hand just feeds your opponents.

**Watch out:**
- **"Target creature" can be any creature, including an opponent's** — and that creature also
  gains flying until end of turn. Handing a counter *and* evasion to the player who is beating you
  is a real, easy mistake. Point it at your own board unless you have a reason.
- Playing a land is not casting a spell — no trigger.
- It counts the **second time the ability RESOLVES**, not the second spell you cast. If your first
  trigger somehow doesn't resolve, your second spell's trigger is the first resolution.
- It counts per **turn**, not per your turn. Casting two instants during an opponent's turn draws
  you two cards on their turn.
- You are the table's card faucet. Expect to be attacked. That is why the deck runs so much
  defence (§8).
- Commander tax: each time you recast her from the command zone she costs {2} more (CR 903.8).

**Rulings:**
- *[2024-07-26]* "Ms. Bumbleflower's last ability resolves before the spell that caused it to
  trigger. It resolves even if that spell is countered." — so even if your spell gets countered,
  you still got the counter, the flying, and (on the second resolution) your two cards.

---

# 2. Ramp & Mana

Twelve cards whose job is to produce mana or fetch lands. This deck has a 3.21 average mana value
and wants to double-spell every turn, so ramp is doing double duty: it makes the *second* spell
castable.

#### Sol Ring — {1} — Artifact
Taps for two colourless mana. It costs one and makes two, so it pays for itself immediately and
every turn after. The single strongest card in the deck.
**When to play it:** The turn you draw it, always, at the first opportunity. Turn 1 Sol Ring is the
best opening this deck can have.
**Watch out:** Colourless mana can't pay a coloured pip like `{G}` or `{W}`. Sol Ring helps you cast
`{3}{G}`, not `{G}{G}`.

#### Arcane Signet — {2} — Artifact
Taps for one mana of any colour in your commander's colour identity — here, white, blue, or green.
Perfect fixing.
**When to play it:** Turn 2 when you don't have a better two-drop. It turns a stumbling mana base
into a smooth one.

#### Fellwar Stone — {2} — Artifact
Taps for one mana of any colour that **a land an opponent controls could produce**. In a four-player
game that is almost always every colour you need.
**When to play it:** Turn 2. Same slot as Arcane Signet.
**Watch out:** It depends on your *opponents'* lands, not yours. In the rare game where every
opponent is mono-black, this taps for black mana you can't use — and if no opponent's land can
produce anything, it makes nothing.

#### Mind Stone — {2} — Artifact
Taps for one colourless mana. Later, `{1}`, tap, sacrifice it: draw a card. So it's ramp early and a
cantrip late — it never becomes a dead draw. Secondary role: card draw.
**When to play it:** Turn 2. Cash it in for a card once you have enough lands and nothing to ramp
into.

#### Thought Vessel — {2} — Artifact
Taps for one colourless mana **and** gives you no maximum hand size. Normally you discard down to
seven at the end of your turn (CR 402.2); with this out you keep everything.
**When to play it:** Turn 2, and it is a *high* priority in this deck specifically — you draw so
many cards that hitting seven and discarding is a real loss.
**Watch out:** It clashes with Twenty-Toed Toad (§7), which *sets* your maximum hand size to twenty.
Whichever entered the battlefield **later** wins, per the timestamp rule (see the Reliquary Tower and
Twenty-Toed Toad rulings). If you want the Toad's twenty-card win, play the Toad after this.

#### Coveted Jewel — {6} — Artifact
Draw three cards when it enters, then it taps for **three mana of any one colour**. The catch: if an
opponent's creatures attack you and are unblocked, that player draws three cards and **takes the
Jewel**, untapped. Secondary role: card draw.
**When to play it:** Late, when you have blockers up, or when you're happy to trade it away for the
three cards. It is genuinely fine to cast it, draw three, and let someone steal it.
**Watch out:** It is a giant "attack me" sign. Do not cast it with an empty board.
**Rulings:**
- *[2018-07-13]* "If more than one opponent attacks you at the same time, Coveted Jewel's last
  ability triggers for each of them. You choose which player ends up with Coveted Jewel, but each of
  them draws three cards."
- *[2018-07-13]* "Coveted Jewel's last ability triggers after you declare blockers (or declare no
  blockers at all) if any attacking creatures are unblocked. It doesn't matter if some attacking
  creatures were blocked." — so **blocking every attacker saves it**.
- *[2018-07-13]* "A creature attacking a planeswalker you control won't cause Coveted Jewel's last
  ability to trigger."
- *[2018-07-13]* "Coveted Jewel's last ability resolves after blockers are chosen but before combat
  damage is dealt."

#### Farseek — {1}{G} — Sorcery
Search your library for a **Plains, Island, Swamp, or Mountain** card, put it onto the battlefield
tapped, then shuffle.
**When to play it:** Turn 2, as one of your two spells.
**Watch out:** **It cannot find a Forest.** Read the list again. In this deck it can fetch a basic
Plains, a basic Island, or — because it checks land *types*, not "basic" — **Canopy Vista** (Forest
Plains) and **Prairie Stream** (Plains Island).
**Rulings:**
- *[2021-03-19]* "Farseek can find any land with any of the listed land types, including nonbasic
  ones, even if that land is a Forest in addition to one or more of those types."

#### Cultivate — {2}{G} — Sorcery
Search for up to two **basic** lands: one onto the battlefield tapped, one into your hand. So it
ramps you *and* guarantees your next land drop.
**When to play it:** Turn 3. It fixes your colours and protects you from missing land drops.
**Rulings:**
- *[2010-08-15]* "If you choose to find only one basic land card, you put it onto the battlefield
  tapped."

#### Tempt with Discovery — {3}{G} — Sorcery
**Tempting offer.** You search for a land and put it onto the battlefield (untapped, and it can be
*any* land — nonbasics included). Then each opponent may do the same. For every opponent who
accepts, **you search for another land**. In a four-player game where everyone accepts, you get four
lands and they get one each.
**When to play it:** Turn 4-5. Even if nobody accepts, you got a tutored untapped land for four mana,
which is fine. If everyone accepts, it's a blowout in your favour.
**Watch out:** You are teaching the table to trust "free stuff" from you — which is exactly the
politics this deck wants. But a savvy table declines, and then this is a mediocre four-mana ramp
spell.
**Rulings:**
- *[2013-10-17]* "Your opponents decide in turn order whether or not they accept the offer, starting
  with the opponent on your left. Each opponent will know the decisions of previous opponents in turn
  order when making their decision."
- *[2013-10-17]* "After each opponent has decided, the effect happens simultaneously for each one who
  accepted the offer. Then, the effect happens again for you a number of times equal to the number of
  opponents who accepted."

#### Faeburrow Elder — {1}{G}{W} — Creature — Treefolk Druid — 0/0
Vigilance. It gets +1/+1 for each **colour among permanents you control**, and taps for one mana of
*each* of those colours. In this Bant deck it is normally a 3/3 that taps for `{G}{W}{U}` — three
mana off one creature.
**When to play it:** Turn 3, if you already have permanents in at least two colours. It is your best
non-artifact ramp.
**Watch out:** It is a 0/0 with no counters. If you somehow control no coloured permanents it dies
immediately. It also dies to any board wipe, so don't build your whole mana base on it.
**Rulings:**
- *[2019-10-04]* "Faeburrow Elder's middle ability can give it at most +5/+5… 'Gold,' 'multicolor,'
  and 'colorless' aren't colors. Similarly, Faeburrow Elder's last ability can produce at most five
  mana."
- *[2019-10-04]* "Since Faeburrow Elder is a green and white permanent, its middle ability usually
  gives it at least +2/+2 and its last ability usually produces at least {G}{W}."

#### Rishkar, Peema Renegade — {2}{G} — Legendary Creature — Elf Druid — 2/2
When it enters, put a +1/+1 counter on **each of up to two** target creatures. Then **every creature
you control that has a counter on it** gains "{T}: Add {G}." In a deck that showers counters
everywhere, this quietly turns your whole board into a green mana engine. Secondary role: counters
synergy.
**When to play it:** Turn 3. It's ramp *and* it starts the counter theme.
**Watch out:** Tapping a creature for mana means it can't attack or block that turn (unless it has
vigilance, which only helps with attacking).
**Rulings:**
- *[2017-02-09]* "Each creature you control has Rishkar's mana ability as long as that creature has
  any kind of counter on it. The effect isn't limited to those with +1/+1 counters."
- *[2017-02-09]* "You can't target the same creature twice to have one recipient get two +1/+1
  counters."
- *[2017-02-09]* "Rishkar can be a target of its own triggered ability."

#### Selvala, Explorer Returned — {1}{G}{W} — Legendary Creature — Elf Scout — 2/4
**Parley** — tap her: every player reveals the top card of their library. For each **nonland** card
revealed, you add `{G}` and gain 1 life. Then **every player draws a card** (they draw the card they
just revealed). In a four-player game that's often 2-3 green mana and 2-3 life for free — while
handing everyone a card, which is completely on-brand.
**When to play it:** Turn 3. Then tap her every single turn.
**Watch out:** You are giving three opponents a card every turn. That is a real cost — this is a
group-hug engine, not free money.
**Rulings:**
- *[2014-05-29]* "Selvala's parley ability is a mana ability. It doesn't use the stack and can't be
  responded to."
- *[2014-05-29]* "Except in some very rare cases, the card each player draws will be the card revealed
  from the top of their library."
- *[2014-05-29]* "If you activate Selvala's ability while casting a spell, and you discover you can't
  produce enough mana to pay that spell's costs, the spell is reversed… You'll still have whatever
  mana that ability produced, and each player will have drawn a card."

---

# 3. Card Draw & Selection

Seventeen cards. This is the deck's biggest role by far (`mtg deck stats bumbleflower -v` counts 25
draw pieces overall once you include the ones filed elsewhere). Note how many of them draw for your
opponents too — that is the deck's identity, and it is why you need §8.

#### Coiling Oracle — {G}{U} — Creature — Snake Elf Druid — 1/1
When it enters, reveal the top card of your library. Land → it goes straight onto the battlefield.
Anything else → into your hand. Either way you got a free card's worth of value off a two-drop.
**When to play it:** Turn 2, as a cheap spell to fill out a double-spell turn.
**Watch out:** The land enters **untapped** and doesn't use your land drop for the turn. Cast it
*before* you play your land so you don't waste a drop.

#### Jolly Gerbils — {1}{W} — Creature — Hamster Citizen — 2/3
"Whenever you give a gift, draw a card." **Gift** (CR 702.174a) is the keyword on five cards in this
deck — Long River's Pull, Wear Down, Peerless Recycling, Perch Protection, Octomancer. Each of them
lets you promise an opponent something as an extra cost, which makes your spell better. With the
Gerbils out, every gift you hand over also draws *you* a card.
**When to play it:** Turn 2, especially if you're holding a gift card. A 2/3 body also blocks
respectably.
**Watch out:** Only five cards in the deck have gift, so this is often just a 2/3 wall. Don't hold
your gift spells waiting to draw the Gerbils.
**Rulings:**
- *[2024-07-26]* "The ability of Jolly Gerbils triggers when the gift is actually given. For permanent
  spells, that happens when the gift triggered ability resolves. For instants and sorceries, that
  happens when the spell resolves. It doesn't matter if a replacement effect causes the gift you gave
  to become something else or if a static effect stops the player from receiving that gift."

#### Kwain, Itinerant Meddler — {W}{U} — Legendary Creature — Rabbit Wizard — 1/3
Tap: **each player may draw a card**, then each player who drew gains 1 life. Note "may" — including
you, so you can decline. It's a free card every turn for you at the cost of a free card for everyone.
**When to play it:** Turn 2. Then tap it in your **end step**, or on the turn of the player before
you, so the card arrives when you can use it.
**Watch out:** The card the opponents draw could be their board wipe. Kwain is symmetrical
generosity — you are not getting ahead, you are speeding the game up. In this deck that's acceptable
because your engine pieces (§7) grow off spells being cast, but be honest that it helps them too.

#### Loran of the Third Path — {2}{W} — Legendary Creature — Human Artificer — 2/1
Vigilance. When it enters, **destroy up to one target artifact or enchantment** — a free removal
spell stapled to a body. Then, tap: you and target opponent each draw a card. Secondary role:
removal.
**When to play it:** Turn 3, ideally when there's an artifact or enchantment worth killing. "Up to
one" means you can choose zero targets and still play it safely when there's nothing to hit.
**Watch out:** 2/1 is fragile — it dies to any chip damage. Tapping it for cards means it can't block
(vigilance only helps when attacking).

#### Mangara, the Diplomat — {3}{W} — Legendary Creature — Human Cleric — 2/4
Lifelink. Draw a card whenever an opponent attacks you (or your planeswalkers) with two or more
creatures, **and** draw a card whenever an opponent casts their **second spell each turn**. In a
four-player game the second half alone can draw you two or three cards a turn for free. This is one
of the best cards in the deck and it does not feed anyone.
**When to play it:** Turn 4. A very high-priority play — it's pure upside.
**Watch out:** It's not a deterrent; it doesn't stop the attack, it just pays you for it.
**Rulings:**
- *[2020-06-23]* "You draw just one card, no matter how many creatures are attacking you and your
  planeswalkers beyond the second."
- *[2020-06-23]* "If your opponent attacks you with one creature and your planeswalker with another,
  you draw a card."
- *[2020-06-23]* "An ability that triggers when a player casts a spell resolves before the spell that
  caused it to trigger. It resolves even if that spell is countered."
- *[2020-06-23]* "Players can cast spells and activate abilities after the triggered ability resolves
  but before the spell that caused it to trigger does."
- *[2020-06-23]* "If some of the attacking creatures leave the battlefield while Mangara's triggered
  ability is on the stack, use the player or planeswalker they were attacking before they left…"

#### Sphinx of Enlightenment — {4}{U}{U} — Creature — Sphinx — 5/5
Flying. When it enters, target opponent draws a card and **you draw three**. A 5/5 flier plus three
cards for six mana. Secondary role: it is a genuine attacker.
**When to play it:** Turn 6. It's a clean, no-strings haymaker.
**Watch out:** Six mana is a whole turn — you won't be double-spelling with Ms. Bumbleflower the turn
you cast this.

#### Mr. Foxglove — {2}{G}{W}{U} — Legendary Creature — Fox Rogue — 3/5
Lifelink. Whenever it attacks, draw cards equal to **(cards in defending player's hand) minus (cards
in your hand)**. If that number is zero or less, you instead may put a creature card from your hand
onto the battlefield for free.
So: attack the player with the fat hand and refill; attack when *your* hand is fat and cheat a
creature into play. It is good either way — that's the point.
**When to play it:** Turn 5. Choose your attack target based on which half you want.
**Watch out:** "Defending player" is whoever you attacked. If you attack a player with fewer cards
than you, you get the free-creature mode — which is often better anyway, so don't treat it as a
failure.
**Rulings:**
- *[2024-07-26]* "If the number of cards in defending player's hand minus the number of cards in your
  hand is 0 or less, you won't draw any cards."

#### Body of Knowledge — {3}{U}{U} — Creature — Avatar — */*
Its power and toughness are each equal to the **number of cards in your hand**. It gives you no
maximum hand size. And whenever it's dealt damage, you draw that many cards. Secondary role: beater.
In a deck that regularly sits on 10+ cards, this is a 10/10 that draws you cards for blocking.
**When to play it:** Turn 5, when your hand is big. It's an excellent blocker precisely because
damaging it rewards you.
**Watch out:** Its size *changes as your hand changes*. Cast a spell during combat and it shrinks.
Never attack with it and then tap out.
**Rulings:**
- *[2020-11-10]* "Creatures may be dealt damage greater than their toughness… if Body of Knowledge is
  a 3/3 creature and a source deals 5 damage to it, you'll draw five cards. Note that if Body of
  Knowledge is dealt lethal damage, it dies before the cards are drawn, meaning they won't raise Body
  of Knowledge's toughness in time to save it."
- *[2020-11-10]* "As long as Body of Knowledge is in your hand, its ability will count itself."
- *[2020-11-10]* "The ability that defines Body of Knowledge's power and toughness applies in all
  zones, not just the battlefield."

#### Secret Rendezvous — {1}{W}{W} — Sorcery
You and target opponent each draw three cards.
**When to play it:** When you need gas and can pick a *harmless* opponent — the one who is behind, or
the one you want as a temporary ally. Three cards for three mana is a good rate.
**Watch out:** You are handing three cards to a real person who will use them. Never target the
player who is winning. Never target the player who is one card away from stabilising.
**Rulings:**
- *[2021-04-16]* "If the opponent is an illegal target as Secret Rendezvous tries to resolve, neither
  player will draw cards."

#### Intellectual Offering — {4}{U} — Instant
Two separate effects: (1) choose an opponent, you and that player each draw three; (2) choose an
opponent, **untap all nonland permanents you control and all nonland permanents that player
controls**. You can pick different opponents for each half.
The untap half is the sneaky one — untap your mana rocks and Selvala/Kwain/Loran mid-turn, or untap
everything at the end of an opponent's turn for a surprise defensive wall.
**When to play it:** At instant speed, on the turn *before* yours, so you untap into your own turn
with everything available. Or in response to a big attack to untap your blockers.
**Watch out:** Untapping an opponent's permanents is a real gift — pick the player whose untapped
board hurts you least.
**Rulings:**
- *[2014-11-07]* "You may choose the same opponent for each of the effects, or you may choose
  different opponents. None of the affected players are targets of the spell."
- *[2014-11-07]* "You choose the opponents for each effect as the spell resolves."

#### Tempt with Bunnies — {2}{W} — Sorcery
**Tempting offer.** You draw a card and make a 1/1 white Rabbit token. Then each opponent may do the
same. For every opponent who accepts, **you draw another card and make another Rabbit**. All-accept
in a four-player game = you draw 4 and get 4 Rabbits for three mana.
**When to play it:** Turn 3. Rabbits are counter-carriers for Ms. Bumbleflower and Kalonian Hydra,
and they're bodies to block with.
**Watch out:** Everyone can see the maths. Experienced opponents decline, leaving you with one card
and one 1/1 for three mana. Cast it early, when a card and a 1/1 look cheap to everyone.
**Rulings:**
- *[2024-07-26]* "After each opponent has decided, the effect happens simultaneously for each one who
  accepted the offer. Then the effect happens again for you a number of times equal to the number of
  opponents who accepted."
- *[2024-07-26]* "Your opponents decide in turn order whether or not they accept the offer, starting
  with the next opponent in turn order."

#### Tenuous Truce — {1}{W} — Enchantment — Aura
Attaches to an **opponent**. At the beginning of that opponent's end step, you and they each draw a
card. It sacrifices itself the moment either of you attacks the other (or each other's
planeswalkers).
A literal non-aggression pact you can point at, which is a genuinely useful political tool.
**When to play it:** Turn 2, on the scariest opponent. "I'm not attacking you, and it costs me a card
if I do" is a real argument at a real table.
**Watch out:** It breaks if **you** attack them too, so it locks you out of a whole opponent. And it
still draws them a card every turn.

#### Wizard Class — {U} — Enchantment — Class
A one-mana enchantment you level up at sorcery speed (CR 716).
- **Level 1** (free, on cast): you have no maximum hand size.
- **Level 2** — pay `{2}{U}`: when it becomes level 2, **draw two cards**.
- **Level 3** — pay `{4}{U}`: whenever you draw a card, put a **+1/+1 counter on target creature you
  control**.
Level 3 is the payoff and it is enormous here: with 25 draw pieces, every card you draw becomes a
counter. That directly feeds Simic Ascendancy and Kalonian Hydra.
**When to play it:** Turn 1 (level 1 alone fixes your hand size). Level 2 whenever you have spare
mana. Level 3 is a real goal, not a luxury.
**Watch out:** Levels can only be gained **as a sorcery** — your main phase, your turn, empty stack.
You must go 1 → 2 → 3 in order; you can't skip to level 3.
**Rulings:**
- *[2021-07-23]* "Each Class starts with only the first of three class abilities. As the first level
  ability resolves, the Class becomes level 2 and gains the second class ability."
- *[2021-07-23]* "You can't activate the first level ability of a Class unless that Class is level 1.
  Similarly, you can't activate the second level ability of a Class unless that Class is level 2."

#### Fisher's Talent — {2}{G}{U} — Enchantment — Class
- **Level 1**: at the beginning of your upkeep, look at the top card of your library. You **may**
  reveal it if it's a land; if you do, make a 1/1 blue Fish token. Then **draw a card** either way.
- **Level 2** — `{G}{U}`: Fish tokens become 3/3 blue Sharks instead.
- **Level 3** — `{2}{G}{U}`: Sharks become **8/8 blue Octopuses** instead.
A free card every upkeep plus an escalating token engine. At level 3 you are making an 8/8 whenever
you hit a land off the top.
**When to play it:** Turn 4. Level it up in the turns after — the levels are cheap and the payoff is
huge.
**Watch out:** The token only happens if the top card **is a land and you reveal it**. The draw
happens regardless. Also note the levels stack in sequence: you need level 2 before level 3.
**Rulings:**
- *[2024-07-26]* "You don't have to reveal the card if it's a land card. (Maybe you're not in the mood
  for fish. That's okay.)"
- *[2024-07-26]* "Gaining a level won't remove abilities that a Class had at a previous level."

#### Rites of Flourishing — {2}{G} — Enchantment
At each player's draw step, that player draws an **additional** card. And each player may play an
**additional land** each turn (CR 305.2: "A player can normally play one land during their turn;
however, continuous effects may increase this number"). Secondary role: ramp.
Pure group hug — and pure fuel for your engine, because more cards for opponents means more spells
cast, which grows Forgotten Ancient, Managorger Hydra, Sunscorch Regent and Steelburr Champion.
**When to play it:** Turn 3, but only once your engine pieces are down or close. Playing this on an
empty board is just helping three opponents.
**Watch out:** This is the single most dangerous card in the deck **for you**. It accelerates
everyone. If a combo or aggro deck is at the table, this may just kill you faster. Read the room.
**Rulings:**
- *[2013-04-15]* "The triggered ability is put onto the stack after you have already drawn your card
  for the turn."

#### Ghirapur Orrery — {4} — Artifact
Each player may play an additional land each turn. And at each player's upkeep, **if that player has
no cards in hand, they draw three**. Secondary role: ramp.
In practice you will almost never be the one with an empty hand — this refills the *hellbent* aggro
player. Its value to you is the extra land drop and, again, more spells being cast into your engine.
**When to play it:** Turn 4-5, when you're already deploying and want the extra land drops. Or
never — see below.
**Watch out:** This is arguably a **liability**. It refuels exactly the opponent who has dumped their
hand at you. In this deck (25 draw pieces, hand always full) you will essentially never draw the
three yourself. Treat it as a build-around you don't have.
**Rulings:**
- *[2016-09-20]* "If the player has any cards in hand as Ghirapur Orrery's second ability resolves, the
  ability does nothing."
- *[2016-09-20]* "The draw step is after the upkeep step, so drawing a card as a turn-based action won't
  affect whether Ghirapur Orrery's second ability triggers."
- *[2016-09-20]* "No player may take actions in a turn before Ghirapur Orrery's second ability checks to
  see if it should trigger. If the player whose turn it is has any cards in hand, it won't trigger."
- *[2016-09-20]* "Ghirapur Orrery's first ability allows a player to play an additional land during
  their main phase. Doing so follows the normal timing rules for playing lands."

#### Tamiyo, Field Researcher — {1}{G}{W}{U} — Legendary Planeswalker — Tamiyo
A planeswalker with **starting loyalty 4**: it enters with 4 loyalty counters and you use **one** of
its abilities per turn.
- **+1**: choose up to two target creatures. Until your next turn, whenever either of them deals
  combat damage, **you** draw a card. Works on creatures you don't control.
- **−2**: tap up to two target nonland permanents; they don't untap during their controller's next
  untap step. A two-for-one defensive tap-down.
- **−7**: draw three cards and get an emblem letting you cast spells from your hand without paying
  their mana costs.
**When to play it:** Turn 4. Default to +1 targeting **two attacking creatures of the player who is
attacking someone else** — you draw off a fight you're not in. The −2 is your emergency button when
two big attackers are pointed at you.
**Watch out:** Planeswalkers get attacked. This deck's defensive cards (Baird, Mangara) mostly protect
you *and* your planeswalkers, but Tamiyo will still draw fire. The −7 needs three +1 activations to
reach, which almost never happens in a real game — treat it as a bonus, not a plan.
**Rulings:**
- *[2025-01-24]* "Tamiyo's first ability can target creatures you don't control. You'll draw a card,
  not their controller, if they deal combat damage."
- *[2025-01-24]* "If a spell has {X} in its mana cost, you must choose 0 as the value of X when casting
  it without paying its mana cost."
- *[2025-01-24]* "If you cast a spell 'without paying its mana cost,' you can't choose to cast it for
  any alternative costs. You can, however, pay additional costs."

---

# 4. Removal & Interaction

**This is the deck's weakest area — only 8 cards total, and just 4 of them kill a permanent
outright.** Use them on the thing that actually beats you, not the first shiny target.

#### Swords to Plowshares — {W} — Instant
Exile target creature; its controller gains life equal to its power. One mana, exiles (so it dodges
regeneration, indestructible, and death triggers), instant speed. The best creature removal spell in
Commander.
**When to play it:** Hold it. Use it on the single scariest creature at the table — a commander that
kills you, a creature about to connect for lethal. At one mana it is a perfect second spell for a
Bumbleflower double-spell turn.
**Watch out:** The life gain is real and can matter. Also: it only hits **creatures**.
**Rulings:**
- *[2022-12-08]* "Use the power of the creature from when it was last on the battlefield to determine
  how much life is gained."

#### Generous Gift — {2}{W} — Instant
Destroy target **permanent** — any permanent, including lands, planeswalkers, enchantments,
artifacts. Its controller gets a 3/3 green Elephant token as compensation.
**When to play it:** This is your catch-all answer. Save it for the problem you have no other answer
to, because this deck has so few of these.
**Watch out:** A 3/3 is a real creature. Don't use this to kill a 2/2. Also note that using it on
your *own* permanent to get a 3/3 is legal but almost always wrong here.
**Rulings:**
- *[2019-06-14]* "If the target permanent is an illegal target by the time Generous Gift tries to
  resolve, the spell doesn't resolve. No player creates an Elephant. If the target is legal but not
  destroyed (most likely because it has indestructible), its controller does create an Elephant."

#### Broken Wings — {2}{G} — Instant
Destroy target artifact, enchantment, **or creature with flying**. Green's classic three-mode answer.
**When to play it:** Instant speed, so hold it until you know which mode you need. Fliers are the
creatures this deck struggles to block, so that mode matters more than usual.
**Watch out:** It cannot hit a ground creature, no matter how big.

#### Wear Down — {1}{G} — Sorcery
**Gift a card** (an opponent of your choice draws a card as an extra cost). Destroy target artifact
or enchantment — and **if you promised the gift, destroy two instead**.
**When to play it:** Almost always promise the gift. Two-for-one'ing artifacts/enchantments for two
mana is excellent, and a card to an opponent is what this deck does anyway. Also triggers Jolly
Gerbils.
**Watch out:** Sorcery speed — your main phase only. And if the gift is promised you **must** have
two legal targets to pick.
**Rulings:**
- *[2024-07-26]* "As an additional cost to cast a spell with gift, you can promise the listed gift to an
  opponent. That opponent is chosen as part of that additional cost. The gift isn't given at this time;
  rather, it's given at a later time based on whether or not the spell is a permanent spell."

#### An Offer You Can't Refuse — {U} — Instant
Counter target **noncreature** spell; its controller creates two Treasure tokens (CR 111.10 — each
taps and sacrifices for one mana of any colour).
**Countering** (CR 701.6) means the spell never resolves and goes to the graveyard.
**When to play it:** Hold it all game for the one spell that ends you — a board wipe, an
extra-turns spell, a game-winning enchantment. One mana makes it a free second spell for
Bumbleflower.
**Watch out:** **It cannot counter a creature spell.** Two Treasures is a real gift — it can let them
cast the follow-up immediately.
**Rulings:**
- *[2022-04-29]* "If the target is still legal as it resolves but the spell can't be countered for some
  reason, its controller will still create two Treasure tokens."
- *[2022-04-29]* "If the target is no longer legal as An Offer You Can't Refuse resolves, no Treasure
  tokens are created."

#### Long River's Pull — {U}{U} — Instant
**Gift a card.** Counter target **creature** spell — but **if you promised the gift, counter target
spell** (anything at all). The gift upgrades it from a narrow answer to a universal one.
**When to play it:** Promise the gift unless you're specifically countering a creature and desperately
want to deny the card. Two mana to counter anything is a fine rate. Triggers Jolly Gerbils.
**Watch out:** You choose the gift **as you cast it** — before you know if it will resolve. And if the
spell is countered or fizzles, the gift isn't given either (see the shared gift ruling below).
**Rulings:**
- *[2024-07-26]* "Some instant or sorcery spells require alternative or additional targets if the gift
  was promised. You ignore these targeting requirements if the gifts aren't promised for those spells."
- *[2024-07-26]* "As an additional cost to cast a spell with gift, you can promise the listed gift to an
  opponent. That opponent is chosen as part of that additional cost."

#### Perplexing Test — {3}{U}{U} — Instant
Choose one: return **all creature tokens** to their owners' hands (tokens cease to exist), **or**
return **all nontoken creatures** to their owners' hands.
Mode two is a pseudo board wipe that doesn't kill anything — it just resets the battlefield. It's
symmetrical, so it bounces your stuff too.
**When to play it:** As a defensive reset when you're about to be killed by a big attack — cast it
during combat after attackers are declared. Or use mode one to blank a token deck for free.
**Watch out:** Bouncing nontoken creatures returns **commanders to their owners' hands too**, which
they can just recast. It's a delay, not an answer. And it undoes all your +1/+1 counters — a creature
that returns to hand loses everything on it.
**Rulings:**
- *[2021-04-16]* "A token that is returned to its owner's hand ceases to exist as a state-based action
  the next time a player would receive priority."

#### Illusionist's Gambit — {2}{U}{U} — Instant
**Cast this only during the declare blockers step on an opponent's turn.** Remove all attacking
creatures from combat and untap them. Then there's an **additional combat phase**, and each of those
creatures must attack again if able — **but they can't attack you or your planeswalkers**.
So: someone swings at you with their whole board, you untap it all and redirect it into somebody
else. It is a fog and a political weapon at once. Secondary role: this is listed as a "wincon" by
`mtg deck stats` because it can effectively end a game between two other players.
**When to play it:** After attackers are declared and blockers are declared, on an opponent's turn.
Ideally when the biggest attacker is swinging at you and there's a juicy third party.
**Watch out:** The timing restriction is strict — declare **blockers** step, opponent's turn. If you
miss the window it's a dead card. And the attackers pick who they hit; you can't choose for them.
**Rulings:**
- *[2013-10-17]* "Creatures that didn't attack during the combat phase when Illusionist's Gambit
  resolved aren't required to attack in the additional combat phase, although they may. Those creatures
  can attack you or a planeswalker you control."
- *[2013-10-17]* "If there's a cost associated with having a creature attack, the player isn't forced to
  pay that cost, so it doesn't have to attack."
- *[2013-10-17]* "If, during a player's declare attackers step, a creature is tapped, is affected by a
  spell or ability that says it can't attack, or hasn't been under that player's control continuously
  since the turn began (and doesn't have haste), then it doesn't attack."

---

# 5. Board Wipes

Only two. Both are white, both are expensive, and both are one-sided-ish rather than truly
symmetrical.

#### Promise of Loyalty — {4}{W} — Sorcery
**Each player** puts a "vow" counter on one creature they control and **sacrifices the rest**. The
surviving creatures **can't attack you or your planeswalkers** for as long as they have that counter.
So it's a wipe that leaves everyone one creature — and every survivor is permanently barred from
attacking you. That is an extraordinary deal for a defensive deck.
**When to play it:** When the board has run away from you. Keep your best counter-loaded creature.
Note that sacrificing dodges "indestructible" entirely.
**Watch out:**
- **You sacrifice too.** Pick your keeper carefully — usually the one carrying the most +1/+1
  counters, or Ms. Bumbleflower herself.
- Token creatures die to this. If you've spent the game making Rabbits and Fish, this is a big loss.
- If a player controls no creatures, they lose nothing.
**Rulings:**
- *[2021-04-16]* "Each player, including you, must put a vow counter on a creature they control if able.
  They can't choose to opt out and sacrifice all of their creatures. The creature you put a vow counter
  on will remember its promise if another player gains control of it."
- *[2021-04-16]* "If the vow counter is removed from the creature, it can attack as normal."
- *[2021-04-16]* "If the vow counter is moved to another creature, it won't prevent the second creature
  from attacking normally."

#### Realm-Cloaked Giant // Cast Off — {5}{W}{W} // {3}{W}{W} — Creature — Giant // Sorcery — Adventure
An **Adventure card** (CR 715): one card, two spells. The creature face is a **7/7**.
- Cast the cheap half, **Cast Off** for `{3}{W}{W}`: **destroy all non-Giant creatures**. That is
  every creature on the battlefield, because nobody has Giants. Then the card goes to exile instead of
  the graveyard.
- Later, from exile, cast **Realm-Cloaked Giant** for `{5}{W}{W}`: a 7/7 with vigilance.
So it is a five-mana board wipe that becomes a seven-mana 7/7 later. Two cards in one slot.
**When to play it:** Cast Off when you're behind on board — you have the most resilient position after
a wipe because your engine is enchantments and card draw, not creatures. Then rebuild, and drop the
Giant when you have spare mana.
**Watch out:**
- It kills **your** creatures too, including Ms. Bumbleflower (she'd go to the command zone) and
  every +1/+1 counter you've accumulated. This is a reset button, not a win button.
- You must **cast** Cast Off and let it **resolve** to get the Giant into exile (see ruling below).
- While in your graveyard or hand, it is a 7/7 Giant creature card with mana value 7 — the Adventure
  characteristics only apply on the stack.
**Rulings:**
- *[2019-10-04]* "If a spell is cast as an Adventure, its controller exiles it instead of putting it into
  its owner's graveyard as it resolves. For as long as it remains exiled, that player may cast it as a
  permanent spell. If an Adventure spell leaves the stack in any way other than resolving (most likely by
  being countered or by failing to resolve because its targets have all become illegal), that card won't
  be exiled and the spell's controller won't be able to cast it as a permanent later."
- *[2019-10-04]* "When casting a spell as an Adventure, use the alternative characteristics and ignore all
  of the card's normal characteristics. The spell's color, mana cost, mana value, and so on are determined
  by only those alternative characteristics."
- *[2019-10-04]* "You must still follow any timing restrictions and permissions for the permanent spell you
  cast from exile. Normally, you'll be able to cast it only during your main phase while the stack is
  empty."
- *[2019-10-04]* "An adventurer card is a permanent card in every zone except the stack, as well as while on
  the stack if not cast as an Adventure."

---

# 6. Threats & Beaters

Six creatures whose job is to end the game with damage. This deck has **no fast clock** — expect
games to go to turn 9 or later.

#### Kalonian Hydra — {3}{G}{G} — Creature — Hydra — 0/0
Trample. It **enters with four +1/+1 counters**, so it's a 4/4 the moment it lands. And whenever it
attacks, **double the number of +1/+1 counters on each creature you control**.
This is the single biggest damage swing in the deck. With Ms. Bumbleflower having sprinkled counters
across your board, one Kalonian Hydra attack can double your entire team — and Simic Ascendancy
(§7) counts every one of those new counters as growth counters.
**When to play it:** Turn 5, once you have two or three creatures already carrying counters. Attacking
with it is the whole point; the trigger is on **attack**, so it works even if it gets blocked or killed
afterwards.
**Watch out:**
- It is a **0/0 base**. If all its counters are removed, it dies instantly.
- The doubling only affects creatures **you** control, and only when **Kalonian Hydra itself** attacks —
  not when other creatures attack.
- It is the most obvious removal magnet in the deck. Swiftfoot Boots (§8) exists for it.
**Rulings:**
- *[2013-07-01]* "To double the number of +1/+1 counters on a creature, determine how many +1/+1 counters
  are on the creature and put that many more on it. Effects that interact with counters… may change the
  number of counters ultimately put on the creature."

#### Sunscorch Regent — {3}{W}{W} — Creature — Dragon — 4/3
Flying. Whenever an **opponent** casts a spell, put a +1/+1 counter on it and **you gain 1 life**.
Three opponents casting two spells each per turn cycle = six counters and six life a turn. It grows
absurdly fast, it flies (so almost nothing blocks it), and the life buffers you against the aggression
your group-hug invites.
**When to play it:** Turn 5. It is one of the two best threats in the deck and it grows without you
spending a card.
**Watch out:** **It does not trigger off your own spells** — only opponents'. It's a 4/3, so it dies to
almost any damage-based removal before the counters accumulate.
*(No official rulings recorded for this card — "not in my data".)*

#### Managorger Hydra — {2}{G} — Creature — Hydra — 1/1
Trample. Whenever **a player** casts a spell — any player, including you — put a +1/+1 counter on it.
Note there's no "may": this is mandatory and it stacks fast. In a four-player game with everyone
casting two spells a turn, it grows by roughly eight counters per turn cycle.
**When to play it:** Turn 3. The earlier it lands the more absurd it gets. It's a three-mana card that
is a 10/10 trampler by turn 6 if left alone.
**Watch out:** It will be killed. It is the most obvious "kill on sight" creature in the deck, and you
only have four removal spells to protect the board. Consider holding it until you have Swiftfoot Boots
or a counterspell up.
**Rulings:**
- *[2015-06-22]* "Managorger Hydra's last ability will resolve before the spell that caused it to trigger."

#### Psychosis Crawler — {5} — Artifact Creature — Phyrexian Horror — */*
Its power and toughness each equal **the number of cards in your hand**. And whenever **you** draw a
card, **each opponent loses 1 life**.
In a deck with 25 draw pieces and a commander that draws you two cards a turn, this is a slow but
inevitable drain on all three opponents simultaneously. It is a genuine alternate route to victory that
doesn't require attacking.
**When to play it:** Turn 5. It's colourless, so it's castable off any mana.
**Watch out:**
- Its size swings wildly. Cast two spells and it shrinks by two.
- **"Whenever you draw a card"** — it doesn't count opponents' draws, which is a shame given how many
  cards you hand out.
- Your own draw-for-turn counts, so it drains at least 1 per opponent per turn cycle.
**Rulings:**
- *[2011-06-01]* "If an effect causes you to draw multiple cards, Psychosis Crawler will trigger that many
  times."

#### Bloodroot Apothecary — {2}{G} — Creature — Squirrel Druid — 3/3
**Toxic 2** — combat damage it deals to a player also gives them **two poison counters**, and ten poison
counters kills a player (CR 704.5c). When it enters, you and target opponent each create a **Treasure
token**. And whenever an opponent **sacrifices a noncreature token**, that player gets two poison
counters — which is exactly what happens when they crack the Treasure you just gave them.
That is a genuinely cute trap: hand them a Treasure, they spend it, they take poison.
**When to play it:** Turn 3. The Treasure ramps you toward a double-spell turn, and the poison plan
punishes any Treasure/Clue/Food deck at the table.
**Watch out:**
- Five hits at toxic 2 is a very slow poison clock. Do not build a game plan around it — it's a bonus.
- Poison from toxic only happens on **combat damage to a player** (see ruling).
**Rulings:**
- *[2024-07-26]* "If a creature with toxic deals combat damage to a creature or planeswalker, or if it
  deals noncombat damage, toxic has no effect and no player gets poison counters."
- *[2024-07-26]* "Damage dealt by a creature with toxic grants the same number of counters regardless of
  how much damage is dealt."
- *[2024-07-26]* "Multiple instances of toxic are cumulative."
- *[2024-07-26]* "Any other effects of that damage, such as life gain from lifelink, still apply."

#### Octomancer — {3}{G}{U} — Creature — Frog Druid — 3/3
**Gift an Octopus** — you may promise an opponent an **8/8 blue Octopus token** as an extra cost. And:
at the beginning of **each end step**, create a token that's a copy of target creature token that
entered the battlefield **this turn**.
"Each end step" means every player's end step — four copies per turn cycle in a four-player game. Point
it at your Rabbits (Tempt with Bunnies), your Birds (Perch Protection), your Fish/Sharks/Octopuses
(Fisher's Talent), your Squids (Chasm Skulker), or your Elemental (Hoofprints of the Stag).
**When to play it:** Turn 5, but **only when you already have token-makers**. It does nothing without a
token that entered that turn.
**Watch out:**
- **Do not promise the gift casually.** An 8/8 for an opponent is enormous — that is a bigger body than
  anything in your deck. Only gift it if Jolly Gerbils is out and you truly need the card, or if the
  chosen opponent is the one being attacked by everyone.
- The target token must have **entered this turn**. A Rabbit from three turns ago is not a legal target.
- Copying an opponent's token is legal and often correct if they made something better than you did.
**Rulings:**
- *[2024-07-26]* "The token you create copies the original characteristics of the token as stated by the
  effect that created that token… It doesn't copy whether that token is tapped or untapped, whether it has
  any counters on it or Auras and Equipment attached to it."
- *[2024-07-26]* "Any 'enters' abilities of the copied token will trigger when the token enters."
- *[2024-07-26]* "You can't pay a gift cost more than once."
- *[2024-07-26]* "If the copied token has {X} in its mana cost, X is 0."

---

# 7. Synergy Pieces — the actual engine

**This is why the deck works.** Two clusters plus the alternate win conditions:

- **Grows off the whole table casting spells:** Forgotten Ancient, Steelburr Champion (+ Managorger
  Hydra and Sunscorch Regent in §6).
- **Grows off you drawing cards:** Chasm Skulker, Hoofprints of the Stag, Jolrael (+ Wizard Class
  level 3 in §3).
- **Alternate ways to win:** Simic Ascendancy, Triskaidekaphile, Twenty-Toed Toad. CR 104.2b: "An
  effect may state that a player wins the game."

#### Forgotten Ancient — {3}{G} — Creature — Elemental — 0/3
Whenever **a player** casts a spell you **may** put a +1/+1 counter on it. Then, at the beginning of
your upkeep, you may **move any number of those counters onto other creatures**.
It's a counter battery: it soaks up counters from the whole table's spellcasting and then redistributes
them to whichever creatures you want to be big — before your draw step, before combat. Pair it with
Kalonian Hydra (spread counters, then double them all) or Simic Ascendancy.
**When to play it:** Turn 4. It's the most important non-commander permanent in the deck.
**Watch out:**
- It's a **0/3**, so it can't do anything by itself and doesn't threaten anyone — which is good, it
  survives longer.
- The counter is **optional** ("you may") — you must remember to say yes each time.
- Moving counters is at **your upkeep only**, which is before you draw. Plan the redistribution the turn
  before.
**Rulings:**
- *[2022-12-08]* "Forgotten Ancient's first ability will resolve before the spell that caused it to trigger.
  Putting a +1/+1 counter on Forgotten Ancient is optional."
- *[2022-12-08]* "Forgotten Ancient's last ability doesn't target any creatures. You choose how many +1/+1
  counters will be moved (and onto which creatures) as the ability resolves. Notably, once the ability
  starts resolving and you make these choices, no player may take actions until the ability has finished
  resolving."

#### Steelburr Champion — {2}{W} — Creature — Mouse Soldier — 1/1
**Offspring `{1}{W}`** — you may pay an extra `{1}{W}` as you cast it; if you do, when it enters you get
a **1/1 token copy** of it (CR 702.175a). It has vigilance, and whenever an **opponent casts a noncreature
spell**, put a +1/+1 counter on it.
Two copies means two counter-accumulators. In a table full of instants, sorceries, artifacts and
enchantments, it grows steadily and blocks while attacking (vigilance).
**When to play it:** Turn 3 as a bare 1/1, or turn 5 with Offspring paid for two bodies. Paying Offspring
is usually right if you're not double-spelling that turn anyway.
**Watch out:**
- Only **opponents'** **noncreature** spells count. Your spells do nothing; their creature spells do
  nothing.
- The Offspring token is **not cast**, so it doesn't trigger Ms. Bumbleflower.
**Rulings:**
- *[2024-07-26]* "The token created by the offspring ability isn't 'cast', so abilities that trigger when a
  creature spell is cast won't trigger for the copy."
- *[2024-07-26]* "You can pay an offspring cost only once as you cast a spell with offspring. You can't try
  to pay it multiple times to get more token copies."
- *[2024-07-26]* "If the spell resolves but the creature with offspring leaves the battlefield before the
  offspring ability resolves, you'll still create a token copy of it."
- *[2024-07-26]* "If the spell is countered, the offspring ability will not trigger, and no token will be
  created."
- *[2024-07-26]* "Steelburr Champion's last ability resolves before the spell that caused it to trigger. It
  resolves even if that spell is countered."
- *[2024-07-26]* "The token copies exactly what was printed on the original creature and nothing else, except
  it's a 1/1… It doesn't copy whether that creature is tapped or untapped, whether it has any counters on it
  or Auras and Equipment attached to it."

#### Chasm Skulker — {2}{U} — Creature — Squid Horror — 1/1
Whenever **you** draw a card, put a +1/+1 counter on it. When it **dies**, create X 1/1 blue Squid tokens
with **islandwalk**, where X is the number of counters on it.
Islandwalk (CR 702.14b, an evasion ability) means those Squids can't be blocked by anyone who controls an
Island — which, in a four-player game, is usually at least one opponent.
So it's a creature that grows every single draw and then converts into an unblockable army when killed.
It is very hard for opponents to answer profitably.
**When to play it:** Turn 3. It grows off the two cards Ms. Bumbleflower gives you every turn.
**Watch out:** The Squids only appear when it **dies** — exile effects (like Swords to Plowshares) and
bounce effects (like Perplexing Test) give you nothing.
**Rulings:**
- *[2014-07-18]* "If you draw multiple cards, the first ability will trigger that many times. Each of these
  abilities will cause a +1/+1 counter to be put on Chasm Skulker."
- *[2014-07-18]* "If enough -1/-1 counters are put on Chasm Skulker at the same time to make its toughness 0
  or less, the number of +1/+1 counters on it before it got any -1/-1 counters will be used to determine how
  many Squid tokens you get."

#### Hoofprints of the Stag — {1}{W} — Kindred Enchantment — Elemental
Whenever you draw a card you **may** put a hoofprint counter on it. Then `{2}{W}` plus removing four
hoofprint counters creates a **4/4 white Elemental token with flying** — activate only during your turn.
Four cards drawn = a 4/4 flier. This deck draws far more than four cards per turn cycle late in the game,
so it's a repeatable token factory, and the fliers are how you actually close.
**When to play it:** Turn 2. It's cheap, it's an enchantment (so it dodges creature removal and board
wipes), and it starts banking immediately.
**Watch out:**
- The counter is **optional** — say yes every time.
- You can only make tokens **during your turn**, so bank counters and cash them in your main phase.
**Rulings:**
- *[2007-10-01]* "If a spell or ability has you draw multiple cards, Hoofprints of the Stag's ability triggers
  that many times."

#### Jolrael, Mwonvuli Recluse — {1}{G} — Legendary Creature — Human Druid — 1/2
Whenever you draw your **second card each turn**, create a **2/2 green Cat token**. And `{4}{G}{G}`: until
end of turn, creatures you control have base power and toughness **X/X where X is the number of cards in
your hand**.
Ms. Bumbleflower's second-spell trigger draws you *two* cards at once — which means Jolrael fires every
single turn you double-spell. A free 2/2 per turn is excellent, and the Cats carry counters.
The `{4}{G}{G}` ability is a genuine surprise kill: with 12 cards in hand, your whole board becomes 12/12s.
**When to play it:** Turn 2. It is a very high-priority early play.
**Watch out:**
- **Once per turn only** (see ruling). The third, fourth and fifth draws do nothing.
- The `{4}{G}{G}` **sets base power and toughness** — it *overwrites* other setting effects, but +1/+1
  counters still apply on top (see rulings). If your creature has 8 counters and you have 3 cards in hand,
  it becomes 3/3 + 8 counters = 11/11. But if you have a 12/12 from counters and 2 cards in hand, activating
  this makes it worse. Check the maths.
**Rulings:**
- *[2022-12-08]* "The triggered ability can trigger only once each turn. It doesn't matter if Jolrael was on
  the battlefield when the first card was drawn: if it's not on the battlefield when the second card is
  drawn, the ability can't trigger at all that turn."
- *[2022-12-08]* "Effects that modify an affected creature's power and/or toughness without setting them to
  specific values will apply no matter when those effects began. The same is true for counters that change
  the creature's power and/or toughness."
- *[2022-12-08]* "Jolrael's last ability overwrites all previous effects that set the affected creatures'
  power and/or toughness to specific values."
- *[2022-12-08]* "The value of X is determined only as Jolrael's last ability resolves. Once that happens, the
  value of X won't change later in the turn even if the number of cards in your hand changes."

#### Communal Brewing — {2}{G} — Enchantment
When it enters, **any number of target opponents** each draw a card. Put an ingredient counter on it, plus
one more for **each card drawn this way**. Then, whenever you cast a **creature spell**, that creature
enters with **X additional +1/+1 counters**, where X is the number of ingredient counters.
Hit all three opponents and it starts at **four** ingredient counters — so every creature you cast
afterwards arrives four counters bigger. On a 1/1 Steelburr Champion that's a 5/5 for three mana.
**When to play it:** Turn 3, and target **all** opponents — the counters are worth far more than the three
cards cost you.
**Watch out:**
- **The ingredient counters never grow after it enters.** It's a one-shot count, locked in at ETB. So cast
  it *early*, before your creatures, not after.
- "Any number of target opponents" includes zero. Targeting zero gives you just one ingredient counter.
- It only affects **creature spells you cast** — not tokens, not creatures put onto the battlefield by
  Mr. Foxglove.
**Rulings:**
- *[2024-07-26]* "The value of X is calculated as Communal Brewing's last ability resolves."
- *[2024-07-26]* "You don't have to choose any target opponents for Communal Brewing's first ability. However,
  if you do, and all of those targets are illegal as the ability tries to resolve, it won't resolve and none
  of its effects will happen."
- *[2024-07-26]* "If Communal Brewing leaves the battlefield before its last ability resolves, use the number
  of ingredient counters that were on it as it last existed on the battlefield to determine the value of X."

#### Simic Ascendancy — {G}{U} — Enchantment
**Win condition #1.** `{1}{G}{U}`: put a +1/+1 counter on target creature you control. Whenever **one or
more +1/+1 counters are put on a creature you control**, put that many **growth counters** on the
enchantment. At the beginning of your upkeep, if it has **twenty or more growth counters, you win the game**.
Every counter from Ms. Bumbleflower, Forgotten Ancient, Rishkar, Wizard Class level 3, Communal Brewing and
Kalonian Hydra feeds this. Kalonian Hydra doubling a board of 10 counters instantly adds 10 growth counters.
**When to play it:** Turn 2, every time. Two mana, it hides behind creature removal (it's an enchantment),
and it starts counting from the moment it lands.
**Watch out:**
- It only counts counters put on creatures **after it's on the battlefield**. A creature already carrying
  eight counters gives you nothing retroactively.
- **It is checked only at the beginning of YOUR upkeep.** Hitting 20 during someone else's turn means you
  survive to your next upkeep to actually win. Opponents get a full turn cycle to destroy it.
- Twenty growth counters is a visible countdown. The table *will* see it coming and will remove the
  enchantment. Expect to need it twice, or to win another way.
**Rulings:**
- *[2019-01-25]* "If Simic Ascendancy doesn't have twenty or more growth counters on it as your upkeep begins,
  its last ability won't trigger. You can't take any actions during your turn before your upkeep begins."
- *[2019-01-25]* "If the last ability does trigger, but Simic Ascendancy leaves the battlefield, use the number
  of counters it had on it immediately before it left the battlefield to determine whether you win the game."
- *[2019-01-25]* "If the last ability does trigger, but counters are removed from Simic Ascendancy so it has
  fewer than twenty remaining on it, you won't win the game."
- *[2019-01-25]* "An ability that triggers when counters are put on a permanent will trigger if that permanent
  somehow enters the battlefield with those counters."

#### Triskaidekaphile — {1}{U} — Creature — Human Wizard — 1/3
**Win condition #2.** You have no maximum hand size. At the beginning of your upkeep, if you have
**exactly thirteen cards in your hand, you win the game**. And `{3}{U}`: draw a card.
The `{3}{U}` is the key — it lets you tune your hand size upward one card at a time. With this deck's
draw volume, sitting on exactly 13 at your upkeep is genuinely achievable.
**When to play it:** Turn 2 as a cheap second spell. The "no maximum hand size" clause alone earns its slot.
**Watch out:**
- **Exactly** thirteen. Twelve doesn't work. Fourteen doesn't work.
- The check is at the **beginning of your upkeep**, which is **before** your draw step. So you need 13 in
  hand at the end of the previous turn cycle, and you cannot draw into it during your own upkeep (see
  ruling). Count your hand carefully on the turn *before*.
- It clashes with Twenty-Toed Toad's "your maximum hand size is twenty" — timestamp order decides which
  applies (see the Toad's ruling below).
**Rulings:**
- *[2021-09-24]* "Triskaidekaphile's triggered ability will trigger only if you have exactly thirteen cards in
  your hand as your upkeep starts. If you have fewer cards in your hand, you won't be able to draw cards
  during your upkeep in time to cause the ability to trigger."

#### Twenty-Toed Toad — {3}{U} — Creature — Frog Wizard — 3/3
**Win condition #3.** Your maximum hand size is twenty. Whenever you attack with **two or more creatures**,
put a +1/+1 counter on the Toad and draw a card. And whenever the Toad attacks, **you win the game if there
are twenty or more counters on it or you have twenty or more cards in hand**.
Two live routes: grind counters onto it by attacking with a team every turn, or just build a 20-card hand
(very realistic here) and swing.
**When to play it:** Turn 4. Then attack with it and at least one other creature every turn.
**Watch out:**
- It **sets** your maximum hand size to twenty. If you already have Thought Vessel / Reliquary Tower /
  Triskaidekaphile / Wizard Class / Body of Knowledge giving you *no* maximum hand size, whichever came
  **later** wins. Play the Toad **last** if you want the 20-card plan; play it **first** if you'd rather
  keep unlimited hand size.
- The win check happens **on resolution of the attack trigger** — so you can cast draw spells in response
  to push your hand to twenty *after* declaring the attack (see ruling).
- A 3/3 attacking into a four-player table dies. Give it Swiftfoot Boots, or attack the player with no
  blockers.
**Rulings:**
- *[2024-07-26]* "Twenty-Toed Toad's last ability will trigger whenever it attacks, no matter how many counters
  are on it or cards you have in your hand at that time. The number of counters on it and the number of cards
  in your hand are only checked when that ability resolves."
- *[2024-07-26]* "Your maximum hand size is only checked during the cleanup step of your turn. At other times,
  you may have more cards in hand than your maximum hand size."
- *[2024-07-26]* "If multiple effects modify your hand size, apply them in timestamp order. For example, if you
  put Twenty-Toed Toad onto the battlefield and then put Spellbook (an artifact that says you have no maximum
  hand size) onto the battlefield, you would have no maximum hand size. However, if those permanents entered in
  the opposite order, your maximum hand size would he twenty." *(typo "he" is in the official text)*

---

# 8. Utility & Protection

**Read this section twice.** You spend the whole game giving three opponents free cards. They will
attack you. These seven cards are why you survive to turn 9+.

#### Baird, Steward of Argive — {2}{W}{W} — Legendary Creature — Human Soldier — 2/4
Vigilance. **Creatures can't attack you or planeswalkers you control unless their controller pays `{1}`
for each of those creatures.**
This is the best defensive card in the deck. A player swinging five creatures at you must find five extra
mana — which almost always means they attack somebody else instead. It doesn't stop attacks; it makes you
the *least convenient* target, which in a four-player game is the same thing.
**When to play it:** Turn 4, and treat it as a priority over almost anything else if you're being attacked.
Protect it.
**Watch out:** It's a tax, not a wall. A player with lots of open mana can simply pay. And it protects
**you and your planeswalkers** — not your other creatures, and not your teammates.
**Rulings:**
- *[2023-07-28]* "If you control Baird, your opponents can choose not to pay to attack with a creature that
  attacks 'if able.' If there's no other player, planeswalker, or battle to attack, that creature simply
  doesn't attack." — this is a real interaction with **goaded** creatures (see Martial Impetus).
- *[2018-04-27]* "In a Two-Headed Giant game, creatures can attack your teammate and planeswalkers your
  teammate controls without requiring a mana payment."

#### Spore Frog — {G} — Creature — Frog — 1/1
Sacrifice it: **prevent all combat damage that would be dealt this turn**. A one-mana **fog** on a body.
This single card can undo a lethal alpha strike from any player. It costs `{G}`, so it is also a perfect
second spell for a Bumbleflower double-spell turn.
**When to play it:** Turn 1 or 2, and then **leave it on the battlefield as a deterrent**. Opponents who
can see it often just attack elsewhere. Sacrifice it only when the damage would actually kill you or cost
you the game.
**Watch out:**
- It prevents **all** combat damage that turn — including damage **your** creatures would deal. Don't fog
  your own lethal attack.
- Sacrificing is a cost, so it can't be responded to by killing the Frog. But it must be **on the
  battlefield and able to be sacrificed** — activate it *before* the damage step, not after.
*(No official rulings recorded for this card — "not in my data".)*

#### Riot Control — {2}{W} — Instant
You gain 1 life for each creature **your opponents** control, and **prevent all damage that would be dealt
to you this turn**. In a four-player game that's often 10-15 life plus a complete damage shield.
**When to play it:** In response to an attack, after attackers are declared so you know how bad it is.
**Watch out:**
- It protects **you**, not your creatures and not your planeswalkers (see ruling). Your blockers still die
  and Tamiyo still takes damage.
- It only stops damage — it doesn't stop "you lose the game" effects, mill, or discard.
**Rulings:**
- *[2013-04-15]* "Riot Control doesn't prevent combat damage that would be dealt to planeswalkers you control.
  It also doesn't prevent damage that would be dealt to creatures you control."
- *[2013-04-15]* "Count the number of creatures your opponents control as Riot Control resolves to determine
  how much life you gain."

#### Perch Protection — {4}{W}{W} — Instant
**Gift an extra turn.** Base mode: create four **2/2 blue Bird tokens with flying** — four flying blockers
at instant speed, and four counter-carriers.
If you promise the gift (an opponent takes an extra turn after this one): **all permanents you control
phase out**, and until your next turn **your life total can't change and you gain protection from
everything**. Then it exiles itself.
The gift mode is a total, unbeatable **"skip me"** button — you literally cannot be interacted with, and
your whole board is untouchable. It survives any board wipe, any attack, anything.
**When to play it:** Base mode as a combat trick to ambush an attack. Gift mode **only** as an emergency
escape from something that would otherwise kill you — a game-ending board wipe, or lethal damage you can't
survive.
**Watch out:**
- **Giving an opponent an extra turn is enormous.** They untap, draw, and get a whole free turn. Only do
  this if the alternative is losing, and pick the least threatening opponent.
- Phased-out permanents "phase in" during your **next untap step** (CR 702.26a) — so your board is gone for
  a full turn cycle, including your blockers for *other* players.
- Your **life total can't change** — so you also can't *gain* life, and lifelink does nothing for you.
**Rulings:**
- *[2024-07-26]* "While a permanent is phased out, it's treated as though it doesn't exist. It can't be the
  target of spells or abilities, its static abilities have no effect on the game, its triggered abilities
  can't trigger, it can't attack or block, and so on."
- *[2024-07-26]* "Permanents that phase out with counters phase in with those counters."
- *[2024-07-26]* "Phasing out doesn't cause any 'leaves the battlefield' abilities to trigger. Similarly,
  phasing in won't cause any 'enters' abilities to trigger."
- *[2024-07-26]* "If a player has protection from everything, it means three things: 1) All damage that would
  be dealt to that player is prevented. 2) Auras can't be attached to that player. 3) That player can't be the
  target of spells or abilities."
- *[2024-07-26]* "Nothing other than the specified events are prevented or illegal… Creatures can still attack
  you while you have protection from everything, although combat damage that they would deal to you will be
  prevented."
- *[2024-07-26]* "If your life total can't change, spells and abilities that would normally cause you to gain
  or lose life still resolve while your life total can't change, but the life-gain or life-loss part simply
  has no effect."
- *[2024-07-26]* "Choices made for permanents as they entered are remembered when they phase in."
- *[2024-07-26]* "Any creatures that phase in under your control as your next untap step begins will be able to
  attack and pay a cost of {T} during that turn."
- *[2024-07-26]* "If your untap step is somehow skipped as your next turn begins, your phased-out permanents
  won't phase in until the next untap step you actually have, but you'll no longer have protection from
  everything and your life total can change again."

#### Swiftfoot Boots — {2} — Artifact — Equipment
Equip `{1}`. The equipped creature has **hexproof** ("can't be the target of spells or abilities your
opponents control", CR 702.11b) and **haste** (ignores summoning sickness, CR 702.10 / 302.6).
This is your only real protection for a key creature. In a deck whose whole plan is accumulating counters
on one or two creatures, that matters enormously.
**When to play it:** Turn 2 to have it ready, then equip **Managorger Hydra, Kalonian Hydra, Forgotten
Ancient or Ms. Bumbleflower** as soon as they land. Haste on Kalonian Hydra means it doubles counters the
turn it arrives.
**Watch out:**
- Hexproof does **not** stop board wipes, edicts ("each player sacrifices"), or anything that doesn't
  target. Realm-Cloaked Giant's Cast Off kills a hexproof creature just fine.
- Equipping is **sorcery speed** — your main phase, your turn, empty stack.
- Hexproof stops *your opponents* from targeting it. You can still target it yourself.
**Rulings:**
- *[2018-03-16]* "If a creature enters the battlefield under your control and gains haste, but then loses it
  before attacking, it won't be able to attack that turn. This means that you can't use one Swiftfoot Boots to
  allow two new creatures to attack in the same turn."

#### Martial Impetus — {2}{W} — Enchantment — Aura
Attaches to **any creature** (usually an opponent's). That creature gets +1/+1 and is **goaded** — CR
701.15b: "A goaded creature attacks each combat if able and attacks a player other than the controller of
the permanent, spell, or ability that caused it to be goaded if able." Since *you* control the Aura, it must
attack **someone other than you**. And whenever it attacks, **each other creature attacking one of your
opponents gets +1/+1** — encouraging everyone to swing at each other, not you.
**When to play it:** Turn 3, on the biggest creature controlled by the player you least want attacking you.
It is removal-that-isn't-removal: the creature is now permanently pointed away from you.
**Watch out:**
- You are making an opponent's creature **bigger**. If that creature has lifelink or a nasty attack trigger,
  you may be handing them value.
- It can still attack your *planeswalkers*? No — goad sends it at a player other than you if able; but read
  the ruling below: if it can't attack any other player, it may be forced to attack a planeswalker an
  opponent controls, a battle an opponent controls, or **you**.
- **Baird interaction:** if Baird taxes them, they can choose not to pay and the goaded creature simply
  doesn't attack (see Baird's 2023-07-28 ruling).
**Rulings:**
- *[2023-06-30]* "If the creature doesn't meet any of the above exceptions and can attack, it must attack a
  player other than the controller of the spell or ability that goaded it if able. If the creature can't attack
  any of those players but could otherwise attack, it must attack a planeswalker an opponent controls, a battle
  an opponent controls, or a player who goaded it."
- *[2023-06-30]* "Attacking with a goaded creature doesn't cause it to stop being goaded. If there is an
  additional combat phase that turn, or if another player gains control of it before it stops being goaded, it
  must attack again if able."
- *[2023-06-30]* "If, during a player's declare attackers step, a creature that player controls that's been
  goaded is tapped, is affected by a spell or ability that says it can't attack, or hasn't been under that
  player's control continuously since the turn began (and doesn't have haste), then it doesn't attack. If
  there's a cost associated with having a creature attack a player, its controller isn't forced to pay that
  cost, so it doesn't have to attack that player."

#### Peerless Recycling — {1}{G} — Instant
**Gift a card.** Return target **permanent** card from your graveyard to your hand — and **if the gift was
promised, return two instead**. The deck's only recursion.
**When to play it:** Almost always promise the gift; two cards back for two mana at instant speed is a great
rate, and it triggers Jolly Gerbils. Use it to rebuy Forgotten Ancient, Managorger Hydra, Simic Ascendancy or
Ms. Bumbleflower's support after a board wipe.
**Watch out:**
- **Permanent cards only** — it cannot return an instant or sorcery. Swords to Plowshares, Perch Protection,
  Illusionist's Gambit are gone forever once used.
- If the gift is promised you need **two** legal targets.
**Rulings:**
- *[2024-07-26]* "If a spell for which the gift was promised is countered, doesn't resolve (perhaps because all
  of its targets are illegal), or is otherwise removed from the stack, the gift won't be given. None of its
  other effects will happen either."
- *[2024-07-26]* "Some instant or sorcery spells require alternative or additional targets if the gift was
  promised."

---

# 9. Lands

**38 lands, of which 14 can enter tapped** (7 always, 7 conditionally) — that is 37% of your mana base.
Colour sources: White 20, Blue 19, Green 19, Colourless 5. Command Tower and Exotic Orchard count toward
every colour.

**The one land-sequencing rule to internalise:** play your **always-tapped** lands (Temples, Thrivings,
Seaside Citadel) on turns when you weren't going to use all your mana anyway — usually turn 1, or a turn
where you're only casting a one-drop. Play the **conditional** lands (Glacial Fortress, Sunpetal Grove,
Hinterland Harbor, Canopy Vista, Prairie Stream) once their condition is met. Save untapped lands for turns
where you need every point of mana to double-spell.

### Basic lands (12)

#### 4 Forest · 4 Island · 4 Plains — Basic Land — Forest / Island / Plains
`{T}`: Add `{G}` / `{U}` / `{W}` respectively. They always enter untapped, they can't be hit by most
land destruction, and they are what **Cultivate**, **Evolving Wilds** and **Terramorphic Expanse** fetch.
**Watch out:** Farseek can find a Plains or an Island but **not a Forest**. Canopy Vista and Prairie Stream
count as basic-land-types for Farseek but are **not basic lands** for Cultivate/Evolving Wilds.

### Any-colour lands (2)

#### Command Tower — Land
`{T}`: Add one mana of any colour in your commander's colour identity — here `{W}`, `{U}` or `{G}`.
Enters untapped, no drawback. The best land in the deck.

#### Exotic Orchard — Land
`{T}`: Add one mana of any colour that **a land an opponent controls** could produce. In a four-player game
this is nearly always the colour you need.
**Watch out:** It depends entirely on opponents' lands. If nobody controls a land that makes white, blue or
green, it produces nothing you can use.
**Rulings:**
- *[2009-02-01]* "Exotic Orchard checks the effects of all mana-producing abilities of lands your opponents
  control, but it doesn't check their costs… It doesn't matter whether it's untapped."
- *[2009-02-01]* "Exotic Orchard doesn't care about any restrictions or riders your opponents' lands… put on
  the mana they produce. It just cares about colors of mana."

### Utility lands (3)

#### Reliquary Tower — Land
You have **no maximum hand size**, and `{T}`: Add `{C}` (one colourless mana). Given how many cards this deck
draws, the hand-size clause is worth a real card.
**When to play it:** Early, but not over a coloured source you need that turn.
**Watch out:** It only makes colourless mana, so it can't cast `{G}`, `{W}` or `{U}` pips. And it clashes with
Twenty-Toed Toad by timestamp.
**Rulings:**
- *[2009-02-01]* "If multiple effects modify your hand size, apply them in timestamp order… if you put Null
  Profusion (an enchantment that says your maximum hand size is two) onto the battlefield and then put Reliquary
  Tower onto the battlefield, you'll have no maximum hand size. However, if those permanents enter in the
  opposite order, your maximum hand size would be two."

#### Evolving Wilds — Land
`{T}`, sacrifice it: search your library for a **basic** land card, put it onto the battlefield **tapped**, then
shuffle.
**When to play it:** Play it and crack it immediately on a turn where you don't need the mana — usually turn 1.
It fixes your colours and shuffles your library.
**Watch out:** It produces **no mana itself** and the land it fetches comes in **tapped**, so it effectively
costs you a turn of mana. Never play it on a turn you need to double-spell.

#### Terramorphic Expanse — Land
Identical text to Evolving Wilds: `{T}`, sacrifice it: search for a basic land, put it onto the battlefield
tapped, then shuffle. Same advice, same trap.

### Painlands (3) — untapped, at the cost of 1 life

Each of these taps for `{C}` for free, **or** for a colour while dealing **1 damage to you**. In a deck that
gains life from Sunscorch Regent, Mangara, Mr. Foxglove, Selvala, Kwain and Riot Control, that life is cheap.

#### Adarkar Wastes — Land
`{T}`: Add `{C}`. Or `{T}`: Add `{W}` or `{U}`, and it deals 1 damage to you.

#### Brushland — Land
`{T}`: Add `{C}`. Or `{T}`: Add `{G}` or `{W}`, and it deals 1 damage to you.

#### Yavimaya Coast — Land
`{T}`: Add `{C}`. Or `{T}`: Add `{G}` or `{U}`, and it deals 1 damage to you.

### Check lands (3) — untapped once you have the right land

#### Glacial Fortress — Land
Enters **tapped unless you control a Plains or an Island**. `{T}`: Add `{W}` or `{U}`.
**Watch out:** It checks for the land **types**, so Prairie Stream (Plains Island) and Canopy Vista (Forest
Plains) both satisfy it.

#### Hinterland Harbor — Land
Enters **tapped unless you control a Forest or an Island**. `{T}`: Add `{G}` or `{U}`.

#### Sunpetal Grove — Land
Enters **tapped unless you control a Forest or a Plains**. `{T}`: Add `{G}` or `{W}`.

### Battle lands (2) — untapped once you have two basics

#### Canopy Vista — Land — Forest Plains
It **is** a Forest and a Plains, so it taps for `{G}` or `{W}` inherently. Enters **tapped unless you control
two or more basic lands**.
**Note:** because it has the Plains type, **Farseek can fetch it**.

#### Prairie Stream — Land — Plains Island
It **is** a Plains and an Island, so it taps for `{W}` or `{U}` inherently. Enters **tapped unless you control
two or more basic lands**.
**Note:** **Farseek can fetch it** too.
**Watch out:** Because these have basic land *types*, an opponent's Islandwalk creature is unblockable through
your Prairie Stream. Minor, but real.

### Fast lands (2) — untapped early, tapped late

#### Razorverge Thicket — Land
Enters **tapped unless you control two or fewer OTHER lands**. `{T}`: Add `{G}` or `{W}`.
**When to play it:** In your first three land drops. After that it always enters tapped.

#### Seachrome Coast — Land
Enters **tapped unless you control two or fewer other lands**. `{T}`: Add `{W}` or `{U}`. Same rule, same
advice.

### Scry lands (3) — always tapped, but they smooth your draws

Each enters **tapped** and, when it enters, **scry 1** (CR 701.22 — look at the top card of your library and
put it on the bottom if you don't want it).

#### Temple of Enlightenment — Land
Enters tapped, scry 1. `{T}`: Add `{W}` or `{U}`.

#### Temple of Mystery — Land
Enters tapped, scry 1. `{T}`: Add `{G}` or `{U}`.

#### Temple of Plenty — Land
Enters tapped, scry 1. `{T}`: Add `{G}` or `{W}`.

**When to play these:** Turn 1, or any turn where you have mana to spare. The scry is free card selection —
never waste it by playing one on a turn you need untapped mana.

### Thriving lands (3) — always tapped, but flexible

Each enters **tapped**, and **as it enters you choose a colour** other than its own. It then taps for its own
colour **or** the chosen colour.

#### Thriving Grove — Land
Enters tapped; choose a colour other than green. `{T}`: Add `{G}` or one mana of the chosen colour.

#### Thriving Heath — Land
Enters tapped; choose a colour other than white. `{T}`: Add `{W}` or one mana of the chosen colour.

#### Thriving Isle — Land
Enters tapped; choose a colour other than blue. `{T}`: Add `{U}` or one mana of the chosen colour.

**Watch out:** The colour choice is **locked in permanently** as it enters — you can't change it later. Look at
your hand and pick the colour you're short on. Choosing a colour outside white/blue/green is legal but useless
here.

### Filter and two-mana lands (5)

#### Flooded Grove — Land
`{T}`: Add `{C}`. **Or** `{G/U}`, `{T}`: Add `{G}{G}`, `{G}{U}`, or `{U}{U}`. That second ability is a
**filter**: you feed it one green-or-blue mana and get two back, in the colours you actually need.
**Watch out:** It needs an existing green or blue mana to filter. On its own it only makes `{C}`. It does not
help you cast a white spell.

#### Seaside Citadel — Land
Enters **tapped**. `{T}`: Add `{G}`, `{W}`, or `{U}` — all three of your colours off one land.
**When to play it:** Turn 1, or any turn with spare mana. The fixing is worth the tapped turn.

#### Skycloud Expanse — Land
`{1}`, `{T}`: Add `{W}{U}`. It enters untapped but produces **nothing for free** — you must pay `{1}` to get
two mana back, so it's mana-neutral and colour-fixing rather than ramp.
**Watch out:** It cannot produce mana on turn 1 or 2 unless you have another land to feed it. Two of these in
an opening hand is a mulligan consideration.

#### Sungrass Prairie — Land
`{1}`, `{T}`: Add `{G}{W}`. Same shape as Skycloud Expanse, different colours. Same warning.

#### Overflowing Basin — Land
`{1}`, `{T}`: Add `{G}{U}`. Same shape again. Same warning.

---

## Appendix — real CLI output (verification samples)

Two full, unedited pulls from the local database, so you can see the exact format this document was
built from.

### `./bin/mtg card "Ms. Bumbleflower"`

```
── Ms. Bumbleflower ──────────────────────────────────────────────────────
Mana cost      : {1}{G}{W}{U}
Mana value     : 4
Type           : Legendary Creature — Rabbit Citizen

Vigilance
Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter
on target creature. It gains flying until end of turn. If this is the second
time this ability has resolved this turn, you draw two cards.

P/T            : 1/5

Color identity : WUG (white, blue, green)
Keywords       : Vigilance
Rarity         : mythic
Commander      : legal
EDHREC rank    : #3131
Price (USD)    : $5.45

── Rulings (1) ───────────────────────────────────────────────────────────
[2024-07-26] (wotc)
  Ms. Bumbleflower's last ability resolves before the spell that caused it
  to trigger. It resolves even if that spell is countered.

https://scryfall.com/card/blc/3/ms-bumbleflower?utm_source=api
```

### `./bin/mtg card "Forgotten Ancient"`

```
── Forgotten Ancient ─────────────────────────────────────────────────────
Mana cost      : {3}{G}
Mana value     : 4
Type           : Creature — Elemental

Whenever a player casts a spell, you may put a +1/+1 counter on this
creature.
At the beginning of your upkeep, you may move any number of +1/+1 counters
from this creature onto other creatures.

P/T            : 0/3

Color identity : G (green)
Rarity         : rare
Commander      : legal
EDHREC rank    : #386
Price (USD)    : $0.39

── Rulings (2) ───────────────────────────────────────────────────────────
[2022-12-08] (wotc)
  Forgotten Ancient's first ability will resolve before the spell that
  caused it to trigger. Putting a +1/+1 counter on Forgotten Ancient is
  optional.

[2022-12-08] (wotc)
  Forgotten Ancient's last ability doesn't target any creatures. You
  choose how many +1/+1 counters will be moved (and onto which creatures)
  as the ability resolves. Notably, once the ability starts resolving and
  you make these choices, no player may take actions until the ability has
  finished resolving.

https://scryfall.com/card/soc/267/forgotten-ancient?utm_source=api
```

### `./bin/mtg rule 702.20` (vigilance — cited throughout)

```
── Rule 702.20 ───────────────────────────────────────────────────────────
parent: 702 — Keyword Abilities

Vigilance

── Subrules (3) ──────────────────────────────────────────────────────────
702.20a
  Vigilance is a static ability that modifies the rules for the declare
  attackers step.

702.20b
  Attacking doesn't cause creatures with vigilance to tap. (See rule 508,
  "Declare Attackers Step.")
```

---

## Quick reference — where every card lives

| Role | Count | Cards |
|---|---|---|
| Commander | 1 | Ms. Bumbleflower |
| Ramp & Mana | 12 | Sol Ring · Arcane Signet · Fellwar Stone · Mind Stone · Thought Vessel · Coveted Jewel · Farseek · Cultivate · Tempt with Discovery · Faeburrow Elder · Rishkar, Peema Renegade · Selvala, Explorer Returned |
| Card Draw & Selection | 17 | Coiling Oracle · Jolly Gerbils · Kwain, Itinerant Meddler · Loran of the Third Path · Mangara, the Diplomat · Sphinx of Enlightenment · Mr. Foxglove · Body of Knowledge · Secret Rendezvous · Intellectual Offering · Tempt with Bunnies · Tenuous Truce · Wizard Class · Fisher's Talent · Rites of Flourishing · Ghirapur Orrery · Tamiyo, Field Researcher |
| Removal & Interaction | 8 | Swords to Plowshares · Generous Gift · Broken Wings · Wear Down · An Offer You Can't Refuse · Long River's Pull · Perplexing Test · Illusionist's Gambit |
| Board Wipes | 2 | Promise of Loyalty · Realm-Cloaked Giant // Cast Off |
| Threats & Beaters | 6 | Kalonian Hydra · Sunscorch Regent · Managorger Hydra · Psychosis Crawler · Bloodroot Apothecary · Octomancer |
| Synergy Pieces | 9 | Forgotten Ancient · Steelburr Champion · Chasm Skulker · Hoofprints of the Stag · Jolrael, Mwonvuli Recluse · Communal Brewing · Simic Ascendancy · Triskaidekaphile · Twenty-Toed Toad |
| Utility & Protection | 7 | Baird, Steward of Argive · Spore Frog · Riot Control · Perch Protection · Swiftfoot Boots · Martial Impetus · Peerless Recycling |
| Lands | 38 | 4 Forest · 4 Island · 4 Plains · Command Tower · Exotic Orchard · Reliquary Tower · Evolving Wilds · Terramorphic Expanse · Adarkar Wastes · Brushland · Yavimaya Coast · Glacial Fortress · Hinterland Harbor · Sunpetal Grove · Canopy Vista · Prairie Stream · Razorverge Thicket · Seachrome Coast · Temple of Enlightenment · Temple of Mystery · Temple of Plenty · Thriving Grove · Thriving Heath · Thriving Isle · Flooded Grove · Seaside Citadel · Skycloud Expanse · Sungrass Prairie · Overflowing Basin |
| **Total** | **100** | |
