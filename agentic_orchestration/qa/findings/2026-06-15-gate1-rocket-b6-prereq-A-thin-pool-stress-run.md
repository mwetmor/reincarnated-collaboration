# Finding — 2026-06-15 — Gate-1 — rocket b6-deletion Prerequisite A (adversarial/thin-pool envelope kit_size stress-run)

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, pre-fire)
**Severity:** N/A (Gate-1 verdict: CLEAR-WITH-AMENDMENTS)
**Target:** `agentic_orchestration/dispatches/2026-06-15-rocket-b6-deletion-prereq-A-thin-pool-stress-run.md`
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate vs full-regen), 5 (severity / honest-fail integrity)

## Verdict

**CLEAR-WITH-AMENDMENTS.** Acceptance criterion is faithful to brief §2-A and §4.1 and is decisive for licensing the b6 deletion. Honest-fail clause is load-bearing and correctly routes to gandalf+KR. Boundaries (no deletion, no L1, no bundling, no push) hold. One amendment required before firing.

## What I found
The pass criterion (10–13 band, 100% meets-floor, per-cell median ≥10, geometry-only-distinct reported SEPARATELY from the (geo, role, tier_band) triple, mechanic-pool path AST-disabled) is the identical Phase-2 gate definition applied to a hostile pool — exactly the design-insurance test brief §2-A specifies. The single Gate-1 gap is the adversarial-pool CONSTRUCTION: "deliberately thin physical-weapon coverage + wide bc-cell spread" is directionally correct but the dispatch leaves construction to rocket's math-note with jack-ryan validation bracketed as CONDITIONAL ("[HALT, jack-ryan Gate-1 if math warrants]" in the Sequence line; "HALT for jack-ryan Gate-2 on the result" in scope item 1). For the precise anti-pattern this whole gate guards against — brief §4: "do NOT treat the cycle-14-balanced pass as sufficient" / "do NOT re-run a friendly pool and call it stressed" — the hostility-construction must be validated at Gate-1 on the math-note BEFORE the multi-day run, not only at Gate-2 on the result. A soft pool would otherwise burn a Pattern-B run before I see it.

## Rationale
Discipline #1 (math-before-code): the adversarial-pool construction IS the math that makes this run meaningful; its rigor is the load-bearing decision. Per REVIEW_PROCESS Principle 1, the math-note is where the test's validity is established. Making my Gate-1 on the construction CONDITIONAL inverts the burden — the whole prerequisite exists because the friendly-pool pass was insufficient, so confirming the pool is genuinely hostile cannot be optional.

## Required amendment (fold in before marking FIRED)
Change scope item 1 and the Sequence line so the math-note Gate-1 is **mandatory, not conditional**:

> Scope item 1: "Math-note FIRST (Discipline #1) — define the adversarial-pool construction (what makes it hostile: thin physical-weapon coverage, wide bc-cell spread), code-cited, and the expected floor behavior. **HALT for MANDATORY jack-ryan Gate-1 on the math-note** (the pool-hostility construction is the load-bearing decision; this Gate-1 is not skippable). Then jack-ryan Gate-2 on the RESULT per brief §2-A owner line."

> Sequence: "...rocket math-note (adversarial-pool construction) → **[HALT — MANDATORY jack-ryan Gate-1 on the construction]** → rocket stress-run → jack-ryan Gate-2 on the result → ..."

## Action
- [ ] KR: fold the amendment into the dispatch, then mark FIRED.
- [ ] rocket: math-note construction must arrive at jack-ryan Gate-1 before the run starts.

## References
- `agentic_orchestration/dispatches/2026-06-15-rocket-b6-deletion-prereq-A-thin-pool-stress-run.md`
- `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` §2-A, §4
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` §6-quater Decision 2
- `~/Games/reincarnated-engine/src/reincarnated/generation/class_generator.py:636-688` (the b6 physical-fork routing the deletion will eventually remove — untouched by this prerequisite)
