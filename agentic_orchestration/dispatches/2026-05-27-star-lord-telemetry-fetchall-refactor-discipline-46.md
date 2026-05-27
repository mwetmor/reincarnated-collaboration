# Dispatch — 2026-05-27 — star-lord — Telemetry fetchall refactor sweep (Dispatch 1C; pre-Phase-4 HIGH-risk remediation)

**From:** knight-rider
**To:** star-lord (engine telemetry seam owner)
**Approved by:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Estimated effort:** ~3-5 hours (5 fetchall sites refactor + EXPLAIN QUERY PLAN per query + tests)
**Acceptance:** 5 telemetry fetchall sites refactored to cursor iteration OR `fetchmany(1000)` patterns; LIMIT clauses added where exploratory; SQL aggregation pushed where applicable; Discipline #46 compliance verified

## Quality criterion

**Game-quality goal this dispatch serves:** eliminate HIGH-risk unbounded fetchall on telemetry DB which grows UNBOUNDED across seasons — Discipline #46 § 2.1 audit finding flagged this as kernel-panic-class risk surface. Prevents Phase 4 mechanical archive math gates (Pareto + Crowding + Mahalanobis operating on archive) from compounding telemetry-row-enumeration failures.

**Refutation conditions** (star-lord surfaces if any apply):
- Any fetchall site already has effective bounding via UPSTREAM filter (e.g., per-season query already returns ≤1k rows naturally)
- Refactor changes semantic behavior (e.g., aggregation push-to-SQL produces different totals due to NULL handling)
- LIMIT addition breaks downstream consumer expectations (telemetry analysis sidecars relying on full enumeration)

## Context

Per `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1: **HIGH risk** telemetry sites:
- `src/reincarnated/telemetry/db.py:77`
- `src/reincarnated/telemetry/recorder.py:65`
- `src/reincarnated/telemetry/recorder.py:80`
- `src/reincarnated/telemetry/recorder.py:93`
- `src/reincarnated/telemetry/recorder.py:114`

Telemetry grows UNBOUNDED across seasons — fetchall on accumulated row set risks kernel-panic-class compute.

This is one of 4 parallel pre-Phase-4 dispatches per KR Path (1) kicker § 3.1.

## Required reading

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1 (HIGH-risk audit findings) + § 1 (7 patterns canonical text)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1 (this dispatch's routing source)
- `~/Games/reincarnated-engine/src/reincarnated/telemetry/db.py:77` (primary touch surface)
- `~/Games/reincarnated-engine/src/reincarnated/telemetry/recorder.py:65/80/93/114` (4 sites)
- `.claude/skills/reincarnated-star-lord-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines` (Discipline #46 candidate)

## Discipline #46 compliance (DB-touching dispatch)

- [ ] All refactored DB queries follow stream / push-to-SQL / index / bound / no-cartesian patterns
- [ ] Per-cell bounding applied for math-gate algorithms (N/A — telemetry refactor scope; Phase 4 math gates separate dispatch)
- [ ] EXPLAIN QUERY PLAN run on every refactored query; output captured in completion record
- [ ] Grep audit at Gate-2: no unbounded `fetchall()` in `src/reincarnated/telemetry/` post-refactor

## Scope

For each of 5 sites:

- [ ] Inspect current fetchall site + understand caller's row-count expectation
- [ ] Choose pattern per Discipline #46 § 1:
  - **Pattern 1 (stream):** cursor iteration OR `fetchmany(1000)` loop
  - **Pattern 2 (push-to-SQL):** if caller enumerates rows for count/filter/sum/group, replace with SQL aggregation
  - **Pattern 4 (bound):** add `LIMIT N` if query is exploratory
- [ ] Verify refactored query EXPLAIN QUERY PLAN (capture in completion record)
- [ ] Run existing telemetry tests to confirm no semantic regression
- [ ] Note any behavior changes in MIGRATION.md (per ADR-004 if cross-seam consumer impact)

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/telemetry/AGENT_STATE.md` (or star-lord-OP-preferred location)
- [ ] Grep audit verification: `grep -n "\.fetchall()" src/reincarnated/telemetry/*.py` returns ONLY refactored-with-LIMIT OR test-fixture matches
- [ ] Append completion record to this dispatch with per-site refactor pattern + EXPLAIN QUERY PLAN captures
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] All 5 telemetry fetchall sites refactored OR documented as already-bounded (with rationale)
- [ ] Per-site EXPLAIN QUERY PLAN captured
- [ ] No semantic regression (existing telemetry tests PASS)
- [ ] Grep audit shows no unbounded fetchall in production paths
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended; commit + push
- [ ] Round-trip: not applicable for refactor (telemetry seam internal; no inter-seam fixture dict change)

## Out of scope

- Do NOT touch substrate fetchall sites (rocket Dispatch 1D)
- Do NOT touch export sites (`season_exporter.py:445/455/502` per Disc #46 § 2.1; LOW-risk per-season-bounded; separate scope if needed)
- Do NOT add Discipline #46 amendments to engineering-disciplines.md (jack-ryan seam at Dispatch 1A)
- Do NOT touch Phase 4 math gates code (gamora Dispatch 3A post Matt-gate on math notes)
- Do NOT refactor `cycle13_loadout_ingest.py` fetchall sites (per-season bounded; LOW risk per audit)

## Open questions for star-lord

- **Q-Tel-Refactor-1:** If any of 5 sites turn out to be already-bounded by upstream filter (e.g., per-class_balance_id query), document as INFO-close + note bounding mechanism. Don't force refactor where unneeded.
- **Q-Tel-Refactor-2:** If push-to-SQL aggregation changes return shape (e.g., scalar vs row list), document semantic change + verify caller compatibility.

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 1 (7 patterns) + § 2.1 (HIGH-risk telemetry sites)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1
- Engineering disciplines #1 + #11 + #46 (candidate; firing in parallel via Dispatch 1A)

---

## Completion record

**Completed:** 2026-05-27
**Agent:** star-lord
**Commit:** (see below)

### Per-site disposition

| Site | Method | Pattern applied | Disposition |
|---|---|---|---|
| `db.py:77` `_get_schema_version` | SELECT schema_version FROM schema_meta | Pattern 1 — cursor iteration | REFACTORED. schema_meta is bounded by migration count (~30 rows) but fetchall() replaced with cursor iteration per Discipline #46 stream-not-materialize. Python-side max() with tuple comparison retained (applied_at timestamps can be identical across fast migration runs; ORDER BY applied_at unsafe as version tiebreaker). |
| `recorder.py:65` `get_used_anchor_ids` | SELECT anchor_id FROM seasons WHERE anchor_id IS NOT NULL | Pattern 1+2 — DISTINCT + cursor iteration | REFACTORED. Unbounded growth (one row per season). DISTINCT pushed to SQL: result bounded by anchor library cardinality (~200-400 distinct anchor IDs) vs. total seasons row count. Return type `set[str]` unchanged; caller (`anchor/selector.py:41`) builds deduplication set from same values. |
| `recorder.py:80` `get_recent_anchor_categories` | SELECT ... FROM seasons ... ORDER BY generated_at DESC LIMIT ? | Already bounded | INFO-CLOSE. Query already has `LIMIT ?` with caller-supplied `n` bound. EXPLAIN QUERY PLAN: SCAN seasons USING INDEX idx_seasons_generated_at. Discipline #46 compliant — fetchall() on bounded LIMIT-qualified result is explicitly permitted per Discipline #46 Pattern 4. No change required. |
| `recorder.py:93` `get_used_element_names` | SELECT element_name FROM seasonal_elements | Pattern 1+2 — DISTINCT + cursor iteration | REFACTORED. Unbounded growth (~4 rows per season × N seasons). DISTINCT pushed to SQL: result bounded by D1 pool cardinality (~81 allow-list entries). Return type `set[str]` unchanged; caller (`element/selector.py:169`) builds deduplication set from same values. |
| `recorder.py:114` `get_recent_element_history` | SELECT ... FROM seasonal_elements se JOIN seasons s ... ORDER BY s.generated_at DESC LIMIT ? | Already bounded | INFO-CLOSE. Query already has `LIMIT ?` with `n*4` bound. EXPLAIN QUERY PLAN: SCAN s USING INDEX idx_seasons_generated_at + SEARCH se USING INDEX sqlite_autoindex_seasonal_elements_1. Discipline #46 compliant. No change required. |

### EXPLAIN QUERY PLAN captures

**Before refactor:**

| Site | Plan |
|---|---|
| `db.py:77` | SCAN schema_meta |
| `recorder.py:65` | SCAN seasons |
| `recorder.py:80` | SCAN seasons USING INDEX idx_seasons_generated_at |
| `recorder.py:93` | SCAN seasonal_elements |
| `recorder.py:114` | SCAN s USING INDEX idx_seasons_generated_at; SEARCH se USING INDEX sqlite_autoindex_seasonal_elements_1 |

**After refactor:**

| Site | Plan |
|---|---|
| `db.py:77` | SCAN schema_meta (unchanged; cursor iteration change is semantic not plan-level) |
| `recorder.py:65` | SCAN seasons; USE TEMP B-TREE FOR DISTINCT |
| `recorder.py:93` | SCAN seasonal_elements; USE TEMP B-TREE FOR DISTINCT |

Note on TEMP B-TREE FOR DISTINCT: this is SQLite's correct deduplication mechanism when the column is not indexed. The result set materialized into Python is bounded by cardinality (D1 pool / anchor library sizes), not by season count. This is the load-bearing Discipline #46 win.

### Grep audit

Post-refactor result of `grep -n "\.fetchall()" src/reincarnated/telemetry/*.py`:

```
src/reincarnated/telemetry/recorder.py:86:            ).fetchall()
src/reincarnated/telemetry/recorder.py:127:            ).fetchall()
```

Both matches have explicit `LIMIT ?` in their SQL (`get_recent_anchor_categories` and `get_recent_element_history`). CLEAN per Discipline #46 Pattern 4 — `fetchall()` is reserved for queries with explicit LIMIT clauses where the limit is empirically known small.

No unbounded fetchall() remains in production paths in `src/reincarnated/telemetry/`.

### Test results

159/159 PASS — full telemetry test suite:
- `test_recorder_fail_loud.py` — 12 tests PASS
- `test_telemetry_tier1.py` — 27 tests PASS
- `test_telemetry_v21.py` — 21 tests PASS
- `test_telemetry_v22.py` — 19 tests PASS
- `test_telemetry_v23.py` — 22 tests PASS
- `test_telemetry_v24.py` — 19 tests PASS
- `test_telemetry_v25_aoe_cast.py` — 27 tests PASS
- `test_gear_generation.py::TestGetSchemaVersionRegression` — 4 tests PASS (direct coverage of `_get_schema_version`)

No semantic regression. Return types unchanged; caller behavior unchanged.

### Q-Tel-Refactor-1 resolution

`recorder.py:80` and `recorder.py:114` are INFO-close — both already bounded by `LIMIT ?` with caller-supplied bounds. No refactor needed. Documented above.

### Q-Tel-Refactor-2 resolution

DISTINCT addition changes the SQL result set (eliminates duplicate rows) but does NOT change the return shape. Both `get_used_anchor_ids` and `get_used_element_names` return `set[str]` — a set is inherently deduplicated. The Python-side `{row[0] for row in cursor}` set comprehension previously did the deduplication in Python from duplicate rows; now SQL does it instead. Semantics are identical. Caller compatibility confirmed by test suite pass.

### Cross-seam impact

None. Telemetry seam internal query optimization only. No schema change. No MIGRATION.md entry needed. No inter-seam fixture dict changes. Callers (`anchor/selector.py`, `element/selector.py`) consume unchanged return types.

### Acceptance criteria checklist

- [x] All 5 telemetry fetchall sites refactored OR documented as already-bounded (with rationale)
- [x] Per-site EXPLAIN QUERY PLAN captured
- [x] No semantic regression (existing telemetry tests PASS — 159/159)
- [x] Grep audit shows no unbounded fetchall in production paths
- [x] AGENT_STATE.md updated
- [x] Completion record appended; commit + push
