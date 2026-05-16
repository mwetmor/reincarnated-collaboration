# Decisions-log entry draft — research.db retired

**Author:** knight-rider
**Date drafted:** 2026-05-16
**Source:** Elrond dispatch A completion + audit § 3.4.1 + Matt's 2026-05-16 cleanup assignment
**Process:** Knight-rider drafts → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the four entries committed 2026-05-15.

**Target location:** before the "Recently considered, not yet decided" section, after the existing 2026-05-15 entries (Court, Enemy visual legibility, Style register, Naming triad).

---

## Entry — research.db retired; 2026-05-07 consolidation deferral closed

### 2026-05-16: research.db retired — consolidation deferral closed

**Decision:** `reincarnated-engine/research.db` is retired. The DB file + its SQLite sidecars (`.shm` / `.wal`) have been removed from disk. The structural content has been preserved as both a binary snapshot and a narrative markdown archive in Elrond's data-steward seam. The 2026-05-07 deferral ("Two telemetry databases — deferred consolidation until research.db contents and schema are audited") is satisfied and **superseded by this entry**.

The empty (0 B) orphan `reincarnated-engine/telemetry.db` at engine root — flagged in Elrond's data-architecture audit § 3.1 as a leftover artifact distinct from the canonical `data/telemetry.db` (15.7 GB) — was bundled into the same cleanup window and removed.

**What was preserved:**

| Artifact | Path | Content |
|---|---|---|
| Binary snapshot | `agentic_orchestration/research/curated/archive/research-db-2026-05-07.db` | Full DB (2.6 MB, SHA-256 `3846b98b272386dc946104676da7cff6ac1f86f529be195799af7b289f96351e`) |
| Narrative archive | `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` | 349 lines; research_notes (5) + bugs_log (5) + single-row metadata tables verbatim; structural-table schemas + counts; integrity-verification footer |

**Row counts archived** (verbatim where small; schema + count where large; full content in binary snapshot):

- `research_notes` — 5 rows
- `bugs_log` — 5 rows
- `generation_runs` — 1 row
- `trial_bosses` — 1 row
- `classes` — 11 rows
- `monsters` — 40 rows
- `gauntlet_matchups` — 110 rows
- `skills` — 166 rows
- `fight_results` — 13,040 rows
- `balance_overview` / `class_summary` — VIEWS derived from classes; not separately persisted
- `sqlite_sequence` — internal SQLite metadata; not preserved separately

**Steward judgment worth noting:** the dispatch's summary line described research.db as "narrative-only (~5+5 rows)." The audit's full § 3.4 enumeration showed 11 tables totaling 13K+ rows. Elrond's steward authority overrode the dispatch's condensed framing and preserved the binary snapshot, preventing structural-data loss. This is Tier C+ data-steward authority operating correctly — knight-rider's authoring summary was loose; the seam owner's domain knowledge corrected.

**Reasoning:** Per the 2026-05-07 entry's stated condition ("deferred until research.db contents and schema are audited"), Elrond's data-architecture audit (2026-05-16) satisfied the audit requirement. The audit found research.db dormant since 2026-05-07 with all structural content having migrated to `data/telemetry.db`. Retention provided no operational value and complicated the data architecture (audit § 3.4 "dormant DB whose deferral has gone stale"). Retirement is the recommended Phase-1 close per the audit.

The data IS preserved — just in a different shape (archive .db + markdown) at a different location (Elrond's curated/archive subdirectory). The 2026-05-07 deferral asked for an audit; the audit has happened and recommends retirement. Decision honors the original deferral's intent.

**Alternatives considered:**

- **Keep research.db dormant indefinitely** — rejected; complicates the data architecture per the audit's "dormant DB whose deferral has gone stale" framing. Carrying a dormant DB raises questions about ongoing maintenance, backup obligations, and consumer expectations.
- **Merge research.db content INTO telemetry.db** — considered but rejected. The research.db structural tables (classes, monsters, skills, etc.) duplicate what's already in telemetry.db. Merging would introduce schema-conflict resolution work without operational gain.
- **Delete without archive** — rejected; the row content (especially the 5 research_notes + 5 bugs_log narrative entries) has historical-context value. Archive preservation is cheap and reversible.

**Status:** Active. Supersedes the 2026-05-07 "Two telemetry databases — deferred consolidation" entry, which should have its status updated to **Superseded by 2026-05-16: research.db retired**.

**Cross-seam follow-on (in flight):** Star-lord dispatch `2026-05-16-star-lord-research-db-script-cleanup.md` handles two engine scripts (`scripts/db.py`, `scripts/capture-regression-baseline.py`) that still reference research.db. Per ADR-004, the cross-seam cleanup is a sibling work item that closes the full retirement. Knight-rider tracks completion.

**Related:**
- `agentic_orchestration/research/curated/data-architecture-audit-2026-05-16.md` § 3.4 (the audit that satisfied the deferral)
- `agentic_orchestration/research/curated/archive/research-db-narrative-archive-2026-05-16.md` (the narrative preservation)
- `agentic_orchestration/dispatches/2026-05-16-elrond-A-research-db-retirement.md` (the dispatch + completion record)
- `agentic_orchestration/dispatches/2026-05-16-star-lord-research-db-script-cleanup.md` (cross-seam follow-on)
- 2026-05-07 decisions-log entry "Two telemetry databases — deferred consolidation" (superseded by this entry)

---

## Companion action — update 2026-05-07 entry status

When this new entry commits, update the 2026-05-07 "Two telemetry databases — deferred consolidation" entry's Status line from "Active. Consolidation deferred..." to **"Superseded by 2026-05-16: research.db retired"** per the decisions-log format convention ("When superseding or reversing an earlier decision, update its status and add a new decision explaining the change. Don't delete or rewrite — preserve the history of how thinking evolved.").
