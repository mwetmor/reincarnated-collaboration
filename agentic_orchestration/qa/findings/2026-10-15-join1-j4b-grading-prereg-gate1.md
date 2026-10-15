# Finding — 2026-10-15 — JOIN-1 J4b GRADING PREREG, Gate-1

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: three WARNs fold into PREREG-ADDENDUM-A, or a corrigendum, **before the first graded run**. Nothing here requires a design change.)
**Target:** engine `32d3325c`, `src/reincarnated/simulation/math/join1-j4b-grading-prereg-2026-10-15.md` (no graded run yet). It consolidates the design `f72316b7`, ADDENDA 1–11, the build prereg `ced19966`, and B0-N (`301e35c1`; PASS, collab `5df853795`).
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 2, 3, 5 · Disciplines #10, #12

## ADDENDA 10 and 11 (not separately delta-gated): ACCEPTED here
- **ADDENDUM-10 (`c9a6cd47`)** folds my `d202525b8` correctly:
  - R-5: the FA trigger in S21's `on_struck`, ordered FA → Oculus → thorns;
  - R-4: absorb on direct rows only, via S13's DoT mark, with `G-ABS-DOT`;
  - R-1…R-3, with R-2 covering S22 (teleport, then lane) and R-3 covering S21/S23 with the latency printed;
  - INFO-1 and INFO-4.
  
  It also folds C-14 stage 4's sourced corrections:
  - monster chill = `coldeffect`, with a game-pair −33 by tier (JUDGED; boss values as a sensitivity), floors 25 % / 15 %, `floor(len/4)`;
  - absorb **heals**, through the existing end-of-tick `_death_check_then_heal` with no new `_cons_add` (it cannot rescue a lethal tick; declared);
  - thorns are physical, mitigated and give no on-kill credit;
  - a blocked strike gives no Oculus proc (sourced);
  - the freeze rounding;
  - champions CHILLED (conductor ruling; frozen as the sensitivity).
  
  **All sound.**
- **ADDENDUM-11 (`9de6f9ad`): the tier correction is RIGHT, and it is a material #12 shift.**
  - The oracle's own `threat_tier` against `monsterClassification` agrees **90/90**: GD **Champion → trash**, **Boss → nemesis**. All 575 attacker records and P′'s 233 now resolve.
  - **Consequence, to be named on the fidelity table:** 112 GD-Champion records move from the D2 champion AR table (+49 % AR, mlvl 87) to the **normal** table, which lowers intake CtH. Under FA they are now **FROZEN rather than chilled**, which means more freezes. **Both effects favour her survival** relative to the pre-correction design.

## WARN-1 — The OBS-1 timeout clause for joined kits is missing from the "runs" gate and from M-b

My `2c5413335` (routed item 6) and ADDENDUM-1 § F agreed a **JOIN-only** clause: a joined kit's wave `timeout` is a **valid terminal**, not `harness_error:TruncatedSalt`. It was agreed under three conditions:
1. a negative control showing that the Warlord's GD path still classes a timeout as `TruncatedSalt`;
2. the referent's tick cap is unchanged;
3. M-b counts a timed-out wave as **reached, not cleared**.

§ 1 says only "executes to a terminal state without exception". If her timed-out cells are emitted as harness errors, the run fails validity for a reason the design already settled.

*Action:* state the clause, its negative control and M-b's timed-out rule in the prereg, and list `timeout` among her valid terminals.

## WARN-2 — The comparator's validity at the J4b pins must be SHOWN, not assumed

The comparator is the G-D3 re-emission at rulebook **`06b9bdb3` / pack v3**. Since then:
- the J3b/J3d pins have moved (`d5384b4b` → `3eefaa2e`);
- **pack v4 (`dee7cf58`) is pinned**;
- the port has moved to J4b's runtime digest.

Her runs are on the J4b port. My J3a close-out condition (`2a0573f8c`) was that the G-D4 row is re-emitted whenever a rulebook change touches the `gd-decoded` path. The likely answer is "unchanged": row 36 is inert at h = 1, the J3d forms are installed on no row, `d2/` is not imported by `__init__`, and the S-sites are inert under the Warlord. **It still has to be demonstrated.**

*Action, before the first graded run, one of:*
- **(a)** re-emit `JOIN[warlord, gd-decoded @ 196]` (25 cells) at the J4b engine pins **and** on the J4b port digest, each predicted **7/7 FILE-equal** to `4c30b0d64`'s G-grains;
- **(b)** an identity proof: P-J2-9 30/30 at pack v4 for every operand the `gd-decoded` path reads, a digest of the `gd-decoded`-reachable rulebook files unchanged since `06b9bdb3`, **and** the port leg of (a).

**The port leg cannot be argued away.** The J4b change set's own gate checks the `gd` golden master, not `gd-decoded`. A failure is a HALT (WARN-3).

## WARN-3 — The halts are right, but three are missing

§ 8's halts are correct: a "runs" FAIL; an ORACLE break (to Matt); a negative control failing its own row identity; disk < 20 GiB; and strict reversal recorded FALSE (a recording rule, not a halt). Add:
1. **A row-replay mismatch.** The engine forms' recomputation of any port-logged row differs. That is the cross-mirror basis of a port-emitted kit (M-1), so a mismatch must **HALT grading**, not merely be counted.
2. **A comparator-validity failure** (WARN-2).
3. **Run invalidity → NO VERDICT** (not FALSE): HEAD moved mid-run, instrument unpinned, foreign reads > 0, or join records failing. This is the J3a/J3b validity block, stated for her runs.

## Checks requested

**Completeness against my prior gates: COMPLETE apart from WARN-1 and these listing items.**
- Present:
  - NC-ANCHOR;
  - the ×1.67 count rule, with T-only for ×1.235;
  - T censored at H;
  - FALSE only on strict reversal;
  - the 0.8 route;
  - every r_HP / r_DMG / yard / FA / ES / Warmth / potion / ECDF / bleeding / no-charm sensitivity;
  - the WARN-1 drain bounds (16a/16b);
  - the RI format;
  - the fidelity lines: rebuff, rate leg, R-2 order, absorb timing, potion timing, moving fraction;
  - the per-family registry.
- *INFO-1, add to the print and instrument lists:*
  - (a) the **R-3 latency** per cell (ADDENDUM-10 promises it);
  - (b) the **lock-log precedence gate** (0 violations; ADDENDUM-4 § 3) and the `on_struck` draw and trigger gates;
  - (c) the **family-keyed killability test** (INFO-9 of `2c5413335`);
  - (d) the **construction- vs landed-weighted CtH print** (ADDENDUM-6 § 2.4);
  - (e) the **bind-classifier `physical_contact` counts and lists** as the number of record;
  - (f) state **M-c = applied, HP-capped** damage per world tick.
- *INFO-2:* the r_HP ordering on M-c (R2 ≤ R1 ≤ non-ladder, ≥ ×1.33 apart) can **plateau** once wave clear is spawn-limited. Bodies die on arrival, and applied-per-tick then tracks the spawn schedule, so a trajectory-noise **strict reversal** becomes possible between near-saturated arms. Either register it on a non-saturating statistic (e.g. Σ applied damage per world tick over waves neither arm clears within the first spawn interval), or keep it and accept the risk explicitly.

**Deferring the two directions (the intake-vs-(life + belt) print with the 0.8 rule, and the M-c closed form) to PREREG-ADDENDUM-A: ACCEPTABLE, on three conditions:**
1. ADDENDUM-A is committed **ALONE, before any graded run**, as stated;
2. its provenance lists its inputs and states that **no emission of her kit was read**: no graded output, and no margin-relevant output of any build or control run of her profile;
3. **my delta gate on ADDENDUM-A** precedes the first run.

A direction computed after seeing her emissions would be a fit, not a prediction.

**RI handling: SOUND.**
- "N ACTIVE + M RI (named) / 23", where ACTIVE requires **non-zero reach AND a passing NC**.
- Predicted 22 + 1 (row 22).
- Candidates are named: 9, the freeze→chill clause of 24, the Resilient-bleed clause of 26, and 32.
- Clause-level RIs do not demote a reached row.
- Row 22's forced-landing unit control (8 families × 3 settings, fail-first registry deletion) shows the setting is implemented without folding it into ACTIVE.

**Comparator choice: RIGHT IN KIND.** `JOIN[warlord, gd-decoded @ 196]` (KP-386 / G-D4) at the same X (her lane is a frame timeline, X = 196, so no re-quantisation). The values recompute from `4c30b0d64`: **17/25, Σ ticks 113,051, Σ intake 21.13 M**. **Its validity at the J4b pins is WARN-2.**

## Action
- [ ] gamora: a corrigendum or ADDENDUM-A text folding WARN-1 (the timeout clause plus its NC and M-b rule), WARN-3 (three halts), INFO-1 (prints) and INFO-2 (the M-c plateau choice). Then ADDENDUM-A itself, alone, under the three conditions.
- [ ] gamora / drax: WARN-2's comparator proof, (a) or (b), with the port leg mandatory.
- [ ] jack-ryan: a delta gate on ADDENDUM-A, and on the WARN-2 evidence.
- [ ] Matt: none.

## References
- engine `32d3325c`, `c9a6cd47` (ADDENDUM-10), `9de6f9ad` (ADDENDUM-11), `ced19966`, `301e35c1`; collab `4c30b0d64` (comparator), `2a0573f8c` (G-D4 re-emission condition), `2c5413335` (OBS-1 clause conditions)
