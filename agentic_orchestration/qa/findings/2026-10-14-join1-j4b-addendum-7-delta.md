# Finding — 2026-10-14 — JOIN-1 J4b ADDENDUM-7 delta: the last check before the Matt ruling sheet

**Reviewer:** jack-ryan
**Severity:** WARN (verdict: **GO for the Matt ruling sheet**, since the 19-site table is unchanged; the design is **GO-WITH-AMENDMENTS**, with 1 WARN and 3 INFO before the prereg)
**Target:** engine `19e31ec1` (ADDENDUM-7), against my ADDENDUM-6 delta `146a3a84f`. Conductor KP-434 (Warmth default back to 18 hard points, 378 %) is noted.
**Developer:** gamora · conductor gandalf
**Principles applied:** 1, 3, 4, 5 · Disciplines #10, #12

## The site table: CONFIRMED UNCHANGED (19 sites)

Every ADDENDUM-7 change alters a **value**, never a code path:
- the ECDF weighting and the tier tables → `anchor_ar_eq_table` (S17 reads integers);
- Warmth / Magefist → the KIT operands of S03's one regen function;
- the orderings → predictions.

So **S01–S15, S16b and S17–S19 (19 port sites; S16a engine-side)** stand as ADDENDUM-6 § 5 states them.

**WARN-2 of `146a3a84f` is the conductor's sheet's to carry:** the booking-census row additions for S04–S06 / S10, whether S16b needs an emitter unfreeze, and the KP-312 condition set including the windowed `.app` self-test. The sheet may go to Matt with those three items on it.

## Checks of gamora's calls

**(1) ECDF weighted on P′ = 243 (P = 248 minus the 5 depth-2 pets), with 248 as a sensitivity: ACCEPTED.**
- KP-381 itself labels the 5 depth-2 pets structurally unspawnable ("only line-up actors cast", `run.py:3485`), so excluding them is the same no-phantom-rows rule WARN-1 asked for.
- The table stays total. Non-P′ rows take `u` against the P′ sample, with a clamp-and-count outside its support.
- Tier resolution with `AttackerTierUnresolved` still covers every row.
- The landed-vs-construction print now compares like with like.

**(2) Tier pairing: champion-hero on the stage-6 champion transform: ACCEPTED.**
- It is labelled a **lower bound**: stage 6 does not re-look-up AR at alvl + 2.
- Pairing heroes with plain uniques would rank them below D2's own champions.

**(3) Boss/nemesis on unique + Extra Strong, 84 [83–87], mlvl 88: ACCEPTED as a JUDGED arm, but not as the D2-faithful marginal. See WARN-1.**
- The H1 extension checks out. I re-ran H1 at mlvl 88 over stage 7's 93 contact attacks for both `ar_unique` and `ar_unique_extra_strong`: **186 / 186 reproduce.** The grid is now 576 rows, with its perturbed-row negative control.

**(4) WARN-3: DISCHARGED.**
- The survival-**count** ordering is registered only for USE-WEIGHTED ≤ PRIMARY (×1.673).
- PRIMARY vs WORST-CASE (×1.235) is registered **only** on paired Σ survival ticks (the death tick, or the window end).
- **FALSE iff the paired total strictly reverses**; the sign test is reported, not used as the pass rule.
- Every pair under ×1.2 is un-ordered. The mean ÷ mean R2/R3/R4 values (76.56 / 72.38 / 77.93) are correctly un-ordered against PRIMARY (78.58).

**(5) The contact counting key: ACCEPTED.**
- The three keys and their counts are reconciled (567 / 280 / 21 at actor + owner + … + tree_index; my 567 / 262 / 23 at record + … + skill).
- Weapon-damage projectiles are declared contact, and add 0 entries.
- **The bind classifier's digested per-runtime-slot output is the number of record**, superseding every hand recount, including mine. That is the right resolution.

**(6) Regen: DISCHARGED.**
- `manarecovery` (stat 26) is 0 by construction, since no 1.13 property code targets it.
- Magefist's `regen-mana` is `manarecoverybonus` (stat 27), entering the multiplier.
- With `max_256 ≥ 3000`, the unified function is **byte-identical for her**.

**(7) Warmth (KP-434 reversal, folded after this verdict):**
- **default = 18 hard points**: slvl 30, `ln12` = 30 + 12·29 = **378 %**;
- **sensitivities**: 1 point (slvl 13, 174 %) and 0 points (0 %; D2 +skills give nothing to a skill with no hard point);
- the registered arithmetic ordering 0 ≤ 1 ≤ 18 on mana-bound casts/s stands;
- the Meteor-starvation and realised-rotation numbers are re-computed by the adapter **before** any run (ADDENDUM-3 condition 5).

## WARN-1 — Extra Strong is a RANDOM unique roll. "unique + ES for every boss" is an upper arm, not the D2 marginal

Stage 7's own U2 says Extra Strong applies **"if rolled"**. Hell uniques draw random bonus mods, and Extra Strong is one possible draw; superuniques get it only where SuperUniques.txt fixes it (e.g. Mod 5 on the Grand Vizier and Lord De Seis). Pairing **every** GD boss and nemesis with the ES distribution therefore assumes the roll always lands. The basis given, "a boss tier must sit above champion", is a rank judgement, not a D2 law. Plain uniques (76 [74–80]) do hit less than D2 champions (≥ 81).

*Action (pre-prereg; no site change):*
- label boss + nemesis = unique + ES as **JUDGED (upper arm)**;
- either ask legolas for **P(Extra Strong)** in the Hell unique mod draw and make the main table the **mixture** `P·ES + (1−P)·plain` (a quantile of the mixed sample, n = 64 × 2 weighted), or keep ES as main with the label and the plain-unique arm printed beside it (already a sensitivity);
- state which on the fidelity table.

## INFO
- **INFO-1:** make the `physical_contact` per-slot classification an **engine-emitted, digested pack row** that the port reads (the `anchor_ar_eq_table` pattern), not a port-side bind computation. The "lists of record" then add no port report key, and S17 never re-derives them. No site change.
- **INFO-2:** Σ survival ticks for a cell that **survives** in both arms reduces to the window-end tick, which moves with clear speed (trajectory noise) rather than with life. Either print the metric split (cells where either arm dies, vs both-survive cells), or define survival ticks as ticks alive **until death, censored at the window end**. The registered direction is unaffected.
- **INFO-3:** with Warmth at 18 points (KP-434), the "17 freed points go to no modelled skill" line in § 6 is moot. Drop it in the fold, so the record does not carry a dead allocation note.

## Action
- [ ] conductor: send the ruling sheet to Matt with the 19 sites and `146a3a84f` WARN-2's three items.
- [ ] gamora: fold KP-434 (Warmth 18), WARN-1 (ES label or mixture) and INFO-1…3 before the prereg.
- [ ] legolas (if the mixture is chosen): P(Extra Strong) for Hell uniques.
- [ ] Matt: the KP-312 ruling.

## References
- engine `19e31ec1`, `c5f66a4e`; collab `agentic_orchestration/legolas/research/2026-10-14-join1-c13-enemy-anchor/d2_unique_ar_r1.json` (stage 7; U1–U3; H1 re-run above), `d2_hit_chance_r1.json` — read-only
