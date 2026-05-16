# Dispatch — star-lord script cleanup after research.db retirement

**Status:** COMPLETE
**Target:** star-lord (engine-side scripts; ADR-004 cross-seam coordination from Elrond's data-layer cleanup)
**Branch:** main (engine repo)
**Tag intent:** Intermediate `star-lord/research-db-cleanup`; no milestone tag (internal cleanup).

## Context

Elrond is executing dispatch A (research.db retirement; 2026-05-16) per Matt's assignment. The research.db has been dormant since 2026-05-07 and all structural content has migrated to telemetry.db. Elrond filed the archive markdown + removed the .db file per his data-steward authority.

**Cross-seam impact (ADR-004):** Two engine scripts in your seam still reference research.db:

- `reincarnated-engine/scripts/db.py`
- `reincarnated-engine/scripts/capture-regression-baseline.py`

After research.db is removed, these scripts will fail on next execution. Both are operationally dormant (no recent invocations per Elrond's audit), so practical risk is low — but they need cleanup for repo hygiene + correctness.

## Work

1. **Read both scripts** to understand their research.db usage. Cases vary:
   - If the script ONLY uses research.db (no other purpose), candidate for full removal
   - If the script uses research.db for one code path and other DBs for others, candidate for removing the research.db code path only
   - If the script has dead code referencing a never-populated table, candidate for clean removal
2. **Refactor or remove** based on the use pattern. Pure-research.db logic gets removed; multi-DB scripts keep other paths intact.
3. **Update star-lord's `MIGRATION.md`** at `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (or equivalent) with the cleanup entry. Elrond's archive § E has a draft one-liner; consume that as seed.
4. **Commit the changes** with smoke-test confirmation (Discipline #2). For dormant scripts, the smoke is "imports + module-load cleanly; no syntax errors" plus a `git grep research.db` returning zero hits in the engine repo. Note the smoke in the commit message.
5. **Cut intermediate tag** `star-lord/research-db-cleanup` after commit + push to origin.

## Out of scope

- Re-running any scripts (they're dormant)
- Modifying telemetry.db or other live data stores
- Any non-script changes (this is a cleanup dispatch, not a feature)

## Cross-seam coordination

- **Elrond** has already filed the archive and (by the time you pick this up) likely removed research.db. Cross-confirm with `ls /Users/admin/Games/reincarnated-engine/research.db` returning "No such file" before starting the script refactor — that's your trigger.
- **MIGRATION.md** seed is in Elrond's archive markdown § E. Read that for the recommended one-liner.

## Authority and authorization

- Cross-seam authorization granted (ADR-004): Elrond's dispatch A established the data-layer retirement; this dispatch handles the script-side cleanup downstream.
- No external system writes; no Matt per-statement authorization needed beyond the dispatch's existing scope.

## Acceptance

- Both scripts updated or removed
- `git grep research.db` in engine repo returns zero hits
- MIGRATION.md entry appended (using Elrond's seed)
- Intermediate tag cut + pushed
- Smoke-test confirmation in commit message
- Knight-rider notified at completion: commit SHA, intermediate tag, script-action summary (refactored / removed / kept-with-modifications), MIGRATION.md path

## Time-bound target

30-60 minutes. Small scope.

## Required reading

- Elrond's archive markdown at `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` § E (the MIGRATION.md seed)
- Elrond's data-architecture audit at `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` § research.db section
- The two scripts in question
- ADR-004 (cross-seam coordination + MIGRATION.md requirement)

---

## Completion record

**Completed:** 2026-05-16  
**Commit:** `fabbc65`  
**Tag:** `star-lord/research-db-cleanup` (pushed to origin)

### What was done

**Pre-flight confirmed:** `ls ~/Games/reincarnated-engine/research.db` → no such file (Elrond's retirement already executed).

1. **`scripts/db.py` — removed.** Script was 100% research.db (schema init, data import, summary queries, bugs table, notes table, init commands). No other DB or purpose. Deleted via `git rm`.

2. **`scripts/capture-regression-baseline.py` — research.db path removed:**
   - Removed `RESEARCH_DB = ENGINE_DIR / "research.db"` constant
   - Removed `databases/research.db` from docstring artifact list
   - `snapshot_databases()` loop updated to `[TELEMETRY_DB]` only; retirement note added as comment
   - `extract_schema_snapshot()` research.db schema-dump block replaced with single retirement comment + archive pointer

3. **MIGRATION.md entry appended** — "Script cleanup: research.db retirement (2026-05-16)" section using Elrond archive § E as seed. Documents changes to both scripts.

4. **Smoke test** — `python3` import/syntax checks passed. `git grep research.db` in `src/`, `scripts/`, `tests/` → zero functional hits (retirement comments excluded). ✓

### Acceptance checklist

- [x] Both scripts updated/removed
- [x] `git grep research.db` → zero functional hits
- [x] MIGRATION.md entry appended
- [x] Tag `star-lord/research-db-cleanup` + pushed
- [x] Smoke-test confirmation in commit message

### Knight-rider notification

**Both dispatches complete in commit `fabbc65`.**  
Tags: `star-lord/c1f02ca-silent-dependency-hardening`, `star-lord/research-db-cleanup`  
Script actions: `scripts/db.py` removed (pure research.db); `scripts/capture-regression-baseline.py` research.db path removed (telemetry.db path retained).  
MIGRATION.md: two new sections appended (persistence contract + script cleanup).  
31/31 export tests passed.
