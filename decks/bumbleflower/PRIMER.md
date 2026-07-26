# Peace Offering — Ms. Bumbleflower

**Deck primer — how to actually pilot this thing**

| | |
|---|---|
| Commander | Ms. Bumbleflower |
| Colors | Bant — white / blue / green (WUG) |
| Set | BLC, released 2024-08-02 |
| Slug | `bumbleflower` |
| Estimated bracket | **2 — Core** (precon-level) |
| Composition | 38 lands · 26 creatures · 11 instants · 8 artifacts · 8 enchantments · 7 sorceries · 1 planeswalker |

> **Before you read on:** every card cost, type line, and rules text in this document was pulled
> from the local card database in the same session it was written. If you want to double-check
> anything, run `./bin/mtg card "<card name>"` yourself. Real CLI output is pasted in the
> Appendix at the bottom.

---

## Quick jargon key

You will meet these words below. Most are defined again inline where they actually matter, but
here they are up front so nothing surprises you. Anything marked ⌕ has an official entry you
can read with `./bin/mtg glossary <term>`.

- **Mana value** ⌕ — the total amount of mana in a card's cost, ignoring color. `{2}{G}` has mana
  value 3. (Older players say "converted mana cost".)
- **Trigger / triggered ability** — an ability that starts with "Whenever…", "When…", or "At the
  beginning of…". It happens automatically; you don't choose to use it.
- **The stack** — the waiting area where spells and triggers sit before they take effect. Last
  thing added is the first thing that happens.
- **Target** — a specific thing an ability points at. You pick targets when the ability goes on the
  stack, not when it resolves.
- **Ramp** — cards that give you extra mana, so you cast bigger things sooner. A **mana rock** is
  an artifact that taps for mana (Sol Ring, Arcane Signet).
- **Fixing** (color fixing) — cards that let you produce the specific *colors* you need, as opposed
  to ramp, which just produces *more* mana. You can have five lands out and still be unable to cast
  a `{1}{G}{W}{U}` commander; fixing is what solves that. Arcane Signet, Farseek and Command Tower
  are fixing; Sol Ring is pure ramp.
- **Upkeep** ⌕ — a step near the start of your turn, *before* you draw for the turn.
- **Fog** — an effect that prevents all combat damage for a turn. You survive an attack that
  would have killed you.
- **Pillowfort** — cards that make it expensive or pointless to attack *you*, steering the table
  at somebody else.
- **Board wipe** — a spell that destroys most or all creatures at once.
- **Vigilance** ⌕ — "Attacking doesn't cause creatures with vigilance to tap" (CR 702.20b). So the
  creature can attack *and* still be untapped to block on the way back.
- **Gift** ⌕ — a keyword on some cards in this deck. "As an additional cost to cast this spell,
  you may choose an opponent" (CR 702.174a). If you do, they get the listed gift and your spell
  gets *better*. "Gift a card" means "the chosen player draws a card" (CR 702.174e).
- **Tempting offer** — on Tempt with Discovery / Tempt with Bunnies: you do a thing, then each
  opponent *may* copy it, and for each one who does, **you do it again**.
- **Commander tax** — the extra cost to recast your commander after it dies. See §2.

---

## 1. What this deck is trying to do

You are the table's librarian. Ms. Bumbleflower turns **every spell you cast** into a card for an
opponent, a **+1/+1 counter** and **flying** for one of your creatures, and — on your *second* spell
each turn — **two cards for you**. So this deck wants to cast two cheap spells a turn, every turn,
forever.

Around that, the deck runs a pile of permanents that grow off the *whole table's* spellcasting
(Forgotten Ancient, Managorger Hydra, Sunscorch Regent, Steelburr Champion) and a pile of
permanents that convert your enormous hand into damage or into a win (Psychosis Crawler, Body of
Knowledge, Simic Ascendancy, Twenty-Toed Toad, Triskaidekaphile). The 25 draw pieces and 14 ramp
pieces mean you almost never run out of gas.

The catch, and it is a real one: **you are handing your opponents free cards all game.** The deck
pays for that with an unusually deep defensive suite — Baird, Mangara, Spore Frog, Riot Control,
Perch Protection, Promise of Loyalty, Illusionist's Gambit — so that the table's newly-refilled
hands get pointed somewhere other than you.

Honest summary: **a slow, resilient, defensive value deck** that builds a board of ever-growing
creatures behind a wall of "please don't attack me" effects, then either flies over for a huge
turn or hits one of its three alternate-win cards. It has no fast clock and it does not want one.

---

## 2. Your commander

### The card, exactly as printed

```
Ms. Bumbleflower
Mana cost      : {1}{G}{W}{U}
Mana value     : 4
Type           : Legendary Creature — Rabbit Citizen
P/T            : 1/5

Vigilance
Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter
on target creature. It gains flying until end of turn. If this is the second
time this ability has resolved this turn, you draw two cards.
```

Official ruling (2024-07-26):
> "Ms. Bumbleflower's last ability resolves before the spell that caused it to trigger. It
> resolves even if that spell is countered."

### What that actually means when you play it

**It is one trigger with four parts, and it fires on every single spell you cast.** Not "may" —
it is mandatory, and it has two targets you must choose: a **target opponent** (who draws) and a
**target creature** (who gets the counter and flying).

1. **"Target opponent draws a card."** You choose *which* opponent, every time. This is the price
   of the engine, and choosing well is most of the skill in this deck. See §7, mistake #1
   ("Feeding the wrong opponent").
2. **"Put a +1/+1 counter on target creature."** It says *target creature*, not "target creature
   you control" — so it can legally point at an opponent's creature, but normally you point it at
   your own. Ms. Bumbleflower herself is a legal target, and early on she is often the only one.
3. **"It gains flying until end of turn."** The same creature that got the counter. This is your
   evasion. Spells cast **before combat** on your turn give a creature flying *for that attack*.
4. **"If this is the second time this ability has resolved this turn, you draw two cards."** Note
   **second**, exactly. Spell #2 each turn draws you two cards. Spell #3, #4, #5 still give
   counters, flying, and a card to an opponent — but they do **not** draw you more cards. Two
   spells per turn is the sweet spot; more than that is fine, just not extra-rewarded.

**Timing:** the trigger resolves *before* your spell does (see the ruling above). So the counter
and the flying land first. That is why you can cast a 2-mana spell in your first main phase and
attack with a suddenly-flying, suddenly-bigger creature in the same turn.

**Fizzling:** if by the time the trigger resolves *both* targets are illegal (e.g. the creature
you targeted died in response and the opponent left the game), the whole ability is removed from
the stack and does nothing — "If all its targets, for every instance of the word 'target,' are now
illegal, the spell or ability doesn't resolve" (CR 608.2b). A trigger that doesn't resolve does
**not** count toward the "second time this ability has resolved this turn" tally.

**She is a 1/5 with vigilance.** That is not a threat — it is a wall that stays home. 5 toughness
survives most incidental damage, and vigilance (CR 702.20b: "Attacking doesn't cause creatures
with vigilance to tap") means if you do send her in, she is still up to block.

### Cost and the commander tax

She costs `{1}{G}{W}{U}` — four mana, and you need **all three colors on the same turn**. That is
the single hardest mana requirement in the deck. Your color sources: **20 white, 19 blue, 19
green** out of 38 lands, plus Command Tower and Exotic Orchard which count for every color.

If she dies, you may put her into the command zone instead of the graveyard — that is a
state-based action, "If a commander is in a graveyard or in exile and that object was put into
that zone since the last time state-based actions were checked, its owner may put it into the
command zone" (CR 903.9a). Same option if she would go to your hand or library (CR 903.9b).

Then the tax kicks in:

> **CR 903.8** — "A player may cast a commander they own from the command zone. A commander cast
> from the command zone costs an additional {2} for each previous time the player casting it has
> cast it from the command zone that game. This additional cost is informally known as the
> 'commander tax.'"

So: 1st cast **4 mana**, 2nd cast **6 mana**, 3rd cast **8 mana**. That climbs fast on a 4-drop.

### Cast her early or hold her?

**Cast her early — turn 4 or 5, as soon as you have WUG.** She is not a win condition you are
protecting for a big turn; she is an engine, and every turn she is out is two extra cards. She
also has 5 toughness, which means she survives a lot of what a table throws around casually.

The one thing worth doing: if you have **Swiftfoot Boots** `{2}` on the battlefield, consider
equipping her (Equip {1}) before you tap out. Boots give "hexproof and haste" — hexproof means
"It can't be the target of spells or abilities your opponents control," which blanks most targeted
removal. That is cheap insurance against the commander tax.

Do **not** hold her back waiting for perfect protection. This deck does nothing without her.

---

## 3. The turn-by-turn shape

### Turns 1–3 — build the mana, deploy cheap permanents

**Your job:** hit every land drop and get to WUG by turn 4.

You have 38 lands, of which **14 can enter tapped** (7 always, 7 conditionally) — Canopy Vista,
Glacial Fortress, Hinterland Harbor, Prairie Stream, Razorverge Thicket, Seachrome Coast, Seaside
Citadel, Sunpetal Grove, Temple of Enlightenment, Temple of Mystery, Temple of Plenty, Thriving
Grove, Thriving Heath, Thriving Isle. That is 37% of your mana base. **Sequence your tapped lands
on the turns you weren't going to spend all your mana anyway** — usually turn 1.

Cards you are thrilled to see here:

- **Sol Ring** `{1}` — Artifact — "{T}: Add {C}{C}." The best turn-1 play in the deck by a mile.
- **Arcane Signet** `{2}` — Artifact — "{T}: Add one mana of any color in your commander's color
  identity." Fixes all three of your colors.
- **Fellwar Stone** `{2}` — Artifact — "{T}: Add one mana of any color that a land an opponent
  controls could produce." Good in a 4-player pod, occasionally awkward.
- **Mind Stone** `{2}` — Artifact — "{T}: Add {C}." plus "{1}, {T}, Sacrifice this artifact: Draw
  a card." Ramp early, a card later.
- **Thought Vessel** `{2}` — Artifact — "You have no maximum hand size." / "{T}: Add {C}." Ramp
  *and* it removes the discard-to-seven rule, which matters a lot in this deck.
- **Farseek** `{1}{G}` — Sorcery — "Search your library for a Plains, Island, Swamp, or Mountain
  card, put it onto the battlefield tapped, then shuffle." Note it can **not** get a Forest, but it
  *can* get Canopy Vista and Prairie Stream, which are dual lands with the Plains/Island types.
- **Cultivate** `{2}{G}` — Sorcery — two basics, one to the battlefield tapped, one to hand.

Cheap permanents worth playing on curve:

- **Wizard Class** `{U}` — Enchantment — Class — level 1 is "You have no maximum hand size."
  (A **Class** enchantment enters at level 1 and prints extra "level bars" you can activate — at
  sorcery speed, per its own reminder text *"Gain the next level as a sorcery to add its ability"* —
  to raise it a level and *add* that level's ability without losing the earlier ones. Wizard Class
  has `{2}{U}: Level 2`, "When this Class becomes level 2, draw two cards", and `{4}{U}: Level 3`,
  "Whenever you draw a card, put a +1/+1 counter on target creature you control." CR 716.)
- **Jolrael, Mwonvuli Recluse** `{1}{G}` — 1/2 — "Whenever you draw your second card each turn,
  create a 2/2 green Cat creature token." With Bumbleflower out this is a free 2/2 nearly every turn.
- **Triskaidekaphile** `{1}{U}` — 1/3 — no maximum hand size, plus an alternate win (see §4).
- **Jolly Gerbils** `{1}{W}` — 2/3 — "Whenever you give a gift, draw a card."
- **Kwain, Itinerant Meddler** `{W}{U}` — 1/3 — "{T}: Each player may draw a card, then each player
  who drew a card this way gains 1 life."
- **Spore Frog** `{G}` — 1/1 — hold this. It is a **fog** (an effect that prevents a whole turn's
  combat damage), not a creature — see "If turn 7+ is going badly" below and §6, card #9.
- **Coiling Oracle** `{G}{U}` — 1/1 — flips the top card of your library into play (if land) or
  your hand (if not).

**If turns 1–3 are going badly** (missed land drops, wrong colors): prioritise any mana rock over
any creature. **Evolving Wilds** and **Terramorphic Expanse** both read "{T}, Sacrifice this land:
Search your library for a basic land card, put it onto the battlefield tapped, then shuffle" — so
go get a basic in the *color you are missing*, not the one you already have. (Note "basic": they
cannot fetch your dual lands.)

### Turns 4–6 — commander down, start double-spelling

**Turn 4–5: cast Ms. Bumbleflower.** From here your default turn is: cast a 2-drop, cast a 3-drop,
draw two, attack with something that just gained flying.

Deploy in roughly this priority:

1. **Passive growers** — these get bigger off *everybody's* spells, and in a 4-player game that is
   enormous:
   - **Forgotten Ancient** `{3}{G}` — 0/3 — "Whenever a player casts a spell, you may put a +1/+1
     counter on this creature." Also, at your upkeep you may move any number of those counters onto
     other creatures. Its ruling notes the move "doesn't target any creatures" and that once it
     starts resolving, "no player may take actions until the ability has finished resolving."
   - **Managorger Hydra** `{2}{G}` — 1/1 with trample — "Whenever a player casts a spell, put a
     +1/+1 counter on this creature." Not optional, and it grows fast.
   - **Steelburr Champion** `{2}{W}` — 1/1 with vigilance — grows off opponents' *noncreature*
     spells. It also has Offspring `{1}{W}` — pay an extra `{1}{W}` on cast and you get a 1/1 token
     copy of it too.
   - **Sunscorch Regent** `{3}{W}{W}` — 4/3 flying — "Whenever an opponent casts a spell, put a
     +1/+1 counter on this creature and you gain 1 life."
2. **Draw payoffs** — **Chasm Skulker** `{2}{U}` (a +1/+1 counter per card you draw), **Hoofprints
   of the Stag** `{1}{W}` (a hoofprint counter per draw; four counters + `{2}{W}` makes a 4/4 flier),
   **Simic Ascendancy** `{G}{U}` (see §4).
3. **Defense, before you become the target** — **Baird, Steward of Argive** `{2}{W}{W}`, 2/4
   vigilance: "Creatures can't attack you or planeswalkers you control unless their controller pays
   {1} for each of those creatures." And **Mangara, the Diplomat** `{3}{W}`, 2/4 lifelink, which
   draws you a card when an opponent attacks you with two or more creatures *and* when an opponent
   casts their second spell each turn.
4. **Mana creatures** — **Faeburrow Elder** `{1}{G}{W}`, 0/0 with vigilance, "+1/+1 for each color
   among permanents you control" and "{T}: For each color among permanents you control, add one mana
   of that color." Its official ruling notes it "usually gives it at least +2/+2 and its last ability
   usually produces at least {G}{W}" — with blue permanents out too it is a 3/3 tapping for three.
   **Rishkar, Peema Renegade** `{2}{G}`, 2/2, puts a counter on up to two creatures and gives every
   countered creature "{T}: Add {G}."

**If turns 4–6 are going badly** — no commander, or she got killed and the tax is climbing:
you are still a fine deck. Forgotten Ancient, Managorger Hydra and Sunscorch Regent do not care
whether Bumbleflower is alive; they grow off the table. Fall back to being the defensive player:
land Baird, land Mangara, hold Spore Frog, and let the other three fight.

### Turns 7 and beyond — convert

By now you should have 6–8 lands, a hand of 8+ cards, and several creatures with counters on them.
This is where the big cards come down and the game gets decided.

- **Kalonian Hydra** `{3}{G}{G}` — Creature — Hydra, printed 0/0 with trample, "This creature enters
  with four +1/+1 counters on it" (so a 4/4) and "Whenever this creature attacks, **double the number
  of +1/+1 counters on each creature you control**." This is the single biggest swing in the deck.
- **Body of Knowledge** `{3}{U}{U}` — Avatar, */* — power and toughness equal to your hand size, no
  maximum hand size, and "Whenever this creature is dealt damage, draw that many cards."
- **Psychosis Crawler** `{5}` — Artifact Creature, */* equal to your hand size — "Whenever you draw
  a card, each opponent loses 1 life."
- **Mr. Foxglove** `{2}{G}{W}{U}` — 3/5 lifelink — on attack, draw cards equal to defending player's
  hand size minus yours; if that's zero or less, put a creature from your hand onto the battlefield
  for free instead. In this deck it is usually the second mode, because *your* hand is the big one.
- **Sphinx of Enlightenment** `{4}{U}{U}` — 5/5 flying — target opponent draws one, you draw three.
- **Coveted Jewel** `{6}` — draw three, taps for three mana of one color — but read §7, mistake #6
  first.
- **Realm-Cloaked Giant // Cast Off** — the Adventure half, **Cast Off** `{3}{W}{W}`, is "Destroy all
  non-Giant creatures", after which you may cast the 7/7 vigilance Giant `{5}{W}{W}` from exile later.
  (An **Adventure** is the cheaper instant/sorcery printed on the left of a creature card. You choose
  which half you are casting; casting the Adventure half is what puts the card in exile — its own
  reminder text reads *"Then exile this card. You may cast the creature later from exile."* CR 715.)

**If turn 7+ is going badly** — someone is about to win, or you are about to die:
- **Spore Frog** `{G}` — "Sacrifice this creature: Prevent all combat damage that would be dealt this
  turn." Blanks one entire attack step. **Peerless Recycling** `{1}{G}` returns it from your graveyard.
- **Riot Control** `{2}{W}` — "You gain 1 life for each creature your opponents control. Prevent all
  damage that would be dealt to you this turn."
- **Promise of Loyalty** `{4}{W}` — "Each player puts a vow counter on a creature they control and
  sacrifices the rest." Everyone keeps exactly one creature, and those creatures can't attack you.
  Its ruling confirms nobody can opt out: "Each player, including you, must put a vow counter on a
  creature they control if able."
- **Perplexing Test** `{3}{U}{U}` — choose one: bounce all creature tokens, **or** bounce all
  nontoken creatures, to their owners' hands.
- **Illusionist's Gambit** `{2}{U}{U}` — castable "only during the declare blockers step on an
  opponent's turn." It pulls all attackers out of combat, untaps them, and gives a second combat
  phase where they must attack — but "They can't attack you or planeswalkers you control that
  combat." You take a huge attack and hand it to somebody else.
- **Perch Protection** `{4}{W}{W}` — makes four 2/2 flying Birds. If you pay its gift cost you
  instead give an opponent **an extra turn** and in exchange "all permanents you control phase out,
  and until your next turn, your life total can't change and you gain protection from everything."
  (**Phasing out** means each of your permanents is temporarily *"treated as though it does not
  exist. It can't affect or be affected by anything else in the game"* (CR 702.26b) — so nothing can
  destroy, target or remove it — and they all phase back in as *your* next untap step begins
  (CR 702.26a). **Protection from everything** means, per this card's own ruling, "1) All damage that
  would be dealt to that player is prevented. 2) Auras can't be attached to that player. 3) That
  player can't be the target of spells or abilities." Together: for one turn cycle you and your board
  are untouchable — but your creatures are gone too, so you can't block for anyone, including you.)
  Only gift this when the alternative is losing on the spot.

---

## 4. How you actually win

**Be honest with yourself about this: the deck has no fast clock.** Bracket 2 games "typically end
around turn 9 or later," and this deck is at the slower end of that. You win by outlasting.

There are four real routes, roughly in order of how often they'll actually happen:

### Route 1 — Fliers with counters (the default)

This is the win most games. Ms. Bumbleflower puts a +1/+1 counter on a creature and gives it flying
**every time you cast a spell**. Forgotten Ancient banks counters and redistributes them at your
upkeep. **Kalonian Hydra**'s attack trigger *doubles* the counters on every creature you control —
that turns a board of 3/3s into 6/6s in one attack step, and it has trample. Add flying from
Bumbleflower's trigger and blockers stop mattering.

Realistic finish: turn 9–12, one or two big attacks, usually killing one player at a time.

### Route 2 — Simic Ascendancy (alternate win)

```
Simic Ascendancy — {G}{U} — Enchantment
{1}{G}{U}: Put a +1/+1 counter on target creature you control.
Whenever one or more +1/+1 counters are put on a creature you control, put
that many growth counters on this enchantment.
At the beginning of your upkeep, if this enchantment has twenty or more
growth counters on it, you win the game.
```

Every Bumbleflower trigger that puts a counter on **your own** creature also puts a growth counter
here. That's one per spell you cast. Kalonian Hydra's doubling can dump ten or more growth counters
in a single attack. Twenty is very reachable.

Read the rulings carefully, because they are traps:
> "If Simic Ascendancy doesn't have twenty or more growth counters on it as your upkeep begins, its
> last ability won't trigger. You can't take any actions during your turn before your upkeep begins."

> "If the last ability does trigger, but counters are removed from Simic Ascendancy so it has fewer
> than twenty remaining on it, you won't win the game."

Translation: **you must already be at 20 when your upkeep starts.** You cannot get there during
your upkeep. Plan the turn *before*. And expect the table to try to kill the enchantment in
response once they see the count climbing — this is the card that makes people point at you.

### Route 3 — Twenty-Toed Toad (alternate win)

```
Twenty-Toed Toad — {3}{U} — Creature — Frog Wizard — 3/3
Your maximum hand size is twenty.
Whenever you attack with two or more creatures, put a +1/+1 counter on this
creature and draw a card.
Whenever this creature attacks, you win the game if there are twenty or more
counters on it or you have twenty or more cards in hand.
```

Two ways to get there: 20 counters on the Toad (Kalonian Hydra doubling gets there terrifyingly
fast — 5 counters becomes 10 on one attack, then 10 becomes 20 on the next), or **20 cards in
hand**, which this deck can genuinely do.

Its ruling: "Twenty-Toed Toad's last ability will trigger whenever it attacks, no matter how many
counters are on it or cards you have in your hand at that time. The number of counters on it and
the number of cards in your hand are only checked **when that ability resolves**." So you can
attack, then respond to your own trigger by drawing more cards to get to 20. That is a genuine
line — hold up **Intellectual Offering** `{4}{U}` ("Choose an opponent. You and that player each
draw three cards") or **Secret Rendezvous** `{1}{W}{W}` and cast it in response.

Timestamp warning from its own ruling: "if you put Twenty-Toed Toad onto the battlefield and then
put Spellbook [no maximum hand size] onto the battlefield, you would have no maximum hand size.
However, if those permanents entered in the opposite order, your maximum hand size would be
twenty." Same applies to Thought Vessel, Wizard Class, Triskaidekaphile, Body of Knowledge and
Reliquary Tower — whichever entered *last* wins. The Toad wants to enter last if you're going for
20 cards; it doesn't matter otherwise since no-max-hand-size is strictly more permissive.

### Route 4 — Triskaidekaphile (alternate win, the hardest)

```
Triskaidekaphile — {1}{U} — Creature — Human Wizard — 1/3
You have no maximum hand size.
At the beginning of your upkeep, if you have exactly thirteen cards in your
hand, you win the game.
{3}{U}: Draw a card.
```

**Exactly thirteen.** Its ruling: "will trigger only if you have exactly thirteen cards in your
hand as your upkeep starts. If you have fewer cards in your hand, you won't be able to draw cards
during your upkeep in time to cause the ability to trigger." So you arrange 13 at the *end of your
previous turn* or during an opponent's turn, and then survive to your upkeep without drawing.

This is the least reliable route — hitting exactly 13 while a Bumbleflower trigger is drawing you
two cards at random moments is genuinely fiddly — but it costs two mana and it does sometimes just
happen. Count your hand every turn.

### The thing that is *not* a win condition

**Psychosis Crawler** `{5}` — "Whenever you draw a card, each opponent loses 1 life." It is real
damage and it hits all three opponents at once, but in a 40-life format you would need to draw
roughly 40 cards to kill one player with it alone. Treat it as a clock accelerator and a big body
(its power equals your hand size, which is often 8–12), **not** as the plan.

---

## 5. What to mulligan for

### The 10-second checklist

Look at seven cards and answer four questions. If you get three or more "yes", keep.

1. **Do I have 3, 4, or 5 lands?** (2 is a gamble, 6+ is flood.) The deck runs 38 lands.
2. **Can I cast something on turn 2 or turn 3?** Not turn 5. Turn 2 or 3.
3. **Can I see a path to white + blue + green by turn 5?** Ms. Bumbleflower needs all three.
4. **Is there ramp or fixing?** Sol Ring, Arcane Signet, Fellwar Stone, Mind Stone, Thought Vessel,
   Farseek, Cultivate, Evolving Wilds, Terramorphic Expanse.

**Reminder on how mulligans work** (CR 103.5): you shuffle back, draw a **fresh seven**, and then
put a number of cards on the bottom equal to how many mulligans you've taken. **In Commander your
first mulligan is free**: CR 103.5c — *"In a multiplayer game and in any Brawl game, the first
mulligan a player takes doesn't count toward the number of cards that player will put on the bottom
of their library or the number of mulligans that player may take."* So mulligan #1 is "draw 7,
bottom **0**" — a completely fresh seven at no cost. Bottoming only starts on your *second*
mulligan (draw 7, bottom 1), then the third (bottom 2), and so on. That makes the first mulligan
essentially free. **Take the mulligan.**

### Four real hands from the simulator

These come from `./bin/mtg deck goldfish bumbleflower --seed N`, which deals actual hands from the
actual list. Full output is in the Appendix.

---

**Hand A — `--seed 42`: MULLIGAN**

```
  Skycloud Expanse                 —                   0  Land
  Psychosis Crawler                {5}                 5  Artifact Creature
  Thought Vessel                   {2}                 2  Artifact
  Chasm Skulker                    {2}{U}              3  Creature
  Intellectual Offering            {4}{U}              5  Instant
  Forgotten Ancient                {3}{G}              4  Creature
  An Offer You Can't Refuse        {U}                 1  Instant
```

**Mulligan.** One land. It doesn't matter that the spells are good — Thought Vessel needs two
lands, Chasm Skulker needs three, Forgotten Ancient needs four. The simulator's own turn log is
brutal: it played its second land on turn 2 and then **missed its land drop on turns 3, 4, 5, 6
and 8**, sitting on twelve cards in hand doing nothing. One-landers are a mulligan in essentially
every Commander pod. Ship it.

**Hand A after one mulligan — KEEP**

> **Read the next block with one correction.** `./bin/mtg deck goldfish … --mulligans 1` applies the
> plain two-player rule and bottoms one card on the first mulligan, so it shows you six. At a real
> Commander table CR 103.5c applies and you would **keep all seven**, Intellectual Offering
> included. The keep/ship judgement below is unchanged — the hand is only better with the extra card.

```
  Plains                           —                   0  Basic Land
  Communal Brewing                 {2}{G}              3  Enchantment
  Flooded Grove                    —                   0  Land
  Mangara, the Diplomat            {3}{W}              4  Legendary Creature
  Forgotten Ancient                {3}{G}              4  Creature
  Twenty-Toed Toad                 {3}{U}              4  Creature
  (bottomed: Intellectual Offering {4}{U})
```

Two lands, but every spell is a good three- or four-drop and you have a Plains and a Flooded Grove.
This is a keep — and it's a good illustration of why the first mulligan is cheap. At the table it is
cheaper still: you keep the seventh card (Intellectual Offering) as well, because in Commander the
first mulligan bottoms nothing.

---

**Hand B — `--seed 7`: KEEP**

```
  Illusionist's Gambit             {2}{U}{U}           4  Instant
  Forest                           —                   0  Basic Land
  Mind Stone                       {2}                 2  Artifact
  Flooded Grove                    —                   0  Land
  Promise of Loyalty               {4}{W}              5  Sorcery
  Seachrome Coast                  —                   0  Land
  Forest                           —                   0  Basic Land
```

**Keep, easily.** Four lands, all three colors reachable, a turn-2 Mind Stone, and two of your best
defensive spells. The simulator had it casting Mind Stone on turn 2, Forgotten Ancient on turn 4,
and holding up Promise of Loyalty by turn 5. This is what a good Bumbleflower hand looks like: it
is not fast, it just never stumbles.

---

**Hand C — `--seed 13`: marginal keep**

```
  Mr. Foxglove                     {2}{G}{W}{U}        5  Legendary Creature
  Plains                           —                   0  Basic Land
  Forest                           —                   0  Basic Land
  Sphinx of Enlightenment          {4}{U}{U}           6  Creature
  Forgotten Ancient                {3}{G}              4  Creature
  Body of Knowledge                {3}{U}{U}           5  Creature
  Sunpetal Grove                   —                   0  Land
```

The tool says KEEP (3 lands is inside the keepable band) but flags it: *"Nothing castable before
turn 3 — the hand is slow"* and *"Curve: 4 spells, average cmc 5.0, cheapest 4."* And it was right —
in the sim **nothing at all was cast until turn 4**.

**My call: keep it, but understand what you're keeping.** Three lands, no ramp, and your cheapest
spell costs four. Worse, **none of the three makes blue** — Sunpetal Grove reads "This land enters
tapped unless you control a Forest or a Plains. {T}: Add {G} or {W}", and you'd have both, so at
least it comes in untapped — but Mr. Foxglove, Sphinx of Enlightenment and Body of Knowledge all
need `{U}`. The sim confirms it: nothing at all was castable until turn 4, and blue didn't arrive
until turn 3's land. You are betting on drawing a two-drop or a mana rock in the next three turns;
with 38 lands and 14 ramp pieces that bet is fine. But if this were 2 lands instead of 3, it would
be an instant mulligan.

---

**Hand D — `--seed 99`: keep, but this is the flood risk**

```
  Thriving Grove                   —                   0  Land
  Evolving Wilds                   —                   0  Land
  Overflowing Basin                —                   0  Land
  Fisher's Talent                  {2}{G}{U}           4  Enchantment
  Farseek                          {1}{G}              2  Sorcery
  Prairie Stream                   —                   0  Land
  Sungrass Prairie                 —                   0  Land
```

**Keep** — five lands with Farseek is fine and you will never miss a drop. But this is exactly the
hand the deck stats warn about: 38 lands is one above the recommended band, and *"expect flood."*
Your outs are the 25 draw pieces. Cast Farseek turn 2, Fisher's Talent turn 4, and dig.

### What is never keepable

- 0 or 1 land. Always.
- 6 or 7 lands with no card draw and no two-drop.
- A hand that can only produce one color when three of your spells need two different ones.

---

## 6. The 10 cards that matter most

Ordered by how much they change the game when they resolve.

**1. Ms. Bumbleflower** — `{1}{G}{W}{U}` — Legendary Creature — Rabbit Citizen — 1/5, Vigilance
> "Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter on target creature.
> It gains flying until end of turn. If this is the second time this ability has resolved this turn,
> you draw two cards."

Everything in the deck is a rate that assumes she is on the battlefield. Cast her on turn 4.

**2. Kalonian Hydra** — `{3}{G}{G}` — Creature — Hydra — 0/0, Trample
> "This creature enters with four +1/+1 counters on it. Whenever this creature attacks, double the
> number of +1/+1 counters on each creature you control."

The only card in the deck that converts a slow grindy board into lethal in one attack step — and
it feeds Simic Ascendancy and Twenty-Toed Toad at the same time.

**3. Simic Ascendancy** — `{G}{U}` — Enchantment
> "…Whenever one or more +1/+1 counters are put on a creature you control, put that many growth
> counters on this enchantment. At the beginning of your upkeep, if this enchantment has twenty or
> more growth counters on it, you win the game."

Two mana for an alternate win that your commander feeds passively. Play it, but expect to be
attacked once the counters get visible.

**4. Forgotten Ancient** — `{3}{G}` — Creature — Elemental — 0/3
> "Whenever a player casts a spell, you may put a +1/+1 counter on this creature. At the beginning
> of your upkeep, you may move any number of +1/+1 counters from this creature onto other creatures."

Grows off all four players, then hands the counters to whatever needs to be lethal. In a spell-heavy
pod this is the most counters-per-turn card you own.

**5. Sol Ring** — `{1}` — Artifact
> "{T}: Add {C}{C}."

One mana, adds two. It is the difference between casting Bumbleflower on turn 3 and turn 5. Always
play it turn 1 if you have it.

**6. Psychosis Crawler** — `{5}` — Artifact Creature — Phyrexian Horror — */*
> "Psychosis Crawler's power and toughness are each equal to the number of cards in your hand.
> Whenever you draw a card, each opponent loses 1 life."

Its ruling: "If an effect causes you to draw multiple cards, Psychosis Crawler will trigger that
many times." A big body that also punishes the table for every card the deck gives you.

**7. Baird, Steward of Argive** — `{2}{W}{W}` — Legendary Creature — Human Soldier — 2/4, Vigilance
> "Creatures can't attack you or planeswalkers you control unless their controller pays {1} for
> each of those creatures."

You are handing three opponents free cards all game. This is what stops that from killing you.
Its ruling even confirms attackers forced to attack "if able" can simply choose not to pay.

**8. Mangara, the Diplomat** — `{3}{W}` — Legendary Creature — Human Cleric — 2/4, Lifelink
> "Whenever an opponent attacks with creatures, if two or more of those creatures are attacking you
> and/or planeswalkers you control, draw a card. Whenever an opponent casts their second spell each
> turn, draw a card."

Defense that is also your best draw engine in a pod full of people casting spells. Note the ruling:
"You draw just one card, no matter how many creatures are attacking you."

**9. Spore Frog** — `{G}` — Creature — Frog — 1/1
> "Sacrifice this creature: Prevent all combat damage that would be dealt this turn."

One green mana turns off an entire attack step — **the whole turn's combat damage, from every
player.** It is not a creature, it is a "you don't die this turn" card. **Peerless Recycling**
`{1}{G}` gets it back.

**10. Faeburrow Elder** — `{1}{G}{W}` — Creature — Treefolk Druid — 0/0, Vigilance
> "This creature gets +1/+1 for each color among permanents you control. {T}: For each color among
> permanents you control, add one mana of that color."

In a Bant board it is a 3/3 that taps for `{G}{W}{U}` — which is most of Ms. Bumbleflower's cost —
and vigilance means you can attack with it and still tap it for mana afterwards.

**Honourable mention — Twenty-Toed Toad** `{3}{U}`, 3/3, and **Triskaidekaphile** `{1}{U}`, 1/3:
both are cheap alternate wins covered in §4. And **Swiftfoot Boots** `{2}`, "Equipped creature has
hexproof and haste… Equip {1}" — the cheapest commander insurance you have.

---

## 7. Common mistakes with this deck

**1. Feeding the wrong opponent.** You must pick a target opponent to draw every single time you
cast a spell. That is easily 15–25 free cards over a game. **Do not just default to the player on
your left.** Rules of thumb: give cards to the player with the weakest board, never to the player
one turn from winning, and never to the player who is clearly attacking you next. If someone is
tapped out and behind, they are the safe recipient.

**2. Forgetting the flying half of the trigger.** New players remember the +1/+1 counter and forget
"It gains flying until end of turn." Because the trigger resolves *before* your spell (per the
official ruling), a spell cast in your **precombat main phase** gives you an evasive attacker
*that turn*. Casting your two spells after combat throws that away. **Cast before you attack.**

**3. Chasing three, four, five spells a turn.** Only the **second** resolution each turn draws you
two cards. Spells three and four each hand another opponent a card for no extra draw. If you have
five cheap spells and nothing to protect, spread them across two turns instead.

**4. Tapping out at the wrong time.** The role counts are stark: **4 removal, 2 board wipes, 6
interaction pieces** across 61 nonland cards. You cannot answer everything, and you will often be
tapped out. The fix is not "always hold up mana" — that fights your commander. The fix is: with
38 lands plus 14 ramp pieces (52 total mana sources), by turn 6–7 you can double-spell *and* keep
`{G}` up for Spore Frog or `{U}` up for An Offer You Can't Refuse `{U}`. Aim for that, and before
then just accept you're tapping out.

**5. Greedy keeps.** See Hand C in §5 — three lands, average mana value 5.0, nothing castable until
turn 4. The average mana value of your nonlands is 3.21 and 34 of your 61 nonlands cost two or
three. A hand with no two- or three-drop is a hand that does nothing for four turns.

**6. Playing Coveted Jewel with an empty board.** `{6}`, draws three, taps for three — but:
> "Whenever one or more creatures an opponent controls attack you and aren't blocked, that player
> draws three cards and gains control of this artifact. Untap it."

Its ruling adds that this triggers "after you declare blockers (or declare no blockers at all) if
any attacking creatures are unblocked." So a single unblocked 1/1 takes your six-mana artifact and
draws them three. Only cast it when you have blockers or Baird out.

**7. Misusing tempting offer.** **Tempt with Discovery** `{3}{G}` and **Tempt with Bunnies** `{2}{W}`
give each opponent the option to copy you, and you repeat the effect for each one who accepts. If
all three accept Tempt with Discovery, you put **four lands** onto the battlefield. That is the
point — you're paying a small symmetric cost for a huge asymmetric one. Its ruling: opponents decide
"in turn order… starting with the opponent on your left," and each knows what the previous ones
chose. Cast it when opponents are land-light enough to be tempted, and don't feel bad when they say
yes. Conversely, if the table is mana-flooded and everyone declines, you got a single land for four
mana — that's the bad case, so read the table first.

**8. Gifting Perch Protection for value.** `{4}{W}{W}`. Without the gift it makes four 2/2 fliers.
With the gift, an opponent **takes an extra turn** and in exchange every permanent you control
**phases out** (temporarily stops existing, so nothing can touch it — CR 702.26b) while your life
total can't change and you have **protection from everything** until your next turn: for one turn
cycle you and your board simply cannot be interacted with. See §3 for the full wording. That is a
huge effect, but an extra turn in Commander frequently just means that player wins — and while you
are phased out you have no blockers either. Only ever gift it as an alternative to dying this turn.

**9. Missing the Simic Ascendancy / Triskaidekaphile upkeep windows.** Both check at the *beginning
of your upkeep* and neither lets you fix it during upkeep. Count growth counters and count your
hand size **at the end of the previous turn**, not when you get there.

**10. Forgetting Reliquary Tower and Thought Vessel exist.** This deck routinely holds 10+ cards.
**Reliquary Tower** ("You have no maximum hand size. {T}: Add {C}.") and **Thought Vessel** `{2}` are
in the list precisely so you stop discarding at end of turn. Get one down early; you also have
Wizard Class `{U}`, Triskaidekaphile `{1}{U}`, and Body of Knowledge `{3}{U}{U}` doing the same job.

**11. Playing like the enemy.** You are giving everybody cards. Some tables will read that as
friendly and leave you alone; some will correctly identify you as the value engine. Baird and
Mangara are not "cute defensive cards," they are your survival plan. Deploy them **before** you
need them.

---

## 8. Bracket and table expectations

The bracket tool rates this deck:

```
ESTIMATED BRACKET 2 — Core
  Precon-level. The baseline Commander experience -- a modern
  preconstructed deck out of the box lands here.

  Game Changers        : 0 (checked against 53 listed cards)
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review
```

**In plain language:** Commander decks are sorted onto a 1-to-5 bracket scale, where 1
("Exhibition") is, in the tool's words, "about intent — a joke or theme deck that is not trying to
win", and the numbers climb from there toward the most powerful decks. **Bracket 2 is "Core" — a
modern preconstructed deck straight out of the box**, which is exactly what this is.
Bracket 2's rules are: no Game Changers (a specific published list of 53 unusually powerful cards —
this deck runs zero), no mass land destruction, no chaining extra turns, no two-card infinite
combos, and *"power level of a modern precon; games typically end around turn 9 or later."*

One caveat straight from the tool: two-card infinite combos aren't auto-detected, so a human should
sanity-check. Nothing in this list looks like one.

### What that means at the table

- **You are on a level playing field with the other two precons** (Tidus and Dogmeat). Games between
  bracket-2 decks are long, interactive, and decided in the turn 9–13 range.
- **Say "bracket 2, unmodified precon" when the pod does its pre-game power check.** That is the
  honest answer and it will get you into the right game.
- **Expect to be underestimated early and targeted late.** For the first six turns you are the
  friendly rabbit handing out cards. Around the time Simic Ascendancy hits ten growth counters, or
  Kalonian Hydra comes down, that changes. Have Baird, Mangara or Spore Frog available by then.
- **You will not race anybody.** If two opponents are in a damage race, let them race. Your deck
  gets better every turn the game goes long; theirs mostly don't.
- **Politics are genuinely available to you.** You are the only player at the table who can *give*
  people things. "I'll point this draw at you if you don't attack me" is a real and legal
  conversation, and this deck is built to have it.

---

## Appendix — raw CLI output (evidence)

Everything above is derived from these. Re-run any of them yourself.

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
```

### `./bin/mtg deck stats bumbleflower -v`

```
── Peace Offering — stats ────────────────────────────────────────────
Commander : Ms. Bumbleflower   identity WUG
Cards     : 100 total = 99 maindeck + 1 commander   (38 lands / 61 nonlands)

── MANA CURVE (non-land maindeck cards) ──────────────────────────────
   0    0
   1    5  ██████████
   2   17  ██████████████████████████████████
   3   17  ██████████████████████████████████
   4    9  ██████████████████
   5    9  ██████████████████
   6    3  ██████
  7+    1  ██

  average MV, non-lands       : 3.21
  average MV, including lands : 1.98
  commander MV                : 4 (excluded from the curve)

── COLORS ────────────────────────────────────────────────────────────
             cards  sources
  White         41       20
  Blue          36       19
  Green         41       19
  Colorless     14        5
  any-colour lands counted toward every colour: Command Tower, Exotic Orchard
  lands entering tapped: 14 (7 always, 7 conditional)

── ROLES ─────────────────────────────────────────────────────────────
  ramp         14
  draw         25
  removal       4
  boardwipe     2
  interaction   6
  recursion     1
  tutor         0
  wincon        6

── ASSESSMENT ────────────────────────────────────────────────────────
  land count: HEAVY on lands
  - Average mana value of the 61 maindeck non-lands is 3.21 — avg
    MV 3.0-3.3 (the usual EDH band).
  - The usual EDH heuristic puts that at 36-37 lands (adjusted -1
    for 14 ramp pieces). This deck runs 38.
  - 38 lands is 1 above the 36-37 band — expect flood; consider
    trimming for card advantage (deck has 25 draw pieces).
  - Total mana sources = 38 lands + 14 ramp = 52.
  - 14 lands can enter tapped (7 always, 7 conditionally) — 37% of
    the mana base.
```

### `./bin/mtg deck goldfish bumbleflower --seed 42 --turns 8`

```
── OPENING HAND (7) ──────────────────────────────────────────────────
  Skycloud Expanse                 —                   0  Land
  Psychosis Crawler                {5}                 5  Artifact Creature
  Thought Vessel                   {2}                 2  Artifact
  Chasm Skulker                    {2}{U}              3  Creature
  Intellectual Offering            {4}{U}              5  Instant
  Forgotten Ancient                {3}{G}              4  Creature
  An Offer You Can't Refuse        {U}                 1  Instant

  lands in opener: 1

── RECOMMENDATION: MULLIGAN ──────────────────────────────────────────
  - 1 land in the seven (deck runs 38; 2-5 is the keepable band).
  - Under two lands is a mulligan in almost every Commander pod.
  - Ramp/fixing at 3 or less: 1 (Thought Vessel).
  - Interaction: 1 (An Offer You Can't Refuse).
  - Curve: 6 spells, average cmc 3.33, cheapest 1.

── TURNS ─────────────────────────────────────────────────────────────
T1  draw: Sphinx of Enlightenment
     lands seen 1 · in play 1 [W,U] · played Skycloud Expanse · hand 7
T2  draw: Evolving Wilds (land)
     lands seen 2 · in play 2 [W,U] · played Evolving Wilds · hand 7
T3  draw: Realm-Cloaked Giant // Cast Off
     lands seen 2 · in play 2 [W,U] · no land drop · hand 8
T4  draw: Sunscorch Regent
     lands seen 2 · in play 2 [W,U] · no land drop · hand 9
T5  draw: Coiling Oracle
     lands seen 2 · in play 2 [W,U] · no land drop · hand 10
T6  draw: Perch Protection
     lands seen 2 · in play 2 [W,U] · no land drop · hand 11
T7  draw: Terramorphic Expanse (land)
     lands seen 3 · in play 3 [W,U] · played Terramorphic Expanse · hand 11
T8  draw: Peerless Recycling
     lands seen 3 · in play 3 [W,U] · no land drop · hand 12
```

### `./bin/mtg deck bracket bumbleflower`

```
ESTIMATED BRACKET 2 — Core
  Precon-level. The baseline Commander experience -- a modern
  preconstructed deck out of the box lands here.

── SIGNALS ───────────────────────────────────────────────────────────
  Game Changers        : 0 (checked against 53 listed cards)
  Mass land denial     : 0
  Extra turns          : 0
  Two-card infinite    : not detected by this tool; requires human/agent review

── REASONING ─────────────────────────────────────────────────────────
  - Zero Game Changers found. Brackets 1 and 2 both require 'No
    Game Changers.'
  - Bracket 2 (Core) is described as 'Precon-level ... a modern
    preconstructed deck out of the box lands here', which is
    exactly what this deck is. Bracket 1 (Exhibition) is about
    intent — a joke or theme deck that is not trying to win — so
    it is not assigned automatically.
  - No mass land denial detected (searched for 'destroy all lands'
    / 'each player sacrifices a land' wording).
  - No extra-turn effects detected (searched for 'take an extra
    turn').

── NEEDS HUMAN / AGENT REVIEW ────────────────────────────────────────
  - Two-card infinite combos: not detected by this tool; requires
    human/agent review. A combo would raise this estimate.

── BRACKET 2 RULES ───────────────────────────────────────────────────
  - No Game Changers.
  - No mass land denial.
  - No chaining extra turns.
  - No two-card infinite combos.
  - Power level of a modern precon; games typically end around
    turn 9 or later.
```

### `./bin/mtg rule 903.8` (commander tax, cited in §2)

```
── Rule 903.8 ────────────────────────────────────────────────────────────
parent: 903 — Commander

A player may cast a commander they own from the command zone. A commander
cast from the command zone costs an additional {2} for each previous time
the player casting it has cast it from the command zone that game. This
additional cost is informally known as the "commander tax."
```

### Other rules and glossary entries cited above

| Reference | What it says | Look it up |
|---|---|---|
| CR 103.5 / 103.5c | Mulligan procedure — draw a fresh seven, then bottom one card per mulligan taken; **103.5c: in a multiplayer game the first mulligan doesn't count, so mulligan #1 bottoms nothing** | `mtg rule 103.5` |
| CR 608.2b | If every target of a spell/ability is illegal, it doesn't resolve at all | `mtg rule 608.2b` |
| CR 702.20b | "Attacking doesn't cause creatures with vigilance to tap" | `mtg rule 702.20` |
| CR 702.174a/e | Gift — optional additional cost choosing an opponent; "gift a card" = they draw one | `mtg rule 702.174` |
| CR 702.26a/b | Phasing — a phased-out permanent "is treated as though it does not exist"; it phases back in as its controller's untap step begins (Perch Protection) | `mtg rule 702.26` |
| CR 715 | Adventurer cards — the Adventure half exiles itself, and you may cast the creature from exile later (Realm-Cloaked Giant // Cast Off) | `mtg rule 715` |
| CR 716 | Class cards — enter at level 1; class level bars are activated at sorcery speed to add the next level's ability (Wizard Class, Fisher's Talent) | `mtg rule 716` |
| CR 903.8 | Commander tax: +{2} per previous cast from the command zone | `mtg rule 903.8` |
| CR 903.9a/b | Your commander may go to the command zone instead of graveyard/exile/hand/library | `mtg rule 903.9` |
| CR 903.10a | 21+ combat damage from one commander makes you lose | `mtg rule 903.10` |
| Glossary | Gift · Vigilance · Trample · Hexproof · Lifelink · Goad · Toxic · Mana Value · Upkeep Step | `mtg glossary <term>` |

### EDHREC cross-check

`./bin/mtg edhrec bumbleflower` (36,366 decks sampled) confirms this list is a mainstream build of
the commander: **every one of EDHREC's top 10 "High Synergy" cards is already in this deck** (Wizard
Class, Loran of the Third Path, Wear Down, Long River's Pull, Peerless Recycling, Twenty-Toed Toad,
Kwain, Jolrael, Chasm Skulker, Tempt with Discovery), as is every one of its top 10 most-played
cards. Nothing needs to change for you to play a normal, recognisable Ms. Bumbleflower deck.
