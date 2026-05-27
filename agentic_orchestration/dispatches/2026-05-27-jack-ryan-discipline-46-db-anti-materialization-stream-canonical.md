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

---

## Completion record

**Completed by:** jack-ryan
**Date:** 2026-05-27
**Status:** DONE — Discipline #46 canonical-write COMPLETE

### Scope checklist — all items closed

- [x] Read gandalf candidate at `2026-05-27-discipline-46-db-streaming-candidate.md` in full
- [x] Canonical-write at `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #46 per 7 patterns (stream + push-to-SQL + index + bound + audit-cartesian + WAL + per-cell-bounding-for-math-gates)
- [x] STATUS: LOAD-BEARING (pre-Phase-4 protection)
- [x] Cross-references to Disciplines #1 (math-before-code) + #11 (empirical inspection) + #18 (math-hotspot) + #34 (concentration) — cited in Discipline #46 "Composes with" section
- [x] Reciprocal cross-references added: #1 (pre-fire projection cross-ref to #46); #11 (EXPLAIN QUERY PLAN cross-ref to #46); #18 (Phase 4 hotspot cross-ref to #46); #34 (per-cell bounding as concentration cross-ref to #46)
- [x] Gate-1 checklist amended: 3 additions at Discipline #46 § "Operational hooks — Gate-1 review (jack-ryan)"
- [x] Gate-2 checklist amended: mechanical grep audit 3-command pattern at Discipline #46 § "Operational hooks — Gate-2 review (jack-ryan)"
- [x] Anchored examples: 5 HIGH-risk telemetry sites + 2 LOW-MEDIUM substrate sites + v1_scope missing index + Phase 4 HIGHEST-without-discipline — all present in § "Audit findings 2026-05-27"
- [x] Dispatch authoring compliance template added: § "Operational hooks — Dispatch authoring (KR)" ready for KR consumption
- [x] Scope note appended to engineering-disciplines.md top-level header
- [x] Anatomy section updated (Discipline #45 slot reserved; Discipline #46 registered)
- [x] Cross-references section updated (Discipline #46 source docs added)

### Q-Disc46-1 resolution

**Question:** Pattern 7 per-cell-bounding for math gates — separate sub-discipline #46.1 OR Pattern 7 of main #46?

**Resolution: Pattern 7 of main #46.** Per-cell bounding is a specific application of the stream-not-materialize + bound-every-query principles already in Patterns 1 and 4, specialized to cross-kit comparison algorithms. The failure mode is the same kernel-panic-class O(n²) materialization; the distinction is the scope (archive-wide vs per-cell). Sub-discipline numbering is warranted when a sub-discipline has its own distinct operational trigger not covered by the parent (precedent: #18.1 substrate-voting-is-binding; #11.1 state-space conditioning — both have distinct failure modes from parent). Pattern 7 does not clear that bar. Stays as Pattern 7 within main #46.

### Q-Disc46-2 resolution

**Question:** Should existing Disciplines #1/#11/#18/#34 forward-reference #46?

**Resolution: YES — surgical bidirectional cross-references applied.** Per precedent from #42/#43/#44 bundle. Applied four forward-references:
- **#1** → #46: at §1.1 pre-fire resource-bounds projection — DB result-set materialization path must be included in memory projection for Phase 4 / telemetry dispatches
- **#11** → #46: at §11.1 cross-references — `EXPLAIN QUERY PLAN` is Discipline #11 applied at DB query cost surface; #46 Pattern 3 operationalizes it
- **#18** → #46: at §18 triggerable Gate-1 question extension — Phase 4 math hotspot methodology lock must include DB query pattern selection, not only algorithm choice
- **#34** → #46: at §34 cross-references — per-cell bounding is concentration applied at archive comparison scope; same architectural principle as mechanic-alteration concentration

### Framing-audit record (Discipline #42 compliance)

- Framing-audit fired: YES
- Q1 load-bearing assumptions identified: (1) gandalf candidate 7 patterns are internally consistent and non-contradicting; (2) Pattern 7 per-cell bounding fits as a named application rather than a distinct sub-discipline; (3) reciprocal cross-references to #1/#11/#18/#34 are warranted by the bidirectional precedent from #42/#43/#44 bundle
- Q2 refutation evidence: checked dispatch refutation conditions — no composition contradictions found; stream + push-to-SQL are complementary not conflicting; per-cell bounding is explicitly a Pattern 4 (bound-every-query) application, not a contradiction
- Q3 outcome: PROCEED — framing sound; no Q3=YES trigger surfaced
