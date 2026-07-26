# Scrappy Survivors — Pilot Primer

**Commander:** Dogmeat, Ever Loyal · **Colors:** Naya (White / Red / Green, identity `WRG`)
**Set:** PIP (released 2024-03-08) · **Deck slug:** `dogmeat` · **Estimated Bracket:** 2 (Core)

> Every card fact, cost, type line, and rule number in this document was pulled live from the
> local database in the session that wrote it (`mtg card`, `mtg search "deck:dogmeat"`,
> `mtg rule`, `mtg glossary`). Nothing here is written from memory.
>
> This is a **Commander (EDH)** document. Commander has **no sideboard** — the 100 cards you
> shuffle up are the only cards you get.

---

## Jargon you will hit in the first paragraph

Read these once. They come up constantly in this deck.

| Term | What it means (from `mtg glossary` / `mtg rule`) |
|---|---|
| **Aura** | An enchantment subtype. Aura spells *target* something, and once they resolve they are **attached** to it. (`mtg glossary aura`, rules 303 / 702.5) |
| **Equipment** | An artifact subtype. It sits on the battlefield **unattached** until you pay its **equip** cost. |
| **Equip** | `"Equip [cost]" means "[Cost]: Attach this permanent to target creature you control. Activate only as a sorcery."` (CR 702.6a). "Only as a sorcery" = **your turn, main phase, nothing else on the stack.** You cannot equip mid-combat or on someone else's turn. |
| **Attached** | The Aura/Equipment is physically slid under the creature. It is "on" that creature. |
| **Mill** | `"To mill a number of cards, a player puts that many cards from the top of their library into their graveyard."` (`mtg glossary mill`, CR 701.17) |
| **Junk token** | `"A Junk token is a colorless artifact token with '{T}, Sacrifice this token: Exile the top card of your library. You may play that card this turn. Activate only as a sorcery.'"` (`mtg glossary "Junk Token"`, CR 111.10t) — this deck's main card-advantage engine. |
| **Modified** | `"A modified creature is a creature that has a counter on it, is equipped, or is enchanted by an Aura its controller also controls."` (`mtg glossary modified`, CR 700.9) |
| **Trample** | Excess combat damage over the blocker's toughness spills through to the defending player. (`mtg glossary trample`, CR 702.19) |
| **Hexproof** | Can't be targeted by *your opponents'* spells and abilities. You can still target it yourself. (`mtg glossary hexproof`, CR 702.11) |
| **Indestructible** | Can't be destroyed. Damage and the word "destroy" don't kill it. (`mtg glossary indestructible`, CR 702.12) |
| **Menace** | Can't be blocked except by two or more creatures. (`mtg glossary menace`, CR 702.111) |
| **Goaded** | `"A goaded creature attacks each combat if able and attacks a player other than the controller of the permanent, spell, or ability that caused it to be goaded if able."` (CR 701.15b; `mtg glossary goad` points there). In plain terms: **when *you* goad something, it must attack someone other than you** — but if an *opponent* goads a creature, it must avoid *them*, not you. You put this on an *opponent's* creature. |
| **Rad counter** | A counter a **player** gets. `"At the beginning of each player's precombat main phase, if that player has one or more rad counters, that player mills a number of cards equal to the number of rad counters they have. For each nonland card milled this way, that player loses 1 life and removes one rad counter from themselves."` (CR 728.1) |

---

## 1. What this deck is trying to do

This deck plays a pile of cheap **Auras and Equipment** (17 enchantments and 17 artifacts out of 61
non-land cards — more than half the spells in the deck), stacks several of them onto one or two
creatures, and turns those creatures into something far bigger than their printed size. The payoff
cards get better for *every* attachment: **All That Glitters** (`{1}{W}`) gives the enchanted creature
`+1/+1 for each artifact and/or enchantment you control`, and **Strong Back** (`{2}{G}`) gives
`+2/+2 for each Aura and Equipment attached to it`.

The engine that stops this from being a "one creature, one removal spell, I lose" deck is your
commander. **Dogmeat, Ever Loyal** turns every attack by a dressed-up creature into a **Junk token**,
which exiles the top card of your library and lets you play it that turn. So attacking *draws you
cards* (functionally), and this deck is built to attack every turn.

The third pillar is **recursion** — bringing Auras and Equipment back after your creature dies. Dogmeat
itself does it on entry. So do **Super Mutant Scavenger**, **Brotherhood Outcast**, **Cass, Hand of
Vengeance**, **Pre-War Formalwear**, and **Mantle of the Ancients**. The deck expects to lose creatures
and rebuild.

**In one sentence:** attack with a heavily-equipped creature every single turn, convert those attacks
into Junk tokens and free cards, and rebuild from the graveyard when they kill your guy.

> **The name is flavor, not strategy.** "Scrappy Survivors" is a Fallout theme. Derived from the actual
> list, this is an **Auras-and-Equipment attackers deck** (sometimes called "Voltron-ish" — piling
> buffs onto a creature), not a sacrifice deck and not a token swarm.

---

## 2. Your commander

### Full card, exactly as printed

```
── Dogmeat, Ever Loyal ───────────────────────────────────────────────────
Mana cost      : {R}{G}{W}
Mana value     : 3
Type           : Legendary Creature — Dog

When Dogmeat enters, mill five cards, then return an Aura or Equipment card
from your graveyard to your hand.
Whenever a creature you control that's enchanted or equipped attacks, create
a Junk token. (It's an artifact with "{T}, Sacrifice this token: Exile the
top card of your library. You may play that card this turn. Activate only as
a sorcery.")

P/T            : 3/3
```

### What that actually means at the table

**The cost `{R}{G}{W}` is three *different* colored pips.** You cannot cast Dogmeat off three Forests.
You need one red source, one green source, and one white source, all untapped, on the same turn. This
is the single biggest practical constraint on the deck. Your deck has **16 white sources, 16 red
sources, and 18 green sources** among 38 lands (from `mtg deck stats dogmeat -v`), plus
**Command Tower** (`{T}: Add one mana of any color in your commander's color identity.`),
**Arcane Signet** (same text, `{2}` artifact), **Exotic Orchard**, **Jungle Shrine**
(`{T}: Add {R}, {G}, or {W}.`), and **Path of Ancestry**.

**Ability 1 — the enter-the-battlefield trigger.** `mill five cards, then return an Aura or Equipment
card from your graveyard to your hand.` Milling yourself sounds bad; here it is **upside**. Five cards
into your graveyard, in a deck with 34 Auras and Equipment, means you very often bin one and
immediately take it back. Official ruling (`mtg card "Dogmeat, Ever Loyal"`, 2024-03-08):

> *"The card you return with Dogmeat's first ability doesn't have to be one of the cards you milled
> with that ability."*

So if you already had a good Aura in the yard, you can grab that instead. And everything else you mill
is live fuel for **Cass, Hand of Vengeance**, **Mantle of the Ancients**, **Super Mutant Scavenger**,
**Brotherhood Outcast**, **Pre-War Formalwear**, and **Buried Ruin**.

**Ability 2 — the engine.** `Whenever a creature you control that's enchanted or equipped attacks,
create a Junk token.` Read it carefully:

- It triggers on **each** qualifying attacker, not once per combat. Three dressed-up attackers = three
  Junk tokens.
- The creature must be **enchanted or equipped at the moment attackers are declared**. An Equipment
  sitting unattached on the battlefield does nothing. Equip *before* combat (equip is sorcery-speed,
  CR 702.6a — so it must happen in your precombat main phase).
- Dogmeat counts itself if Dogmeat is enchanted or equipped and attacks.
- Junk tokens arrive **during combat**, after your precombat main phase. See the piloting note below.

**Junk token timing — the most useful trick in this deck.** A Junk token's ability is
`Activate only as a sorcery`, so you can only crack it in a main phase on your turn with an empty
stack. Since the tokens are *created during combat*, that means your **postcombat (second) main
phase**. Two official rulings matter (`mtg card "Junk Jet"`, 2024-03-08):

> *"You pay all costs and follow all normal timing rules for the card played from exile with a Junk
> token's ability. For example, if the exiled card is a land card, you may play it only during your
> main phase while the stack is empty."*

> *"You can't sacrifice a Junk token to pay multiple costs."*

**Practical consequence: on turns where you plan to attack with dressed-up creatures, consider holding
your land drop until your second main phase.** If a Junk token exiles a land, you can still play it —
but only if you haven't already used your land drop for the turn. Also leave a little mana unspent
before combat so you can actually *cast* whatever the Junk tokens exile.

### If Dogmeat dies — the commander tax

When your commander dies, is exiled, or is put into your library or hand, you may put it into the
**command zone** instead, and cast it again from there. Each recast costs more:

> **CR 903.8** — *"A player may cast a commander they own from the command zone. A commander cast from
> the command zone costs an additional {2} for each previous time the player casting it has cast it
> from the command zone that game. This additional cost is informally known as the 'commander tax.'"*

So Dogmeat costs `{R}{G}{W}` the first time, `{2}{R}{G}{W}` the second time, `{4}{R}{G}{W}` the third
time. Three casts is realistic; four is painful. Note that **the tax is generic mana** — the colored
requirement never changes, so you still need R, G *and* W every single time.

There's also a hard win-condition rule you should know because this deck can reach it:

> **CR 903.10a** — *"A player who's been dealt 21 or more combat damage by the same commander over the
> course of the game loses the game."*

### Cast it early or hold it?

**Cast it early — turn 3 or 4 if the mana allows it.** Reasons, in order:

1. Dogmeat is only `{R}{G}{W}` (mana value 3) and is a 3/3 body. It is cheap for what it does.
2. The enter trigger (mill 5, return an Aura/Equipment) is card advantage you want *early*, when
   your hand is thin.
3. The Junk engine only produces value on turns you attack, so every turn Dogmeat isn't out is a turn
   you generate nothing.
4. Bracket 2 tables (see §8) do not run wall-to-wall removal. You will usually get a couple of attacks
   in before someone answers it.

**The exception:** if an opponent is visibly holding up removal and you have no protection, and you
have a fine turn without Dogmeat (say, casting **Puresteel Paladin** and equipping something), take
the fine turn. You have **Swiftfoot Boots** (`{2}`, `Equipped creature has hexproof and haste`,
`Equip {1}`) and **Champion's Helm** (`{3}`, `Equipped creature gets +2/+2. As long as equipped
creature is legendary, it has hexproof. Equip {1}`) — Dogmeat is legendary, so Champion's Helm is a
proper protective helmet for it. **Codsworth, Handy Helper** (`{2}{W}`) also passively protects it:
`Commanders you control have ward {2}` (ward = a triggered ability that counters a targeting spell or
ability unless its controller pays the cost — `mtg glossary ward`, CR 702.21).

---

## 3. The turn-by-turn shape

**Deck math you should internalise** (from `mtg deck stats dogmeat -v`):

- 38 lands, 61 non-lands. Average mana value of non-lands = **2.82**. Curve: 11 one-drops, 18 two-drops,
  18 three-drops, 5 fours, 6 fives, 2 sixes, 1 at seven-plus.
- **12 of your 38 lands can enter tapped** (7 always, 5 conditional) = 32% of the mana base.
- Total mana sources = 38 lands + 11 ramp pieces = 49.

That means: **this is a cheap deck with a slow mana base.** You will usually have things to cast; the
question is whether the right colors are online.

### Turns 1–3 — set up cheap attachments, land Dogmeat

**What good looks like:**

- **T1:** Land, then ideally a one-mana artifact. The best T1 play in the deck is **Sol Ring**
  (`{1}`, `{T}: Add {C}{C}.`) — it is the single most powerful card in the 99 and doubles your mana
  from turn 2 onward. Failing that: **Basilisk Collar** (`{1}`, `Equipped creature has deathtouch and
  lifelink`, `Equip {2}`), **Bloodforged Battle-Axe** (`{1}`, `Equipped creature gets +2/+0`,
  `Equip {2}`), **Explorer's Scope** (`{1}`, `Equip {1}`), **Pip-Boy 3000** (`{1}`, `Equip {2}`),
  **Masterwork of Ingenuity** (`{1}`), or a one-mana Aura on a land: **Wild Growth** (`{G}`),
  **Abundant Growth** (`{G}`, `When this Aura enters, draw a card. Enchanted land has "{T}: Add one
  mana of any color."`).
- **T2:** Land, then **Puresteel Paladin** (`{W}{W}`, 2/2, `Whenever an Equipment you control enters,
  you may draw a card.` / `Metalcraft — Equipment you control have equip {0} as long as you control
  three or more artifacts.`) is the dream. Or **Arcane Signet** (`{2}`), **Mister Gutsy** (`{2}`,
  `Whenever you cast an Aura or Equipment spell, put a +1/+1 counter on this creature.`),
  **Cait, Cage Brawler** (`{R}{G}`), or **Fertile Ground** (`{1}{G}`).
- **T3:** **Cast Dogmeat.** Mill five, take back an Aura or Equipment, and pass with a 3/3 on board.
  If you can't produce all three colors, cast **Codsworth, Handy Helper** (`{2}{W}`),
  **Armory Paladin** (`{1}{R}{W}`, 3/3 trample, `Whenever you cast an Aura or Equipment spell, exile
  the top card of your library. You may play that card until the end of your next turn.`),
  **Veronica, Dissident Scribe** (`{2}{R}`, 3/3 menace), or **Moira Brown, Guide Author** (`{1}{R}{W}`)
  instead.

**If the game is going badly at this stage** (one or two lands, or missing a color): stop trying to
force Dogmeat. Play the colorless artifacts you *can* cast — Sol Ring, Basilisk Collar, Bloodforged
Battle-Axe, Explorer's Scope, Pip-Boy 3000, Masterwork of Ingenuity, Silver Shroud Costume, Swiftfoot
Boots — and dig for lands. **Explorer's Scope** (`Whenever equipped creature attacks, look at the top
card of your library. If it's a land card, you may put it onto the battlefield tapped.`) is a genuine
land-finder here; equipping it to any 1/1 and attacking is a real play. Also remember
**Ash Barrens** has `Basic landcycling {1}` — for one mana you can discard it and fetch a basic to
hand, which is a colour-fixing safety valve.

### Turns 4–6 — dress a creature and start attacking

This is where the deck actually operates. A good turn 5 looks like:

Dogmeat is out. You attack with Dogmeat carrying **Behemoth Sledge** (`{1}{G}{W}`, `Equipped creature
gets +2/+2 and has trample and lifelink. Equip {3}`) — that's a 5/5 trampling lifelinker. Dogmeat's
second ability triggers and you get a Junk token. In your second main phase you crack the Junk token,
exile the top card, and cast it if it's cheap. You gained 5 life, dealt 5, and drew a card's worth of
value, all off one attack.

Cards you specifically hope to be deploying in this window:

- **All That Glitters** (`{1}{W}`) — with Dogmeat, 2 Equipment and 2 other artifacts out, that's easily
  +5/+5.
- **Strong Back** (`{2}{G}`) — read the whole card: `Equip abilities you activate that target enchanted
  creature cost {3} less to activate. Aura spells you cast that target enchanted creature cost {3} less
  to cast. Enchanted creature gets +2/+2 for each Aura and Equipment attached to it.` Official ruling
  (2024-03-08): *"Strong Back's abilities reduce only the amount of generic mana in equip abilities that
  target the enchanted creature and in the total cost of Aura spells that target the enchanted creature.
  For example, it will reduce the total cost of Animal Friend from {1}{G} to {G}."* It makes Behemoth
  Sledge's `Equip {3}` free.
- **Rancor** (`{G}`, `Enchanted creature gets +2/+0 and has trample.` `When this Aura is put into a
  graveyard from the battlefield, return it to its owner's hand.`) — the safest Aura in the deck,
  because it comes back when the creature dies.
- **Preston Garvey, Minuteman** (`{2}{R}{G}{W}`, 4/4) — `At the beginning of combat on your turn, create
  a green Aura enchantment token named Settlement attached to up to one target land you control. It has
  enchant land and "Enchanted land has '{T}: Add one mana of any color.'"` / `Whenever Preston Garvey
  attacks, untap each enchanted permanent you control.` This is ramp *and* fixing *and* it untaps your
  enchanted lands when he swings.
- **Cass, Hand of Vengeance** (`{2}{R}{W}`, 4/3 vigilance) — your insurance policy, see §6.

**If the game is going badly here** — meaning your creatures keep dying and you're being 2-for-1'd —
change gear. Stop over-committing Auras. Play the Equipment (Equipment survives when the creature dies;
Auras go to the graveyard, CR 704.5m: *"If an Aura is attached to an illegal object or player, or is not
attached to an object or player, that Aura is put into its owner's graveyard."*). Hold
**Heroic Intervention** (`{1}{G}`, `Permanents you control gain hexproof and indestructible until end of
turn.`) — this is your one big protection spell and it saves the entire board, not just one creature.

### Turn 7+ — convert to a real threat, or grind

By now you should be either (a) attacking every turn with a huge creature, or (b) rebuilding. The
top-end cards that close games:

- **Mantle of the Ancients** (`{3}{W}{W}`) — `When this Aura enters, return any number of target Aura
  and/or Equipment cards from your graveyard to the battlefield attached to enchanted creature.
  Enchanted creature gets +1/+1 for each Aura and Equipment attached to it.` If you've lost two
  creatures, this reassembles the whole pile in one card.
- **Almost Perfect** (`{4}{G}{W}`) — `Enchanted creature has base power and toughness 9/10 and has
  indestructible.` Turns anything into a 9/10 that survives most board wipes. Ruling (2024-03-08):
  *"Effects that modify a creature's power and/or toughness … will apply to the creature no matter
  when they started to take effect."* So Behemoth Sledge's +2/+2 stacks on top → 11/12.
- **Grim Reaper's Sprint** (`{4}{R}`) — `Morbid — This spell costs {3} less to cast if a creature died
  this turn.` / `When this Aura enters, untap each creature you control. If it's your main phase, there
  is an additional combat phase after this phase.` / `Enchanted creature gets +2/+2 and has haste.`
  **This is your surprise-kill card**: an extra combat phase with everything untapped. Cast it in your
  *postcombat main phase* to get a second attack.
- **Vault 101: Birthday Party** (`{3}{W}`, Saga) — chapters II and III each let you `put an Aura or
  Equipment card from your hand or graveyard onto the battlefield` for free.

**If the game is going badly at turn 7+** — you're behind on board and someone else is threatening to
win — your outs are the sweepers and the big single-target answers, not more Auras:
**Blasphemous Act** (`{8}{R}`, `This spell costs {1} less to cast for each creature on the battlefield.
Blasphemous Act deals 13 damage to each creature.` — in a real four-player game with 9 creatures out
that costs `{R}`), **Single Combat** (`{3}{W}{W}`, `Each player chooses a creature or planeswalker they
control, then sacrifices the rest. Players can't cast creature or planeswalker spells until the end of
your next turn.`), and **Megaton's Fate** (`{5}{R}`, `Detonate — Megaton's Fate deals 8 damage to each
creature. Each player gets four rad counters.`).

Note the synergy: **Almost Perfect** makes its creature indestructible, so *you* survive your own
Blasphemous Act. **Single Combat** lets you keep your one dressed-up creature and forces everyone else
down to one — that is often a game-winning asymmetric wipe for this deck specifically.

---

## 4. How you actually win

**You win by attacking.** There is no alternate win condition, no infinite combo, and no burn plan in
this list. The deck has **2 cards tagged as win conditions** by `mtg deck stats` (Grim Reaper's Sprint
and Junk Jet) and **0 tutors** — you cannot go find your best card. You draw what you draw and you
attack with it.

**Be honest about the clock: this deck is not fast.** Its own bracket assessment says games at this
level "typically end around turn 9 or later." Your realistic plan is to start attacking around turn 5
and to kill one player at a time, or to accumulate damage across the table while your Junk tokens keep
your hand full.

### The three concrete ways games end

**(a) One giant trampler.** Stack attachments on a creature with trample and swing. Trample means damage
above the blocker's toughness goes through to the player, so chump-blockers don't save them.
Trample sources: **Rancor** (`+2/+0 and has trample`), **Behemoth Sledge** (`+2/+2 and has trample and
lifelink`), **Gunner Conscript** (`{1}{G}`, 2/2 trample, `This creature gets +1/+1 for each Aura and
Equipment attached to it.`), **Armory Paladin** (3/3 trample), **Super Mutant Scavenger** (`{4}{G}`, 5/5
trample), **Crimson Caravaneer** (`{2}{R}`, 1/2, `Double strike, trample`).

**(b) Commander damage.** Per CR 903.10a, 21 combat damage from Dogmeat alone eliminates a player. The
arithmetic is real: Dogmeat is a 3/3. Add **Behemoth Sledge** (+2/+2) → 5/5. Add **Fireshrieker**
(`{3}`, `Equipped creature has double strike.`, `Equip {2}`) → 5/5 with double strike = **10 damage per
unblocked attack**. Three connections (10, 20, 30) is lethal commander damage. Add **Brass Knuckles**
(`{4}`, `Equipped creature has double strike as long as two or more Equipment are attached to it.`) or
**Junk Jet** (`{1}{R}`, `{3}, Sacrifice another artifact: Double equipped creature's power until end of
turn.` — and Junk tokens are artifacts you can feed it) and it gets there faster.

**(c) Forcing damage through.** The deck has real evasion tools to make sure the big creature connects:
**Silver Shroud Costume** (`{2}`, flash, `Equipped creature can't be blocked.`, `Equip {3}`),
**Rogue's Passage** (land, `{4}, {T}: Target creature can't be blocked this turn.`),
**Sticky Fingers** (`{R}`, grants menace plus a Treasure on damage, and `When enchanted creature dies,
draw a card.`), **Agility Bobblehead** (`{3}`, `{3}, {T}: Up to X target creatures you control each gain
haste until end of turn and can't be blocked this turn except by creatures with haste, where X is the
number of Bobbleheads you control`), and **Idolized** (`{1}{W}`, `Enchanted creature has "Whenever this
creature attacks alone, it gets +X/+X until end of turn, where X is the number of nonland permanents you
control."` — note the ruling: *"A creature attacks alone if it's the only creature declared as an
attacker during the declare attackers step"*, so this only works when you send exactly one attacker).

**What you do NOT have:** no counterspells, no reanimation of opponents' stuff, no extra turns, no mass
land destruction. `mtg deck bracket dogmeat` confirms zero extra-turn effects and zero mass land denial.

---

## 5. What to mulligan for

**First, the free mulligan.** In Commander your first mulligan costs you nothing:

> **CR 103.5c** — *"In a multiplayer game and in any Brawl game, the first mulligan a player takes
> doesn't count toward the number of cards that player will put on the bottom of their library or the
> number of mulligans that player may take."*

So the first "mull to 7" is genuinely free. **Take it liberally.** A bad seven is much worse than a
fresh seven.

### The 10-second keep checklist

Look at your hand and answer three questions:

1. **Do I have 2 to 4 lands that make *colored* mana?** Careful — count these as *half* a land:
   **Temple of the False God** (`{T}: Add {C}{C}. Activate only if you control five or more lands.` — it
   makes zero mana until your fifth land and produces no color), **Junktown**, **Buried Ruin**,
   **Roadside Reliquary**, **Scavenger Grounds**, **Rogue's Passage**, and **Ash Barrens** (all
   `{T}: Add {C}`).
2. **Do I have a play on turn 1 or 2?** Any `{1}` Equipment, any one-mana Aura, Sol Ring, Arcane Signet.
3. **Can I see a path to Dogmeat by turn 4?** Do the lands + rocks in hand produce `{R}`, `{G}`, and
   `{W}`? If not, is there a fixer — **Command Tower**, **Jungle Shrine**, **Arcane Signet**,
   **Abundant Growth**, **Fertile Ground**, **Exotic Orchard**, **Path of Ancestry**, **Evolving
   Wilds**, **Terramorphic Expanse**?

Two "yes" answers = keep. One or zero = mulligan.

### Real hands from the goldfish simulator

These are actual outputs of `mtg deck goldfish dogmeat --seed N`. The simulator's mana model is
lands-only (it ignores whether lands enter tapped and it never casts your commander), so treat its
recommendation as a starting point and apply the checklist yourself.

---

**Seed 13 — the hand you want. KEEP.**

```
  Mantle of the Ancients           {3}{W}{W}           5  Enchantment
  Mountain                         —                   0  Basic Land
  Clifftop Retreat                 —                   0  Land
  Scavenger Grounds                —                   0  Land
  Command Tower                    —                   0  Land
  Animal Friend                    {1}{G}              2  Enchantment
  Sol Ring                         {1}                 1  Artifact

  lands in opener: 4
── RECOMMENDATION: KEEP ──
```

**Keep, easily.** Four lands, Sol Ring on turn 1, and Command Tower fixes any color. Checklist: 3 colored
lands (Mountain, Clifftop Retreat, Command Tower) — yes; T1 play (Sol Ring) — yes; Dogmeat by T4 — yes,
Command Tower plus Clifftop Retreat covers R and W and you'll find green. Two small sequencing notes:
Scavenger Grounds only adds `{C}`, so this is really a three-colored-land hand; and **Clifftop Retreat**
reads `This land enters tapped unless you control a Mountain or a Plains`, so **play the Mountain first**
and Clifftop Retreat will come in untapped on the following turn.

---

**Seed 42 — a keep with a trap in it. KEEP, but know what you're keeping.**

```
  Rootbound Crag                   —                   0  Land
  Perception Bobblehead            {3}                 3  Artifact
  Temple of the False God          —                   0  Land
  Basilisk Collar                  {1}                 1  Artifact
  Fertile Ground                   {1}{G}              2  Enchantment
  Command Tower                    —                   0  Land
  Acquired Mutation                {2}{R}              3  Enchantment

  lands in opener: 3
── RECOMMENDATION: KEEP ──
```

**Keep.** But the simulator says "3 lands" and that is optimistic: **Temple of the False God** produces
nothing until you control five lands. Functionally this is a **two-land hand** with a good curve
(Basilisk Collar T1 off Command Tower, Fertile Ground T2 — and Fertile Ground is `Whenever enchanted land
is tapped for mana, its controller adds an additional one mana of any color`, which is both ramp and
fixing). Sequencing note: **Rootbound Crag** reads `This land enters tapped unless you control a Mountain
or a Forest`, and you control neither, so it enters **tapped** — lead with Command Tower on turn 1 and
Rootbound Crag on turn 2. Command Tower alone can make any of your three colors, and Rootbound Crag adds
`{R}` or `{G}` — you'll still need a third land before Dogmeat is castable. It's a keep because the
two real lands are excellent and you have a cheap curve, but you are one land away from being stuck, so
prioritise hitting land drops over casting Perception Bobblehead.

---

**Seed 7 — a marginal keep. I'd keep it, but understand why it's marginal.**

```
  Explorer's Scope                 {1}                 1  Artifact
  Chaos Warp                       {2}{R}              3  Instant
  Junktown                         —                   0  Land
  Champion's Helm                  {3}                 3  Artifact
  Path to Exile                    {W}                 1  Instant
  Preston Garvey, Minuteman        {2}{R}{G}{W}        5  Legendary Creature
  Clifftop Retreat                 —                   0  Land

  lands in opener: 2
── RECOMMENDATION: KEEP ──
```

**Marginal keep.** Two lands, and **Junktown only makes `{C}`** (`{T}: Add {C}.`) — so you effectively
have *one* colored source. Worse: **Clifftop Retreat** reads `This land enters tapped unless you control
a Mountain or a Plains`, and on turn 1 you control neither, so it comes in **tapped**. Your first real
play is Explorer's Scope on turn 2. What saves it: Path to Exile (`{W}`) is premium removal, Chaos Warp
(`{2}{R}`) answers anything, and Clifftop Retreat produces both R and W. If your pod is casual and slow,
keep. If you are the kind of player who hates being punished for greed, mulligan — you are one land off
a functional hand and this deck's mana is genuinely demanding.

---

**Seed 3 — MULLIGAN. No debate.**

```
  Almost Perfect                   {4}{G}{W}           6  Enchantment
  Mountain                         —                   0  Basic Land
  Bighorner Rancher                {4}{G}              5  Creature
  Break Down                       {2}{G}              3  Instant
  Pip-Boy 3000                     {1}                 1  Artifact
  Abundant Growth                  {G}                 1  Enchantment
  Grim Reaper's Sprint             {4}{R}              5  Enchantment

  lands in opener: 1
── RECOMMENDATION: MULLIGAN ──
  - 1 land in the seven (deck runs 38; 2-5 is the keepable band).
  - Under two lands is a mulligan in almost every Commander pod.
```

**Mulligan.** One land, and three of the seven cards cost five or six mana. Even the "cheap" spells
(Abundant Growth `{G}`, Break Down `{2}{G}`) need green and your only land is a Mountain. This hand does
nothing for four turns. Take the free mulligan.

---

**Seed 1 — technically a "keep" by land count; a good teaching hand.**

```
  Mossfire Valley                  —                   0  Land
  Forest                           —                   0  Basic Land
  Plains                           —                   0  Basic Land
  Mister Gutsy                     {2}                 2  Artifact Creature
  Almost Perfect                   {4}{G}{W}           6  Enchantment
  Cass, Hand of Vengeance          {2}{R}{W}           4  Legendary Creature
  Forest                           —                   0  Basic Land

  lands in opener: 4
── RECOMMENDATION: KEEP ──
  - Curve: 3 spells, average cmc 4.0, cheapest 2.
```

**Keep, but slowly.** Four lands is good and — worth noticing — you *can* cast Dogmeat on turn 3 off
three of them: **Mossfire Valley** reads `{1}, {T}: Add {R}{G}`, so tap Forest for `{G}`, spend it on
Mossfire Valley's activation, get `{R}{G}` back, tap Plains for `{W}` → `{R}{G}{W}`. That is exactly
your commander. Nothing else in the hand happens before turn 2 (Mister Gutsy), and Almost Perfect at
six mana is a long way off. This is the profile of a slow-but-functional keep: land Dogmeat on time and
let the mill-five find you something.

---

## 6. The 8–10 cards that matter most

Ranked by how much they change the game when you draw them.

### 1. Sol Ring — `{1}` — Artifact
> `{T}: Add {C}{C}.`

One mana, taps for two. It is the best card in the 99 and it isn't close. EDHREC has it in
**91.9% of 8,826 Dogmeat decks**. Play it turn 1 every single time.

### 2. Puresteel Paladin — `{W}{W}` — Creature — Human Knight — 2/2
> `Whenever an Equipment you control enters, you may draw a card.`
> `Metalcraft — Equipment you control have equip {0} as long as you control three or more artifacts.`

This is the deck's engine card. Thirteen Equipment in the list means it draws cards repeatedly, and once
you have three artifacts on board **every equip cost becomes {0}** — you can move the whole toolbox onto
a new creature for free, every turn. Ruling (2020-08-07): *"Once the equip {0} ability is activated,
causing Puresteel Paladin to leave the battlefield or causing its controller to control fewer than three
artifacts won't stop the equip ability from resolving."* Note that Equipment are themselves artifacts,
so three Equipment on board is enough to switch metalcraft on.

### 3. All That Glitters — `{1}{W}` — Enchantment — Aura
> `Enchant creature`
> `Enchanted creature gets +1/+1 for each artifact and/or enchantment you control.`

Two mana for the single biggest stat swing in the deck. In a deck with 34 artifacts and enchantments,
mid-game this is routinely +5/+5 or more. Ruling (2019-10-04): *"A permanent that's both an artifact and
an enchantment is counted only once."* and *"Because All That Glitters is an enchantment, the enchanted
creature usually gets at least +1/+1."* It counts **all** your artifacts and enchantments, not just the
ones attached to that creature.

### 4. Strong Back — `{2}{G}` — Enchantment — Aura
> `Enchant creature`
> `Equip abilities you activate that target enchanted creature cost {3} less to activate.`
> `Aura spells you cast that target enchanted creature cost {3} less to cast.`
> `Enchanted creature gets +2/+2 for each Aura and Equipment attached to it.`

Cost reduction *and* the biggest per-attachment buff in the deck. Four attachments = +8/+8. It also makes
your expensive equips (Behemoth Sledge `Equip {3}`, Pre-War Formalwear `Equip {3}`, Silver Shroud Costume
`Equip {3}`) free. Ruling (2024-03-08): *"Strong Back's third ability won't reduce its own cost."*

### 5. Mantle of the Ancients — `{3}{W}{W}` — Enchantment — Aura
> `Enchant creature you control`
> `When this Aura enters, return any number of target Aura and/or Equipment cards from your graveyard to the battlefield attached to enchanted creature.`
> `Enchanted creature gets +1/+1 for each Aura and Equipment attached to it.`

Your comeback card. After you've been blown out once or twice, this rebuilds the entire pile onto one
creature in a single card — and Dogmeat's mill-five has been stocking your graveyard all game.
EDHREC's #1 synergy card for this commander (86.3% of decks).

### 6. Codsworth, Handy Helper — `{2}{W}` — Legendary Artifact Creature — Robot — 2/3
> `Commanders you control have ward {2}.`
> `{T}: Add {W}{W}. Spend this mana only to cast Aura and/or Equipment spells.`
> `{T}: Attach target Aura or Equipment you control to target creature you control. Activate only as a sorcery.`

Three separate jobs: it taxes removal aimed at Dogmeat, it ramps you specifically for the spells you
actually want to cast, and it **moves Auras** — normally impossible. Two rulings to know
(both 2024-03-08): *"You can't spend mana generated by Codsworth's second ability to activate abilities
of Auras or Equipment. This includes paying equip costs."* and *"The Aura or Equipment you target with
Codsworth's last ability doesn't have to be attached to a creature you control when you target it."*

### 7. Cass, Hand of Vengeance — `{2}{R}{W}` — Legendary Creature — Human Ranger — 4/3
> `Vigilance`
> `Whenever Cass or another creature you control dies, if it was enchanted or equipped, return any number of Aura cards that were attached to it from your graveyard to the battlefield attached to target creature, then attach any number of Equipment that were attached to it to that creature.`

This is the card that fixes the deck's structural weakness. Normally, killing your dressed-up creature
2-for-1s you and the Auras die with it. With Cass out, the Auras come **straight back** onto another
creature. If you are worried about removal, deploy Cass before you over-commit. Ruling (2024-03-08):
*"You can't return Aura cards that can't legally be attached to the target creature."*

### 8. Inventory Management — `{R}{W}` — Instant
> `Split second (As long as this spell is on the stack, players can't cast spells or activate abilities that aren't mana abilities.)`
> `For each Aura and Equipment you control, you may attach it to a creature you control.`

Two mana, at instant speed, moves your **entire** collection of Auras and Equipment onto one creature —
and it has **split second**, meaning opponents cannot respond at all. Use it: (a) in response to targeted
removal, to move the gear off the doomed creature; (b) mid-combat, after blockers are declared, to make
a blocked creature enormous; (c) after a Junk token exiles nothing useful, just to reconfigure. Ruling
(2024-03-08): *"You can't try to attach an Aura or Equipment to a creature if that Aura or Equipment
can't legally be attached to it."*

### 9. Grim Reaper's Sprint — `{4}{R}` — Enchantment — Aura
> `Morbid — This spell costs {3} less to cast if a creature died this turn.`
> `Enchant creature`
> `When this Aura enters, untap each creature you control. If it's your main phase, there is an additional combat phase after this phase.`
> `Enchanted creature gets +2/+2 and has haste.`

The out-of-nowhere kill. Untap everything and take a second combat phase — with a big equipped creature
that is often lethal on one player. If a creature died this turn (including in the combat you just had)
it costs only `{1}{R}`. **Warning**, per its ruling (2024-03-08): *"If the creature Grim Reaper's Sprint
would enchant is an illegal target by the time Grim Reaper's Sprint would resolve, the entire spell
doesn't resolve … you won't untap your creatures or get an additional combat phase."* Don't cast it
targeting a creature an opponent can kill in response.

### 10. Heroic Intervention — `{1}{G}` — Instant
> `Permanents you control gain hexproof and indestructible until end of turn.`

Your best defensive card and the only one that protects the *whole board*. It beats board wipes, it
beats targeted removal, and it costs two mana. **Hold it.** This deck loses games to a single well-timed
wipe more than to anything else.

---

## 7. Common mistakes with this deck

Each of these is grounded in the deck's actual numbers.

### Mistake 1 — Putting all your Auras on one creature with no protection
The deck has **17 enchantments**, almost all Auras. When the enchanted creature dies or is exiled, every
Aura on it goes to the graveyard (CR 704.5m). Three Auras on one creature + one removal spell = you lost
four cards for their one. **Fix:** deploy **Cass, Hand of Vengeance** or **Champion's Helm** / **Swiftfoot
Boots** (both grant hexproof) *before* you commit the third Aura. And note that Equipment do **not** have
this problem — an Equipment just becomes unattached and stays on the battlefield. When in doubt, lead
with Equipment and follow with Auras once the creature is protected.

### Mistake 2 — Tapping out every turn
`mtg deck stats` counts **4 removal spells, 1 board wipe, and 6 interaction pieces** in 61 non-lands.
That is *low*. Your two most important reactive cards are **Heroic Intervention** (`{1}{G}`) and
**Valorous Stance** (`{1}{W}`, `Choose one — • Target creature gains indestructible until end of turn.
• Destroy target creature with toughness 4 or greater.`), and both cost exactly two mana. If you have one
in hand, leaving two mana up is frequently better than casting a third Aura.

### Mistake 3 — Equipping after you attack (or forgetting to equip at all)
Equip is **sorcery-speed only** (CR 702.6a: *"Activate only as a sorcery"*). Once you've declared
attackers, it's too late. Worse, Dogmeat's trigger checks whether the creature is enchanted **or equipped
at the moment it attacks** — an Equipment sitting unattached generates nothing. **Build the habit:
precombat main phase → equip everything → then declare attackers.** The exception is **Silver Shroud
Costume**, which has **flash** and attaches itself on entry (`When this Equipment enters, attach it to
target creature you control`), so it can come down at instant speed — but its ruling notes
*"Attaching Silver Shroud Costume to a creature that has already been blocked won't cause it to become
unblocked."*

### Mistake 4 — Cracking Junk tokens at the wrong time, or wasting the land
A Junk token's ability is `Activate only as a sorcery` and the exiled card is playable **only that turn**.
Two failure modes: (a) you crack Junk tokens with no mana left, so the exiled spell is wasted; (b) the
Junk exiles a land but you already played a land this turn. **Fix:** on attacking turns, hold your land
drop until your **postcombat main phase**, and leave 1–3 mana unspent before combat. Also remember the
ruling: *"You can't sacrifice a Junk token to pay multiple costs"* — one Junk token, one cost.

### Mistake 5 — Greedy keeps because "38 lands is a lot"
The stats assessment flags this deck as **HEAVY on lands**: 38 lands against a 2.82 average mana value,
where the usual heuristic wants 34–36. That means **flood is a real risk** — but it does *not* make a
one- or two-land hand safe, because **32% of your lands enter tapped** (12 of 38) and your commander
needs three different colors. A hand with two tapped lands is a hand that does nothing until turn 3.
Count *untapped, colored* sources, not lands.

### Mistake 6 — Treating Temple of the False God as a land
**Temple of the False God**: `{T}: Add {C}{C}. Activate only if you control five or more lands.` Before
your fifth land it produces **zero** mana, and it never produces a color. Same trap, milder, with
**Junktown**, **Buried Ruin**, **Roadside Reliquary**, **Scavenger Grounds**, **Rogue's Passage** and
**Ash Barrens** — all `{T}: Add {C}` only. That's **7 lands that make no colored mana**, in a
three-color deck. Factor that into every mulligan decision.

### Mistake 7 — Recasting Dogmeat immediately, every time
Commander tax is `{2}` more per previous cast from the command zone (CR 903.8), and the colored pips
never get cheaper. Cast #3 is `{4}{R}{G}{W}` — seven mana. Sometimes the right play is to leave Dogmeat
in the command zone for a turn and develop instead. **Codsworth's `ward {2}`** and **Champion's Helm**'s
hexproof-for-legendaries exist specifically to keep the tax from spiralling.

### Mistake 8 — Forgetting that goading is aimed at *opponents*
**Acquired Mutation** (`{2}{R}`) reads `Enchanted creature gets +2/+2 and is goaded` and
`Whenever enchanted creature attacks, defending player gets two rad counters`. The card's own reminder
text spells the effect out from your seat: *"(It attacks each combat if able and attacks a player other
than you if able.)"* — that reads "other than you" because *you* are the one goading it. The general
rule (CR 701.15b) is *"a player other than the controller of the permanent, spell, or ability that
caused it to be goaded"*. Put it on the **scariest creature an opponent controls** — it forces that creature to attack someone else, and rad counters make its
controller mill and lose life (CR 728.1). Putting it on your own creature is almost always wrong.

### Mistake 9 — Attacking with everything when Idolized is your plan
**Idolized** only triggers when the creature `attacks alone` — per its ruling, *"A creature attacks alone
if it's the only creature declared as an attacker during the declare attackers step."* If you want the
Idolized bonus you must send **exactly one** attacker, which conflicts with Dogmeat's "one Junk token per
dressed-up attacker." Decide which plan you're on before declaring attackers.

---

## 8. Bracket and table expectations

Straight from `mtg deck bracket dogmeat`:

```
ESTIMATED BRACKET 2 — Core
  Precon-level. The baseline Commander experience -- a modern
  preconstructed deck out of the box lands here.

  Game Changers        : 0 (checked against 53 listed cards)
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review
```

**In plain language:** this is an unmodified precon and it plays like one. Bracket 2 is the "Core"
Commander experience — the level where most kitchen-table and store-casual pods sit.

What to expect:

- **Games run long.** The bracket description says games "typically end around turn 9 or later." Don't
  panic if nothing has happened by turn 6 — that's normal at this power level.
- **You are not the fastest deck at the table, and that's fine.** Your deck's job is to build a threat
  over several turns and then convert. It doesn't have the explosive turns of a tuned deck.
- **Zero "Game Changers."** That's the official list of 53 high-power cards; your deck has none of them.
  EDHREC shows the four most common Game Changers Dogmeat players add (Enlightened Tutor, Teferi's
  Protection, Smothering Tithe, Farewell) — none are in your list. So you can honestly tell a pod
  "this is an out-of-the-box precon, Bracket 2."
- **The one caveat the tool flags:** it cannot detect two-card infinite combos and asks for human review.
  Nothing in the oracle text I retrieved for this list forms an obvious infinite loop, but if you later
  add cards, re-run `mtg deck bracket dogmeat` and check.
- **Table politics:** you will be visibly building a big creature. That draws removal. This is the
  correct time to be friendly, point out that someone else's deck is doing scarier things, and keep
  **Heroic Intervention** up. A Bracket 2 pod usually has 1–2 removal spells per player, not 8.
- **Your deck is well-built for its bracket.** Cross-referencing `mtg edhrec dogmeat` against your list,
  you already run **all 10 of the highest-synergy cards** and **all 10 of the top cards** EDHREC lists
  for this commander (8,826 decks tracked). That is unusual for a precon — the box happens to contain
  the cards this commander actually wants.

---

## Quick reference: your turn sequence

1. **Untap, upkeep, draw.**
2. **Precombat main:** play a land *only if* you don't expect Junk tokens this turn. Cast creatures.
   **Equip everything** (sorcery-speed only). Cast Auras.
3. **Declare attackers:** every creature that is enchanted or equipped makes a Junk token when it
   attacks (Dogmeat's trigger). Send them.
4. **Damage.** Watch for Bloodforged Battle-Axe (`Whenever equipped creature deals combat damage to a
   player, create a token that's a copy of this Equipment.`) and Sticky Fingers (Treasure) triggers.
5. **Postcombat main:** crack Junk tokens now, with mana available. Play your held land drop if a Junk
   exiles a land. Consider **Grim Reaper's Sprint** here for a second combat.
6. **End step:** hold Heroic Intervention / Valorous Stance / Path to Exile mana if you have them.
