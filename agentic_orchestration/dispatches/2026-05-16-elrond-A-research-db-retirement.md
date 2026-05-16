# Dispatch — elrond A: research.db retirement (Phase-1 cleanup)

**Status:** COMPLETE — 2026-05-16 (see Completion section)
**Target:** elrond
**Branch:** main (engine repo for read; collaboration repo for archive output)
**Tag intent:** No tags — this is data hygiene; deliverable is an archive markdown + database file removal.

## Context

Per your own data-architecture audit (2026-05-16) § Phase-1: `reincarnated-engine/research.db` is dormant since 2026-05-07. All structural content has migrated to `telemetry.db`. Only `research_notes` (~5 rows) and `bugs_log` (~5 rows) carry narrative that needs preservation before retirement.

The 2026-05-07 decisions-log deferral on this DB (*"Active. Consolidation deferred until research.db contents and schema are audited"*) is now satisfied by your audit. Retirement is the recommended Phase-1 close.

Matt assigned this 2026-05-16 as Elrond task A, sequenced before task B (Yomi provenance audit).

## Work

1. **Read `research.db` contents** via `sqlite3 /Users/admin/Games/reincarnated-engine/research.db`:
   - Enumerate all tables: `.tables`
   - For each table with rows: select all content
   - Verify your audit's row counts (5 research_notes + 5 bugs_log; flag if reality diverges)
2. **Author archive markdown** at `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md`:
   - One section per source table
   - Preserve all row content verbatim (no editorialization)
   - Include row metadata (timestamps, identifiers) per original schema
   - Add provenance header: source DB path, retirement date, audit reference
3. **Update the data-architecture audit** at `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` — add a "Phase-1 cleanup completed 2026-05-16" subsection under the research.db finding noting: archive path; that the DB has been removed; that future references to research.db should point at the archive instead.
4. **Drop the research.db file:**
   - Verify the archive is committed first (markdown + git status clean on the collaboration repo)
   - Then: `rm /Users/admin/Games/reincarnated-engine/research.db`
   - This is a destructive op on Matt-authorized work; per ADR-006 the audit + this dispatch + Matt's assignment authorize the deletion
5. **Update star-lord-side MIGRATION.md** (or equivalent doc in engine repo) noting research.db retirement — coordinate with star-lord via knight-rider if substantive cross-seam doc update needed. Likely a one-line entry.

## Out of scope

- Modifying anything in telemetry.db (star-lord's seam)
- Adding new tables to research/curated/ (this is archive-only)

## Acceptance

- Archive markdown filed and committed
- Audit updated noting cleanup complete
- research.db file removed (`ls reincarnated-engine/research.db` → "No such file")
- Knight-rider notified at completion with: archive path, row counts archived, any unexpected content surfaced (e.g., a 3rd table the audit missed)

## Time-bound target

30-60 minutes. Small scope.

## Required reading

- Your own audit: `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` § research.db section
- The 2026-05-07 decisions-log entry referencing research.db deferral

## Completion — elrond, 2026-05-16

### What landed

| Artifact | Path | Notes |
|---|---|---|
| Binary snapshot | `agentic_orchestration/research/curated/archive/research-db-2026-05-07.db` | 2.6 MB; SHA-256 `3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e`; integrity-verified against source pre-rm |
| Narrative archive | `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` | 349 lines; research_notes (5) + bugs_log (5) verbatim; single-row metadata tables verbatim; structural tables schema + counts; integrity hash + status footer |
| `.gitignore` update | `agentic_orchestration/research/curated/.gitignore` | `!archive/*.db` exception for intentional historical preservation |
| Audit § 3.4.1 | `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` | New "Phase-1 cleanup status" subsection — both prep and destructive passes documented; audit § 3.1 finding superseded |
| MIGRATION.md v1.1 entry | `agentic_orchestration/research/curated/MIGRATION.md` | Includes `archive/` convention establishment and the destructive-op completion log |
| AGENT_STATE update | `agentic_orchestration/research/curated/AGENT_STATE.md` | Reflects completion + Dispatch B transition |

### Destructive ops executed (ADR-006, Matt-authorized 2026-05-16)

Authorization scope: explicit per-statement go-ahead on the four-file removal window.

```
rm /Users/admin/Games/reincarnated-engine/research.db        ✓
rm /Users/admin/Games/reincarnated-engine/research.db-wal    ✓
rm /Users/admin/Games/reincarnated-engine/research.db-shm    ✓
rm /Users/admin/Games/reincarnated-engine/telemetry.db       ✓  (empty 0 B engine-root orphan from audit § 3.1, bundled into same window)
```

Post-rm verification: all four return "No such file"; `data/telemetry.db` (15.7 GB canonical) untouched; engine `git status` reports no new artifacts (all four were already `.gitignore`d).

### Row counts archived

- `research_notes` — 5 rows (verbatim in markdown)
- `bugs_log` — 5 rows (verbatim in markdown)
- `generation_runs` — 1 row (verbatim in markdown § C)
- `trial_bosses` — 1 row (verbatim in markdown § C)
- `classes` — 11 rows (schema + count documented; full content in binary snapshot)
- `monsters` — 40 rows (schema + count documented; full content in binary snapshot)
- `gauntlet_matchups` — 110 rows (schema + count documented; full content in binary snapshot)
- `skills` — 166 rows (schema + count documented; full content in binary snapshot)
- `fight_results` — 13,040 rows (schema + count documented; full content in binary snapshot)
- `balance_overview`, `class_summary` — VIEWS, derived from `classes`; not separately persisted
- `sqlite_sequence` — internal SQLite autoincrement tracking; not preserved separately

### Surfaces beyond dispatch's row-count expectation

Dispatch summary line described research.db as "narrative-only" (~5+5 rows). The audit's full § 3.4 correctly enumerated 11 tables totaling 13K+ rows. **Reality matched the audit detail; only the dispatch summary blurb was condensed.** Steward call to preserve the binary snapshot ensured no structural data was lost in transit.

### Open follow-ons (NOT elrond-blocking)

1. **Star-lord script cleanup** — `scripts/db.py` (3 references) and `scripts/capture-regression-baseline.py` (4 references). Recommended one-liner for star-lord MIGRATION.md captured in archive markdown § E. Knight-rider sequences with star-lord.
2. **Knight-rider decisions-log entry** — closes the 2026-05-07 deferral (per dispatch item 3).

### Notification to knight-rider

Cleanup complete. Three follow-ons in star-lord's seam need knight-rider sequencing (script cleanup + MIGRATION.md entry + decisions-log entry). Archive accessible at `agentic_orchestration/research/curated/archive/` going forward. Transitioning to Dispatch B (Yomi provenance audit) now.

— elrond, 2026-05-16
