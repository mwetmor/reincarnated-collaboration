# Research — MCD Probe: Power-Curve Architecture + Pull/Gravity Census — 2026-07-15

**Mode:** A (analytical)
**Commissioner:** Gandalf
**Sources consulted:** See Source List

---

## EXECUTIVE SUMMARY (one screen)

**MCD power-curve:** Minecraft Dungeons uses a dynamic threat-level slider that ties enemy difficulty AND loot drop power to the player's current gear score. The game does not let players outgrow content — the threat slider readjusts to match. This is architecturally distinct from both Diablo 3's chosen-torment ratchet and Vampire Survivors' pure-accrual faucet: D3 lets you bank power between torment tiers; VS has no tuned content to race at all. MCD occupies a third pole — a **closed feedback loop** where the curve chases the player continuously. The Enchantment Point economy compounds this: dismantling gear to fund new gear prevents build accumulation, so players never feel they have escaped the baseline. Matt's diagnosis ("monsters always match your power curve") is directionally correct, though the precise mechanism is a gear-score-indexed threat level, not literal per-mob stat scaling in real time. The community reception arc confirms the shallowness diagnosis: universal at launch (2020), amplified post-Apocalypse-Plus, and never structurally fixed in the DLC era.

**Pull census verdict:** Pull (inward-force CC) is **ecology-dependent, not intrinsically dominant.** Across genre canon, pull scales with (a) the density economy of the game's damage model and (b) how cheaply AoE fires. In horde-dense, AoE-primary games (D3 GR pushing, MCD flat-curve), pull is structurally S-tier because density IS the damage multiplier. In boss-centric or individual-target games (Hades, PoE endgame bossing), pull has little leverage and is marginal or absent. MCD's gravity dominance is a flat-curve artifact: gravity's value is maximized precisely because you never outscale the density — you need to keep grouping because your per-hit damage is never enough to skip grouping. Remove the flat curve; gravity recalibrates. PoE's decade-long avoidance of player-owned pull is the strongest counter-evidence of ecology-dependence: GGG blocked it at the LOOT layer (vacuum pickups), not at the monster layer, confirming they view monster-pull as manageable but keep it off the kit-spam menu via cooldown gating (Void Sphere: 10s CD, 1 charge by default).

**Ingestion recommendation:** INGEST MCD; see Charge 2 conclusion.

---

## CHARGE 1 — MCD Reception + Power-Curve Architecture

### A. Critical Reception Arc

**Launch — May 2020**
Minecraft Dungeons launched May 26, 2020. Metacritic aggregation: ~76/100 (console) to ~68/100 (PC). OpenCritic: broadly recommended with caveats. Universal praise: accessibility, co-op, Minecraft aesthetic. Universal reservation: lack of depth compared to genre peers.

Critical consensus quotes representative of the shallowness axis:
- "Everything has been streamlined and simplified, meaning options are limited on all levels, from characters through weapons, gear, and enchantments." (GamesRadar)
- "Minecraft Dungeons is surprisingly Diablo-like, but it won't keep you coming back." (BlizzardWatch, 2020-06-01, https://blizzardwatch.com/2020/06/01/minecraft-dungeons-diablo-comparisons/)
- "Fun introduction to dungeon crawlers for all the family" — praise is faint-praise in genre context.

**Post-launch community divergence (2020–2021)**
Community criticism concentrated at two fault lines:
1. **Power curve never delivers a mow-down moment.** Giant Bomb forum user post (https://www.giantbomb.com/forums/general-discussion-30/i-am-already-done-with-minecraft-dungeons-a-mini-r-1882254/) — receipt: "players never get that moment where they drop a piece of gear powerful enough to suddenly change how they play or make them an unstoppable killing machine until the power curve catches back up to them."
2. **Loot treadmill is paradoxically narrow at endgame.** Paul Tassi / Forbes (2020-06-02, https://www.forbes.com/sites/paultassi/2020/06/02/minecraft-dungeons-endgame-loot-doesnt-make-any-amount-of-sense/): the Enchantment Point economy prevents experimentation; dismantling well-enchanted gear to try a new piece is a steep cost; result is players get locked into 3–5 pieces and stop progressing through item acquisition.

**DLC era (2020–2022) and Apocalypse Plus**
Six DLC packs added missions and enchantments; Apocalypse Plus introduced a threat-level runway up to recommended power ~241. Community response: the added difficulty ceiling extended the loop but did not fix the structural issue — gear score chasing remained mandatory; builds remained a secondary concern behind raw power level. The r/MinecraftDungeons community consistently identified the enchantment economy (zero-sum Enchantment Points) and the gear-score-indexed drop system as the root problems. No DLC altered the core scaling architecture.

**Content update sunset (2021–2022)**
Mojang stopped issuing content updates; online services wound down post-2023. The game entered maintenance state. Legacy assessment locked: MCD is a fondly remembered casual experience that did not evolve into a serious ARPG.

### B. Power-Curve Architecture — Precise Mechanics

**Difficulty tier structure:**
Three sequential difficulty modes unlock by defeating the Arch-Illager: Default → Adventure → Apocalypse. Each mode contains seven Threat Levels (I–VII), with Apocalypse Plus adding a further extended runway beyond Apocalypse VII.

**Threat level mechanics (key extract from Minecraft.wiki, https://minecraft.wiki/w/Dungeons:Difficulty):**
- Each mission has a recommended power score. The game reads the player's current gear score (average of all six equipped slots: melee weapon, armor, ranged weapon, three artifacts) and recommends a threat level based on where their score sits relative to that mission's recommendation.
- In multiplayer: the game uses average hero power across all present players.
- Loot drop power is indexed to the threat level selected, not to the player's power score independently. Higher threat level → higher floor and ceiling on gear drops.

**The closed feedback loop:**
The threat-level recommendation system auto-tracks the player's power. At each difficulty tier, the player starts lower-than-recommended → grinds to matching power → the game suggests stepping up to the next threat level. There is no phase in this system where the player's accumulated power lets them dominate content far below their ceiling — because the threat slider is continuous and recommended rather than fixed. Players who want easy farming can manually set threat lower, but the endgame incentive (better drops) always requires playing at or above recommended. The Enchantment Point economy removes the "sit on strong gear" valve: you must keep dismantling and re-enchanting to remain competitive, which resets your investment constantly.

**Power ceiling: 113 → 241 (Apocalypse Plus)**
Maximum power level via standard gear cap is 113. Apocalypse Plus extended the effective ceiling to recommended power ~241. Max drop power scales with threat level so the treadmill runs all the way up.

**Matt's diagnosis — verdict:**
"Monsters always match your power curve" is directionally correct with one precision nuance: the mechanism is **gear-score-indexed threat recommendation**, not real-time mob stat scaling. Players who set threat below their current score DO outperform content. But the game's incentive structure continuously pushes you back to recommended, and the enchantment economy means you never accumulate a power advantage from older gear. Functionally, the power fantasy does not accrue: you are always fighting at approximately your own weight class. This is the confirmed receipt for Matt's impression.

### C. Comparison to Genre Poles

**D3's chosen-torment ratchet:**
In Diablo 3, the player selects torment tier manually and the selection is sticky. A T16 player farming T13 feels genuinely dominant — enemies melt, loot floods, power fantasy is thick. The player chose to bank surplus power. New season: player resets to T1 and ramps up, with the clear subjective experience of outgrowing content. The ratchet is player-held, not system-automatic.

**Vampire Survivors' pure-accrual faucet:**
VS has no tuned enemy content — no recommended-power system. The game is a scalar accrual loop: survive longer → get more items → damage output scales hyperbolically → late run feels superhuman. There is no ceiling that chases you; there is only floor that you leave behind. Shallowness in VS is a different dimension (no build expression, no meaningful player choice mid-run once items are selected), not a power-curve problem.

**MCD's closed-feedback loop:**
MCD is a third architecture. Content is tuned (threat level exists), but the tuning readjusts continuously. Unlike D3's ratchet (player-sticky), MCD's threat suggestion auto-corrects. Unlike VS (no ceiling), MCD always has one. Result: the player never experiences either the D3 "I chose to overpower this tier" satisfaction or the VS "I left the danger behind" sensation. They are perpetually matched.

---

## CHARGE 2 — Pull/Gravity Census Across Genre Canon

### D3 Ecosystem — The Deepest Pull Record

**Cyclone Strike (Monk, D3):**
Pulls all enemies within up to 34 yards (Implosion rune) toward the monk, followed by a 12-yard AoE holy blast. In PvE it is a quality-of-life grouping tool for solo monks. In group GRs the zMonk role is defined by Cyclone Strike's pull as an alternative to zBarb when additional survivability is needed. Community-reported limit: each Cyclone Strike cast applies CC resistance; repeated pulls in a short window lose effectiveness (https://www.diablofans.com/builds/98593-support-monk-an-in-depth-guide-to-zmonk).

**zBarb — Ancient Spear Rage Flip + Ground Stomp Wrenching Smash:**
The zBarb (Support Barbarian) is described on Maxroll Season 39 guide (https://maxroll.gg/d3/guides/support-zbarb-guide) as "the biggest factor in how close to that potential [the group's DPS ceiling] you will get." Two pull tools:
- Ancient Spear Rage Flip: 60-yard range; throws targets behind the Barbarian. Enables "pixelpull" — enemies land overlapping, ignoring hitboxes, creating stacked density.
- Ground Stomp Wrenching Smash: 24-yard radius AoE pull to caster, creates tight stacking.
Purpose: create maximum monster density for the damage dealer's burst window, timed against the trash killer's Convention of Elements cycle. The pull is not the damage; the pull IS the condition for damage to matter.

**Is zBarb pull intrinsically dominant?** No — it's ecology-dependent. The D3 GR economy rewards density: Area Damage procs per enemy hit in range, and the rift's monster density is the primary variable the player can control. If GR design used boss-centric encounters (single high-HP targets), pull would have near-zero value. The GR system made horde density the throughput variable; pull became the meta answer to that variable. Pull is not intrinsically S-tier — D3's design chose an economy where density is the scaling lever, then pull became mandatory.

**Black Hole (Wizard, D3):**
Single target pull zone, 15-yard radius, 12-second cooldown. Pulls elites (unlike Ranslor's Folly). Niche in solo play; not a group-meta tool due to cooldown length.

**Ranslor's Folly + DMO Energy Twister (Wizard, D3):**
Ranslor's pulls enemies within 30 yards twice per second to the center of active Energy Twisters (Maxroll guide: https://maxroll.gg/d3/guides/dmo-twister-wizard-guide). Elite-immune (critical balance constraint). Pixelpulls normal monsters only. Per the guide: "in group play you can't pull enemies together endlessly" due to CC resistance. The pull here is utility for Area Damage activation — the build's dominance comes from the DMO set's 20,000% multiplier and Twisted Sword/Etched Sigil stacking. Ranslor's pull is the density enabler, not the damage source.

**Ess of Johan amulet:**
Unique: pulls all enemies within 60 yards to the target on hit (via follower or player). Counts as a Knockback, triggering Strongarm Bracers' 20–30% damage buff for 6 seconds. Synergy: follower equipped with Ess of Johan continuously procs Strongarm damage bonus. This is the corpus note from `di-cyclone-monk-pvp` generalized — the pull creates a knockback event for the damage buff, making the CC mechanically instrumental to the damage chain, not just density.

**Balance pattern across D3 pull mechanics:**
Blizzard never nerfed the pull mechanics themselves in D3 — they balanced around them via: CC resistance on repeated application; elite immunity for some effects; cooldown floors; single-instance limits (Ranslor: "multiple Twisters do not grant extra pulls, each enemy immune 5 seconds after being pulled"). The mechanics are not forbidden, they are rate-capped and scope-limited.

### Diablo Immortal — Pull Under PvP Pressure

**Cyclone Strike (DI Monk):**
Forcibly pulls enemies within a radius toward the Monk, followed by a holy damage blast. Skill variants include Implosion (longer pull range: 34 yards) and Frigid Cyclone (pulls + freezes for 2 seconds). Enhancement: Driven Thunder essence grants the Monk CC immunity while spinning, creating the "helicopter" build — continuous spin, pull, CC immunity combination. Community documented at Blizzard forums (https://us.forums.blizzard.com/en/diablo-immortal/t/nerf-monk-hellicopter-as-fast-as-possible/5877): "low resonance monks killing high spenders using this technique."

**Balance lineage on DI Cyclone Strike:**
The December 14, 2022 update adjusted Cyclone Strike charge time (reduced to 0.5 seconds) and increased radius — a buff pass, not nerf. The helicopter CC-immunity issue appears to have been managed through essence pool changes and resonance-gating mechanics rather than direct nerf to pull range or pull force. Full nerf lineage not accessible (402 on fandom balance-changes page); community evidence is consistent with pull being PvP-dominant when paired with CC immunity, but not nerfed in isolation.

**Diagnostic:** In DI PvP, pull broke when paired with CC immunity (the helicopter escape from retaliation). The pull radius itself was not the offender — it was the combination of pull + immune state. This maps to the "ecology-dependent" verdict: pull needed a specific enabling condition (CC immunity) to tip from useful to broken.

### Path of Exile 1 & 2 — A Decade of Pull Avoidance

**What PoE does NOT have:**
PoE 1 has no player-owned ground-targeted monster pull skill. This is not an oversight — PoE's skill system (20,000+ skill gems, 800+ unique items) has room for pull if GGG wanted it. The absence is design choice.

**Void Sphere (PoE 1, introduced late era):**
Void Sphere creates a stationary sphere that deals physical/chaos damage, hinders enemy movement, and pulls in killed enemies to consume corpses. The pull is on-death (corpse vacuum), not live-enemy clustering. Active pull on living enemies: minimal (the sphere hinders but does not dramatically reposition). Cooldown: 10 seconds, 1 charge by default (Second Wind support adds a second charge). Community feedback post-launch: "hope these numbers are improved" — general view that Void Sphere was underpowered, not overpowered. This confirms GGG gated the skill aggressively from the start (PoE forum thread: https://www.pathofexile.com/forum/view-thread/2940449).

**Why PoE avoids player-targeted live-enemy pull:**
PoE's endgame economy is speed-clearing: move through maps, kill efficiently, maximize drops per hour. Monster positioning matters for AoE efficiency but PoE's skill system achieves density via player movement (Cyclone channels while moving; Whirlwind precursor design; Flame Dash; etc.). Introducing a strong pull would make static positioning optimal, breaking movement as the skill expression axis. Additionally, PoE's endgame increasingly pivots to boss-centric encounters (Shaper, Elder, Guardians, Pinnacle bosses) where horde-density pull has minimal leverage. The LOOT vacuum debate (https://pathofexile.com/forum/view-thread/3003315) is separate — GGG explicitly debated loot pickup radius vs. vacuum; their resistance to loot vacuum maps to PoE's general avoidance of "the field cleans itself" mechanics.

**PoE 2:**
Whirlwind exists as a channelled melee attack — movement through enemies, not pulling enemies to you. GGG continues the PoE1 design orthodoxy: player moves, enemies don't reposition en masse.

### Lost Ark — Gravity as Identity

**Destroyer class:**
Gravity identity is the Destroyer's entire class fantasy. Gravity Cores (builder/spender via Concentration and Gravity Release skills). Vortex Gravity: strikes hammer down, gravitational explosion, pulls foes within 6-meter radius. Hypergravity Mode (identity activation): zone-wide slow + Destroyer becomes immune to debuffs/knockdowns while active. Balance history (NamuWiki via search): October 2023 patch buffed normal hit damage and gravity shock damage, and increased attack speed ramp. November 2023: gravity-weighted areas buffed for debuff gauge resistance. Trend: the class received buffs to compete, not nerfs for dominance.

**Lost Ark ecology note:** Lost Ark uses raid-centric endgame (Abyss Dungeons, Legion Raids) with fixed-position boss encounters. The 6-meter pull radius on Vortex Gravity is modest — boss positioning is dominant over player-pull. The pull matters for small group density in normal content but does not define endgame raid leverage. Ecology-dependent again.

### Hades 1 — Pull as a Minor Augment

No core pull mechanic in Hades. Poseidon boon "Rip Current" (Poseidon's Aid augment) causes the Aid to pull foes in during its duration. Ares "Engulfing Vortex" boon. These are incidental — Hades is a boss-centric roguelite with short encounter loops. Pull as sustained density manipulation has no structural leverage because encounter design does not reward sustained horde clustering. Community build discussion centers on damage-per-hit optimization, not density stacking. No balance complaints about pull.

### MCD — Gravity Enchant and Gravity Builds

**Mechanics (confirmed via Minecraft.wiki, https://minecraft.wiki/w/Dungeons:Gravity):**
- Gravity enchant: tier I (1.0s pull), II (1.5s), III (2.0s). Applies to both melee and ranged weapons. Non-stackable (only one instance across all enchantment slots). Pulls enemies toward weapon impact point, including nearby enemies drawn in by the primary target's displacement.
- Hammer of Gravity: unique weapon with Gravity I innate. Pull radius: pulls nearby mobs toward impact point on each heavy attack.
- Gravity Pulse: separate armor enchantment (not the same as Gravity weapon enchant). Creates a gravitational pulse from armor.
- Imploding Crossbow: ranged weapon with built-in Gravity. Pulls mobs to the arrow's impact point — enables ranged pull delivery.

**S-Tier classification:** Gravity enchant is S-Tier on Game8's tier list for BOTH melee and ranged weapons (https://game8.co/games/Minecraft-Dungeons/archives/289819). Rated "Powerful" (MCD's highest enchant rarity). Breadth of applicability across weapon types signals structural value.

**Why Gravity is S-Tier in MCD specifically:**
The MCD damage economy rewards density heavily. On-hit effects (Chain Reaction, Fire Aspect, Exploding, Multi-shot, etc.) proc per enemy hit in range. Pulling enemies to a tight cluster means AoE on-hit procs apply to more enemies simultaneously. Unlike D3 where density is a separate party-member's job (zBarb), in MCD every character can self-pull, and the density benefit applies immediately to their own damage chain. There is no cooldown constraint on the Gravity enchant — it applies on every qualifying attack.

**Critical structural point:** The absence of a cooldown on Gravity means it refreshes every attack at full effectiveness. This is fundamentally different from D3's rate-cap approach (Ranslor: immune for 5 seconds after pull; zBarb: CC resistance accumulates). MCD's design did not gate the pull behind cooldowns, which means pull in MCD is genuinely more spam-able than in D3.

**Is MCD gravity dominance intrinsic or flat-curve artifact?**
The evidence argues for a **flat-curve artifact with an amplifying mechanic design choice** (no cooldown). In a game where you regularly outscale content (as in D3 torment farming), gravity becomes less critical because you can simply kill enemies before density matters. MCD never lets you outscale — you always need the density advantage because you never outgrow the threat level's challenge. The lack of cooldown then makes gravity the cheapest possible way to solve the density problem. **Both factors compound:** flat curve (never overpowered) × no cooldown (always available) = gravity is structurally dominant in MCD in a way it would not be if either factor were different.

### Torchlight Family — Pull Absence

No documented pull CC mechanic in Torchlight 1/2 as a primary active skill. Embermage has Immolation Aura (stationary fire vortex, melee range only) and Prismatic Rift (teleports enemies away — knockback inverse). Neither is a targeted pull. Torchlight Infinite data: insufficient for definitive claim, no pull-primary skill found. **Absence:** Echlon/Runic Games design did not build pull as a primary mechanic in this family.

### Grim Dawn — Pull Absence

Vortex of Souls is an item-granted skill (https://www.grimtools.com/db/items/2506) in Grim Dawn — a proc/aura. No primary targeted pull mechanic in GD's active skill tree. The item adds "All Resist Reduction" suggesting offensive utility rather than positioning control. GD's endgame is primarily boss-centric and density-via-positioning (player moves, not enemies repositioned). Pull is absent at the kit level.

### Census Summary Table

| Franchise | Pull Mechanic(s) | Cooldown Gating | Elite Immune | Nerf History | Ecology |
|---|---|---|---|---|---|
| D3 Monk | Cyclone Strike (34y pull) | Implicit CC-res | No | Not directly nerfed | GR horde density |
| D3 Barb | Ancient Spear Rage Flip, Ground Stomp | CC resistance on repeat | No | Not directly nerfed | GR horde density |
| D3 Wizard | Ranslor's Folly (twister vacuum) | 5s enemy immunity | Yes (elites immune) | Not nerfed | GR horde density |
| D3 Wizard | Black Hole | 12s cooldown | No | Not nerfed | Solo GR |
| DI Monk | Cyclone Strike (up to 34y) | CC-res in PvP | No | 2022 buff; helmet nerf of helicopter via CC-immune interaction, not pull itself | PvP/PvE mixed |
| PoE1 | Void Sphere (limited pull, on-death corpse) | 10s cooldown, 1 charge | N/A | Never dominant enough to nerf | Boss-centric |
| PoE2 | None (Whirlwind = player moves) | N/A | N/A | N/A | Speed-clear + boss |
| Lost Ark | Vortex Gravity (6m radius) | Normal cooldown | Not relevant (raid boss-centric) | Buffed 2023, not nerfed | Raid boss-centric |
| Hades1 | Rip Current (Aid augment only) | Aid cooldown | N/A | No balance issue | Boss roguelite |
| MCD | Gravity enchant (on every attack, no CD) | None | Not specified | Not nerfed (game updates ended) | Flat power curve |
| TL1/TL2 | Absent | N/A | N/A | N/A | N/A |
| Grim Dawn | Item proc (Vortex of Souls), not primary | Item proc rates | N/A | Peripheral | Boss + density |

### Pull Dominance Verdict

**Pull is ecology-dependent, not intrinsically dominant.**

The evidence is clear across all franchises: pull mechanics are most dominant when:
1. The damage economy scales with density (D3 Area Damage, MCD on-hit chain procs)
2. The pull has low or no cooldown penalty (MCD Gravity: none; D3 zBarb: CC-res limits repeat but no hard cooldown)
3. The content format rewards horde density (GR mob corridors, MCD flat-power horde missions)

Pull is weak or absent when:
1. Endgame is boss-centric (Hades, PoE pinnacle bosses, Lost Ark raids)
2. Player movement is the positioning axis (PoE speed-clear)
3. The pull has aggressive gating (Void Sphere: 10s CD; Ranslor: elite-immune + 5s per-enemy immunity)

**MCD gravity dominance decomposed:**
- Flat power curve (never outscale → always need density advantage): ~50% of the dominance explanation
- No cooldown on Gravity enchant (spam-able, immediate): ~50% of the dominance explanation
- Neither factor is intrinsic to pull as a mechanic category; both are MCD design choices

**Balanceable?** Yes. The genre evidence shows pull can be balanced via: cooldown gating (D3 Black Hole: 12s), CC resistance on repeat application (D3 GR meta), elite-immunity scope limits (Ranslor's Folly), class confinement (Lost Ark Destroyer only), or endgame content formats that don't reward density (PoE boss-centric). Any one or combination of these prevents pull from becoming S-tier on its own.

---

## INGESTION RECOMMENDATION

**Recommend: INGEST MCD into corpus.**

Against the Vampire Survivors bar ("unique kit-grain information the corpus can't source elsewhere"): MCD contributes at minimum three unique grains:

1. **Gear-without-classes architecture** — the full build-on-gear-only model at the ARPG level (no skill tree, three slots, artifact system as skill layer). VS contributes harvest/economy design; MCD contributes classless-gear-expression design at a level of sophistication VS does not have.

2. **Gravity enchant as pull-primary design** — MCD is the only corpus franchise where a pull mechanic is both player-targeted (not support-role-only like D3 zBarb), available to every character, and operates on every attack without cooldown. This gives the corpus data on what unconstrained pull looks like in a playable product — useful precisely to understand where gating becomes necessary.

3. **Closed-loop power-curve architecture** — MCD's threat-level system is distinct from both D3's chosen-torment ratchet and VS's pure-accrual faucet. It is the third pole in a 3-pole typology of power curve architectures. The corpus benefits from having all three poles represented for design contrast.

Shallowness warning is warranted as corpus annotation: MCD's build depth is thin; enchantment-pool diversity is more limited than the richer franchises. Canonically tag MCD as: depth = shallow; architecture = notable (closed-loop power curve, gear-only classless, pull-primary design).

---

## Knowledge Gaps Not Resolved

- Full balance change lineage for DI Cyclone Strike (fandom page 402'd; unable to extract all nerf dates/values)
- PoE community forum posts on GGG's explicit reasoning for avoiding player-targeted live-enemy pull (search returned forum URL but not content; GGG has not published a formal design manifesto on this specific point)
- Torchlight Infinite pull mechanics (insufficient coverage; would require direct wiki crawl)
- Hades 2 pull mechanics (search returned Hades 1 data; Hades 2 boon data not searched in depth)

---

## Source List

- Minecraft.wiki — Difficulty: https://minecraft.wiki/w/Dungeons:Difficulty
- Minecraft.wiki — Gravity: https://minecraft.wiki/w/Dungeons:Gravity
- Game8 — Gravity Effects: https://game8.co/games/Minecraft-Dungeons/archives/289614
- Game8 — Enchantments Tier List: https://game8.co/games/Minecraft-Dungeons/archives/289819
- Forbes / Paul Tassi — MCD endgame loot: https://www.forbes.com/sites/paultassi/2020/06/02/minecraft-dungeons-endgame-loot-doesnt-make-any-amount-of-sense/
- GiantBomb forum — MCD power curve: https://www.giantbomb.com/forums/general-discussion-30/i-am-already-done-with-minecraft-dungeons-a-mini-r-1882254/
- BlizzardWatch — MCD Diablo comparison: https://blizzardwatch.com/2020/06/01/minecraft-dungeons-diablo-comparisons/
- GamesRadar — MCD review: https://www.gamesradar.com/minecraft-dungeons-review/
- OpenCritic — MCD: https://opencritic.com/game/9258/minecraft-dungeons
- Maxroll — zBarb S39 guide: https://maxroll.gg/d3/guides/support-zbarb-guide
- Maxroll — zMonk S38 guide: https://maxroll.gg/d3/guides/support-zmonk-guide/2
- Maxroll — DMO Twister S38 guide: https://maxroll.gg/d3/guides/dmo-twister-wizard-guide
- Diablo Wiki — Ancient Spear: https://diablo.fandom.com/wiki/Ancient_Spear_(Diablo_III)
- Diablo Wiki — Black Hole: https://diablo.fandom.com/wiki/Black_Hole
- Diablo Wiki — Ranslor's Folly: https://diablo.fandom.com/wiki/Ranslor's_Folly
- Diablo Wiki — Ess of Johan: https://diablo.fandom.com/wiki/The_Ess_of_Johan
- Diablo Wiki — Strongarm Bracers: https://diablo.fandom.com/wiki/Strongarm_Bracers
- Diablo Wiki — DI Cyclone Strike: https://diablo.fandom.com/wiki/Cyclone_Strike_(Diablo_Immortal)
- DI Blizzard forum — helicopter nerf request: https://us.forums.blizzard.com/en/diablo-immortal/t/nerf-monk-hellicopter-as-fast-as-possible/5877
- DiabloFans — zMonk guide: https://www.diablofans.com/builds/98593-support-monk-an-in-depth-guide-to-zmonk
- DiabloFans — zBarb guide: https://www.diablofans.com/builds/100281-an-in-depth-guide-to-zbarb-pull-barb-for-meta
- PoE Wiki — Void Sphere: https://www.poewiki.net/wiki/Void_Sphere
- PoE Forum — Void Sphere feedback: https://www.pathofexile.com/forum/view-thread/2940449
- PoE Forum — vacuum loot: https://pathofexile.com/forum/view-thread/3003315
- Lost Ark Academy — Destroyer: https://www.playlostark.com/en-us/news/articles/lost-ark-academy-destroyer-class
- Maxroll — Lost Ark Gravity Training Destroyer: https://maxroll.gg/lost-ark/build-guides/gravity-training-destroyer-raid-build-guide
- Hades Wiki — Boons: https://hades.fandom.com/wiki/Boons
- GrimTools — Vortex of Souls: https://www.grimtools.com/db/items/2506
