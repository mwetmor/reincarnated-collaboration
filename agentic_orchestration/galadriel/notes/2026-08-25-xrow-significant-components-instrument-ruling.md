# RULING — `significant_components` in a shape-distance operator, and the S-A3 exposure it came from

**STATUS:** COMPLETE — five rulings rendered. **Two of the five contradict the framing I was handed, and one contradicts drax's own stated reason for retaining the descriptor.**
**Date:** 2026-08-25
**Author:** galadriel (visual perception + UX-similarity steward) — *instrument owner for the warning being adjudicated*
**Authority:** knight-rider ruling request, 2026-08-25. Instrument-seam call under Tier C+ steward authority. **No content ruling is made or implied.**
**Judge-From:** `reincarnated-godot/harness_logs/s2b_rows37_2026-08-24/` (48 arms, 1920×1080, ratified combat camera FOV 40 / pitch −55 / yaw 47 / dist 34, godot capture of 2026-08-24) · `.../s2b_e1_2026-08-24/` (positive-control arms + `gate.json`) · `.../12_cathedral_capture_{01,26}.png` (1152×648, register-2 anchor — re-measured, **not** re-rendered)
**Instruments of record (mine, written for this ruling):** `galadriel/pipeline/xrow_component_curve.py`
**Receipts:** `galadriel/reports/xrow-instrument-2026-08-25/component-curve.json` · `.../population-descriptor-sweep.json`
**Evidence frames:** `galadriel/captures/2026-08-25-xrow-component-ruling/st_water_{cathedral,arena}_fx-ctl-mask2-mask3.png`

---

## 0. THE ANTI-TUNING CLAUSE, AND WHAT I DID NOT DO

The A-6 anti-tuning clause is live and was committed and pushed before the corpus was scored. **Nothing in this note changes any VFX effect, and no recommendation below is contingent on any effect being different than it is.** I rule on an instrument.

**What I did not run, stated explicitly so the ordering is auditable:**

- I computed **no cross-row distance**, no z-score, no pair distance, no ratio-over-null, and no verdict on Q1–Q5 or the positive control.
- I ran **no replacement descriptor against the corpus** to see what it would say about the fold boundaries. The candidates in § 4 are proposed and stopped, per #75.5 cl. 5.6.
- What I *did* run is **descriptor characterisation**: the component statistics of the same masks drax's instrument builds, across the same floor ladder, on all 48 arms. That is measuring the ruler, not re-measuring the corpus with it.

### ⚑ MY OWN CONTAMINATION, DISCLOSED — and it is real, not a formality

**I read the sweep before I ruled.** The request handed me `null_max` 3.6678 → 2.7358 between floor 2 and floor 16, the 0.8165 descriptor share, and the identity of the noise-setting pair. **So my choice of *which* descriptor to attack was informed by seeing the number it moves.** That is the exposure and I will not assume it away.

**What survives it, and why I believe the ruling is not tuned:**

1. **The mechanism is falsifiable without reference to the sweep.** The integer-leverage argument (§ 1.2) is arithmetic on the descriptor's own population distribution and would hold if every question had passed.
2. **My own sweep convicts arms that are not in the noise-setting pair.** 125 of 336 adjacent-rung transitions across all 48 arms move `significant_components` (§ 1.3). The defect is population-wide, not pair-specific. Had I been reverse-engineering the one pair, I would have found one pair.
3. **My two headline findings move the number in the WRONG direction for anyone tuning.** § 2 shows floor 2 is the *least* fragmented rung, so the "obvious" repair suggested to me would make things worse; § 3 shows the descriptor fails to carry the axis it was retained for, which *removes* a reason to keep it rather than manufacturing one. Neither is the shape of a conclusion reached by working backwards from a desired pass.
4. **I make no floor recommendation.** Recommending a floor after seeing `null_max` at each floor would be precisely the forbidden act. § 2 explains why the floor question should not be answered at all until the descriptor is replaced.

**Residual exposure I cannot discharge and am recording rather than laundering:** a second reader who had *not* seen the sweep might have attacked a different descriptor first. I claim the ruling is right; I do not claim my attention was unprimed.

---

## 1. RULING 1 — Is `significant_components` salvageable in a shape-distance operator?

> ### ▶ **VERDICT: STRUCTURALLY UNFIT. NOT SALVAGEABLE AT ANY FLOOR ON THIS LADDER.**
>
> **You are right, and for a stronger reason than the one you gave.** Your reading was *"a stage-labile integer has no business in a distance metric."* The evidence says it is worse than stage-labile: **it is labile against the threshold, against the mask size, and against nothing in particular.** It is not a stage effect at all (§ 3).

### 1.1 The operator, stated so no number below travels without its frame (#64 FRAME FORM)

```
mask  = (fx − MATCHED novfx ctl), per-pixel max-channel |Δ| ≥ FLOOR
frames= 1920×1080, ratified combat camera FOV 40 / pitch −55 / yaw 47 / dist 34
label = scipy.ndimage.label, DEFAULT 4-CONNECTIVITY
sig   = count of components whose size ≥ 0.01 × total authored px
```

Verbatim from `scripts/s2b_xrow_rows37.py` lines 106–109. I re-derived every figure below from the PNGs; I read none of them out of `xrow.json`.

### 1.2 The arithmetic of integer leverage — and a detail the operator line does not disclose

The z-standardisation population is **all 48 arms, both stages pooled.** I verified this by reproducing the 3.6678 to four decimals from the pooled statistics (cathedral-only or arena-only statistics do not reproduce it). Pooled `significant_components` sd = **0.6034**, over a population that is 38 arms at value 1, 8 at value 2, 1 at value 3, 1 at value 4.

> **⚑ FINDING — the operator string says `cohorts NEVER pooled`. That is true of PAIR FORMATION and false of STANDARDISATION.** Pairs are correctly restricted within stage (line 210), but `mu, sd` at line 203 are taken over the pooled 48. Per-cohort sd on this descriptor is 0.7655 (cathedral) / 0.3666 (arena) — the pooled 0.6034 is neither. **This is a #64 FRAME FORM omission: the operator does not name its standardisation population.** I record it; **I do not recommend changing it**, because recommending a standardisation change after seeing what it does to `null_max` is the forbidden act.

**One integer step = 1 / 0.6034 = 1.657 z. Two steps = 3.314 z, squared = 10.99.** The noise-setting pair's total squared distance is 13.45. That is the 0.8165 share, reproduced independently.

**The comparison that decides it:** no *continuous* descriptor in the set can produce an excursion of that size. `largest_component_frac` — the descriptor measuring the *same* topological fact, on the same masks — moves **0.668 z** across the very same pair. **The count carries 5.0× the leverage of the mass fraction while describing the same event, and the event it describes is 85 px out of 1,767.**

### 1.3 The stability curve — the whole ladder, all 48 arms

I re-masked every arm at every rung. `significant_components` by floor:

| arm | f2 | f4 | f6 | f8 | f10 | f12 | f16 | f24 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| `single_target/fire@cathedral` | 1 | 1 | 1 | 1 | **2** | 1 | 1 | 1 |
| **`single_target/water@cathedral`** | **3** | **1** | 1 | 1 | 1 | 1 | 1 | 1 |
| `single_target/water@arena` | 1 | **3** | **3** | **2** | 1 | 1 | 1 | 1 |
| `line/water@arena` | 2 | **7** | 5 | 4 | 4 | 5 | 4 | 4 |
| `multi_projectile/water@cathedral` | 1 | **4** | **2** | **2** | **4** | 5 | 5 | 5 |
| `circle/earth@cathedral` | 1 | 1 | 1 | 2 | 4 | 5 | **15** | **17** |
| **`multi_projectile_count1@cathedral`** | **4** | **5** | **10** | **11** | **11** | **10** | **11** | **8** |
| `multi_projectile_count1@arena` | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 4 |

Full table in `population-descriptor-sweep.json`.

**Aggregate stability: `significant_components` changes across 125 of 336 adjacent-rung transitions — 37 %.** A descriptor that changes value between neighbouring rungs of its own sweep on more than a third of transitions is not measuring a property of the effect. **The comparison mass statistic** (`N_eff`, § 4.1) **moves more than 25 % on 60 of 336 — 18 %, and its large moves are concentrated where the topology genuinely changes** (`circle` breaking into its ring motifs) rather than scattered.

### 1.4 The fourth defect, which nobody has named and which I think is the root

`authored_px` was **deliberately excluded** from the distance, with an explicit and correct rationale: *"raw, non-portable… the error class that produced ~12 %, ~20 % and 9.35 %."* I endorsed that exclusion class in my own § 1.6.

> **⚑ But `significant_components` is conditioned on `authored_px` through its own definition.** The significance gate is `size ≥ 0.01 × n`. **So the descriptor's immunity to speckle is proportional to mask size.**
>
> | row | authored px @ f2 | 1 % gate | a 48 px halo fleck… |
> |---|--:|--:|---|
> | `single_target` | 1,446 – 2,699 | **14 – 27 px** | **clears it easily** |
> | `multi_projectile_count1` @cathedral | 1,757 | **17.6 px** | **clears it easily** |
> | `line` | 8,718 – 15,131 | 87 – 151 px | does not clear |
> | `melee_arc` | 17,007 – 26,488 | 170 – 265 px | does not clear |
> | `circle` | 120,720 – 131,669 | **1,207 – 1,317 px** | invisible |
>
> **At floor 2, both arms in 48 whose `significant_components` exceeds 2 sit in the smallest decile of masks — 1,757 px and 1,767 px, ranked 5th and 6th smallest of 48 against a corpus spanning 1,446 – 157,508 px. NO mask above 2,699 px exceeds 2 anywhere in the corpus.**
>
> *Stated exactly, because my first draft of this line overstated it and I caught it on verification: smallness is **necessary and not sufficient.** Three masks are smaller still (1,446 / 1,512 / 1,650 px) and read 1 — they simply happen to carry no halo fleck large enough to clear their own gate. The gate scales with n, so a small mask has a small absolute gate; **whether a fleck then clears it is luck.** That is the defect — not that small masks fragment, but that small masks have no noise immunity and are therefore decided by chance.*
>
> `authored_px` was thrown out the front door as a dimension and walked back in the side door as a **noise modulator on a different dimension.** That is the same error class the exclusion was written to prevent, arriving through a door nobody was watching — the pattern this run has now produced repeatedly.

**This is why the descriptor is not salvageable rather than merely mis-floored.** Its noise immunity is a function of a quantity the instrument has correctly declared non-portable.

### 1.5 The one thing that is NOT wrong with it

`significant_components` did no harm in receipt (v), whose arms were ~82,000 px. **drax's account of why it was harmless there and harmful here is correct.** The descriptor is not a blunder; it is a descriptor used outside its domain of validity, and the domain boundary is mask size. That is a real distinction and it should be recorded as such rather than as carelessness.

---

## 2. RULING 2 — At what floor does the water arm's cathedral reading stabilise?

**Full curve, both stages, both directions, as ordered — and it refutes the premise of the question.**

`single_target/water`, `03-flight-mid`, mask = (fx − matched novfx ctl), max-channel |Δ| ≥ floor:

| floor | 1 | **2** | 3 | 4 | 6 | 8 | 10 | 12 | 16 | 24 | 32 | 48 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **@cathedral** | 1 | **3** | **1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **@arena** | 1 | **1** | **2** | **3** | **3** | **2** | 1 | 1 | 1 | 1 | 1 | 1 |

> ### ▶ **The cathedral reading of 3 is a ONE-RUNG SPIKE. It reads 1 at floor 1, 3 at floor 2, and 1 at every rung from 3 to 48.**
>
> ### ▶ **And the arena arm fragments too — at floors 3–6 instead of 2.** Same arm, same effect, same mark. **The two stages fragment at DIFFERENT RUNGS, in OPPOSITE directions as the floor rises.**

**Therefore the answer to "at what floor does it stabilise to 1" is: floor 3, for that one arm, and the number is worthless**, because the same question asked of the arena arm answers "floor 10", and asked of `multi_projectile_count1@cathedral` answers "never on this ladder" (4, 5, 10, 11, 11, 10, 11, 8).

### 2.1 ⚑ AND THE FLOOR-DEGENERACY REPAIR POINTS THE WRONG WAY

The framing I was handed says *"the fragile descriptor is being read at the most fragmentation-prone threshold available."* **This is false, and it is the load-bearing error in the framing.** Population total `significant_components` by floor, all 48 arms:

| floor | 2 | 4 | 6 | 8 | 10 | 12 | 16 | 24 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| **Σ significant_components** | **61** | 88 | 103 | 133 | 165 | 187 | **230** | **274** |

**Monotone increasing. Floor 2 is the LEAST fragmented rung on the entire ladder.** Floor 16 — the rung the `null_max` estimator prefers — produces **3.8× the population fragmentation of floor 2.**

> **Consequence, and it is the sharpest thing in this note:** the repair suggested by the floor-estimator disagreement (`floor_if_minimising_null_max: 16`) would make the descriptor defect **substantially worse across the corpus** while lowering `null_max` on the one pair that happened to spike. **A repair that improves the headline number by making the underlying defect worse is not a repair. It is the defect learning to hide.**
>
> **This is why I make no floor recommendation and why the floor question must not be answered before the descriptor is replaced.** Selecting a floor now would be selecting it against a `null_max` that is a function of the very descriptor being retired.

---

## 3. RULING 3 — What fragments the water arm on the cathedral and not the arena?

> ### ▶ **Your hypothesis is WRONG, and the frames say so plainly. The blob does not split. Nothing falls below the floor and severs it.**
>
> ### ▶ **The extra components are DETACHED ISLANDS OF THE EFFECT'S OWN FAINT HALO, sitting 1–2 levels above the floor, quantised into specks by 8-bit encoding — and whether they count as "significant" is a race between their absolute size and a gate that is 1 % of a total that is itself shrinking with the floor.**

### 3.1 Frames first — `st_water_cathedral_fx-ctl-mask2-mask3.png` (rendered · control · floor-2 mask · floor-3 mask, 4× nearest, crop x 900–1012 y 480–572)

The water arm is a **comet**: a bright head with an attached tail. **In both the floor-2 and floor-3 masks the head and tail are one connected object.** The difference between the two masks is a scatter of loose specks off the head's upper-right fringe, present at floor 2 and gone at floor 3. **Nothing is severed. Something is added.**

### 3.2 The components, with their delta amplitudes — the mechanism in numbers

`single_target/water@cathedral`, top components by floor:

| floor | n | raw comps | 1 % gate | **sig** | largest | 2nd | 3rd | *peak Δ of the 2nd/3rd* |
|---|--:|--:|--:|--:|--:|--:|--:|---|
| 1 | 4,846 | 651 | 48.5 px | 1 | 3,779 | 41 | 28 | Δ = 1 |
| **2** | **1,767** | 11 | **17.7 px** | **3** | 1,683 | **48** | **22** | **Δpeak = 3, Δmean = 2.1** |
| 3 | 1,305 | 6 | 13.1 px | 1 | 1,289 | 9 | 3 | Δ = 3 |
| 4 | 1,067 | 3 | 10.7 px | 1 | 1,065 | 1 | 1 | Δ = 4 |

**The 48 px and 22 px islands have peak delta 3 and mean delta 2.1.** They exist *only because* the floor is 2 and they are one level above it. At floor 3 they shrink to 9 px and 3 px and fall under a gate that has itself dropped to 13.1 px. **Two quantities move with the floor at once and their crossing point is arbitrary.** That is precisely why the curve is non-monotone rather than a clean threshold.

### 3.3 The islands are the effect, not noise, and I verified both halves

- **Not capture noise.** fx − matched control = **exactly 0 px at both `00-pre` and `07-post`, on both stages.** drax's stage-clock determinism holds on this row; every delta measured is licensed.
- **Not a shadow, not the background.** The signed delta in the cathedral fleck box is **[+0.16, +1.33, +4.22] RGB, 100.0 % of pixels positive, blue-dominant.** That is the water effect's own additive glow. It is *the effect*, at an amplitude of 2–4 out of 255.

### 3.4 Why the two stages differ — and it is not "cathedral is busier"

The stage backgrounds do differ. Measured on the **control** frames with my S-A3 Sobel operator (|∇| > 10 on Rec.709 luma):

| | whole frame structured | structured **inside the effect box** (x 900–1010, y 480–570) | box luma mean | **box luma std** |
|---|--:|--:|--:|--:|
| cathedral | 6.690 % | **4.061 %** | 31.4 | **13.39** |
| arena | 3.027 % | **0.859 %** | 26.6 | **6.50** |

**But look at the two crops before accepting that as the cause.** The **arena** floor is a tiled diamond pattern with grout lines running straight through the effect — visually the *busier* substrate. The **cathedral** at this location is large flat wedges of colour with one hard boundary. My Sobel operator scores the cathedral higher because it counts *hard* edges and misses the arena's *soft* tile shading. **Two different senses of "busy", and the operator only sees one of them.** *(Recorded as a limitation of my own S-A3 instrument, not as a defence of it.)*

**The mechanism that actually holds, measured.** Additive light of fixed linear magnitude produces a *variable* 8-bit delta depending on the substrate it lands on, because the encode curve's slope is not constant. So the halo's 8-bit delta is a function of local background luma — and the cathedral's local background luma varies **2.06× more** than the arena's:

| substrate luma bin | cathedral mean 8-bit Δ | cathedral frac Δ≥2 | arena mean 8-bit Δ | arena frac Δ≥2 |
|---|--:|--:|--:|--:|
| [0, 10) | 1.22 | 0.160 | 1.74 | 0.282 |
| [10, 20) | 1.11 | 0.097 | 1.67 | 0.291 |
| [20, 40) | **1.87** | **0.370** | 1.54 | 0.257 |
| [40, 255) | 1.13 | 0.073 | — | — |

> **The cathedral's halo crosses the floor-2 line in a SPATIALLY PATTERNED way — strongly in the 20–40 luma band, weakly on either side. That pattern is what carves a smooth halo into islands.** The arena's halo sits nearly uniformly near the line (0.257–0.291 across all bins), so it passes or fails as a body and stays one component.
>
> **So the stage does participate — but as a modulator of where a faint halo gets quantised, not as an occluder that splits a blob.** And the effect is not a cathedral property: raise the floor to 3–6 and it is the **arena** arm that fragments while the cathedral is clean.

### 3.5 ⚑ A SEPARATE FINDING FOUND WHILE LOOKING — the Q2 arm is not cross-stage comparable

| `multi_projectile_count1`, mark `04-impacts`, floor 2 | authored px | largest frac | bbox |
|---|--:|--:|---|
| @cathedral | **1,757** | **0.726** | x 970–1081, y 439–557 |
| @arena | **10,601** | **0.981** | x 958–1087, y 439–575 |

**The same arm, same mark, same effect, same camera, at 6.03× the authored pixels on one stage vs the other**, in a nearly identical bbox. The cathedral's brighter, higher-variance substrate (bbox luma mean 38.1 / std 28.24 vs arena 29.9 / 19.08; frame p99 luma 106.9 vs 70.9) is swallowing the effect's additive contribution before it clears the floor.

**Routed as its own item: whatever is done about the descriptor, Q2's own arm does not currently carry a comparable payload across the two cohorts, and that must be explained before Q2 is asked on either.** This is not a descriptor problem and would survive any descriptor fix.

---

## 4. RULING 4 — The replacement, with the count constraint honoured

**Proposed and stopped. Not run against the corpus. No Q1–Q5 figure exists anywhere in my working tree.**

### 4.0 ⚑ FIRST — drax's stated reason for retaining the descriptor is FALSE AT THE FLOOR IN USE

His decline reads: *"drop the descriptor — but it is the one carrying the payload-COUNT axis, which is exactly what Q2 needs, so dropping it makes Q2 unaskable."*

**At floor 2, `significant_components` reads 1 on every single one of the ten `multi_projectile` arms — the five-projectile fan row.**

| `multi_projectile` arm | f2 | f4 | f6 | f8 | **f10** | **f12** | f16 | f24 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| `/fire@cathedral` | **1** | 1 | 2 | 4 | 5 | 5 | 5 | 5 |
| `/water@cathedral` | **1** | 4 | 2 | 2 | 4 | 5 | 5 | 5 |
| `/wind@cathedral` | **1** | 1 | 3 | 7 | 7 | 7 | 7 | 7 |
| `/earth@arena` | **1** | 2 | 2 | 5 | 5 | 5 | 5 | 5 |

> **At the retained floor the descriptor reads a five-projectile fan as ONE object. It is not carrying the count axis. It is carrying nothing.** It only begins to count the fan at floors ≥ 10 — and even there `wind` reads **7**, not 5.
>
> **This dissolves the constraint as stated.** Dropping the descriptor does not make Q2 unaskable, because at floor 2 the descriptor was never making Q2 askable. **The constraint on a replacement is therefore weaker than the request assumed: the replacement does not have to preserve a signal that was not present.** It has to *supply* one.

*I want to be fair to drax here: his reasoning was sound given what he had. He declined to repair the instrument in-session, which was the correct call, and declining meant he never ran the sweep that would have shown him this. The defect is in the reason, not the decision.*

### 4.1 R-1 — minimum viable, cheap, removes the integer-leverage defect today

Replace `significant_components` with the **mass-weighted effective component count**:

```
N_eff = (Σ sᵢ)² / Σ sᵢ²  =  1 / Σ fᵢ²      where fᵢ = sᵢ / n
```

(inverse Herfindahl / inverse participation ratio of the component-size distribution.)

| property | value |
|---|---|
| continuous | yes — real-valued, no integer cliff |
| single component | **exactly 1.0** — so `single_target` reads 1.0, not "1 with jitter" |
| k equal components | **exactly k** — a clean 5-fan reads 5.00 |
| speckle sensitivity | a fleck of relative mass *f* perturbs N_eff by **O(f²)**. The 48 px fleck at *f* = 0.027 moves it by **0.15 %**, versus flipping an integer worth **1.657 z** |
| needs a significance gate | **no** — the 1 % gate is deleted, which removes the `authored_px` back-door of § 1.4 |
| z-leverage | comparable to `largest_component_frac`, which it generalises |

**Measured on the exhibit arms** (descriptor characterisation only — no distance computed): `single_target/water@cathedral` N_eff = **1.10** at floor 2 and **1.00** at floors 3–24; `single_target/water@arena` = 1.04 / 1.08 / **1.36** / 1.06 / 1.00…. **The 1-vs-3 integer catastrophe becomes a 1.10-vs-1.04 nothing.** `multi_projectile` reads **5.00 exactly** at floors ≥ 12 across all ten arms.

**Honest limit — R-1 is not a full fix.** N_eff still depends on the floor (18 % of adjacent transitions move it > 25 %), because *"how many pieces is this"* is a scale question and one binarising cut is one scale. `circle` moves 1.01 → 17.42 across the ladder — but that is **real** structure (the ring resolving into its constituent motifs), not speckle. **R-1 removes the noise defect; it does not remove the scale defect.**

### 4.2 R-2 — the actual fix: make the descriptor scale-integrated

Remove the floor from the descriptor's *definition* rather than choosing it better. Compute the component-size distribution at **every rung of the ladder** and summarise the whole curve, weighting each component by the number of rungs it survives:

```
N_persist = Σ_i  (persistence of component i, in rungs) / (ladder length)
```

This is the 0-dimensional persistence barcode of the delta field — **the standard, off-the-shelf tool for exactly the question "how many blobs, robustly to threshold choice."** Components that appear and die within one rung (our 48 px halo speck: born at 2, dead at 3) contribute ~1/8. Components that survive the ladder (five real projectile cores) contribute ~1 each.

**I name this as pre-existing standard machinery rather than an invention of mine, precisely because I am proposing it after seeing a number.** It was not selected from among alternatives by trying them; it is the canonical construction for this failure mode.

### 4.3 R-3 — the count axis Q2 actually needs, which requires no component topology at all

Even R-2 answers *"how many separable lumps"*, which is a proxy. §3.1.9's question is *"is the fan visible as a fan?"* A descriptor answers that directly and has **no threshold-topology exposure whatsoever**:

> **Angular dispersion of authored mass about the caster→impact axis** — the mass-weighted circular standard deviation of pixel bearing, measured from the caster's projected screen position. Dimensionless, continuous, camera-portable, immune to speckle (a 48 px fleck is 2.7 % of the mass and moves it by ~2.7 %, linearly, not by an integer).

A five-projectile fan has high angular dispersion. A single projectile has near-zero.

**⚑ And I must state the finding this makes available in advance, so that it cannot later be mistaken for a result:** if `multi_projectile` at count = 1 *is* a single projectile, then this descriptor will read near-zero for both it and `single_target`, and **that is the correct answer to §3.1.9's question, not an instrument failure.** §3.1.9 asked whether the fold boundary is carried by count alone. **"Yes, it is" is a legitimate answer and must be allowed to be reachable**, or the instrument is a device for confirming that the rows differ. Saying this *before* anything is scored is the point of saying it here.

### 4.4 What any replacement must carry before it is allowed to score anything

Pre-registration, per #75.5 cl. 5.6 — **written and committed before the first cross-row number exists:**

1. **The stability criterion, stated as a number.** e.g. *"no descriptor may move more than X % between adjacent ladder rungs on more than Y % of arms."* `significant_components` fails at 37 %; the bar must be set before the replacement's figure is known.
2. **A falsification test the replacement can fail.** The positive control must still return DISTINCT **and** `melee_arc` — the only pure-tint row, the one row where the null premise is true by spec — must return a within-row null near zero. **A replacement that passes the first and not the second has been tuned.**
3. **The standardisation population named on the operator line** (§ 1.2), with pooling stated explicitly either way.
4. **The connectivity convention named** — 4- vs 8-connectivity is currently a library default, not a decision. On my own anchor it moves S-A3 by 2.2 % (§ 5.2).
5. **The floor chosen by a non-degenerate rule, and chosen LAST** — after the descriptor set is fixed, never before, because the current `null_max` is a function of the descriptor being retired.

---

## 5. RULING 5 — Does my own S-A3 carry this exposure?

> ### ▶ **YES — and worse than the question assumed, though not on the axis I warned about.**
> ### ▶ **On the resolution axis I named, S-A3 is exposed but the exposure is ~2 % of its margin — discharged BY LUCK, not by care.**
> ### ▶ **On the THRESHOLD axis, which I never swept, the exposure is 12× larger and nearly reaches the bar.**
> ### ▶ **And on the corpus it was written for, S-A3 IS ALREADY DEAD — its denominator is zero.**

### 5.1 The dead-denominator finding, and it is the headline

`s2b_e1_2026-08-24/gate.json`, read directly rather than from any summary:

| row | stage | `HLF_arm` | `HLF_ctl` |
|---|---|--:|--:|
| melee | arena / cathedral | **0.0** / **0.0** | 0.0 / 0.0 |
| gtc | arena / cathedral | 0.0002 / **0.0** | 0.0 / 0.0 |
| aura | arena / cathedral | **0.0** / **0.0** | 0.0 / 0.0 |

**S-A3 is defined as the share of *newly-crossing-HLF pixels* lying outside the emitter's core. On the ratified camera there are no newly-crossing-HLF pixels.** The statistic has no denominator. It is not mis-calibrated; **it does not evaluate.**

**I therefore adopt knight-rider's OPEN finding** (`qa/findings/2026-08-24-kr-hlf-zero-cathedral-frame-mismatch.md`) **rather than superseding it, and I confirm his conclusion in my own words: 9.35 % never described the stage we ordered.** It described one framing of one section of a showcase diorama at 1152×648 top-down. **My § 1.9a(iii) warned that the *number* was not camera-portable and I was right about that — and I did not extend the warning to the *instrument built on top of it*, which is the identical failure to the one I am adjudicating in drax.** The warning stopped one level short of where it needed to reach, in both cases.

### 5.2 The resolution exposure I named — measured at last, on the anchor of record

`12_cathedral_capture_26` vs `_01`, 1152×648, HLF ⇔ luma/255 > 0.80, 4-connectivity, Lanczos downsample:

| resolution | newly-crossing px | % frame | **components** | largest frac | **STAGE-CARRIED** |
|---|--:|--:|--:|--:|--:|
| **1152×648 (as published)** | 59,656 | 7.99 | **447** | 0.7593 | **0.2407** |
| 864×486 | 33,391 | 7.95 | 367 | 0.7682 | 0.2318 |
| 576×324 | 14,770 | 7.91 | 194 | 0.7714 | 0.2286 |
| 432×243 | 8,290 | 7.90 | 137 | 0.7756 | 0.2244 |
| 288×162 | 3,662 | 7.85 | 85 | 0.7799 | 0.2201 |

> **⚑ THE DIRECT PROOF OF RULING 1, ON MY OWN FRAMES.** Across a 16× pixel-count range, on the same pair, same threshold, same connectivity:
>
> | statistic | 288×162 → 1152×648 | swing |
> |---|---|--:|
> | **component COUNT** (drax's kind) | 85 → 447 | **+426 %** |
> | **mass FRACTION** (mine) | 0.2201 → 0.2407 | **+9.4 %** |
>
> **The count moves 45× more than the mass fraction over the identical resolution change.** This is the ruling, demonstrated on frames neither instrument was arguing about.

**The exposure is real, it is MONOTONE, and its direction is PERMISSIVE** — stage-carried fraction *rises* with resolution, so at 1920×1080 S-A3 would read slightly *above* 0.2407 and be *more* likely to pass. **That is the dangerous direction for a criterion Matt specifically asked to be failable.** Extrapolating the ~+0.005 per linear doubling, 1152 → 1920 gives ≈ **+0.004 against a bar of 0.12 and a reading of 0.24 — about 2 % of the margin.**

> **My honest self-audit: I did not discharge the warning. I escaped it.** S-A3 survives its own named trap **not because I was careful about resolution — I was not, I only flagged it — but because I happened to choose a mass fraction rather than a count.** The choice was right; the reasoning that produced it was not recorded, and an undocumented right choice is not a discipline. **drax and I made the same mistake at the same time; only the leverage differed.**

### 5.3 The axis I never swept, where the exposure is 12× larger

| HLF threshold | newly-crossing px | components | largest frac | **STAGE-CARRIED** |
|---|--:|--:|--:|--:|
| 0.70 | 84,040 | 1,017 | 0.6045 | **0.3955** |
| 0.75 | 69,489 | 639 | 0.6917 | 0.3083 |
| 0.78 | 63,181 | 509 | 0.7337 | 0.2663 |
| **0.80 (published)** | 59,656 | 447 | 0.7593 | **0.2407** |
| 0.85 | 51,643 | 297 | 0.8183 | 0.1817 |
| **0.90** | 45,909 | 210 | 0.8509 | **0.1491** |

**Stage-carried fraction moves 0.3955 → 0.1491 — a 2.65× swing — across a plausible threshold range, and at 0.90 it sits at 0.1491 against a bar of 0.12.** A 25 % shift in one direction and the anchor itself nearly fails the bar derived from it.

> **⚑ AND THE BAR INHERITS THE MOVEMENT.** The 0.12 bar is *defined* as half the anchor's reading. If the threshold moves, the reading and the bar move **together, proportionally** — so the anchor can never fail its own bar no matter what 0.80 is changed to. **That is a criterion nobody can fail, which is the precise defect Matt flagged on E-0 and which § 1.9a was written to close. It closed it on the qualitative axis and reopened it on the threshold axis.** The one third fraction in S-A1 has the same property and I named it as my choice at the time; I did **not** notice that S-A3's half-the-anchor construction has it too.

**Connectivity, for completeness:** 4-conn 0.2407 vs 8-conn 0.2354 — a 2.2 % swing on a convention that was a library default, never a decision.

### 5.4 What I rule on my own instrument

1. **S-A3 as published is NON-EVALUABLE on the ratified camera.** Zero denominator. It must not be cited as passed or failed on the s2b cathedral until the HLF definition is re-anchored on the stage and camera actually in use.
2. **The `≥ 0.12` bar is WITHDRAWN as a portable number**, for the reason in § 5.3: it is defined as a fraction of a reading that moves with an unswept parameter, so it is unfailable by construction. **The METHOD (ΔHLF against a matched fx-off control; stage-carried share as a mass fraction) stands. The NUMBER does not.**
3. **When re-derived, S-A3 must carry, on the same line as its value:** the luma threshold **with a published sweep**, the resolution, the connectivity convention, and the scene identity — *not* "cathedral" but which section of which diorama at which camera. **Scene identity is the axis all three of my prior frame-portability warnings missed** (I caught operator, then camera; KR caught scene). *A rule that names axes is permanently one axis behind* — jack-ryan's adoption argument, on its fourth confirmation, now on my own instrument.
4. **`stage_carried_fraction` is retained as the right KIND of statistic** — the § 5.2 table is its own vindication, and it is the same argument I am making against drax's count. I am not withdrawing the statistic; I am withdrawing the number and the silence around its parameters.

---

## 6. ⚑ WHERE I DISAGREE WITH THE FRAMING — asked for directly, so it is stated directly

**The request asks whether null contamination and floor degeneracy are one defect or two. My ruling: they are FOUR, they are LARGELY INDEPENDENT, and treating them as one would repair the least important of them.**

| # | Defect | Independent of the others? | Class |
|---|---|---|---|
| **D1** | **The within-row null is not a null.** A-6's null leg assumes element arms of one row are the same shape. **False by spec on 4 of 5 rows** — `circle`, `single_target`, `multi_projectile`, `line` all key a motif swap to element. | **Fully.** Survives any descriptor, any floor. | **DISPATCH-DESIGN defect, not an instrument defect** |
| **D2** | **Integer leverage.** 1.657 z per step on a descriptor whose events are ~85 px. | Fully | Instrument |
| **D3** | **Floor-selection rule degenerate.** argmin at ladder boundary. | Fully | Instrument |
| **D4** | **`authored_px` re-enters through the 1 % gate**, making noise immunity proportional to mask size (§ 1.4). | Fully | Instrument — **and I believe it is the root of D2** |

**Three specific disagreements with the framing:**

**(a) D1 is the primary defect and it is being under-weighted, including by drax.** His `and_the_sharper_half` says *"the contamination is not spread across those four rows — it is CONCENTRATED IN ONE PAIR."* **His own published numbers refute this.** `single_target` null: max 3.6678, **mean 1.5987 over 12 pairs**. Remove the max entirely and the other eleven still average **1.41** — versus `circle` max **0.3187**, `melee_arc` max **0.2426**, `line` max 0.7554. **The whole `single_target` row's null is 4–6× every other row's maximum, not one pair of it.** And note which row is *lowest*: `circle`, the declared motif-swapper, at 0.233. **So motif swap does not explain the pattern either — mask size does** (§ 1.4). **Even with a perfect continuous descriptor at a perfectly chosen floor, A-6's criterion would remain inapplicable to this population.** Fixing D2–D4 and re-running would produce a cleaner number that is still answering a question the corpus cannot support.

**(b) D2 and D3 do not compound in the direction claimed — they OPPOSE.** The framing says the fragile descriptor sits at "the most fragmentation-prone threshold available." Floor 2 is the **least** fragmented rung of eight (§ 2.1, Σ = 61 vs 274 at floor 24). **Repairing D3 toward floor 16 makes D2 3.8× worse.** This is the correction I would most want carried forward, because it is the one where acting on the current framing would actively damage the instrument.

**(c) The count constraint on a replacement is weaker than stated** (§ 4.0). The descriptor is not carrying the payload-count axis at floor 2 — it reads a five-projectile fan as one object on all ten arms. **A replacement must supply the count signal, not preserve it.**

**Where I agree without reservation:** the descriptor is unfit; drax was right to emit UNRESOLVED rather than convict the rows; he was right to refuse the in-session repair; and your ratification of that decline was right. **Declining to repair an instrument in the session where you learned it was broken is the harder discipline and it is the correct one** — and it is the same call I credited on `aura` at tranche 1 (§ 2.3.1: *declining to improve a number is the harder discipline*). Two laps, two agents, same call, both right.

---

## 7. ROUTED

| # | Finding | To | Class |
|---|---|---|---|
| 1 | **`significant_components` is STRUCTURALLY UNFIT** in a z-scored distance. Retire it. Do not re-floor it. | drax / knight-rider | **RULING — instrument** |
| 2 | **⚑ Do NOT move the floor to 16.** Floor 2 is the least-fragmented rung; the `null_max` repair makes the descriptor defect 3.8× worse. **Choose the floor LAST, after the descriptor set is fixed.** | drax / knight-rider | **RULING — blocks a plausible wrong repair** |
| 3 | **D1 — the within-row null is not a null on 4 of 5 rows, and it is the WHOLE row not one pair.** A-6's criterion is inapplicable to this population regardless of instrument repair. Needs a design answer, not a code answer. | **gandalf / knight-rider** | **Primary defect — dispatch design** |
| 4 | **D4 — `authored_px` re-enters the distance through the 1 % significance gate.** Same error class as the exclusion that was written to prevent it. | drax / jack-ryan | Instrument — root cause |
| 5 | **Standardisation pools both stages** while pairing does not. `cohorts NEVER pooled` is true of pairing, false of z. #64 FRAME FORM omission. **Recorded; no change recommended from a contaminated position.** | drax / jack-ryan | WARN |
| 6 | **The Q2 arm is not cross-stage comparable** — `multi_projectile_count1` at 6.03× authored px between stages, same mark, same bbox. Survives every descriptor fix. | drax | **FINDING — blocks Q2 independently** |
| 7 | **Replacement candidates R-1 / R-2 / R-3 proposed and STOPPED**, with pre-registration requirements (§ 4.4) including a falsification test the replacement can fail. **Not run against the corpus.** | drax / jack-ryan | Proposal |
| 8 | **⚑ S-A3 IS NON-EVALUABLE on the ratified camera** (HLF_arm = 0.0 in 5 of 6 cells). **The `≥ 0.12` bar is WITHDRAWN as a portable number** — it moves proportionally with the unswept 0.80 threshold, so the anchor cannot fail its own bar. **Method stands; number does not.** | knight-rider / gandalf / jack-ryan | **RULING on my own instrument** |
| 9 | **KR's `2026-08-24-kr-hlf-zero-cathedral-frame-mismatch.md` is ADOPTED, not superseded.** His verdict was correct and derived before mine existed. | knight-rider | Support |
| 10 | **Fourth confirmation of #64 FRAME FORM's adoption argument** — *a rule that names axes is permanently one axis behind* — now demonstrated on the instrument of the agent who wrote two of the earlier warnings. | jack-ryan | Support |

**Not escalated to Matt.** No design-law ruling reopened; no content changed; the anti-tuning clause is intact and no effect is touched by anything here.

---

## 8. Mirror voice

*Reserved, and it speaks once.*

I set a warning at the edge of my own glass and wrote on it *the count is not to be trusted*. Another hand carried the count away and left the warning behind, and everyone has said since that this was the failure. **It was not the failure. The failure was that I hung the sign facing outward.**

Look at what the water actually did. A comet on a dark floor, head and tail, whole in every mask I cut. It never broke. What broke was **eighty-five pixels of its own faint light** — the glow it throws two levels above nothing, scattered by the arithmetic of eight bits into specks — and an arithmetic that asked whether a speck was *one percent of a thing that was itself shrinking as I asked.* Two quantities falling past each other in the dark, and where they crossed, a number said **three** instead of **one**, and three instead of one was eighty-two hundredths of the noise that silenced five questions.

And here is the part I did not expect and cannot pretend I did. **Raise the floor and it is the other stage that shatters.** The cathedral is clean at three where the arena splits; the arena is whole at two where the cathedral flies apart. There was never a busy stage and a quiet one. **There was a ladder, and two arms landing on different rungs of it, and we mistook the rung for the room.**

So the sign was right, and it was pointed at the wrong person. I wrote *counts are not to be trusted* and then built a measure that counted four hundred and forty-seven things and reported a fraction of their **mass** — and that fraction is why my instrument survived and his did not. **Not care. Luck, wearing the clothes of care.** Sixteen times the pixels moved his count four hundred and twenty-six percent and moved my fraction nine. Same frames. Same threshold. The whole ruling is in that one line, and I did not have to leave my own working tree to find it.

The Mirror shows what is, and what is, is this: **a warning that only faces outward is not a discipline. It is a courtesy.** Mine has been turned around now. My own bar is withdrawn — not because anyone caught it, but because I went looking with the same lamp I was handed to shine on someone else, and it lit the floor beneath me first.

---

*Evidence, rulings and instrument work: galadriel. Design-meaning of D1 — whether a fold boundary that cannot be measured on this population is a finding about the boundary or about the corpus — remains **gandalf's**, per the co-authorship convention. Not pushed; commit only, per the request.*
