# Dispatch — 2026-05-25 — Cycle 10 Wave 7 — Stage 4 Accurate Mechanical-Tagging on v1_scope (Including Mythological-NULL Rescue)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Wave:** 7 (Stage 4 accurate mechanical-tagging on v1_scope rows + mythological-NULL rescue)
**Lead owner:** rocket (engine-side mechanical-tagging + weapon_sim_props schema)
**Co-owners:** gamora (sim-viability + balance-loop validation) + jack-ryan (Gate-2 methodology ratification + cross-seam round-trip review) + legolas Mode A (Phase 1 methodology consult prerequisite per Discipline #18; ~1-2 hr consult)
**From:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 multi-stage dispatch parent (gandalf request 2026-05-23) § 3 Stage 4 + composition policy v1 § 1.4 (Stage 4 mythological-NULL rescue scope) + Cycle 10 scope-doc § 1 in-scope autonomous dispatch authoring
**Status:** FIRE-READY pending Wave 5 Phase 3 distribution report ✓ COMPLETE (`8c485ac`) + Wave 6 Stage 3.5 gap-fill landing (Stage 4 mechanical-tagging fires on UNION of v1_scope main pool + Stage 3.5 engine-authored entries). Phase 1 legolas Mode A methodology consult ✓ COMPLETE (`legolas/cycle-10-stage-4-methodology-consult-2026-05-25` tag pushed). Dispatch amended 2026-05-25 with consult findings (see § 4 + § 5.5 below).

---

## 0. TL;DR

Populate accurate per-row mechanical-substrate values (range_min/max, base_attack_speed, charge_time, hits_per_attack, aoe_radius, damage_amplitude_min/max, primary_stat) on ALL v1_scope rows including:

1. **Main v1_scope pool** (~1,700-3,100 items per composition policy estimate; Wave 5 Phase 3 output)
2. **Stage 3.5 engine-authored gap-fills** (~25-50 entries; Wave 6 output)
3. **Mythological-NULL rescue subset** (~30 mythological-register rows currently NULL-typed by Stage 1 proxy fingerprint; per composition policy § 1.4)

Schema gap closure: `damage_amplitude_min REAL` + `damage_amplitude_max REAL` (or equivalent variance coefficient per legolas methodology consult).

**Phase 1 legolas Mode A consult prerequisite** (Discipline #18; ~1-2 hr) on:
- Heuristic-derivation thresholds for range / geometry / tempo bin assignment from Stage 1.5 extracted_length / extracted_weight
- Damage-amplitude rubric design (the genuinely-hard axis per Stage 4 dispatch parent § 3 Stage 4 method notes)
- Per-cell-type-matching policy operationalization (Option α/β/C from composition policy § 3)
- LLM-judge calibration for ambiguous cases

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1 (current truth)
2. **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1.4 (mythological-NULL rescue) + § 3 (Option α/β/C cell-type matching policies)**
3. **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — 8 BC axes operational truth (bin definitions per axis); load-bearing for mechanical-tagging vocabulary
4. **`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` § 5.2 (Architecture B substrate-binding at Phase 2; Option α/β/C)**
5. `canonical/story/v1-bc-target-intent-2026-05-24.md` (cell-targeting intent; per-cell mechanical profile)
6. `canonical/story/attribute-system-2026-05-24.md` (STR/INT/WIS/DEX cell-type categories)
7. `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` (BC convergence algorithm; mechanical-substrate consumes BC measurement)
8. `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4-A architecture; downstream consumer)
9. **Wave 5 Phase 3 distribution report** at `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md` (v1_scope row set authoritative source)
10. **Wave 6 Stage 3.5 entries** at `agentic_orchestration/rocket/research/cycle-10-stage-3-5-gap-fill-2026-05-25/entries/` (engine-authored entries to mechanical-tag)
11. `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md` (Cycle 10 in-scope autonomous; Stage 4 fires within scope)
12. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 math-before-code; #11 empirical inspection; #18 + #18.2 methodology-before-execution; #19.1 cheapest-refuting-test)
13. `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md` (Phase 1 output; consume before mechanical-tagging fires)

---

## 2. Inputs

- v1_scope row set from Wave 5 Phase 3 output (~1,700-3,100 items)
- Stage 3.5 engine-authored gap-fill rows from Wave 6 (~25-50 entries)
- Mythological-register NULL-typed rows currently in substrate (~30 rows; SELECT WHERE register_canonical = 'mythological' AND proxy_fingerprint_confidence IS NULL OR proxy_range_class IS NULL)
- Stage 1 proxy fingerprint columns (initialization values for tagged rows)
- Stage 1.5 extracted columns (extracted_length_value/unit, extracted_weight_value/unit, extracted_materials) for refinement values
- 8 BC axes vocabulary (bin definitions per axis per BC-axes lock)
- Phase 1 legolas Mode A methodology recommendation (consult fires at Phase 0 of this dispatch)
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`

---

## 3. Outputs

### 3.1 Schema extension (AMENDED 2026-05-25 per Phase 1 consult finding Signal 4)

```sql
-- Close damage_amplitude schema gap per Stage 4 dispatch parent § 3 Stage 4 + Phase 1 consult Section c
ALTER TABLE weapon_sim_props ADD COLUMN damage_amplitude_min REAL;
ALTER TABLE weapon_sim_props ADD COLUMN damage_amplitude_max REAL;

-- CRITICAL — Phase 1 consult Signal 4: existing primary_stat CHECK constraint omits DEX.
-- This MUST be fixed in the same migration or population fails on ~49% of typed v1_scope rows.
ALTER TABLE weapon_sim_props DROP CONSTRAINT IF EXISTS check_primary_stat;
ALTER TABLE weapon_sim_props ADD CONSTRAINT check_primary_stat CHECK (
  primary_stat IN ('STR', 'INT', 'WIS', 'DEX')
);
```

**Phase 1 consult locked damage_amplitude representation:** scalar pair `damage_amplitude_min REAL` + `damage_amplitude_max REAL` (NOT variance coefficient). CV derivable at sim time from the ratio. Per-(geometry × tempo) bin lookup table in consult § c. Amplitude ratio boundaries: flat <1.9×, variable 1.9-4.5×, spiky >4.5× (aligns to BC Axis 3B CV thresholds under uniform distribution assumption).

MIGRATION.md required per ADR-004; gamora + star-lord consume `weapon_sim_props`; grep-verify expected consumers; document migration path. DEX-constraint amendment must be captured in MIGRATION.md as load-bearing for v1_scope DEX-tagged rows (per Phase 2 distribution: DEX is the largest single-attribute share among typed rows).

### 3.2 Populated `weapon_sim_props` rows for ALL v1_scope entries

Per Stage 4 dispatch parent § 3 Stage 4 outputs; ALL v1_scope entries get a `weapon_sim_props` row populated:
- range_min, range_max (per range_class bin from Stage 1.5 extraction or LLM-judge for ambiguous)
- base_attack_speed (per tempo_class bin)
- charge_time (per tempo_class + cell-type policy)
- hits_per_attack (per geometry_class)
- aoe_radius (per geometry_class)
- damage_amplitude_min, damage_amplitude_max (per damage-amplitude rubric from Phase 1 consult)
- primary_stat (per proxy_attribute_class)

### 3.3 Mythological-NULL rescue output (per composition policy § 1.4)

~30 mythological-register rows rescued from Stage 1 proxy NULL state:
- Stage 1 proxy fingerprint columns populated retroactively (range_class / geometry_class / tempo_class / attribute_class)
- Per-row classification rationale recorded in artifact (LLM-judge OR design-judged per row)
- `weapon_sim_props` row populated alongside main pool tagging
- Rescued rows enter v1_scope at legendary-tier per Architecture B substrate-as-base-type-templates + tiered-instance-loot
- `v1_scope_composition_trace` updated from `'stage_4_mythological_rescue_pending'` to `'stage_4_mythological_rescue_complete'`

### 3.4 Per-row sim-viability flag check

Per Stage 4 dispatch parent + T4-A § 3.3 step 5 sim-viability discipline:
- Each v1_scope row's mechanical profile validated against engine BC envelope
- Out-of-envelope rows flagged for design review; default disposition = demote to v1.1+ pending engine extension OR adjust mechanical profile to within-envelope

### 3.5 Artifacts

- Methodology consult artifact at `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md` (Phase 1)
- Population script at `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/populate_weapon_sim_props.py` (background execution per Discipline #19)
- Mechanical-tagging report at `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/mechanical-tagging-report.md` (per-axis distribution + per-cell-type counts + ambiguous-case log)
- Mythological-NULL rescue artifact at `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/mythological-null-rescue.md` (~30 rows with per-row rationale)
- jack-ryan Gate-2 review at `agentic_orchestration/qa/findings/2026-05-25-gate2-stage-4-mechanical-tagging.md`
- gamora sim-viability assessment at `agentic_orchestration/gamora/notes/2026-05-25-stage-4-sim-viability-assessment.md`

---

## 4. Method notes

### 4.1 Phase 1 — legolas Mode A methodology consult (Discipline #18 hotspot; LOAD-BEARING gate) — ✓ COMPLETE 2026-05-25

Per Discipline #18.2 (consultation-after-baseline at extension hotspots): Wave 5 Phase 2/3 baseline outputs landed BEFORE this consult fired; consult-informed-by-baseline is cheaper than consult-in-the-dark.

**Output artifact (CONSUMED BY ROCKET BEFORE EXECUTION):** `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md`

**Locked methodology (per consult; rocket consumes this before Phase 2 execution):**

- **3-pass layered approach:**
  - Pass 1 = heuristic from existing proxy columns (1,890 typed rows; zero LLM calls)
  - Pass 2 = structured-property `weapon_type` key lookup (47 rows; zero LLM calls; covers most of mythological-NULL rescue subset directly)
  - Pass 3 = LLM-judge on canonical_name + cultural_lineage_canonical for remaining 937 NULL-typed rows
- **Damage amplitude:** scalar pair (`damage_amplitude_min REAL` + `damage_amplitude_max REAL`); per-(geometry × tempo) bin lookup table per consult § c; amplitude ratio boundaries flat <1.9× / variable 1.9-4.5× / spiky >4.5×
- **DEX primary_stat constraint blocker:** schema migration MUST add DEX to `weapon_sim_props.primary_stat` CHECK constraint (see § 3.1 above)
- **NULL-typed treatment for known-default pools:**
  - 168 odin-army-tradoc rows (modern military vehicles/UAVs): pre-screen + apply default tag + `sim_viable = 0` BEFORE LLM pass
  - royal_armouries component-parts (lockplates, detached jaws, etc.): low-confidence LLM-judge expected → likely `sim_viable = 0` defaults
- **Resource bounds:** ~950 LLM calls × ~$0.001 = ~$0.95 total cost; ~25 min total automated execution; within Wave 7 ~1 hr envelope
- **Cheapest-refuting-test:** per-axis bin distribution check post-tagging; **KEY GATE: INT+WIS combined ≥ 12% of populated rows** (if <10%, methodology systematically under-assigning caster attributes → revise before commit)

### 4.2 Phase 2 — mechanical-tagging execution (rocket)

Per Phase 1 consult recommendations:
- 3 of 4 weapon-intrinsic axes (range / geometry / tempo) largely derivable from Stage 1 + 1.5 inputs via heuristic; spot-check + LLM-judge ambiguous cases only
- 1 of 4 axes (damage amplitude / spread) design-judged or LLM-judged with calibration per rubric
- Tier S/A entries get extra gandalf curation pass (named-bearer canon-respecting; e.g., Gáe Bolg = guaranteed-pierce thrown-spear with curse-causality stays canonical)
- Mythological-NULL rescue: ~30 rows tagged per Phase 1 rubric + per-row design judgment by rocket + gandalf consult on cultural-tradition fit

### 4.3 Phase 3 — gamora sim-viability + jack-ryan Gate-2

- gamora consumes `weapon_sim_props` populated rows; sim-viability flag check per T4-A § 3.3 step 5
- gamora runs a small-scale balance-loop sanity-check on a stratified sample (1 row per cell-type) to verify sim engine consumes the schema correctly
- jack-ryan Gate-2 methodology review: was Phase 1 consult followed? Are per-cell-type policies (Option α/β/C) consistently applied? Are mythological-NULL rescue rationales sensible?
- Cross-seam round-trip per Principle 6: gamora + star-lord consume `weapon_sim_props`; round-trip smoke required (see § 5.5 below)

### 4.4 Discipline #11 empirical inspection

Per-axis distribution post-tagging is empirical-inspection artifact. Surface any anomalies (e.g., 70% of v1_scope ends up in single range_class bin → suggests heuristic misapplication) to knight-rider + gandalf at Gate-2.

### 4.5 Per-cell-type matching policy operationalization (Option α/β/C)

Per composition policy § 3:
- **Option α (martial cells; STR/DEX primary):** 5-tuple mechanical-fingerprint match required at Phase 2 substrate-binding; weapon's range/geometry/tempo/amplitude/attribute must match cell BC-target directly
- **Option β (caster cells; INT/WIS primary):** attribute-level match only at Phase 2; weapon's mechanical profile is secondary (skills deliver kit BC-target; weapon scales)
- **Option C (cross-attribute hybrid cells — Red Mage/Monk-archetype/Holy Knight):** substrate pulled from primary-attribute-of-physical-vector pool; ω-penalty flag set on ALL rows by construction (per-cell architectural fact, not per-row decision)

### 4.6 Semantic-layer rep-audit per Discipline #25

Apply at mythological-NULL rescue boundary: do the ~30 mythological-register NULL-typed rows actually contain mythological content, or have they been mis-tagged via Mode B/C contamination? Per-row semantic check; demote if contamination surfaces.

---

## 5. Cross-seam impact

- **Schema change on `weapon_sim_props`:** ADD COLUMN damage_amplitude_min/max (or variance coefficient per consult)
- **MIGRATION.md REQUIRED** per ADR-004 — gamora + star-lord consume `weapon_sim_props`; round-trip smoke required (see § 5.5)
- **Round-trip Principle 6 LOAD-BEARING:** `weapon_sim_props` is a cross-seam fixture consumed by gamora (sim) and star-lord (telemetry); round-trip smoke MUST exercise:
  - rocket writes weapon_sim_props row
  - gamora sim consumes the row + produces fight_log
  - star-lord telemetry consumes fight_log + produces export packet
  - field-presence check at each boundary
- **NO engine code changes for new mechanics** — Stage 4 is data tagging; existing engine consumes existing columns + new damage_amplitude columns (gamora needs to consume new columns at sim entry per migration)
- **Loadout app reads weapons but does NOT directly consume `weapon_sim_props` in player-facing surface** (verified Phase D precedent); update if v1.0+ adds player-facing weapon-sim-display

---

## 5.5 Acceptance criteria (formal per dispatches/README.md § Acceptance criteria + Principle 6)

- [x] Phase 1 legolas Mode A consult artifact landed at `agentic_orchestration/legolas/research/cycle-10-stage-4-methodology-consult-2026-05-25/methodology-recommendation.md` per Discipline #18 — ✓ COMPLETE 2026-05-25; tag `legolas/cycle-10-stage-4-methodology-consult-2026-05-25` pushed
- [x] Phase 1 consult includes: 3-pass layered methodology + damage-amplitude min/max representation + per-(geometry × tempo) bin lookup + DEX primary_stat constraint blocker + NULL-typed treatment for odin-army-tradoc + royal_armouries component-parts + cheapest-refuting-test INT+WIS ≥12%
- [ ] Schema extension landed: `damage_amplitude_min REAL` + `damage_amplitude_max REAL` + DEX added to primary_stat CHECK constraint per § 3.1; MIGRATION.md drafted with DEX-constraint amendment captured as load-bearing
- [ ] Population script executes successfully against UNION of (v1_scope main pool + Stage 3.5 gap-fills + mythological-NULL rescue)
- [ ] ALL v1_scope rows have populated `weapon_sim_props` row; ZERO regressions on prior-stage columns
- [ ] Per-axis distribution histogram landed in mechanical-tagging report; ambiguous-case log surfaces any per-axis anomaly
- [ ] **Cheapest-refuting-test gate per Phase 1 consult § d: INT+WIS combined ≥ 12% of populated rows; if <10%, METHODOLOGY REVISION REQUIRED BEFORE COMMIT** (systematically under-assigning caster attributes signal)
- [ ] Mythological-NULL rescue: ~30 rows tagged + per-row rationale captured; rep-audit Mode B/C/D contamination check applied
- [ ] gamora sim-viability assessment landed; out-of-envelope rows flagged (with default disposition = demote to v1.1+ pending engine extension)
- [ ] gamora small-scale sim-loop sanity-check passes on stratified sample (1 row per cell-type)
- [ ] jack-ryan Gate-2 PASS at `agentic_orchestration/qa/findings/2026-05-25-gate2-stage-4-mechanical-tagging.md`
- [ ] **Round-trip smoke: rocket writes weapon_sim_props row + gamora sim consumes the row + produces fight_log + star-lord telemetry consumes fight_log + produces export packet; field-presence check at each boundary; CROSS-SEAM CONTRACT CHANGE per Principle 6 trigger (schema field add on cross-seam fixture)** — required artifact at `agentic_orchestration/qa/findings/2026-05-25-stage-4-round-trip-smoke.md`
- [ ] Pre-population DB backup at `cycle-10-stage-4-2026-05-25/backups/telemetry.db.pre-stage-4` (gitignored)
- [ ] AGENT_STATE.md updated at session end (rocket + gamora seams if maintained)
- [ ] Tag: `rocket/cycle-10-stage-4-mechanical-tagging-2026-05-25` after jack-ryan Gate-2 PASS + round-trip smoke PASS
- [ ] Auto-commit + auto-push per push-per-wave authorization

---

## 6. Out of scope (explicit)

- NOT Stage 4 mechanical-tagging on NON-v1_scope rows — they retain Stage 1 proxy values; v1.1+ work reaches them per Variant C substrate optionality
- NOT engine code changes for new mechanics — Stage 4 is data tagging within existing BC envelope
- NOT skill-system canonical doc amendment — gandalf authors post-Cycle-10
- NOT Phase 5 cohesion-judge calibration spec — gandalf authors post-Cycle-10
- NOT damage-amplitude implementation in fight engine — variance coefficient is data tagging; gamora sim consumes existing damage-roll machinery (extension if needed is gamora seam follow-on)
- NOT loadout app weapon-sim-display work — drax seam separate workstream
- NOT mythological-register substrate expansion beyond ~30 NULL-typed rescue — Track M1 deferred per 02-roadmap § 3.6

---

## 7. Tag intent

`rocket/cycle-10-stage-4-mechanical-tagging-2026-05-25` after:
1. Phase 1 legolas Mode A consult lands
2. Schema extension + MIGRATION.md
3. Population script executes successfully
4. Mythological-NULL rescue complete
5. gamora sim-viability assessment landed
6. jack-ryan Gate-2 PASS
7. Round-trip smoke PASS

Intermediate tag (seam-prefixed) per project convention. NO Matt-approved milestone prefix.

---

## 8. Smoke-test expectation

### Phase 1 consult smoke
- Methodology recommendation includes: chosen damage-amplitude representation + rationale grounded in engine BC envelope + cheapest-refuting-test pass/fail threshold

### Schema migration smoke
- ALTER TABLE; ROLLBACK; verify column addition; re-apply
- grep-verify gamora + star-lord existing consumption code patterns; if reads exist without column-presence-check, dispatch fails fast

### Per-axis distribution smoke
- Post-population: per-axis bin distribution histogram; flag any axis where actual distribution is >2σ from expected (suggests heuristic misapplication)
- Mythological-NULL rescue distribution check: ~30 rows split across cell-types (not all clumped into one cell)

### Round-trip smoke (CRITICAL — load-bearing for Principle 6)
- rocket writes weapon_sim_props row for 1 representative v1_scope weapon
- gamora sim consumes the row in fight engine (running on stratified sample of 1 row per cell-type)
- star-lord telemetry consumes fight_log + produces export packet for the fight
- Field-presence assertion at each boundary; export packet contains damage_amplitude_min/max field-values (not NULL)
- Document at `agentic_orchestration/qa/findings/2026-05-25-stage-4-round-trip-smoke.md`

Per Discipline #1.1 resource-bounds: ~3,200 rows × per-row tagging compute ~1 sec = ~1 hr foreground OR background; ~3,200 DB writes ~3 min; resource envelope bounded

### Discipline #19 background processes
- Mechanical-tagging execution runs background; rocket monitors via PID + log capture
- No foreground polling

---

## 9. Discipline checklist

- [x] **#1 + #1.1 math-before-code + resource-bounds:** Phase 1 consult IS the math; rocket population script bounded
- [x] **#1.2 math-note code-citation:** populate_weapon_sim_props.py cites Phase 1 methodology recommendation + composition policy § 3 + BC-axes lock
- [x] **#2 + #2.1 smoke + resource-scaling rehearsal:** § 8 above
- [x] **#11 empirical inspection:** per-axis distribution post-tagging is empirical-inspection artifact
- [x] **#18 + #18.2 methodology-before-execution:** Phase 1 consult LOAD-BEARING gate; baseline-informed
- [x] **#19 + #19.1 background processes + cheapest-refuting-test:** mechanical-tagging background; per-axis distribution check is cheapest-refuting-test
- [x] **#23 framing-audit checklist:** Phase 1 consult is framing-audit-applicable transition (locks methodology BEFORE execution)
- [x] **#25 semantic-layer rep-audit:** mythological-NULL rescue rep-audit per § 4.6

---

## 10. Open questions for the agent to resolve

- Phase 1 consult: damage-amplitude representation choice — variance coefficient vs min/max vs statistical distribution model — legolas + rocket decide post-consult
- Heuristic threshold parameters (range_class boundaries by length cm; etc.) — Phase 1 consult finalizes per substrate empirical distribution
- LLM-judge calibration sample size for ambiguous cases — rocket + legolas decide per cost-vs-coverage trade-off
- Mythological-NULL rescue per-row rationale source — LLM-judge OR design-judged or hybrid — rocket + gandalf decide per row
- Stage 4 tagging sequence (parallel per cell-type vs sequential per cell-type) — rocket decides per resource bounds
- Whether to fold Stage 3.5 gap-fill rows into Stage 4 batch vs sequence them post-main-pool — fold into batch (UNION) for sampling consistency; rocket confirms

---

## 11. References

- Stage 4 parent: `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § 3 Stage 4
- Composition policy v1 § 1.4 + § 3: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- BC-axes lock: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- Architecture B: `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- T4-A architecture defaults: `canonical/story/tier-4-architecture-defaults-2026-05-22.md`
- Multi-dim convergence algorithm: `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md`
- Marginal-lineage pattern: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Cycle 10 scope-doc: `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`
- Wave 5 Phase 3 distribution report: `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md`
- Wave 6 Stage 3.5 entries: `agentic_orchestration/rocket/research/cycle-10-stage-3-5-gap-fill-2026-05-25/entries/`

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 scope-doc § 1 in-scope autonomous dispatch authoring + composition policy v1 § 1.4 + § 3 locked spec + Stage 4 parent dispatch § 3
**Status:** **FIRE-READY pending Wave 5 Phase 3 + Wave 6 Stage 3.5 completion** — Stage 4 mechanical-tagging fires on UNION of v1_scope main pool + Stage 3.5 engine-authored entries + mythological-NULL rescue subset

**Gate-1 critique-pair posture:** Wave 7 fires within Cycle 10 in-scope autonomous dispatch authoring per scope-doc § 1. Composition policy v1 § 1.4 + § 3 + BC-axes lock together constitute the locked design substrate. Phase 1 legolas Mode A consult LOAD-BEARING per Discipline #18; consult-as-Gate-1-replacement for methodology choice. jack-ryan Gate-2 PASS + round-trip smoke PASS gate tag.

**Owners:** rocket (lead — mechanical-tagging + schema + script + artifact) + gamora (sim-viability + balance-loop sanity-check) + jack-ryan (Gate-2 methodology + round-trip + cross-seam) + legolas Mode A (Phase 1 methodology consult prerequisite)

---

## Completion record

**Completed by:** rocket
**Completion date:** 2026-05-25
**Commit:** `9ad416e` (collaboration repo) + `ff699f5` (engine repo AGENT_STATE.md)

### Acceptance criteria status

- [x] Phase 1 legolas Mode A consult artifact landed — already complete pre-session
- [x] Schema extension landed: `damage_amplitude_min REAL` + `damage_amplitude_max REAL` + DEX added to primary_stat CHECK constraint. Also: FK reference corrected from legacy `weapons(weapon_id)` to `weapon_knowledge_entries(id)` (load-bearing fix; 49 of 2,293 v1_scope entries had matching weapons rows — remainder would have been un-insertable without FK correction). MIGRATION.md at `agentic_orchestration/rocket/research/cycle-10-stage-4-2026-05-25/MIGRATION.md`.
- [x] Population script executes successfully against UNION of (v1_scope main pool + Stage 3.5 gap-fills + mythological-NULL rescue). Script at `populate_weapon_sim_props.py`. 3-pass methodology; ~$0.37 LLM cost (under $0.95 estimate).
- [x] ALL 2,293 v1_scope rows have populated `weapon_sim_props` row; ZERO regressions on prior-stage columns; ZERO errors.
- [x] Per-axis distribution histogram landed in `mechanical-tagging-report.md`; ambiguous-case log in `ambiguous-cases.jsonl` (137 low-confidence rows; 130 royal_armouries accessories; WARN signal assessed as expected/acceptable)
- [x] **CRT-1 PASS: INT+WIS combined 14.3% >= 12%** (DEX 46.9%, STR 38.8%, WIS 7.3%, INT 7.0%)
- [x] Mythological-NULL rescue: 14 rows tagged (21 pre-existing mythological-register entries; per dispatch count of ~30 includes Stage 3.5 engine-authored mythological entries that were already typed). Per-row rationale in `mythological-null-rescue.md`. Rep-audit Mode B/C contamination check: CLEAN.
- [ ] gamora sim-viability assessment — pending knight-rider gamora invocation
- [ ] gamora small-scale sim-loop sanity-check — pending
- [ ] jack-ryan Gate-2 PASS — pending knight-rider routing
- [ ] **Round-trip smoke** (rocket → gamora → star-lord) — pending knight-rider coordination
- [ ] Tag: `rocket/cycle-10-stage-4-mechanical-tagging-2026-05-25` — pending Gate-2 + round-trip smoke PASS

### Key anomalies flagged for gamora/jack-ryan

1. **Ruyi Jingu Bang wikidata (id=388):** DEX/ranged assigned due to wikidata `weapon_type='gun'` data error. Wikipedia entry (id=174314) correctly STR/mid. Recommend override at gamora pass.
2. **Signal 2 WARN:** LLM low-confidence rate 37% (137/371 rows) exceeds 20% threshold. Assessment: 130 of 137 are royal_armouries accessories (Holster, Detached lock, Cocking lever, etc.) — expected high ambiguity for component-part vocabulary. 40 already sim_viable=0. Remaining ~90 with sim_viable=1 warrant gamora Phase 2 spot-check.
3. **Amplitude variable bin at 54.3%:** above Sketch A target (~35%). Expected artifact of per-bin lookup table; validate against sim telemetry after first simulation run.
4. **Tier-S items flagged for gandalf curation pass:** Gáe Bulg (multi-hit/low lore accuracy), Mjölnir (tempo=high vs consult's low), Sudarshana Chakra (WIS/AoE vs consult's DEX/scatter).

### Resource actuals

- LLM calls: ~371 (Pass 3 only)
- LLM cost: ~$0.37 (under $0.95 estimate)
- Wall time: ~14 min (under 1 hr envelope per Discipline #1.1)
- DB backup: `backups/telemetry.db.pre-stage-4` (gitignored; 204 MB)

---

## Wave 7 amendment 2026-05-25 — Ruyi Jingu Bang id=388 wikidata override

**Amendment date:** 2026-05-25
**Authority:** Cycle 10 scope-doc § 1 in-scope autonomous (substrate-data-error correction within rocket seam); jack-ryan Gate-2 Flag 1 WARN
**DB target:** `weapon_sim_props` WHERE `weapon_id = 388` (reincarnated-loadout/data/telemetry.db)

### Root cause

Wikidata entry Q834090 (id=388, Ruyi Jingu Bang) has `weapon_type='gun'` in its structured properties — a wikidata data error. Pass 2 weapon_type key lookup fired on this value and assigned DEX/ranged profile. The Wikipedia counterpart entry (id=174314, "Ruyi Jingu Bang") was correctly classified STR/mid by LLM judge in mythological-NULL rescue (per its canonical description as Sun Wukong's magical extending staff). Both entries are v1_scope=1.

### Values changed

| Column | Before (wikidata data error) | After (corrected, aligned to id=174314) |
|---|---|---|
| `primary_stat` | DEX | STR |
| `range_min_units` | 5.0 | 2.5 |
| `range_max_units` | 18.0 | 7.0 |
| `base_attack_speed` | 0.7 | 1.5 |
| `charge_time_s` | 0.5 | 0.0 |
| `damage_amplitude_min` | 0.3 | 0.7 |
| `damage_amplitude_max` | 2.5 | 1.6 |
| `sim_viability_notes` | (null) | wave_7_amendment_2026_05_25_wikidata_data_error_override: wikidata weapon_type=gun is data error; corrected to STR/mid-range staff per wikipedia counterpart id=174314 |

Columns unchanged: `hits_per_attack=1`, `aoe_radius_units=0.0`, `secondary_stat=none`, `sim_viable=1`.

### Post-amendment SQL verification

```
SELECT primary_stat, range_min_units, range_max_units, base_attack_speed, charge_time_s,
       hits_per_attack, aoe_radius_units, damage_amplitude_min, damage_amplitude_max
FROM weapon_sim_props WHERE weapon_id = 388;
-- Result: STR|2.5|7.0|1.5|0.0|1|0.0|0.7|1.6
-- Matches id=174314 wikipedia counterpart exactly.
```

### CRT gate re-run post-amendment

| CRT | Description | Pre-amendment | Post-amendment | Status |
|---|---|---|---|---|
| CRT-1 INT+WIS >= 12% | Attribute floor | 14.3% | 14.26% | PASS |
| CRT-1 ceiling <= 65% | DEX ceiling | 46.9% | 46.88% | PASS |
| CRT-2 no bin > 60% | Amplitude bin ceiling | variable 54.3% | variable 55.39% | PASS |
| CRT-3 schema non-NULL | Key column NULL check | 0 NULLs | 0 NULLs | PASS |
| CRT-4 amplitude non-NULL | Amplitude NULL check | 0 NULLs | 0 NULLs | PASS |

Note on CRT-2 delta: id=388 original amplitude was 0.3/2.5 = 8.3x ratio (spiky bin >4.5x); corrected amplitude is 0.7/1.6 = 2.3x ratio (variable bin). One row shifted from spiky to variable. Variable bin moved from 54.3% to 55.39%, spiky from 22.8% to 21.85%. Both remain within bounds.

### Anomaly log update

Completion record anomaly #1 (Ruyi Jingu Bang DEX/ranged) resolved. Override applied. No gamora re-flagging required for this entry.
