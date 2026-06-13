# Item 10 Part B landed — cross-seam flag (rocket → knight-rider; cc gamora, jack-ryan, gandalf)

**From:** rocket (content-generation seam)
**Date:** 2026-06-12
**Re:** Item 10 Part B (charge-stack magnitude distribution) UN-HELD + landed + pushed
**Trigger:** Matt — "gamora finished item four. Please proceed to item 10 and push once done and committed."
**Commit:** engine main `452ca29` (`d2ea435..452ca29`, pushed)

---

## 1. What landed

Part B of Item 10 — the per-kit hold-vs-spend magnitude assignment for charge-stack kits. Extends
`generation/charge_stack_generation.py` (Part A was `3a122d3`). Math note
`session-3-item-10-part-b-charge-stack-magnitude-distribution-2026-06-12.md` precedes the code (Disc #1).
Smoke: charge-stack 26 passed (13 A + 13 B); full Session 3/4 rocket suite **180 passed** (167 + 13).

The first-order crossover model `α(T) = S − (T−2)(T−1)/(2T)` (S=10) is anchored to gamora's kernel Item 4
(`dae0349`) §6.1–6.4 economics. HOLD-optimal ⟺ `cbps/psb < α(T)`. PROVISIONAL config bands
(do-not-self-adjust). PREDICTED Axis-5 bin emitted at generation; MEASURED split is a downstream RUN.

## 2. KR ACTION — ratify the cross-seam field-name contract

There is a name mismatch for the **same** quantity across the rocket↔gamora seam:

| Quantity | rocket field (`skill_schema.Skill`) | kernel field (`combatant.CombatantState`) |
|---|---|---|
| per-held-stack damage mult (hold reward) | `per_stack_passive_bonus` | `per_stack_passive_bonus` (✔ identical) |
| per-spent-stack burst rate (spend reward) | `threshold_burst_magnitude` | **`charge_burst_per_stack`** (✘ name differs) |

Both are the *same per-stack rate* — NOT a total magnitude. I kept the rocket name (a shipped reserved
field — renaming churns a published schema) and documented the 1:1 mapping
`threshold_burst_magnitude → charge_burst_per_stack` in `generation/MIGRATION.md`. **This is a HOW-latitude
call; it does not change a ratified surface.** Recommend KR/gandalf ratify either (a) the documented alias
(status quo — cheapest), or (b) a future rename so one name spans the seam. No action blocks the gate.

## 3. gamora ACTION — kit→CombatantState live wiring (follow-on, not blocking)

The kernel reads **actor-level** `per_stack_passive_bonus` + `charge_burst_per_stack`. Part B emits these
on the per-chain **spend skill** (Part A guarantees exactly one per chain), with the generation invariant
that all spend skills in one kit share the `(psb, cbps)` pair. The kit→CombatantState builder (gamora
seam) must lift them to actor level. **This wiring does not exist yet** — no charge-stack kit is in the
Season 001010 corpus (gamora's golden-master delta was 0/60 precisely because every charge-stack branch
is dead code for that corpus). Same follow-on pattern as the companion-record wiring gamora flagged. The
live lift + the MEASURED Axis-5 split RUN fire once a generated season carries a charge-stack kit.

## 4. Gate-2

jack-ryan's pending Gate-2 (handoff note `2026-06-12-session-3-4-generation-cascade-gate-2-handoff.md`,
§ 5.1 added) now covers Parts A **and** B. No milestone tag pending the verdict.

## 5. Collab-repo push status

Engine repo: Part B pushed (`452ca29`). Collab repo: this note + the dispatch completion-record addendum
+ the Gate-2 handoff update are committed locally; collab push held (one teammate commit — gandalf
`c838ff4` — also sits unpushed; the Item-10 push authorization was for the engine code). KR/Matt: collab
push is your call.
