# Finding — 2026-07-09 — gate2-gamora-clear-time-floor-guard

**Reviewer:** jack-ryan
**Severity:** INFO (PASS)
**Target:** commit `9154f81` / tag `gamora/v1.4-clear-time-floor-guard-1`
**Developer:** gamora
**Principles applied:** #1 (math-before-code), #2 (smoke-gate), #3 (cross-seam impact), #4 (decisions-log as truth), #5 (severity/attribution)

## What I found

gamora's clear-time floor guard is a clean, spec-faithful, sim-internal instrument fix that passes all five Gate-2 review principles with no amendments. `StratumFightBatch.observed_kpm` now floors each fight's clear-time at `T_floor = CLEAR_SHELL_DOMAIN_TMIN_S` (1.0 s / 10 ticks) BEFORE the KPM ratio (`floored_duration_s = sum(max(f.duration_s, CLEAR_SHELL_DOMAIN_TMIN_S) for f in self.fights)`), de-censoring the KPM instrument at the root. The code is a verbatim match to the shipped-remedy spec (`elite-pack-kpm-cap-2026-07-09.md` §2, REMEDY 2). The smoke harness demonstrates BOTH required properties (de-censoring AND floor-not-clamp). The change touches no cross-seam contract, no band, and no telemetry field. It is consistent with the Q14 decisions-log entry I authored (`f532cb7`) on every clause.

### Principle-by-principle

1. **Math-before-code (Disc #1): PASS.** Code matches the note. Spec `elite-pack-kpm-cap-2026-07-09.md` §2 derives `T_floor = ceil((TICK_SIZE/band_half_width)/TICK_SIZE) × TICK_SIZE = ceil(0.9346/0.1)×0.1 = 10 ticks = 1.0 s`; `CLEAR_SHELL_DOMAIN_TMIN_S = 1.0` (t4_sim_cycling.py:117) is that value, inherited from the STANDING 2026-06-21 domain-guard precedent (not a new magic number). The in-domain KPM ceiling `3×60/1.0 = 180` matches the note. Companion note `lurch-semantics-refinement-2026-07-09.md` is note-only per ruling (iv), no impl.

2. **Smoke-gate (Disc #2): PASS — re-run by reviewer.** `python3 -m reincarnated.simulation.clear_time_floor_guard_smoke_2026_07_09` reproduced live. De-censoring shown: 0.4 s (450-cap pin) → 180; 0.3 s (600, above cap) → 180; 0.5 s (E2 offensive-tail) → 180. Floor-NOT-clamp shown: 2.0 s normal clear UNCHANGED at 90; mixed 5×0.4s + 5×2.0s floors only the fast fights (150→120). Boundary case (1.0 s exactly) reads at ceiling, a no-op boundary. Both required demonstrations present.

3. **Cross-seam impact (Principle #3 / ADR-004): CLEAN sim-internal — no MIGRATION.** Every consumer of `observed_kpm` lives in `src/reincarnated/simulation/` (gamora seam). Zero references in `export/`, `telemetry/`, `output/` (star-lord) or `generation/`/`anchor/` (rocket). This confirms the Q14 entry's prediction (audit metrics are in-JSON gamora-side → MIGRATION-free). No driver→star-lord exported KPM field is touched. No contract change.

4. **Decisions-log SSoT (Principle #4): CONSISTENT with Q14 (`f532cb7`) on every clause.** (ii) floor guard SHIPS, NOT cap-raise ✓; T_floor=1.0s/10 ticks per `ff3f33b` ✓; closes the Lane-3 elite_pack KPM=450 item (same censoring family) ✓; (iii) NO band re-fit bundled — commit touches no band/refit/anchor file, message states "Did NOT re-fit any band" ✓; (iv) lurch-semantics refinement note-only, no audit driver touched ✓.

5. **Severity/attribution (Principle #5): fixture edits legitimate, NOT masking a regression.** The 3 fixtures (`_make_batch_with_kpm`, the Tier-2 compound-gate builder, `_make_t4_sim_record`) previously manufactured KPM via `kills=1, duration=60/target_kpm` — which for target_kpm > 60 produces sub-1.0 s durations, EXACTLY the degenerate sub-domain the guard now floors. The new guard-aware strategy holds duration at a fixed 60.0 s (guard no-op) and sets `kills = round(target_kpm)` so the target hits THROUGH the guard. This re-parameterizes the fixture out of the degenerate region; it does not weaken or mask any assertion. Regression: 171/171 PASS across `test_cycle13_wave4_sim_cycling.py` + `test_cycle13_wave5_gauntlet_sim.py` + `test_cycle13_wave4_follow_on_sim_cycling_export.py` (reviewer re-ran).

### Pre-existing season_generation errors — attributed to ROCKET, not gamora

The 21 errors in `test_cycle13_wave5_season_generation.py` (reviewer reproduced: 46 passed, 21 errors) are a rocket-seam cell-grain dedup contract issue in `season_generation_pipeline.py` (`legendary_id` is cell-level per the :1713-1714 contract, not per-sample). The traceback touches zero KPM/floor-guard code — `season_generation_pipeline` and the `observed_kpm` computation site are disjoint code paths, so the errors are independent of this commit. Matches the "cell-grain dedup contract finding" in commit `a5c3848`. **Attributed to rocket (INFO for rocket-seam follow-up), NOT to gamora.** Does not block this commit.

## Rationale

All five review principles satisfied (see per-principle above). The change is anti-Goodhart-clean (Disc #12 semantic-shift framed explicitly; no tolerance widened; extends a Matt-ratified precedent rather than inventing a value) and consistent with the locked Q14 decisions-log entry. Cited: Disciplines #1, #2, #11, #12; Review Principles #3, #4, #5; ADR-004 (no MIGRATION required — no cross-seam contract touched).

## Action

- [x] Reviewer: verdict PASS — push authorized (Matt pre-authorized push-on-Gate-2-PASS for this run).
- [ ] rocket (INFO, independent): resolve the `season_generation_pipeline.py` cell-grain dedup contract violation (per `a5c3848` finding) — not this commit's concern.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/t4_sim_cycling.py` (observed_kpm guard, :271-309; CLEAR_SHELL_DOMAIN_TMIN_S :117)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/clear_time_floor_guard_smoke_2026_07_09.py` (smoke, re-run PASS)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/elite-pack-kpm-cap-2026-07-09.md` (spec §2 REMEDY 2, `ff3f33b`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/math/lurch-semantics-refinement-2026-07-09.md` (D2 note, note-only)
- `~/Games/reincarnated-engine/tests/test_cycle13_wave4_sim_cycling.py` (3 fixtures, guard-aware)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (Q14 entry, `f532cb7`)
