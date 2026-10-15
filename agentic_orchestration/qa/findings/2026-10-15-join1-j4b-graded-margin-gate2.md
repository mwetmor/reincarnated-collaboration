# Finding — 2026-10-15 — JOIN-1 J4b GRADED MARGIN Gate-2

**Reviewer:** jack-ryan
**Severity:** **BLOCK** (1 BLOCK / 2 WARN / 5 INFO). The arithmetic is exact. One registered NO-VERDICT check was never evaluated, so the PRIMARY cannot be printed TRUE yet.
**Target:** collab `aaa1f6a3f` (`agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-GRADED-MARGIN/`); grader engine `e7939e40` (fail-first `de0233bb`); grains = gb-fix (pins `1a17de52…`; G1–G7 `b77414ef…`)
**Developers:** gamora (grade), drax (grains)
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10, #12; prereg § 8; ADDENDUM-A § F + CORR-1 § 2 + CORR-2 §§ 2–3; my delta `2026-10-15-join1-j4b-addendum-a-corrigenda-delta.md`

## (1) M-c and pairing, re-derived from the raw grains with my own script: EXACT
- **Inputs read:** GO (`applied`, every source, his summons included), G7 (`n_ticks` for waves 159 and 160), G5.
- **Pairing:** the pairing rule held. Both kits reached wave 159 in all 25 cells, so none were dropped.
- **Result:** **25 pairs, 25/0/0, p = 5.96e-8**. Paired totals **3,069,651.0 vs 2,023,172.6** (×1.5172). Per-cell ratio min / median / max **1.085 / 1.548 / 2.032**. His no-summons total is 2,022,944.2, also 25/0.
- **Agreement with `per_cell.json`:** within about 1e-14 relative. The only difference is summation order (fsum vs a running sum).
- **Integrity checks:**
  - every GO row's wave tag sits inside its G7 window (0 mismatches);
  - `Σ ticks` equals the window spans;
  - there are 0 negative `applied` values;
  - there are 0 GO rows outside the target's GB span.
- **Grade path:** I also ran the `e7939e40` `grade()` on the 25-cell sets I assembled. It gives the same M-c verdict and totals, and runs / OBS-1 pass 25/25 on both arms.

## (2) The instrument fix: ACCEPTED
- **Fail-first:** I reproduced the new test in scratch. It is **RED at `de0233bb` (1 failed / 34 passed)** and **GREEN at `e7939e40` (35/35)**.
- **Scope:** the diff touches only the `offered` and `offered_per_tick` lines. They are computed **after** `M_c_waves` and do not touch `applied`.
- **No figure could be read before the fix.** I ran the pre-fix grader on the released set and it **raises TypeError** inside `cell_metrics` before `grade()` returns anything.
- **Timestamps:** both commits are stamped 18:47:07, in the same second, so the order is shown by their content, not by time. The result commit is 18:50:21.

## (3) The gates listed PASS
- These hold, re-verified on these exact grains (in my `39433b107` and here):
  - runs and OBS-1;
  - comparator legs: engine 7/7, port `53b8a7f` 7/7 on all 5 arms, plus null-path inertness;
  - row replay (her 25 cells, every class; his 173,430 GH rows);
  - effect gates;
  - DoT conservation;
  - completeness under the POST-HOC rule.
- **BLOCK-1 — a registered gate is missing from the list.** ADDENDUM-A CORR-1 § 2, as restated by CORR-2 § 2, defines the **leech-reconciled HP-chain identity**: asserted per cell, and **a failure is NO VERDICT**. CORR-2 § 3 adds: *"Her emitter must report the leech heal on enemy bodies … or the identity cannot close and her cell is NO VERDICT."* I carried that to drax in my corrigenda delta (Action: emit the leech heal from `mut_fold.tel`). The graded output neither evaluates nor names this identity.
  - **His arm: computable, and PASS by my recompute.** Σ applied = Σ (hp_initial − hp_final) [GO-BODIES] + `leech_heal_hp` [JOIN `go` block] holds in **25/25 cells, worst 6.0e-14**. `n_off_ledger` is 0 and the port's own `identity_pass` is true 25/25.
  - **Her arm: NOT computable from the released set.**
    - Her cells have no GO-BODIES, no `go` identity block and no leech-heal telemetry.
    - Her chain from J4B-ROWS packets shows **0 off-ledger falls over 24,295 packets**, so clause 1 holds.
    - It also shows **18.80 M of visible heal (363 rises)** with no independent heal total to reconcile it against (clauses 2 and 3).
    - Her G3 reports `n_leech_events = 0` in every cell, even though monsters on her arm visibly heal. That is exactly the kind of unexplained mechanism the identity exists to catch.
  - **Status by the registration:** her cells are NO VERDICT on the identity, so **the PRIMARY M-c is NO VERDICT, not TRUE, until the identity is run.**
  - **Magnitude:** this is not a likely reversal. Stripping **all** her visible heal in {159, 160} from her applied still leaves a minimum ratio of **1.059**. Stripping all her intake gives 1.074. These bounds are printed for context only; they do not discharge the gate.
  - **Path forward:**
    - **drax:** emit, observe-only, her per-cell `leech_heal_hp` / `leech_overheal_hp` from `fight.mut_fold.tel`, plus GO-BODIES. The emitter already has this block at `kc2p_join2_emit.gd:754–797`, used for his arm. Do a labelled rerun of her 25 cells. **Inertness:** every graded grain must be sha-equal to the gb-fix pins. Explain `n_leech_events = 0` against the visible heal.
    - **gamora:** evaluate CORR-2 § 2 clauses 1–3 on both arms, then re-issue. The M-c figures cannot move, because the identity does not touch `applied`.

## (4) The NO VERDICT list
| Item | Status |
|---|---|
| NC-J4b-ANCHOR (raw arm) | truly unrun |
| r_DMG ×97.06 / ×46.98 arms and orderings | truly unrun |
| Offered per tick R2 ≤ R1 ≤ non-ladder | truly unrun |
| Per-row NCs and fraction (b) | truly unrun |
| ADDENDUM-B off/off (her flinch-off arm) | truly unrun |
| **Fraction (a), rows mapped / 32** | **wrongly left NO VERDICT** (INFO-1) |

Fraction (a) is a census / implementation property under prereg § 2. It is computable from the census and pack v5.1 at their pinned commits, without grains.

NC-ANCHOR is registered "Unconditional", so its non-run needs a **recorded disposition** (deferred or declined), not silence (INFO-3).

## (5) KP-427
- **WARN-1, verified.** `non_health_by_type` is empty in **25/25** of her cells, so her drain bias is **0**. His S16b shows **14 routings over 11 cells**. The engine-side 16a recorder was never built, which is correctly NO VERDICT.
- **WARN-2, verified.** `move_refused_cast` 28,765; `resilient_bleed_noop` 62; her S12 = **10** landings, matching replay control 10/10.
- **WARN-2 (mine):** row 22 is registered "**Predicted RI**". Ten landings contradict that prediction, so it must be recorded **FALSE AS PRE-STATED** under prereg § 8, not "RI does not hold". Fraction (b)'s predicted form "22 ACTIVE + 1 RI" falls with it. It stays NO VERDICT pending the NCs.

## (6) Labels
- **WARN-1:** the labels appear **only in `README.md`**. `grade_report.json`, `per_cell.json` and `sensitivities.json` carry no POST-HOC, CORR-4 FALSE-AS-PRE-STATED or probe-limb label.
- `grade_report.json` also prints **`"verdict": "TRUE"` on UN-PREDICTED metrics** (M-d, T, M-b), and T is computed with **H = 1e9**, which is not stated.
- **Fix:** add a `labels` block to every JSON. Print UN-PREDICTED metrics as "UN-PREDICTED (printed)". State H.

## INFO
- **INFO-1:** compute fraction (a) from the census / pack.
- **INFO-2:** the instrument fix is accepted (§ 2).
- **INFO-3:** give NC-ANCHOR and the other unrun registered arms a recorded disposition.
- **INFO-4:** his Leeching heals put **54.6 M (1.33 %)** more `applied` than HP lost on his side. That is by design (CORR-2 § 3) and conservative for her claim.
- **INFO-5:** the decimals agree to about 1e-14 (summation order). The verdict is unaffected.

## Action
- [ ] drax: emit her leech-heal telemetry and GO-BODIES with pinned inertness (BLOCK-1). Explain her `n_leech_events = 0`.
- [ ] gamora: evaluate the identity on both arms and re-issue (BLOCK-1). Fix WARN-1 and WARN-2, and INFO-1 and INFO-3.
- [ ] Matt: none, unless BLOCK-1 stays unresolved, or the conductor proposes to waive a registered check. That would need Matt.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/join1-j4b-grading-prereg-2026-10-15{,-ADDENDUM-A,-ADDENDUM-A-CORRIGENDUM-1,-ADDENDUM-A-CORRIGENDUM-2,-PREREG-ADDENDUM-B,-PREREG-ADDENDUM-C}.md`
- grains `/Users/admin/Games/join3c-bulk/gb-fix/arms/{her,his}/`; `reincarnated-godot/kc2_play/tools/kc2p_join2_emit.gd`; `reincarnated-godot/evidence/join1/j4b-hook/comparator-port/`
