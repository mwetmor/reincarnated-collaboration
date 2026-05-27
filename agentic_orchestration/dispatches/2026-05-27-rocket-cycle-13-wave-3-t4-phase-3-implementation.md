# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 3 T4 Phase 3 Implementation (W3.0-W3.5 Bundled)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 verbatim "Resume Wave 0 → Wave 1 dispatch sequencing per ratified framing brief § 4.1 autonomous scope" + jack-ryan Wave 3 Gate-1 PASS-with-WARN verdict (commit `50028cb`) on doc 44 + gandalf W1 clarification landed (commit `375af07`; § 8.3 amendment corrected true-count 4→3) + I1+I2+I5 KR fold-ins
**Estimated effort:** ~8-16 hrs bundled implementation (6 sub-waves W3.0-W3.5; smaller than Wave 2's 10 sub-waves; rocket may sub-checkpoint per logical chunk)
**Acceptance:** Wave 3 T4 Phase 3 implementation landed per doc 44 (§ 7 sub-wave structure + § 8.3 amended); character-wide vs chain-wide scope dimension operationalized + per-category applicability + 6-step selection algorithm + biggest-design-risk 4-mitigation bundle + composition with Wave 2 + round-trip smoke per Principle 6 including legendary_t0_5 rarity carryover

## Context

Cycle 13 Wave 2 CLOSED 2026-05-27 (WARN-pattern REMEDIATED). Wave 3 = T4 algorithm Phase 3 implementation per doc 44 amended (commits `a80044a` + `375af07`).

**Per jack-ryan Wave 3 Gate-1 fold-ins (REQUIRED in THIS dispatch per next-action sequence):**

- **W1 RESOLVED (gandalf clarification commit `375af07`):** doc 44 § 8.3 `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count corrected from 4 → 3. Empirically: TRADE_OFF + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION (NOT 4; "multiplier strategies" = skill-specific TRADE_OFF, NOT distinct STRATEGY_MULTIPLIER constant). Doc 44 § 8.3 now includes module-load assert `sum(STRATEGY_CHARACTER_WIDE_ELIGIBILITY.values()) == 3` + full per-key breakdown. Rocket W3.1 implements per amended § 8.3.

- **I1 INFO (rocket resolves at W3.3):** doc 44 § 4 Step 4 score formula `score × (1 + prior_weight)` behavior when ALL scope candidates have negative net synergy scores is unspecified. Rocket resolves at W3.3 implementation with sensible default (e.g., select least-negative; OR fall through to Option F Retry 4 scope-flip). Gamora SC-7 surfaces empirically post-Wave-3-baseline.

- **I2 KR FOLD-IN (REQUIRED in W3.3 acceptance criteria):** W3.3 acceptance criteria must include minimum **8 cohort × scope coverage combinations** for prior-weighting validation (4 cohorts × 2 scopes = 8 minimum combinations; verify rocket implementation generates ≥8 distinct cohort × scope test cases). Per jack-ryan Wave 3 Gate-1 I2 INFO.

- **I5 PLANNING NOTE (Wave 3+ drax cross-seam touch):** per-scope projection emission (doc 44 § 5.3 + § 8.6) is potential drax cross-seam touch at Wave 3+ integration. Not actionable in Wave 3 rocket implementation; rocket should produce data structure that drax can consume downstream (clean separation; no drax-specific code in rocket Wave 3).

**Carryover from Wave 2 (preserved):**
- legendary_t0_5 rarity in W3.5 round-trip smoke (Wave 1 Gate-2 I1; Wave 2 Gate-2 confirmed)
- Pattern 9+10 stubs preserved (Wave 2 W2.6); Wave 3 may extend per doc 44 § 5 biggest-design-risk Pattern 9+10 scope-amplification detection
- WARN-pattern REMEDIATED status (per Wave 2 Gate-2 PASS); maintain in Wave 3 (post-script empirical count assertions 100% accurate target)

## Required reading before starting

1. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (W1 § 8.3 + § 3.2 corrected per commit `375af07`; design intent)
2. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-1-doc-44-critique.md` (Gate-1 verdict; W1+I1+I2+I5 specifics)
3. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Wave 2 Gate-2 PASS; WARN-pattern REMEDIATED status preserved)
4. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 substrate; Wave 3 builds on)
5. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D81 Phase 3 architectural foundation)
6. `canonical/41-progression-framework-2026-05-27.md` (L50 hybrid + cell × node × cohort context)
7. `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` § 1.3 + § 1.4 + § 2.4 (substantive locks)
8. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #27 + #29 + #30 + #31 + #32 + Principle 6)
9. `agentic_orchestration/operating-procedures/rocket.md` (operating procedure)
10. Existing engine code paths (Wave 2 implementation; Wave 3 extends):
    - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (Wave 3 extends — scope-dimension field addition per Option A)
    - `reincarnated-engine/src/reincarnated/generation/t4_synergy_scan.py` (Wave 3 reuses; consumes elrond priors)
    - `reincarnated-engine/src/reincarnated/generation/t4_option_f.py` (Wave 3 extends — Option F Retry 4 scope-flip per doc 44 § 4)
    - `reincarnated-engine/src/reincarnated/generation/t4_algorithm_wave2.py` (Wave 3 orchestrator extension target)
    - `reincarnated-engine/tests/test_cycle13_wave2_t4_algorithm.py` (Wave 3 tests extend)

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before W3.1 schema-implementation:

- [ ] Document the scope-dimension applicability math: Category A inherently character-wide (Step 1 routing); Categories B/C chain-wide default but parallel-chain reach + scope-promotion extends; per-key eligibility per amended § 8.3 (TRADE_OFF + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION = True; GEOMETRY_COLLAPSE + Category-A-strategies = False)
- [ ] Document the 6-step selection algorithm math: applicability bound (Step 1) + cohort-archetype prior (Step 2 prior_weight) + per-scope synergy scan (Step 3) + cohort-weighted score selection (Step 4 `score × (1 + prior_weight)`) + magnitude downscaling (Step 5 `1/sqrt(class_chain_count)` for character-wide-promoted Category B/C) + Option F Retry 4 scope-flip (Step 6)
- [ ] Document the all-negative-score handling (I1 resolution): if all scope candidates have negative net synergy, select least-negative (default OR fall through to Option F Retry 4 scope-flip; rocket seam-owner decides)
- [ ] Document the 8-combination minimum coverage math (I2 fold-in): 4 cohorts × 2 scopes = 8 minimum; W3.3 implementation produces ≥8 distinct cohort × scope test cases

## Cross-seam contract change? (Principle 6 gate)

**Round-trip REQUIRED.** Wave 3 T4 Phase 3 introduces NEW schema (scope-dimension field on T4CandidateV2 per § 8.5 Option A field-addition path; scope-selection metadata; magnitude-downscaling state). Composes with Wave 2 schema (existing parallel_chain_mode + new scope_dimension field).

**Round-trip smoke:** Generate ≥10 kits per archetype × per scope-dimension (character-wide + chain-wide); verify field-presence + type-consistency; verify scope-selection algorithm fires across all 6 steps; verify Option F Retry 4 scope-flip fires correctly when synthetic failure injected. **CRITICAL per carryover: include `legendary_t0_5` rarity in round-trip smoke.**

**MIGRATION.md required** if cross-seam contract change per ADR-004 (likely yes — new scope_dimension field).

## Scope (W3.0-W3.5 sub-wave structure per doc 44 § 7)

### W3.0 — Substrate prep + repo-scaffold

- [ ] Review Wave 2 implementation (engine commits `2445bad` + `7287b43`); identify integration points for scope-dimension extension
- [ ] Scaffold scope-dimension modules per doc 44 § 7 W3.0

### W3.1 — Scope-dimension schema extension (per doc 44 § 8.5 Option A field-addition)

**Per W1 clarification (doc 44 § 8.3 amended; commit `375af07`):**

- [ ] Implement scope-dimension field on T4CandidateV2 (NOT V3 bifurcation; mirrors W2.3 `parallel_chain_mode` precedent per Option A)
- [ ] Implement `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` dict per amended § 8.3: TRADE_OFF=True + ELEMENT_CONVERSION=True + DUAL_ELEMENT_ADDITION=True (true-count = 3); RESOURCE_CONVERSION=False + DEFENSIVE_CONVERSION=False + GEOMETRY_COLLAPSE=False + DEFENSIVE_TRADEOFF=False
- [ ] Module-load assert `sum(STRATEGY_CHARACTER_WIDE_ELIGIBILITY.values()) == 3` (companion to existing `len(...) == 7`)
- [ ] Math-note per Discipline #1 BEFORE implementation

### W3.2 — Per-category scope-dimension applicability implementation

- [ ] Category A: scope inherently character-wide (Step 1 routing per § 4); fixed
- [ ] Categories B/C: scope chain-wide by default; parallel-chain reach (Wave 2 W2.3 `parallel_chain_mode`) sub-dimension; scope-promotion to character-wide via § 8.3 eligibility
- [ ] Unit test: generation per category honors scope-dimension applicability rules

### W3.3 — Scope-dimension selection algorithm (6-step per doc 44 § 4)

**Per I1 fold-in (rocket resolves):**
- [ ] Step 1: applicability bound (Category A → character-wide fixed; Categories B/C → check § 8.3 eligibility)
- [ ] Step 2: cohort-archetype prior weighting (4 cohorts × scope dimension)
- [ ] Step 3: per-scope synergy scan (reuse Wave 2 t4_synergy_scan.py for each scope candidate)
- [ ] Step 4: cohort-weighted score selection `score × (1 + prior_weight)`. **I1 resolution: if all scope candidates have negative net synergy, select least-negative AND log; fall through to Step 6 Option F Retry 4 scope-flip if no improvement after retry. Document choice in completion record.**
- [ ] Step 5: magnitude downscaling `1/sqrt(class_chain_count)` for character-wide-promoted Category B/C
- [ ] Step 6: Option F Retry 4 scope-flip integration with t4_option_f.py

**Per I2 fold-in (KR REQUIRED):**
- [ ] **W3.3 acceptance criteria: minimum 8 cohort × scope coverage combinations** (4 cohorts × 2 scopes = 8); generate ≥8 distinct cohort × scope test cases for prior-weighting validation; verify empirically

### W3.4 — Cross-cohesion validation per #26 + Block C scaffolding

- [ ] Extend Wave 2 W2.8 cross-cohesion to include scope-dimension variance
- [ ] 4 cohorts × scope-dimension validation (DPS-min-maxer / Balanced / Defensive / Hybrid × character-wide / chain-wide); produces non-degenerate scope-dimension distribution

### W3.5 — Round-trip smoke per Principle 6 + tag-commit

**CRITICAL per carryover: include `legendary_t0_5` rarity in W3.5 round-trip smoke.**

- [ ] End-to-end smoke: generate N=10-20 kits per archetype × per scope-dimension including legendary_t0_5 rarity
- [ ] Verify all fields present + types consistent + 6-step algorithm fires correctly across all 4 cohorts + ≥8 cohort × scope combinations covered + Option F Retry 4 scope-flip fires on synthetic failure
- [ ] MIGRATION.md updated for new scope-dimension field per ADR-004
- [ ] AGENT_STATE.md updated per session end
- [ ] Tag intent: `rocket: Cycle 13 Wave 3 T4 algorithm Phase 3 implementation — W3.0-W3.5 bundled per doc 44 amended + jack-ryan Gate-1 W1+I1+I2 folded`

### Discipline compose-check

- [ ] **#1 math-before-code:** math-note per § Math-before-code above
- [ ] **#1.2 code-citation:** all references to existing code (file + line)
- [ ] **#11 empirical inspection (MAINTAIN WARN-PATTERN REMEDIATED STATUS) — post-script empirical count assertions MUST be 100% accurate.** Per Wave 2 Gate-2 verdict, WARN-pattern REMEDIATED; preserve in Wave 3 (no count understatements OR overstatements).
- [ ] **#18 + #18.2:** scope-dimension is math hotspot; gamora SC-7 consultation FULL post-Wave-3-baseline per #18.2 (FIRES AFTER WAVE 3 CLOSE, not before)
- [ ] **#26 playability:** W3.4 cross-cohesion operationalizes
- [ ] **#27 + #31 + #32:** preserved from Wave 2; Wave 3 maintains dual-effect separability + first-do-no-harm compositions
- [ ] **#29 commitment-to-consequence:** scope-dimension selection lands with consequence
- [ ] **#30 sim methodology naming:** composes with gamora SC-7 post-Wave-3
- [ ] **Principle 6 round-trip:** W3.5 smoke PASSes including legendary_t0_5

## Acceptance criteria

- [ ] All 6 sub-waves W3.0-W3.5 land
- [ ] Scope-dimension field added to T4CandidateV2 per § 8.5 Option A
- [ ] `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count = 3 per amended § 8.3 (module-load assert PASSes)
- [ ] 6-step selection algorithm implemented per doc 44 § 4
- [ ] **Minimum 8 cohort × scope coverage combinations** in W3.3 (per I2)
- [ ] I1 resolution (all-negative-score handling) documented in completion record
- [ ] Option F Retry 4 scope-flip integration with existing t4_option_f.py
- [ ] `legendary_t0_5` rarity covered in W3.5 round-trip smoke (carryover preserved)
- [ ] Round-trip smoke per Principle 6 PASSes
- [ ] MIGRATION.md updated for new scope-dimension field per ADR-004
- [ ] **POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE** (WARN-pattern REMEDIATED status MAINTAINED)
- [ ] Tagged commit per rocket convention
- [ ] Math notes filed per Discipline #1

## Out of scope (explicit non-goals)

- LLM T4 naming (still Phase 5 / Cycle 14+; structure-only Wave 3)
- Pattern 9+10 calibration beyond starting-estimate thresholds (gamora SC-7 post-Wave-3-baseline per #18.2)
- DUAL_ELEMENT_ADDITION magnitude empirical iteration beyond starting anchors (gamora SC-7 post-Wave-3-baseline)
- First-pass class roster (Block A2b deferred-commitment)
- D9 element/mechanic-gating gear-affix trait surface (Wave 4 scope)
- Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling (separate)
- Wave 5 gauntlet sim + season gen + close (separate)
- jack-ryan Gate-2 verification (separate dispatch post-rocket-implementation)
- gamora SC-7 methodology consultation FULL execution (post-Wave-3-CLOSE per #18.2)
- Modifying doc 40 / 41 / 42 / 43 / 44 (cross-seam gandalf authority)
- I5 drax per-scope projection emission (planning note for Wave 3+; not actionable in Wave 3 rocket)
- decisions-log entries
- Production telemetry DB migration

## Open questions for the agent to resolve

- W3 sub-wave sequencing: W3.0 → W3.1 → W3.2 (depends on W3.1) → W3.3 (depends on W3.1 + reuses Wave 2 synergy scan) → W3.4 (extends Wave 2 W2.8) → W3.5. Internal sequencing your seam-owner call.
- I1 resolution form (all-negative-score handling): select least-negative AND log + fall through to Option F Retry 4 if no improvement (recommended) OR alternative. Your seam-owner call; document choice.
- T4CandidateV2 extension granularity: scope_dimension as single field vs composite (scope + parallel_chain_mode merger if cleaner). Your call; preserve W2.3 precedent.
- MIGRATION.md scope: minimal (new scope-dimension field) vs comprehensive; recommend minimal per Principle 6.

## References

- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (commits `a80044a` + `375af07`)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-1-doc-44-critique.md` (Gate-1 W1+I1+I2+I5 fold-ins)
- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Wave 2 Gate-2 PASS + WARN-pattern REMEDIATED)
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 substrate)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended
- `canonical/41-progression-framework-2026-05-27.md`
- Engine code (Wave 2 implementation): see § Required reading #10
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `agentic_orchestration/operating-procedures/rocket.md`

---

**Cycle:** 13
**Wave:** 3 implementation (W3.0-W3.5 bundled)
**Gates:** Wave 3 close = jack-ryan Gate-2 PASS on this implementation; unblocks Wave 4 spec-driven gear gen + T4 Phase 4 sim cycling + gamora SC-7 methodology consultation FULL per #18.2
**Priority:** P1 — critical-path Wave 3 close

---

## Completion record

**Completed by:** rocket
**Date:** 2026-05-27
**Commit:** `2e8bc33` — `rocket: Cycle 13 Wave 3 T4 algorithm Phase 3 implementation — W3.0-W3.5 bundled per doc 44 amended + jack-ryan Gate-1 W1+I1+I2 folded`
**Smoke result:** 146/146 PASS (Wave 1: 27, Wave 2: 69, Wave 3: 50); 0 regressions; 0.41s

### Per-sub-wave status

- W3.0 COMPLETE: Substrate prep — reviewed Wave 2 integration points; identified scope-dimension extension targets
- W3.1 COMPLETE: T4Scope enum (3 values), STRATEGY_CHARACTER_WIDE_ELIGIBILITY (7 keys, 3 True: TRADE_OFF + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION), COHORT_SCOPE_PRIORS (4 cohorts), T4CandidateV2 scope fields (5 new: t4_scope, scope_downscale_factor, scope_prior_weight, scope_weighted_score, scope_projection_data), __post_init__ coherence rule, backward-compat from_dict()
- W3.2 COMPLETE: Per-category applicability (Category A fixed CHARACTER_WIDE; B/C per eligibility + has_parallel_chains)
- W3.3 COMPLETE: New module t4_scope_selector.py — 6-step algorithm; PASS_1_CATALOG 5→6; PASS_2_CATALOG 8→10
- W3.4 COMPLETE: validate_cross_cohesion_w34() + Option F Retry 4 scope-flip (DEFAULT_MAX_RETRIES 3→4; OPTION_F_PHASES PRESERVED at 4)
- W3.5 COMPLETE: Round-trip smoke PASS (all 10 rarities incl. legendary_t0_5); MIGRATION.md updated; AGENT_STATE.md updated

### W1 RESOLVED

STRATEGY_CHARACTER_WIDE_ELIGIBILITY true-count = 3 per gandalf clarification (375af07): TRADE_OFF + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION. Module-load assert `sum(...values()) == 3` PASSES. BC alternation note: GEOMETRY_COLLAPSE alternates to TRADE_OFF at Retry 1 (via _BC_ALTERNATION); at Retry 4, current_bc_strategy is TRADE_OFF (eligible), so scope correctly flips to CHARACTER_WIDE for that retry path.

### I1 resolution

All-negative scope score handling: select least-negative candidate AND log at WARNING level; fall through to Retry 4 scope-flip if no improvement after retry. Implemented in `t4_scope_selector.py:select_scope()`. The Step 4 formula `score × (1 + prior_weight)` makes negative scores more negative for preferred cohorts — unintuitive effect flagged in log; gamora SC-7 surfaces empirically post-Wave-3-baseline.

### I2 8-combination verification

ACHIEVED via `TestI28CombinationCoverage.test_i2_8_combination_coverage_across_4_cohorts`: calls `select_scope_dimension` directly for all 4 cohorts × CHARACTER_WIDE-eligible scenario (TRADE_OFF strategy) + CHAIN_WIDE scenario (GEOMETRY_COLLAPSE ineligible strategy) = 8 distinct (cohort, scope) combinations. Also: `test_i2_cohort_scope_combinations_all_eligible_strategies` exercises 16 combinations (4 cohorts × 2 strategies × 2 scores). Design note: per-run generation with strong cohort priors correctly produces 1 dominant scope per cohort; the I2 8-combo requirement is test-suite coverage (per dispatch "verify rocket implementation generates ≥8 distinct cohort × scope test cases"), not per-run diversity.

### legendary_t0_5 round-trip result

CONFIRMED: `TestW35RoundTripSmoke.test_w35_legendary_t0_5_rarity_present` PASSES. All 10 rarity tiers exercised in round-trip smoke (Wave 1 Gate-2 I1 carryover preserved).

### POST-SCRIPT EMPIRICAL COUNT ASSERTIONS (100% accurate — WARN-pattern REMEDIATED status maintained)

| Assertion | Value | Verification |
|---|---|---|
| T4Scope values | 3 | `len(list(T4Scope))` |
| CHARACTER_WIDE eligible strategies | 3 | `sum(STRATEGY_CHARACTER_WIDE_ELIGIBILITY.values())` |
| STRATEGY_CHARACTER_WIDE_ELIGIBILITY keys | 7 | `len(STRATEGY_CHARACTER_WIDE_ELIGIBILITY)` |
| Cohort priors | 4 | `len(COHORT_SCOPE_PRIORS)` |
| Strategy count | 7 | `len(ALL_T4_STRATEGIES)` |
| Category count | 3 | `len(list(T4Category))` |
| Synergy taxonomy categories | 5 | `len(SYNERGY_CATEGORIES)` |
| Pass-1 catalog entries | 6 | `len(PASS_1_CATALOG)` |
| Pass-2 catalog entries | 10 | `len(PASS_2_CATALOG)` |
| Degenerate detection patterns | 2 | `len(DEGENERATE_DETECTION_PATTERNS)` |
| Option F phases | 4 | `len(OPTION_F_PHASES)` |
| DEFAULT_MAX_RETRIES | 4 | `DEFAULT_MAX_RETRIES` |
| Rarity tiers (incl. legendary_t0_5) | 10 | `len(list(PartitionRarity))` |
| Wave 3 sub-waves (W3.0-W3.5) | 6 | by enumeration |

### Cross-seam flags for knight-rider

- gamora SC-7 fires post-Wave-3-CLOSE per Discipline #18.2 — scope-dimension is extension hotspot; methodology consultation after baseline lands
- drax scope_projection_data consumption is Wave 3+ integration (I5 planning note); data structure ready in T4CandidateV2
- star-lord T4CandidateV2.to_dict() carries 5 new scope fields; backward-compatible additive; export schema update needed at Wave 4 integration milestone
