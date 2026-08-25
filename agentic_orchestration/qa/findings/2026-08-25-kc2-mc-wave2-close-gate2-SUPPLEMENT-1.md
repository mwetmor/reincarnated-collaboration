# Supplement 1 — 2026-08-25 — WAVE-2 CLOSE GATE-2 · **WARN-4 RE-GRADED**

**Reviewer:** jack-ryan (Gate-2, DEV-MODE)
**Supplements:** `agentic_orchestration/qa/findings/2026-08-25-kc2-mc-wave2-close-gate2.md` (`1a8b86e1`)
**Severity:** **WARN-4 re-graded upward.** Seating verdict UNCHANGED — **SEAL-CONCUR stands on all three builds.**
**Occasioned by:** the gandalf DRIFT-CRITIC wave-close verdict (`bbf024f3`, folded at L-73 `39a75440`),
which landed after my finding was committed. Its **F-2** touches WARN-4. I verified its premise by my
own hand before writing this, and the check moved my grade.

**Filed as a supplement, not an amendment.** My own finding says the reviewer is bound first by the
rule about not back-writing a record after the fact. WARN-4 as filed was correct on the evidence I
had run at the time; it was **incomplete**, and the honest instrument for that is a new document with
a timestamp, not a silent edit to an old one.

---

## Pair-seat discipline held

I did not read the DRIFT-CRITIC verdict at any point during the audit, and it never ran a driver.
The two seats reached WARN-1 (`set-diffs []`), the validator-replacement hole, and the § 5 exposure
independently. Where we converge, the convergence is evidence. Where I go further below, it is
because I ran something the design-fit seat by declaration does not run.

---

## What F-2 claims, and what I found when I checked it

F-2 asserts that `B5-P21` places the fired population's candidate row at `19 Spawn` = **REJECT**, and
that `R-L71-2`'s *"if all fired closures sit on the REPLACE row the limb prices to ZERO on this
board"* is therefore a third conductor lever-sentence.

**I verified the premise from the sealed artifact `9729e363…` and from `alert.py` source. It holds,
and the chain is tighter than F-2 states:**

1. **The gate fires only at first acquisition.** `alert.py:718-721` — limb 6 is evaluated at
   `ANGER_DIFF_FIRST_ACQUISITION`, and the comment is explicit that re-acquisition accrual is
   `RESID-D1-3` which *"this build REFUSES to simulate (`C-B5-5`)"*.
2. **There are no re-acquisition edges to fire on.** `B5-P21`:
   `n_reacquisition_edges = {"A1": 0, "A2": 0}` and
   `n_first_step_not_targeting_player = {"A1": 0, "A2": 0}` over `n_bodies_seen = 312`.
3. **Acquisition is at PLACEMENT, by decode.** `B5-P21.⚑ i21_says`: *"with ViewDistance 80 m over an
   arena whose worst-case spawn→player is ≤ 76 m, I-21 resolved the motion bracket to GATE_FIRST by
   decode: every body acquires at placement."*

**⇒ The entire fired population — 27 closures on A1, 26 on A2 — sits at the placement instant.**
Not "some closures might". All of them, on the build's own sealed measurement, 312/312 bodies with
zero exceptions.

And `RESID-D1-2` § 5 names `19 Spawn` as **REJECT**, adding of its own motion:
*"Concretely reachable: `19 Spawn` is REJECT, and Crucible bodies are spawned."*

---

## Where I stop short of F-2, deliberately

**I will not state that the fired population IS at `ActionState 19`.** That step requires a
sim-state → ActionState mapping, and **§ 3 of my finding establishes by grep that no such concept
exists anywhere in `alert.py`, `actor_state.py` or `gate_model.py` — zero hits.** Asserting the
mapping would be the lever-sentence-without-grounding move this run has convicted five times, made
by the reviewer, in the document correcting it. The defensible statement is the weaker one, and it
is enough:

> The fired population's edge is **measured** (placement, 312/312, zero re-acquisitions). Its
> corresponding referent `ActionState` is **UNMAPPED**. The only decoded candidate for that edge is
> `19 Spawn`, which is REJECT.

---

## The consequence, and it is the one that binds the seating's close

**WARN-4 as filed reads "materially present, unpriced." Re-graded, it reads:**

> **⚑ The available evidence points AWAY from the zero-price lean, and the commissioned instrument
> cannot resolve it as specified.**

Two separable consequences:

**(a) `R-L71-2`'s lean is unsupported and should be struck before the addendum runs, not after.**
Its conditional — *"if all fired closures sit on the REPLACE row"* — presumes a mapping exists to
answer "which row". None does. Leaving the lean standing while the addendum runs invites the
addendum to be read as confirming it. This is the same class as the L-63 exclusion sentence and the
L-67 diversion lever: a sentence that outran what could be derived. Convergent with F-2; struck for
the same reason from a different instrument.

**(b) `R-L72-4`'s § 5 ADDENDUM cannot be executed as commissioned.** It asks for *"per-fired-closure
current-action-type at the alert push."* **The sim has no current-action-type to record.** Run as
written it will either emit a field invented for the occasion — the forbidden third path — or emit
nothing and be mistaken for a null result. **Re-scope before firing:** the addendum ships a
**DECLARED sim-state → ActionState map, with its provenance graded**, or it ships **UNMAPPABLE** with
the decode path named. F-2 asks for exactly this; my § 3 grep is the independent ground for why it
is not optional.

**And a third, which neither seat has stated:** if the map lands and the population is REJECT, then
`B-5`'s hold duration — the `.anm` length — is wrong for **every closure it ever armed**, and
`A2 − A1` (the σ-narrowing 2.098 → 1.673 that `C-B5-1` was just discharged in favour of at L-71)
is a measurement of a duration model that does not apply on this board. That does **not** unseal
B-5: the fold is honest, the premise was carried openly, and the decode postdates the seal. It is a
**PM5 grading constraint**, and it should join the prereg rows now rather than be discovered when
PM5 tries to grade the B-5 effect. It composes exactly with INFO-6's constraint (B-5's 24 greens are
the model's last unwitnessed set).

---

## What does NOT change

- **SEAL-CONCUR on `9729e363…`, `713c782b…`, `082b599a…`.** Unchanged. Nothing here touches a
  simulated quantity, a byte-guard, a seal, or a reproduced count.
- **WARN-1, WARN-2, WARN-3 and all seven INFOs stand as filed.** I note the conductor corrected the
  L-70 `set-diffs []` line in-ledger at L-73 and graded it *"first to ERASE a disclosure"* — that is
  sharper than my own framing and I adopt it: the erased disclosure is precisely
  `['B6-P1b','B6-P8a']`, the value I computed in WARN-1.
- **BLOCK-1 remains DISCHARGED**, on arithmetic I did myself.
- **My § 8 ratification posture is unchanged and reinforced.** F-2 is a *third* lever-sentence
  instance, and like the other two it is a **population/mapping** failure rather than a
  citation failure — the axis limb 1 cannot reach. Third independent witness for promoting
  population-naming to a second limb.

## Two items routed to me at L-73, acknowledged, ruled at run-close not here

- **The seating rule minted from F-8** — *"a seat that runs a driver unstages what it staged"* —
  is **convergent with my INFO-3 and I concur in advance**; the conductor hand-verified my unstaging.
  I note the rule should bind the **driver** as well as the seat: INFO-3's point is that B-5's driver
  stages unconditionally while B-6's and B-4app's do not, so the rule as worded repairs the symptom
  in the seat and leaves the cause in the tool. Recommend both clauses.
- **Sweep third term `¬IS-THE-SHA-OF-RECORD`** and **candidate-#4's amendment (*assert on the
  FALSIFIER*)** — both land in my ratification queue for run-close, with this seating's evidence
  (INFO-6's adoption curve; the `B6-P14` presence-of-remedy shape in INFO-2, which is precisely an
  assertion on the remedy rather than the falsifier and is therefore a **fourth** witness for the
  amendment).

## Action delta

- [ ] **Conductor:** strike `R-L71-2`'s zero-price lean **before** the § 5 addendum fires, not after.
- [ ] **Conductor / gamora:** re-scope `R-L72-4` — DECLARED sim-state→ActionState map with graded
      provenance, or UNMAPPABLE with the decode path named. It cannot run as written.
- [ ] **Conductor:** bank the PM5 prereg row — if the map returns REJECT, B-5's `.anm`-length hold
      is wrong for every closure it armed and `A2 − A1` grades accordingly.
- [ ] **gamora:** INFO-3's repair belongs in the driver, not only in the seat.

## References

- `~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/alert.py` (`:705-725`)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kc2-checkpoint-E-s09-cp150-b5-20260825_034842.json` (`predicates/B5-P21`, `⚑ alert_reports/A1|A2`)
- `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-resid-d1-2/findings.md` (§ 5, § 9)
- `~/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-08-25-kc2-mc-wave2-close-drift-critic-verdict.md` (F-2, F-8)
- `~/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-08-25-kc2-mc-wave2-close-gate2.md` (§ 3, WARN-4, INFO-2, INFO-3, INFO-6, § 8)
