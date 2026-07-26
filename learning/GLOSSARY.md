# MTG Brain — Working Glossary

A beginner's working set for **Commander (EDH)** — the only format this system covers.
Not a rules dump. These are the terms you will actually hit in your first ten games with
**Counter Blitz (tidus)**, **Peace Offering (bumbleflower)**, and **Scrappy Survivors (dogmeat)**.

**Every rule number in this file was retrieved from the local database** with `mtg glossary`
or `mtg rule` — none written from memory. Quoted "Official" text is the Comprehensive Rules
glossary or rule text as returned by the CLI (rules as of **2026-06-19**, per `mtg status`).
Where a term is player slang with no official entry, it says so plainly instead of inventing
a citation.

Run any command below from `/Users/omaralatas/Work/personal/mtg-brain`.

---

## Read this first — the 8 terms that unlock everything else

If you only learn eight things before your first game, learn these. Everything else in this
file hangs off them.

1. **[The stack](#the-stack)** — spells don't just happen; they queue up and resolve one at a time, last one first.
2. **[Priority](#priority)** — the invisible turn-taking system that decides who may act right now.
3. **[Instant speed vs. sorcery speed](#instant-speed-vs-sorcery-speed)** — *when* you're allowed to do a thing.
4. **[Mana value](#mana-value)** — the single number that describes what a card costs.
5. **[The zones](#zones-where-cards-live)** — the seven places a card can be: library, hand, battlefield, graveyard, stack, exile, command zone.
6. **[Triggered vs. activated vs. static abilities](#triggered-ability)** — the three ways a card *does* something.
7. **[State-based actions](#state-based-actions)** — the game's automatic janitor: dead creatures, lost games, the legend rule.
8. **[Counter (cancel) vs. counter (marker)](#counter--the-beginner-trap)** — one word, two totally unrelated meanings. This one *will* confuse you.

---

## Turn structure

Your turn is always the same five phases in the same order. You never skip one.

### Turn (the five phases)
**In plain English:** Every turn runs: beginning → precombat main → combat → postcombat main → ending. You untap, you draw, you play stuff, you attack, you play more stuff, you discard down to seven.
**Official:** "A turn consists of five phases, in this order: beginning, precombat main, combat, postcombat main, and ending. Each of these phases takes place every turn, even if nothing happens during the phase. The beginning, combat, and ending phases are further broken down into steps, which proceed in order."
**Rule:** CR 500.1 — run `mtg rule 500.1` for the full text
**Why it matters in your decks:** Tidus's first ability says "At the beginning of combat on your turn" — that is a specific step, *before* you declare attackers, so you move the counter first and *then* decide who swings.

### Untap step
**In plain English:** The first thing that happens on your turn. All your tapped permanents straighten back up. Nobody can respond during this step.
**Official:** "Part of the turn. This step is the first step of the beginning phase. See rule 502, 'Untap Step.'"
**Rule:** CR 502 — run `mtg rule 502`
**Why it matters in your decks:** Your lands and your **Sol Ring** (`{T}: Add {C}{C}` — in all three decks' ramp list) untap here. This is why you can safely tap out on your turn but should think twice about tapping out on someone else's.

### Upkeep step
**In plain English:** A brief pause right after untapping, before you draw. "At the beginning of your upkeep" triggers go off here.
**Official:** "Part of the turn. This step is the second step of the beginning phase. See rule 503, 'Upkeep Step.'"
**Rule:** CR 503 — run `mtg rule 503`
**Why it matters in your decks:** It's the earliest window in your turn where anyone can act, so it's a common moment for opponents to respond to your board before you get to do anything.

### Draw step
**In plain English:** You draw one card. In a multiplayer Commander game the player who goes first **still draws** on turn one — the "first player skips their draw" rule only applies to two-player games.
**Official:** "Part of the turn. This step is the third and final step of the beginning phase. See rule 504, 'Draw Step.'" And CR 103.8c: "In all other multiplayer games, no player skips the draw step of their first turn." (CR 800.7 says the same: "In a multiplayer game other than a Two-Headed Giant game, the starting player doesn't skip the draw step of their first turn.")
**Rule:** CR 504, CR 103.8c, CR 800.7 — run `mtg rule 103.8`
**Why it matters in your decks:** **Hoofprints of the Stag** (bumbleflower) reads "Whenever you draw a card, you may put a hoofprint counter on this enchantment" — your normal draw-step draw counts.

### Main phase
**In plain English:** Where you play lands, cast creatures, and cast sorceries. You get two of them: one before combat, one after.
**Official:** "Part of the turn. The first, or precombat, main phase is the second phase of the turn. The second, or postcombat, main phase is the fourth phase of the turn. See rule 505, 'Main Phase.'"
**Rule:** CR 505 — run `mtg rule 505`
**Why it matters in your decks:** Standard beginner habit worth building: cast **combat tricks and creatures that want to attack** in the *precombat* main, and hold everything else for the *postcombat* main so you keep mana up during combat.

### Playing a land
**In plain English:** One land per turn, on your own turn, in a main phase, with nothing waiting on the stack. It is not a spell — nobody can respond to it.
**Official:** "Playing a land is a special action. To play a land, a player puts that land onto the battlefield from the zone it was in (usually that player's hand). By default, a player can take this action only once during each of their turns. A player can take this action any time they have priority and the stack is empty during a main phase of their turn."
**Rule:** CR 116.2a — run `mtg rule 116.2a`
**Why it matters in your decks:** All three decks run 37–38 lands (`mtg deck stats <slug>`), and tidus has 16 lands that enter tapped, bumbleflower 14, dogmeat 12. A land that enters tapped produces nothing this turn — so play those on turns where you weren't going to spend all your mana anyway.

### End step
**In plain English:** The "at end of turn" window. Effects that last "until end of turn" are still on during this step — they wear off afterwards, in cleanup.
**Official:** "Part of the turn. This step is the first step of the ending phase. See rule 513, 'End Step.'"
**Rule:** CR 513 — run `mtg rule 513`
**Why it matters in your decks:** This is the polite spot to cast instants on an opponent's turn — you've seen their whole turn and they're nearly done, so your mana was never wasted.

### Cleanup step
**In plain English:** Discard down to seven cards, damage on creatures wears off, "until end of turn" effects end. Usually nobody does anything here.
**Official:** "Part of the turn. This step is the second and final step of the ending phase. See rule 514, 'Cleanup Step.'"
**Rule:** CR 514 — run `mtg rule 514`
**Why it matters in your decks:** Bumbleflower draws you a *lot* of cards (25 draw pieces per `mtg deck stats bumbleflower -v`). You will genuinely hit the seven-card discard limit. Spend cards rather than hoard them.

---

## The stack and timing

This section is the one that separates "I can read a card" from "I can play Magic."

### The stack
**In plain English:** A waiting line for spells and abilities. When you cast something it does **not** happen immediately — it goes on the stack. Everyone gets a chance to respond. Then the **last** thing added resolves **first**, like a stack of plates.
**Official:** "A zone. The stack is the zone in which spells, activated abilities, and triggered abilities wait to resolve. See rule 405, 'Stack.'"
**Rule:** CR 405; resolution order in CR 405.5 — "When all players pass in succession, the top (last-added) spell or ability on the stack resolves. If the stack is empty when all players pass, the current step or phase ends and the next begins." Run `mtg rule 405` and `mtg rule 405.5`
**Why it matters in your decks:** Bumbleflower triggers on **every spell you cast**, so your own trigger sits on the stack *above* the spell that caused it — meaning the counter and the flying land *before* your spell resolves. Read the stack top-down and you'll never be surprised.

### Priority
**In plain English:** Only one player is allowed to act at a time. That player "has priority." After you cast something, priority passes around the table; when everyone declines in a row, the top of the stack resolves.
**Official:** "Which player can take actions at any given time is determined by a system of 'priority.' See rule 117, 'Timing and Priority.'" And CR 117.1: "…The player with priority may cast spells, activate abilities, and take special actions."
**Rule:** CR 117, CR 117.1 — run `mtg rule 117`
**Why it matters in your decks:** "Can I do this now?" is almost always answered by "do I have priority, and is what I'm casting an instant?" See the next entry.

### Instant speed vs. sorcery speed
**In plain English:** **Instant speed** = you can do it almost any time you have priority, including on someone else's turn and in the middle of combat. **Sorcery speed** = only on *your* turn, in a *main phase*, with an *empty stack*. Note: "instant speed" and "sorcery speed" are player shorthand — the CLI has no glossary entry for either (`mtg glossary "instant speed"` returns no exact match). The real rule is CR 117.1a.
**Official:** "A player may cast an instant spell any time they have priority. A player may cast a noninstant spell during their main phase any time they have priority and the stack is empty."
**Rule:** CR 117.1a — run `mtg rule 117.1a`. Card types: instant CR 304, sorcery CR 307
**Why it matters in your decks:** dogmeat's **Heroic Intervention** and **Valorous Stance** are instants — hold them up. **Equip** is explicitly sorcery-speed ("Activate only as a sorcery," CR 702.6a), so you cannot suit up a creature mid-combat in response to a removal spell. That's a real dogmeat trap.

### In response
**In plain English:** Casting or activating something while another spell/ability is still waiting on the stack. Because the stack resolves last-in-first-out, your response resolves **before** the thing you responded to.
**Official:** Not a defined glossary term. It's the practical consequence of CR 405.5 (top of the stack resolves first) and CR 117.1a (instants may be cast any time you have priority).
**Rule:** CR 405.5 + CR 117.1a — run `mtg rule 405.5`
**Why it matters in your decks:** Opponent targets your commander with removal → *in response* you cast **Heroic Intervention** (dogmeat) giving your permanents indestructible. Your instant resolves first, so by the time their spell resolves, the creature can't be destroyed.

### Resolve
**In plain English:** The moment a spell or ability actually *does* the thing printed on it.
**Official:** "When the spell or ability on top of the stack 'resolves,' its instructions are followed and it has its effect. See rule 608, 'Resolving Spells and Abilities.'"
**Rule:** CR 608 — run `mtg rule 608`
**Why it matters in your decks:** Bumbleflower's ability says "If this is the **second time this ability has resolved** this turn, you draw two cards." Casting two spells isn't enough — both triggers have to actually resolve.

### Target
**In plain English:** Something a spell or ability picks out *when you cast/activate it*, not when it resolves. You choose targets up front, and they must be legal choices.
**Official:** "A preselected object or player a spell or ability will affect. See rule 115, 'Targets.'"
**Rule:** CR 115; "any target" explained in CR 115.4 — run `mtg rule 115`
**Why it matters in your decks:** Tidus reads "move a counter from **target** creature you control onto a **second target** creature you control" — you must have two legal creatures at the moment the trigger goes on the stack, not later.

### Fizzle (all targets illegal)
**In plain English:** If every target a spell picked is gone or no longer legal by the time it resolves, the spell does nothing at all and goes to the graveyard. Players call this "fizzling."
**Official:** "…If all its targets, for every instance of the word 'target,' are now illegal, the spell or ability doesn't resolve. It's removed from the stack and, if it's a spell, put into its owner's graveyard…"
**Rule:** CR 608.2b — run `mtg rule 608.2b`
**Why it matters in your decks:** This is *defense*. Opponent aims removal at your enchanted dogmeat creature; if you can make that creature an illegal target (hexproof from **Swiftfoot Boots**, "Equipped creature has hexproof and haste") *before* the spell resolves, their spell fizzles entirely.

### Mana ability
**In plain English:** An ability that makes mana. It does **not** use the stack — it just happens, and nobody can respond to it.
**Official:** "An activated or triggered ability that could create mana and doesn't use the stack. See rule 605, 'Mana Abilities.'"
**Rule:** CR 605 — run `mtg rule 605`
**Why it matters in your decks:** Tapping **Sol Ring** for `{C}{C}` can't be "responded to." You can also tap for mana in the middle of casting a spell (CR 117.1d).

### Cast
**In plain English:** Taking a card from your hand (usually), putting it on the stack, and paying for it. Note: putting a token onto the battlefield or playing a land is **not** casting.
**Official:** "To cast a spell is to take it from where it is (usually the hand), put it on the stack, and pay its costs, so that it will eventually resolve and have its effect."
**Rule:** CR 601.2 — run `mtg rule 601.2`
**Why it matters in your decks:** Bumbleflower triggers on "**Whenever you cast a spell**" — lands don't trigger it, and neither do abilities you activate. Only spells. **Inexorable Tide** in tidus ("Whenever you cast a spell, proliferate") works the same way.

---

## Abilities — the three kinds

Almost every confusing card resolves once you can say which of these three it is.

### Triggered ability
**In plain English:** Starts with **when / whenever / at**. You don't choose to use it — it fires by itself when its condition happens, then goes on the stack.
**Official:** "A kind of ability. Triggered abilities begin with the word 'when,' 'whenever,' or 'at.' They're written as '[Trigger condition], [effect].'"
**Rule:** CR 113 (Abilities), CR 603 (Handling Triggered Abilities) — run `mtg rule 603`
**Why it matters in your decks:** All three commanders are trigger engines. Dogmeat: "**Whenever** a creature you control that's enchanted or equipped attacks, create a Junk token." You must remember these — an opponent is not obliged to remind you.

### Activated ability
**In plain English:** Written as **cost : effect**, with a colon. You choose to pay the cost, and then it goes on the stack.
**Official:** "A kind of ability. Activated abilities are written as '[Cost]: [Effect.] [Activation instructions (if any).]'"
**Rule:** CR 113, CR 602 (Activating Activated Abilities) — run `mtg rule 602`
**Why it matters in your decks:** **Hoofprints of the Stag** (bumbleflower): "{2}{W}, Remove four hoofprint counters from this enchantment: Create a 4/4 white Elemental creature token with flying. Activate only during your turn." Everything before the colon is a cost you must pay.

### Static ability
**In plain English:** No trigger, no cost. It's just true, all the time, while the card is out.
**Official:** "A kind of ability. Static abilities do something all the time rather than being activated or triggered."
**Rule:** CR 113, CR 604 (Handling Static Abilities) — run `mtg rule 604`
**Why it matters in your decks:** **All That Glitters** (dogmeat): "Enchanted creature gets +1/+1 for each artifact and/or enchantment you control." That number recalculates continuously — it goes up the instant another Equipment hits the battlefield.

### Enters the battlefield (ETB)
**In plain English:** A trigger that fires when a permanent shows up on the battlefield. Modern cards just say "When ~ enters."
**Official:** "A nontoken permanent enters the battlefield when it's moved onto the battlefield from another zone. A token enters the battlefield as it's created. … This phrase has been shortened to simply 'enters' in rules text on cards in most contexts."
**Rule:** CR 403.3, 603.6a, 603.6d, 614.12 — run `mtg rule 603.6a`
**Why it matters in your decks:** Dogmeat: "When Dogmeat enters, mill five cards, then return an Aura or Equipment card from your graveyard to your hand." Per its official ruling (`mtg card "Dogmeat, Ever Loyal"`): *"The card you return with Dogmeat's first ability doesn't have to be one of the cards you milled with that ability."*

### Permanent
**In plain English:** Anything sitting on the battlefield: creatures, lands, artifacts, enchantments. Instants and sorceries are never permanents — they resolve and go to the graveyard.
**Official:** "A card or token on the battlefield. See rule 110, 'Permanents.'"
**Rule:** CR 110 — run `mtg rule 110`
**Why it matters in your decks:** "Destroy target permanent" hits far more than "destroy target creature." Board wipes usually name a permanent type.

### Spell
**In plain English:** A card while it is on the stack, on its way to resolving. Once it resolves it stops being a spell.
**Official:** "A card on the stack. Also a copy (of either a card or another spell) on the stack. See rule 112, 'Spells.'"
**Rule:** CR 112 — run `mtg rule 112`
**Why it matters in your decks:** **An Offer You Can't Refuse** (tidus and bumbleflower) reads "Counter target **noncreature spell**" — it can only be aimed at something currently on the stack, never at a creature already on the battlefield.

---

## Zones — where cards live

### Zones (overview)
**In plain English:** **Seven** places a card can be. Cards constantly move between them, and *a card that changes zone is treated as a brand-new object* — which is why counters fall off.
**Official:** "A place where objects can be during a game. See section 4, 'Zones.'" And CR 400.1: "A zone is a place where objects can be during a game. There are normally seven zones: library, hand, battlefield, graveyard, stack, exile, and command." And CR 400.7: "An object that moves from one zone to another becomes a new object with no memory of, or relation to, its previous existence."
**Rule:** CR 400.1 (what a zone is, and the list of seven), CR 400.7 (changing zones = brand-new object), CR 400.2 (public vs. hidden zones) — run `mtg rule 400.1`

| Zone | Plain English | Official (glossary) | Rule |
|---|---|---|---|
| **Library** | Your face-down deck. | "A zone. A player's library is where that player draws cards from." | CR 401 |
| **Hand** | Cards you've drawn but not played. | "A zone. A player's hand is where that player holds cards they have drawn but not played yet." | CR 402 |
| **Battlefield** | The table in front of you — where permanents live. | "A zone. The battlefield is the zone in which permanents exist. It used to be known as the 'in-play' zone." | CR 403 |
| **Graveyard** | Your discard pile, face up. | "A zone. A player's graveyard is their discard pile." | CR 404 |
| **Stack** | The waiting line for spells and abilities. Yes, it's a zone — a spell on the stack is a card in the stack zone. Full entry: **[The stack](#the-stack)** above. | "A zone. The stack is the zone in which spells, activated abilities, and triggered abilities wait to resolve." | CR 405 |
| **Exile** | Out of the game, essentially a holding pen. | "A zone. Exile is essentially a holding area for cards. It used to be known as the 'removed-from-the-game' zone." | CR 406 |
| **Command zone** | Where your commander waits. | "A zone for certain specialized objects that have an overarching effect on the game, yet are not permanents and cannot be destroyed." | CR 408 |

Chase any of them with `mtg rule 404` etc.
**Why it matters in your decks:** Dogmeat mills five and returns an Aura/Equipment from the **graveyard** to your **hand** — three zones in one sentence. And **Junk tokens** exile the top of your **library** and let you play it from **exile**.

---

## Combat

### Combat phase (the five steps)
**In plain English:** Beginning of combat → declare attackers → declare blockers → combat damage → end of combat. There are *two* damage steps if anything has first or double strike.
**Official:** "The combat phase has five steps, which proceed in order: beginning of combat, declare attackers, declare blockers, combat damage, and end of combat. … There are two combat damage steps if any attacking or blocking creature has first strike (see rule 702.7) or double strike (see rule 702.4)."
**Rule:** CR 506.1 — run `mtg rule 506.1`
**Why it matters in your decks:** Tidus moves a counter at the **beginning of combat**, one step *before* you declare attackers — so the counter is already where you want it when you swing.

### Declare attackers step
**In plain English:** You pick which of your creatures attack and who each one is attacking. Attacking normally taps the creature. In Commander you choose which opponent (or planeswalker) each attacker goes at.
**Official:** "Part of the turn. This step is the second step of the combat phase. See rule 508, 'Declare Attackers Step.'"
**Rule:** CR 508 — run `mtg rule 508`
**Why it matters in your decks:** Dogmeat's Junk trigger is "**whenever** a creature you control that's enchanted or equipped **attacks**" — it triggers on declaration, before any blocks, before any damage. Even if the creature dies to a blocker, you already got the Junk token.

### Blocking
**In plain English:** On defense, you choose which of your untapped creatures block which attackers. The attacker doesn't get to choose your blocks.
**Official:** "To send a creature into combat defensively. A creature can block an attacking creature." And CR 509.1a: "The defending player chooses which creatures they control, if any, will block. The chosen creatures must be untapped … For each of the chosen creatures, the defending player chooses one creature for it to block that's attacking that player, a planeswalker they control, or a battle they protect."
**Rule:** CR 509, CR 509.1a — run `mtg rule 509.1a`
**Why it matters in your decks:** Blockers must be **untapped**. That's exactly why **vigilance** matters — six of bumbleflower's creatures have it, including Ms. Bumbleflower herself (1/5, a genuinely good blocker).

### Combat damage step
**In plain English:** Attackers and blockers hit each other simultaneously. Unblocked attackers hit the player.
**Official:** "Damage dealt during the combat damage step by attacking creatures and blocking creatures as a consequence of combat. See rule 510, 'Combat Damage Step.'"
**Rule:** CR 510; damage assignment among multiple blockers in CR 510.1c — run `mtg rule 510.1c`
**Why it matters in your decks:** Tidus's **Cheer** ability keys off "creatures you control **with counters on them** deal combat damage to a player" — so it only pays off on damage that gets *through*, not damage traded with blockers. That's what evasion is for.

### Damage / lethal damage
**In plain English:** Damage sticks on a creature until cleanup. A creature dies when total damage marked on it is at least its toughness.
**Official:** "If a creature has toughness greater than 0, it has damage marked on it, and the total damage marked on it is greater than or equal to its toughness, that creature has been dealt lethal damage and is destroyed."
**Rule:** CR 120 (Damage), CR 704.5g (lethal damage as a state-based action) — run `mtg rule 704.5g`
**Why it matters in your decks:** Damage is *marked*, not permanent. A creature that survived 2 damage this turn is back to full at cleanup — so a +1/+1 counter from Tidus or Bumbleflower can save a creature mid-combat, permanently.

### Evasion
**In plain English:** Any ability that makes a creature hard or impossible to block. **Flying** and **menace** are the ones in your decks — the CR names both outright. **Trample is *not* evasion**, and that is the most common mix-up here: a creature with trample gets blocked completely normally. Trample only changes how its damage is *assigned* after blockers are in (CR 702.19a: "Trample is a static ability that modifies the rules for assigning an attacking creature's combat damage").
**Official:** "An ability that restricts what creatures can block an attacking creature. See rules 509.1b–c." And CR 702.9a: "Flying is an evasion ability." And CR 702.111a: "Menace is an evasion ability."
**Rule:** CR 509.1b (the blocking restriction evasion creates), CR 702.9a (flying), CR 702.111a (menace). Trample is CR 702.19a–b and is a damage-assignment ability, not evasion — run `mtg rule 509.1b` then `mtg rule 702.19`
**Why it matters in your decks:** Tidus wants damage to *connect*, so evasion is how the Cheer engine actually turns on. Bumbleflower literally grants flying every time you cast a spell (verified: `mtg card "Ms. Bumbleflower"` — "Put a +1/+1 counter on target creature. It gains flying until end of turn."). Trample feeds the same engine by a different route — excess damage spills past the blocker onto the player — which is exactly why people file it under evasion by mistake.

### Keyword abilities you will actually see
Each of these is confirmed present in at least one of your three decks (verified via `mtg search "deck:<slug> <keyword>"`).

| Keyword | Plain English | Official (glossary) | Rule | Where it shows up |
|---|---|---|---|---|
| **Flying** | Only creatures with flying or reach can block it. | "A keyword ability that restricts how a creature may be blocked." | CR 702.9 | 7 cards in tidus, 6 in bumbleflower; Bumbleflower *grants* it every spell |
| **Reach** | Can block fliers, but can't fly itself. | "A keyword ability that allows a creature to block an attacking creature with flying." | CR 702.17 | 2 cards in tidus |
| **Menace** | Can't be blocked by just one creature — needs two or more. | "An evasion ability that makes creatures unblockable by a single creature." | CR 702.111 | dogmeat: **Sticky Fingers**, **Veronica, Dissident Scribe** |
| **Trample** | Excess damage past the blocker spills onto the player. | "A keyword ability that modifies how a creature assigns combat damage." | CR 702.19 | 6 cards in dogmeat (**Rancor**, **Behemoth Sledge**…), 4 in tidus |
| **Vigilance** | Attacking doesn't tap it, so it can still block. | "A keyword ability that lets a creature attack without tapping." | CR 702.20 | 6 in bumbleflower, 3 in tidus, 3 in dogmeat |
| **First strike** | Deals its combat damage in an earlier damage step. | "A keyword ability that lets a creature deal its combat damage before other creatures." | CR 702.7 | 1 each in tidus and dogmeat |
| **Double strike** | Deals combat damage twice — first-strike damage *and* normal damage. | "A keyword ability that lets a creature deal its combat damage twice." | CR 702.4 | 3 in dogmeat (**Fireshrieker**), 1 in tidus |
| **Deathtouch** | Any nonzero damage from it destroys the creature. | "A keyword ability that causes damage dealt by an object to be especially effective." | CR 702.2 | dogmeat: **Basilisk Collar** |
| **Lifelink** | Damage it deals also gains you that much life. | "A keyword ability that causes a player to gain life." | CR 702.15 | 1–2 cards in each deck |
| **Haste** | Ignores summoning sickness — can attack and tap the turn it arrives. | "A keyword ability that lets a creature ignore the 'summoning sickness' rule." | CR 702.10, CR 302.6 | **Swiftfoot Boots** (bumbleflower, dogmeat) |
| **Hexproof** | Your opponents can't target it. *You* still can. | "A keyword ability that precludes a permanent or player from being targeted by an opponent." | CR 702.11 | **Swiftfoot Boots**, **Champion's Helm** (dogmeat) |
| **Ward** | Opponents must pay an extra cost to target it, or their spell is countered. | "A triggered ability that can counter spells or abilities that target the permanent with ward." | CR 702.21 | dogmeat: **Codsworth, Handy Helper** |
| **Indestructible** | Can't be destroyed by damage or "destroy" effects. Can still be exiled or sacrificed. | "A keyword ability that precludes a permanent from being destroyed." | CR 702.12 | dogmeat: **Heroic Intervention**, **Valorous Stance**, **Almost Perfect**, **Cait, Cage Brawler** |
| **Flash** | You may cast it any time you could cast an instant. | "A keyword ability that lets a player play a card any time they could cast an instant." | CR 702.8 | 1 in tidus, 2 in dogmeat |

Chase any of these with `mtg rule 702.19` (etc.) or `mtg glossary trample`.

---

## State-based actions and other automatic stuff

### State-based actions
**In plain English:** The game's automatic janitor. Nobody casts anything and nothing uses the stack — the game just checks, constantly, and cleans up: creatures with lethal damage die, players at 0 life lose, the legend rule applies.
**Official:** "Game actions that happen automatically whenever certain conditions are met. See rule 704, 'State-Based Actions.'" And CR 704.3: "Whenever a player would get priority … the game checks for any of the listed conditions for state-based actions, then performs all applicable state-based actions simultaneously as a single event."
**Rule:** CR 704, CR 704.3 — run `mtg rule 704`
**Why it matters in your decks:** Losing at 0 or less life (CR 704.5a), dying to lethal damage (CR 704.5g), the legend rule (CR 704.5j), and **commander damage** (CR 903.10a) are all state-based actions. You never "cast" them — they just happen, and you can't respond to them.

### Legend rule
**In plain English:** You can't control two legendary permanents with the same name. If you somehow do, you pick one to keep and the other goes to the graveyard.
**Official:** "A state-based action that causes a player who controls two or more legendary permanents with the same name to put all but one into their owners' graveyards. See rule 704.5j."
**Rule:** CR 704.5j — run `mtg rule 704.5j`
**Why it matters in your decks:** Your decks are full of legends — 14 legendary cards in tidus, 12 in dogmeat, 10 in bumbleflower (via `mtg search "deck:<slug> legendary"`). Two *different* legends are fine; only same-name collides. In practice this mostly comes up if an opponent is running the same legend as you.

### Summoning sickness
**In plain English:** A creature that just arrived can't attack, and can't use abilities with the tap `{T}` or untap symbol, until the start of your next turn. It *can* block immediately.
**Official:** "Informal term for a player's inability to attack with a creature or to activate its abilities that include the tap symbol or the untap symbol unless the creature has been under that player's control since the beginning of that player's most recent turn."
**Rule:** CR 302.6 — run `mtg rule 302.6`
**Why it matters in your decks:** dogmeat runs 11 one-drops and a very low curve (avg MV 2.82). Everything you play is sick for a turn — which is why **Swiftfoot Boots** granting haste is worth so much there.

### Tap
**In plain English:** Turning a card sideways to show it's been used. Lands tap for mana; creatures tap to attack.
**Official:** "To turn a permanent sideways from an upright position. See rule 701.26, 'Tap and Untap.'"
**Rule:** CR 701.26 — run `mtg rule 701.26`
**Why it matters in your decks:** Tapped creatures can't block (CR 509.1a). Attacking with everything leaves you wide open — this is the single most common beginner mistake in multiplayer Commander.

---

## Counters, tokens, and things you attach

### Counter — the beginner trap
**In plain English:** The word "counter" means **two completely unrelated things**, and Magic never disambiguates for you.
1. **Counter (the verb)** = cancel a spell so it never resolves.
2. **Counter (the noun)** = a physical marker you put on a permanent, like a **+1/+1 counter**.
**Official:** "1. To cancel a spell or ability so it doesn't resolve and none of its effects occur. See rule 701.6, 'Counter.' 2. A marker placed on an object or player that modifies its characteristics or interacts with a rule or ability. See rule 122, 'Counters.'"
**Rule:** CR 701.6 (cancel) and CR 122 (marker) — run `mtg rule 701.6` and `mtg rule 122`
**Why it matters in your decks:** Tidus's deck is literally named *Counter Blitz* and it means **+1/+1 counters** — it runs only **one** actual counterspell, **An Offer You Can't Refuse** (verified: `mtg search "deck:tidus counter target spell"` → 1 match). Bumbleflower has 4 cards mentioning countering spells. When someone at the table says "counter it," they mean cancel. When your card says "put a counter on it," it means marker.

### +1/+1 counter
**In plain English:** A marker that permanently makes a creature +1 power and +1 toughness. It stays until the creature leaves the battlefield.
**Official:** "A counter is a marker placed on an object or player that modifies its characteristics and/or interacts with a rule, ability, or effect. Counters are not objects and have no characteristics. **Notably, a counter is not a token, and a token is not a counter.**"
**Rule:** CR 122.1 — run `mtg rule 122`
**Why it matters in your decks:** This is tidus's entire engine (38 cards reference `+1/+1`, per `mtg search "deck:tidus +1/+1"`), and bumbleflower's commander adds one every single time you cast a spell.

### Counters fall off when a card changes zone
**In plain English:** If the creature bounces, dies, or gets exiled, its counters do not come back. They cease to exist.
**Official:** "Counters on an object are not retained if that object moves from one zone to another. The counters are not 'removed'; they simply cease to exist. See rule 400.7."
**Rule:** CR 122.2 — run `mtg rule 122`
**Why it matters in your decks:** A tidus creature loaded with counters is a single removal spell away from nothing. This is the argument for spreading counters around (which is exactly what Tidus's "move a counter" ability lets you do) rather than building one giant target.

### Moving a counter
**In plain English:** Move = remove from one thing, put on another. If either half is impossible, *nothing* moves.
**Official:** "If an effect says to 'move' a counter, it means to remove that counter from the object it's currently on and put it onto a second object. If either of these actions isn't possible, it's not possible to move a counter, and no counter is removed from or put onto anything."
**Rule:** CR 122.5 — run `mtg rule 122`
**Why it matters in your decks:** This is Tidus's beginning-of-combat ability exactly. If the first creature loses its counter in response, the whole move does nothing.

### Proliferate
**In plain English:** Look at every permanent and player that already has at least one counter; for any of them you choose, add one more of each kind of counter it already has. It never *creates* the first counter.
**Official:** "To give an additional counter to any number of players and/or permanents of each kind they already have. See rule 701.34, 'Proliferate.'"
**Rule:** CR 701.34 — run `mtg rule 701.34`
**Why it matters in your decks:** 5 cards in tidus proliferate, including the commander and **Inexorable Tide** ("Whenever you cast a spell, proliferate"). Rule of thumb: get counters down *first*, then proliferate is a free scaling engine. (`mtg search "deck:tidus proliferate"`)

### Evolve
**In plain English:** When a bigger creature shows up under your control, this creature gets a +1/+1 counter.
**Official:** "A keyword ability that lets you put a +1/+1 counter on a creature when a larger creature enters the battlefield under your control. See rule 702.100, 'Evolve.'"
**Rule:** CR 702.100 — run `mtg rule 702.100`
**Why it matters in your decks:** tidus runs **Gyre Sage** and **Fathom Mage**. Play your small evolve creature *before* the big ones, not after.

### Adapt
**In plain English:** Pay a cost; if the creature has **no** +1/+1 counters at all, it gets a batch of them. If it already has any, adapt does nothing.
**Official:** "A keyword action that puts +1/+1 counters on a creature that doesn't have any yet. See rule 701.46, 'Adapt.'"
**Rule:** CR 701.46 — run `mtg rule 701.46`
**Why it matters in your decks:** tidus's **Incubation Druid**. Adapt *first*, then let Tidus and proliferate stack on top — do it the other way round and you wasted the mana.

### Token
**In plain English:** A permanent that isn't a real card — you represent it with a marker or a spare card. Tokens exist only on the battlefield; if one leaves, it's gone for good.
**Official:** "A marker used to represent any permanent that isn't represented by a card. See rule 111, 'Tokens.'" And CR 111.1: "Some effects put tokens onto the battlefield."
**Rule:** CR 111 — run `mtg rule 111`
**Why it matters in your decks:** dogmeat makes 20 cards' worth of token references, bumbleflower 9. Dogmeat's **Junk token** is defined right on the commander: *"It's an artifact with '{T}, Sacrifice this token: Exile the top card of your library. You may play that card this turn. Activate only as a sorcery.'"* Note the ruling from `mtg card "Dogmeat, Ever Loyal"`: *"You can't sacrifice a Junk token to pay multiple costs."*

### Aura
**In plain English:** An enchantment that sticks onto a creature (or other thing) and modifies it. It's cast targeting that creature, and it enters already attached.
**Official:** "An enchantment subtype. Aura spells target objects or players, and Aura permanents are attached to objects or players." And CR 303.4: "…An Aura enters the battlefield attached to an object or player. What an Aura can be attached to is defined by its enchant keyword ability…"
**Rule:** CR 303, CR 303.4, CR 702.5 (Enchant) — run `mtg rule 303.4`
**Why it matters in your decks:** dogmeat runs **15 Auras** (`mtg search "deck:dogmeat is:aura"`) — **Rancor**, **All That Glitters**, **Sticky Fingers**, **Mantle of the Ancients**… If the creature dies, most Auras die with it. **Rancor** is the exception: *"When this Aura is put into a graveyard from the battlefield, return it to its owner's hand."*

### Equipment (and Equip)
**In plain English:** An artifact you attach to a creature. Unlike an Aura, the Equipment **stays on the battlefield** when the creature dies — you just re-equip it to something else. But equipping is sorcery-speed only.
**Official:** Equipment — "An artifact subtype. Equipment can be attached to creatures." Equip — CR 702.6a: "Equip is an activated ability of Equipment cards. 'Equip [cost]' means '[Cost]: Attach this permanent to target creature you control. **Activate only as a sorcery.**'"
**Rule:** CR 301 (Artifacts), CR 702.6, CR 702.6a — run `mtg rule 702.6a`
**Why it matters in your decks:** dogmeat runs **13 Equipment** (`mtg search "deck:dogmeat is:equipment"`). **Aura vs. Equipment is the key dogmeat decision:** Auras are cheaper and bigger but die with the creature; Equipment survives but costs mana every time you move it — and you can't move it in response to removal.

### Attach
**In plain English:** The formal word for putting an Aura or Equipment onto something.
**Official:** "To take an Aura, Equipment, or Fortification from where it currently is and put it onto a specified object or player. See rule 701.3, 'Attach.'"
**Rule:** CR 701.3 — run `mtg rule 701.3`
**Why it matters in your decks:** Dogmeat's Junk trigger checks whether the attacking creature is "enchanted or equipped" — i.e. whether something is *attached* to it. One Aura on a creature is enough to turn every attack into a Junk token.

### Mill
**In plain English:** Put cards from the top of your library straight into your graveyard.
**Official:** "To mill a number of cards, a player puts that many cards from the top of their library into their graveyard. See rule 701.17."
**Rule:** CR 701.17 — run `mtg rule 701.17`
**Why it matters in your decks:** Dogmeat mills **you**, on purpose — it's fuel, not damage, because you then return an Aura or Equipment from that graveyard.

---

## Card frames that tell a story — Saga, Class, Adventure

Three card types whose text box is laid out differently from a normal card. Each gets its own
numbered section in the *back* of the Comprehensive Rules (714, 715, 716) precisely because the
frame itself carries rules meaning. You own examples of all three.

### Saga
**In plain English:** An enchantment that does a scripted sequence of things over consecutive turns — chapter I on the turn it lands, chapter II next turn, and so on — then sacrifices itself when it runs out of chapters.
**Official:** "An enchantment subtype. Sagas have a number of chapter abilities that take effect over a number of turns to tell a story. See rule 714, 'Saga Cards.'" And CR 714.4: "If the number of lore counters on a Saga permanent with one or more chapter abilities is greater than or equal to its final chapter number, and it isn't the source of a chapter ability that has triggered but not yet left the stack, that Saga's controller sacrifices it. This state-based action doesn't use the stack."
**Rule:** CR 714 — run `mtg rule 714`
**Why it matters in your decks:** Verified with `mtg search "deck:<slug> type:saga"` — **tidus has 4, dogmeat has 2, bumbleflower has none.** tidus's four are unusual: they're **Enchantment Creature — Saga** (**Summon: Yojimbo**, **Summon: Ixion**, **Summon: Valefor**, **Summon: Magus Sisters**), so they attack and block *and* run their chapters, then sacrifice themselves. dogmeat's two are plain enchantments (**Vault 101: Birthday Party**, **Vault 21: House Gambit**). The self-sacrifice is not optional and it is a state-based action — you cannot keep a finished Saga around.

### Lore counter
**In plain English:** The marker that tracks which chapter a Saga is on. One goes on when the Saga arrives, and one more at the start of each of your turns.
**Official:** No glossary entry under that exact name (`mtg glossary "lore counter"` returns no exact match), but it is an official rules term. CR 714.3: "Sagas use lore counters to track their progress." CR 714.3a: "Each Saga without read ahead has the intrinsic ability 'This Saga enters with a lore counter on it.'" CR 714.3c: "As a player's precombat main phase begins, that player puts a lore counter on each Saga they control with one or more chapter abilities. This turn-based action doesn't use the stack."
**Rule:** CR 714.3, 714.3a, 714.3c (and CR 505.4, the same turn-based action written into the main-phase rules) — run `mtg rule 714.3`
**Why it matters in your decks:** Your Sagas print the shorthand version: **Summon: Yojimbo** reads *"(As this Saga enters and after your draw step, add a lore counter. Sacrifice after IV.)"* — that's the same moment CR 714.3c describes, since the precombat main phase begins right after the draw step. Two consequences: the counter goes on **automatically** (nobody may respond to the counter itself), and a lore counter is still a counter under CR 122 — so it **ceases to exist if the Saga changes zone**, exactly like a +1/+1 counter.

### Chapter ability
**In plain English:** The "I —", "II —", "III —" lines on a Saga. Each one is a **triggered ability** that fires when the lore counters reach that number. It uses the stack, so it can be responded to.
**Official:** No glossary entry under that exact name (`mtg glossary "chapter ability"` returns no exact match). CR 714.2: "A chapter symbol is a keyword ability that represents a triggered ability referred to as a chapter ability." CR 714.2b: "'{rN}—[Effect]' means 'When one or more lore counters are put onto this Saga, if the number of lore counters on it was less than N and became at least N, [effect].'" CR 714.2c: "'{rN1}, {rN2}—[Effect]' means the same as '{rN1}—[Effect]' and '{rN2}—[Effect].'"
**Rule:** CR 714.2, 714.2b, 714.2c — run `mtg rule 714.2`
**Why it matters in your decks:** Two of your Sagas use the combined form CR 714.2c describes. **Summon: Yojimbo** (tidus): *"II, III — Until your next turn, creatures can't attack you unless their controller pays {2} for each of those creatures."* **Vault 101: Birthday Party** (dogmeat): *"II, III — You may put an Aura or Equipment card from your hand or graveyard onto the battlefield…"* That is **two separate chapter abilities**, not one that lasts two turns — you get the effect on chapter II and again on chapter III. Because they're triggered abilities they go on the stack, so an opponent can respond before a chapter resolves.

### Class (enchantment)
**In plain English:** An enchantment you level up by paying mana. Level 1 is free — it's just on. Each higher level costs mana, is sorcery-speed, and permanently adds an ability. You can't skip levels.
**Official:** "An enchantment subtype. Classes have a number of class level abilities that increase their level and grant them new abilities. See rule 716, 'Class Cards.'" And CR 716.2: "A class level bar is a keyword ability that represents both an activated ability and a static ability. A class level bar includes the activation cost of its activated ability and a level number. Any abilities printed within the same text box section as the class level bar are part of its static ability." And CR 716.3: "Any ability printed on a Class card that isn't preceded by a class level bar is treated normally. In particular, the Class has the ability printed in its top text box section at all times."
**Rule:** CR 716, 716.2, 716.3 — run `mtg rule 716`
**Why it matters in your decks:** **bumbleflower is the only deck with Classes** — 2 of them (`mtg search "deck:bumbleflower type:class"`): **Wizard Class** and **Fisher's Talent**. Wizard Class costs `{U}` and its always-on top box is *"You have no maximum hand size"* — which directly cancels the cleanup-step discard problem this file warns about above, in the deck that actually has it (25 draw pieces). Its level 3 (*"Whenever you draw a card, put a +1/+1 counter on target creature you control"*) turns bumbleflower's draw engine into a counter engine. Note the reminder text on both cards: *"(Gain the next level as a sorcery to add its ability.)"* — you cannot level up on someone else's turn or in response to anything.

### Adventure
**In plain English:** A single card with a second, cheaper spell printed on the left. You choose which half to cast. Cast the Adventure half and the card is **exiled**, and you may cast the creature from exile later — one card, two uses.
**Official:** The glossary entry is under *Adventurer Card* (`mtg glossary Adventure` returns no exact entry): "Cards with a two-part card frame (one part of which is inset on the left) on a single card where the alternative characteristics include the Adventure spell type. See rule 715, 'Adventurer Cards.'" And CR 715.3: "As a player plays an adventurer card, the player chooses whether they play the card normally or as an Adventure." And CR 715.4: "In every zone except the stack, and while on the stack not as an Adventure, an adventurer card has only its normal characteristics."
**Rule:** CR 715, 715.3, 715.4 — run `mtg rule 715`
**Why it matters in your decks:** One card, in bumbleflower: **Realm-Cloaked Giant // Cast Off** (`mtg search "deck:bumbleflower type:adventure"`). Cast Off is `{3}{W}{W}` *"Sorcery — Adventure: Destroy all non-Giant creatures. (Then exile this card. You may cast the creature later from exile.)"*; the creature half is `{5}{W}{W}` for a 7/7 with vigilance. So bumbleflower's second board wipe and one of its biggest bodies are the **same card** — wipe the table in the midgame, then cast the Giant out of exile several turns later. CR 715.4 is why it counts as a Giant creature card everywhere except while it's on the stack as Cast Off.

---

## More keyword actions and abilities

Everything in this group is printed on at least one card you own (or, where noted, on none of them
— which is itself worth knowing). All are official; each has a real CR number.

### Scry
**In plain English:** Look at the top N cards of your library and decide, for each, top or bottom. You do **not** draw them — scry only improves what your *next* draw will be.
**Official:** "To manipulate some of the cards on top of your library. See rule 701.22, 'Scry.'" And CR 701.22a: "To 'scry N' means to look at the top N cards of your library, then put any number of them on the bottom of your library in any order and the rest on top of your library in any order."
**Rule:** CR 701.22, 701.22a — run `mtg rule 701.22`
**Why it matters in your decks:** All three decks scry, and in all three it comes from **lands** (`mtg search "deck:<slug> scry"` → tidus 4, bumbleflower 3, dogmeat 4). The Temples — e.g. **Temple of Enlightenment**: *"This land enters tapped. When this land enters, scry 1. {T}: Add {W} or {U}."* — trade a turn of speed for a two-color land plus a look. **Path of Ancestry** (tidus, dogmeat) is fussier: it only scries *"When that mana is spent to cast a creature spell that shares a creature type with your commander."* With 0 tutors in every deck, scry is the only card selection you have — use it, and be willing to bottom a card.

### Surveil
**In plain English:** Like scry, except the cards you don't want go to your **graveyard** instead of the bottom of your library.
**Official:** "To manipulate some of the cards on top of your library, sending some of them to your graveyard and rearranging the rest. See rule 701.25, 'Surveil.'" And CR 701.25a: "To 'surveil N' means to look at the top N cards of your library, then put any number of them into your graveyard and the rest on top of your library in any order."
**Rule:** CR 701.25, 701.25a — run `mtg rule 701.25`
**Why it matters in your decks:** **It doesn't — none of your three decks contains a card that surveils** (verified: `mtg search "deck:tidus surveil"`, `deck:bumbleflower`, `deck:dogmeat` → *not in my data* for all three). It's here because it is scry's twin and you *will* hear it at the table, and the one-line difference is the whole point: scry sends unwanted cards where you can never get them, surveil sends them somewhere Dogmeat can dig them back out of. For a graveyard deck, surveil is an upgrade over scry; for tidus and bumbleflower it is not.

### Investigate / Clue
**In plain English:** Investigate = make a Clue token. A Clue is an artifact that sits on the battlefield doing nothing until you pay `{2}` and sacrifice it to draw a card. It's a stored draw you buy later.
**Official:** Investigate — "A keyword action that creates a Clue artifact token. See rule 701.16, 'Investigate.'" Clue Token — "A Clue token is a colorless artifact token with '{2}, Sacrifice this token: Draw a card.' For more information about predefined tokens, see rule 111.10." And CR 701.16a: "'Investigate' means 'Create a Clue token.' See rule 111.10f." And CR 111.10f: "A Clue token is a colorless Clue artifact token with '{2}, Sacrifice this token: Draw a card.'"
**Rule:** CR 701.16, 701.16a, CR 111.10f — run `mtg rule 701.16`
**Why it matters in your decks:** **tidus only** — 2 cards, none in bumbleflower or dogmeat (`mtg search "deck:<slug> investigate"`). **Tireless Tracker**: *"Landfall — Whenever a land you control enters, investigate"* plus *"Whenever you sacrifice a Clue, put a +1/+1 counter on this creature."* **Lord Jyscal Guado**: *"At the beginning of each end step, if you put a counter on a creature this turn, investigate."* That is a genuine loop in tidus — put a counter on something, get a Clue at end of turn, cash the Clue for a card *and* a counter on the Tracker. Budget the `{2}`: an uncracked Clue is not card advantage yet.

### Hideaway
**In plain English:** When the permanent arrives, look at the top few cards, exile one face down (only you may look at it), and bury the rest at the bottom of your library. Later, if you meet the card's condition, you get to play the exiled card — often for free.
**Official:** "A keyword ability that lets a player store a secret card. See rule 702.75, 'Hideaway.'" And CR 702.75a: "Hideaway is a triggered ability. 'Hideaway N' means 'When this permanent enters, look at the top N cards of your library. Exile one of them face down and put the rest on the bottom of your library in a random order. The exiled card gains "The player who controls the permanent that exiled this card may look at this card in the exile zone."'"
**Rule:** CR 702.75, 702.75a — run `mtg rule 702.75`
**Why it matters in your decks:** **tidus only** — **Fight Rigging** (`mtg search "deck:tidus hideaway"`): *"Hideaway 5"* plus *"At the beginning of combat on your turn, put a +1/+1 counter on target creature you control. Then if you control a creature with power 7 or greater, you may play the exiled card without paying its mana cost."* Two beginner notes. First, the other four cards go to the **bottom of your library in a random order** — that is a real cost, so pick greedily, not safely. Second, the unlock is power **7 or greater**, and stacking +1/+1 counters is exactly what tidus does — Fight Rigging even feeds itself a counter every combat.

### Multikicker
**In plain English:** An optional extra cost you may pay **as many times as you like** while casting the spell. The card then does more for each time you paid.
**Official:** "Multikicker is a variant of the kicker keyword ability. It represents an optional additional cost that may be paid any number of times. See rule 702.33, 'Kicker.' See also Kicker." And CR 702.33c: "Multikicker is a variant of the kicker ability. 'Multikicker [cost]' means 'You may pay an additional [cost] any number of times as you cast this spell.' A multikicker cost is a kicker cost." And CR 702.33d: "If a spell's controller declares the intention to pay any of that spell's kicker costs, that spell has been 'kicked.' If a spell has two kicker costs or has multikicker, it may be kicked multiple times."
**Rule:** CR 702.33, 702.33c, 702.33d — run `mtg rule 702.33`
**Why it matters in your decks:** **tidus only** — **Everflowing Chalice** (`mtg search "deck:tidus multikicker"`): base cost `{0}`, *"Multikicker {2}"*, *"This artifact enters with a charge counter on it for each time it was kicked"*, *"{T}: Add {C} for each charge counter on this artifact."* So it is a mana rock whose size you choose on the way down: pay {2} → taps for one, pay {4} → taps for two. You choose how many times to kick **as you cast it** and never afterwards. And because charge counters are counters, tidus's 5 proliferate cards can grow the Chalice later — proliferate adds one more of each kind of counter already there.

### Monstrosity
**In plain English:** Pay a cost to dump a batch of +1/+1 counters on a creature and flip it to "monstrous." It only works **once ever** — once a creature is monstrous, paying again does nothing.
**Official:** "A keyword action that puts +1/+1 counters on a creature and makes it become monstrous. See rule 701.37, 'Monstrosity.'" And CR 701.37a: "'Monstrosity N' means 'If this permanent isn't monstrous, put N +1/+1 counters on it and it becomes monstrous.'" And CR 701.37b: "Monstrous is a designation that has no rules meaning other than to act as a marker that the monstrosity action and other spells and abilities can identify. Only permanents can be or become monstrous. Once a permanent becomes monstrous, it stays monstrous until it leaves the battlefield. Monstrous is neither an ability nor part of the permanent's copiable values."
**Rule:** CR 701.37, 701.37a, 701.37b, 701.37c — run `mtg rule 701.37`
**Why it matters in your decks:** **tidus only** — **Maester Seymour** (`mtg search "deck:tidus monstrosity"`): *"{3}{G}{G}: Monstrosity X, where X is the number of counters among creatures you control."* Because X counts counters **across your whole board** and you only get one shot, this is a payoff you save: build the board first, then go monstrous once, late. Per CR 701.37b, monstrous is **not** a counter — proliferate can't touch it, and nothing removes it while the creature stays on the battlefield.

### Phasing / phase out
**In plain English:** A phased-out permanent is still yours and still on the battlefield, but the game pretends it doesn't exist — it can't be hit by anything, and it can't do anything. It comes back on your next untap step, unchanged.
**Official:** Phasing — "A keyword ability that causes a permanent to sometimes be treated as though it does not exist. See rule 702.26, 'Phasing.'" Phased In, Phased Out — "A status a permanent may have. Phased-in is the default status. Phased-out permanents are treated as though they do not exist. See rule 110.5 and rule 702.26, 'Phasing.' ('Phased-out' was a zone in older versions of the rules.)" And CR 702.26b: "If a permanent phases out, its status changes to 'phased out.' Except for rules and effects that specifically mention phased-out permanents, a phased-out permanent is treated as though it does not exist. It can't affect or be affected by anything else in the game." And CR 702.26d: "The phasing event doesn't actually cause a permanent to change zones or control… **Counters and stickers remain on a permanent while it's phased out.**" And CR 702.26g: "When a permanent phases out, any Auras, Equipment, or Fortifications attached to that permanent phase out at the same time."
**Rule:** CR 702.26, 702.26b, 702.26d, 702.26g, CR 110.5 — run `mtg rule 702.26`
**Why it matters in your decks:** No card in any deck has the *keyword ability* phasing (`mtg search "deck:<slug> phasing"` → nothing in all three), but **bumbleflower's Perch Protection** phases your whole board out: *"…all permanents you control phase out, and until your next turn, your life total can't change and you gain protection from everything."* This is the single best "dodge a board wipe" line you own, and CR 702.26d is why it's better than it looks — **your counters survive.** Compare CR 122.2 above: a creature that leaves the battlefield loses its counters forever, but a creature that phases out comes back with every +1/+1 counter and every Aura and Equipment still on it.

### Protection from everything
**In plain English:** A blanket version of protection. Nothing can target it, enchant it, equip it, block it, or damage it. It does **not** make it indestructible, and it does not stop sacrifice.
**Official:** Protection — "A keyword ability that provides a range of benefits against objects with a specific quality. See rule 702.16, 'Protection.'" And CR 702.16j: "'Protection from everything' is a variant of the protection ability. A permanent or player with protection from everything has protection from each object regardless of that object's characteristic values. Such a permanent or player can't be targeted by spells or abilities and can't be enchanted by Auras. Such a permanent can't be equipped by Equipment, fortified by Fortifications, or blocked by creatures. All damage that would be dealt to such a permanent or player is prevented."
**Rule:** CR 702.16, 702.16j — run `mtg rule 702.16`
**Why it matters in your decks:** One card in your three decks has it, and it grants it to **you, the player**, not to a creature: **Perch Protection** in bumbleflower (`mtg search "deck:bumbleflower protection from everything"`). Read CR 702.16j as a list of exactly five things and nothing more — targeting, Auras, Equipment, blocking, damage. It says nothing about *destroy*, *exile*, or *sacrifice*, which is the same trap as **Heroic Intervention** in the destroy/sacrifice/exile section below: protection is not immunity.

---

## Destroy vs. sacrifice vs. exile — why the difference matters

These three all "get rid of a permanent," and they are **not** interchangeable. Knowing which is which is how you dodge removal and how you beat other people's threats.

### Destroy
**In plain English:** Send a permanent from the battlefield to the graveyard. **Indestructible stops this.** Regeneration and similar effects can stop it.
**Official:** "To move a permanent from the battlefield to its owner's graveyard. See rule 701.8, 'Destroy.'"
**Rule:** CR 701.8 — run `mtg rule 701.8`

### Sacrifice
**In plain English:** *You* move *your own* permanent to the graveyard, usually as a cost. Indestructible does **not** save it. Hexproof does **not** save it — nothing is targeting it.
**Official:** "To move a permanent you control to its owner's graveyard. See rule 701.21, 'Sacrifice.'"
**Rule:** CR 701.21 — run `mtg rule 701.21`

### Exile
**In plain English:** Remove it from the game entirely. It doesn't go to the graveyard, so nothing can recur it. Indestructible does **not** save it. This is the cleanest removal in the game.
**Official:** "1. A zone. Exile is essentially a holding area for cards. … 2. To put an object into the exile zone from whatever zone it's currently in."
**Rule:** CR 406 — run `mtg rule 406`

**Why the distinction matters in your decks:**
- Your best removal is exile-based: **Path to Exile** ("Exile target creature") in tidus and dogmeat, **Swords to Plowshares** ("Exile target creature") in bumbleflower. Use these on the threats that come *back* — including opponents' commanders.
- **Farewell** (tidus) exiles rather than destroys: *"Choose one or more — Exile all artifacts. / Exile all creatures. / Exile all enchantments. / Exile all graveyards."* Indestructible creatures do not survive it.
- dogmeat's **Heroic Intervention** grants indestructible — great against a "destroy all" wipe, **useless** against a "exile all" wipe like Farewell, and useless against sacrifice effects.
- dogmeat's whole Junk engine is built on *sacrificing your own tokens*: "{T}, Sacrifice this token: Exile the top card of your library."

---

## Commander-specific

### Commander (the format)
**In plain English:** A 100-card multiplayer format where one legendary creature leads your deck, starts in the command zone, and can be cast from there over and over.
**Official:** "1. A casual variant in which each deck is led by a legendary card (usually a creature). See rule 903, 'Commander.' 2. A designation given to one legendary card in each player's deck in the Commander casual variant."
**Rule:** CR 903 — run `mtg rule 903`
**Why it matters in your decks:** Your three commanders are Tidus, Yuna's Guardian; Ms. Bumbleflower; and Dogmeat, Ever Loyal. Run `mtg card "<name>"` to see the exact text plus every official ruling.

### Starting life total (40) and multiplayer
**In plain English:** Everyone starts at **40 life**, not 20, and the default is a free-for-all where anyone can attack anyone.
**Official:** "Once the starting player has been determined, each player sets their life total to 40 and draws a hand of seven cards." And CR 903.2: "A Commander game may be a two-player game or a multiplayer game. The default multiplayer setup is the Free-for-All variant with the attack multiple players option…"
**Rule:** CR 903.7, CR 903.2 — run `mtg rule 903.7`
**Why it matters in your decks:** 40 life means games are *long*. That's why all three decks lean on engines (counters, draw, Junk tokens) rather than fast damage — and why chip damage from one attacker rarely matters.

### The command zone
**In plain English:** A special zone outside the game where your commander sits at the start and returns to. Your commander is never really gone.
**Official:** "A zone for certain specialized objects that have an overarching effect on the game, yet are not permanents and cannot be destroyed. See rule 408, 'Command.'"
**Rule:** CR 408, and CR 903.9 for returning — run `mtg rule 903.9`

### Commander returning to the command zone
**In plain English:** If your commander would die, be exiled, go to hand, or go to library — you may put it back in the command zone instead.
**Official:** CR 903.9a: "If a commander is in a graveyard or in exile and that object was put into that zone since the last time state-based actions were checked, its owner may put it into the command zone. This is a state-based action." CR 903.9b: "If a commander would be put into its owner's hand or library from anywhere, its owner may put it into the command zone instead."
**Rule:** CR 903.9, 903.9a, 903.9b — run `mtg rule 903.9`
**Why it matters in your decks:** It's a *choice*, not automatic. Sometimes you'd rather leave Dogmeat in the graveyard than pay commander tax again — but usually you take the command zone, because recasting is how you re-trigger his ETB mill-and-return.

### Commander tax
**In plain English:** Every time you recast your commander from the command zone, it costs `{2}` more than the last time. Second cast +{2}, third cast +{4}, and so on.
**Official:** "A player may cast a commander they own from the command zone. A commander cast from the command zone costs an additional {2} for each previous time the player casting it has cast it from the command zone that game. This additional cost is informally known as the 'commander tax.'"
**Rule:** CR 903.8 — run `mtg rule 903.8`
**Why it matters in your decks:** Tidus and Dogmeat both cost `{3}` (mana value 3), Bumbleflower `{1}{G}{W}{U}` (mana value 4). By the third cast you're paying 7 or 8. Protecting your commander (dogmeat's **Swiftfoot Boots**, **Champion's Helm**, **Heroic Intervention**) is cheaper than recasting it.

### Commander damage (21)
**In plain English:** A second way to lose. If a *single* commander has dealt you 21 or more **combat damage** across the whole game, you lose — even at high life. Damage from each commander is tracked separately.
**Official:** "A player who's been dealt 21 or more combat damage by the same commander over the course of the game loses the game. (This is a state-based action. See rule 704.)"
**Rule:** CR 903.10, CR 903.10a — run `mtg rule 903.10`
**Why it matters in your decks:** It must be **combat** damage from the commander itself. Tidus is a 3/3 and Dogmeat a 3/3, so on paper that's seven connections — but tidus stacks +1/+1 counters and dogmeat straps on Auras and Equipment, which is exactly how a 3/3 commander gets there in three or four swings. Track it out loud; nobody remembers otherwise.

### Color identity
**In plain English:** The colors your commander "is," counting every mana symbol in its cost *and* its rules text. Every card in your deck must fit inside it.
**Official:** "The Commander variant uses color identity to determine what cards can be in a deck with a certain commander. The color identity of a card is the color or colors of any mana symbols in that card's mana cost or rules text, plus any colors defined by its characteristic-defining abilities … or color indicator." And CR 903.5c: "A card can be included in a Commander deck only if every color in its color identity is also found in the color identity of the deck's commander."
**Rule:** CR 903.4, CR 903.5c — run `mtg rule 903.4`
**Why it matters in your decks:** tidus and bumbleflower are both **WUG** (white/blue/green, "Bant"); dogmeat is **WRG** (white/red/green, "Naya"). Confirmed by `mtg deck stats <slug>`. This is why `mtg merge tidus bumbleflower --commander "..."` can pool cards between those two but not freely with dogmeat.

### Singleton (the 100-card rule)
**In plain English:** Exactly 100 cards including your commander, and no two cards may share a name — except basic lands, which are unlimited. Note: "singleton" is player slang; `mtg glossary singleton` returns *not in my data*. The real rule is CR 903.5.
**Official:** CR 903.5a: "Each deck must contain exactly 100 cards, including its commander. In other words, the minimum deck size and the maximum deck size are both 100." CR 903.5b: "Other than basic lands, each card in a Commander deck must have a different English name."
**Rule:** CR 903.5, 903.5a, 903.5b — run `mtg rule 903.5`
**Why it matters in your decks:** `mtg status` confirms each of your decks is 99 main + 1 commander = 100. It also means **you will never reliably draw a specific card** — which is why your decks are built around repeatable engines rather than one combo piece.

### No sideboards
**In plain English:** Commander has no sideboard. You have one deck, and it does not change between games.
**Official:** "Commander games do not use sideboards."
**Rule:** CR 903.5e — run `mtg rule 903.5e`

### Mulligan (the London mulligan)
**In plain English:** Unhappy with your opening seven? Shuffle back, draw a fresh **seven**, then put a number of cards on the bottom equal to how many mulligans you've taken — **except that your first mulligan is free**, because a Commander game is normally a multiplayer game (CR 903.2: the default setup is Free-for-All; CR 800.1: "A multiplayer game is a game that begins with more than two players") and CR 103.5c makes the first mulligan in a multiplayer game not count. So at a normal Commander table:

| Mulligan | You draw | You bottom | You keep |
|---|---|---|---|
| #1 | 7 | **0 — it's free** | **7** |
| #2 | 7 | 1 | 6 |
| #3 | 7 | 2 | 5 |

You still choose *which* cards go to the bottom, and you see all seven before choosing. Because #1 costs you nothing, a genuinely bad opener is never worth keeping.
**Official:** "To take a mulligan is to reject a prospective opening hand in favor of a new one." And CR 103.5: "…To take a mulligan, a player shuffles the cards in their hand back into their library, draws a new hand of cards equal to their starting hand size, then puts a number of those cards equal to the number of times that player has taken a mulligan on the bottom of their library in any order…" And CR 103.5c, which is the one that actually governs your games: "In a multiplayer game and in any Brawl game, the first mulligan a player takes doesn't count toward the number of cards that player will put on the bottom of their library or the number of mulligans that player may take. Subsequent mulligans are counted toward these numbers as normal."
**Rule:** CR 103.5 (the general procedure), **CR 103.5c** (the free first mulligan in multiplayer — this is the one that applies to you), CR 800.1 (what "multiplayer" means), CR 903.2 (Commander's default is multiplayer Free-for-All) — run `mtg rule 103.5` and `mtg rule 103.5c`
**Why it matters in your decks:** Your decks run 37–38 lands. A beginner-safe keep is **3–5 lands** with something to do on turns 2 and 3. Mulligan a one-lander or a six-lander without hesitation — the first one is free — and you can practice the decision with `mtg deck goldfish tidus --mulligans 1 --bottom worst-lands`.

---

## Deckbuilding vocabulary (player slang, not official rules)

**None of the five terms below has a Comprehensive Rules glossary entry.** Verified: `mtg glossary ramp`, `mtg glossary tutor`, `mtg glossary removal`, `mtg glossary "board wipe"`, and `mtg glossary "card advantage"` all return either *not in my data* or unrelated near-matches. They are how players talk, and they're the categories `mtg deck stats <slug>` scores your decks on.

### Ramp
**In plain English:** Cards that get you extra mana faster than one-land-per-turn — mana rocks, land fetch, creatures that tap for mana.
**Official:** No glossary entry (`mtg glossary ramp` returns only *Rampage*, an unrelated keyword).
**Rule:** No clean CR number — it's a deckbuilding category, not a game rule.
**Why it matters in your decks:** tidus 12, bumbleflower 14, dogmeat 11 ramp pieces (`mtg deck stats <slug> -v`). All three run **Sol Ring** and **Arcane Signet**. Playing ramp on turns 1–3 is almost always right.

### Card advantage
**In plain English:** Having more cards to work with than everyone else. Drawing extra cards, or trading one card for two of theirs.
**Official:** No glossary entry.
**Rule:** No CR number.
**Why it matters in your decks:** bumbleflower has **25** draw pieces — it is a card-advantage deck first. dogmeat has 8; it wins by grinding value out of Junk tokens instead.

### Removal
**In plain English:** A spell that answers one specific permanent — kill the creature, blow up the artifact.
**Official:** No glossary entry (`mtg glossary removal` → *not in my data*).
**Rule:** No CR number.
**Why it matters in your decks:** tidus 8, bumbleflower 4, dogmeat 4 (`mtg deck stats`). That's *thin*. Save removal for genuine threats — an opponent's commander, or a creature that will kill you.

### Board wipe
**In plain English:** One spell that destroys or exiles many permanents at once. Resets the whole table.
**Official:** No glossary entry.
**Rule:** No CR number.
**Why it matters in your decks:** tidus 4 (incl. **Farewell**), bumbleflower 2, dogmeat 1. Since your decks build up boards over time, someone else's board wipe is your biggest risk — don't overcommit creatures when a table has open mana.

### Tutor
**In plain English:** A card that searches your library for a specific non-land card.
**Official:** No glossary entry (`mtg glossary tutor` → *not in my data*).
**Rule:** No CR number.
**Why it matters in your decks:** All three decks run **zero** tutors (`mtg deck stats <slug> -v` → `tutor 0`). Combined with the singleton rule, that means you genuinely cannot plan around drawing any one card. Play what you draw.

---

## Table talk (more player slang, also not official rules)

**Every term in this section is slang.** Each was checked against the local database and none has a
Comprehensive Rules glossary entry — `mtg glossary pip`, `flood`, `fixing`, `clock`, `interaction`,
`"alpha strike"`, `pillowfort`, `midrange`, and `aggro` all return *not in my data* or unrelated
near-matches. **They carry no CR citation, on purpose.** Where an official term exists for the same
idea, it's named and cited so you can chase the real rule.

### Pip
**In plain English:** One mana symbol in a cost. `{1}{G}{W}{U}` has three colored pips; `{2}{W}{W}` has a "double white pip." The pip count, not the mana value, is what tells you how hard a card is to cast.
**Official:** **Slang — not an official term.** `mtg glossary pip` → *not in my data*, and `mtg rule "pip"` → *not in my data: any rule mentioning 'pip'*. The official term for the symbol itself is **mana symbol**: "An icon that represents mana or a mana cost. See rule 107.4." CR 107.4a: "There are five primary colored mana symbols… Colored mana in costs can be paid only with the appropriate color of mana."
**Rule:** No CR number for the slang. The underlying official rule is CR 107.4 / 107.4a — run `mtg rule 107.4`
**Why it matters in your decks:** **Ms. Bumbleflower** costs `{1}{G}{W}{U}` — three *different* colored pips, so you need all three colors online by turn 4, not just four mana. `mtg deck stats bumbleflower` gives 20 white / 19 blue / 19 green sources across 38 lands. Double pips are the other trap: **Baird, Steward of Argive** (`{2}{W}{W}`) and **Perch Protection** (`{4}{W}{W}`) are meaningfully harder in a three-color deck than their mana values suggest.

### Flood / flooding out
**In plain English:** Drawing far more lands than you can use, so you spend turns doing nothing while the table develops. The opposite is being "screwed" (too few lands).
**Official:** **Slang — not an official term.** `mtg glossary flood` → *not in my data*.
**Rule:** No CR citation — it's an outcome, not a rule.
**Why it matters in your decks:** `mtg deck stats` uses this exact word on **two of your three decks**. bumbleflower (38 lands, avg MV 3.21): *"38 lands is 1 above the 36-37 band — expect flood; consider trimming for card advantage (deck has 25 draw pieces)."* dogmeat (38 lands, avg MV 2.82): *"38 lands is 2 above the 34-36 band — expect flood; consider trimming for card advantage (deck has 8 draw pieces)."* tidus at 37 is rated **SANE**. The practical read: bumbleflower floods but has 25 draw pieces to dig out of it; **dogmeat floods with only 8**, so it is the deck most likely to stall out drawing lands. That is also the argument for the free first mulligan on a six-land opener.

### Fixing (mana fixing)
**In plain English:** Making sure you have the right **colors**, as opposed to ramp, which gets you **more mana**. A land that taps for any color fixes; a Sol Ring ramps but fixes nothing.
**Official:** **Slang — not an official term.** `mtg glossary fixing` → *not in my data*.
**Rule:** No CR citation. The rule it works against is color identity, CR 903.4 / 903.5c (see **[Color identity](#color-identity)** above).
**Why it matters in your decks:** `mtg deck stats` folds fixing into the ramp role — *"ramp — accelerates or fixes mana (land fetch, mana rocks, dorks, Treasure)."* All three decks are three colors, so fixing is not optional. Your any-color lands, listed by `mtg deck stats`: **Command Tower, Exotic Orchard, Path of Ancestry** in tidus and dogmeat; **Command Tower, Exotic Orchard** in bumbleflower. The scry Temples each fix two colors but enter tapped, which is why tidus has 16 tapped lands and dogmeat 12. Color sources, verified: tidus W20/U19/G20, bumbleflower W20/U19/G19, dogmeat W16/R16/G18 — dogmeat is the thinnest on any one color.

### Clock
**In plain English:** How many turns your board needs to kill a specific opponent. "A four-turn clock" means they die in four more turns if nothing changes. Used to decide whether to race someone or answer them.
**Official:** **Slang — not an official term.** `mtg glossary clock` → *not in my data*.
**Rule:** No CR citation.
**Why it matters in your decks:** Starting life is **40** (CR 903.7, above), so clocks in Commander are slow and there are two of them running at once — the life clock and the **commander damage** clock at 21 (CR 903.10). **Tidus, Yuna's Guardian** and **Dogmeat, Ever Loyal** are both 3/3s (`mtg card "<name>"`), which is a 14-turn life clock and a 7-turn commander clock — useless on its own. Everything tidus does with +1/+1 counters and everything dogmeat does with Auras and Equipment exists to shorten that number. When you're deciding whether to hold up removal, ask "what's their clock on me?" before "is that scary?".

### Interaction
**In plain English:** Cards that let you affect what *other people* are doing — counterspells, instant-speed removal, protection tricks. A deck with no interaction can only race.
**Official:** **Slang — not an official term** as a deckbuilding category. `mtg glossary interaction` returns no exact entry — only *Layer* and *Base Power, Base Toughness*, which point at CR 613, "Interaction of Continuous Effects." That is a completely different subject (the layer system) and is **not** what players mean by this word.
**Rule:** No CR citation for the slang sense.
**Why it matters in your decks:** It's a scored role in `mtg deck stats`, sitting next to removal: tidus **3** interaction / 8 removal, bumbleflower **6** / 4, dogmeat **6** / 4. tidus has the fewest ways to act on someone else's turn, which is the deck where you most need to hold up **An Offer You Can't Refuse** instead of tapping out. See **[In response](#in-response)** and **[Instant speed vs. sorcery speed](#instant-speed-vs-sorcery-speed)** above — interaction is only interaction if you have the mana up when it matters.

### Alpha strike
**In plain English:** Attacking with your entire board at once, holding nothing back.
**Official:** **Slang — not an official term.** `mtg glossary "alpha strike"` returns no exact entry — only *First Strike* and *Double Strike*, which are unrelated keyword abilities.
**Rule:** No CR citation.
**Why it matters in your decks:** In a four-player game an alpha strike taps your whole board (attacking taps — CR 508, CR 701.26 above), and then **two opponents you didn't attack still get their turns** before you untap. That is how beginners lose Commander games they were winning. Two mitigations you already own: **vigilance** (6 creatures in bumbleflower, 3 in tidus, 3 in dogmeat — see the keyword table above) lets you swing and still block, and Baird below taxes anyone who tries it against you.

### Pillowfort
**In plain English:** Cards that make attacking *you* expensive or impossible, so the table goes after somebody else. It's a tax, not a wall — a determined opponent just pays.
**Official:** **Slang — not an official term.** `mtg glossary pillowfort` → *not in my data*.
**Rule:** No CR citation.
**Why it matters in your decks:** Verified with `mtg search "deck:<slug> unless their controller pays"` — you own exactly two, one each in tidus and bumbleflower, and **none in dogmeat**. bumbleflower: **Baird, Steward of Argive**, *"Creatures can't attack you or planeswalkers you control unless their controller pays {1} for each of those creatures"* — permanent, and it has vigilance itself. tidus: **Summon: Yojimbo** chapters II and III, *"Until your next turn, creatures can't attack you unless their controller pays {2} for each of those creatures"* — stronger per creature but only for two turns, and then the Saga sacrifices itself. Both are strongest when you're the visible threat at the table and want the aggression pointed elsewhere.

### Midrange
**In plain English:** A deck that neither races to kill early nor sits back controlling — it plays efficient threats on curve and takes over the middle turns. The default shape of a preconstructed Commander deck.
**Official:** **Slang — not an official term.** `mtg glossary midrange` → *not in my data*.
**Rule:** No CR citation.
**Why it matters in your decks:** **All three of your decks are midrange**, and the numbers say so: average non-land mana value 3.03 (tidus), 3.21 (bumbleflower), 2.82 (dogmeat), with the curve peaking at 2–3 in every deck, **0 tutors** in all three, and engines rather than combos as the win route (`mtg deck stats <slug>`). That's the honest expectation to bring to your first games: you are not going to kill anyone on turn 5, and you are not going to lock the table down either. You build a board, you draw cards, and you look for the turn the engine outgrows everyone.

### Aggro
**In plain English:** A deck built to knock someone's life total down fast with cheap creatures, accepting that it runs out of gas if the game goes long.
**Official:** **Slang — not an official term.** `mtg glossary aggro` → *not in my data*.
**Rule:** No CR citation.
**Why it matters in your decks:** **dogmeat is the closest thing you own** — 11 one-drops, the lowest curve of the three (avg MV 2.82), and the most tapped-land-light mana base (12 tapped lands, 32%). But true aggro doesn't work here: 40 starting life (CR 903.7) across three opponents is 120 life on the table, and killing one player doesn't win. Dogmeat's real plan is the value engine — 6 recursion pieces and the Junk tokens — with the low curve serving to get enchanted and equipped creatures attacking early, not to burn someone down. Play it as fast midrange, not as aggro.

---

## How to look anything up

Everything above came from the local database. Nothing here needs the internet (only `mtg rebuild` does).

```bash
cd /Users/omaralatas/Work/personal/mtg-brain

# A term — official glossary definition plus the rules it points at
./bin/mtg glossary trample
./bin/mtg glossary "state-based action"

# A rule by number — prints the parent rule and all child subrules
./bin/mtg rule 903.10          # commander damage
./bin/mtg rule 122             # counters (the markers)
./bin/mtg rule 701.6           # counter (the verb)

# A rule by what you remember of the wording — full-text search
./bin/mtg rule "play a land only during their main phase"
./bin/mtg rule "lethal damage" --limit 5

# A card — full text plus every official ruling Wizards has published on it
./bin/mtg card "Dogmeat, Ever Loyal"
./bin/mtg card Rancor --no-rulings

# What's actually in your decks
./bin/mtg deck dogmeat                          # full decklist by type
./bin/mtg deck stats dogmeat -v                 # curve, colors, role counts
./bin/mtg search "deck:dogmeat is:equipment"    # every Equipment in the deck
./bin/mtg search "deck:tidus proliferate"       # every proliferate card
./bin/mtg search "deck:bumbleflower cmc<=2 legal:commander"

# Practice a draw without a table
./bin/mtg deck goldfish tidus --turns 6
./bin/mtg deck goldfish tidus --seed 7 --mulligans 1 --bottom worst-lands

# When you get a rule wrong in a real game, log it so it stops happening
./bin/mtg log rule --rule 702.6a --note "tried to equip mid-combat; equip is sorcery-speed only"
./bin/mtg log rule --list
```

**If the database can't answer, it says so** — `not in my data`. That's the correct answer, not a
prompt to guess. Do not accept a card text, a mana cost, or a rule number that didn't come out of
one of these commands.
