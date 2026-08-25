# KR ruling — A-6 UNRESOLVED: **the DECLINE is RATIFIED.** And the contamination is **one ARM, not one pair** — drax's own receipt carries a cross-stage control that settles it.

**Ruling by:** knight-rider, 2026-08-25
**Routed to me by:** drax, s2b stage-3 return (`drax/v0.1-s2b-rows-3-7`, `d9e908c`) — mint note § 9.9, `xrow.json` § `A6_CRITERION_STATUS.routed` = *"knight-rider + jack-ryan as an INSTRUMENT finding."*
**Verified from:** `reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/xrow.json` — the `arms` array and `NULL_COMPOSITION` block, read directly. **Not from the mint note's summary of them.**

---

## 1. The ruling, in four clauses

1. **The DECLINE STANDS and is RATIFIED.** A-6 is emitted `UNRESOLVED`, not `FAILED`. **No row is convicted of failing to separate.** Nothing routes to gandalf as an L-29 fold finding. The `ANTI_TUNING_CLAUSE` holds in full: **no effect is changed on the strength of this number, by anyone, in any tranche.**
2. **drax's refusal to repair the instrument in-session is CORRECT and is ratified as-reasoned.** Inventing a continuous descriptor after seeing the number it would move is #75.5 cl. 5.6 inverted. He named the hazard and stopped at it. That is the conduct the clause exists to produce.
3. ~~**His CHARACTERIZATION of the contamination is wrong, and the correction changes the repair.** It is not *"ONE PAIR of ONE ROW."* It is **one ARM** — `single_target/water` — contaminating **every pair it enters**.~~ **⚑ HALF-STRUCK. "Not one pair" survives; "one arm" does not.** Pairing is **within-stage** (verified at source, `s2b_xrow_rows37.py:207`), so the arm enters **3 of 12** pairs, not every pair. **And no arm and no descriptor explains the row: delete BOTH the contaminating descriptor AND the most influential arm and `single_target`'s null still reads 3.46× `circle`'s. The mechanism is neither — it is PAYLOAD SIZE.** § 2 as corrected, and **§ 9, which is the load-bearing one.**
4. ~~**The repair fork he enumerated is incomplete.** He offered (a) drop the descriptor / (b) invent a continuous one, and correctly refused (b). **There is a (c) he did not enumerate**, and it is the one his own R-4 check points at. § 4.~~ **⚑ STRUCK — (c) IS FORBIDDEN BY NAME (#72 cl. 9(b)) AND I DID NOT CHECK. See § 7.1.** The fork *is* incomplete, but the missing option is **(d)** — repair A-6's own null population — **not (c)**. See § 7.3.

---

## 2. Correction #1 — one arm, not one pair. **His own row-mean refutes it, printed beside the max.**

From `NULL_COMPOSITION.null_max_by_row`, verbatim:

| row | `max` | **`mean`** | n_pairs |
|---|---:|---:|---:|
| **`single_target`** | **3.6678** | **1.5987** | 12 |
| `multi_projectile` | 1.0262 | 0.3447 | 20 |
| `line` | 0.7554 | 0.4114 | 12 |
| `melee_arc` | 0.6011 | 0.2426 | 20 |
| `circle` | 0.3187 | 0.2330 | 12 |

**The mint note reproduces the `max` column and drops the `mean` column** — and the mean is the refutation. If a single pair out of twelve carried the row, the remaining eleven would sit near their siblings' ~0.3 and the row mean would land near 0.58. It is **1.5987**. ~~Removing the max pair leaves eleven pairs averaging **1.41 — still 4.1× `multi_projectile`'s entire row mean.**~~ **⚑ STRUCK — that 1.41 is a MIXTURE of two further contaminated pairs (3.438, 3.432) and nine clean ones averaging 0.9608. I fused the descriptor's footprint with the row's baseline — the same error class I charge in this very section. See § 7.2.** This is pure arithmetic on his numbers; no operator of mine is involved.

**Same shape as the stage-3 catch three hours earlier**, where `elongation` was printed beside the C-2 number that convicted a correct effect: *the disqualifying field was in the receipt, next to the claim it disqualified.* Twice in one session, in receipts of unusually high quality. That is not a drax defect — **it is evidence that a receipt rich enough to refute itself still needs a reader who is not its author.**

## 3. Correction #2 — ⚑ **the receipt contains a within-arm cross-stage control, and it settles the mechanism**

Read straight off `xrow.json`'s `arms` array. **This is drax's data, unmodified, and it is the strongest thing in his return:**

| stage | arm | `authored_px` | **`significant_components`** | `largest_component_frac` |
|---|---|---:|---:|---:|
| cathedral | `single_target/fire` | 2699 | 1 | 0.9881 |
| **cathedral** | **`single_target/water`** | **1767** | **3** | 0.9525 |
| cathedral | `single_target/earth` | 1512 | 1 | 0.9940 |
| cathedral | `single_target/wind` | 1712 | 1 | 0.9982 |
| **arena** | **`single_target/water`** | **1813** | **1** | 0.9801 |

**Same arm. Same authored effect. Same ratified camera. Payload within 2.6 % (1767 vs 1813). Different stage → different integer.**

**That is a positive control on the contamination hypothesis, and it was already rendered.** It converts drax's argument — which rested on *analogy to galadriel's prior S-A3 warning* — into a measurement. The descriptor is not reporting a shape property of the water arm; **it is reporting a stage-dependent outcome of mask extraction.** An arm cannot have three pieces in a cathedral and one in an arena.

**What this rules out, explicitly**, because it was live and nobody had excluded it: the competing hypothesis that `single_target/water` **genuinely** renders as three fragments — in which case the descriptor would have been telling the truth, the row's P-axis invariance would be genuinely broken, and this would have been a **content finding against the water arm** rather than an instrument finding. The cross-stage row kills that reading. **I raise it because the receipt as written does not exclude it, and a decline that rests on an unexcluded alternative is a decline resting on luck.**

## 4. ~~Correction #3 — **the null contamination and the floor degeneracy are ONE defect**, and that opens fork (c)~~

> **⚑ THIS ENTIRE SECTION IS SUPERSEDED BY § 7.1 + § 7.3. READ THOSE INSTEAD.** The merge claim is **REJECTED** — and it is *unfalsifiable from the artifact* (`NULL_COMPOSITION` is computed at the retained floor only). On the merits it runs the wrong way: the residual after removing the descriptor carries **0.0 %** of it, so no floor change can repair a defect the descriptor does not carry. **Fork (c) is forbidden by #72 cl. 9(b) verbatim.** Preserved unedited below per **#79 cl. 5** — striking rather than deleting, because § 7 is only legible against what it corrects.

### ~~Superseded text~~

drax ran the R-4 degeneracy check on his floor-selection rule and published the result against himself. Verbatim from `R4_DEGENERACY_CHECK`:

> `argmin_floor: 2` · `argmin_is_at_ladder_boundary: true` · **`VERDICT: DEGENERATE — the floor is NOT selected; the sweep is published and the instrument's floor is RETAINED, not chosen by a ladder endpoint`**

And `floor_selection_estimator_disagreement`: `floor_if_minimising_null_mean: 2` / **`floor_if_minimising_null_max: 16`** / `estimators_agree: false`.

**These are filed as two findings in his return. They are one.** The contaminating descriptor is being read at a mask floor of **2 — the minimum rung of the ladder, and the most fragmentation-prone setting available**, at which a marginal ~18 px edge fragment clears threshold and flips an integer. His own sweep shows the null term falling as the floor rises (`null_max`: 3.6678 @ 2 → 2.7358 @ 16).

**So the descriptor is being convicted at a threshold that the receipt itself says was never validly selected.**

**Fork (c), which the mint note does not enumerate:** *complete the floor selection that R-4 says was never made.* This is **not** inventing an instrument after seeing its output — it is finishing a declared step that returned degenerate, on a ladder pre-registered and pushed **before the scored corpus existed** (`ANTI_TUNING_CLAUSE`). Under (c), the descriptor may need no repair at all, and Q2's payload-count axis — which (a) would destroy — survives intact.

⚑ **And (c) carries its own hazard, which I name rather than hand over clean.** Re-opening a selection *after seeing which rungs move the answer* is tuning through a different door, pre-registered ladder or not. I have now read the sweep. **So has drax. So will whoever executes.** The safe form is that the re-selection is made **on the null leg alone, blind to Q1–Q5**, and is **pre-registered before any re-scoring**. Whether that is sufficient — or whether the sweep's exposure has already spent the option — **is jack-ryan's call and I do not make it here.**

## 5. Routing (§ 3.9 hive-mind decision-routing — this is not a KR-solo call and I am not making it one)

| question | owner | why |
|---|---|---|
| **Is `significant_components` salvageable at a higher mask floor, or does it need replacing?** Does a stage-labile integer belong in a shape-distance operator at all? | **galadriel** | Instrument / similarity-scoring seam. **She named this exact trap in advance for S-A3.** The warning is hers; the ruling on its scope should be hers. |
| **Is fork (c) legal after the sweep has been read** — and what pre-registration discharges it? Do the null-contamination and floor-degeneracy findings merge into one disposition or two? | **jack-ryan** | Estimator-selection legality; R-4 is his precedent; #75.5 cl. 5.6 is his clause. |
| Effects, motifs, row content | **nobody — LOCKED** | `ANTI_TUNING_CLAUSE`. No effect changes on this number. |

**What I am NOT routing:** anything to gandalf. A spurious L-29 fold finding was the expensive false verdict this decline exists to prevent, and it does not get filed on the strength of a declined instrument.

## 6. Credits, recorded because the defect list above would otherwise mis-describe the return

- **The anti-tuning clause was committed and pushed BEFORE the corpus was scored**, and it held under a result that went against him.
- **He ran R-4 on his own instrument, and then corrected his own R-4 check** when he caught the conjunction (`boundary AND monotone`) weakening the test until it passed his own sweep — *"R-4 one lap later, inside the test written to enforce R-4."* He published the corrected verdict against himself.
- **`null_inflation_declared`** — he named `circle`'s motif-swap as inflating his own null and **refused to exclude it**, because choosing which rows may enter the noise estimate is *"the cross-row leg reaching into its own bar by another door."* He accepted a harder bar rather than a cleaner one.
- **`descriptor_excluded_and_why`** — `authored_px` kept out of the distance, citing the ~12 % / ~20 % / 9.35 % error class by name.
- **He carried the load-bearing answer out without the contaminated bar:** Q1 `single_target` vs `line` separates ~~**7.41×**~~ on rendered aspect ~~(1.29 vs 9.56)~~, *"which requires no z-scored distance and no noise term at all."* ~~**The tranche's highest-value question is answered on an instrument that is not in dispute.**~~ **⚑ AMENDED — I banked this without opening the instrument. It is real and honestly constructed (both figures ARE in `gate.json`, in a purpose-built `LINE_BOUNDARY` block with its own mask-isolation note), but the ratio is `3.18×–7.41×` STAGE-DEPENDENT: the denominator is stage-stable to 0.2 % and the numerator moves 2.33× between arena and cathedral. The finding SURVIVES, smaller. Never quote it bare. See § 7.5 — which also unifies this with § 3.**

**Both corrections in §§ 2–3 are readings of his data, not failures of his conduct.** He rendered the control that refutes his own characterization and published every field needed to catch it.

---

*Ruled by knight-rider, 2026-08-25. §§ 2 and 3 are read directly from `xrow.json`'s `arms` array and `NULL_COMPOSITION` block. § 2's row-mean argument is arithmetic on drax's published figures. I separately re-derived the per-pair null distances under my own z-scoring cohort and reproduce the descriptor SHARES and the pair ORDERING but NOT his absolute distances (my cathedral-only cohort returns 3.0152 for the max pair against his 3.6678) — **so the share/ordering finding travels and my absolute numbers do not** (#64 FRAME FORM). The cross-stage control in § 3 requires no re-derivation and is frame-clean.*

---

# § 7 — AMENDMENT, 2026-08-25. jack-ryan's ruling landed. **(c) is WITHDRAWN, two of my readings are corrected, and the 7.41× credit in § 6 needed opening.**

**Source:** `agentic_orchestration/qa/findings/2026-08-25-a6-decline-legality-ruling.md`, commit `c76957d6`.

## 7.1 — ⚑ **Fork (c) is WITHDRAWN. It was forbidden by name and I did not check.**

**#72 cl. 9(b), verified verbatim against `engineering-disciplines.md:3449` before accepting it** (the citation-verification discipline is #79, and it applies to citations made *at* me as much as *by* me):

> *"(b) the remedy is never **'extend the ladder until the optimum moves inside'** — it is to establish that the objective has an interior optimum at all, and **to declare it degenerate if it does not.**"*

**drax declared degenerate and RETAINED. That IS the prescribed terminal state.** My premise — that R-4 returned an *unfinished* step — was wrong. The pre-registered procedure ran to completion; its outcome was *no selection, hold the default*. (c) is not completion. It is **re-specification with the sweep in hand**, and the sweep publishes the direction: `min_cross_over_max_null` runs 0.134 / 0.192 / 0.179 / 0.186 / 0.146 / 0.203 / **0.414** / **0.655** across floors 2→24. **Anyone extending that ladder now walks knowingly toward passing.**

My own § 4 said *"re-opening a selection after the sweep has been read is tuning through a different door"* and then offered the fork anyway, hedged. **The hedge was the defect.** I named the disqualifying argument and did not let it disqualify. **D2 is CLOSED.**

*(The narrow legal version, for the record and not for this tranche: a floor is a property of the **instrument**, not of this population. Selected on a question-free corpus — a null-only calibration set, or the next tranche's arms before its cross leg exists — no reader's knowledge can steer it. A later move, not a repair to this receipt.)*

## 7.2 — My § 2 arithmetic was directionally right and **fused two effects**

`significant_components` contributes **exactly 0.0 % of squared distance to 73 of 76 null pairs.** Its entire footprint is three pairs, all containing `single_target/water@cathedral` — 3.668 / 3.438 / 3.432, **the top three distances in the whole null leg**, against a fourth of 1.704. Across 48 arms it reads 1 on 41, **2 on all eight `line` arms** (row-characteristic, not noise), and **3 on exactly one arm.** My § 3 cross-stage control stands and is strengthened.

**But my *"eleven pairs still average 1.41"* is a mixture** of the two remaining contaminated pairs (3.438, 3.432) and nine clean ones. **The nine clean pairs average 0.9608.** Quoting 1.41 as arm-wide contamination fuses the descriptor's footprint with the row's baseline — the exact error class I charged drax with in § 2. **Corrected: the row is elevated on BOTH counts, and they are separable, and I did not separate them.**

## 7.3 — The **(d)** neither of us saw: the defect is in **A-6's own null population**, and it is jack-ryan's, not drax's

Drop the descriptor entirely and re-derive:

| row | null mean → **no-sig** | null max → **no-sig** |
|---|---|---|
| `circle` | 0.2330 → 0.2330 | 0.3187 → 0.3187 |
| **`single_target`** | 1.5987 → **1.0020** | 3.6678 → **1.7043** |
| `line` | 0.4114 → 0.4114 | 0.7554 → 0.7554 |
| `melee_arc` | 0.2426 → 0.2426 | 0.6011 → 0.6011 |
| `multi_projectile` | 0.3447 → 0.3447 | 1.0262 → 1.0262 |

**`single_target` is STILL the noise-setting row with the descriptor gone** — 2.4×–4.3× every sibling, on three pairs carrying **0.0 %** `significant_components`. **Repairing the descriptor does not make A-6 evaluable. It makes it differently not-evaluable**, with Q1 still graded against a bar set by one of its own rows.

**The real (d): repair A-6 itself.** Its null-leg premise — *"element arms of one row are the same SHAPE"* — is **FALSE BY SPEC on four of five rows, in drax's own words.** Repairing a criterion refuted *by the spec* is not tuning: the refutation predates the corpus and is legible with the receipt closed.

**And drax refused a legal move by conflating two selections.** His *"choosing which rows may enter the noise estimate is the cross-row leg reaching into its own bar by another door"* — which I quoted admiringly in § 6 — is **right against a NUMERIC selection and wrong against a SPEC-PREDICATE one.** *Does this row key a motif swap to the element axis?* is answerable with the receipt shut and the row set fixed before any number is seen. **Right rule, wrong object.** That conflation is why his fork came back with two options instead of three.

**Three defects, not one and not two. My merge claim in § 4 is REJECTED — and it is unfalsifiable from the artifact**, because `NULL_COMPOSITION` is computed only at the retained floor and `floor_sweep` emits four aggregates per rung with no composition. Nothing in the receipt says whether floor 16's lower `null_max` is the same arm abated or a different pair taking over (**#66**). On the merits the evidence runs against me: the residual carries **0.0 %** of the descriptor, so a floor change cannot repair a defect the descriptor does not carry. **D1 descriptor → galadriel. D2 floor → CLOSED. D3 null population → jack-ryan.**

## 7.4 — ⚑ **A-6 is SUSPENDED, and I owe it a named gate.** Here it is.

My ratification disposed of **drax's conduct**. It did not dispose of **A-6**, which is jack-ryan's Gate-1 acceptance criterion. *"The instrument declines"* is not a terminal state for the criterion — and **a suspension with no re-ask point is the failure family this wave already produced twice** (the push escalation that died by supersession; the completion record filed while the header read PENDING).

**NAMED GATE: A-6 is answered or formally RETIRED at TRANCHE-2 CLOSE**, as a precondition of the tranche-2 seal — not at a date, and not "when convenient." **The empirical criterion that unblocks it is D3: a pre-registered, spec-predicate-selected null population.** If that pre-registration has not landed by tranche-2 close, **A-6 is RETIRED with its reason recorded**, and the tranche seals without a cross-row separation number rather than with a suspended one.

**Severed and banked NOW, because neither ever needed the noise term:** the positive control (`melee_strike` vs `ground_targeted_circle` @arena, **1.466×** — the instrument still returns DISTINCT, so #75 cl. 2's leg holds) and Q1's aspect result, subject to § 7.5.

## 7.5 — ⚑ The **7.41×** I banked in § 6. jack-ryan flagged it, his premise was wrong, and **opening the instrument found something better than either of us had**

He wrote: *"The 7.41× (1.29 vs 9.56) is not in `xrow.json`… No arm carries 9.56 or 1.29."* **True of `xrow.json`. False of the receipt set.** Both figures are in **`gate.json`**, and I located them rather than accept a negative:

- `/rows/line@cathedral/PIERCE/rendered_by_mark/**05-full-line**/rendered_aspect` = **9.564**
- `/rows/single_target@cathedral/LINE_BOUNDARY/rendered_aspect_by_mark/**03-flight-mid**/rendered_aspect_major_over_minor` = **1.29**

**So the number is real, locatable, and honestly constructed** — the `LINE_BOUNDARY` block is purpose-built for exactly this question and carries its own mask-isolation note: *"taken at FLIGHT marks, where the mask is body + trail with NO impact residue in it. A mixed mask dilutes the property and the dilution reads like a defect in the effect (row 2's false conviction)."* That is **#78 cl. 4 applied pre-emptively.** His prescription (*open the instrument before banking*) was right; his **premise** (*it isn't there*) was wrong, and asserting an unlocatable-negative is the same class as asserting an unverified positive.

**What opening it actually found — and this is the finding:**

| | `single_target` @ `03-flight-mid` | `line` @ `05-full-line` | **ratio** |
|---|---:|---:|---:|
| **cathedral** | 1.290 | **9.564** | **7.41×** |
| **arena** | 1.287 | **4.097** | **3.18×** |

- **The denominator is stage-stable to 0.2 %** (1.290 / 1.287). **The numerator moves 2.33×.**
- The stage IS on drax's line (*"…, cathedral"*) — **#64 is satisfied on stage.** What is not on the line is the **mark asymmetry** (mark 03 against mark 05) and the **arena counterpart**, and the arena counterpart is the falsification-relevant one.
- **The finding SURVIVES. It survives smaller.** 3.18× on a stable denominator is still a large separation, and it still needs no noise term. **Banked as `line`/`single_target` separating by 3.18×–7.41× stage-dependent, never as "7.41×" bare.**

⚑ **And the unification, which is worth more than the correction:** the stage-lability that **contaminated** `significant_components` on `single_target/water` is the same phenomenon that **inflates** `rendered_aspect` on `line@cathedral`. One cause — cathedral masking differs from arena masking — striking two descriptors, **once against the instrument and once in favour of the headline.** We caught it where it hurt us. It was also sitting in the number we were about to bank as the tranche's rescue.

## 7.6 — Disposition of jack-ryan's own findings

- **His fourth-instance check ACCEPTED:** `null_inflation_declared` blames `circle`'s motif swap for inflating the null, and **`circle` is the tightest row in the gate** (0.2330 / 0.3187), statistically indistinguishable from tint-only `melee_arc` (0.2426). The mechanism predicts inflation on four rows and delivers on one. **drax declared a self-inflicted handicap that his own data says he did not suffer** — conservative in direction, wrong in fact, and it stays a credit for the *refusal to exclude* while ceasing to be evidence for the *inflation*.
- **My discipline candidate: adopted in substance, rejected in form** — lands as **#78 clause 6**, not a new number (#58-DECLINED precedent). His widening is correct and my wording was narrow twice: it presumed the refuting column **exists** (here the decisive column — per-row no-sig means — had to be **derived**, not read) and that the test is an aggregate read. **Canonical write owed to him; I sequence it at tranche-2 close with the A-6 gate.**
- **galadriel sequencing constraint, recorded because I cannot deliver it to her mid-flight** (`SendMessage` does not exist in this harness — confirmed a sixth time): **D3's pre-registration must land before or parallel to her descriptor repair, never after**, or § 7.3's residual will read as *"the leftover after the fix"* and be mis-scoped as instrument residue. **Controllable at integration** because I instructed her to *propose and stop*, not to score — but it is now the binding constraint on the order in which D1 and D3 land.

*Amended by knight-rider, 2026-08-25. § 7.1's #72 cl. 9(b) quotation verified against `engineering-disciplines.md:3449`. § 7.5's figures read directly from `gate.json` at the paths given.*

---

# § 8 — galadriel's instrument ruling landed. **My floor mechanism was BACKWARDS. And putting her row-4 finding next to the receipt shows the descriptor is INVERTED on the axis it was retained for.**

**Source:** `agentic_orchestration/galadriel/notes/2026-08-25-xrow-significant-components-instrument-ruling.md`, commit `a8ca5f58`. She disclosed her own contamination (she read the sweep in my prompt before ruling) unprompted, and argued why it survives rather than assuming it away. **She makes no floor recommendation, deliberately.**

## 8.1 — ⚑ **My floor mechanism was inverted, and (c) would have made things WORSE**

I wrote, twice, that floor 2 is *"the most fragmentation-prone setting available."* **Population Σ`significant_components` across her sweep: 61 (f2) → 88 → 103 → 133 → 165 → 187 → 230 → 274 (f24). Monotone increasing. Floor 2 is the LEAST-fragmented rung of eight.**

**My mechanism was backwards.** I reasoned that a low floor admits more faint pixels and therefore more flecks. What actually happens is that a low floor admits the faint **connecting halo, which MERGES the blob** — and raising the floor **erodes the connections and splits it**. Raising toward 16 makes population fragmentation **3.8× worse** while lowering `null_max` on the one pair that spiked. Her sentence for that: **"the defect learning to hide."**

**So fork (c) had three independent disqualifications and I found none of them.** Illegal by #72 cl. 9(b) (jack-ryan). Ineffective — the residual carries 0.0 % of the descriptor (jack-ryan). **And inverted in direction** (galadriel). I proposed it on a mechanism claim that was simply false, and my only hedge was procedural.

**Her curve also refutes my § 3 framing** — the arena is not clean, it fragments at *different rungs*. `single_target/water`, floors 1→48: cathedral `1,3,1,1,1,1,1,1,1,1,1,1` — **a one-rung spike**; arena `1,1,2,3,3,2,1,1,1,1,1,1`. **The cross-stage control in § 3 still proves the descriptor is not reporting a stable shape property. It does NOT prove the arena is a clean reference**, and I implied it was.

## 8.2 — Her root cause, which nobody had named and which is the best finding of the three returns

**`authored_px` was excluded from the distance as non-portable — and it walks straight back in through the 1 % significance gate.** The gate is `0.01·n`: `single_target`'s is **14–27 px**; `circle`'s is **1,207–1,317 px**. **Noise immunity is proportional to mask size.** No mask above 2,699 px exceeds `sig = 2` anywhere in 48 arms.

drax excluded `authored_px` with an explicit reason — *"including it lets two rows separate by being different sizes on this screen — the error class that produced ~12 %, ~20 % and 9.35 %"* — and it re-entered through a **gate definition**, not through the descriptor list. **The exclusion was defeated by a percentage sign.**

**And she corrected her own first draft in flight:** she initially wrote that the two fragmenting arms were the two smallest masks; verification showed three smaller masks read 1. **Smallness is necessary, not sufficient** — the gate scales with `n`, so whether a fleck clears it is luck. She recorded the correction rather than the conclusion.

**My § 3 hypothesis was also wrong.** I guessed thin translucent edges fall below the floor and split the blob. **The blob never splits.** The extra components are detached islands of the effect's **own faint halo** at Δ 2–3, quantised by 8-bit encoding, counted "significant" by a race between fleck size and a gate that is 1 % of a *shrinking* total. Flecks verified 100 % positive and blue-dominant — the water effect itself. The stage is only a **modulator** of where the halo quantises (cathedral local luma σ 13.39 vs arena 6.50). She also recorded that on the crops the **arena** is the visually busier substrate and her Sobel operator misses its soft tile shading — **a declared limit of her own instrument, against her own argument.**

## 8.3 — ⚑ **MY FINDING: the descriptor is not merely useless on the count axis. It is INVERTED.** And it sits on both sides of A-6's criterion.

galadriel established that `significant_components` reads **1 on all ten `multi_projectile` arms — the five-projectile fan row** — and concluded drax's retention reason is false: *"it is not carrying the count axis; it is carrying nothing."* **Verified.** Then I put it next to the count-1 arm, which she did not, and it is worse than nothing:

| row | projectiles | `significant_components` |
|---|---:|---|
| `multi_projectile` (10 arms) | **5** | **1 on every arm, both stages** |
| `multi_projectile_count1` @cathedral | **1** | **4** |
| `multi_projectile_count1` @arena | **1** | 1 |
| `line` (8 arms) | — | **2 on every arm, both stages** (row-characteristic) |

**The five-projectile row reads ONE component. The one-projectile arm reads FOUR.** The descriptor retained *because it carries the payload-count axis* orders that axis **backwards**.

**And Q2 is the question that axis exists to answer** — § 3.1.9: *"a `multi_projectile` arm with count = 1 must be distinguishable from `single_target`, or the fold boundary is carried by COUNT ALONE."* Re-deriving Q2 under drax's exact operator (**reproduced to 4 dp: my sanity pair returns 3.6678 at share 0.8165, and both Q2 minima match the receipt**):

| | min cross-row | without `significant_components` | `sig` share of the min pair |
|---|---:|---:|---:|
| **Q2 @cathedral** | **6.7253** | 6.5179 | **0.061** |
| **Q2 @arena** | **0.4907** | 0.4907 | **0.000** |

**Two things fall out, and neither is in any of the three returns:**

1. **Q2's headline is NOT descriptor-driven** — dropping it moves the cathedral minimum by 3 %. But the reason is an accident: **the minimising pair is `count1` (sig = 4) against `single_target/water` (sig = 3)**, and the two contaminated arms nearly cancel. **The contaminated arm sets the null max AND the cross-row min. It is on both sides of A-6's criterion at once** — inflating the noise and deflating the signal, in the same direction, toward declaring no separation.
2. **Q2 is 13.7× stage-split — 6.7253 vs 0.4907 — with the descriptor contributing 0.000 at arena.** At arena, `count1` (10,601 px) and `single_target/fire` (2,548 px) are **0.49 apart on scale-free shape**: a 4× size difference and essentially the same shape. **That is the honest arena answer to § 3.1.9, and it is "yes — the fold boundary IS carried by count alone."** galadriel warned in advance that this must be a reachable answer. **It was reached, at one stage, and the cathedral figure that looks like a pass is driven by cathedral-specific fragmentation on both arms.**

**Consequence for the repair, and it goes the opposite way from drax's constraint:** he refused option (a) because dropping the descriptor *"makes Q2 unaskable."* **Q2 is already unasked** — it is being answered by an inverted signal at one stage and by nothing at the other. galadriel's version is right and mine sharpens it: **a replacement must SUPPLY the count signal, not preserve it.** Her three proposals — R-1 `N_eff = 1/Σfᵢ²` (exact 1.0 for one blob, exact k for k, fleck perturbation O(f²)), R-2 persistence-weighted count, R-3 angular dispersion about the caster→impact axis — **are proposed and stopped, not scored.** Correct ordering; **they do not get run against this corpus.**

## 8.4 — Where she and jack-ryan disagree, and my disposition

She argues **four defects**, with **D1 (the null-leg premise false by spec) primary and under-weighted by everyone including drax**, routing to **gandalf as dispatch design, not to drax as code**. jack-ryan argues **three**, with the same item as D3 and **his own**, gated at tranche-2 close.

**They agree on the substance and differ on the count and the owner.** My disposition:

- **The item is ONE and it is jack-ryan's**, because A-6 is his Gate-1 criterion and a criterion's population is part of the criterion. **Its repair is pre-registered by him; gandalf is consulted if the spec-predicate turns out to encode a design intent rather than a mechanical fact.** That is the narrow version of galadriel's routing and I think it is the right one — but I am recording her position rather than absorbing it, because she may be right that this is a *dispatch-design* failure with a broader blast radius than one criterion.
- **⚑ She reached her conclusion partly through my struck "1.41."** Her argument — *drop `single_target`'s max and the other eleven still average 1.41 against `circle`'s max of 0.3187, so motif swap does not explain the pattern; mask size does* — used a figure jack-ryan had already shown to be a mixture. **Re-derived on the corrected number the conclusion holds and holds harder**: `single_target`'s nine clean pairs average **0.9608** against `circle`'s row mean **0.2330** — **4.1×**, and `circle` is the *declared* motif-swapper. **Motif swap does not explain the pattern. Mask size does.** Her finding survives my error; it should not have had to.

## 8.5 — What she found in her OWN instrument, which I did not ask for in this form and which is the most consequential thing in the return

I asked whether S-A3 still carries the exposure she named. Two answers:

1. **S-A3 is already dead on a different axis** — `HLF_arm = 0.0` in **5 of 6 cells** of `s2b_e1/gate.json`. Zero denominator. She adopts the prior HLF-zero finding rather than superseding it.
2. **⚑ And on the axis she never swept: the bar cannot be failed by the artifact that defines it.** Stage-carried moves **0.3955 → 0.1491** under the threshold she had not varied — **and the 0.12 bar is defined as HALF THE ANCHOR'S OWN READING, so both move together and the anchor cannot fail its own bar.** She withdraws the number and keeps the method.

**That is Matt's "criterion nobody can fail," reopened one axis over**, and it is the same family as the register-2 bloom gate already parked with gandalf (a gate the cathedral clears with the hero VFX switched off). **Routed to gandalf as a second instance of one class, not as a second incident** — filed separately; **not folded into the A-6 disposition, because it is not about A-6 and burying it there is how it would be lost.**

*Amended by knight-rider, 2026-08-25. § 8.3's operator is drax's, reproduced to 4 dp against two published values before any new number was derived from it. Row-level `significant_components` figures in § 8.3 are read directly from `xrow.json`'s `arms` array (48 arms, enumerated in full).*

---

# § 9 — AMENDMENT 3 (drax stage-4 return). **My own Correction #1 is half-wrong, and killing it exposes the mechanism all three of us missed: it is not an arm and not a descriptor. It is PAYLOAD SIZE.**

**Occasioned by:** drax's stage-4 completion record (`f29f12b` godot / `35bc58e8` meta), routed finding #2. **He refuted a correction I had issued against him, from source, and he was right.**

## 9.1 — The refutation, verified at source rather than accepted

He claimed my *"every pair it enters"* is false because cohorts are never pooled. **I read the operator rather than his description of it** — `reincarnated-godot/scripts/s2b_xrow_rows37.py:207`:

```python
    for i, j in itertools.combinations(range(len(arms)), 2):
        ai, aj = arms[i], arms[j]
        if ai["stage"] != aj["stage"]:
            continue                       # ⚑ COHORTS ARE NEVER POOLED
```

**Confirmed. Pairing is WITHIN-STAGE.** `single_target/water@cathedral` enters **3 of 12** row pairs, not 7 of 12 and not "every pair." His counterfactual is also correct and I reproduce it: bound all three contaminated pairs at the row max and the remaining nine still sit at mean ≥ 0.9090. **The one-arm story predicts a row mean of 1.14–1.23 against an observed 1.5987 — it undershoots by ~29 %, which is exactly how the one-pair story failed.** I replaced a story that undershot with a story that undershoots less.

**What survives of Correction #1:** *"not one pair"* — that part was right and drax accepts it. **What does not:** *"one arm."* **I did to him what jack-ryan had already caught me doing on the 1.41: I read a summary statistic and inferred a mechanism without opening the operator that produced it.** Third time this run. It is not a lapse, it is my failure mode.

## 9.2 — Then I deleted the descriptor and the arm TOGETHER, which nobody had done

Every argument so far — mine, drax's, jack-ryan's, galadriel's — has attacked **one** of the two suspects. The decisive test attacks both at once. Operator reproduced exactly (all five row means reproduce the receipt to 4 dp before anything new is derived):

**Per-row within-stage null, with `significant_components` DELETED, rows ordered by median payload:**

| row | median `authored_px` | null mean (9 desc) | **null mean (8 desc, no sig)** | null max (no sig) |
|---|---:|---:|---:|---:|
| **single_target** | **1,740** | 1.5987 | **1.0020** | 1.7043 |
| multi_projectile | 5,446 | 0.3447 | **0.3447** | 1.0262 |
| line | 11,475 | 0.4114 | **0.4114** | 0.7554 |
| melee_arc | 22,117 | 0.2426 | **0.2426** | 0.6011 |
| circle | 127,746 | 0.2330 | **0.2330** | 0.3187 |

**Four of five rows are UNCHANGED to 4 dp.** They are constant on the descriptor within-stage, so it contributes exactly zero. **The descriptor's entire footprint on the null is one row** — which is jack-ryan's 0.0 % finding generalised, and it means **option (a) "drop the descriptor" cannot rescue A-6: it moves `single_target` from 1.5987 to 1.0020 and leaves it 4.3× `circle`.**

**Then leave-one-arm-out on the no-sig row**, all eight arms:

| arm dropped | remaining mean | | arm dropped | remaining mean |
|---|---:|---|---|---:|
| `water@arena` | 1.1295 | | `fire@arena` | 0.9488 |
| `wind@arena` | 1.1211 | | **`water@cathedral`** *(the contaminated one)* | **0.9608** |
| `earth@arena` | 1.0764 | | **`fire@cathedral`** *(most influential)* | **0.8056** |
| `earth@cathedral` | 0.9993 | | `wind@cathedral` | 0.9741 |

**⚑ Delete the descriptor AND the single most influential arm and the row still reads 0.8056 — 3.46× `circle`'s 0.2330.** And the most influential arm is **not** the contaminated one: it is `fire@cathedral`, which reads `sig = 1` and is the **largest** payload in the row (2,699 px). **The row's top pair after both deletions is `fire@cathedral` × `wind@cathedral` at 1.7043 — neither arm contaminated, neither fragmenting.**

**There is no arm-level story. There is no descriptor-level story. Both suspects can be removed simultaneously and the anomaly is still 3.5×.**

## 9.3 — The mechanism, stated so it can be refuted

**`single_target` reads anomalous because its descriptors are computed on masks ~70× smaller than `circle`'s** (1,446–2,699 px vs 120,720–131,669 px), and eight of nine descriptors are **ratios of pixel counts**. At ~1,700 px a single-digit pixel change moves `fill_of_bbox`, `inner_core_frac` and `outer_shell_frac` by amounts that are structural at `circle`'s scale. **The z-score then amplifies it**: the descriptors are standardised across all 48 arms, so a quantisation wobble on a tiny mask is measured in units set by the corpus's large masks.

This is **drax's** sentence, promoted from a routing note to the mechanism of record — *"raising a mask floor does not add resolution to a 1,700 px mask; it removes pixels from it"* — converged with **galadriel's** `0.01·n` gate root cause. **They are one mechanism seen from two ends.** Neither of them stated it as the row-level explanation; both supplied the half they owned.

**⚑ What I am NOT claiming, because the table does not support it.** The rank order is monotone in payload for four rows and **inverts once**: `line` (11,475 px) reads 0.4114 against `multi_projectile` (5,446 px) at 0.3447. **Payload size is not a sufficient statistic.** `line` is also the only row reading `sig = 2` on every arm — a row-characteristic value, not fragmentation — and it carries the corpus's most extreme aspect ratios. **One inversion in five is not a law and I am not going to dress it as one.**

**Cheapest refuting test, per #19.1, and it does not need a re-mint:** recompute the eight descriptors on **downsampled `circle` masks** decimated to ~1,700 px and re-run the within-stage null. **If `circle`'s null rises toward `single_target`'s, payload size is the mechanism. If it does not, the mechanism is something about `single_target`'s shape and I am wrong.** The masks are retained; this is arithmetic on existing PNGs, not a render. **It belongs to galadriel's seam and I am filing it as a proposal, not ordering it.**

## 9.4 — What this does to the repair fork, and it narrows it

| option | status after § 9.2 |
|---|---|
| **(a) drop `significant_components`** | **Insufficient, now demonstrated rather than argued.** Zero footprint on four rows; leaves `single_target` at 4.3×. It remains *correct* — the descriptor is inverted on the count axis (§ 8.3) — but it is a separate repair that does not touch A-6. |
| **(b) invent a continuous replacement** | Still refused, still correctly (#75.5 cl. 5.6). galadriel's R-1/R-2/R-3 remain **proposed and unscored.** |
| ~~(c) re-open floor selection~~ | **Struck three times over** (§ 7.1). § 9.2 adds a fourth: the floor cannot fix a row whose anomaly survives deleting the descriptor the floor governs. |
| **(d) repair A-6's null population** | **Confirmed as the live one, and § 9 strengthens it.** If the within-row null is elevated by payload scale rather than by element variation, then **the null is not measuring what A-6's premise says it measures on small-payload rows, at any floor and with any descriptor set.** |

**The consequence for A-6 is now sharper than "UNRESOLVED."** Its null leg assumed element arms of one row are the same shape, so the null runs to ~0. **On four of five rows it approximately does** (0.23–0.41). **On the fifth it reads 1.0–1.6 for reasons that have nothing to do with element and nothing to do with the descriptor anyone has blamed.** The criterion is not merely unpopulated — **it is unpopulated in a way that is a function of row payload, which means the same criterion is stricter on some rows than others by construction.** That is the same family as the S-A3 finding routed to gandalf in § 8.5 and the register-2 bloom gate: **a bar whose difficulty is set by the thing it measures.** I am naming the resemblance and **not** merging the items — three instances of one shape is gandalf's to rule on, and I have filed the second instance separately for exactly that reason.

## 9.5 — Stage 4 itself: the acceptance condition is MET, and by a different cause than either of us expected

galadriel's condition — **cross-arm maxdiff 0 at `00-pre`, `01-windup-early`, `09-off`** — is **MET**, against her G-2 readings of 185 / 114 / 216 at `1692d6e`. 60 PNGs with `sha256.txt`; determinism 60/60 over two passes plus a third 20/20 proving comment edits inert; census green; **positive control retained at `wwcr_2026-08-25-PROBE-noneutralise/` returning `count: 1`** — drax's reason for building it is the one I want on the record: ***"'fixed' and 'blind' print the same zero."*** A gate that cannot fail is a gate nobody has tested; he tested his.

**⚑ And the neutraliser is NOT what met the condition — the CLOCK PIN is.** The probe corpus with emissive still in also returns 0; the emissive cancels exactly (158 px, ΔLum 116.62 in **both** arms). **galadriel's G-4 was asserted and is now measured, and it holds exactly.** The correct disposition is that the neutraliser is **not vindicated by this result** — it is untested by it. Recorded as such rather than banked as a win.

**Quarantine held.** No clip; SB-1 harness neither touched nor read; capture plan parameterised (`--capture=seq`, `--seq-from/-to/-every`, ffmpeg in the runner) **so the motion artifact the WW-AB experiment actually needs is a re-invocation, not a re-authoring** — which is the non-foreclosure constraint A-7 imposed, met.

## 9.6 — Two further defects in his return, both self-reported, both against himself

1. **⚑ Fourth "VERBATIM"-sentence instance.** `wwcr_stage.gd` asserts its E-0 extraction is verbatim; the ground plane diverges `60×60 no-subdiv` → `80×80 subdiv 24` (`s2a_stage.gd`'s value since `c6eede0`). **~62,048 px are void at mint and ground at HEAD.** His framing is the finding: ***"in three of four, the sibling carried a sentence asserting the parity it did not have."*** → **his discipline candidate #6, *a fix ported in prose is a fix that reads as adopted*, routes to jack-ryan.** I endorse it and add the sharpening: **the sentence is not merely wrong, it is load-bearing in the wrong direction — it is the reason nobody looked.** An unasserted parity gets checked; an asserted one does not.
2. **⚑ Third gate measuring the wrong region.** `wwcr_occlusion_gate.py`'s `enemies` region: 62,301 px of which **62,048 (99.6 %) is sky**. **Not repaired — same call as A-6, and the same call is correct.** The row's real claim is untouched (lower-body excess 1.78 % → 1.73 %) but the noise floor collapsed 2.87 % → 0.00 %: ***"the noise floor WAS the pose drift."*** → **galadriel** (instrument seam) with me.

**Three wrong-region gates and two unfalsifiable bars in one run.** I am not proposing a discipline for it here — jack-ryan holds four candidates already and this is the kind of pattern that should be minted once, from the whole set, at tranche-2 close.

## 9.7 — Disposition and routing

| item | to | when |
|---|---|---|
| **§ 9.2's two-deletion result + the payload mechanism** | **galadriel** (instrument) + **jack-ryan** (A-6's owner) | **now**, as A-10 on the dispatch |
| **§ 9.3's decimation test** — proposed, NOT ordered; refutes or confirms the mechanism without a re-mint | **galadriel** | her sequencing, after D3 pre-registration |
| **(d) — repair A-6's null population**, now with the added finding that the null's floor is row-dependent | **jack-ryan**, pre-registered before results | tranche-2 close |
| **Candidate: *a fix ported in prose is a fix that reads as adopted*** | **jack-ryan** | with the other four |
| **`wwcr_occlusion_gate.py` region split** | **galadriel** | tranche-2 close |
| **`run_s2b_e1.sh` superseded `_fxoff_` frames in the E-1 corpus** | **me** | tranche-2 close; no scored artifact consumed them |
| **Three-wrong-region / two-unfalsifiable-bar pattern** | **jack-ryan** (mint once from the whole set), **gandalf** (the bar half) | tranche-2 close |

## 9.8 — ⚑ Flags on this amendment

- **§ 9.2's numbers are mine and are newly derived.** The operator is drax's, reproduced to 4 dp against all five published row means before anything new was computed from it. **The two-deletion result and the leave-one-arm-out table appear in no agent's return, including his.** They should be re-derived by galadriel rather than adopted from me — **I have been wrong three times this run on exactly this move** (reading a statistic, inferring a mechanism), and § 9.2 is that move performed more carefully, not a different move.
- **The mechanism in § 9.3 is a hypothesis with one inversion already against it**, and I have named the test that kills it. It is not a finding.
- **`multi_projectile_count1` and `melee_strike` are singleton rows** (n=1 and n=2 arms) and contribute no within-stage null. They are excluded from § 9.2's table for that reason, not because they are clean.
- **Push:** `f29f12b` is in **`reincarnated-godot`**, which the live "push as you go" pattern **does not cover**. It stays local pending a fresh ask. `35bc58e8` and this amendment are covered and go out.

*Amended by knight-rider, 2026-08-25. drax's refutation of my Correction #1 was verified at source (`s2b_xrow_rows37.py:207`) before being accepted; his stage-4 acceptance result was verified from `sha256.txt` and the probe corpus, not from his summary.*

---

# § 10 — AMENDMENT 4 (jack-ryan D3 return, `f527995b`). **A-6 is RETIRED — refuted, not defaulted. And my § 9.3 payload mechanism is REFUTED. I verified both against the artifact rather than adopting them.**

## 10.1 — The retirement, and the test that produced it

**He found a control the corpus had been carrying the whole time and none of the four of us used: the two stages are two independent cohorts measuring the same element pairs. Every within-row null pair is a TWO-FOLD REPLICATE.** Nobody had asked whether the null reproduces.

**It does not, on any row.** Re-derived by me from `xrow.json`, not adopted:

| row | median `authored_px` | **cross-stage median relative \|Δ\|** |
|---|---:|---:|
| `line` | 11,475 | **19.2 %** |
| `circle` | 127,746 | **25.7 %** |
| `single_target` | 1,740 | **49.4 %** |
| `multi_projectile` | 5,446 | **56.8 %** |
| **`melee_arc`** | **22,117** | **76.4 %** |

**⚑ `melee_arc` — the one spec-clean row, which A-4 designates and which drax's receipt calls "the tightest invariance in the whole gate" — replicates WORST in the corpus.** Its `fire`/`water` null is **0.6011 at cathedral and 0.1610 at arena** (verified). **3.7×, on a row whose arms are specified to be the same shape.** Its stage shift dwarfs its element spread.

**That is what kills A-6, and it kills it on its own terms.** D3 required a **spec-predicate-selected** null population. The spec predicate selects `melee_arc`. **A bar carrying ~76 % relative uncertainty from a single row, consumed as a global `null_max`, is not a bar.** jack-ryan's clause and I ratify it verbatim: ***"a criterion whose null leg has no valid population is mis-specified, not suspended."***

**A-6 is RETIRED with reason recorded. Tranche 2 seals without a cross-row number rather than with a suspended one** — the disposition the dispatch pre-authorised at line 1006, reached by refutation rather than by timeout. **This is the better of the two outcomes that gate allowed**, because the reason is now known. `ANTI_TUNING_CLAUSE` survives retirement **in full**: no effect changes on the strength of any of this, and Q1–Q5 remain open — only the null-referenced criterion dies.

## 10.2 — My payload mechanism is REFUTED. Three predictions, all backwards, all verified by me.

§ 9.3 said the anomaly was mask-scale quantisation. **It is wrong, and the way it is wrong is instructive.**

1. **Leave-one-out points the opposite way.** Dropping the element across both cohorts: **`fire` → 0.6277** *(his 0.6206; 1.1 % apart, immaterial, flagged in § 10.4)*, against `water` 1.1315 / `earth` 1.1097 / `wind` 1.1390. **`fire` is the LARGEST payload in the row (2,699 / 2,548 px vs 1,446–1,813) and it is the sole driver. Dropping any of the three smaller arms RAISES the mean.** Quantisation-on-small-masks predicts the smallest dominates. The smallest are the quiet ones.
2. **The drivers are the quantisation-ROBUST descriptors.** Share of total squared distance across the twelve pairs: **`radial_mean` 28.35 % + `radial_std` 22.91 % = 51.3 %.** Those are **moments over all *n* mask pixels** — averaging suppresses per-pixel quantisation as ~1/√n. The extremum-normalised descriptors I indicted by name total **29.6 %**, and the single largest of them (`fill_of_bbox`, 16.58 %) is also an all-pixel ratio.
3. **A second inversion I had not found.** `melee_arc` (22,117 px) carries 3–4× `multi_projectile`'s (5,446 px) within-row coefficient of variation on four descriptors. **4× the payload, more variation.** I named one inversion against my own hypothesis and stopped looking; there were two.

**And his positive account is better than my negative one.** `single_target/fire` has `radial_mean` **0.4855 @cathedral / 0.4559 @arena** while the other three cluster **0.3733–0.4067 at both stages.** **Fire is genuinely a different shape, and it REPLICATES.** ***Noise does not reproduce across independent cohorts; signal does.*** **drax's original motif-swap-by-spec account was right and did not need replacing — mine included.** The rank order is still roughly payload-ordered, so the correlation may well be real; **payload is not its cause.**

**⚑ On my own conduct here.** § 9.8 flagged that § 9 was *"that move performed more carefully, not a different move"* — reading a statistic and inferring a mechanism. **It was the same move and it failed the same way.** The flag was accurate and did not save me, which is the point worth keeping: **naming a failure mode is not a control on it. The control was the replicate cohort, and it was sitting in the artifact the whole time.** **Fourth premise error of the run, and the first one I flagged in advance and committed anyway.**

## 10.3 — Sequencing: ruled, and the ruling is general

**Ruled against running the `circle`-decimation test on the scored corpus.** His test is sharper than the one I posed — not *"is it structural"* but ***"could the outcome change which criterion I choose."*** The decimation variant recomputes **the within-stage null — a term of A-6's own criterion — in corpus units.** Not structural. **Correctly withheld.**

**New binding precedent, which I ratify and route to canonical:** ***a diagnostic that recomputes a term of the criterion never qualifies as pre-registration-safe. Synthesise the input, or run it after disposition.***

**The synthetic-mask variant is authorised at any time** and he records my offering it as the right instinct. **It is also now MOOTED** — `radial_*` are scale-normalised by construction and carry 51 % of the residual, so it would very likely return "no rise," which is § 10.2's conclusion reached more expensively.

## 10.4 — ⚑ Two flags against the return, neither material

1. **His `single_target` replication figure (49.4 %) is the 8-descriptor no-sig basis; so are the other four rows.** The table is internally consistent — **but it is not labelled as no-sig, and the 9-descriptor figure for that row is 100.8 %.** A reader taking the table at face value gets the right conclusion from a basis the table does not state. **#64 FRAME FORM in miniature: the operator travelled, the descriptor set did not.** Worth one line in his canonical write; changes nothing.
2. **`drop fire` = 0.6277 by my derivation, 0.6206 by his** — 1.1 % apart, same rank, same conclusion. Not chased further; recorded so the next reader is not surprised by it.

**He also self-reported that his FIRST reading of the leave-one-out table was wrong** — cathedral/arena matching to 4 dp looked like perfect replication and is an averaging artifact; checking directly found the opposite. **That is the return's most valuable single act and it is against himself.**

## 10.5 — #80, minted once from all five candidates

He declined to mint five disciplines and minted one, and I think he is right that they are one:

> **#80 — a gate's green is not evidence until that gate has been shown to go red, on this population, in this configuration.**
> **cl. 1 — the region** (99.6 % sky in a region named `enemies`).
> **cl. 2 — the bar** — *which convicts A-6's own null leg by name.* S-A3 and the register-2 bloom gate are **named and left to gandalf, not merged.**
> **cl. 3 — drax's title verbatim**, *"a fix ported in prose is a fix that reads as adopted,"* with my sharpening as the operative half: **an asserted parity does not get checked — the sentence is a negative control that prints green by construction.**

**#75 cl. 2 already holds its mirror** (can the instrument return the *positive*?); all five candidates were the missing **negative** control. **Founding positive instance is drax's `PROBE-noneutralise` corpus, and #80 is his sentence generalised: *"'fixed' and 'blind' print the same zero."*** Canonical write lands with my #78 cl. 6 write in one edit.

## 10.6 — ⚑ Harness note: galadriel could not be amended mid-flight, and part of her task is now dead

She was dispatched in parallel with Item 1 = *specify the decimation test, do not run it.* **jack-ryan's § 2 moots that item and his § 3 authorises the synthetic variant she was being asked to rule on.** `SendMessage` does not exist in this harness (confirmed seven times against the tool surface, despite the agent-launch output advertising it), **so a running agent cannot be told that its task has been overtaken.** Her Item 2 — the `wwcr_occlusion_gate.py` region repair and the sibling-gate sweep — is untouched and is the more valuable half. **Recorded as an orchestration cost, not as a defect of hers: I fired two agents in parallel on questions that turned out to be sequential, and the parallelism is what made them unfixable mid-flight.**

*Amended by knight-rider, 2026-08-25. Every figure in §§ 10.1–10.2 was re-derived from `xrow.json` before being accepted; the two that did not reproduce are flagged in § 10.4 rather than smoothed.*

---

# § 11 — AMENDMENT 5 (galadriel return, `01cef26b`). **My two senior agents re-derived from the same source and reached OPPOSITE verdicts on the same hypothesis. They are describing the same physics. jack-ryan's premise 2 cites the correct scaling law as evidence AGAINST the mechanism that scaling law describes — and my § 10.2 retraction was PREMATURE.**

## 11.1 — The collision, stated exactly

- **jack-ryan (§ 10.2, premise 2):** `radial_mean` + `radial_std` carry 51.3 % of the residual; they are **moments over all *n* pixels**, so *"averaging suppresses per-pixel quantisation as ~1/√n"* → **quantisation-ROBUST** → **not the driver** → mechanism refuted.
- **galadriel:** log-log regression of within-row raw dispersion on median payload, excluding `line`: **`radial_std` slope −0.492, r = −0.984**; `radial_mean` −0.452. **Counting noise predicts −0.5.** `radial_std`'s `single_target`/`circle` ratio is **8.79 against √73.4 = 8.57.** → the mechanism **IS** 1/√n counting noise, **concentrated in the radial moments.**

**Both re-derived from source. Both reproduce under my own hand — I ran the regression before writing this line: `radial_std` slope −0.492, r = −0.984, ratio 8.79 vs 8.57.**

**⚑ They are the same statement.** *"Suppressed as 1/√n"* and *"scales as n^−0.5"* are one physics. **The error is jack-ryan's inference, not his arithmetic: suppressed-as-1/√n does not mean negligible, it means the noise is 8.57× larger on a 1,740 px mask than on a 127,746 px one — which is the 8.79× galadriel measured.** He named the law that predicts the effect and read it as ruling the effect out.

**This is the most instructive thing in the run and I want it recorded as such:** two Tier-A agents, same artifact, same operator, opposite verdicts, **and neither is careless.** The disagreement is not about data. It is about whether a known scaling law is a *suppression* or a *rate*.

## 11.2 — What actually survives, itemised, because "I was wrong" was too coarse

| § 9.3 claim | status |
|---|---|
| **Within-row dispersion scales with payload** | **UPHELD, and quantitatively stronger than I stated it** — I asserted a rank order; she measured an exponent against a prediction. |
| **The mechanism is 1/√n counting noise** | **UPHELD**, but I never said this — I said generic ratio wobble. **Her mechanism is not mine; it is a better one occupying the same slot.** |
| **It lives in `fill_of_bbox` / `inner_core_frac` / `outer_shell_frac`** | **REFUTED.** It lives in the **radial moments**. |
| **`outer_shell_frac` is a driver** | **REFUTED HARD.** Slope **+0.075** — the wrong *sign*. Raw dispersion 0.0057 on `single_target` vs 0.0098 on `circle`: **the corpus's second most stable descriptor on the row I claimed it destabilised.** |
| **`line` is an inversion against me** | **WITHDRAWN — it is a second effect.** Its null is carried by `aspect_major_minor`, whose raw dispersion is **0.1510 — the largest single raw dispersion anywhere in the corpus, 8.6× `circle`'s** — genuine inter-element shape variation on a row that also has a smaller payload term. **Confirmed by my own run.** |
| **"Smallest mask dominates the leave-one-out"** | **REFUTED by jack-ryan and NOT rescued by galadriel.** `fire` — the largest payload in the row — drives it, because `fire` is genuinely a different shape. |

**So the correct account is a SUPERPOSITION, and neither agent stated it:**

> **`single_target`'s null = a real shape difference in `fire` (signal — it REPLICATES across cohorts) SITTING ON a payload-scaled noise floor (counting noise — it does NOT replicate).** jack-ryan measured the first and concluded the second was absent. galadriel measured the second and did not address the first. **Both measurements are right. Both exclusions are wrong.**

**⚑ And jack-ryan's replication test is the discriminator that proves it, used against his own conclusion:** noise does not reproduce across independent cohorts, signal does. **`fire`'s `radial_mean` reproduces (0.4855 / 0.4559). The row-level null does not (49.4 %).** That is exactly what a superposition predicts and neither a pure-signal nor a pure-noise account does.

## 11.3 — ⚑ My § 10.2 retraction was premature, and the way it failed is the same way, a fifth time

**I verified jack-ryan's three arithmetic claims — all three reproduced — and did not check the INFERENCE drawn from claim 2.** I checked that 51.3 % was 51.3 % and not whether "all-pixel moment ⇒ quantisation-robust" follows. **It does not.**

**This is the fifth instance of one failure mode and the second in consecutive amendments**, immediately after I wrote *"naming a failure mode is not a control on it."* **It still is not.** The refinement I can actually use: **my verification habit terminates at numbers.** Every catch this run came from re-deriving a figure; every miss came from accepting a *sentence* that sat next to a figure I had confirmed. **Confirming an agent's arithmetic licenses nothing about their reasoning, and a verified number beside an unverified inference reads as a verified claim.** That is drax's *"a fix ported in prose is a fix that reads as adopted"* pointed at a reviewer instead of a codebase — **and it is #80 cl. 3 operating on me.**

**§ 10.2 stands as written, struck where § 11.2 corrects it, per #79 cl. 5.** I am not editing the retraction away; being wrong twice in opposite directions is the record.

## 11.4 — Does A-6's retirement survive? **YES — and galadriel STRENGTHENS it.**

**The retirement does not rest on the mechanism.** It rests on the null failing to reproduce across cohorts, worst on the one spec-clean row (`melee_arc`, 76.4 %). **galadriel does not contest that and nothing in § 11 touches it.**

**And she supplies a second, independent reason A-6 is mis-specified:** if the within-row null floor **scales as n^−0.5**, then a **global `null_max` consumed across rows spanning 1,740 → 127,746 px is comparing bars that differ by ~8.6× in noise floor by construction.** A-6 was not merely unpopulated — **it was un-poolable.** Two independent refutations, from two agents, neither aware of the other's. **A-6 is RETIRED and the retirement is now over-determined.**

## 11.5 — Item 2: **⚑ my premise was half-wrong and the verdict MOVES — PASS → FAIL, on both corpora**

I told her the repaired region *"does not move any verdict."* **That was true of the LOWER-BODY claim and never established for the ENEMY claim** — drax measured the defect; nobody measured the repair. Thresholds carried verbatim, neither re-tuned:

| corpus | | lower | enemy |
|---|---|---|---|
| mint | OLD | 1.78 % PASS | 0.01 % PASS |
| mint | **NEW** | **5.47 % FAIL** | **23.01 % FAIL** |
| HEAD | OLD | 1.73 % PASS | 0.00 % PASS |
| HEAD | **NEW** | 1.38 % PASS | **26.98 % FAIL** |

**Root defect is `actor`, not the complement:** it reads *"differs from the floor colour,"* so the **darker void is admitted**; the box then cannot exclude it. **Two composing errors.** Repair: actor must be **brighter** than floor, split by **connected component** not by box. Denominator **50,840 → 1,705 px**; ledger resolves to caster (972 px) + exactly four mobs. The mint's lower-body flip is **drax's own predicted failure realised** — the old `lower` pooled caster with mobs.

**Her disposition, which I ratify and which is the important part: this is NOT "the row fails."** The 20 % bar was calibrated against a 99.6 %-sky denominator, so **the repaired FAIL is as uninterpretable as the original PASS. Third instance of the bar-set-by-what-it-measures class.** The region is adopted only with a **re-derived bar, derived before the repaired number is looked at again** — a pre-registration act, **jack-ryan's, not hers**. She declined to set it. Correct.

**What IS newly known and is a real finding: ~27 % of true enemy-silhouette pixels change at `05-sustain`, on both corpora — the exact failure the row exists to correct, which the gate was structurally incapable of seeing.**

## 11.6 — Sibling scan: **NO FOURTH**, and the counter-example is by the same hand

`wwcr` is the **only** gate hardcoding a frame-relative box. `cj_gate:152` / `sa_gate:209` boxes are world-projected with no denominator; complement regions are count-only (`quiltfix:138`) or content-derived (`s2b_rows12:437`, `s2b_stagemetrics:238`).

**⚑ `s2b_rows12` and `rows37` — drax's own — derive regions from engine geometry AND print the denominator beside the fraction. `wwcr` did neither, and the absence of that one integer hid 62,048 px of sky for an entire run.** Routed to jack-ryan as **ratification of existing practice, not a new discipline** — the practice already exists in this codebase and has been right the whole time.

**Her closing line is the run's thesis and I am putting it in the record verbatim:** *"every bar in this run that could not be failed was measured against a region chosen for convenience. The sky was not an error of arithmetic. It was an error of not printing the denominator."*

## 11.7 — Disposition

- **T-1 fires** — synthetic parametric shapes at the corpus's own payload ladder, k=4 arms per rung, shape held **exactly** constant while payload varies. **Zero corpus data, zero hazard, authorised by jack-ryan at any time, ~60 lines, minutes.** It is the decisive discriminator between two Tier-A agents and **the outcome is engine-level**: if descriptor dispersion scales n^−0.5, **every future cross-row instrument comparing effects of different payload size carries a built-in bias.** Engine first.
- **T-2 (corpus-side) does NOT fire**, and her correction to my spec is accepted: random decimation destroys connectivity and is not the physical situation — **a mask smaller on screen is not a mask with pixels deleted.** Area-downscale + re-threshold, and only after disposition.
- **My synthetic worry was unfounded and she explained why I was wrong to have it:** the halo structure drives `significant_components`, which is **excluded** from the eight descriptors under test. **I worried about a contaminant that is not in the experiment.**
- **Her correction on `count1`:** its `sig = 4` is evidence for her `0.01·n` **gate** mechanism, **not** the payload mechanism — `sig` is excluded from the null being explained. **Two mechanisms keyed to small *n*; I pooled them and she unpooled them.** Accepted.
- **The bar re-derivation for the repaired enemy region → jack-ryan**, pre-registered before the repaired number is looked at again.
- **R-1 / R-2 / R-3 remain proposed and unscored.** Third time that ordering has held under pressure.

*Amended by knight-rider, 2026-08-25. The regression in § 11.1, the `outer_shell_frac` sign, and `line`'s 0.1510 aspect dispersion were re-derived by me from `xrow.json` before this section was written. Where two agents disagree, both were reproduced rather than one adjudicated on authority.*

---

# § 12 — AMENDMENT 6 (jack-ryan, `1cc2c5f8`). **He concedes premise 2 and finds a WORSE defect in it than I did. Then he attacks the other side and lands two of three. And I broke his pre-registration by handing him the numbers.**

## 12.1 — His concession is sharper than my charge

I said premise 2 confused a *rate* for a *suppression*. **He says the defect is worse and he is right:**

> **1/√n is common to EVERY all-pixel descriptor — including `fill_of_bbox`, which he flagged as an all-pixel ratio in the same sentence. A law that applies equally to both sides cannot discriminate, and discrimination was the entire work premise 2 was doing.**

**It was not over-strong. It was irrelevant to its own conclusion.** His summary — *"I got a defensible verdict from an argument that could never support it"* — is the cleanest self-assessment anyone has filed this run.

## 12.2 — Then he attacks galadriel's side. **Two of three land. I verified all three.**

**(a) The exponent is SELECTED, not measured. — LANDS, with one mitigation he does not address.** All eight slopes, line-excluded, re-derived by me:

| descriptor | slope | \|dist from −0.5\| |
|---|---:|---:|
| `inner_core_frac` | −0.596 | 0.096 |
| **`radial_std`** | **−0.492** | **0.008** |
| `radial_mean` | −0.452 | 0.048 |
| `largest_component_frac` | −0.391 | 0.109 |
| `aspect_major_minor` | −0.362 | 0.138 |
| `fill_of_bbox` | −0.321 | 0.179 |
| `major_over_diag` | −0.156 | 0.344 |
| `outer_shell_frac` | **+0.057** | 0.557 |

**Corpus mean = −0.339** (his ≈ −0.34, exact). **`radial_std` is the descriptor of eight nearest −0.5, reported as a hit against −0.5.** Ratios span 0.59 → 19.10 around the 8.57 prediction, and **estimator choice alone moves the slope −0.492 → −0.457** — the claimed 1.6 % agreement sits inside the analyst's-choice band. **⚑ The mitigation he skips: galadriel selected the radial pair on an INDEPENDENT criterion — their 51.3 % share of the residual, which HE computed — and only then found the exponent. That is a conjunction, not a slope-hunt.** It weakens (a); it does not clear it.

**(b) Payload and shape are perfectly confounded. — LANDS, and is unanswerable from this corpus.** Four rows, each one shape class, one payload. **Nothing in the artifact separates "bigger mask, less noise" from "bigger mask, converged shape." This is why T-1 exists and why it is decisive.**

**(c) The per-row replication test. — ⚑ DOES NOT DISCRIMINATE, and his own framing is what shows it.** His table reproduces exactly:

| row | px | mean r |
|---|---:|---:|
| `single_target` | 1,740 | +0.525 |
| `multi_projectile` | 5,446 | +0.687 |
| `line` | 11,475 | +0.512 |
| **`melee_arc`** | 22,117 | **−0.075** |
| `circle` | 127,746 | +0.221 |

**But rank correlation is SCALE-FREE. It measures signal-to-NOISE, not noise.** His load-bearing case is `melee_arc`: *spec'd shape-constant, therefore its dispersion IS noise, therefore r ≈ 0 at 12.7× `single_target`'s payload refutes a payload-scaled floor.* **A row with no signal returns r ≈ 0 whether its noise is enormous or vanishing.** Zero signal over any noise is zero. **`melee_arc`'s r ≈ 0 is predicted by "shape-constant by spec" alone and carries no information about noise magnitude.**

**The test that DOES bear on it is absolute dispersion, and I ran it.** `radial_std`, anchored on `single_target`, against the n^−0.5 prediction:

| row | obs | pred | **obs/pred** |
|---|---:|---:|---:|
| `single_target` | 0.00784 | — | 1.00 *(anchor)* |
| `multi_projectile` | 0.00318 | 0.00443 | **0.72** |
| `line` | 0.00100 | 0.00305 | 0.33 *(second-effect row)* |
| **`melee_arc`** | **0.00170** | **0.00220** | **0.77** |
| `circle` | 0.00089 | 0.00091 | **0.97** |

**`melee_arc` — his refuting case — sits at 0.77 of the payload-law prediction.** Excluding `line`, the fit spans 0.72–1.00 across a **73× payload range.** **That is not decisive either**, but it points the opposite way from (c), and **(c) cannot be the reason to reject the mechanism.**

## 12.3 — His verdict, which I adopt over my own § 11.2

> **Superposition of signal + a NON-REPLICATING component: ESTABLISHED** (by the replication test, independent of galadriel).
> **That the component is payload-scaled counting noise: NOT ESTABLISHED.**
> **"You un-retracted to the second when only the first was earned."**

**Correct, and § 11.2's "UPHELD, quantitatively stronger" is hereby downgraded to: UPHELD IN DIRECTION; MECHANISM OPEN; T-1 DECISIVE.** I have now overstated this hypothesis, retracted it, and over-restored it. **Three swings on one question is the signature of an agent adjudicating between specialists on evidence rather than routing to the instrument that settles it. T-1 is running.**

**⚑ And he ran an attack that failed and reported it:** including `line` moves `radial_std` from −0.492 to **−0.484**. **The post-hoc exclusion buys r, not slope. galadriel's exclusion is honest.** He planned to convict her of it and published the acquittal.

## 12.4 — ⚑ **I broke the pre-registration in the act of requesting it**

**I handed him 23.01 % / 26.98 % in the same message that asked him to pre-register a bar blind to them.** He is contaminated on the area observable and says so. **Third instance of the "bar set by what it measures" class this run — committed by me, inside the repair of the second.** There is no version of this that is not my error: **I pasted the results into the request for the pre-registration.**

**His recovery is the right kind and I want it recorded as such — he did not claim to be uncontaminated. He found an observable he is still blind on:**

`wwcr_occlusion_gate.py:179–192` **already computes an edge mask** (dilate-minus-erode) **and passes it to the report — then scores the AREA mask at :197. Readability is an outline property. No one has ever seen an edge number, so pre-registration on it is intact.**

**Bar registered before any edge number is computed** (#80 cl. 2(a)): `excess_edge > floor_mean + 3·floor_sd` over inert frames on the repaired region, **k = 3 fixed**; **< 5 inert frames ⇒ UNEVALUABLE, not PASS**; **denominator printed beside the fraction.** Replaces `max()` at :202–207 and the literal `20.0` at :214.

**Do not retire the gate** — ~27 % of *true* silhouette pixels changing is the defect the row exists to catch. **Re-specify the observable.** Ratified.

## 12.5 — #80 canonical write landed

**cl. 4** = galadriel's sibling finding, ratified as **existing practice applied uniformly, not a new obligation** (drax's `s2b_rows12`/`rows37` derive regions from engine geometry *and print the denominator beside the fraction*).

**⚑ cl. 3(a) added, on my proposal, against my conduct: it names REVIEWERS explicitly.** *A fix ported in prose is a fix that reads as adopted* now covers **a verified figure sitting beside an unverified inference.** That is the fifth-instance failure mode from § 11.3, minted as a rule that applies to me.

Canonical: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (`1cc2c5f8`).

## 12.6 — Standing

**A-6 stays RETIRED.** Nothing in this amendment touches the ground it rests on. **T-1 is the only open instrument and it is running.** If it returns flat, the payload mechanism dies for the third and final time and §§ 9.3 / 11.2 are wrong; if it returns slope ≈ −0.5 with shape held exactly constant, **(b)'s confounding is broken and the mechanism is established.** Either way the answer arrives from an instrument rather than from me arbitrating two specialists.

*Amended by knight-rider, 2026-08-25. All three of his attacks were re-derived before disposition; the obs/pred table in § 12.2(c) is mine and is the reason (c) does not carry.*

---

# § 13 — AMENDMENT 7 (galadriel T-1, `fd6b4f24`). **T-1 CONFIRMS, and it confirms the SUPERPOSITION — the account neither specialist held. Both of them were right about the row they were looking at.**

## 13.1 — The instrument, verified before the result

`agentic_orchestration/galadriel/pipeline/t1_payload_scaling.py`. **`descriptors` is imported via `importlib` from `~/Games/reincarnated-godot/scripts/s2b_xrow_rows37.py:53` — not retyped. I checked the import, not her description of it.** The two are one function. **Zero corpus data; the only corpus input is the published payload ladder.** Receipt reproduces her reported figures exactly under my own read.

**She ran TWO conditions where I specified one, and the second is what makes this decisive.** **A** = sub-pixel phase only, **true shape difference exactly zero**. **B** = ±2° / ±1 % real shape perturbation on top. k = 4 at the corpus cohort size; **60 replicates, because a 4-arm null is 6 pairs and is itself a noisy estimate.** I did not ask for the replication and it is the difference between a number and a measurement.

## 13.2 — Condition A: the noise limb is real, and jack-ryan's (a) and (b) both fall

**Monotone on all four shape families. Slopes −0.514 / −0.517 / −0.633 / −0.663, r = −0.995 … −1.000.** Radial moments **−0.564 / −0.582** against the −0.5 prediction. **Endpoint ratios 8.65× and 9.19× against √73.4 = 8.57×.**

- **(a) "the exponent is selected" — ANSWERED.** Four shape families, pre-specified prediction, r ≈ −1.000. **You cannot slope-hunt across a family you generated.**
- **(b) "payload and shape are perfectly confounded" — BROKEN, which is exactly what T-1 was built to do.** Condition A holds shape **exactly** constant while payload varies over 73×. **The confounding that is unanswerable in the corpus is absent by construction here.**
- **(c) was already shown not to discriminate** (§ 12.2).

**The payload mechanism is ESTABLISHED.** Not "upheld in direction" — established, on an instrument with no corpus data in it.

## 13.3 — ⚑ And the superposition is MEASURED. This is the finding.

Noise and a real shape difference are **independent contributions to a Euclidean distance, so they add in quadrature**, not linearly. She decomposes **S = √(B² − A²)**:

| family | A slope (**noise**) | **S slope (signal)** | B/A @ 128k | B/A @ 1.7k |
|---|---:|---:|---:|---:|
| elongate | −0.514 | **−0.081** | **3.64×** | 1.11× |
| scatter | −0.663 | **+0.028** | **5.44×** | 1.05× |
| lobed | −0.517 | −0.145 | 1.40× | 1.02× |
| blob | −0.633 | −0.222 | 1.29× | 0.86× |

> **The noise limb falls at n^−0.5. The signal limb is flat.**

**Crossover n\* = 9.0k – 32.9k px — INSIDE the corpus's own ladder.** `single_target` (1,740 px) sits far **below** it; `circle` (127,747 px) far **above**.

**⚑ Her sentence is the resolution of the entire collision and I am putting it in verbatim:** ***"jack-ryan and I were each measuring the limb that dominates the row we looked at."***

**Neither specialist was wrong. Each generalised from the regime they sampled.** jack-ryan looked at `fire@cathedral` — a real shape difference on a row below crossover where B/A ≈ 1.05–1.11, so signal is what he saw. galadriel regressed across the ladder, which is dominated by the noise limb. **The superposition I proposed in § 11.2 is the account, and it is now measured rather than asserted.**

**⚑ Flag, mine, against the result I just accepted:** the **S-limb regressions are weakly fit** — r = −0.693 / +0.230 / −0.622 / −0.761 — against condition A's r ≈ −1.000. **"The signal limb is flat" is inferred from a POOR fit to a power law, not from a good fit to a flat line.** That is consistent with a size-independent constant plus estimation noise — which is what it should look like — **but it is weaker evidence than the A limb and the table's presentation does not distinguish them.** The finding stands; the asymmetry in evidential strength should travel with it.

## 13.4 — Two corrections she filed against herself, and the second is a third instance of the run's thesis

1. **Her own confirm band was wrong.** She pre-specified *"1.4k reads 3–8× 128k"* — **below the prediction her own mechanism makes (√73.4 = 8.57×).** Applied literally, **it would have called a dead-on 9.19× an overshoot and rejected a correct result.** ⚑ **That is #80 pointed at a pre-registration: a band that could convict the truth.** The band was wrong, not the result. **She caught it herself, in the return that used it.**
2. **Her third discriminator FAILED, and the failure is more informative than the success.** She had said *"if `outer_shell_frac` stays flat, § 1.3 is confirmed independently."* **It does not stay flat — it reads −0.593, like everything else.** So its corpus **+0.075 is NOT quantisation immunity**; it is a descriptor whose **signal term outweighs its noise term even at 1,740 px.** **Her conclusion (not a driver) stands; her reason for it is refuted.**

**⚑ And that is a SECOND, INDEPENDENT instance of the superposition visible in the corpus itself:** `outer_shell_frac`'s **+0.075** is the **pure-signal limb**, sitting in the same corpus beside `radial_std`'s **−0.492** noise-dominated limb. **The two descriptors I and jack-ryan each argued from were the two limbs, and neither of us noticed we were holding one each.**

## 13.5 — Standing after T-1

- **A-6 stays RETIRED, now on THREE independent grounds:** cohort non-replication (jack-ryan); un-poolability across payload (galadriel, corpus); **and now T-1's measured n^−0.5 noise limb with crossover inside the corpus ladder.** Her engine-level statement is ratified: **any cross-row instrument pooling a null across payloads spanning ~10× compares bars at different noise floors by construction.**
- **§ 9.3's direction: VINDICATED. § 9.3's descriptor attribution: REFUTED and it stays refuted** — I named `outer_shell_frac`, which is the *signal* limb, i.e. **I picked the one descriptor of eight that is the counter-example to my own mechanism.**
- **§ 12.3's downgrade is itself upgraded:** *upheld in direction / mechanism open / T-1 decisive* → **mechanism ESTABLISHED.** jack-ryan's calibration was correct **at the time he made it** and T-1 is what moved it. **That is the ordering working: he refused to let me bank an unearned conclusion, and the instrument settled it two hours later.**
- **T-2 does not fire.** Nothing needs it.
- **She set no bar.** Third time she has declined to set one. Correct each time.

*Amended by knight-rider, 2026-08-25. The `importlib` import at `t1_payload_scaling.py:53` and every figure in §§ 13.2–13.3 were verified from the instrument and its receipt before this section was written. § 13.3's flag on the S-limb fit quality is mine and is against the result I am accepting.*

---

# § 14 — The basis. **The instrument was compliant the whole time. The unregistered operator is OURS, it is in this document four times, and the descriptor we informally dropped carries 82 % of the null.**

**Appended 2026-08-25. This is the third time the 8-vs-9-descriptor ambiguity has cost someone a re-derivation in this run** — mine in § 9.3, jack-ryan's in his instance 4, and a third in the cross-stage ratio table below. **I went looking for a missing label on the instrument. It is not missing. The defect is entirely analysis-side and I am one of the two analysts.**

## 14.1 The receipt declares its basis — three ways, not one

Read out of `harness_logs/s2b_rows37_2026-08-24/xrow.json` directly:

| field | content |
|---|---|
| `operator` | *"z-scored euclidean **over 9 dimensionless shape descriptors** of the authored-pixel mask…"* |
| `descriptors_in_distance` | **all nine, by name**, `significant_components` among them |
| `descriptor_excluded_and_why` | `authored_px` — *"raw, non-portable… the error class that produced ~12 %, ~20 % and 9.35 %"* |

**The instrument states its count, enumerates its members, AND documents what it excluded with the reason.** That is more than #64 asks of a quantity. **There is no repair owed here and I want that on the record before the rest of this section, because I filed the question expecting to find an instrument defect.**

## 14.2 Where the eight came from — nobody excluded it; it had nothing to say

`galadriel/pipeline/t1_payload_scaling_result.json`, `per_descriptor`:

```json
"significant_components": { "slope": null, "note": "constant" }
```

**T-1 runs the same operator** (`operator_source` names `s2b_xrow_rows37.py`) **on all nine.** On synthetic masks the ninth is **constant** — each family produces the same component count — so it contributes nothing to a scaling regression, and the receipt says so honestly rather than dropping it silently. **That is #63(c) again, and it is why the receipt is not at fault.**

**What happened next is the whole defect: we carried "the eight" back out of the synthetic experiment and into statements about the REAL corpus,** where it is not constant at all.

## 14.3 ⚑ Of all nine, it is the worst one to have informally dropped

`xrow.json` → `NULL_COMPOSITION.noise_setting_pair.descriptor_share_of_squared_distance`:

| descriptor | share of squared distance |
|---|---:|
| **`significant_components`** | **0.8165** |
| `radial_mean` | 0.0525 |
| `radial_std` | 0.0473 |
| `largest_component_frac` | 0.0332 |

**The descriptor that is inert in synthetic is 82 % of the null in the corpus.** The derived basis does not shave a small term off the distance — **it removes four-fifths of it, precisely in the pair that produced the contamination this ruling is named after.**

## 14.4 The consequence, measured, and the canonical ranking INVERTS

Re-derived from `xrow.json`, per row, median `authored_px` and the within-stage null on each basis:

| row | median `authored_px` | null **9d** | null **8d** | cross-stage ratio **9d** | cross-stage ratio **8d** |
|---|---:|---:|---:|---:|---:|
| `single_target` | 1,740 | **1.5987** | **1.0020** | **2.99** | **1.50** |
| `multi_projectile` | 5,446 | 0.3447 | 0.3447 | 2.45 | **2.45** |
| `line` | 11,475 | 0.4114 | 0.4114 | 1.20 | 1.20 |
| `melee_arc` | 22,117 | 0.2426 | 0.2426 | 1.83 | 1.83 |
| `circle` | 127,746 | 0.2330 | 0.2330 | 1.06 | 1.06 |

**`single_target` is the ONLY row that moves between bases** — because it is the only row holding the contaminated `sig = 3` arm (`water@cathedral`; arena reads 0.8010 on both bases, cathedral goes 1.2029 → 2.3965). **Four rows are basis-invariant to the digit, which is exactly what makes the ambiguity survivable long enough to bite three times.**

**And the headline ranking flips.** On the registered 9d basis, **`single_target` is the most cross-stage-variable row of the tranche (2.99).** On the derived 8d basis it is **fourth of five (1.50)** and **`multi_projectile` (2.45) takes the top.** ~~**The same receipt, the same arithmetic, opposite canonical statements — distinguished only by an operator neither analyst wrote down.**~~ **⚑ STRUCK 2026-08-25 on jack-ryan's ruling, and the strike is the point of § 14.8: there are NOT two canonical statements. `single_target` at 2.99× IS the tranche's most cross-stage-variable row — that is the registered reading and it stands. The 8d ordering is unregistered arithmetic, and by writing "opposite canonical statements" I granted it standing in the same breath as convicting it.**

## 14.5 ⚑ This document uses both bases, and only one of them is registered

`grep` against my own ruling: **four occurrences treat the basis as eight** (§§ at lines 309, 501, 535, 650 — *"the eight descriptors"*, *"the descriptor of eight"*, *"the one descriptor of eight"*), while **line 303 correctly says "eight of nine descriptors are ratios of pixel counts."** **I wrote both, in one file, without noticing.**

**Worse, line 501's reason is wrong in a way I already convicted someone else for.** I wrote that `significant_components` is *"**excluded** from the eight descriptors under test."* **It is not excluded. It is inert.** The conclusion that section reaches — my synthetic-halo worry was unfounded — **survives**; the reason given for it does not. **That is the same shape as galadriel's `outer_shell_frac` discriminator in § 13.4: right conclusion, refuted reason.** I ratified that finding against her two sections before committing the identical error, and I did not see it until I read my own file with `grep`.

**Corrected form of line 501:** the halo structure drives `significant_components`, which is **present in the operator and measures constant on the synthetic masks**, so it cannot carry the contaminant into T-1's slopes.

## 14.6 What I am NOT doing to the rest of this ruling

**Not re-deriving the 8d figures. They are correct as arithmetic and wrong only as unlabelled arithmetic** — and rewriting them would erase the evidence that the ambiguity was live in a document that spent 650 lines being careful (#79 cl. 5, the same principle that kept twenty PNGs on disk one ruling over).

**Nothing in A-6's disposition moves.** Its three retirement grounds — cohort non-replication, un-poolability across payload, T-1's n^−0.5 noise limb — **are each basis-independent**, and I checked that rather than assuming it: the T-1 slopes are per-family regressions over the full operator, and one inert term cannot change an exponent.

## 14.7 Offered to jack-ryan — a mint I am NOT asserting

**Candidate, and I think it is a small one:** *#64 FRAME FORM makes a **denominator** travel with a **number**. The same obligation attaches to an **operator**: a distance reported on a basis other than the receipt's declared one must name the basis on the same line, and a basis derived by an analyst is not a basis until it is written down.*

**It may not need a number.** It plausibly reads as **#80 cl. 1** — a derived basis is a region nobody printed the composition of — and cl. 1 is already minted. **His call, and the evidence for it is this section rather than my argument for it:** three analysts, one instrument that did everything right, and an operator that existed only in our heads until 82 % of a null went missing three times.

*Appended by knight-rider, 2026-08-25. Verified before writing: `xrow.json` (`operator`, `descriptors_in_distance`, `descriptor_excluded_and_why`, `NULL_COMPOSITION.noise_setting_pair.descriptor_share_of_squared_distance`, and the per-row nulls on both bases), `t1_payload_scaling_result.json` (`per_descriptor.significant_components`, `operator_source`), and a `grep` of this file for its own basis-count usage. **The `grep` is the only reason § 14.5 exists — I did not remember writing "of eight" and would have denied it.***

## 14.8 — jack-ryan's disposition: **mint DECLINED, and he refused my framing twice. Both refusals were right and the second one convicts THIS section.**

Returned at `aa332c6a` (`reincarnated-engine`), re-verified by him against both receipts before writing. Read at source, not from his summary.

**Refusal 1 — the defect I reported does not land as stated.** I told him instance 4 was mis-stated because it treated the instrument as ambiguous. **It never did.** Every conviction in that text is aimed at his own sentence. **On instrument-exoneration the existing text already survived, and I had constructed a defect out of my own framing of the question rather than out of the text.**

**Refusal 2 — ⚑ the real defect was worse, and I committed a milder form of it in § 14.4 while reporting it.** Instance 4 called the derived basis **"the clean basis"** and stated the inversion **in the indicative**, which grants canonical standing to an operator nobody registered — in a *discipline file*, making the unregistered ranking the one a future reader cites. He repaired it to *"that second basis"* with conditional verbs and **restored the registered ranking**.

**And § 14.4, as I first wrote it, said the two bases produce "opposite canonical statements."** There are not two canonical statements. **There is one registered reading and one piece of unregistered arithmetic**, and I put them on equal footing in the sentence whose entire job was to say they are not. **Struck above rather than silently rewritten** (#79 cl. 5) — this is now the *second* time in one section that I reproduced the error I was documenting, after § 14.5's right-conclusion-wrong-reason. **A section about an unregistered operator committed the operator's own error twice while describing it.** I do not have a tidy account of why; the honest report is that both were caught by mechanical checks (`grep`, and another agent's read) and neither by me re-reading my own prose.

**The mint: DECLINED per #58-DECLINED**, and my own suspicion in § 14.7 was right — it decomposes with nothing left over. **Reporting limb → #64** (the basis travels on the same line). **Derivation limb → #80 cl. 1** (a quantity is a claim about the set it is taken over).

**⚑ But he pushed back on "it's just a citation" too, and this is the part worth carrying:** he logged it as **#80 cl. 1's SECOND founding instance — and its first with no script involved.** `wwcr_occlusion_gate.py` took its *region* from a frame-relative box; **three analysts took an *operator's basis* from a synthetic experiment's incidental constant.** Same shape, no code, different agents. **Until now cl. 1 had one instance and read as one gate's bug; it now reads as a class.** His sentence: *"§ 14 did not just fail to mint — it supplied the evidence that an existing clause was under-scoped."* **That is a better outcome than a number and I would not have got there; I was arguing about whether the proposition was new.**

**One correction he filed in my favour, recorded because refusing credit is its own distortion:** on § 14.5 he ruled that the wrong-reason line is a genuine #78 cl. 6 hit, but **the sweep that caught it is #72 executed against myself** and is not a breach. **I am not claiming more than that** — the sweep was run because I had already been wrong five times this run, not from foresight.

*Appended by knight-rider, 2026-08-25, from `aa332c6a`'s diff read directly. ⚑ **And the cwd hazard I documented in `CLAUDE.md` forty minutes ago fired again while writing this section** — a `grep` for my own file returned "No such file or directory" because the shell was still in `reincarnated-engine`. **`pwd` first caught it in one call.** First recording cost an imagined disappearance; second cost nothing. That is the only evidence the note works.*
