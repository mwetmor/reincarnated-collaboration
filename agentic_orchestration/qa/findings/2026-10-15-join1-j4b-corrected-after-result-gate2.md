# Finding — 2026-10-15 — JOIN-1 J4b CORRECTED-AFTER-RESULT primary (car2) Gate-2

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-NOTES**; 0 WARN / 5 INFO). The CORRECTED-AFTER-RESULT figure may be printed **beside** `aaa1f6a3f`, which stays the result of record.
**Target:** gamora's re-grade at collab `e349130fb`. drax's car2 at godot `98aeae6` (pins `4bbea4a5…`, 75 files). Lane: `da95cb2`, `145bb57`, fail-first `ae78c16`; KP-487 `fbefa3a` / `8443db2`, CARRY `043bf82`. Corrigenda at engine `c264e523`, `648e193b`, `c79ea0fd`, `5f637abe`, `38eb0495`.
**Developers:** drax, gamora
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10, #12; PREREG-ADDENDUM-C

## (1) M-c and pairing on car2, re-derived with my own script: EXACT
- **Inputs:** car2 is her arm. His arm is gb-fix flinch-on, unchanged; I checked his per-cell M-c in 25/25 cells.
- **Result:** **25 pairs, 25/0/0, p = 5.96e-8**. Totals **3,097,858.8 vs 2,023,172.6** (×1.5312). Per-cell ratio **1.085 / 1.556 / 2.145**.
- **Against as-graded:** net Δ(her M-c) **+28,207.8**: 9 cells up, 7 down, 9 unchanged. Extremes: W1-NULL|3 at −22,402.8 and W1|3 at +18,297.4.
- **Integrity:** 0 wave-tag mismatches, 0 negative `applied`.
- All of this matches gamora's figures.

## (2) The lane changes are exactly the ruled set
I read the full diff of `kc2rb_d2lane.gd`, `kc2rb_d2_locks.gd` and `kc2p_join2_emit.gd` from `a381c21` (the gb-fix lane) to `98aeae6`. `kc2_runtime/` is untouched.

| Change | Ruling |
|---|---|
| Debit at the **action frame** for all four skills (`DEBIT_AT_ACTION`); nothing on a pre-action interrupt or an invalid point | KP-482 / c264e523 |
| `minmana` floor (`_cost256`); inert, since every cost exceeds 256 | EXT1 § 3 |
| The free cast when mana at the action frame is below cost | EXT1 § 1 (4), M3. **Fires 0 times on car2** |
| No body at the action: Meteor goes to a valid cast-start point (walkable, D2 distance ≤ 100), else no missile, no mana, no delay. Fire Ball goes to the cast-start point | KP-481; KP-484 gap-fill |
| Lock boundary `<` → `<=` (an interrupt on the action frame counts as before the action) | EXT1 § 4 |
| A retired or aborted cast emits its contract row (instrument only; no mana, no missile) | KP-487 (a) |
| An action rebased onto the new wave's unprocessed frame 0 fires at the first processed frame | KP-487 (b) CARRY |
| `--rb-hp-chain` (observe-only); the `--rb-kit-corr481` flag; the `actions` array in J4B-ROWS | instruments |

**Nothing else changed.** On car2's action rows:
- 0 free casts;
- 0 debits away from the action frame;
- 0 spends on an interrupted cast.

**The legacy-flag reproduction is narrow (INFO-1).** It covers **one cell** (W1-NULL/0 at `da95cb2`, `ae78c16` C1). And the `corr481=legacy` flag does **not** gate the `<=` change or CARRY, so the flag cannot reproduce the old lane wherever those bite. I therefore grounded (3) on a divergence analysis instead.

## (3) Every car2 cell departs from gb-fix ONLY through the ruled corrections
**Method.** In my own script, for each of the 25 cells I found the first divergence by tick, between gb-fix and car2, across casts (including preempts), packets, potions and struck rows.

- **23 cells:** the first divergence is a **Super Mana potion drunk later on car2**. Everything before it is identical: casts, packets, potions and struck rows. This is the direct effect of the KP-482 action-frame debit, because the potion trigger (mana below the wanted skill's cost) reads the not-yet-debited mana during the 5-frame cast window.
- **2 cells (M0 s4, M-POL-2-NULL s4):** the first divergence is a **preempt relabel, `after_action` → `before_action`, at frame 166 / tick 217**. That is an interrupt exactly on the action frame, which is EXT1 § 4.
- **No cell** diverges first for any other reason.

**The two boundary cells** (M-POL-2-NULL s2, W1-NULL s4) also diverge first by potion timing; CARRY acts later. Separately I verified drax's B1 claim: car2 differs from the superseded car emission **only in those 2 cells**, across every grain file and J4B-ROWS.

## (4) Gates on car2: PASS, re-run by me
- **Engine row replay** (engine HEAD `38eb0495`, pack v5.1, L-21 at 4 world ticks, tapes of record): **PASS 5/5 arms, every class 0 bad.** tape 34,478 · packet 25,568 · mana 72,304 · cast 8,663 · potion 123 · struck 950 · rebase 225 · control 11 · dot 462 · locks 8,869 · gh 15,474 · gr 1,034 · **action 8,688**. These are identical to gamora's counts.
- **Leech HP-chain identity:** 25/25. Worst clause-2 residual 1.4e-16, 0 off-ledger falls, clause 3 passes 25/25, 0 coverage defects.
- **Effect gates (a)/(b)/(c)/dying:** 0 violations on all 5 arms.
- **DoT conservation:** PASS.
- **Completeness (POST-HOC):** (P) holds; **6 orphans, all TERMINAL.**

## (5) Labels
`grade_report.json` and `per_cell.json` each carry the **9 labels**: CORRECTED-AFTER-RESULT; **NOT CONSERVATIVE**; POST-HOC; CORR-4 FALSE; probe limbs; **Meteor-delay RULED** (car2 only; the OPEN wording is quoted only to say it belongs to `aaa1f6a3f`); row 22 FALSE; KP-485 ×4; KP-490 drops.

The README repeats them. The evidence JSONs (gates, hpchain, replay, dropped) carry none (INFO-3).

## Dropped-Meteor counts (312 vs 289): NOT MATERIAL to the verdict
- **Nothing graded reads either count.** M-c reads only the packets that landed, and no gate uses the counts.
- **Direction.** A dropped delivery lowers her offense, so it cannot help her claim. The drop itself is the existing KP-490 parity behaviour (it was in the gb-fix lane as well), not one of these corrections.
- **Why they cannot reconcile.** Neither figure is a count of record; both are proxies. A Meteor that hits no body emits no packet: on car2, 1,725 Meteors were created and only 593 explosions carry hits. So impacts are not directly observable, and two proxies built that way need not agree cell by cell.
- **What is owed (INFO-2):** an emitted counter (`n_meteor_dropped_boundary`, and Fire Ball / pyre likewise) at the next emitter touch. Until then, cite neither number as a count.

## Notes (INFO)
- **INFO-1:** the legacy reproduction covers one cell and does not gate `<=` or CARRY. The divergence analysis in (3) is the evidence of record.
- **INFO-2:** add the dropped-delivery counters; the 312 / 289 figures stay labelled proxies.
- **INFO-3:** add the label block to the evidence JSONs, for consistency.
- **INFO-4:** the per-skill split of Fire Ball no-body actions is NO VERDICT in this run (counter added afterwards in `f25ee1f`). It does not touch M-c.
- **INFO-5:** per-cell deltas range from −14.7 % to +14.8 %, which is trajectory sensitivity. Only the net and the sign are graded, and **no pair flips** (closest W1-NULL|2 at ×1.085, unchanged).

## Action
- [ ] drax: dropped-delivery counters at the next emitter touch (INFO-2).
- [ ] gamora: labels on the evidence JSONs (INFO-3).
- [ ] Matt: none.

## References
- grains `/Users/admin/Games/join3c-bulk/car2/primary/`, `/Users/admin/Games/join3c-bulk/car/primary/`, `/Users/admin/Games/join3c-bulk/gb-fix/arms/`
- `reincarnated-godot/evidence/join1/j4b-hook/{car-primary,kp481-failfirst,kp487a-failfirst}/`
- `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-CORRECTED-AFTER-RESULT/`
