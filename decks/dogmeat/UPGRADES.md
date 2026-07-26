# Scrappy Survivors — Upgrade Path

**Deck:** Scrappy Survivors · **Commander:** Dogmeat, Ever Loyal · **Colors:** Naya (`{R}{G}{W}`) · **Slug:** `dogmeat`
**Current bracket:** 2 (Core) — verified with `./bin/mtg deck bracket dogmeat`
**Format:** Commander / EDH only. Commander has **no sideboard** — every change here is a straight 1-for-1 swap inside the 100-card deck.

> **Read this first.** You do not have to buy anything. This precon already works. The tiers below are a *shopping order*, not a to-do list — Tier 0 costs nothing at all, and if you stop after Tier 1 (four dollars and thirty cents) you will already have fixed the deck's two real problems. Skip to the closing note if you want the short version.

---

## Table of contents

1. [What this deck actually needs](#1-what-this-deck-actually-needs)
2. [Words used in this file](#2-words-used-in-this-file)
3. [Tier 0 — Free (cards Omar already owns)](#tier-0--free-cards-omar-already-owns)
4. [Tier 1 — Under $5 total](#tier-1--under-5-total)
5. [Tier 2 — Under $20 total](#tier-2--under-20-total)
6. [Tier 3 — Under $50 total](#tier-3--under-50-total)
7. [The whole picture, tier by tier](#7-the-whole-picture-tier-by-tier)
8. [Do NOT buy these yet](#8-do-not-buy-these-yet)
9. [Appendix — raw CLI output](#9-appendix--raw-cli-output)
10. [Closing note](#10-closing-note)

---

## 1. What this deck actually needs

Run this yourself before you believe me:

```
./bin/mtg deck stats dogmeat -v
./bin/mtg deck bracket dogmeat
```

Here is what the numbers say, in order of how much they hurt.

### Problem A — the deck cannot answer anything (worst problem)

`mtg deck stats dogmeat -v` role counts, over 61 maindeck non-land cards:

| Role | Count | What that means |
|---|---:|---|
| removal | **4** | Break Down · Megaton's Fate · Path to Exile · Valorous Stance |
| boardwipe | **1** | Single Combat |
| tutor | **0** | nothing searches your library for a spell |
| interaction | 6 | Almost Perfect · Cait, Cage Brawler · Champion's Helm · Heroic Intervention · Swiftfoot Boots · Valorous Stance |

Four answers in 99 cards. In a four-player game, three opponents will each resolve a threat you cannot touch. Two of those four "answers" are also conditional — `mtg card "Valorous Stance"` reads *"Destroy target creature with toughness 4 or greater"*, so it whiffs on small creatures; `mtg card "Break Down"` reads *"Destroy target artifact or enchantment"*, so it cannot touch a creature at all.

### Problem B — your own board wipes are aimed at you

This is the sneaky one, and it is a rules interaction, not an opinion.

- `mtg card "Blasphemous Act"` → `{8}{R}`, Sorcery, *"This spell costs {1} less to cast for each creature on the battlefield. Blasphemous Act deals 13 damage to each creature."*
- `mtg card "Single Combat"` → `{3}{W}{W}`, Sorcery, *"Each player chooses a creature or planeswalker they control, then sacrifices the rest. Players can't cast creature or planeswalker spells until the end of your next turn."*

Both kill **your** creatures too. And when your creature dies, every Aura on it dies with it — that is a hard rule, not a card:

```
./bin/mtg rule 704.5m
  If an Aura is attached to an illegal object or player, or is not attached
  to an object or player, that Aura is put into its owner's graveyard.
```

So a deck holding 15 Auras loses far more to a symmetrical wipe than the opponent who is playing five vanilla creatures. Every other deck at the table takes a trade; you take a trade **plus** you dump your enchantments in the bin. Blasphemous Act is the single most self-destructive card in the 99.

### Problem C — the mana base is bloated and slow

From `mtg deck stats dogmeat -v`:

```
land count: HEAVY on lands
- Average mana value of the 61 maindeck non-lands is 2.82
- The usual EDH heuristic puts that at 34-36 lands (adjusted -1 for 11 ramp pieces).
  This deck runs 38.
- 38 lands is 2 above the 34-36 band — expect flood
- Total mana sources = 38 lands + 11 ramp = 49.
- 12 lands can enter tapped (7 always, 5 conditionally) — 32% of the mana base.
```

Seven of those lands cannot produce a colored mana at all (Ash Barrens, Buried Ruin, Junktown, Roadside Reliquary, Rogue's Passage, Scavenger Grounds, Temple of the False God). Against a three-color commander that costs `{R}{G}{W}`, that is a lot of dead weight. `mtg card "Temple of the False God"` is the worst offender: *"{T}: Add {C}{C}. Activate only if you control five or more lands"* — it produces **zero** mana on turns 1-4 and can never cast a single colored spell in this deck.

You can see it in a goldfish (a solo practice draw, no opponents):

```
./bin/mtg deck goldfish dogmeat --seed 13 --turns 8
T7  draw: Temple of Plenty (land)
     lands seen 7 · in play 7 [W,R,G] · played Temple of Plenty · hand 7
```

Seven lands on turn seven in a deck whose average spell costs 2.82.

### Problem D — no way to find your payoff, no insurance when it dies

Zero tutors means you cannot go get Strong Back or Mantle of the Ancients when you need them. And the deck's whole plan is "stack attachments on one creature" — which means one removal spell from an opponent can undo four turns of work. `mtg card "Cass, Hand of Vengeance"` and `mtg card "Inventory Management"` are the existing insurance, and they are excellent, but two cards is not a package.

### What is already good (do not touch these)

The attachment-density engine is genuinely strong and every upgrade below is designed to feed it:

- `mtg card "Strong Back"` → `{2}{G}`, *"Equip abilities you activate that target enchanted creature cost {3} less to activate. Aura spells you cast that target enchanted creature cost {3} less to cast. Enchanted creature gets +2/+2 for each Aura and Equipment attached to it."*
- `mtg card "All That Glitters"` → `{1}{W}`, *"Enchanted creature gets +1/+1 for each artifact and/or enchantment you control."*
- `mtg card "Mantle of the Ancients"` → `{3}{W}{W}`, *"When this Aura enters, return any number of target Aura and/or Equipment cards from your graveyard to the battlefield attached to enchanted creature. Enchanted creature gets +1/+1 for each Aura and Equipment attached to it."*
- `mtg card "Puresteel Paladin"` → `{W}{W}`, *"Whenever an Equipment you control enters, you may draw a card. Metalcraft — Equipment you control have equip {0} as long as you control three or more artifacts."*

**Priority order for spending:** removal first → mana base second → card draw third → protection fourth → bigger payoffs last.

---

## 2. Words used in this file

Look any of these up yourself with `./bin/mtg glossary <term>` or `./bin/mtg rule <number>`.

> **How quotes work here.** Text in quotation marks is copied from the database — verify it with `mtg card "<name>"`, `mtg rule <number>` or `mtg glossary "<term>"`. A card's printed text spans several lines; quoting it inline turns each line break into a sentence break. An ellipsis (**…**) marks a cut *inside* a quote — almost always **reminder text**, the parenthetical a card prints to restate a keyword it already has (e.g. "hexproof *(It can't be the target of spells or abilities your opponents control.)*"). Reminder text changes nothing about how a card works. **No ability, cost, condition or number is ever cut.**

| Term | Plain English | Chase it |
|---|---|---|
| **Aura** | An enchantment that attaches to something. It picks its target when you cast it (`mtg rule 303.4a`). If the thing it is on leaves, the Aura goes to the graveyard (`mtg rule 704.5m`). | `mtg glossary Aura` |
| **Equipment** | An artifact you attach to a creature by paying its **equip** cost. Unlike an Aura, it stays on the battlefield when the creature dies. | `mtg glossary Equip` |
| **Modified** | *"A modified creature is a creature that has a counter on it, is equipped, or is enchanted by an Aura its controller also controls."* — `mtg glossary Modified`. (`mtg rule 700.9` states the same test for permanents generally.) | `mtg glossary Modified` |
| **Umbra armor** (old name: totem armor) | *"If enchanted permanent would be destroyed, instead remove all damage marked on it and destroy this Aura."* — `mtg rule 702.89a`. A one-use shield built into an Aura. | `mtg glossary umbra armor` |
| **Hexproof** | Opponents cannot target it. You still can. (`mtg rule 702.11`) | `mtg glossary hexproof` |
| **Shroud** | *"This permanent or player can't be the target of spells or abilities."* — `mtg rule 702.18a`. **Nobody** can target it, including you. This matters a lot below. | `mtg glossary shroud` |
| **Protection from creatures** | Cannot be blocked by creatures, cannot be damaged by creatures, cannot be targeted by creature abilities (`mtg rule 702.16b`, `702.16e`, `702.16f`). | `mtg glossary protection` |
| **Ward {2}** | If an opponent targets it, they must pay {2} more or their spell is countered. | `mtg glossary ward` |
| **State-based action** | *"Game actions that happen automatically whenever certain conditions are met."* — `mtg glossary "State-Based Actions"`, rule 704. In this deck the one that bites is "an Aura with nothing legal to enchant goes to the graveyard" (`mtg rule 704.5m`). Nobody has to do anything for these to happen. | `mtg glossary "State-Based Actions"` |
| **Flashback** | Lets you cast a card a second time, from your graveyard, for a different cost. Then it is exiled. | `mtg glossary flashback` |
| **Escalate** | On a modal spell: pay an extra cost to choose more than one mode. | `mtg glossary escalate` |
| **Living weapon** | *"A keyword ability that creates a 0/0 black Phyrexian Germ creature token and then attaches the Equipment with the ability to that token."* — `mtg glossary "living weapon"`, rule 702.92. The Equipment brings its own creature to hold it. | `mtg glossary "living weapon"` |
| **Goldfish** | Practising your draws with no opponent, to see how the deck flows. `mtg deck goldfish dogmeat --seed 5 --turns 10` | — |
| **Bracket** | Commander's power-level scale, 1 (Exhibition) to 5. Bracket 2 = "Core / precon level". Bracket 2 allows **zero** Game Changers. | `mtg deck bracket dogmeat` |
| **Game Changer** | A specific list of 53 cards (in `data/brackets.json`) that Wizards flags as raising a deck's power. Playing even one pushes you out of Bracket 2. | see §8 |

---

## Tier 0 — Free (cards Omar already owns)

You own three precons. Cards can legally move between decks **only if the moved card's color identity fits the receiving commander's color identity** — that is rule `mtg rule 903.4`: *"The color identity of a card is the color or colors of any mana symbols in that card's mana cost or rules text, plus any colors defined by its characteristic-defining abilities … or color indicator …"*

- Dogmeat is `{R}{G}{W}` → Naya (white/red/green).
- Tidus and Ms. Bumbleflower are both Bant (`{G}{U}{W}`) → green/blue/white.

The overlap is **green, white, and colorless**. Nothing blue or red can move from those decks into this one. I checked with:

```
./bin/mtg search "deck:tidus"        # then filtered to G/W/colorless identity
./bin/mtg search "deck:bumbleflower"
```

> ### ⚠️ The honest cost of Tier 0
> There is no free lunch. A card can only be in one deck at a time. Every swap below **weakens Tidus or Ms. Bumbleflower by exactly one card.** If you play those decks regularly, do the Tier 0 swaps you like and buy replacements later; if Scrappy Survivors is your main deck, take them all. The per-swap cost is spelled out each time.

> **One more card you already own.** **Generous Gift** sits in Ms. Bumbleflower and is legal here (`[W]` identity). It is written up as a *paid* swap at **T2-7** rather than listed as T0-7, because taking it on top of T0-1 strips Ms. Bumbleflower of both of its unconditional answers, and `decks/tidus/UPGRADES.md` swap 0-5 also wants that same single copy. Read T2-7 before you decide; the card is 69 cents if you would rather not fight over it.

### T0-1 · Swords to Plowshares → in, Squirrel Nest → out

- **IN: Swords to Plowshares** — `{W}` · Instant · **$1.30** (free — from Ms. Bumbleflower)
  > *"Exile target creature. Its controller gains life equal to its power."*
  Ruling (2022-12-08): *"Use the power of the creature from when it was last on the battlefield to determine how much life is gained."*
- **OUT: Squirrel Nest** — `{1}{G}{G}` · Enchantment — Aura · *"Enchant land. Enchanted land has '{T}: Create a 1/1 green Squirrel creature token.'"*
  It is the weakest link because it is a three-mana Aura that goes on a **land**, so it does nothing for your two biggest payoffs: Strong Back (*"+2/+2 for each Aura and Equipment attached to it"*) and Mantle of the Ancients (same wording) only count attachments on the enchanted **creature**. Squirrel Nest is never on one. It does still count for All That Glitters (*"each artifact and/or enchantment you control"*) — that is its only contribution, and it is a weak one for three mana. Making one 1/1 per turn, starting the turn after you cast it, is far too slow.
- **Why:** takes removal from 4 → 5. One mana to permanently delete any creature in the game — no toughness clause like Valorous Stance, no artifact-only clause like Break Down. It also exiles, which beats indestructible and stops graveyard recursion.
- **Bracket impact:** none. Swords to Plowshares is **not** on the 53-card Game Changers list in `data/brackets.json`. Still Bracket 2.
- **Cost to the other deck:** Ms. Bumbleflower loses its cheapest answer. It keeps Generous Gift, Broken Wings, Riot Control, Perch Protection and Realm-Cloaked Giant, so it is not left defenceless.

### T0-2 · Collective Effort → in, Acquired Mutation → out

- **IN: Collective Effort** — `{1}{W}{W}` · Sorcery · **price not in my data** (free — from Tidus)
  > *"Escalate—Tap an untapped creature you control. (Pay this cost for each mode chosen beyond the first.) Choose one or more — • Destroy target creature with power 4 or greater. • Destroy target enchantment. • Put a +1/+1 counter on each creature target player controls."*
  Ruling (2016-07-13): *"You can tap any untapped creature you control to pay the escalate cost, including one you haven't controlled continuously since the beginning of the turn."*
- **OUT: Acquired Mutation** — `{2}{R}` · Enchantment — Aura · *"Enchant creature. Enchanted creature gets +2/+2 and is goaded. … Whenever enchanted creature attacks, defending player gets two rad counters."*
  It is the weakest link because **goaded** means it forces the enchanted creature to attack someone other than you — so you put it on an *opponent's* creature. That means it is an Aura you control that is not attached to your own creature, so it does nothing for Strong Back or Mantle of the Ancients (both of which count *"each Aura and Equipment attached to it"*, meaning the creature they are on), and it hands an opponent a +2/+2 buff on the way through.
- **Why:** removal 5 → 6, and it is your only card that can destroy an **enchantment** other than Break Down. It is also modal, so it is rarely dead. Note the counters mode is a nice bonus with `mtg rule 700.9` — counters make a creature *modified*, which turns on Lion Umbra later.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.
- **Cost to the other deck:** Tidus loses a flexible removal spell. It keeps Path to Exile, Destroy Evil, Damning Verdict, Promise of Loyalty and Farewell, so it is still the best-defended of the three decks.

### T0-3 · Loran of the Third Path → in, Junktown → out

- **IN: Loran of the Third Path** — `{2}{W}` · Legendary Creature — Human Artificer · 2/1 · $3.81 (free — from Ms. Bumbleflower)
  > *"Vigilance. When Loran enters, destroy up to one target artifact or enchantment. {T}: You and target opponent each draw a card."*
- **OUT: Junktown** — Land · *"{T}: Add {C}. {4}{R}, {T}, Sacrifice this land: Create three Junk tokens."*
  It is the weakest link because it produces only colorless mana, and its ability costs **five mana plus the land itself** to make three Junk tokens — a rate you will essentially never pay in a deck whose average spell costs 2.82.
- **Why:** removal 6 → 7, this time stapled to a body that can hold your Auras. "Vigilance" means it does not tap to attack, so you can still use its draw ability. This also starts fixing Problem C: lands 38 → 37, moving toward the 34-36 band that `mtg deck stats` recommends.
- **Bracket impact:** none. Still Bracket 2.
- **Cost to the other deck:** Ms. Bumbleflower loses a solid utility creature.

### T0-4 · Mind Stone → in, Roadside Reliquary → out

- **IN: Mind Stone** — `{2}` · Artifact · **$0.35** (free — from Ms. Bumbleflower)
  > *"{T}: Add {C}. {1}, {T}, Sacrifice this artifact: Draw a card."*
- **OUT: Roadside Reliquary** — Land · *"{T}: Add {C}. {2}, {T}, Sacrifice this land: Draw a card if you control an artifact. Draw a card if you control an enchantment."*
  It is the weakest link because it is another colorless land, and its draw ability costs {2} **and** the land, one time. Mind Stone does the same "sacrifice for a card" job while actually accelerating you in the meantime.
- **Why:** lands 37 → 36, exactly on the top of the 34-36 band. Total mana sources go 49 → 48 but the *quality* rises: a colorless land that only ever makes {C} becomes a rock that ramps on turn 2 and converts to a card in the late game — which is the actual cure for flood.
- **Bracket impact:** none. Still Bracket 2.
- **Cost to the other deck:** Ms. Bumbleflower drops from four two-mana rocks (Arcane Signet, Fellwar Stone, Mind Stone, Thought Vessel) to three. Cheapest possible cost of the six.

### T0-5 · Brushland → in, Temple of the False God → out

- **IN: Brushland** — Land · **$1.75** (free — from Tidus)
  > *"{T}: Add {C}. {T}: Add {G} or {W}. This land deals 1 damage to you."*
- **OUT: Temple of the False God** — Land · *"{T}: Add {C}{C}. Activate only if you control five or more lands."*
  It is the weakest link, full stop. It taps for **nothing** until you have five lands, and it can never help cast a colored spell in a deck whose commander costs `{R}{G}{W}`.
- **Why:** the stats block says 32% of your lands enter tapped and only 7 sources are colorless-only. This swaps a land that is blank on turns 1-4 for one that produces green **or** white on turn 1 at the price of 1 life. Colored sources go up, dead draws go down.
- **Bracket impact:** none. Still Bracket 2.
- **Cost to the other deck:** Tidus loses an untapped green/white dual — a real hit to a two-color-heavy Bant deck. This is the most expensive Tier 0 swap in terms of what it takes away.

### T0-6 · Fortified Village → in, Sunscorched Divide → out

- **IN: Fortified Village** — Land · **$0.23** (free — from Tidus)
  > *"As this land enters, you may reveal a Forest or Plains card from your hand. If you don't, this land enters tapped. {T}: Add {G} or {W}."*
- **OUT: Sunscorched Divide** — Land · *"{1}, {T}: Add {R}{W}."*
  It is the weakest link because it is a "filter" land — it does not make mana, it *converts* mana. On turn 1 with no other lands, it literally cannot produce anything. Sungrass Prairie and Mossfire Valley have the same flaw (they get cut in Tier 1).
- **Why:** you run 12 basics (4 Forest / 4 Mountain / 4 Plains), so revealing a Forest or Plains to make this enter untapped will happen often. Tapped lands drop from 12 to 11.
- **Bracket impact:** none. Still Bracket 2.
- **Cost to the other deck:** Tidus loses another green/white land. If you only take **one** land from Tidus, take Brushland and leave this one.

### Tier 0 running total

| | |
|---|---|
| Swaps | 6 |
| **Money spent** | **$0.00** |
| Removal | 4 → **7** |
| Lands | 38 → **36** |
| Colorless-only lands | 7 → **4** |
| Decks weakened | Tidus (−3 cards), Ms. Bumbleflower (−3 cards) |
| Bracket | **2** (0 Game Changers) |

---

## Tier 1 — Under $5 total

This is the tier that matters most per dollar. Eleven cards, **$4.30**.

### T1-1 · Ethereal Armor — $0.43

- **IN: Ethereal Armor** — `{W}` · Enchantment — Aura · **$0.43**
  > *"Enchant creature. Enchanted creature gets +1/+1 for each enchantment you control and has first strike."*
  Ruling (2021-03-19): *"Ethereal Armor counts each enchantment you control, including itself and any Auras you control that are attached to an opponent or to permanents controlled by an opponent."*
- **OUT: Explorer's Scope** — `{1}` · Artifact — Equipment · *"Whenever equipped creature attacks, look at the top card of your library. If it's a land card, you may put it onto the battlefield tapped. Equip {1}."*
  It is the weakest link because it gives **no stats at all** — a creature carrying it is exactly as big as before — and its upside is finding lands, which is the resource you have *too much* of (Problem C). It is an attachment that makes flood worse.
- **Why:** you run 17 enchantments today. A one-mana Aura that is routinely +5/+5 or bigger, and hands out first strike (deals its combat damage before creatures without it), is one of the best rate-per-mana cards available in these colors. First strike also stops your enchanted creature from trading with a same-sized blocker, which protects your whole Aura stack.
- **Bracket impact:** none — not on the Game Changers list. Still Bracket 2.

### T1-2 · Winds of Rath — $0.34  ⭐ top pick

- **IN: Winds of Rath** — `{3}{W}{W}` · Sorcery · **$0.34**
  > *"Destroy all creatures that aren't enchanted. They can't be regenerated."*
  Ruling (2005-08-01): *"A creature is 'enchanted' if it has any Auras attached to it."*
- **OUT: Blasphemous Act** — `{8}{R}` · Sorcery · *"This spell costs {1} less to cast for each creature on the battlefield. Blasphemous Act deals 13 damage to each creature."*
  It is the weakest link because it is the single most self-destructive card in the deck. It kills your enchanted creature along with everyone else's, and then `mtg rule 704.5m` sends every Aura that was on it to the graveyard. You spend a card to lose more material than any opponent.
- **Why:** this is the fix for Problem B, and it is 34 cents. Your deck runs 15 Auras. Their decks run zero. "Destroy all creatures that aren't enchanted" is a **one-sided board wipe** in your list — you keep the creature carrying your stack, they keep nothing. Boardwipe count stays at 1, but it flips from a card that loses you the game to a card that wins it.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.
- **Careful:** Equipment does **not** make a creature "enchanted". A creature holding only Equipment dies to your own Winds of Rath. Put an Aura on your key creature before you cast it.

### T1-3 · Reyav, Master Smith — $0.23

- **IN: Reyav, Master Smith** — `{R}{W}` · Legendary Creature — Dwarf Artificer · 2/2 · **$0.23**
  > *"Whenever a creature you control that's enchanted or equipped attacks, that creature gains double strike until end of turn."*
  Ruling (2020-11-10): *"If a creature you control that's enchanted and equipped attacks, Reyav's ability will trigger only once for that creature."*
- **OUT: Ian the Reckless** — `{1}{R}` · Legendary Creature — Human Warrior · *"Whenever Ian the Reckless attacks, if it's modified, you may have it deal damage equal to its power to you and any target."*
  It is the weakest link because the damage hits **you** as well as the target. In a deck built to make one creature enormous, that ability will kill you long before it kills a 40-life opponent.
- **Why:** read Reyav's trigger condition next to your commander's: `mtg card "Dogmeat, Ever Loyal"` says *"Whenever a creature you control that's enchanted or equipped attacks, create a Junk token."* Identical wording. Every attack that makes a Junk token now also gives that creature **double strike** (it deals combat damage twice — once with first strike, once normally). That is a straight doubling of your damage output for two mana.
- **Bracket impact:** none. Still Bracket 2.

### T1-4 · Lion Umbra — $0.24

- **IN: Lion Umbra** — `{G}{G}` · Enchantment — Aura · **$0.24**
  > *"Enchant modified creature … Enchanted creature gets +3/+3 and has vigilance and reach. Umbra armor (If enchanted creature would be destroyed, instead remove all damage from it and destroy this Aura.)"*
  Ruling (2024-06-07): *"Umbra armor has no effect if the enchanted creature is put into a graveyard for any other reason, such as if it's sacrificed, if the 'legend rule' applies to it, or if its toughness is 0 or less."*
- **OUT: Brass Knuckles** — `{4}` · Artifact — Equipment · *"When you cast this spell, copy it. … Equipped creature has double strike as long as two or more Equipment are attached to it. Equip {1}. …"*
  It is the weakest link on cost. Casting it does give you two copies, so it can turn itself on — but the full bill is **four mana to cast plus {1} plus {1} to equip both = six mana** before your creature has double strike. Reyav (above) grants double strike for two mana, automatically, on every enchanted or equipped attacker.
- **Why:** this is Problem D's cheapest fix. `mtg rule 702.89a` — *"If enchanted permanent would be destroyed, instead remove all damage marked on it and destroy this Aura"* — means the next Doom Blade an opponent points at your commander kills a 24-cent Aura instead of your whole board. "Enchant modified creature" is not a restriction here: `mtg rule 700.9` says a creature is modified if it has a counter, is equipped, **or** is enchanted by an Aura you control — which describes almost every creature in this deck.
- **Bracket impact:** none. Still Bracket 2.

### T1-5 · Sevinne's Reclamation — $0.36

- **IN: Sevinne's Reclamation** — `{2}{W}` · Sorcery · **$0.36**
  > *"Return target permanent card with mana value 3 or less from your graveyard to the battlefield. If this spell was cast from a graveyard, you may copy this spell and may choose a new target for the copy. Flashback {4}{W}."*
  Ruling (2024-06-07): *"A permanent card is an artifact, battle, creature, enchantment, land, or planeswalker card."*
- **OUT: Agility Bobblehead** — `{3}` · Artifact — Bobblehead · *"{T}: Add one mana of any color. {3}, {T}: Up to X target creatures you control each gain haste until end of turn and can't be blocked this turn except by creatures with haste, where X is the number of Bobbleheads you control as you activate this ability."*
  It is the weakest link because it is a **three-mana rock that produces one mana**. In a deck with an average spell cost of 2.82, spending turn 3 to add one mana is a net loss, and its second ability costs another {3} to use.
- **Why:** direct answer to Problem D. Your creature dies, your Auras hit the graveyard (`mtg rule 704.5m`) — this buys one back onto the battlefield for three mana, then does it a *second* time later from the graveyard via flashback. Two cards' worth of recovery in one slot.
- **Bracket impact:** none. Still Bracket 2.

### T1-6 · Sage's Reverie — $0.34

- **IN: Sage's Reverie** — `{3}{W}` · Enchantment — Aura · **$0.34**
  > *"Enchant creature. When this Aura enters, draw a card for each Aura you control that's attached to a creature. Enchanted creature gets +1/+1 for each Aura you control that's attached to a creature."*
  Ruling (2014-11-24): *"Count the number of Auras you control attached to creatures as the enters-the-battlefield ability resolves to determine how many cards to draw. This will include Sage's Reverie as long as it's still on the battlefield at that time."*
- **OUT: Perception Bobblehead** — `{3}` · Artifact — Bobblehead · *"{T}: Add one mana of any color. {3}, {T}: Look at the top X cards of your library, where X is the number of Bobbleheads you control. You may cast a spell with mana value 3 or less from among them without paying its mana cost. Put the rest on the bottom of your library in a random order."*
  Same problem as the other Bobblehead: three mana for one mana of acceleration, and the card-selection mode needs {3} more **and** multiple Bobbleheads to look at more than one card. You are cutting the second one, so it would be looking at exactly one card.
- **Why:** card draw was listed at 8 sources but most of them are conditional on attacking. This one is unconditional — it replaces itself the moment it lands and then keeps buffing. In a normal board state (Rancor + Strong Back + All That Glitters on one creature) it is "draw 4, and that creature gets +4/+4".
- **Bracket impact:** none. Still Bracket 2.
- **Trade-off, stated plainly:** cutting both Bobbleheads drops your artifact count by 2, which shrinks All That Glitters (*"+1/+1 for each artifact and/or enchantment you control"*) and makes Puresteel Paladin's metalcraft (*"as long as you control three or more artifacts"*) a little harder to switch on. You are paying about two points of All That Glitters to gain an unconditional draw-4 Aura. Take the deal — but know you are making it. Full accounting in §7.

### T1-7 · Unfinished Business — $0.22

- **IN: Unfinished Business** — `{3}{W}{W}` · Sorcery · **$0.22**
  > *"Return target creature card from your graveyard to the battlefield, then return up to two target Aura and/or Equipment cards from your graveyard to the battlefield attached to that creature."*
  Ruling (2023-09-01): *"Any target Equipment cards that can't legally be attached to the creature will enter the battlefield unattached."*
- **OUT: Almost Perfect** — `{4}{G}{W}` · Enchantment — Aura · *"Enchant creature. Enchanted creature has base power and toughness 9/10 and has indestructible."*
  It is the weakest link because **"base power and toughness 9/10" overwrites your work.** It sets the creature to 9/10 and then your other bonuses apply on top — but you are paying six mana for a card that, in a deck where Strong Back alone gives +2/+2 per attachment, is often a *downgrade* on your best creature. Six mana for one Aura is also the worst rate in the deck.
- **Why:** this is the "undo a board wipe" button. One card rebuilds a creature *and* two attachments already assembled. It is the same job Mantle of the Ancients does, at a lower cost and without needing a creature already on the battlefield.
- **Bracket impact:** none. Still Bracket 2.

### T1-8 · Spirit Mantle — $0.35

- **IN: Spirit Mantle** — `{1}{W}` · Enchantment — Aura · **$0.35**
  > *"Enchant creature. Enchanted creature gets +1/+1 and has protection from creatures."*
- **OUT: Idolized** — `{1}{W}` · Enchantment — Aura · *"Enchant creature. Enchanted creature has 'Whenever this creature attacks alone, it gets +X/+X until end of turn, where X is the number of nonland permanents you control.'"*
  It is the weakest link because of the words **"attacks alone."** Your commander's whole text rewards attacking with multiple enchanted or equipped creatures (*"Whenever a creature you control that's enchanted or equipped attacks, create a Junk token"*). Idolized asks you to do the opposite of your own game plan.
- **Why:** protection from creatures does three things at once, all from `mtg rule 702.16`: your creature **can't be blocked** by creatures (702.16f), **takes no damage** from creatures (702.16e), and **can't be targeted** by creature abilities (702.16b). For two mana, your loaded-up threat becomes unblockable and survives combat. That is how you actually close a game.
- **Bracket impact:** none. Still Bracket 2.

### T1-9 · Danitha Capashen, Paragon — $1.00

- **IN: Danitha Capashen, Paragon** — `{2}{W}` · Legendary Creature — Human Knight · 2/2 · **$1.00**
  > *"First strike, vigilance, lifelink. Aura and Equipment spells you cast cost {1} less to cast."*
- **OUT: Single Combat** — `{3}{W}{W}` · Sorcery · *"Each player chooses a creature or planeswalker they control, then sacrifices the rest. Players can't cast creature or planeswalker spells until the end of your next turn."*
  It is the weakest link for the same reason as Blasphemous Act: it is symmetric, and symmetric is bad for you. Note the ruling in `mtg rule 702.89a` does *not* save you here — Single Combat says **sacrifice**, and the Lion Umbra ruling above confirms *"Umbra armor has no effect if the enchanted creature is put into a graveyard for any other reason, such as if it's sacrificed."* Your Auras go to the graveyard either way.
- **Why:** you replace your second self-harming wipe with a discount engine. With 26 attachments in the deck at this point, {1} off every single one of them compounds every turn. Lifelink (you gain life equal to the damage it deals) plus first strike plus vigilance also makes her a fine early body to start stacking on.
- **Bracket impact:** none. Still Bracket 2.

### T1-10 · Battlefield Forge — $0.33

- **IN: Battlefield Forge** — Land · **$0.33** · *"{T}: Add {C}. {T}: Add {R} or {W}. This land deals 1 damage to you."*
- **OUT: Mossfire Valley** — Land · *"{1}, {T}: Add {R}{G}."*
  It is the weakest link because it is a filter land: it needs a mana to make mana, so it is blank on turn 1 and makes zero net mana whenever you are casting a one-drop.
- **Why:** 32% of your lands enter tapped and your commander needs three different colors on turn 3. An untapped red-or-white source for one life is a straight upgrade over a land that cannot function alone.
- **Bracket impact:** none. Still Bracket 2.

### T1-11 · Karplusan Forest — $0.46

- **IN: Karplusan Forest** — Land · **$0.46** · *"{T}: Add {C}. {T}: Add {R} or {G}. This land deals 1 damage to you."*
- **OUT: Sungrass Prairie** — Land · *"{1}, {T}: Add {G}{W}."*
  Same weakness as Mossfire Valley — a filter land that cannot produce mana on its own.
- **Why:** completes the untapped-pain-land pair. Between Battlefield Forge (R/W) and Karplusan Forest (R/G) you now have two more turn-1 colored sources for 79 cents.
- **Bracket impact:** none. Still Bracket 2.

### Tier 1 running total

| # | Card in | Price | Running |
|---:|---|---:|---:|
| 1 | Ethereal Armor | $0.43 | $0.43 |
| 2 | Winds of Rath | $0.34 | $0.77 |
| 3 | Reyav, Master Smith | $0.23 | $1.00 |
| 4 | Lion Umbra | $0.24 | $1.24 |
| 5 | Sevinne's Reclamation | $0.36 | $1.60 |
| 6 | Sage's Reverie | $0.34 | $1.94 |
| 7 | Unfinished Business | $0.22 | $2.16 |
| 8 | Spirit Mantle | $0.35 | $2.51 |
| 9 | Danitha Capashen, Paragon | $1.00 | $3.51 |
| 10 | Battlefield Forge | $0.33 | $3.84 |
| 11 | Karplusan Forest | $0.46 | **$4.30** |

**Tier 1 total: $4.30** · lands stay at 36 · both self-harming wipes gone · Bracket still **2**.

---

## Tier 2 — Under $20 total

Assumes Tier 0 and Tier 1 are done. Twelve cards, **$14.98**.

### T2-1 · Sram, Senior Edificer — $0.81  ⭐ top pick

- **IN: Sram, Senior Edificer** — `{1}{W}` · Legendary Creature — Dwarf Advisor · 2/2 · **$0.81**
  > *"Whenever you cast an Aura, Equipment, or Vehicle spell, draw a card."*
  Ruling (2025-06-06): *"Sram's ability resolves before the spell that caused it to trigger. It resolves even if that spell is countered or otherwise leaves the stack."*
- **OUT: Mister Gutsy** — `{2}` · Artifact Creature — Robot Soldier · 1/1 · *"Whenever you cast an Aura or Equipment spell, put a +1/+1 counter on this creature. When this creature dies, create X Junk tokens, where X is the number of +1/+1 counters on it."*
  It is the weakest link because it has the *same trigger condition* as Sram and pays you far less for it. A 1/1 that grows slowly, versus a 2/2 that draws you a card.
- **Why:** this is the single best card-advantage engine available to this deck at any price. You run 26 attachments coming into this tier — Sram turns more than a quarter of your deck into cantrips (spells that replace themselves). The EDHREC data agrees emphatically:
  ```
  ./bin/mtg edhrec dogmeat --missing --limit 40
  Sram, Senior Edificer     syn  +51.6%    59.9% of 8826 decks
  ```
  That +51.6% synergy score is the highest number in the entire EDHREC report for this commander.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T2-2 · Kor Spiritdancer — $0.36

- **IN: Kor Spiritdancer** — `{1}{W}` · Creature — Kor Wizard · 0/2 · **$0.36**
  > *"This creature gets +2/+2 for each Aura attached to it. Whenever you cast an Aura spell, you may draw a card."*
  Ruling (2010-06-15): *"The second ability triggers when you cast any Aura spell, not just one that targets Kor Spiritdancer."*
- **OUT: Gunner Conscript** — `{1}{G}` · Creature — Human Mercenary · 2/2 · *"Trample. This creature gets +1/+1 for each Aura and Equipment attached to it. When this creature dies, if it was enchanted, create a Junk token. When this creature dies, if it was equipped, create a Junk token."*
  It is the weakest link because Kor Spiritdancer does the same "grows with attachments" job at **double the rate** (+2/+2 per Aura instead of +1/+1) and adds a draw engine on top.
- **Why:** card draw plus a threat in one slot. With Strong Back also attached, a Spiritdancer carrying three Auras is a 0/2 base +6/+6 (Spiritdancer) +6/+6 (Strong Back, +2/+2 per attachment) = an 12/14 for very little mana.
- **Bracket impact:** none. Still Bracket 2.

### T2-3 · Open the Armory — $2.79

- **IN: Open the Armory** — `{1}{W}` · Sorcery · **$2.79**
  > *"Search your library for an Aura or Equipment card, reveal it, put it into your hand, then shuffle."*
- **OUT: Megaton's Fate** — `{5}{R}` · Sorcery · *"Choose one — • Disarm — Destroy target artifact. Create four Treasure tokens. • Detonate — Megaton's Fate deals 8 damage to each creature. Each player gets four rad counters."*
  It is the weakest link because it costs **six mana** and its second mode is a third self-harming board wipe (8 damage to *each* creature, including yours, which then dumps your Auras per `mtg rule 704.5m`). Six mana in a 2.82-average-cost deck is a turn you will rarely have.
- **Why:** this fixes Problem D's other half — `mtg deck stats` reports **tutor: 0**. Two mana to find exactly the attachment the board calls for: Strong Back when you need the discount, Mantle of the Ancients when you need to rebuild, Spirit Mantle when you need to get through. Megaton's Fate was counted as one of your four original removal spells, so cutting it costs you one — but this same tier adds three (Sheltered by Ghosts, Generous Gift, Beast Within), so the tier still ends at 9.
- **Bracket impact:** none. Open the Armory is a *narrow* tutor and is **not** on the Game Changers list — unlike Enlightened Tutor, which is (see §8). Still Bracket 2.

### T2-4 · Snake Umbra — $1.29

- **IN: Snake Umbra** — `{2}{G}` · Enchantment — Aura · **$1.29**
  > *"Enchant creature. Enchanted creature gets +1/+1 and has 'Whenever this creature deals damage to an opponent, you may draw a card.' Umbra armor."*
  Ruling (2010-06-15): *"The ability triggers when the enchanted creature deals any damage, not just combat damage."*
  Ruling (2024-06-07): *"Umbra armor's effect is not regeneration. Specifically, if umbra armor's effect is applied, the enchanted creature does not become tapped and is not removed from combat as a result."*
- **OUT: Fireshrieker** — `{3}` · Artifact — Equipment · *"Equipped creature has double strike. … Equip {2}. …"*
  It is the weakest link because it costs three mana to cast **plus two to equip** = five mana total for double strike, and Reyav, Master Smith (from Tier 1) now hands out double strike for free on every attack.
- **Why:** a second piece of umbra armor insurance, and this one draws cards while it protects. That combination — protection that is also an engine — is exactly what a fragile one-creature deck needs.
- **Bracket impact:** none. Still Bracket 2.

### T2-5 · Sheltered by Ghosts — $1.26

- **IN: Sheltered by Ghosts** — `{1}{W}` · Enchantment — Aura · **$1.26**
  > *"Enchant creature you control. When this Aura enters, exile target nonland permanent an opponent controls until this Aura leaves the battlefield. Enchanted creature gets +1/+0 and has lifelink and ward {2}."*
  Ruling (2024-09-20): *"If a token is exiled this way, it will cease to exist and won't return to the battlefield."*
- **OUT: Silver Shroud Costume** — `{2}` · Artifact — Equipment · *"Flash. When this Equipment enters, attach it to target creature you control. That creature gains shroud until end of turn. … Equipped creature can't be blocked. Equip {3}."*
  It is the weakest link because of **shroud**: `mtg rule 702.18a` — *"This permanent or player can't be the target of spells or abilities."* That includes *your own* Aura spells, which require a target (`mtg rule 303.4a`). Handing shroud to the creature you want to load up is working against yourself. Its equip cost of {3} is also the highest tier in the deck.
- **Why:** removal 6 → 7, and the removal is *attached to your threat*. Two mana that exiles an opponent's best permanent, buffs your creature, gains you life, and gives ward {2} (opponents must pay {2} extra to target it or their spell is countered). Four jobs in one card.
- **Bracket impact:** none. Still Bracket 2.

### T2-6 · Nettlecyst — $3.51

- **IN: Nettlecyst** — `{3}` · Artifact — Equipment · **$3.51**
  > *"Living weapon … Equipped creature gets +1/+1 for each artifact and/or enchantment you control. Equip {2}."*
  Ruling (2021-06-18): *"If a permanent you control is both an artifact and an enchantment, count it only once when determining the bonus from an equipped Nettlecyst."*
- **OUT: Vault 21: House Gambit** — `{1}{R}` · Enchantment — Saga · *"I, II — Discard a card, then draw a card. III — Reveal up to five nonland cards from your hand. For each of those cards that has the same mana value as another card revealed this way, create a Treasure token."*
  It is the weakest link because chapters I and II are "rummage" — they do not gain you cards, they swap them — and chapter III's payoff is conditional on a specific hand shape. Three turns of setup for at most a couple of Treasures.
- **Why:** **living weapon** is the key word (`mtg glossary living weapon`): it creates its own 0/0 Germ creature token and attaches itself. That means Nettlecyst is a threat even when you have no creatures on board — which is precisely your worst position after someone wipes. It also scales on the same axis as All That Glitters.
- **Bracket impact:** none. Still Bracket 2.

### T2-7 · Generous Gift — $0.69 (or **free** — you already own one)

- **IN: Generous Gift** — `{2}{W}` · Instant · **$0.69**
  > *"Destroy target permanent. Its controller creates a 3/3 green Elephant creature token."*
  Ruling (2019-06-14): *"If the target permanent is an illegal target by the time Generous Gift tries to resolve, the spell doesn't resolve. No player creates an Elephant."*
- **💡 You do not have to buy this — take it as a Tier 0 swap for $0.00.** Ms. Bumbleflower already runs
  exactly one copy (verified: `./bin/mtg deck bumbleflower --json`, count 1). Its color identity is `[W]`,
  a subset of Dogmeat's Naya `[W,R,G]`, so the move is legal under `mtg rule 903.4`. Doing that drops the
  Tier 2 bill from **$14.98 to $14.29** and the cumulative all-tiers figure from **$68.57 to $67.88**.
  The tables in §7 and the Tier 2 running total quote the *buy-it* price, so they stay as printed if
  you buy a second copy.
- **⚠️ Two upgrade paths want this same physical card.** `decks/tidus/UPGRADES.md` swap **0-5** claims that
  same single copy for Tidus. Only one deck can have it. Either decide which deck needs it more, or buy
  a second copy for 69 cents — which is why this swap is priced here rather than filed under Tier 0.
- **⚠️ Cost to `bumbleflower` if you move it: high, and it compounds with T0-1.** Swords to Plowshares and
  Generous Gift are that deck's only two answers that hit *any* creature or *any* permanent; its other
  removal is narrow (`Broken Wings` — *"Destroy target artifact, enchantment, or creature with flying"*;
  `Wear Down` — *"… Destroy target artifact or enchantment …"*). Tier 0 swap **T0-1** already takes the
  Swords. Taking both leaves Ms. Bumbleflower with **zero** unconditional removal. If you do both, buy
  the 69-cent copy instead of moving this one.
- **OUT: Crimson Caravaneer** — `{2}{R}` · Creature — Human Scout · 1/2 · *"Double strike, trample. Whenever this creature deals combat damage to a player, create a Junk token."*
  It is the weakest link because it is a **1/2** for three mana. Double strike on one power is one extra damage. It needs several attachments before it does anything, and you have better bodies competing for those attachments.
- **Why:** removal 7 → 8, and this is the flexible kind. "Destroy target permanent" answers a creature, an artifact, an enchantment, a planeswalker, or a land — at instant speed, meaning you can cast it on someone else's turn. Handing over a 3/3 is a real cost, but being able to answer *literally anything* is worth it in a deck with this few outs.
- **Bracket impact:** none. Still Bracket 2.

### T2-8 · Beast Within — $0.48

- **IN: Beast Within** — `{2}{G}` · Instant · **$0.48**
  > *"Destroy target permanent. Its controller creates a 3/3 green Beast creature token."*
- **OUT: Duchess, Wayward Tavernkeep** — `{3}{R}` · Legendary Creature — Human Citizen · 4/3 · *"Hunters for Hire — Whenever a creature you control deals combat damage to a player, put a quest counter on it. {1}, Remove a quest counter from a permanent you control: Create a Junk token."*
  It is the weakest link because its whole output is Junk tokens, and your commander already makes one every time an enchanted or equipped creature attacks. Paying {1} per extra Junk is a poor rate for a card slot.
- **Why:** removal 8 → 9, in your *other* color, so you are never stuck holding an answer you cannot cast. Nine answers in 99 cards is a normal, healthy Commander number.
- **Bracket impact:** none. Still Bracket 2.

### T2-9 · Akiri, Fearless Voyager — $1.32

- **IN: Akiri, Fearless Voyager** — `{1}{R}{W}` · Legendary Creature — Kor Warrior · 3/3 · **$1.32**
  > *"Whenever you attack a player with one or more equipped creatures, draw a card. {W}: You may unattach an Equipment from a creature you control. If you do, tap that creature and it gains indestructible until end of turn."*
  Ruling (2020-09-25): *"Akiri's first ability has you draw just one card per player you attack with an equipped creature, no matter how many equipped creatures you attack them with beyond the first."*
- **OUT: Commander Sofia Daguerre** — `{3}{W}` · Legendary Creature — Human Pilot · 1/3 · *"Flash. Crash Landing — When Commander Sofia Daguerre enters, destroy up to one target legendary permanent. That permanent's controller creates a Junk token. …"*
  It is the weakest link because its removal only hits **legendary** permanents. Against a table that has not played a legendary permanent yet, it is a four-mana 1/3 that does nothing.
- **Why:** a second protection valve. For `{W}` you can pull an Equipment off your key creature and it gains **indestructible** — *"a keyword ability that precludes a permanent from being destroyed"* (`mtg glossary indestructible`) — which saves it from a targeted kill spell or a board wipe. Plus card draw every combat.
- **Bracket impact:** none. Still Bracket 2.

### T2-10 · Strength of the Harvest — $0.37

- **IN: Strength of the Harvest // Haven of the Harvest** — modal double-faced card · mana value 3 · **$0.37**
  > Front face — **Strength of the Harvest**, `{2}{G/W}`, Enchantment — Aura: *"Enchant creature. Enchanted creature gets +1/+1 for each creature and/or enchantment you control."*
  > Back face — **Haven of the Harvest**, Land: *"This land enters tapped. {T}: Add {G} or {W}."*
- **OUT: Evolving Wilds** — Land · *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle."*
  It is the weakest link because it always enters, taps for nothing, then fetches a **tapped** basic — two turns of tapped mana for one land drop. You already run Terramorphic Expanse, which is the identical card.
- **Why:** this is how you cut a land without cutting a land. A modal double-faced card lets you *choose*, when you play it, whether it is a spell or a land. Flooding? Play it as a land. Have plenty? Cast a huge Aura. Your nominal land count drops to 35 but your practical land drops stay at 36 — with the upside that this "land" can be a game-ending Aura instead.
- **Bracket impact:** none. Still Bracket 2.

### T2-11 · Fabled Passage — $1.16

- **IN: Fabled Passage** — Land · **$1.16**
  > *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle. Then if you control four or more lands, untap that land."*
- **OUT: Terramorphic Expanse** — Land · *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle."*
  It is the weakest link because it is Fabled Passage without the last sentence — the basic always arrives tapped, no exceptions.
- **Why:** identical effect, except from your fourth land onward the fetched basic **untaps**. Tapped-land count falls, and you fix all three colors on demand.
- **Bracket impact:** none. Still Bracket 2.

### T2-12 · Bruenor Battlehammer — $0.94

- **IN: Bruenor Battlehammer** — `{2}{R}{W}` · Legendary Creature — Dwarf Warrior · 5/3 · **$0.94**
  > *"Each creature you control gets +2/+0 for each Equipment attached to it. You may pay {0} rather than pay the equip cost of the first equip ability you activate each turn."*
- **OUT: Masterwork of Ingenuity** — `{1}` · Artifact — Equipment · *"You may have this Equipment enter as a copy of any Equipment on the battlefield."*
  It is the weakest link because it does **nothing** if no Equipment is already on the battlefield — it is a card that is only good when you were already winning.
- **Why:** solves the equip-cost tax that quietly slows this deck down. The precon shipped with three Equipment at equip {3} — Behemoth Sledge, Pre-War Formalwear and Silver Shroud Costume (the last of those is cut in T2-5, and Behemoth Sledge goes in T3-2, so this mostly protects Pre-War Formalwear and Champion's Helm). Bruenor makes the first equip each turn free, which is the difference between deploying one attachment a turn and two. The +2/+0 per Equipment also applies to *every* creature you control, not just one.
- **Bracket impact:** none. Still Bracket 2.

### Tier 2 running total

| # | Card in | Price | Running |
|---:|---|---:|---:|
| 1 | Sram, Senior Edificer | $0.81 | $0.81 |
| 2 | Kor Spiritdancer | $0.36 | $1.17 |
| 3 | Open the Armory | $2.79 | $3.96 |
| 4 | Snake Umbra | $1.29 | $5.25 |
| 5 | Sheltered by Ghosts | $1.26 | $6.51 |
| 6 | Nettlecyst | $3.51 | $10.02 |
| 7 | Generous Gift *(or $0.00 — move Ms. Bumbleflower's copy; see T2-7)* | $0.69 | $10.71 |
| 8 | Beast Within | $0.48 | $11.19 |
| 9 | Akiri, Fearless Voyager | $1.32 | $12.51 |
| 10 | Strength of the Harvest | $0.37 | $12.88 |
| 11 | Fabled Passage | $1.16 | $14.04 |
| 12 | Bruenor Battlehammer | $0.94 | **$14.98** |

**Tier 2 total: $14.98** (cumulative with Tier 1: **$19.28**) · removal 7 → **9** · tutors 0 → **1** · Bracket still **2**.
*If you move Ms. Bumbleflower's Generous Gift instead of buying one, Tier 2 is **$14.29** and the cumulative figure is **$18.59** — read the warning under T2-7 first.*

---

## Tier 3 — Under $50 total

The luxury tier. Ten cards, **$49.29**. Nothing here is *needed*; everything here is a step up in raw power. Do not start with this tier.

### T3-1 · Ardenn, Intrepid Archaeologist — $5.26  ⭐ top pick

- **IN: Ardenn, Intrepid Archaeologist** — `{2}{W}` · Legendary Creature — Kor Scout · 2/2 · **$5.26**
  > *"At the beginning of combat on your turn, you may attach any number of Auras and Equipment you control to target permanent or player. Partner."*
  Ruling (2020-11-10): *"You choose which Auras and Equipment to move as Ardenn's ability resolves. Players can't take actions between the time you choose what to move and the time they're attached to the target permanent or player."*
- **OUT: Three Dog, Galaxy News DJ** — `{1}{R}{W}` · Legendary Creature — Human Bard · 1/5 · *"Whenever you attack, you may pay {2} and sacrifice an Aura attached to Three Dog. When you sacrifice an Aura this way, for each other attacking creature you control, create a token that's a copy of that Aura attached to that creature."*
  It is the weakest link because the ability asks you to pay {2} **and destroy one of your own Auras**, and only pays off if you have several other attackers. In a deck that concentrates attachments on one creature, that condition is rarely met, and a 1/5 body contributes almost nothing.
- **Why:** this is the highest-leverage card in the whole plan. At the beginning of combat every turn, for **zero mana**, you consolidate your entire attachment stack onto whichever creature is best placed — no equip costs, no Aura re-casting. When a loaded creature dies, its Equipment stays on the battlefield (only Auras fall off, per `mtg rule 704.5m`), and Ardenn re-deploys all of it for free on your next turn. That turns "they killed my guy" from a disaster into a one-turn delay.
  Two things to be clear about: the trigger only happens **at the beginning of combat on your turn**, so it cannot be used in response to a removal spell — it is a rebuild tool, not a save. And Ardenn has **partner** (*"You can have two commanders if both have partner"*), but Dogmeat does not have partner, so Ardenn goes in the 99 as a normal creature. That is fine — it is exactly as good there.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T3-2 · Forge Anew — $5.77

- **IN: Forge Anew** — `{2}{W}` · Enchantment · **$5.77**
  > *"When this enchantment enters, return target Equipment card from your graveyard to the battlefield. During your turn, you may activate equip abilities any time you could cast an instant. You may pay {0} rather than pay the equip cost of the first equip ability you activate during each of your turns."*
- **OUT: Behemoth Sledge** — `{1}{G}{W}` · Artifact — Equipment · *"Equipped creature gets +2/+2 and has trample and lifelink. Equip {3}."*
  It is the weakest link because equip {3} is the most expensive tier in the deck — three mana to cast plus three to attach is six mana for +2/+2. Forge Anew makes that same class of card free to move, so you want to cut the tax, not pay it.
- **Why:** three separate upgrades in one card — Equipment recursion, a second free equip each turn (stacks with Bruenor: two free equips per turn), and instant-speed equipping, which lets you move Equipment *after* blockers are declared or in response to a removal spell.
- **Bracket impact:** none. Still Bracket 2.

### T3-3 · Sword of the Animist — $6.65

- **IN: Sword of the Animist** — `{2}` · Legendary Artifact — Equipment · **$6.65**
  > *"Equipped creature gets +1/+1. Whenever equipped creature attacks, you may search your library for a basic land card, put it onto the battlefield tapped, then shuffle. Equip {2}."*
- **OUT: Wild Growth** — `{G}` · Enchantment — Aura · *"Enchant land. Whenever enchanted land is tapped for mana, its controller adds an additional {G}."*
  It is the weakest link among your land-Auras because it only produces **green**, while Abundant Growth (*"Enchanted land has '{T}: Add one mana of any color'"* — and it draws a card when it enters) and Fertile Ground (*"adds an additional one mana of any color"*) both fix all three colors. In a `{R}{G}{W}` deck, extra green is the least useful kind of extra mana. Like Squirrel Nest, it also sits on a land, so it never counts for Strong Back or Mantle of the Ancients.
- **Why:** replaces that ramp with ramp that is *also* an attachment. Every attack fetches a basic, which thins your deck and fixes colors, while the Equipment itself counts for Strong Back, All That Glitters, Nettlecyst and Mantle of the Ancients.
- **Bracket impact:** none. Still Bracket 2.

### T3-4 · Sythis, Harvest's Hand — $4.76

- **IN: Sythis, Harvest's Hand** — `{G}{W}` · Legendary Enchantment Creature — Nymph · 1/2 · **$4.76**
  > *"Whenever you cast an enchantment spell, you gain 1 life and draw a card."*
  Ruling (2021-06-18): *"Sythis, Harvest Hand's ability doesn't trigger when it is cast."*
- **OUT: Armory Paladin** — `{1}{R}{W}` · Creature — Human Knight · 3/3 · *"Trample. Whenever you cast an Aura or Equipment spell, exile the top card of your library. You may play that card until the end of your next turn."*
  It is the weakest link because its "impulse draw" has a deadline — if you cannot pay for the exiled card before the end of your next turn, it is gone forever. Sythis puts the card in your hand permanently, for one less mana.
- **Why:** a second Sram. After all the earlier tiers you run roughly 20 enchantments; Sythis converts each one into a card and a life. Two-mana engines that draw this consistently are the backbone of every good enchantment deck.
- **Bracket impact:** none. Still Bracket 2.

### T3-5 · Ancestral Mask — $2.41

- **IN: Ancestral Mask** — `{2}{G}` · Enchantment — Aura · **$2.41**
  > *"Enchant creature. Enchanted creature gets +2/+2 for each other enchantment on the battlefield."*
- **OUT: Animal Friend** — `{1}{G}` · Enchantment — Aura · *"Enchant creature. Enchanted creature has 'Whenever this creature attacks, create a 1/1 green Squirrel creature token. Put a +1/+1 counter on that token for each Aura and Equipment attached to this creature other than Animal Friend.'"*
  It is the weakest link because it gives the enchanted creature **no stats of its own** and only pays off on attack, one token at a time — a slow, small return on a slot that could be swinging the game.
- **Why:** read the wording carefully — *"each **other** enchantment on the battlefield"*, not "you control." It counts your opponents' enchantments too. With around 20 enchantments in your own deck and typically a few across the table, this is regularly +14/+14 or more for three mana. It is the single largest stat swing available to you at this price.
- **Bracket impact:** none. Still Bracket 2.

### T3-6 · Kutzil, Malamet Exemplar — $3.93

- **IN: Kutzil, Malamet Exemplar** — `{1}{G}{W}` · Legendary Creature — Cat Warrior · 3/3 · **$3.93**
  > *"Your opponents can't cast spells during your turn. Whenever one or more creatures you control each with power greater than its base power deals combat damage to a player, draw a card."*
  Ruling (2023-11-10): *"Normally, a creature's base power and toughness are the power and toughness printed on the card… If an effect modifies a creature's power and/or toughness without setting them, that is not included when determining its base power and toughness."*
- **OUT: Sticky Fingers** — `{R}` · Enchantment — Aura · *"Enchant creature. Enchanted creature has menace and 'Whenever this creature deals combat damage to a player, create a Treasure token.' … When enchanted creature dies, draw a card."*
  It is the weakest link at this stage because its main payoff — a Treasure token per hit — is ramp, and by Tier 3 you have Sword of the Animist, Mind Stone and 36 lands. It is the last of your low-impact one-mana Auras.
- **Why:** the first line is a shield you cannot buy any other way. *"Your opponents can't cast spells during your turn"* means nobody can destroy your loaded creature in response to your attack — the exact scenario that loses this deck games. The draw trigger is close to automatic here, since every Aura you control raises a creature's power above its base power.
- **Bracket impact:** none. Still Bracket 2.

### T3-7 · Bear Umbra — $12.09

- **IN: Bear Umbra** — `{2}{G}{G}` · Enchantment — Aura · **$12.09**
  > *"Enchant creature. Enchanted creature gets +2/+2 and has 'Whenever this creature attacks, untap all lands you control.' Umbra armor."*
  Ruling (2024-06-07): *"If a creature you control is enchanted with multiple Auras that have umbra armor, and the enchanted creature would be destroyed, one of those Auras is destroyed instead—but only one of them. You choose which one because you control the enchanted creature."*
- **OUT: Grim Reaper's Sprint** — `{4}{R}` · Enchantment — Aura · *"Morbid — This spell costs {3} less to cast if a creature died this turn. Enchant creature. When this Aura enters, untap each creature you control. If it's your main phase, there is an additional combat phase after this phase. Enchanted creature gets +2/+2 and has haste."*
  It is the weakest link because at full price it is a **five-mana** Aura, and its discount requires a creature to have died this turn — a condition you do not reliably control. Bear Umbra does the "get more mana out of a combat" job every single turn, not once.
- **Why:** your third umbra armor, and the strongest. Untapping all your lands when you attack effectively doubles your mana on your own turn — cast the attachments, attack, untap, cast more. Combined with Ardenn's free re-attach, that is a genuine engine turn.
- **Careful:** the price is the highest single line in this document. If $12 is too much, Lion Umbra (Tier 1, $0.24) and Snake Umbra (Tier 2, $1.29) already cover the protection role; Bear Umbra is the upgrade, not the requirement.
- **Bracket impact:** none. Still Bracket 2.

### T3-8 · Sundown Pass — $2.06

- **IN: Sundown Pass** — Land · **$2.06** · *"This land enters tapped unless you control two or more other lands. {T}: Add {R} or {W}."*
- **OUT: Temple of Triumph** — Land · *"This land enters tapped. When this land enters, scry 1. … {T}: Add {R} or {W}."*
  It is the weakest link because it **always** enters tapped. Scry 1 (look at your top card, optionally bottom it) is a nice bonus but not worth a full turn of tempo every time.
- **Why:** identical colors, but untapped from your third land onward. This is a straight tempo gain with zero fixing loss.
- **Bracket impact:** none. Still Bracket 2.

### T3-9 · Overgrown Farmland — $3.59

- **IN: Overgrown Farmland** — Land · **$3.59** · *"This land enters tapped unless you control two or more other lands. {T}: Add {G} or {W}."*
- **OUT: Temple of Plenty** — Land · *"This land enters tapped. When this land enters, scry 1. … {T}: Add {G} or {W}."*
  Same weakness — always tapped.
- **Why:** same green/white pair, untapped from land three onward.
- **Bracket impact:** none. Still Bracket 2.

### T3-10 · Rockfall Vale — $2.77

- **IN: Rockfall Vale** — Land · **$2.77** · *"This land enters tapped unless you control two or more other lands. {T}: Add {R} or {G}."*
- **OUT: Temple of Abandon** — Land · *"This land enters tapped. When this land enters, scry 1. … {T}: Add {R} or {G}."*
  Same weakness — always tapped.
- **Why:** completes the set. All three Temples out, all three color pairs still covered, and the *unconditional* tapped-land count drops by three at once.
  Be precise about what changed. The original stats block reads `lands entering tapped: 12 (7 always, 5 conditional)`. After every tier in this document, the raw count of lands that *can* enter tapped is about the same — but the split moves from **7 always / 6 conditional** to **4 always / 9 conditional**, and the conditions get much easier: "unless you control two or more other lands" (Sundown Pass, Overgrown Farmland, Rockfall Vale) is satisfied from your third land onward, every game. A Temple is tapped on turn 8. Rockfall Vale is not.
- **Bracket impact:** none. Still Bracket 2.

### Tier 3 running total

| # | Card in | Price | Running |
|---:|---|---:|---:|
| 1 | Ardenn, Intrepid Archaeologist | $5.26 | $5.26 |
| 2 | Forge Anew | $5.77 | $11.03 |
| 3 | Sword of the Animist | $6.65 | $17.68 |
| 4 | Sythis, Harvest's Hand | $4.76 | $22.44 |
| 5 | Ancestral Mask | $2.41 | $24.85 |
| 6 | Kutzil, Malamet Exemplar | $3.93 | $28.78 |
| 7 | Bear Umbra | $12.09 | $40.87 |
| 8 | Sundown Pass | $2.06 | $42.93 |
| 9 | Overgrown Farmland | $3.59 | $46.52 |
| 10 | Rockfall Vale | $2.77 | **$49.29** |

**Tier 3 total: $49.29** (cumulative all tiers: **$68.57**) · Bracket still **2**.

---

## 7. The whole picture, tier by tier

| Measure | Now | After T0 | After T1 | After T2 | After T3 |
|---|---:|---:|---:|---:|---:|
| Money spent (this tier) | — | $0.00 | $4.30 | $14.98 | $49.29 |
| Money spent (cumulative) | — | $0.00 | $4.30 | $19.28 | $68.57 |
| Spot removal | 4 | 7 | 7 | 9 | 9 |
| Board wipes | 1 (kills you) | 1 (kills you) | **1 (one-sided)** | 1 | 1 |
| Tutors | 0 | 0 | 0 | 1 | 1 |
| Lands | 38 | 36 | 36 | 35 (+1 flex face) | 35 (+1 flex face) |
| Colorless-only lands | 7 | 4 | 4 | 4 | 4 |
| Unconditionally-tapped lands | 7 | 7 | 7 | 7 | **4** |
| Filter lands (need mana to make mana) | 3 | 2 | 0 | 0 | 0 |
| Creatures (excl. commander) | 18 | 19 | 20 | 19 | 19 |
| Attachments (Auras + Equipment) | 28 (15+13) | 26 (13+13) | 26 (15+11) | 27 (18+9) | 27 (18+9) |
| Umbra-armor protection | 0 | 0 | 1 | 2 | 3 |
| Game Changers | 0 | 0 | 0 | 0 | 0 |
| **Bracket** | **2** | **2** | **2** | **2** | **2** |

**Two honest trade-offs in this plan:**

1. **Artifact count falls; All That Glitters gets a bit smaller.** Across all four tiers you cut nine artifacts (Explorer's Scope, Brass Knuckles, both Bobbleheads, Mister Gutsy, Fireshrieker, Silver Shroud Costume, Masterwork of Ingenuity, Behemoth Sledge) and add three (Mind Stone, Nettlecyst, Sword of the Animist): **19 → 13**. Enchantments go the other way — nine out, eleven in: **17 → 19**. So the combined pool that All That Glitters and Nettlecyst count (*"each artifact and/or enchantment you control"*) drops from 36 to 32. Puresteel Paladin's metalcraft (*"three or more artifacts"*) also gets a little harder to switch on.
   That is a real cost, and it is worth paying: the enchantment side is where Ethereal Armor (*"+1/+1 for each enchantment you control"*), Ancestral Mask (*"+2/+2 for each other enchantment on the battlefield"*) and Sage's Reverie live, and those three scale far harder than the four points you gave up. If you want to keep the artifact count high instead, the easiest edit to this plan is to keep both Bobbleheads and skip T1-5 and T1-6.
2. **The deck shifts from Equipment-leaning to Aura-leaning** (13 Equipment / 15 Auras → 9 Equipment / 18 Auras). That is deliberate — Winds of Rath only spares *enchanted* creatures, and Ethereal Armor, Ancestral Mask, Sage's Reverie and Strength of the Harvest all count enchantments. It does mean your commander's Junk-token trigger will more often be fired by Auras than Equipment, and it means more of your board is vulnerable to `mtg rule 704.5m` (Auras die with the creature; Equipment does not). That is precisely why the plan buys three pieces of umbra armor and Sevinne's Reclamation / Unfinished Business to rebuy them. Both halves still trigger your commander: *"a creature you control that's enchanted **or** equipped."*

**A note on Bracket 2 and combos.** `mtg deck bracket dogmeat` flags one thing it cannot check: *"Two-card infinite combos: not detected by this tool; requires human/agent review."* Nothing in this list is a known two-card infinite loop as far as my database shows, but I cannot verify combos from card text alone — if you build toward Bracket 2 for a specific pod, mention the list to them.

---

## 8. Do NOT buy these yet

These are all popular, all correct in *some* deck, and all wrong for you right now. I am listing them because EDHREC will keep recommending them and you should know why you are saying no.

### The four Game Changers

`./bin/mtg edhrec dogmeat --missing` returns a section literally headed "Game Changers." Every card in it appears on the 53-card list in `data/brackets.json`. Bracket 2's rule is unambiguous: **"No Game Changers."** Playing even one moves you to Bracket 3 (Upgraded, max 3 Game Changers). That is not a moral failure — it just means you should tell your table before you sit down.

| Card | Cost | Price | Real text | Why not yet |
|---|---|---:|---|---|
| **Smothering Tithe** | `{3}{W}` | **$63.65** | *"Whenever an opponent draws a card, that player may pay {2}. If the player doesn't, you create a Treasure token."* | Your deck's problem is that it cannot answer threats, not that it lacks mana — `mtg deck stats` already counts **49 mana sources**. Sixty-four dollars to fix a problem you do not have. **Game Changer → Bracket 3.** |
| **Teferi's Protection** | `{2}{W}` | **$52.60** | *"Until your next turn, your life total can't change and you gain protection from everything. All permanents you control phase out."* | A superb card and a genuine save from a board wipe — but $52 buys all of Tier 1, Tier 2 and most of Tier 3. **Game Changer → Bracket 3.** |
| **Enlightened Tutor** | `{W}` | **$38.71** | *"Search your library for an artifact or enchantment card, reveal it, then shuffle and put that card on top."* | Open the Armory (Tier 2, $2.79) finds an Aura or Equipment and puts it **in your hand**, not on top of your library. For a beginner, one dollar-per-thirteen of the price and easier to use. **Game Changer → Bracket 3.** |
| **Farewell** | `{4}{W}{W}` | $5.91 | *"Choose one or more — • Exile all artifacts. • Exile all creatures. • Exile all enchantments. • Exile all graveyards."* | Cheap, and Tidus already owns a copy — but it is Problem B in its purest form. Exiling all creatures *and* all enchantments destroys your deck more thoroughly than anyone else's, and exile means no recursion. Winds of Rath is 34 cents and one-sided. **Game Changer → Bracket 3.** |

### Expensive staples that are actively wrong here

| Card | Price | Real text | Why it is wrong for this deck |
|---|---:|---|---|
| **Lightning Greaves** | $3.85 | *"Equipped creature has haste and shroud … Equip {0}"* | **Shroud, not hexproof.** `mtg rule 702.18a`: *"This permanent or player can't be the target of spells or abilities."* Your own Aura spells require a target (`mtg rule 303.4a`), so a creature wearing Greaves **cannot be enchanted by you**. It actively shuts off your deck. Champion's Helm (already in your deck) gives *hexproof* to legendary creatures instead — that only stops opponents. Keep the Helm; skip the Greaves. |
| **Colossus Hammer** | $1.91 | *"Equipped creature gets +10/+10 and loses flying. Equip {8}"* | Equip **eight**. It is only playable in decks built specifically around free-equip effects. You will have Bruenor and Forge Anew eventually, but until then this is a card you cannot use. |
| **Sword of Feast and Famine** | $39.18 | *"Equipped creature gets +2/+2 and has protection from black and from green… Equip {2}"* | Note "protection from **green**." `mtg rule 702.16c`: *"A permanent or player with protection can't be enchanted by Auras that have the stated quality. Such Auras attached to the permanent or player with protection will be put into their owners' graveyards as a state-based action."* You run green Auras — Rancor, Lion Umbra, Snake Umbra, Bear Umbra, Ancestral Mask, Strong Back. They would fall off as a state-based action. A trap in this specific deck. |
| **Shadowspear** | $30.20 | *"Equipped creature gets +1/+1 and has trample and lifelink. {1}: Permanents your opponents control lose hexproof and indestructible until end of turn. Equip {2}"* | Genuinely great, but $30 for +1/+1 and a utility ability aimed at high-power tables. Behemoth Sledge already gives +2/+2, trample and lifelink for a fraction of the price. |
| **Stoneforge Mystic** | $31.34 | *"When this creature enters, you may search your library for an Equipment card… {1}{W}, {T}: You may put an Equipment card from your hand onto the battlefield."* | Your plan is drifting toward Auras (see §7), and Stoneforge only finds Equipment. Open the Armory finds **either** for $2.79. |
| **Boseiju, Who Endures** | $49.35 | *"{T}: Add {G}. Channel — {1}{G}, Discard this card: Destroy target artifact, enchantment, or nonbasic land an opponent controls…"* | $49 for one flexible land. Your mana base problems are solved for under $10 with pain lands and "enters untapped unless" lands. |
| **Halvar, God of Battle** | $25.66 | (double-faced: Legendary Creature — God // Legendary Artifact — Equipment) | Strong, but $25 and complicated to pilot. Ardenn ($5.26) does the "move all my attachments" job better and simpler. |
| **Kodama of the West Tree** | $22.73 | *"Modified creatures you control have trample… Whenever a modified creature you control deals combat damage to a player, search your library for a basic land card, put it onto the battlefield tapped…"* | Excellent synergy, but $22 and its main reward is *more lands* — the thing `mtg deck stats` says you already have too many of. |
| **Mjölnir, Hammer of Thor** | $24.01 | *"Double all damage equipped creature would deal. Equip worthy {1}"* | $24, and "equip worthy" only reduces the cost for legendary red and/or white creatures. Reyav (Tier 1, $0.23) gives double strike to *every* enchanted or equipped attacker. |
| **Power Fist** | $16.40 | *"Equipped creature has trample and 'Whenever this creature deals combat damage to a player, put that many +1/+1 counters on it.' Equip {2}"* | $16 for a card that is win-more: it only pays off after you already connected with a big creature. |
| **Steelshaper's Gift** | $9.13 | *"Search your library for an Equipment card, reveal that card, put it into your hand, then shuffle."* | Open the Armory finds Auras **and** Equipment for $2.79. This is only better if you go heavily Equipment, which this plan does not. |
| **Idyllic Tutor** | $12.60 | *"Search your library for an enchantment card, reveal it, put it into your hand, then shuffle."* | Same reasoning — $12.60 versus $2.79 for a tutor that covers both halves of your deck. |
| **Hall of Heliod's Generosity** | $12.41 | *"{T}: Add {C}. {1}{W}, {T}: Put target enchantment card from your graveyard on top of your library."* | $12 for a colorless land — the exact category you spent Tier 0 cutting. It also only puts the card on *top of your library*, not into play; Sevinne's Reclamation (36 cents) returns it to the battlefield. |

### The one honourable mention

**Sigarda's Aid** — `{W}` · Enchantment · **$18.29** · *"You may cast Aura and Equipment spells as though they had flash. Whenever an Equipment you control enters, you may attach it to target creature you control."*
This is genuinely the best single card for this deck that is not in the plan. Casting Auras at instant speed — after blockers, or in response to removal — is a real skill ceiling raiser. It is excluded only because $18.29 would eat 37% of the Tier 3 budget on its own. Buy it as the *first* thing after Tier 3, or instead of Bear Umbra if you prefer trickery to protection.

---

## 9. Appendix — raw CLI output

Everything above came from these calls. Run them yourself.

### Candidate 1 — Winds of Rath (the Tier 1 anchor)

```
$ ./bin/mtg card "Winds of Rath"
── Winds of Rath ─────────────────────────────────────────────────────────
Mana cost      : {3}{W}{W}
Mana value     : 5
Type           : Sorcery

Destroy all creatures that aren't enchanted. They can't be regenerated.

Color identity : W (white)
Rarity         : rare
Commander      : legal
EDHREC rank    : #1617
Price (USD)    : $0.34

── Rulings (1) ───────────────────────────────────────────────────────────
[2005-08-01] (wotc)
  A creature is "enchanted" if it has any Auras attached to it.

https://scryfall.com/card/soc/185/winds-of-rath?utm_source=api
```

### Candidate 2 — Sram, Senior Edificer (the Tier 2 anchor)

```
$ ./bin/mtg card "Sram, Senior Edificer"
── Sram, Senior Edificer ─────────────────────────────────────────────────
Mana cost      : {1}{W}
Mana value     : 2
Type           : Legendary Creature — Dwarf Advisor

Whenever you cast an Aura, Equipment, or Vehicle spell, draw a card.

P/T            : 2/2

Color identity : W (white)
Rarity         : rare
Commander      : legal
EDHREC rank    : #454
Price (USD)    : $0.81

── Rulings (1) ───────────────────────────────────────────────────────────
[2025-06-06] (wotc)
  Sram's ability resolves before the spell that caused it to trigger. It
  resolves even if that spell is countered or otherwise leaves the stack.

https://scryfall.com/card/soc/176/sram-senior-edificer?utm_source=api
```

### Candidate 3 — Ardenn, Intrepid Archaeologist (the Tier 3 anchor)

```
$ ./bin/mtg card "Ardenn, Intrepid Archaeologist" --no-rulings
── Ardenn, Intrepid Archaeologist ────────────────────────────────────────
Mana cost      : {2}{W}
Mana value     : 3
Type           : Legendary Creature — Kor Scout

At the beginning of combat on your turn, you may attach any number of Auras
and Equipment you control to target permanent or player.
Partner (You can have two commanders if both have partner.)

P/T            : 2/2

Color identity : W (white)
Keywords       : Partner
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #1678
Price (USD)    : $5.26

https://scryfall.com/card/cmr/10/ardenn-intrepid-archaeologist?utm_source=api
```

### Candidate 4 — Ethereal Armor (cheapest real upgrade in the file)

```
$ ./bin/mtg card "Ethereal Armor"
── Ethereal Armor ────────────────────────────────────────────────────────
Mana cost      : {W}
Mana value     : 1
Type           : Enchantment — Aura

Enchant creature
Enchanted creature gets +1/+1 for each enchantment you control and has first
strike.

Color identity : W (white)
Keywords       : Enchant
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #1072
Price (USD)    : $0.43

── Rulings (1) ───────────────────────────────────────────────────────────
[2021-03-19] (wotc)
  Ethereal Armor counts each enchantment you control, including itself and
  any Auras you control that are attached to an opponent or to permanents
  controlled by an opponent.

https://scryfall.com/card/dsk/7/ethereal-armor?utm_source=api
```

### Candidate 5 — Lion Umbra (the protection package, 24 cents)

```
$ ./bin/mtg card "Lion Umbra"
── Lion Umbra ────────────────────────────────────────────────────────────
Mana cost      : {G}{G}
Mana value     : 2
Type           : Enchantment — Aura

Enchant modified creature (Equipment, Auras its controller controls, and
counters are modifications.)
Enchanted creature gets +3/+3 and has vigilance and reach.
Umbra armor (If enchanted creature would be destroyed, instead remove all
damage from it and destroy this Aura.)

Color identity : G (green)
Keywords       : Umbra armor, Enchant
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #3252
Price (USD)    : $0.24

── Rulings (14) ──────────────────────────────────────────────────────────
[2024-06-07] (wotc)
  An Aura controlled by another player does not cause a creature you
  control to be modified.

[2024-06-07] (wotc)
  A creature that is equipped is considered modified no matter who
  controls the Equipment that's attached to it.

[2024-06-07] (wotc)
  Umbra armor has no effect if the enchanted creature is put into a
  graveyard for any other reason, such as if it's sacrificed, if the
  "legend rule" applies to it, or if its toughness is 0 or less.
```

### The bracket check (before and after — unchanged)

```
$ ./bin/mtg deck bracket dogmeat
── Scrappy Survivors — bracket ───────────────────────────────────────
Commander : Dogmeat, Ever Loyal

ESTIMATED BRACKET 2 — Core
  Precon-level. The baseline Commander experience -- a modern
  preconstructed deck out of the box lands here.

── SIGNALS ───────────────────────────────────────────────────────────
  Game Changers        : 0 (checked against 53 listed cards)
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review
```

### The EDHREC backing (top synergy cards you do not own)

```
$ ./bin/mtg edhrec dogmeat --missing --limit 40
── Creatures (35 of 35 missing — 50 in list) ─────────────────────────
    Sram, Senior Edificer            syn  +51.6%    59.9% of 8826 decks
    Danitha, New Benalia's Light     syn  +42.2%    45.2% of 8826 decks
    Danitha Capashen, Paragon        syn  +36.4%    41.9% of 8826 decks
    ...
    Reyav, Master Smith              syn  +28.8%    31.5% of 8826 decks
    Ardenn, Intrepid Archaeologist   syn  +15.7%    18.0% of 8826 decks

── Sorceries (15 of 15 missing — 17 in list) ─────────────────────────
    Open the Armory                  syn  +26.9%    31.8% of 8826 decks
    ...
    Winds of Rath                    syn   +7.3%     9.3% of 8826 decks

── Enchantments (21 of 21 missing — 32 in list) ──────────────────────
    Sigarda's Aid                    syn  +29.6%    34.8% of 8826 decks
    Forge Anew                       syn  +25.2%    30.3% of 8826 decks
    Bear Umbra                       syn  +21.4%    25.2% of 8826 decks
    Ethereal Armor                   syn  +10.8%    13.3% of 8826 decks
```

---

## 10. Closing note

**None of this is required.** Scrappy Survivors is a real Commander deck that came out of the box able to play a fair, fun game against other precons — that is exactly what Bracket 2 means, and Bracket 2 is where most kitchen-table Commander actually lives. Nobody at a normal table is going to look at an unmodified precon and think less of it.

If you only ever do one thing: do **Tier 0**. It costs nothing but a bit of shuffling between your three decks, it nearly doubles your removal, and it fixes the worst four lands in your mana base.

If you do one *purchase*: buy **Winds of Rath for 34 cents**. It is the only card in this document that changes what your deck is capable of rather than just how well it does what it already does.

And a piece of advice that no shopping list can replace — play twenty games with the deck as it is before you change anything. You will find out which cards you are always happy to draw and which ones you keep leaving in your hand, and *that* list will be better than mine, because it will be about how you actually play. Everything above is a starting hypothesis. Your games are the evidence.

Upgrading is a hobby inside the hobby. There is no deadline.
