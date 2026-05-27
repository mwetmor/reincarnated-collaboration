# Dispatch — 2026-05-27 — gandalf — Cycle 13 Doc 43 W1 Amendment (Add § 11.9 Discipline #23 Framing-Audit Section)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 2 Gate-1 PASS-with-WARN verdict (commit `f9ead71`) requesting W1 doc 43 amendment (non-blocking on rocket fire)
**Estimated effort:** 30-60 min small canonical amendment
**Acceptance:** § 11.9 Discipline #23 framing-audit section added to doc 43 per Wave 1 doc 42 § 11 precedent pattern; three-question protocol answered explicitly; tagged commit

## Context

Jack-ryan Wave 2 Gate-1 critique on doc 43 (commit `f9ead71`) returned PASS-with-WARN with W1 amendment requested:

> **W1 (WARN — gandalf, non-blocking on rocket fire):** Doc 43 is missing a Discipline #23 framing-audit section. Doc 42 (Wave 1 precedent) carried § 11 with the three-question protocol; doc 43 is larger and more load-bearing and has no equivalent. Three-question answers are available and surface no design contradiction — but the section should exist for future readers. Gandalf should add § 11.9 before Wave 3 dispatch authoring.

This dispatch fires the W1 amendment. NON-BLOCKING on rocket Wave 2 implementation (firing in parallel per jack-ryan classification). Gates Wave 3 dispatch authoring (W1 amendment should land before Wave 3 fires for clean canonical state).

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (Gate-1 verdict; W1 amendment specifics)
2. `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` (YOUR doc to amend; specifically § 11 where § 11.9 will land)
3. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` § 11 (precedent for framing-audit section structure)
4. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #23 framing-audit three-question protocol spec)
5. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)

## Math-before-code (canonical amendment; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 43 amendment is canonical-text refinement; no schema / fixture / boundary mutation.

## Scope

- [ ] Author NEW § 11.9 in doc 43 — Discipline #23 framing-audit (three-question protocol)
  - **Q1 (what would refute):** if 3-category T4 taxonomy is wrong shape, what evidence would surface? (Per jack-ryan Gate-1 Q1)
  - **Q2 (cheapest refuting test):** how cheaply can rocket implementation falsify? (Per jack-ryan Gate-1 Q2)
  - **Q3 (alternative framing):** is "3-category as primary unit" framing right, OR is "6-strategy as primary + 3-category as player-facing" cleaner? (Per jack-ryan Gate-1 Q3)
- [ ] Mirror doc 42 § 11 structural pattern (three-question table + answer + load-bearing-or-not classification)
- [ ] Section length proportional to doc 42 § 11 scope (~1-2 pages typical)

## Acceptance criteria

- [ ] § 11.9 added to doc 43 with all three Q1/Q2/Q3 answers
- [ ] Mirror doc 42 § 11 structural pattern
- [ ] No regression in other doc 43 sections
- [ ] Tag intent: `gandalf: Cycle 13 doc 43 W1 amendment — § 11.9 Discipline #23 framing-audit section (per jack-ryan Wave 2 Gate-1 verdict f9ead71)`
- [ ] Round-trip: not applicable

## Out of scope

- Amendments beyond W1 (other Gate-1 amendments are KR fold-into-rocket-dispatch scope)
- Modifying doc 40 / doc 41 / doc 42 / other canonical docs
- Re-litigating doc 43 architectural commitments
- Production code modifications

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-1-doc-43-critique.md` (Gate-1 source)
- `canonical/43-t4-algorithm-wave-2-intent-2026-05-27.md` (target)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` § 11 (precedent pattern)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#23)

---

**Cycle:** 13
**Wave:** 2 amendment (small follow-on; non-blocking on rocket)
**Gates:** clean canonical state for Wave 3 dispatch authoring
**Priority:** P3 — small follow-on; rocket Wave 2 implementation fires in parallel
