# Gate-2 submission — Step 3: mob-lethality calibration (STOP-and-flag) + R4 ship-gate flip

**From:** gamora (simulation seam)
**To:** jack-ryan (Gate-2, DEV-MODE, BLOCK authority)
**Date:** 2026-07-07
**Dispatch:** `agentic_orchestration/dispatches/2026-07-07-gamora-step3-mob-lethality-calibration-stratified-repilot.md`
**Tag:** `gamora/v-batch2-step3-mob-lethality-calibration-1` (engine `08972d0`; push HELD — Matt-gated)
**Why Gate-2:** mob-constant-path code + the R4 certification-contract flip = certification-path code (dispatch scope).

---

## What to review

**1. R4 ship-gate flip (EXECUTED) — `gauntlet_sim.py:854`**
`GauntletKitResult.gauntlet_pass()` now `return self.family_certification_pass(cohort)` (was legacy `eligible_encounters_passed >= 9-of-18 W-α6`). Four-family conjunction; STR carve-out retires. **Discipline #12 semantic shift** framed in-code (`:825-847`), math note §6, MIGRATION v1.85.
- Cross-seam behavioral consequence (NO schema change): `season_emit` rides the new gate → `season_generation_pipeline.py:1681-1816` (rocket) season-content set contracts to zero until Lane-3 registers the F4 band AND calibration lands (F4 currently un-passable → `family_certification_pass` False universally today — correct not-yet-certifiable state). Bool unchanged; truth-conditions shift.
- **Decisions-log entry is YOURS to write** (R4 certification-contract shift; already flagged in metrology §6/§7 + Lane-1 build §7).

**2. Calibration — STOP-and-flag (NO code change to constants; Disc #24 hotspot)**
Math note `simulation/math/step3-mob-lethality-calibration-2026-07-07.md` + probe `scripts/gamora_step3_calibration_probe_2026_07_07.py` → `output/step3_calibration/step3_probe.json`.
- **Lever (a) "mob damage UP" is INERT** on the metrology instrument: mob damage-per-hit = 0.0, unchanged at damage_multiplier 1×→32× (direct `resolve_spatial_hit` measure + F3 sweep). Root cause: metrology driver + build-smoke hand-roll a damage-LESS mob dict (`effect_category` string, not an `effects` list) → typed death channel selected → `MOB_DAMAGE_SCALE` inert → `resolve_skill` accumulates only `"damage"`-named effects → zero. **This refines your §7 WR=1.0 reading: rooms don't kill because the mob-damage channel is structurally dead, not "too easy" tunably.**
- Fix is canonical (magnitude-source Q closed): source mob skills from `emit_skills_for_threat_tier` (`spatial_engine.py:3122` names it as the intended source). Proven to open a real two-sided surface (dead channel F2/F3 WR 1.0; canonical-full WR 0.0). **NO knob tuned, NO constant moved, NO bar/band moved.** Flagged to knight-rider for the instrument-fix ruling (this is the parallel-methodology-check checkpoint you're running).

## Cited verification points (Discipline #11 — verify vs SOURCE, not smoke)
- R4 routing: `GauntletKitResult.gauntlet_pass` returns `self.family_certification_pass(cohort)` (`:854`); `family_certification_pass` = `all(family_passed(cohort, fam) for fam in _ALL_FAMILIES)` (`:785`). F4 `escape_lane` has no band in `_shell_result_passed` → un-passable → gate False today (intended).
- Frozen guard: NO kit-side chassis constants touched (`BASE_PHYSICAL/SPELL_DAMAGE_L50`, 2.3384× fossil). `git show 08972d0 --stat` = 7 files, none in `element/`/`generation/`/`telemetry/`/`export/`.
- Probe determinism: seed 65M (probe), 66M (canonical-emitter confirm); next free 67M+ (Disc #3).

## Regression (Discipline #2 — re-run recommended, don't trust GREEN)
- `tests/test_cycle13_wave5_gauntlet_sim.py` **50/50** — 5 legacy-floor tests rewritten to the four-family contract (`test_gauntlet_pass_requires_all_four_families` = carve-out retired; `test_gauntlet_fail_if_any_family_fails`; `test_f4_band_unregistered_blocks_certification_pending_lane3`; `season_emit`/`to_dict` updated), helper `_make_four_family_kit` added.
- `test_phase7_bridge` + `test_wave5_swift_closure_provisional_marker` + `test_cascade_r4_amendment_1` + `test_cycle14_wave5_loadout_emission` **151/151**.
- Broader spatial+gauntlet+wave5+cycle13 slice: **868 PASS / 1 pre-existing fail** (`...phase5_cohesion_judge...smoke` — LLM/P5 seam; **verified fails identically with R4 changes stashed**, not this seam) / 4 pre-existing rocket grouping-vocab collection errors.
- `gauntlet_sim.py` py_compile OK.

## Known deferrals (Rider-scoped, NOT defects)
- F4-martial KPM (Rider 2): MEASURED (metrology §7 median 23.9, below 60 floor); NOT acted on; kit-side deferred.
- The mob-lethality calibration + stratified re-pilot + F-b closing read: BLOCKED on the instrument-fix ruling (STOP). NOT executed here.

**Requested:** Gate-2 verdict on the R4 flip (certification-path code) + the STOP-and-flag disposition (methodology). Decisions-log R4 entry is yours to author.
