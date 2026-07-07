# Finding — 2026-07-07 — star-lord arc-close scaffold + gear-pool advance (Gate 2)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-FOLLOWUPS (WARN on one repo-hygiene item; no BLOCK)
**Target:** tag `star-lord/v-batch2-arc-close-scaffold-1`, commit `e57b796`
**Developer:** star-lord
**Principles applied:** 2 (smoke-gate), 3 (cross-seam MIGRATION), 6 (round-trip); ADR-004, ADR-006; Discipline #11 (empirical inspection)

## What I found

All three bundled items verified against the actual artifacts (Discipline #11 — every claim reproduced independently, not accepted from the completion record).

**Item 1 — DB v2.20 APPLY (production telemetry.db):** PASS. Production integrity confirmed. `PRAGMA integrity_check` = ok. Schema advanced to 2.20; `schema_meta` chain records v2.16→v2.20 (five entries, one apply timestamp — consistent with a single chained apply from the v2.15 baseline). `spatial_fight_results` carries both new columns `escape_reached INTEGER` and `continuous_spawned_total INTEGER` as columns 24/25 of a 26-column table — an exact match to the code-level v2.20 definition in `telemetry/migrations.py` (`_V2_20`) that passed Gate-2 at commit `7d999db` (tag `star-lord/v-batch2-f4-telemetry-consume-1`). **No schema drift between applied DB and Gate-2-passed code.** Row count: 7,841 spatial_fight_results rows. Backfill integrity: both new columns are 100% NULL (7,841/7,841 NULL, 0 non-NULL) — no invented values. Intermediate columns from the chained migration also backfilled correctly (`total_displacement` all 0.0 per NOT NULL DEFAULT; `player_death_element` all NULL). Six distinct rooms present, matching the "six existing rooms" report. `fight_events` (2,337,247 rows) and all 22 tables intact — no data loss.

Note on baseline: the git-tracked `telemetry.db` blob at the parent commit was the stale v2.15 baseline (2.1MB, 4,590 spatial rows, 0 fight_events). The migration was correctly applied to the **live on-disk production DB** (the working instance, which had legitimately accumulated more data than the stale git blob). This is expected — the live DB is the production instance; the git blob had gone stale. Not a discrepancy against the apply.

**Item 2 — II.3 scaffold bundle:** PASS. Round-trip smoke reproduced independently via `smoke_validate_batch1_scaffold_bundle()`: `pass=True`, 0 errors, 14 kits / 40 monsters / 200 gear. `bundle_version=one-realm-v1` (identical to LOCKED schema), `schema_status=BATCH1-SCAFFOLD`, `_batch1_scaffold=True`, no `telemetry` top-level key (Gate-1 fold (c) held). `faction_present=False` (III.7 invariant HELD). `tests/test_one_realm_bundle_assembler.py` + `tests/round_trip_spatial_telemetry.py`: 171 passed, matching the report. Assembler diff is additive-only (285 insertions, 0 deletions) — no existing-function changes.

**Item 3 — gear-pool writer advance:** PASS. 200 items against season_001005, `gear_slot` distribution includes 50 `off_hand`. Resist-cap correctly deferred: 0/200 items carry any non-empty `partition_modifiers.elemental_resistances` — no resist-cap VALUES invented (Q10 sweep / band-sheet deferral held).

**Hard-guards:** all HELD. No kit-side chassis constant changes (additive-only diff). No bar/band file moves (file set is exactly 5: AGENT_STATE.md, MIGRATION.md, one_realm_bundle_assembler.py additive, the new JSON artifact, telemetry.db). MIGRATION.md §v2.21-batch1-scaffold in lockstep (ADR-004), documenting drax consumer obligations (NONE), the additive schema contract, gear-pool advancement, resist-cap deferral, III.7, and a correctly-attributed pre-existing bow-affix warning in rocket's seam. Round-trip discipline satisfied (Principle 6): smoke present + additive-nullable consumer tolerance.

## Rationale

Item 1 satisfies ADR-006 (Matt per-statement DB-write authorization 2026-07-07) with the applied schema matching the already-Gate-2-passed v2.20 code (no drift, Principle 6). Items 2+3 are additive outputs with round-trip smoke reproduced (Principle 2, Principle 6) and cross-seam MIGRATION.md present (Principle 3, ADR-004). Production DB integrity verified empirically (Discipline #11). The single WARN below is repo-hygiene, not a principle violation or a named hard-guard, so it does not gate the tag.

**WARN (repo-hygiene followup, non-blocking):** the migration committed a 450MB binary `telemetry.db` blob into git history (2.1MB → 450MB, permanent in history; SQLite files delta/compress poorly). This is not a data-integrity or schema issue and is outside the named hard-guards, but it materially bloats the engine repo permanently and will slow every future clone/fetch. Escalated to Matt as a policy decision (below) — it is not star-lord's to unilaterally resolve, and it does not warrant blocking a correct, Matt-authorized production migration.

## Action

- [x] Developer (star-lord): no remediation required for the migration or bundle work — all three items PASS.
- [ ] Matt (ESCALATE — repo-hygiene policy): decide whether the production `telemetry.db` should be git-tracked at all. Options: (a) `.gitignore` telemetry.db going forward and keep only a small fixture/seed DB in-tree (recommended); (b) accept the 450MB blob as a one-time cost; (c) history rewrite to excise the blob (high-touch, coordinate across all four repos' clones). This is a cross-seam/architectural call per ADR-002 — parked as a followup, does not gate this tag.

## References

- `~/Games/reincarnated-engine` commit `e57b796`, tag `star-lord/v-batch2-arc-close-scaffold-1`
- v2.20 code baseline: commit `7d999db`, tag `star-lord/v-batch2-f4-telemetry-consume-1` (note: invocation cited `984981b`; the actual v2.20 migration-code commit is `7d999db` — flagged for the record)
- `src/reincarnated/telemetry/telemetry.db` (applied production DB; 7,841 spatial rows, integrity_check ok)
- `src/reincarnated/telemetry/migrations.py` (`_V2_20`, schema_meta chain)
- `src/reincarnated/output/one_realm_batch1_scaffold_bundle.json` (14/40/200; smoke PASS)
- `src/reincarnated/export/one_realm_bundle_assembler.py` (additive-only; 3 new functions)
- `src/reincarnated/export/MIGRATION.md` §v2.21-batch1-scaffold
- `agentic_orchestration/qa/pending/2026-07-07-star-lord-arc-close-scaffold-gate2.md` (submission; archived)
