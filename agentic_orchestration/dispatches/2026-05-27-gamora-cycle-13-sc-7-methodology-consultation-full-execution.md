# Dispatch — 2026-05-27 — gamora — Cycle 13 SC-7 Methodology Consultation FULL Execution (Post-Wave-3-Baseline per #18.2)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-05-27 + Cycle 13 framing brief § 4.1 KR autonomous (sidecar dispatching) + Q6 ratification (gamora consultation gates Wave 4) + jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777`) — Wave 3 CLOSED + Discipline #18.2 timing satisfied (Wave 3 baseline landed; methodology consultation at extension hotspot fires AFTER baseline)
**Estimated effort:** 4-8 hrs methodology FULL closure (review prep doc + baseline data + close 12 REQUIRES-WAVE-3-BASELINE items per prep doc)
**Acceptance:** SC-7 methodology framework FULL closure produced; 22 PRE-BASELINE-RESOLVABLE items confirmed; 12 REQUIRES-WAVE-3-BASELINE items closed with empirical baseline data from Wave 3; framework consumed by Wave 4 gamora sim cycling implementation + jack-ryan Gate-1/Gate-2 review

## Context

Per Discipline #18.2 amendment ("methodology consultation timing at extension hotspots — fires AFTER baseline"): gamora SC-7 methodology consultation FULL execution was DEFERRED post-Wave-3-baseline. Wave 3 baseline NOW LANDED per jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777`). Timing is CORRECT.

**Gamora SC-7 PREP DOC (prior session; commit `115f2a6`):**
- Location: `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md`
- 22 PRE-BASELINE-RESOLVABLE items (framework structure + cohort archetypes + compute discipline + #26 playability operationalization)
- 12 REQUIRES-WAVE-3-BASELINE items (WR band numerical thresholds; DPS-min-maxer bimodal split; power-level calibration anchors; playability sub-gates 3+6 hard thresholds; cross-cohort collapse candidates)
- Methodology pattern named per #30: "Per-weapon-cohort-exhaustive with sub-option-B fallback for cohort-clear legendaries; stratified by progression node; tiered quick-estimate first validation"
- D84 sub-option choice: Hybrid-within-hybrid (Sub-option A for cohort-ambiguous; Sub-option B for cohort-clear)
- Compute budget projection: 11,000-20,000 fights; 1-2 hours sequential at 0.34s/fight; <5MB peak memory; WELL WITHIN M2 8GB threshold (per #1.1)

**Wave 3 baseline data now available** for closure of 12 REQUIRES-WAVE-3-BASELINE items:
- Wave 3 implementation (engine commit `2e8bc33`) provides T4 scope-dimension data (T4Scope=3; STRATEGY_CHARACTER_WIDE_ELIGIBILITY 7/3; COHORT_SCOPE_PRIORS=4; 5 new T4CandidateV2 scope fields)
- 146 tests landed providing empirical baseline (Wave 1: 27 + Wave 2: 69 + Wave 3: 50)
- Cohort × scope coverage matrix (per W3.3 I2 implementation; 8 distinct cohort × scope pairs)

This dispatch fires SC-7 FULL execution per #18.2 timing. Output is the methodology framework that gamora Wave 4 sim cycling implementation consumes + jack-ryan Gate-1/Gate-2 reviews.

## Required reading before starting

1. `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` (YOUR SC-7 PREP doc; 22 PRE-BASELINE + 12 REQUIRES-WAVE-3-BASELINE items)
2. `agentic_orchestration/dispatches/2026-05-26-gamora-cycle-13-wave-0-methodology-consultation-prep.md` (prep dispatch + completion record)
3. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` (Wave 3 Gate-2 PASS; baseline landed)
4. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (Wave 3 design intent; scope-dimension specifics)
5. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 substrate)
6. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition substrate)
7. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D84 + D60 + D85 + D62 sim methodology architecture)
8. `canonical/41-progression-framework-2026-05-27.md` (cell × node × cohort + L50 hybrid; for power-level calibration anchors)
9. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (Block C P_node + C_archetype + W function; consumes for Wave 4 calibration)
10. Wave 3 rocket implementation files (engine commit `2e8bc33`):
    - `reincarnated-engine/src/reincarnated/generation/t4_scope_selector.py` (NEW; scope-dimension selection algorithm)
    - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (T4Scope + eligibility + cohort priors)
    - `reincarnated-engine/src/reincarnated/generation/t4_option_f.py` (Option F Retry 4 scope-flip)
11. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #30 + #1.1 + Principle 6)
12. `agentic_orchestration/operating-procedures/gamora.md` (operating procedure)

## Math-before-code (methodology closure; no engine code modifications)

NOT applicable for direct engine code — but math-grounded calibration is the substantive output. Methodology framework FULL closure includes numerical thresholds, banding anchors, calibration formulas. Per #1 spirit: ground numerical choices in empirical Wave 3 baseline + canonical anchors (Block C scaffolding + doc 41 § 3 node-identity power-vector intents).

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required (low impact).** SC-7 methodology framework FULL is consumed by gamora Wave 4 sim cycling implementation (gamora-internal; no cross-seam fixture mutation). However, methodology may flag requirements for rocket Wave 4 spec-driven gear gen (e.g., specific data fields needed for sim cycling). If so, flag in completion record for KR routing.

**Round-trip smoke:** methodology framework FULL doc loadable + parseable by Wave 4 gamora implementation; clear closure on the 12 REQUIRES-WAVE-3-BASELINE items with concrete numerical thresholds + calibration anchors.

## Scope

### Close 12 REQUIRES-WAVE-3-BASELINE items per prep doc § G classification

Per prep doc § G classification, the 12 items requiring Wave 3 baseline are (verify exact list against prep doc):
- WR band numerical thresholds (per cell × cohort × progression node)
- DPS-min-maxer bimodal split numerics
- Power-level calibration anchors (P_node per Block C scaffolding § 1.4 intent → empirical Wave 3 values)
- Playability sub-gates 3+6 hard thresholds (per #26)
- Cross-cohort collapse candidates
- ... (full list per prep doc § G)

For each REQUIRES-WAVE-3-BASELINE item:
- [ ] Reference Wave 3 baseline empirical data (T4 scope-dimension implementation; cohort × scope coverage matrix; 146-test baseline)
- [ ] Close the item with concrete numerical threshold OR calibration anchor OR explicit deferred-commitment with empirical-evidence trigger
- [ ] Cite the Wave 3 source per Discipline #1.2

### Confirm 22 PRE-BASELINE-RESOLVABLE items hold post-baseline

- [ ] Spot-check 5-8 of 22 items against landed Wave 3 implementation; verify framework choices remain valid OR amend with rationale
- [ ] If any PRE-BASELINE-RESOLVABLE item now requires amendment per Wave 3 baseline observation, FLAG explicitly

### Methodology framework FULL output

- [ ] Update `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` (prep doc) with FULL closure section (or new sibling doc `2026-05-27-cycle-13-wave-4-sim-methodology-framework-full.md`; your seam-owner call)
- [ ] Section: "FULL Closure (2026-05-27 post-Wave-3-baseline)" listing all 12 REQUIRES-WAVE-3-BASELINE items + their closure status (CLOSED with values / DEFERRED with trigger)
- [ ] Compute budget projection re-verified against Wave 3 actual: 146 tests in 0.41s = ~360 fight-equivalents per second observed; project Wave 4 sim cycling at scale
- [ ] Wave 4 gamora implementation guidance: sub-wave structure W4G.0-W4G.X (mirror Wave 1/2/3 sub-wave pattern but for sim cycling track)
- [ ] Cross-reference Wave 4 rocket spec-driven gear gen track dependencies (gear instances at all rarity tiers feeding sim cycling)

### Discipline compose-check

- [ ] **#18 + #18.2:** methodology consultation FULL execution at extension hotspot post-baseline (timing correct per #18.2)
- [ ] **#26 playability:** 6 sub-gates operationalized with empirical thresholds (per Wave 3 baseline)
- [ ] **#30 sim methodology naming:** methodology pattern named explicitly (extend or refine prep doc § A.2 naming)
- [ ] **#1.1 resource-bounds projection:** compute budget re-verified against Wave 3 actual; M2 8GB threshold preserved
- [ ] **#11 empirical inspection:** all numerical closures grounded in Wave 3 baseline empirical data
- [ ] **#1.2 code-citation:** Wave 3 source citations per closure item

## Acceptance criteria

- [ ] All 12 REQUIRES-WAVE-3-BASELINE items closed (with values OR deferred-with-trigger)
- [ ] 22 PRE-BASELINE-RESOLVABLE items spot-checked + confirmed/amended
- [ ] Methodology framework FULL closure output landed (updated prep doc OR new sibling doc)
- [ ] Wave 4 gamora implementation guidance sub-wave structure provided
- [ ] Compute budget re-projection per Wave 3 actual
- [ ] Cross-seam coordination flags (if Wave 4 rocket gear gen has data-field implications)
- [ ] Tagged commit per gamora convention: `gamora: Cycle 13 SC-7 methodology consultation FULL — Wave 3 baseline closure + Wave 4 implementation guidance (post-Wave-3-baseline per #18.2)`
- [ ] Round-trip: methodology framework FULL loadable + parseable by Wave 4 gamora implementation

## Out of scope (explicit non-goals)

- Wave 4 gamora sim cycling implementation (separate dispatch post-SC-7-FULL + post-Wave-4-design-intent landing)
- Wave 4 rocket spec-driven gear gen (separate dispatch; KR fires gandalf doc 45 design intent for rocket track in parallel with THIS SC-7)
- Running simulations at scale (methodology framework FULL closure only; full Wave 4 sim execution post-implementation)
- Modifying simulation code (NO code changes in this dispatch)
- Phase 5 cohesion coalescence (Cycle 14)
- Wave 5 gauntlet sim + season gen + close (separate)
- Modifying doc 40 / 41 / 42 / 43 / 44 (cross-seam gandalf authority)
- decisions-log entries

## Open questions for the agent to resolve

- Output location: update prep doc with FULL closure section vs new sibling doc — your seam-owner call (prep-doc-extension is simpler; sibling-doc is cleaner separation)
- Sub-wave structure for Wave 4 gamora track: how many sub-waves; recommend mirror Wave 3 W3.0-W3.5 pattern (~5-7 sub-waves)
- Compute budget for Wave 4 at scale: 11,000-20,000 fight projection from prep doc — verify against Wave 3 baseline (146 tests in 0.41s); refine projection
- Cross-seam dependency on rocket Wave 4 gear gen: flag specific data fields gear-gen-output must include for sim cycling consumption

## References

- `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` (PREP doc to extend)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` (Wave 3 Gate-2 PASS; baseline)
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8
- `canonical/41-progression-framework-2026-05-27.md` § 3 (node identity)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md`
- Wave 3 rocket implementation files (engine commit `2e8bc33`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#18 + #18.2 + #26 + #30 + #1.1 + #11 + Principle 6)
- `agentic_orchestration/operating-procedures/gamora.md`

---

**Cycle:** 13
**Wave:** 4 prep (SC-7 methodology consultation FULL closure)
**Gates:** Wave 4 gamora sim cycling implementation (post-SC-7-FULL + post-Wave-4-rocket-gear-gen-landing)
**Priority:** P1 — critical-path Wave 4 prep; fires in parallel with gandalf Wave 4 doc 45 design intent (rocket track)
