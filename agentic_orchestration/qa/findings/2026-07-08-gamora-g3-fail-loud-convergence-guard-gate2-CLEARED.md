# Gate-2 Submission — 2026-07-08 — gamora: G3 fail-loud convergence guard on the spatial fight loop

**Submitter:** gamora (simulation seam — PRIMARY on the co-diagnosis)
**Reviewer:** jack-ryan (Gate-2)
**Tag:** `gamora/v-spatial-fail-loud-convergence-guard-1`
**Authority:** dispatch `2026-07-08-gamora-starlord-spatial-floor-diagnosis.md` G3 (rider 2 —
  REQUIRED deliverable, unconditional; ships regardless of the G1/G2 disposition).
**MIGRATION.md:** **NONE required** — no boundary field moves. The guard raises an exception; it does
  NOT add/change any `SpatialFightResult` field, telemetry schema, or balance constant. (G1 moved no
  constant — design-finding path — so the gamora half has no MIGRATION obligation per the dispatch's
  Principle-6 gate.)
**Files changed (all gamora-owned, within-seam):**
  - `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — new `SpatialFightConvergenceError`
    + budget constants/helper + three-layer guard in `SpatialFightEngine.run()` + fail-loud propagation
    in `run_spatial_fight`'s batch loop.
  - `src/reincarnated/simulation/spatial_gauntlet/__init__.py` — export the new exception.
  - `src/reincarnated/simulation/spatial_gauntlet/_g3_convergence_guard_fire_smoke.py` — NEW positive-fire smoke.
  - `src/reincarnated/simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md` — math note (authored FIRST, Disc #1).

---

## What this fixes

The leg-3 Tier-1 $0 dry-run (seed 56000000) was fired twice on **byte-identical params** with divergent
liveness: **v2 HUNG** (STEP 3/4 live gauntlet wedged; process sat **silent-alive 29 min** naming no
offending unit, then vanished); **v3 COMPLETED** (25,530 fights, 1588s). Identical params → hang-vs-complete
means the wedge is **INTERMITTENT** (state-dependent, not parameter-dependent) — it will recur
unpredictably, and at Leg-C scale the recurrence probability compounds. A 29-min silent-alive wedge that
names no unit is a Disc-#24-shape **fail-loud violation**.

## Mechanism (Discipline #11 honesty)

Every loop in the stack is *structurally* bounded under nominal state (`gauntlet_sim` triple for-loop →
bounded `n_fights` batch → bounded outer `while elapsed < max_duration` advancing `elapsed += tick_size`).
Therefore the wedge is a **state-dependent non-advancement of simulated time** under some seed/entity
interaction — NOT a deterministic infinite loop. I did **NOT** reproduce the exact v2 trigger (intermittent;
the v2 process is gone). The correct posture for an intermittent fault is to **fail loud on the invariant
violation (simulated time not advancing) and name the unit**, rather than depend on having isolated one
root cause. Highest-risk site identified: the nested continuous-spawn `while` (spatial_engine.py:~2105),
the only nested unbounded-*shaped* loop; direct infinite-loop if `interval_s ≤ 0`.

## What changed — three fail-loud layers (all name class+scenario), math note §3

- **Layer A — tick-budget** (outer-loop, simulated-time invariant): a fight advances at most
  `ceil(max_duration/tick_size)+8` ticks. Exceeding the budget while still looping ⇒ `elapsed` not
  advancing ⇒ `SpatialFightConvergenceError`. Reuses the existing `_tick_counter` (single source of truth).
- **Layer B — continuous-spawn catch-up cap** (nested `while`): capped at `ceil(max_duration/interval_s)+8`
  for `interval_s > 0`; for the degenerate `interval_s ≤ 0` (the DIRECT infinite-loop cause) capped at a
  small constant so it fails loud IMMEDIATELY (a naive `max(interval, ε)` denominator would have
  mis-bounded to ~1e10 iterations — an effective hang; caught and fixed during smoke).
- **Layer C — wall-clock watchdog** (scale-invariant backstop): per-tick `time.monotonic()` check against
  `max(30, 50·max_duration/60)` s (env-overridable via `REINCARNATED_SPATIAL_FIGHT_WALL_BUDGET_S`).
  Bounds the 29-min silent-alive class of wedge to seconds even if A/B are somehow bypassed.
- **Propagation** (`run_spatial_fight` batch loop, math note §3.4): a wedged fight is caught, logged
  `ERROR` with kit/scenario/fight-idx/seed context, and **re-raised** — never silently swallowed.

## Smoke (Discipline #2) — `_g3_convergence_guard_fire_smoke.py`

| Case | Result |
|---|---|
| A — Layer B (interval_s=0.0) | **FIRED LOUD in 0.001s**, message names class+scenario, NOT a hang |
| B — Layer C (0.001s wall budget) | **FIRED LOUD in 0.002s**, "wall-clock budget exceeded", names class+scenario |
| D — regression-neutral (nominal magic_pack fight) | **ran clean, guard INERT** (no false positive) |

## Regression (Discipline #2 acceptance §4.1) — guard is byte-neutral on nominal fights

- `test_spatial_gauntlet_scenarios` + `test_telemetry_v23` + `test_cycle13_wave5_gauntlet_sim` +
  `round_trip_spatial_telemetry`: **180 passed**.
- `test_w010_boss_ai_focus` + `test_w093_usage_modes` + `test_w094_performance` + `test_w095_telemetry` +
  `test_wd_spatial_bc_measurement`: **132 passed**.
- **Total 312 spatial tests pass, 0 failures.** (4 pre-existing collection errors in naming/vocab test
  files — `RuntimeError: Cannot locate grouping-layer-vocab` — are unrelated to this change; they are
  outside the spatial seam and fail on a missing vocab asset.)

## What this is NOT
- NOT a difficulty change — touches no `MOB_HP_DIFFICULTY_MULTIPLIER`, bar, band, or kit/balance constant.
- NOT a root-cause fix for the specific v2 trigger — it is a fail-loud *invariant guard* that converts the
  silent-wedge class into an immediate named halt (the G3 deliverable). Root-cause isolation of the specific
  spawn-cadence interaction, if it recurs, is now *tractable* (the guard captures class+scenario+state) and
  is a NAMED follow-up.

## Requested Gate-2 disposition
PASS (or PASS-WITH-INFO). Within-seam liveness safety rail; math-note-first; smoke fires loud + regression
byte-neutral; no boundary field / no MIGRATION obligation.
