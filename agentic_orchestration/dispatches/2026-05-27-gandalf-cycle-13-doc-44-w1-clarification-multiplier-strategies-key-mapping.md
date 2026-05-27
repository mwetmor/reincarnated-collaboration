# Dispatch — 2026-05-27 — gandalf — Cycle 13 Doc 44 W1 Clarification (Multiplier Strategies Key-Mapping)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 3 Gate-1 PASS-with-WARN verdict (commit `50028cb`) flagging W1 multiplier-strategies-key-mapping arithmetic ambiguity in doc 44 § 8.3
**Estimated effort:** 15-30 min small canonical clarification
**Acceptance:** doc 44 § 8.3 `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count assertion corrected per empirical t4_category_schema.py state; tagged commit

## Context

Jack-ryan Wave 3 Gate-1 critique on doc 44 (commit `50028cb`) returned PASS-with-WARN with one pre-fire required amendment:

> **W1 (WARN — pre-fire required):** `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count = 4 assertion in doc 44 § 8.3 is arithmetically ambiguous. "Multiplier strategies" is not a discrete strategy string constant in `t4_category_schema.py` (7 strategies confirmed empirically; no `STRATEGY_MULTIPLIER` exists). The true-count among Category B/C eligible strategies is likely 3 (TRADE_OFF when skill-specific + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION), not 4. KR resolves with gandalf in a short clarification exchange before rocket W3.1 fires; folded resolution goes into W3.1 acceptance criteria. **This is a precision gap in implementation-spec, not an architectural failure — no BLOCK.**

This dispatch fires the small W1 clarification. NON-BLOCKING on Wave 3 architectural intent (doc 44 is substantively sound per jack-ryan PASS-with-WARN); precision-only correction.

**Per jack-ryan also flagged but already resolved (KR verified empirically — no action needed):**
- I3 doc 44 ground-state § 1 row: ✅ already present (your authoring commit `a80044a` landed it)
- I4 synthetic same-bucket test: ✅ already closed via rocket Wave 2 amendments commit `7287b43` (TestSyntheticAdditiveWindowBucket::test_trade_off_geometry_collapse_int_additive_bucket_penalty present)

Jack-ryan flagged I3+I4 reading pre-most-recent-commits state; empirically clear.

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-1-doc-44-critique.md` (Gate-1 verdict; W1 amendment specifics)
2. `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` § 8.3 (the assertion location to correct)
3. `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (empirical 7-strategy registry; verify true-count by mapping each strategy to Category A vs B/C vs character-wide eligibility)
4. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)

## Math-before-code (canonical amendment; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 44 amendment is canonical-text precision correction; no schema / fixture / boundary mutation.

## Scope

- [ ] Empirically inspect `t4_category_schema.py` to enumerate the 7 strategies + their category mapping (Category A / B / C) + their character-wide eligibility
- [ ] Per jack-ryan analysis: true-count is likely 3 (TRADE_OFF skill-specific + ELEMENT_CONVERSION + DUAL_ELEMENT_ADDITION). Verify or amend.
- [ ] Correct doc 44 § 8.3 `STRATEGY_CHARACTER_WIDE_ELIGIBILITY` true-count assertion to match empirical state
- [ ] Ensure the corrected statement is implementation-actionable for rocket W3.1 (rocket reads § 8.3 + knows exactly how to construct the eligibility set without re-clarification)
- [ ] No regression in other doc 44 sections (verify § 8.3 amendment doesn't conflict with surrounding context)
- [ ] If empirical enumeration surfaces additional inconsistencies in adjacent sections, FLAG (don't author beyond W1 scope)

## Acceptance criteria

- [ ] Doc 44 § 8.3 corrected per empirical t4_category_schema.py state
- [ ] True-count assertion arithmetically grounded
- [ ] Implementation-actionable for rocket W3.1
- [ ] Tag intent: `gandalf: Cycle 13 doc 44 W1 clarification — § 8.3 STRATEGY_CHARACTER_WIDE_ELIGIBILITY true-count corrected per empirical t4_category_schema.py (per jack-ryan Wave 3 Gate-1 verdict 50028cb)`
- [ ] Round-trip: not applicable

## Out of scope

- Any amendment beyond W1 § 8.3 correction
- Doc 40 / doc 41 / doc 42 / doc 43 modifications
- Re-litigating doc 44 architectural commitments (W1 is precision correction, not architectural change)
- I1 / I2 / I5 — those are rocket-dispatch-fold-in or planning-note scope; KR handles
- Production code modifications
- Modifying t4_category_schema.py (it is the source-of-truth; doc 44 amends to match)

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-3-gate-1-doc-44-critique.md` (Gate-1 source)
- `canonical/44-t4-algorithm-wave-3-phase-3-intent-2026-05-27.md` § 8.3 (amendment target)
- `reincarnated-engine/src/reincarnated/generation/t4_category_schema.py` (empirical source)
- `agentic_orchestration/operating-procedures/gandalf.md` (canonical authority)

---

**Cycle:** 13
**Wave:** 3 amendment (small W1; pre-rocket-fire required)
**Gates:** unblocks rocket Wave 3 W3.1 implementation
**Priority:** P2 — small precision correction; gates rocket Wave 3 dispatch authoring
