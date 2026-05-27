# Dispatch — 2026-05-27 — gamora — Cycle 13 Wave 4 Sim Cycling Implementation (W4G.0-W4G.5 Bundled; Track B)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-05-27 + Cycle 13 framing brief § 4.1 KR autonomous + Q6 ratification + jack-ryan Wave 3 Gate-2 PASS verdict (commit `99ec777`) + gamora SC-7 FULL closure (commit `6ebf6c8`)
**Estimated effort:** ~8-16 hrs bundled implementation (6 sub-waves W4G.0-W4G.5 per SC-7 § 9; Wave 4 Track B = sim cycling; Track A rocket gear gen fires separately)
**Acceptance:** Wave 4 sim cycling implementation landed per SC-7 framework FULL closure; W4G.0 calibration setup + W4G.1 Tier 1 sweep + W4G.2 Tier 2 full-sim + W4G.3 KPM median calibration + W4G.4 sub-gate calibration + W4G.5 archive insertion + quality report; round-trip smoke per Principle 6; ~9,340 fight projection landed within ~19-53 min wall-clock per SC-7 compute re-projection

## Context

Wave 4 has TWO tracks:
- **Track A (rocket): spec-driven gear gen** — gandalf doc 45 design intent + jack-ryan Gate-1 + rocket implementation; firing in parallel
- **Track B (gamora): T4 Phase 4 sim cycling** — THIS DISPATCH; gamora SC-7 FULL framework + gamora implementation

Per gamora SC-7 FULL closure (commit `6ebf6c8`; output at `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9):
- Compute re-projection: ~9,340 fights total (revised down ~50% from prep doc); ~19-53 min wall-clock (endgame-only to full 4-node); peak <5MB; M2 8GB not at risk
- Methodology pattern: "Per-weapon-cohort-exhaustive with sub-option-B fallback for cohort-clear legendaries; stratified by progression node; tiered quick-estimate first validation" — Sub-option B relabeled from "fallback" to "dominant path" (~85-90% Sub-option B)
- Sub-wave structure W4G.0-W4G.5 defined
- 12 REQUIRES-WAVE-3-BASELINE items addressed (mostly DEFERRED-WITH-TRIGGER for Wave 4; some PARTIALLY CLOSED with structural amendments)

**Per SC-7 cross-seam flag (1) — star-lord export schema update concurrent dependency:**
Star-lord dispatch fired in parallel for export schema update (gates W4G.5). If star-lord schema not yet landed when W4G.5 fires, gamora uses stub-write pattern + integrates when star-lord landing detected.

**Per SC-7 cross-seam flag (2) — rocket Wave 4 gear gen NO new fields needed:**
T4CandidateV2 Wave 3 schema is gamora-ready; gamora consumes existing fields.

**Per SC-7 cross-seam flag (3) — drax I5 scope_projection_data production-ready:**
Drax integration is Phase 5 / Cycle 14+ scope; not actionable Wave 4 gamora.

## Required reading before starting

1. `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9 FULL Closure (YOUR SC-7 framework; substrate for this implementation)
2. `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-sc-7-methodology-consultation-full-execution.md` (SC-7 dispatch + completion record)
3. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` amended (Wave 3 T4 scope-dimension; consumes for cohort × scope cycling)
4. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` amended (Wave 2 T4 algorithm)
5. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` amended (Wave 1 partition)
6. `canonical/41-progression-framework-2026-05-27.md` (cell × node × cohort + L50 hybrid for endgame-only Cycle 13 v1 scope per Block C § 1.5)
7. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8 amended (D60+D62+D84+D85)
8. `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` (Block C P_node + C_archetype + W function)
9. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-2-rocket-implementation.md` (Wave 3 Gate-2 PASS; baseline landed)
10. Wave 3 rocket implementation files (engine commit `2e8bc33`):
    - `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (T4Scope + T4CandidateV2)
    - `reincarnated-engine/src/reincarnated/generation/t4_scope_selector.py` (scope-dimension selection)
    - `reincarnated-engine/src/reincarnated/generation/t4_option_f.py` (Option F retry mechanism)
11. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #1.2 + #11 + #18 + #18.2 + #26 + #30 + #1.1 + Principle 6)
12. `agentic_orchestration/operating-procedures/gamora.md` (operating procedure)
13. Existing simulation code (your seam): `reincarnated-engine/src/reincarnated/simulation/` for B14.5 V1 primary loop + gauntlet sim infrastructure
14. SC-6 endgame encounter content (engine commit `ee15c96`): `reincarnated-engine/src/reincarnated/simulation/endgame_mob_stat_profile.py` + `endgame_encounter_catalog.py` (sim cycling consumes; 18 encounters)

## Math-before-code (#1 — REQUIRED)

Per Discipline #1 math-before-code, before W4G.1 implementation:

- [ ] Document the per-tier sim cycling math: Tier 1 sweep (quick-estimate) vs Tier 2 full-sim; tiered validation threshold per SC-7
- [ ] Document KPM median calibration math per stratification (cell × cohort × scope × progression node)
- [ ] Document sub-gate calibration math per #26 (6 sub-gates per SC-7 § E1 sub-gate 6 cognitive-load burst threshold structurally amended: ≤8 × scope_chain_breadth events per 0.5s)
- [ ] Document quality report metadata per SC-7 § B1+B4+E2 (T4 regeneration rate; quarantine rate <5% revised; cohort membership classification)
- [ ] Document Cycle 13 v1 scope: endgame-only per Block C § 1.5; multi-node calibration deferred per doc 41 § 4 #2

## Cross-seam contract change? (Principle 6 gate)

**Round-trip required.** Wave 4 sim cycling produces NEW outputs consumed by star-lord export (concurrent dispatch firing) + downstream Wave 5 gauntlet sim PASS verification. Round-trip smoke required per ADR-004.

**Round-trip smoke:** sample Wave 4 sim-result data structure → consumed by star-lord export (if landed) OR stub-write pattern fallback; verify field-presence + type-consistency.

**MIGRATION.md required** per ADR-004 (new sim-result schema fields for Wave 4 sim cycling).

## Scope (W4G.0-W4G.5 sub-wave structure per SC-7 § 9)

### W4G.0 — Calibration setup

- [ ] Substrate prep + repo-scaffold: review B14.5 V1 primary loop + existing gauntlet sim infrastructure; identify integration points for Wave 4 sim cycling
- [ ] Initialize cohort × scope coverage matrix (4 cohorts × T4Scope=3 scopes = 12 strata)
- [ ] Math-note per Discipline #1

### W4G.1 — Tier 1 sweep (quick-estimate)

- [ ] Implement Tier 1 quick-estimate sim per SC-7 methodology pattern
- [ ] Sweep across cohort × scope × cell strata (endgame node only per Cycle 13 v1 scope)
- [ ] Filter candidates passing quick-estimate for Tier 2 full-sim
- [ ] Compute budget: ~10 fights per Tier 1 strata per SC-7 § D2 standard

### W4G.2 — Tier 2 full-sim

- [ ] Implement Tier 2 full-sim for candidates passing Tier 1
- [ ] Cycle through all T4 configurations per kit (multi-T4 architecture)
- [ ] Per-fight outcome capture for downstream KPM calibration
- [ ] Elevated 20 fights per Tier 2 strata for I1 all-negative-score legendaries per SC-7 § D2 conditional

### W4G.3 — KPM median calibration

- [ ] Calibrate per-cell KPM medians per stratification (cell × cohort × scope × progression node)
- [ ] **Critical structural note from SC-7 § B3:** historical B14.5 medians INVALID as Wave 4 anchors — scope-amplification effect changes KPM distribution structurally; use Wave 4 fresh empirical baselines
- [ ] Cycle 13 v1 scope: endgame node only

### W4G.4 — Sub-gate calibration

- [ ] Operationalize 6 #26 sub-gates with empirical thresholds per SC-7 § E1
- [ ] **Sub-gate 6 cognitive-load burst threshold per SC-7 amendment:** ≤8 × scope_chain_breadth events per 0.5s (1 for CHAIN_WIDE_OWN; 2 for CHAIN_WIDE_PARALLEL; class_chain_count for CHARACTER_WIDE)
- [ ] Sub-gate 3 remains first-cycle empirical per SC-7

### W4G.5 — Archive insertion + quality report

**GATES on star-lord export schema update (concurrent dispatch firing per cross-seam flag 1):**
- [ ] If star-lord schema landed: integrate export directly
- [ ] If star-lord schema NOT yet landed: stub-write pattern + flag integration handoff for star-lord return

- [ ] Implement archive insertion per existing math gates (Pareto dominance + crowding distance + Mahalanobis + information gain)
- [ ] Multi-T4 archive entries per scope-dimension
- [ ] Quality report metadata: T4 regeneration rate per SC-7 § B1 (revised ~5.8/legendary; ~9,340 fights total); quarantine rate per SC-7 § E2 (revised <5%); cohort membership classification per SC-7 § B4 (read directly from T4CandidateV2.scope_projection_data)

### Discipline compose-check

- [ ] #1 math-before-code: math-note per § Math-before-code
- [ ] #1.2 code-citation: existing-code references per Discipline #1.2
- [ ] **#11 empirical inspection — POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE (CRITICAL — WARN-pattern PRESERVED status target; Wave 3 maintained; Wave 4 preserves)**
- [ ] #18 + #18.2: methodology consumed from SC-7 FULL framework
- [ ] #26 playability: 6 sub-gates operationalized per W4G.4
- [ ] #30 sim methodology naming: methodology pattern named per SC-7 § A.2
- [ ] #1.1 resource-bounds: compute budget within M2 8GB per SC-7
- [ ] Principle 6 round-trip: W4G.5 smoke PASSes (with stub-write fallback if star-lord not landed)

## Acceptance criteria

- [ ] All 6 sub-waves W4G.0-W4G.5 land
- [ ] Cohort × scope coverage matrix complete (12 strata)
- [ ] KPM median calibration produces empirical anchors per stratification
- [ ] Sub-gate calibration 6 sub-gates per #26
- [ ] Archive insertion + quality report (multi-T4 entries; regeneration rate + quarantine rate + cohort classification)
- [ ] Compute budget within projection (~9,340 fights / ~19-53 min wall-clock per SC-7 § D1)
- [ ] **POST-SCRIPT EMPIRICAL COUNT ASSERTIONS 100% ACCURATE** (WARN-pattern PRESERVED)
- [ ] Round-trip smoke per Principle 6 PASSes (with star-lord integration OR stub-write fallback)
- [ ] MIGRATION.md updated per ADR-004
- [ ] Tagged commit per gamora convention: `gamora: Cycle 13 Wave 4 sim cycling implementation — W4G.0-W4G.5 bundled per SC-7 FULL closure 6ebf6c8`

## Out of scope (explicit non-goals)

- Wave 4 Track A rocket spec-driven gear gen (separate dispatch; firing in parallel)
- Wave 5 gauntlet sim PASS execution (separate; consumes Wave 4 outputs)
- Phase 5 cohesion coalescence (Cycle 14)
- Multi-node sim cycling (Cycle 13 v1 endgame-only per Block C § 1.5; multi-node deferred to per-level scaling formulas implementation per doc 41 § 4 #2)
- Drax cross-seam integration (I5 production-ready but Phase 5+/Cycle 14+ scope)
- Telemetry DB migration v2.16 (separate; per ADR-006)
- Modifying canonical docs (cross-seam gandalf authority)
- jack-ryan Gate-2 (separate dispatch post-implementation)
- decisions-log entries

## Open questions for the agent to resolve

- Sub-wave sequencing: W4G.0 → W4G.1 → W4G.2 (depends on W4G.1 candidate filter) → W4G.3 (depends on W4G.2 fight outcomes) → W4G.4 (independent calibration) → W4G.5 (depends on W4G.3 + W4G.4); internal your call
- W4G.5 star-lord integration mode: integrate directly if landed OR stub-write pattern; check star-lord commit status at W4G.5 time
- Tier 2 elevated 20-fight threshold (per SC-7 § D2): trigger on scope_projection_data warning field (per `t4_scope_selector.py:285-299`); verify implementation

## References

- `agentic_orchestration/gamora/notes/2026-05-26-cycle-13-wave-4-sim-methodology-framework.md` § 9 (SC-7 FULL framework)
- `agentic_orchestration/dispatches/2026-05-27-gamora-cycle-13-sc-7-methodology-consultation-full-execution.md`
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` (Wave 3 T4 scope)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md`
- Wave 3 rocket implementation (engine commit `2e8bc33`)
- SC-6 endgame encounter content (engine commit `ee15c96`)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `agentic_orchestration/operating-procedures/gamora.md`

---

**Cycle:** 13
**Wave:** 4 Track B (gamora sim cycling implementation)
**Gates:** Wave 4 close = jack-ryan Gate-2 PASS on this implementation + Track A rocket implementation Gate-2 PASS (bundled or separate)
**Priority:** P1 — critical-path Wave 4 Track B; fires in parallel with Track A (gandalf doc 45 + jack-ryan Gate-1 + rocket implementation) + star-lord export schema update
