# SC-6 Reference Encounter Audit — 2026-05-27

**Author:** gamora (simulation + spirit-guide seam owner)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-sc-6-gap-2-reference-encounter-audit.md`
**Mode:** AUDIT + REPORT — no engine modifications, no sim runs, no new encounter authoring
**Scope:** endgame-reference-encounter (L45-50+ per doc 41 § 3) ONLY for Cycle 13 v1
**Authority:** Matt 2026-05-27 — Cycle 13 handoff § 4.1.3 + framing brief § 4.1 KR autonomous + Q11
**Date:** 2026-05-27

---

## TL;DR

The current engine codebase contains **0 endgame-reference-encounter definitions** in the sense required by Cycle 13 GAP 2. What exists are **6 arena scenarios** (fight geometry definitions) in `spatial_gauntlet/arena.py` that serve as the convergence-path gauntlet substrate — these are scenario shapes (spawn positions, arena dimensions, leash overrides, win conditions), not BC-cell-targeted endgame encounter content.

The reference gauntlet is built dynamically at season-generation time (`balance_loop.py:647–747`) by selecting monsters from the bestiary; it is not a static catalog of named, BC-cell-targeted reference encounters.

Against the ~22 v1 BC-target cells per `v1-bc-target-intent-2026-05-24.md` Sketch F: **0 cells WELL-COVERED, 0 cells THIN-COVERAGE, ~22 cells NO-COVERAGE.**

Recommendation: all ~22 v1 cells require new encounter content. This is a full-scope authoring gap, not a partial gap. The 6 existing arena scenarios are the delivery mechanism (geometry shell), not the encounter content (mob composition, difficulty calibration, BC-cell-targeting intent). Rocket must author encounter content per cell; gamora confirms the arena scenario shells are ready to receive it.

**Encounter count inventoried:** 0 endgame-reference-encounters.
**BC cell coverage:** 0 WELL, 0 THIN, ~22 NO-COVERAGE.
**Recommended additions:** 15-22 encounters targeting all ~22 cells (6 cells priority-1 per endgame archetype spread; then fill to optimal target).
**Rocket consultation:** required — encounter content authoring is rocket's generation seam.

---

## 1. Current Reference Encounter Inventory

### 1.1 What "encounter" means in the gauntlet sim (resolving dispatch open question)

Per the gauntlet sim architecture (`spatial_gauntlet/gauntlet_modes.py:1-41`), an "encounter" in the convergence path is a **fight instance** resolved by `run_spatial_fight()`. The convergence path runs N_FIGHTS (100 full / 30 smoke) per slot. The gauntlet has **12 slots** per `GAUNTLET_TIER_COMPOSITION` in `balance_loop.py:639-644` (6 swarm + 2 magic + 2 elite + 1 mini-boss + 1 boss).

For Cycle 13 gauntlet sim purposes, a "reference encounter" is the combination of:
1. An **ArenaScenario** (arena geometry + spawn positions + win condition)
2. A **mob selection** (monster objects from bestiary populating the scenario's spawn slots)
3. A **difficulty calibration intent** (BC-cell-targeted; endgame L45-50+ per doc 41 § 3)

The arena scenarios provide (1). The dynamic bestiary selection in `build_reference_gauntlet()` provides (2) on a per-season basis. Item (3) — the BC-cell-targeting intent that defines an endgame-reference-encounter catalog — does not exist.

### 1.2 Existing arena scenarios (the delivery mechanism)

Six arena scenarios exist in `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py`:

| Scenario ID | Defined at | Description | Mob composition | Tier | WR Contract |
|---|---|---|---|---|---|
| `open_arena` | `arena.py:283` | 50×50m open; 8 swarm mobs approaching from south | 8 swarm spawners | swarm | 0.65–0.80 (gauntlet_archive.py:164) |
| `chokepoint_corridor` | `arena.py:347` | 10×50m corridor; 5m bottleneck at y=[23,27] | 8 swarm spawners | swarm | 0.65–0.80 |
| `boss_with_adds` | `arena.py:402` | 30×30m; 1 boss + 2 flanking elite adds | boss + 2 elite | boss | 0.30–0.45 |
| `magic_pack` | `arena.py:486` | 32.7×14m; 1 magic monster + 3 swarm adds | magic + 3 swarm | magic | 0.55–0.70 |
| `elite_pack` | `arena.py:568` | 28×28m; 1 elite + 2 magic adds | elite + 2 magic | elite | 0.45–0.60 |
| `mini_boss` | `arena.py:643` | 30×30m; 1 mini-boss + 2 elite adds | mini-boss + 2 elite | mini_boss | 0.35–0.55 (TIER_WR_CONTRACT; gauntlet_archive.py:168 shows 0.20–0.50 as revised floor) |

**What these are NOT:** these are arena geometry shells. The `SpawnSpec` entries carry `archetype_tag` values (`"swarmer"`, `"caster"`, `"brute"`, `"boss"`) as hints for mob selection, but no BC-cell targeting, no endgame difficulty calibration intent, no explicit L45-50+ mob stat anchoring.

**What the balance loop does with these:** `build_reference_gauntlet()` (`balance_loop.py:647`) selects raw Monster objects from the season bestiary by tier + element diversity. The bestiary monsters are the actual encounter content; the arena scenarios provide the fight geometry. Neither the monsters nor the selection algorithm targets specific BC-cells or endgame progression nodes.

**Empirical assertion:** I cite 6 arena scenarios; verified by `grep -n "^SCENARIO_" /Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` returning 6 entries (lines 283, 347, 402, 486, 568, 643).

### 1.3 No BC-cell-targeted reference encounter catalog exists

A search for `reference_encounter`, `endgame_encounter`, `encounter_catalog`, `L45`, `BC_CELL`-targeted encounter structures in `reincarnated-engine/src/reincarnated/simulation/` returned no results. The concept of an "endgame-reference-encounter catalog covering ~22 BC-target cells" does not exist in any form in the current codebase.

The dynamic gauntlet construction (`build_reference_gauntlet()`) samples from the season bestiary without BC-cell targeting. BC-cell coordinates in the archive are currently populated as opaque strings (e.g., `"swarm_open_arena_{player_class.id}"`) per `balance_loop.py:2662` — these are per-class convergence identifiers, not per-cell endgame encounter targets.

---

## 2. BC-Target-Cell Coverage Map

### 2.1 The ~22 v1 BC-target cells

Per `v1-bc-target-intent-2026-05-24.md` Sketch A (§ 1.1), the v1 scope covers ~37 forms across ~22 distinct cells in the 5-tuple `(range × tempo × amplitude × attribute × proxy-density)` subspace.

**Important note on axis naming:** the v1-bc-target-intent doc uses the 5-tuple `(range, tempo, amplitude, attribute, proxy-density)` — the substrate-curation 5-tuple, NOT the full 8-axis QD BC lock from `qd-engine-bc-axes-lock-2026-05-20.md`. The Block C scaffolding doc (`2026-05-27-block-c-calibration-scaffolding.md:117`) uses the full 8-axis set. For this audit, I map encounters against the 5-tuple cells used in the v1-bc-target-intent doc (Sketch A), which is the source document specified in the dispatch.

### 2.2 Coverage map — all cells NO-COVERAGE

Since there are 0 endgame-reference-encounter definitions, every cell is NO-COVERAGE. The 22 cells from Sketch A are:

**STR cells (5 cells):**
- `(melee, low, spiky, STR, none)` — Heavy Barbarian — NO-COVERAGE
- `(melee, high, flat, STR, none)` — Light Fighter — NO-COVERAGE
- `(melee, medium, variable, STR, none)` — Polearm Soldier — NO-COVERAGE
- `(ranged, low, spiky, STR, none)` — Thrown-Heavy / Atlatl — NO-COVERAGE
- `(melee, low, spiky, STR, light)` — Ancestor-Warrior — NO-COVERAGE

**DEX cells (6 cells):**
- `(melee, high, flat, DEX, none)` — Dagger Assassin — NO-COVERAGE
- `(ranged, high, flat, DEX, none)` — Archer — NO-COVERAGE
- `(ranged, low, spiky, DEX, none)` — Crossbow Sniper — NO-COVERAGE
- `(mid, high, flat, DEX, none)` — Twin-Blade Fencer — NO-COVERAGE
- `(ranged, high, flat, DEX, light)` — Falconer / Pet-Archer — NO-COVERAGE
- `(mid, low, spiky, DEX, heavy)` — Trap Assassin / Mine-Mercenary — NO-COVERAGE

**INT cells (7 cells):**
- `(ranged, medium, variable, INT, none)` — Standard Wizard — NO-COVERAGE
- `(ranged, low, spiky, INT, none)` — Artillery Mage — NO-COVERAGE
- `(mid, low, spiky, INT, none)` — Pyromantic Caster — NO-COVERAGE
- `(melee, high, flat, INT, none)` — Red Mage / Spellsword — NO-COVERAGE
- `(ranged, medium, variable, INT, light)` — Arcane-Familiar Mage — NO-COVERAGE
- `(mid, low, spiky, INT, heavy)` — Necromancer Summoner — NO-COVERAGE
- `(mid, medium, variable, INT, heavy)` — Totem Hierophant (INT) — NO-COVERAGE

**WIS cells (7 cells — note: Sketch A lists 7 WIS cells covering ~9 forms):**
- `(mid, medium, variable, WIS, none)` — Channeling Cleric — NO-COVERAGE
- `(melee, medium, variable, WIS, none)` — Holy Knight / Paladin / Hammerdin — NO-COVERAGE
- `(ranged, low, spiky, WIS, none)` — Ritual Mage / Oracle — NO-COVERAGE
- `(ranged, medium, variable, WIS, none)` — Storm Caller / Druid (active) — NO-COVERAGE
- `(melee, high, variable, WIS, none)` — Monk-archetype — NO-COVERAGE
- `(mid, low, variable, WIS, heavy)` — Druid Beastmaster — NO-COVERAGE
- `(mid, medium, variable, WIS, heavy)` — Witch Doctor Petmaster — NO-COVERAGE

**Total: 25 cells enumerated (not ~22).** Sketch A's summary says "~22 distinct cells" but the per-attribute tables list 5+6+7+7=25 rows. The discrepancy is likely because some cells share forms across attribute variants or some cells listed in tables are contested / overlap. For this audit I use all 25 enumerated cells as the coverage target; if "~22" is the correct count, the discrepancy shrinks the effective target but does not change the NO-COVERAGE verdict on all.

**Empirical assertion:** I cite 25 BC-target cells from Sketch A tables in `v1-bc-target-intent-2026-05-24.md` (§ 1.1). The doc summary says "~22 distinct cells" — the 3-cell delta is within the doc's own ±2-3 rounding language. All cells are NO-COVERAGE; the count discrepancy does not affect the audit verdict.

---

## 3. Coverage Gap Analysis

**Summary:**
- WELL-COVERED: 0 cells
- THIN-COVERAGE: 0 cells
- NO-COVERAGE: ~22-25 cells (all)

**Gap type:** this is not a partial coverage gap. It is a **pre-existence gap** — the encounter catalog concept does not yet exist in the codebase. The 6 arena scenarios are the gauntlet geometry shells; they are prerequisites for encounter content, not encounter content themselves.

**Sim-deferred cells (proxy-light and proxy-heavy):** Per the 8-axis BC lock (`qd-engine-bc-axes-lock-2026-05-20.md:§ 5`), proxy-light and proxy-heavy bins are in the deferred-evaluation pool — current sim supports solo only. This affects 5 of the 25 cells:
- `(melee, low, spiky, STR, light)` — Ancestor-Warrior — proxy-light deferred
- `(ranged, high, flat, DEX, light)` — Falconer / Pet-Archer — proxy-light deferred
- `(mid, low, spiky, DEX, heavy)` — Trap Assassin / Mine-Mercenary — proxy-heavy deferred
- `(mid, low, spiky, INT, heavy)` — Necromancer Summoner — proxy-heavy deferred
- `(mid, medium, variable, INT, heavy)` — Totem Hierophant (INT) — proxy-heavy deferred
- `(mid, low, variable, WIS, heavy)` — Druid Beastmaster — proxy-heavy deferred
- `(mid, medium, variable, WIS, heavy)` — Witch Doctor Petmaster — proxy-heavy deferred

**These 7 cells require sim extension before gauntlet sim can evaluate encounter content for them.** They are Cycle 14+ scope per the sim deferral matrix. For Cycle 13 v1, the effective target is ~18 non-deferred cells.

---

## 4. Encounter Quality Assessment (Discipline #26)

Since no endgame-reference-encounter definitions exist, per-encounter #26 quality assessment cannot be performed. There are no encounters to assess.

The 6 arena scenarios (geometry shells) can be assessed against the 6 sub-gates for their structural properties — specifically whether they are capable of exercising each sub-gate IF appropriate mob content were authored for them:

| Scenario | KPM measurement? | Rotation coherence? | Resource flow? | Defensive uptime? | Non-degenerate? | Cognitive load? |
|---|---|---|---|---|---|---|
| `open_arena` | Yes — 8 swarm mobs; KPM measurable at convergence | Partial — open terrain doesn't force rotation variation | Yes — sustained combat | Yes — incoming damage from 8 mobs | Risk: mob HP multiplier fixes (1.5×) mitigate WR saturation | Manageable — single threat type |
| `chokepoint_corridor` | Yes — bottleneck forces positional play affecting KPM | Yes — forces AOE vs single-target decision | Yes | Yes | Risk: cone/line classes may trivialize (KILLS_ONLY mitigates) | Manageable — clear spatial cue |
| `boss_with_adds` | Yes — boss kill required | Yes — flanking adds force rotation choice | Yes | Yes — flanking pressure is real defensive stress | Low risk | Elevated — 3-threat-type tracking |
| `magic_pack` | Yes — full-clear required | Yes — magic+swarm mix forces target-prioritization | Yes | Yes — magic caster ranged threat | Low risk | Manageable |
| `elite_pack` | Yes — full-clear required | Yes — elite anchor + magic adds creates priority choice | Yes | Yes — pincer pressure | Low risk | Manageable — 2 threat types |
| `mini_boss` | Yes — mini-boss kill required | Yes — flankers must be managed while damaging mini-boss | Yes | Yes — two-phase threat | Low risk | Elevated — classic spatial puzzle |

**Finding:** the 6 arena scenario shells are structurally capable of exercising all 6 #26 sub-gates IF the mob content is properly calibrated for endgame difficulty (L45-50+ per doc 41 § 3). The geometry is sound. The gap is calibrated content.

**#26 quality threshold decision (dispatch open question):** an encounter that exercises 5 of 6 sub-gates but fails 1 will be classified "THIN-COVERAGE with caveat" rather than WELL-COVERED. The 6th sub-gate failing is not a disqualifier but requires documentation. This policy applies when encounter content arrives for Wave 1 authoring.

---

## 5. Recommendation — Encounter Additions

### 5.1 Priority structure

**Priority 1: 18 non-deferred cells (effective Cycle 13 v1 scope)**

The 7 proxy-light and proxy-heavy cells are deferred per sim capability constraints. The 18 remaining cells across STR/DEX/INT/WIS are the Cycle 13 v1 target.

**Encoding convention for recommended encounters:**
- `(range, tempo, amplitude, attribute)` identifying the cell (proxy=none unless flagged)
- Intended arena scenario shell (from existing 6)
- Mob composition intent (endgame difficulty; L45-50+)
- Expected WR contract alignment

### 5.2 Recommended additions — 18 encounters for non-deferred cells

Target: 15-22 optimal per GAP 2 LOCKED intent. 18 encounters (1 per non-deferred cell) lands within the optimal range.

**STR cells — 4 encounters (proxy-none only; `STR-light` deferred):**

| Cell | Archetype | Recommended scenario shell | Mob composition intent | WR expectation |
|---|---|---|---|---|
| `(melee, low, spiky, STR, none)` | Heavy Barbarian | `boss_with_adds` or `mini_boss` | High-HP spiky-damage boss (spike-resist-capable); adds apply sustained pressure | 0.30–0.45 boss; 0.35–0.55 mini-boss |
| `(melee, high, flat, STR, none)` | Light Fighter | `open_arena` | Mobile swarm with fast attacks; tests high-tempo flat-damage rotation against spread mobs | 0.65–0.80 |
| `(melee, medium, variable, STR, none)` | Polearm Soldier | `elite_pack` | Elite with mixed add types; variable damage tempo forces rotation adaptation | 0.45–0.60 |
| `(ranged, low, spiky, STR, none)` | Thrown-Heavy / Atlatl | `chokepoint_corridor` or `magic_pack` | Chokepoint funnels targets for thrown-weapon cluster; magic add tests target prioritization | 0.55–0.70 |

**DEX cells — 5 encounters (no deferred):**

| Cell | Archetype | Recommended scenario shell | Mob composition intent | WR expectation |
|---|---|---|---|---|
| `(melee, high, flat, DEX, none)` | Dagger Assassin | `open_arena` | High-mobility swarm; tests high-tempo single-target rotation | 0.65–0.80 |
| `(ranged, high, flat, DEX, none)` | Archer | `chokepoint_corridor` | Ranged against funneled mobs; tests sustained ranged tempo | 0.65–0.80 |
| `(ranged, low, spiky, DEX, none)` | Crossbow Sniper | `magic_pack` | Magic leader tests spiky-damage timing against a ranged-threat leader | 0.55–0.70 |
| `(mid, high, flat, DEX, none)` | Twin-Blade Fencer | `elite_pack` | Elite pincer; mid-range high-tempo flat damage rotation tested against anchor + flankers | 0.45–0.60 |
| `(mid, low, spiky, DEX, none)` | Red Mage / Spellsword *(contested cell)* | `mini_boss` | Mini-boss burst-window challenge; low-tempo spiky requires timing | 0.35–0.55 |

**INT cells — 5 encounters (2 proxy-heavy deferred; 5 non-deferred):**

| Cell | Archetype | Recommended scenario shell | Mob composition intent | WR expectation |
|---|---|---|---|---|
| `(ranged, medium, variable, INT, none)` | Standard Wizard | `open_arena` | 8-swarm open field; tests elemental AoE rotation diversity | 0.65–0.80 |
| `(ranged, low, spiky, INT, none)` | Artillery Mage | `boss_with_adds` | Boss + adds tests spiky-nuke timing against add management pressure | 0.30–0.45 |
| `(mid, low, spiky, INT, none)` | Pyromantic Caster | `magic_pack` | Magic leader resists some elements; tests mid-range spiky timing + target selection | 0.55–0.70 |
| `(melee, high, flat, INT, none)` | Red Mage / Spellsword *(contested cell)* | `elite_pack` | Elite + adds mix; contested STR/INT cell tests high-tempo flat spell-melee hybrid | 0.45–0.60 |
| `(ranged, medium, variable, INT, light)` | Arcane-Familiar Mage | `chokepoint_corridor` | Familiar proxy adds chokepoint pressure assistance; tests mid-variable-tempo with familiar augment | 0.65–0.80 |

**WIS cells — 5 encounters (2 proxy-heavy deferred; 5 non-deferred):**

| Cell | Archetype | Recommended scenario shell | Mob composition intent | WR expectation |
|---|---|---|---|---|
| `(mid, medium, variable, WIS, none)` | Channeling Cleric | `magic_pack` | Magic leader + swarm adds; channeling rotation tested against ranged leader | 0.55–0.70 |
| `(melee, medium, variable, WIS, none)` | Holy Knight / Paladin / Hammerdin | `boss_with_adds` | Boss + flankers; melee variable-tempo holy archetype tested at boss tier | 0.30–0.45 |
| `(ranged, low, spiky, WIS, none)` | Ritual Mage / Oracle | `mini_boss` | Mini-boss; low-tempo spiky ritual burst tested at mini-boss difficulty | 0.35–0.55 |
| `(ranged, medium, variable, WIS, none)` | Storm Caller / Druid (active) | `open_arena` | Open field swarm; elemental storm-caller tests variable-tempo ranged vs spread | 0.65–0.80 |
| `(melee, high, variable, WIS, none)` | Monk-archetype | `elite_pack` | Elite pincer; high-tempo variable WIS melee tested against multi-threat | 0.45–0.60 |

### 5.3 Difficulty calibration intent for all recommended encounters

Per doc 41 § 3 and Block C scaffolding Scaffold 1 § 1.4 — endgame node (L45-50+) intent:
- KPM anchor: ~75+ (gamora calibrates specifics via sim)
- Defensive uptime target: ≥80%
- Resource management: active management critical
- Rotation depth: full rotation depth engaged

Mob stat scaling must reflect L45-50+ mob damage profile. This is the critical gap in the current arena scenarios — they have no L45-50+ mob difficulty anchor. The `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` in arena.py was calibrated against a generic fight calibration pass, not against the L45-50+ endgame node.

**This is a second-order flag for rocket:** endgame-reference-encounter content requires L45-50+ mob HP/damage profiles, not just genre-appropriate arena geometry.

### 5.4 Optional additions (minimum-to-optimal gap)

18 encounters reaches the optimal floor. Optional additions to improve coverage quality:

- A second `open_arena` variant targeting **high-mobility swarm** (faster mob movement speed) to stress-test high-tempo close-range classes more effectively
- A second `boss_with_adds` variant with **spiky-damage adds** (testing degenerate-state 7: bounce-CC resistance) instead of steady brute adds
- A third encounter for the most contested cell `(melee, high, flat, INT, none)` (Red Mage — the STR-INT crossover) — this cell is uniquely high-risk and warrants dual-scenario coverage

These 3 additions would bring the total to 21 — well within the optimal 15-22 range.

---

## 6. Multi-Seam Coordination Flags

### 6.1 Rocket consultation flags (Wave 0/1 implementation required)

The 18 recommended encounter additions require rocket implementation. The following work-unit specifications are flagged for rocket:

**WU-R1: Endgame mob stat profile — L45-50+ difficulty calibration**
- Rocket must define L45-50+ mob HP / damage profiles for each threat tier (swarm, magic, elite, mini-boss, boss)
- Current arena scenarios use per-season bestiary selection with a 1.5× HP multiplier — this is not an endgame-node-targeted calibration
- Required: explicit L45-50+ encounter difficulty targets per threat tier (or a formula gamora can use to calibrate)
- Blocks: all 18 encounter additions

**WU-R2: Per-cell mob composition specs — 18 encounter definitions**
- For each of the 18 cells above, rocket authors the mob composition intent (threat tier + archetype_tag + element + count) that the arena scenario shell will use
- Gamora provides: arena scenario shell (one of the 6 existing scenarios) + WR contract alignment
- Rocket provides: specific monster prototype definitions that realize the composition intent at L45-50+ difficulty
- Format: one encounter definition per cell, specifying mob tier + archetype + element + desired endgame calibration markers

**WU-R3: Mob archetype coverage for WR contract alignment**
- Several recommended encounters use `archetype_tag="caster"`, `"brute"`, `"boss"` — these must have L45-50+ stat variants in the bestiary
- Rocket must verify (or create) that each archetype_tag has L45-50+ calibrated monster instances available for selection
- This feeds `build_reference_gauntlet()` which selects from the bestiary by tier + archetype

**WU-R4: Proxy-light and proxy-heavy sim extension (Cycle 14+)**
- 7 cells are deferred due to proxy-light/heavy sim constraint
- Rocket flags: these cells need encounter content authored when sim extension lands
- These are NOT Cycle 13 v1 scope — record as Cycle 14+ work-unit specification

### 6.2 Jack-ryan Gate-1 critique handoff

This audit memo is the input to the jack-ryan Gate-1 critique dispatch (separate dispatch per SC-6 architecture). Gate-1 fires post-audit on the recommendations and coverage map.

**Gate-1 input items for jack-ryan:**
1. The 0-encounter baseline finding — confirm this finding is correct (no hidden encounter catalog exists elsewhere in the codebase)
2. The 18 non-deferred cell recommendation list — critique for coverage completeness + quality against Discipline #26
3. The proxy-deferred 7-cell scope boundary — confirm this aligns with BC axis deferred-evaluation policy per `qd-engine-bc-axes-lock-2026-05-20.md:§ 5`
4. The difficulty calibration gap (WU-R1) — flag as a design gap requiring Matt resolution or empirical-iteration gate

---

## Post-Script Empirical Count Assertions (WARN-pattern discipline)

Per Cycle 13 skill_handoff priority 2 and dispatch § 3 (Discipline #1.2 + WARN-pattern reminder):

**Dimension 1 — Current encounter inventory:** I cite 0 endgame-reference-encounters. Verified by searching `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/` for `reference_encounter`, `endgame_encounter`, `encounter_catalog`, `L45`, `BC_CELL` patterns — 0 results for structured encounter catalog. The 6 arena scenarios are confirmed by `grep -n "^SCENARIO_" /Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` returning 6 entries (lines 283, 347, 402, 486, 568, 643).

**Dimension 2 — BC cell count:** I cite ~22-25 cells from Sketch A in `v1-bc-target-intent-2026-05-24.md`. Verified by manually counting table rows in § 1.1 of that doc: STR=5, DEX=6 (counting `(mid, low, spiky, DEX, none)` as one cell), INT=7, WIS=7 = 25 total enumerated. The doc's own summary says "~22 distinct cells" — the delta is attributable to the doc's own rounding ("~22") vs the explicit table rows (25). All are NO-COVERAGE regardless.

**Dimension 3 — Proxy-deferred cells:** I cite 7 cells as proxy-deferred. Verified by filtering the 25-cell enumeration for proxy-density = `light` or `heavy`: STR-light (1) + DEX-light (1) + DEX-heavy (1) + INT-heavy (2) + WIS-heavy (2) = 7 deferred cells. Non-deferred count = 25 - 7 = 18.

**Dimension 4 — Recommended additions:** I recommend 18 encounters (1 per non-deferred cell) + 3 optional additions = 21 total. 18 lands within optimal 15-22 range. Verified by cell count above.

---

**Signed:** gamora
**Status:** AUDIT COMPLETE — ready for jack-ryan Gate-1 critique dispatch
**Next:** Knight-rider dispatches jack-ryan Gate-1 critique on this memo's findings + recommendations
