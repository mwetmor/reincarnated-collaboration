# Dispatch — 2026-05-27 — gandalf — Cycle 13 Doc 45 W1 Clarification (CapabilityCategory Enum Members)

**From:** knight-rider
**To:** gandalf
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 4 Track A Gate-1 PASS-with-WARN verdict (commit `a149001`) flagging W1 capability toolkit enum naming ambiguity in doc 45 § 7.1
**Estimated effort:** 20-40 min small canonical clarification + (optional) downstream semantic alignment
**Acceptance:** doc 45 § 7.1 capability toolkit member list resolved per empirical `partition_schema.py:376-381`; tagged commit

## Context

Jack-ryan Wave 4 Track A Gate-1 critique on doc 45 (commit `a149001`) returned PASS-with-WARN with W1 amendment required before rocket W4R.4 fires:

> **W1 (WARN — required before rocket W4R.4):** `CapabilityCategory.MULTIPLICATIVE` listed in doc 45 § 7.1 does not exist in `partition_schema.py:376-381`. Empirically confirmed via Python import — actual 5th member is `TRUE_ACTIVE`. Resolve with gandalf: either (a) MULTIPLICATIVE is a Wave 4 enum extension added at W4R.1 (len → 6), or (b) § 7.1 contains a naming error and should read TRUE_ACTIVE.

**KR empirical verification confirms:** `CapabilityCategory` has 5 members per `partition_schema.py`:
1. `MECHANIC_ADJUSTING`
2. `SPATIAL_ADJUSTING`
3. `AXIS_ADJUSTING`
4. `TRIGGERED_PASSIVE`
5. `TRUE_ACTIVE`

No `MULTIPLICATIVE` exists. But doc 40 § 3.3 capability toolkit lists "multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill" as the canonical 5-category framework. There's a semantic-vs-naming divergence between canon (doc 40) + implementation (partition_schema.py).

**Resolution options (gandalf seam-owner decides):**

A. **MULTIPLICATIVE is a Wave 4 enum extension** — add new `MULTIPLICATIVE` member to `CapabilityCategory` enum at W4R.1; len → 6; preserves doc 40 canonical taxonomy at implementation level
B. **§ 7.1 naming error** — doc 45 amends to use `TRUE_ACTIVE` (existing); reconcile with doc 40 § 3.3 "multiplicative" framing (e.g., "TRUE_ACTIVE = multiplicative effect at consumption time" semantic note)
C. **Semantic mapping** — doc 45 amends § 7.1 to enumerate the 5 implementation enum members with cross-reference to doc 40 § 3.3 canonical taxonomy + maps the 5 implementation → doc 40 categories
D. **Other** (gandalf seam-owner alternative)

Gandalf clarifies + amends doc 45 § 7.1 accordingly.

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-1-doc-45-critique.md` (Gate-1 verdict; W1 specifics)
2. `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` § 7.1 (the assertion location to correct)
3. `reincarnated-engine/src/reincarnated/generation/partition_schema.py` lines 376-381 (empirical CapabilityCategory enum — 5 members)
4. `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3.3 amended (capability toolkit 5-category framework: multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill)
5. `agentic_orchestration/operating-procedures/gandalf.md` (canonical-doc-format authority)

## Math-before-code (canonical amendment; no code)

NOT applicable.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no cross-seam contract change in this dispatch.** Doc 45 amendment is canonical-text precision correction. If gandalf chooses Option A (enum extension), that's a rocket Wave 4 implementation work item documented in this amendment; the schema change happens at W4R.1, not in this dispatch.

## Scope

- [ ] Empirically inspect `partition_schema.py:376-381` to confirm CapabilityCategory 5 members
- [ ] Cross-reference doc 40 § 3.3 amended capability toolkit 5-category framework
- [ ] Resolve W1 per Option A / B / C / D (gandalf seam-owner call)
- [ ] Amend doc 45 § 7.1 to match resolution (enum member list + any semantic notes)
- [ ] Ensure doc 45 § 7.1 is implementation-actionable for rocket W4R.4 (rocket reads § 7.1 + knows exactly how to implement capability toolkit enforcement without re-clarification)
- [ ] Flag any adjacent inconsistencies (e.g., doc 45 § 5.1 #6 accessory pattern entry references "true-active" — KR is handling W2 in rocket dispatch; gandalf doesn't need to amend if W2 is KR-authorable)

## Acceptance criteria

- [ ] Doc 45 § 7.1 capability toolkit member list resolved per empirical `partition_schema.py` + doc 40 § 3.3
- [ ] Resolution option (A/B/C/D) explicit in commit message + completion record
- [ ] Implementation-actionable for rocket W4R.4
- [ ] Tag intent: `gandalf: Cycle 13 doc 45 W1 clarification — § 7.1 CapabilityCategory enum reconciled per empirical partition_schema.py + doc 40 § 3.3 (per jack-ryan Wave 4 Gate-1 verdict a149001)`
- [ ] Round-trip: not applicable

## Out of scope

- Any amendment beyond W1 § 7.1
- W2 (accessory true-active omission language in W4R.3) — KR-authorable; folds into rocket dispatch; gandalf does NOT amend
- Doc 40 / 41 / 42 / 43 / 44 modifications
- Re-litigating doc 45 architectural commitments
- Production code modifications (if Option A chosen, enum extension is rocket W4R.1 implementation work; doc 45 amendment notes it; rocket implements)

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-4-gate-1-doc-45-critique.md` (Gate-1 source)
- `canonical/45-spec-driven-gear-gen-wave-4-rocket-track-intent-2026-05-27.md` § 7.1 (target)
- `reincarnated-engine/src/reincarnated/generation/partition_schema.py` lines 376-381 (empirical source)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 3.3 (canonical taxonomy)
- `agentic_orchestration/operating-procedures/gandalf.md`

---

**Cycle:** 13
**Wave:** 4 Track A amendment (small W1; pre-rocket-fire required for W4R.4)
**Gates:** unblocks rocket Wave 4 Track A W4R.4 implementation
**Priority:** P2 — small precision correction; gates rocket Wave 4 Track A dispatch authoring on W4R.4 acceptance criteria
