# DISPATCH — gamora Boss HP Rebase (Case 8 Canonical Scaffold Resolution)

**Authored:** 2026-05-28
**Author:** knight-rider (Cycle 14 hive-mind state orchestrator)
**Recipient:** gamora (simulation seam; ANCHOR INTENTS calibration handoff target per `ee15c96` source annotation)
**Pattern:** Pattern B (~0.75-1d; empirical sweep + cross-seam HP rebase + Track 1 re-run + smoke ≥12/18)
**Status:** PENDING — fires on jack-ryan Gate-1 PASS
**Authority:** Matt 2026-05-28 Gate-5 D1 RATIFIED — Option 1 Boss HP Rebase for Cycle 14 canonical scaffold resolution

---

## 0. AUTHORITY

Matt 2026-05-28 Gate-5 D1 ratification: *"Option 1 — Boss HP Rebase to current kit-damage population for Cycle 14. Architectural anchor: this is the CANONICAL SCAFFOLD RESOLUTION that endgame_mob_stat_profile.py 'ANCHOR INTENTS, not locked simulation targets' annotation (ee15c96, Cycle 13 SC-6) was waiting for. Not a workaround, not a Discipline #39 scaffold-fallback (D2-REJECTED territory at Gate-4 still holds). The rebase IS the calibration SC-6 deferred to Phase 7 gate."*

Jack-ryan Gate-5 disposition: `agentic_orchestration/qa/pending/2026-05-28-8th-scaffold-drift-boss-kpm-damage-gap-gate-5-disposition.md` § 4 Option 1 (full rationale + risk analysis).

Source annotation handoff: `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` line 43 verbatim: *"These ranges are ANCHOR INTENTS, not locked simulation targets."* — explicitly hands calibration to gamora at the Phase 7 gate.

---

## 1. SCOPE

### 1.1 Empirical population-DPS sweep (Discipline #11)

Measure current population DPS across all 18 production kits at boss encounters under CURRENT boss HP (factor range `(9.00, 14.00)` × `CLASS_HP_REFERENCE = 20_000` = 180k-280k effective HP). For each kit:
- Run gauntlet sim at L50 against each cohort (steamroll / balanced / hard-out / soft-out)
- Measure per-kit DPS (damage / second) at boss encounters
- Identify population-median DPS + 25th/75th percentile bands

**Critical:** the Track 1 telemetry at `cycle-14-wave-5-season-001/option-f-track-1-calibration-telemetry.json` may already contain the underlying signal; assess whether re-sweep needed or extraction from existing telemetry sufficient.

### 1.2 Target HP back-calculation (Discipline #1 math-before-code)

Math note required at `~/Games/reincarnated-engine/src/reincarnated/simulation/math/boss-hp-rebase-case-8-resolution-2026-05-28.md`:

Working backwards from Track 1 INT/WIS KPM bands (75-82 median observed):
- KPM_target = 75 (or per-archetype Track 1 band median)
- KPM = (DPS × 60) / boss_HP
- boss_HP_target = (DPS × 60) / KPM_target

Compute new `ENDGAME_TIER_HP_FACTOR_RANGE["boss"]` from population-median DPS. Show derivation. Include sensitivity analysis: what if KPM target = 50 vs 75 vs 100? What if population DPS distribution shifts ±20%?

**Cross-cohort variance operationalization (jack-ryan Gate-1 Amendment B):** median DPS target = population median at Balanced cohort (primary calibration anchor); range width `(lo, hi)` spans steamroll/hard-out spread empirically — report 25th/75th percentile DPS across cohorts as the lo/hi bounding inputs to the new HP factor range. This operationalizes the cross-cohort risk at § 5 and removes execution-time judgment from the decision.

**Mini-boss tier decision rule (jack-ryan Gate-1 Amendment A):** if Track 1 telemetry contains ≥6 mini-boss encounter KPM observations across ≥2 cohorts, rebase mini-boss tier proportionally per same method (Balanced median anchor + 25th/75th percentile spread). Otherwise, preserve `(5.00, 8.00)` unchanged, document as Cycle 14-deferred in MIGRATION.md § v1.39 with explicit forward-link to "Cycle 15 per-tier calibration sweep" gate. No discretionary path; gamora has the decision rule.

### 1.3 Cross-seam rebase (ADR-004)

File: `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` (rocket-owned seam; gamora touches per ANCHOR INTENTS source-annotation handoff at line 43).

Changes:
- Update `ENDGAME_TIER_HP_FACTOR_RANGE["boss"]` from `(9.00, 14.00)` to empirically-derived range
- Update `ENDGAME_TIER_HP_FACTOR_RANGE["mini-boss"]` from `(5.00, 8.00)` if Track 1 telemetry supports (else preserve and note rationale)
- Update inline comments to reflect calibration completion: replace "ANCHOR INTENTS, not locked simulation targets" with calibration provenance ("calibrated via boss-hp-rebase-case-8-resolution math note; Phase 7 gate empirical signal; SC-6 scaffold resolution complete")
- Preserve historical commit reference to `ee15c96` for trace

**MIGRATION.md filed** at `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.39 (or next available) capturing:
- Cross-seam touch (gamora → generation file per ANCHOR INTENTS handoff)
- Calibration provenance (math note + empirical sweep)
- Source annotation update (scaffold resolution complete)
- Cross-reference to Gate-5 disposition + Matt D1 ratification

### 1.4 Track 1 re-run + acceptance

Re-run `run_track1_archetype_sweep()` against NEW boss HP. Expected outcomes:
- INT/WIS bands re-calibrated against broader kit population (not artillery_mage outlier only)
- STR/DEX bands populated (no more FALLBACK; physical kits now produce measurable boss KPM)
- 16-cell band table values change; Track 1 infrastructure re-activates as intended

Run full smoke production season. **Acceptance: season_emit ≥ 12/18 kits.** (Required ≥12/18 per Wave 5 Position B / D4 cadence.)

### 1.5 Canonical doc update

`~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` § 3.9 — populate new 16-cell band table with post-rebase empirical values; remove FALLBACK notation; cross-reference to boss-HP-rebase math note.

**Note:** Discipline #40 case (c) third iteration on the canonical doc is JACK-RYAN'S responsibility per parallel dispatch (`2026-05-28-jack-ryan-phase-7-canonical-retraction-third-iteration.md`); gamora populates § 3.9 band table values once Track 1 re-run completes; jack-ryan files retraction record §§ 3.11+ documenting the canonical authority shift.

### 1.6 AGENT_STATE + tag

- AGENT_STATE.md updated post-completion
- Tag: `gamora/v2.1-boss-hp-rebase-1` per Matt D3 ratification

---

## 2. REQUIRED READING

Substrate context:
- `~/Games/reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` (full file; source annotation at line 43)
- Git blame at `ee15c96` (Cycle 13 SC-6 commit; ANCHOR INTENTS rationale)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/option-f-track-1-per-damage-path-kpm-bands-2026-05-28.md` (Track 1 math note)
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-calibration-telemetry.json` (Track 1 empirical sweep)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/sc7_calibration_loop.py` (`run_track1_archetype_sweep()` re-run target)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (Phase 7 gate; `_ARCHETYPE_COHORT_KPM_BAND` registry)

Disposition + ratification:
- `agentic_orchestration/qa/pending/2026-05-28-8th-scaffold-drift-boss-kpm-damage-gap-gate-5-disposition.md` (jack-ryan Gate-5 disposition; Option 1 § 4 + rationale § 5)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT GATE-5 RATIFICATIONS LOCKED 2026-05-28" (Matt D1+D2+D3 + case-register reframing)

Disciplines:
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #1 math-before-code, #11 empirical inspection, #18.1 pre-fire resource projection, #39 scaffold framework, #40 case (c) canonical retraction (jack-ryan's concurrent), #45 vocabulary lock

Cross-seam coordination:
- `~/Games/reincarnated-collaboration/agentic_orchestration/GOVERNANCE.md` ADR-004 (MIGRATION.md cross-seam handoff)

Canonical doc:
- `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` § 3.7-3.10 (current state)
- `~/Games/reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-26.md` § 3 (4 damage-scaling paths; mechanical partition)

---

## 3. DELIVERABLE + ACCEPTANCE

| # | Artifact | Location |
|---|---|---|
| 1 | Empirical population-DPS sweep telemetry | `agentic_orchestration/cycle-14-wave-5-season-001/boss-hp-rebase-empirical-dps-telemetry.json` |
| 2 | Math note (Discipline #1) | `~/Games/reincarnated-engine/src/reincarnated/simulation/math/boss-hp-rebase-case-8-resolution-2026-05-28.md` |
| 3 | Updated `endgame_mob_stat_profile.py` boss HP factor range + comment | rocket-owned file; cross-seam touch per ANCHOR INTENTS handoff |
| 4 | MIGRATION.md § v1.39 | `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` |
| 5 | Track 1 re-run telemetry post-rebase | `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` |
| 6 | Canonical doc § 3.9 16-cell band table populated with post-rebase values | `~/Games/reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` |
| 7 | Smoke production season ≥12/18 emit | gauntlet sim + season generation pipeline |
| 8 | AGENT_STATE.md updated | `~/Games/reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` |
| 9 | Tag `gamora/v2.1-boss-hp-rebase-1` | engine commit |

**Acceptance criterion: ≥12/18 production season emit** under new boss HP factor range.

**Commit + push pattern:** auto-commit per CLAUDE.md addendum (Matt D1 ratification authorizes the work; commit auto-fires); auto-push per Cycle 14 per-workstream push pattern (D11; gamora pushes after dispatch lands).

---

## 4. OUT OF SCOPE — explicit

- **Do NOT modify** `base_physical_damage_l50` (SC-6b) or `BASE_SPELL_DAMAGE_L50` (SC-7). Per jack-ryan Gate-5 § 3.1, those are second/third co-implicated constants whose calibration is deferred to Cycle 15 architectural commit (Option 6 damage/HP% metric replacement; D2 Matt ratification).
- **Do NOT widen T1 REJECT threshold** (`TIER_1_REJECT_THRESHOLD = 0.30`). Per Option 4 explicit rejection.
- **Do NOT touch generation kit-skill-base-damage values per-skill.** Per Option 3 deferral (Cycle 15 path via Option 6 metric replacement).
- **Do NOT author Phase 7 canonical retraction record §§ 3.11+.** That is jack-ryan's concurrent dispatch.
- **Do NOT touch Option F Phase 1 stratified floor or KPM=600.0 ceiling-artifact bypass.** Per D2 (Gate-4) Phase 2 per-encounter-type bands subsumed by Option 6 single-metric architecture (Cycle 15); KPM=600.0 investigation retains Cycle 15 scope.

---

## 5. RISKS + COMPLICATIONS

- **Population-DPS variance high.** If population-median DPS varies materially across cohorts (steamroll vs hard-out), single rebase value may not produce broad emit signal across all cohorts. **Resolved via Amendment B operationalization at § 1.2:** Balanced cohort = primary calibration anchor; range width spans empirical 25th/75th percentile across cohorts.
- **mini-boss tier rebase decision-rule.** **Resolved via Amendment A operationalization at § 1.2:** ≥6 observations across ≥2 cohorts → rebase mini-boss proportionally; else preserve + Cycle 15 forward-link in MIGRATION.md.
- **Cross-seam ADR-004 friction.** Touching `endgame_mob_stat_profile.py` requires MIGRATION.md; the file lives in generation/ (rocket seam). The source annotation explicitly pre-authorizes the handoff, but rocket is informed via MIGRATION.md update and may file a future audit on the new values' consistency with rocket's substrate generation expectations (low risk; rocket SC-6 commit authored the ANCHOR INTENTS scaffold expecting this gate).
- **Track 1 re-run cost.** `run_track1_archetype_sweep()` is the longest single sim operation; budget ~30-60min wall time + per-cohort assertions. Pre-fire resource projection per Discipline #18.1 — if peak memory exceeds host RAM, scope-reduce per cohort sequence.

---

## 6. COORDINATION

- **Jack-ryan parallel dispatch:** `2026-05-28-jack-ryan-phase-7-canonical-retraction-third-iteration.md` (Discipline #40 case (c) third iteration on Phase 7 doc §§ 3.11+; ~0.25d; tag `jack-ryan/v1.5-phase-7-canonical-retraction-3`). Jack-ryan reads gamora's Track 1 re-run telemetry post-completion to author retraction record with empirical anchor.
- **No rocket sub-agent dispatch.** Per ANCHOR INTENTS source-annotation handoff, rocket informed via MIGRATION.md. If rocket discovers downstream inconsistency post-rebase, files separate dispatch (Cycle 15 territory at minimum).
- **Wave 5 cascade resumes post completion.** KR fires Wave 5 Step 1 production seasons (3 per D4) post Track 1 re-run smoke PASS.

---

## 7. URGENCY

**Cycle 14 v1 close trajectory: ~4-6 days from this dispatch firing.** Each day of delay shifts v1 tag accordingly. D13 P1-P9 parallel framework gates on Wave 5 Gate-2 PASS, which gates on this resolution.

Fire ASAP on jack-ryan Gate-1 PASS.

---

**KR signature:** authored per Matt 2026-05-28 Gate-5 D1+D3 ratification + jack-ryan Gate-5 § 4 Option 1 + ANCHOR INTENTS source-annotation handoff at `ee15c96` Cycle 13 SC-6. Case 8 = first canonical scaffold resolution per Matt's case-register reframing. Discipline #18.1 + #1 + #11 + #40 case (c) coordination + #45 vocabulary lock all load-bearing.
