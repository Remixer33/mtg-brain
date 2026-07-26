# Peace Offering — Ms. Bumbleflower — Staged Upgrade Path

**Deck slug:** `bumbleflower` · **Commander:** Ms. Bumbleflower · **Colour identity:** Bant (Green–White–Blue, `WUG`)
**Current bracket:** **2 — Core** (verified with `./bin/mtg deck bracket bumbleflower`)
**Format:** Commander / EDH only. **CR 903.5a**: *"Each deck must contain exactly 100 cards, including its commander. In other words, the minimum deck size and the maximum deck size are both 100."* That is why every upgrade below is a **swap** — a card going in always means a named card coming out.

> **Read this first.** The precon is already a legal, functional, fun deck. Nothing below is required. This is a menu, staged by money, and you can stop after any tier. Every price is the real `price_usd` value in the local card database, retrieved card-by-card. Where the database has no price I say so instead of guessing.

---

## 1. What this deck actually needs

Numbers below come from `./bin/mtg deck stats bumbleflower -v` and `./bin/mtg deck bracket bumbleflower`, run today.

| Role | Count | Verdict |
|---|---|---|
| draw | 25 | Enormous. This is the deck's engine and it does not need help. |
| ramp | 14 | Plenty. |
| wincon | 6 | Fine. |
| **interaction** | 6 | Only **2** of those 6 actually stop a spell (An Offer You Can't Refuse, Long River's Pull). The other 4 are defensive/protective. |
| **boardwipe** | 2 | Thin. |
| **removal** | **4** | **The problem.** |
| **recursion** | **1** | Peerless Recycling only. |
| **tutor** | **0** | Zero. |

**The diagnosis, in one sentence:** across **61 non-land cards** you have exactly **4 cards that kill an opposing permanent** — and two of those (Broken Wings, Wear Down) can only hit artifacts, enchantments, or creatures with flying. Against a normal 4-player table you have **two unconditional answers** (Swords to Plowshares, Generous Gift) for **three opponents**.

That gap matters more here than in most precons, because of what your commander does.

Ms. Bumbleflower (retrieved via `mtg card "Ms. Bumbleflower"`):

> Mana cost `{1}{G}{W}{U}` — Legendary Creature — Rabbit Citizen — 1/5
> Vigilance
> Whenever you cast a spell, **target opponent draws a card.** Put a +1/+1 counter on target creature. It gains flying until end of turn. If this is the second time this ability has resolved this turn, you draw two cards.

Every single spell you cast hands an opponent a free card. Over a real game that is 15–25 extra cards distributed around the table. You are actively *building* your opponents' hands. A deck that does that **must** be able to answer what those hands produce, and right now it cannot.

**Second diagnosis: your best engine is under-supported.** The strongest cluster in the deck is "everyone's spells make my counters":

- **Forgotten Ancient** `{3}{G}` — *"Whenever a player casts a spell, you may put a +1/+1 counter on this creature."*
- **Managorger Hydra** `{2}{G}` — *"Trample / Whenever a player casts a spell, put a +1/+1 counter on this creature."*
- **Sunscorch Regent** `{3}{W}{W}` — *"Flying / Whenever an opponent casts a spell, put a +1/+1 counter on this creature and you gain 1 life."*
- **Steelburr Champion** `{2}{W}` — *"Whenever an opponent casts a noncreature spell, put a +1/+1 counter on this creature."*
- **Simic Ascendancy** `{G}{U}` — *"Whenever one or more +1/+1 counters are put on a creature you control, put that many growth counters on this enchantment. At the beginning of your upkeep, if this enchantment has twenty or more growth counters on it, you win the game."*
- **Kalonian Hydra** `{3}{G}{G}` — *"Trample / This creature enters with four +1/+1 counters on it. / Whenever this creature attacks, double the number of +1/+1 counters on each creature you control."*

The deck currently owns **zero** counter-multipliers. Adding even one turns every Bumbleflower trigger into two or more growth counters on Simic Ascendancy — that is the single highest-leverage thing money can buy here.

**Third, smaller item: mana.** The assessment says 38 lands is **1 above** the 36–37 band the deck's 3.21 average mana value calls for, and **14 of your lands enter tapped (37% of the mana base)**. One land becomes a spell in Tier 3.

**So the priority order is:** (1) answers, (2) counter-multipliers, (3) recursion, (4) one tutor, (5) trim a land.

---

## 2. Jargon used below (beginner glossary)

Chase any of these with `mtg glossary <term>` or `mtg rule <number>`.

- **Mana value** — the total amount of mana in a card's mana cost, ignoring colour. `{2}{G}` has mana value 3. (`mtg glossary "Mana Value"` → see rule 202.3.)
- **Fixing** (colour fixing) — cards that let you produce the specific *colours* you need, as opposed to **ramp**, which just produces *more* mana. You can have five lands and still be unable to cast a `{1}{G}{W}{U}` commander; fixing is what solves that. Command Tower, Arcane Signet and Farseek are fixing; Sol Ring is pure ramp. (Not an official rules term.)
- **Instant speed** — you can cast it during any player's turn, including in response to something. Sorceries can only be cast on your own turn when nothing else is happening. Removal at instant speed is much better than removal at sorcery speed.
- **Board wipe** — a spell that destroys many creatures at once. (Not an official rules term; `mtg glossary "Board Wipe"` returns no entry.)
- **Counterspell** — a spell that stops another spell from resolving. "Casting" a spell is defined in **CR 701.5a**: *"To cast a spell is to take it from the zone it's in (usually the hand), put it on the stack, and pay its costs, so that it will eventually resolve and have its effect."* A counterspell removes it from the stack before that happens.
- **Hexproof** — *"A keyword ability that precludes a permanent or player from being targeted by an opponent"* (`mtg glossary Hexproof`, CR 702.11).
- **Indestructible** — *"A permanent with indestructible can't be destroyed. Such permanents aren't destroyed by lethal damage"* (**CR 702.12b**). Note: it does **not** stop exile or "sacrifice" effects.
- **Ward {1}** — *"Whenever this permanent becomes the target of a spell or ability an opponent controls, counter that spell or ability unless that player pays [cost]"* (**CR 702.21a**). It taxes removal aimed at your stuff.
- **Proliferate** — *"To give an additional counter to any number of players and/or permanents of each kind they already have"* (`mtg glossary Proliferate`, CR 701.34). If a creature has one +1/+1 counter, proliferate gives it a second. If Simic Ascendancy has growth counters, proliferate adds one.
- **Counter (the marker)** — **CR 122.1**: *"A counter is a marker placed on an object or player that modifies its characteristics… Notably, a counter is not a token, and a token is not a counter."* Careful: the word "counter" means two totally different things (the marker, and the verb "to counter a spell"). Your deck uses both.
- **State trigger** — **CR 603.8**: an ability that *"trigger[s] when a game state … is true, rather than triggering when an event occurs."* Simic Ascendancy's win condition is checked at your upkeep, so it is a normal upkeep trigger, not a state trigger — but Triskaidekaphile's "if you have exactly thirteen cards in your hand" works the same upkeep-check way. You get no window to act between "condition true" and "upkeep."
- **Bracket** — the Commander power-level scale, 1 (Exhibition) to 5 (cEDH). Your deck is **Bracket 2 — Core**: *"Precon-level. The baseline Commander experience -- a modern preconstructed deck out of the box lands here."* (quoted exactly as `data/brackets.json` stores it, double hyphen and all) Bracket 2 permits **zero Game Changers** (the official list of 53 high-power cards stored in `data/brackets.json`).

---

## 3. Why Tier 0 is possible: the colour-identity rule

**CR 903.4** (quoted verbatim, so American spelling): *"The Commander variant uses color identity to determine what cards can be in a deck with a certain commander. The color identity of a card is the color or colors of any mana symbols in that card's mana cost or rules text, plus any colors defined by its characteristic-defining abilities (see rule 604.3) or color indicator (see rule 204)."*

Your three decks:

| Deck | Commander | Colour identity |
|---|---|---|
| `bumbleflower` | Ms. Bumbleflower | `WUG` (Bant) |
| `tidus` | Tidus, Yuna's Guardian | `WUG` (Bant) — **identical** |
| `dogmeat` | Dogmeat, Ever Loyal | `RGW` (Naya) |

Because **Tidus is exactly the same colour identity as Bumbleflower**, *every non-land card in the Tidus deck is legal in Bumbleflower.* From `dogmeat`, only the cards whose colour identity is White, Green, White-Green, or colourless are legal — anything with a red mana symbol is not.

**The honest cost:** these are physical cards. Moving one out of another deck leaves a hole in that deck. Two mitigations, both true:

1. You only pilot one deck at a time. If Tidus and Bumbleflower are never at the same table, a shared card is genuinely free.
2. If you *do* want two decks playable simultaneously (a friend borrows one), you have to buy a second copy — I list the real price of each Tier 0 card so you know what un-sharing would cost.

Tier 0 takes **3 cards from Tidus and 3 from Dogmeat**. Be aware: Tidus is *also* a +1/+1 counters deck, so these are its good cards, not its spare parts. I flag the damage on each one.

---

## 4. Tier 0 — Free (cross-deck swaps) · **$0.00**

Running total: **$0.00**

### T0-1 · IN: Path to Exile → OUT: Broken Wings
- **IN — Path to Exile** · `{W}` · Instant · from **`dogmeat`** · *retail $1.03 if you buy a second copy*
  > *"Exile target creature. Its controller may search their library for a basic land card, put that card onto the battlefield tapped, then shuffle."*
  Official ruling [2026-01-27]: *"The controller of the exiled creature isn't required to search their library for a basic land."*
- **OUT — Broken Wings** `{2}{G}` Instant ($0.13) — *"Destroy target artifact, enchantment, or creature with flying."* This is the weakest of your four removal spells: it costs 3 mana and it **cannot touch a ground creature**. Half the threats you will face are ground creatures. Path to Exile answers any creature for one mana at instant speed.
- **Why:** removal count is 4 out of 61 non-lands. This upgrades your worst removal slot into the second-best white removal spell in the format (EDHREC rank #15) at a third of the cost.
- **Cost to Dogmeat:** it loses its cleanest creature answer. Dogmeat keeps Chaos Warp, Valorous Stance, Break Down, Single Combat and Blasphemous Act, so it is not left defenceless — it is just slower.
- **Bracket impact:** none. Path to Exile is **not** on the Game Changers list. Still Bracket 2.

### T0-2 · IN: Damning Verdict → OUT: Illusionist's Gambit
- **IN — Damning Verdict** · `{3}{W}{W}` · Sorcery · from **`tidus`** · *retail $11.71*
  > *"Destroy all creatures with no counters on them."*
  (`mtg card "Damning Verdict"` returns **no official rulings** — "not in my data" for rulings, but full oracle text and price are confirmed.)
- **OUT — Illusionist's Gambit** `{2}{U}{U}` Instant ($0.44) — *"Cast this spell only during the declare blockers step on an opponent's turn. Remove all attacking creatures from combat and untap them. After this phase, there is an additional combat phase…"* It is a one-shot trick that requires you to be attacked, requires you to hold up 4 mana, and does not remove anything permanently. EDHREC rank #3742 — one of the least-played cards in the deck.
- **Why:** this is the single most on-theme card in either of your other decks. Your board is *made of creatures with +1/+1 counters on it* — Forgotten Ancient, Managorger Hydra, Sunscorch Regent, Steelburr Champion and anything Bumbleflower has touched. Damning Verdict is a board wipe that **your team survives and theirs does not**. It takes your boardwipe count from 2 to 3 and makes one of them one-sided.
- **Cost to Tidus:** real. Tidus is also a counters deck, so Damning Verdict is asymmetric there too. Tidus keeps Farewell, Promise of Loyalty and Collective Effort.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T0-3 · IN: Heroic Intervention → OUT: Riot Control
- **IN — Heroic Intervention** · `{1}{G}` · Instant · from **`dogmeat`** · *retail $16.17 (the most valuable free swap on this list)*
  > *"Permanents you control gain hexproof and indestructible until end of turn."*
  Official ruling [2020-06-23]: *"The set of permanents affected by Heroic Intervention is determined as the spell resolves. Permanents you begin to control later in the turn won't gain hexproof and indestructible."*
- **OUT — Riot Control** `{2}{W}` Instant ($0.29) — *"You gain 1 life for each creature your opponents control. Prevent all damage that would be dealt to you this turn."* It buys you one turn and does nothing else. It does not protect your board, which is where all your value is.
- **Why:** you are building a slow engine — 25 draw pieces, a 1/5 commander, counters accumulating on Simic Ascendancy toward 20. The way that deck loses is one board wipe deleting ten turns of work. Two mana at instant speed protecting *every permanent you control* (including Simic Ascendancy and its growth counters) is the correct insurance. Note the limit: indestructible does **not** stop exile or forced sacrifice (**CR 702.12b** only covers "destroy" and lethal damage).
- **Cost to Dogmeat:** significant, and I want to be honest about it. Dogmeat is an Aura/Equipment deck — when a creature carrying four Auras gets killed, you lose five cards at once. Heroic Intervention is Dogmeat's best card against exactly that. If you play Dogmeat regularly, **buy a second copy instead** ($16.17) or skip this swap and take Unbreakable Formation from Tier 2 ($1.18) as the budget substitute.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T0-4 · IN: Hardened Scales → OUT: Martial Impetus
- **IN — Hardened Scales** · `{G}` · Enchantment · from **`tidus`** · *retail $2.28*
  > *"If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1 counters are put on it instead."*
  Official ruling [2023-09-01]: *"If a creature you control would enter the battlefield with a number of +1/+1 counters on it, it enters with that many plus one instead."*
- **OUT — Martial Impetus** `{2}{W}` Enchantment — Aura ($0.24) — *"Enchant creature / Enchanted creature gets +1/+1 and is goaded… Whenever enchanted creature attacks, each other creature that's attacking one of your opponents gets +1/+1 until end of turn."* It is a political card that makes *someone else's* creature attack *someone else*. It adds nothing to your counters engine and nothing to your board. EDHREC rank #3767.
- **Why:** this is the deck's **first counter-multiplier**, and it costs one mana. Every Bumbleflower trigger goes from 1 counter to 2. Every Forgotten Ancient / Managorger Hydra / Sunscorch Regent / Steelburr Champion trigger doubles. And because Simic Ascendancy reads *"Whenever one or more +1/+1 counters are put on a creature you control, put **that many** growth counters,"* your progress toward the 20-growth-counter win **also doubles**. One `{G}` enchantment roughly halves the time your alternate win condition needs.
- **Cost to Tidus:** Tidus wants this exact card for the exact same reason. This is the swap that hurts Tidus most per dollar. At $2.28 it is also the cheapest one to just buy twice — **recommended**.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T0-5 · IN: Inexorable Tide → OUT: Body of Knowledge
- **IN — Inexorable Tide** · `{3}{U}{U}` · Enchantment · from **`tidus`** · *retail $3.71*
  > *"Whenever you cast a spell, proliferate."*
  Official ruling [2011-01-01]: *"Whenever you cast a spell, Inexorable Tide's ability triggers and goes on the stack on top of it. It will resolve (and you'll proliferate) before the spell resolves."*
- **OUT — Body of Knowledge** `{3}{U}{U}` Creature — Avatar, `*/*` ($0.35) — *"Body of Knowledge's power and toughness are each equal to the number of cards in your hand. You have no maximum hand size. Whenever this creature is dealt damage, draw that many cards."* Same mana cost, so the curve does not move. The "no maximum hand size" clause is **triply redundant** — you already have Reliquary Tower (a land), Triskaidekaphile and Wizard Class level 1 all providing it. Strip that away and it is a vanilla body that dies to any removal.
- **Why:** the single best synergy card sitting in your other deck. Every spell you cast already triggers Bumbleflower; now it *also* proliferates. That means: +1 more counter on every creature that already has one, **+1 growth counter on Simic Ascendancy**, another level toward any Class, another vow counter, another hoofprint counter. And per the ruling it resolves *before* your spell, so it stacks with the Bumbleflower trigger from the same spell. On a board with three counter-creatures out, one cheap spell now generates 5–6 counters.
- **Cost to Tidus:** yes, this is arguably Tidus's best enchantment. Tidus keeps Hardened Scales-style effects only if you skip T0-4 — decide which of the two decks you want to be the counters deck, and commit.
- **Bracket impact:** none — not a Game Changer. Still Bracket 2.

### T0-6 · IN: Rogue's Passage → OUT: Evolving Wilds
- **IN — Rogue's Passage** · Land · from **`dogmeat`** · *retail $0.38*
  > *"{T}: Add {C}. / {4}, {T}: Target creature can't be blocked this turn."*
- **OUT — Evolving Wilds** · Land · **price not in my data** — *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle."* You run **both** Evolving Wilds and Terramorphic Expanse, which have identical text. Two copies of the slowest fixer in a deck that already has 14 lands entering tapped is one too many.
- **Why:** you have no way to force damage through. Kalonian Hydra reads *"Whenever this creature attacks, double the number of +1/+1 counters on each creature you control"* — that only matters if it connects, and a 4/4-and-growing trampler still gets chump-blocked. Rogue's Passage turns your biggest creature into a clock. Land count stays at 38.
- **Honest downside:** Evolving Wilds could fetch a basic of any of your three colours, so you lose a small amount of colour fixing, and Rogue's Passage taps for colourless only. With Command Tower, Exotic Orchard, Seaside Citadel and 14 dual lands you can afford it — but this is the one Tier 0 swap that makes your mana slightly worse.
- **Cost to Dogmeat:** minor. Dogmeat is a Voltron deck (all eggs in one big creature), so Rogue's Passage is genuinely useful there too — but Dogmeat runs 38 lands, so it keeps Junktown, Buried Ruin and 35 other lands.
- **Bracket impact:** none. Still Bracket 2.

> ### Optional Tier 0 extra — Nesting Grounds
> **Nesting Grounds** (Land, from `tidus`, $0.32) — *"{T}: Add {C}. / {1}, {T}: Move a counter from target permanent you control onto a second target permanent. Activate only as a sorcery."* A repeatable way to rescue counters off a creature that is about to die. Take it only if you are willing to cut a second basic; I have not assigned it an OUT because the land count is already being trimmed in Tier 3.

**TIER 0 RUNNING TOTAL: $0.00** (6 swaps · retail value of the cards moved: $1.03 + $11.71 + $16.17 + $2.28 + $3.71 + $0.38 = **$35.28** of value relocated for free)

---

## 5. Tier 1 — Under $5 total · **$3.13**

Everything here is a common or uncommon under a dollar. This tier exists to fix the removal and recursion holes for pocket change.

### T1-1 · IN: Beast Within ($0.48) → OUT: Wear Down
- **IN — Beast Within** · `{2}{G}` · Instant · **$0.48** · EDHREC #25
  > *"Destroy target permanent. Its controller creates a 3/3 green Beast creature token."*
  Official ruling [2021-03-19]: *"If the target permanent is an illegal target by the time Beast Within tries to resolve, the spell won't resolve. No player creates a Beast token. If the target is legal but not destroyed (most likely because it has indestructible), its controller does create a Beast token."*
- **OUT — Wear Down** `{1}{G}` Sorcery ($0.24) — *"Gift a card… Destroy target artifact or enchantment. If the gift was promised, instead destroy two target artifacts and/or enchantments."* Sorcery speed, and it only hits two permanent types. Worse, its bonus mode **draws an opponent a card** — in a deck that already gives away 20+ cards a game, paying more cards for a discount is exactly backwards.
- **Why:** takes you from 2 unconditional answers to 3, and this one answers **anything** — creature, artifact, enchantment, planeswalker, or a land. Giving them a 3/3 is a real cost, but for a deck with only 4 removal spells across 61 non-lands, "I can kill literally any permanent at instant speed for 3 mana" is worth it.
- **Bracket impact:** none. Not a Game Changer.

### T1-2 · IN: Stroke of Midnight ($0.39) → OUT: Perch Protection
- **IN — Stroke of Midnight** · `{2}{W}` · Instant · **$0.39** · EDHREC #201
  > *"Destroy target nonland permanent. Its controller creates a 1/1 white Human creature token."*
- **OUT — Perch Protection** `{4}{W}{W}` Instant ($3.72) — *"Gift an extra turn… Create four 2/2 blue Bird creature tokens with flying. If the gift was promised, all permanents you control phase out, and until your next turn, your life total can't change and you gain protection from everything. / Exile Perch Protection."* Six mana. The powerful half of this card requires **giving an opponent an extra turn**. In a 4-player game, handing a live opponent a free turn to untap and swing is how you lose. It is also the most expensive card in your deck by mana value alongside Coveted Jewel.
- **Why:** same effect as Beast Within but in white and one mana-symbol cheaper on the token they get (1/1 instead of 3/3). Removal count goes to 4 unconditional answers. Also cuts the curve: your `6+` bucket goes from 4 cards to 3.
- **Bracket impact:** none.

### T1-3 · IN: Return to Dust ($0.37) → OUT: Tenuous Truce
- **IN — Return to Dust** · `{2}{W}{W}` · Instant · **$0.37**
  > *"Exile target artifact or enchantment. If you cast this spell during your main phase, you may exile up to one other target artifact or enchantment."*
- **OUT — Tenuous Truce** `{1}{W}` Enchantment — Aura ($0.42) — *"Enchant opponent / At the beginning of enchanted opponent's end step, you and that player each draw a card. / When you attack enchanted opponent… or when they attack you…, sacrifice this Aura."* You have 25 draw pieces. You do not need a 26th, especially one that gives an opponent equal value and evaporates the moment combat happens. EDHREC #3242.
- **Why:** you are cutting Broken Wings and Wear Down, which were your only artifact/enchantment answers. This replaces both of them with one card that **exiles** (bypassing indestructible and regeneration, per **CR 702.12b** which only prevents *destruction*) and frequently answers two permanents for four mana.
- **Bracket impact:** none.

### T1-4 · IN: Evolution Witness ($0.33) → OUT: Bloodroot Apothecary
- **IN — Evolution Witness** · `{2}{G}` · Creature — Elf Shaman Mutant · 2/1 · **$0.33**
  > *"{1}{G}: Adapt 2. (If this creature has no +1/+1 counters on it, put two +1/+1 counters on it.) / Whenever one or more +1/+1 counters are put on this creature, return target permanent card from your graveyard to your hand."*
  Official ruling [2024-06-07]: *"If a creature somehow loses all of its +1/+1 counters, it can adapt again and get more +1/+1 counters."*
- **OUT — Bloodroot Apothecary** `{2}{G}` Creature — Squirrel Druid · 3/3 ($4.81) — *"Toxic 2… When this creature enters, you and target opponent each create a Treasure token. Whenever an opponent sacrifices a noncreature token, that player gets two poison counters."* Poison is a completely separate win condition (10 poison counters) that this deck has **no other support for** — it is a dead-end plan on one card. It also gives an opponent a free Treasure. EDHREC #3542. (Bonus: it is the most expensive card you are cutting, at $4.81 — you could sell it and fund all of Tier 1.)
- **Why:** recursion count goes from **1 to 2**. And read the trigger carefully: it is *"whenever one or more +1/+1 counters are put on this creature"* — **not** just from adapt. Ms. Bumbleflower puts a counter on a target creature every time you cast a spell. Point it at Evolution Witness and you return a permanent from your graveyard to your hand **for free, every turn**. With Hardened Scales (T0-4) it triggers on turn one of having both out.
- **Bracket impact:** none.

### T1-5 · IN: Regrowth ($0.48) → OUT: Octomancer
- **IN — Regrowth** · `{1}{G}` · Sorcery · **$0.48**
  > *"Return target card from your graveyard to your hand."*
- **OUT — Octomancer** `{3}{G}{U}` Creature — Frog Druid · 3/3 ($0.39) — *"Gift an Octopus (…they create an 8/8 blue Octopus creature token.) / At the beginning of each end step, create a token that's a copy of target creature token that entered the battlefield this turn."* A 5-mana 3/3 whose ability **does nothing unless a creature token entered this turn**, and whose discount mode gives an opponent an **8/8**. EDHREC #4348 — the least-played card in your deck after Jolly Gerbils.
- **Why:** recursion 2 → 3, and unlike Evolution Witness this one gets back *anything* — a countered board wipe, a destroyed Simic Ascendancy, a Sol Ring. Two mana. Also trims a 5-drop; your curve has 9 cards at 5 mana.
- **Bracket impact:** none.

### T1-6 · IN: Sun Titan ($0.32) → OUT: Coveted Jewel
- **IN — Sun Titan** · `{4}{W}{W}` · Creature — Giant · 6/6 · **$0.32** · EDHREC #293
  > *"Vigilance / Whenever this creature enters or attacks, you may return target permanent card with mana value 3 or less from your graveyard to the battlefield."*
  Official ruling [2010-08-15]: *"If a card in your graveyard has no mana symbols in its upper right corner (because it's a land card, for example), its mana value is 0."* — so Sun Titan can rebuild your **lands** too.
- **OUT — Coveted Jewel** `{6}` Artifact ($0.21) — *"When this artifact enters, draw three cards. {T}: Add three mana of any one color. Whenever one or more creatures an opponent controls attack you and aren't blocked, that player draws three cards and gains control of this artifact."* Six mana, and the drawback is catastrophic in a 4-player game: any opponent who gets a single unblocked creature through **takes your artifact and draws three cards**. Your commander is a 1/5 and your board is often small early. This card is designed to change hands.
- **Why:** recursion 3 → 4, and Sun Titan's targets are exactly your best cheap permanents: **Simic Ascendancy** (mana value 2), Hardened Scales (1), Wizard Class (1), Sol Ring (1), Arcane Signet (2), Mind Stone (2), Swiftfoot Boots (2), Evolution Witness (3), plus every land (mana value 0). Same slot on the curve (6 mana out, 6 mana in), massively better body (6/6 vigilance vs no body at all).
- **Bracket impact:** none.

### T1-7 · IN: Negate ($0.33) → OUT: Perplexing Test
- **IN — Negate** · `{1}{U}` · Instant · **$0.33** · EDHREC #54
  > *"Counter target noncreature spell."*
- **OUT — Perplexing Test** `{3}{U}{U}` Instant ($0.31) — *"Choose one — Return all creature tokens to their owners' hands. / Return all nontoken creatures to their owners' hands."* Five mana, and the second mode **bounces your own board too** — including every creature you have spent the game loading with +1/+1 counters. Counters do not come back with the creature (**CR 122.1**: counters are markers on the object, and the object becomes a new object when it changes zone). This card can undo your entire game.
- **Why:** the thing that actually kills you is an opponent's board wipe, an opponent's Simic-Ascendancy-style win condition, or a big enchantment. All of those are noncreature spells. Two mana to say no. Counterspell count 2 → 3 (you keep An Offer You Can't Refuse; Long River's Pull leaves in Tier 3).
- **Bracket impact:** none.

### T1-8 · IN: Gluntch, the Bestower ($0.43) → OUT: Jolly Gerbils
- **IN — Gluntch, the Bestower** · `{1}{G}{W}` · Legendary Creature — Jellyfish · 0/5 · **$0.43**
  > *"Flying / At the beginning of your end step, choose a player. They put two +1/+1 counters on a creature they control. Choose a second player to draw a card. Then choose a third player to create two Treasure tokens."*
  Official ruling [2022-06-10]: *"You may choose a player who doesn't control any creatures as the first chosen player."* — and all three chosen players must be different, so you pick yourself for the counters and hand the card and the Treasures to whoever you most want to befriend.
- **OUT — Jolly Gerbils** `{1}{W}` Creature — Hamster Citizen · 2/3 ($0.14) — *"Whenever you give a gift, draw a card."* Here is the bookkeeping reason it must go: after Tiers 0–1 you have cut **Wear Down**, **Perch Protection** and **Octomancer** — three of the deck's gift cards. Jolly Gerbils is now nearly blank. EDHREC rank **#13633**, the lowest-played card in the entire deck.
- **Why:** **two free +1/+1 counters on your own creature every single turn**, at no mana cost, from a 0/5 flying blocker that survives combat and protects your 1/5 commander. With Hardened Scales that is 3 counters/turn; with Simic Ascendancy that is 3 growth counters/turn toward 20. And the "gifts" you hand out (one card, two Treasures) buy you genuine table goodwill — which is the actual strategy this deck is built around.
- **Bracket impact:** none.

**TIER 1 SUBTOTAL:** $0.48 + $0.39 + $0.37 + $0.33 + $0.48 + $0.32 + $0.33 + $0.43 = **$3.13**
**RUNNING TOTAL AFTER TIERS 0+1: $3.13**

---

## 6. Tier 2 — Under $20 total · **$14.70**

This tier buys *quality*: cheaper interaction, real counter-multipliers, and the deck's first land upgrade.

### T2-1 · IN: Arcane Denial ($1.43) → OUT: Secret Rendezvous
- **IN — Arcane Denial** · `{1}{U}` · Instant · **$1.43** · EDHREC #55
  > *"Counter target spell. Its controller may draw up to two cards at the beginning of the next turn's upkeep. / You draw a card at the beginning of the next turn's upkeep."*
  Official ruling [2007-09-16]: *"The controller of the countered spell doesn't choose how many cards to draw until the relevant ability resolves. The player may draw 0, 1, or 2 cards."*
- **OUT — Secret Rendezvous** `{1}{W}{W}` Sorcery ($0.36) — *"You and target opponent each draw three cards."* Three cards to you, three cards to a single opponent, at sorcery speed, in a deck that already has 25 draw pieces. It is the most one-sidedly generous card in the deck and it does not advance any of your win conditions.
- **Why:** **counter *anything*** for two mana — a board wipe, a game-winning spell, a commander. The "they draw two" drawback is nearly free in *this* deck: you are already handing out cards with every Bumbleflower trigger, so opponents are used to it and it is politically cheap. Arcane Denial is the correct beginner counterspell because there is no awkward conversation afterward. Answers total is now 4 removal + 3 wipes + 3 counters = **10**, up from 8.
- **Bracket impact:** none.

### T2-2 · IN: Pongify ($1.60) → OUT: Ghirapur Orrery
- **IN — Pongify** · `{U}` · Instant · **$1.60** · EDHREC #155
  > *"Destroy target creature. It can't be regenerated. Its controller creates a 3/3 green Ape creature token."*
- **OUT — Ghirapur Orrery** `{4}` Artifact ($0.36) — *"Each player may play an additional land on each of their turns. / At the beginning of each player's upkeep, if that player has no cards in hand, that player draws three cards."* Pure group hug with no payoff attached. It accelerates **all three opponents** equally, and its refill clause almost never fires for you — you have 25 draw pieces and multiple no-maximum-hand-size effects, so your hand is never empty. It is helping them, not you.
- **Why:** one-mana instant-speed creature removal. When the table's scariest creature resolves and you are tapped low, this is the card you want. Removal count 4 → 5.
- **Bracket impact:** none.

### T2-3 · IN: Rapid Hybridization ($1.09) → OUT: Rites of Flourishing
- **IN — Rapid Hybridization** · `{U}` · Instant · **$1.09** · EDHREC #208
  > *"Destroy target creature. It can't be regenerated. That creature's controller creates a 3/3 green Frog Lizard creature token."*
- **OUT — Rites of Flourishing** `{2}{G}` Enchantment ($0.57) — *"At the beginning of each player's draw step, that player draws an additional card. / Each player may play an additional land on each of their turns."* This is the deck's single most self-destructive card. Three opponents each draw an extra card **every turn** and each get an extra land drop **every turn**. You draw one extra and get one extra. In a 4-player game you are giving away three cards for every one you gain — while your commander is *already* giving each of them a card per spell you cast. Cut it.
- **Why:** a second one-mana answer, which matters because your only unconditional creature removal was one Swords to Plowshares. Removal count 5 → 6. And removing Rites of Flourishing is a **defensive upgrade** on its own: you stop feeding the table.
- **Bracket impact:** none.

### T2-4 · IN: Nature's Claim ($1.40) → OUT: Communal Brewing
- **IN — Nature's Claim** · `{G}` · Instant · **$1.40** · EDHREC #378
  > *"Destroy target artifact or enchantment. Its controller gains 4 life."*
- **OUT — Communal Brewing** `{2}{G}` Enchantment ($0.75) — *"When this enchantment enters, any number of target opponents each draw a card. Put an ingredient counter on this enchantment, then put an ingredient counter on it for each card drawn this way. / Whenever you cast a creature spell, that creature enters with X additional +1/+1 counters on it, where X is the number of ingredient counters on this enchantment."* It does feed your counters plan — but the counter total is locked in at the moment it enters (max 4 ingredient counters with 3 opponents drawing), it only applies to **creature spells** (you have 26 creatures out of 61 non-lands), and the cost is giving three opponents a card up front. The multipliers in this tier and Tier 3 do the same job better and permanently.
- **Why:** one mana, instant speed, kills the enchantment that is beating you (a Ghostly Prison, a rival's Simic Ascendancy, a Smothering Tithe) or the artifact ramp piece that is running away with the game. The 4 life they gain is irrelevant at Bracket 2 where nobody is racing. Removal count 6 → 7.
- **Bracket impact:** none.

### T2-5 · IN: Unbreakable Formation ($1.18) → OUT: Hoofprints of the Stag
- **IN — Unbreakable Formation** · `{2}{W}` · Instant · **$1.18** · EDHREC #544
  > *"Creatures you control gain indestructible until end of turn. / Addendum — If you cast this spell during your main phase, put a +1/+1 counter on each of those creatures and they gain vigilance until end of turn."*
  Official ruling [2024-01-12]: *"Addendum abilities of instant spells apply while the spell is resolving, not immediately after casting it."*
- **OUT — Hoofprints of the Stag** `{1}{W}` Kindred Enchantment — Elemental ($0.17) — *"Whenever you draw a card, you may put a hoofprint counter on this enchantment. / {2}{W}, Remove four hoofprint counters from this enchantment: Create a 4/4 white Elemental creature token with flying. Activate only during your turn."* Painfully slow: four draws **plus** three mana for a single 4/4, and the counters it makes are hoofprint counters, which Simic Ascendancy does not care about (it only counts **+1/+1** counters). EDHREC #9488.
- **Why:** this is a two-for-one. On defence it is a board-wipe answer at 3 mana. On offence, cast in your main phase it puts **a +1/+1 counter on every creature you control** — which with Simic Ascendancy out means *that many growth counters at once*. On a board of five creatures, that is 5 growth counters (10 with Hardened Scales) from a single 3-mana instant. It is your best "protect the engine" and "advance the engine" card in one slot.
- **Bracket impact:** none.

### T2-6 · IN: Kami of Whispered Hopes ($2.94) → OUT: Twenty-Toed Toad
- **IN — Kami of Whispered Hopes** · `{2}{G}` · Creature — Spirit · **$2.94** · EDHREC #403
  > *"If one or more +1/+1 counters would be put on a permanent you control, that many plus one +1/+1 counters are put on that permanent instead. / {T}: Add X mana of any one color, where X is this creature's power."*
- **OUT — Twenty-Toed Toad** `{3}{U}` Creature — Frog Wizard · 3/3 ($4.70) — *"Your maximum hand size is twenty. / Whenever you attack with two or more creatures, put a +1/+1 counter on this creature and draw a card. / Whenever this creature attacks, you win the game if there are twenty or more counters on it or you have twenty or more cards in hand."* A third alternate win condition on top of Simic Ascendancy and Triskaidekaphile. Twenty counters on one creature or twenty cards in hand is a very long way away, and this card **caps your hand size at twenty**, actively fighting Reliquary Tower and Wizard Class. Three win conditions competing for the same slots is one too many; keep the one that is actually supported.
- **Why:** your **second counter-multiplier**, and note it says *"permanent you control"*, not "creature" — broader than Hardened Scales. Stacked with Hardened Scales, one Bumbleflower trigger becomes 3 counters (1 → +1 → +1). It is also a mana creature that gets better as it grows: with two counters on it, it taps for 3 mana of any one colour. The $4.70 card you are removing more than pays for the $2.94 card going in.
- **Bracket impact:** none.

### T2-7 · IN: Proft's Eidetic Memory ($1.94) → OUT: Sphinx of Enlightenment
- **IN — Proft's Eidetic Memory** · `{1}{U}` · Legendary Enchantment · **$1.94**
  > *"When Proft's Eidetic Memory enters, draw a card. / You have no maximum hand size. / At the beginning of combat on your turn, if you've drawn more than one card this turn, put X +1/+1 counters on target creature you control, where X is the number of cards you've drawn this turn minus one."*
  Official ruling [2024-02-02]: *"Proft's Eidetic Memory's last ability looks at how many cards you've drawn this turn, even if it wasn't on the battlefield when you drew"* those cards.
- **OUT — Sphinx of Enlightenment** `{4}{U}{U}` Creature — Sphinx · 5/5 · **price not in my data** — *"Flying / When this creature enters, target opponent draws a card and you draw three cards."* Six mana for a one-shot draw-three attached to a body with no protection, in a deck with 25 draw pieces. EDHREC rank **#9323**. It also gives an opponent yet another card.
- **Why:** this is the card that finally *converts* your 25 draw pieces into your win condition. Bumbleflower alone draws you two extra cards on your second trigger each turn; add your draw step and one cantrip and you are at 4+ cards drawn, which is **3 +1/+1 counters on one creature at the beginning of combat — every turn, for free**. With Hardened Scales and Kami of Whispered Hopes that is 5 counters, which is 5 growth counters on Simic Ascendancy. Four turns of that wins the game outright. It also replaces the "no maximum hand size" text you are cutting elsewhere, and trims a 6-drop.
- **Bracket impact:** none.

### T2-8 · IN: Eternal Witness ($1.96) → OUT: Tempt with Bunnies
- **IN — Eternal Witness** · `{1}{G}{G}` · Creature — Human Shaman · 2/1 · **$1.96** · EDHREC #112
  > *"When this creature enters, you may return target card from your graveyard to your hand."*
- **OUT — Tempt with Bunnies** `{2}{W}` Sorcery ($4.53) — *"Tempting Offer — Draw a card and create a 1/1 white Rabbit creature token. Then each opponent may draw a card and create a 1/1 white Rabbit creature token. For each opponent who does, you draw a card and you create a 1/1 white Rabbit creature token."* Tempting Offer cards are the exact failure mode the diagnosis identified: **you arm all three opponents to get value yourself.** Best case you get 4 cards and 4 rabbits while your three opponents each get a card and a rabbit — a total of 3 extra cards and 3 extra bodies working against you. In a deck that already gives away a card per spell, this is compounding the problem. (It is also the second-most-expensive card you are cutting at $4.53.)
- **Why:** recursion count reaches **5** (Peerless Recycling, Evolution Witness, Regrowth, Sun Titan, Eternal Witness). A creature body that returns any card is far better than a sorcery, because Sun Titan can bring **Eternal Witness itself** back (mana value 3) to do it again.
- **Bracket impact:** none.

### T2-9 · IN: Fabled Passage ($1.16) → OUT: Terramorphic Expanse
- **IN — Fabled Passage** · Land · **$1.16** · EDHREC #50
  > *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle. Then if you control four or more lands, untap that land."*
- **OUT — Terramorphic Expanse** · Land ($0.28) — *"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle."*
- **Why:** a **strict upgrade** — identical text plus *"Then if you control four or more lands, untap that land."* Your stats flag **14 lands entering tapped (37% of the mana base)**; from turn 4 onward this one stops being one of them. Land count unchanged at 38.
- **Bracket impact:** none.

**TIER 2 SUBTOTAL:** $1.43 + $1.60 + $1.09 + $1.40 + $1.18 + $2.94 + $1.94 + $1.96 + $1.16 = **$14.70**
**RUNNING TOTAL AFTER TIERS 0+1+2: $17.83**

---

## 7. Tier 3 — Under $50 total · **$44.68**

Five higher-value cards. Every one is still **Bracket 2 legal** — I checked all 28 recommended cards against the 53-card Game Changers list in `data/brackets.json` and **none of them appear on it**.

### T3-1 · IN: Faerie Mastermind ($12.08) → OUT: Jolrael, Mwonvuli Recluse
- **IN — Faerie Mastermind** · `{1}{U}` · Creature — Faerie Rogue · 2/1 · **$12.08** · EDHREC #313
  > *"Flash / Flying / Whenever an opponent draws their second card each turn, you draw a card. / {3}{U}: Each player draws a card."*
  Official ruling [2023-04-14]: *"Faerie Mastermind doesn't need to have been under your control when the first card is drawn for its ability to trigger. As long as you control it when an opponent draws their second card in a turn, that ability will trigger."*
- **OUT — Jolrael, Mwonvuli Recluse** `{1}{G}` Legendary Creature — Human Druid · 1/2 ($0.23) — *"Whenever you draw your second card each turn, create a 2/2 green Cat creature token. / {4}{G}{G}: Until end of turn, creatures you control have base power and toughness X/X, where X is the number of cards in your hand."* The Cat tokens are fine but they arrive with no counters, so they contribute nothing to Simic Ascendancy. Worse, the activated ability sets creatures to **base** power and toughness X/X. Per **CR 613.4b**, *"Layer 7b: Effects that set power and/or toughness to a specific number or value are applied"* — that wipes out the printed stats, and only then does **CR 613.4c** (*"Layer 7c: Effects and counters that modify power and/or toughness … are applied"*) add your +1/+1 counters back on top. Your counters survive, but the printed body underneath them does not: a 4/3 Sunscorch Regent with three counters is a 7/6 normally, and becomes a (X+3)/(X+3) after Jolrael — a **downgrade** unless your hand is enormous. It is an anti-synergy in your own deck. EDHREC #2786.
- **Why:** this is the single most synergistic card that exists for Ms. Bumbleflower and it is not in your deck. Your commander reads *"Whenever you cast a spell, **target opponent draws a card.**"* Faerie Mastermind reads *"Whenever an opponent draws their **second** card each turn, you draw a card."* Cast two spells in a turn pointed at the same opponent and you draw a card off Faerie Mastermind on top of Bumbleflower's own "you draw two cards" clause. It turns your deck's biggest liability — arming opponents with cards — into your engine. It has **flash** (castable at instant speed) and **flying**, so it also blocks. EDHREC lists it as the #1 most-played creature missing from your deck (40.8% of 36,366 Ms. Bumbleflower decks).
- **Bracket impact:** none. Not a Game Changer.

### T3-2 · IN: Branching Evolution ($6.85) → OUT: Baird, Steward of Argive
- **IN — Branching Evolution** · `{2}{G}` · Enchantment · **$6.85** · EDHREC #368
  > *"If one or more +1/+1 counters would be put on a creature you control, twice that many +1/+1 counters are put on that creature instead."*
  Official ruling [2020-06-23]: *"If two or more effects attempt to modify how many counters would be put onto a creature you control, **you choose the order to apply those effects**, no matter who controls the sources of those effects."*
- **OUT — Baird, Steward of Argive** `{2}{W}{W}` Legendary Creature — Human Soldier · 2/4 ($0.31) — *"Vigilance / Creatures can't attack you or planeswalkers you control unless their controller pays {1} for each of those creatures."* A {1}-per-creature tax is the weakest version of this effect — a determined attacker simply pays it. Your deck already deters attacks with Mangara, the Diplomat (draws you a card when opponents attack you with two or more creatures) and Promise of Loyalty (which leaves creatures unable to attack you). Four mana for a soft tax is the least productive slot left.
- **Why:** the **third and best counter-multiplier**, and the ruling above is the reason it goes in *after* Hardened Scales and Kami of Whispered Hopes rather than instead of them — you choose the order, so you apply the two "+1" effects first and the "×2" last. One Bumbleflower trigger becomes: **1 → 2 (Hardened Scales) → 3 (Kami) → 6 (Branching Evolution)**. Six +1/+1 counters from one spell. Simic Ascendancy converts that into **6 growth counters**; it needs 20 to win outright. Four spells and the game ends.
- **Bracket impact:** none. Not a Game Changer.

### T3-3 · IN: Eladamri's Call ($11.49) → OUT: Long River's Pull
- **IN — Eladamri's Call** · `{G}{W}` · Instant · **$11.49** · EDHREC #759
  > *"Search your library for a creature card, reveal that card, put it into your hand, then shuffle."*
  Official ruling [2004-10-04]: *"Because the 'search' requires you to find a card with certain characteristics, you don't have to find the card if you don't want to."*
- **OUT — Long River's Pull** `{U}{U}` Instant ($0.35) — *"Gift a card… Counter target creature spell. If the gift was promised, instead counter target spell."* To counter anything other than a creature spell, you must **give an opponent a card**. Your deck already gives away a card every time you cast a spell — this one asks you to pay again for the privilege. And a counterspell that only stops creatures is the wrong half of the format; the things that beat you are board wipes and enchantments. You keep An Offer You Can't Refuse, and you have added Negate and Arcane Denial.
- **Why:** **the tutor count goes from 0 to 1.** (A tutor is a card that searches your library for a specific card.) 26 of your 61 non-lands are creatures, including every counter-multiplier body, Kalonian Hydra, Gluntch, Faerie Mastermind, Evolution Witness, Eternal Witness and Sun Titan. At instant speed for two mana, Eladamri's Call means the piece you need is always one card away. For a beginner this is also a *learning* card: it forces you to think about which creature actually solves the board in front of you.
- **Bracket impact:** none — Eladamri's Call is **not** on the Game Changers list. Note that the three tutors EDHREC recommends for this commander — **Enlightened Tutor** ($38.71), **Mystical Tutor** ($16.26) and **Worldly Tutor** ($27.13) — **are all on the Game Changers list**, and any one of them would push the deck out of Bracket 2 and into Bracket 3. Eladamri's Call gets you 80% of the effect with zero bracket cost. That is deliberate.

### T3-4 · IN: Innkeeper's Talent ($7.99) → OUT: Fisher's Talent
- **IN — Innkeeper's Talent** · `{1}{G}` · Enchantment — Class · **$7.99** · EDHREC #676
  > *"At the beginning of combat on your turn, put a +1/+1 counter on target creature you control. / {G}: Level 2 — Permanents you control with counters on them have ward {1}. / {3}{G}: Level 3 — If you would put one or more counters on a permanent or player, put twice that many of each of those kinds of counters on that permanent or player instead."*
  Official ruling [2024-07-26]: *"Each Class starts with only the first of its three class abilities. As the first level ability resolves, the Class becomes level 2 and gains the second class ability."*
- **OUT — Fisher's Talent** `{2}{G}{U}` Enchantment — Class ($0.36) — *"At the beginning of your upkeep, look at the top card of your library. You may reveal it if it's a land card. Create a 1/1 blue Fish creature token if you revealed it this way. Then draw a card. / {G}{U}: Level 2 — If you would create a Fish token, create a 3/3 blue Shark token instead. / {2}{G}{U}: Level 3 — …an 8/8 blue Octopus token instead."* A like-for-like Class swap. Fisher's Talent costs 4 mana up front, then 2 more, then 4 more (10 total) to reach its payoff, and the tokens it makes arrive **with no counters** — they do nothing for Simic Ascendancy. EDHREC rank **#8214**, the least-played card remaining in the deck.
- **Why:** three upgrades in one card for two mana. **Level 1** is a free +1/+1 counter every combat, forever. **Level 2** gives *every permanent with a counter on it* **ward {1}** — per **CR 702.21a**, an opponent targeting your Simic Ascendancy, your Forgotten Ancient or your commander must pay an extra {1} or their spell is countered. That is blanket protection for the whole engine. **Level 3** reads *"a permanent **or player**"* and *"each of those kinds of counters"* — so unlike Branching Evolution it doubles **growth counters on Simic Ascendancy** too, on top of the +1/+1 counters already doubled. This is the card that closes the game.
- **Bracket impact:** none. Not a Game Changer.

### T3-5 · IN: Bala Ged Recovery ($6.27) → OUT: 1 Forest
- **IN — Bala Ged Recovery // Bala Ged Sanctuary** · **$6.27** · EDHREC #319 — a modal double-faced card (one physical card, two faces; you choose which face to play):
  > Face 1 — **Bala Ged Recovery**, `{2}{G}` Sorcery: *"Return target card from your graveyard to your hand."*
  > Face 2 — **Bala Ged Sanctuary**, Land: *"This land enters tapped. {T}: Add {G}."*
- **OUT — 1 Forest** (Basic Land — Forest)
- **Why:** this is the land trim your stats explicitly asked for. The assessment says: *"38 lands is 1 above the 36-37 band — expect flood; consider trimming for card advantage (deck has 25 draw pieces)."* Bala Ged Recovery is the perfect trim because **it is not really a cut** — when you need a land, you play it as a tapped Forest; when you have enough lands, it is a Regrowth. True land count goes to **37, inside the recommended band**, with a 38th flexible slot. Green sources stay at 19 (Bala Ged Sanctuary replaces the Forest as a green source). Recursion count reaches **6**, up from the 1 you started with.
- **Honest downside:** Bala Ged Sanctuary **always enters tapped**, so your tapped-land count goes from 14 to 15 (37% → 39% of the mana base). If you find yourself stumbling on mana, this is the first swap to reverse.
- **Bracket impact:** none. Not a Game Changer.

**TIER 3 SUBTOTAL:** $12.08 + $6.85 + $11.49 + $7.99 + $6.27 = **$44.68**
**RUNNING TOTAL, ALL FOUR TIERS: $0.00 + $3.13 + $14.70 + $44.68 = $62.51 · 28 cards changed**

---

## 8. Where the numbers land

| Metric | Precon (from `deck stats`) | After all 4 tiers |
|---|---|---|
| Single-target removal | **4** (2 conditional) | **9** (all unconditional) |
| Board wipes | 2 | 3 (one of them one-sided) |
| Counterspells | 2 | 3 |
| **Total hard answers** | **8** | **15** |
| Recursion | **1** | **6** |
| Tutors | **0** | **1** |
| Counter-multipliers | **0** | **4** (Hardened Scales, Kami of Whispered Hopes, Branching Evolution, Innkeeper's Talent L3) |
| Lands | 38 (1 over band) | 37 + 1 flexible |
| Cards that hand opponents free resources | Rites of Flourishing, Ghirapur Orrery, Tempt with Bunnies, Secret Rendezvous, Coveted Jewel, Tenuous Truce, Wear Down, Perch Protection, Octomancer | **all removed** |
| Estimated bracket | **2 — Core** | **2 — Core** |

The single biggest behavioural change: **you stop paying opponents for value you were already getting from your commander.** Bumbleflower gives away a card per spell. That is the price of the engine. You should not also be running six other cards that give things away for free.

---

## 9. Do NOT buy these yet

These are all popular on EDHREC for Ms. Bumbleflower and all wrong for you right now. No judgement — they are good cards. They are just the wrong purchase at this stage.

**Because they break Bracket 2.** `data/brackets.json` lists 53 Game Changers, and Bracket 2's first rule is *"No Game Changers."* Bracket 3 allows up to 3. Buying **any one** of these moves your deck out of Core and into Upgraded — which means the pod expects a tuned deck, and casual opponents may reasonably ask you to swap it out:

| Card | Price | EDHREC play rate in Ms. Bumbleflower decks | Why it's wrong *now* |
|---|---|---|---|
| **Rhystic Study** `{2}{U}` | **$69.85** | 20.0% | The most expensive card on the list and the most socially expensive. It requires you to ask "did you pay the {1}?" on every single spell for the rest of the game. Beginners hate playing it and tables hate playing against it. |
| **Smothering Tithe** `{3}{W}` | **$63.65** | 35.8% | Same "did you pay?" problem, four times per turn cycle. It is also a ramp card, and you already have 14 ramp pieces. |
| **Fierce Guardianship** `{2}{U}` | **$56.48** | 12.4% | A free counterspell. $56 for one card that does nothing most games. |
| **Teferi's Protection** `{2}{W}` | **$52.60** | 15.8% | Powerful, but it is a defensive card you will not know when to use for your first fifty games. |
| **Cyclonic Rift** `{1}{U}` | **$40.76** | 17.5% | The overloaded mode ends games out of nowhere. That is a Bracket 3–4 experience. |
| **Enlightened Tutor** `{W}` | **$38.71** | 11.3% | See Eladamri's Call in Tier 3 — you get the tutor slot for $11.49 with no bracket cost. |
| **Consecrated Sphinx** `{4}{U}{U}` | **$30.67** | 18.3% | Six mana. It reads well with your draw theme but it makes you the archenemy the moment it resolves. |
| **Worldly Tutor** `{G}` / **Mystical Tutor** `{U}` | **$27.13 / $16.26** | 8.3% each | Same reasoning as Enlightened Tutor. |
| **Seedborn Muse** `{3}{G}{G}` | **$15.12** | 21.7% | Untapping every turn is genuinely great — and genuinely a signal to the table that you are not playing a precon. |
| **Narset, Parter of Veils** `{1}{U}{U}` | **$1.59** | 8.9% | Cheap, but note it is a **Game Changer** despite the price — brackets are about effect, not cost. It is also close to anti-synergy here: your commander *makes opponents draw*, and Narset's *"Each opponent can't draw more than one card each turn"* shuts off **Faerie Mastermind** (T3-1), which needs an opponent to draw their **second** card in a turn. Your commander would be feeding a card to an opponent that Narset then stops from mattering. |

**Because they are expensive and not actually better for you:**

- **The Ozolith** `{1}` Legendary Artifact — **$65.37**. *"Whenever a creature you control leaves the battlefield, if it had counters on it, put those counters on The Ozolith…"* It is insurance against your creatures dying. **Ozolith, the Shattered Spire** ($5.20) is a different card that adds counters proactively, and honestly Hardened Scales at $2.28 does more for you. Do not spend $65 on a safety net.
- **Esper Sentinel** `{W}` — **$57.50** for a 1/1. It is a fantastic card. It is also $57.50 for a 1/1 that dies to everything.
- **Boseiju, Who Endures** — **$49.35** for a land. **Otawara, Soaring City** — **$27.47** for a land. Both are excellent and both are pure luxury. Your mana base already has 14 dual lands.
- **Doubling Season** `{4}{G}` — **$33.53**. A fourth counter-multiplier at five mana, when you will already have four for a combined $20.06. Diminishing returns.
- **Burgeoning** `{G}` — **$34.27**. Land acceleration in a deck the stats say already has *too many* lands.
- **Bloom Tender** ($12.86) / **Noble Hierarch** ($12.80) / **Birds of Paradise** ($9.03) — mana creatures. You have **14 ramp pieces and 52 total mana sources**. Mana is not your problem.

**Because they make the same mistake the precon already makes:**

- **Howling Mine** ($5.26), **Temple Bell** ($6.07), **Font of Mythos**, **Dictate of Kruphix** ($0.38), **Wedding Ring** ($11.13) — symmetric group-hug draw. EDHREC likes them because they trigger things. But you are already the most generous deck at the table thanks to your commander. Adding *more* cards that draw everyone cards makes three opponents faster and you only one-third faster. If you want a group-hug payoff, **Scrawling Crawler** ($6.70) at least drains them ( *"At the beginning of your upkeep, each player draws a card. Whenever an opponent draws a card, that player loses 1 life."* ) — but even that is a Tier 4 conversation.

---

## 10. Bracket check after all four tiers

I ran every one of the 28 recommended IN cards against the 53-name Game Changers list in `data/brackets.json`:

```
GAME CHANGERS AMONG RECOMMENDED INS: NONE
total ins: 28
```

The other Bracket 2 requirements, checked against what is going in:

- **"No mass land denial."** — no card added destroys lands. ✔
- **"No chaining extra turns."** — no card added takes an extra turn. In fact you are *removing* Perch Protection, whose alternate mode **gives an opponent an extra turn**. ✔
- **"No two-card infinite combos."** — none of the 28 additions form one. The bracket tool flags this as *"not detected by this tool; requires human/agent review"*, and my review found no two-card loop. The counter-multipliers (Hardened Scales, Kami of Whispered Hopes, Branching Evolution, Innkeeper's Talent) multiply a *finite* number of counters per trigger; they do not loop. ✔
- **"Power level of a modern precon; games typically end around turn 9 or later."** — This is the one to watch. With all four counter-multipliers plus Simic Ascendancy, a strong draw can assemble 20 growth counters faster than a precon "should." If your regular pod starts finding that oppressive, the honest thing to do is either say "I think this is a Bracket 3 deck now" before the game, or take out one multiplier. **Brackets are a conversation, not a rule.**

**Verdict: after all four tiers the deck is still Bracket 2 — Core.** It is a *strong* Bracket 2, which is exactly the right place for an upgraded precon.

Re-verify any time the deck changes:
```
./bin/mtg deck bracket bumbleflower
```

---

## 11. A closing note

**None of this is necessary.** Peace Offering is a real deck as it came in the box — the bracket tool says so plainly: *"Bracket 2 (Core) is described as 'Precon-level … a modern preconstructed deck out of the box lands here', which is exactly what this deck is."* It has a commander with a genuinely unusual ability, a working alternate win condition in Simic Ascendancy, 25 ways to draw cards and a mana base with 14 dual lands. People have won plenty of games with less.

If you do nothing else, do **Tier 0** — it costs zero dollars, it takes fifteen minutes with three deck boxes on a table, and it fixes the two worst problems (no answers, no counter-multiplier).

If you want the best value for money, do **Tier 1**. Eight cards, $3.13, and your removal count nearly doubles.

And play the deck a few times between tiers. The point of staging this is that you get to notice *which* problem is actually beating you before you spend anything. A deck you understand is worth more than a deck you bought.

---

## Appendix — Real CLI output for candidate cards

Pasted verbatim from `./bin/mtg card "<name>"` so every price and every line of text above can be checked.

```
── Path to Exile ─────────────────────────────────────────────────────────
Mana cost      : {W}
Mana value     : 1
Type           : Instant

Exile target creature. Its controller may search their library for a basic
land card, put that card onto the battlefield tapped, then shuffle.

Color identity : W (white)
Rarity         : uncommon
Commander      : legal
EDHREC rank    : #15
Price (USD)    : $1.03

── Rulings (2) ───────────────────────────────────────────────────────────
[2026-01-27] (wotc)
  The controller of the exiled creature isn't required to search their
  library for a basic land. If that player doesn't, the player won't
  shuffle their library.

[2026-01-27] (wotc)
  If the target creature is an illegal target by the time Path to Exile
  tries to resolve, it won't resolve and none of its effects will happen.
  The creature's controller won't search for a basic land card.
```

```
── Branching Evolution ───────────────────────────────────────────────────
Mana cost      : {2}{G}
Mana value     : 3
Type           : Enchantment

If one or more +1/+1 counters would be put on a creature you control, twice
that many +1/+1 counters are put on that creature instead.

Color identity : G (green)
Rarity         : rare
Commander      : legal
EDHREC rank    : #368
Price (USD)    : $6.85

── Rulings (3) ───────────────────────────────────────────────────────────
[2020-06-23] (wotc)
  If a creature you control would enter the battlefield with a number of
  +1/+1 counters on it, it enters with twice that many instead.

[2020-06-23] (wotc)
  If two or more effects attempt to modify how many counters would be put
  onto a creature you control, you choose the order to apply those
  effects, no matter who controls the sources of those effects.

[2020-06-23] (wotc)
  If you control two Branching Evolutions, the number of +1/+1 counters
  put on a creature is four times the original number. Three Branching
  Evolutions multiplies the original number by eight, and so on.
```

```
── Faerie Mastermind ─────────────────────────────────────────────────────
Mana cost      : {1}{U}
Mana value     : 2
Type           : Creature — Faerie Rogue

Flash
Flying
Whenever an opponent draws their second card each turn, you draw a card.
{3}{U}: Each player draws a card.

P/T            : 2/1

Color identity : U (blue)
Keywords       : Flying, Flash
Rarity         : rare
Commander      : legal
EDHREC rank    : #313
Price (USD)    : $12.08

── Rulings (1) ───────────────────────────────────────────────────────────
[2023-04-14] (wotc)
  Faerie Mastermind doesn't need to have been under your control when the
  first card is drawn for its ability to trigger. As long as you control
  it when an opponent draws their second card in a turn, that ability will
  trigger.
```

```
── Hardened Scales ───────────────────────────────────────────────────────
Mana cost      : {G}
Mana value     : 1
Type           : Enchantment

If one or more +1/+1 counters would be put on a creature you control, that
many plus one +1/+1 counters are put on it instead.

Color identity : G (green)
Rarity         : rare
Commander      : legal
EDHREC rank    : #186
Price (USD)    : $2.28

── Rulings (3) ───────────────────────────────────────────────────────────
[2023-09-01] (wotc)
  If a creature you control would enter the battlefield with a number of
  +1/+1 counters on it, it enters with that many plus one instead.

[2023-09-01] (wotc)
  If two or more effects attempt to modify how many counters would be put
  on a creature you control, you choose the order to apply those effects,
  no matter who controls the sources of those effects.

[2023-09-01] (wotc)
  Each additional Hardened Scales you control will increase the number of
  +1/+1 counters placed on a creature you control by one.
```

```
── Heroic Intervention ───────────────────────────────────────────────────
Mana cost      : {1}{G}
Mana value     : 2
Type           : Instant

Permanents you control gain hexproof and indestructible until end of turn.

Color identity : G (green)
Rarity         : rare
Commander      : legal
EDHREC rank    : #31
Price (USD)    : $16.17

── Rulings (3) ───────────────────────────────────────────────────────────
[2020-06-23] (wotc)
  A planeswalker with indestructible still loses loyalty counters as it's
  dealt damage and will still be put into its owner's graveyard if its
  loyalty reaches 0.

[2020-06-23] (wotc)
  The set of permanents affected by Heroic Intervention is determined as
  the spell resolves. Permanents you begin to control later in the turn
  won't gain hexproof and indestructible.
```

```
── Simic Ascendancy ──────────────────────────────────────────────────────
Mana cost      : {G}{U}
Mana value     : 2
Type           : Enchantment

{1}{G}{U}: Put a +1/+1 counter on target creature you control.
Whenever one or more +1/+1 counters are put on a creature you control, put
that many growth counters on this enchantment.
At the beginning of your upkeep, if this enchantment has twenty or more
growth counters on it, you win the game.

Color identity : UG (blue, green)
Rarity         : rare
Commander      : legal
EDHREC rank    : #1258
Price (USD)    : $0.44

── Rulings (4) ───────────────────────────────────────────────────────────
[2019-01-25] (wotc)
  If Simic Ascendancy doesn't have twenty or more growth counters on it as
  your upkeep begins, its last ability won't trigger. You can't take any
  actions during your turn before your upkeep begins.

[2019-01-25] (wotc)
  If the last ability does trigger, but Simic Ascendancy leaves the
  battlefield, use the number of counters it had on it immediately before
  it left the battlefield to determine whether you win the game.
```

**Cards with no price in the local database** (stated as such above, never estimated): Evolving Wilds, Sphinx of Enlightenment, Promise of Loyalty, Mr. Foxglove, Cleansing Nova, Sylvan Tutor.
