# Dispatch — 2026-05-28 — gamora — SC-7: BASE_SPELL_DAMAGE_L50 calibration against endgame mob HP profile (Discipline #40 closure; ~1-2 days)

**From:** knight-rider
**To:** gamora (simulation seam owner; balance-loop / calibration-loop infrastructure)
**Approved by:** Matt 2026-05-27 (Wave 5 production season firing authorization composes with cascade scaffold-drift remediation per Discipline #40); jack-ryan Gate-2 PASS-with-WARN cascade routing confirmation 2026-05-28
**Estimated effort:** ~1-2 days gamora impl (calibration loop run + per-tier value derivation + post-calibration KPM distribution verification)
**Acceptance:** `BASE_SPELL_DAMAGE_L50` per-tier values (`T1`/`T2`/`T3`/`T4`) calibrated against ENDGAME_ENCOUNTER_CATALOG mob HP profile via existing gamora calibration-loop infrastructure; per-kit KPM across the encounter sweep falls within Phase 7 ±0.25 cohort midpoint band for all 5 cohorts at 18 Phase 2 staged kits; post-calibration smoke-test PASS

## Quality criterion (Move 1)

**Game-quality goal this dispatch serves:** close the Discipline #40 scaffold-with-pending-decision case at `BASE_SPELL_DAMAGE_L50` (Wave 0.5 STARTING ESTIMATE explicitly awaiting gamora SC-7 calibration per Wave 0.5 math note § 7). Without SC-7 calibration, Phase 3 real-kit re-impl produces valid BC coordinates but Phase 4+7 KPM gating rejects all kits as season_emit=False (current ~150x gap below KPM floor 52). Composes "Engine first. Game second. Phase third." — calibrated base-damage values are engine-layer infrastructure protecting Phase 7 2-layer joint-gate quality-filter authority.

**Refutation conditions** (gamora surfaces if any apply):
- Calibration produces tier values that work for light mobs but fail for boss mobs (or vice versa) — encounter HP 65× variance may exceed single-tier-calibration capacity
- Methodology depth exceeds your judgment (route to legolas Mode A per Discipline #18 hotspot)
- Per-cohort KPM distribution after calibration shows substrate-led degenerate clustering (some cohorts saturate; others starve)
- Calibrated values produce in-band KPM but introduce balance regressions in B14.5 V1 historical telemetry

## Context

**Authority chain:**
- Matt 2026-05-27 Wave 5 production season authorization (composes with cascade scaffold-drift remediation)
- Rocket Phase 3 re-impl at engine `96f5e32` + tag `rocket/v1.7-phase-3-real-kit-re-impl-1` — surfaced BASE_SPELL_DAMAGE_L50 KPM ~0.34 vs floor 52
- Jack-ryan Gate-2 PASS-with-WARN — cascade finding correctly framed as Discipline #40 Wave 0.5 scaffold (NOT Phase 3 defect)
- Wave 0.5 math note `wave-0-5-per-skill-emission-math-2026-05-27.md` § 7 line 178: *"This table is a STARTING ESTIMATE. gamora SC-7 (post-baseline) calibrates further against fight outcomes."* — explicit canonical authorization
- Discipline #40 LOAD-BEARING (scaffold-with-pending-decision; calibration is the canonical decision closure path)
- Phase 7 canonical thresholds at engine `3d4eda5` (jack-ryan; gauntlet_pass_rate > 0.70 + cohort midpoint ±0.25 band; cohesion ≥0.75)
- Phase 2 staged at `cycle-14-wave-5-season-001/phase2_kit_candidates.json` (18 kits VALID)
- ENDGAME_ENCOUNTER_CATALOG mob HP profile (3,500–230,000 = 65× variance)
- B14.5 V1 calibration-loop infrastructure (your seam)

**Discipline #39 design pattern VALIDATED:** synthetic stub retirement (`_SyntheticPlayerClass` magnitude=3000) surfaced this previously-hidden upstream gap. Framework operating as architectural recommitment specified.

## Required reading

- `~/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` lines 38-50 (`BASE_SPELL_DAMAGE_L50 = {T1: 300, T2: 450, T3: 650, T4: 1200}`; calibration target)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-0-5-per-skill-emission-math-2026-05-27.md` § 7 (STARTING ESTIMATE rationale + SC-7 deferral note)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/phase-3-real-kit-re-impl-math-2026-05-28.md` (rocket Phase 3 spec; consumes BASE_SPELL_DAMAGE_L50)
- `agentic_orchestration/cycle-14-wave-5-season-001/phase2_kit_candidates.json` (18 staged kits)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/ENDGAME_ENCOUNTER_CATALOG` reference (your seam; mob HP profile)
- `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` (jack-ryan canonical thresholds; KPM band per cohort)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #18 (math-hotspot routing) + #40 (scaffold-with-pending-decision) + #46 § 7 (per-cell bounding)
- B14.5 V1 calibration-loop infrastructure (your seam familiarity)

## Discipline #46 compliance

- Calibration loop iterations should follow per-cell bounding patterns where applicable
- EXPLAIN QUERY PLAN at any new DB queries during calibration empirical capture
- Bounded query patterns at telemetry capture per cohort

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:**
  1. Existing B14.5 V1 calibration-loop infrastructure can absorb SC-7 calibration without new methodology
  2. Single-tier base-damage calibration can produce in-band KPM across 65× mob HP variance via encounter-sweep aggregation
  3. 18 Phase 2 staged kits are representative enough sample size for calibration (vs full Phase 2 production scale)
  4. Phase 7 cohort midpoint ±0.25 band is achievable for ALL 5 cohorts simultaneously
- **Q2 refutation evidence to seek:** verify calibration loop infrastructure absorbs scope without methodology gap; smoke-test on 3-5 kit subset before full 18-kit run; check per-cohort distribution post-calibration
- **Q3 outcome trigger:** if methodology depth exceeds your judgment, invoke Discipline #44 framing-refusal + route to legolas Mode A per Discipline #18 hotspot

## Scope

### Part 1 — Calibration loop setup (~0.5 day)

- [ ] Configure existing B14.5 V1 calibration-loop infrastructure for SC-7 scope
- [ ] Input: 18 Phase 2 staged kits + ENDGAME_ENCOUNTER_CATALOG + Phase 7 cohort midpoint ±0.25 band (per jack-ryan `3d4eda5`)
- [ ] Output: calibrated `BASE_SPELL_DAMAGE_L50 = {T1, T2, T3, T4}` per-tier values
- [ ] Calibration objective: KPM distribution across encounter sweep falls within Phase 7 band for all 5 cohorts (Support / Control / Defensive / Damage / Hybrid)

### Part 2 — Calibration loop run (~0.5-1 day)

- [ ] Run calibration loop with starting estimates `{300, 450, 650, 1200}` as initial seed
- [ ] Per-kit run + per-encounter KPM measurement + cohort classification + band check
- [ ] Iterate per-tier values per existing calibration-loop convergence semantics
- [ ] Capture empirical convergence trajectory (telemetry)

### Part 3 — Per-cohort verification (~0.25 day)

- [ ] Post-calibration: verify per-cohort KPM distribution across all 5 cohorts
- [ ] Verify no cohort saturates (all kits PASS) OR starves (all kits FAIL)
- [ ] Substrate-led discipline preserved (no pre-imposed cohort taxonomy)

### Part 4 — Update BASE_SPELL_DAMAGE_L50 values (~0.25 day)

- [ ] Update `per_skill_emitter.py` lines 38-50 with calibrated `{T1, T2, T3, T4}` values
- [ ] Inline comment cross-reference: Wave 0.5 STARTING ESTIMATE retired; gamora SC-7 calibration 2026-05-28
- [ ] Math note amendment at `per-skill-emitter-math-*.md` or new SC-7 calibration math note (your judgment; Discipline #1)

### Part 5 — Smoke-test post-calibration (~0.5 day)

- [ ] Re-run Phase 3 (per rocket's `run_phase3_from_staged_phase2()`) with calibrated values
- [ ] Verify 18 staged kits produce `season_emit=True` (or empirically explain rejections)
- [ ] Verify Principle 6 round-trip still PASS (combatant.from_player_class field-presence)
- [ ] Verify BC coordinate validity preserved post-calibration

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md`
- [ ] Tag at completion: `gamora/v1.8-sc-7-base-spell-damage-calibration-1`
- [ ] Empirical capture artifact at `agentic_orchestration/cycle-14-wave-5-season-001/sc-7-calibration-telemetry.json` (per-tier convergence + per-cohort KPM distribution + final values)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt's per-cycle push pattern

## Acceptance criteria

- [ ] Calibrated BASE_SPELL_DAMAGE_L50 values landed in per_skill_emitter.py
- [ ] Per-cohort KPM distribution within Phase 7 ±0.25 cohort midpoint band for all 5 cohorts
- [ ] 18 Phase 2 staged kits produce `season_emit=True` post-calibration (or empirically explain rejections)
- [ ] Principle 6 round-trip preserved
- [ ] BC coordinate validity preserved
- [ ] Math note authored / amended (Discipline #1)
- [ ] Empirical telemetry artifact filed
- [ ] Tag cut + AGENT_STATE.md updated
- [ ] Completion record + commit + push

## Out of scope

- Do NOT modify Phase 2 generation (gamora seam touchpoint; staged output LOCKED)
- Do NOT modify rocket Phase 3 re-impl at engine `96f5e32` (rocket seam; LOCKED per Gate-2 PASS)
- Do NOT touch Phase 7 thresholds (jack-ryan canonical `3d4eda5` LOCKED)
- Do NOT touch Phase 4 mechanical archive (gamora `749d5aa` LOCKED)
- Do NOT promote calibrated values without empirical convergence (Discipline #11 empirical-inspection)
- Do NOT introduce new scaffold-with-pending-decision values (Discipline #40)

## Open questions for gamora

- **Q-SC7-1:** Calibration objective function — minimize KPM dispersion across cohorts vs minimize total reject count vs hybrid? Your judgment per existing calibration-loop conventions
- **Q-SC7-2:** Per-tier degrees of freedom — calibrate 4 independent values (T1/T2/T3/T4) OR enforce a tier-ratio constraint (e.g., T2/T1 = T3/T2 = ratio)? Your judgment
- **Q-SC7-3:** Convergence acceptance threshold — what KPM dispersion does the calibration loop drive below before declaring convergence? Per-cohort or aggregate?
- **Q-SC7-4:** Methodology depth — does this fit existing B14.5 V1 calibration loop OR require legolas Mode A consultation? Invoke #44 framing-refusal if escalation needed

## References

- Wave 0.5 math note § 7 (STARTING ESTIMATE + SC-7 deferral note canonical authorization)
- Rocket Phase 3 re-impl `96f5e32` (cascade finding source)
- Jack-ryan Gate-2 PASS-with-WARN (cascade framing confirmation)
- Phase 7 canonical thresholds `3d4eda5` (KPM band + cohort midpoints)
- Discipline #18 + #40 + #11 + #46

---

## Completion record

(append on completion)
