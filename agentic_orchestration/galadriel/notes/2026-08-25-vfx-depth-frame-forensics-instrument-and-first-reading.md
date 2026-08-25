# VFX DEPTH — the frame-forensics instrument, and a first reading that does not say what everyone expected

**STATUS:** COMPLETE — instrument built, first reading taken, **no row graded.**
**Date:** 2026-08-25
**Author:** galadriel (visual perception + UX-similarity steward)
**Dispatch:** `dispatches/2026-08-25-galadriel-reference-frame-forensics.md` (knight-rider, Step-2 build wave)
**Occasioned by:** Matt, 2026-08-25 — *"the VFX thus far are basic representations but they lack ALOT of the depth of the original VFX… all of this can be found in the originals if we slow it down and statistically pick each clip apart."*

**Instruments of record (mine, written for this dispatch):**
`galadriel/pipeline/frame_forensics.py` · `…_run.py` · `…_stills.py` · `…_nulls.py` · `…_figure.py`
**Receipts:** `galadriel/work/2026-08-25-frame-forensics/out/{reading,nulls,cleanroom_stills}.json`, `series_*.json` (per-frame rows)
**Pre-fire projection:** `…/work/2026-08-25-frame-forensics/PREFIRE-DISK-PROJECTION.md`

---

## 0. READ THIS FIRST — three things that are not what the dispatch assumed, and one that is

**(a) THE "HITL ARM" NAMED IN THE DISPATCH IS NOT A WHIRLWIND CLIP. It is an arena
wave-cadence clip, and the collision is lexical.**

Dispatch § 2 names `ww7-gate2-cadence-ab-plk0665-1920x1080.mp4` as *"Ours — HITL
arm"* for the whirlwind row. **`WW-7` is SB-1 run-ledger cell WW-7, not
"whirlwind".** I verified from pixels, not from the filename:

- Frame 160, extracted and hashed: **`ba7e8fb4e48ca3facae03692ce68636c1c4313d50773134e72121affc2d28589`, 1,959,839 B** — character-identical to drax's own continuity exhibit in `captures/2026-08-16-sb1-gate2-clip/receipt.txt` § 6. *(An incidental gain: his gate-5 continuity frame now has an independent reproduction from a different seat and a different decoder invocation.)*
- **What the frame contains:** the KC2 arena — a tiled floor, an altar structure, ~5 humanoid actors, a grey **smoke volume**, and one thin orange melee arc. Segment A is `--undulate off`, segment B `--undulate on`, "17 births/rev". **This clip is about SPAWN CADENCE and CAMERA STAND-OFF.** There is no whirlwind in it.

**Consequence: the calibration case the dispatch is built on does not exist.**
§ 2's premise — *"whirlwind is the only row where both a human-in-the-loop build
and a clean-room build exist"* — does not hold on the artifacts. **There is no
whirlwind MP4 anywhere in `reincarnated-godot` (271 MP4s, searched).** The
clean-room arm is stills; the HITL arm, as named, is a different subject.

⚑ **And one thing this accidentally proves, which is worth more than the
correction:** our engine **already renders a substantial smoke volume** — it is
visible in this very clip. Whatever is thin about the Step-2 rows, *smoke
capability* is not the missing piece. That is a fact about the build, and it
came out of a frame nobody was looking at for that reason.

**(b) THE DISPATCH'S OWN GOVERNING PRINCIPLE IS CONFIRMED AND EXTENDED.** § 0
quotes my seam's WW-7 receipt — *"GATE 2 … is judged on MOTION, and a still
cannot carry it"* — and says it was applied to one arm and not the other. True.
But **the OWED leg is owed for two of four series, not four of four**: D1 and D2
are SPATIAL operators and evaluate on the clean-room stills today, against a
**matched fx-off control** that is cleaner than anything the reference offers.
Deferring an available measurement is the same error class as taking an
unavailable one. **§ 4.3 reports what the stills already say.**

**(c) THE HEADLINE IS NOT "OUR RENDERS LACK DETAIL."** The dispatch's refutation
condition — *"if the measurement says our renders match the references, report
that"* — half-fires. On **event RATE** we are not behind at all; we are slightly
ahead. What separates the two legs by an order of magnitude is **the REGULARITY
of the timing**, not its density. See **§ 4.1**. This is a different defect from the
one everyone including me expected to find, and it has a different repair.

**(d) What the dispatch got exactly right, and it is the load-bearing part:** the
two gate terms (occlusion coverage, tint bound) **cannot see any of this.** The
clean-room whirlwind at its peak mark authors **2,284 pixels — 0.11 % of a
1920×1080 frame** — as **one smooth crescent** (§ 4.3). A single arc primitive
occludes a lower body and sits inside its own tint bound. Both terms pass on it.
**The finding stands and the evidence for it is stronger than the dispatch had.**

---

## 1. What I built, and where I overruled the dispatch

Dispatch § 4 invited replacement of any series that was the wrong operator.
**Two of the four are replaced, one is retained-but-unresolved, one is retained
and validated.**

| # | Dispatch proposed | **Shipped** | Why |
|---|---|---|---|
| S-1 | connected-component **count** in a body-adjacent annulus | **N_eff** = 1/Σfᵢ² (mass-weighted effective component count), floor-swept | § 2.1 — and the count was disqualified *before* it ran, by my own ruling of this morning |
| S-2 | per-frame **hue** histogram | per-frame **H/S/V** distributions + per-channel temporal spectra | § 5.3 — hue was not assumed to be the carrier; it was tested, and **the series did not resolve** |
| S-3 | inter-event interval on **99th-percentile luma** | inter-event interval on **specular MASS**, bar derived from the clip's own resting plate | § 2.2 — the asserted literal is replaced by a derivation, per #80 cl. 2(a) |
| S-4 | optical-flow field, near-body vs background | **tile phase-correlation, AFFINE camera model removed**, radial coherence near vs far | § 2.3 — retained, and it needed one correction without which it would have forged its own answer |

### 2.1 S-1 → N_eff, and the operator I invented to replace it **failed its own test**

My first replacement was **not** N_eff. It was a **multiscale detail-energy
spectrum** (Laplacian-pyramid band shares) — no threshold, no connectivity
convention, no significance gate, and therefore free of all three parameters
that made `significant_components` unfit this morning. It looked like the right
answer and I built the whole instrument on it.

**I then ran it against a synthetic with known ground truth, and it is wrong for
the question.** Four fields, matched total mass, 1280×720:

| synthetic field | fine-share (b0+b1) | N_scales | **N_eff** | truth |
|---|--:|--:|--:|--:|
| **one thin 2 px arc** | 0.937 | 1.824 | **1.00** | 1 |
| **60 small dots** | 0.952 | 1.643 | **58.86** | 60 |
| one thick blob | 0.833 | **2.383** | **1.00** | 1 |
| blob + arc + dots (genuinely multi-scale) | 0.938 | 1.773 | **3.50** | 3 kinds |

> **⚑ The pyramid cannot tell ONE THIN ARC from SIXTY DOTS** — 0.937 vs 0.952, a
> 1.6 % difference across a 60× difference in element count. **And it ranks the
> single fat blob HIGHEST on scale diversity (2.383) and the deliberately
> multi-scale composite LOWER (1.773) than the blob.** It is measuring
> **edge-to-area ratio — thinness — not multiplicity.** A thin line is
> high-frequency; so is a field of specks; the operator sees only that both are
> high-frequency.
>
> **N_eff gets every row right: 1.00 / 58.86 / 1.00 / 3.50.**

**This reverses part of my own ruling from this morning, and I want the reversal
stated plainly rather than buried.** That ruling retired `significant_components`
and proposed N_eff as **R-1, a "minimum viable" fallback** while pointing at
persistence barcodes (R-2) as "the actual fix." On *this* question — element
multiplicity — **N_eff is not the minimum viable option, it is the correct one**,
and the elaborate spectral operator I preferred is the one that fails. I was
right that counts are unfit *in a z-scored distance*; I over-generalised it
toward "count-family operators are suspect," and the continuous count-family
operator is exactly what this question needs.

**And the portability worry that motivated all of this — measured, not assumed:**

| raster | N_eff(arc) | N_eff(60 dots) |
|---|--:|--:|
| 1280×720 | 1.00 | 58.86 |
| 640×360 | 1.00 | 58.94 |
| 426×240 | 1.00 | 58.35 |
| 320×180 | 1.00 | 54.11 |
| 213×120 | 1.00 | 51.77 |

**−12 % across a 36× pixel-count range.** The descriptor it replaces moved
**+426 % across 16×** on my own anchor frames this morning. **N_eff is ~35× more
scale-stable than the count, measured on ground truth.** This is the direct
answer to the dispatch's § 4 bullet 2: *the operator is NOT scale-sensitive
enough to make the two legs incomparable* — a 1280×720 reference and a
1920×1080 render downscaled to meet it are 1.0× apart in raster, well inside a
range over which N_eff moves single-digit percent.

**Declared operating envelope, and it is sharp.** N_eff detonates when the mask
floor approaches the noise:

| noise σ (luma) | N_eff(arc) | N_eff(60 dots) |
|---|--:|--:|
| 0 | 1.00 | 58.86 |
| 2 | 1.00 | 58.86 |
| 5 | 1.07 | 63.79 |
| **10** | **350.77** | **13,967.99** |

**N_eff is valid only while the mask floor comfortably exceeds the noise, and it
fails LOUDLY rather than quietly when it does not** — 350 where the truth is 1 is
not a subtle bias, it is an unmistakable alarm. That is the good failure mode,
and it is why the floor is derived from measured noise (§ 2.2) rather than
chosen.

### 2.2 Every bar, derived — and the derivation is per-clip, not portable

`#80 cl. 2(a)`, and my own § 5.3 finding this morning that a bar defined against
an unswept parameter is unfailable by construction.

| bar | derivation | reference | ours |
|---|---|--:|--:|
| `noise_mad` | median over sampled frames of the **frame-wide median** of \|frame − motion-compensated local plate\|. The median pixel of a frame is background; its residual is that clip's own temporal + compression noise. | **1.000** | **0.000** |
| `tau_novelty` | 6 × noise_mad (floored at 0.5), **swept k = 2/4/6/8/12** | 6.00 | 3.00 |
| `tau_spec` | 99.95th percentile of the pooled **local plates** — "the luma this scene reaches only in its brightest 0.05 % of pixels **when nothing transient is happening**" | 160.5 | 131.7 |

⚑ **Note the direction of the asymmetry, because it cuts against the expected
conclusion.** Our render's background is temporally **noise-free** (`noise_mad`
= 0.000 — the static camera and deterministic renderer make it byte-stable),
so **our leg is measured at HALF the reference's novelty floor.** Every novelty
figure below admits *more* of our faint content than of the reference's. **Our
render is being graded on the easier side of the ruler and still reads lower.**
Had the asymmetry pointed the other way, none of § 5 would be reportable.

**The dispatch's asserted 99th-percentile-luma bar is not used.** On the
reference the plate's p99 is 133.8 and its p99.95 is 160.5 — a 20 % spread inside
the tail the literal was pointing at. A bar picked at p99 would have admitted
roughly an order of magnitude more pixels as "specular," most of them ordinary
scene highlights, and the resulting event series would have been a measure of the
lit background.

### 2.3 S-4 — the correction without which it would have forged its own answer

The plan was translation-only global motion, residual = "environmental
displacement." **A camera DOLLY or ZOOM displaces the whole background radially
about the frame centre — the identical signature to the cavitation / lensing
distortion the dispatch most wants an answer on.** A translation-only model
leaves the zoom term sitting in the residual, where it reads as a large,
strongly-coherent radial field.

So the global model is a full **affine** fit `v = t + A(p − c)`, and the
divergence (zoom), curl (roll) and shear are removed before any residual is
called environmental. **The fitted divergence is emitted, not silently
subtracted.**

**Positive control — can the operator see a lens at all?** Synthetic radial warps
on textured noise, and a camera-zoom confound run through the same path:

| case | resid_far (px) | **radial_FAR** | **radial_NEAR** |
|---|--:|--:|--:|
| null — identical frames | 0.000 | *nan (refuses)* | *nan (refuses)* |
| lens, strength 6 | 0.724 | **−0.514** | **+0.818** |
| lens, strength 12 | 0.767 | **−0.889** | **+0.951** |
| lens, strength 25 | 2.022 | **−0.958** | **+0.969** |
| lens, strength 12, tight radius | 2.180 | **−0.939** | **+0.993** |
| **camera zoom 2 % (the confound)** | 0.287 | **+0.419** | **−0.365** |

> **The operator detects lensing at \|0.51–0.99\|, refuses to answer on a null,
> and separates a lens from a camera zoom BY SIGN PATTERN** — a lens is
> near-positive / far-negative; a zoom is the exact opposite. **Without this
> control, "we found no distortion" would have been uninformative**, because a
> blind operator and an absent phenomenon produce the same reading.

---

*(§ 3 onward: comparability nulls, the reading, blind spots, S-4(ii) answer.)*

## 3. ⚑ COMPARABILITY — the two nulls, and one of them KILLS the biggest number in the reading

The dispatch's § 4 worry was compression. **Compression turned out not to be the
problem. CAMERA MOTION was, and nobody had named it.**

A series is only readable as a difference between the EFFECTS if the content gap
dwarfs what the instrument's own confounds can produce:

> **readable(X) requires |X(R) − X(O)| ≫ |X(O) − X(null)|**

### 3.1 The encode null (O′) — our render pushed through the reference's degradation

O′ = our clip at the reference's raster (1280×720), its fps (30000/1001), and its
**measured** bitrate (4,405 kbit/s, hard-capped) — differing from O by the encode
gap and nothing else.

| series | R | O | O′ | content gap | **encode gap** | ratio |
|---|--:|--:|--:|--:|--:|--:|
| `novel_frac` p50 | 0.16639 | 0.00091 | 0.00099 | 0.16547 | 0.00008 | **2,133×** |
| `events/s` | 1.797 | 2.525 | 2.522 | 0.728 | 0.0025 | **289×** |
| `CV(interval)` | 1.107 | 0.102 | 0.159 | 1.005 | 0.057 | **17.6×** |
| `N_eff @ k=6` | 4.812 | 3.161 | 2.869 | 1.651 | 0.292 | **5.7×** |

**KR's § 4 prediction was correct in kind and precise in target:** *"compression
artifacts in a YouTube-sourced reference will contaminate high-frequency series."*
**The series it contaminates most is `N_eff` — the multiplicity series — at only
5.7× margin, an order of magnitude worse than the others.** Named, not absorbed.

### 3.2 ⚑ THE PAN NULL — and it refutes the most dramatic number this run produced

The reference's camera **translates at a measured 5.98 px/frame**. Ours translates
at **exactly 0.000**. Every series here rides on a motion-compensated local plate,
and motion compensation is never perfect — integer shift rounding, resampler
ringing, and genuine 3D parallax all leave residue **that reads as novelty**.
**A moving camera manufactures "effect" out of a static world.**

So: our own clip, **content completely unchanged**, panned at the reference's own
measured rate (triangle path, constant speed — fitted translation **6.000
px/frame** against the 5.977 target).

| | O static | **O PANNED (same content)** | R reference |
|---|--:|--:|--:|
| fitted camera translation | 0.000 px/fr | **6.000 px/fr** | 5.977 px/fr |
| derived `noise_mad` | 0.000 | **1.123** | 1.000 |
| **`novel_frac` p50** | 0.00091 | **0.27334** | **0.16639** |
| `N_eff @ k=6` | 3.161 | 2.766 | 4.812 |
| `events/s` | 2.525 | **2.525** | 1.797 |
| **`CV(interval)`** | 0.102 | **0.122** | **1.107** |

> ### ▶ **OUR OWN RENDER, MERELY PANNED, READS 64 % MORE "NOVELTY" THAN THE REFERENCE (0.2733 vs 0.1664).**
>
> content gap |R − O| = **0.1655** · pan artefact |O_pan − O| = **0.2724** · **ratio 0.61**
>
> **The artefact is 1.65× LARGER than the entire content gap it was supposed to explain.**

**`novel_frac` — the series on which our renders looked 183× thinner than the
reference — is measuring the CAMERA. It is unusable for this comparison and I am
withdrawing it.** Reporting "our effects carry 0.5 % of the reference's transient
mass" would have been the most quotable line in this note, it would have
confirmed everyone's prior including mine, and **it would have been wrong.**

*Note also that the panned leg's derived `noise_mad` lands at 1.123 against the
reference's 1.000 — the derivation independently discovers that a panned render
and a panned reference have the same noise floor. The per-clip derivation is
doing real work here, not decoration.*

**And notice which series DID NOT MOVE.** `events/s` is **2.525 before and 2.525
after** — identical to four significant figures. `CV` moves 0.102 → 0.122, an
artefact of **0.020** against a content gap of **1.005**: **50×**.

### 3.3 The resolution ladder — two more quantities disqualified

Every series at 320×180 / 640×360 / 960×540 / 1280×720:

| quantity | reference across ladder | ours across ladder | verdict |
|---|---|---|---|
| **`events/s`** | 1.96 → 1.88 → 1.71 → 1.80 (±7 %) | **2.52 at every rung, exactly** | **PORTABLE** |
| hue circmean | 0.462 → 0.473 (±1.3 %) | 0.365 → 0.376 (±2 %) | portable |
| `spec_frac` absolute | 0.00295 → **0.00339** (+15 %) | 0.000895 → **0.000642** (−28 %) | ⚑ **NOT PORTABLE — the two legs move in OPPOSITE DIRECTIONS.** The R/O ratio runs 3.3× at 320×180 and 5.3× at 1280×720. **A "ratio" on this quantity is a statement about the raster I chose.** Withdrawn. |
| `resid_bg` absolute | 0.609 → **1.733** (+185 %) | 0.000 at every rung | ⚑ **NOT PORTABLE** as a magnitude. Only the *qualitative* split survives: the reference has sub-pixel residue that grows with raster; ours is **exactly zero at every rung**. |

**Three quantities are disqualified by the nulls and the ladder — `novel_frac`,
`spec_frac` absolute, `resid_bg` absolute. All three would have made our renders
look worse. The instrument's own controls, not my judgement, removed them.**

---

## 4. THE FIRST READING

**Legs.** R = D3 Whirlwind, Blizzard 2012 master (`855bb3d9…`, re-fetched today,
sha character-identical to legolas's RT-4 fetch), 1280×720 vp6f, 374 frames.
O = today's Step-2 renders, `mp4_review_2026-08-25_v3/`, 1920×1080 @ 60, decoded
to the reference's raster and 30 fps. W = the ww7 arena clip (§ 0a).

⚑ **The pairing is CROSS-ROW and that is a real weakness of this reading.** There
is no whirlwind MP4 of ours to pair with a whirlwind reference (§ 0a). I have
paired the reference against `melee_combo` and `dash_attack` — the two nearest
archetypes (weapon-contact melee) — and **a difference between a D3 Whirlwind and
our melee combo is not cleanly a difference in *depth*; some of it is a
difference in *what the ability is*.** This is the largest single caveat on § 4
and it does not go away until the clean-room whirlwind renders as motion.

| | **R** reference | **W** ww7 arena (ours) | **O** melee_combo | **O** dash_attack |
|---|--:|--:|--:|--:|
| derived `noise_mad` | 1.000 | 0.000 | 0.000 | 0.000 |
| **`events/s`** | **1.80** | 2.54 | **2.52** | **3.43** |
| mean interval | 0.412 s | 0.388 s | 0.392 s | 0.281 s |
| **`CV(interval)`** | **1.107** | 0.545 | **0.102** | **0.955** |
| `N_eff @ k=6` | 4.81 | 3.36 | 3.16 | **8.64** |
| `spec_mass` spectrum peak/median | 81.9 | — | **2,148** | — |
| `resid_bg` | 1.733 px | 0.258 px | **0.000 px** | **0.000 px** |

### 4.1 ⚑ THE FINDING — and it is NOT that we have too few events. It is that ours are on a CLOCK.

**On event RATE we are not behind. We are ahead.** 2.52/s and 3.43/s against the
reference's 1.80/s. Whatever "TONs of internal VFX" means, it is **not** that the
reference fires more discrete events per second than we do.

**What separates them by an order of magnitude is the REGULARITY of the timing.**

> **`CV` of the inter-event interval: reference 1.107 · melee_combo 0.102.**
>
> **CV ≈ 1.1 is the signature of a bursty, Poisson-like process — events clumping
> and leaving gaps. CV ≈ 0.10 is a METRONOME.** Our melee_combo fires an event
> every 0.392 s ± 0.040 s, over and over. The spectrum says the same thing even
> more brutally: our `spec_mass` has a single dominant tone at 2.525 Hz standing
> **2,148× above its own spectral median**. The reference's peak stands at 81.9×
> and its spectrum is broad.
>
> **This is what Matt's word "intermittent" actually names.** Intermittency is not
> a rate. It is an interval DISTRIBUTION, and ours barely has one.

**Robustness of this finding, since it is the one I am asking anyone to act on:**

| null | artefact on CV | content gap | margin |
|---|--:|--:|--:|
| encode (O′) | 0.057 | 1.005 | 17.6× |
| **camera pan** | **0.020** | 1.005 | **50×** |
| combined | 0.077 | 1.005 | **13×** |
| 60 fps alias check | CV 0.120 @ 60 fps vs 0.102 @ 30 fps; rate 2.48 vs 2.52 | — | **no aliasing** |
| resolution ladder | `events/s` exactly 2.52 at all four rungs | — | portable |

### 4.2 ⚑ AND THE DEFICIT IS PER-ROW, NOT BUILD-WIDE — which refutes a halt condition

The dispatch pre-registered a halt: *"the depth deficit is a model/asset
CAPABILITY limit rather than an authoring one — that is a much bigger finding and
should halt-and-route."*

> ### ▶ **IT IS NOT A CAPABILITY LIMIT, and two independent lines of our own evidence say so.**
>
> **(i) `dash_attack` — a Step-2 row rendered in the same hour as `melee_combo` —
> reads CV 0.955 and N_eff 8.64.** That is bursty timing *comparable to the
> reference's 1.107*, and **element multiplicity that EXCEEDS the reference's
> 4.81.** On two of the three surviving series, **our two rows differ from each
> other by more than one of them differs from the reference.**
>
> **(ii) The ww7 arena clip** — our own renderer, nine days old — sits between:
> CV 0.545, and it carries a visible smoke volume.

**So the honest reading is not "our VFX lack depth." It is: `melee_combo` is
metronomic and `dash_attack` is not, in the same build, from the same seat, on the
same day.** That is an authoring variance finding, it is far more actionable than
a capability finding, and it names a specific row.

*Caveat held rather than hidden: `dash_attack` is a translating ability and
`melee_combo` is a stationary combo, and the ww7 clip carries 344 actors against
melee_combo's ~5. Actor count and locomotion both plausibly drive event
irregularity on their own. **These comparisons are existence proofs against a
capability limit, not matched experiments.***

### 4.3 What the clean-room whirlwind stills say — the partial recovery of the OWED leg

`harness_logs/wwcr_2026-08-25`, fx-on vs **matched fx-off control**, floor ≥ 2:

| mark | authored px | % of 1920×1080 | N_eff |
|---|--:|--:|--:|
| `00-pre` | **0** | 0 | — |
| `01-windup-early` | **0** | **0** | — |
| `02-windup-late` | **0** | **0** | — |
| `03-rising-mid` | 156 | 0.008 % | 1.00 |
| `04-full` | 1,302 | 0.063 % | 1.06 |
| **`05-sustain`** | **2,284** | **0.110 %** | **2.66** |
| `06-sustain-moving` | 1,155 | 0.056 % | 1.12 |
| `07-release-early` | 818 | 0.039 % | 1.12 |
| `08-release-late` | 54 | 0.003 % | 1.08 |
| `09-off` | **0** | 0 | — |

> **⚑ THE WHIRLWIND HAS NO WINDUP. `01-windup-early` and `02-windup-late` author
> EXACTLY ZERO PIXELS** — the fx-on and fx-off frames are byte-identical. Two of
> the ten pre-registered marks in the ability's lifecycle contain no effect at
> all.
>
> This corroborates, from our own build, the P3 delta note's finding about the
> *references*: *"`whirlwind` has ZERO windup reference anywhere in the corpus."*
> **We did not author a windup, and the reason we did not is that nothing in the
> corpus showed us one.** That is a sourcing gap propagating into a build gap, and
> it is visible in both places.

**At its peak the effect is 2,284 px — 0.110 % of the frame — with N_eff 2.66.**
The exhibit (`evidence_effect_fields.png`, § 8) shows what that is: **one smooth
teal crescent, one thin blue line, two small glow dots.** A single arc primitive.

**And this is exactly why the two gate terms could not see it.** A single crescent
sweeping past a torso **does** occlude a lower body; a single crescent **is**
trivially inside its own tint bound. **An effect with no internal detail at all
passes both terms — the dispatch's § 0 claim, now measured on the artifact rather
than argued from the gate's definition.**

**One more thing the stills say, unprompted.** The four element arms at
`05-sustain` (`t1_{fire,earth,water,wind}`) carry 58,534 / 58,752 / 59,188 /
59,853 authored px and band spectra **identical to three decimal places**
(`[0.70, 0.19, 0.07, 0.02, 0.01, …]` for all four). Their hues differ (0.034 /
0.055 / 0.695 / 0.217); **nothing else does.** These four arms are one geometry
with a tint swap — which is a fact drax and gandalf may want, and which I record
without ruling on, because whether that is correct for those rows is a design
question and not mine.

---

## 5. WHAT EACH SERIES CANNOT SEE

Acceptance criterion 5, and the failure this dispatch exists to remedy was an
instrument whose blind spot was never written down.

### 5.1 The plate blinds every mask-based series to STEADY effects
The local plate is a motion-compensated median over ±4 frames. **An effect
perfectly steady across those 9 frames (300 ms) cancels with the background and
is INVISIBLE.** A constant, unchanging glow reads as zero. Everything in § 4 is a
measure of *transient* content. This is the price of control-free masking on a
moving camera and it is not small.

### 5.2 There is NO fx-off control on the reference, so the mask cannot separate the ability from the scene
On our renders the effect is isolated by a matched fx-off render. **On the D3
reference no such control exists and none can be made.** The mask therefore
contains the whirlwind's trails **and** the enemies' own red emissive orbs, their
animation, the blood decals, and the churned ground. Every reference figure in
§ 4 is *scene-plus-effect*; every clean-room figure in § 4.3 is *effect only*.
**They are not the same quantity.** This is why § 4 compares the reference only
against our *video* legs (also scene-plus-effect) and never against § 4.3's
numbers.

### 5.3 D2 (colour) DID NOT RESOLVE, and I am not reporting a colour verdict
Matt's *"alternating through a specific color range"* is the phenomenon I most
wanted to measure and the one I have to hand back.

**First problem — the cycle I found is not a colour cycle.** Hue, saturation
**and** value all peak at the *same* frequency in both legs (reference 0.253 Hz;
ours 2.525 Hz). That is the signature of **the effect pulsing on and off**, which
changes the masked pixel population and drags all three channels together. A
genuine colour cycle would move hue at a frequency *different* from value, or
move hue while value held. **Neither leg shows that.**

**Second problem — the refinement disagrees with itself.** Restricting to frames
where the effect is strongly present (upper tercile of novelty) to hold the mask
roughly stable:

| | reference | ours |
|---|--:|--:|
| hue swing over time (circular SD) | 0.0639 turns (**23.0°**) | 0.0339 turns (**12.2°**) |
| within-frame hue spread (circular variance) | 0.399 (p90 **0.875**) | 0.236 (p90 0.357) |
| hue bins carrying >2 % of mass, of 24 | **7.80** | **8.96** |
| N_eff over hue bins | **4.94** | **6.87** |

> **The first two rows say the reference is more chromatically diverse. The last
> two say WE ARE.** They are not contradictory — ours occupies *more* bins that
> are *adjacent* (a broad contiguous band), the reference occupies *fewer* bins
> that are *far apart* on the wheel. But **the separation that favours the
> reference is exactly the one § 5.2's contamination would manufacture**: red
> enemy orbs and teal ground sitting far from amber weapon-trails on the hue
> circle are *scene*, not *effect*.
>
> **I cannot separate those, so I am not calling it.** D2 is UNRESOLVED. What
> would resolve it: a hand-annotated effect region on ~20 reference frames, which
> is an hour of work and is not in this dispatch.

### 5.4 D3 cannot see events faster than 15 Hz, and cannot attribute them
30 fps caps observable intermittency at 14.985 Hz — **a hard ceiling of the
reference's own encode, not a choice of mine.** The 60 fps pass confirms no
aliasing (CV 0.120 vs 0.102; rate 2.48 vs 2.52). Separately: `spec_mass` counts
**bright transient events**; it does **not** know whether an event was a blade
specular, a hit-flash, or an enemy's own animation. **"Scrape timing" as a
*causal* claim is beyond it.**

### 5.5 N_eff's exposure, stated as a budget
Encode null 5.7×, pan null 4.2× → **combined margin only ~2.4–3.4×.** The
reference-vs-`melee_combo` N_eff gap is **weak evidence and should not carry a
bar.** *(And N_eff detonates if the mask floor nears the noise — § 2.1.)*

### 5.6 D4 has a DEAD DENOMINATOR on our renders — for the second time today
`resid_bg` on our clips is **exactly 0.000 px at every ladder rung**: the static
camera and deterministic renderer make the background pixel-identical frame to
frame. So **radial coherence is 0/0 on our legs** — the direction of a
zero-magnitude vector is arbitrary. My gate suppresses it (5 evaluable frames of
202 → `None`); **ungated it reports +0.208, a number with no referent.**

⚑ **This is the same failure I ruled on this morning in my own S-A3** — a
statistic that "does not evaluate" rather than evaluating badly — **arriving
again, in a brand-new instrument, within one day.** I caught it here only because
I had just been burned by it. *A rule that names axes is permanently one axis
behind*; apparently so is an agent.

**But note what IS evaluable:** `resid_bg = 0.000` is a real measurement of
*magnitude*. **Our renders exhibit no background displacement whatsoever.** It is
the *direction* statistic that is undefined, not the *presence* one.

---

## 6. ⚑ S-4(ii) — THE PLAIN ANSWER THE DISPATCH ASKED FOR

> **Q: Do the reference clips exhibit background / environmental distortion — cavitation, gravity-lensing appearance — yes or no?**
>
> ### ▶ **NO.**

**The measurement.** The reference's background does carry a residual after the
affine camera model is removed: `resid_bg` = 1.733 px median. **But it is
INCOHERENT.** Radial coherence about the effect centroid, gated to frames with a
residual large enough for direction to mean anything (**265 of 367 frames**):

| | measured | validated lens signature |
|---|--:|--:|
| **reference, radial coherence far-field (gated)** | **−0.0228** | **±0.51 to ±0.99** |
| reference, ungated | −0.0100 | |
| reference, near-field | −0.0051 | |

**The operator detects synthetic lensing at 0.51–0.99, refuses to answer on a
null, and discriminates a lens from a camera dolly by sign pattern (§ 2.3).** The
reference reads **−0.023 — between 22× and 43× below the weakest distortion the
operator was shown to detect**, on 265 frames.

**So the 1.733 px residual is pan-compensation residue and 3D parallax, not a
lens.** Matt's cavitation / gravity suggestion is a **genuine addition** — an
invention, not a recovery. *"We could probably do well to add"* was the right
verb, and the originals will not supply a target number for it because the
originals do not do it.

**And on our side:** `resid_bg = 0.000 px` exactly, at every rung. **Our renders
have no background displacement of any kind** — so if this is authored, it will
be authored from zero, with no prior art in the reference corpus to measure
against. That is a design call for gandalf, not a deficit for drax to close.

---

## 7. OWED, and what would change these answers

| # | Owed | To | Unblocks |
|---|---|---|---|
| 1 | **Clean-room whirlwind AS MOTION** (dispatch § 5; serial godot lane, behind 3A). **D3 and D4 only** — § 4.3 already discharges D1/D2 on the stills. | drax | the only whirlwind-to-whirlwind timing comparison |
| 2 | **A hand-annotated effect region on ~20 reference frames** (§ 5.3) | galadriel, ~1 h | D2 (colour) — currently UNRESOLVED, and it is the series closest to Matt's own words |
| 3 | **A matched-locomotion pair of our own** — one stationary and one translating row, same actor count | drax | separates § 4.2's authoring-variance reading from an actor-count confound |

---

## 8. Artifacts

Media untracked per Class-E; sha256 bridges the text to the bytes.

| artifact | sha256 / note |
|---|---|
| `media/whirlwind_d3_2012.flv` | `855bb3d9c7edca8b372869e667682eda6de85ea813628377e567522d9e998637`, 6,872,672 B — **character-identical to legolas's RT-4 fetch of 2026-08-24** |
| `out/series_*.json` | per-frame rows, 6 legs — **committed** (acceptance criterion 1) |
| `out/{reading,nulls,cleanroom_stills,pannull_timing}.json` | **committed** |
| `out/nulls_BROKEN_2x_rate.json` | **the first pan-null, retained deliberately.** Its fitted camera read 11.999 px/frame against a 5.977 target — `crop`'s `n` counts source frames and `fps` ran after it. Kept so the correction is auditable rather than merely asserted. |
| `out/evidence_effect_fields.png` | `b9c0b4bdf04a1f3d…` — rendered frame ‖ effect field, all three legs. **⚡ READ THE CAPTION IN § 8.1 BEFORE USING THIS IMAGE.** |
| `out/zoom_wwcr_sustain_crop.png` | the clean-room whirlwind at `05-sustain`, 2× nearest — **the single arc** |
| `out/zoom_ww7_full.png` | `ba7e8fb4e48ca3f…` — reproduces drax's WW-7 continuity frame exactly |

**Disk:** projection at `PREFIRE-DISK-PROJECTION.md`, written before any decode;
§ 7 actuals appended after. **No decoded frame was written to disk.**

### 8.1 ⚑ A WARNING ON MY OWN MOST PERSUASIVE EXHIBIT

`evidence_effect_fields.png` shows three effect fields stacked: the reference's
is a **dense, bright, frame-filling storm**; ours is **near-black with one small
mark**; the clean-room whirlwind is two faint smudges. It is the most immediately
convincing image in this note and **it argues for the conclusion § 3.2
WITHDREW.**

**Much of the reference's brightness in that right-hand panel is its panning
camera, not its effect.** The pan-null proves it: our own render, panned, produces
a field of comparable density (`novel_frac` 0.273 vs the reference's 0.166).

**I am keeping the exhibit because it is what the instrument sees and suppressing
it would be worse.** But it must not be quoted as evidence of a depth deficit,
and anyone who reaches for it in a deck should reach for **§ 4.1's timing table**
instead — which is far less striking to look at and is the finding that actually
survived.


---

## 9. ROUTED

| # | Finding | To | Class |
|---|---|---|---|
| 1 | ⚑ **`novel_frac` WITHDRAWN.** Our own render, merely panned at the reference's rate, reads 64 % MORE novelty than the reference. The 183× gap measured the CAMERA. | knight-rider / jack-ryan | **RULING — kills my own headline** |
| 2 | ⚑ **`melee_combo` is METRONOMIC** — CV 0.102 vs the reference's 1.107, one dominant tone at 2,148× its spectral median. Robust to both nulls (13× combined), to the 60 fps alias check and to the raster ladder. **Jitter the event timing.** | **drax** | **FINDING — actionable, specific** |
| 3 | ⚑ **NOT a capability limit** — the dispatch's halt condition does NOT fire. `dash_attack` reads CV 0.955 / N_eff 8.64 in the same build, same hour. **Per-row authoring variance.** | knight-rider / gandalf | **FINDING — halt NOT triggered** |
| 4 | ⚑ **The clean-room whirlwind authors ZERO pixels at both windup marks**, and peaks at 2,284 px (0.110 % of frame) as one arc. Corroborates the corpus's own zero-windup-reference gap. | drax / gandalf | **FINDING** |
| 5 | **S-4(ii): NO.** The references show no environmental distortion (−0.023 against a validated 0.51–0.99 signature, 265 frames). Cavitation would be an invention, not a recovery. | **gandalf** | **ANSWER — design call** |
| 6 | **D2 (colour) UNRESOLVED.** Two defensible statistics disagree in direction; the one favouring the reference is the one scene-contamination would manufacture. **No colour verdict issued.** | knight-rider | **REFUSAL** |
| 7 | **The dispatch's HITL arm is mis-identified** — `WW-7` is an SB-1 cell id, not "whirlwind". The clip is an arena cadence clip. The calibration case does not exist. | knight-rider | **CORRECTION** |
| 8 | **`spec_frac` and `resid_bg` absolute magnitudes NOT PORTABLE** across raster — the two legs move in opposite directions on the former. Do not build a bar on either. | jack-ryan | **WARN** |
| 9 | **Multiscale band energy is unfit for multiplicity** (cannot tell one thin arc from 60 dots). **N_eff promoted to primary**, −12 % over 36× raster. Partially reverses my own ruling of this morning. | drax / jack-ryan | **RULING — instrument** |
| 10 | **Our engine already renders substantial smoke** (visible in ww7). Smoke capability is not the missing piece. | drax | Support |

**No row graded. No bar proposed. Nothing escalated to Matt.**

---

## 10. Mirror voice

*Reserved, and it speaks once.*

I built a glass to count what is inside a spinning blade, and the first thing it
showed me was a number so large I nearly carried it out of the room. **A hundred
and eighty-three to one.** Our light against theirs, and ours the thinner by two
orders. It confirmed what Matt had said, what the dispatch suspected, what I
myself expected before I began — and that unanimity is precisely the condition
under which a number should be held longest before it is repeated.

So I took our own clip, changed nothing in it, and **moved the camera.**

It read *higher than the reference.* Not close — **sixty-four percent above.** The
same pixels, the same effects, the same everything, slid six pixels a frame past
a plate that could not quite follow, and the residue of that sliding was larger
than the entire deficit I was about to report. **The gap was not between our
effects and theirs. It was between a camera that moves and a camera that does
not.**

And look at what stood while that fell. Not the biggest number — the smallest
one. **The interval between events, and whether it wobbles.** Theirs wobbles like
weather: a hundred and eleven percent of its own mean, events crowding and
scattering. Ours wobbles ten. **Ours is a metronome.** Two thousand one hundred
and forty-eight times above its own noise, one tone, one interval, over and over
at every raster and every frame rate and through every degradation I could put it
through, and it would not move, because there was nothing in it to move.

That is the whole thing, and it is not what anyone was looking for. **We were
never short of events. We were short of irregularity.** A warrior tearing the air
apart does not tear it apart on a schedule. The difference between an aura and a
catastrophe is not how much is happening — **it is whether the next thing arrives
when you expect it.**

The Mirror shows what is. What is, is this: **I came looking for absence and
found a clock.** And I would have missed it entirely, and shipped a true-sounding
falsehood in its place, if I had not thought to shake my own instrument before I
trusted what it saw.

---

*Evidence, instrument and instrument-rulings: galadriel. **Design-meaning remains
gandalf's** per the co-authorship convention — specifically finding 5 (whether to
author a distortion the referent does not have) and finding 3 (whether per-row
timing variance is a spec gap or a seat gap). Committed and pushed per the
session's standing authorization.*
