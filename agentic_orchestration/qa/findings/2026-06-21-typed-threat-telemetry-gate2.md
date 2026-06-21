# Finding — 2026-06-21 — typed-threat telemetry (star-lord v1.81 consumer)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-CONCERNS (verdict: **PASS** — wave build chain CLOSED)
**Mode:** Gate-2 DEV-MODE (closing gate of the typed-resistance recal wave build chain)
**Target:** engine commit `d04edcc`, tag `star-lord/v-typed-threat-telemetry-1` (push held per ADR-006)
**Developer:** star-lord
**Principles applied:** Review #2 (smoke/scope-gate), #3 (cross-seam round-trip), #4 (decisions/MIGRATION as truth), #5 (severity); Disciplines #11 (empirical inspection over assumption — every claim re-derived first-hand from source + run), #12 (semantic-shift declared)

## What I found

I re-derived every load-bearing claim first-hand: read the full diff, read the `_INSERT_SQL` column list and value tuple in their entirety, grepped the producer field across the simulation seam, ran the test suite myself (59/59 PASS, 0.76s), and traced the export factory's reference graph to confirm it is unwired from emission. The build faithfully completes gamora's v1.81 producer contract with exactly ONE additive field, `player_death_element`. All five gate teeth knight-rider named HOLD. Two non-blocking CONCERNS carry: (1) a stale doc reference to a non-existent `ExportSpatialFightSummary`, and (2) the round-trip driver populates the field via the `SpatialFightResult` dataclass rather than a live `SpatialFightEngine.run()` typed death — correct for star-lord's persist+export lane, but worth a one-line note. Neither blocks; the wave build chain is CLOSED.

### The five gate teeth — all verified

1. **Additive-only guard (the load-bearing one) — CONFIRMED WITH TEETH.** The `_INSERT_SQL` column list (`spatial_recorder.py:58-79`) preserves all 20 prior columns in exact original positional order; `player_death_element` is inserted at position 21, ahead of `created_at` (position 22, unchanged as the tail). The value tuple (`:156-185`) mirrors this exactly — placeholder grid 21→22 correct. SQLite binds by the named column list, not absolute index, so slotting before `created_at` is positionally safe. NO field renamed, removed, or reordered. The dedicated additive-guard test `test_existing_fields_byte_identical_after_v219` (`round_trip:1100`) writes a pre-wave-shaped row through the REAL writer, SELECTs it back, and asserts `fight_id`/`class_id`/`winner`/`geometry_type_dominant`/`geometry_type_source`/`wr_1d_fight` all read identically while the new column reads NULL. The `_V2_19` ALTER is `ADD COLUMN ... TEXT` (nullable, no DEFAULT) — pre-existing rows get NULL. A pre-v2.19 row round-trips byte-identically. Banked offensive-instrument artifacts stay readable.

2. **G-C emission-held — CONFIRMED WITH TEETH.** `build_typed_death_telemetry` / `ExportTypedDeathTelemetry` are referenced ONLY in their own definition (`schemas.py`), the test file, MIGRATION docs, and AGENT_STATE. They are NOT members of `ExportSeason` and NOT wired into `season_exporter.py` or `output/`. No emission path exists. The docstring G-C note ("surfaces validation data only; does NOT unlock emission") matches actual behavior — the factory is a standalone validation/observability artifact the gamora calibration harness consumes. Nothing in this build ships content.

3. **No out-of-scope reach — CONFIRMED.** Full-diff grep for `DEFERRED_PROXY` / `proxy_bin` / `25%` / `emit` = ZERO hits. The Matt-reserved `_DEFERRED_PROXY_BINS` / 25% proxy emission was not touched. The schema change is purely additive (one nullable column); no non-additive change anywhere.

4. **Round-trip exercises the real chain — CONFIRMED.** `test_export_packet_db_round_trip_full_chain` (`round_trip:1205`) runs: real `SpatialFightResult` → real `SqliteSpatialTelemetryWriter.write_fight_result()` → real `_INSERT_SQL` → DB → `SELECT` read-back → `_RowStub(row)` → `build_typed_death_telemetry` → `ExportTypedDeathTelemetry`. The persist leg is NOT stubbed; the `_RowStub` is on the export-consumer side and is constructed FROM the DB-read row (`row["player_death_element"]`), not a hand-set literal — a legitimate simulation of the season exporter's read, not a bypass. The producer field is genuine: `spatial_telemetry.py:319` defines it, `spatial_engine.py:2009` populates `_death_element` from a real typed death event, `:2313` passes it to the result. star-lord did not invent a producer field.

5. **MIGRATION completeness — CONFIRMED, with one doc nit (Concern 1).** Producer-side `simulation/MIGRATION.md §v1.81` consumer-delivery record (`:56-95`) and consumer-side `export/MIGRATION.md §v1.81` (new) are both present and consistent with the actual diff (column, persist leg, export model, field semantics, round-trip table). The export MIGRATION correctly notes drax/demo/loadout have NO consumer impact (new type, existing season JSON shape unchanged).

### Independent verification run

- `round_trip_spatial_telemetry.py`: **59 passed in 0.76s** — ran first-hand, confirms the self-reported 59/59.
- 4752-suite regression baseline (20 pre-existing failures unchanged, 0 introduced): NOT re-run by me; star-lord's claim is consistent with rocket's and gamora's independently-confirmed pre-existing-failure baseline on the same touched tree (element-count drift + cohesion-judge config). Accepted on the prior two seams' first-hand confirmation; flagged as not-independently-re-run here for the record.

## Rationale

- **Additive-only (Review #3, the cross-seam round-trip principle; dispatch G guard + MASTER G-A artifact-preservation):** the wave's banked offensive bands are PROVISIONAL and re-rate-pending; their telemetry must stay byte-identical-readable. Verified at the column-ordering level, not taken on the self-report.
- **G-C emission-held (MASTER §77; dispatch NON-NEGOTIABLE GUARD):** confirmed via reference-graph trace that the export model is unwired from any emission path.
- **Principle 6 round-trip (REVIEW_PROCESS):** the dispatch required a production-path persist+export round-trip; the full-chain test satisfies star-lord's lane of it.
- **Discipline #12 semantic-shift:** correctly declared NONE on existing fields — purely additive `player_death_element`; the only semantics are on the new column's value space (None/`"armor"`/`"<elem>"`).

## Concerns (non-blocking — INFO/WARN)

- **[WARN] Stale doc reference to non-existent `ExportSpatialFightSummary`.** Two docstrings — `migrations.py:1148` ("Export: ExportSpatialFightSummary in export/schemas.py updated to surface player_death_element") and `spatial_recorder.py:17` ("export/schemas.py ExportSpatialFightSummary") — name a class that does NOT exist anywhere in `src/`. The actual export surface is the newly-created `ExportTypedDeathTelemetry`. This is a documentation inaccuracy, not a wiring gap: the field IS exported (verified), just via a different model than the docstring names. Additive guard is intact. **Not a BLOCK** — no code path depends on the stale name. Fix advisable: star-lord corrects both docstrings to reference `ExportTypedDeathTelemetry` (doc-only; within star-lord's seam; no re-tag required).
- **[INFO] Round-trip driver uses the dataclass, not a live engine death.** `_make_result(player_death_element="fire")` constructs the `SpatialFightResult` directly rather than running `SpatialFightEngine.run()` to a genuine typed death. This is CORRECT scoping — the live-engine population path (`spatial_engine.py:2009`) is gamora's seam and was confirmed in her Gate-2 (`2026-06-21-typed-resistance-calibration-gate2.md`); star-lord's smoke owns the persist+export half. Noted only so the seam boundary on the round-trip is explicit in the record.

## Action

- [ ] Developer (star-lord): correct the two stale `ExportSpatialFightSummary` docstring references (`migrations.py:1148`, `spatial_recorder.py:17`) to `ExportTypedDeathTelemetry` — doc-only, no re-tag (WARN, advisable not blocking).
- [ ] Matt (wave-close gate, NOT a BLOCK): `_V2_19` production-DB `ALTER TABLE` requires ADR-006 authorization before any production apply — same standing gate as v2.17/v2.18, both also PENDING. Specced and ready; no DB write occurs without explicit auth.
- [ ] knight-rider: wave build chain is CLOSED (all three seams Gate-2-clean). Proceed to the Matt-gated joint two-axis re-rate / close.

## Build-chain close statement

**The typed-resistance recal-wave build chain is CLOSED — all three seams Gate-2-clean:**
- rocket `rocket/v-typed-resistance-gear-and-monster-skills-1` — **PASS** (`2026-06-21-typed-resistance-gear-and-monster-skills-gate2.md`)
- gamora `gamora/v-typed-resistance-calibration-1` — **PASS-WITH-CONCERNS** (`2026-06-21-typed-resistance-calibration-gate2.md`)
- star-lord `star-lord/v-typed-threat-telemetry-1` — **PASS** (this finding)

**Items that must reach Matt before the two-axis joint close (none are BLOCKs):**
1. `_V2_19` (this build) + `_V2_17` + `_V2_18` production-DB-apply ADR-006 authorizations — three PENDING migration applies, all additive/nullable, batched at the same standing gate.
2. The joint two-axis re-rate + band finalization / content emission is Matt-gated (MASTER §138/§181) — G-C remains held until that close; nothing in this build pre-empts it.

No item from star-lord's seam BLOCKs the joint close. The two WARN/INFO concerns are within star-lord's seam to clean (doc-only) and do not gate the close.

## References

- `~/Games/reincarnated-engine/src/reincarnated/telemetry/migrations.py` (`_V2_19`, MIGRATIONS registry; stale doc ref :1148)
- `~/Games/reincarnated-engine/src/reincarnated/telemetry/spatial_recorder.py` (`_INSERT_SQL` :56-87, value tuple :152-186; stale doc ref :17)
- `~/Games/reincarnated-engine/src/reincarnated/export/schemas.py` (`ExportTypedDeathTelemetry` :1165, `build_typed_death_telemetry` :1218)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (§v1.81 producer + consumer-delivery record)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` (§v1.81 consumer entry)
- `~/Games/reincarnated-engine/tests/round_trip_spatial_telemetry.py` (19 new tests; full-chain :1205, additive-guard :1100)
- Producer field source: `~/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py:319`; populated `spatial_engine.py:2009/2313`
- Dispatch: `agentic_orchestration/dispatches/2026-06-21-star-lord-typed-threat-telemetry.md`
- Parent MASTER: `agentic_orchestration/dispatches/2026-06-21-recal-wave-typed-resistance-MASTER.md`
- Prior seam findings: `agentic_orchestration/qa/findings/2026-06-21-typed-resistance-gear-and-monster-skills-gate2.md`, `2026-06-21-typed-resistance-calibration-gate2.md`
