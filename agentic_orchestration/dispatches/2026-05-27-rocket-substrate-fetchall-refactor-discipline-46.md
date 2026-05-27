# Dispatch — 2026-05-27 — rocket — Substrate fetchall refactor (Dispatch 1D; pre-Phase-4 LOW-MEDIUM-risk remediation)

**From:** knight-rider
**To:** rocket (engine generation seam owner)
**Approved by:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Estimated effort:** ~2-3 hours (2 fetchall sites refactor + EXPLAIN QUERY PLAN per query + tests)
**Acceptance:** 2 substrate fetchall sites refactored per Discipline #46 § 1 patterns; EXPLAIN QUERY PLAN captured; grep audit clean post-refactor

## Quality criterion

**Game-quality goal this dispatch serves:** apply Discipline #46 streaming + bounding patterns to substrate query sites; preserves clean query patterns as substrate grows (currently ~2,499 v1_scope rows; could grow across cycles); composes with elrond v1_scope index addition (Dispatch 1B parallel) for filter-column index hits.

**Refutation conditions** (rocket surfaces if any apply):
- Either site is already effectively bounded (substrate v1_scope returns ~2,499 rows < 10k threshold; ratify if bounded by intent)
- Refactor introduces semantic regression in substrate selection (e.g., per-seed determinism breaks if stream order differs)
- Post-refactor performance regresses (LOW-MEDIUM risk per audit — refactor may be over-engineering for ~2,499 row scale)

## Context

Per `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1: **LOW-MEDIUM risk** substrate sites:
- `src/reincarnated/generation/substrate_weapon_binding.py:332`
- `src/reincarnated/generation/bc_target_substrate_engine.py:342`

Substrate currently bounded short-term (~2,499 rows) but grows across cycles. Pre-Phase-4 remediation applies Discipline #46 patterns pre-emptively.

This is one of 4 parallel pre-Phase-4 dispatches per KR Path (1) kicker § 3.1.

## Required reading

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 2.1 (LOW-MEDIUM substrate sites) + § 1 (7 patterns)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1 (this dispatch's routing source)
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py:332` (primary touch surface 1)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_substrate_engine.py:342` (primary touch surface 2)
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines` (Discipline #46 candidate)

## Discipline #46 compliance (DB-touching dispatch)

- [ ] All refactored DB queries follow stream / push-to-SQL / index / bound / no-cartesian patterns
- [ ] Per-cell bounding applied for math-gate algorithms (N/A — substrate refactor scope; Phase 4 math gates separate dispatch)
- [ ] EXPLAIN QUERY PLAN run on every refactored query; output captured in completion record (verify v1_scope index hit per elrond Dispatch 1B parallel)
- [ ] Grep audit at Gate-2: no unbounded `fetchall()` in `src/reincarnated/generation/substrate_weapon_binding.py` + `bc_target_substrate_engine.py` post-refactor

## Scope

For each of 2 sites:

- [ ] Inspect current fetchall site + understand caller's row-count expectation
- [ ] Choose pattern per Discipline #46 § 1:
  - **Pattern 1 (stream):** cursor iteration OR `fetchmany(1000)` if substrate could grow >1000
  - **Pattern 2 (push-to-SQL):** if caller enumerates rows for count/filter, replace with SQL aggregation
  - **Pattern 4 (bound):** if exploratory, add `LIMIT N`
- [ ] Confirm v1_scope index hit (per elrond Dispatch 1B parallel; expect `SEARCH ... USING INDEX idx_knowledge_v1_scope`)
- [ ] Run existing substrate generation tests to confirm no semantic regression (per-seed determinism preserved)

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
- [ ] Grep audit verification: `grep -n "\.fetchall()" src/reincarnated/generation/substrate_weapon_binding.py src/reincarnated/generation/bc_target_substrate_engine.py` returns ONLY refactored-with-LIMIT OR ratified-as-bounded matches
- [ ] Append completion record to this dispatch with per-site refactor pattern + EXPLAIN QUERY PLAN captures
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Both substrate fetchall sites refactored OR documented as already-bounded (with rationale)
- [ ] Per-site EXPLAIN QUERY PLAN captured (verifies v1_scope index hit)
- [ ] No semantic regression (existing generation tests PASS; per-seed determinism preserved)
- [ ] Grep audit shows no unbounded fetchall in these 2 sites
- [ ] AGENT_STATE.md updated
- [ ] Completion record appended; commit + push
- [ ] Round-trip: not applicable (generation seam internal; no inter-seam fixture dict change)

## Out of scope

- Do NOT touch telemetry fetchall sites (star-lord Dispatch 1C)
- Do NOT touch v1_scope index addition (elrond Dispatch 1B)
- Do NOT add Discipline #46 amendments to engineering-disciplines.md (jack-ryan seam at Dispatch 1A)
- Do NOT touch Phase 4 math gates code (gamora Dispatch 3A post Matt-gate on math notes)
- Do NOT touch export sites (LOW risk per audit; separate scope if needed)

## Open questions for rocket

- **Q-Sub-Refactor-1:** If substrate fetchall is already effectively bounded at ~2,499 rows < 10k threshold per Discipline #46 § 1 Pattern 4 (bound every exploratory query), document as INFO-close + ratify-as-bounded with rationale. Don't force refactor where unneeded.
- **Q-Sub-Refactor-2:** Per-seed determinism — if stream order differs from materialized order, verify per-seed reproducibility preserved (rocket OP seed-stability discipline composes).

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` § 1 (7 patterns) + § 2.1 (LOW-MEDIUM substrate sites)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1
- Engineering disciplines #1 + #11 + #46 (candidate; firing in parallel via Dispatch 1A)
