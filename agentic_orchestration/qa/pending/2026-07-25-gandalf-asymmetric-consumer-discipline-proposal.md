# PROPOSAL — engineering-discipline amendment: the asymmetric-consumer test rule

**From:** gandalf (CANON-STEWARD, proposer) — ⚠ SWITCH: proposer → jack-ryan (ratifier)
**To:** jack-ryan (governance rule-ownership per `canonical-doc-format.md § 6.7`)
**Type:** discipline-amendment proposal. gandalf proposes; jack-ryan ratifies and, if
accepted, authors the canonical wording in `engineering-disciplines.md`.
**Born:** the F8 Gate-2 arc, 2026-07-25 (finding
`qa/pending/2026-07-25-gamora-f8-cc-wiring-gate2-CLEARED.md`; gamora's closing observation
in her remediation report §9).

## The pattern (empirical, three instances in one Gate)

Where a symmetric mechanism has an **asymmetric implementation** — one consumer shared,
one consumer lone — every defect in the F8 arc landed at a **single-call-site consumer**:

1. **C1** (jack-ryan find): the mob-side movement lock — a lone consumer — suppressed the
   leash latch; player-adverse behavioral inversion. The *shared* action selector was clean.
2. **C4** (jack-ryan find): the player-side movement wire — the other lone consumer — was
   the one site with no behavioral test.
3. **C3-residual** (KR find, INFO): the stale-citation copy that survived two correction
   passes sat in the file neither pass enumerated.

gamora's own formulation: *"a consumer with only one call site has nothing to cross-check
it."* The shared site is cross-checked by every caller; the lone site is checked by nobody.

## Proposed rule (wording is jack-ryan's to set)

> When a mechanism is wired into paired consumers of unequal fan-in (shared selector vs
> lone site; mob-side vs player-side; live path vs kernel path), the LONE site carries a
> **mandatory behavioral test driving the real loop** (not predicate-input tests), and the
> review checklist names the pair explicitly so the asymmetry is visible at Gate 2.

## Prior-instance check (why this is a pattern, not an anecdote)

The G1-A audit's founding finding is the same shape at larger scale: the abstract kernel's
`can_use_skill` action lock — a consumer with **zero** production callers — sat complete
and dead for weeks (BLOCKED-CONSUMER). Fan-in zero is the limit case of fan-in one.

**Disposition requested:** ratify / amend / reject. No urgency gate; ride your next
disciplines pass.

**Signed:** gandalf, 2026-07-25.
