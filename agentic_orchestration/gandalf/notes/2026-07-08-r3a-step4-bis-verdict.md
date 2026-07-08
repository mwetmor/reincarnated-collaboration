# R3a step-4-bis — Acceptance Verdict on the Endgame-BC Spatial Surface (Amended Criterion)

**Author:** gandalf (DRIFT-CRITIC scoring my OWN amended acceptance criterion — the moving-goalposts
risk is maximal here, and I hold it in front of me the whole way)
**Role-tag:** ▶ ROLE: DRIFT-CRITIC — judging existing run data against a spec (my own §3 reframe)
**Date:** 2026-07-08
**Chain:** batch-2 autonomous chain, step R3a-4-bis (verdict on EXISTING step-4 re-run data; NO re-run).
**Scores against:** the AMENDED criterion in `2026-07-08-s4-inverted-surface-acceptance-reframe.md §3`
(tier-1 KPM = the measurement; tier-2 WR = validity screen; WR-gradient = post-demo ladder). NOT the
retired §4-as-authored (single-rung WR gradient), which was an uncontested FAIL and correctly mis-pointed.
**Consumes (all read at source):**
- my reframe note §3/§4/§6 (the criterion + its falsifier + this verdict's own place in the chain)
- `qa/findings/2026-07-08-jackryan-s4-reframe-review.md` (DESIGN-MODE clearance + 2 conditions)
- `gamora/notes/2026-07-08-r3a-step6-cert-repoint-magicpack-audit.md` (zero-code cert re-point; magic_pack re-band + trimodal finding)
- `qa/findings/2026-07-08-jackryan-r3a-step6-gate2.md` (Gate-2 PASS-WITH-FOLLOWUP; all 5 points source-verified)
- `batch2-run-state-2026-07-06.md` tail (step-4 surface: 765/769 clean cells at ceiling, ceil-fraction 0.995; tier-1 KPM spread live)
**Disciplines:** #11, #12 (semantic-shift honesty — if the data contradicts my reframe I say so), rider-4
(anti-Goodhart), Goodhart-guard (self-scoring an own amended criterion → falsifier held explicit).

---

## VERDICT: PASS (under the amended criterion)

The endgame-BC spatial surface PASSES acceptance under the §3 reframe. All three pass-conditions are
met on the EXISTING step-4 re-run data; the falsifier is checked and does NOT fire; no preserved finding
is curve-fit away. The magic_pack re-band changes the surface materially in one scenario but does NOT
change the verdict — it strengthens it. The two content-lane non-viability findings survive as FLAGGED,
carried forward to R4.

**Both gates below me cleared before I score:** jack-ryan CLEARED-WITH-CONDITIONS the reframe itself, and
Gate-2 PASSED gamora's re-point with both conditions discharged (magic_pack audited; boss untouched). I am
not scoring into an open condition — the surface I score is a cleared surface. That matters for honesty:
if I were scoring while Condition 1 (the stale magic_pack band) were still open, the measurement instrument
would be partially uncalibrated on that shell and this PASS would be premature. It is not. Condition 1 is
discharged and Gate-2-verified. I proceed.

---

## Pass-condition 1 — tier-1 KPM is the DISCRIMINATION surface, and the spread is LIVE (falsifier check)

**The falsifier, stated in my own words at reframe §4 q2/q4a:** *"if KPM spread ever collapses to a point
mass, the instrument is dead and the amended criterion FAILS."* This is the load-bearing test. A PASS is
only legitimate if the falsifier is genuinely checkable on this data and genuinely does not fire.

**Evidence (run-state tail, gamora diagnosis, both source-confirmed):**

| scenario | tier-1 KPM p10 / med / p90 | spread (p90/p10) |
|---|---|---|
| open_arena | 22.3 / 31.9 / 53.8 | ~2.41× |
| chokepoint | 23.3 / 35.2 / 57.1 | ~2.45× |

**Falsifier check: DOES NOT FIRE.** A ~2.4× spread from p10 to p90 across the endgame-BC population is not a
point mass by any honest reading. A point-mass collapse would look like p10≈med≈p90 — a degenerate
distribution where every kit clears at the same rate and the instrument discriminates nothing. What the data
shows is the opposite: a continuous clear-speed envelope roughly two-and-a-half times wide, with the median
sitting well off both tails (31.9 between 22.3 and 53.8; 35.2 between 23.3 and 57.1 — not pinned to either
edge). This is the shape the genre produces on farm-tier content: every viable build clears, and the
discrimination between them is clear speed (D3 rifts-per-hour, PoE maps-per-hour). The differential §4
wanted — "spread, not rails" — is alive, one layer down, in the observable the genre actually uses.

**Am I reaching?** I asked myself directly, applying the same Goodhart honesty as §4. No. A 2.4× spread is
not a marginal, squint-to-see-it gradient that I am dressing up as discrimination. It is wide. If the spread
had come back at, say, 1.1× — median hard against p10, a near-degenerate clump with a thin tail — I would be
obligated to call that a soft point-mass and FAIL, and I would. It did not. The pass here is not generous;
it clears the falsifier with room to spare.

**PASS on condition 1.**

## Pass-condition 2 — tier-2 WR is a VALIDITY SCREEN; population clears on-tier; non-engagement is FLAGGED

The amended role for tier-2 WR: not a demanded gradient, but a viability bit — clears on-tier ⇒ viable;
cannot engage ⇒ flagged non-viable, NOT silently gating emission.

**Evidence:** 765/769 clean-surface cells at the WR ceiling (ceil-fraction 0.995); 4 mid; 0 floor. Under
the retired §4 this was the FAIL (I demanded mid-mass and got rails). Under the amended criterion this is
exactly what a validity screen should show on a competent endgame population clearing on-tier content:
near-universal viability. The un-stack + serial-engagement pass removed the lockout mechanic (65× stacked
HP on a fixed clock, tick-0 total-field convergence) that previously made WR≈1.000 mean "instrument broken."
What remains at ceiling is not lockout — it is a viable population passing its validity screen. jack-ryan
code-verified (reframe review §2) that the certification architecture ALREADY runs this way: clear shells
gate on the KPM band, boss shells gate on a survive-and-kill viability bit, and NO code path ever demanded a
WR gradient. gamora confirmed the same at zero code delta. The reframe aligns the criterion to what the
engine always did.

**Non-engagement FLAGGED, not silently gating:** gamora confirmed the flags are already served by the
step-5 `tier_1_reject_breakout` in-JSON aggregate — `reject_below_floor` / `reject_no_kpm` ARE the flags. A
cell that kills zero mobs surfaces as `reject_no_kpm`; a cell that cannot clear in the window surfaces as
`reject_below_floor`. This is the crux of the reframe's integrity: non-viability does not vanish into a
silent floor-fail — it emits a named flag that routes to the content lane. Verified as existing machinery,
not aspirational.

**PASS on condition 2.**

## Pass-condition 3 — non-viability findings PRESERVED, not deleted (Discipline #12 honesty)

Two genuine content non-viability findings must survive as FLAGGED content-lane items, not be curve-fit away.

**(a) boss_with_adds — 117/189 kits kill ZERO mobs.** This is content non-viability, not a band mis-fit.
Zero engagement is not a difficulty gradient — it is a room a large fraction of the population cannot engage
at all. It stays FLAGGED, carried to R4 as a content-lane item, and it must NOT silently gate Leg-C.
jack-ryan's Condition 2 keeps the open sub-question honest: KPM may be the wrong observable for boss rooms
entirely (a boss fight's genre observable is TTK + deaths, not kills-per-minute), and boss shells already
gate on a survival-viability bit, not KPM — so the reframe's "tier-1 KPM = THE measurement" statement
applies to CLEAR shells, not universally. I affirm that scoping explicitly here so no future reader
over-reads KPM-primacy onto boss rooms.

**(b) magic_pack trimodal-LOW — 117 timeout non-clears.** gamora's re-point surfaced a NEW finding: magic_pack
is genuinely trimodal (LOW 117 / MID 54 / HIGH 18), with a CLEAN kit tripartition (13/4/4 distinct kits,
ZERO LOW-HIGH overlap). The 117 LOW-mode cells are timeout partial-clears (~17-22 of 24 mobs killed at the
120s cap → cannot full-clear). These are a genuine below-floor CONTENT finding, floor-insensitive: they
reject below floor whether the floor is the stale 18.61 or the density-honest 12.52 (they cluster at
~8.7-11, below both). gamora did NOT curve-fit the floor down to admit them, and jack-ryan Gate-2-verified
that call. This stays FLAGGED, carried to R4 parallel to boss_with_adds.

**PASS on condition 3.**

---

## Discipline guards on my own verdict (the moving-goalposts audit)

I am scoring my own amended criterion. The obligation is to be at least as hard on this PASS as I was on the
§4 FAIL. Four honesty checks:

**1. Does the existing data satisfy the amended criterion on its own terms, or am I reaching?** On its own
terms. The 2.4× KPM spread is not a marginal signal dressed up as discrimination — it is wide and the median
sits off both tails. The validity screen is a clean 765/769. The flags are existing machinery, not
aspirational. If any single element were marginal I would say so; none is. **No reach.**

**2. Does the magic_pack re-band (in-band 36→54 for that scenario) materially change the verdict?** It
changes the SURFACE materially in that one scenario (+18 fast-clears admitted; the honest density-anchored
ceiling at 102.86 lands ~1.4 KPM above p90 = anti-curve-fit signature, Gate-2-verified). But it does NOT
change the VERDICT — it strengthens it in the reframe's own direction: the +18 admitted cells are the
HIGH-mode fast-clears, which are precisely the live clear-speed discrimination signal the amended criterion
treats as the measurement. A caster deleting trash fast is the power fantasy, admitted without mob-HP
inflation. The re-band moves the surface TOWARD the reframe's expectation, not against it. Materially
strengthens, does not overturn.

**3. Discipline #12 — does anything in the existing data CONTRADICT the reframe's expectation?** I looked for
this specifically, because smoothing over a contradiction is the failure mode. One tension, surfaced not
smoothed: the magic_pack trimodal-LOW 117 is a LARGER non-viability cohort than I had front-of-mind when I
wrote the reframe (§5 flagged magic_pack for audit but framed its rejects as a band-staleness question; the
audit revealed 117 of them are genuine timeout non-clears, a real content hole, not a band artifact). This
does NOT contradict the reframe — the reframe's whole architecture is "non-viability gets FLAGGED, not
curve-fit" and that is exactly what happened. But it does mean the endgame-BC content surface has MORE
genuine non-viability than the clean 765/769 headline suggests: two scenarios (boss_with_adds, magic_pack)
carry real content holes. That is honest content signal the reframe is designed to preserve, and it is
preserved. I flag it loudly here rather than letting the 765/769 number read as "surface is clean." The
CLEAN cells are clean; the FLAGGED scenarios are genuinely broken content and R4 inherits them.

**4. What would have made this a FAIL (so the PASS is falsifiable)?** Explicitly:
- **KPM spread at or near point-mass** (p10≈med≈p90, e.g. under ~1.2×). The instrument would be dead and
  the amended criterion FAILS by its own falsifier. It came back at 2.4×. Did not fire.
- **Non-viability silently gating emission** — if a zero-kill or timeout cell read as a floor-fail with no
  emitted flag, the reframe's integrity would collapse (it would be curve-fitting non-viability into silence).
  gamora + jack-ryan confirmed the flags emit. Did not fire.
- **magic_pack re-band curve-fitting the floor down to green the 117 timeouts.** If gamora had lowered the
  floor to admit the timeout non-clears as "in-band," that would be Goodharting the surface clean and I would
  FAIL it on Discipline rider-4. She did the opposite — floor is density-honest, the 117 stay below-floor.
  Did not fire.
- **A finding deleted between §4 and here.** If boss_with_adds or the magic_pack hole had quietly dropped off
  the ledger, FAIL. Both are carried, FLAGGED, verified present. Did not fire.

None of the four fired. The PASS is falsifiable and it clears.

---

## What survives to R4

1. **The chain unblocks.** step-4-bis PASSES; R4 / Leg-C (summoner campaign) fires per reframe §6.4.
2. **boss_with_adds carried as a FLAGGED content-lane scenario** — 117/189 kits kill zero mobs. Must NOT
   silently gate Leg-C. Open fork (jack-ryan Condition 2): KPM may be the wrong observable for boss rooms;
   boss shells already gate on survival-viability, not KPM. Content read + gamora data pull decides pre-/post-R4
   sequencing (KR's call).
3. **magic_pack trimodal-LOW carried as a FLAGGED content-lane scenario** — 117 timeout non-clears, genuine
   below-floor content hole (floor-insensitive). Parallel to boss_with_adds. Band re-derived to
   (12.52, 102.86); the re-band does not admit these — they are real content non-viability, not a band artifact.
4. **Non-blocking watch (from Gate-2):** magic_pack ceiling margin is thin (~1.4 KPM above p90, coarse
   brisk-sweep estimate). Revisit ONLY if magic_pack rails at 102.86 on a future run. Not a gate.
5. **KPM-primacy is a CLEAR-shell statement, not universal.** R4 and any future reader must not over-read
   "tier-1 KPM = THE measurement" onto boss rooms, which gate on the survival-viability bit.

The scoreboard R4 inherits: the CLEAN spatial surface is accepted (765/769 viable, KPM discrimination live);
TWO scenarios (boss_with_adds, magic_pack) carry genuine content non-viability, FLAGGED and preserved. R4
fires on the clean surface; the two flagged scenarios ride alongside as content-lane work, not emission gates.

---

**Sign-off:** gandalf, 2026-07-08. **VERDICT: PASS under the amended criterion.** Falsifier (KPM
point-mass) checked and does not fire (2.4× spread live). Chain CLEARED to proceed to R4. Two content-lane
non-viability findings carried forward FLAGGED. Anchors: reframe note §3/§4/§6, jack-ryan reframe-review +
Gate-2 findings, gamora cert-repoint note, run-state tail (765/769 @ 0.995 ceil-fraction; KPM spread
22.3/31.9/53.8 open, 23.3/35.2/57.1 choke).
