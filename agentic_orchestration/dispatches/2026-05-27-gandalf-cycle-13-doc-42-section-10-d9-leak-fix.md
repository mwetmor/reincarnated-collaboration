# Dispatch — 2026-05-27 — gandalf — Cycle 13 Doc 42 § 10 D9 Leak Fix (Follow-on to W1+W3+I1 Amendment)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 — Cycle 13 framing brief § 4.1 KR autonomous + gandalf prior amendment (commit `6d4213b`) spot-check surfaced additional D9 leak; follow-on amendment per spot-check recommendation
**Estimated effort:** 5-10 min trivial canonical-text amendment
**Acceptance:** § 10 Wave 1 close criterion bullet 6 amended to remove stale D9 reference; tagged commit

## Context

Gandalf doc 42 amendment commit `6d4213b` landed W1 + W3 + I1 per jack-ryan Gate-1 verdict. Spot-check at end of amendment pass surfaced one additional D9 inconsistency NOT included in original amendment scope:

> **§ 10 Wave 1 close criterion bullet 6 still mentions "+ D9 element/mechanic-gating operational per § 8" — same underlying inconsistency at a third location.** Recommend small follow-on amendment to fully align W1.6 table + § 8 text + § 10 close criterion on D9 → Wave 4. Did not amend per "do not amend beyond W1/W3/I1 scope" discipline.

This dispatch is the small follow-on amendment per spot-check recommendation. Trivial canonical-text fix; ~5-10 min.

## Required reading before starting

1. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` § 10 (Wave 1 close criterion; bullet 6 D9 mention)
2. `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` § 8 (correct text — D9 = Wave 4 scope)
3. `agentic_orchestration/dispatches/2026-05-27-gandalf-cycle-13-doc-42-amendment-w1-w3-i1.md` completion record (spot-check finding source)

## Math-before-code (canonical amendment; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 42 amendment is canonical-text refinement; no schema / fixture / boundary mutation.

## Scope

- [ ] Amend doc 42 § 10 Wave 1 close criterion bullet 6 — remove D9 element/mechanic-gating mention OR explicitly mark "(D9 → Wave 4 scope per § 8)" to maintain consistency with W1.6 + § 8 + § 9 amended text
- [ ] Verify NO other D9 references remain in Wave 1 scope text (W1.0-W1.8 implementation sections, close criteria, principles, etc.); if other leaks found, amend in same commit
- [ ] Tagged commit per gandalf convention: `gandalf: Cycle 13 doc 42 § 10 D9 leak fix — follow-on to amendment commit 6d4213b per spot-check finding`

## Acceptance criteria

- [ ] § 10 bullet 6 amended; D9 stale reference removed OR explicitly scoped to Wave 4
- [ ] No other D9 leaks remain in Wave 1 scope text
- [ ] Tagged commit
- [ ] Round-trip: not applicable

## Out of scope

- Any amendment beyond D9 leak fixes
- Modifying doc 40 / doc 41 / other canonical docs
- Re-litigating doc 42 architectural commitments
- Production code modifications

## References

- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md`
- `agentic_orchestration/dispatches/2026-05-27-gandalf-cycle-13-doc-42-amendment-w1-w3-i1.md` (prior amendment + spot-check)

---

**Cycle:** 13
**Wave:** 1 amendment follow-on
**Gates:** clean canonical state for downstream consumers
**Priority:** P3 — small follow-on; rocket Wave 1 implementation can proceed in parallel since § 10 is close-criterion text, not entry-implementation guidance
