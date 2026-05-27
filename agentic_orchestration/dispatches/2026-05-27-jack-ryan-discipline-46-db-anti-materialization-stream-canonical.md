# Dispatch — 2026-05-27 — jack-ryan — Discipline #46 canonical-write (Dispatch 1A; pre-Phase-4 LOAD-BEARING)

**From:** knight-rider
**To:** jack-ryan (canonical-write authority for engineering-disciplines.md)
**Approved by:** Matt 2026-05-27 verbatim "I confirm Path (1) + Discipline #46 + the operational moves above"
**Estimated effort:** ~1-2 days canonical-write + Gate-1/Gate-2 checklist amendments
**Acceptance:** Discipline #46 entry authored at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46 (STATUS LOAD-BEARING); Gate-1 + Gate-2 checklists amended with Discipline #46 grep audit; Discipline #46 compliance template added for KR dispatch authoring

## Quality criterion

**Game-quality goal this dispatch serves:** establish DB query discipline that protects Phase 4 mechanical archive math gates (Pareto + Crowding + Mahalanobis + KL + Eviction) from O(n²) kernel-panic-class computational explosions as kit archive grows across seasons. Composes Engine-first orientation: DB query integrity is engine-layer infrastructure protecting downstream game-quality at Wave 5+ scale.

**Refutation conditions** (jack-ryan surfaces if any apply):
- Discipline #46 composition produces contradiction with existing disciplines (#1/#11/#18/#34)
- 7-pattern specification has internal contradiction (e.g., stream + push-to-SQL conflicting)
- Per-cell bounding (§ 7) ambiguous for cross-cell math gates (Phase 4 specific)
- Gate-1/Gate-2 grep audit patterns too brittle (false positives on legitimate `fetchall()` with `LIMIT`)

## Context

Per `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` + KR Path (1) kicker § 3.1 dispatch 1A. Discipline #46 is LOAD-BEARING pre-Phase-4 protection — without it, Phase 4 math gates against growing kit archive risk kernel-panic-class failure. Audit findings 2026-05-27: telemetry/db.py:77 + recorder.py:65/80/93/114 unbounded fetchall (HIGH risk; unbounded growth across seasons); substrate sites (LOW-MEDIUM); v1_scope index missing.

WAL mode ✅ confirmed; JOIN audit ✅ clean. v1_scope index + telemetry fetchall + substrate fetchall refactors fire in parallel via Dispatches 1B/1C/1D.

## Required reading

- `canonical/00-ground-state.md` — ground-state oracle
- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` — **PRIMARY SUBSTANTIVE INPUT** (gandalf candidate; 7-pattern spec + audit findings + operational hooks)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1 (this dispatch's routing source)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition; Phase 4 math gates load-bearing)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § Phase 4 (math gates spec consuming Discipline #46)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — canonical target; particularly Disciplines #1, #11, #18, #34 for composition
- `.claude/skills/reincarnated-jack-ryan-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`

## Discipline #46 compliance (this dispatch authors the discipline; no DB queries touched)

N/A — this dispatch is canonical-write only; no DB queries introduced. The discipline itself defines the compliance template for downstream dispatches.

## Scope

- [ ] Read gandalf candidate at `2026-05-27-discipline-46-db-streaming-candidate.md` in full
- [ ] Canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46 per § 1 proposed canonical text (7 patterns: stream + push-to-SQL + index + bound + audit-cartesian + WAL + per-cell-bounding-for-math-gates)
- [ ] STATUS: LOAD-BEARING (pre-Phase-4 protection)
- [ ] Cross-references to Disciplines #1 (math-before-code; query patterns specified pre-impl) + #11 (empirical inspection; EXPLAIN QUERY PLAN verifies) + #18 (math-hotspot; query-cost methodology) + #34 (concentration at DB layer)
- [ ] Reciprocal cross-references where appropriate (your judgment per critique-pair-gate-protocol)
- [ ] **Amend Gate-1 checklist** per § 3.2: "Does dispatch include Discipline #46 compliance section?" / "Do specified DB queries follow streaming + per-cell patterns?" / "Are indexes mentioned for filter columns?"
- [ ] **Amend Gate-2 checklist** per § 3.3: mechanical grep audit (unbounded fetchall / JOIN without ON / implicit comma-joins)
- [ ] Anchored examples per § 2.1 audit findings (5 HIGH-risk telemetry sites; 2 LOW-MEDIUM substrate sites; v1_scope missing index; Phase 4 math gates HIGHEST-without-discipline)
- [ ] Append completion record to this dispatch
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern (auto-fire per CLAUDE.md addendum)

## Acceptance criteria

- [ ] Discipline #46 entry authored with § Statement + § Why + § Operational hooks + § Cross-references + § Anchored examples
- [ ] STATUS LOAD-BEARING (pre-Phase-4 protection per Matt ratification)
- [ ] Gate-1 + Gate-2 checklist amendments landed
- [ ] Dispatch authoring compliance template per § 3.1 ready for KR consumption
- [ ] Completion record appended; commit + push
- [ ] Round-trip: not applicable (canonical-write; no inter-seam fixture dict change)

## Out of scope

- Do NOT execute v1_scope index addition (elrond Dispatch 1B)
- Do NOT execute telemetry fetchall refactor (star-lord Dispatch 1C)
- Do NOT execute substrate fetchall refactor (rocket Dispatch 1D)
- Do NOT author Phase 4 math notes (bundled Dispatch 2 fires after Discipline #46 ratifies)
- Do NOT amend canonical docs beyond engineering-disciplines.md (gandalf seam)
- Do NOT enter DEV-MODE Gate-2 review (discipline-ratification mode)

## Open questions for jack-ryan

- **Q-Disc46-1:** Pattern 7 per-cell-bounding for math gates — does this need a separate sub-discipline #46.1 OR fits as Pattern 7 of main #46? Your judgment.
- **Q-Disc46-2:** Reciprocal cross-references — should existing Disciplines #1/#11/#18/#34 entries forward-reference #46? Your judgment per surgical bidirectional pattern from Disc #42/#43/#44 bundle precedent.

## References

- `agentic_orchestration/gandalf/notes/2026-05-27-discipline-46-db-streaming-candidate.md` (PRIMARY input)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-kr-scope-expansion-kicker.md` § 3.1
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (canonical target)
- Hive-mind protocol § 4 (decision-routing) + § 7 (math hotspots)
