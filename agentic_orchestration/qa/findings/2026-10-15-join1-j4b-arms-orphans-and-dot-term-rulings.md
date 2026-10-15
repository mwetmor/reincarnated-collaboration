# Finding — 2026-10-15 — JOIN-1 J4b graded-arm gate rules: N-2 orphans (completeness) and the DoT `running_at_end` term

**Reviewer:** jack-ryan
**Severity:** BLOCK on any graded J4b verdict (ruling 1 HELD; the completeness gate stays HALT) · ruling 2 ACKNOWLEDGED
**Target:** grains at godot `2ca2298` (105 files; **I re-verified the sha256 + size pins: 105/105**); gamora's checks in collab `33eddbc97`, engine `3c8519b1…0c97b2ef`
**Developers:** gamora (gates), drax (grains)
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10; my CORR-3 delta `6d6d0195f` WARN-1/INFO-1; seal Gate-2 `90b2e12ad` N-2

## Ruling 1 — orphans: HELD; the gate stays HALT
**The CORR-4 test is FALSE AS PRE-STATED and stays recorded that way.** That is the conductor's position, and I concur.

**What I derived from GB / GHR / GH / G5 myself.** An orphan is a GHR `(salt, seq)` with no GH row. GB spans are `[on, off)`.
- **Orphan counts:** her 3 and his 60, all with `passed: false`.
  - 49 orphans sit on the final tick and 14 do not. The 14 are 2–13 ticks earlier, in 11 cells, all in his wave 160.
  - In every cell `seq` is contiguous, and no GH row lacks a GHR.
- **(a)** For each of the 14, no body is alive at any tick after it: **0/14**.
- **(c)** No orphan anywhere has a living body after it: **0/63**.
- **(b)** Each target is dead by its tick (`off ≤ t+1`): **63/63, but only because GB says so.** In several orphans the target had left the board **before** the hit:
  - M0 s1: `off 4067`, hit 4074;
  - M-POL-2 s3 (×2): `off 4559`, hit 4561;
  - M-POL-2-NULL s4: `off 4643`, hit 4653.

  In those cells the last tick any body is on the board is *earlier* than the orphan. gamora's cause ("the tick of the last hit on the board") is therefore not what the grains show for them.
- **The anomaly is not confined to orphans. It is pervasive for PETS:**
  - **his side:** 35,292 records target a pet at or after its GB `off_tick` (35,282 of them have a GH decision). They cover 7,145 pet bodies, with a lag of 0–19 ticks.
  - **her side:** 53 such records, plus **204 records on pets that have no GB span at all**.
  - **Roster bodies: 0.** Every roster record is inside its span.

**Consequence.** GB is not yet a trustworthy oracle for "no body remains" or "target dead", so the proposed restatement cannot be confirmed. The fault is in the instrument, not the rule. This also bears on the GB-based **effect gate (b)** and the **flinch duty** wherever pets enter. Roster-only uses are unaffected, including WARN-2's death tick.

**What is needed:**
1. **drax's diagnosis** of what pet `off_tick` means.
   - **If the GB emitter is wrong:** fix it fail-first. Every GHR target needs a span, and spans must end at true removal. Then rerun both arms.
   - **If the sealed runtime books hits on gone pets** (referent behaviour): document it. Then **rule whether those records draw `gethit`**. KP-455 includes *killing blows*, not hits after death, and 35k records move the stream position.
2. **The restated rule, in falsifiable form (my answer to (d)).** An orphan is a terminal truncation iff:
   - **(i)** no body, roster or pet, is on the board at any tick after its tick;
   - **(ii)** its target's death tick is at or before its tick.

   Both are evaluated **only when precondition (P) holds.** (P) has two parts:
   - GB is **complete**: every GHR target has a span;
   - GB is **consistent**: no record falls at or after its target's `off_tick`, beyond whatever drax's ruling sanctions.

   If (P) fails, the result is NO VERDICT, not a pass. (P) fails today.
3. If (P) holds on the corrected grains and (i)/(ii) pass, I will rule the gate passable under the rule, **named as post-hoc** (adopted after CORR-4 failed).

## Ruling 2 — DoT conservation: `running_at_end` ACKNOWLEDGED
- My CORR-3 WARN-1 item 2 identity omitted the mass still in flight when the run ends. The term is legitimate, and the identity of record is **registered = landed + mirror_dropped + running_at_end**.
- **What I verified:**
  - The term is **computed from the mirror's live state** (Σ `rate_f × rem` over `dots`, plus `dots_once`; `kc2p_join2_emit.gd:803–807`). It is not taken as a residual.
  - It is nonzero in **1 of 25** cells (M-POL-2 s1, 739.854…, a `survived_window` terminal at tick 1,372), and there it equals the pre-term residual to about 3e-12 absolute.
  - The worst relative error across all 25 cells is **2.6e-15**.
- **Conditions:**
  - the term is reported per cell and never counted as landed intake;
  - a negative value, or a nonzero value on a cell with no live DoT at the end, is a HALT.

## Action
- [ ] drax: diagnose pet `off_tick`. Close the 204 span-less pet targets. Fix the emitter fail-first or document the referent, whichever applies.
- [ ] gamora: adopt the (P) + (i)/(ii) form. Keep CORR-4 recorded FALSE AS PRE-STATED. Put the ruling 2 conditions in the grader.
- [ ] Matt: only if drax finds the referent books hits on gone pets *and* those records should draw gethit. That is a KP-455 scope question.

## References
- grains `/Users/admin/Games/join3c-bulk/arms-v51/{her,his}/<arm>{,-join}/` (pins `reincarnated-godot/evidence/join1/j4b-hook/arms-v51/grains_sha256.json`)
- `reincarnated-godot/evidence/join1/j4b-hook/arms-v51/{RESULTS.md,checks.json,GC-*.jsonl}`; `reincarnated-godot/kc2_play/tools/kc2p_join2_emit.gd`
- `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-arms-v51-engine-checks/`
