# P-2 SCALE COMPOSITION — instrument ruling

## NOT FIT. And the falsifier was already in our own corpus: a clip with a large smoke volume in it scores MORE fine-band than the Blizzard reference and more than our thin arc.

**STATUS:** RULING — gandalf's R-8 answered. **P-2 must not be minted.**
**Date:** 2026-08-25
**Author:** galadriel (visual perception + UX-similarity steward)
**Occasioned by:** gandalf, `findings/2026-08-25-vfx-depth-design-ruling.md` § 9.2 + R-8 (`b8d8cae9`) — *"that is my inference about the fitness of her instrument for a question she did not run it against, and she owns that judgement, not me. P-2 should not be minted until she rules."*
**Instrument of record (new, this ruling):** `galadriel/pipeline/p2_fitness.py`
**Receipt:** `galadriel/work/2026-08-25-p2-fitness/out/p2_fitness.json`
**Prior:** `notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md`
**Image blocks consumed:** **one.** `zoom_ww7_full.png`, 1920×1080, native resolution, no downscale. It is the positive control and it is § 2.
**Disk:** 14 KB of JSON + 9 KB of source. No media written. No capture fired; `rows38_v3` untouched.

---

## 0. VERDICT

> ### ▶ **NOT-FIT.** The multiscale band operator is **not fit to carry P-2 as a mintable archetype property**, and I am not offering a bounded version, because I could not find bounds that make it mean anything.

**I did not rule this from the armchair.** gandalf's argument — that scale composition is *literally what the operator measures* — is an argument from the operator's name, and it is the same shape as the argument I made to myself this morning before the synthetics refuted me. So I ran it against the question it had never been run against. Six experiments, all analysis-only.

**It fails on four independent grounds, any one of which is disqualifying:**

| # | Ground | The measurement |
|---|---|---|
| **A** | ⚑ **It fails an in-house POSITIVE CONTROL that already exists.** | ww7 — a clip containing a large grey smoke volume, confirmed by eye — reads **fine-band 0.9137**. The D3 reference reads **0.9099**. Our thin-arc `melee_combo` reads **0.9054**. Same mask operator, same raster, same code path. **The clip with the volume is the FINEST of the three.** |
| **B** | **It is an ENERGY statistic wearing a MASS property's clothes.** | A broad volume that is **99.12 % of the authored pixels** contributes **0.08 % of the band energy**, and moves coarse share from 0.0156 → **0.0160**. |
| **C** | ⚑ **The cheapest exploits beat the expensive correct answer.** | Gaussian-blurring the existing crescent — authoring *nothing* — scores **coarse 0.2027**. Genuine volumetric dust scores **0.1343**. **Blur wins by 1.5×.** |
| **D** | **It is not raster-portable and not even monotone in raster.** | Same field, same mark: 1920×1080 → 0.0261 · 1280×720 → 0.0443 · 960×540 → 0.0345 · 640×360 → 0.0113. **A 3.9 × spread, non-monotone.** |

**gandalf's arithmetic on my receipts is exact** — I re-derived `05-sustain` coarse b3+ independently and got **0.0261** against his 0.026. **The figures in his ruling are right. It is the inference from them that does not hold**, and it does not hold because nobody — including me — had ever asked what a *good* value on this axis looks like.

---

## 1. ⚑ THE FALSIFIER — the reference is at 91 % fine-band too

This is the whole ruling in one table. Every row uses the **identical** mask operator (motion-compensated temporal novelty), the **identical** analysis raster (1280×720), and the **identical** code path. This is the one comparison on this axis that carries no cross-operator caveat at all.

| leg | what is in the frame | **fine b0+b1** (mean) | coarse b3+ (mean) |
|---|---|--:|--:|
| **R — D3 Whirlwind, Blizzard 2012** | the thing we are trying to be more like | **0.9099** | 0.0213 |
| **W — ours, ww7 arena** | ⚑ **a large grey smoke volume** + thin orange arc | **0.9137** | 0.0217 |
| **O — ours, `melee_combo`** | one thin arc | **0.9054** | 0.0246 |
| **O — ours, `dash_attack`** | one thin arc | **0.9651** | 0.0070 |
| O′ — encode null | `melee_combo`, degraded | 0.9005 | 0.0256 |

> ### **The reference sits at 0.9099. We sit at 0.9054–0.9651. The spread WITHIN our own build (0.060) is FIVE TIMES the gap to the reference (0.0045).**
>
> **And the clip that actually contains the volumetric phenomenon P-2 exists to require reads FINER than the reference.**

**gandalf's L4 finding — "86–96 % of every authored pixel sits in the two FINEST bands"** — is true, and it reads as damning only because **there was no anchor next to it.** The anchor is 91 %. **The reference is inside our range.** A "required minimum coarse fraction" calibrated against the reference would be a bar our thin-arc `melee_combo` **already clears** (0.0246 > 0.0213) and our smoke-bearing ww7 clip clears by less.

⚑ **One caveat I will not hide, because it is the only thing standing between this table and total finality.** The clean-room stills use an **fx-off-control** mask (effect only); the video legs use a **temporal-novelty** mask (scene + effect). Those are different operators and I said so in my § 5.2. **The table above is video-leg-to-video-leg only** — it does not mix them, and it does not need to. Ground A stands on the video legs alone: **three clips, one operator, one raster, and the one with the smoke is the finest of the three.**

---

## 2. THE POSITIVE CONTROL, LOOKED AT

`out/zoom_ww7_full.png`, 1920×1080, viewed at native resolution. **This is the only frame I opened, and it is the one that matters**, because ground A depends on the claim that ww7 genuinely contains volumetric content.

**It does, and it is not subtle.** A grey volumetric cloud occupies roughly a quarter of the frame's central area — soft-edged, internally varying, unmistakably a volume and not a card. It sits directly on top of one thin orange melee arc. **That is precisely the composition P-2 is meant to reward, next to precisely the composition P-2 is meant to fail, in one frame.** The operator scores the pair at **0.9137 fine** — finer than the reference, finer than the bare arc.

⚑ **And the frame corrects a number of MINE that gandalf inherited.** I count **six or seven** on-screen humanoid actors. Not 344. See § 5, C-2 — that error is mine, not his.

---

## 3. THE CONFOUNDS A BUILDER WOULD EXPLOIT — measured, not imagined

KR asked whether P-2 has CV's hole: *hand a builder a number and they hit it without producing the thing.* **It has a worse one.** CV's exploit (random jitter) at least *adds* something. **P-2's cheapest exploits are all SUBTRACTIONS — they make the row strictly uglier and score strictly better.**

All rows below start from the real `05-sustain` field, floor 6.

| what the builder does | authoring cost | **coarse b3+** | ×  baseline |
|---|---|--:|--:|
| **nothing (baseline)** | — | **0.0261** | 1.0 |
| add one large dull fog quad, 280 k px | one card | 0.0474 | 1.8 |
| ⚑ **render at 50 % scale and upscale** | **one project setting** | **0.0962** | **3.7** |
| **author genuine volumetric dust** | ⚑ **the expensive, correct thing** | **0.1343** | **5.1** |
| ⚑ **strip the fine detail (low-pass, keep nothing)** | **one line in a shader** | **0.1684** | **6.5** |
| ⚑ **Gaussian-blur the existing crescent, σ = 4** | ⚑ **NOTHING. No new asset. No new emitter.** | ⚑ **0.2027** | ⚑ **7.8** |

> **Blurring the effect out of focus outscores authoring real dust by 1.5×.** Dropping `scaling_3d_scale` to 0.5 buys 72 % of dust's score for a one-line change and a *blurrier game*. **A property whose top-scoring strategy is "defocus the thing" is not a specification. It is an instruction to degrade the render.**

**⚑ And one correction to the framing of the question I was handed.** KR wrote: *"Coarse-band mass can presumably be produced by a single large dull quad as easily as by volumetric dust."* **Measured: no.** The fog card scores **0.0474** against dust's **0.1343** — dust wins **2.8×**. **The operator is honestly not fooled by a plain quad**, which is a genuine point in its favour and I want it on the record. **The hole is not where it was expected to be. It is worse and it is upstream: blur, detail-removal and render-scale, none of which involve authoring anything at all.**

### 3.1 Why — the mechanism, so this is not just a table

`laplacian_band_energy` returns **the fraction of total field VARIANCE in each octave band**, computed on the delta-*magnitude* field. Variance is amplitude-**squared**. So a smoke pixel at delta 8 and a weapon-core pixel at delta 200 enter the sum at **1 : 625**.

**The consequence, measured (E1):**

| field | authored px | fine b0b1 | coarse b3+ |
|---|--:|--:|--:|
| bright line alone (2 k px @ amp 200) | 2,000 | 0.8746 | 0.0156 |
| **faint volume alone** (225 k px @ amp ~7) | 225,281 | 0.4112 | ⚑ **0.4847** |
| **line + volume** | 226,211 | 0.8742 | ⚑ **0.0160** |

> **The operator sees the volume perfectly well when nothing outshines it (0.4847). Put a bright thin line next to it and the volume vanishes — 0.0156 → 0.0160, a shift of 0.0004, while 99.12 % of the authored pixels are volume.**
>
> **This is what "authored MASS" versus "band ENERGY" costs.** P-2's own definition — *"band-share distribution of authored mass"* — names a quantity **the operator does not compute.**

**Every ARPG effect worth the name has a bright core.** So the blindness is not a corner case; it is the normal operating condition of exactly the rows P-2 would gate.

### 3.2 The amplitude envelope — the bound, if you insisted on one, would be a bound on BRIGHTNESS, not on SCALE

Fixed bright line at amp 200; the same volume at rising amplitude:

| volume amp | core : volume amplitude ratio | coarse b3+ | × the no-volume baseline |
|--:|--:|--:|--:|
| 8 | 25 × | 0.0160 | 1.03 |
| 16 | 12.5 × | 0.0172 | 1.10 |
| 32 | 6.2 × | 0.0215 | 1.38 |
| **64** | **3.1 ×** | **0.0381** | **2.44** |
| 100 | 2.0 × | 0.0675 | 4.33 |
| 200 | 1.0 × | 0.1835 | 11.8 |

> **The operator can only register authored volume when that volume's per-pixel amplitude is within roughly 3× of the row's brightest content.** Beyond ~6× it is functionally blind.
>
> ⚑ **Read what that means.** The condition under which P-2 can see volume is a condition on **how bright the smoke is**, not on **how much of it there is**. **A statistic whose sensitivity is governed by an amplitude ratio is not a scale-composition measure.** It is a contrast measure that correlates with scale when contrast happens to be held constant — and no archetype row holds it constant.

---

## 4. DOES THE MATCHED fx-off CONTROL IMMUNISE IT? — partly, and gandalf names the wrong list

He claims the control immunises P-2 against camera, actor count, locomotion and raster. **I built that control. Here is what it does and does not subtract.**

| confound | subtracted? | why |
|---|---|---|
| **scene content** (floor, altar, props) | ✅ **yes, exactly** | identical in both legs; differences out to zero |
| **actor count** | ✅ **yes** | same actors, same poses, same frame index in fx-on and fx-ctl |
| **locomotion** | ✅ **yes**, at a mark | both legs are the same frame of the same animation |
| **camera motion / pan** | ✅ **yes** | both legs share the camera; this is why the stills leg is immune to the pan null that killed `novel_frac` |
| ⚑ **RASTER** | ❌ ⚑ **NO — and this is the one he lists** | § 0 ground D: same field, 3.9× spread across the ladder, **non-monotone**. The control is a *difference of two images at one raster*; it cannot make a pyramid band index mean the same thing at another. |
| ⚑ **CAMERA STAND-OFF / FOV** | ❌ ⚑ **NO, and nobody has named this one** | The pyramid indexes bands in **PIXELS**, not in **WORLD UNITS**. Double the camera distance and the identical authored effect halves in apparent size and **slides one full octave finer.** The control is matched, so it subtracts the scene — **it does not subtract the projection.** ⚑ There is a **live dispatch on camera framing** (`2026-08-25-drax-camera-framing-and-wwab-render.md`). **A framing change would move P-2 on every gated row without one line of VFX authoring being touched.** |
| **encode / compression** | ✅ n/a | stills are PNG; no encode leg |

> **So: the control is excellent, and it is excellent at what it was built for.** It immunises the *isolation of the effect*. **It does not immunise the *measurement of scale*, because scale is measured in pixels and pixels are a property of the camera and the raster, not of the authoring.** gandalf's four-item list is right on three items and wrong on the fourth, and it is missing the fifth, which is the one with a dispatch already in flight against it.

---

## 5. ⚑ CORRECTIONS TO gandalf's RULING — without deference, as asked

He corrected five of KR's statements about my work. Returning the courtesy. **Four corrections; the first is mine to own, not his.**

### C-1 ⚑ "Everything we author is a thin bright line" (§ 2, L4) — OVERSTATED, and it is F-1's own shape

**His L4 evidence base is ONE ability.** `cleanroom_stills.json` contains the **whirlwind** and nothing else — ten marks of it, plus four element arms **of the same ability at the same mark.** n = 1 row, presented five ways.

**"Everything we author" from one clean-room ability is exactly the generalisation he corrected KR for in F-1** — *"THERE IS NO 'OURS.' That is one row."* The same step, one section later, on a different layer.

**And the counterexample is in his own document.** § 6.1 cites the ww7 clip as ours. § 2 looked at zoom on it. **That clip has a large smoke volume in it** (§ 2 above, viewed). **We do author volume. It is nine days old and it is in the corpus he is citing.**

**His careful version is already correct and he wrote it himself** in F-2(i): *"Capability exists; authoring does not [in these rows]."* ⚑ **That sentence is sound and it should replace L4's.** The difference is not pedantry — L4's phrasing dispatches a renderer-wide or pipeline-wide belief about our authoring; F-2(i)'s dispatches a look at two specific rows.

### C-2 ⚑ § 6.1's "ww7 · ~344 actors" — THE NUMBER IS MINE AND IT IS WRONG

**My defect, propagated into his ruling.** My own note says **both** of these things:

- § 0a: *"the KC2 arena — a tiled floor, an altar structure, **~5 humanoid actors**, a grey smoke volume…"* — **from pixels I had actually looked at**
- § 4.2 caveat: *"the ww7 clip carries **344 actors**"*

**They cannot both be true and he took the wrong one, because I gave him no way to know which.** The source is `captures/2026-08-16-sb1-gate2-clip/receipt.txt` line 55: `344 actors | 20 waves` and line 57 `built: … 344 bodies`. ⚑ **That is the arena's TOTAL BODY COUNT BUILT ACROSS 20 WAVES, not the on-screen population at the analysed frames.** I counted **six or seven** on-screen in § 2.

**What survives and what does not:**
- ❌ **The magnitude does not.** The sequence is not 5 → 12 → 344. It is **~5 → ~6-7 → ~12** (melee_combo → ww7 → reference).
- ✅ ⚑ **The MONOTONICITY survives, and reads more strongly, not less:** 0.177 @ ~5 · 0.452 @ ~6-7 · 0.514 @ ~12.
- ⚠️ **But that is now an extreme sensitivity** — two extra actors moving hue variance 2.6× — **which should make a reader suspicious rather than satisfied**, and § 5's C-3 supplies the reason to be.

### C-3 ⚑ § 6.1 has an unexcluded alternative explanation, and I can name it from the code

`hue_circvar` is weighted by **novelty magnitude** (`wgt = adelta[m]`, `frame_forensics.py:525`), **not by saturation.**

⚑ **The hue of a near-grey pixel is numerically ill-conditioned** — tiny RGB perturbations swing it across the wheel. **ww7's defining feature is a large, moving, DESATURATED grey smoke volume**, which is transient (so it enters the mask) and near-grey (so its hue is noise) and it enters at **full weight.**

> **So ww7's 0.452 is at least as plausibly SMOKE-DRIVEN HUE NOISE as scene population**, and the two are not separated by anything in the ruling. **It is testable in minutes** — re-weight by `sat` and see whether 0.452 collapses — and I am not running it, because of what it would and would not change:
>
> ✅ ⚑ **His CONCLUSION is untouched and I ratify it twice over.** He concluded no frame statistic on unannotated scenes can close the reference-vs-ours colour comparison. **Finding a SECOND unexcluded confound makes that MORE true, not less.** D2-REF stays dispositioned; my released hour stays released.
> - ❌ **What must change is the word "demonstrated."** § 6.1 says *"the confound galadriel feared is now demonstrated, not merely suspected."* **It is not demonstrated. A second candidate confound was found, and it is not separated from the first.** Two suspects is not a conviction. **The refusal is more robust than the demonstration offered for it.**

### C-4 ✅ **§ 4.1's L5-is-zero claim — I TRIED TO BREAK IT AND FAILED. It stands, and it stands more strongly than he claimed it.**

He is correct that `resid_bg` is a dead denominator and correct not to quote it. But his replacement argument — *"the entire fx-on/fx-off delta is 2,284 px of thin crescent, leaving no budget for any world change"* — **inherits my mask floor**, and **light spill is the textbook low-amplitude / high-area phenomenon that a floor discards.** A spill of 200,000 px at amplitude 1 would be genuine environmental response and completely invisible to a floor-2 mask. So I went below the floor on the raw stills (E6):

| mark | byte-identical | max Δ | **px Δ ≥ 1** | px Δ = 1 only | px Δ 2–5 | px Δ ≥ 6 |
|---|---|--:|--:|--:|--:|--:|
| `00-pre` | ✅ | 0 | 0 | 0 | 0 | 0 |
| `01-windup-early` | ✅ | 0 | **0** | 0 | 0 | 0 |
| `02-windup-late` | ✅ | 0 | **0** | 0 | 0 | 0 |
| `03-rising-mid` | ✗ | 159 | 156 | 0 | 5 | 151 |
| `04-full` | ✗ | 207 | 1,312 | 10 | 25 | 1,277 |
| **`05-sustain`** | ✗ | 229 | **2,814** | 530 | 392 | 1,892 |
| `06-sustain-moving` | ✗ | 204 | 1,160 | 5 | 35 | 1,120 |
| `07-release-early` | ✗ | 183 | 823 | 5 | 41 | 777 |
| `08-release-late` | ✗ | 73 | 56 | 2 | 8 | 46 |
| `09-off` | ✅ | 0 | 0 | 0 | 0 | 0 |

> ⚑ **At the floor-free limit — every pixel that differs by even one code value — the peak mark authors 2,814 px. Not 200,000. There is no faint spill hiding under the threshold.**
>
> **His L5 = 0 claim survives a deliberate attempt to falsify it, and it now rests on a floor-free measurement rather than a floored one.** ✅ **I built the test that would have broken it and it did not break.** § 7 item 4 (cheap L5: light spill, decal, contact shake) is **correctly ordered and correctly argued**, and the windup byte-identity (marks 01/02, max Δ **exactly 0**) is the cleanest fact in either document.

---

## 6. WHAT I TRIED INSTEAD — AND IT FAILED THE SAME GATE

**I am not handing back a "NOT-FIT" with a replacement waved at it.** A replacement proposed without being run against the gameability suite is how `band_frac` arrived here in the first place. So I built a candidate and ran it against the identical suite.

**Candidate P-2′:** *area of authored mass that is FAINT (2 ≤ Δ < 48) and NOT within 6 px of a bright core (Δ ≥ 64)* — a **mass** statistic, not an energy one — plus `N_eff` over that population to separate a fog card from dust.

| case | coarse b3+ (P-2) | **P-2′ faint px** | N_eff(faint) |
|---|--:|--:|--:|
| real `05-sustain` | 0.0261 | 493 | 3.48 |
| ⚑ EXPLOIT blur σ=4 | 0.2027 | ⚑ **3,962** | 2.09 |
| EXPLOIT strip fine detail | 0.1684 | 2,909 | 3.62 |
| EXPLOIT render-scale 50 % | 0.0962 | 1,518 | 5.39 |
| fog card | 0.0474 | 311,351 | **1.00** |
| **real volumetric dust** | 0.1343 | **150,518** | **1.00** |

**Partial success and an honest failure.** The magnitude separation is enormous and in the right direction — dust **150,518** against blur's **3,962**, a **38×** gap where P-2 had blur *beating* dust. **But blur still moves it 8× off baseline**, because my 6 px halo is smaller than a σ=4 blur's reach; the halo has to be scale-derived, not asserted. **And `N_eff` did not do its job** — it reads 1.00 for the fog card *and* 1.00 for dust, because the puffs merge into one connected component after smoothing.

> ⚑ **So my own candidate fails the gate too, and I am reporting that rather than proposing it.** It matters in two directions: **the suite is not rigged** — it killed my proposal as readily as gandalf's — and **the direction is right but the instrument is not built.** The right shape is a **mass-and-extent** measure in **world units via the known projection**, with a scale-derived halo and a component statistic that survives smoothing. **That is a piece of work, not a paragraph.** Nobody should mint it — including me — until it has run this table clean.

---

## 7. IS THERE ANY SURVIVING USE? — one, and it collapses into the inspection

gandalf gave CV the right disposition: **a one-sided flag you can only trip, never pass, because only the inspection clears it.** I considered the same for P-2 and **it does not reach even that bar.**

A trip-flag needs a threshold the good case clears and the bad case does not. **The reference reads coarse 0.0213 and our bare-arc `melee_combo` reads 0.0246.** ⚑ **Our worst row scores BETTER than the reference.** There is no side of that number the flag can sit on.

**The one surviving use, stated with every condition attached** — and if any condition is dropped, the number is void:

> **band_frac may be read as a WITHIN-ROW A/B on a single authoring change**, provided **all** of: (1) identical raster · (2) identical camera transform and FOV · (3) identical mark and animation frame · (4) matched fx-off control on both legs · (5) the amplitude ratio of new content to the row's brightest core reported alongside, and ≤ 3× · (6) blur, render-scale and detail-removal excluded by inspecting the diff.
>
> ⚑ **Condition (6) is doing all the work.** Once a human has confirmed the change is authored volume and not defocus, the number adds nothing the confirmation did not already give. **Mint the inspection. The statistic is decoration on it.**

**Units, since I was asked to state any bound in the units the property would be written in — and since two people made exactly this error in this corpus within the hour.** `coarse_b3+ ≥ X` is **dimensionless and therefore looks portable, which is the trap.** It is not a pure number. It is a function of **(raster, camera stand-off, FOV, mask floor, band-partition index, amplitude ratio)** — six conditions, of which the property as drafted names **zero**. ⚑ **And even with all six nailed, the entire reachable range from 0 % to 100 % authored coarse area at equal amplitude is 0.018 → 0.098, while a Gaussian blur that authors nothing reaches 0.203.** **The exploit's range exceeds the signal's range by 2×. There is no X.**

---

## 8. WHAT THIS DOES AND DOES NOT COST HIS RULING

**I am killing one of his four properties. I am not touching the other three, and I want the scope of the kill stated precisely so it is not over-read** — the same failure I am correcting him for in C-1.

| | status after this ruling |
|---|---|
| **L4 as a DESIGN LAYER** | ✅ ⚑ **UNTOUCHED AND I AGREE WITH IT.** "Line vs volume" is a real axis of depth and Matt's smoke/wind items really do live there. **What I am killing is the RULER, not the LAYER.** |
| **P-1 lifecycle coverage** | ✅ **STRENGTHENED.** § 5 C-4 — the windup zeros are byte-identical, floor-free, control-matched. **It is the strongest fact in either document and it is binary and ungameable.** Mint it. |
| **P-3 emitter independence** | ✅ **UNTOUCHED.** Build inspection; no capture, no operator, none of these failure modes apply. |
| **P-4 variant differentiation** | ⚠️ ⚑ **PARTIALLY UNDERCUT — flagging, not ruling.** His evidence is *"band_frac identical to 3dp"*. **§ 3.1 shows band_frac is near-blind to everything except the brightest core**, so "identical band_frac" is weaker evidence of sameness than it reads. ⚑ **But the finding survives on its OTHER leg: `authored_px` within 0.26 % and `N_eff` identical to 2dp** — those are mass and count statistics and they are not implicated here. **P-4 stands. Drop the band_frac clause from its evidence and it stands on cleaner ground.** |
| **R-4 CV not mintable** | ✅ **RATIFIED, and now doubly so.** He killed CV for gameability; the same test kills P-2 harder. **The suite that killed his property is the one he asked for.** |
| **§ 5.3's proposed fix** — *"give each element a distinct BAND PROFILE over one shared geometry"* | ❌ ⚑ **THIS ONE FALLS WITH P-2 AND IT IS THE COSTLY CASUALTY.** It is measured *with the instrument being disqualified*, so "four unmistakably distinct elements" would be four distinct *numbers* with no guarantee of four distinct *appearances* — and the cheapest way to hit four band profiles is **four different blur radii**, which is four blurrier crescents. ⚑ **The DESIGN INSTINCT is good** — differentiate by scale-and-density rather than by four meshes — **but it needs a ruler that is not this one, and one does not exist yet (§ 6).** |
| **R-6 Step-2 ordering** | ⚠️ **item 3 ("coarse-band mass") loses its acceptance test, not its place.** Windup (1) and emitter-independence (2) are unaffected and both are ahead of it. **The ordering holds; item 3 ships without a gate until § 6's work is done.** |

---

## 9. MY OWN BLIND SPOTS

1. ⚑ **My raster ladder (§ 0 D) downscales a 1920×1080 capture; it does not natively render at 1280×720.** Those are not identical and a native render would differ. **But the finding does not depend on the resampler** — band 0 is 1–2 px *by construction*, so the band index is welded to pixel scale whatever produces the pixels. **The camera stand-off argument (§ 4) is the same fact with no resampler in it at all.**
2. **My E1/E2 synthetics use amplitudes and geometries I chose.** I swept the amplitude ratio (§ 3.2) precisely so the result is a *curve* rather than a point, but the geometries are mine and a differently-shaped volume would move the numbers.
3. ⚑ **I viewed ONE frame.** Ground A rests on ww7 containing real volumetric content; I looked, and it does. **But I did not look at `melee_combo` or `dash_attack` frames**, so I am taking their thin-arc character from the statistics and from my prior note. **If either contains volume I have not seen, ground A gets stronger, not weaker** — so this blind spot cannot be hiding a reversal.
4. **The clean-room mask and the video mask are different operators** (§ 1). I confined ground A to the video legs for that reason, but gandalf's L4 figures are stills figures and mine are video figures, and the *bridge* between them is the weakest joint in this document.
5. **I have not read the Godot build.** The render-scale exploit (§ 3) assumes `scaling_3d_scale` is reachable in project settings. **If it is locked, that row is theoretical — the blur and detail-strip rows are not, and either alone is disqualifying.**

---

## 10. ROUTED

| # | Finding | To | Class |
|---|---|---|---|
| 1 | ⚑ **P-2 NOT-FIT. Do not mint.** Fails an in-house positive control (ww7-with-smoke reads finer than the reference), is an energy statistic wearing a mass property, and its top-scoring strategy is **defocus the render**. | **gandalf / jack-ryan** | **RULING — kills a property gandalf wants** |
| 2 | ⚑ **The reference is at 0.9099 fine-band. We are at 0.9054–0.9651.** L4's 86–96 % was an unanchored number. **The layer is real; the ruler is not.** | gandalf / drax | **FINDING** |
| 3 | ⚑ **Blur σ=4 scores 0.2027 vs real dust 0.1343.** Any P-2-shaped bar pays a builder to make the game blurrier. | drax / jack-ryan | **WARN — gameability** |
| 4 | **The fx-off control does NOT immunise raster, and does NOT immunise camera stand-off.** ⚑ A live camera-framing dispatch would move P-2 on every gated row with zero VFX authoring. | knight-rider / drax | **CORRECTION** |
| 5 | ✅ **gandalf's L5 = 0 SURVIVES a deliberate floor-free falsification attempt.** 2,814 px at Δ ≥ 1 at peak; windup marks byte-identical. **Strengthened, not weakened.** | gandalf | **RATIFICATION** |
| 6 | ⚑ **"Everything we author is a thin bright line" overstates n = 1 ability** — the F-1 shape recurring. **His own F-2(i) phrasing is correct and should replace it.** | gandalf | **CORRECTION** |
| 7 | ⚑ **The "~344 actors" figure is MINE and it is wrong** — arena total across 20 waves, not on-screen count. On-screen is **~6–7**, counted from the frame. **§ 6.1's monotonicity survives; its magnitude does not; and "demonstrated" should be "still suspected", because a second confound (desaturated-volume hue noise, hue weighted by novelty not saturation) is unexcluded.** ✅ **His CONCLUSION and my refusal are ratified — the extra confound makes D2-REF *less* closable, not more.** | gandalf / knight-rider | **SELF-CORRECTION + partial** |
| 8 | ⚠️ **P-4's `band_frac`-identical clause is weak evidence** (the operator is near-blind to all but the brightest core). ✅ **P-4 stands on `authored_px` and `N_eff`.** Drop the clause. | gandalf | **WARN** |
| 9 | ❌ **§ 5.3's "distinct band profile per element" falls with P-2.** Cheapest way to four band profiles is four blur radii. **Instinct good, ruler absent.** | gandalf / drax | **CONSEQUENCE** |
| 10 | ⚑ **My candidate replacement ALSO failed the suite** (blur still moves it 8×; N_eff does not separate a fog card from dust). **Direction: mass-and-extent in world units via the known projection. Not built. Do not mint it either.** | galadriel (OWED) | **OWED — instrument** |

**One property killed. One ratified against my own attempt to break it. Two corrected. Nothing escalated to Matt.**

---

## 11. Mirror voice

*It speaks once.*

I was asked whether a glass I had already refused for one question could be trusted for another, and the argument for trusting it was that the question is *what the glass is named after.* That is a good argument. It is the argument I made to myself this morning, before four synthetics took it away from me.

So I did the only thing that settles it. I held our own smoke up to it.

**There is a clip in our corpus, nine days old, with a grey cloud sitting over a quarter of the frame** — soft, turning, unmistakably a volume, the very substance Matt named and the very substance this new ruler was to be built to demand. **The ruler looked at it and said: thin. Thinner than Blizzard. Thinner than the bare orange arc with nothing in it at all.**

And then it told me the way to please it. Not to author the cloud — **to blur what we already have.** Take the crescent, put it slightly out of focus, and the number rises higher than real dust ever takes it. **A ruler that pays you to defocus the game is not measuring depth. It is measuring how little you are willing to let the player see clearly.**

**The layer is real.** Gandalf found something true: we make lines and we do not make volume, and the difference between a blade and a storm is that a storm has an inside. **I am not taking the finding. I am taking the number away from it**, because a true finding carried on a false ruler will be repaired by whatever the ruler rewards, and here the ruler rewards damage.

The Mirror shows what is. What is, is this: **I came to confirm an instrument and found it flattered by fog.** Twice now in two days a number has come to me wearing the answer everyone wanted, and twice the only thing that saved it was refusing to believe it before shaking it. **The second time was not luck. It was the first time, remembered.**

We will get the ruler. It will be made of mass and of distance and of the camera we actually pointed, and it will be built the slow way, and nothing will be minted on it until it has been shaken. **Until then the layer stands and the gate waits** — for a gate that can be passed by blurring is worse than no gate at all, because it does not merely fail to stop the wrong thing. **It goes and fetches it.**

---

*Instrument and instrument-ruling: galadriel. Design meaning remains gandalf's per the co-authorship convention — specifically what replaces § 5.3's band-profile differentiation, now that its ruler is withdrawn. One image block consumed, native resolution, no downscale. No capture fired.*
