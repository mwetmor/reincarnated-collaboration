# Gate-2 Submission — star-lord F4 telemetry consume (schema v2.20)

**Submitter:** star-lord
**Date:** 2026-07-07
**Tag:** `star-lord/v-batch2-f4-telemetry-consume-1`
**Dispatch:** `agentic_orchestration/dispatches/2026-07-07-star-lord-f4-telemetry-migration-consume.md`
**Reviewer:** jack-ryan

## What this implements

MIGRATION v1.84 consume side (gamora's F4 escape-lane producer already shipped at `8d45f95`).

1. **Schema v2.20** — two new nullable columns on `spatial_fight_results`:
   - `escape_reached INTEGER` (NULL=pre-v2.20, 0=did not escape, 1=escaped; F4 win signal)
   - `continuous_spawned_total INTEGER` (NULL=pre-v2.20, 0=non-F4, N=reinforcements minted)

2. **Scoped invariant relaxation** — `mobs_killed` is no longer bounded by `total_mob_count` for
   F4 (`escape_lane` / continuous-spawn). Six existing rooms byte-identical; tight invariant preserved.
   No DDL change to `mobs_killed`; semantic noted in `_V2_20` DDL comment and MIGRATION.md.

3. **Persist path** — `spatial_recorder.py` `_INSERT_SQL` + `write_fight_result()` persist both fields.

4. **Export/read-back** — `mean_mobs_killed` in `gauntlet_four_family_metrology_driver.py` reads
   from `run_spatial_fight()` raw dict; value now exceeds `total_mob_count` for F4 by construction.
   No export JSON shape change; no drax consumer impact.

## Acceptance evidence (Principle 6 round-trip)

Both cases GREEN in `tests/round_trip_spatial_telemetry.py::TestF4EscapeLaneTelemetrySchema220`:

```
CASE 1 (F4 escape):
  SpatialFightResult(scenario_id="escape_lane", mobs_killed=35, total_mob_count=8,
                     escape_reached=True, continuous_spawned_total=27)
  -> write_fight_result() -> DB -> SELECT
  -> mobs_killed=35 (>8), escape_reached=1, continuous_spawned_total=27
  PASS

CASE 2 (non-F4 tight invariant):
  SpatialFightResult(scenario_id="open_arena", mobs_killed=8, total_mob_count=8,
                     escape_reached=False, continuous_spawned_total=0)
  -> write_fight_result() -> DB -> SELECT
  -> mobs_killed=8 <= total_mob_count=8, escape_reached=0, continuous_spawned_total=0
  PASS
```

## Test counts

- `round_trip_spatial_telemetry`: 78 PASS (70 pre-existing + 8 new F4 tests). Zero regressions.
- Round-trip suites (r1, r3, kill-rate, WD spatial, b11 geometry): 174 PASS. Zero regressions.

## Files changed

- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` — `_V2_20` block + MIGRATIONS entry
- `reincarnated-engine/src/reincarnated/telemetry/spatial_recorder.py` — `_INSERT_SQL` + `write_fight_result()`
- `reincarnated-engine/src/reincarnated/telemetry/MIGRATION.md` — v2.20 entry
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — v2.20-telemetry entry
- `reincarnated-engine/tests/round_trip_spatial_telemetry.py` — `TestF4EscapeLaneTelemetrySchema220` (8 tests)
- `reincarnated-collaboration/agentic_orchestration/dispatches/2026-07-07-star-lord-f4-telemetry-migration-consume.md` — completion record

## Out of scope (confirmed)

- gamora's `spatial_engine.py` producer: NOT touched (read-only)
- mob-constant / bar / kit-constant changes: NONE
- New telemetry beyond the three flagged items: NONE
- drax consumer JSON shape: UNCHANGED

## Production DB apply

PENDING Matt explicit authorization per ADR-006 (Matt's 2026-07-07 go authorized the code change;
production DB apply is a separate statement per ADR-006 standing gate).
