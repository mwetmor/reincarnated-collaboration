# ARPG Fight-Mechanics Database — Comparator Research (2026-05-18)

**Status:** Structured research artifact. Companion to `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` and `agentic_orchestration/gandalf/research/arpg-gap-analysis-2026-05-18.md`. Load-bearing input for Pattern-B commercial-direction dialogue (2026-05-19 morning).

**Authored by:** gandalf (synthesis), commissioning 4 parallel Legolas Mode-A research agents:
- Wolcen: Lords of Mayhem — deep-dive (Director rec #1)
- Dragon's Dogma 2 — deep-dive (Director rec #2)
- Grim Dawn — deep-dive (Director rec #3)
- Genre-baseline: Diablo 2/3/4, Path of Exile, Last Epoch — survey

**Authored:** 2026-05-18 evening. Populated iteratively as background research agents complete.

**Scope note:** "ARPG" here covers both *looter-ARPG* (Diablo lineage — Wolcen, Grim Dawn, PoE, Last Epoch, D2/D3/D4) and one *action-RPG* (Dragon's Dogma 2). The sub-genre boundary is load-bearing — see DD2 entry's mandatory sub-genre flag.

---

## § 0 — Schema (12 axes per game)

Every game profile addresses these 12 axes:

| # | Axis | Question |
|---|---|---|
| 1 | Dimensional model | 2D top-down / 2.5D isometric / 3D third-person; camera; engine |
| 2 | Collision system | entity↔entity (hard/soft/none); entity↔environment; pack density behavior |
| 3 | Per-skill range as design lever | Published per-skill? Modifiable via build? Out-ranging possible? |
| 4 | Disengagement mechanics | Aggro radius; leash + reset; outrun; LOS break; movement skills |
| 5 | Pack handling | Typical pack size; tier mix; boss-with-adds frequency |
| 6 | AI patterns | Framework (BT/FSM/utility); melee approach; ranged kite; boss phases; telegraph windows |
| 7 | AOE coverage | Footprint spatial? Falloff? Multi-target caps? |
| 8 | Balance approach | Per-tier balance? Heavy playtest vs. sim? Dev philosophy posts |
| 9 | Movement skills centrality | Essential / strong / optional / minimal |
| 10 | Notable anti-patterns + fixes | What got wrong; what got fixed |
| 11 | Key design lessons | 1–3 takeaways for a Reincarnated mod-into-this-game author |
| 12 | Modding scene | Mod ecosystem; content-injection ceiling; total-conversion viability |

---

## § 1 — Cross-cutting findings (genre baseline)

*This section will be populated when the genre-baseline research returns. Pre-summary based on existing gandalf knowledge + DD2 research returned:*

**Universal-or-near-universal across all comparators:**
- **Spatial substrate.** Every comparator operates in real spatial coordinates (2D isometric or 3D). None reduces combat to 1D scalar distance. Reincarnated's engine is the unicum here.
- **Entity↔entity collision.** Every comparator enforces some form of body-occupancy. Hard collision (DD2, Grim Dawn) or soft separation forces (D2, PoE, D3, D4). Reincarnated's demo violates the universal.
- **Per-skill range, published.** Every comparator publishes per-skill range in tooltips (meters, yards, or radius). Range is moddable via gear/passives in every looter-ARPG (PoE Increased AoE, Grim Dawn +Radius, D4 Ranged Damage > 11yd). Reincarnated does not carry per-skill range data.
- **Disengagement is a real option.** Every comparator has aggro-radius + leash + outrun-viable. Reincarnated has none (fight-to-0-HP only).
- **Per-tier balance is the contract.** Every comparator tunes boss-tier separately from trash. Reincarnated uses aggregate-mean across 12 tiers.

**Variable across comparators:**
- AI framework granularity (D3 uses BT-heavy; D2 simpler FSM; PoE mid-complexity)
- AOE footprint fidelity (Wolcen/PoE highly spatial; D3 more abstracted)
- Movement-skill centrality (D3 high, D2 medium, PoE high, Grim Dawn medium, DD2 vocation-dependent)
- Modding ceiling (Grim Dawn high, PoE moderate, D3/D4 minimal, DD2 limited, Wolcen low-moderate)

*Full cross-cutting analysis after genre-baseline research returns.*

---

## § 2 — Wolcen: Lords of Mayhem (Wolcen Studio, 2020)

**Director recommendation: #1 mod-first target. Research returned 2026-05-18 evening.**

### CRITICAL VIABILITY FLAG — READ FIRST

**The Director's #1 mod-first recommendation is NOT supported by technical or community evidence.** Wolcen has: no Steam Workshop (developer-confirmed not planned), a shallow XML-only modding surface that cannot reach progression systems (Gate of Fates) or AI behaviors (compiled Kythera), a functionally dormant modding community (most popular mods uploaded 2020–2021, none since), and an actively contracting playerbase. Last patch was July 2023; multiplayer shut down September 2024; ~24 average concurrent players as of May 2026 (all-time peak was 127,542 at launch). Development is in single-player maintenance-only mode. The genre-adjacency is real (isometric ARPG, procedural dungeons, stat-heavy character building), but the platform is not a viable modding target.

This finding **inverts the Director's mod-first target ranking on technical grounds**: Grim Dawn (mature ecosystem) > Dragon's Dogma 2 (active community, narrow ceiling) > Wolcen (dormant). The Director's ranking may have been based on genre-fit + commercial-visibility intuition rather than modding-platform diligence — that's a fair call for him to make; we're just naming what the technical evidence shows.

### Axis profile

| Axis | Finding |
|---|---|
| 1. Dimensional model | Full 3D rendered in fixed isometric perspective. CryEngine 5 (rare for ARPGs; most use Unity/Unreal/proprietary). Quixel Megascans textures. Kythera AI from Moon Collider for navigation + behavior trees + spatial queries. Fixed camera angle, no rotation. |
| 2. Collision system | **Hard entity↔entity collision** — a defining and contested feature. Enemies physically block player movement. Compounded by animation-commit lock — multiple deaths attributed to "stuck in cast/attack animation, can't move out." Mitigation: one Gate of Fates passive grants ignore-collision; Leap can be modded to pass over enemies; Aether Jump teleports through. Dense packs (esp. Lambach add-spawn at <10% HP) can pin the player. Mob separation via Kythera boid-style contextual steering. Hard environment collision via runtime navmesh. |
| 3. Per-skill range | **Range IS a real internal metric (meters)** but vanilla tooltips do not surface it consistently. "Better Skill Descriptions" mod corrects this — confirming underlying data exists. Passive nodes reference explicit distances: "Safe From Afar" gives +175% Projectile Damage scaling with Distance at 15m; "Meditative Focus" +25% Damage at ≥6m; "Bestial Frenzy" +4% per enemy within 4m. Out-ranging is a viable intentional Ranger build strategy. Skill modifier system (up to 16 mods per skill, unlocked via use) allows range/AoE adjustment. Weapon gates enforce melee/ranged role separation at equipment layer. |
| 4. Disengagement | **Presence stat** functions as aggro-radius proxy — baseline 100%, lower = stealthier; 0% = invisible. Functions as the game's aggro slider. No explicit numerical aggro radius published. Some leash behavior exists (e.g., NightStalkers stopped indefinite-chasing in a patch; teleport-to-attack instead). General leash distance Unknown. No mounts. Movement speed stackable. Dodge roll is global (Spacebar, stamina-gated, Dark-Souls-style I-frames). Aether Jump + Evasion provide skill-based repositioning. |
| 5. Pack handling | Designed for 50+ unit armies (per Kythera documentation); typical campaign packs 5–20 with set-piece battles up to 50+. Three tiers: Regular / Elite (with Break Bar + affixes) / Boss (multi-phase, dedicated mechanics). Post-launch Bloodtrail added area modifiers (up to 30 per expedition) + active boss modifiers (auto-cast projectile volleys, hazard zones). Boss-with-adds is recurring pattern (Lambach escalating add waves as HP drops). |
| 6. AI patterns | Kythera behavior trees (web-authored, not pure scripted). Boid-style contextual steering for groups. Formation system maintains relative positions during approach. Bloodtrail added "Hunt" pathfinding (diverse non-obvious routes — anti-formulaic kiting). **Spatial Query System** enables bosses to detect player-placed DoT zones and dodge them. Boss phase transitions are HP-threshold (not timed). Telegraph via visual arena mechanics + animation tells; launch-era complaint was telegraphs poorly readable. Quantified telegraph windows not published. |
| 7. AOE coverage | **Geometrically real** — 3D world-space radius/cone/cylinder volumes test actual enemy positions. Radii defined in meters, modifiable via skill mod system. Some skill mods trade radius (Deathgazer Railgun: longer charge → more damage, smaller AoE). Damage falloff and target caps Unknown — not surfaced in public sources. |
| 8. Balance approach | **Reactive playtesting, not sim-heavy.** Launch shipped with Bane of Tyranny massively overpowered (nerfed in first hotfix). 5-month content freeze (1.0.4–1.0.16) for bug + balance fixes; devs described "testing to see if things work." Trash vs. boss tuned separately (specific boss HP/range adjustments in patches). Bloodtrail (Feb 2021) was the systemic rebalance — attribute scaling rework, multiplicative item scaling, 80+ damage-type modifiers added. No GDC talks, no published design philosophy doc, no sim infrastructure documented. |
| 9. Movement skills | **Universal dodge roll: essential.** Spacebar, all builds, 4-8 stamina nodes, I-frames. Aether Jump (teleport, collision-bypass), Evasion (dash-backstep, Rogue), Leap (modifiable to pass enemies), Slayer's Flurry (conditional dash-to-target). Centrality: Rogue = movement core; Mage = Aether Jump life-saver in boss-add scenarios; Warrior = Leap. No mounts. |
| 10. Anti-patterns + fixes | **Launch (Feb 2020): "worst ARPG launch in history."** 127k peak concurrent → servers down/corrupted within hours. Online-only requirement amplified damage. Fixed: offline mode added (significant reversal); Bane of Tyranny nerfed; 5-month content freeze for fixes; monster movement speed reduced for telegraph readability; Bloodtrail rebalance; Break Bar system added (structured CC rhythm); loot filter. **Unfixed at end-of-development:** enemy targeting geometry, ~25% kill-count-to-boss-spawn missions broken, animation lock persisted, HP scaling at L75 (tens of millions HP, never solved — community Better Expeditions mod patched), netcode unfairness in co-op, character pathing stuck on geometry. **Development ended July 2023; multiplayer shut down September 2024; maintenance-only mode.** |
| 11. Lessons for Reincarnated mod-author | **(1) Hard unit collision is non-negotiable in Wolcen's substrate** — every skill assumes it. Reincarnated's 1D-scalar content would trap players in dense packs without collision-bypass design. **(2) Gate of Fates is the design chokepoint** — XML modding cannot add new tree segments without engine-side changes. Reincarnated's progression mechanics (traits, spirit-swap) have no place to attach. **(3) Combat rhythm is stamina-dodge / break-bar / phase-transition** — any new enemy must be legible in that vocabulary. Reincarnated's ±25% variance generation would produce un-contextualized encounters. |
| 12. Modding scene | **No Steam Workshop** (devs explicitly not planning). File-replacement Umbra folder mechanism. CryEngine .PAK archives encrypted (initial barrier — unpacker tool decrypts). XML-based: editable balance (drop rates, stats, skills), UI, cosmetic, light mechanical. **Cannot mod without source access:** Gate of Fates nodes, new skill animations, new enemy models, new dungeon layouts, new story content, new AI behaviors (compiled Kythera). **Community dormant** — Nexus total <60 mods, most uploaded 2020–2021, none significant since. ~24 average concurrent players May 2026 vs. 127k all-time peak. |

### Verdict for mod-first viability

**Lowest viability of the three Director-named targets on technical and community grounds.** Genre-adjacency is real but the platform is not a viable modding ladder. If pursued for *commercial visibility* (Wolcen is a name people recognize), the realistic value is brand-association, not technical proof. If technical proof is the goal, **Grim Dawn is dramatically stronger**; even DD2 has more active modding momentum than Wolcen does today.

---

## § 3 — Dragon's Dogma 2 (Capcom, 2024)

**Director recommendation: #2 mod-first target. Research returned 2026-05-18 evening.**

### MANDATORY SUB-GENRE FLAG — READ FIRST

Dragon's Dogma 2 is an **action-RPG**, not a looter-ARPG. This distinction is load-bearing for the mod-first path evaluation. Looter-ARPGs (Wolcen, Grim Dawn, Diablo IV) are defined by procedural/semi-procedural loot treadmills, build diversity driven by randomized affixes, gear as primary progression axis, infinite enemy density, and explicit difficulty tiers. DD2 has **none of these**. It is a handcrafted, narrative-driven, single-playthrough action game with fixed enemy placements, hand-authored gear with fixed stats, no loot treadmill, encounter design scaled toward individual monster spectacle rather than pack throughput. **Reincarnated's content model — substrates, procedural seasonal regens, class-specific skill pools, gear-affix rolls — has no direct equivalent in DD2's architecture.** This is the single largest structural incompatibility for the mod-first path.

### Axis profile

| Axis | Finding |
|---|---|
| 1. Dimensional model | Full 3D, third-person over-shoulder, dynamic camera (pulls back for mounted/climbing). RE Engine (first open-world deployment, ~1yr pre-production tool work). |
| 2. Collision system | **Defining feature.** Hard entity↔entity collision (bodies impede). Climb-the-monster physics system (player physically grabs/climbs Cyclops legs, Drake backs, Griffin wings). Environment is fully destructible — flood positions via dam destruction, topple enemies off cliffs. |
| 3. Per-skill range | **No numeric tooltips.** Range communicated via animation reach, projectile travel, spell radius. Itsuno's explicit design: narrow each vocation's range of actions, buff the remaining. Fighter is melee-only by design; Archer ineffective in melee; Sorcerer immobile during cast. Mystic Spearhand is the explicit exception (effective at all ranges). |
| 4. Disengagement | **DD2 does NOT implement traditional ARPG leash.** Enemies pursue persistently across regional seams (deliberate — Itsuno removed DD1's load-area restrictions for this). Escape is genuinely difficult: stamina-gated running, LOS-break works but chase distance is long. Griffin can intercept oxcarts and force chained encounters. |
| 5. Pack handling | Small packs (3–8 standard enemies). Mixed-type encounters via proximity (Cyclops + ambient goblins, not scripted waves). **Climbable boss-monsters are the centerpiece.** Chimera (3 heads, distinct AI per), Cyclops, Drake, Griffin, etc. |
| 6. AI patterns | **Pawn AI is the headline system** — goal-based (not ML), observes and learns from player. "Knowledge sharing" across online sessions. Monster AI varies sharply by species: goblins flank + use fire on grass, harpies dive-bomb, griffins flee at low HP, drakes have aerial breath. Telegraph design north-star: "balance when the player can judge enemy behaviour and how long it takes to react." |
| 7. AOE coverage | Spatial-real. Maelstrom = persistent tornado, fills corridors; Meteoron = 5-impact area; melee greatsword swings are wide-arc. No documented falloff. Footprint × terrain geometry interactions are intentional. |
| 8. Balance approach | Itsuno: "I didn't make a Nintendo game designed to be liked by everyone." Vocation balance is "is it fun to play together," not "are vocations equal." **Famous failure: no enemy level scaling** — players one-shot standard mobs by level ~20, intended enemy-variant tactics never matter. No NG+. |
| 9. Movement skills | All movement is stamina-gated. Thief = most mobile (Swift Step). Mystic Spearhand = blink strike. Fighter/Warrior = grounded. Sorcerer = rooted during cast. **No standard dodge roll** — community immediately built lock-on + dodge mod (one of earliest, most-downloaded). |
| 10. Anti-patterns + fixes | Launch perf issues (patched); single-save slot (workarounds only); day-one MTX (severe backlash, items obtainable in-game); disabled loose-file loading (mod-community fragmentation); no enemy scaling (unresolved). Combat-system praise: climbing monsters, Pawn AI, vocation depth, environmental combat. |
| 11. Lessons for Reincarnated mod-author | **(1) DD2 modding is content-recombination, not content-injection at system level.** SkillMaker / DD2_VocationKit allow remixing existing skill nodes — not new mechanics. **(2) Sub-genre mismatch is architectural, not cosmetic.** Reincarnated's procedural model has no injection point in DD2's handcrafted-encounter substrate. **(3) DD2's full-3D physics-driven combat strips away Reincarnated's 1D scalar simulation — the generation engine could only serve as a *design-input tool*, not a runtime system.** |
| 12. Modding scene | ~1,100+ Nexus mods. REFramework is foundational (Lua API). Categories: UI/QoL, gameplay tweaks, vocation/skill overhauls (SkillMaker as ceiling), cosmetics, encounter randomization (within authored cells), unofficial patches. **Total-conversion = NOT feasible.** RE Engine exposes no level editor, quest system, world-spawn editor. December 2024 patch broke significant mod portion (recurring RE-Engine-patches fragility pattern). |

### Verdict for mod-first viability

**Weakest of the three Director-named targets.** Sub-genre mismatch + RE Engine modding ceiling means the mod-first path here is closer to "build a recombination mod that uses Reincarnated as a design-input tool" than "ship Reincarnated content as DD2 content." If pursued, the value is **proof that the engine has cross-genre legs** rather than commercial penetration into DD2's player base.

---

## § 4 — Grim Dawn (Crate Entertainment, 2016 + expansions through 2024+)

**Director recommendation: #3 mod-first target. Research returned 2026-05-18 evening.**

### STRONGEST MOD-FIRST CANDIDATE — VIABILITY CONFIRMED

Grim Dawn ranks **first** on technical mod-feasibility grounds among the three Director-named targets, by a wide margin. Crate ships the same tools they use internally (Asset Manager, World Editor, Database Editor, Quest Editor, Conversation Editor, Particle Editor, Lua scripting). Empirical proof of injection-at-scale exists: the **Dawn of Masteries** mod adds 53 playable classes ported from Diablo 1/2/3, Path of Exile, Titan Quest, plus originals; **Grimarillion** compiles Zenith + Grim Quest (TQ) + Diablo 3 port + density modifier + stash expansion. Fangs of Asterkarn (final expansion, expected 2025–2026) keeps the engine in active development. Mature 10+ year modding community anchored on NexusMods + official forum.

**Single hard constraint:** Engine loads only **one mod at a time**. Mod merging requires tool-assisted compilation (Mod Merger, WanezToolsGD, ComboMod). A Reincarnated-into-GD mod must be designed as a single unified package from inception with clean file namespace to remain mergeable.

### Axis profile

| Axis | Finding |
|---|---|
| 1. Dimensional model | **2.5D isometric, fixed-angle three-quarter perspective.** Modified Titan Quest engine (Crate licensed from Iron Lore; Crate principals are TQ alumni). Single-threaded core simulation logic — has real consequences for AI complexity. Click-to-move + optional WASD. v1.2.0.0 (Nov 2023) added universal Evade dash (Spacebar, brief i-frames) as the first non-mastery movement primitive. |
| 2. Collision system | **Hard player-to-entity collision** — mobs physically block player. Crucible DLC most-cited friction case: "enemies rush and surround you like a wall." Workarounds: AOE-to-clear, movement-skill classes, weapon-component dash procs. Classes without built-in movement (Arcanist, Occultist solo) have no native escape from enclosure. **Entity-to-entity (mob-mob) collision:** Unknown definitively — standard ARPG practice is passthrough, GD likely same. Pet pathfinding explicitly optimized in patches (large battles). |
| 3. Per-skill range | **Skills publish Radius (AOE) + Projectile values in tooltips.** Range scales with skill level on some skills. Examples: Blackwater Cocktail (arc projectile → burst → burning ground patch); Stun Jacks (arcing projectiles with per-projectile burst radii); Primal Strike Torrent (chain lightning). **Dual-mastery system forces intentional range trade-offs** — e.g., Demolitionist (ranged/AOE) + Nightblade (melee) gives split profile by design. Range modification via gear is secondary (Cast/Attack Speed affixes; no primary +Range affix). **Transmuters** can alter skill range profiles fundamentally — Crate's stated philosophy: "interesting trade-offs that dramatically alter the way you use the skill." |
| 4. Disengagement | Aggro radius: Unknown numerically; aggressive once engaged. **"Once they start chasing they will never stop unless you run several screens away to reset"** — leash is large by modern ARPG standards. Discourages kite-to-reset as a primary strategy. **Nemesis system** — red-tier ultra-rares spawn based on faction infamy; not session-persistent, but proximity-trigger during faction kill streaks, sudden one-shot potential. Movement skill access is unequal across masteries (only Soldier/Nightblade/Oathkeeper have native; others rely on medal-slot runes); v1.2 universal Evade partially closed the gap. |
| 5. Pack handling | **Color-coded tier system:** White (common) / Yellow (Champion, +abilities, +loot) / Orange (Hero, named, star marker) / Lavender (Unique Boss, scripted) / Red (Nemesis, faction-linked). Expansion content (Forgotten Gods, Ashes of Malmouth) is dense — overlapping hero spawns, tight corridors. Mob composition typically mixes 2–3 types per pack with pseudo-random Hero spawns. **Grimmest mod** multiplies hero rates substantially — proving density is a tunable parameter via mod tools. |
| 6. AI patterns | **"Almost any monster follows the same pattern: move to player until in range, attack."** Direct quote from Crate forum analysis. Ranged enemies advance to range then root in place and fire. Area abilities used without positional intelligence. No flanking, grouping, or coordinated behavior at base AI. **Engine constraint:** "AI eats CPU for breakfast. Engine is single-threaded, smarter AI may be too complicated." This is the architectural ceiling. **Boss AI:** "Barely different from random champion encounters — both AI and skill setup." Loghorrean uses HP-threshold phase gates (summons at 65% HP; +cast/attack speed at 50%). Celestial superbosses (Ravager, Mogdrogen) are stat-checks not AI-checks. No telegraph system — players learn patterns through repetition. v1.2 specifically "limited special attack tracking, reduced charge ability speeds" (targeted one-shot fix). |
| 7. AOE coverage | **Explicit spatial shapes** — radius circles, cones, projectile lines. Skills print Radius in tooltips. Real geometries, not multi-hit flags. **Damage falloff: NOT universal** — most AOE is binary in/out. Multi-target caps: per-skill parameter, not engine cap. Element AOE coverage ranking (community-sourced): Acid/Fire > Elemental > Aether > Chaos/Vitality > Cold > Lightning > Pierce/Bleed > Physical. |
| 8. Balance approach | **Zantai philosophy:** "Items/skills may seem under/overpowered in vacuum but are fine in context of all items/skills." Holistic context-dependent tuning. **Empirical, not simulated** — no sim infrastructure publicly documented; manual playtesting + forum community telemetry + hotfix cycle. 8+ years iteration cadence. Build diversity is load-bearing goal; transmuters serve this. **No automated balance pipeline known.** v1.2.0.0 (Nov 2023) made structural late-life changes: 30–60% loot quantity reduction + quality increase; level scaling to 100 in Normal/Elite (eliminating forced difficulty ladder). |
| 9. Movement skills | **Mastery-native (three only):** Blitz (Soldier, charge — requires target), Shadow Strike (Nightblade, blink-to-target), Vire's Might (Oathkeeper, ground-targeted line dash — the only true escape tool). **Medal-slot movement runes** provide parity for masteries without native movement (consumes gear slot). **v1.2 universal Evade** on Spacebar is the largest movement system change in GD's history — explicit class-disparity fix. In endgame (Shattered Realm, Crucible), movement skill access is significant build factor. Dervish (Nightblade + Oathkeeper) prized for two distinct movement skills. |
| 10. Anti-patterns + fixes | **Damage Reflect (pre-v1.1.0.0)** — "% Damage Reflected" was poorly designed mechanic, bypassed defenses, caused one-shots; fully replaced in v1.1 with specific retaliation damage types. **Retaliation builds** underperformed for years; reframed as "complementary damage" rather than standalone archetype. **One-shot endgame** — nemesis spawns + boss charge speed + Ultimate scaling; v1.2 targeted fix. **Monster stun/freeze removed from standard abilities** in v1.2 — retained on bosses by design. **Pet build volatility** — moved from auto-attack to special-attack based over patches. |
| 11. Lessons for Reincarnated mod-author | **(1) Engine geometry locked** — 2.5D isometric, click-to-move. Reincarnated's 1D scalar would express through GD's spatial engine: range becomes AOE radius selection, leash becomes GD's built-in chase. **(2) New masteries fully injectable, proven at scale.** `skill_classselectiontable.dbr` registers new classes; Asset Manager compiles. Dawn of Masteries (53 ported classes) is the empirical proof. **(3) One-mod-at-a-time constraint requires upfront architecture discipline.** Engine loads single mod module. Mod Merger / WanezToolsGD handle DBR merging with conflict detection; clean file namespace from inception is mandatory. |
| 12. Modding scene | **Tools (shipped by Crate, free to all owners):** Asset Manager (central hub), World Editor (level design, custom maps, weather, dynamic), Quest Editor (branching, conditional), Conversation Editor, Particle Effects Editor, Database Editor (items/skills/monsters/loot tables/affixes), Lua scripting (advanced gameplay automation). **Injectable:** new masteries/classes (proven — 53 in DoM), new skills (full template system), new items (loot tables, affixes, Monster Infrequents), new enemies (DBR records with stat blocks + skills + faction), new zones/maps (World Editor — entire new campaign acts), new factions. **Not engine-supported:** procedural map generation (maps hand-crafted; Enemy and Item Randomizer is a content-layer trick, not engine-level procedural). **Distribution:** No Steam Workshop; NexusMods + official forum + ModDB. Manual install. **Flagship mods:** Grimarillion (#79 — Zenith + Grim Quest + D3 + density), Dawn of Masteries (#82 — 53 classes), Grim Quest (standalone TQ port). Grim Internals deprecated (broken by patch). Modding scene active and healthy in 2026; Fangs of Asterkarn final expansion sustains long-tail. |

### Verdict for mod-first viability

**Highest viability of the three Director-named targets on technical and community grounds, by a wide margin.** The procedural-content constraint (no engine-native procgen) is the one hard incompatibility with Reincarnated's seasonal-regen model — but Reincarnated's content (substrates, classes, gear pools, balance math) can be exported as static GD masteries + items + skills + enemies + zones, with seasonal regeneration happening server-side at Reincarnated's engine and the per-season output compiled into a fresh GD mod. **The mod ladder is: (a) prove one mastery/class injection works → (b) prove a full single-season export works as a coherent mod → (c) prove rolling per-season mod releases is operationally viable. Grim Dawn supports all three.**

---

## § 5 — Genre baseline (Diablo II / III / IV, Path of Exile, Last Epoch)

**Research returned 2026-05-18 evening.**

### § 5.1 — Diablo II + D2R (Blizzard North 2000 / Vicarious Visions 2021)

| Axis | Finding |
|---|---|
| 1. Dimensional model | Fixed 2D isometric (D2R replaced sprites with 3D geometry but preserved underlying grid engine identically). 1 yard ≈ 0.6 subtiles. Integer tile math throughout. Circles appear elliptical due to isometric projection. |
| 2. Collision | Hard collision on walls. Entity↔entity: monsters block narrow corridor passages (explicit community complaint requesting removal in D2R). Monster sizes 1/2/3 in MonStats2.txt interact with melee range. |
| 3. Per-skill range | **Yes — defined since 2000.** `rangeadder + Size` from Weapons.txt. Scale 0 (daggers/wands) to 4 (most polearms/spears). Act 2 Rogue mercenary fixed range 3. Monster melee ranges in MonStats2.txt — Zombies range 2, Blood Lords range 7, bosses (Mephisto/Diablo/Baal) range 4. Ranged: missile range = velocity-px-per-frame × frame-count-until-expiration. **D2 in the year 2000 had richer per-skill range data than Reincarnated has in 2026.** |
| 4. Disengagement | Per-monster `aidist` parameter in monstats.txt, capped ~0x15. Many melee AIs have "100% chance to approach or attack" — no leash in modern sense; chase indefinitely once aggro. Outrun viable (FRW gear stat meaningful). LOS break: yes for ranged AIs (transition to "hide behind obstacle"). |
| 5. Pack handling | Champions (2–4 same-type, 20%) and Unique groups (1 boss + 3–6 minions, 80%). Champion types: Champion (300% life), Berserker (+270% AR/dmg), Fanatic (300% life + 100% speed), Ghostly (80% damage resist), Possessed (600% life). Unique bosses: 1–3 affixes scaled by difficulty (Normal/Nightmare/Hell). 13 affix pool. Super Uniques: fixed-location scripted. |
| 6. AI patterns | FSM with parameter tables. The Phrozen Keep AI Compendium documents 100+ AI scripts, up to 8 named parameters (par1–par8) governing radius thresholds, approach probability, attack delay, escape radius. 4 detection zones (inner = retreat; melee = attack; outer = pursue; disengage). |
| 7. AOE coverage | Radius in yards (1yd = 1.5 subtiles). Spell circles elliptical due to isometric distortion. No falloff within radius — flat damage. Pierce (Amazon passive) for projectiles; Chain (Chain Lightning). |
| 8. Balance approach | Empirical playtest. Synergies system (LoD expansion) was major rebalance. D2R retained original numbers; Project Diablo 2 community mod represents ongoing rebalance. |
| 9. Movement skills | **Optional/Statistical.** No dedicated movement slot. Sorceress Teleport is the outlier exception. FRW gear stat heavily optimized in competitive play. |
| 10. Innovations | Elite pack tier system with random affixes (foundational template). Procedural world + fixed boss anchors. |
| 11. Failures | Melee viability cliff (ranged/caster dominance structural). Teleport exceptionalism (large class quality-of-life gap). |

### § 5.2 — Diablo III (Blizzard 2012, post-RoS 2014)

| Axis | Finding |
|---|---|
| 1. Dimensional model | Fixed isometric on 3D engine. Ragdoll physics, destructible environments. Camera locked overhead, more zoomed-in than D2 precedent (criticism with D4). |
| 2. Collision | **Soft / functionally absent at endgame.** Monster packs can be kited and stacked infinitely tight — explicitly exploited in Greater Rift optimization with Area Damage scaling. Vile Swarm "no collision box." **Deliberate design choice: throughput over spatial integrity.** |
| 3. Per-skill range | Per-skill range implicit in design (no UI number). Skills explicitly melee / short-AOE / mid / long-projectile. Rune system alters projectile behavior (pierce/bouncing/chain). |
| 4. Disengagement | Proximity + LOS triggered. Leash functionally soft/absent at dungeon/rift scale. Fast affix (+40% MS) makes elites un-outrunnable without movement skill. Teleporter affix chases aggressively. |
| 5. Pack handling | Normal → Champion (blue, 2–7 pack, 1 shared affix) → Rare (yellow, 1+minions, up to 3 affixes) → Legendary → Rift Guardian. **23 elite affixes with explicit spatial/behavioral effects** (see Axis 7). |
| 6. AI patterns | FSM with per-archetype scripts. Documented archetypes: Swarmers, Bruisers, Ranged, Casters, Boss-phase. Design principle: "monsters designed such that designers cannot figure out how player defeats them, then give the player the tools." |
| 7. AOE coverage | **AOE footprint matters BIG** because of Area Damage stat (10yd splash chance). Stacking monsters multiplies AD proc rate. Named elite affixes have explicit dimensions: Molten 5yd trail/18yd death; Frozen Pulse 15yd; Arcane Enchanted 25yd rotating beam; Thunderstorm 12yd × 5 strikes; Vortex 50yd pull; Knockback ~30yd; Waller (1 wall blues / 3 yellows). |
| 8. Balance approach | Iterative seasonal + hotfix culture. Inferno launch (2012) failed catastrophically — affixes that removed player agency (Waller, Vortex, Jailer); 5-min enrage timers; AH dependency. RoS 2014 = near-total combat rethink. Post-RoS seasonal balance loop: new Legendary/Set → top-speed meta → next-season rebalance. |
| 9. Movement skills | **Strong / near-mandatory.** Every class has at least one (Wizard Teleport, Barb Leap/Whirlwind, Monk Dashing Strike, DH Vault, WD Spirit Walk, Crusader Steed Charge, Necro Bone Sprint). Required to survive Vortex/Waller/Jailer affixes. |
| 10. Innovations | Spatial elite affixes with geometric AOE (transformed elite encounters into spatial puzzles). Adventure Mode + Greater Rift infinite scaling (template for PoE Atlas, LE Monolith, D4 Pit). |
| 11. Failures | Inferno launch (one of the most disastrous post-launch states). Soft-collision stacking as dominant endgame meta (cognitively boring, decouples positioning from meaning). |

### § 5.3 — Diablo IV (Blizzard 2023 + Vessel of Hatred 2024)

| Axis | Finding |
|---|---|
| 1. Dimensional model | True 3D engine, fixed isometric-style camera with slight dynamic zoom. Camera criticized at launch as more zoomed-in than D2/D3. Genuine 3D vectors → slopes, elevation, true 3D pathfinding. Euclidean distances, not tile-quantized. |
| 2. Collision | **Hard entity collision** — stronger than D3, softer than PoE2. Monsters block narrow passages. Season 5 patch explicitly: "Monster packs will group up less, making them harder to take out in one fell swoop." |
| 3. Per-skill range | Per skill and per class. Skill tag system (Melee, Ranged, AOE, Projectile, Channeled) for Aspect/Charm interactions. Range modifiable via Aspects (legendary affixes) and Paragon nodes. |
| 4. Disengagement | **Leash exists and is actively complained about.** Forum thread: monsters "run like 50 feet and then remember they left the stove on." Player reports: 7–8 rooms in some areas, ~10 feet in others. **Inconsistency across content types — breaks player trust in world rules.** PvP zone bosses shorter leash. Season 5: AI made more "dynamic." |
| 5. Pack handling | Normal → Elite (yellow, affixed) → Boss. Open-world bosses (Ashava, Wandering Death, Grigoire). Endgame pinnacle bosses (Lilith, Duriel, Andariel) + Tormented versions. Infernal Hordes (Season 5/VoH): wave-based arena, 5–10 waves scaling by tier. **Boss stagger system: CC-filling yellow bar staggers boss (full stop, Vulnerable, all CC applied) — Ashava loses arm blade on first stagger reducing sweep AOE.** |
| 6. AI patterns | Not publicly detailed. Observable: melee charge, ranged maintain distance, boss scripted phase transitions. Season 5 changed AI to be more dynamic + scale attack speed with difficulty tier (in addition to movement speed). Stagger-phase = scripted helpless state. |
| 7. AOE coverage | Footprint matters. Explicit ground-targeted areas (Blizzard, Bone Prison, Landslide columns). Evade has spatial i-frame + reposition. Stagger triggers spatial changes (Ashava arm geometry shrinks). VoH Enchantments modify skill behavior spatially (Tempest Roar → Tornado on Storm Strike). |
| 8. Balance approach | Seasonal iteration + PTR testing. Layered power systems each requiring independent balance (Aspects, Paragon, Charms, Talismans). Near-total endgame redesign post-launch (Helltides → NM Dungeons → Pit → Infernal Hordes → Tormented Bosses). PCGamer 2026: "D4 finally feels finished." |
| 9. Movement skills | **Mandatory for endgame.** Evade universal (cooldown'd). Class-specific: Sorc Teleport (de facto mandatory). **Dev acknowledged in patch 2.5: "This option has been treated as mandatory for too long."** Single clearest official genre acknowledgment of movement-skill-mandatoriness tension. |
| 10. Innovations | Boss stagger with permanent fight-state changes (Ashava arm = persistent mechanical memory within fight). True 3D open-world ARPG (removed corridor/dungeon-only model). |
| 11. Failures | Launch endgame vacuum (sparse density, broken objectives, weak seasonal loop — required 18mo dev to be complete). Leash inconsistency (varies wildly by zone/tier/content). |

### § 5.4 — Path of Exile 1 (GGG, 2013–ongoing)

| Axis | Finding |
|---|---|
| 1. Dimensional model | Fixed isometric on 3D engine, 2D gameplay conventions. Procedural tilesets. Functionally 2D combat plane. |
| 2. Collision | **Hard entity collision documented design choice.** PoE2 (Early Access 2024) strengthened it — body blocking became significant feedback issue. PoE1 endgame fast pace made it less frequently felt. Monster size variations affect collision radii. |
| 3. Per-skill range | **Explicit and modifiable.** Melee: `weapon melee range + character hitbox (2)`. Two-handers longer reach; daggers shortest. Ranged: projectile range in game units. **Pierce > Fork > Chain > Return ordering — formal projectile propagation hierarchy.** AOE: cast distance + effect radius. Increased AoE: +100% → radius × √2. Radius-specific modifiers add before AOE% (more efficient per-unit). |
| 4. Disengagement | Leash soft/none for map content. Some types lose aggro quickly. 4 detection zones (inner retreat / blue ranged-attack / orange pursue / red disengage). Melee "suicide charges" within LOS. PoE1 endgame meta of "kill before they reach you" renders leash largely irrelevant. |
| 5. Pack handling | Normal (white) → Magic (blue, 1–2 affixes) → Rare (yellow, up to 4 affixes) → Unique (named, fixed abilities). Map modifiers affect pack sizes + spawn rates. No "champion" tier (LE addition). Endgame league mechanics add density layers (Delirium mist spawns waves). |
| 6. AI patterns | Not publicly detailed by GGG. Observable: melee linear charge, ranged maintain distance, casters stand+cast, Unique scripted multi-phase. **Dominant design philosophy observation: "kill before detection" is intended endgame meta — AI sophistication less important because optimized players never let monsters act.** |
| 7. AOE coverage | **Spatial positioning extremely load-bearing.** Skill geometry: circles, cones, lines, ground-targeted (mines/totems/traps). Pierce/Fork/Chain create distinct spatial AOE profiles per build — meaningful incentive to position pack members. Totem/Mine/Trap builds make spatial positioning of tools the primary skill expression. |
| 8. Balance approach | **Most public balance philosophy in the genre.** Chris Wilson GDC 2019 ("Designing PoE to be Played Forever"): structured league cadence, overlapping randomness axes, deep systems for long-term engagement. Development Manifestos on official forum. Delirium manifesto (2020) self-identified reward-to-depth scaling error and published. Power creep acknowledged; 3.15 nerf patch widely regarded as overreach. |
| 9. Movement skills | **Essential / de facto mandatory.** Dash "most desired for mapping." Flame Dash, Whirling Blades, Leap Slam, Shield Charge, Smoke Mine widely used. Cyclone simultaneously attack + movement (removes opportunity cost). Skipping movement skill in endgame is a significant tradeoff most players do not make voluntarily. |
| 10. Innovations | 1,300+ node passive tree + skill gem system decoupled (skills socket into any class's gear). Hundreds of thousands of viable distinct builds. Pierce/Fork/Chain as explicit build modifiers — unique PoE spatial design language. |
| 11. Failures | Trade dependency as ceiling (SSF cannot reach competitive endgame). Accumulated power creep requiring PoE2 as reset (combat dissolved into visual noise). |

### § 5.5 — Last Epoch (Eleventh Hour Games, 1.0 February 2024)

| Axis | Finding |
|---|---|
| 1. Dimensional model | Fixed isometric on 3D engine. Same category as D3/D4. Monolith of Fate endgame uses node-graph map system (each node a combat arena), not contiguous open world. |
| 2. Collision | **Hard entity collision (PoE1-equivalent, not PoE2-level).** EHG tunes aggro leash and minion target range explicitly: patch reduced follow distance 13% and minion target distance 8%. **Aggro radius and leash are tuned as explicit numerical parameters in patch notes.** |
| 3. Per-skill range | Per-skill, implicit in design (no UI number). 5 classes × 3 masteries × up to 20 skill tree points deep. Heartseeker "always strikes its chosen target" — explicit performance-vs-traditional-projectile tradeoff publicly discussed. Build-modifiable via mastery passives/gear. |
| 4. Disengagement | **Leash explicitly tuned per patch.** Before server-hosted architecture there was no leash (players dragged entire maps). Added with server hosting. "Enemies will generally aggro from further away than before but are less likely to aggro from below the edge of the screen" — explicit aggro-to-visible-area calibration. |
| 5. Pack handling | Normal → Magic (1 affix) → Rare (1 prefix + 1 suffix) → **Champion (LE-unique tier)** → Boss. Champions sit between Rare and Boss, exclusive additional modifier, guaranteed drop with Sealed affix from 14-affix pool. Season 2: Champions become new tier with 20 types × 3 random mods each (including 1 skill-granting). |
| 6. AI patterns | Not publicly detailed by EHG. 13% leash reduction patch implies FSM-style parameter tuning. Shade of Orobyss has "pool of skills to draw from" rather than fixed list — weighted random or lightweight utility — makes encounters feel different. |
| 7. AOE coverage | Spatial positioning significant. Ground-targeted AOE (Glacier, Maelstrom, Warpath, Flame Rush). Pierce/chain/fork via skill tree nodes. Heartseeker = explicit performance trade. |
| 8. Balance approach | **Math-first internal, then playtest.** Dev blog: "After lots of math, formulas, and testing, we settled on Recurve Chance multiplied by 0.8 each time it recurves" — explicit formula-based exponential-scaling prevention. **Skill tree philosophy: "commonly desirable nodes accessible; niche unusual nodes harder to reach; individual nodes shouldn't feel mandatory" — direct response to PoE1 mandatory-gatekeeper-node problem.** |
| 9. Movement skills | **Strong / structurally integrated.** Each class has dedicated traversal: Primalist Fury Leap, Acolyte Transplant (health cost), Mage Teleport (mana cost), Sentinel Lunge, Rogue Shift. **Same function thematically distinct: Transplant vs Teleport identical mechanically but resource-themed to class.** Practically always in endgame builds. |
| 10. Innovations | **Deterministic crafting system (The Forge)** — player-directed crafting with Runes/Glyphs/Forging Potential, not pure random reroll. Most cited LE genre contribution. **Champion tier as loot-delivery + combat mechanism** — bridges PoE rare-as-challenge and D3 elite-as-density. |
| 11. Failures | 1.0 launch server disaster (150k players in 20 min overwhelmed servers, prolonged playability crisis). Boss AI readability issues on some Monolith timeline bosses (over-reliance on dramatic entrance animations; inconsistent telegraph legibility on Shade of Orobyss random pool). |

### § 5.6 — Cross-comparator synthesis (refined from § 1)

**The 2024 modern genre contract — present in ALL five baseline games:**

| Property | Genre Default | All Five Games? | Reincarnated |
|---|---|---|---|
| Isometric / overhead fixed camera | Fixed overhead, free movement | **Yes** | Demo compatible |
| **Per-skill range, explicitly modeled** | Every skill has distinct range; melee 5–15 units, ranged long; often buildable | **Yes (D2 since year 2000)** | **NO** |
| Entity collision (at least partial) | Monsters have collision volume; packs don't freely stack | **Yes (D3 softest, PoE2 hardest)** | **NO** |
| Enemy rarity tiers with behavioral modifiers | Min 3 tiers + affixes that alter behavior, not just stats | **Yes** | **NO (scalar HP/dmg only)** |
| Aggro radius — activation at distance | Monsters activate when player enters radius; dormant outside | **Yes** | **NO** |
| Leash / reset — disengagement limit | Maximum pursuit distance; reset toward spawn when exceeded | **Yes (D2 weakest, D4/LE explicit numeric)** | **NO** |
| Dedicated movement skill per class | Every class has at least one repositioning skill with cooldown | **Yes (D2 partial, D3/D4/PoE/LE explicit)** | **NO** |
| AOE with meaningful spatial footprint | Defined radius matters for targeting | **Yes** | **NO (1D affects nearby targets by scalar dist)** |
| Boss with distinct phases / adds | Named bosses have phase transitions and/or add spawning | **Yes** | Partial in engine; not in demo |
| Public balance documentation | Patch notes / manifestos / design blogs | **Yes (GGG most extensive, EHG moderate, Blizzard patch notes)** | Internal only |

**Additional near-universal design norms:**
- Pierce/Chain/Fork or equivalent projectile propagation (all five have at least one). Reincarnated: none.
- Elite/affix system that changes BEHAVIOR not just stats (D2: 13 / D3: 23 / D4: many / PoE: magic+rare mods / LE: Champion sealed). Reincarnated: none.
- Monster aggression scaling with difficulty tier (D4 Season 5 explicit: "Monsters now scale attack speed as difficulty goes up in addition to movement speed"). Reincarnated: scalar HP/damage only.
- Movement skill as cooldown resource (post-2012 universal in all of D3/D4/PoE1/LE; D2 the exception with Teleport-Sorceress outlier). Reincarnated: none.

**Gap severity ranking (from research synthesis):**

1. **Per-skill range** — oldest and most fundamental. D2 had this in year 2000. Absence is "pre-genre-standard."
2. **Entity collision** — absent in D3 but present everywhere else; absence makes spatial play feel fake.
3. **Aggro radius + leash** — present as explicit parameters in all five; without them, world has no "at rest" state.
4. **Dedicated movement skill** — post-2012 universal; absence is single clearest signal that combat is pre-genre-standard.
5. **Enemy tier + behavioral modifier system** — without it, all fights are the same fight at different HP/damage values. No strategic read, no adaptive response.

---

---

## § 6 — Reincarnated current-state column (for direct comparison)

For completeness, Reincarnated's own profile across the 12 axes:

| Axis | Reincarnated current state |
|---|---|
| 1. Dimensional model | **Engine sim: 1D scalar distance only.** Demo: 2D pixel-space. Engine: Python; Demo: Pixi.js (TypeScript). No shared spatial substrate. |
| 2. Collision system | **Engine: N/A (no space).** Demo: NONE (explicitly deferred at `world/movement.ts:197-199`; "Repulsion forces can be added here if overlap looks bad at future playtests — not added speculatively"). |
| 3. Per-skill range | **NONE on either surface.** Engine has only `at_melee_range` binary gate at CLOSE_THRESHOLD (1.5m). Catalogue carries no per-skill range data. Demo applies hardcoded range constants `{ close: 90, medium: 420, long: 660 }`. |
| 4. Disengagement | **NONE.** No aggro radius, no leash, no outrun, no LOS break. Fight runs to 0 HP. FAR-band auto-converges back to MID (monster always advances). |
| 5. Pack handling | **PackProxy** — N×HP single entity, AOE × N damage. No spatial separation; no death-attrition momentum; no focus-fire dynamics. |
| 6. AI patterns | Three decoupled implementations (engine sim Python, demo runtime TS, balance-loop implicit). Engine sim: priority-rotation by archetype. Demo: hardcoded kite-if-long. No shared source of truth. |
| 7. AOE coverage | Engine: AOE = damage × pack_size multiplier (not spatial). Demo: no spatial AOE collision check (AOE just hits the stack). |
| 8. Balance approach | **Aggregate mean WR** across 12-fight gauntlet. No per-tier WR targets. Boss/miniboss failure invisible to metric. |
| 9. Movement skills | Limited; no class-wide dodge/dash convention; movement_speed is a per-mob stat but not a build axis on the player side. |
| 10. Notable anti-patterns | Engine + demo divergence accumulating since B10.2 (PackProxy ship) and Gate 3b (3-band scalar). Diagnosed 2026-05-18. |
| 11. Lessons learned | The simplifications were correct at the time; the gap is what happens when good simplifications accumulate without periodic architecture review. |
| 12. Modding | N/A — Reincarnated is not a mod host. |

---

## § 7 — Updates log

- **2026-05-18 evening (initial)** — File created. § 0 schema + § 6 Reincarnated profile + § 3 DD2 entry populated.
- **2026-05-18 evening (Wolcen + GD returns)** — § 2 Wolcen + § 4 Grim Dawn populated. Critical viability inversion finding documented (Director's #1 Wolcen is technical #3; Grim Dawn is technical #1).
- **2026-05-18 evening (genre-baseline return)** — § 5 populated with all five baseline games (D2, D3, D4, PoE1, LE). Cross-comparator synthesis (§ 5.6) refined with explicit gap-severity ranking.
- **2026-05-18 evening (FINAL)** — Database complete across 8 comparators on 12 axes. Genre contract codified. Ready for Pattern-B input.

---

*Database closed 2026-05-18 evening. Final cross-cutting synthesis confirms: Reincarnated currently violates 7 of 7 genre universals and 4 of 4 near-universal design norms. The fight-integrity gap diagnosis (canonical doc) is fully corroborated against the modern ARPG contract. Pattern-B has the data it needs.*
