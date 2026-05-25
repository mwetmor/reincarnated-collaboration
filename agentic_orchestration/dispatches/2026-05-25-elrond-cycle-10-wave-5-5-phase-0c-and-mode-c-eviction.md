# Dispatch — 2026-05-25 — Cycle 10 Wave 5.5 — Phase 0c Tier-A NULL-Subtype Classifier Extension + Mode-C-by-Semantics Eviction Pass (elrond)

**Cycle:** 10 — Substrate Curation Multi-Stage Dispatch
**Wave:** 5.5 (add-on per gandalf SO-4 amendment + sign-off Condition 1 + Condition 3)
**Owner:** elrond (substrate seam; subtype classifier extension + SQL eviction)
**Co-owner:** gandalf (post-eviction sample audit — small batch, ~10 rows)
**From:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 scope-doc § 1 in-scope autonomous dispatch authoring + gandalf SO-3 Pattern A-deep verdict + SO-4 RATIFY-WITH-AMENDMENT + Phase 3 distribution report sign-off Condition 1 + Condition 3 (all per `f40b714`); per scope-doc § 6 known-unknown: "Stage 3 execution surfaces a thin-cell pattern that composition policy v1 doesn't address → Route to gandalf sub-agent for design-fit critique; integrate return; fire forward without Matt re-asking unless gandalf escalates." Gandalf returned + did NOT escalate; this dispatch IS the integration of return.
**Status:** FIRE-READY pending Sidecar B elrond mining return (avoid elrond-on-elrond git race per Cycle 9.15 lesson)

---

## 0. TL;DR

Two-part add-on remediation pass for Cycle 10 Wave 5 Phase 2 v1_scope material per gandalf 50-row spot-check FAIL (29/50 = 58%) + Phase 3 distribution report sign-off PASS-WITH-CONDITIONS:

1. **Phase 0c — Tier-A NULL-subtype classifier extension:** apply Phase 0a-equivalent subcategory classifier to the ~940 Tier-A NULL-subtype rows that escaped Phase 0a's Tier-S-only scope. Closes D1c-equivalent scope-creep on Tier-A pathway (8/21 of 50-row spot-check FAILs traced to this gap: helmet, sallet, cuisses, riding boot, magazine, display plinth, etc.).

2. **Mode-C-by-semantics SQL eviction pass on v1_scope:** evict ~50-100 rows from v1_scope per gandalf's SQL signature spec (semantic-layer Mode-C contamination beyond register-based substitute scope; affects ~28 historical-register + 64 UAVs + 39 F-prefix fighter jets currently in v1_scope; spot-check examples: Karna "Tank EX", Quetzalcoatl "AIM-68 Big Q", Thor "Dark Elf Particle Rifle", Achilles "Swiss sabre with sci-fi description", Grendel "KelTec SUB-2000", Lugh "Claíomh Solais but in modern period").

**Cleans v1_scope material before Phase 2 form-generation fires against it (Wave 7 Stage 4 mechanical-tagging + downstream Phase 2 form-generation per Architecture B).**

**Final Stage 3 milestone tag** `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` defers until Wave 5.5 + Wave 6 land (per gandalf-lean recommendation; cleanest sequencing).

---

## 1. Required reading

1. `canonical/00-ground-state.md` § 1
2. **`agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md` § 3 Conditions 1-3 (THE SPEC; especially Condition 3 SQL eviction signature)**
3. **`agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md`** (50-row spot-check FAIL profile; 21 FAIL breakdown by Tier-A NULL-subtype + Mode-C-by-semantics)
4. **`agentic_orchestration/gandalf/notes/2026-05-25-so-1-2-4-sign-off-verdicts.md`** (SO-4 RATIFY-WITH-AMENDMENT proposing Phase 0c-extension)
5. **`agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md`** (Discipline #25 rep-audit empirical context)
6. `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` (parent dispatch; Phase 0a pattern Wave 5.5 Phase 0c extends)
7. `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/accessory-armor-subcategory-classification.{md,json}` (Phase 0a classifier; Wave 5.5 reuses heuristics for Tier-A extension)
8. `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md` (Phase 3 distribution report; v1_scope membership context)
9. `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 1 (D1a/D1b/D1c gates; Tier-A preferred-include)
10. `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md` (in-scope autonomous)
11. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#11 empirical inspection; #25 semantic-layer rep-audit)

---

## 2. Inputs

- v1_scope = 3,042 rows materialized via Phase 2 (commit `f80b72a`)
- 940 Tier-A NULL-subtype rows: `SELECT * FROM weapon_knowledge_entries WHERE quality_tier='A' AND weapon_kind_classified_subtype IS NULL` (per Phase 3 F-4 + sampling-algorithm-rationale)
- Phase 0a classifier heuristic rule table at `accessory-armor-subcategory-classification.md` (extended Tier-S scope; Wave 5.5 Phase 0c reuses heuristics for Tier-A pool)
- Mode-C eviction SQL signature per gandalf sign-off § 3 Condition 3
- Substrate DB: `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`

---

## 3. Outputs

### 3.1 Phase 0c classifier extension on 940 Tier-A NULL-subtype rows

- Apply Phase 0a classifier heuristics (name-token + structured_properties keys) to the 940-row Tier-A NULL-subtype pool
- Subdivide per existing `weapon_kind_classified_subtype` enum:
  - `handheld_weapon` / `siege_vehicle` / `armor_body_or_head` / `armor_shield` / `accessory_handheld` / `accessory_weapon_integrated` / `accessory_horse_or_equipment` / `art_object` / `other` / `ammo_consumable`
- Update v1_scope eligibility for Tier-A rows that classify as D1c-excluded subtypes (siege_vehicle / art_object / other / ammo_consumable / accessory_horse_or_equipment / armor_body_or_head) — set `v1_scope = 0` + update `v1_scope_composition_trace.rule = 'd1c_excluded_scope_deferred_tier_a_post_phase_0c'`
- Output: `agentic_orchestration/elrond/research/cycle-10-wave-5-5-2026-05-25/phase-0c-tier-a-subtype-classification.md` + companion JSON
- Heuristic-only; no LLM cost

### 3.2 Mode-C-by-semantics SQL eviction pass on v1_scope

Per gandalf sign-off § 3 Condition 3 SQL signature:

```sql
-- semantic-layer Mode-C contamination — eviction candidates from v1_scope
SELECT id, canonical_name, register_canonical, historical_period_canonical,
       cultural_lineage_canonical, named_mythological_match
FROM weapon_knowledge_entries
WHERE v1_scope = 1
  AND named_mythological_match IS NOT NULL
  AND (
    -- modern-period + named-mythological-match overlap (Mode-C-by-period)
    historical_period_canonical IN ('contemporary', 'modern', 'industrial')
    OR
    -- canonical_name contains modern military signatures
    canonical_name LIKE '%UAV%' OR canonical_name LIKE '%missile%'
    OR canonical_name LIKE '%helicopter%' OR canonical_name LIKE '%submarine%'
    OR canonical_name LIKE '%aircraft%' OR canonical_name LIKE 'F-%'
    OR canonical_name LIKE '%MK-%' OR canonical_name LIKE 'AIM-%'
    OR canonical_name LIKE 'AGM-%' OR canonical_name LIKE 'SUB-%'
    OR canonical_name LIKE '%Type %'
    OR
    -- substrate-tagged fantasy_generic with sci-fi description signatures
    canonical_name LIKE '%Particle %' OR canonical_name LIKE '%Plasma %'
    OR canonical_name LIKE '%Quantum %' OR canonical_name LIKE '%Laser %'
  );
```

Expected eviction count: ~50-100 rows (gandalf estimate based on substrate audit).

- Apply eviction: UPDATE `v1_scope = 0` + `v1_scope_composition_trace.rule = 'mode_c_by_semantics_evicted_wave_5_5'` for matching rows
- Output: `agentic_orchestration/elrond/research/cycle-10-wave-5-5-2026-05-25/mode-c-semantics-eviction.md` + companion JSON
- Pre-eviction list saved for gandalf small-batch audit (~10 rows random sample) post-eviction

### 3.3 Combined Wave 5.5 closeout report

- Combined report at `agentic_orchestration/elrond/research/cycle-10-wave-5-5-2026-05-25/wave-5-5-closeout.md`
- Sections:
  - Phase 0c classifier results (940 rows; per-subtype counts; D1c-excluded Tier-A count)
  - Mode-C eviction results (actual eviction count vs ~50-100 estimate)
  - Updated v1_scope count post-Wave-5.5 (target: net ~50-150 reduction from 3,042; new total ~2,900-2,990)
  - Updated per-tier counts post-Wave-5.5
  - Updated per-axis distribution post-Wave-5.5 (verify still within ±5pp targets)
  - 50-row spot-check re-run on cleaned v1_scope sample (KR routes to gandalf post-Wave-5.5)

### 3.4 Pre-Wave-5.5 DB backup

`cycle-10-wave-5-5-2026-05-25/backups/telemetry.db.pre-wave-5-5` (gitignored per Stage 1.5 precedent)

### 3.5 MIGRATION.md

`agentic_orchestration/elrond/research/cycle-10-wave-5-5-2026-05-25/MIGRATION.md` per ADR-004 — updates-only; no new columns; documents Tier-A subtype population + v1_scope UPDATE pattern.

---

## 4. Method notes

### 4.1 Phase 0c reuses Phase 0a heuristics

- Phase 0a populated `weapon_kind_classified_subtype` on 1,126 Tier-S rows
- Phase 0c extends to 940 Tier-A NULL-subtype rows using identical heuristic rules
- Document any heuristic adjustments needed for Tier-A pool (Tier-A may have different subtype distribution than Tier-S)

### 4.2 Mode-C eviction is post-hoc semantic-layer remediation

Per gandalf sign-off § 3 Condition 3: the Phase 2 sampler executed correctly per gate-specs; the gate-specs were under-specified at semantic-layer boundaries. Wave 5.5 closes that gap retroactively without re-engaging composition policy v1 architecture.

### 4.3 Discipline #25 rep-audit operationalization

This is the **second canonical production-Cycle-10 application of Discipline #25** (first was gandalf SO-3 verdict). Wave 5.5 SQL eviction operationalizes Mode-A (cultural-tradition) / Mode-B (geographic-origin) / Mode-C (naming-allusion) / Mode-D (cross-tagged-error) framework from `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` at substrate-curation layer.

### 4.4 Tier-A post-Phase-0c v1_scope eligibility recheck

For Tier-A rows newly classified to D1c-excluded subtypes, the Phase 2 sampler may have admitted them via Sub-phase A (Tier-A preferred-include). Wave 5.5 reverts those `v1_scope = 1` to `0` with composition_trace updated. The freed budget can be filled in a follow-on Phase 2 micro-sample (NOT in this dispatch scope — Wave 5.5 is pure remediation; if substantial budget freed, knight-rider routes a Phase 2 micro-sample dispatch as follow-on).

---

## 5. Cross-seam impact

- **Substrate DB updates** (Phase 0c column population on 940 rows + v1_scope UPDATE on ~50-150 rows)
- **MIGRATION.md required** per ADR-004 (additive updates; no schema change)
- **Round-trip Principle 6:** Round-trip: not applicable — substrate-only updates; no fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; no engine code touched
- **No engine code changes**

---

## 5.5 Acceptance criteria (formal per dispatches/README.md § Acceptance criteria + Principle 6)

- [ ] Phase 0c classifier executed on 940 Tier-A NULL-subtype rows; subtype counts documented
- [ ] Per-subtype v1_scope eligibility recheck applied (D1c-excluded subtypes downgraded)
- [ ] Mode-C SQL eviction executed per gandalf sign-off § 3 Condition 3 signature
- [ ] Actual eviction count documented vs ~50-100 estimate
- [ ] Updated v1_scope count + per-tier + per-axis distribution documented (verify still within ±5pp composition policy § 2 targets)
- [ ] Wave 5.5 closeout report + per-phase outputs at named paths
- [ ] Pre-Wave-5.5 DB backup at named path (gitignored)
- [ ] MIGRATION.md drafted (updates-only pattern)
- [ ] **Round-trip: not applicable — substrate-only updates; no cross-seam contract change per Principle 6 trigger-type table**
- [ ] AGENT_STATE.md updated at session end (elrond seam if maintained)
- [ ] Tag: `elrond/cycle-10-wave-5-5-phase-0c-and-mode-c-eviction-2026-05-25` after closeout report PASS
- [ ] Auto-commit + auto-push per push-per-wave authorization
- [ ] Pre-eviction list saved for gandalf small-batch audit (~10 rows random sample of evicted rows)

---

## 6. Out of scope (explicit)

- NOT Phase 2 re-sample to fill freed v1_scope budget — separate follow-on dispatch if substantial budget freed (knight-rider routes per Phase 0c output)
- NOT modification to composition policy v1 architecture — Wave 5.5 is gate-extension at semantic-layer boundary; composition policy unchanged
- NOT Stage 4 mechanical-tagging on Wave 5.5 evicted rows — Wave 7 dispatch operates on cleaned v1_scope (post-Wave-5.5)
- NOT broad weapon-library crawl for main weapons — Path A LOCKED
- NOT canonical doc amendments — gandalf authors post-Cycle-10
- NOT engine code changes

---

## 7. Tag intent

`elrond/cycle-10-wave-5-5-phase-0c-and-mode-c-eviction-2026-05-25` after closeout report PASS + gandalf small-batch eviction-sample audit PASS.

Intermediate tag (seam-prefixed) per project convention. **Final Stage 3 milestone tag** `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization` fires AFTER Wave 5.5 + Wave 6 (amended scope) land — per gandalf sign-off § 4 tag-sequencing recommendation (cleanest path; tag commits clean v1_scope as Stage 3 canonical output).

---

## 8. Smoke-test expectation

### Phase 0c smoke
- 25 random rows from 940 Tier-A NULL-subtype pool; gandalf 25-row spot-check ≥ 20/25 sensible classification (~80% threshold; same as Phase 0a precedent)

### Mode-C eviction smoke
- Pre-eviction: SELECT 10 random rows from eviction-candidate set; gandalf small-batch audit confirms ≥ 8/10 are genuine Mode-C-by-semantics contamination (not false positives)
- Post-eviction: SQL assertion: `SELECT COUNT(*) WHERE v1_scope = 1 AND v1_scope_composition_trace LIKE '%mode_c_by_semantics_evicted_wave_5_5%'` returns 0 (evicted rows are NOT in v1_scope post-eviction)

### Resource bounds
- Phase 0c: 940 rows × ~50 token regex × <1ms = ~1 sec compute + <1 sec DB write
- Mode-C eviction: 1 SQL with LIKE patterns; ~3,042-row WHERE scan ~0.1 sec; ~50-100 row UPDATE ~0.1 sec
- Total: <5 sec compute + <2 sec DB write; well within host RAM envelope

---

## 9. Discipline checklist

- [x] **#1 + #1.1 math-before-code + resource-bounds:** gandalf sign-off Condition 1 + 3 IS the math; SQL signature pre-specified
- [x] **#1.2 math-note code-citation:** scripts cite gandalf sign-off § 3 Conditions in code comments
- [x] **#2 + #2.1 smoke + resource-scaling rehearsal:** § 8 above
- [x] **#11 empirical inspection:** Phase 0c + eviction outputs are empirical-inspection artifacts; gandalf audits eviction sample
- [x] **#18 + #18.2 methodology-before-execution:** SQL signature pre-specified by gandalf at sign-off time (consultation-as-Gate-1-replacement; consult landed BEFORE execution)
- [x] **#19 + #19.1 background processes + cheapest-refuting-test:** quick execution (~5 sec); gandalf 10-row eviction sample is cheapest-refuting-test
- [x] **#23 framing-audit checklist:** gandalf sign-off IS the framing-audit-applicable transition (locked Conditions BEFORE Wave 5.5 execution)
- [x] **#25 semantic-layer rep-audit:** Wave 5.5 IS the operationalization of Discipline #25 at substrate-curation layer (second canonical production application)

---

## 10. Open questions for the agent to resolve

- Phase 0c heuristic adjustments for Tier-A pool (if Tier-A subtype distribution differs from Tier-S) — elrond proposes adjustments; documented in classifier rationale
- Mode-C eviction SQL extension if additional patterns surface during execution (e.g., other modern-military canonical_name signatures beyond the named list) — elrond documents in eviction artifact
- Whether to fire Phase 2 micro-sample post-Wave-5.5 to fill freed budget (separate follow-on; NOT in this dispatch scope) — knight-rider routes per Phase 0c output count
- Final Stage 3 milestone tag sequencing — knight-rider follows gandalf sign-off § 4 recommendation (tag AFTER Wave 5.5 + Wave 6 land)

---

## 11. References

- Gandalf sign-off (THE SPEC): `agentic_orchestration/gandalf/notes/2026-05-25-stage-3-distribution-report-sign-off.md` § 3 Conditions 1-3
- Gandalf 50-row spot-check: `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md`
- Gandalf SO-1/2/4 verdicts: `agentic_orchestration/gandalf/notes/2026-05-25-so-1-2-4-sign-off-verdicts.md`
- Gandalf SO-3 Pattern A-deep verdict: `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md`
- Cycle 10 scope-doc: `agentic_orchestration/cycles/cycle-10-hive-mind-scope.md`
- Composition policy v1: `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- Marginal-lineage Mode A/B/C/D framework: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Stage 3 execution dispatch parent: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## 12. Sign-off

**Author:** knight-rider (orchestrator)
**Date:** 2026-05-25
**Authority:** Cycle 10 scope-doc § 1 in-scope autonomous dispatch authoring + gandalf sign-off Conditions 1 + 3 (post-Pattern-A-deep verdict integration) + scope-doc § 6 known-unknown forward-motion authority
**Status:** **FIRE-READY pending elrond Sidecar B mining return** — avoids elrond-on-elrond git race per Cycle 9.15 parallel-commit-race lesson. Knight-rider fires Wave 5.5 elrond invocation after Sidecar B mining commit lands.

**Gate-1 critique-pair posture:** gandalf sign-off § 3 Conditions ARE the gate-1 equivalent (Pattern A-deep verdict authoring + SQL signature specification). Re-firing Gate-1 not warranted per scope-doc § 1 in-scope autonomous (dispatch authoring integrating gandalf return).

**Owners:** elrond (lead — classifier extension + SQL eviction + closeout report) + gandalf (small-batch post-eviction audit ~10 rows)
