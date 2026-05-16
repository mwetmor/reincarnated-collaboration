# Dispatch — star-lord telemetry Tier 1 extension (2026-05-14)

**Target:** star-lord (reincarnated-engine) — cross-seam authorization to also touch gamora-owned files (see § Cross-seam authorization below)
**Branch:** main
**Tag intent:**
- Intermediate: `star-lord/telemetry-tier1-extension` — star-lord-autonomous after acceptance verified
- Milestone: `v1.3-telemetry-tier1` — **Confirm with knight-rider before cutting** (ADR-003 protocol; knight-rider escalates to Matt for sign-off)

## Context

Drax v0.7-encounter-analytics needs 4 feature dimensions to render centroid + stdev-ellipse clustering across (class, encounter slot) pairs. Per the 2026-05-14 fight-log granularity research pass (findings captured in `agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md`), two of the four dimensions are already in the in-memory fight log but never persisted, and one tracked field on `CombatantState` is never read into `FightResult`. This dispatch wires those up.

Matt approved Tier 1 (this dispatch) and deferred Tier 2 (`action_trace → fight_skill_uses` table) "as time allows."

## Work

Three new fields persisted per fight in the `class_fight_loadouts` table:

| New column | Source | Purpose |
|---|---|---|
| `duration_seconds` | Already in fight_log dict; just dropped at persist step | Time-to-kill dimension |
| `a_heals_received` | Read `state_a.heals_received` in `_build_result()`; expose on `FightResult`; include in fight_log dict | Sustain expenditure dimension |
| `a_potions_used` | Read `(POTION_COUNT - state_a.health_potions)` in `_build_result()`; expose on `FightResult`; include in fight_log dict | Sustain expenditure dimension |

Exact column names are star-lord's call; pick names consistent with existing schema conventions in `class_fight_loadouts`. Document chosen names in the completion record.

### Files touched (cross-seam authorization granted)

- `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (gamora seam) — `_build_result()` reads heals_received and computes potions_used
- `reincarnated-engine/src/reincarnated/simulation/fight_result.py` or wherever `FightResult` is defined (gamora seam) — add three fields
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (gamora seam) — include new fields in fight_log dict construction
- `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (star-lord seam) — read new fields from fight_log; write to schema
- Schema migration (star-lord seam) — `ALTER TABLE class_fight_loadouts ADD COLUMN ...` × 3; bump `schema_meta` version

## Cross-seam authorization

This dispatch touches gamora-owned simulation files. Knight-rider authorizes the cross-seam work per ADR-004 because:

1. The change is small (~9 lines total across all files) and well-scoped
2. The CombatantState tracking already exists — this just exposes it through the FightResult contract
3. No simulation behavior changes — only data capture
4. **MIGRATION.md is required** (see below)

If star-lord encounters anything that suggests the change is larger or more invasive than ~9 lines, **PAUSE and escalate to knight-rider** before continuing.

## MIGRATION.md requirement (ADR-004)

Star-lord authors `MIGRATION.md` in the engine repo describing:
- Schema change (3 new columns, version bump in schema_meta)
- That existing 1.8M rows will have NULL for the new columns (no backfill — values aren't preserved in aggregate)
- That downstream consumers (drax v0.7) will need a fresh Yomi regen with the new telemetry capture to populate the columns
- No behavioral change to balance loop or fight outcomes — only additional data capture

## Backfill — explicitly not done

The existing 1.8M `class_fight_loadouts` rows will have NULL for the three new columns. `duration_seconds` and `heals_received` are runtime computed and not preserved on aggregate. Backfill is impossible without re-running the fights. **This is intentional.** Drax v0.7 will require a fresh Yomi regen with the new telemetry in place — that regen happens at v0.7 time, not Tier 1 time.

## Acceptance

1. Schema migration applied; `schema_meta` shows new version
2. `class_fight_loadouts` table has 3 new columns
3. A test fight run (smoke or single-class) populates the 3 new columns with non-NULL values
4. Existing 1.8M rows remain unaffected (NULL in new columns, all other data preserved)
5. Full test suite (gamora-side simulation tests) still passes — no behavioral change
6. `MIGRATION.md` authored at `reincarnated-engine/MIGRATION.md` or equivalent path

## Out of scope

- **Tier 2** (action_trace → fight_skill_uses table) — deferred per Matt
- PackProxy disaggregation — deferred indefinitely
- Backfilling existing rows — impossible; not attempted
- v0.7 drax dispatch — separate work, knight-rider authors after Tier 1 lands

## Tag protocol

- Intermediate tag: `star-lord/telemetry-tier1-extension` — star-lord-autonomous
- Milestone tag: `v1.3-telemetry-tier1` — **Confirm with knight-rider before cutting** (ADR-003)

## Required reading

- Fight-log research findings: `agentic_orchestration/dispatches/2026-05-14-v0-7-scoping-notes.md` § "Star-lord research findings"
- B10.2 decisions-log entry (PackProxy + fight log emission notes)
- ADR-004 (cross-seam coordination + MIGRATION.md requirement)

## Completion record

**Completed:** 2026-05-16 by star-lord (claude-sonnet-4-6)
**Execution note:** This dispatch was split across two subagent invocations. The first subagent (previous session) applied the 5 code edits and paused at the ADR-005/ADR-006 boundary before the DB migration. This session continued from that paused state after Matt's authorization was relayed.

### Commit SHA

Primary commit: `baa3bed` — "v1.3-telemetry-tier1: persist duration_seconds + a_heals_received + a_potions_used"
SHA update commit: `0943cbf` — "chore: update AGENT_STATE with telemetry-tier1 commit SHA"
Branch: `main` (pushed to `origin`)

### Intermediate tag

`star-lord/telemetry-tier1-extension` — pushed to origin

### Milestone tag

NOT cut. Per ADR-003, milestone tag `v1.3-telemetry-tier1` requires knight-rider confirmation. Requesting knight-rider relay to Matt for sign-off.

### Exact column names chosen

| Column | Type | Notes |
|---|---|---|
| `duration_seconds` | REAL | Matches existing column naming convention in the table; consistent with `generation_runs.duration_seconds` |
| `a_heals_received` | REAL | Prefixed with `a_` per FightResult naming convention (a_id, a_final_hp, a_damage_dealt, etc.) |
| `a_potions_used` | INTEGER | Same prefix convention |

### MIGRATION.md path

`reincarnated-engine/src/reincarnated/export/MIGRATION.md` — Schema 1.9 → 2.0 section appended

### Test results

- **Full suite** (pre-migration): 1,291 passed, 0 failures
- **Targeted smoke** (`tests/test_telemetry_tier1.py`): 15/15 passed
  - V2.0 migration applies cleanly from V1.9
  - Three columns present with correct REAL/REAL/INTEGER types
  - FightResult dataclass has both new fields with zero defaults
  - balance_loop fight_log entries carry all three new fields with correct types
  - record_class_fight_loadouts persists non-NULL when provided; NULL when absent (backward compat)

### DB state after migration

- `data/telemetry.db` schema_meta shows version `2.0` (applied 2026-05-16 01:05:30 UTC)
- `class_fight_loadouts` table has 14 columns total (columns 12-14 are the three new)
- 1,925,180 existing rows all have NULL in new columns (no backfill, as spec'd)

### Acceptance checklist

- [x] Schema migration applied; schema_meta shows 2.0
- [x] class_fight_loadouts has 3 new columns with correct types
- [x] Smoke test (in-memory) populates new columns with non-NULL values
- [x] Existing 1.8M rows unaffected (NULL in new columns, all prior data preserved)
- [x] Full test suite passes (1,291 tests, no behavioral change)
- [x] MIGRATION.md authored at `reincarnated-engine/src/reincarnated/export/MIGRATION.md`

### Deviations from spec

None. The 5 code edits were as described. Column names match the names specified in the authorization relay. The test file `tests/test_telemetry_tier1.py` was added (not mentioned in spec, but a natural Discipline #2 artifact). The SQLite spot-check showing 5 non-NULL rows from a live regen could not be performed without a full Yomi regen — the in-memory smoke test in the pytest suite serves as the functional equivalent.

### Milestone tag cut

Milestone tag `v1.3-telemetry-tier1` cut 2026-05-16 per Matt sign-off via knight-rider. Points at commit `0943cbf0ff69ee31b992cdb0cb43adaee4050380`. **Pushed to origin** (`refs/tags/v1.3-telemetry-tier1` on `github.com/mwetmor/reincarnated-engine`). Tag cut performed by knight-rider with Matt's explicit per-statement authorization (ADR-006-adjacent) given the subagent-Bash limitation that blocked star-lord from cutting it autonomously.
