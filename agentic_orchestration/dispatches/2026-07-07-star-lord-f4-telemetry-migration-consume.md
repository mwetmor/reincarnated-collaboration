# Dispatch — 2026-07-07 — star-lord — F4 telemetry MIGRATION v1.84 consume (escape fields + mobs_killed range)

**From:** knight-rider
**To:** star-lord (export/telemetry seam)
**Approved by:** Matt 2026-07-07 ("the two queued flags fire with this go" — this is the star-lord half; the R4 flip is gamora's half)
**Estimated effort:** small–medium (schema widen + invariant relaxation + round-trip; telemetry-boundary change)
**Acceptance:** the F4 fight-result fields produced by gamora's Lane-1 build (`escape_reached`, `continuous_spawned_total`) persist and read back through the telemetry/export path, and the `mobs_killed` invariant is relaxed to admit F4's continuous-spawn range (F4 `mobs_killed` is unbounded by initial spawn count), with a round-trip smoke and no regression to the six existing rooms.

## Context — the deferred obligation now going live

gamora's Lane-1 build (`8d45f95`, Gate-2 PASS) added two additive `SpatialFightResult` fields for F4 (`escape_reached`, `continuous_spawned_total` at `spatial_engine.py:2868-2869`) plus a `mobs_killed` range semantic-shift (F4's continuous spawner makes `mobs_killed` unbounded by the initial `total_mob_count`). At Gate-2, jack-ryan determined these were **safe as additive/unpersisted/unconsumed** — star-lord's obligations go live **only when export/persistence needs the F4 fields on-disk.** MIGRATION v1.84 (gamora, `simulation/MIGRATION.md`) documents the producer side and flags the star-lord consume.

Step 3 (gamora's stratified re-pilot, running IN PARALLEL) exercises F4 and benefits from F4 telemetry persisting for analysis. So the consume goes live now.

**Coordination:** gamora is dispatched in parallel for the Step-3 calibration + R4 flip. You own the CONSUME side (schema/persist/read-back); gamora owns the PRODUCE side (already shipped in Lane 1). Coordinate via MIGRATION v1.84 — do not touch gamora's `spatial_engine.py` producer; wire the telemetry/export consumer.

## Required reading before starting
- `simulation/MIGRATION.md` v1.84 entry (gamora's producer-side contract + the flagged consume — the authoritative handoff).
- `spatial_engine.py:2868-2869` (the two new fields — READ ONLY, gamora's producer).
- Your telemetry recorder + schema: the `SpatialFightResult` persist path, the SQLite `_INSERT_SQL`, and the `mobs_killed ≤ total_mob_count` invariant jack-ryan cited at Gate-2 (verify the exact site).
- `agentic_orchestration/qa/findings/2026-07-07-gamora-gauntlet-four-family-instrument-gate2.md` (jack-ryan's cross-seam determination — the precise scope of what's needed).
- Run-state `batch2-run-state-2026-07-06.md` Lane-3 RESULT block (downstream flag #2 — this dispatch).

## Math/design-before-code (Discipline #1)
- Document the exact schema delta (which columns/keys added) and the invariant relaxation: `mobs_killed` is bounded by `total_mob_count` ONLY for non-continuous rooms; for F4 (continuous spawn) it is unbounded — the relaxation must be SCOPED so the six existing rooms still assert the tight invariant (don't blanket-remove it).

## Cross-seam contract change? (Principle 6 gate — YES)
**YES — telemetry-boundary change.** Acceptance MUST include a **round-trip smoke:** an F4 fight-result with `escape_reached` + `continuous_spawned_total` + a `mobs_killed` exceeding initial spawn → persist → read-back → values intact; AND a non-continuous room (e.g. F1/F2/F3) still asserts `mobs_killed ≤ total_mob_count` (invariant preserved where it should hold). **MIGRATION.md REQUIRED** — update your telemetry/export MIGRATION in lockstep with the v1.84 producer entry.

## Scope
- [ ] Design/math note (schema delta + scoped invariant relaxation) first.
- [ ] Widen the telemetry schema / persist path to carry `escape_reached` + `continuous_spawned_total`.
- [ ] Relax the `mobs_killed` invariant SCOPED to continuous-spawn rooms; preserve the tight invariant for the six existing rooms.
- [ ] Confirm export/read-back consumes `mean_mobs_killed` correctly with the widened range.
- [ ] Round-trip smoke (both cases above) GREEN.
- [ ] Regression clean; six existing rooms' telemetry byte-behavior unchanged.
- [ ] MIGRATION.md lockstep with v1.84.
- [ ] AGENT_STATE.md updated.
- [ ] Tag: `star-lord/v-batch2-f4-telemetry-consume-1`.
- [ ] **Submit tagged commit to `agentic_orchestration/qa/pending/` for jack-ryan Gate-2** (telemetry-boundary change).

## Out of scope
- **NO change to gamora's producer** (`spatial_engine.py` F4 fields) — consume side only.
- **NO mob-constant / bar / kit-constant changes** — that's gamora's Step-3 / frozen.
- **NO new telemetry beyond the three flagged items** (escape_reached, continuous_spawned_total, mobs_killed range).

## References
- MIGRATION v1.84 (producer contract); Gate-2 finding `qa/findings/2026-07-07-gamora-gauntlet-four-family-instrument-gate2.md`
- ADR-004 (MIGRATION), Principle 6 (round-trip), Disciplines #1, #8 (schema-at-boundaries), #11, #12
- Run-state `batch2-run-state-2026-07-06.md` (downstream flag #2)

## Completion record

**Completed:** 2026-07-07
**Tag:** `star-lord/v-batch2-f4-telemetry-consume-1`
**Status:** ALL SCOPE ITEMS COMPLETE

### Schema delta (math/design note — Discipline #1)

Three changes, no DDL on `mobs_killed`:
1. `spatial_fight_results.escape_reached INTEGER` NULL (NULL=pre-v2.20, 0=did not escape, 1=escaped)
2. `spatial_fight_results.continuous_spawned_total INTEGER` NULL (NULL=pre-v2.20, 0=non-F4, N=reinforcements)
3. `mobs_killed` range semantic: unbounded for F4 (documented in `_V2_20` DDL comment; no DDL change)

### Scoped invariant approach

`mobs_killed <= total_mob_count` is NOT enforced in `validate()` — it is a semantic contract in comments/tests. The relaxation is scoped by the discriminant `continuous_spawned_total > 0` (or `scenario_id == 'escape_lane'`). Six existing rooms remain byte-identical. Tight invariant is preserved and asserted in the new `test_non_f4_room_tight_invariant_preserved` test. F4 unbounded range is asserted in `test_f4_escape_reached_true_round_trip` (`mobs_killed=35 > total_mob_count=8`).

### Round-trip smoke result

```
CASE 1 (F4 escape): mobs_killed=35, escape_reached=1, continuous_spawned_total=27 — PASS
CASE 2 (non-F4 invariant): mobs_killed=8 <= total_mob_count=8, escape_reached=0 — PASS
78 round_trip_spatial_telemetry tests PASS. 174 other round-trip + spatial tests PASS. Zero regressions.
```

### Files committed
- `telemetry/migrations.py` — `_V2_20` + MIGRATIONS entry `("2.20", ...)`
- `telemetry/spatial_recorder.py` — `_INSERT_SQL` (24 cols) + `write_fight_result()` persist
- `telemetry/MIGRATION.md` — v2.20 entry (top)
- `export/MIGRATION.md` — v2.20-telemetry entry (top)
- `tests/round_trip_spatial_telemetry.py` — `TestF4EscapeLaneTelemetrySchema220` (8 tests)
- `export/AGENT_STATE.md` — updated
- `agentic_orchestration/qa/pending/2026-07-07-star-lord-f4-telemetry-consume-gate2.md` — submitted

### Production DB apply
PENDING Matt explicit authorization per ADR-006. No DB write executed in this session.
