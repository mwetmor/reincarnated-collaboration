# Dispatch — 2026-05-27 — elrond — v1_scope index addition (Dispatch 1B; pre-Phase-4 small focused)

**From:** knight-rider
**To:** elrond (catalogue DB seam owner)
**Approved by:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Estimated effort:** ~1 hour
**Acceptance:** `idx_knowledge_v1_scope` index created on `weapon_knowledge_entries(v1_scope)`; EXPLAIN QUERY PLAN verified to hit index on existing substrate queries

## Quality criterion

**Game-quality goal this dispatch serves:** quick remediation of missing index on the v1_scope filter column — applied to every substrate query (SC-6 audit + SC-6b enrichment + Path A revert + Substrate enrichment); composes with Discipline #46 § 3 index-filter-columns pattern. Without this index, substrate queries do full scans against 90,014-row weapon_knowledge_entries table.

**Refutation conditions** (elrond surfaces if any apply):
- Index already exists (verify via `sqlite_master`; if so, INFO-close)
- EXPLAIN QUERY PLAN post-index still shows full scan (would invalidate the remediation)
- Index addition contradicts existing schema invariants

## Context

Per `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1: "Indexes status: `weapon_knowledge_entries` has indexes on `canonical_name`, `source_library`, `cluster_id`. **Missing: `v1_scope` index** (filter column used in EVERY substrate query). Quick remediation."

This is one of 4 parallel pre-Phase-4 dispatches per KR Path (1) kicker § 3.1.

## Required reading

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1 (audit finding)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1 (this dispatch's routing source)
- `agentic_orchestration/elrond/notes/2026-05-27-cycle-14-sc-6-substrate-weapon-audit.md` § 1.1 (substrate DB schema)
- `agentic_orchestration/elrond/research/sc-6b-substrate-enrichment-2026-05-27/MIGRATION.md` (SC-6b schema extension precedent)
- `.claude/skills/reincarnated-elrond-operating-procedure`

## Discipline #46 compliance (DB-touching dispatch)

- [x] All new DB queries follow stream / push-to-SQL / index / bound / no-cartesian patterns (this dispatch ADDS an index; doesn't introduce new queries)
- [ ] Per-cell bounding applied for math-gate algorithms (N/A — index-only scope)
- [ ] EXPLAIN QUERY PLAN run on every existing substrate query post-index; output captured in completion record
- [ ] Grep audit at Gate-2: N/A (no code changes; DDL only)

## Scope

- [ ] Verify index doesn't already exist: `SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='weapon_knowledge_entries';`
- [ ] Execute: `CREATE INDEX IF NOT EXISTS idx_knowledge_v1_scope ON weapon_knowledge_entries(v1_scope);` against `~/Games/reincarnated-loadout/data/telemetry.db`
- [ ] Verify EXPLAIN QUERY PLAN hits index on representative substrate queries (e.g., `EXPLAIN QUERY PLAN SELECT * FROM weapon_knowledge_entries WHERE v1_scope=1;`)
- [ ] Pre-add backup: confirm latest substrate DB backup exists (per SC-6b precedent at `telemetry.db.pre-substrate-enrichment-2026-05-27.bak` already in place)
- [ ] Append completion record to this dispatch with EXPLAIN QUERY PLAN output captured
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] `idx_knowledge_v1_scope` exists in `sqlite_master`
- [ ] EXPLAIN QUERY PLAN on `SELECT * FROM weapon_knowledge_entries WHERE v1_scope=1` shows `SEARCH ... USING INDEX idx_knowledge_v1_scope` (NOT `SCAN`)
- [ ] Completion record appended with EXPLAIN QUERY PLAN output
- [ ] Round-trip: not applicable (intra-seam DDL; no cross-seam contract change)

## Out of scope

- Do NOT modify substrate library data (DDL only)
- Do NOT touch telemetry fetchall sites (star-lord Dispatch 1C)
- Do NOT touch substrate fetchall sites (rocket Dispatch 1D)
- Do NOT add indexes beyond v1_scope (other filter columns per Discipline #46 evaluation are separate scope)
- Do NOT enter Phase D substrate cleaning execution mode

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1
- Engineering disciplines #11 + #46 (candidate; firing in parallel via Dispatch 1A)
