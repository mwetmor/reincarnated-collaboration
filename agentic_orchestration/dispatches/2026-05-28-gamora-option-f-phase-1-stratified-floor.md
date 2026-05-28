# Dispatch — 2026-05-28 — gamora — Option F Phase 1: Stratified per-encounter-type floor + KPM=600.0 ceiling-artifact bypass (~0.5 day; Cycle 14 v1 unblock)

**From:** knight-rider
**To:** gamora (simulation seam owner)
**Approved by:** Matt 2026-05-28 verbatim D1+D3 ratification per jack-ryan Gate-3 Option F Phase 1 (BLOCK authority exercised; SC7-F1 architectural disposition `044f4ea`)
**Estimated effort:** ~0.5 day gamora impl
**Acceptance:** ≥12/18 Phase 2 kits emit under stratified per-encounter-type floor + KPM=600.0 ceiling-artifact bypass; MIGRATION.md v1.37 documents architectural retraction; post-impl smoke-test PASS

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close Cycle 14 v1 architectural block (SC7-F1 compound finding) via stratified per-encounter-type quality floor — boss-encounter KPM signal IS meaningful and operative as Cycle 14 v1 quality gate; swarm/magic_pack KPM is degenerate engine-artifact (600.0 ceiling) and bypassed honestly rather than papered over. Composes "Engine first. Game second. Phase third." — engine-layer measurement integrity protected by explicit artifact bypass.

**Refutation conditions:**
- Stratified floor still produces <12/18 emit (gamora SC-7 telemetry suggested 2-3/18 boss-in-band per cohort × 5 cohorts ≈ 12-15 — but new architecture)
- KPM ceiling 600.0 bypass introduces side-effect on Phase 4 or Phase 7 downstream consumers
- Acceptance threshold ≥12/18 doesn't compose with cohort midpoint median estimator (jack-ryan canonical `3d4eda5`)

## Context

**Authority chain:**
- Matt 2026-05-28 D1 RATIFIED — Option F Phase 1 stratified per-encounter-type floor + KPM=600.0 ceiling-artifact bypass
- Matt 2026-05-28 D3 RATIFIED — Engine KPM ceiling 600.0 = simulation artifact; Cycle 14 bypass; Cycle 15 investigate concurrent with D2 Phase 2
- Jack-ryan SC7-F1 Gate-3 disposition at `agentic_orchestration/qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md` + commit `044f4ea`
- Gamora SC-7 calibration at engine `e7af7db` (calibrated BASE_SPELL_DAMAGE_L50 stands)
- Phase 7 canonical thresholds at engine `3d4eda5` (jack-ryan re-canonicalizes in parallel per ~0.25d work)
- Discipline #40 case (c) canonical-lock retraction procedure (6-step per engineering-disciplines.md § 40)

**6th scaffold-drift case recognized 2026-05-28:** Phase 7 KPM-uniform-band-across-encounter-types is formally a Discipline #39 scaffold-with-pending-decision (KR observation; Matt ratified). Stratified floor (D1 Phase 1) is the operational unblock; per-type bands (D2 Phase 2) is the Cycle 15 architectural close.

## Required reading

- `agentic_orchestration/qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md` (jack-ryan Gate-3 6-option analysis; Option F detailed spec)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` line 85 (`GAUNTLET_ENCOUNTER_PASS_FLOOR=14`; primary modification target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` lines 117-122 (`COHORT_KPM_BAND`; verify composition)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/sc-7-base-spell-damage-calibration-2026-05-28.md` § 12 (SC-7 empirical results)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (your seam; v1.37 addition)
- `agentic_orchestration/cycle-14-wave-5-season-001/sc-7-calibration-telemetry.json` (empirical encounter-type distribution)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #40 case (c) 6-step retraction procedure

## Discipline #46 compliance

- N/A — constant updates + filter logic; no DB queries

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) ≥12/18 emit acceptance threshold composes with cohort midpoint median estimator; (2) KPM=600.0 ceiling bypass is correctly classified as artifact (not legitimate quality signal); (3) stratified floor on boss-only encounters preserves quality discrimination Cycle 14 v1
- **Q2 refutation evidence to seek:** smoke-test against 18 staged kits to verify ≥12/18 acceptance threshold achievable; verify ceiling bypass doesn't side-effect Phase 4/7 downstream consumers
- **Q3 outcome trigger:** if <12/18 emit OR ceiling bypass side-effects surface, invoke #44 framing-refusal + surface to KR for re-routing

## Scope (4 parts)

### Part 1 — Stratified per-encounter-type floor (~0.25 day)

- [ ] Update `GAUNTLET_ENCOUNTER_PASS_FLOOR=14` semantics — replace single-floor with stratified per-type criterion
- [ ] New logic: GAUNTLET_PASS = boss-type encounters ≥2 of 3 in Phase 7 cohort midpoint band per cohort (5 cohorts: Support/Control/Defensive/Damage/Hybrid)
- [ ] Explicit encounter-type filter: boss + mini-boss as ELIGIBLE for quality gate; swarm + magic_pack + elite_pack as bypassed for Cycle 14 v1
- [ ] Cycle 15 Phase 2 cross-reference inline comment (Option A per-type KPM bands per Matt D2 ratification)

### Part 2 — KPM=600.0 ceiling-artifact bypass (~0.1 day)

- [ ] At gauntlet sweep loop: when encounter KPM == 600.0 (engine ceiling artifact per D3 ratification), explicit BYPASS — encounter does NOT count toward in-band OR out-of-band tally; cleanly excluded from quality measurement
- [ ] Inline comment per Discipline #11: "KPM=600.0 is fight-duration discretization artifact (Matt D3 ratified Cycle 14 2026-05-28); Cycle 15 investigation concurrent with D2 Phase 2 Option A per-type bands"
- [ ] Telemetry capture: record bypassed-encounter count per cohort for Cycle 15 investigation

### Part 3 — MIGRATION.md v1.37 (~0.05 day)

- [ ] `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.37 entry:
  - Architectural retraction per Discipline #40 case (c) 6-step procedure
  - SC7-F1 root cause: HP variance 65× + engine KPM ceiling 600.0 artifact
  - Cycle 14 v1 fix: stratified per-encounter-type floor + ceiling bypass
  - Cycle 15 forward-link: Option A per-type KPM bands + engine ceiling investigation
  - Cross-reference: jack-ryan Gate-3 disposition `044f4ea` + Matt D1+D2+D3 ratifications 2026-05-28

### Part 4 — Smoke-test ≥12/18 emit acceptance (~0.1 day)

- [ ] Re-run Phase 3 via rocket's `run_phase3_from_staged_phase2()` with stratified floor + ceiling bypass
- [ ] Verify ≥12/18 Phase 2 kits achieve `season_emit=True`
- [ ] Per-cohort emit distribution capture (target ≥2-3 per cohort under stratified floor)
- [ ] Principle 6 round-trip preserved (rocket Phase 3 `_principle6_round_trip_check` still PASS)
- [ ] Capture empirical telemetry at `agentic_orchestration/cycle-14-wave-5-season-001/option-f-phase-1-smoke-telemetry.json`

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- [ ] Tag at completion: `gamora/v1.9-option-f-phase-1-stratified-floor-1`
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt's per-cycle push pattern

## Acceptance criteria

- [ ] Stratified per-encounter-type floor landed (boss + mini-boss ELIGIBLE; swarm + magic_pack + elite_pack BYPASSED Cycle 14 v1)
- [ ] KPM=600.0 ceiling-artifact bypass landed at gauntlet sweep loop
- [ ] **≥12/18 Phase 2 kits emit under stratified floor** (per Matt D1 ratification acceptance)
- [ ] MIGRATION.md v1.37 documents Discipline #40 case (c) retraction with full cross-references
- [ ] Principle 6 round-trip preserved
- [ ] Empirical telemetry filed
- [ ] Tag + AGENT_STATE.md updated
- [ ] Completion record + commit + push

## Out of scope

- Do NOT implement Option A per-type KPM bands (D2 Cycle 15 scope)
- Do NOT investigate engine KPM ceiling 600.0 root cause (D3 Cycle 15 concurrent investigation)
- Do NOT modify SC-7 calibrated BASE_SPELL_DAMAGE_L50 values (gamora `e7af7db` LOCKED — calibration stands)
- Do NOT modify Phase 7 IMPL bridge (engine `eca0aa5` LOCKED)
- Do NOT modify Phase 4 mechanical archive (engine `749d5aa` LOCKED)
- Do NOT touch jack-ryan canonical Phase 7 threshold doc (firing in parallel)

## Open questions for gamora

- **Q-OF1-1:** Bypass semantics — at encounter KPM ≡ 600.0 OR at fight outcome flag (preferred check method)? Your judgment per engine measurement signal
- **Q-OF1-2:** Acceptance threshold ≥12/18 — boss-only stratified counts 3 encounters/cohort × 5 cohorts = 15 boss encounters total; if 2 of 3 per cohort PASS = 10 boss-PASS / 15 boss-total = 67%; check whether ≥12/18 maps to ≥12 BOSS encounters in-band (across all kits) OR a different aggregation per Matt D1 acceptance criterion
- **Q-OF1-3:** Smoke verification surface — full 18-kit run OR 3-5 kit subset first? Your judgment per Discipline #11

## References

- Matt 2026-05-28 D1+D3 verbatim ratifications
- Jack-ryan SC7-F1 Gate-3 disposition `044f4ea`
- Gamora SC-7 calibration `e7af7db` (calibrated values stand)
- Phase 7 canonical thresholds `3d4eda5` (jack-ryan re-canonicalizes in parallel ~0.25d)
- Discipline #40 case (c) 6-step retraction procedure

---

## Completion record

### Cross-seam co-completion record — jack-ryan canonical authority (2026-05-28)

**jack-ryan canonical re-write COMPLETE.** Canonical authority for gamora Option F Phase 1 implementation is now established.

**Canonical target:** `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md`

**What was established for gamora's implementation:**

1. **§ 3.4** — Discipline #40 case (c) retraction record: GAUNTLET_ENCOUNTER_PASS_FLOOR=14 uniform application RETIRED 2026-05-28 per Matt D1. Inline strike-through + audit trail. Pre-retraction state at engine `3d4eda5`.

2. **§ 3.5** — Stratified floor canonical (LOAD-BEARING; Matt D1):
   - `boss` + `mini_boss`: ELIGIBLE (KPM band quality gate applies)
   - `swarm` + `magic_pack` + `elite_pack`: BYPASSED Cycle 14 v1
   - Per-cohort PASS criterion: >= 2 of 3 boss encounters in-band per cohort midpoint ±0.25
   - Season emit acceptance: >= 12/18 Phase 2 kits achieve GAUNTLET_PASS
   - Median estimator composition: boss-only denominator filter; `gauntlet_pass_rate` raw column unchanged

3. **§ 3.6** — KPM=600.0 ceiling-artifact bypass canonical (LOAD-BEARING; Matt D3):
   - Bypass rule: KPM==600.0 → excluded from both in-band AND out-of-band tally
   - SCAFFOLD-WITH-PENDING-DECISION: Cycle 15 investigation gate
   - Telemetry obligation: `bypassed_encounter_count_by_type` per cohort (Cycle 15 input)

4. **§ 3.7** — Cycle 15 Option A forward-link (non-committal architectural roadmap; Matt D2)

**Gamora implementation authority:** gamora may implement Parts 1-4 of the Option F Phase 1 dispatch against this canonical authority. The stratified floor logic in `gauntlet_sim.py` + bypass rule are now canonical-backed. MIGRATION.md v1.37 at gamora seam is the seam-side counterpart.

**Discipline #43 audit A5 compliance:** EXPLICIT retraction documented. Not silent relaxation.

**jack-ryan dispatch:** `2026-05-28-jack-ryan-phase-7-threshold-canonical-re-write-option-f-phase-1.md` (completion record appended)

---

### Gamora implementation completion record (2026-05-28)

**Status: IMPLEMENTATION COMPLETE — DISCIPLINE #44 FRAMING-REFUSAL INVOKED**

**Parts 1-3 status: COMPLETE**

- **Part 1 — Stratified per-encounter-type floor:** IMPLEMENTED in `gauntlet_sim.py`. New constants: `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 = frozenset({"boss_with_adds", "mini_boss"})`, `GAUNTLET_ELIGIBLE_PASS_FLOOR_C14V1 = 2`. Old `GAUNTLET_ENCOUNTER_PASS_FLOOR=14` retained as retracted constant with RETRACTED comment per Discipline #40 case (c). New methods: `eligible_encounters_passed()`, `eligible_encounters_total()`, `bypassed_encounters()` on `GauntletKitResult`. `gauntlet_pass()` semantics changed from 18-encounter uniform floor to boss-type-only 2/4 floor — Discipline #12 semantic shift explicitly framed in MIGRATION.md v1.37.
- **Part 2 — KPM=600.0 ceiling-artifact bypass:** IMPLEMENTED. `KPM_CEILING_ARTIFACT_VALUE = 600.0` constant added. Bypass logic in `w5g1_gauntlet_execution()` fires after Tier 2 result: `KPM ≡ 600.0 → bypassed_ceiling_artifact=True, in_band=False, excluded from tally`. New telemetry fields: `bypassed_ceiling_artifact_total`, `bypassed_per_cohort`. `GAUNTLET_REQUIRED_FIELDS` count 13→14 (`bypassed_ceiling_artifact` added to `GauntletEncounterResult.to_dict()`). Principle 6 round-trip count updated.
- **Part 3 — MIGRATION.md v1.37:** FILED at `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`. Full Discipline #40 case (c) retraction documentation. SC7-F1 root cause. Changed constants table. Discipline #12 semantic shift framing. Downstream impact (Phase 4 LOCKED, Phase 7 LOCKED, star-lord no schema changes needed). Cycle 15 forward-link. All cross-references: jack-ryan Gate-3 `044f4ea`, Matt D1+D2+D3, SC-7 calibration tag `e7af7db`.
- **Tests:** 132/132 PASS after updating `test_cycle13_wave5_gauntlet_sim.py` to reflect new semantics. New test class `TestStratifiedFloor`. Old 14/18 floor tests replaced with stratified floor pass/fail/count tests.
- **Math note:** `simulation/math/option-f-phase-1-stratified-floor-math-2026-05-28.md` authored BEFORE implementation per Discipline #1.

**Part 4 status: SMOKE FAIL — DISCIPLINE #44 INVOKED**

- **Acceptance threshold:** ≥12/18 kits season_emit=True
- **Smoke result:** 3/18 kits season_emit=True (season_emit_rate=0.167)
- **KPM=600.0 bypass fires:** 0 times (real Phase 3 boss KPM is 60-150; the 600.0 ceiling was specific to calibration loop at boosted reference-class DPS — bypass correctly implemented but not operative on real kits)
- **Root cause (deeper than dispatch prediction):** SC-7 calibration proved ONE reference class achieves boss KPM in-band at mult=93.81×. The 18 Phase 2 kits have class-specific DPS that varies widely. 85% T1 REJECT rate on eligible (boss_with_adds/mini_boss) encounters across all cohorts (e.g., Balanced: 61/72 T1 rejected). Only 10/216 eligible encounter evaluations were in-band (4.6%). The dispatch prediction of 12-15 kits passing was based on an incorrect assumption that all 18 classes produce boss KPM near-band. Cross-class DPS variance is the deeper SC7-F1 root cause, not resolved by stratified floor alone.
- **Per-cohort emit:** DPS-min-maxer=0, Balanced=1, Defensive=0, Hybrid=2, [remaining cohorts]=0
- **Discipline #44 trigger:** "<12/18 emit OR ceiling bypass side-effects surface → invoke #44 framing-refusal + surface to KR for re-routing" — invoked.
- **Framing-refusal meaning:** gate architecture change is correct and canonical-backed; acceptance threshold is not achievable with current gate structure given cross-class DPS variance; KR re-routing required for re-disposition.

**Empirical telemetry artifact:** `agentic_orchestration/cycle-14-wave-5-season-001/option-f-phase-1-smoke-telemetry.json`

**Tag decision:** `gamora/v1.9-option-f-phase-1-stratified-floor-1` NOT applied — Discipline #44 invocation holds tag pending re-routing disposition.

**Commit:** implementation committed (Parts 1-3 complete, Part 4 smoke FAIL documented); see engine commit.

**KR re-routing signal:** The cross-class DPS variance finding changes the diagnosis. Option F Phase 1 stratified floor addresses the HP variance problem correctly. The remaining block is that each class produces KPM at a different rate — most classes fall outside the boss-encounter KPM band that ONE reference class sits in. Resolution paths for KR/Matt disposition:
1. Per-class KPM bands (generalization of Matt D2 per-type bands) — each class has its own expected KPM range at boss tier
2. Wider band (increase COHORT_KPM_BAND from ±0.25 to something wider — but this loses discrimination)
3. Different quality metric entirely for Phase 3 gate (e.g., damage output relative to boss HP %, not time-based KPM)
4. Normalize class DPS to reference class before applying KPM gate

**Signed:** gamora 2026-05-28 — Discipline #44 invoked; implementation delivered per 4-part scope; smoke FAIL; KR re-routing required
