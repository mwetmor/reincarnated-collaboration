# Finding — 2026-10-15 — JOIN-1 J4b GRADED MARGIN: re-gate after BLOCK-1 (follows `4bf8738a9` / `4959e1100`)

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: **PASS-WITH-NOTES**; BLOCK-1 **RELEASED**; 0 WARN / 5 INFO)
**Target:** her HP-chain rerun at godot `9b49805` (instruments `964cf9a`, fail-first `b824fa3`; pins `de73dfb8…`); identity evaluation at collab `d56403c40`; re-issue at collab `19005de93`. `aaa1f6a3f` stays the result of record.
**Developers:** drax, gamora
**Principles applied:** REVIEW_PROCESS 1, 2, 4; Disciplines #8, #10, #12; ADDENDUM-A CORR-1 § 2 / CORR-2 §§ 2–3; prereg §§ 2, 8

## Inputs
- **Pins:** 75/75 match the files under `join3c-bulk/hpchain`.
- **Against the gb-fix pins:** GO, GH, GHR, GR, GC, GM, GB and all 25 J4B-ROWS files are **sha-equal (60 files)**. Only JOIN-PROVENANCE differs, and GO-BODIES / HPCHAIN are new.
- **Her G1–G7:** **35/35 byte-identical** to gb-fix by `cmp`.
- **Conclusion:** the graded inputs are unchanged.

## Her identity, re-derived with my own script
Inputs: GO `applied`, GO-BODIES, HPCHAIN `leech_heal_hp`, and the J4B-ROWS packet chain.

| Clause (CORR-2 § 2) | Result |
|---|---|
| 1. No off-ledger fall (each hit's HP-before ≥ the previous recorded HP; first hit against `hp_initial`) | **0 falls** over 24,295 packets, 25/25 cells |
| 2. Σ applied = Σ (initial − final) + Σ `leech_heal_hp` | **25/25, worst 1.4e-16** (gamora 7.7e-17; the difference is summation order) |
| 3. Visible heal ≤ Σ `leech_heal_hp` | **25/25.** Σ visible 18,799,918 = Σ leech 18,799,918 |

**Coverage checks:**
- every GO target has a GO-BODIES row;
- no body changed HP without a GO hit;
- each body's last `hp_after` equals its `hp_final`;
- HPCHAIN `hp_fall` equals Σ (initial − final).

**My earlier concern is answered.** Her G3 `n_leech_events` counts the **player's** leech, which is 0 because she has none (drax `964cf9a`). Monster leech is the sealed fold's `leech_heal`, and it reconciles exactly.

## His off-ledger reliance on `identity_pass`: ACCEPTABLE, no `hp_after` rerun required
- **What the port's flag tests.** In `kc2p_join2_emit.gd:793–815`, `identity_pass` is a per-body net test: fall > applied counts as an off-ledger fall. Its inputs are the same GO and GO-BODIES grains. **I recomputed it from the grains: 0 of 14,785 bodies.**
- **What clause 2 adds.** Clause 2 closes at 25/25 (my recompute: 6e-14 on gb-fix; gamora: 1.7e-16), with `leech_heal_hp` taken from independent fold telemetry.
- **Why that is enough.** A hidden per-hit fall would need a hidden rise that cancels it to ~1e-16 in every cell. For his arm, that leaves only offsetting off-ledger pairs inside one body unexcluded.
- **Direction.** An off-ledger fall on his bodies would *understate* his `applied` and favour her. The flag and the closure together make a material understatement implausible.
- **Advisory, not owed:** add per-hit `hp_after` to his GO the next time the emitter is touched for another reason (INFO-1).

## BLOCK-1: RELEASED
- The registered identity passes on both arms, as above.
- The re-issue's `M_c` block **equals `aaa1f6a3f`'s exactly** (I compared them directly). `per_cell.json` → `data` is 25/25 equal.
- **The PRIMARY may now read "M-c (her) ≥ M-c (Warlord) over {159, 160}: TRUE as graded (25/0, p = 5.96e-8)"**, carrying the seven labels now present in the README, `grade_report.json` → `labels` and `per_cell.json` → `labels`.
- My WARN-1 (labels; UN-PREDICTED prints; H) is **resolved**: T, M-d and M-b now print "printed, un-predicted", and H = 40,000 is stated.

## Fraction (a): **FALSE AS PRE-STATED**, 31/32 of record
**The reading of record is "mapped = the setting is implemented in the port with its operands bound".**
- That is what the census classes count.
- gamora's "the pack carries the operand" is a stricter pack-completeness criterion. It is printed beside: **29/32**, missing rows 18, 23 and 24.

**Result: 31/32 by implementation.** Rows 23 and 24 are implemented from design-text operands. **Row 18 (build legality, OUT-OF-ARENA) is not implemented**: the port has no legality check.

**Grade against "32/32, or 31/32 if row 18 is ruled unmappable": FALSE AS PRE-STATED.**
- Row 18 was never *ruled* unmappable. It is mappable (a kit-load check with the NC "drop Fire Wall → refuse") and simply unbuilt.
- Applying the alternative now would be a post-hoc ruling, and nobody has made one.
- **Recorded FALSE** under prereg § 8. There is no effect on the margin: row 18 is out-of-arena.

**INFO-2:** rows 23 and 24 run on operands that are not pack rows. That conflicts with the pack law ("every constant is a PACK ROW, never a literal"). star-lord should cut those operands into the next pack. Until then the 29/32 print stands beside the 31/32.

## Notes (INFO)
- **INFO-1:** add his per-hit `hp_after` at the next emitter touch (advisory).
- **INFO-2:** pack rows are owed for the row 23 and 24 operands.
- **INFO-3:** the Meteor-delay label now cites a departure set of **21 early Meteors (7 in waves 159/160)** after the KP-481 / KP-485 semantics. My earlier set of 9 in 159/160 is a superset, so my bound (closest 98,614 vs 90,504) still covers it. The corrected re-grade is labelled *not conservative* and goes to its own later gate.
- **INFO-4:** the r_DMG-by-digest replay binding (`ff527d2e` / `e8864ac8` / `90e12d52`), KP-481 EXT1/EXT2 (`648e193b`, `c79ea0fd`) and the KP-485 tie order are **noted, not re-gated here**. The `M_c` equality above shows they did not move the as-graded result.
- **INFO-5:** row 22's NC is still only partly discharged (addendum `4959e1100` § (c)). Fraction (b) stays NO VERDICT.

## Action
- [ ] gamora: record fraction (a) as FALSE AS PRE-STATED (31/32 of record; 29/32 printed beside).
- [ ] star-lord: pack rows for the row 23 and 24 operands.
- [ ] drax: row 22's remaining NC legs; his `hp_after` at the next emitter touch.
- [ ] Matt: none.

## References
- `reincarnated-godot/evidence/join1/j4b-hook/hpchain/rerun/`; grains `/Users/admin/Games/join3c-bulk/hpchain/her/`
- `agentic_orchestration/gamora/analyses/2026-10-15-join1-j4b-GRADED-MARGIN{,-REISSUE}/`; the `d56403c40` identity folder
- `reincarnated-godot/kc2_play/tools/kc2p_join2_emit.gd`
