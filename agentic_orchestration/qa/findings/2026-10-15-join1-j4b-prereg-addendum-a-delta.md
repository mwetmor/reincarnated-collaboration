# Finding — 2026-10-15 — JOIN-1 J4b PREREG-ADDENDUM-A, delta gate

**Reviewer:** jack-ryan
**Severity:** WARN (verdict **GO-WITH-AMENDMENTS**: two WARNs settle before the first graded run. M-a's non-registration, the halts, the timeout clause and the six prints are accepted.)
**Target:** engine `343ee41e` (ADDENDUM-A), `5286811d` (instrument), `1c88cd4c` → `85dd6058` (grader); collab `d11ce3a12` (`prereg_a.json`); against my Gate-1 `09f080754`
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 2, 5 · Disciplines #10, #12

## Is it a prediction, not a fit? **YES**
- **The instrument's read set**, which I read: `gamora_join4b_prereg_a_2026_10_15.py` opens only:
  - the Warlord baseline bulk `gd3-v3-emission-06b9bdb3/emission/{G1, G2, G7}`;
  - C-13 `gd_enemy_quantities.json`;
  - `join2_rulebook.d2.laws`.
  
  Nothing of hers.
- **No emission of her kit can yet exist.** The engine refuses her (`PortOnlyKit`), and the port's J4b change set is not yet landed and gated.
- **The doc was committed before any run**, with the provenance statement.

My three Gate-1 conditions on ADDENDUM-A are met: alone, before any run, no emission read. This gate is the third.

## The grader: SOUND
- `tests/test_join4b_grade.py` **re-run here: 8/8 green** at the current checkout.
- The fail-first commit `1c88cd4c` precedes the grader `85dd6058`.
- It covers:
  - the runs gate (raised / KeyError, non-terminal, missing cells → RUNS FAIL);
  - the OBS-1 truncation negative control, with timeout as a valid terminal, reached not cleared;
  - T censored at H;
  - paired totals with an exact two-sided sign test, FALSE only on strict reversal;
  - the fraction-(b) line and the family registry;
  - **comparator without the offence grain → M-c NO VERDICT** (correct, given WARN-2).

## M-a: NOT REGISTERED in any arm. CORRECT
The deliberately loose upper bound (his packets, pre-mitigation, × (1 − her row-25 resist), ÷ his landed fraction 0.84994; block, absorb and her lower CtH ignored) breaks 0.8 × (life + belt) on **7 / 3 / 32 of 250** cell-waves. The rule requires every wave, so the route correctly registers nothing. "Un-predicted" in all three arms stands.

## WARN-1 — M-c "her ≥ Warlord": an UPPER bound of her rate is compared with his REALISED rate. That cannot by itself support the direction, and saturation is exactly where it fails

`her_capacity_per_tick` = 3.125 casts/s × the single-target applied damage per cast ÷ tps. **It assumes a fresh target for every cast**, so it is an **upper bound** of her realised M-c. Removing splash, burning ground and Static lowers it, but it remains a ceiling.

Comparing her ceiling with his realised rate (`board HP per wave ÷ his mean wave ticks`) shows the ordering is **possible**, not that it holds. ADDENDUM-A's own residual-risk line names the mechanism: **both kits kill bodies only as they arrive.** If his waves are **arrival-limited** (he clears bodies about as fast as they spawn), then her realised rate cannot exceed his by much either. Both converge on the same HP-per-tick of the spawn flow, the paired M-c total becomes a **near-tie**, and a strict reversal is a coin-flip on trajectory noise. That is the J3a lesson on a continuous metric.

The ×2.32 capacity margin protects only waves where **he is kill-limited**.

*Action (pre-run, from his data only, so still a prediction):*
- compute, per wave, the **last-arrival tick** from the trajectory-invariant spawn schedule (step-2b: the roll is fixed by the wave seed) against his wave end tick (G7 `wave_end_tick`);
- **register M-c (her) ≥ (Warlord) only on waves where his post-arrival kill tail is a material share of the wave** (state the share before computing it, e.g. ≥ 25 % of the wave's ticks), and grade the paired total over those waves;
- **if no wave qualifies, M-c is UN-PREDICTED.**

That registers exactly what the capacity argument can carry.

## WARN-2 — Adding an applied-damage grain to the comparator re-emission is an instrument change. Preregister its definition, alone, before the re-emission

The comparator's grains carry no applied-damage grain for his offence (the conductor's note), so the KP-386 instrument has to emit one. **§ E says the re-emission uses the instrument "unmodified", which is now false.**

*Action:* a short corrigendum to ADDENDUM-A, **alone, before the re-emission**, that:
- (a) defines M-c identically for both kits:
  - **HP-capped applied damage on enemy bodies, including enemy pets / summons**, per world tick, over the same tick base;
  - **his sources:** EoR disc, Soulfire, bleed rider, and **whether his own summons' damage counts** (declare it);
  - **her sources:** Fire Ball, Meteor impact, burning ground, Static, thorns;
- (b) requires **the existing G1–G7 byte-identical** (7/7 against `4c30b0d64`), with the new grain additive;
- (c) gives the new grain its own sanity identity: Σ applied damage over a cell equals the Σ HP of bodies killed plus the damage on survivors at the window end, within float tolerance.

Her grain is port-emitted and his engine- or port-emitted, so the **same definition text** must bind both emitters.

## Accepted as folded (my Gate-1 amendments)
- **WARN-1 (timeout):** a valid terminal for the joined kit, reached not cleared, the tick cap unchanged, and the truncation negative control in the grader's fail-first suite.
- **WARN-2 (comparator), option (a):** engine leg plus a **mandatory port leg**, each 7/7 against `4c30b0d64`, with what drax needs listed. Subject to this gate's WARN-2.
- **WARN-3:** row-replay mismatch, comparator failure and run invalidity are **NO VERDICT**, not FALSE.
- **INFO-1:** all six prints (R-3 latency; lock and on_struck gates; family-keyed killability; landed vs construction CtH; classifier counts 2,187 / 800 / 13; M-c HP-capped beside offered).
- **INFO-2:** the r_HP ordering moved to **offered** damage per tick (R2 ≤ R1 ≤ non-ladder), and the M-c ordering is withdrawn. *Note:* offered ∝ r_HP × casts, so this is an **anchor-reach check**, not a behavioural prediction. That is correctly labelled.

## Action
- [ ] gamora: a corrigendum to ADDENDUM-A (alone) folding WARN-1 (the arrival-limited test and the per-wave M-c registration, or un-predicted) and WARN-2 (the M-c definition binding both emitters, existing grains 7/7, the new grain's identity; correct § E's "unmodified").
- [ ] gamora / drax: the comparator re-emission (both legs) under that definition.
- [ ] jack-ryan: a narrow delta on the corrigendum; then the first graded run may proceed.
- [ ] Matt: none.

## References
- engine `343ee41e`, `5286811d` (read set and capacity code, read here), `1c88cd4c`, `85dd6058` (tests re-run 8/8); collab `d11ce3a12`; Warlord bulk `gd3-v3-emission-06b9bdb3` (G7 wave ticks, read-only)
