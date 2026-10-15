# Finding — 2026-10-15 — JOIN-1 J4b PORT-LEGS Gate-2 (graded-verdict readiness)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-NOTES**; 0 WARN / 5 INFO). **The graded J4b margin may be computed under PREREG-ADDENDUM-C (engine `0c97b2ef`)**, with the completeness gate passed under a **POST-HOC** rule.
**Target:** godot `fa0357f`/`16debee`, `e98309c`→`2ca2298`, `c305adb`/`4a1eed0`, `907b41e`/`e459f22`, `6280843`/`166c214`, `3d4fe8f`/`ac0f9b2`/`0be73e2`, `73e340e`/`a381c21`; engine `3c8519b1…0c97b2ef`, `93c40dea`/`a99d2af3`; collab `33eddbc97`, `f1f9eb323`; ledger KP-461…467
**Developers:** drax, gamora
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10; my rulings `826520a1d`, `6d6d0195f`, `90b2e12ad`

## Inputs verified first
- The pin file's sha256 is `1a17de52…`, and **105/105 pins match** the files under `join3c-bulk/gb-fix/arms`.
- Against the `2ca2298` pins, 85 files are identical. The other 20 are **GB + JOIN-PROVENANCE only**.
- G1–G7 are not in the pin file. I compared them **byte for byte** across the `2ca2298` and gb-fix runs: **50/50 identical**.
- The runtime tree digest at HEAD recomputes to `fb49080f…`. **No commit in scope touches `kc2_runtime/`.**
- The mirror census still reads **MATCH 8/8**.

## Answers
**(1) Precondition (P) on the new GB: PASS, 50/50.** My own join over GHR and GH: **0 targets without a span and 0 records outside `[on, off)`**, for pets and roster on both sides. The checks cover her 7,662 GHR and his 173,490 GHR, and every GH row. The old GB, on the same script, still fails: his side has 35,292 records after `off_tick`; her side has 53 after `off_tick`, 2 before `on`, and 204 span-less.

**(2) Completeness form (d): all 63 orphans are TERMINAL.**
- Every orphan sits on its cell's last tick on which any body is alive, and its target dies on that tick: 63/63.
- The 14 non-final orphans are in `survived_window` cells: the board was clear and the clock ran out 2–13 ticks later.
- **Ruling:** the completeness gate is **passable under the POST-HOC rule** (adopted after CORR-4 failed, collab `826520a1d`). CORR-4 stays recorded **FALSE AS PRE-STATED**. Every graded print of this gate carries the POST-HOC label.
- The rule is falsifiable, not true by construction. (P) **failed** on the old GB with real counts. (i) and (ii) are evaluated against spans that are derived from `alive`, independently of the records.

**(3) Effect gates and duty on the new GB: confirmed.**
- Grader `a99d2af3` on all 10 arms: (a) 0, (b) 0, (c) 0, `dying_not_at_death` 0. His `n_dying` is 377.
- **His pet-wave duty, computed independently** (my own loop over the GH lock windows and the new GB): 156 **0.0632**, 157 **0.0542**, 159 **0.0580**, 160 **0.0430**. The other waves are unchanged, and the maximum is 0.063.
- **Nothing registered depends on duty.**
  - PREREG-ADDENDUM-C reads only G7, GO first-hit ticks (roster), GS and `applied`.
  - ADDENDUM-A/B do not reference duty.
  - CORR-2 § 3's duty is a printed diagnostic, and its "near 1" clause is not triggered.

**Independent replays** (my own runs; L-21 built from pack v5.1 `world_l21.json` with `length_frames = 4` world ticks):
- **his side:** 173,430 GH rows replayed through `BodyLock.qualifying_hit` with the tape draw, **0 mismatches**;
- **her side:** engine row replay, every class PASS. The counts are identical to ADDENDUM-C § 3 (tape 31,882 … gh 15,368, gr 1,018, all 0 bad).

**(4) The second HALT in my DoT ruling: acceptable without a new field.** It is **satisfied by construction**, and I verified this in code, at the emitter of the graded run (`e98309c`/`2ca2298`, `kc2p_join2_emit.gd:740–742`) and in the lane (`kc2rb_d2lane.gd:1343–1345`).
- `running_at_end` sums only the live `dots` entries and `dots_once`.
- A form is erased when `rem <= 0`.
- So a nonzero value implies a live DoT. Also, `rate_f > 0` and `rem ≥ 0`, so the value cannot be negative.
- **No rerun is needed.** Add a `live_dots_at_end` field the next time the emitter is touched for another reason.

**(5) The tick field: correction.** My "0–19" was the **label of a 10-tick histogram bucket** (lags 10–19), not an observed maximum. The field was GHR `run_tick` − old GB `off_tick`. On the old grains its true maximum is **11 on his side and 7 on hers**, which agrees with drax's 0–11.

**(6) Today's FALSE-AS-PRE-STATED limbs: none is a defect disguised as a prediction error.**

| Limb | Cause, checked against the evidence |
|---|---|
| PROBE-1 S12 (9 vs 8) | The rows are 8 forced (ticks 100–107, d2-strict) plus 1 natural Stun at tick 1108 in the perturbed fight. 2.0999999 s gives `ceil(25·s)` = 53 f, under the 250 f cap, so the row is lawful. The natural run has 0 rows. The grader keyed limbs by family, which was disclosed; PROBE-2 counts by tick and passed. |
| Freeze (iv) (13 of 55 missing) | **13/13** have exactly one GH row: frozen, no flinch, `d ≥ H`. They were killed in the tick they were frozen, before any mover entry, so there is no movement to observe. |
| S16b (4) (4050 vs 2000) | Limb (5) shows the export **equals the sealed booking**. The 2.025 factor is upstream sealed fold behaviour. **S16b has 0 natural reach in all 25 graded cells** (no `J4B-S16b` counter), so it has **no graded impact** (INFO-2). |
| GB fail-first count | Her 2 before-`on` records were not pre-stated. I had seen the same 2. A fail-first that fails in more ways than predicted is not a defect. |
| GB (vi) (178 + 25) | Reproduced exactly from GB and GF: 24 were frozen at every mover entry after their spawn tick, and 1 was flinch-locked (`[907, 911)` covers 907–909). Diagnosis (KP-465): the old GB was blind to pets that skip the mover under S26 / FREEZE. That is an emitter-definition defect, now fixed observe-only. |

**(7) Inertness of `3d4fe8f` (and `73e340e`) on the graded grains: TRUE.**
- The gb-fix run, made after both emitter changes, reproduced every graded grain **byte-identically**: G1–G7 by `cmp`; GO, GH, GHR, GR, GM, GC, GO-BODIES and J4B-ROWS by pin. Only GB and provenance changed.
- The freeze run (GF on) has 60/60 non-provenance pins equal to `2ca2298`.

## Notes (INFO)
- **INFO-1.** The graded run must name its grain set. Use the gb-fix grains for every gate that reads GB (completeness, gate (b), duty). The registered metrics are identical on either set. Pin G1–G7 in the graded output, since drax's pin file omits them.
- **INFO-2.** The S16b 2.025 fold factor is unexplained. Diagnose it before any profile with natural non-health rows is graded.
- **INFO-3.** The POST-HOC label and CORR-4's FALSE record travel with every graded print.
- **INFO-4.** The tag `…-j4b2s26` push still waits on Matt's windowed self-test (KP-459). This gate does not change that.
- **INFO-5 (disclosure).** During this review I accidentally copied grader `a99d2af3` into the engine's `simulation/scripts/` as an untracked file. I moved it to my scratchpad within seconds with `mv`, never `rm`. It was never staged, and the engine tree is clean.

## Action
- [ ] gamora: compute the graded margin per ADDENDUM-C, following INFO-1 and INFO-3.
- [ ] drax: INFO-2 (diagnose the S16b fold factor); add `live_dots_at_end` at the next emitter touch.
- [ ] Matt: the windowed self-test (KP-459). Nothing else is needed.

## References
- `reincarnated-godot/evidence/join1/j4b-hook/{arms-v51,gb-fix,d2kit-probe,d2kit-probe2,n4-pets,n4-freeze,s16b-force}/`
- grains `/Users/admin/Games/join3c-bulk/{arms-v51,gb-fix/arms,n4-freeze}/`; tapes `/Users/admin/Games/join3a-bulk-evidence/j4b-tapes-4e6ed5b3`
- engine `gamora_join4b_grade.py@a99d2af3`, `gamora_join4b_row_replay_2026_10_15.py`, `join1-j4b-grading-prereg-2026-10-15-PREREG-ADDENDUM-C.md`
- collab `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-{arms-v51-engine-checks,gbfix-completeness}/`
