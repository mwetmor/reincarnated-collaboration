# Finding — 2026-08-25 — A-6 decline: legality of re-opening floor selection (Gate-1-shaped ruling)

**Reviewer:** jack-ryan
**Severity:** WARN (one new defect named; one BLOCK-adjacent obligation on A-6 itself)
**Target:** `drax/v0.1-s2b-rows-3-7` @ `d9e908c` — receipt `~/Games/reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/xrow.json`
**Developer:** drax (instrument) · knight-rider (ruling under review)
**Principles applied:** REVIEW_PROCESS #1, #2, #4, #5
**Disciplines cited:** #72 cl. 9(b) · #75 cl. 2 · #75.5 cl. 5.6 · #78 cl. 2/4 · #66 · #68 · #19.1(b) · #79 cl. 1 · #73

---

## 0. Derivation basis (so nothing below is inherited)

I reproduced the operator from the receipt's own 48 arm rows before ruling: **z-score over all 48 arms, population sd (ddof=0), euclidean over the 9 named descriptors.** This returns the noise pair `single_target/fire`–`single_target/water` @cathedral at **3.6678** and the global null mean at **0.5088**, both to 4 dp, matching `NULL_COMPOSITION` and `NULL_within_row` exactly. Per-stage, null-only and ddof=1 populations all fail to reproduce. Every number below is derived from that reconstruction, not read from a summary (**#19.1(b)**, **#79 cl. 1**).

**I deliberately did not compute any cross-row quantity.** All derivation is confined to the null leg — the same restriction drax's own `floor_selection_rule` imposes on floor choice. Computing a cross ratio under any alternative null would spend the option for whoever executes.

---

## 1. What I found

### 1.1 KR's Fact 1 is CONFIRMED, and provable harder than he put it

`significant_components` contributes **exactly 0.0 % of squared distance to 73 of the 76 within-row null pairs.** Its entire footprint in the null leg is three pairs, and all three contain the same arm, `single_target/water@cathedral`:

| pair | distance | sig share | distance with sig removed |
|---|---|---|---|
| single_target cathedral fire–water | 3.668 | 81.7 % | 1.571 |
| single_target cathedral water–wind | 3.438 | 93.0 % | 0.913 |
| single_target cathedral water–earth | 3.432 | 93.2 % | 0.893 |

Those are the **top three distances in the entire null leg**; the fourth is 1.704. Across all 48 arms the descriptor reads 1 on 41 arms, 2 on all eight `line` arms (row-characteristic, not noise), **3 on exactly one arm**, and 4 on exactly one (`multi_projectile_count1@cathedral`, a question arm). drax's *"ONE PAIR of ONE ROW"* is refuted by his own corpus. **It is one arm, in three pairs.**

### 1.2 KR's supporting arithmetic is correct and its framing misleads

*"Removing the max pair still leaves eleven pairs averaging 1.41"* is arithmetically right — `(12 × 1.5987 − 3.6678) / 11 = 1.4106`. But that 1.41 is a **mixture** of the two remaining contaminated pairs (3.438, 3.432) and nine clean ones (mean **0.9608**). Quoted as evidence of arm-wide contamination it conflates two effects. The nine clean pairs are the interesting half, and they lead to §1.3.

### 1.3 ⚑ THE THIRD DEFECT — neither drax nor KR enumerated it, and it is not in galadriel's lane

Drop `significant_components` entirely and recompute the null leg:

| row | n pairs | null mean | null max | **no-sig mean** | **no-sig max** |
|---|---|---|---|---|---|
| circle | 12 | 0.2330 | 0.3187 | 0.2330 | 0.3187 |
| single_target | 12 | 1.5987 | 3.6678 | **1.0020** | **1.7043** |
| line | 12 | 0.4114 | 0.7554 | 0.4114 | 0.7554 |
| melee_arc | 20 | 0.2426 | 0.6011 | 0.2426 | 0.6011 |
| multi_projectile | 20 | 0.3447 | 1.0262 | 0.3447 | 1.0262 |
| **GLOBAL** | 76 | 0.5088 | 3.6678 | **0.4145** | **1.7043** |

**`single_target` remains the noise-setting row after the descriptor is removed**, at 2.4×–4.3× every sibling's mean, with 0.0 % `significant_components` contribution in the three pairs that set it (fire–wind 1.704, fire–earth 1.497, arena fire–earth 1.430).

**Consequence:** repairing or replacing the descriptor — galadriel's lane — **does not make A-6 evaluable. It makes it differently not-evaluable.** Q1 (`single_target` vs `line`), the tranche's load-bearing question, would still be graded against a bar set by one of its own two rows. This defect lives in the **null leg's population**, not in the descriptor, and it currently has no owner.

### 1.4 The receipt refutes its own declared inflation mechanism — a THIRD instance of KR's class

`null_inflation_declared` states `circle`'s motif swap inflates the null. **`circle` is the tightest row in the gate** (mean 0.2330 / max 0.3187). `A6_CRITERION_STATUS` names four motif-swap rows (`circle`, `single_target`, `multi_projectile`, `line`) against `melee_arc` as the sole tint-only row — yet `melee_arc` (0.2426) and `circle` (0.2330) are indistinguishable. **The declared mechanism predicts inflation on four rows and it materialises on one.** The motif-swap story is therefore not established as the cause of §1.3's residual; it is the *hypothesis* that must be tested, and the tranche has an internal control for it (`melee_arc`) that has never been used that way.

### 1.5 The merge claim is unfalsifiable from the receipt as emitted (#66-shaped gap)

`NULL_COMPOSITION` is computed **only at the retained floor**. `floor_sweep` emits four aggregates per rung and no composition. So nothing in the artifact says whether floor 16's lower `null_max` (2.7358) is the same arm abated or a different pair taking over. drax's own stated reason for writing `NULL_COMPOSITION` — *"if it is set by ONE pair of ONE row, the criterion is about that pair"* — applies at every rung and was discharged at one. **The discriminator exists at one floor and does not survive the sweep** (#66; #68's per-arm-discriminator prescription one layer up).

---

## 2. Rulings

### Q1 — Is (c) legal? **NO. It is forbidden by name.**

**#72 cl. 9(b):** *"the remedy is never 'extend the ladder until the optimum moves inside' — it is to establish that the objective has an interior optimum at all, and to declare it degenerate if it does not."*

drax declared degenerate and RETAINED. **That is the prescribed terminal state, not an unfinished step.** KR's premise — that a step returned degenerate and therefore remains open — is wrong: the pre-registered procedure ran to completion and its outcome was *no selection; hold the default*. What (c) asks for is not completion but **re-specification with the sweep in hand**, and the sweep publishes the direction of the answer: `min_cross_over_max_null` runs 0.134 / 0.192 / 0.179 / 0.186 / 0.146 / 0.203 / **0.414** / **0.655** across floors 2→24. Anyone who has read that ladder and proposes extending it upward is walking knowingly toward the passing direction. **75.5 cl. 5.6 inverted, different door, same room.** No pre-registration authored by a sweep-reader discharges it *on this corpus*.

**The narrow legal version, for the record:** a floor is a property of the **instrument**, not of this tranche. Selected on a population that does not contain the questions — a null-only calibration corpus, or the next tranche's arms before its cross leg is computed — the selector's knowledge of this sweep cannot steer the outcome. That is legal, pre-registerable, and a **later** move. It is not a repair to this receipt.

### Q2 — Is there a (d)? **YES. Repair A-6, not the instrument.**

A-6's null-leg premise — *"element arms of one row are the same SHAPE"* — is **FALSE BY SPEC on four of five rows**, in drax's own words. The defective artifact is therefore **my Gate-1 acceptance criterion**, not drax's instrument. The instrument reported faithfully; it declined because the criterion handed it a noise term the spec guarantees is heterogeneous.

Repairing an acceptance criterion whose premise is refuted **by the spec** is not tuning: the refutation (motif-swap-keyed-to-element) is a design fact dated before the corpus existed, and it is legible with the receipt closed.

**drax refused a legal move by conflating two different selections.** *"Choosing which rows may enter the noise estimate is the cross-row leg reaching into its own bar by another door"* is correct against a **numeric** row selection. It is **not** correct against a **spec-predicate** selection: *"does this row key a motif swap to the element axis?"* is answerable from the spec without opening the receipt, and the resulting row set is fixed before any number is seen. He applied the right rule to the wrong object, and that is why the fork came back with two options.

**Pre-registration cost that must be stated up front, not discovered:** a null restricted to spec-conforming rows is n = 20 pairs, not 76, and a max over 20 is not a max over 76. Under **#68** that is a dynamic-range statement and belongs in the pre-registration beside the decision rule.

### Q3 — Merge or stay separate? **NEITHER, as posed.**

KR claims one defect filed as two. My derived evidence points **against** the merge: the residual that keeps `single_target` as the noise-setting row carries **0.0 % `significant_components`**, so a floor change cannot fix a defect the descriptor does not carry. But the merge also cannot be *refuted* from the artifact, because the composition does not travel with the sweep (§1.5).

**Disposition: three defects, two owners, one unanswerable question.**
- **D1** — fragile integer descriptor on a small mask → galadriel (instrument lane).
- **D2** — floor retained-not-selected → **CLOSED as prescribed by #72 cl. 9(b)**; re-selection only on a question-free population.
- **D3** — §1.3, A-6's null-leg population violates its own premise → **jack-ryan (the criterion is mine)**.
- **Open** — whether D1 and D2 share a mechanism is not decidable from `xrow.json`; discharged by emitting per-rung null composition at the next authorised scoring, not by re-scoring now.

### Q4 — Does the DECLINE need disposition beyond ratification? **YES, and it does not have one.**

KR's ratification disposes of **drax's conduct**. It does not dispose of **A-6**, which is my Gate-1 criterion and my obligation. An UNRESOLVED acceptance criterion with no owner and no re-ask gate is the mooted-escalation family named in `CLAUDE.md`'s own conflict-rule corollary and in **#73** one level up.

**Disposition — A-6 is SUSPENDED. Not passed. Not failed.**
1. Repair route named: (d), §Q2.
2. Owners named: jack-ryan (criterion), galadriel (descriptor), drax (per-rung composition emission).
3. **A named gate at which A-6 is answered or formally RETIRED.** KR sequences it; a suspension without a re-ask date is the defect it was raised to close.
4. **Sever now.** Results that do not depend on the noise term must be banked immediately so a suspended criterion does not hold hostage work that never needed it — the positive control (`melee_strike` vs `ground_targeted_circle`, 1.466×, `#75 cl. 2` leg intact) and Q1's rendered-aspect answer.

**⚑ Caveat on the Q1 aspect figure, filed under #19.1(b).** The **7.41× (1.29 vs 9.56)** is **not in `xrow.json`.** I could not verify it from the receipt I was pointed at. `xrow.json`'s own `aspect_major_minor` column gives cathedral `line` 6.157–6.763 vs `single_target` 1.173–1.446, and arena `line` 2.927–3.148 — no arm carries 9.56 or 1.29. The figure appears in KR's ruling and in `drax/notes/2026-08-24-s2b-mint-note.md`. Whatever instrument produced it, it is a *different* instrument from this receipt. Relaying it with provenance is compliant; **banking it as CARRIED without opening that instrument is not.** Open it before it becomes a record.

### Q5 — Discipline candidate: **ADOPTED IN SUBSTANCE, REJECTED IN FORM.**

**It is not #19.1(b).** That rule governs a claim you **inherit**. drax characterised his **own** receipt from his **own** column. Nothing was inherited.

**Nearest live neighbour is #78 cl. 4** — *"before acting on a conviction, ISOLATE THE CONVICTED POPULATION… a verdict taken over a mixed mask, a pooled cohort, or an aggregate is a verdict about the mixture."* drax's *"ONE PAIR"* is precisely an un-isolated locus claim. But cl. 4's trigger is *"before acting on a conviction"* and **drax declined to act** — his case falls outside the existing text by one word.

**KR's wording is too narrow twice.** *"Tested against the receipt's own aggregate columns"* presumes (i) that the refuting column exists — here the decisive column (per-row no-sig means, §1.3) **does not exist in the receipt**; I had to derive it — and (ii) that the test is an aggregate read. Both presumptions are what let the class survive.

**Ruled: lands as #78 clause 6, not a new number** (#58-DECLINED precedent, consistent with #19.1(b) / #19.2 / #75.5):

> **A claim about WHERE a defect lives is itself a verdict about a population, and is isolated by the same set difference clause 4 requires — and the obligation fires when the locus is used to scope a REPAIR FORK, not only when a repair is applied.** A decline is not an exemption: an un-isolated locus produces a fork whose options are the wrong options, and the fork is the artifact the next agent inherits. Where the receipt does not carry a column that could refute the locus, the locus is **derived**, not read off (**#76 cl. 1** at the diagnosis layer).

**Three founding instances, all one session, all drax, all in receipts of unusually high quality** — which is the argument for the clause, not against it:
1. Stage 3 — `elongation` printed beside the C-2 number that convicted a correct effect (already carried at #75.5 cl. 4(b)).
2. `"ONE PAIR of ONE ROW"` — refuted by the `mean` column in the same block (§1.1).
3. `null_inflation_declared` on `circle` — refuted by `circle` being the tightest row in the gate (§1.4). **KR counted two; there are three.**

Canonical write to `engineering-disciplines.md` is owed and not performed in this session (KR sequences).

---

## 3. Dependency on galadriel

**My ruling does not depend on her answer** for Q1, Q3, Q4 or Q5.

**It interacts on Q2, and the sequencing matters.** D1 (descriptor) and D3 (null population) are **independent** defects. If her descriptor repair lands **first**, §1.3's residual will present as *"the leftover after the fix"* and be mis-scoped as instrument residue rather than as a criterion defect. **Sequence D3's pre-registration BEFORE or PARALLEL to her landing — not after.** KR sequences; I do not contact her.

---

## 4. Action

- [ ] **knight-rider:** sequence D3 pre-registration at or before galadriel's descriptor landing (§3).
- [ ] **knight-rider:** name the gate at which A-6 is answered or retired (§Q4.3). A suspension without a re-ask date is the defect.
- [ ] **knight-rider:** withdraw (c) from the dispatch's A-7 block — #72 cl. 9(b) forbids it by name.
- [ ] **knight-rider / drax:** open the instrument behind **7.41× (1.29 vs 9.56)** before it is banked as CARRIED (§Q4 caveat).
- [ ] **jack-ryan:** author D3 / A-6 repair pre-registration under (d) — spec-predicate row selection, n = 20 cost declared up front, no cross-row quantity computed before it is registered and pushed.
- [ ] **jack-ryan:** canonical write of **#78 cl. 6** to `engineering-disciplines.md`, on KR's sequencing.
- [ ] **drax:** emit per-rung null composition alongside `floor_sweep` at the next authorised scoring (§1.5, #66). **Not now — no re-scoring before pre-registration lands.**
- [ ] **Matt:** none. Nothing here is cross-seam schema, a new ADR, or a milestone tag. ADR-002 process tier.

## 5. Credits carried forward

Recorded because a decline that is correct and unremarked is how the next one gets made differently. drax pushed the anti-tuning clause before the corpus existed and held it under a result that went against him; ran **R-4 against his own instrument**, caught his own check being weakened by a `boundary AND monotone` conjunction *until it passed his own sweep*, and published the corrected verdict against himself; declared `circle`'s inflation and refused to exclude it on a principle that cost him; and refused fork (b) on **75.5 cl. 5.6** correctly. **His refusal of (b) was right. His refusal of the spec-predicate move was the right rule applied to the wrong object** — and that distinction, not the decline, is the whole content of §Q2.

## 6. References

- `~/Games/reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/xrow.json`
- `~/Games/reincarnated-collaboration/agentic_orchestration/knight-rider/rulings/2026-08-25-a6-decline-ratified-contamination-is-one-arm-not-one-pair.md`
- `~/Games/reincarnated-collaboration/agentic_orchestration/dispatches/2026-08-24-drax-s2b-rows-redispatch.md` (§ A-7)
- `~/Games/reincarnated-collaboration/agentic_orchestration/drax/notes/2026-08-24-s2b-mint-note.md`
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — #66, #68, #72 cl. 9, #75, #75.5, #76, #78, #79, #19.1(b), #73
