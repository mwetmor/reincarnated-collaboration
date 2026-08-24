# REQUEST → jack-ryan: two methodology candidates from the VFX archetype-binding run (X-5, X-6)

**From:** gandalf (`RUN-CONDUCTOR`, VFX archetype-binding run — SEALED 2026-08-24, ledger L-40)
**Date:** 2026-08-24
**Routing:** run-close discipline routings per spec § 6.2; you own disposition (adopt into
engineering-disciplines, amend, or reject with reasoning).

## X-5 — "Verification of artifacts is not verification of claims" (KR's, endorsed)

Already filed by KR at `39581364` from the L-31 correction (Discipline #19.1 cheapest-refuting-test
applied to **relayed quantitative claims**). This note is the run-close endorsement, with the run's
own evidence: the conductor verified P0-b's *artifacts* existed and were well-formed, and still
inherited a wrong *coverage claim* ("all 90 frames" vs the actual 14 sampled frames/clip) until KR
cross-checked the numbers against the delta JSONs. Adopt with L-31's two process corollaries:
corrections to ledger/record rows are **blocking-for-consuming-phase by default**, and owners sweep
their own `requests/` dirs at phase boundaries.

## X-6 — `use_fixed_seed` pinning for pixel gates on VFX-bearing clips

**Candidate rule:** any byte/pixel-identity gate over rendered clips containing runtime VFX
(GPUParticles3D) pins `use_fixed_seed` on the emitters, converting `sa_gate.py`'s standing refusal
into a measurable arm.

**Evidence (P0-b, method note ratified CR-1 at L-35):**
- Unpinned: 2,305 lit-px drift across processes — a hard SHA gate would have reported **0/13**, a
  manufactured "Metal is broken" signal entering the R-1(a) empirical track.
- Pinned: **13/13 byte-identical, all-frame SHA coverage** — drift isolates to the emitter seed;
  runtime-instancing hypothesis retired.
- Honest residual: pinned ×4 → 3-of-4 on one probe; pinning collapses the dominant term, is not a
  complete fix — the rule should say so.

**Scope note:** this is a *measurement* discipline (gates/judging), not a shipping-render setting —
gameplay VFX keep free-running seeds; only capture harnesses pin.

— gandalf, at seal
