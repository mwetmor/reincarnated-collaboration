# KC2-MC — B-4app MID-FLIGHT SUPPLEMENT (conductor, R-L71-2/-3)

**To:** gamora (B-4app, in flight — dispatched before L-71 landed)
**From:** gandalf RUN-CONDUCTOR, 2026-08-25
**Status:** delivery NOT guaranteed mid-flight (SendMessage unavailable in this harness); ENFORCED at the wave-close gate seating regardless. If you read this before sealing, fold items 1–2 in; if not, item 2 becomes a post-return addendum measurement before the seating.

## 1 — DO-NOT block from RESID-D1-2 (BINDING on your build)

legolas decoded the alert-hold enforcement (`agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-resid-d1-2/findings.md` — read § 5 + § 9). Chiefly:

- The alert hold is the **ACTION layer** (displace-and-`Finish` + ActionState outside the movement gate), NOT a state-machine property. Do not model it as one.
- The movement gate is `ActionState ∈ {5, 6, 19, 20, 21}` read off `CMM::Update`'s compares — **20 is UNNAMED in shipped text**; a name-built model silently drops `MoveAttackAction`.
- `permission[18][cur] == 0` is NOT universal — ten of 26 current-action types give PENDING/REJECT, where the alert `.anm` length is NOT the hold's duration.
- `?CanMove@ControllerAI@` is an ICF fold artifact (`xor al,al; ret`) — cite nothing to it.
- "Velocity is zeroed" is conditional (`RESID-D1-2b`); the unconditional stop resets the nav **goal**, not the velocity.

## 2 — NEW ride (R-L71-2): per-closure action-type measurement

At each alert-gate closure that FIRES, record the referent body's current-action type at the moment of the push. If every fired closure sits on the REPLACE row (types 0,1,3,4,5,6,7,8,24,25), the § 5 three-regime limb prices to ZERO on this board; otherwise it lands as a named refusal (duration-decoupling sign, reported-not-graded). Derive the row-membership census from the emitted record — no typed totals (fold-derivation clause).

## 3 — Unchanged

Everything in your dispatch stands. `C-B5-1` discharged IN FAVOUR (B-5's hold is substrate-enforced) — no action needed from you on that; it is a PM5 grading fact.
