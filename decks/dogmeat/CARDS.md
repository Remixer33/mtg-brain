# Scrappy Survivors — Card-by-Card Study Guide

**Deck slug:** `dogmeat` · **Commander:** Dogmeat, Ever Loyal · **Colors:** Naya (white/red/green, `WRG`)
**Format: Commander (EDH) only.** 100 cards, singleton (one copy of everything except basic lands), no sideboard — Commander has no sideboard.

Every card in the deck is explained below, grouped by **the job it does**, not alphabetically. Each card appears exactly once; where a card does two jobs, the second job is called out in its entry.

Every fact in this file — mana cost, type line, power/toughness, rules text, official rulings, rules numbers — was pulled from the local database in the same session this file was written. If something is not in the database, this file says "not in my data" rather than guessing.

---

## How to read this file

**Mana symbols.** `{W}` = one white mana. `{G}` = green. `{R}` = red. `{1}`, `{2}`, `{3}` = that much *generic* mana, payable with any color. `{T}` = "tap this permanent" (turn it sideways) as a cost. `{C}` = one colorless mana, which can only pay generic costs and other `{C}` costs — it cannot pay `{W}`, `{R}`, or `{G}`.

**Mana value (MV)** = the total amount of mana in a card's cost. `{2}{W}` has mana value 3.

**How quotes work in this file.** Text inside quotation marks is copied from the database, not paraphrased — check any of it with `mtg card "<name>"`, `mtg rule <number>` or `mtg glossary "<term>"`. Two conventions:
- A card's printed text runs across several lines; quoting it inline turns each line break into a sentence break. Nothing is added.
- An ellipsis (**…**) marks a cut inside a quote. Almost every cut is **reminder text** — the italic parenthetical a card prints to restate a keyword it already has, e.g. Swiftfoot Boots printing "(It can't be the target of spells or abilities your opponents control…)" after the word *hexproof*. Reminder text changes nothing about how a card works, and this file explains those keywords itself, so it is cut for length. **No ability, cost, condition or number is ever cut.** Run `mtg card "<name>"` to see the full printed text. A quote may also simply stop early — e.g. the first sentence of a long ruling — which is why the date and card name are always given so you can read the rest.

**The two words this whole deck runs on:**

- **Aura** — *"An enchantment subtype. Aura spells target objects or players, and Aura permanents are attached to objects or players."* (`mtg glossary Aura`, pointing at rules 303 and 702.5). In plain terms: an enchantment you stick onto something. Most Auras here say "Enchant creature" and sit on a creature, buffing it.
- **Equipment** — *"An artifact subtype. Equipment can be attached to creatures."* (`mtg glossary Equipment`, rules 301 and 702.6). A piece of gear. It enters the battlefield **unattached** and you pay its **equip** cost to move it onto a creature.

**Equip**, precisely (rule 702.6a): *"Equip is an activated ability of Equipment cards. 'Equip [cost]' means '[Cost]: Attach this permanent to target creature you control. Activate only as a sorcery.'"* — "**only as a sorcery**" means only on **your** turn, during a **main phase** (before or after combat), when nothing else is waiting to resolve. **You cannot equip during combat or on someone else's turn.** This is the single most common beginner mistake with this deck.

**Attach** (`mtg glossary Attach`, rule 701.3): *"To take an Aura, Equipment, or Fortification from where it currently is and put it onto a specified object or player."*

**Modified** (`mtg glossary Modified`, rule 700.9): *"A modified creature is a creature that has a counter on it, is equipped, or is enchanted by an Aura its controller also controls."* Several cards here care about this word. (Rule 700.9 states the same test for permanents generally, with pointers to the counter, Equipment and Aura rules.)

**When the creature dies:**
- Auras go to the graveyard with it — rule 704.5m: *"If an Aura is attached to an illegal object or player, or is not attached to an object or player, that Aura is put into its owner's graveyard."*
- Equipment **stays on the battlefield**, just unattached — rule 301.5c: *"An Equipment that equips an illegal or nonexistent permanent becomes unattached from that permanent but remains on the battlefield."*

That asymmetry is why this deck runs so much Aura recursion and so little Equipment recursion.

**Junk token** (`mtg glossary "Junk Token"`): *"A Junk token is a colorless artifact token with '{T}, Sacrifice this token: Exile the top card of your library. You may play that card this turn. Activate only as a sorcery.'"* Junk is this deck's currency. Note the fine print from the Dogmeat rulings: *"You pay all costs and follow all normal timing rules for the card played from exile with a Junk token's ability. For example, if the exiled card is a land card, you may play it only during your main phase while the stack is empty."* And: *"You can't sacrifice a Junk token to pay multiple costs."*

**Treasure token** (`mtg glossary "Treasure Token"`): *"A Treasure token is a colorless artifact token with '{T}, Sacrifice this token: Add one mana of any color.'"*
**Food token** (`mtg glossary "Food Token"`): *"A Food token is a colorless artifact token with '{2}, {T}, Sacrifice this token: You gain 3 life.'"*

---

## Commander

#### Dogmeat, Ever Loyal — {R}{G}{W} — Legendary Creature — Dog — 3/3

Your commander. He starts in the **command zone**, a special zone outside your deck, and you may cast him from there any time you could cast a creature spell.

Two abilities:
1. **"When Dogmeat enters, mill five cards, then return an Aura or Equipment card from your graveyard to your hand."** *Mill* means "puts that many cards from the top of their library into their graveyard" (`mtg glossary Mill`, rule 701.17). So: dump your own top 5 cards into your graveyard, then grab one Aura or Equipment card out of the graveyard. Since 28 of your 61 maindeck non-land cards are Auras (15) or Equipment (13), milling 5 usually hands you a live target.
2. **"Whenever a creature you control that's enchanted or equipped attacks, create a Junk token."** This is the card-advantage engine. Not "whenever Dogmeat attacks" — **any** creature you control that has an Aura or an Equipment on it. Attack with three dressed-up creatures, get three Junk. Each Junk later exiles your top card and lets you play it that turn.

**When to play it:** Turn 3 if you have the `{R}{G}{W}` (all three colors on turn 3 is genuinely hard here — 12 of your 38 lands enter tapped). Otherwise turn 4 or 5 is fine. He is not required for the deck to function; attachments still buff creatures without him. Cast him when you can also afford to protect him or when you want the mill-5 to refill your graveyard.

**Watch out:** He is a 3/3 with no protection built in — he dies to almost anything. Every time you recast him from the command zone he costs {2} more (rule 903.8: *"A commander cast from the command zone costs an additional {2} for each previous time the player casting it has cast it from the command zone that game"*). Also: the Junk trigger checks *attacking*, so a creature with an Aura that sits home blocking makes you nothing. And note his mill-5 hits **your** library, not an opponent's.

**Rulings:**
- [2024-03-08] *"The card you return with Dogmeat's first ability doesn't have to be one of the cards you milled with that ability."* — you can grab something that was already in the graveyard.
- [2024-03-08] *"You pay all costs and follow all normal timing rules for the card played from exile with a Junk token's ability. For example, if the exiled card is a land card, you may play it only during your main phase while the stack is empty."*
- [2024-03-08] *"You can't sacrifice a Junk token to pay multiple costs. For example, you can't sacrifice a Junk token to activate its own ability and also to activate the second ability of Junk Jet."*
- [2024-03-08] *"Some spells and abilities that create Junk tokens may require targets. If each target chosen is illegal as that spell or ability tries to resolve, it won't resolve and none of its effects happen. You won't create any Junk tokens."*

---

## Ramp & Mana

"Ramp" = anything that gets you more mana than your one-land-per-turn allowance. This deck has 9 such cards plus 38 lands.

#### Sol Ring — {1} — Artifact
Costs one mana, taps for two colorless. It pays for itself the turn after you play it and every turn thereafter. The single most-played card in Commander (EDHREC rank #1 in the local database).

**When to play it:** Immediately, on any turn you draw it. Turn 1 Sol Ring is the best opening in the format.

**Watch out:** It makes `{C}{C}` — **colorless** mana. Colorless mana cannot pay the `{R}`, `{G}`, or `{W}` in Dogmeat's cost. Sol Ring accelerates your *generic* costs (equip costs, `{3}` of Grim Reaper's Sprint, Champion's Helm), not your colored ones.

#### Arcane Signet — {2} — Artifact
Taps for one mana of any color in your commander's color identity — for you, that means any one of red, green, or white. A two-mana rock that fixes all three of your colors.

**When to play it:** Turn 2 if you have nothing better, or the turn before you want to cast Dogmeat. It directly solves the "I have three lands but not the right three colors" problem.

**Watch out:** Unlike Sol Ring it only makes **one** mana — it fixes colors, it doesn't really accelerate.

#### Agility Bobblehead — {3} — Artifact — Bobblehead
Two abilities. `{T}: Add one mana of any color` — a three-mana rock that fixes every color. And `{3}, {T}: Up to X target creatures you control each gain haste until end of turn and can't be blocked this turn except by creatures with haste, where X is the number of Bobbleheads you control as you activate this ability.` You control two Bobbleheads in this deck (this one and Perception Bobblehead), so X is 1 or 2.

**When to play it:** As a mana rock early. Late, its second ability is a finisher — near-unblockable is exactly what a creature loaded with Auras wants.

**Watch out:** It taps for **either** mana **or** the haste/evasion ability, not both — and the ability also costs {3} on top of the tap. Realistically you use it as a mana rock most turns. Also, "can't be blocked this turn except by creatures with haste" is not true unblockable; a fast opponent with a hasty creature can still block.

#### Perception Bobblehead — {3} — Artifact — Bobblehead
`{T}: Add one mana of any color.` Plus `{3}, {T}: Look at the top X cards of your library, where X is the number of Bobbleheads you control. You may cast a spell with mana value 3 or less from among them without paying its mana cost. Put the rest on the bottom of your library in a random order.`

**When to play it:** Same as Agility Bobblehead — a colour-fixing rock first. With both Bobbleheads out, X = 2, and a free mana-value-3-or-less spell is a real bonus given this deck's average non-land mana value of 2.82.

**Watch out:** With only one Bobblehead you look at exactly one card. Six mana total (three to cast, then {3} to activate) for a peek at one card is a bad rate — treat this as a mana rock that occasionally does something extra.

#### Wild Growth — {G} — Enchantment — Aura
"Enchant land. Whenever enchanted land is tapped for mana, its controller adds an additional {G}." One mana, and from then on that land taps for one extra green.

**When to play it:** Turn 1 on a land you will tap every turn. Put it on a basic Forest or a land that taps for green.

**Watch out:** The extra mana is **green specifically**, regardless of what the land makes. It also does not untap the land — it just adds `{G}` when the land is tapped for mana. And it counts as an enchantment you control, which quietly grows All That Glitters.

#### Abundant Growth — {G} — Enchantment — Aura
"Enchant land. When this Aura enters, draw a card. Enchanted land has '{T}: Add one mana of any color.'" One green mana, replaces itself with a card, and turns any land — including a colorless one — into a perfect any-color land.

**When to play it:** Turn 1, ideally on one of your seven colorless-only lands (Ash Barrens, Buried Ruin, Junktown, Roadside Reliquary, Rogue's Passage, Scavenger Grounds, Temple of the False God), converting a dead-ish land into a Command Tower.

**Watch out:** It *replaces* nothing — it grants the land a **new** ability. The land keeps its original one too, but you can only tap it once. This is fixing, not ramp.

#### Fertile Ground — {1}{G} — Enchantment — Aura
"Enchant land. Whenever enchanted land is tapped for mana, its controller adds an additional one mana of any color." Wild Growth's bigger sibling: real ramp *and* real fixing in one card.

**When to play it:** Turn 2. This is the ramp piece that most reliably gets you to a turn-3 Dogmeat, because the extra mana can be any color.

**Watch out:** Like Wild Growth, if the enchanted land is destroyed or bounced you lose both cards. Do not stack multiple land Auras on the same land unless you are trying to power out something huge.

#### Bighorner Rancher — {4}{G} — Creature — Human Ranger — 2/5
Vigilance (it attacks without tapping). `{T}: Add an amount of {G} equal to the greatest power among creatures you control.` And `Sacrifice this creature: You gain life equal to the greatest toughness among other creatures you control.`

**When to play it:** Late, once you have a fat creature. In a deck that regularly makes a 9/10 (Almost Perfect) or a creature stacked with Strong Back, tapping this for 6–10 green mana is genuinely explosive.

**Watch out:** It is a five-mana 2/5 that does nothing the turn it arrives — creatures have "summoning sickness" and cannot use `{T}` abilities the turn they enter unless they have haste. The mana it makes is all **green**, so it cannot cast Dogmeat by itself. The sacrifice ability checks **other** creatures' toughness, so it does nothing if it is your only creature.

#### Preston Garvey, Minuteman — {2}{R}{G}{W} — Legendary Creature — Human Soldier — 4/4
A five-mana 4/4 with two triggers. At the beginning of combat on your turn, he creates an Aura token named **Settlement** attached to a land you control, and that land gains "`{T}`: Add one mana of any color." Second: whenever Preston attacks, untap each **enchanted permanent** you control.

**When to play it:** Turn 5+, once you already have Auras out. The untap clause is the real payoff — attack with Preston and untap every land wearing Wild Growth, Fertile Ground, Abundant Growth, a Settlement token, or Squirrel Nest, which is a big mana burst in the middle of combat.

**Watch out:** "Untap each enchanted permanent" only hits things with an **Aura** on them (rule 700.9's definition of enchanted). Equipment does not count. Also, `{2}{R}{G}{W}` is the hardest cost in the deck to assemble.

**Rulings:**
- [2024-03-08] *"If the target land is an illegal target as Preston Garvey's first ability tries to resolve, it won't resolve and none of its effects happen. The Settlement token won't be created."*
- [2024-03-08] *"In the rare case that the target land is a legal target as Preston Garvey's first ability resolves but the target land can't legally be enchanted by the Settlement token, the token won't be created at all."*

---

## Card Draw & Selection

The deck has no tutors (cards that search your library for a specific non-land card) — zero, per `mtg deck stats dogmeat -v`. These six cards are how you find action.

#### Pip-Boy 3000 — {1} — Artifact — Equipment
"Whenever equipped creature attacks, choose one — • **Sort Inventory** — Draw a card, then discard a card. • **Pick a Perk** — Put a +1/+1 counter on that creature. • **Check Map** — Untap up to two target lands. Equip {2}."

A one-mana Equipment that turns every attack into a small choice. Critically, it makes the creature *equipped*, which turns on Dogmeat's Junk trigger for one mana.

**When to play it:** Turn 1 or 2, and equip it to your first creature. It is the cheapest way to make a creature "equipped" for Dogmeat.

**Watch out:** "Draw a card, then discard a card" is not net card advantage — it is filtering (this is called *looting*). Also remember Check Map untaps **lands**, not creatures. And this is the classic equip-timing trap: equip it in your **precombat main phase**, before you declare attackers, or you get nothing.

#### Vault 21: House Gambit — {1}{R} — Enchantment — Saga
A **Saga** is an enchantment subtype — *"Sagas have a number of chapter abilities that take effect over a number of turns to tell a story"* (`mtg glossary Saga`, rule 714). The card itself prints the how-to as reminder text: *"(As this Saga enters and after your draw step, add a lore counter. Sacrifice after III.)"* In the rules that is: it enters with one lore counter (rule 714.3a), gets another as your precombat main phase begins — i.e. right after your draw step (rule 714.3c) — and is sacrificed once its counters reach its final chapter number (rule 714.4).
- I, II — Discard a card, then draw a card.
- III — Reveal up to five nonland cards from your hand. For each of those cards that has the same mana value as another card revealed this way, create a Treasure token.

**When to play it:** Turn 2 when your hand has a clunker or two you would like to swap. Three turns later, chapter III often gives 2–4 Treasures because this deck is packed with 1-, 2-, and 3-drops.

**Watch out:** Chapters I and II are discard-**then**-draw, so you must have a card to pitch. Chapter III counts *matching pairs*, so revealing five cards of five different mana values makes zero Treasures. The Saga sacrifices itself after chapter III, which briefly lowers your All That Glitters count.

#### Veronica, Dissident Scribe — {2}{R} — Legendary Creature — Human Artificer Rogue — 3/3
Menace (*"A creature with menace can't be blocked except by two or more creatures"* — rule 702.111b). Whenever she attacks, you may discard a card, and if you do, draw a card. And: whenever you discard one or more nonland cards for the first time each turn, create a Junk token.

**When to play it:** Turn 3. She is an evasive body that filters your hand every combat and converts each discard into Junk.

**Watch out:** The Junk trigger is "first time each turn" — discarding twice in a turn only makes one Junk. Discarding a **land** does not trigger it at all (nonland cards only). She has no built-in protection, so an Aura on her is still a 2-for-1 risk.

**Rulings:**
- [2024-03-08] *"You pay all costs and follow all normal timing rules for the card played from exile with a Junk token's ability."*
- [2024-03-08] *"You can't sacrifice a Junk token to pay multiple costs."*

#### Armory Paladin — {1}{R}{W} — Creature — Human Knight — 3/3
Trample. "Whenever you cast an Aura or Equipment spell, exile the top card of your library. You may play that card until the end of your next turn."

A 3/3 trampler that turns every attachment you cast into a free extra card. This is called *impulse draw* — the card is exiled face up and you have a window to play it.

**When to play it:** Turn 3, before a run of cheap attachments. With 28 Auras and Equipment in the deck, he triggers constantly.

**Watch out:** You still **pay** for the exiled card; it is not free. If the window closes (end of your next turn) the card is lost forever. And if you exile a land, you can only play it as your land for the turn.

#### Cait, Cage Brawler — {R}{G} — Legendary Creature — Human Warrior — 1/1
"During your turn, Cait has indestructible." (Indestructible: *"a keyword ability that precludes a permanent from being destroyed"* — `mtg glossary Indestructible`, rule 702.12. It does not stop exile or "sacrifice" effects.) "Whenever Cait attacks, you and defending player each draw a card, then discard a card. Put two +1/+1 counters on Cait if you discarded the card with the greatest mana value among those cards or tied for greatest."

**When to play it:** Turn 2, and treat her as your **premier Aura carrier**. She survives every removal spell that says "destroy" during your own turn, which is exactly when you attack — so your Auras stay attached.

**Watch out:** She is a 1/1 base, so she needs help to matter. The indestructible is **only on your turn** — on an opponent's turn she is a fragile 1/1, and your Auras go with her. The draw-then-discard is symmetric: the defending player draws too.

**Rulings:**
- [2024-03-08] *"If a card you discard has {X} in its mana cost, X is considered to be 0."*
- [2024-03-08] *"If you somehow can't discard a card… you won't put any counters on Cait no matter whether or not the defending player discarded a card."*

#### Well Rested — {1}{G} — Enchantment — Aura
"Enchant creature. Enchanted creature has 'Whenever this creature becomes untapped, put two +1/+1 counters on it, then you gain 2 life and draw a card. This ability triggers only once each turn.'"

Attack with the creature; on your next untap step it untaps, and you get +2/+2 permanently, 2 life, and a card. Repeat every turn.

**When to play it:** Turn 2–3 on a creature you plan to attack with every single turn. Over three turns that is six counters and three cards.

**Watch out:** The trigger is on **untapping**, not on attacking. A creature with **vigilance** (attacks without tapping — e.g. Cass or Bighorner Rancher) never taps, so it never untaps, so Well Rested does **nothing** on it. That is a real trap. Put it on a creature that taps to attack.

---

## Removal & Interaction

Only 4 dedicated removal spells and 6 interaction pieces across 99 cards — this is the deck's thinnest area. Spend removal carefully.

#### Path to Exile — {W} — Instant
"Exile target creature. Its controller may search their library for a basic land card, put that card onto the battlefield tapped, then shuffle." One white mana, at instant speed, and the creature is **exiled** — gone permanently, not to the graveyard, so it dodges indestructible and recursion.

**When to play it:** On the scariest creature at the table, ideally when it attacks or when its controller taps out. Best used on a commander or a creature carrying attachments.

**Watch out:** You are **ramping your opponent** — they get a basic land. That is a real cost early; less so on turn 10. Also, exile removes their creature's Auras too (they hit the graveyard per rule 704.5m), which is a bonus when hitting an enchanted creature.

**Rulings:**
- [2026-01-27] *"The controller of the exiled creature isn't required to search their library for a basic land. If that player doesn't, the player won't shuffle their library."*
- [2026-01-27] *"If the target creature is an illegal target by the time Path to Exile tries to resolve, it won't resolve and none of its effects will happen."*

#### Valorous Stance — {1}{W} — Instant
"Choose one — • Target creature gains indestructible until end of turn. … • Destroy target creature with toughness 4 or greater."

A two-in-one: either save your own guy from a "destroy" effect or kill something big.

**When to play it:** Hold it. If someone points removal at your loaded-up creature, use mode 1. If nothing threatens you, kill their best big creature at end of turn.

**Watch out:** Mode 2 only hits **toughness 4 or greater** — it cannot kill a 5/2. Mode 1's indestructible does **not** stop exile, "-X/-X" effects, sacrifice effects, or bounce.

#### Break Down — {2}{G} — Instant
"Destroy target artifact or enchantment. Create a Junk token. …"

Green removal for artifacts and enchantments, with a Junk token stapled on so it always does something extra.

**When to play it:** On an opposing mana rock, an Equipment, a pillowfort enchantment, or anything artifact/enchantment that is beating you. In a pod full of Commander decks there is basically always a target.

**Watch out:** It cannot hit an ordinary creature, a land, or a planeswalker. It *can* hit an artifact creature such as Mister Gutsy or Codsworth, because an artifact creature is still an artifact — but do not hold this card hoping to kill a normal creature.

#### Chaos Warp — {2}{R} — Instant
"The owner of target permanent shuffles it into their library, then reveals the top card of their library. If it's a permanent card, they put it onto the battlefield."

Red's catch-all answer: it can hit **any permanent** — creature, enchantment, artifact, land, planeswalker, or a commander. Red normally cannot touch enchantments, so this is precious.

**When to play it:** On the one problem permanent your other removal cannot answer. It also handles commanders well, because shuffling into the library keeps them off the command zone.

**Watch out:** It is a gamble — they might flip into something worse. Do not use it as your default removal spell; save it for the permanent nothing else in your deck can answer.

**Rulings:**
- [2011-09-22] *"A permanent card is a card with one or more of the following card types: artifact, creature, enchantment, land, or planeswalker."*
- [2011-09-22] *"If the revealed card is not a permanent card, it remains on top of that library."*
- [2011-09-22] *"If the revealed card is a permanent card but can't enter (perhaps because it's an Aura with nothing to enchant), it remains on top of that library."*
- [2011-09-22] *"The owner of a token is the player under whose control the token was put onto the battlefield."*

#### Heroic Intervention — {1}{G} — Instant
"Permanents you control gain hexproof and indestructible until end of turn." (*Hexproof*: cannot be targeted by opponents — rule 702.11.)

Two mana that blanks a board wipe, a targeted removal spell, or an edict-ish sweep aimed at your permanents. In a deck that stacks four attachments onto one creature, this is the card that stops you losing the game to one Wrath effect.

**When to play it:** Hold two mana open once you have committed 3+ cards to a single creature. Cast it **in response** to the removal spell or wipe, not before.

**Watch out:** It does not stop **exile** effects, sacrifice effects, or "-X/-X". It only protects permanents you control **at the time it resolves**. It is one card — you will not always have it, so do not over-commit assuming you do.

**Rulings:**
- [2020-06-23] *"The set of permanents affected by Heroic Intervention is determined as the spell resolves. Permanents you begin to control later in the turn won't gain hexproof and indestructible."*

#### Commander Sofia Daguerre — {3}{W} — Legendary Creature — Human Pilot — 1/3
Flash (*"a keyword ability that lets a player play a card any time they could cast an instant"* — rule 702.8). "Crash Landing — When Commander Sofia Daguerre enters, destroy up to one target legendary permanent. That permanent's controller creates a Junk token."

Because she has flash, she is effectively a four-mana instant-speed "destroy target commander" that leaves a 1/3 behind.

**When to play it:** Flash her in on an opponent's turn to kill their commander, ideally after they have equipped it or spent mana on it. "Up to one" means you can also just flash her in as a surprise blocker with no target.

**Watch out:** **Legendary permanents only** — she cannot kill a normal creature. Most opposing commanders are legendary, so she almost always has a target, but check first. Also note she gives *them* the Junk token, not you.

---

## Board Wipes

One true sweeper plus two conditional ones. Because your creatures usually carry Auras, wipes cost **you** more cards than they cost your opponents — that is the core tension in this deck.

#### Blasphemous Act — {8}{R} — Sorcery
"This spell costs {1} less to cast for each creature on the battlefield. Blasphemous Act deals 13 damage to each creature."

The printed cost is nine mana, but it counts **every** creature on the battlefield, including your own and every opponent's. In a four-player game with eight creatures out, it costs `{R}` plus zero generic — one red mana to kill everything.

**When to play it:** When you are behind on board and the table has committed a lot of creatures. Ideally when you hold Heroic Intervention (your creatures survive) or when your own board is nearly empty.

**Watch out:** 13 damage is *damage*, so indestructible creatures survive it. It kills **your** creatures too, and every Aura on them goes to the graveyard with them. Never cast it into your own developed board without protection.

**Rulings:**
- [2020-11-10] *"Blasphemous Act's ability can't reduce the total cost to cast the spell below {R}."*
- [2020-11-10] *"The total cost to cast Blasphemous Act is locked in before you pay that cost."*
- [2020-11-10] *"To determine the total cost of a spell, start with the mana cost or alternative cost you're paying, add any cost increases, then apply any cost reductions… The mana value of the spell is determined only by its mana cost, no matter what the total cost to cast the spell was."* — so it is still a mana-value-9 card for anything that checks mana value.

#### Single Combat — {3}{W}{W} — Sorcery
"Each player chooses a creature or planeswalker they control, then sacrifices the rest. Players can't cast creature or planeswalker spells until the end of your next turn."

A one-sided-ish wipe: **you** keep your best creature (the one wearing all the Auras), everyone else keeps one too — and then nobody can rebuild for a full turn cycle.

**When to play it:** When you have one dressed-up creature and everyone else has a wide board. You then get a free swing at a nearly empty table while they cannot deploy blockers.

**Watch out:** This is a **sacrifice**, not a destroy — indestructible does not save the creatures you lose, and it *does* get past opposing indestructible. Everything sacrificed is a creature you no longer have to carry attachments. If you have three enchanted creatures, you lose two of them plus all their Auras.

**Rulings:**
- [2019-05-03] *"As Single Combat resolves, first the player whose turn it is chooses a creature or planeswalker they control, then each other player in turn order does the same, knowing the choices made before them. Then each unchosen creature and planeswalker is sacrificed at the same time."*
- [2019-05-03] *"In a multiplayer game, if you leave the game after Single Combat resolves but before your next turn begins, its effect lasts until your next turn would have begun."*

#### Megaton's Fate — {5}{R} — Sorcery
"Choose one — • **Disarm** — Destroy target artifact. Create four Treasure tokens. • **Detonate** — Megaton's Fate deals 8 damage to each creature. Each player gets four rad counters."

Two very different cards in one. Disarm is artifact removal that also makes four Treasures (a big ramp burst). Detonate is a sweeper that also inflicts **rad counters**.

**Rad counters**, precisely (from the official ruling): *"There is an inherent triggered ability associated with having rad counters… 'At the beginning of the precombat main phase of a player with rad counters, that player mills cards equal to the number of rad counters they have. For each nonland card milled this way, that player loses 1 life and removes one rad counter from themselves.'"*

**When to play it:** Six mana is a lot. Disarm mode is the one you will use most — kill a Sol Ring or an opposing Equipment and pocket four Treasures, which effectively refunds most of the cost. Detonate only when 8 damage kills more of theirs than yours.

**Watch out:** Detonate gives **every player** four rad counters, including **you** — you will mill and lose life too. Note also from the rulings: *"Rad counters don't go away as steps, phases, or turns end. They only go away when an effect instructs a player to remove rad counters from themselves."* Mild upside: milling yourself fills the graveyard for Dogmeat, Cass, and Mantle of the Ancients.

**Rulings:**
- [2024-03-08] *"If a player has fewer cards remaining in their library than the number of rad counters they have when the triggered ability resolves, they'll mill as many cards as they can."*
- [2024-03-08] *"Rad counters are a kind of counter that a player may have. They're not associated with any specific permanents."*

---

## Threats & Beaters

This deck's real threats are its attachments — these are the bodies and the finishers that convert attachments into damage.

#### Gunner Conscript — {1}{G} — Creature — Human Mercenary — 2/2
Trample (excess damage carries through to the player past blockers — rule 702.19b). "This creature gets +1/+1 for each Aura and Equipment attached to it." Plus: when it dies, if it was enchanted, create a Junk token; when it dies, if it was equipped, create a Junk token (two separate triggers, so both can fire).

The perfect two-mana carrier: it grows with every attachment, has trample so the extra power actually reaches the player, and pays you back when it dies.

**When to play it:** Turn 2, then start piling attachments on it. With three attachments it is a 5/5 trampler for two mana.

**Watch out:** No protection whatsoever. If you stack four Auras on it and it eats a removal spell, you lose five cards for two Junk tokens. Pair it with Swiftfoot Boots or Champion's Helm before over-committing.

#### Ian the Reckless — {1}{R} — Legendary Creature — Human Warrior — 2/1
"Whenever Ian the Reckless attacks, if it's modified, you may have it deal damage equal to its power to you and any target." (Its own reminder text: *"Equipment, Auras you control, and counters are modifications."*)

A two-mana body that, once dressed up, throws its power at anything each attack — a creature, a planeswalker, or a player. It is a second damage source stapled to combat.

**When to play it:** Turn 2 as an early carrier; later, when you can make him big, each attack becomes "deal X to a creature" removal *and* combat damage.

**Watch out:** The damage hits **you** as well as the target — a 9-power Ian deals 9 to you. It is a "may," so you always get the choice, but at 40 starting life you can only do this a few times. He is also a 2/1, dying to any chip damage.

**Rulings:**
- [2024-03-08] *"If Ian the Reckless isn't modified when it attacks, its ability won't trigger at all. When its ability tries to resolve, if it isn't modified at that time, the ability won't resolve."*
- [2024-03-08] *"If Ian the Reckless leaves the battlefield before its last ability resolves, as long as it was modified when it was last on the battlefield, use its power as it last existed on the battlefield to determine how much damage that ability deals."*

#### Crimson Caravaneer — {2}{R} — Creature — Human Scout — 1/2
Double strike and trample. "Whenever this creature deals combat damage to a player, create a Junk token."

Double strike means *"a keyword ability that lets a creature deal its combat damage twice"* (rule 702.4) — it deals damage in a first-strike step and again in the normal step. Combined with trample, every point of pump you put on it is worth **double**.

**When to play it:** Turn 3, then attach everything to it. All That Glitters giving +5/+5 turns this into 12 trample damage across two strikes.

**Watch out:** A 1/2 base body dies to a stiff breeze. Its Junk trigger requires damage **to a player**, so a chump-blocked Caravaneer makes nothing — trample helps here, since even 1 point getting through counts.

#### Duchess, Wayward Tavernkeep — {3}{R} — Legendary Creature — Human Citizen — 4/3
"Hunters for Hire — Whenever a creature you control deals combat damage to a player, put a quest counter on it." And `{1}, Remove a quest counter from a permanent you control: Create a Junk token. …`

A four-mana 4/3 that turns connecting in combat into stored value. Quest counters accumulate on your creatures, and you can cash them in for Junk any time you have a spare mana.

**When to play it:** Turn 4 on a board where you are already attacking. Note her counters make creatures **modified** (rule 700.9), which turns on Ian the Reckless.

**Watch out:** Removing the counter costs {1} on top — Junk is not free. And each quest counter is +0/+0 by itself; only Moira Brown's Book Equipment token actually converts them into stats.

**Rulings:**
- [2024-03-08] *"You can't sacrifice a Junk token to pay multiple costs. For example, you can't sacrifice a Junk token to activate its own ability and also to activate the second ability of Junk Jet."*
- [2024-03-08] *"Some spells and abilities that create Junk tokens may require targets. If each target chosen is illegal as that spell or ability tries to resolve, it won't resolve and none of its effects happen. You won't create any Junk tokens."*

#### Super Mutant Scavenger — {4}{G} — Creature — Mutant Warrior — 5/5
Trample. "When this creature enters **or dies**, return up to one target Aura or Equipment card from your graveyard to your hand."

A five-mana 5/5 trampler that buys back an attachment twice — once coming down, once going away. Secondary role: this is one of your six recursion pieces.

**When to play it:** Turn 5, especially after a board wipe or after Dogmeat's mill has stocked your graveyard. It is the biggest naked body in the deck.

**Watch out:** It returns the card to your **hand**, not the battlefield — you still have to pay for it again. "Up to one" means it can also do nothing if your graveyard is empty, which is fine.

#### Grim Reaper's Sprint — {4}{R} — Enchantment — Aura
"Morbid — This spell costs {3} less to cast if a creature died this turn. Enchant creature. When this Aura enters, untap each creature you control. If it's your main phase, there is an additional combat phase after this phase. Enchanted creature gets +2/+2 and has haste."

This is the deck's finisher. Untap all your creatures and take a **second combat phase** — meaning every enchanted or equipped creature attacks again, and Dogmeat triggers again for each one.

**When to play it:** In your **postcombat main phase**, after your first attack. Cast it there and you get a whole second combat. If a creature has died this turn (yours or anyone's, including in that combat) it costs only `{1}{R}`.

**Watch out:** Read the timing carefully — the extra combat only happens "if it's your main phase," so casting it during combat gets you nothing but +2/+2 and haste. Morbid checks whether a creature **died this turn**, so combat deaths from your own first attack turn it on.

**Rulings:**
- [2024-03-08] *"If the creature Grim Reaper's Sprint would enchant is an illegal target by the time Grim Reaper's Sprint would resolve, the entire spell doesn't resolve. It's put into the graveyard from the stack, so its triggered ability won't trigger, and you won't untap your creatures or get an additional combat phase."* — if they kill the target in response, you lose everything.

#### Junk Jet — {1}{R} — Artifact — Equipment
"When this Equipment enters, create a Junk token. … `{3}, Sacrifice another artifact: Double equipped creature's power until end of turn.` Equip {1}."

Comes with a free Junk token, and its activated ability doubles power — that is your out-of-nowhere lethal button. It can be activated multiple times if you have artifacts to feed it (each activation doubles again).

**When to play it:** Turn 2 for the free Junk. Save the doubling ability for the attack that ends someone.

**Watch out:** It sacrifices **another** artifact — Junk tokens, Treasures, Food, and even other Equipment all qualify, but you cannot sacrifice Junk Jet itself. And per the official ruling: *"You can't sacrifice a Junk token to pay multiple costs. For example, you can't sacrifice a Junk token to activate its own ability and also to activate the second ability of Junk Jet."* The doubling only affects **power**, not toughness.

---

## Synergy Pieces — the deck's actual engine

Twenty-six cards. This is what the deck **is**: Auras and Equipment, plus the creatures that pay you for having them. Of the 61 non-land cards in the 99-card maindeck, 28 are Auras (15) or Equipment (13). Counted a different way, the deck holds 19 artifacts and 17 enchantments in total.

### The payoffs — cards that reward you for having attachments

#### Puresteel Paladin — {W}{W} — Creature — Human Knight — 2/2
"Whenever an Equipment you control enters, you may draw a card. **Metalcraft** — Equipment you control have equip {0} as long as you control three or more artifacts."

Two mana for the best Equipment engine in the deck. Every Equipment you play draws a card, and once you control three artifacts, **all equip costs become free** — you can move gear onto any creature, as many times as you like, for zero mana.

**When to play it:** Turn 2 whenever possible. This card single-handedly fixes the deck's biggest weakness: expensive equip costs — Behemoth Sledge, Pre-War Formalwear and Silver Shroud Costume all cost equip {3}.

**Watch out:** Metalcraft counts **artifacts**, not Equipment — Sol Ring, Arcane Signet, the Bobbleheads, Junk tokens, Treasures, Food, and Mister Gutsy all count. `{W}{W}` is a hard cost on turn 2 with only 16 white sources. And equip is still "activate only as a sorcery" even at {0} — free does not mean instant-speed.

**Rulings:**
- [2020-08-07] *"Once the equip {0} ability is activated, causing Puresteel Paladin to leave the battlefield or causing its controller to control fewer than three artifacts won't stop the equip ability from resolving."*
- [2020-08-07] *"You may still activate the Equipment's other equip abilities if you wish."*

#### Codsworth, Handy Helper — {2}{W} — Legendary Artifact Creature — Robot — 2/3
Three abilities: "Commanders you control have **ward {2}**." `{T}: Add {W}{W}. Spend this mana only to cast Aura and/or Equipment spells.` `{T}: Attach target Aura or Equipment you control to target creature you control. Activate only as a sorcery.`

**Ward** is a triggered ability; rule 702.21a defines it as a template — *"Ward [cost] means 'Whenever this permanent becomes the target of a spell or ability an opponent controls, counter that spell or ability unless that player pays [cost].'"* Here `[cost]` is `{2}`, so an opponent targeting your commander pays {2} extra or their spell is countered. That is a genuine tax on removal aimed at Dogmeat.

The third ability is the deck's rescue button: it **moves an Aura**, which normally cannot be moved at all. Secondary role: it also ramps (for attachments only).

**When to play it:** Turn 3, ideally before Dogmeat, so your commander lands with ward already up.

**Watch out:** The two `{T}` abilities compete — Codsworth taps for one or the other each turn, not both. The mana is Aura/Equipment-spell-only: per the ruling, *"You can't spend mana generated by Codsworth's second ability to activate abilities of Auras or Equipment. This includes paying equip costs."*

**Rulings:**
- [2024-03-08] *"Once a commander's ward ability has triggered, causing that commander to lose ward by removing Codsworth won't affect the ability."*
- [2024-03-08] *"The Aura or Equipment you target with Codsworth's last ability doesn't have to be attached to a creature you control when you target it. You just have to control the Aura or Equipment you're targeting as well as the creature you're targeting."*
- [2024-03-08] *"As Codsworth's last ability resolves, if the target Aura or Equipment can't legally be attached to the target creature… the target Aura or Equipment won't move."*

#### Mister Gutsy — {2} — Artifact Creature — Robot Soldier — 1/1
"Whenever you cast an Aura or Equipment spell, put a +1/+1 counter on this creature. When this creature dies, create X Junk tokens, where X is the number of +1/+1 counters on it. …"

A colorless 1/1 that grows with your whole deck and cashes out into a pile of Junk when it dies. It is also an **artifact**, so it feeds Puresteel Paladin's metalcraft.

**When to play it:** Turn 2 in any hand. Colorless cost means it is always castable, which matters in a three-color deck.

**Watch out:** It grows on **casting** the spell, not on the attachment entering — so Auras and Equipment put onto the battlefield by Vault 101, Mantle of the Ancients, or Brotherhood Outcast do **not** trigger it. And counters make it *modified*, so it also enables Ian the Reckless.

**Rulings:**
- [2024-03-08] *"You pay all costs and follow all normal timing rules for the card played from exile with a Junk token's ability."*
- [2024-03-08] *"Some spells and abilities that create Junk tokens may require targets. If each target chosen is illegal as that spell or ability tries to resolve, it won't resolve and none of its effects happen."*

#### Three Dog, Galaxy News DJ — {1}{R}{W} — Legendary Creature — Human Bard — 1/5
"Whenever you attack, you may pay {2} and sacrifice an Aura attached to Three Dog. When you sacrifice an Aura this way, for each other attacking creature you control, create a token that's a copy of that Aura attached to that creature."

Put one Aura on Three Dog, attack with a team, pay {2}, and every other attacker gets a copy of that Aura. Copy All That Glitters onto four attackers and your whole team explodes in size — and every one of them is now enchanted, so Dogmeat makes four Junk tokens.

**When to play it:** Turn 3 as a defensive 1/5 body; the payoff comes on a turn you attack with three or more creatures.

**Watch out:** You **sacrifice** the original Aura, so this is a one-shot per Aura (though Cass, Hand of Vengeance can bring it back). Copies only go to **other** attacking creatures, not to Three Dog. And the copied Auras are tokens — they cease to exist when the creature dies.

**Rulings:**
- [2024-03-08] *"The tokens copy exactly what was printed on the original Aura and nothing else… It doesn't copy whether that Aura was tapped or untapped, whether it had any counters on it or Auras attached to it."*
- [2024-03-08] *"Any enters-the-battlefield abilities of the copied Aura will trigger when the tokens enter the battlefield."*
- [2024-03-08] *"If one of the Aura tokens being created couldn't legally be attached to the appropriate attacking creature (because of an ability like protection from enchantments), that Aura token won't be created."*
- [2024-03-08] *"Since Three Dog's reflexive triggered ability doesn't target, Aura tokens created by that ability will be attached to attacking creatures you control with shroud."*

#### Moira Brown, Guide Author — {1}{R}{W} — Legendary Creature — Human Citizen — 2/3
"When Moira Brown enters, create a colorless Book Equipment artifact token named **Wasteland Survival Guide** with 'Equipped creature gets +1/+1 for each quest counter among permanents you control' and equip {1}. Whenever you attack, put a quest counter on target nonland permanent you control."

She brings her own Equipment and then feeds it. Every attack adds a quest counter somewhere, and the Book counts **all** quest counters across all your permanents — so they stack up fast alongside Duchess.

**When to play it:** Turn 3. The free Equipment token immediately makes a creature "equipped" for Dogmeat, and equip {1} is cheap.

**Watch out:** The quest counter goes on a **nonland** permanent you control — you can put it on an artifact or enchantment, it does not have to be a creature. The Book is a token: if it leaves the battlefield it is gone for good, and Cass cannot bring it back (Cass returns Aura *cards* and attaches Equipment, but a destroyed token ceases to exist).

*(No official rulings recorded for this card in my data.)*

#### Strong Back — {2}{G} — Enchantment — Aura
"Enchant creature. Equip abilities you activate that target enchanted creature cost {3} less to activate. Aura spells you cast that target enchanted creature cost {3} less to cast. Enchanted creature gets +2/+2 for each Aura and Equipment attached to it."

Three effects in one: a massive discount on everything else you want to put on this creature, plus **+2/+2 per attachment** — the biggest pump multiplier in the deck. Four attachments makes it +8/+8 on top of everything else those attachments do.

**When to play it:** Turn 3, on the creature you have decided is your win condition, *before* you cast the expensive stuff. The discounts turn Behemoth Sledge's equip {3} into equip {0}.

**Watch out:** The discount only reduces **generic** mana. From the ruling: *"Strong Back's abilities reduce only the amount of generic mana in equip abilities that target the enchanted creature and in the total cost of Aura spells that target the enchanted creature. For example, it will reduce the total cost of Animal Friend from {1}{G} to {G}."* — the colored pips stay. Also, Strong Back does not reduce its own cost.

**Rulings:**
- [2024-03-08] *"Strong Back's third ability won't reduce its own cost."*
- [2024-03-08] *"Some Equipment creature cards in other sets have reconfigure… Reconfigure is not an equip ability, and reconfigure costs are not reduced by Strong Back's second ability."*

#### Inventory Management — {R}{W} — Instant
"**Split second** … For each Aura and Equipment you control, you may attach it to a creature you control."

Split second means *"As long as this spell is on the stack, players can't cast spells or activate abilities that aren't mana abilities."* — it is effectively uncounterable and unresponse-able.

This is the deck's emergency button. Opponent casts removal on your loaded-up creature? Respond with Inventory Management and **move every attachment** onto a different creature. The removal resolves and kills a naked body while your five attachments live on somewhere else. It is also the only way in the deck to move Auras at instant speed.

**When to play it:** In response to targeted removal or a "sacrifice a creature" effect. Or proactively, on a turn you want to re-shuffle everything onto one creature for a lethal attack.

**Watch out:** It attaches things to creatures **you control** — you cannot steal. It does not stop a board wipe (all your creatures die anyway). Per rule 704.5m, Auras that end up unattached go to the graveyard, so this must be cast while there is still a legal creature to move onto.

**Rulings:**
- [2024-03-08] *"Split second doesn't stop triggered abilities from triggering."*
- [2024-03-08] *"Casting a spell with split second won't affect spells and abilities that are already on the stack."*
- [2024-03-08] *"You can't try to attach an Aura or Equipment to a creature if that Aura or Equipment can't legally be attached to it."*
- [2024-03-08] *"After a spell with split second resolves (or otherwise leaves the stack), players may again cast spells and activate abilities before the next object on the stack resolves."*

#### Vault 101: Birthday Party — {3}{W} — Enchantment — Saga
- I — Create a 1/1 white Human Soldier creature token **and** a Food token.
- II, III — You may put an Aura or Equipment card from your hand **or graveyard** onto the battlefield. If an Equipment is put onto the battlefield this way, you may attach it to a creature you control.

A four-mana Saga that gives you a body, a Food, and then two free attachments over the next two turns — from your graveyard, which pairs perfectly with Dogmeat's mill-5.

**When to play it:** Turn 4, especially after Dogmeat has milled. Free-casting Mantle of the Ancients or Almost Perfect out of the graveyard is a huge tempo swing.

**Watch out:** Putting an **Aura** onto the battlefield this way — it attaches to whatever it legally can (you choose what it enchants as it enters); an Aura with no legal target cannot be put in. Equipment enters unattached unless you use the "you may attach it" clause. And note these are *put onto the battlefield*, not cast — so Mister Gutsy and Armory Paladin do **not** trigger.

### Recursion — getting your attachments back

Six recursion pieces. This is how the deck fights the 2-for-1 problem: when a creature dies, the Auras on it go to the graveyard, and these cards buy them back.

#### Brotherhood Outcast — {2}{W} — Creature — Human Soldier — 3/2
"When this creature enters, choose one — • Return target Aura or Equipment card with mana value 3 or less from your graveyard **to the battlefield**. • Put a shield counter on target creature. …"

A three-mana 3/2 that either reanimates a cheap attachment directly onto the battlefield (free!) or shields a creature.

**Shield counter** (rule 122.1c): *"One or more shield counters on a permanent create a single replacement effect and a single prevention effect… 'If this permanent would be destroyed as the result of an effect, instead remove a shield counter from it' and 'If damage would be dealt to this permanent, prevent that damage and remove a shield counter from it.'"* One free "no" to a removal spell.

**When to play it:** Turn 3, and read the board. If your key creature is under threat, take the shield counter. If you just lost a creature to a wipe, reanimate an attachment.

**Watch out:** Mana value **3 or less** — it cannot bring back Mantle of the Ancients (MV 5), Almost Perfect (MV 6), or Grim Reaper's Sprint (MV 5). The shield counter is a one-shot and does not stop exile or sacrifice.

#### Cass, Hand of Vengeance — {2}{R}{W} — Legendary Creature — Human Ranger — 4/3
Vigilance. "Whenever Cass or another creature you control dies, if it was enchanted or equipped, return any number of Aura cards that were attached to it from your graveyard to the battlefield attached to target creature, then attach any number of Equipment that were attached to it to that creature."

This is the answer to the deck's central weakness. Normally, killing your enchanted creature costs you five cards. With Cass out, the creature dies and **all its Auras come straight back** onto another creature, and all its Equipment moves over too — for free, automatically.

**When to play it:** Turn 4, before you commit heavily to a single creature. Cass turns your fragile all-in board into something resilient. Her vigilance means she attacks and still blocks.

**Watch out:** It only works on **Aura cards** — Aura *tokens* (Three Dog's copies, Preston's Settlement) cease to exist and cannot return. It also requires that you have another creature to move things onto, so it does not save you from a full board wipe.

**Rulings:**
- [2024-03-08] *"You can't return Aura cards that can't legally be attached to the target creature. For example, if the target creature has protection from red, you can't return Grim Reaper's Sprint to the battlefield with Cass's last ability."*

#### Mantle of the Ancients — {3}{W}{W} — Enchantment — Aura
"Enchant creature you control. When this Aura enters, return **any number** of target Aura and/or Equipment cards from your graveyard to the battlefield attached to enchanted creature. Enchanted creature gets +1/+1 for each Aura and Equipment attached to it."

Five mana for a mass reanimation of every attachment in your graveyard, all landing on one creature — then that creature gets +1/+1 for each of them. This is the deck's single biggest swing card. After a Dogmeat mill and a couple of dead creatures, this can put five attachments into play at once.

**When to play it:** Late, when your graveyard is stocked. Ideally on a creature that already has protection (Champion's Helm, Swiftfoot Boots) or with Heroic Intervention held up — because everything is now on one body.

**Watch out:** It is the ultimate "all eggs in one basket." One removal spell in response to the trigger, or after it resolves, costs you the entire game. Hold up protection or accept the risk knowingly.

**Rulings:**
- [2021-07-23] *"As the enters-the-battlefield ability is resolving, any targets that couldn't be legally attached to the creature enchanted by Mantle of the Ancients stay in your graveyard."*
- [2021-07-23] *"If Mantle of the Ancients becomes attached to a different creature in response to its enters-the-battlefield ability, the creature it's attached to as that ability is resolving is the 'enchanted creature,' even though you used the original enchanted creature to choose targets."*
- [2021-07-23] *"If Mantle of the Ancients leaves the battlefield before its enters-the-battlefield ability resolves, the last permanent it was attached to before leaving the battlefield is the 'enchanted creature.'"*

#### Pre-War Formalwear — {2}{W} — Artifact — Equipment
"When this Equipment enters, return target creature card with mana value 3 or less from your graveyard to the battlefield and attach this Equipment to it. Equipped creature gets +2/+2 and has vigilance. Equip {3}."

Three mana: reanimate a cheap creature *and* it arrives already equipped with a +2/+2 vigilance boost. That is an instant Dogmeat trigger enabler and a free body.

**When to play it:** After you lose a creature. Dogmeat's mill-5 also sometimes puts a creature in the graveyard for it. Great with Cait, Cage Brawler (MV 2), Gunner Conscript (MV 2), Puresteel Paladin (MV 2), or Mister Gutsy (MV 2).

**Watch out:** Mana value **3 or less** — it cannot return Cass (MV 4), Super Mutant Scavenger (MV 5), or Preston Garvey (MV 5). Equip {3} is expensive if you ever want to move it (Strong Back or Puresteel Paladin fix this).

### Pump attachments — the raw stat boosts

#### All That Glitters — {1}{W} — Enchantment — Aura
"Enchant creature. Enchanted creature gets +1/+1 for each artifact and/or enchantment you control."

Two mana. The deck contains 19 artifacts and 17 enchantments before you count a single token, and Junk, Treasure and Food tokens are all artifacts too — so this is routinely +4/+4 to +8/+8.

**When to play it:** Turn 2 onward on your best creature — preferably one with trample or evasion so the size converts to damage.

**Watch out:** It counts **artifacts and enchantments you control**, not attachments — every land Aura, Junk token, and mana rock counts. A permanent that is both artifact and enchantment counts only once.

**Rulings:**
- [2019-10-04] *"A permanent that's both an artifact and an enchantment is counted only once."*
- [2019-10-04] *"Because All That Glitters is an enchantment, the enchanted creature usually gets at least +1/+1."*
- [2019-10-04] *"You still control Auras that you put onto the battlefield attached to a permanent you don't control."*

#### Rancor — {G} — Enchantment — Aura
"Enchant creature. Enchanted creature gets +2/+0 and has trample. When this Aura is put into a graveyard from the battlefield, return it to its owner's hand."

One mana for +2/+0 and trample — and it is the only attachment in the deck that **comes back to your hand** when the creature dies. That makes it the safest Aura here.

**When to play it:** Turn 1 or 2, on anything. Never a wasted card, because you always get it back. Trample is the keyword this deck most needs.

**Watch out:** It returns to your **hand**, not the battlefield — you must pay {G} again each time. Its return trigger only fires when Rancor goes to the **graveyard from the battlefield**, so if Rancor itself is exiled you lose it for good. And +2/+0 alone does not get past a big blocker; the trample is what makes it work.

**Rulings:**
- [2018-03-16] *"If the creature this Aura would enchant is an illegal target by the time Rancor tries to resolve, the Aura spell doesn't resolve. It won't enter the battlefield, so it won't be put into a graveyard from the battlefield and its ability won't trigger."*

#### Idolized — {1}{W} — Enchantment — Aura
"Enchant creature. Enchanted creature has 'Whenever this creature attacks alone, it gets +X/+X until end of turn, where X is the number of nonland permanents you control.'"

Attack with **one** creature and it gets enormous — every artifact, enchantment, creature, Junk token and Treasure you control adds +1/+1.

**When to play it:** Turn 2–3 as a cheap enabler, but its big turn comes late, when you have a wide board of nonland permanents and can afford to send exactly one attacker.

**Watch out:** "Attacks alone" is strict. Per the official ruling: *"A creature attacks alone if it's the only creature declared as an attacker during the declare attackers step… the ability granted by Idolized won't trigger if you attack with multiple creatures and all but one of them are removed from combat."* Attacking alone directly fights Dogmeat's "make a Junk for each enchanted attacker" plan — pick one line or the other.

**Rulings:**
- [2024-03-08] *"A creature attacks alone if it's the only creature declared as an attacker during the declare attackers step (including creatures controlled by your teammates, if applicable)."*

#### Almost Perfect — {4}{G}{W} — Enchantment — Aura
"Enchant creature. Enchanted creature has base power and toughness 9/10 and has indestructible."

Six mana that turns anything — a 1/1 Squirrel token, Cait, a Junk-fed token — into an indestructible 9/10. Secondary role: this is genuinely a protection card, since indestructible stops all "destroy" effects and combat damage.

**When to play it:** Turn 6+, on a creature that has evasion (menace from Sticky Fingers, unblockable from Silver Shroud Costume) or trample.

**Watch out:** It **sets base** power and toughness, overwriting the creature's printed stats — putting it on an already-huge creature can make it *smaller*. Per the ruling: *"Almost Perfect overwrites all previous effects that set the creature's base power and toughness to specific values."* But other effects still apply: *"Effects that modify a creature's power and/or toughness… will apply to the creature no matter when they started to take effect."* Indestructible does not stop exile, bounce, or sacrifice effects. Six mana is a lot in a deck with an average non-land mana value of 2.82.

**Rulings:**
- [2024-03-08] *"Almost Perfect overwrites all previous effects that set the creature's base power and toughness to specific values. Any power- or toughness-setting effects that start to apply after the ability resolves will overwrite this effect."*
- [2024-03-08] *"Effects that modify a creature's power and/or toughness, such as the effect of the ability granted by Idolized, will apply to the creature no matter when they started to take effect."*

#### Behemoth Sledge — {1}{G}{W} — Artifact — Equipment
"Equipped creature gets +2/+2 and has trample and lifelink. Equip {3}."

Lifelink means damage dealt also gains you that much life (rule 702.15). +2/+2, trample, and lifelink on one card is a strong package — the lifelink in particular buys you turns at a four-player table.

**When to play it:** Turn 3 to deploy, then equip when you can afford {3} — or for free under Puresteel Paladin's metalcraft, or for {0} with Strong Back on the target.

**Watch out:** Equip {3} is the joint-highest equip cost in the deck (shared with Pre-War Formalwear and Silver Shroud Costume). Deploying it and equipping it in the same turn costs six mana. Plan around Puresteel Paladin or Strong Back.

#### Bloodforged Battle-Axe — {1} — Artifact — Equipment
"Equipped creature gets +2/+0. Whenever equipped creature deals combat damage to a player, create a token that's a copy of this Equipment. Equip {2}."

One mana, +2/+0, and it **duplicates itself** every time the creature connects. Two copies next turn, four the turn after (if you equip them all). It also snowballs your artifact count for metalcraft and All That Glitters.

**When to play it:** Turn 1. Get it onto an evasive creature as early as possible and let it multiply.

**Watch out:** Per the ruling, *"The token enters the battlefield unattached"* — you must pay equip {2} for each copy (or {0} under Puresteel Paladin). It requires damage **to a player**, so being blocked stops the copying.

**Rulings:**
- [2017-08-25] *"The token has all three of Bloodforged Battle-Axe's abilities, including the one that creates more tokens."*
- [2017-08-25] *"The token enters the battlefield unattached."*

#### Brass Knuckles — {4} — Artifact — Equipment
"When you cast this spell, copy it. (The copy becomes a token.) Equipped creature has double strike as long as two or more Equipment are attached to it. Equip {1}. …"

Four mana gets you **two** Brass Knuckles, and two Equipment on the same creature is exactly the condition for double strike — so one card gives a creature double strike for {4} plus two {1} equips.

**When to play it:** Turn 4 onwards, on your main attacker. Doubling combat damage on a creature loaded with Strong Back or All That Glitters is often lethal.

**Watch out:** The double strike needs **two or more Equipment attached to that creature** — the two Brass Knuckles satisfy this, but if you move one away the double strike turns off. Also, from the ruling: *"Multiple instances of double strike do not increase the number of strikes."* Brass Knuckles plus Fireshrieker is redundant.

**Rulings:**
- [2022-04-29] *"A copy of a permanent spell enters the battlefield as a token. This is not the same as an effect that creates a token, and any effect that refers to creating a token does not apply to copies of permanent spells."*
- [2022-04-29] *"Multiple instances of double strike do not increase the number of strikes. That creature still only gets to deal combat damage twice."*

#### Fireshrieker — {3} — Artifact — Equipment
"Equipped creature has double strike. … Equip {2}. …"

Straight double strike, no conditions. Every +X/+X you have piled on gets counted twice.

**When to play it:** On the creature carrying Strong Back / All That Glitters / Mantle of the Ancients. Double strike is the highest-leverage keyword in a deck built on stacking pump.

**Watch out:** Five mana to cast and equip in one turn. Redundant with Brass Knuckles on the same creature (multiple double strikes do not stack). Double strike does nothing if the creature cannot get through — pair with trample or evasion.

#### Basilisk Collar — {1} — Artifact — Equipment
"Equipped creature has deathtouch and lifelink. … Equip {2}. …"

Deathtouch: any amount of damage it deals to a creature destroys that creature (rule 702.2). Lifelink: damage dealt gains you that much life (rule 702.15).

Cheap, and it makes even a 1/1 a creature nobody wants to block — which is a form of evasion. On a trampler, deathtouch is brutal: you only need to assign 1 damage to each blocker, and the rest tramples over.

**When to play it:** Turn 1–2 for the cheap deploy; equip it to whichever creature is attacking into a board of big blockers.

**Watch out:** It gives no stats at all — a 1/1 with Basilisk Collar is still a 1/1 that dies to any blocker with 1 power. It is a deterrent and a trample-enabler, not a threat by itself.

#### Masterwork of Ingenuity — {1} — Artifact — Equipment
"You may have this Equipment enter as a copy of any Equipment on the battlefield."

One mana: become a second copy of the best Equipment in play — **anyone's**, including your opponents'. Copy Behemoth Sledge, Champion's Helm, or an opponent's expensive gear.

**When to play it:** After the best Equipment is already on the battlefield. Holding it one extra turn is usually right.

**Watch out:** If there is no Equipment on the battlefield, it enters as a vanilla Equipment with no abilities and no equip cost — a dead card. Per the ruling: *"Masterwork of Ingenuity enters the battlefield unattached. It doesn't enter attached to the same creature as the Equipment it copies."* You still pay the copied Equipment's equip cost.

**Rulings:**
- [2020-08-07] *"Masterwork of Ingenuity enters the battlefield unattached. It doesn't enter attached to the same creature as the Equipment it copies."*

#### Explorer's Scope — {1} — Artifact — Equipment
"Whenever equipped creature attacks, look at the top card of your library. If it's a land card, you may put it onto the battlefield tapped. Equip {1}. …"

Two mana total (cast plus equip) makes a creature *equipped* — which is the cheapest way in the deck to switch on Dogmeat's Junk trigger — and it occasionally puts a free land into play.

**When to play it:** Turn 1–2. Its main job is being a cheap "equipped" enabler; the free lands are a bonus.

**Watch out:** With 38 lands in a 100-card deck, this hits roughly a third of the time. The land enters **tapped**, and it does not draw you the card — a non-land stays on top. This is a support card, not an engine.

#### Acquired Mutation — {2}{R} — Enchantment — Aura
"Enchant creature. Enchanted creature gets +2/+2 and is **goaded**. … Whenever enchanted creature attacks, defending player gets two rad counters."

**Goad** (`mtg glossary Goad`, rule 701.15) forces a creature to attack each combat if able, and — per rule 701.15b — to attack *"a player other than the controller of the permanent, spell, or ability that caused it to be goaded"* if able. Since you are the one goading here, that means anyone but you; the card's own reminder text says exactly that: *"(It attacks each combat if able and attacks a player other than you if able.)"* So this is a **political card**: put it on an *opponent's* biggest creature, and it must attack one of your other opponents every turn, taking rad counters along for the ride.

**When to play it:** On an opposing threat, not your own creature. Aim it at the player who is building the scariest board so they are forced to fight someone else.

**Watch out:** This is the one Aura in the deck you deliberately put on someone else's creature — but note you keep controlling the Aura (see the All That Glitters ruling: *"You still control Auras that you put onto the battlefield attached to a permanent you don't control"*), so it still counts for All That Glitters. Also, the +2/+2 makes their creature **bigger** — do not goad something that can kill you anyway. Per the rulings, a goaded creature that is tapped, or that cannot attack, simply does not attack; and attacking does not clear the goad.

**Rulings:**
- [2024-03-08] *"Being goaded isn't an ability the creature has. Once it's been goaded, it must attack as detailed above even if it loses all abilities."*
- [2024-03-08] *"If the creature doesn't meet any of the above exceptions and can attack, it must attack a player other than the controller of the spell or ability that goaded it if able."*
- [2024-03-08] *"Attacking with a goaded creature doesn't cause it to stop being goaded."*

#### Animal Friend — {1}{G} — Enchantment — Aura
"Enchant creature. Enchanted creature has 'Whenever this creature attacks, create a 1/1 green Squirrel creature token. Put a +1/+1 counter on that token for each Aura and Equipment attached to this creature other than Animal Friend.'"

Every attack makes a Squirrel sized to match how loaded the enchanted creature is. On a creature with four other attachments, each attack makes a 5/5.

**When to play it:** Turn 2 on your intended main carrier. The Squirrels give you extra bodies — which matter, because this deck has only 18 maindeck creatures (19 counting Dogmeat).

**Watch out:** The Squirrels enter **after** attackers are declared, so they are not attacking and cannot be blocked or block that turn. They also arrive without attachments, so they do not trigger Dogmeat unless you dress them up later. Note Strong Back reduces this to just `{G}` if it targets the enchanted creature.

#### Sticky Fingers — {R} — Enchantment — Aura
"Enchant creature. Enchanted creature has menace and 'Whenever this creature deals combat damage to a player, create a Treasure token.' … When enchanted creature dies, draw a card."

One mana for evasion (menace: can't be blocked except by two or more creatures), a ramp trigger, and a built-in consolation card when the creature dies.

**When to play it:** Turn 1 or 2. It is the cheapest evasion in the deck, and evasion is what converts a stacked creature into damage.

**Watch out:** Menace is not unblockable — two small creatures still stop it. The card draw only fires when the enchanted creature **dies**, not when it is exiled or bounced.

#### Squirrel Nest — {1}{G}{G} — Enchantment — Aura
"Enchant land. Enchanted land has '{T}: Create a 1/1 green Squirrel creature token.'"

Three mana that turns a land into a Squirrel factory: one free 1/1 every turn, forever. With only 18 maindeck creatures (19 counting Dogmeat), this is a steady supply of bodies to hang Auras and Equipment on.

**When to play it:** Turn 3 on a land you can afford to stop tapping for mana, or on a land you would otherwise not use. Enchanting a land also makes that land an "enchanted permanent" for Preston Garvey's untap trigger — meaning with Preston attacking you can make a Squirrel *and* still use the land for mana.

**Watch out:** The land is now competing with itself — a turn spent making a Squirrel is a turn that land makes no mana. Do not put it on your only white source. And do not put it on a land you might want to sacrifice (Evolving Wilds, Terramorphic Expanse, Buried Ruin) — the Aura goes to the graveyard.

---

## Utility & Protection

Only four cards whose primary job is keeping your investment alive. Given that this deck routinely stacks 3–5 cards onto one creature, these are more important than their count suggests.

#### Swiftfoot Boots — {2} — Artifact — Equipment
"Equipped creature has hexproof and haste. … Equip {1}. …"

Hexproof means opponents cannot **target** it — no targeted removal, no targeted "sacrifice", no auras or theft effects from them (rule 702.11). Haste lets it attack the turn it arrives.

**When to play it:** Turn 2, and equip it to Dogmeat or to whatever creature you are about to load up. Equipping this *before* you commit Auras is the correct sequencing.

**Watch out:** Hexproof does **not** stop board wipes or "each player sacrifices a creature" effects — those do not target. And a critical interaction: hexproof stops **your opponents** from targeting it, but not you. However, Codsworth's attach ability targets a creature *you* control, so it still works fine.

#### Champion's Helm — {3} — Artifact — Equipment
"Equipped creature gets +2/+2. As long as equipped creature is legendary, it has hexproof. … Equip {1}."

+2/+2 always; hexproof only on a legendary creature. This deck runs 11 legendary creatures in total — Dogmeat plus Cait, Ian the Reckless, Codsworth, Moira Brown, Three Dog, Veronica, Cass, Commander Sofia Daguerre, Duchess and Preston Garvey — so the hexproof is live more often than not.

**When to play it:** Turn 3, then equip to Dogmeat for {1}. Dogmeat with Champion's Helm is a hexproof 5/5 — a night-and-day upgrade over a naked 3/3.

**Watch out:** On a **nonlegendary** creature (Gunner Conscript, Crimson Caravaneer, a Squirrel token) it is just +2/+2 with no protection. Also remember the legend rule (rule 704.5j): *"If two or more legendary permanents with the same name are controlled by the same player, that player chooses one of them, and the rest are put into their owners' graveyards."* — you can never have two Dogmeats.

#### Silver Shroud Costume — {2} — Artifact — Equipment
"**Flash.** When this Equipment enters, attach it to target creature you control. That creature gains **shroud** until end of turn. … Equipped creature can't be blocked. Equip {3}."

Three things: it can be cast at instant speed (flash), it attaches **itself for free** on entry, it grants shroud for a turn (*"precludes a permanent or player from being targeted"* — rule 702.18, and unlike hexproof this stops **you** targeting it too), and permanently makes the creature **unblockable**.

**When to play it:** Two ways. (1) Offensively — get it attached **before blockers are declared** (your precombat main phase, or flashed in during the declare-attackers step) so your attacker is unblockable. (2) Defensively — flash it in response to a targeted removal spell; the shroud makes that spell lose its only legal target and do nothing.

**Watch out:** Per the official ruling: *"Attaching Silver Shroud Costume to a creature that has already been blocked won't cause it to become unblocked."* You must have it attached before blockers are declared. And shroud cuts both ways — while it lasts, **you** cannot target that creature either (no equipping other gear onto it, no Aura spells at it).

**Rulings:**
- [2024-03-08] *"Attaching Silver Shroud Costume to a creature that has already been blocked won't cause it to become unblocked."*

> **Note on protection generally:** this deck has **no counterspells** and only two hexproof sources (Swiftfoot Boots, Champion's Helm) plus Heroic Intervention and Valorous Stance. Play accordingly: sequence protection *before* threats, not after.

---

## Lands — 38 total

`mtg deck stats dogmeat -v` reports 38 lands, of which **12 can enter tapped** (7 always, 5 conditionally) and **7 produce only colorless mana**. Color sources: White 16, Red 16, Green 18. That is a genuinely tight mana base for a `{R}{G}{W}` commander — sequencing your lands matters.

### Basic lands — 12 total

#### 4 Forest · 4 Mountain · 4 Plains — Basic Land
Forest taps for `{G}`, Mountain for `{R}`, Plains for `{W}` (rule 305.6: an object with a basic land type has the intrinsic ability "{T}: Add [that colour]"). They always enter untapped and can never be countered or made to enter tapped by their own text.

**When to play it:** Early, and pay attention to which one. Several of your dual lands check whether you control a Mountain, Forest, or Plains — playing the right basic on turn 1 makes your turn-2 land enter untapped.

**Watch out:** Only 12 basics in 38 lands. Canopy Vista and Cinder Glade specifically need **two or more basic lands** to enter untapped, and with only 12 basics that condition fails more often than you would like. Also, Evolving Wilds and Terramorphic Expanse can only fetch basics — so do not be too eager to play them all out.

### Any-color and three-color lands

#### Command Tower — (no mana cost) — Land
"{T}: Add one mana of any color in your commander's color identity." For you that means red, green, or white, untapped, no drawback. The best land in the deck.

**When to play it:** Any time. There is no reason not to.

**Watch out:** None worth mentioning — it makes only the three colors of your commander's identity (rule 903.4), never blue or black, but this deck has no blue or black cards.

#### Exotic Orchard — (no mana cost) — Land
"{T}: Add one mana of any color that a land an opponent controls could produce."

**When to play it:** Play it and see what your opponents are running. In a typical multi-color pod it usually makes whatever you need.

**Watch out:** If every opponent is playing a mono-blue and a mono-black deck, this makes mana you cannot use. From the rulings: *"The colors of mana are white, blue, black, red, and green. Exotic Orchard can't be tapped for colorless mana, even if a land an opponent controls could produce colorless mana."* — so against an all-colorless board this land makes **nothing**.

**Rulings:**
- [2009-02-01] *"Exotic Orchard checks the effects of all mana-producing abilities of lands your opponents control, but it doesn't check their costs."* — an opponent's Vivid Crag lets you tap for any color regardless of whether it is tapped or has counters.
- [2009-02-01] *"Exotic Orchard doesn't care about any restrictions or riders your opponents' lands … put on the mana they produce. It just cares about colors of mana."*

#### Path of Ancestry — (no mana cost) — Land
"This land enters tapped. {T}: Add one mana of any color in your commander's color identity. When that mana is spent to cast a creature spell that shares a creature type with your commander, scry 1. …" (Scry 1: look at the top card of your library and you may put it on the bottom — rule 701.22.)

**When to play it:** On a turn where entering tapped costs you nothing — ideally turn 1, or a turn you already have enough mana.

**Watch out:** Dogmeat is a **Dog**. There are no other Dogs in the deck (the 18 maindeck creatures are Human Warrior ×2, Human Mercenary, Robot Soldier, Human Knight ×2, Human Soldier ×2, Robot, Human Scout, Human Citizen ×2, Human Bard, Human Artificer Rogue, Human Ranger ×2, Human Pilot, Mutant Warrior — no Dogs). So the scry only ever happens when you use this mana to **recast Dogmeat himself**. Treat it as an enters-tapped Command Tower.

#### Jungle Shrine — (no mana cost) — Land
"This land enters tapped. {T}: Add {R}, {G}, or {W}."

**When to play it:** Turn 1, or any turn where you can afford the tempo loss. It fixes all three colors perfectly.

**Watch out:** It **always** enters tapped, no exceptions. Playing this on the turn you want to cast Dogmeat is how you miss your curve.

### Dual lands that can enter untapped

#### Clifftop Retreat — (no mana cost) — Land
"This land enters tapped unless you control a Mountain or a Plains. {T}: Add {R} or {W}."

**When to play it:** After a Mountain or Plains. Note this checks the **land type**, not just basics — Cinder Glade and Sheltered Thicket are Mountain Forests, and Canopy Vista and Scattered Groves are Forest Plains, so any of those also turn it on.

**Watch out:** Turn 1, with nothing in play, it enters tapped.

#### Rootbound Crag — (no mana cost) — Land
"This land enters tapped unless you control a Mountain or a Forest. {T}: Add {R} or {G}."

**When to play it:** After a Mountain, Forest, Cinder Glade, or Sheltered Thicket.

**Watch out:** Same as Clifftop Retreat — do not lead on it.

#### Sunpetal Grove — (no mana cost) — Land
"This land enters tapped unless you control a Forest or a Plains. {T}: Add {G} or {W}."

**When to play it:** After a Forest, Plains, Canopy Vista, or Scattered Groves.

**Watch out:** Same trap as above.

#### Canopy Vista — (no mana cost) — Land — Forest Plains
"({T}: Add {G} or {W}.) This land enters tapped unless you control **two or more basic lands**."

Because its type line is *Forest Plains*, it counts as a Forest **and** a Plains for every "do you control a Mountain/Forest/Plains" check.

**When to play it:** Once you have two basics out. With only 12 basics in the deck, that is often turn 3 or later.

**Watch out:** It checks **basic** lands specifically — other dual lands do not count toward its own condition.

#### Cinder Glade — (no mana cost) — Land — Mountain Forest
"({T}: Add {R} or {G}.) This land enters tapped unless you control two or more basic lands." Counts as a Mountain and a Forest.

**When to play it:** Same as Canopy Vista — hold it until two basics are down, if you can.

**Watch out:** Same basic-land condition.

### Lands that always enter tapped

#### Scattered Groves — (no mana cost) — Land — Forest Plains
"({T}: Add {G} or {W}.) This land enters tapped. **Cycling {2}** ({2}, Discard this card: Draw a card.)"

Cycling lets you throw it away for a fresh card when you are flooded — very relevant in a deck running 2 lands above the recommended count.

**When to play it:** Early if you need the fixing; cycle it late when you have 6+ lands.

**Watch out:** Cycling is discarding, which triggers Veronica's Junk maker — a nice bonus. But it is discarding a **land**, and Veronica's Junk trigger requires a **nonland** card. So cycling a land does not make Junk.

#### Sheltered Thicket — (no mana cost) — Land — Mountain Forest
"({T}: Add {R} or {G}.) This land enters tapped. Cycling {2} …" Counts as a Mountain and a Forest.

**When to play it:** Same logic as Scattered Groves.

**Watch out:** Same — always tapped, and cycling costs 2 mana.

#### Temple of Abandon — (no mana cost) — Land
"This land enters tapped. When this land enters, scry 1. … {T}: Add {R} or {G}."

**When to play it:** Turn 1 whenever you have it. The scry smooths your next draw and the tapped-ness costs nothing on turn 1.

**Watch out:** Playing any Temple on turn 3 while trying to cast Dogmeat is a wasted turn.

#### Temple of Plenty — (no mana cost) — Land
"This land enters tapped. When this land enters, scry 1. … {T}: Add {G} or {W}."

**When to play it:** Turn 1, same as the other Temples.

**Watch out:** Same.

#### Temple of Triumph — (no mana cost) — Land
"This land enters tapped. When this land enters, scry 1. … {T}: Add {R} or {W}."

**When to play it:** Turn 1.

**Watch out:** Three Temples, plus Jungle Shrine and Path of Ancestry, is five always-tapped lands. Drawing two in one opening hand is a real speed problem — front-load them.

### Filter and utility lands

#### Mossfire Valley — (no mana cost) — Land
"{1}, {T}: Add {R}{G}."

Enters untapped and turns one mana into two colored mana of specific colors. Net mana neutral, but it fixes.

**When to play it:** Any time; it is untapped, so it never costs you tempo. It shines when you have a colorless source (Sol Ring, Temple of the False God) whose mana you need to convert into colors.

**Watch out:** It cannot be your *only* land — you need a spare mana to activate it, so it makes zero mana on turn 1.

#### Sungrass Prairie — (no mana cost) — Land
"{1}, {T}: Add {G}{W}."

**When to play it:** Same as Mossfire Valley. Excellent with Sol Ring: tap Sol Ring for `{C}{C}`, feed one into this, and now you have `{C}{G}{W}`.

**Watch out:** Same — needs another mana source first.

#### Sunscorched Divide — (no mana cost) — Land
"{1}, {T}: Add {R}{W}."

**When to play it:** Same as the two above. These three "filter lands" are how a Sol Ring turns into Dogmeat mana.

**Watch out:** Same. Three filter lands in one hand is a functional mulligan.

#### Temple of the False God — (no mana cost) — Land
"{T}: Add {C}{C}. Activate only if you control five or more lands."

**When to play it:** Only once you already have four other lands in play. Then it is a free extra mana every turn.

**Watch out:** **This is the single most dangerous card in the mana base.** Until you control five lands, it produces **nothing at all** — it is a blank. Never count it as a land when deciding whether to keep an opening hand, and never lead on it. Also, the mana is colorless: it can never help cast Dogmeat's `{R}{G}{W}`.

#### Ash Barrens — (no mana cost) — Land
"{T}: Add {C}. **Basic landcycling {1}** ({1}, Discard this card: Search your library for a basic land card, reveal it, put it into your hand, then shuffle.)"

A flexible card: either a colorless land now, or one mana to turn it into the exact basic you are missing.

**When to play it:** If your colors are fine, play it as a land. If you are missing a color, landcycle it for the basic you need — note the basic goes to your **hand**, so you still have to play it as your land for the turn.

**Watch out:** Landcycling does not put the land into play, and it uses up your land drop. Untapped colorless is fine mid-game and terrible when you need `{W}` for Puresteel Paladin.

#### Evolving Wilds — (no mana cost) — Land
"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle."

Fixes one color, but always at the cost of the land entering **tapped**.

**When to play it:** Turn 1, then crack it immediately so the tapped basic costs you nothing.

**Watch out:** It only finds **basics** — you have exactly 12. It also does not produce mana itself; playing it on the turn you need mana costs you a full land drop. Do not enchant it with Wild Growth or Squirrel Nest.

#### Terramorphic Expanse — (no mana cost) — Land
"{T}, Sacrifice this land: Search your library for a basic land card, put it onto the battlefield tapped, then shuffle." Functionally identical to Evolving Wilds.

**When to play it:** Turn 1, crack immediately.

**Watch out:** Same as Evolving Wilds. Note that both of these thin your basics, which makes Canopy Vista and Cinder Glade *worse*.

#### Buried Ruin — (no mana cost) — Land
"{T}: Add {C}. {2}, {T}, Sacrifice this land: Return target artifact card from your graveyard to your hand."

A colorless land that later rebuys a dead Equipment. Secondary role: recursion.

**When to play it:** As a land early; save the ability for when a key Equipment has been destroyed. Remember Equipment are artifacts, so this reclaims Behemoth Sledge, Champion's Helm, Bloodforged Battle-Axe, etc.

**Watch out:** It returns the artifact to your **hand**, not the battlefield, and costs you a land plus {2}. Also colorless-only mana.

#### Roadside Reliquary — (no mana cost) — Land
"{T}: Add {C}. {2}, {T}, Sacrifice this land: Draw a card if you control an artifact. Draw a card if you control an enchantment."

In this deck, with 19 artifacts and 17 enchantments in the 99-card maindeck, you will very often control both — so this is "sacrifice a land, {2}: draw two."

**When to play it:** Late, when you are flooded (a real risk at 38 lands) and holding both an artifact and an enchantment. This is one of the deck's best flood outlets.

**Watch out:** Two separate checks — one artifact and one enchantment gets you two cards; two artifacts and no enchantment gets you only one. Colorless-only mana in the meantime.

#### Rogue's Passage — (no mana cost) — Land
"{T}: Add {C}. {4}, {T}: Target creature can't be blocked this turn."

The unblockable button. Point it at the creature carrying all your attachments and the damage goes through, guaranteed.

**When to play it:** Any time as a land; activate it in your precombat main phase on the turn you want to close a game or land a big commander-damage hit (rule 903.10a: *"A player who's been dealt 21 or more combat damage by the same commander over the course of the game loses the game."*).

**Watch out:** {4} plus the tap is expensive — five mana's worth of a turn. It only makes colorless mana otherwise. And unblockable does not stop removal or damage prevention.

#### Scavenger Grounds — (no mana cost) — Land — Desert
"{T}: Add {C}. {2}, {T}, Sacrifice a Desert: Exile all graveyards."

Graveyard hate. It answers opposing reanimator decks and recursive threats.

**When to play it:** Only when an opponent's graveyard is actively winning them the game.

**Watch out:** **This exiles YOUR graveyard too** — and your graveyard is a resource in this deck (Dogmeat's return, Cass, Mantle of the Ancients, Brotherhood Outcast, Vault 101, Super Mutant Scavenger all feed on it). Using this at the wrong moment can cost you more than your opponents. It is the only Desert in the deck, so it must sacrifice itself.

**Rulings:**
- [2017-07-14] *"The sacrificed Desert will be in your graveyard to be exiled by the last ability of Scavenger Grounds."*

#### Junktown — (no mana cost) — Land
"{T}: Add {C}. {4}{R}, {T}, Sacrifice this land: Create three Junk tokens. …"

A colorless land that converts into three Junk tokens late — three cards' worth of impulse draw, plus three artifacts for metalcraft and All That Glitters.

**When to play it:** Late, when you are flooded and have five spare mana. This is a genuine flood outlet in a deck that runs 2 lands above the recommended count.

**Watch out:** Five mana **and** a land is a heavy price. Remember the Junk timing ruling — each token exiles a card that you must play *that turn*, and lands from Junk still cost you your land drop.

---

## Completeness check

All 91 unique card names in `mtg deck dogmeat --json` (100 cards including 4 Forest, 4 Mountain, 4 Plains) appear in this file exactly once. Basic lands share a single grouped entry, as intended.

---

## Quick cross-references

- **The 5 cards that make this deck function:** Puresteel Paladin (free equips), Strong Back (+2/+2 per attachment plus {3} discounts), All That Glitters (+1/+1 per artifact/enchantment), Cass Hand of Vengeance (Aura insurance), Mantle of the Ancients (mass attachment reanimation).
- **The 3 cards that save you from disaster:** Heroic Intervention, Inventory Management, Silver Shroud Costume.
- **The 2 cards that end games:** Grim Reaper's Sprint (extra combat), Junk Jet (double power).
- **The 3 lands to be careful with:** Temple of the False God (dead until 5 lands), Scavenger Grounds (exiles your own graveyard), Path of Ancestry (always tapped, scry almost never triggers).
- Full deck stats: `./bin/mtg deck stats dogmeat -v` · Bracket: `./bin/mtg deck bracket dogmeat` (estimated **Bracket 2 — Core**, 0 Game Changers).
