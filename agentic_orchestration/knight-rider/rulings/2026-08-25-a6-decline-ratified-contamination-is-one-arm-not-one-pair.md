# KR ruling — A-6 UNRESOLVED: **the DECLINE is RATIFIED.** And the contamination is **one ARM, not one pair** — drax's own receipt carries a cross-stage control that settles it.

**Ruling by:** knight-rider, 2026-08-25
**Routed to me by:** drax, s2b stage-3 return (`drax/v0.1-s2b-rows-3-7`, `d9e908c`) — mint note § 9.9, `xrow.json` § `A6_CRITERION_STATUS.routed` = *"knight-rider + jack-ryan as an INSTRUMENT finding."*
**Verified from:** `reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/xrow.json` — the `arms` array and `NULL_COMPOSITION` block, read directly. **Not from the mint note's summary of them.**

---

## 1. The ruling, in four clauses

1. **The DECLINE STANDS and is RATIFIED.** A-6 is emitted `UNRESOLVED`, not `FAILED`. **No row is convicted of failing to separate.** Nothing routes to gandalf as an L-29 fold finding. The `ANTI_TUNING_CLAUSE` holds in full: **no effect is changed on the strength of this number, by anyone, in any tranche.**
2. **drax's refusal to repair the instrument in-session is CORRECT and is ratified as-reasoned.** Inventing a continuous descriptor after seeing the number it would move is #75.5 cl. 5.6 inverted. He named the hazard and stopped at it. That is the conduct the clause exists to produce.
3. **His CHARACTERIZATION of the contamination is wrong, and the correction changes the repair.** It is not *"ONE PAIR of ONE ROW."* It is **one ARM** — `single_target/water` — contaminating **every pair it enters**. § 2 below.
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
