# Phase 2 Code-Side Verification — QD-Engine Rebuild W0.4
# Consolidated Multi-Seam Deliverable

**Date:** 2026-05-21
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-rocket-plus-gamora-plus-star-lord-w0-4-specialist-code-audit.md`
**Status:** star-lord section COMPLETE; rocket + gamora sections PENDING (append when complete)
**Jack-ryan review:** PENDING (after all 3 seam sections appended)

---

## Star-Lord Section (Telemetry / Export / LLM Seam)

**Author:** star-lord
**Seam tag:** `star-lord/v1.15-w0-4-code-side-audit-1`
**Full deliverable:** `agentic_orchestration/star-lord/research/qd-rebuild-w0-4-star-lord-code-side-audit.md`

### LC Verdicts — Star-Lord Seam

| LC | Constraint | Verdict | Key File:Line |
|---|---|---|---|
| LC-006 | Canonical-four LLM exposure | RESOLVED (star-lord seam) | `llm/naming.py:74-95` (cipher live, test-guarded) |
| LC-007 | Humanoid gear schema in export | VERIFIED (not yet fixed) | `export/schemas.py:88-89`; `telemetry/migrations.py:_V1_6` |
| LC-003 | Modifier floor-lock telemetry gap | DRIFT-FROM-AUDIT | `floor_lock_recompose/working_modifier/floor_lock_detected` absent from schema and recorder |
| LC-008 | STR/DEX/INT in LLM prompt | NEEDS-DOWNSTREAM-FIX | `llm/naming.py:323` stats.as_dict() in name_class prompt |

### W1.13 ArchiveEntry Schema-Extension Scope

None of the W1.13 ArchiveEntry fields (`node_subset`, `per_node_coefficients`, `scalar_modifier`, `bc_coordinate`, `per_tier_WR`, `cohesion_theme`, `visual_identity`) exist in the star-lord seam. Requires new `archive_entries` table (not an extension of existing tables). Matt authorization required for DB migration. Export schema change not needed until P3.

### W0.8 `bounce_count` + `spawn_count` Scope (P1 W1.1)

Clean additive extension: 2 nullable columns on `abilities` table. 4 files, ~20 lines, no round-trip breakage. Matt authorization required for DB migration.

### v2.12 + v2.13 Schema Status

Both LIVE as of 2026-05-19 production DB apply. No drift.

### Recompose-Hive P1 Fields

`floor_lock_recompose`, `working_modifier`, `floor_lock_detected` are specced in gamora's `simulation/MIGRATION.md` but absent from star-lord telemetry schema and recorder. This is a P1-priority cross-seam gap — if gamora ships Option B before star-lord adds the columns, these fields will be silently dropped. Routed to knight-rider for P1 dispatch scoping.

### MEDIUM-Risk LCs — Quick Verdict Table (Star-Lord Touches)

| LC | Star-Lord Touch? | Status |
|---|---|---|
| LC-013 | No | rocket seam only |
| LC-015 | No | gamora seam only |
| LC-016 | No | gamora seam only |
| LC-017 | Partial (no pack-fight tag column) | W0.9 follow-on item |
| LC-018 | No | generation/gamora seam |
| LC-019 | Confirmed absent | consistent with deferred status |
| LC-020 | Schema ready (per-tier WRs recorded) | consistent with A3-primary design |
| LC-021 | Schema ready (observed_movement_speed NULL) | upstream unblocked; schema live |
| LC-022 | canonical-7-ready (D6 Coupling #9 live) | ready for substrate expansion |
| LC-023 | No fight-context discriminator column | P0/W0.9 follow-on item |
| LC-024 | No | gamora seam |
| LC-025 | No | generation/gamora seam |
| LC-026 | base_mana column queryable for bug evidence | empirical jack-ryan DB query |
| LC-027 | No | gamora/generation seam |
| LC-028 | No word-count validation at write boundary | acceptable for current scope |
| LC-030 | No cost_type column on abilities | P1 substrate enrichment scope |

---

## W0.4 Rocket Portion (Generation Seam; 2026-05-21)

**Author:** rocket
**Seam tag:** `rocket/v1.23-w0-4-code-side-audit-1`
**Full deliverable:** `agentic_orchestration/rocket/research/qd-rebuild-w0-4-rocket-code-side-audit.md`

### LC Verdicts — Rocket Seam

| LC | Constraint | Verdict | Key File:Line |
|---|---|---|---|
| LC-001 | Archetype template hardcoded dict | DRIFT-FROM-AUDIT (positive — D3 composition live) | `b6_archetype_templates.py:290-305`; `archetype_composer.py` (D3 Path-a, tag `gamora/v1.4-d3-path-a-impl-1`) |
| LC-002 | Fire selection bias | VERIFIED (structural presupposition confirmed; ablation not yet run) | `selector.py:601-609` (allow-list 2× weight); `b6_archetype_templates.py:36-46` (ELEMENT_AFFINITY) |
| LC-006 | Canonical-four LLM exposure | SUBSTANTIALLY-RESOLVED (test coverage gap outstanding) | `selector.py:65-73` compliant; `selector.py:663-674` `fire_slot` keys in example JSON (architecturally acceptable per W0.6; test not yet extended to `_build_prompt()` output); `library_generator.py:84` non-issue (one-time setup) |
| LC-007 | Humanoid gear schema | VERIFIED (not yet fixed; deferred P4 W4.1) | `gear_schema.py:29-34, 131-177, 198-216`; `gear_catalog.py:12-42` |
| LC-008 | STR/DEX/INT math-bearing labels | NEEDS-DOWNSTREAM-FIX (star-lord `naming.py:323` is the actionable site; rocket-side `can_equip()` is math-bearing and clean) | `gear_generation.py:263-315` |
| LC-012 | Foundation validator | RESOLVED (W0.3 work; commit `3e428ae`; no drift) | `foundation/foundation.py:39-65` |

### LC-001 — Archetype Template Structural Inventory (W0.2 Prerequisite)

The hardcoded-14-template architecture was replaced by D3 Path-a (on-boot composition from SubstrateIdentity × Role). Current state:

**ArchetypeTemplate fields:** `archetype_tag`, `kit_min/kit_mode/kit_max` (triangular), `aoe_share_min/max`, `dominant_share/secondary_share/tertiary_share`, `chain_count_min/max`, `tier_depth` (3=generalist / 4=specialist), `cross_chain_rule` (STRICT/FLEXIBLE), `required_roles` (list of (role, count)), `geometry_bias` (name→multiplier), `energy_type`, `skill_power_tier`, `special_constraints`.

**Composition count:** 23 total templates in `ARCHETYPE_TEMPLATES` (18 composed elemental + 5 physical hardcoded). hybrid_mage RETIRED 2026-05-18.

**Role × substrate matrix:** burst_damage → `_mage`; area_damage → `_caster`; control → `_controller`. Aliases: fire/water burst=area share same tag (fire_mage, water_mage). earth/wind burst = earth_burst, wind_burst (distinct from caster). All 7 canonical substrates × 3 roles populated.

**BC-target implicit assumptions:**
- All elemental: `energy_type="mana"`, `skill_power_tier=50`
- Physical warrior/grappler: `energy_type="rage"`, `skill_power_tier=65`
- Hunter/skirmisher/rogue: `energy_type="focus"/"combo"`, `skill_power_tier=58`

**W0.2 notes:** Physical hardcoded templates carry role-specific geometry constraints (`require_cleave`, `require_escape_mobility`, `require_2_mobility`) not expressible via substrate-identity × role formula. These are W0.2's most structurally resistant surface.

### § 2.8 W1.13 Current-State Verification

**Skill-tree-node infrastructure is FULLY ABSENT from generation seam.** No `SkillTreeNode`, `TreeNode`, `node_subset`, `per_node_coefficients`, `bc_coordinate`, or any tree-node concept in `b6_kit_builder.py`, `class_generator.py`, or `b6_archetype_templates.py`. Kit builder operates on flat `_SlotPlan` list (tier/chain/role/element). W1.13 requires building NEW generation-side infrastructure to produce `ArchiveEntry`-compatible kit descriptions with node_subset + per_node_coefficients fields — no modifications to existing classes.

### OQ-2 — chain_lightning Boss Multi-Hop

chain_lightning uses geometric-series fan-out model: total multiplier = `(1 - decay^(n+1)) / (1 - decay)`, default n=3 arcs, decay=0.7 → ~2.76× (`damage_resolver.py:323-337`). In solo-sim (1v1), all arc hits resolve on the single boss defender — full multiplier applied. Not bin-limited. Key caveat: solo-sim OVER-estimates chain_lightning boss damage vs multi-target environments where arcs would hop to nearby enemies. File: `damage_resolver.py:325-337`.

### OQ-3 — 5-Skill Kit Generation Anomaly

No hard 5-skill floor in code. Kit size is triangular-sampled from `(kit_min, kit_mode, kit_max)` per template (`b6_kit_builder.py:129-135`), minimum kit_min=10 for all current templates. `_plan_tier_counts()` (lines 312-346) allocates via band constraints; last tier gets remainder clamped to band. If a 5-skill kit was observed in Alt A spot-checks, it is not reproducible from current templates (kit_min=10 prevents it). This anomaly may have been from a legacy template state or test fixture. File: `b6_kit_builder.py:312-346`.

### MEDIUM-Risk LCs — Rocket Seam Quick Verdicts

| LC | Verdict |
|---|---|
| LC-013 | VERIFIED — `ARCHETYPES_FORBIDDEN_CLOSE_RANGE = {fire_mage, water_mage}` at `b6_archetype_templates.py:343-347`; earth_caster/wind_caster not in list (acknowledged asymmetry) |
| LC-014 | FORMALLY-DEFERRED per W0.6; Q4 syllable-cap gate active; Q2 `{word}-bolt` unamended |
| LC-018 | VERIFIED as DOCUMENTED — all elemental archetypes energy_type="mana"; structural homogeneity confirmed |
| LC-022 | DRIFT-FROM-AUDIT (positive) — D3 composition generates lightning/holy/shadow templates at boot; 11 new tags present |
| LC-025 | VERIFIED ABSENT — no charge-stack or CWDT-style skill generation in ability_grammar.py or b6_kit_builder.py |
| LC-026 | DRIFT-FROM-AUDIT (positive) — mana bug RESOLVED; `combatant.py:362-375` branches correctly on energy_type |
| LC-028 | VERIFIED — single-word rule enforced in `selector.py:658` in `_build_prompt()` rules block |
| LC-030 | VERIFIED ABSENT — no `hp_cost` or `cost_type` in generation seam; HP-economy Axis 5 bin will be empty |

### Cross-Seam Contract Notes

- LC-001 D3 tag expansion: 23 tags in `ARCHETYPE_TEMPLATES` vs prior 13. Telemetry queries enumerating hardcoded archetype tags need updating. No MIGRATION.md entry filed for the tag expansion — gamora/star-lord awareness item.
- LC-006 test coverage: W0.6 action item outstanding — add `_build_prompt()` user prompt coverage assertion to `tests/test_no_canonical_four_in_llm_prompts.py`. Rocket seam owns this addition.
- LC-007 gear schema → drax: Position C migration requires Loadout schema changes surfacing in reincarnated-loadout/ (drax seam). MIGRATION.md + Discipline #15 UI decomposition required when P4 W4.1 dispatch fires.

### New HIGH-Risk LC Discovery

None. No phase-halt triggered.

---

## Gamora Section (Simulation Seam)

**Status: PENDING — gamora to append**

---

## Jack-Ryan Review

**Status: PENDING — after all 3 seam sections present**

---

## W0.6 Drift Candidate Dispositions (jack-ryan; 2026-05-21)

**Author:** jack-ryan (drift-discipline owner per Discipline #13a)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-multi-seam-w0-6-drift-candidate-closures.md`
**Date:** 2026-05-21
**Status:** COMPLETE — all 4 LCs dispositioned; tag fired `qd-rebuild/v0.6-drift-closures-partial` (gandalf-review-pending on LC-006)

---

### LC-006 — Canonical-four element labels universally exposed to LLM

**Disposition:** (c) FORMAL-DEFER-TO-DOWNSTREAM — but with PARTIAL RESOLUTION noted. Cipher migration is substantially complete at both seams; residual `library_generator.py` exposure is a one-time-setup script, not per-season LLM generation.

**Owner seam(s):** rocket (generation / element selector) + star-lord (llm/naming.py — already RESOLVED)

**Decision rationale:** Star-lord audit confirmed `llm/naming.py` is fully migrated (cipher live, test-guarded at `tests/test_no_canonical_four_in_llm_prompts.py`). Direct code inspection of rocket's remaining flagged sites confirms the Stage 3 migration is also live in `element/selector.py`:

- **Lines 43-47** (original audit concern): the `_get_valid_slots()` function at lines 43-56 is internal routing logic only — canonical-four labels are routing keys, NOT LLM-visible prompt content. The Stage 3 note at lines 74-79 explicitly documents this separation.
- **Lines 65-73** (`_SYSTEM_PROMPT`): uses grouping-layer abstract labels (ignition / suffusion / bulwark / displacement), NOT canonical-four. Confirmed compliant.
- **Lines 394-446** (`_score_word()`): Q7 at lines 442-448 references canonical-four labels as an audit-flag-only check string — it is a rubric question presented to the LLM, not an internal-schema exposure. The canonical-four names appear in a question about word similarity, which is a legitimate rubric use case (the question probes for over-proximity to canonical labels, helping FLAG them for demotion). This is Discipline #14 compliant; it is not a "hide canonical-four from LLM" violation but rather uses them to check for leak-risk in candidate words.
- **`canonical/library_generator.py:85`** (line 84 in current code): `"Element: {element}"` exposes canonical-four labels in the user prompt of `_generate_entry()`. HOWEVER, `library_generator.py` is a **one-time project-setup script** (not per-season generation), runs with `force=False` guard, and generates the canonical library that is loaded from disk for all subsequent seasons. This is not Discipline #14 drift in the per-season-generation sense. The canonical library itself carries canonical-four labels by design (they ARE the canonical layer); exposing them to the LLM to generate canonical names is structurally appropriate. No remediation needed for this site.

**Net finding:** The drift that LC-006 originally documented — per-season LLM prompt construction exposing canonical-four labels — is RESOLVED across both seams. The remaining `library_generator.py` site is a structural non-issue (one-time canonical layer generation, not per-season).

**Formal deferral for remaining D3 work:** The **cipher migration's cohesion-BC integration** (D3: cohesion-BC sequenced post-cipher migration per hive activation dispatch § 1.2) remains ahead. Under substrate-as-cohesion-only (supplement 2026-05-21), the cohesion-BC archive's correctness depends on per-season vocabulary being genuinely alien, not defaulting to canonical-four echo. The test guard at `tests/test_no_canonical_four_in_llm_prompts.py` is the load-bearing enforcement; rocket must verify this test covers `selector.py` prompt construction sites as well as `naming.py`.

**Action items:** None blocking. Rocket W0.4 section should confirm test coverage extends to `selector.py` prompt construction path. If test currently only covers `naming.py`, add a coverage assertion for `_build_prompt()` output.

**Deferral target:** D3 cohesion-BC integration — post-P3 per hive-mind protocol § 6.1.2 W0.6. Cross-ref: hive activation dispatch § 1.2 D3; `canonical/story/form-bias-cadence-strategy.md` § 7 Stage 3.

**Critique-pair status:** gandalf reviewed: **PENDING** (see flag below); jack-ryan reviewed: YES

**Status:** SUBSTANTIALLY-RESOLVED — per-season LLM exposure sites confirmed clean; formal deferral of D3 cohesion-BC integration; rocket to confirm test coverage extension.

**gandalf review pending:** Under substrate-as-cohesion-only architecture (supplement 2026-05-21 § 1.2), the cohesion-judge assigns substrate/element/theme post-generation based on mechanical signature. If per-season vocabulary is LLM-generated and the cipher is now working correctly (canonical-four hidden), does the cohesion judge still receive per-season vocabulary as input, or does it reason purely from mechanical signature? Specifically: is there any remaining design risk that the cohesion layer re-introduces canonical-four echo via the cohesion-judge's own prompt context? This question affects whether D3 requires a second cipher-style migration at the cohesion-judge layer, or whether the substrate-as-cohesion-only architecture dissolves the concern entirely.

---

### LC-007 — Humanoid-presupposing gear schema

**Disposition:** (c) FORMAL-DEFER-TO-DOWNSTREAM

**Owner seam(s):** rocket (gear schema + gear_catalog) + star-lord (export packets)

**Decision rationale:** Star-lord W0.4 audit confirmed `export/schemas.py:88-89` carries slot/handedness humanoid values and `telemetry/migrations.py:_V1_6` anchors the schema. The Position C migration (slot-as-functional-mechanic + embodiment-as-narrative-skin, per `canonical/37-form-bias-diagnosis-and-recovery.md` § 4) is locked in canonical docs but not yet shipped. Under substrate-as-cohesion-only (supplement 2026-05-21), the gear schema's humanoid presupposition is a Cluster A structural issue, NOT a cohesion-layer issue — gear schema shapes mechanical kit generation. The disposition decision is: the migration is multi-seam coordinated work (rocket schema refactor + star-lord export schema update + drax/loadout UI decomposition per Discipline #15) that cannot land safely in W0.6 without its own dedicated dispatch, MIGRATION.md per ADR-004, and round-trip smoke per R11(b). Deferral is correct per-dispatch-scope discipline.

**Action items:** None in W0.6. Downstream dispatch authoring (rocket + star-lord + drax) must include: MIGRATION.md cross-seam contract change entry; Discipline #15 UI scope decomposition for loadout slot relabeling; round-trip smoke per R11(b).

**Deferral target:** P4 W4.1 (player-side proxy support enabling non-humanoid embodiments) + Stage 1 form-bias migration (embodiment-axis schema per `canonical/story/form-bias-cadence-strategy.md` § 7 Option II Stage 1). Cross-ref: hive-mind protocol § 6.1.2; dispatch framing in W0.6 dispatch § "LC-007."

**Critique-pair status:** gandalf reviewed: NO (thematic implications of Position C migration framing during deferred period are low-urgency; no gandalf flag required for this deferral); jack-ryan reviewed: YES

**Status:** OPEN — formally deferred; no blocking action items in W0.6.

---

### LC-014 — D1 element-name pool humanoid-fantasy selection bias (Flag A + three-level drift)

**Disposition:** (c) FORMAL-DEFER-TO-DOWNSTREAM

**Owner seam(s):** rocket (element/selector.py rubric at lines 282-296 in original audit / Q1-Q7 in current code)

**Decision rationale:** LC-014 carries MEDIUM QD-rebuild risk and has three distinct drift levels: (1) pool content selection bias, (2) status assignment methodology, (3) rubric sub-properties embedding humanoid-fantasy compounding via Q2 and Q4. The decisions-log 2026-05-16 "four form-bias sub-locks" explicitly deferred D1 reconsideration to catalogue-track sub-locks. Two additional facts sharpen the deferral:

First, the D1 rubric has been amended since the original audit. Code inspection shows Q4 now carries a `_Q4_SYLLABLE_CAP` gate (polysyllabic words get a cosmological-usage test instead of the `{word}-Knight/{word}-Mage` compound check), which directly addresses the humanoid-fantasy compounding concern the audit raised. Q7 (canonical-pair-leak audit flag) is now present as an audit-only signal — it does not gate or demote, but surfaces words that echo canonical-four labels, directly enabling future catalogue-track sub-lock decisions.

Second, LC-014's dependency chain (`LC-006` + `LC-012`) is now largely resolved: LC-006 is substantially resolved (per above); LC-012 (Foundation validator) is handled in W0.3 per D5. The rubric's residual humanoid-fantasy compounding in Q2 (`{word}-bolt` / `{word}-armor`) remains unamended, but under substrate-as-cohesion-only, the element pool shapes per-season cohesion vocabulary — not mechanical generation. The BC measurement risk is LOW (per inventory: "affects LLM vocabulary, not mechanical BC measurements"). Deferral does not block QD archive filling.

The recommended Flag A ablation (run D1 rubric on non-humanoid-cosmology candidate words; measure systematic under-scoring) remains the correct next action. This is an empirical experiment per Discipline #13b, not a code change — it belongs in a targeted experiment dispatch, not W0.6.

**Action items:** None in W0.6. Flag A ablation experiment should be scoped as a follow-on dispatch when catalogue-track sub-lock milestones approach. Q2 (`{word}-bolt` / `{word}-armor`) humanoid compounding remains unamended; note for future rubric iteration.

**Deferral target:** Catalogue-track sub-lock milestones per decisions-log 2026-05-16 "four form-bias sub-locks" + `canonical/story/form-bias-cadence-strategy.md` Stage 3 cipher migration follow-on (pool may require structural rebuild post-cipher). Cross-ref: LC-006 disposition above; LC-012 W0.3 resolution.

**Critique-pair status:** gandalf reviewed: NO; jack-ryan reviewed: YES

**Status:** OPEN — formally deferred; Q4 syllable-cap amendment is a partial implicit mitigation; Q2 remains unamended but LOW risk in current operational context.

---

### LC-028 — Single-word rule for element names constrains seasonal vocabulary

**Disposition:** (b) REVISE-CANONICAL-DOC — scoped to clarifying architectural ambiguity only; no code change required.

**Owner seam(s):** rocket (element/selector.py) + star-lord (element pool pipeline)

**Decision rationale:** LC-028 is a documented architectural ambiguity, not a code-vs-intent drift. The decisions-log 2026-05-07 single-word rule was authored before the three-layer model (L1 engine substrate / L2 Reincarnated cosmology / L3 per-season content) was codified. Direct code inspection confirms the rule IS already enforced in `selector.py`'s LLM output rules: `_build_prompt()` line 658 specifies `"Names must be single words (hyphens OK; no spaces)"` in the LLM instruction block. The enforcement is active for D1 allow-list pool entries AND for the LLM's in-session proposals.

The ambiguity LC-028 correctly surfaces is: does the single-word rule apply to per-season vocabulary-layer words generated by the cipher architecture? Under substrate-as-cohesion-only (supplement 2026-05-21) and the three-layer model (`canonical/story/form-bias-cadence-strategy.md` § 1.3), L3 per-season vocabulary is LLM-generated via the grouping-layer/cipher architecture — it is NOT sourced from the D1 pool. The question is whether the single-word constraint should propagate to L3 vocabulary, or whether L3 vocabulary operates under different constraints (per-season names that are more expressive compound labels like "deep-current" may be legitimate at L3).

This is a design decision, not a code fix. The correct disposition is (b): the canonical documentation (decisions-log 2026-05-07 entry) should be clarified to explicitly scope the single-word rule to D1 allow-list pool entries and in-session proposals, and explicitly state whether the rule applies or does not apply to L3 cipher-generated per-season vocabulary. This clarification prevents LC-028 from becoming a blocking ambiguity when cipher migration dispatches ship.

Under (b), no code change is required. The rule as enforced in `selector.py` is correct for D1 pool scope. The decisions-log entry needs one sentence of scope clarification.

**Action items:**
- [ ] knight-rider: draft decisions-log entry clarifying single-word rule scope. Entry should state: (1) single-word rule applies to D1 allow-list pool and in-session LLM proposals; (2) explicitly resolve whether L3 per-season cipher-generated vocabulary is or is not subject to the same constraint; (3) cite `engine-generic-meta-structure.md` three-layer model as context. Matt approval not strictly required per ADR-002 (documentation clarification within jack-ryan approval authority) but decision (2) constitutes a design call that Matt should confirm if not already implicit in the three-layer model framing.

**Deferral target:** Not deferred — this is (b) REVISE-CANONICAL-DOC. Resolution should happen before cipher migration dispatches ship to prevent blocking ambiguity. Cross-ref: LC-014 deferral above (both affect vocabulary layer); `canonical/story/form-bias-cadence-strategy.md` Stage 3.

**Critique-pair status:** gandalf reviewed: NO; jack-ryan reviewed: YES

**Status:** OPEN — (b) action item: decisions-log entry scoping single-word rule. Low urgency; must land before cipher migration dispatch authoring.

---

## W0.6 Summary

| LC | Disposition | Seam(s) | Deferral target | Gandalf pending | Status |
|---|---|---|---|---|---|
| LC-006 | (c) FORMAL-DEFER + PARTIAL RESOLUTION | rocket + star-lord | D3 cohesion-BC integration / P3+ | YES | SUBSTANTIALLY-RESOLVED |
| LC-007 | (c) FORMAL-DEFER | rocket + star-lord | P4 W4.1 + Stage 1 form-bias | NO | OPEN |
| LC-014 | (c) FORMAL-DEFER | rocket | Catalogue-track sub-locks | NO | OPEN |
| LC-028 | (b) REVISE-CANONICAL-DOC | knight-rider (decisions-log) | Pre-cipher-migration-dispatch | NO | OPEN |

**Tag:** `qd-rebuild/v0.6-drift-closures-partial` — all 4 LCs dispositioned; gandalf-review-pending on LC-006 cohesion-judge prompt context question.

**Cross-seam follow-on work surfaced:**
- LC-006: rocket to confirm `tests/test_no_canonical_four_in_llm_prompts.py` covers `selector.py` `_build_prompt()` path
- LC-007: downstream dispatch requires MIGRATION.md (ADR-004) + Discipline #15 UI decomposition + R11(b) round-trip smoke
- LC-028: knight-rider decisions-log clarification entry (jack-ryan approval authority per ADR-002; Matt confirmation recommended on the L3 scope call)
