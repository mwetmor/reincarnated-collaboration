# 32 — Progression System Design Discussion

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Captured:** 2026-05-11
**Status:** Design discussion document — covers character progression layer that the engine queue (file 28) has gaps around. **B9 series built the endgame math (level=50 baseline, 120 skill points, trait floors at 1/12/25/38, max rank 4) but NOT the surrounding progression scaffold** (XP mechanism, stat allocation, enemy level scaling, multi-band sim, gear tier curves, trait acquisition UX, death penalty, per-act content scaling).

This doc captures: what we've thought through, what we need to think through, what's already decided. **Each section has three buckets** — Decided ✅ / Thought-through ⚠️ / Open 🔴 — plus reference notes from genre research.

## Cross-references

- `28-engine-arpg-rebalance-design.md` — engine queue; B9 series covers endgame math; this doc covers what B9 doesn't
- `29-design-overview.md` — strategic anchor; "Tier 1-2 progression systems (XP, levels, skills, gear)" stated in scope but not specified
- `16-project-roadmap.md` — Stage A7 (this design's implementation) lands here; design fully resolved 2026-05-12
- `17-gear-and-spirit-guide-design.md` — gear progression endgame math; § "Loot economy validation — journey vs outcome" surfaces the "scenario tier" extension
- `33-progression-skeleton.md` — companion empty skeleton; this doc's discussion lands there as decisions firm up
- Memory `project_progression_concept.md` — Priority 14 sketch (predecessor framing; this doc supersedes)
- Engine `docs/foundation.md` — 50-tier power scale aligned with character levels (immutable substrate)

---

## TL;DR — Status as of 2026-05-11 (ALL 12 SECTIONS RESOLVED)

| Layer | Locked decisions |
|---|---|
| **Progression philosophy (§1)** | XP-primary hybrid. 100 SP from level + 20 SP from Trial body-swap milestones. Four XP sources (kills + quest XP + discovery + Trial body-swap). Body-swap-offered death with seasonal-death consequences. Anti-patterns rejected: paragon grind, mandatory respec gold, level-locked gates, full player-scaling, hardcore at launch, mid-game balance debt. |
| **Character level curve (§2)** | L50 hard cap. Smooth polynomial XP curve (level^2.0-2.5). Free pre-cap leveling. Body-swap inherits player level. |
| **Stat allocation (§3)** | Auto-allocate per class identity (D3-style). No player allocation; no reset needed. Existing soft caps preserved (DODGE 0.60, CRIT 0.75). |
| **Ability progression (§4)** | Trait auto-unlock at floor + auto-rank with level. All skills visible from L1, gated by tier-unlock. Trait stacking additive across sources. **Hierarchical Skill Tree with Dimensional Threading**: 4 tiers × 2-4 chains (variance allowed); rank thresholds 3/5/8; cross-chain unlock asymmetry per element (single-element strict, multi-element flexible); smooth rank cap min(15, floor(level/3.33)); tier-specific scaling coefficients. |
| **Gear progression (§5)** | Monster-level-tied drop rates per band. Polynomial power-score curve. ilvl as separate axis. Drops/slot: 10/25/50 per band. Constant 70/30 smart-loot. Smuggling principles locked. 10 gear slots final (+boots/gloves/belt). **Seasonal Sets** ⭐ (Reincarnated-distinctive; class-specific endgame sets). Auto-pickup with rarity filter (mobile-first). Pet system parked as design intent. |
| **Enemy/monster scaling (§6)** | D2/PoE-style FIXED-PER-BAND (no D3-style player-scaling). Trial bosses level-bound at season-generation. Doppelganger level = max(player_level, trial_band_level) + handicap. |
| **Alignment validation (§7)** | B14 multi-band sim covers (9 runs per class: 6 kit+variance + 3 doppelganger mirrors). Class identity is trajectory across phases. Spirit Guide cross-phase coaching at act-transitions + reset moments + proactive reset recommendation when >30% divergence. |
| **Sim architecture (§8)** | Option β — 3-band act-aligned discrete convergence at L17/L33/L50. Per-band optimal distribution. Per-band monster pools (b interpretation). Per-band generated gauntlets. Recompose-first failure handling. 9 convergence runs per class. ~30-45 min/season cost. Zero LLM impact from sim itself; +$1-2/season from per-band monster pools. |
| **Death penalty (§9)** | 5-10% XP loss on refuse-swap. NO durability. NO gold drop. Trial encounter resets on death. Pool depletion: pool=1 single-choice; pool=0 only refuse-respawn. |
| **Per-act content (§10)** | 3 acts (file 29 lock supersedes "4, 5, or 6"). Level bands: A1=1-17, A2=18-33, A3=34-50. 1 Trial body-swap per act. |
| **Quest as XP source (§11)** | Trial body-swap = sole milestone-SP source. 4/7/9 SP per act = 20 total. Resistance +10% per Trial (cap +75% with gear). Doppelganger path = 1/4 immediate + end-game quest reclaim. XP grant = % of XP-to-next-level (50%/75%/100% per act). 1 form ascends per season. |
| **Movement + mobility (§12 + §12.5)** | B12: not stat-driven; boots primary; +25% gear cap; engine emits movement_speed. B13: 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance); telegraphs + i-frames; archetype-emergence observability. Last Epoch per-class mobility model (NOT D4 universal Evade). |
| **Earth meta-layer** | Reincarnated Phase 0 = seasonal journey portion of larger eventual game. Earth Self = persistent identity. Form library = gacha-style accumulation of ascended spirits. Eventual Earth events (PVP/PVE rift). Full spec in `../collaboration-handoff/34-earth-meta-layer.md` (to be drafted; memory captured). |

---

## Section 1 — Progression philosophy (architectural decision)

**The single most important decision in this doc.** Everything downstream is shaped by what we choose here.

### ✅ Decided
- **Tier 1-2 progression in scope** (file 29 § "Scope: what Reincarnated is NOT"): XP, levels, skills, gear, basic crafting if any. Deep systems (paragon, complex economies, guild systems) out of scope.
- **Meta-progression spine: body-swap + gear smuggling + accumulated knowledge** (file 29). Three components of one mechanism.
- **Solo gameplay** (no multiplayer scaling concerns).
- **Roguelike + Hades influence** (file 29: "death is progress" framing applied to body-swap).
- **Per-game arc has a defined end** (final act boss). Seasons rotate; each playthrough has shape.

### ⚠️ Thought through (in fragments)
- The 100-points-from-level + 20-from-quests/bosses split (B9b) implies a hybrid: levels grant some progression, milestones grant some. This is a partial commitment to a hybrid model without explicit naming.
- Spirit Guide marginal-value math extends from gear (Phase 5.5f) to skill points (B9c). Implies progression isn't purely free choice; the engine has an opinion about the meta build.

### 🔴 Open → ✅ RESOLVED 2026-05-11

1. **XP-driven, milestone-driven, or hybrid?** → **RESOLVED: XP-primary hybrid.** B9b's 100-from-levels + 20-from-quests/bosses already structurally committed; matches genre median (D2/D4/PoE all hybrid).

2. **If XP-driven: what gives XP?** → **RESOLVED: four sources.**
   - Monster kills (genre-universal)
   - Quest completion XP (D2-style flat XP on top of any skill-point reward)
   - Discovery / exploration XP (D4 Renown-adjacent)
   - **Trial body-swap completion XP** (Reincarnated-distinctive — defeating Trial boss + electing swap grants meaningful XP)

3. **If milestone-driven: how many milestones per act?** → **PARTIALLY RESOLVED (full detail in Section 11):** Trial body-swap is the primary milestone source. Each Trial body-swap grants **XP + global resistances + skill point(s)** as a permanent character buff bundle:
   - Early acts: 1 skill point per Trial body-swap
   - Later acts: more than one (specific scaling deferred to Section 11)
   - Trial body-swap is "mini ascension" — strictly positive rewards
   - Trial body-swap reward bundle is similar to D2's quest reward pattern (Den of Evil +1 SP; Anya's Scroll of Resistance +10% global res; Lam Esen +5 stat) but consolidated and on the body-swap mechanic.

4. **Death penalty philosophy** → **RESOLVED: body-swap-offered with seasonal-death consequences.** This is a Reincarnated-distinctive design (no genre precedent):
   - Death pauses → player offered body-swap to a previously-defeated boss form
   - **Refuse swap:** normal respawn + small XP loss (genre-standard)
   - **Accept swap:** the dead class is **permanently lost for the current season** (cannot be played again this season) AND **cannot be ascended to the Earth realm at season end** (cannot be added to the form library for future seasons)
   - The trade-off is real: keep playing this character (refuse, accept XP loss) vs commit to a new form (accept, lose this class forever for the season)
   - **This is distinct from Trial body-swap** — Trial swaps are mini-ascensions with positive rewards (XP + resistances + skill point); death body-swap is the harsh-consequence alternate path.

5. **What does Reincarnated NOT want to copy from genre flagships?** → **RESOLVED: anti-patterns list locked.**
   - ❌ Paragon-style infinite grind (D3/D4 paragon doesn't fit one-week seasons; level-50 soft cap is intentional)
   - ❌ Mandatory respec gold (PoE Orbs of Regret punishes experimentation; conflicts with B9c's "strict during play, paid endgame")
   - ❌ Level-locked content gates (D3 GR-tier prerequisite friction; doesn't fit player-agency thesis)
   - ❌ Skyrim-style full player-level monster scaling (Section 6 will revisit; full scaling = anti-pattern per genre consensus)
   - ❌ Hardcore mode as launch requirement (defer; ship without it; revisit post-launch)
   - ❌ Mid-game balance debt acceptance ("your build comes online at level X" — explicitly REJECT via multi-band sim per Section 8 architectural commitment to Option β)

### 📚 Reference notes (genre research)

- **XP-driven is the genre default.** Effectively 100% of mainstream loot-driven ARPGs use kill→XP→level as the spine (D2, D3, D4, PoE 1+2, Last Epoch, Grim Dawn, Torchlight 2). Variance is in *what else feeds the curve*, not whether XP exists.
- **D2 is the canonical hybrid.** Monster XP + quest rewards giving skill points (Den of Evil A1 +1, Radament A2 +1, Fallen Angel A4 +2 — repeated across 3 difficulties = **12 skill points + 15 stat points + permanent life/resist bonuses from quests alone**). This is the cleanest precedent for Reincarnated's "20 from quests/bosses" model.
- **D3 = purer XP-driven.** Quest XP exists in Campaign Mode (Normal/NM/Hell) only and disappears at Inferno/L60. System relies on monster XP + difficulty multipliers, not milestones.
- **D4 = layered hybrid via Renown.** Renown (account-wide currency from waypoints, Altars, dungeons, side quests, strongholds) converts to skill points at specific thresholds (Tier 1 = 1 SP + XP + gold; Tier 3 = another SP). 5 regions × 2 SP = 10 quest-source skill points.
- **PoE = strong hybrid.** 99 levels + 23–24 quest passive points + 20 quest refund points; ~20% of total budget comes from quests.
- **Death-as-progress (Hades model) is rogue-lite, NOT ARPG.** No mainstream loot-ARPG uses death as primary progression spine. The closest analog is D4's Renown being account-wide so dead characters' progress persists for alts. Loot-ARPGs commit to a single long character arc; rogue-lites commit to meta across many short runs — opposite design philosophy. The body-swap pillar puts Reincarnated in interesting middle ground.

Sources: [Maxroll D3 XP](https://maxroll.gg/d3/resources/experience-explained) · [D2R quest rewards](https://www.rpgstash.com/blog/d2r-quests-skill-stat-life-resist-bonus) · [Maxroll D4 Renown](https://maxroll.gg/d4/resources/renown-system) · [PoE passive points](https://www.poewiki.net/wiki/Passive_skill) · [Hades meta-progression analysis](https://dms462fall2020.wordpress.com/2020/12/06/meta-is-etymologically-greek-right-meta-progression-in-hades/)

---

## Section 2 — Character combatant progression

### ✅ Decided
- **Endgame: character level 50** (B9 series).
- **Skill point gains:** 2 per level (100 total) + 20 from quests/act-bosses = 120 endgame budget (B9b).
- **Trait acquisition floors:** 1, 12, 25, 38 (B9a) — implies a stable level curve a player traverses.

> **🔗 Vocabulary note (added 2026-05-11 by Matt; full discussion in Section 4 § Open):** "skill point gains" assumes a particular relationship between *skills* and *abilities* that hasn't been formally defined. Are they the same thing? Overlapping subsets? Distinct concepts? **See Section 4 Open #6 for the full question + proposed taxonomies.** Resolving this affects how every section below talks about ability/skill/trait acquisition.

### ⚠️ Thought through
- Endgame state is balanced; "scale back" data structures exist conceptually (file 28 line 521).
- Body-swap mid-act preserves world state + quest progress + inventory (file 29 § "Cross-season meta-progression"); class identity transforms.

### 🔴 Open → ✅ RESOLVED 2026-05-11
1. **XP curve shape.** → **LOCKED: smooth polynomial (Option α).** Polynomial exponent ~2.0-2.5 hits "Act-1-quick / Act-3-substantial" naturally. Specific per-level XP values tuned during engine implementation. Matches D2 lineage scaled to 50 levels (vs D2's 99).
2. **Level cap behavior.** → **LOCKED: hard cap L50, free pre-cap leveling.** No Paragon-equivalent (anti-pattern lock from Section 1). No per-act soft caps — multi-band sim (B14) provides confidence at L17/L33/L50 specifically; overleveling earlier acts is fine and rebalances naturally via per-band gauntlet.
3. **What grants XP** → **LOCKED via Section 1:** monster kills + quest completion XP + discovery XP + Trial body-swap XP (all four sources).
4. **Death penalty** → **LOCKED via Section 1:** body-swap-offered model with seasonal-death consequences for accept; 5-10% XP loss for refuse; no gear durability; no gold drop (file 32 § 9).
5. **Body-swap and level inheritance** → **LOCKED: yes — inherit player level.** Body-swap is CLASS CHANGE, not character reset. Trial body-swap bonuses (XP + SP + resistances) apply ON TOP of inherited level state.
   - **Build reset implicit at body-swap** (per B9c reset triggers): player re-allocates total earned SP across the new class's tree. Spirit Guide recommends a starting distribution based on the new class's meta build for current band.

### 📚 Reference notes (genre research)

**Level caps + XP curve shapes:**
- **D2:** cap 99; polynomial-then-exponential. L1→2 = 500 XP; L10→11 ≈ 14,429; L20→21 ≈ 134,378; L40→41 ≈ 1.96M; L99 requires multi-billion totals. XP comes almost entirely from monster kills (with quest bonuses layered in). Optimal XP within ±5 levels of monster level.
- **D3:** cap 70 post-RoS, then uncapped Paragon. Paragon XP scales: P1–60 = 1.44M/lvl; P61–70 = 2.88M; P71–80 = 5.02M; into trillions at P2,250+. Paragon is account-wide.
- **D4:** cap raised 60→70 in Lord of Hatred (S13). Skill points 2–50 = 48 from levels. Paragon starts at L50 with ~4 Paragon points/level. Recommended act levels: Prologue → L5; A2 ≈ L10; A3 ≈ L15; A4 ≈ L20; A5 ≈ L35; A6 ≈ L40–45.
- **PoE:** cap 100 (effective soft cap — very few reach it). XP grows steeply; death penalty + 10% map XP loss makes 95→100 a months-long grind. Monster levels 1–67 campaign, 68–84 maps.
- **Grim Dawn:** cap 100. **Deliberately front-loaded** skill point curve: **3/level at L2–50, 2/level at L51–90, 1/level at L91+**. Plus 1 attribute point + 10 OA + 10 DA per level.
- **Torchlight 2:** cap 100. 5 stat points/level. 100 SP from levels + 32 from Fame = 132 total.

**Reincarnated implications:**
- Reincarnated cap = **50**, which sits below all comparable ARPGs (TL2/GD/PoE = 100; D3/D4 = 70 + Paragon). This is intentionally a SHORTER arc — closer to D2's "real game" window (D2 endgame is L80-90 territory; L99 is grind).
- 50 levels × 2 SP/level = 100 SP from levels matches **PoE's "1 passive per level" rhythm**, not D2's "1 SP/level".
- A polynomial-then-exponential XP curve is genre standard; flat curves trivialize late game.
- ±5 level optimal band (D2 standard) is a clean rule for monster-level fit; would map cleanly to Section 6's monster-scaling discussion.

Sources: [D2 official XP table](https://classic.battle.net/diablo2exp/basics/experience.shtml) · [Maxroll D2 XP](https://maxroll.gg/d2/resources/experience) · [D3 Paragon charts](https://www.diablowiki.net/Paragon_experience_charts) · [D4 leveling guide](https://www.icy-veins.com/d4/guides/quick-reference-campaign-leveling-guide-for-diablo-4/) · [PoE XP](https://www.poewiki.net/wiki/Experience) · [Grim Dawn skill points/level](https://orbispatches.com/gaming-faq/how-many-points-do-you-get-per-level-in-grim-dawn)

---

## Section 3 — Stat point progression

### ✅ Decided
- **Six attributes:** STR, DEX, INT, WIS, VIT (CON), AGI (currently dead/reserved per decisions-log 2026-05-09).
- **50-tier stat scale aligned with character levels** (foundation.md line 156: "A level-50 character uses tier-50 abilities and gear").
- **Stats per class are differentiated** (existing engine state — fire mages get INT-scaling, warriors STR, etc.).
- **Stats do NOT drive movement speed** (2026-05-11 design directive). Movement speed is gear-driven, primarily from boots affixes. **AGI must NOT be revived for movement speed** even though it's currently dead/reserved. See **Section 12 — Movement speed and mobility**.

### ⚠️ Thought through
- Engine math knows stat-to-effect scaling (HEAL_WIS_SCALE = 0.002, etc.).
- B9 doesn't touch stats — its 120 budget is skill points only.

### 🔴 Open → ✅ RESOLVED 2026-05-11
1. **Allocation model.** → **LOCKED: auto-allocate per class identity (D3-style).** Class generator determines stat growth per archetype (fire mage = INT-heavy auto-allocation; warrior = STR-heavy; etc.). No player allocation. Reasoning:
   - Player-agency thesis (Section 1) is about SKILLS / BUILDS, not stats
   - Shaped-balance philosophy = build variance via skills/gear/traits/aspects, NOT stats
   - Eliminates min-max stat trap (D3's documented design rationale)
   - Consistent with AGI-dead/reserved decision (Section 12) — if player-allocated, players would put points in AGI looking for effect
2. **Reset rules.** → **LOCKED: N/A (auto-allocation).** Engine controls stat distribution; no player reset applicable.
3. **Stat point count per level** → **LOCKED: N/A (auto-allocation).** Engine determines per-class growth rates.
4. **Diminishing returns curves.** → **LOCKED: existing soft caps preserved.** Current engine has `DODGE_CHANCE_CAP = 0.60` + `CRIT_CHANCE_CAP = 0.75`. Additional soft caps documented during engine impl as patterns surface — not an architectural decision.

### 📚 Reference notes (genre research)

**Allocation model spectrum across genre:**
- **D2 = full free allocation.** 5 stat points/level (495 total) across STR/DEX/VIT/ENG, allocate anywhere. Plus Lam Esen's Tome quest +5 × 3 difficulties = +15. Free respec once per difficulty from Akara (after Den of Evil); additional respecs via Token of Absolution craft.
- **D3 = no player stat allocation at all (during 1–70).** Stats auto-allocate, biased to class primary. Jay Wilson's design rationale: *"Stat progression as a system is very difficult for a lot of players to understand."* Player choice returns at Paragon — cycling Core/Offense/Defense/Utility with each Off/Def/Util capped at 50. Free Paragon respec anytime out of combat.
- **PoE = no raw stat points, passive tree only.** All STR/DEX/INT comes from tree node traversal or jewel sockets. 99 levels = 99 points + 23–24 quest passive + 20 quest refund. Respec via Orbs of Regret (1 point each — drop/buy) or quest refunds. Full respec is intentionally hard to discourage rerolling-via-respec.
- **Last Epoch = passive-tree with mastery gating.** ~113 passive points across base + mastery trees. Mastery class (selected mid-campaign Ch4) is **permanent**. Respec passive points by paying gold per node.
- **Grim Dawn = hybrid.** 1 attribute point/level (free across Physique/Cunning/Spirit) PLUS auto-granted 10 OA + 10 DA per level. Respec attribute points via Spirit Guide NPC for iron.
- **Torchlight 2 = D2-style free.** 5 stat points/level across STR/DEX/Focus/Vitality.

**Respec spectrum:**
- Free-anywhere (D3 Paragon, LE skills) → cheap-anywhere (GD, LE passives via gold) → limited-quest-based (D2, PoE) → none/permanent (LE mastery choice).
- PoE's design philosophy: limit respec so players reroll instead of fixing.

**Reincarnated implications:**
- B9c's "strict during play, paid endgame" matches PoE's reroll-discouraging philosophy, not D3's free-anytime.
- Reincarnated has 6 attributes (STR/DEX/INT/WIS/VIT/AGI), which is one more than D2's 4 — affects per-level allocation math if going player-allocated.
- AGI is currently dead/reserved per decisions-log; if stat allocation goes player-driven, AGI either needs to acquire meaning OR be removed.
- The body-swap pillar may map cleanly to mastery-style permanence — class identity transformation is conceptually similar to "you can't undo your mastery pick" but applied at the season-level.

Sources: [D2R skill points](https://www.gamerguides.com/diablo-ii-resurrected/guide/characters/builds/skill-points) · [D3 attributes design](https://www.diablowiki.net/Attributes) · [PoE respec](https://www.poewiki.net/wiki/Respec) · [LE passives](https://maxroll.gg/last-epoch/resources/passives-and-skills) · [Grim Dawn attributes](https://grimdawn.fandom.com/wiki/Attributes)

---

## Section 4 — Ability progression (extends B9)

### ✅ Decided
- **Skill point budget:** 120 at endgame (B9b).
- **Per-skill cap:** 15 (B9b — allows ~8 maxable from 10-15 kit; forces specialization).
- **Trait pool:** 5-10 per class with floors 1/12/25/38, max rank 4 (B9a).
- **Reset rules:** strict during play, paid endgame (B9c).
- **Spirit Guide as build coach:** recommends optimal distribution (B9c).
- **All eligible traits reach similar power at character level 50** (B9a calibration intent).

### ⚠️ Thought through
- Trait curves: higher-floor traits start more powerful AND ramp faster, so all converge by level 50 (file 28 lines 537-543; file 31 Stage 7).
- Skill scaling coefficients: engine-determined per skill (primary attacks ~1.05/point; ultimates ~1.20/point — file 31 Stage 5).
- Engine computes optimal 120-point distribution as the "meta build" — written to export packet (file 31 Stage 6).
- Naming: trait names get LLM treatment with archetype context (file 28 § "trait naming pipeline").

### 🔴 Open → ✅ RESOLVED 2026-05-11

1. **Trait moment-of-acquisition.** → **LOCKED: auto-unlock all at floor; auto-rank with character level.** At trait floor level N (1, 12, 25, 38), all class traits with that floor automatically activate. Traits AUTO-RANK based on character level + per-trait curve (B9a calibration intent: "all eligible traits reach max rank at L50"). Player does NOT invest skill points in traits — traits are passive class-identity.
   - **No trait choice within pool.** Class identity IS the trait pool; player agency lives at skill investment level.
   - Open follow-up (future consideration): whether traits should ALSO have tree structure like skills. Deferred — keep simple for now.

2. **Skill availability over time.** → **LOCKED: all skills present in the class kit from L1, BUT gated by tier-unlock structure (Q4.3).** Player can SEE the full skill tree from L1; can only INVEST in Tier 1 initially; higher tiers unlock via investment thresholds.

3. **Skill rank cap progression.** → **LOCKED 2026-05-11: Hierarchical Skill Tree with Dimensional Threading.** See dedicated subsection below — significant design that uses mathematical / geometric / thematic / color / power-curve dimensions per Matt's creative direction.

4. **Quest-reward skill points.** → **LOCKED via Section 11:** 20 SP from Trial body-swaps (4/7/9 per act) — already locked.

5. **Trait stacking with gear traits.** → **LOCKED: additive across all sources.** Same trait name from gear + progression + aspects = additive stacking (e.g., +10% fire damage from gear + +10% from progression trait = +20% fire damage total). Matches genre standard.

### Q4.3 Detail — Hierarchical Skill Tree with Dimensional Threading (LOCKED 2026-05-11)

The smooth cap math is preserved, AND layered with hierarchical tree structure that uses multiple design dimensions.

#### Tree structure

Each class kit organized as a TREE with:

**Vertical axis: 4 TIERS (power hierarchy + math dimension)**

| Tier | Count | Role | Power identity |
|---|---|---|---|
| Tier 1 — Primaries | 3-5 skills | Spammable, low cost | Base power; available from L1 |
| Tier 2 — Mids | 3-5 skills | Medium cost, higher power | Build-defining body |
| Tier 3 — Advanced | 2-4 skills | Spender-shaped | Build-specialization layer |
| Tier 4 — Keystones | 1-3 skills | Ultimate / class-identity peak | Build-climax payoff |

**Horizontal axis: 2-4 CHAINS (thematic + color dimensions)**

- Each chain runs vertically through some/all tiers
- Each chain has LLM-named **thematic continuity** (e.g., Spark → Fireball → Inferno → Phoenix Reborn)
- Each chain has **color palette coherence** (element-base + chain-specific tint)
- Each chain has **textual identity** ("the Combustion line", "the Heat line", "the Defensive line")

**Example fire mage — 3 chains × 4 tiers = ~12 skills:**

| Tier | Combustion Chain | Heat Chain | Defensive Chain |
|---|---|---|---|
| 4 (Keystone) | Phoenix Reborn | Solar Apocalypse | Inner Sun |
| 3 (Advanced) | Inferno | Conflagration | Solar Form |
| 2 (Mid) | Fireball | Combustion | Ignite Aura |
| 1 (Primary) | Spark | Heat Wave | Flame Shield |

#### Chain count variance — supports archetype emergence

**Chain count varies per class** (locked 2026-05-11 — Matt's directive to "allow variance to emerge"):

- **Specialists:** 2 chains × 4 tiers = ~8 skills (deep single-chain mastery)
- **Balanced:** 3 chains × 4 tiers = ~12 skills (default-ish)
- **Generalists:** 4 chains × 3 tiers = ~12 skills (wide options, fewer Tier-4 keystones)
- **Asymmetric chain depth allowed** — e.g., 1 chain × 4 tiers + 2 chains × 3 tiers = 10 skills (focused with options)

Generator picks chain count + depths per class based on archetype dimensions:
- Single-element specialists → favor fewer/deeper chains
- Multi-element hybrid_mage → favor more chains (broader element coverage) *[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. Post-canonical-6, multi-element generated archetypes are not produced; this chain-count rule was hybrid_mage-specific and no longer applies to any canonical-6 archetype. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*
- Engine generates the shape; novel archetypes (e.g., "dual-keystone-rusher") emerge

#### Hierarchical unlock gates (the mathematical dimension)

Tier N+1 unlocks based on **rank investment in Tier N parent skills:**

| Tier | Unlock requirement |
|---|---|
| Tier 1 | Available from L1 (always) |
| Tier 2 | ≥3 ranks invested in any Tier 1 parent skill |
| Tier 3 | ≥5 ranks invested in any Tier 2 parent skill |
| Tier 4 | ≥8 ranks invested in any Tier 3 parent skill |

Unlocks are based on **per-skill rank** (not cumulative across skills). Tier 4 requires deep commitment to a build path, not casual spreading.

#### Cross-chain unlock asymmetry (encodes archetype identity)

**LOCKED 2026-05-11 per Matt's directive — cross-chain rule depends on class element distribution:**

| Class element distribution | Cross-chain unlock rule | Effect |
|---|---|---|
| **Multi-element** (hybrid_mage, etc.) | **ANY Tier N skill unlocks Tier N+1** (cross-chain investment counts) | Build flexibility; encourages multi-chain builds; matches multi-element identity |
| **Single-element** (fire_mage, etc.) | **Only SAME-CHAIN Tier N skill unlocks SAME-CHAIN Tier N+1** (strict chain investment) | Build depth; specialist identity; forces deep commitment to one chain at a time |

This **mechanically encodes archetype identity into the skill tree structure** — single-element classes get focused specialist depth; multi-element classes get build breadth.

*[hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; the "Multi-element" row above is historical record. Post-canonical-6, multi-element generatively-produced archetypes are not part of the canonical roster; the cross-chain unlock rule for multi-element classes no longer applies to any actively-generated archetype. If gear-secondary-element kit shapes emerge (see canonical-6 transition § 5.3), their skill-tree cross-chain rules are a post-canonical-6 design decision. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for context.]*

#### Smooth rank cap (preserved)

`rank_cap_per_skill = min(15, floor(level/3.33))`

| Level | Rank cap | Tier-progress milestone |
|---|---|---|
| L1 | 1 | Tier 1 only |
| L7 | 2 | Tier 1; approaching Tier 2 unlock (need rank 3) |
| L10 | 3 | **Tier 2 unlocks** (≥3 reachable) |
| L17 (Act 1 end) | 5 | Tier 2 fully usable; **Tier 3 unlocks** (≥5 reachable) |
| L26 | 7 | Tier 3 progressing toward Tier 4 unlock |
| L27 | 8 | **Tier 4 unlocks** (≥8 reachable) |
| L33 (Act 2 end) | 10 | Tier 4 progressing |
| L50 (endgame) | 15 | Full tree available, max ranks |

**Natural pacing** — Tier 4 keystones unlock organically as commitment to a build path deepens. No arbitrary level milestones; the math gates content via the player's investment shape.

#### Tier-specific scaling coefficients (the power-curve dimension)

| Tier | scaling_coefficient range | Per-rank power gain |
|---|---|---|
| Tier 1 (primary) | 1.05-1.08 | Modest per-rank; spammable feel |
| Tier 2 (mid) | 1.08-1.12 | Moderate per-rank |
| Tier 3 (advanced) | 1.12-1.18 | Strong per-rank |
| Tier 4 (keystone) | 1.18-1.25 | Very strong per-rank (build-defining payoff) |

Each Tier 4 keystone rank is dramatically more impactful than Tier 1 rank — rewards late-game commitment to keystones.

#### Build patterns that emerge

| Build pattern | Distribution shape | Feel |
|---|---|---|
| **Pure-chain specialist** | Max 1 chain through all 4 tiers + light Tier 1 fillers | One build line maxed; "I'm a fire-combustion mage" |
| **Two-chain balanced** | Max 2 chains through Tier 3; keystone in one | Versatile; build-defining keystone with depth in two |
| **Cross-tier hybrid** | Multiple Tier 1+2 maxed; few advanced | Wide kit; lots of options; no keystone |
| **Keystone-rusher** | Min path to one Tier 4 + heavy investment | Build defined by one keystone; everything supports |

Multiple viable build patterns emerge naturally from 120 SP budget × tree structure × smooth cap × tier coefficients.

#### Engine + generator implications (B6 extension + B14 integration)

**B6 generator additions:**
- Determine class element distribution (single vs multi) → locks cross-chain unlock rule
- Pick chain count + depths per archetype (variance allowed)
- Per-skill metadata: `tier` (1-4), `chain_id`, `chain_position`, `parent_skill_ids`, `scaling_coefficient`
- Tree validation: chain structure consistent; tier counts within target ranges (3-5/3-5/2-4/1-3 per chain)

**B14 multi-band convergence:**
- Per-band optimal distribution computed against TREE not flat skill list
- Tier-unlock constraints checked at each band (e.g., L17 band optimal can't max Tier 4 because cap=5)
- Spirit Guide recommends paths through tree per band

**LLM naming pipeline:**
- Chain-coherent skill naming (Tier 1 chain anchor + tier-progression naming)
- Context: chain affiliation + tier + parent skills
- Same call count (~12-15 names/class); richer thematic continuity

**Demo/UI:**
- Skill tree visualization (D4-style branching, Last Epoch per-skill, or simpler tier-row layout)
- Show unlock state per tier (locked/unlocked)
- Investment ranks visualized
- Chain color tinting for visual grouping

#### Body-swap interaction

At Trial or Death body-swap:
- New class has its OWN tree structure (potentially different chain count, tier shape, cross-chain rules)
- Player's earned SP is RESET across the new tree (per B9c: body-swap is a free-reset trigger)
- Spirit Guide recommends a starting distribution on the new tree for the player's current band
5. **Trait stacking with gear traits.** File 17 line 461 mentions same-schema-different-lifecycle — does the engine separate "progression traits" from "gear traits" in the convergence loop?

6. **Abilities vs skills vs traits — vocabulary alignment** (added 2026-05-11 by Matt; **RESOLVED 2026-05-11 — Taxonomy A-prime adopted as working hypothesis** after Matt confirmed the underlying design concerns are covered by existing B9a + B9b, just under confusing labels).

**Resolution:** Adopt Taxonomy A-prime (D4 model) as the working vocabulary:
- **Player-facing — three named categories:**
  - **Skills** = the active class kit (10-15 slots; player invests skill points; per-skill cap 15). This is B9b.
  - **Aspects** = gear-granted active/passive effects (legendary `granted_ability`, `aura`, `on_hit`, `cast_on_attack`). This is B5.
  - **Traits** = passive modifiers acquired through progression (5-10 per class with floors 1/12/25/38, max rank 4). This is B9a.
- **Engine-internal:** keep `generate_ability()` as the generic generator; tag outputs as skill/aspect/trait. No engine code renames required.

**Skill-nodes / augment-slots clarification:** during the design discussion, Matt raised the concept of "skill nodes / augment slots / non-fundamental ability-esque skills loaded into skill nodes." These map cleanly to **existing B9a traits** — the trait pool IS the passive-augment infrastructure (5-10 per class, varying floors, max rank 4, modifies active skills or character stats). No new mechanism needed; the existing B9a infrastructure covers this design space once relabeled per Taxonomy A-prime.

**Original framing (preserved for historical record):**

This was a real conceptual gap that affected every section below. **Current engine usage is inconsistent:**
   - File 28 B5 introduces `granted_ability` (legendary gear adds a "7th hotbar slot") + `aura` + `on_hit` + `cast_on_attack` — using "ability" as the umbrella
   - File 28 B9b says "120 skill points... 10-15 skill kit per archetype" — using "skill" for the class kit
   - File 17 line 419 says "Class progression (Priority 14: Traits-and-Skills system)" — using "skills" again for the progression kit
   - File 17 line 441: "Granted abilities — add a new ability to the class's repertoire. Rarer; legendary-tier gear or late-game progression unlocks" — using "ability" for kit additions

   **Two plausible taxonomies to choose between:**

   **Taxonomy A — engine-current (ability = base; skill = invested ability):**
   ```
   Ability  = base mechanical unit (geometry + element + role + effect + trigger)
   Skill    = an ability that occupies a class kit slot (10-15 per class)
            → receives skill point investment (0-15 each, cap 15)
            → subject to B9c reset rules
            → LLM-named with archetype context
   Granted  = ability sourced from legendary gear (B5)
   ability    → not in class kit; doesn't receive skill points
              → has its own hotbar slot (7th)
   Aura/proc/= ability with non-player-triggered firing (B5 aura, on_hit, cast_on_attack)
   trigger    → no hotbar slot; fires on condition
   Trait    = NOT an ability — passive modifier (B9a, gear traits per file 17)
   ```
   Under Taxonomy A: **all skills ARE abilities** (kit-slotted abilities); **not all abilities are skills** (granted abilities, auras, procs are abilities but not kit-slotted).

   **Taxonomy B — D&D-style (skill = broad capability; ability = active power):**
   ```
   Skill    = any capability the character possesses (umbrella)
            → includes active abilities, passive traits, gear-granted effects
   Ability  = an active power within the skill set (player-triggered)
            → kit abilities, granted abilities, all consolidated
   Trait    = a passive skill (no active trigger)
   Proc/aura= an automatic-firing ability (sub-category of ability)
   ```
   Under Taxonomy B: **abilities ⊆ skills**; **traits ⊆ skills**; both are sibling subsets of "skill."

   **Stakes of the decision:**
   - Engine API naming (`generate_ability()` vs `generate_skill()` — current engine uses the former)
   - Naming pipeline (file 31 Stage 12 — "Skill names: each slot now has distinct..." uses Taxonomy A implicitly)
   - File 33 skeleton structure (currently written in Taxonomy A)
   - Player-facing UI vocabulary ("skill points" vs "ability points" vs both)
   - Spirit Guide build-coach surfacing (does it recommend "skills" or "abilities" or both?)
   - LLM prompts ("generate an ability for…" vs "generate a skill for…")

   **My read (subject to revision):** Taxonomy A matches current engine usage and is the lower-friction choice. Taxonomy B has more linguistic clarity (skill = capability is closer to vernacular) but requires renaming a lot of existing engine code and pipeline references. **There's also a hybrid where "ability" is engine-internal and "skill" is player-facing** — same thing, two labels for two audiences.

   This question needs to resolve before Section 4's other open questions can be answered cleanly. It also touches Section 5 (do gear `granted_ability` items add to the skill point budget, or are they separate?), Section 7 (alignment validation — does sim count granted abilities the same as kit skills?), and Section 8 (sim architecture — does multi-band convergence treat them identically?).

7. **🆕 Spirit Guide gear-percentile awareness — meta vs above-meta gear** (added 2026-05-11 by Matt). The convergence loop balances classes at `GEAR_PERCENTILE=0.75` baseline. Spirit Guide trains on the resulting "meta build" — the optimal 120-point distribution for 75th-percentile gear. **But** with 95th-99th percentile gear (B7 variance-check territory), the meta's optimality assumption breaks: *a player who finds an exceptional legendary might genuinely beat the meta by deviating to a skill that the sim under-valued.* Spirit Guide currently has no way to recognize this — its build coaching is anchored to 75th-percentile assumptions.

**This is the player-agency-vs-sim-tuning question.** Matt explicitly wants:
- Players free to deviate from the meta to define personal builds (even if underperforming)
- Players free to capitalize on godly gear by selecting "under-appreciated" abilities that the sim couldn't see (because sim didn't model that gear tier)
- Spirit Guide to recognize when above-baseline gear changes the optimal distribution, not be locked to 75th-baseline recommendations

**Three answers proposed:**

- **Answer A — "Meta is the floor of competence."** Spirit Guide trains on 75th-percentile gear meta only. Players who beat the meta with godly gear are doing it intentionally and don't need the Guide's blessing. The Guide's job is to keep average players from falling behind, not to optimize at the ceiling. **Simplest; matches existing B9c spec.**
- **Answer B — Multi-band gear-percentile-aware Spirit Guide.** Engine runs convergence at multiple gear percentile bands (50th / 75th / 90th / 99th) — produces multiple "meta builds" per class, one per band. At runtime, Spirit Guide detects the player's actual equipped percentile and surfaces the meta build for that band. A player with 99th-percentile gear sees a different recommended build than a 75th-percentile player. **Most rigorous; ~3-4× convergence cost; aligns architecturally with Section 8 multi-band sim if chosen — same percentile axis as B7's variance check.**
- **Answer C — Runtime heuristic adaptation.** Engine only converges at 75th. At runtime, Spirit Guide notices "your gear is much better than baseline" and applies a heuristic shift to recommendations (e.g., "since your gear's high-end damage is +40% over baseline, AOE skills become relatively stronger; bias recommendations toward AOE"). **Middle cost; heuristic quality is uncertain.**

**Architectural alignment:** Answer B is the rigorous choice **and** aligns architecturally with Section 8's multi-band sim. If Section 8 picks Option β (3-tier level-band: L10/L25/L50), adding a gear-percentile axis on top is the same architectural pattern. The convergence call becomes:

```
converge(class, gear_percentile=[0.50, 0.75, 0.90, 0.99] × level_band=[10, 25, 50])
```

= 12 convergence runs per class. Each produces a meta build. Spirit Guide picks the right one based on player state (current level + equipped gear percentile).

**Reincarnated-distinctive:** no mainstream ARPG does this. PoB / Maxroll planners are community tools; they don't ship with the game. Reincarnated's engine + Spirit Guide as an INTERNAL build-coach trained across the full gear × level matrix is genuinely novel.

**Cross-references:** Section 7 (alignment validation — multi-band meta needs validation pass), Section 8 (sim architecture — the level-band sim should add the gear-percentile axis if Answer B is chosen).

### 📚 Reference notes (genre research)

**Acquisition UX patterns across genre:**
- **D2 = skill point + class tree + skill-tier gates.** 1 SP/level on a class-specific tree (3 sub-trees × ~30 skills). **Skills have *level prerequisites*: tier-1 at L1, tier-2 at L6, tier-3 at L12, tier-4 at L18, tier-5 at L24, tier-6 at L30.** So the gate isn't just having points — it's reaching the right character level. Plus quest skill points. Max 20 per skill + gear bonuses.
- **D3 = auto-unlock at level + rune slots.** Active skills auto-unlock at specific character levels; players pick from a hot-bar of 6 slots; rune variants unlock per skill as the player levels. No skill-point *spending* — choice is *which slot/rune*, not *how to invest*.
- **D4 = branching skill tree.** 1 SP/level (2–50) = 48 from levels + 10 from Renown = 58 max. Tree clusters: Basic/Core/Defensive/Utility/Mastery. Ranks 1–5 per active. At L50, skill points stop and Paragon Boards take over.
- **PoE = orthogonal acquisition (skill gems + passive tree).** Active abilities are *items* (gems) that level up with use and socket into gear; passive points spent on the global tree. Completely independent paths.
- **Last Epoch = per-skill skill tree + class passive tree.** Each active ability has its own ~20-node subtree, in addition to the class passive tree. Some skills unlock by char level, others by spending points in the base class passive tree (4 unlock this way), others by Mastery choice.
- **Grim Dawn = dual-mastery hybrid.** Pick 2 of 9 masteries; skill points buy ability ranks AND mastery bar levels (which unlock new tiers). Devotion is a separate constellation tree leveled via shrines.

**The closest analog to Reincarnated's "trait gained at level 12":**
- **No major ARPG uses pure "you-just-get-it-at-N" auto-grant** for traits the way B9a's floor pattern describes.
- Closest analogs:
  - **D2's skill-tier unlock at level milestones** (skill becomes *available* at L6/12/18/24/30 — but you still spend a point to invest)
  - **D4 paragon legendary nodes** (gain a slot at level 50, fill it later with choice)
- The trait-floor pattern is **closer to Last Epoch's per-skill specialization gate or D2's tier unlock than to any auto-grant system.** This is genuinely a novel mechanism in genre terms — worth knowing.

**Reincarnated implications:**
- B9a's "floor at level N" maps to D2's tier-unlock gate (genre-precedent). Choosing AUTO-GRANT (vs choice-from-pool vs quest-reward) is a real design decision with no dominant genre pattern.
- B9b's 120-point budget over 10-15 skills is closer to D4 (58 max over ~25 skills × 5 ranks = 125 max points) than D2 (skill cap 20 over far fewer slots).
- The Spirit Guide build-coach pattern (recommended-allocation surfacing) has no clean genre analog — community tools (PoB, Maxroll planners) play this role externally. Spirit Guide as INTERNAL build coach is a Reincarnated-distinctive feature.

**Vocabulary across the genre (relevant to Open #6 abilities-vs-skills question):**
- **D2:** "**skills**" exclusively for the kit (skill tree, skill points, +skills gear bonuses). The word "ability" appears in flavor text but not as a mechanical concept.
- **D3:** "**skills**" for the hotbar slots; "**runes**" for variants of a skill. No "ability" as a separate concept.
- **D4:** "**skills**" for tree-invested kit; "**Aspects**" for legendary-granted effects (NOT called abilities — Aspects are their own category, closer to Reincarnated's `granted_ability` + `aura` concepts merged).
- **PoE:** "**skill gems**" for active abilities (skill = the item; ability = the effect, used interchangeably); "**passives**" for tree nodes. "Ability" rarely used in formal vocabulary.
- **Last Epoch:** "**skills**" for the kit; "**passives**" for tree. Same pattern.
- **Grim Dawn:** "**skills**" for both class trees AND devotion constellation. "**Abilities**" appears in flavor only.

**Genre observation:** "**Skill**" is dominant ARPG vocabulary for the kit; "**ability**" is mostly flavor/synonym in the genre. D4's "**Aspects**" is the closest precedent for treating legendary-granted effects as a SEPARATE NAMED CATEGORY from kit skills — and that pattern works well player-facing.

**This argues for a Taxonomy A variant:**
- Player-facing: "**skills**" (the kit) + "**aspects**" (legendary-granted) + "**traits**" (passive modifiers) — three distinct named categories, no umbrella "ability" needed.
- Engine-internal: "**ability**" as the base generated unit; "**skill**" is the kit-slotted variant; "**aspect**" is the gear-granted variant; "**trait**" is the passive modifier.
- Same as D4 vocabulary, which the genre validates as clear to players.

Sources: [D4 Aspects](https://www.icy-veins.com/d4/guides/legendary-aspects/) · [D2 skill tree](https://diablo.fandom.com/wiki/Skill_points) · [PoE skill gem](https://www.poewiki.net/wiki/Skill_gem)

Sources: [D2 skill tier gates](https://diablo.fandom.com/wiki/Skill_points) · [D4 paragon boards](https://www.wowhead.com/diablo-4/guide/gameplay/paragon-boards-nodes-glyphs) · [PoE skill gem system](https://www.poewiki.net/wiki/Passive_skill) · [LE skill trees](https://maxroll.gg/last-epoch/resources/passives-and-skills) · [Grim Dawn masteries](https://grimdawn.fandom.com/wiki/Masteries)

---

## Section 5 — Gear progression

### ✅ Decided
- **Five rarity tiers:** common / uncommon / rare / epic / legendary (file 17 § "Tier gradient").
- **Stat-threshold equip gating** with calibrated `stat_requirements` (decisions-log 2026-05-09 — Option C).
- **70/30 smart-loot / pure-RNG hybrid** (file 17 § "Loot economy model" 2026-05-10).
- **One-week seasons** (file 17 loot economy model).
- **B5 legendary mechanical-novelty:** granted_ability / aura / on_hit / cast_on_attack (Stage A5).
- **End-game baseline:** `END_GAME_DROPS_PER_SLOT = 50` (file 17 line 80).
- **50-tier power scale aligned with character levels** (foundation.md).
- **Boots gear slot exists** (2026-05-11 design directive). Primary source of movement speed affix. **See Section 12 + file 28 B12** for the engine queue item (boots + gloves + belt + slot audit).

### ⚠️ Thought through
- `END_GAME_DROPS_PER_SLOT` becomes one entry in a tier of per-phase constants (file 17 line 107).
- LLM-naming gradient by tier: rare = first LLM-named tier; legendary = full LLM treatment (file 17 § "Tier gradient").

### 🔴 Open → ✅ RESOLVED 2026-05-11

1. **Tier-availability curves per character level.** → **LOCKED: monster-level-tied with band-appropriate rarity rates** (aligns with per-band monster pools from Section 8):

| Band | common | uncommon | rare | epic | legendary |
|---|---|---|---|---|---|
| A1 (L1-17) | 70% | 25% | 4% | 0.9% | 0.1% |
| A2 (L18-33) | 50% | 30% | 15% | 4% | 1% |
| A3 (L34-50) | 30% | 30% | 25% | 12% | 3% |

   Per-monster-tier multipliers on top (elite ~1.5× rare; boss ~3×; act-boss ~10× legendary).

2. **Power-score growth curve** → **LOCKED: polynomial matching XP curve** (`level^2.0-2.5` shape). Single shape parameter across XP / gear / monster scaling — consistent design dimension.

3. **`*_DROPS_PER_SLOT` per band** → **LOCKED:**
   - L17 (Act 1 end): **10 drops/slot**
   - L33 (Act 2 end): **25 drops/slot**
   - L50 (endgame): **50 drops/slot** (existing B9b lock)

4. **Item level (ilvl) as separate axis** → **LOCKED: YES** (PoE/LE pattern). Gear stamps with ilvl at drop time; affix-tier gating on ilvl (e.g., Tier-7 affix requires ilvl 35+); equip requirement = stat_thresholds + character_level ≥ ilvl - 3 (slight permissiveness for smuggled gear). Cross-season smuggled gear retains ilvl forever.

5. **Smart-loot phase shifts** → **LOCKED: constant 70/30 across all bands.** No phase-shifting; matches genre (D3/D4 keep constant). If playtest reveals early-game RNG starvation, revisit during engine impl.

6. **Cross-season smuggling principles** → **PARTIALLY LOCKED:**
   - ✅ Smuggling exists (per file 29 body-swap pillar + Earth meta-layer reveal)
   - ✅ Smuggled gear retains ilvl (no auto-scaling)
   - ✅ Capacity is limited (preserves rarity meaning across seasons)
   - 🔴 Open (deferred to Earth meta-layer design doc `../collaboration-handoff/34-earth-meta-layer.md`): specific capacity number; legendary-only-smuggling vs any-tier; cross-season ilvl validity if game numbers shift between seasons; stash overflow handling on Earth Self

7. **Final gear slot list (B12)** → **LOCKED: 10 slots:**
   1. Main hand weapon (1H or 2H per handedness)
   2. Off-hand (shield/orb/focus/off-hand-weapon/grimoire — 1H weapons only)
   3. Head (helmet for heavy; hood for caster — archetype-gated)
   4. Chest (chest for heavy; robe for caster — archetype-gated)
   5. **Hands (gloves)** — NEW per B12
   6. **Feet (boots)** — NEW per B12; primary movement speed source
   7. **Belt** — NEW per B12
   8. Ring 1 (2 ring slots — matches D3/D4/PoE)
   9. Ring 2
   10. Amulet

### Q5.8 — Seasonal Sets (NEW 2026-05-11 — Matt's addition)

**LOCKED: at L50, one seasonal gear set per playable class unlocks as a collectable.**

**Design intent:**
- Each season generates **one unique set per playable class** (5-6 sets per season)
- Sets are class-specific (set pieces only fit one class's archetype + stat requirements)
- Sets only **drop / become available at L50** (Act 3 endgame band) — the ascended L50 character is the only one who can collect their set
- **Set pieces are individually rare** (legendary-tier or above) — gathering a full set across one season is genuine endgame goal
- **Set bonuses** apply at multi-piece thresholds (genre-standard: 2-piece / 4-piece / full-set tiers)

**Strategic / narrative significance:**
- **Real seasonal goal** beyond "ascend a form": gather your favorite class's weekly seasonal set
- **Form library trophy value:** ascended spirits in the Earth Self library who wore the seasonal set become visible accomplishments
- **Earth meta-layer event value:** set-wearing spirits add identity + power to Earth events (PVP / PVE in the rift)
- **Procedural-generation gacha extension:** every season generates fresh unique sets per class — no two seasons produce the same set; collecting becomes meta-progression hook

**Generator additions:**
- Per-season set generation per playable class (5-6 sets × N pieces each)
- Set pieces share thematic identity (LLM-named with set theme: e.g., "Hearthwind's Pyric Robes" / "Hearthwind's Pyric Helm" / "Hearthwind's Pyric Boots")
- Set bonuses encoded mechanically (2-piece: +X% fire damage; 4-piece: +stat or +trait; full-set: cast_on_attack ability or major effect)
- Set affix coherence (all pieces emphasize class's primary scaling stat)

**Drop mechanism:**
- Set pieces drop ONLY from L50 content (Act 3 endgame)
- Specific encounter types favor set drops (act-boss / Trial boss kills favor set pieces?)
- Drop rate calibrated so a focused L50 player can complete a set in ~3-7 hours of endgame play
- Cross-season smuggling: set pieces smuggle to next season's Earth Self storage; can be "worn" by re-ascended forms

**LLM cost impact:**
- ~5-6 sets × 5-6 pieces × naming+flavor calls = +25-36 LLM calls/season
- ~+$1-2 per season (modest within $5-10/season budget)

**Engine queue: see file 28 B15** (Seasonal Sets) for the implementation queue item.

### Q5.9 — Mobile-first loot density solution (LOCKED 2026-05-11)

**Path (C) adopted: ship auto-pickup-with-rarity-filter near-term; pet system captured as design intent for a focused later sprint.**

#### Near-term: Auto-pickup with rarity filter (LOCKED — ships in Stage A3 demo follow-on)

- **Common / uncommon tier:** auto-pickup; auto-converted to gold/currency on pickup (no inventory friction)
- **Rare / epic / legendary tier:** auto-pickup; deposited into inventory for Spirit Guide review
- Spirit Guide marginal-value pass evaluates the rare+ drops; presents player with summary at room/encounter end ("3 Strong upgrades, 2 Sidegrades, 5 ignored — review?")
- Player can adjust the rarity threshold in settings (e.g., advanced players might want auto-pickup at rare-only and ignore uncommon)
- **Engine cost:** zero (uses existing rarity tier data + Spirit Guide marginal-value math)
- **Demo cost:** ~3-5 days (UX flow + rarity filter logic + summary screen)
- **Ships in Stage A3 demo follow-on** (gear regen produces new rarity tiers; auto-pickup consumes that data)

#### Pet system (LOCKED as design intent; specific scope deferred)

**Design intent captured** (per Matt's 2026-05-11 directive):
- Pet picks up gear automatically; takes to Spirit Guide for review
- Pet takes one inventory slot
- Pets drop with seasonal rarities (gacha extension layer)
- Pets become "fun + gacha-accumulation" layer on top of class/spirit accumulation
- Pets persist across body-swap (loyal companion regardless of class identity transformation)

**Scope deferred** because:
- Pet system = new generation pipeline + AI behavior + inventory mechanics + visual generation + handoff UX
- Realistic estimate: ~4-6 weeks engine + demo + design work
- Adding now would significantly expand Stage A3 already-large scope

**Pet system relationship to auto-pickup:**
- Auto-pickup solves the IMMEDIATE mobile-loot-density problem (Stage A3)
- Pet system, when shipped later, becomes the FUN layer on top — pet visually animates the pickup mechanic, adds gacha-collection dimension, and provides personality
- Pets may shift the auto-pickup THRESHOLD (e.g., higher-rarity pets pick up at lower thresholds, eliminating the player's need to manually adjust settings)

**Captured in:** memory file `project_pet_system.md` (Matt's design intent preserved for later focused sprint)

**When pets eventually ship:** likely Track B / demo2 territory (parallel to Engine 2 prototyping) — not core engine work; primarily game-feel layer.

### 📚 Reference notes (genre research)

**Tier-availability + ilvl patterns:**
- **D2 = area-level-driven drops.** Fixed by zone in Normal; in NM/Hell, area level = monster level. Champion/Unique mobs are +2/+3 mlvl. Hell endgame areas hit mlvl 85 (the cap for top drops). Treasure class is gated by area level; rares/uniques need specific item levels to roll.
- **D3 = Smart Loot 85%.** ~85% of item drops roll with affixes matching the finder's class. Most build-defining legendary sets only drop at **level 70**; some are Torment-only. Loot 2.0 reset the philosophy from D3 vanilla.
- **PoE = item level (ilvl) is a SEPARATE AXIS from character level.** Each base type has a *minimum drop level* (datamined, not displayed in-game). ilvl determines which affixes can roll. Monster level → ilvl, so map tier 16 areas drop ilvl 84+ items with top-tier mods. Character level only governs *equip requirements*, NOT drop ranges.
- **Last Epoch = affix tier scales with area level.** Tier 7 affixes require **area level 90+** to drop. Affix level requirements use a formula: `sum of affix level values + (2 × max affix value) − 10`. Effective item req = max(base req, affix req).
- **PoE/LE deliberately REJECT smart-loot** as part of trade-economy design. The 70/30 smart-loot/RNG model Reincarnated has committed to is the **D3/D4 lineage**, not the PoE/LE lineage.

**Two scales the genre converges on:**
1. **area/monster level → ilvl → affix tier eligibility** (universal)
2. **drop-rate weight by rarity tier scaled with difficulty** (universal)
3. Smart-loot ON or OFF is a binary lineage split (D3/D4 yes; PoE/LE/GD no).

**Reincarnated implications:**
- The 50-tier power scale (foundation.md) is closer to PoE's ilvl model than D3's level-70-gates-legendary model — a level-1 character technically COULD see a tier-50 item if the engine allowed it (and stat-threshold equip gating handles unwearability).
- **Smart-loot 70% IS the design choice already locked.** This puts Reincarnated in D3/D4 lineage; doesn't need to be re-debated.
- One real question: do gear TIERS have level-gates (legendary = L30+) like D3, or is it pure ilvl-based (PoE-style) where a level-5 character could theoretically drop a legendary that they can't equip yet?
- Genre median answer: **rarity tier × ilvl together gate drops**. D3 explicitly tier-gates (L70 for top sets); PoE ilvl-gates implicitly. Reincarnated's stat-threshold gating already implies the latter; could add explicit tier-gates as a design choice.
- **The `*_DROPS_PER_SLOT` tier from file 17 line 107 should be populated per-progression-phase** — early-game (L1-12) ≈ N=5-10 drops; mid-game (L13-25) ≈ N=15-25; late-game (L26-50) ≈ N=30-50.

Sources: [D2 area level](https://diablo-archive.fandom.com/wiki/Area_Level_(Diablo_II)) · [D3 Smart Loot](https://www.diablowiki.net/Smart_Loot) · [PoE ilvl](https://www.poewiki.net/wiki/Item_level) · [LE T7 affix gating](https://forum.lastepoch.com/t/tier-7-affix-item-drop-clarification/23051) · [Loot 2.0 design](https://www.diablowiki.net/Loot_2.0)

---

## Section 6 — Enemy / monster progression

### ✅ Decided
- **Seven monster tiers (B10):** swarm / magic / trash / elite / mini-boss / boss / act-boss with HP/damage multipliers 0.10× → 10×+ (Stage A3).
- **Boss fights stay 1v1** (B10 — genre convention preserved).
- **Procedural generation per season** — monsters generated by engine, not hand-authored.

### ⚠️ Thought through
- B10 multipliers are RELATIVE to a baseline — but the baseline itself isn't level-bound in the current spec.
- Trial bosses have damage_modifier (per-class balance lever); gauntlet monsters don't (file 16 was Priority 13 — partially absorbed into B10).

### 🔴 Open → ✅ RESOLVED 2026-05-11 (see "Section 6 + 7 closures" subsection below for inline locks)
1. **Scaling philosophy** (the architectural call): → **LOCKED: D2/PoE-style FIXED-PER-BAND** (see closures below)
   - **Fixed-per-zone (D2-classic):** Act 1 monsters always level 1-12; Act 2 always 13-25; etc. Overleveled player → trivializes content; underleveled → wall.
   - **Scales-with-player (Skyrim-style):** monsters always match player level. No level-walls but also no "I've outgrown this content" satisfaction.
   - **Per-act fixed with bands (D3/D4):** each act has a level band; within band, mostly-fixed; some scaling above max.
   - **Difficulty-tier scaling (D3 Greater Rifts):** content level scales with chosen difficulty, decoupled from character level.
2. **Monster level vs character level mapping.** If Act 1 = levels 1-12 and player reaches level 13, what happens in Act 1's remaining content?
3. **Trial boss level binding.** Trial bosses are class-converged opponents — do they scale with player level on encounter, or are they fixed at season-generation level?
4. **Pack composition per progression phase.** Early-game (level 5): is the pack still 5-12 swarm + 1 elite? Or simpler (smaller packs as player adjusts)?

### 📚 Reference notes (genre research)

**Four scaling models the genre uses:**

| Model | Games | Trade-off |
|---|---|---|
| **Fixed-per-zone** (classic) | D2 Normal, PoE campaign, LE campaign | Sense of progression preserved; over/under-leveling is real; "I've outgrown this content" satisfaction |
| **Scales-with-player** (full) | D3 post-RoS | No level-walls; loses zone identity ("every act feels the same") — widely cited anti-pattern |
| **Per-act fixed with bands** (D3/D4 hybrid) | D4 open world (scales) + dungeons (tier-fixed) + bosses (level-fixed until cleared) | Best of both: open exploration scales; tuned challenges don't |
| **Difficulty-tier scaling** (decoupled) | D3 Greater Rifts, D4 Pit Tiers, LE Monolith timelines | Content level scales with chosen DIFFICULTY, not character — opt-in challenge |

**Concrete level bands:**
- **D2:** A1 = mlvl 12/43/73 (Normal/NM/Hell), A2 = 17/49/80, A3 = 25/55/83, A4 = 28/58/85. Optimal XP within ±5 levels.
- **D4:** A1 = ~L1-10; A2 = L10; A3 = L15; A4 = L20; A5 = L35; A6 = L40-45.
- **PoE:** campaign 1–67; map tiers 1–16 map to area levels 68–83+ (T16 = area 83).
- **Last Epoch:** Monolith timelines have higher area levels per timeline; empowered at 100.

**Boss handling across genre:**
- D2 Ubers: always level 110 regardless of player.
- D4 story bosses: fixed levels until chapter cleared.
- PoE bosses: monster level = area level (so map boss level = map tier).
- **Reincarnated trial bosses already have `damage_modifier` (per-class balance lever)** — they can be level-bound at season-generation level OR rescale at encounter. Open question.

**Genre consensus (community + dev commentary):**
- **Fixed-per-zone OR hybrid wins over full player-scaling** for sense of progression.
- D3's full scaling is *often cited as removing meaningful zone identity*.
- D4 hybrid is generally considered the modern best practice.

**Reincarnated implications:**
- B10's tier multipliers (swarm 0.10× → act-boss 10×+) are RELATIVE — they don't fix the absolute level baseline. The baseline-binding decision is the level-scaling philosophy itself.
- Reincarnated has **3 acts** (LOCKED 2026-05-11). Per-act level bands: A1: 1-17, A2: 18-33, A3: 34-50 (~17 levels per act).
- Trial bosses being class-converged opponents argues for level-bound at season-generation (their stats already reflect a specific level baseline; rescaling distorts the convergence work).
- B10's 10-12 room generated act has implicit per-level density tuning — if A1 = L1-10, the pack-size might be 5-8 swarms; if A5 = L41-50, the pack-size might be 10-15 swarms.

Sources: [D2 area levels per act](https://us.forums.blizzard.com/en/d2r/t/can-someone-please-explain-the-lvls-needed-per-area/38975) · [D3 RoS scaling](https://www.tentonhammer.com/guides/diablo-3-reaper-of-souls-difficulty-explained) · [D4 level scaling](https://game8.co/games/Diablo-4/archives/415872) · [PoE monster level](https://www.poewiki.net/wiki/Monster_level) · [LE Monolith](https://maxroll.gg/last-epoch/monolith/beginner-guide)

### 📚 Reference notes — Early/mid-game density patterns (2026-05-11 research)

**Prior research (file 32 Section 1-11 + file 28 B10) was endgame-focused** (~80-100 mobs/min, 70% trash, 5-12 mobs per pack). This subsection covers the early/mid bands explicitly. **Key insight: density delta from early to endgame is 6-10× — NOT 2-3× — so naive scaling from endgame numbers will under-deliver progression feel.**

**Kills/min across bands:**
- Early-game (Act 1): **~5-15 kills/min** in normal play (D2 Den of Evil ~3-5/min on first run; PoE Twilight Strand ~3-6/min; D4 Fractured Peaks WT1 sparse)
- Mid-game (Acts 2-3): **~15-40 kills/min** as packs grow and movement skills come online
- Endgame: ~80-120 kills/min (D2 Throne, PoE T16 juiced, D3 GR, D4 Helltides)
- **6-10× density delta from Act 1 to endgame** (much larger than typically assumed)

**Pack size scaling (genre median):**
| Phase | Pack size | Solo-trash fraction | Multi-pack overlap |
|---|---|---|---|
| Act 1 (L1-12) | **2-4 mobs** | ~30-40% solo | Rare (~5% chance) |
| Acts 2-3 (L13-30) | **3-6 mobs** | ~15-25% solo | Occasional (~15-25%) |
| Acts 4-5 (L31-50) | **5-12 mobs** | <10% solo | Normalized (~40-60%) |
| Endgame juiced | 5-15+ mobs | <5% solo | Default |

**The knee is at Act 3/4 boundary** — that's where "endgame density feel" begins.

**Trash/magic/elite ratio across bands:**
- Act 1 Normal: ~**90% trash / ~8% magic / ~2% elite** (D2 Tristram has 2 elite packs; PoE Act 1 has 1-3 rares per zone)
- Mid-game (Acts 2-3): ~80% trash / ~15% magic / ~5% elite
- Endgame (Acts 4-5 / juiced): ~**70% trash / ~20% magic / ~10% elite** (file 28 B10 target)

**Multi-pack overlap is the endgame-density-defining variable:**
- Below Act 3-4 (or pre-endgame in equivalent), packs read as **discrete and spatially separated**
- Endgame: 2-3+ distinct packs share a screen routinely (D3 GR, PoE juiced maps, D4 Helltides, D2 Hell A4+)
- Scale-up mostly via map mods (PoE), difficulty tier (D3), or area type (D4 Helltides) — NOT pack size growth alone
- **Tune multi-pack overlap probability from ~5% Act 1 → ~40-60% Act 5+** — single highest-impact per-band knob

**Time-to-kill stays roughly constant for trash:**
- Trash dies in **~1-3 hits across all phases** (this is THE design constant in genre)
- Elite TTK lengthens: 10-30s Act 1 → 30-60s endgame
- Elite HP scales faster than player damage to preserve "boss-feel" of elites across phases

**Movement/combat time fraction:**
- Act 1: **~50/50 combat-vs-movement** (lots of exploration/travel)
- Mid-game: ~65/35
- Endgame: **~80-95% combat** (PoE juiced maps near-continuous combat after >40% MS boots)
- This is why naive kills/min comparisons across bands mislead — multiply by combat-time fraction to get wall-clock kills/hour

**Mob archetype variety unlocks per act (genre baseline):**
- Act 1: **~12-20 distinct base archetypes** (tight industry convention)
- Act 3: ~30-40
- Act 5 / campaign end: ~70-120
- Per-act introduction rate: ~5-15 new archetypes
- Re-skins / elite versions multiply perceived variety

**Reincarnated multi-band sim tuning implications:**
- **Density delta is large (6-10×), not small.** If sim assumes near-constant density across bands and only varies HP/damage, will under-deliver progression. **Bake density growth (packs/min, pack size, multi-pack overlap probability) into the band tuning, not just stats.**
- **Pack size scales ~2-4× (Act 1 2-4 → endgame 5-12); multi-pack overlap is the real endgame multiplier** (5% → 40-60%). This is the single most impactful per-band knob.
- **Trash TTK near-constant; elite TTK is the lengthening variable.** Tune elite HP to grow faster than player damage across bands.
- **Movement-time fraction matters for comparing kills/min across bands.** Engine sim's "fights per minute" needs to factor in movement overhead per band (early game ~50% combat-time; endgame ~80%+).
- For Section 8 multi-band sim (α/β/γ choice): **per-band density tuning is a real architectural axis** — band-discrete (β) cleanly supports this; band-continuous (γ) needs sample-point density curves.

Sources: [D2 Tristram density](https://rankedboost.com/diablo-2/locations/tristram/) · [PoE Twilight Strand pack size](https://pathofexile.fandom.com/wiki/The_Twilight_Strand_(Act_1)) · [D2 Worldstone Keep elite density](https://maxroll.gg/d2/meta/worldstone-keep-and-baal-farming-guide) · [D3 elite mechanics](https://diablo-archive.fandom.com/wiki/Elite_Monsters) · [PoE map pack-size](https://www.pathofexile.com/forum/view-thread/1083536) · [D4 NMD vs Helltide density](https://us.forums.blizzard.com/en/d4/t/levelling-in-the-helltides-vs-nightmare-dungeons/167955) · [PoE Twilight Strand drowned packs](https://pathofexile.fandom.com/wiki/The_Twilight_Strand_(Act_1))

---

## Section 7 — Character-Enemy-Monster progression alignment

This section is the **validation layer** that ensures, for any character level N, the content the player faces is appropriately tuned. It's where Sections 2-6 cohere or fail.

### ✅ Decided
- **Endgame convergence:** balance loop converges classes at level 50 endgame state (B9 + existing balance loop).

### ⚠️ Thought through
- File 17 line 107: future state will use `*_DROPS_PER_SLOT` tier per phase; convergence at multiple bands.

### 🔴 Open
1. **What validation pass guarantees alignment?**
   - At endgame: gauntlet pass rate ~50% at level 50 with N=50 drops, max traits, full skill budget.
   - At mid-game (level 25): what's the pass criterion? What gear-N? What trait state? Same gauntlet shape or different?
   - At early-game (level 10): same question.
2. **What happens if a class converges at endgame but not mid-game?** Reject class for regeneration, or accept with mid-game weakness flagged?
3. **Class identity preservation across phases.** Does a fire mage feel like a fire mage at level 5? Or does the class only fully "express" at endgame? Genre split (D3: classes feel like themselves from level 1; PoE: identity emerges from build, takes mid-game to crystallize).
4. **Spirit Guide cross-phase awareness.** Does the build coach know the player is mid-game and recommend differently than at endgame?

### 📚 Reference notes (genre research)

**How genre flagships validate level-N alignment:**
- **D3 Greater Rifts as numerical balance benchmark.** Each GR tier = **+17% monster HP, +13.2% damage**. Community uses GR clear-tier as the standard build/level fit metric: fresh-70 build should clear ~GR 20; mid-Paragon GR 70-90; top builds GR 130+. Blizzard capped GR at 150 explicitly because endless tier-scaling was "not the healthiest approach."
- **PoE map tier balancing.** Tier 1-5 / 6-10 / 11-16 are the canonical low/mid/high bands. Each band has documented "sustain" thresholds for self-supply of maps. Top-tier maps roll mods lower-tier maps can't — so the balance gate is "which mods can coexist at this tier."
- **D3 RoS balance philosophy** (Wyatt Cheng public design talks): *"No build should be more than 2× better than the next."* Greater Rift leaderboards function as a LIVE balance signal — Blizzard buffs/nerfs sets to keep top-tier builds within ~10-tier band on GR ladder.
- **PoE league cycle as balance loop.** GGG ships a new league every 3 months. League mechanic + balance pass is intentionally a live experiment. Chris Wilson's GDC talk "Designing Path of Exile to Be Played Forever" describes seasons as the primary balance lever — meta shifts via league mods, not constant base-game patching.
- **D4 Pit Tiers (S13).** All Glyph/Paragon upgrades gated by Pit Tier completion — Pit becomes the canonical level-fit benchmark, similar to GR.

**Industry observation:**
- Mainstream ARPGs publicly document very little automated balance testing. The validation loop is **overwhelmingly leaderboards + community feedback + post-release patches** on a seasonal cadence. NONE of the major studios has publicly described a simulation pipeline that validates damage/survivability across level bands automatically.

**Reincarnated implications:**
- Reincarnated's convergence loop is **already more automated than anything the genre publishes** — running classes through a gauntlet at endgame and converging on 50% win rate is more rigorous than D3's "internal test characters" approach.
- Extending convergence to multi-band (Section 8 below) would put Reincarnated ahead of genre practice for *generation-time validation* — community planners (PoB, Maxroll planners) calculate damage at arbitrary levels but aren't part of dev QA. Reincarnated's engine + Spirit Guide already moves toward genuinely-integrated build validation.
- **Class identity preservation across phases is widely acknowledged as a hard problem** (forum/Reddit consensus across D3/D4/PoE: "your build won't come online until level X"). Most ARPGs accept mid-game balance debt. Reincarnated has the engine substrate to do better.

Sources: [D3 GR mechanics](https://www.purediablo.com/a-total-guide-to-greater-rifts) · [PoE GDC talk](https://www.gdcvault.com/play/1025784/Designing-Path-of-Exile-to) · [80.lv GDC PoE summary](https://80.lv/articles/gdc-designing-path-of-exile) · [PoE map](https://www.poewiki.net/wiki/Map) · [D4 Pit Tiers](https://d4gold.com/news/diablo-4-season-13-lord-of-hatred-ways-to-max-paragon-board-torment-10-difficulty)

---

## Section 8 — Engine simulation update for progression

This is the **engine architecture decision** that operationalizes Sections 2-7. Three options:

### ✅ Decided
- Engine currently converges at endgame-only (single 50% win-rate target against gauntlet).
- Convergence loop architecture is established (file 30 Stage 8).

### 🔴 Open → ✅ RESOLVED 2026-05-11

1. **Which option?** → **LOCKED: Option β (N-tier discrete convergence).** Section 1 anti-pattern lock already implied this; Section 8 confirms.

2. **Which bands?** → **LOCKED: 3 bands, act-aligned, sample at band-end:**
   - **Early band: L17** (Act 1 end)
   - **Mid band: L33** (Act 2 end)
   - **Late band: L50** (Act 3 end / endgame)
   - Represents "class is ready to advance to next act" at each sample point
   - Mid-act balance can flex; act-end is the gate

3. **Gear-percentile axis × band axis** → **LOCKED: endgame + mid-baseline (6 runs):**
   - L17 × {75th percentile gear} = 1 run
   - L33 × {75th percentile gear} = 1 run
   - L50 × {50th / 75th / 95th / 99th percentile gear} = 4 runs (B7 variance check at endgame only)
   - **Initial subtotal: 6 convergence runs per class** (kit + variance)
   - **+3 doppelganger validation runs added 2026-05-11 per Section 7 Q7.2** → final total **9 convergence runs per class** (kit composition + variance check + doppelganger validation)
   - Rationale: mid-bands need to PASS at baseline (75%) gear; extreme-gear pathology (B7) is fundamentally an endgame phenomenon

4. **Per-band gauntlet shape** → **LOCKED: per-band-generated gauntlet** (NOT same-gauntlet-scaled-stats). The early/mid/late density delta is 6-10×; same gauntlet with stat scaling won't capture it.
   - **Sub-clarification pending:** does "per-band-generated gauntlet" mean (a) same monster pool composed differently per band, or (b) per-band monster pools with band-specific archetype generation? See discussion below.

5. **Failure handling** → **LOCKED: recompose-at-band-specific-budget.**
   - Engine tries different per-band skill point distributions before falling back to damage_modifier
   - **The engine's "meta build" output becomes PER-BAND meta builds**, not just an endgame meta
   - If recomposition fails across all bands: regenerate class
   - Spirit Guide build coach recommends DIFFERENT distributions at different progression phases (consumes per-band optimal_distribution from export packet)

6. **Cost budget** → **LOCKED: ~30-45 min/season acceptable** (was ~3-5 min/season; ~9× increase after doppelganger validation addition).
   - **LLM cost impact: ZERO from sim work** (convergence is mechanical-only; no LLM calls in the loop)
   - **LLM cost impact from per-band gauntlets: depends on sub-clarification above** (interpretation (a) = zero LLM impact; (b) = ~3× monster generation cost ≈ +$1-2/season)
   - Per-class iteration during design: 30 min vs 5 min — tractable for "submit run, do something else, come back"
   - Per-season batch generation (~10 classes × 30 min = 5h compute) is trivial vs one-week-season cadence

7. **Telemetry packet** → **LOCKED: proposed structure adopted:**
   ```
   class.convergence_report = {
       'endgame_L50': { 'winrate': 0.50, 'iterations': 23, 'dimensions_explored': [...],
                         'optimal_distribution': {...} },
       'mid_band_L33': { 'winrate': 0.50, 'iterations': 18, 'optimal_distribution': {...} },
       'early_band_L17': { 'winrate': 0.50, 'iterations': 15, 'optimal_distribution': {...} },
       'variance_check_L50': { 'p50': 0.45, 'p75': 0.50, 'p95': 0.62, 'p99': 0.78 }
   }
   ```
   Spirit Guide consumes per-band `optimal_distribution` for cross-phase coaching.

### 🔴 → ✅ Sub-clarification RESOLVED 2026-05-11

**Per-band gauntlet interpretation: (b) Per-band monster pools.** Engine generates a SEPARATE monster pool per band (A1-flavored mobs, A2-flavored, A3-flavored). Matches genre pattern of new archetype introduction per act ("5-15 new archetypes per act" from research). LLM cost impact: ~3× monster generation per season (~+$1-2 / season). At total seasonal LLM budget of $5-10, this is modest.

**Implementation:** B10 + B14 generate monster pools per band; B14 multi-band convergence runs against the band-appropriate pool. File 28 B10 + B14 + file 31 stages need to reflect per-band monster pool generation.

### 📚 Reference notes (genre research)

**The published material on multi-level balance sim is SPARSE.** Cross-checking GDC Vault, Maxroll, IcyVeins, PoE Wiki, dev blogs: **no major ARPG team has publicly described a simulation pipeline that validates damage/survivability across level bands automatically.**

**What the major studios actually do (per public material + community accounts):**
- **GGG (PoE):** Chris Wilson's GDC talk describes balance methodology as (1) procedural generation + multiple overlapping random axes to make any single number less load-bearing, (2) seasonal league cycle as live experiment with explicit "we expect to nerf this" telegraphing. **No automated sim mentioned.**
- **Blizzard (D3):** Internal "test characters" at various Paragon levels run through canonical content; tuning passes target the median Paragon at season-end. **Manual playtesting, not simulation.**
- **Last Epoch / Grim Dawn:** smaller teams; balance is reported as iterative + community-feedback-driven.
- **Community-driven sim:** PoB (Path of Building), LE Build Planner, D4 Maxroll planner, D3 Maxroll. These calculate effective damage/EHP/clear speed at arbitrary level inputs — devs reference them implicitly but they're not part of official QA pipeline.

**Mid-game balance is widely acknowledged as the weakest band.**
- Forum/Reddit consensus across D3/D4/PoE: campaign band (levels ~20-50 in 100-cap games) gets least balance attention because endgame leaderboards generate the loudest signal.
- IcyVeins/Maxroll guides explicitly say *"your build won't come online until level X"* — devs accept mid-game balance debt.

**Implication for Reincarnated:**
- The genre does NOT have a turnkey methodology for validating mid-game balance.
- Building one (sim across N level bands, multiple builds, target time-to-kill envelope) would be **unusual but not contradictory to genre practice** — it would put Reincarnated ahead of mainstream ARPG QA pipelines for generation-time validation.
- Option α (endgame-only + scale-back) is essentially what D3 does manually with test characters.
- Option β (N-tier discrete) maps cleanly to D3 GR/D4 Pit/PoE map-tier band thinking — those games validate at discrete band breakpoints not continuously.
- Option γ (continuous scalar) has no genre precedent; would be a Reincarnated-distinctive choice that may or may not be worth the cost.

**Cost reality check:**
- Current convergence: ~3-5 min/season per file 30.
- Option β @ 3 bands: ~10-15 min/season — still well within "side project" envelope.
- Option γ @ 10 sample points: ~30-50 min/season — possibly painful for iteration speed but not impossible.

Sources: [PoE GDC talk](https://www.gdcvault.com/play/1025784/Designing-Path-of-Exile-to) · [80.lv GDC summary](https://80.lv/articles/gdc-designing-path-of-exile) · [Game progression theory](https://gamedesignskills.com/game-design/game-progression/) · [XP curve design](https://flavor365.com/the-ultimate-guide-to-xp-curves-leveling-systems/)

---

## Section 9 — Death penalty + regression mechanics

### Section 6 + 7 closures — locked 2026-05-11

**Section 6:**

- **Q6.1 Scaling philosophy** → **LOCKED: D2/PoE-style FIXED-PER-BAND** (implicit via per-band monster pools + per-band gauntlets). Monsters in A1 band have A1 stats and don't rescale when player overlevels. Genre-canonical; preserves zone identity.

- **Q6.2 Trial boss level binding** → **LOCKED: level-bound at season-generation; no rescaling at encounter time.**
  - A1 Trial boss = L17-band ilvl
  - A2 Trial boss = L33-band ilvl
  - A3 Trial boss = L50-band ilvl
  - Trial bosses are class-converged opponents — their stats reflect convergence work at specific band; rescaling distorts the convergence.

- **Q6.3 Doppelganger level binding** → **LOCKED: player level + slight handicap (+20% HP / +10% damage), MINIMUM-GATED at Trial boss bound level.**
  - Formula: `doppelganger_level = max(player_level, trial_boss_band_level)` then apply +20% HP / +10% damage handicap
  - **Prevents underlevel-rush exploit:** player who somehow reaches A1 Trial at L5 still faces an L17 doppelganger (not an easy L5 doppelganger)
  - **Overleveled players still face a true mirror:** L25 player at A1 Trial faces L25 doppelganger + handicap (mirror fights scale up appropriately)
  - Engine implementation: at Trial encounter, engine determines doppelganger level = max of player + band; emits doppelganger stats accordingly

**Section 7:**

- **Q7.1 Class identity preservation across phases** → **LOCKED: identity is a trajectory.** Class identity SHAPE (element distribution, kit composition rules from B6, trait pool from B9a) is preserved across bands even when not all skills accessible. Class identity at L17 = "fire mage with early kit"; at L50 = "fire mage with full keystones." Matches genre + locked shaped-balance design philosophy.

- **Q7.2 Doppelganger as alignment-validation tool** → **LOCKED: add to B14 validation passes.**
  - **+3 convergence runs total** (one per band × class-vs-its-doppelganger = 3)
  - New B14 total: 6 (kit composition + variance) + 3 (doppelganger mirror) = **9 convergence runs per class**
  - A class that can't reliably defeat its own doppelganger is unbalanced (too defense-heavy can't damage self; too damage-heavy can't survive self)
  - Provides genuine class-internal-balance validation; closes a hole that pure gauntlet-convergence doesn't catch
  - **Doppelganger level for VALIDATION pass:** matches band level (L17/L33/L50) since convergence happens at those points; runtime doppelganger uses the player-level + handicap + minimum-gating per Q6.3

- **Q7.3 Spirit Guide cross-phase coaching UX trigger** → **LOCKED: (b) + (c) combined + reset recommendation:**
  - **Act-transition surfacing:** "Welcome to Act 2 — Spirit Guide has a refined build recommendation for L18 band"
  - **Reset-trigger surfacing:** Spirit Guide shows per-band options at every reset moment (B9c)
  - **🆕 Auto-reset recommendation at act-transition:** if the band-meta build differs significantly from player's current build, Spirit Guide proactively recommends a FREE SKILL RESET to align — accelerating arrival at the new band's optimal distribution
    - Adds a NEW B9c reset trigger: "Spirit Guide proactive recommendation at act transition" (alongside existing struggling-heuristic / body-swap / end-game / refused-body-swap triggers)
    - "Significant divergence" heuristic: needs definition (e.g., >30% of allocated SP would need to relocate for the new meta) — engine-impl detail
    - **Player can decline the reset** — recommendation, not mandate
  - **Implication:** B9c's free-reset trigger set expands by one. File 28 B9c needs update.

---

### ✅ Decided (resolved via Section 1 — 2026-05-11)
- **Body-swap-offered with seasonal-death consequences** (Reincarnated-distinctive; no mainstream ARPG precedent).
- **No permadeath enforcement** for the SEASON (file 29 single-player); but body-swap-on-death IS effectively perma-death for that class within the season.
- **Build-reset triggers** include body-swap, refused body-swap, end-game completion (B9c).
- **Death body-swap distinct from Trial body-swap.** Trial = positive rewards (skill point + resistances + XP). Death = harsh consequences (class lost for season + cannot ascend).

### Death penalty model (Section 1 resolution; pool model corrected 2026-05-11)

Death pauses → player offered body-swap to a class from the season's remaining pool:

| Choice | Immediate consequence | Meta-progression consequence |
|---|---|---|
| **Refuse swap** | Normal respawn + small XP loss (~5-10% to next level) | None — class continues; can ascend to Earth realm at season end if survives to that point |
| **Accept swap** | Swap into chosen class from remaining pool | **Class permanently lost for current season** (cannot play again) AND **cannot ascend to Earth realm** (the dying spirit cannot enter form library) |

### Body-swap pool dynamics (CORRECTED 2026-05-11)

The body-swap target pool is **WITHIN-SEASON** — all engine-generated classes in the current season minus the starter, minus any classes already left behind via prior body-swaps.

- **Pool source:** engine generates ~8-9 classes per season (5-6 playable + 3 act-boss per file 29); pool starts as (N − 1) at season start
- **Pool shrinkage:** BOTH Trial body-swap AND Death body-swap remove the abandoned class from pool (pool −= 1 per event)
- **Doppelganger path (Trial refuse):** pool unchanged — staying as same class doesn't shrink anything
- **Form library is SEPARATE.** Library is cross-season accumulation of ascended spirits on Earth Self; library forms are NOT death-body-swap targets within a season

### ⚠️ Thought through
- Refusing death body-swap = "keep playing this class, accept tactical setback"
- Accepting death body-swap = "commit to a new form from within-season pool, lose this class forever for the season"
- The decision moment makes EVERY death meaningful — not just tactical setback, but a meta-progression choice
- **Pool depletion is a real strategic concern.** A player who Trial-body-swaps in all 3 acts AND dies twice has used 5 of ~8 pool slots — meaningful resource scarcity
- **First-time players ARE able to death-body-swap** (corrected from prior incorrect note) — the pool is within-season-generated, not cross-season library, so available from session 1

### 🔴 Open → ✅ Closures 2026-05-11
1. **XP loss percentage on refuse.** → **LOCKED: 5-10% to next level, no level loss.** Specific value (7.5% midpoint vs 5% vs 10%) to be finalized at engine-implementation time.
2. **Gear durability on death.** → **LOCKED: NO durability system.** Matches PoE/D2 simplicity. No gold-cost-to-repair, no item-breaking-at-0-durability.
3. **Death-during-Trial-boss-encounter.** → **LOCKED 2026-05-11:**
   - **Trial encounter resets on death.** Boss HP refreshes; player can re-attempt.
   - Death body-swap offered as normal (refuse-respawn or accept-swap with seasonal-death consequences).
   - **Trial path choice can be re-made on re-attempt:** if player chose body-swap path and died, they can switch to doppelganger path on retry (or vice versa).
   - **Trial body-swap opportunity persists** until Trial is completed — death doesn't burn the chance.
4. **Gold/currency drop on death.** → **LOCKED: NO gold/currency drop.** No corpse-run mechanic.
5. **Cross-season class persistence.** → **LOCKED:** lost FOR THE SEASON only (per Section 1 Answer 3). Other seasons regenerate fresh classes.
6. **Pool depletion edge cases (dying with 1 or 0 forms in pool).** → **LOCKED 2026-05-11:**
   - **Pool ≥ 2:** choice of multiple body-swap targets (current locked behavior)
   - **Pool = 1:** single-choice body-swap — player picks accept-that-one-form or refuse-respawn. No forced auto-swap. Player agency preserved.
   - **Pool = 0:** death body-swap UI unavailable. Only refuse-respawn remains. UI shows "No spirits available — only respawn remains." Player must keep current class until season end (or die-and-refuse).
   - **Trial body-swap NOT affected by pool depletion** — Trial boss class is a specific encounter; body-swap path always available; consuming it via Trial body-swap retroactively reduces pool by 1.

### 📚 Reference notes (genre research)

**Genre death-penalty patterns:**
- **D2:** XP loss + gold drop + corpse run.
  - Normal: no XP loss
  - Nightmare: lose 5% of XP needed for next level
  - Hell: lose 10%
  - You won't lose your current level
  - Recover corpse for 75% of lost XP back
  - Gold penalty: lose `min(character_level%, 20%)` of carried gold; ITEMS stay with corpse → actual corpse run required.
- **D3:** durability loss + gold cost to repair; hardcore = permadeath (character deletion).
- **D4:** **10 durability loss per death; gold repair; HC = permadeath only below L11, otherwise transfer to Eternal/softcore.** Items break at 0 durability (lose affixes).
- **PoE:** ~10% XP loss in maps (gear stays, no corpse run). Death in maps loses the map itself. Campaign A1-4: free or very small loss. Hardcore = move to Standard, no deletion. Omen of Amelioration reduces XP loss 75%.
- **Last Epoch:** zero penalty in regular softcore gameplay. Lose run rewards if you die in Monolith/Dungeon/Arena (lose the Echo/Dungeon entirely). Hardcore = character transferred to softcore.

**Hardcore patterns:**
- All major ARPGs (D2/D3/D4/PoE/LE) offer separate Hardcore mode.
- D2/PoE delete or banish to softcore.
- D4 deletes only below L11, otherwise transfers.

**No mainstream ARPG turns death into forward progression** the way Hades does.

**Hades-style rogue-lite hybrids in ARPG space are rare:**
- Curse of the Dead Gods, Hades, Dead Cells use death-as-progress.
- They're isometric action games, not loot-ARPGs.
- Loot-ARPGs commit to a single long character arc; rogue-lites commit to meta across many short runs.
- **Reincarnated occupies interesting middle ground** with body-swap as the meta-progression spine.

**Reincarnated implications:**
- The "death = forced body-swap" model would be **genre-novel** — no major ARPG does this.
- The "death = opt-in body-swap offered" model is closer to D4's Eternal-realm transfer (HC death → softcore character) and softer than D2's XP loss.
- A modest XP loss + gear stays + body-swap-offered approach would feel familiar to ARPG players while preserving the body-swap pillar.
- **There is no Hardcore-mode design dependency yet** — Reincarnated could ship without HC entirely (matches "solo, defined-end" framing) or add it post-launch.
- Trial boss death vs combat death distinction has no genre precedent — would be a Reincarnated-distinctive design choice.

Sources: [Maxroll D2 death](https://maxroll.gg/d2/resources/death) · [D2 death penalty](https://diablo.fandom.com/wiki/Death) · [D4 death penalty](https://mythicdrop.com/guide/diablo-4-death-penalty) · [D4 HC rules](https://game8.co/games/Diablo-4/archives/414517) · [PoE 2 death](https://gamerant.com/path-of-exile-2-death-penalty-what-happens-die-dying-effects-poe2/) · [LE death](https://upcomer.com/last-epoch-death-penalty-explained/)

---

## Section 10 — Per-act content scaling

### ✅ Decided
- **3 acts per game** (LOCKED 2026-05-11 per Matt's Section 11 answer — supersedes file 29's "4, 5, or 6" open question). B10 generates 10-12 rooms per act.
- **Per-act level bands (50 levels / 3 acts ≈ 17 levels per act):**
  - **Act 1: levels 1-17** (early game; ~50% combat / ~50% movement; pack size 2-4; ~5-15 kills/min)
  - **Act 2: levels 18-33** (mid game; ~65% combat; pack size 3-6; ~15-40 kills/min)
  - **Act 3: levels 34-50** (late/endgame; ~80%+ combat; pack size 5-12; ~80-120 kills/min)
- **1 Trial body-swap per act** = 3 Trial body-swap opportunities per season (Section 11 lock).
- **Act-bosses tuned outside the balance window** (file 22 / file 29 — specific tuning per act).
- **Quest completion in current act unlocks next** (file 29).
- **Per-act SP scaling (Trial body-swap):** 4 / 7 / 9 = 20 SP from milestones (proposed; awaiting confirmation per Section 11).

### ⚠️ Thought through
- Acts gate content (file 29).
- Act-bosses drop carried gear (file 22 demo1 plan — already partially proven).

### 🔴 Open
1. **Per-act level band.** Act 1 = levels 1-12? 1-10? 1-15? Genre convention varies.
2. **Per-act content density.** Is Act 4 just a "harder Act 1" with more monsters, or are mechanics layered (new ailments, new geometries, new monster archetypes unlock per act)?
3. **Side quests vs main quests.** Both grant XP/skill points? Different rates?
4. **Replayability per act.** Can player re-clear Act 1 for more XP / drops? Diminishing returns?
5. **Trial room per act.** Trial dungeons are "the boss gallery" (file 29 design intent). One per act? One mid-act?

### 📚 Reference notes (genre research)

**Per-act structure across the genre:**
- **D2 = 5 acts; each = new monster archetype + immunity profile.**
  - A1: mixed Demon/Undead/Animal — Fallen, Skeletons, Zombies
  - A2: predominantly Animals + Undead — mummies, scarabs, desert/tomb
  - A3: jungle/temple — Flayers, Council members, new ailments
  - A4: demon-heavy — Pandemonium Fortress
  - A5 (LoD expansion): barbarian highlands, frost-themed
  - **Each act introduces new monster archetypes + new immunity profiles that force gearing/skill adjustments** — this is the canonical per-act mechanical shift.
- **D3 = 5 acts; story + Adventure Mode.** New monster set + boss + biome per act. Adventure Mode bounties unify all 5 acts as level-scaled content post-campaign.
- **D4 = 6 acts + Prologue + Epilogue.** Acts 1-3 **open-order** across Fractured Peaks / Scosglen / Dry Steppes. Act 4 forced (mounts unlock here). Acts 5-6 in Hawezar/Kehjistan, more linear. Vessel of Hatred adds Nahantu region. **Branching non-linear act order is the major D4 innovation** vs prior Diablos.
- **PoE = 10 acts.** Each act introduces new mob set, new ailment/mechanic theming, plus a passive point and often a gem/refund quest reward. Acts 6-10 **re-walk acts 1-5 zones** with new mob levels and storyline (a structural choice that reduces unique-content burden).
- **Grim Dawn = 5 acts + 2 expansion acts (7 total).** Act 1 swamps (Aetherials), Act 2 ruins (Cronley's Gang + Aetherials), Act 3 Homestead (Chthonics introduced), Acts 4-5 broaden Chthonic threat, FG expansion = desert/Korvan acts. **Act = enemy-faction switch** (Aetherial → Chthonic → Eldritch) more than a level band.

**Canonical "Act N introduces..." pattern across the genre:**
1. New biome / visual identity
2. New monster archetype family (often with thematic immunity)
3. New boss
4. Sometimes a new mechanic (mount in D4 A4, ascendancy trial in PoE A3/6/10, mastery quest in LE Ch4)
5. Quest rewards that gate progression (skill point, passive point, stat point, life/resist bonus)

**Reincarnated implications:**
- **3 acts (LOCKED 2026-05-11 per Section 11 closures)** — below genre median (D2/D3 = 5; D4 = 6; PoE 10 outlier). Reflects deliberate shorter-arc design matching one-week-season cadence; per-act content density tuned to ~17-level bands.
- **The "new monster archetype family per act + thematic immunity" pattern is universal genre signal** — Reincarnated currently generates monsters per season; could layer "monster archetype groups intro'd per act" on top.
- **D4's non-linear A1-3 order is a recent design innovation** — Reincarnated's body-swap + seasonal rotation already builds non-linearity at the meta level; linear acts within a season is probably fine.
- **PoE's re-walk-acts-1-5 model** is worth knowing but probably not right for Reincarnated (one-week seasons argue for fresh content per act, not re-walk).
- Reincarnated trial rooms are "the boss gallery" — most natural placement is **one trial per act at the act-boss climax**, optionally one mid-act for pacing.
- Per-act level band mapping: 4 acts × ~12 levels/act = 1-12/13-25/26-37/38-50; or 5 acts × ~10 = 1-10/11-20/21-30/31-40/41-50; or 6 acts × ~8-9. Choice depends on Section 6's scaling philosophy.

Sources: [D2 monsters per act](https://diablo.fandom.com/wiki/Act_II_Bestiary) · [D2 monster archetype mix](http://blackjackrants.blogspot.com/2020/06/reviewing-monsters-diablo-ii-part-1.html) · [D4 acts](https://www.bulbaritos.com/diablo-4/diablo-4-acts) · [D4 non-linear design rationale](https://www.dexerto.com/diablo/exclusive-diablo-4-devs-explain-campaigns-new-structure-with-non-linear-acts-2158996/) · [Grim Dawn act 1](https://grimdawn.fandom.com/wiki/Act_1) · [Grim Dawn enemy factions](https://grimdawn.fandom.com/wiki/Aetherials)

### 📚 Reference notes — Per-act content pacing (2026-05-11 research)

**Time-to-complete per act across genre:**
- D2 full campaign: ~10 hrs casual / ~5 hrs rushed; Act 1 = ~1.5-2 hrs casual
- D4 Act 1 (Fractured Peaks): **~1.5 hours** — shortest act in the game
- PoE full campaign (Acts 1-10): **~6-10 hours** experienced; ~45-60 min per act average; speedrun A10 record 1:25:50 = ~8.5 min/act
- Grim Dawn Act 1 (Cairn): **~2.5-5 hours** (slowest in genre; intentional)
- Last Epoch: ~10-12 hours full campaign (10 chapters)

**For Reincarnated (one-week seasons, body-swap meta-progression):** target ~30-60 min per act for a full playthrough = ~3-5 hr season completion. Genre median.

**Mob archetype introduction pace per act:**
- **Act 1: ~12-20 distinct base archetypes** (tight industry convention across D2/D3/D4/PoE/LE/GD)
- Act 3: ~30-40 cumulative
- Act 5 / campaign end: ~70-120 cumulative
- **Per-act introduction: ~5-15 new archetypes** + elite/superunique re-skins multiplying perceived variety
- Reincarnated's procedural generator currently emits ~15-25 archetypes per season — sits at Act-1 variety. Cross-season rotation + body-swap form library effectively multiplies perceived diversity, but per-act archetype VARIETY within a single season is at the genre LOW end.

**Quest skill-point grants per act (cross-references Section 11):**
- D2: A1 +1 SP, A2 +1 SP, A4 +2 SP (per difficulty); ~25% of campaign budget by end of Act 1
- PoE: A1 = 2 passive, A2 = 3, A5 = 12 cumulative, A10 = 24 cumulative (Act 1 = ~8% of campaign quest passives)
- LE: 8 passive points from main campaign across chapters 1-9; ~12% by end of chapter 1
- D3/D4: no per-act quest skill grants; auto-unlock per level

**Early-game grant DELIBERATELY small (1-3 SP / ~5-15% of campaign quest total).** Power-feel in early acts comes from **base leveling + first gear drops**, NOT quest milestones. Counter-intuitive but universally followed.

**Reincarnated implications for per-act pacing:**
- Per-act time targets ~30-60 min × 3 acts = ~1.5-3 hr season (matches one-week-season design; locked 3-act structure)
- Per-act mob archetype introduction: ~5-10 new types per act (matches genre median); season generator can layer "archetype groups intro'd per act" on top of existing per-season pool
- Early-act skill point grants should be SMALL — most of the 20 quest skill points cluster around mid/late acts; this is counter-intuitive but matches every shipped ARPG. Recommended split (rough): A1 +1, A2 +2, A3 +4, A4 +5, A5 +8 = 20 cumulative
- **Front-load gear over quest milestones in early acts** — power-feel in Act 1 should come from boots / first legendary / first epic, not quest grants

Sources: [D2 how long](https://www.gamespew.com/2021/10/how-long-does-it-take-to-beat-diablo-2-resurrected/) · [D4 act length](https://www.gamespot.com/articles/how-long-to-beat-diablo-4-mission-list-and-how-many-acts-in-the-campaign/1100-6514620/) · [PoE leveling guide](https://www.playerauctions.com/path-of-exile-guide/leveling/poe-leveling-guide/) · [Grim Dawn Act 1 length](https://steamcommunity.com/app/219990/discussions/0/1483232961030998055/) · [PoE Act 1 monsters](https://pathofexile.fandom.com/wiki/Category:Act_1_monsters) · [PoE Act 2 monsters](https://pathofexile.fandom.com/wiki/Category:Act_2_monsters) · [LE passive quests](https://www.thegamer.com/last-epoch-every-main-side-quest-that-gives-passive-points/) · [PoE side quest passives](https://mobalytics.gg/poe/guides/side-quest-passive-points)

---

## Section 11 — Quest as XP / skill-point source

### ✅ Decided
- **20 skill points from quests/act-bosses/Trial-body-swaps** at endgame (B9b).
- **Quest chains tied to act progression** (file 29 — "what demo1 didn't validate").
- **Trial body-swap is the PRIMARY milestone source** (Section 1 resolution 2026-05-11). Each Trial body-swap grants: **XP + global resistances + skill point(s)**.
- **Per-act skill-point scaling:** early acts grant 1 SP per Trial body-swap; later acts grant more than one (specific scaling locked in this section).
- **Trial body-swap = "mini ascension"** with strictly positive rewards (vs death body-swap which has harsh consequences — see Section 9).

### ⚠️ Thought through
- Quest generation = Engine 2 territory (file 29).
- The 20-skill-point endgame target needs to be honored by Trial-body-swap design + secondary quest rewards.
- D2 pattern is the cleanest precedent: ~9-12 SP from key quests across 3 difficulties; Reincarnated consolidates this into one season at 20 SP total.
- Early-game research finding (2026-05-11): Act 1 grants should be **deliberately small** (~5-15% of campaign quest budget) — power-feel in early acts should come from base leveling + first gear, NOT quest milestones.

### 🔴 Open → ✅ Closures 2026-05-11 (some pending clarification)

1. **Trial body-swap count per act.** → **LOCKED: 1 per act × 3 acts = 3 Trial body-swap opportunities per season.**

2. **Skill point scaling per act.** → **LOCKED 2026-05-11: 4 / 7 / 9 = 20** across A1/A2/A3:
   - A1 (L1-17 band): +4 SP at Trial body-swap (early-game power-feel comes from gear, not SP)
   - A2 (L18-33 band): +7 SP at Trial body-swap (mid-game build crystallizes)
   - A3 (L34-50 band): +9 SP at Trial body-swap (late-game keystone unlocks)
   - **Total: 20 SP from milestones** ✓ (matches B9b budget)

3. **Global resistance scaling per Trial body-swap.** → **LOCKED 2026-05-11 (Option C — within-season cap with gear contribution):**
   - **Per Trial body-swap: +10%** all-element resistances (permanent within-season buff)
   - **Maximum from milestones: 3 trials × +10% = +30%** within a season (full body-swap path)
   - **Maximum from gear: +45%** must come from gear resistance affixes rolled across equipment loadout
   - **Within-season cap: +75% all-element resistances** (the standard ARPG endgame resist cap)
   - **No cross-season resistance accumulation** — each season starts at +0% baseline; form library carries class identity only, not accumulated stat state
   - **🔗 New gear-generation constraint** (Section 5 / file 17 / B5 / B12 scope): gear must be capable of rolling resistance affixes totaling ~+45% all-element across the equipment loadout. Matches PoE per-piece resistance rolling pattern. **Will be added to file 17 gear schema requirements + flagged in B5 + B12.**
   - **Refuse-Trial-body-swap (doppelganger path) gives half resistance reward** = +5% per Trial → +15% max from milestones if all Trials use doppelganger path; remaining +15% claimable via end-game quest to reach the +30% body-swap-equivalent ceiling

4. **XP grant per Trial body-swap.** → **LOCKED 2026-05-11 (framing locked; specific multipliers as starting tuning values):**

   **Framing: XP grant = % of XP-to-next-level at the band** (auto-scales with the polynomial XP curve locked in Section 2):

   | Band | Trial body-swap XP (full path) | Doppelganger XP (refuse, 1/4) | End-game quest reclaim (3/4) |
   |---|---|---|---|
   | A1 (L17) | +50% of XP-to-next-level | +12.5% | +37.5% |
   | A2 (L33) | +75% of XP-to-next-level | +18.75% | +56.25% |
   | A3 (L50) | +100% of XP-to-next-level (a full level) | +25% | +75% |

   **Total Trial-body-swap XP across season:** ~225% of XP-to-next-level (≈ 2.25 levels' worth, spread across 3 acts).

   **Doppelganger path total = same** (immediate 1/4 + end-game quest reclaim 3/4 combined).

   **Specific multipliers are starting values for engine-impl tuning.** Framing (% of XP-to-next-level) is the architectural lock; multipliers may shift during balance work.

5. **Non-Trial quest skill points.** → **LOCKED: Trial body-swap is the SOLE milestone-SP source** (Section 1 Answer 2 confirmation: "trial body-swap grant XP, global resistances and a skill point"). Reinforces body-swap pillar; matches D2's "few large quest rewards" model. Non-Trial quests grant XP-only.

6. **Refusing Trial body-swap consequences (doppelganger mechanic).** → **LOCKED 2026-05-11 (Option D — doppelganger fight as upfront choice):**

   **Trial encounter offers TWO paths chosen UPFRONT (before fighting):**

   | Path | Fight | Outcome on win | Reward |
   |---|---|---|---|
   | **Body-swap path** | LLM-generated Trial boss (a fresh class) | Transform into that class identity | Full XP + full SP (4/7/9 per act) + full resistances (+10%) |
   | **Doppelganger path** | Mirror of your current class (self-fight; "your doppelganger/shadow") | Stay as current class identity | 1/4 XP + half SP (2/3.5/4.5 per act) + half resistances (+5%); remaining claimable via end-game quest |

   - **Net pacing difference:** body-swap path = faster season completion (full rewards immediately + transformation); doppelganger path = needs end-game quest to fully catch up but preserves chosen class identity
   - **Engine cost minimal:** doppelganger fights reuse the class-as-Trial-boss machinery already in the engine — the doppelganger is just the player's current class deployed as a Trial-boss-tuned opponent
   - **"Adept body-swappers complete their season faster"** — convenience vs commitment tension, not "miss out" punishment
   - **Reincarnated-distinctive design pattern** — no genre precedent for this mirror-match Trial alternative

7. **Form library acquisition + body-swap pool model.** → **LOCKED + CORRECTED 2026-05-11:**

   **Body-swap pool (WITHIN-SEASON only):**
   - Engine generates ~8-9 classes per season (per file 29: 5-6 playable + 3 act-boss)
   - Pool of body-swap targets starts at (N − 1) = ~7-8 at season start (all generated classes minus the starter)
   - **BOTH Trial body-swap AND Death body-swap shrink the pool by 1** (the abandoned class is "left behind" and cannot be returned to)
   - Doppelganger path (Trial refuse) does NOT shrink the pool (player stays as same class)
   - Pool depletion is a real strategic concern — heavy body-swappers may run low on options
   - **First-time players have death-body-swap available** from session 1 (the pool is within-season-generated, not cross-season library)

   **Form library (CROSS-SEASON, separate concept):**
   - **Only ONE form ascends to Earth realm per season** — the form alive at season end (the one the player has been actively playing)
   - Trial bosses on doppelganger path are **lost for the season** — not added to form library
   - Death-body-swapped-from classes (the dying spirits) **cannot ascend**
   - Trial-body-swapped-from classes (left-behind classes) are also **not ascended** (you've moved on; they're abandoned)
   - **Library is slow-accumulating:** at most 1 form per season; over N seasons of play, library size ≤ N
   - **Library purpose:** see "Earth Self meta-layer" framing below

   **Strategic tension:** "play one class to mastery and ascend that" vs "body-swap for power gains but ascend a less-mastered form" — same as before, now clarified that body-swap-for-power has REAL pool-depletion cost on top of the ascend-trade-off.

### Earth Self meta-layer framing (added 2026-05-11; far-future implementation)

**Reincarnated as currently scoped (Phase 0) = the SEASONAL JOURNEY portion of a larger eventual game.**

The eventual full gameplay loop introduces an **Earth meta-layer** as the player's persistent home:

- **Earth Self** = the player's persistent identity that lives on Earth (the meta-layer hub; not in current development)
- **Seasonal journey = descent.** Earth Self body-swaps into a seasonal spirit form for a time-bound seasonal journey — this is the current Reincarnated ARPG scope
- **Ascension = return.** The goal of each seasonal journey is to ascend the most meaningful life back to Earth as a Spirit form
- **Form library = accumulated ascended spirits** on Earth Self — described as "a truly novel gacha-style accumulation of uniquely LLM-generated ascended spirits"
- **Earth-layer events** (eventual feature; not Phase 0): PVP and PVE guild events, usually in **the rift** (liminal space between Earth and Seasonal realms), defending against monsters "not of either Earth or the Seasonal realm" (third-faction enemies)
- **Earth gameplay loop:** TBD — possibly MOBA, Pokemon Battles, Arena Style, or other combinations. A truly distinct mode from the seasonal ARPG.

**Implication for current scope:**
- Phase 0 builds the SEASONAL JOURNEY only (solo ARPG)
- Form library accumulation works during Phase 0 (one spirit per season ascends) but the LIBRARY ITSELF doesn't have a gameplay use until the Earth meta-layer ships
- Multiplayer scope clarification: out of scope for SEASONAL play indefinitely; envisioned for Earth meta-layer events post-Phase 0
- **Full vision captured in `../collaboration-handoff/34-earth-meta-layer.md`** (separate design doc — to be drafted)

8. **Failure modes.** Player takes doppelganger path in every Trial — under-skilled for later acts? Section 7 (alignment validation) cross-reference. Note: doppelganger path is NOT trivially weaker than body-swap path — same XP/SP/resistance TOTAL via end-game quest; just delayed pacing. So "under-skilled" risk is moderate, not severe.

### 📚 Reference notes (genre research)

**Quest-as-progression-currency across the genre:**

| Game | Quest skill / stat budget | Mechanism |
|---|---|---|
| **D2** | **12 SP + 15 stat across 3 difficulties** | 3 quests grant SP (Den of Evil A1 +1, Radament A2 +1, Fallen Angel A4 +2); 1 quest grants stat (Lam Esen's Tome A3 +5). Plus permanent life/resist bonuses. |
| **PoE** | **23-24 passive points + 20 refund points** | ~20% of total passive budget. Refund points are quest-only; can't farm from drops. Specific examples: A Dirty Job (+2 refund), Through Sacred Ground (+2 refund). |
| **D4** | **10 SP via Renown** (quest-adjacent) | Renown from waypoints, side quests, dungeons, strongholds. 5 regions × 2 SP at Tiers 1+3 = 10. Plus Paragon points + Murmuring Obol capacity. Account-wide. |
| **D3** | **0 (outlier)** | No quest skill points. Campaign quest XP exists Normal/NM/Hell, vanishes at L60. D3 simply doesn't have player-spent skill/stat points. |
| **Grim Dawn** | **50-55 Devotion from shrines** (quest-adjacent) | Restore shrines + sometimes defeat guardian → Devotion point. Separate from XP-driven skill points. |
| **Last Epoch** | **Mastery + idol slots from chapter quests** | Mastery quest Ch4 unlocks mastery tree (permanent). Idol slots from campaign chapter completions. Modest. |

**Almost every ARPG grants XP from quests.** Games that grant SKILL POINTS specifically: D2 (12), PoE (23-24 + 20 refund), D4 (10 via Renown), GD (50 Devotion).

**D2 model = cleanest precedent for Reincarnated's "20 from quests/bosses":**
- Small absolute number of quests
- Each grants a MEANINGFUL permanent bonus
- Quest XP separate (and large, especially at low level)
- Permanent buffs layered on top (life, resists)

**PoE's "quest refund points" is a separate idea worth knowing:** quest-only respec currency. This could pair with B9c's "strict during play" reset model — refund points become an in-play minor-reset currency that doesn't break the strict-during-play discipline.

**Reincarnated implications:**
- 20 skill points from quests/bosses is in the same ballpark as D2 (12) and D4 (10) — closer to PoE (23 + 20) — but interpretation matters.
- Pure-quest model (D2-style, ~5 quests × 4 SP each, or similar) keeps grants meaningful and player-noticeable.
- Pure-boss model (4 act-bosses × 5 SP each = 20) ties progression to climactic moments.
- Hybrid (act-bosses give bulk, scattered side quests give small grants) matches Reincarnated's seasonal generation rhythm.
- 20 SP from quests vs 100 from levels = 17% — well below PoE's 20% and similar to D2's 12-out-of-110 (~11%).
- **The Engine 2 quest generation system needs to honor whatever this section decides** as a hard contract.

Sources: [D2R complete quest rewards](https://www.rpgstash.com/blog/d2r-quests-skill-stat-life-resist-bonus) · [Maxroll D2 quests](https://maxroll.gg/d2/resources/important-quests) · [PoE side quest passive points](https://mobalytics.gg/poe/guides/side-quest-passive-points) · [PoE skill point quest list](http://www.vhpg.com/poe-skill-point-quests/) · [D4 Renown SP](https://www.icy-veins.com/d4/guides/renown/) · [Grim Dawn devotion](https://grimdawn.fandom.com/wiki/Devotion)

---

## Section 12 — Movement speed and mobility (added 2026-05-11)

The progression layer affects what speed-running looks like at endgame. This section captures movement-speed philosophy, the boots gear slot gap, and class-based movement abilities.

### ✅ Decided (2026-05-11 design conversation)
- **Movement speed is NOT stat-driven.** STR/DEX/INT/WIS/VIT/AGI do not affect base movement speed. AGI is currently dead/reserved (decisions-log 2026-05-09) — should NOT be revived for movement speed.
- **All classes can speed run at endgame.** Base movement speed is class-agnostic; speed-gear-driven progression is uniform across archetypes.
- **Boots is a gear slot.** Primary gear slot for movement speed affix. (Currently missing from gear schema per file 17 — see open item below.)
- **Boots have a decent chance to roll a movement speed affix** as a primary modifier.

### ⚠️ Thought through
- Current Reincarnated state: engine emits no `movement_speed` field; demo synthesizes from `range_profile` via `movement.ts:speedForProfile` (close-range faster than long-range). This is demo-side stat-by-proxy and contradicts the "all classes speed run at endgame" goal — must be removed when engine emits proper `movement_speed`.
- File 17's current gear schema is missing several slots that ARPGs uniformly include: **boots, gloves, belt** (and arguably amulet/ring counts — most ARPGs have 2 rings). The boots gap is the immediate driver, but a complete gear slot audit is needed.
- Class movement abilities (whirlwind, dash_attack, leap_strike) are already scoped in B11 — these layer mobility on top of base speed, matching genre pattern (Sprint/Vault/Charge/Whirling Blades).

### 🔴 Open → mostly resolved via B12 lock; minor implementation-tuning items remain

1. **Hard cap on gear-sourced movement speed.** → **LOCKED: +25% hard cap from gear** (matches D3/D4; preserves balance). Tuning of specific affix bands per gear tier deferred to engine impl.

2. **Boots affix bands per gear tier.** Genre median: common boots +5-10%, rare +10-15%, epic +15-20%, legendary +20-25% movement speed roll. Should Reincarnated follow this gradient? And should every boots roll have movement speed, or is it one possible affix among others?

3. **Base movement speed value.** Engine needs to emit this. Genre: ~5-7 m/s base in D3/D4. Reincarnated: needs a value. Demo currently uses different values per range_profile (close: 240px/s, medium: 200px/s, long: 160px/s per `movement.ts:speedForProfile`) — these need to **collapse to a single base value** per engine work.

4. **Monster movement speed.** Genre: most monsters slightly slower than player base; some "fast" monster types (Quill Rats in D2, Fallen Imp in D3) faster. Boss/elite usually slower (compensated by ranged or AOE attacks). **Engine should emit `movement_speed` per monster tier** alongside HP/damage scaling.

5. **Mobility flask / consumable analog.** PoE's Quicksilver Flask gives +40% speed for 5s — a build-defining mobility tool. Should Reincarnated have an equivalent consumable, or only gear + movement skills?

6. **Per-class movement abilities.** B11 already scopes whirlwind/dash_attack/leap_strike. Are these the ONLY mobility skills, or should every class have at least one mobility option (D4-Evade-style universal short-dash)?

7. **Slow / chill / root interaction with movement speed.** Currently ailments slow movement (per file 28 B2 § ailment design). Should these be % multipliers on player's actual speed (so high-MS boots resist slows better) or flat reductions? Genre split — D3 multiplicative; D2 partly additive.

### 📚 Reference notes (genre research)

**Movement speed source across genre:**
- **D2:** +%FRW on boots/belts/helms; running drains stamina; sorceress slightly faster base; movement skills (Teleport, Leap, Charge, Vigor aura).
- **D3:** **+% Movement Speed cap = +25% from gear**; boots ~12% typical roll; class movement skills (Sprint, Vault, Tempest Rush, Furious Charge).
- **D4:** Standardized base; **boots primary +10-25% MS roll**; **hard cap +25% from gear**; universal Evade button (spacebar dash for everyone); mounts in open world post-Act 4.
- **PoE:** Standardized base; boots +10-30% MS; Quicksilver Flask (+40% / 5s consumable); class movement skills (Shield Charge, Whirling Blades, Flame Dash, Leap Slam, Lightning Warp).
- **Last Epoch:** Standardized base; boots primary MS; per-class movement abilities.

**Genre consensus (5/5 games):**
1. Base speed is class-agnostic (decoupled from class identity)
2. Boots are THE primary gear slot for movement speed
3. Hard cap +25% from gear is the D3/D4 standard
4. Stats are never the source of movement speed in modern ARPGs
5. Class movement skills layer on top

**Reincarnated implications:**
- The user's design directive ("all classes speed run at endgame; no stat-based speed; boots primary source") is **100% genre-canonical** — no friction with established patterns.
- Adding boots + gloves + belt (the three missing slots) brings Reincarnated's gear slot count from ~7 to ~10, in line with D3/D4.
- Engine queue item B12 (movement speed + boots gear slot + slot audit) — ships in Stage A3 alongside B10/B11 as ARPG-feel infrastructure work.

Sources: [D3 movement speed cap](https://maxroll.gg/d3/resources/d3-stats-explained) · [D4 movement speed](https://d4.cc/movement-speed-stat-cap-percentage-soft-cap-hard-cap/) · [PoE boots](https://www.poewiki.net/wiki/Boots) · [D2 FRW](https://diablo.fandom.com/wiki/Faster_Run/Walk)

---

## Section 12.5 — Active mobility, evasion, telegraphs, emergent archetypes (added 2026-05-11)

This section extends Section 12 with **active mobility / defensive evasion** as a distinct sub-system. Where Section 12 covers BASE movement speed (gear-driven; class-agnostic), Section 12.5 covers ACTIVE evasion abilities (class-generated; per-archetype) plus the substrate required to make them meaningful (telegraphs + i-frames).

### ✅ Decided (2026-05-11 design conversation)

- **Last Epoch model adopted — per-class movement abilities** (NOT D4 universal Evade). The procedural generator picks mobility abilities like every other ability — archetype-appropriate, emerges from generation rather than hardcoded.
- **NO guaranteed mobility per class.** The generator picks freely. Some classes will have mobility; some won't. This is intentional — preserves the emergence-driven design thesis.
- **Engine archetype-emergence observability required.** Engine must surface kit-mobility-presence in telemetry/export so we can monitor which archetype clusters emerge across seasons. Novel constructs (dodge-tank, kiting-mage, berserker-skirmisher) should be detectable from convergence outputs without manual inspection.
- **Statistical evasion (`DODGE_CHANCE_CAP = 0.60`) stays as-is.** Active evasion layers on top, not replaces.

### ⚠️ Thought through

- Two flavors of evasion exist independently: **statistical** (dodge chance roll; already in engine) and **active/positional** (move out of hitbox; needs substrate).
- For active evasion to be meaningful: skills need **telegraphs** (windup before damage applies, player sees hitbox), **i-frames** (untargetable window during evasion), and **active mobility geometries** in the generator pool.
- B11 motion geometries are all OFFENSIVE (whirlwind, dash_attack, leap_strike — damage while moving). B13 adds the missing DEFENSIVE category (roll, defensive_dash, strafe_mode, blink, dodge_stance — mobility without damage).
- This is mostly demo-side work, not engine sim. Engine emits metadata (cast_time, i_frame_window, geometry); demo resolves positional hitboxes + i-frame respect.

### 🔴 Open → architectural items resolved via B13; tuning details remain for engine impl

1. **Specific evasion geometry roster.** → **LOCKED: 5 geometries** (`roll`, `defensive_dash`, `strafe_mode`, `blink`, `dodge_stance`). Additions like `parry` or `phase_shift` parked as post-B13 extension if playtest demand surfaces. **STAY OPEN; B13-proper at Stage A2 closeout** — the 5-geometry roster is a B13-proper deliverable as *kit-pool additions on top of the universal dodge floor* (per L3 narrow-slice decision 2026-05-17; see amendment below). The narrow slice ships the universal dodge mechanic only; the 5 mobility geometries layer on later as per-class kit additions.
2. **i-frame duration ranges.** → **LOCKED for narrow slice (2026-05-17):** universal dodge i-frame window 0.4s default; substrate numerical asymmetry for earth (~0.45s, shorter distance ~3m) and wind (~0.4s, longer distance ~5m); all other substrates 0.4s/4m. Per gandalf L3 briefing § 2.2. Rationale: minimum substrate-coupling that honors cosmological commitments (earth refuses to move; wind moves things best) without making dodge a balance-sensitive system. Per-skill mobility-ability i-frames remain a B13-proper question.
3. **Cast time on player abilities.** → **LOCKED for narrow slice (2026-05-17): NO player-AOE telegraph in solo play.** Player AOEs do NOT telegraph; player kit self-discipline is enforced via cooldown not visual telegraph. Per gandalf L3 briefing § 3.6. Multiplayer (out of scope per `project_design_intent.md`) would re-evaluate. Player-AOE indicators DO show post-cast for ~0.3s at 0.92× hitbox (visual feedback only; no escape window from own AOE).
4. **Telegraph indicator shape vs hitbox.** → **LOCKED for narrow slice (2026-05-17):** indicator geometry mirrors AOE hit-region exactly (existing geometry-painter reuse). Enemy indicator scaling 1.08× hitbox (dodges feel narrow); player post-cast indicator 0.92× hitbox (generous edges, no windup). Per gandalf L3 briefing § 3.3 + existing post-B11 lock. Rocket schema fields landing per `2026-05-17-rocket-narrow-slice-engine-schema-fields.md` dispatch (`windup_duration_seconds` + `indicator_color_hex` per substrate).
5. **Mobility role-tagging in generator.** **STAY OPEN; B13-proper at Stage A2 closeout** — narrow slice ships universal dodge mechanic but does NOT introduce mobility-as-kit-role taxonomy; that lives with the 5-geometry kit-pool additions in B13-proper.
6. **Archetype-emergence reporting cadence.** → **LOCKED for narrow slice (2026-05-17): per-substrate windup table** per gandalf L3 briefing § 3.2 (fire 0.8-1.2s escalating; water 1.0-1.5s filling; earth 0.4-0.7s instant+persistent; wind 0.5-0.8s directional; lightning 0.0-0.2s first-arc + 0.4-0.6s chain; holy 1.5-2.0s radiant; shadow 0.3-0.5s late-commit). Cadence values consumed via `windup_duration_seconds` schema field (rocket dispatch). Archetype-emergence telemetry surfacing remains a B13-proper question.

---

### 🟢 Amendment 2026-05-17 — Narrow-slice Phase-1 P1 extension (L3 binding decision)

**Source:** gandalf L3 briefing `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` (tag `gandalf/v1.2-dodge-and-telegraphed-combat-l3-briefing-1` @ `3ec108f`); Matt standing delegation; PARTIAL Phase-1 P1 extension chosen per § 7 recommendation.

**What landed in the narrow slice (folded into Phase-1 P1 as Deliverable 28):**

- Universal player dodge mechanic (Shift-key; ~0.4s i-frame; ~4m distance; 4-5s shared cooldown; substrate-VFX-coupled animation per briefing § 2.2; substrate numerical asymmetry for earth/wind only)
- Enemy-AOE ground-indicator system (per-substrate windup character per briefing § 3.2; `windup_duration_seconds` + `indicator_color_hex` schema fields per rocket dispatch)
- Elite-tier reactive escape AI (perpendicular-escape on visible player-AOE indicator with 50-70% probability; gamora narrow-slice work)
- Player AOEs DO NOT telegraph (solo-play discipline; post-cast 0.3s indicator at 0.92× for feedback only)
- Indicator geometry mirrors AOE hitbox exactly (geometry-painter reuse)

**What stays open for B13-proper (Stage A2 closeout per `canonical/16-project-roadmap.md`):**

- 5 defensive mobility geometries as kit-pool additions (`roll` / `defensive_dash` / `strafe_mode` / `blink` / `dodge_stance`) — items #1 above
- Mobility role-tagging in the generator — item #5 above
- Mini-boss + boss strategic / anticipatory / substrate-coherent escape AI (per briefing § 4.3)
- Archetype-emergence observability (kit-mobility composition per-class per-season telemetry)
- Future trait-pool extension surface for windup-modulating / escape-modulating traits (per briefing § 3.4; Phase-1 P2 or B13-proper)

**B13 scope reduction:** narrow slice covers ~25% of original B13 scope; remaining B13 estimate ~2.5-3 weeks at Stage A2 closeout (down from 3-4 weeks per `canonical/16a-roadmap-shipped-log.md` line 86). See `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b" for the amended B13 scope.

**Why the narrow slice exists:** the D27 perception test was at risk of false-negatives without a spatial-combat substrate (per briefing § 1.3). The narrow slice is the *minimum-viable* substrate that lets substrate-identity-declarations (per `canonical/story/substrate-identity-declarations-2026-05-17.md`) be perceptually distinguishable in 90-second fights. Full B13 polish (richness for the shipped game) stays in its existing post-VS2a slot.

### 📚 Reference notes (genre research)

**Per-class movement model across genre:**
- **D4 universal Evade:** every class has a spacebar dash (~6m, ~5s CD). Universal mobility floor; cannot be designed around.
- **Last Epoch per-class:** Mages get Teleport variants; Rogues get Shift; Sentinels get Lunge. Each class has 1-2 mobility skills in their tree. Generator-friendly because mobility is part of the class kit pool.
- **PoE skill gem socketing:** mobility skills are gems (Flame Dash, Shield Charge, Whirling Blades, Leap Slam, Lightning Warp, Dash in PoE 2). Any class can socket any gem; the meta has class-by-class favorites due to stat scaling.
- **D2 per-class:** Sorceress Teleport, Barbarian Leap, Paladin Charge, Assassin Burst of Speed, Necromancer no native mobility (notoriously slow). Per-class is the default genre model historically.
- **D3 mixed:** every class has a movement skill in their hotbar (Sprint/Vault/Tempest Rush/Furious Charge/Strafe), AND can use mobility legendaries. Hybrid model.

**i-frame patterns in genre:**
- **Roll abilities (Dark Souls / Elden Ring lineage):** ~0.4s i-frames standard. Roll-and-attack chains common.
- **Dash abilities (D3/D4):** ~0.2s i-frames typical. Vault in D3 has ~0.3s.
- **Phase/Blink (PoE Whirling Blades):** functional i-frames (~0.1-0.2s) during animation; not full invulnerability but hitbox is offset.
- **Stance buffs (D3 Smoke Screen):** 1-2s untargetable; very strong, gated by CD/resource.

**Telegraph patterns in genre:**
- **Boss telegraphs:** universal across genre. Cast bar + ground indicator + 0.5-2s windup. D3/D4 ground patches glow before damage; PoE bosses have animation tells.
- **Trash mob telegraphs:** D3/D4 some; PoE less; D2 minimal. The denser the mob count, the less individual telegraphing (would clutter screen). Trade-off: telegraphs scale inversely with density.
- **Player-side telegraphs:** rare in single-player ARPGs (player knows their own abilities); more common in multiplayer.

**Emergent archetype discovery in procedural ARPGs:**
- **No mainstream precedent.** D3 / D4 / PoE classes are hand-designed. Last Epoch classes hand-designed. None procedurally generate classes and then DISCOVER emergent archetype clusters.
- **This is a Reincarnated-distinctive observability requirement.** Surfacing "this season produced 3 dodge-tank style classes that nobody designed for" is genuinely novel design feedback.

**Reincarnated implications:**
- Last Epoch model fits Reincarnated's procedural generation thesis without modification.
- 5 defensive mobility geometries proposed (roll, defensive_dash, strafe_mode, blink, dodge_stance) — vs 3 offensive in B11 (whirlwind, dash_attack, leap_strike) — gives the generator a meaningful pool to draw from.
- Telegraphs + i-frames + 5 new geometries bundled as **B13** queue item (file 28). Ships Stage A3 alongside B6/B7/B10/B11/B12.
- **Archetype-emergence observability** is the Reincarnated-distinctive piece — the engine should surface kit-mobility composition per-class per-season so we can detect novel constructs. Adds to B13 scope.

Sources: [LE skill specialization](https://maxroll.gg/last-epoch/resources/passives-and-skills) · [PoE movement skills](https://www.poewiki.net/wiki/List_of_movement_skill_gems) · [D4 Evade design](https://www.icy-veins.com/d4/guides/evade-mechanic/) · [D3 mobility skills tier list](https://www.icy-veins.com/d3/movement-skills) · [Dark Souls i-frames](https://soulsplanner.com/darksouls3/iframes)

---

## Section 13 — React-or-auto interaction primitive + healing-cooldown mechanic (added 2026-05-17)

**Source:** gandalf DoE feel-target doc `canonical/story/mobile-feel-target-doe-2026-05-17.md` (§§ 5.3, 5.4, 7.1, 7.2, 7.6). Matt L3 lock 2026-05-17 evening: "Yes, if A makes portrait primary that works" — Path A doc-cascade (this dispatch) locks the design contract; engine-side refactor deferred to VS2b (`agentic_orchestration/dispatches/2026-05-17-gandalf-doe-doc-cascade-path-a-portrait-primary.md`).

This section is the canonical home for two related design primitives surfaced by the Dungeon of Exile play-session reference: (a) **react-or-auto** affordances for environmental interactions, and (b) the **single cooldown-gated heal** that replaces the inventoried potion stack. Both apply on PC and mobile (consistency lock).

### § 13.1 — Healing: cooldown-gated ability (retires the potion-inventory mechanic)

**Decision (LOCKED 2026-05-17):** Reincarnated does not use a potion-inventory mechanic. Healing is a single ability on a global cooldown, surfaced as one button on PC (default key `Q`) and one bottom-right button on mobile. There is no stack count, no "potion of greater healing vs lesser healing" inventory, no shop-purchased restock. The same primitive ships on both platforms.

**Genre alignment:** DoE/Diablo Immortal converged on this on mobile because input-frequency cost made inventory potion management hostile to combat flow; PC-side, D3/D4 retain stack-based health pots but already gate them by Healing Potion CD (~30s in D3, ~30s ramping in D4). Reincarnated collapses the gate-and-stack pair into a single cooldown-only affordance — closer to D4's evolution and explicitly genre-canonical for mobile-first design.

**Baseline values (tunable; gear/trait modifiable per Section 5 + canonical-17 § 13 amendment):**

| Parameter | Baseline | Notes |
|---|---|---|
| `heal_cooldown_seconds` | **10.0s** | Center of the 8-12s band per DoE feel-target § 7.2. Tunable via gear/trait. |
| `heal_magnitude_pct_max_hp` | **35%** | Restores 35% of max HP per cast. Significant but not single-cast full-heal; player still positions and dodges. |
| `heal_floor_hp_flat` | **+50 HP** | Minimum-restore safety floor for low-max-HP early-game characters. |
| `heal_cast_time_seconds` | **0.0s** | Instant on cast; no animation lock. |
| `heal_invuln_window_seconds` | **0.0s baseline** | No invulnerability granted by default. (Affix `heal_secondary_effect = "brief_invuln"` can add 1.0-2.0s; see canonical-17 amendment.) |
| `heal_consumes_resource` | **No** | Heal does not drain mana / energy / stamina; it is its own gated resource (the cooldown is the cost). |

**Mana / energy mechanic survives unchanged.** The substrate-energy resource model (per dimensional refactor + Section 4) is independent of the heal mechanic. Mana remains spend-as-you-cast for skills; the heal cooldown is parallel infrastructure.

**Inventory-slot impact.** Slots that would have held potion stacks are freed for build-crafting consumables (e.g., future buff scrolls, identification reagents, town-portal-equivalents if any) or are simply not surfaced as a UI affordance. Per § 5 Q5.9, inventory is already a Spirit-Guide-curated rare-or-better surface; removing potions reduces inventory's combat-time relevance further (DoE-validated: inventory is a between-combat inspect surface, not a during-combat surface — see § 13.3 below).

**Engine-side execution (deferred to VS2b).** The engine refactor (`STAMINA_POTION_USE` → cooldown-gated `heal_ability` in `combatant.py`) is out of scope for this dispatch — see Knight-rider VS2b sequencing. Cross-references: gamora + star-lord + rocket execute post-D11.

**CC interaction — heals BLOCKED during stun / freeze / silence (LOCKED 2026-05-17; Matt L3 verdict #121):**

`heal_ability` is blocked during stun, freeze, and silence states (and any future CC ailment satisfying "actor cannot take voluntary action"). The heal is suppressed — not queued, not partial, not delayed — and the cooldown does not advance during the CC window. When the CC ends, the heal cooldown state is unchanged from when CC was applied: a heal that was ready before CC fires remains ready; a heal on cooldown resumes its timer from where it paused.

Cross-reference: `canonical/17-gear-and-spirit-guide-design.md` § "Heal-cooldown affix family — CC interaction" (affix-layer mirror of this rule); `reincarnated-engine/design/decisions/decisions-log.md` entry "2026-05-17: Heal blocked by CC ailments — #121 verdict" (full rationale, alternative considered, seam obligations).

### § 13.2 — React-or-auto interaction primitive (new design primitive)

**Decision (LOCKED 2026-05-17):** Every battlefield environmental interaction (chests, doors, levers, NPC dialogue triggers, shrine activations, lore-glyph readings) follows the **react-or-auto** primitive. The interaction surfaces as a pop-up affordance when the player enters its activation radius. If the player taps/clicks within the `auto_complete_window`, the activation is treated as intentional; if the window expires without input, the game auto-completes the interaction on the player's behalf.

**Baseline values (tunable per interaction type):**

| Parameter | Baseline | Notes |
|---|---|---|
| `auto_complete_window_seconds` | **1.2s** | Centroid of the 0.8-1.5s band per DoE feel-target § 5.3. Long enough to react during combat; short enough to keep flow when the player chooses to ignore. |
| `affordance_visual` | hand-icon + ring | A pop-up icon (DoE-canonical "hand/finger button" per Matt's paragraph) overlaid on the interaction target. Affordance ring visible at activation-radius edge. |
| `intentional_tap_priority` | wins ties | If `auto_complete_window` is mid-countdown and the player taps the affordance, the tap is treated as intentional (no double-fire). |
| `auto_complete_idempotent` | true | Auto-completion must produce identical world-state effects to a manual tap. No "missed it" penalty. |
| `combat-state-suppression` | optional per interaction | Some interactions may be suppressed entirely when the player is `combat_active` (e.g., shrines), to avoid mid-fight auto-completion of high-commitment activations. Per-interaction config. |

**Applies to:**

- Treasure chests (small / medium / large / strongbox)
- Doors (passable doors, locked doors with key-bearer state, story-gated doors)
- Levers / pressure plates (single-state activations; not repeatedly-tappable mechanisms)
- NPC dialogue triggers in hub / non-combat zones
- Shrine activations (with `combat-state-suppression = true` recommended; player should intentionally invoke a shrine, not auto-fire one while running past in a fight)
- Lore-glyph readings (low-stakes; auto-complete safely surfaces the lore text in the floating-text channel)

**Does NOT apply to:**

- **Combat skill activations** — skills are tap-only; never auto-cast. (Auto-attack is separate infrastructure per § 5.5 / combat-loop pattern; auto-attack is not a react-or-auto skill.)
- **Loot equip** — the "tap red-dot character portrait to equip" affordance is its own pattern (DoE § 4.3) and does NOT auto-fire. Equip is an intentional player decision; the Spirit Guide's marginal-value gate already filters down to upgrades-only, but the final tap is always intentional. (Rationale: silent auto-equip would surprise the player; the red-dot is opt-in.)
- **High-stakes one-way activations** — e.g., entering a trial-room from a hub-side portal. The player intentionally enters; no auto-complete on proximity.
- **Substrate / element activations during combat** — any interaction that triggers a substrate event (e.g., shadow-substrate altar) requires intentional tap to preserve archetype-emergence telemetry attribution.

**Design rationale (player-experience).** The primitive reduces decision fatigue in dense combat: the player should not have to break combat focus to tap a chest icon during a fight; the chest opens for them. It preserves agency by giving the player a window to intentionally engage; nothing happens without the player at least walking past it. The pattern is mature ARPG mobile canon (DoE, Diablo Immortal, Torchlight Infinite) and lifts cleanly to PC (the keybind / click-during-window pattern is symmetrical).

**Genre alignment.** DoE: chest auto-opens after ~1.0-1.5s if not tapped. Diablo Immortal: shrine + lever interactions are tap-only (no auto-complete) — Reincarnated is going *further* than DI in adopting react-or-auto as a generalized primitive. PoE and PC-era Diablo: pure tap-only (legacy keyboard/mouse era). Reincarnated's adoption of react-or-auto on PC is intentional and forward-leaning; it is also low-risk because intentional tap always wins (no behavior loss).

### § 13.3 — Inventory-as-between-combat (clarification, not new lock)

This section captures a clarification of the Stage A3 demo-follow-on inventory model (Section 5 Q5.9) in light of the DoE reference: inventory is **inspect-and-equip**, not active management. Modal contents prioritize equipped-gear visualization, comparison-pane, affix/set-bonus detail, loadout-swap shortcut. Inventory-grid sorting / management is secondary.

Cross-reference: `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 4.4 + § 7.3.

### § 13.4 — Mobile orientation: portrait-primary, landscape-secondary

**Decision (LOCKED 2026-05-17):** Mobile target is **portrait-primary**. Landscape is supported as a secondary / polish-phase orientation, not a v1 requirement. PC orientation is unchanged (landscape canvas remains the desktop target).

**Why portrait.** The DoE reference is portrait-only; the cluster (Diablo Immortal, Torchlight Infinite, Eternium, Dungeon Hunter 6, Anima ARPG) is portrait-primary or portrait-only. One-handed thumb-reach ergonomics, App Store / Play Store discovery patterns, and notification-overlay coexistence all favor portrait. The HUD-layout consequences (HP-bar top-attached-to-minimap, heal button bottom-right, skill arc bottom-center) are derived in `canonical/story/mobile-feel-target-doe-2026-05-17.md` § 2 + `canonical/story/mobile-ux-execution-plan-2026-05-17.md` § 4.2 (portrait-amended; see Amendment 3 of this dispatch).

**Cross-reference:** Section 7 (combat-UI sparseness) and § 13.1-13.2 above apply identically across orientations; the orientation lock affects HUD layout, not interaction primitives.

### 📚 Reference notes (genre research)

- **DoE (Dungeon of Exile):** portrait-only; cooldown-gated single heal button; react-or-auto chests + environmental interactions; auto-attack handles most damage output. Reference: `canonical/story/mobile-feel-target-doe-2026-05-17.md` (Matt's 15-minute play-session capture + screenshot).
- **Diablo Immortal:** portrait-primary (landscape supported on tablet); single heal potion on ~30s CD with stack count (3 charges) — partially-stacked but cooldown-gated; chest interactions are tap-only.
- **Diablo III / IV (PC + console):** Healing Potion on ~30s CD with stack count (1-3 charges); chest interactions tap-only; no react-or-auto primitive.
- **PoE 1 / 2:** Flask system (5 flasks, charge-recovery via kills; not cooldown-gated in the same way). Reincarnated deliberately diverges from the flask paradigm — flasks are a build-crafting surface in PoE; Reincarnated's heal is a survival floor, not a build-crafting surface (build-crafting expression lives in skills + traits + gear, per Sections 4-5).
- **Last Epoch:** Health potion on cooldown with charge recovery from kills (hybrid model). Could be a future Reincarnated direction if a "earn-your-heal" feedback loop becomes desirable, but the baseline is the pure-cooldown DoE model.

---

## Cross-section integration — the unified progression vector

By the end of this discussion, we should be able to write down, for any character level N:

```
At level N, a player has:
  - X stat points allocated (per Section 3 model)
  - Y skill points allocated (per Section 4 budget × pacing)
  - Z traits unlocked at appropriate ranks (per Section 4 acquisition)
  - Gear: equipped distribution at N(level) drops per slot (per Section 5)
  - Faces: monsters at level-band(N) with tier composition (per Section 6)
  - Convergence-validated: pass rate at N matches design target (per Section 8)
  - Death-state: ... (per Section 9)
```

This unified vector is what file 33 (companion empty skeleton) captures the structure for.

---

## Decision sequencing recommendation

These sections need to be discussed in dependency order. Roughly:

1. **Section 1 (philosophy)** first — determines XP vs milestone vs hybrid; everything else hangs from this
2. **Section 8 (sim architecture)** next — determines whether design needs to specify mid-game state or only endgame + scale-back
3. **Sections 2-4 (character / stats / abilities)** next — the player-facing progression mechanics
4. **Sections 5-6 (gear / enemies)** next — the content-facing scaling
5. **Section 7 (alignment)** as cross-check
6. **Sections 9-11** as detail rounds

Each section's decisions land in file 33 as they firm up.

## How to use this doc

- Read TL;DR first
- Read Section 1 before any other section
- Section by section: read the three buckets (Decided / Thought through / Open), engage with the open questions, decisions land in file 33
- Reference notes (genre research) live at the bottom of each section — consulted as evidence, not authority
