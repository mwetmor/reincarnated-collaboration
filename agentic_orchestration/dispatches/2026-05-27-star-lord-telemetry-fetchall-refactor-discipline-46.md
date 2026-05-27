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
