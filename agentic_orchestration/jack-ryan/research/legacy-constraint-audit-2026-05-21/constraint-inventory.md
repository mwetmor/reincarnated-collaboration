# Constraint Inventory — Legacy Constraint Audit (QD-Engine Rebuild Prerequisite)

**Date:** 2026-05-21
**Author:** jack-ryan (DESIGN-MODE)
**Schema version:** per dispatch § 3
**Status:** COMPLETE — 62 entries

---

## Section 1: HIGH-Risk Constraints

---

**LC-001**
- **constraint_name:** Archetype template hardcoded dict (Cluster-B humanoid-fantasy substrate)
- **description:** `ARCHETYPE_TEMPLATES` in `b6_archetype_templates.py:99-465` is a frozen dict of exactly 14 hardcoded templates (now 13 after hybrid_mage RETIRED 2026-05-18). Every (role × element) pair must be manually authored; no new substrates can generate archetypes without new templates. The classifier dispatch at `archetype_classifier.py:9-44` produces tags with no backing template for novel substrates, crashing the kit builder.
- **source_documents:** `canonical/story/archetype-coupling-archaeology-2026-05-17.md` § 2, Coupling #1 + #2; `canonical/story/substrate-expansion-decision-2026-05-17.md` § 3.1; decisions-log 2026-05-17 (substrate expansion)
- **status:** DOCUMENTED
- **engine_surface_affected:** generation
- **bc_axis_affected:** cross-cutting (all 8 axes — template shapes all kit characteristics measured by BC axes)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** REMOVE (replace with on-boot composition from substrate identity declarations × role shape templates per Path-a refactor); VERIFY Phase 2 code audit confirms exact coupling sites
- **dependencies:** LC-002, LC-003, LC-022
- **notes:** The archaeology 2026-05-17 confirmed: fixing one cluster is a single coordinated migration, not 14 distributed problems. The Path-a refactor (composition at boot from `ELEMENT_PROFILES × ROLE_SHAPES`) is the architectural answer. Hybrid_mage RETIRED per `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md`.

---

**LC-002**
- **constraint_name:** Element selection bias — structural-presupposition toward fire (23.6%)
- **description:** Fire element is over-represented at 23.6% vs 20% uniform expected across ~15 historical seasons (B14.5 sidecar finding). Per Discipline #13b, per-variable attribution is unknown without ablation; the structural presupposition exists in the element selector's scoring and rotation logic. If BC axes measure element distribution as part of kit identity, this bias contaminates cell-filling patterns.
- **source_documents:** `memory/project_b14_5_sidecar_analyses.md` finding (4); `canonical/story/pre-llm-substrate-inventory.md` § 4-6; `engineering-disciplines.md` § 13b
- **status:** EMPIRICALLY-SURFACED
- **engine_surface_affected:** generation / element selector
- **bc_axis_affected:** Axis 2B (control density) — fire's DoT signature affects control-vs-damage distribution; Axis 3B (damage amplitude variance) — fire's burn DoT creates temporal amplitude patterns
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** ABLATE (run Discipline #13b experiment: regenerate with fire weight halved; compare BC distribution vs current; attribute fraction of observed convergence shape to selection logic)
- **dependencies:** LC-001, LC-020
- **notes:** The 23.6% over-representation is a convergence-shape observation (claimable from telemetry); attribution to specific selector variables requires ablation per Discipline #13b. Current `element/selector.py` rotation logic and D1 pool weighting are the prime suspects.

---

**LC-003**
- **constraint_name:** Modifier floor-lock at 0.05 (floor-widening partially addressed by recompose-hive)
- **description:** The balance loop binary-search lower bound was 0.05, hard-blocking convergence for kits requiring modifier ~0.02-0.04. Recompose-hive Phase 0 (Option A) widened this floor. However, the operational calibration epoch is mean |mod-1.0| ≈ 0.82, range 0.09-0.52 — still far from the file 29 aspirational 0.85-1.15 band. Low-modifier classes disproportionately fill specific BC cells, creating measurement-contamination.
- **source_documents:** decisions-log 2026-05-16 "B10.4 Option 2 modifier baseline"; `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` § 3.1; `canonical/28-engine-arpg-rebalance-design.md` § B14.5
- **status:** DOCUMENTED (partially addressed — floor widened; epoch still constrained)
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (modifier affects DPS which feeds Axis 3A tempo, Axis 3B variance, Axis 5 economy)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** VERIFY (confirm recompose-hive final state; measure whether remaining modifier spread creates BC cell clustering at extreme bins)
- **dependencies:** LC-004, LC-009
- **notes:** The decisions-log 2026-05-16 epoch entry explicitly states the 0.09-0.52 range is "not a regression — it's the expected output of structural mechanical gaps." B6 energy-type-aware tier assignment + B14.5 V2 are the architectural fix. For QD-rebuild, if cells fill with floor-locked kits, low-modifier archetypes will cluster in certain BC cells, creating false-sparse regions elsewhere.

---

**LC-004**
- **constraint_name:** Energy-type mechanical gradient (~3-5× DPS differential, rage vs mana)
- **description:** Physical/rage classes face a structural ~3-5× DPS-per-modifier disadvantage vs elemental/mana classes, composed of: rage startup delay (~1.5-2×), physical miss rate (~1.18×), armor vs elemental resistance (~1.23×), melee positioning delays (~1.1×). This compounds into the 0.09-0.52 modifier spread observed across the calibration epoch. BC axes measuring DPS tempo and amplitude will reflect this gradient, not the true design space.
- **source_documents:** decisions-log 2026-05-16 "B10.4 Option 2 modifier baseline" (§ full mechanical gap derivation); `simulation/math/modifier-range-root-cause.md` §4.3; `canonical/story/archetype-coupling-archaeology-2026-05-17.md` § 3 stat_allocator
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 3A (damage tempo — rage classes register lower tempo at same modifier), Axis 3B (damage amplitude variance — rage startup creates early-fight variance spike), Axis 4 (defensive profile — melee classes with low modifier must survive longer, inflating eHP requirements)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** REMOVE (via B6 energy-type-aware tier assignment + B14.5 V2 energy-type lever; these are already roadmapped)
- **dependencies:** LC-003, LC-001
- **notes:** Key negative finding from the epoch entry: "generation is NOT the cause" — both hybrid_mage (0.095) and physical_warrior (0.525) have nearly identical magnitude distributions (~77k DPS estimate at mod=1.0). The ~5.5× modifier gap is entirely from sim mechanics. Fix must be in sim energy-system awareness, not generation power budget.

---

**LC-005**
- **constraint_name:** AOE skew — PackProxy ×8 multiplier creates AOE win-rate inflation
- **description:** The PackProxy entity (`simulation/combatant.py`) multiplies AOE damage by pack_size=8 against swarm encounters. This correctly models AOE advantage but creates ~100% win rates for AOE classes against pack slots, inflating aggregate win rates. Convergence binary-search was re-routed (Option 2 per decisions-log 2026-05-16) to exclude pack fights from the convergence target. The skew is thus managed but not removed; AOE vs single-target differential signal in telemetry is partial approximation, not full genre-correct behavior (B10 V2 with HP carryover is the full fix).
- **source_documents:** decisions-log 2026-05-14 "B10.2 Two-Gauntlet Pattern"; decisions-log 2026-05-16 "B10.2 superseded — Option 2"; `canonical/28-engine-arpg-rebalance-design.md` § B10; decisions-log 2026-05-16 "View A locked as AOE balance philosophy"
- **status:** DOCUMENTED (managed via Option 2; B10 V2 is the full resolution)
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 2 (damage geometry) — AOE vs single-target bin assignment directly affected; Axis 3A (tempo — AOE has high-tempo pack fights)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** PRESERVE (View A is locked AOE philosophy; AOE classes earn pack-clear identity as genre-correct archetype payoff); DOCUMENT that Axis 2 BC measurement uses non-pack fight telemetry only; B10 V2 upgrades to sequential-room semantics post-rebuild
- **dependencies:** LC-003
- **notes:** Option 2 makes the convergence binary-search semantically clean ("value at which class wins 50% of canonical 1v1 balance encounters"). Pack fights still simulate; their telemetry captures geometry usage. BC Axis 2 measurement should draw from total fight telemetry, not only convergence fights — this distinction needs explicit spec in the rebuild.

---

**LC-006**
- **constraint_name:** Canonical-four element labels universally exposed to LLM (Cluster E universal drift)
- **description:** Every LLM prompt-construction site in the generation seam currently exposes canonical-four labels (fire/water/earth/wind): `llm/naming.py:26-36`, `:87`, `:89`; `element/selector.py:43-47`, `:394-446`; `canonical/library_generator.py:85`. Doc 37 § 6 specifies these must be hidden. The cipher architecture (doc 37 § 6) specifying canonical-four as resistance-translation-only is unimplemented. This is the cleanest Discipline #13a drift instance in the project.
- **source_documents:** `canonical/story/pre-llm-substrate-inventory.md` § 9 (Cluster E); `engineering-disciplines.md` § 13a (operational example); decisions-log 2026-05-16 "Disciplines #13a / #13b / #14 codified"; `canonical/37-form-bias-diagnosis-and-recovery.md` § 6 + § 9.1
- **status:** DRIFT-CANDIDATE (documented intent; code contradicts it)
- **engine_surface_affected:** generation / llm
- **bc_axis_affected:** cross-cutting (affects all LLM-generated kit content, which feeds every BC axis via kit composition)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** REMOVE (Stage 3 of form-bias migration cadence — cipher migration per form-bias-cadence-strategy.md Option II); VERIFY residual-bias after migration via no-seed cosmology test (Experiment 1 in sub-locks deferred entry)
- **dependencies:** LC-007, LC-014
- **notes:** This constraint does not directly affect the current simulation-based BC measurements, but it contaminates the LLM-generated kit flavor and skill identity that feeds the cohesion-BC archive. If cohesion-BC is part of the QD-engine's joint-gate (Discipline #18 candidate), this drift is HIGH risk for that archive.

---

**LC-007**
- **constraint_name:** Humanoid-presupposing gear schema (Cluster A — loadout/gear 14-item cluster)
- **description:** The gear schema (`generation/gear_schema.py:198-310`) has explicit `weapon`, `off_hand`, `armor`, `accessory` fields presupposing bilateral arm anatomy and humanoid body structure. `handedness` field gates off-hand access on "1h"/"2h". Base item type IDs (`gear_catalog.py:10-49`) include sword/dagger/helmet/chest/robe/gauntlets/boots — medieval-humanoid equipment. `can_equip()` + `stat_requirements` gate equippability on STR/DEX values, presupposing humanoid physical capabilities.
- **source_documents:** `canonical/story/pre-llm-substrate-inventory.md` § 5 (Cluster A); `canonical/37-form-bias-diagnosis-and-recovery.md` § 2 + § 4; `canonical/story/form-bias-cadence-strategy.md` § 1.2
- **status:** DOCUMENTED (Position C migration locked but not yet shipped)
- **engine_surface_affected:** generation / export
- **bc_axis_affected:** Axis 4 (defensive profile — armor schema affects eHP calculation); Axis 5 (resource economy — gear affixes affect resource dynamics)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** REMOVE (Stage 1 of form-bias migration — embodiment-axis as additive schema per cadence entry); PRESERVE the mechanical schema (Position C: slot-as-functional-mechanic); rename to functional labels per doc 37 § 4
- **dependencies:** LC-006, LC-008
- **notes:** Per pre-llm-substrate-inventory.md § 5: "fixing one cluster is operationally different from fixing 14 distributed surfaces. A coordinated schema migration resolves the cluster in one change." The 14-item count is the manifestation of one schema-shape choice. This is Stage 1 of form-bias cadence (rocket dispatch territory), not yet shipped.

---

**LC-008**
- **constraint_name:** STR/DEX/INT attribute axes as math-bearing humanoid labels
- **description:** STR/DEX/INT are not just labels — they flow into `can_equip()` and `stat_requirements` as actual gating math. STR gates melee weapons and heavy armor; DEX gates bows. The math is form-agnostic but the labels carry humanoid-physical connotations (strength = muscular force; dexterity = manual agility). Under structural realignment, these survive as "abstract power dimensions divorced from physical interpretation" (doc 37 § 2) — but the LLM-visible layer still reads them as humanoid.
- **source_documents:** `canonical/37-form-bias-diagnosis-and-recovery.md` § 2; `canonical/story/pre-llm-substrate-inventory.md` § 5 (Cluster A `can_equip()` entry); decisions-log 2026-05-09 "stat-threshold equip gating"
- **status:** DOCUMENTED (survival path via Discipline #14 — labels stay for math; LLM-visible narrative reframes per-embodiment)
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** Axis 4 (defensive profile — STR-heavy archetypes have higher armor); Axis 5 (resource economy — DEX affects dodge/energy patterns)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** PRESERVE (math-bearing labels survive as abstract power dimensions per Position C); DOCUMENT that LLM-visible surfaces show per-embodiment narrative skin, not raw STR/DEX/INT labels (Discipline #14 enforcement)
- **dependencies:** LC-007, LC-006
- **notes:** Key distinction from doc 37 § 2: "Under structural realignment these survive as abstract power dimensions divorced from physical interpretation — the labels stay (for engine math, gear gating, balance) but the LLM-visible narrative reframes them per-embodiment." This is a PRESERVE at the math layer + REMOVE at the LLM-visibility layer.

---

**LC-009**
- **constraint_name:** Hunter archetype modifier range 1.82 — inconsistent convergence shape
- **description:** Hunter archetype has a 1.82 modifier range across seeds (B14.5 sidecar finding #2) — the least consistent shape across seeds of any archetype. This means BC cell assignment for hunter-shaped kits is noisier than other archetypes, creating measurement instability in the archive. Per Discipline #13b, attribution to specific variables is unknown without ablation.
- **source_documents:** `memory/project_b14_5_sidecar_analyses.md` finding (2); `engineering-disciplines.md` § 13b
- **status:** EMPIRICALLY-SURFACED
- **engine_surface_affected:** generation / simulation / balance_loop
- **bc_axis_affected:** Axis 1 (engagement profile — hunter is ranged-fast); Axis 3A/3B (tempo/variance — hunter's range advantage creates variable fight durations)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** ABLATE (run Discipline #13b experiment: isolate hunter template variables — range_profile, geometry_bias, kit_size — one at a time; measure modifier variance contribution per variable)
- **dependencies:** LC-001, LC-004
- **notes:** The 1.82 range is a convergence-shape observation. The template's `range_profile=long` + `geometry_bias` toward ranged projectiles likely interact with the sim's `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` constraint (added for mages) in ways that produce inconsistent positioning outcomes across seeds.

---

**LC-010**
- **constraint_name:** Proxy density measurement gap — current sim is solo-only
- **description:** Axis 2A (proxy density) BC bins `proxy-light` and `proxy-heavy` are categorically unmeasurable by the current sim. "Player-side proxy generation absent today — major substrate gap" per BC axes lock § 3.3. All kits requiring summoning, charming, totem-placement, or mind-control will route to deferred-evaluation pool. Profile A operational archive excludes these bins entirely.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.3 (Axis 2A substrate flags + sim deferral risk HIGH); § 5 sim deferral matrix
- **status:** DOCUMENTED (explicitly deferred in BC axes lock)
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 2A (proxy density) — all non-solo bins deferred
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** PRESERVE as deferred; DOCUMENT that Profile A operational archive uses solo bin only; VERIFY current generation never accidentally produces proxy-type skills that would require proxy sim support to evaluate
- **dependencies:** LC-001
- **notes:** BC axes lock Profile A reduces cell space from 68,040 to 25,920. This is intentional but means 62% of the nominal design space is inaccessible until proxy sim extensions land. For QD-rebuild planning, any proxy-type skill that appears in generation would be silently mis-evaluated in the solo sim context — a P7-pattern risk.

---

**LC-011**
- **constraint_name:** Convergence iterations highest for controllers/mages, lowest for rogue/hunter
- **description:** B14.5 sidecar finding #1: convergence iterations are highest for controllers/mages and lowest for rogue/hunter. This means controller and mage archetypes consume more recompose budget per season generation. Under a QD archive generation loop, kits that converge slowly will be underrepresented in the archive (they take more compute per iteration). Per Discipline #13b, the per-variable contribution to this convergence-difficulty pattern is unknown without ablation.
- **source_documents:** `memory/project_b14_5_sidecar_analyses.md` finding (1); `canonical/28-engine-arpg-rebalance-design.md` § B14.5; decisions-log 2026-05-12 "B14.5 scope expansion"
- **status:** EMPIRICALLY-SURFACED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 2B (control density — control-pure archetypes are the slowest-converging); cross-cutting QD generation efficiency
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** ABLATE (run Discipline #13b experiment: measure convergence iterations per archetype-type under current vs simplified constraint sets; attribute iteration overhead to specific constraint variables)
- **dependencies:** LC-001, LC-004
- **notes:** If controller/mage kits require 3-5× more recompose iterations per kit, the QD archive will see them as "expensive to generate" and may deprioritize them in favor of cheaper rogue/hunter cells. This creates a structural under-representation in the archive that reflects generation cost, not true kit quality. The QD generation loop should be cost-aware per cell to prevent this.

---

**LC-012**
- **constraint_name:** Foundation model validator hard-codes 4-rotating + 1-physical (Flag B)
- **description:** `foundation/foundation.py:39-43` enforces via model_validator: exactly 1 non-rotating element named "physical" plus 4 rotating elements. Substrate expansion to 6 substrates (decision: fire/water/wind/earth + lightning + holy/shadow per decisions-log 2026-05-17) requires this validator to update. The architectural question — does Foundation grow with the cipher or decouple to a separate L2 cosmology concept — is explicitly deferred to catalogue-track empirical gates.
- **source_documents:** `canonical/story/pre-llm-substrate-inventory.md` § 12 (Flag B); decisions-log 2026-05-16 "four form-bias sub-locks explicitly deferred"; `canonical/story/substrate-expansion-decision-2026-05-17.md` § 3
- **status:** DRIFT-CANDIDATE (canonical decision: expand to 6; validator enforces 4; drift between committed design direction and code state)
- **engine_surface_affected:** generation / foundation
- **bc_axis_affected:** cross-cutting (foundation shapes all kit generation primitives)
- **qd_rebuild_risk:** HIGH
- **recommended_disposition:** VERIFY (Phase 2 specialist confirms current validator state and whether substrate expansion dispatch has shipped against it); REMOVE/UPDATE as part of Phase-1 P1 substrate expansion work
- **dependencies:** LC-001, LC-006
- **notes:** The substrate-expansion decision names Phase-1 P1 as the ship gate, explicitly not VS2a/VS2b. For QD-rebuild, if the Foundation validator still enforces canonical-four at rebuild time, any attempt to generate 6-substrate seasons will fail the validator, truncating the archive's substrate variety.

---

## Section 2: MEDIUM-Risk Constraints

---

**LC-013**
- **constraint_name:** Mage range constraint — ARCHETYPES_FORBIDDEN_CLOSE_RANGE list
- **description:** `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` in `generation/b6_kit_builder.py` (or similar) prevents fire_mage, water_mage, hybrid_mage (now retired) from generating close-range kits. This was added during KI-B6-1 resolution as a "design violation" fix. Extension candidates (earth_caster, wind_caster, all controllers) were surfaced but deferred.
- **source_documents:** decisions-log 2026-05-12 "B6 generator-validated — KI-B6-1 resolution" (step 3 generator constraint satisfaction); `canonical/story/archetype-coupling-archaeology-2026-05-17.md` § 2 Coupling #3
- **status:** DOCUMENTED
- **engine_surface_affected:** generation
- **bc_axis_affected:** Axis 1 (engagement profile) — prevents close-fast / close-slow bins from populating for mage archetypes
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** PRESERVE (intentional design constraint for Phase 0); DOCUMENT explicitly in BC Axis 1 spec that mage archetypes are excluded from close-range bins; VERIFY whether earth_caster and wind_caster should also be in the list
- **dependencies:** LC-001
- **notes:** The B14.5 sidecar finding #5 found "close-range controllers exist (earth/fire/wind)" — meaning the mage constraint doesn't prevent all close-range magical archetypes, just the named mages. This creates an asymmetry between mage and controller that is unresolved at the design level.

---

**LC-014**
- **constraint_name:** D1 element-name pool humanoid-fantasy selection bias (Flag A + three-level drift)
- **description:** The D1 element-name pool (81 allow-list / 40 eligible / 35 quarantine = 156 entries) was assembled against rubric criteria (`visualizable`, `fantasy-heroic`, `genre-precedent`, proposed `vocabulary_commonness`) that are implicitly Earth-realm-humanoid-fantasy-reader-perspective. Three levels of drift: pool contents selection, status assignments, and rubric sub-properties. The rubric at `element/selector.py:282-296` embeds humanoid-fantasy compounding via Q2 (`{word}-bolt` or `{word}-armor`) and Q4 (`{word}-Knight` or `{word}-Mage`), each scoring +2.
- **source_documents:** `canonical/37-form-bias-diagnosis-and-recovery.md` § 7; `canonical/story/pre-llm-substrate-inventory.md` § 12 (Flag A); `memory/project_b14_5_sidecar_analyses.md` (element selection); decisions-log 2026-05-16 "four form-bias sub-locks" (D1 reconsideration deferred)
- **status:** DRIFT-CANDIDATE (rubric encodes humanoid-fantasy perspective without naming that as the intent)
- **engine_surface_affected:** generation / element selector
- **bc_axis_affected:** Axis 2B (control density) and Axis 3A/3B (tempo/variance) — element names affect LLM-generated skill characterizations, which feed into kit behavior
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** ABLATE (run Flag A targeted test: run D1 rubric on non-humanoid-cosmology candidate words; measure systematic under-scoring); then DOCUMENT whether D1 pool approach survives cipher migration or requires structural rebuild
- **dependencies:** LC-006, LC-012
- **notes:** D1 pool reconsideration is explicitly deferred to catalogue-track sub-locks per decisions-log 2026-05-16. The pool approach itself may not survive the cipher architecture migration. For QD-rebuild, the element pool shapes what season-vocabulary the LLM can generate, which affects cohesion-BC archive quality but has lower direct impact on simulation-based mechanical BC measurements.

---

**LC-015**
- **constraint_name:** DOPPELGANGER_MODIFIER_FLOOR = 0.30 — floor creates gate behavior discontinuity
- **description:** The doppelganger gate runs at `max(player_class.balance_modifier, 0.30)` to prevent timeout artifacts for extreme low-modifier classes. The constant is "empirically confirmed — all current archetypes resolve via kills at this floor." This means the doppelganger gate's quality signal changes character at the floor boundary: below 0.30, the gate validates "can win at normalized power"; above 0.30, it validates "can win at balanced power." If future substrates produce kits that converge below 0.30, the gate's semantic changes without warning.
- **source_documents:** decisions-log 2026-05-12 "B14.5 doppelganger gate — floor balance_modifier"; `canonical/28-engine-arpg-rebalance-design.md` § B14.5; `src/reincarnated/simulation/balance_loop.py` DOPPELGANGER_MODIFIER_FLOOR
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (doppelganger gate affects which kits survive into BC measurement at all)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** PRESERVE (the floor is the right design for current archetypes); DOCUMENT the semantic discontinuity explicitly; VERIFY that 6-substrate expansion and QD-generated kits don't produce systematic sub-0.30 convergers that would silently change gate semantics
- **dependencies:** LC-003, LC-004
- **notes:** The decisions-log entry notes: "if a future archetype introduces even lower modifiers, the floor value may need upward adjustment." Under QD archive generation, the engine will explore novel kit configurations that may converge at very low modifiers. The floor gate's semantic shift is an invisible constraint on what the archive can contain.

---

**LC-016**
- **constraint_name:** Per-fight damage variance ±25% (Prop 4)
- **description:** At fight start, each combatant's `damage_modifier` is multiplied by `uniform[0.75, 1.25]` using a separate seeded RNG stream. This was the actual root-cause fix for KI-B6-1 (1/√N analysis showed per-hit variance couldn't fix doppelganger gate failures; per-fight variance bypasses 1/√N entirely). The ±25% is acknowledged as "on the high end" with a note that B14.5 may dissolve the need via kit composition improvement.
- **source_documents:** decisions-log 2026-05-12 "B6 generator-validated — KI-B6-1 resolution" (Prop 4); `src/reincarnated/simulation/fight_engine.py` `enable_fight_damage_variance`
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 3B (damage amplitude variance — the ±25% per-fight roll contributes to CV measurement); Axis 5 (resource economy — fight-level DPS variance affects resource cycle patterns)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** ABLATE (measure CV contribution from ±25% per-fight variance vs intrinsic kit variance; determine whether this inflates the flat/variable/spiky bin boundaries); DOCUMENT interaction with BC Axis 3B measurement spec
- **dependencies:** LC-009
- **notes:** The ±25% per-fight variance may cause legitimately-flat kits to register as "variable" in Axis 3B and legitimately-variable kits to register as "spiky." This blurs the bin boundaries. The BC axes lock specifies "Event-level variance, not windowed" for Axis 3B — per-fight variance is fight-level, which is coarser than event-level. The spec may not fully account for this distinction.

---

**LC-017**
- **constraint_name:** Gauntlet composition — 6 PackProxy slots + 6 non-proxy 1v1 slots
- **description:** `GAUNTLET_TIER_COMPOSITION` (made public at B10.2) defines 6 swarm PackProxy slots + 2 magic + 2 elite + 1 mini-boss + 1 boss = 12 total monsters per A3 convergence gauntlet. Convergence binary-search (Option 2) excludes pack fights and targets non-pack WR = 50%. Pack fights still simulate and appear in telemetry. BC Axis 2 (geometry) measurement should draw from full fight telemetry but the "convergence WR" semantic is non-pack only.
- **source_documents:** decisions-log 2026-05-14 "B10.2 PackProxy entity"; decisions-log 2026-05-16 "B10.2 superseded — Option 2"; `src/reincarnated/simulation/balance_loop.py` GAUNTLET_TIER_COMPOSITION
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 2 (damage geometry — pack fights inflate AOE geometry usage in telemetry); Axis 3A (tempo — pack fights skew tempo high for AOE classes)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** DOCUMENT that BC Axis 2 geometry measurement must source from fight_telemetry including pack fights (captures AOE identity), but Axis 3A tempo measurement should be normalized or sourced separately to avoid pack-fight inflation; VERIFY the BC measurement spec handles this distinction
- **dependencies:** LC-005
- **notes:** BC axes lock § 3.2 specifies geometry measurement "per fight_telemetry" without distinguishing pack vs non-pack. This is an underspecification relative to Option 2's distinction. Must be resolved before BC measurement implementation.

---

**LC-018**
- **constraint_name:** Energy homogeneity — low variance in energy patterns across kit compositions
- **description:** B14.5 sidecar finding: energy patterns are homogeneous across many generated kits — generators produce similar resource-cycle shapes regardless of archetype. This means BC Axis 5 (resource economy) cells will be populated unevenly: some bins will fill readily (steady, generator-spender which map to common patterns) while others will be sparse (charge-stack, HP-economy, damage-taken-converts which require structural mechanic flags not present in current generation).
- **source_documents:** `memory/project_b14_5_sidecar_analyses.md` finding (5); `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.8 (Axis 5 substrate flags)
- **status:** EMPIRICALLY-SURFACED
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** Axis 5 (resource economy) primarily
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** ABLATE (measure current generation's distribution across the 7 Axis 5 bins; identify which bins are currently unreachable without new mechanic flags); DOCUMENT minimum substrate volume needed per bin before QD archive can fill meaningfully
- **dependencies:** LC-001, LC-030
- **notes:** BC axes lock § 3.8 lists substrate flags needed: HP-cost skill variety (~35 templates), charge-stack mechanic variety (similar). These are explicitly new substrate requirements, not currently present.

---

**LC-019**
- **constraint_name:** Cohesion gate — LLM-judged thematic coherence not yet wired
- **description:** The QD-engine vision doc specifies a Cohesion-BC archive (separate from Mechanical-BC) that uses LLM-judge-measured thematic coherence. The cohesion-BC archive is "owned by gandalf" per BC axes lock § 1.3. No cohesion gate currently exists in the engine; the cohesion score in the B14.5 fitness function (`w_cohesion × theme_cohesion_score(k, theme)`) is specified but not implemented.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 1.3; `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` § 2.4 fitness function
- **status:** IMPLIED
- **engine_surface_affected:** simulation / telemetry / export
- **bc_axis_affected:** cohesion-BC archive (separate from the 8 mechanical axes)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** DOCUMENT as explicit Phase 2 gate (after mechanical BC measurement lands); design cohesion gate spec against the BC axes lock's LUCB1 / information-bottleneck framing
- **dependencies:** LC-006
- **notes:** The Discipline #14 drift (LC-006) contaminates cohesion measurement: if canonical-four labels appear in LLM output (which they currently do via the prompt sites), the cohesion gate can't distinguish "thematically coherent to the season" from "defaulting to canonical-four Earth-realm pattern." Cohesion-BC archive correctness depends on the cipher migration shipping first.

---

**LC-020**
- **constraint_name:** Per-tier WR convergence targets (A1/A2 diagnostic-only, A3 primary)
- **description:** The convergence framework uses A3 (L50 endgame) as the primary convergence driver; A1/A2 produce diagnostic-only win-rate reports per B10 V1 decision. Full per-band convergence (each band as a separate convergence target) requires B9 per-band SP allocation — deferred. When B9 ships, A1/A2 move from diagnostic-only to full convergence drivers.
- **source_documents:** decisions-log 2026-05-13 "B10 V1 ships pack-proxy AOE approximation"; `canonical/28-engine-arpg-rebalance-design.md` § B10, B14.2-B14.4; decisions-log 2026-05-11 "progression philosophy"
- **status:** DOCUMENTED (A1/A2 diagnostic-only is intentional, not a bug)
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (per-tier targets affect which kits converge at all and at what modifier)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** PRESERVE as current architecture (A3 primary; A1/A2 diagnostic) until B9 ships; DOCUMENT that QD archive kits are "A3-converged" and may not be A1/A2-optimal; BC measurements drawn from A3-fight telemetry specifically
- **dependencies:** LC-003
- **notes:** BC axes lock thresholds (Axis 4 eHP formula uses encounter_duration_target=30s) are calibrated against the A3 endgame encounter context. A1/A2 fights (lower-tier content) may produce different BC measurements for the same kit. The archive should be labeled by convergence tier.

---

**LC-021**
- **constraint_name:** Movement-modeling abstraction limitation — sim is movement-speed-blind
- **description:** The sim has positional state (range_profile, at_melee_range, CLOSE_TO_MELEE_TIME=0.5s, teleport range-closure) but no `movement_speed` parameter; no kiting modeling; no L1-vs-L50 differentiation. BC Axis 1 (engagement profile) measures mobility by "movement-skill-attributable displacement" — but the BC axes lock's Axis 1 substrate flag requires `movement_displacement_per_cast` attribute on skills, which does not currently exist. Walking and reactive repositioning are excluded from the mobility component.
- **source_documents:** decisions-log 2026-05-16 "View A locked as AOE balance philosophy" (Lock 3 — movement-modeling abstraction limitation); `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.1 Axis 1 substrate flags; `canonical/story/engine-balance-stewardship.md` Gate-3
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 1 (engagement profile — mobility component measurement requires `movement_displacement_per_cast`)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** DOCUMENT as a known BC measurement gap; VERIFY that Axis 1 mobility bin assignment gracefully handles missing `movement_displacement_per_cast` (defaults to low-mobility); schedule movement-speed-aware sim extension per decisions-log Stage A2 B-series item
- **dependencies:** LC-001
- **notes:** The decisions-log Lock 3 finding: "the View A finding's -25% non-pack KPM is from a movement-speed-blind sim. Real gameplay would have movement-speed-aware kiting (genre-standard mitigation). The 'less-efficient, not helpless' reading is therefore CONSERVATIVE — real gameplay closes the gap further." For BC Axis 1, this means the close-fast and mid-fast bins may be under-populated vs what would emerge in a movement-aware sim.

---

**LC-022**
- **constraint_name:** Substrate-expansion archetype matrix gap (6-substrate expansion has no templates)
- **description:** The substrate expansion decision (decisions-log 2026-05-17) adds lightning + holy + shadow to the canonical-four. However, `ARCHETYPE_TEMPLATES` has no templates for these new substrates. The archetype classifier dispatch would produce `{lightning}_controller`, `{holy}_mage`, etc. as tags, then crash the kit builder with `ValueError("No B6 template for archetype")`. Phase-1 P1 is the ship gate but templates don't yet exist.
- **source_documents:** decisions-log 2026-05-17 "substrate expansion"; `canonical/story/archetype-coupling-archaeology-2026-05-17.md` § 2 Coupling #1 (template authoring cost); `canonical/story/substrate-expansion-decision-2026-05-17.md` § 5
- **status:** IMPLIED (decision made; implementation gap implied)
- **engine_surface_affected:** generation
- **bc_axis_affected:** cross-cutting (all axes — new substrates would populate new regions of the archive)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** VERIFY (Phase 2 confirms current generation strictly stays in canonical-four until substrate expansion lands); DOCUMENT that QD archive filling will be canonical-four-only until Phase-1 P1 ships
- **dependencies:** LC-001, LC-012
- **notes:** Per archetype-coupling-archaeology: Path-a refactor (on-boot composition from substrate identity declarations × role shape templates) would make this a 0-new-template problem. Path-b (manual authoring) requires 9 new templates for 3 substrates × 3 roles minimum. The QD rebuild should be designed against the Path-a architecture even if implementation lags.

---

**LC-023**
- **constraint_name:** Recompose-gauntlet stripping PackProxy — recompose vs convergence semantic asymmetry
- **description:** `_make_recompose_gauntlet()` strips PackProxy → base_monster for the recompose loop, while convergence loop uses the full gauntlet (but excludes pack fights from the binary-search target per Option 2). This creates three distinct semantic contexts: recompose evaluation (pure 1v1), convergence target (non-pack 1v1 WR = 50%), and full telemetry (includes pack fights). BC measurements drawing from "fight_telemetry" span all three contexts; care must be taken to specify which context per axis.
- **source_documents:** decisions-log 2026-05-14 "Two-Gauntlet Pattern"; decisions-log 2026-05-16 "Option 2 supersession"; `src/reincarnated/simulation/balance_loop.py` `_make_recompose_gauntlet()`
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 2 (geometry), Axis 3A (tempo) — semantics differ across fight contexts
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** DOCUMENT per-axis telemetry sourcing in BC measurement spec; VERIFY Phase 2 confirms the gauntlet semantic map is still accurate in the recompose-hive post-state
- **dependencies:** LC-005, LC-017
- **notes:** General principle from decisions-log: "Any future proxy entity that modifies encounter shape requires the same treatment. Recompose = proxy-free 1v1. Convergence binary-search excludes pack fights. Pack telemetry = diagnostic-only surface." This is a stable documented constraint once fully wired.

---

**LC-024**
- **constraint_name:** Dodger bin — stealth/iframe/reflection sub-cases deferred
- **description:** Axis 4 dodger bin has partial sim deferral: probabilistic evasion is supported; stealth (untargetable-for-duration), iframes (skill-cast-state), and reflection (per-hit redirection) are NOT supported. Evasion-stack builds populate dodger bin today; stealth+iframe+reflection builds route to deferred-evaluation pool.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.7 (Axis 4 sim deferral risk PARTIAL)
- **status:** DOCUMENTED (partially deferred per BC axes lock)
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 4 (defensive profile — dodger bin)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** PRESERVE (deferred per axes lock design); DOCUMENT Profile A filter excludes stealth/iframe/reflection sub-cases; VERIFY generation doesn't produce stealth/iframe/reflection skills that would need a proxy path
- **dependencies:** LC-010
- **notes:** Per BC axes lock, Profile A operational archive uses dodger bin only via evasion-stack builds. The sim deferral matrix is explicit. This is a clean designed constraint, not a hidden one.

---

**LC-025**
- **constraint_name:** Charge-stack and damage-taken-converts bins deferred (Axis 5)
- **description:** Axis 5 charge-stack and damage-taken-converts bins are conditionally deferred: both may need sim extensions (charge buildup triggers, cap behavior, decay timers, consumption skills; damage-to-resource conversion at hit-resolution). Profile A operational archive uses HP-economy + starved + generator-spender + steady (4 of 7 bins), excluding charge-stack, damage-taken-converts, and overflow.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.8 (Axis 5 sim deferral risk MODERATE); § 5 sim deferral matrix; § 10.3 Profile A operational cell count
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 5 (resource economy)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** VERIFY current generation doesn't produce charge-stack or CWDT-style skills that would silently mis-classify into steady/generator-spender bins; DOCUMENT Profile A operational archive explicitly excludes these bins
- **dependencies:** LC-018
- **notes:** Per BC axes lock, Profile A cell count = 6 × 5 × 1 × 3 × 3 × 3 × 4 × 4 = 25,920 (not full 68,040). The reduction from 7 to 4 bins on Axis 5 is the largest single-axis contribution to the reduction.

---

**LC-026**
- **constraint_name:** Mana bug (structural) — non-mana classes assigned mana by pipeline
- **description:** Non-mana classes (rage, combo, focus, stamina) are assigned mana by a pipeline that assumes every combatant has mana. This was a documented structural bug as of the 2026-05-08 engine state findings. Phase 1 of the dimensional generation refactor was designed to remove the assumption rather than patch the symptom. Status of implementation requires Phase 2 verification.
- **source_documents:** `memory/project_engine_state_findings.md` (mana bug is structural); decisions-log 2026-05-08 "Dimensional generation refactor adopted (Option C)"; `canonical/28-engine-arpg-rebalance-design.md` § A (Bug fixes)
- **status:** DOCUMENTED (flagged; fix designed; implementation status requires VERIFY)
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 5 (resource economy — mana being incorrectly assigned would inflate mana-availability for non-mana classes, distorting economy bin assignment)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** VERIFY (Phase 2 confirms whether mana bug was resolved in dimensional generation refactor or still present)
- **dependencies:** LC-004
- **notes:** If non-mana classes have mana fields silently populated, Axis 5's structural checks (hp_cost_fraction, has_damage_to_resource_conversion_mechanic) may behave correctly because the structural mechanics override mana. But statistical checks (mean_resource_fraction, resource_fraction_variance) drawing on the wrong resource pool would produce incorrect economy bin assignments.

---

**LC-027**
- **constraint_name:** Ailment-damage-signatures DEFERRED (thematic secondary damage on control ailments)
- **description:** The design proposal to add small secondary damage signatures to control ailments (wind cut+bleed, earth thorny root, water cold-burn; fire already has burn DoT) was deferred indefinitely after B14.5 V1 doppelganger gate re-run showed HIGH signal (all four pure-control archetypes in 0.39-0.49 mirror-match WR range). The proposal is in design-polish queue.
- **source_documents:** decisions-log 2026-05-16 "Ailment-damage-signatures deferral made indefinite"; `memory/project_ailment_damage_thematic.md`; `canonical/37-form-bias-diagnosis-and-recovery.md` § 6.4
- **status:** DOCUMENTED (DEFERRED indefinitely per HIGH-signal doppelganger gate result)
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 2B (control density — secondary damage would shift control-pure kits toward mixed); Axis 3A/3B (tempo/variance)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** PRESERVE as design-polish queue; DOCUMENT that the QD rebuild inherits the current state (pure control ailments without secondary damage); if BC Axis 2B shows control-pure bin underpopulated, revisit as a lever
- **dependencies:** LC-011
- **notes:** The deferral reason is empirical and clean. Reactivation gate: "if wind_controllers hover at 20-25% (in-band borderline) → implement; if out of band → immediate fix." Under QD generation, novel controller kits may require this mechanism. The design-polish queue classification means it's available as a lever without being on the critical path.

---

**LC-028**
- **constraint_name:** Single-word rule for element names constrains seasonal vocabulary
- **description:** All entries in the seasonal element pool must be single words (decisions-log 2026-05-07). Compound element names and multi-word phrases are reserved for ability naming. This constrains the per-season vocabulary that the cipher architecture will eventually generate — deep-sea cosmology words like "bioluminescence" and "deep-current" would fail single-word validation if multi-word.
- **source_documents:** decisions-log 2026-05-07 "Single-word rule for element names"; `memory/project_b14_5_sidecar_analyses.md` (element pool note)
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / element selector
- **bc_axis_affected:** LOW — affects LLM vocabulary, not mechanical BC measurements
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** VERIFY whether the cipher architecture's per-season vocabulary generation pipeline enforces this rule; DOCUMENT whether the rule applies to per-season LLM-generated vocabulary under the grouping layer or only to the D1 allow-list pool
- **dependencies:** LC-014
- **notes:** Under the three-layer model (substrate / grouping / vocabulary), vocabulary-layer words are LLM-generated per season — they may not be pool-sourced and thus may not be subject to the single-word rule. This is an architectural ambiguity that needs resolution before the cipher migration dispatches ship.

---

**LC-029**
- **constraint_name:** Swarm eff_attr=7 calibration — minor attack threat floor
- **description:** `TIER_EFFECTIVE_ATTRIBUTE["swarm"]` was bumped from 0 to 7 at B10.4 to give swarm encounters a "modestly calibrated threat floor." The design-intent ratio (swarm 0.20× damage vs trash 0.60× = 3× differential) is NOT achievable via eff_attr alone; the constraint `damage_scaling(eff_attr)` only gives 1.0-2.0× range, requiring generator-side skill magnitude tuning for the full differential.
- **source_documents:** decisions-log 2026-05-14 "B10.4 swarm eff_attr calibration"; `simulation/math/b10-4-swarm-eff-attr-calibration.md`
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 4 (defensive profile — swarm threat affects eHP requirements); Axis 3A (tempo — swarm attack timing)
- **qd_rebuild_risk:** LOW (swarm fights excluded from convergence target under Option 2)
- **recommended_disposition:** PRESERVE; DOCUMENT that swarm threat is partial approximation; B10 V2 with HP carryover is the full resolution
- **dependencies:** LC-005, LC-017

---

**LC-030**
- **constraint_name:** HP-cost skill variety gap — structural Axis 5 bin
- **description:** BC axes lock Axis 5 specifies: "HP-cost skill variety (5× rule on 7-bin axis = ~35 distinguishable templates)." Current generation may not produce HP-cost skills (skill cost_type = HP). The BC axes lock explicitly flags this as a substrate gap: "HP-cost as recognized skill cost type" is listed as a required sim telemetry extension.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.8 Axis 5 substrate flags item 2 and item 7
- **status:** IMPLIED
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** Axis 5 (resource economy — HP-economy bin)
- **qd_rebuild_risk:** MEDIUM
- **recommended_disposition:** VERIFY (Phase 2 checks whether current generation can produce HP-cost skills; if not, HP-economy bin will be empty in the QD archive until generation is extended)
- **dependencies:** LC-018, LC-025
- **notes:** PoE Blood Magic and D2 Bone Spirit are canonical ARPG precedents. Not having HP-cost skills is a significant substrate gap for Axis 5 diversity.

---

## Section 3: LOW-Risk Constraints

---

**LC-031**
- **constraint_name:** Auto-accept LLM element proposals for Phase 0
- **description:** When the element selector's LLM proposes a new element, it is automatically accepted and added to the pool without manual review. Proposals are tracked in `element_proposals` table with status "auto_accepted." A manual review process should be defined before production deployment.
- **source_documents:** decisions-log 2026-05-07 "Auto-accept LLM element proposals for Phase 0"
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / element selector
- **bc_axis_affected:** Axis 2B (control density) marginally — element vocabulary affects LLM-generated skill roles
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** DOCUMENT that QD archive generation under Phase 0 inherits this policy; POST-QD-MVP add review gate for high-volume generation runs
- **dependencies:** LC-014

---

**LC-032**
- **constraint_name:** END_GAME_DROPS_PER_SLOT = 50 loadout sampling model
- **description:** Balance loop loadout sampling uses best-of-50 analytical tier distribution rather than per-drop probabilities. This calibrates balance against realistic player gear state (~0% common, ~40% rare, ~38% uncommon, ~9.5% epic, ~9.5% legendary) rather than first-drop distribution.
- **source_documents:** decisions-log 2026-05-09 "Equipped-distribution loadout model"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 4 (defensive profile — gear affects eHP), Axis 5 (resource economy — gear affixes affect resource pool)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; DOCUMENT that BC measurements are calibrated against end-game gear state assumption
- **dependencies:** none

---

**LC-033**
- **constraint_name:** Discipline #17 smoke-environment-must-mirror-production (D11.2 amendment)
- **description:** Smoke environments must mirror production environment dimensions: gear_catalog loaded, monster_pool present, archetype parameters identical. D11.2 Phase A showed false-positive smoke at scale=0.75 due to no-gear environment; Phase B showed 0/17 FAIL in full-gear production. This is now a process constraint, not a code constraint, but it shapes all future calibration work.
- **source_documents:** `engineering-disciplines.md` § 17 (Discipline #17 + D11.2 amendment); decisions-log 2026-05-18 "RETIRE hybrid_mage — #160 verdict"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop (calibration process)
- **bc_axis_affected:** cross-cutting (calibration quality affects all axes)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE as standing process discipline; ensure QD calibration experiments follow the production-environment-mirror rule
- **dependencies:** none

---

**LC-034**
- **constraint_name:** Single-season-per-playtest cost guardrail
- **description:** Post-Stage-A2 LLM cost ~$5-10/season. Decision: regenerate AT MOST ONE season per playtest cycle as default policy. Multi-season regen exceptions require explicit justification. This limits QD archive fill-rate validation to slow cycles unless a cheaper per-generation mode is available.
- **source_documents:** decisions-log 2026-05-12 "Track A approach — refactor not rewrite + legacy preservation + single-season-per-playtest"; `canonical/28-engine-arpg-rebalance-design.md` header guardrail
- **status:** DOCUMENTED
- **engine_surface_affected:** generation (LLM cost constraint)
- **bc_axis_affected:** all (limits archive fill velocity)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** DOCUMENT that QD archive filling requires a cost model; QD generation loop should support `--no-llm` mode (already exists for smoke) to fill archive without LLM naming overhead; LLM naming deferred to coalescence step per IDC architecture
- **dependencies:** none

---

**LC-035**
- **constraint_name:** Block fires before crit — combat damage resolution ordering
- **description:** In the damage resolver, block check fires before crit check. A blocked hit is reduced and skips crit. This creates a specific interaction pattern where block-heavy kits counter crit-heavy attackers — affecting BC Axis 4 defensive profile (mitigator vs tank) measurement.
- **source_documents:** decisions-log 2026-05-09 "Block fires before crit"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 4 (defensive profile — block behavior affects mitigator vs tank classification)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; DOCUMENT in Axis 4 measurement spec that block precedes crit in resolution order
- **dependencies:** none

---

**LC-036**
- **constraint_name:** Percentage armor formula K=3000 — no zero-damage floor for physical
- **description:** Physical damage mitigation uses `reduction = armor / (armor + 3000)`. This was introduced to fix the flat-subtraction formula that created a zero-damage floor blocking physical class convergence. The K=3000 is explicitly noted as "retunable as gear armor scales change."
- **source_documents:** decisions-log 2026-05-08 "Percentage armor formula with K=3000"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 4 (defensive profile — armor mitigation affects eHP_effective_ratio calculation)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; note K=3000 is a calibration constant that may need retuning under 6-substrate expansion if new substrates have different armor scaling profiles
- **dependencies:** LC-004

---

**LC-037**
- **constraint_name:** DoT bypass fix — buff_dmg_mult applied to tick_damage
- **description:** `buff_dmg_mult` is applied to tick_damage for burn/bleed ailments; `damage_modifier` is applied to HoT tick_heal. Before CP7b, DoT and HoT effects bypassed the balance modifier. Classes with DoT-primary kits were harder to converge than equivalent direct-damage classes — not because their kit was stronger, but because the modifier couldn't reach the DoT component.
- **source_documents:** decisions-log 2026-05-09 "DoT bypass fix (Q11 resolved)"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation
- **bc_axis_affected:** Axis 3A (tempo — DoT-heavy kits register different damage event patterns); Axis 3B (variance — DoT creates sustained low-variance damage streams)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; ensure BC Axis 3A/3B measurement correctly handles DoT tick events in the damage-application event count
- **dependencies:** none

---

**LC-038**
- **constraint_name:** SWAP_VALUE_FLOOR = 0.10 Spirit Guide threshold
- **description:** Spirit Guide swap recommendations use an absolute threshold of 0.10 ("10% of a reference-tier item"). This is a provisionally-calibrated constant. If gear distributions shift significantly under new substrate expansion or B15 set bonuses, this threshold may need retuning.
- **source_documents:** decisions-log 2026-05-09 "Single absolute marginal-value threshold for Spirit Guide"
- **status:** DOCUMENTED
- **engine_surface_affected:** spirit_guide
- **bc_axis_affected:** Axis 5 (resource economy — Spirit Guide affects gear recommendations which affect resource pool composition)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; note as a calibration constant requiring Discipline #17 empirical re-validation when gear profiles change materially
- **dependencies:** none

---

**LC-039**
- **constraint_name:** B14.5 hybrid rejection gate — reverts levers if modifier moves away from 1.0
- **description:** After the primary recompose loop and binary search, if post-lever modifier is NOT closer to 1.0 than the pre-lever proxy (eval_modifier), skills are reverted to the original snapshot. Convergence_report tracks outcome as `primary_loop_converged`, `primary_loop_reverted`, `modifier_fallback`, or `skipped_experimental`. The gate uses eval_modifier as baseline proxy (approximate); V2 would use true converged modifier.
- **source_documents:** decisions-log 2026-05-12 "B14.5 hybrid rejection gate"; `canonical/28-engine-arpg-rebalance-design.md` § B14.5 V1
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (gate determines final kit composition, which affects all BC axes)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; DOCUMENT that the gate's proxy-baseline approximation may cause occasional false-reverts; telemetry can track revert rate to detect systematic issues
- **dependencies:** LC-003

---

**LC-040**
- **constraint_name:** Season manifest versioning 1.3 (forward-compat schema additions)
- **description:** Stage A1 shipped 14 forward-compat schema fields all defaulting to None/[]/{}. Season manifest version bumped 1.2 → 1.3. Existing 5 production seasons load without regeneration. QD archive output must maintain forward-compat discipline as new fields are added.
- **source_documents:** decisions-log 2026-05-12 "Stage A1 closed"
- **status:** DOCUMENTED
- **engine_surface_affected:** export
- **bc_axis_affected:** none directly (schema versioning does not affect BC measurement)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE versioning discipline; QD-engine rebuild output must bump manifest version appropriately and maintain backward-compat reader logic
- **dependencies:** none

---

**LC-041**
- **constraint_name:** Gauntlet backward-compat "standard" tier treated as "trash"
- **description:** The "standard" tier was deprecated in generation but kept in all tables for backward compat with old season JSON fields. Functionally equivalent to "trash" in the new tier table.
- **source_documents:** decisions-log 2026-05-12 "B10.1 — Tier structure shipped"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 4 (defensive profile — tier affects threat level)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; document that "standard" is backward-compat alias for "trash" in any BC measurement that uses tier labels
- **dependencies:** none

---

**LC-042**
- **constraint_name:** R8 inverted-mode coalescence — season theme coalesced post-convergence
- **description:** R8 inverted-mode (default since engine-rebuild 2026-05-19) defers theme injection from generation-time to coalescence-time. The season's theme is not an input; it emerges from the converged kit set. This is the IDC meta-principle's primary instance. A/B test across 6 seasons (3 baseline + 3 inverted at seed parity) confirmed inverted produces comparable cohesion to baseline.
- **source_documents:** `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` § 5 (IDC); `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md` § 1 R8 workstream
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / llm
- **bc_axis_affected:** cohesion-BC (theme coalescence affects cohesion measurement); mechanical BC axes not directly affected
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE as the IDC default; DOCUMENT that QD archive season manifests have coalesced themes (post-convergence), not pre-declared themes
- **dependencies:** LC-006, LC-019

---

**LC-043**
- **constraint_name:** earth_caster B6 constraint deferred — tier1_ground_slam_and_melee_arc unsatisfiable
- **description:** `tier1_ground_slam_and_melee_arc` constraint was removed from earth_caster's `special_constraints` because the current foundation geometry pool doesn't include `ground_slam` or `melee_arc`. A `TODO(B11)` comment marks the deferred restoration. When B11 geometry expansion lands, the constraint should be restored.
- **source_documents:** decisions-log 2026-05-12 "earth_caster B6 constraint deferred to B11"
- **status:** DOCUMENTED (deferred with explicit restoration dependency)
- **engine_surface_affected:** generation
- **bc_axis_affected:** Axis 2 (damage geometry — earth_caster's geometry bias will differ until B11 restores the constraint)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** VERIFY B11 geometry expansion has shipped and TODO restored before QD archive filling begins; if not shipped, earth_caster populates Axis 2 without ground_slam/melee_arc constraint
- **dependencies:** LC-001

---

## Section 4: PRESERVE-Disposition Constraints (Intentional Lock-Ins)

---

**LC-044**
- **constraint_name:** Solo gameplay only (summoner multi-actor gated to Phase 5)
- **description:** Gameplay is solo only; summoner-with-AI-minions deferred to Phase 5. This is a design scope decision (file 29), not an oversight. Proxy-heavy bin (Axis 2A) unavailability for Profile A is a direct consequence of this lock.
- **source_documents:** decisions-log 2026-05-08 "Spirit-swap and form library framing" (solo only clause)
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / generation
- **bc_axis_affected:** Axis 2A (proxy density — proxy-light and proxy-heavy bins excluded from Profile A)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** LC-010

---

**LC-045**
- **constraint_name:** Profile A scope filter — excludes deferred bins from shippable seasons
- **description:** Profile A excludes all currently-deferred bins from shippable seasons: Axis 2A proxy-light/heavy; Axis 4 dodger stealth/iframe sub-cases; Axis 5 charge-stack and damage-taken-converts. This reduces the operational cell space to 25,920 cells.
- **source_documents:** `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 5 (profile filter) + § 10.3
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** Axis 2A, Axis 4, Axis 5
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** LC-010, LC-024, LC-025

---

**LC-046**
- **constraint_name:** ARPG-canon-primary at substrate-mechanical layer (explicit-hybrid Phase-0 lock)
- **description:** Phase-0 ships with ARPG-canon-primary at the substrate-mechanical layer (Cluster A + B mechanics preserved — weapon/armor/attribute math + archetype templates). The isekai-canon work (cipher migration, embodiment-axis) operates at the narrative-skin and convergence layers, not at the mechanical layer.
- **source_documents:** decisions-log 2026-05-16 "Form-bias strategic-axis locked as explicit-hybrid Phase-0"
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** cross-cutting (architectural commitment to ARPG mechanical substrate)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** LC-007, LC-008

---

**LC-047**
- **constraint_name:** View A — AOE classes earn pack-clear identity as genre-correct archetype payoff
- **description:** AOE classes carry pack-clear identity as their archetype payoff. No damage-ratio compensation required at per-skill or per-class level. Single-target classes retain playable floor via encounter-distribution (~30% non-pack content in gauntlet). The compensating axis is content-distribution, NOT damage-ratio. This is locked per decisions-log 2026-05-16.
- **source_documents:** decisions-log 2026-05-16 "View A locked as AOE balance philosophy"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** Axis 2 (damage geometry), Axis 4 (defensive profile indirectly)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** LC-005

---

**LC-048**
- **constraint_name:** B14.5 success metric — mean |modifier - 1.0| not max/min spread ratio
- **description:** The canonical success metric for modifier calibration quality is mean |balance_modifier − 1.0| across taxonomy classes. The max/min spread ratio is a secondary diagnostic only. This prevents the misleading signal where improvement shows as worse max/min ratio (e.g., hunter at 0.525 vs mage at 0.095 produces wide spread even though both are closer to 1.0 than pre-B14.5 baseline).
- **source_documents:** decisions-log 2026-05-12 "B14.5 V1 success metric"
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop (calibration metrics)
- **bc_axis_affected:** none directly (calibration quality metric, not BC measurement)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; apply same metric to QD archive calibration reports
- **dependencies:** none

---

**LC-049**
- **constraint_name:** Court of Forms meta-archetype registry — cross-season accumulation
- **description:** The Court framing locks cross-season meta-archetype-registry behavior: ascending forms accumulate in the Court with named retainers, stations, and presence. This is the Profile A equivalent of the QD engine's cross-deployment registry. The QD architecture's "Court-of-Forms accumulation" cross-deployment mode is explicitly specified in the Profile A config YAML.
- **source_documents:** decisions-log 2026-05-15 "Court of Forms as form-library framing"; `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` § 4.1 Profile A config
- **status:** DOCUMENTED
- **engine_surface_affected:** export / telemetry
- **bc_axis_affected:** none directly (meta-layer accumulation, not per-kit BC measurement)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** none

---

**LC-050**
- **constraint_name:** Naming triad — Trial/Mirror/Passage universal frame locked
- **description:** The three player-facing choice-moments are canonically named Trial/Mirror/Passage. Technical identifiers (doppelganger_validation_runs, etc.) can retain technical names until export-boundary rename. Player-facing display uses seasonal variants on the universal frame.
- **source_documents:** decisions-log 2026-05-15 "Naming triad locked"
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / export / telemetry
- **bc_axis_affected:** none directly
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; engine-side telemetry field names retained (low urgency rename per decisions-log)
- **dependencies:** none

---

**LC-051**
- **constraint_name:** Style register locked — Hand-drawn pixel-art (HD-2D-shaped)
- **description:** The project's primary visual style register is Hand-drawn pixel-art (HD-2D-shaped). Legolas Mode B catalogue crawls tag assets by register; consumption filters by this lock. This is a consumption-time filter, not a crawl-scope constraint.
- **source_documents:** decisions-log 2026-05-15 "Style register locked"
- **status:** DOCUMENTED
- **engine_surface_affected:** export (asset packaging)
- **bc_axis_affected:** none directly (visual, not mechanical)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** none

---

**LC-052**
- **constraint_name:** Perception asymmetry constants — tuning-drift discipline (Discipline #16)
- **description:** `ENEMY_AOE_APPARENT_RATIO` [1.08, 1.18] and `PLAYER_AOE_APPARENT_RATIO` [0.85, 0.93] are gandalf-authoritative constants with a fail-loud guard (`_validate_constants()` raises ValueError at module load if outside bounds). Both Python and TypeScript versions must remain byte-identical on constant values.
- **source_documents:** `engineering-disciplines.md` § 16; `canonical/story/asymmetric-perceived-aoe-radius-briefing-2026-05-17.md` § 7.1 + § 8
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / demo
- **bc_axis_affected:** Axis 1 (engagement profile — AOE radius affects range component measurement); Axis 2 (damage geometry — AOE radius thresholds use actual hitbox, not apparent radius)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; BC Axis 2 geometry measurement uses actual skill `aoe_radius` (hitbox), not apparent radius — the asymmetry constants affect player feel at the demo layer, not the BC measurement
- **dependencies:** none

---

**LC-053**
- **constraint_name:** Body-swap gear rules — three paths with distinct gear outcomes
- **description:** Three body-swap paths: Doppelganger victory (keep yours + gain doppelganger's), Trial body-swap (lose yours + gain boss's equipped), Death body-swap (lose yours + start with L1 default). Smart-loot invariant preserved (boss gear is embodiment-appropriate). These create distinct progression risk/reward gradients.
- **source_documents:** decisions-log 2026-05-08 "Spirit-swap and form library framing"; `canonical/37-form-bias-diagnosis-and-recovery.md` § 8
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / generation (gear generation)
- **bc_axis_affected:** Axis 4 (defensive profile — different gear loadouts affect eHP); Axis 5 (resource economy — gear affixes affect resource patterns)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** none

---

**LC-054**
- **constraint_name:** Divergence floor constraint — ≥2 differing axes per archetype-mate pair
- **description:** Per the multi-dimensional divergence framework (decisions-log 2026-05-16), the engine must produce ≥2 differing values across 6 player-behavior axes for any two archetype-mates within the same class lineage. Divergence floor: geometry mix / resource regen pattern / sustain expenditure / target prioritization / range engagement profile / cooldown rhythm.
- **source_documents:** decisions-log 2026-05-16 "View A locked — multi-dimensional divergence framework" (Lock 2)
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / simulation
- **bc_axis_affected:** cross-cutting (divergence floor is complementary to BC cell-address uniqueness)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; MAP-Elites cell-address uniqueness in the QD archive is the stronger structural enforcer of divergence (each cell captures ONE archetype); divergence floor is a within-season generation gate
- **dependencies:** none

---

**LC-055**
- **constraint_name:** Canonical-four as resistance-cipher only (Position ii locked)
- **description:** The canonical four (fire/water/earth/wind) are used purely as a fixed-size resistance-cipher key, NOT as mechanical-signature archetypes. Per-season vocabulary carries its own mechanical signatures. The cipher's job is narrowed to resistance-translation only.
- **source_documents:** `canonical/37-form-bias-diagnosis-and-recovery.md` § 6.2; decisions-log 2026-05-16 "Form-bias architecture — three-layer model"
- **status:** DOCUMENTED
- **engine_surface_affected:** generation (architecture locked; implementation pending cipher migration)
- **bc_axis_affected:** cross-cutting (affects how mechanical signatures are assigned to elements, which feeds all BC axes)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE (Position ii is architectural; implementation via Stage 3 cipher migration is still ahead)
- **dependencies:** LC-006, LC-012

---

**LC-056**
- **constraint_name:** Experimental classes bypass recompose loop
- **description:** Experimental classes (those that don't match known archetype labels) are marked `skipped_experimental` and bypass the B14.5 primary recompose loop. This is intentional — experimental kits get high variance via wider role pool and adding trait variance complications complicates archetype-emergence observability signal.
- **source_documents:** decisions-log 2026-05-12 "Trait architecture — dual-source design" (experimental classes note); decisions-log 2026-05-12 "B14.5 hybrid rejection gate" (skipped_experimental outcome)
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** all (experimental classes have lower convergence quality, affecting BC measurement reliability for those kits)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; DOCUMENT that experimental-class kits in the QD archive may have less reliable BC measurements than labeled-archetype kits; consider routing them to deferred-evaluation pool per BC axes lock pattern
- **dependencies:** LC-001

---

**LC-057**
- **constraint_name:** B10.4 multi-dimensional divergence ceiling — per-class WR ≥ 25% per content type
- **description:** Per the divergence ceiling lock (decisions-log 2026-05-16), per-class win rate against EACH content-type slot (swarm/magic/trash/elite/mini-boss/boss/trial) must be ≥ 25%. Below = "helpless" against that content. This is a validation constraint on which kits are permitted in the archive.
- **source_documents:** decisions-log 2026-05-16 "View A locked — divergence ceiling" (Lock 2)
- **status:** DOCUMENTED
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (divergence ceiling filters which kits populate the archive)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** LC-020

---

**LC-058**
- **constraint_name:** B9 per-band SP allocation deferred — A1/A2 diagnostic-only
- **description:** Full per-band convergence (A1/A2 as separate convergence targets) requires B9 per-band SP allocation which has not yet shipped. Until B9 ships, A1/A2 produce diagnostic-only reports. Archive kits are calibrated to A3 endgame only.
- **source_documents:** decisions-log 2026-05-13 "B10 V1" (D2 per-band convergence deferred); `canonical/28-engine-arpg-rebalance-design.md` § B9
- **status:** DOCUMENTED (B9 deferred, A1/A2 diagnostic explicitly)
- **engine_surface_affected:** simulation / balance_loop
- **bc_axis_affected:** cross-cutting (per-band convergence affects modifier calibration quality)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE as current architecture; note that QD archive kits are A3-calibrated; A1/A2 calibration improves once B9 ships
- **dependencies:** LC-020

---

**LC-059**
- **constraint_name:** IDC meta-principle default — season theme coalesced post-convergence
- **description:** The IDC (Information-Deferred-to-Coalescence) meta-principle is the canonical architectural target. Theme discovery via LUCB1 Best-Arm Identification (BAI) is specified for Profile B; Profile A uses simpler discovery. R8 inverted-mode is the default since engine-rebuild. The principle extends to role orientation, substrate identity, and element identity as potential IDC candidates (not committed).
- **source_documents:** `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` § 5; `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md` R8 workstream
- **status:** DOCUMENTED
- **engine_surface_affected:** generation / llm
- **bc_axis_affected:** cohesion-BC (IDC coalescence affects theme coherence scoring)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE as the architectural default
- **dependencies:** LC-042

---

**LC-060**
- **constraint_name:** Trait architecture — skill-specific traits on gear prohibited
- **description:** Gear-affix rolls cannot include skill-specific traits (only element/mechanic-gated traits). This is because skill IDs are season-specific; element/mechanic categories are stable across seasons. Cross-season gear smuggling would produce trait effects pointing to non-existent skills.
- **source_documents:** decisions-log 2026-05-12 "Trait architecture — dual-source design"
- **status:** DOCUMENTED
- **engine_surface_affected:** generation (gear generation)
- **bc_axis_affected:** Axis 5 (resource economy — trait affixes affect resource dynamics marginally)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE
- **dependencies:** none

---

**LC-061**
- **constraint_name:** Mage range constraint extension candidates (earth_caster, wind_caster, controllers) unresolved
- **description:** During B6 resolution, ARCHETYPES_FORBIDDEN_CLOSE_RANGE was added for fire_mage/water_mage. Extension candidates (earth_caster, wind_caster, all controllers) were surfaced as "deferred design questions." The B14.5 sidecar finding #5 confirmed close-range controllers exist (earth/fire/wind). The question of whether these should be forbidden from close-range is unresolved.
- **source_documents:** decisions-log 2026-05-12 "B6 generator-validated — KI-B6-1 resolution" (extension candidates); `memory/project_b14_5_sidecar_analyses.md` finding (5)
- **status:** ABLATION-CANDIDATE (suspected that close-range controllers affect convergence but no direct evidence)
- **engine_surface_affected:** generation
- **bc_axis_affected:** Axis 1 (engagement profile — close-range vs ranged bin assignment for controllers)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** ABLATE (run Discipline #13b experiment: compare controller convergence with and without close-range constraint; measure effect on doppelganger gate pass rates)
- **dependencies:** LC-013

---

**LC-062**
- **constraint_name:** AGI stat — dead/reserved column
- **description:** The `agi_stat` column in `telemetry/migrations.py:110` is reserved for a future AGI/dodge/initiative mechanic and is not currently populated. Removing it would break existing tooling; leaving it is zero-cost and preserves schema intent.
- **source_documents:** decisions-log 2026-05-09 "AGI stat — dead/reserved"
- **status:** DOCUMENTED
- **engine_surface_affected:** telemetry
- **bc_axis_affected:** Axis 4 (defensive profile — AGI/dodge would affect avoidance_rate measurement when implemented)
- **qd_rebuild_risk:** LOW
- **recommended_disposition:** PRESERVE; when Axis 4 dodger bin is fully implemented (iframes + evasion), revisit whether AGI stat should be populated from skill metadata
- **dependencies:** LC-024

---

*End of constraint inventory. 62 constraints total.*
