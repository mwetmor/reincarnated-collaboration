# Finding — 2026-07-07 — star-lord F4 telemetry consume (schema v2.20)

**Reviewer:** jack-ryan
**Severity:** PASS (no followups blocking; two INFO notes for the record)
**Target:** commit `7d999db` / tag `star-lord/v-batch2-f4-telemetry-consume-1` — NOT pushed
**Developer:** star-lord (export/telemetry seam)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam MIGRATION), 6 (cross-seam round-trip); ADR-004, ADR-006; Disciplines #1, #2, #8 (schema-at-boundaries), #11, #12

## What I found

Verified against SOURCE (not the smoke summary), re-ran the suite myself per standing Gate-2 discipline. Every load-bearing claim in the submission holds. This is the CONSUME side of gamora's MIGRATION v1.84 producer (`8d45f95`), and it wires exactly the scope I fenced in the gamora Gate-2 finding — no more, no less. Diff touches six files only (`migrations.py`, `spatial_recorder.py`, telemetry/MIGRATION.md, export/MIGRATION.md, test file, AGENT_STATE.md); gamora's `spatial_engine.py` producer is untouched, and a grep of the diff for constant/mob/bar/kit assignment lines returns nothing but the reversibility-DDL comment — the out-of-scope list held byte-for-byte.

Schema v2.20 (`_V2_20` in `migrations.py`) adds two nullable columns via `ALTER TABLE ... ADD COLUMN` with NO DEFAULT clause: `escape_reached INTEGER` and `continuous_spawned_total INTEGER`. Registered correctly as `("2.20", _V2_20, ...)` at the tail of the MIGRATIONS list, sequencing after 2.19. The no-DEFAULT choice is the correct backfill semantic — a future apply on the populated `telemetry.db` will set pre-v2.20 rows to NULL, matching the documented contract and asserted by `test_pre_v220_rows_have_null_f4_fields` (`dflt_value is None`).

The persist path is the classic positional-INSERT hazard, so I checked column/placeholder/value-tuple alignment specifically: `_INSERT_SQL` now names 24 columns with 24 `?` placeholders, and the value tuple in `write_fight_result()` places `escape_reached` (bool→1/0) then `continuous_spawned_total` then `result.created_at` last — matching the column order (`...escape_reached, continuous_spawned_total, created_at`). Both new fields use `getattr(result, ..., default)` brownfield-safe reads, consistent with the established `geometry_type_source`/`player_death_element` pattern.

The `mobs_killed` invariant relaxation is SCOPED, not blanket. There is no in-code `assert mobs_killed <= total_mob_count` to remove — the invariant lives as a semantic contract in comments and tests. The relaxation is expressed via the discriminant `continuous_spawned_total > 0` / `scenario_id == 'escape_lane'`, documented in the `_V2_20` DDL comment and both MIGRATION.md entries. The six existing rooms retain the tight bound: `test_non_f4_room_tight_invariant_preserved` and `test_non_f4_partial_kill_tight_invariant` both assert `mobs_killed <= total_mob_count` for `open_arena` / `boss_with_adds`.

Round-trip acceptance (Principle 6) is real, not a rubber stamp. CASE 1 `test_f4_escape_reached_true_round_trip` constructs `mobs_killed=35 > total_mob_count=8, escape_reached=True, continuous_spawned_total=27`, writes through `write_fight_result()`, SELECTs back, and asserts `mobs_killed==35`, `mobs_killed > total_mob_count`, `escape_reached==1`, `continuous_spawned_total==27`. CASE 2 asserts the tight invariant for non-F4. 8 new tests, 70 pre-existing — I re-ran `tests/round_trip_spatial_telemetry.py` and confirmed **78 passed**, zero regressions.

MIGRATION.md lockstep verified: telemetry/MIGRATION.md v2.20 and export/MIGRATION.md v2.20-telemetry both present, both cite the v1.84 producer, both flag ADR-006 production-DB gating, and the export entry correctly declares NONE consumer action for drax (telemetry-internal; no JSON shape change).

## Rationale

- **Principle 1 / Disc #1:** the design/math note (schema delta + scoped invariant relaxation) is in the dispatch completion record and the `_V2_20` DDL comment, authored before/with the code. Adequate for a schema-widen of this size. PASS.
- **Principle 2 / Disc #2:** round-trip smoke present, GREEN, re-run by reviewer. PASS.
- **Principle 3 + 6 / ADR-004 / Disc #8, #12:** telemetry-boundary change carries MIGRATION.md in lockstep on both sides; round-trip is the acceptance gate and it asserts what it claims. PASS.
- **ADR-006:** production DB apply deliberately NOT executed; migration CODE shipped and correctly staged (nullable, no-DEFAULT backfill). Correctly gated, not incomplete. PASS.
- **Disc #11:** all claims verified against source; suite re-run; scope-guard grep clean.

## INFO notes (for the record; NOT blocking, no action required to tag)

- **INFO-1:** `mean_mobs_killed` read-back is confirmed correct-by-construction (metrology driver reads `run_spatial_fight()` raw dict in-process, not from the season JSON bundle), so no export-schema change was needed. Worth a one-line watch when/if F4 metrology output ever migrates into the exported season bundle — at that point drax becomes a consumer and a fresh export/MIGRATION entry would be owed. Noted, not owed now.
- **INFO-2:** the `escape_reached`/`continuous_spawned_total` reads use `getattr(..., default)` for brownfield safety even though the gamora dataclass now always defaults these fields. Defensive-consistent with the existing pattern; slightly redundant given the producer guarantee. Fine as-is; noted only so a future reader doesn't mistake the defensive read for an uncertainty about the producer contract.

## Action

- [x] jack-ryan: Gate-2 review complete — verified against source, re-ran round-trip suite (78 pass), scope-guard grep clean.
- [ ] star-lord: none blocking. Tag stands.
- [ ] Matt (ADR-006, separate from this tag): production DB apply of v2.20 to `telemetry.db` remains gated; the two ALTER TABLE statements will apply cleanly (nullable, no-DEFAULT → NULL backfill) when authorized.

## References

- `reincarnated-engine/src/reincarnated/telemetry/migrations.py` (`_V2_20` block + MIGRATIONS `("2.20", ...)` registration)
- `reincarnated-engine/src/reincarnated/telemetry/spatial_recorder.py` (`_INSERT_SQL` 24 cols :64-96; `write_fight_result()` persist path :190-201)
- `reincarnated-engine/tests/round_trip_spatial_telemetry.py` (`TestF4EscapeLaneTelemetrySchema220`, 8 tests; re-run 78 pass)
- `reincarnated-engine/src/reincarnated/telemetry/MIGRATION.md` v2.20
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` v2.20-telemetry
- Producer contract: `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` v1.84; `spatial_engine.py:2868-2869` (READ ONLY, gamora's producer — not in star-lord's scope, unchanged)
- Prior cross-seam determination: `agentic_orchestration/qa/findings/2026-07-07-gamora-gauntlet-four-family-instrument-gate2.md`
- Dispatch: `agentic_orchestration/dispatches/2026-07-07-star-lord-f4-telemetry-migration-consume.md`
