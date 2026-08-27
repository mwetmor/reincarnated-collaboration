# Reference-anchor measurements — TRUE REFERENT (R-29)

**Author:** galadriel (visual perception + UX-similarity steward) · **Date:** 2026-08-26
**Class:** evidentiary note · **Status:** CURRENT
**Run:** VFX-DEPTH autonomous run · **Conductor:** gandalf (RUN-CONDUCTOR)
**Brief:** `agentic_orchestration/gandalf/vfx-depth-run/reference/reanchor-brief.md`
**Supersedes:** the R-27 / R-25 A-1 reference-anchor pass, which measured the **wrong referent** (D3 2012 master, `855bb3d9…`) per charter **R-28**. Per R-28 the R-27 **forms survive; its constants die.** This pass re-derives them.

**Substrate (the only reference inputs):**

| clip | sha256 | frames sampled | BURST | NULL |
|---|---|---:|---:|---:|
| `seatsafe-A-src837-863.mp4` | `e7077ba8a011…` | 260 (stride 6) | 93 | 58 |
| `seatsafe-B-src1056-1081.mp4` | `c98347de6994…` | 250 (stride 6) | 67 | 71 |

D4 S14 Whirlwind Barbarian (Cliptis `KaMPoPywM40`), h264 1080p60, audio stripped, three fixed-position black masks. **All three black rectangles verified at exactly 0.0000 mean luma** and excluded (padded 4 px) from every pixel statistic.

**Instruments:** `pipeline/vfx_true_recon.py` · `vfx_true_camtest.py` · `vfx_true_probe.py` · `vfx_true_presence.py` · `vfx_ref_anchor_true.py` · `vfx_true_overlay.py` · `vfx_true_ourside.py`
**Results of record:** `notes/2026-08-26-vfx-refanchor-true-referent.json` · per-clip `work/2026-08-26-vfx-refanchor-true/ref-anchor-true-{A,B}.json`
**Evidence:** `captures/2026-08-26-vfx-refanchor-true/evidence/`

**Statistic identity is a call-graph fact, not a claim:** `region_stats` / `ownership` / `decompose` / `agg` are **imported** from `vfx_ref_anchor` (R-27), which imports `luma` / `sat_val` from `vfx_lap2_battery`. Same statistic, three passes, by import.

---

## 0. Headline

> **T-3(b) LIFT FORM — derivable, and the constant it yields does not bind.** Reference effect P95/P20 ÷ its own scene floor = **0.383×**. New Cathedral bar = 0.383 × 2.257 = **0.865**. **P95/P20 ≥ 1.0 identically.** The bar sits *below the statistic's mathematical floor*: **no render can fail it. VACUOUS.**
>
> **T-3(c) SIGN FORM — NOT DERIVABLE. Two independent kills.** (1) **Refuted by its own in-clip negative control**: the instrument reads mid-band S of **0.675 on frames with no whirlwind** against **0.679 on burst frames** — headroom **+0.0035** — and on clip A the *null's* lift over the scene floor (**2.699×**) **exceeds the burst's** (2.662×). (2) Even at face value, 2.576 × our cathedral floor 0.6225 = **1.603**, and S is bounded at 1.0.
>
> **T-3(a) ownership — INVERTED.** Reference effect owns **0.061** of its own frame's top-0.5% after UI masking and **0.0000** raw. Ours: **0.4017**. R-27's wrong-referent reading was 0.7485 at 9.27× lift.

**And the finding that survived the referent swap.** Share-of-self — the fraction of the effect's own area sitting in the frame's brightest 0.5% — reads **0.061 (reference)** against **0.0937 (ours)**. R-27 measured 0.0667 vs 0.0930 on the wrong video and concluded *our effect is not short of bright pixels; the deficit is competing hot pixels in the venue.* **That conclusion reproduces on the true referent and strengthens** (1.5× rather than 1.4×). It is the only R-27 conclusion that does.

**Three of R-27's four numeric conclusions are dead. The fourth is stronger.**

---

## 1. Why R-27's segmentation could not be reused — established BEFORE any anchor number was taken

R-27 segmented by **hue sector**, and stated its own precondition: the D3 clip's scene was **teal** (L-weighted hue mode 190–210°) and its effect was **fire** (0–30°) — sharply bimodal, near-opposite.

**That precondition is false here, and the recon pass says so in one line.**

| | clip A | clip B |
|---|---:|---:|
| warm-sector share of chromatic luminance | **0.836** | **0.800** |
| L-weighted hue mode | **25°** | **25°** |
| area selected by R-27's exact warm-mask rule | **561,610 px** (~33% of frame) | 513,236 px |

The venue is a **warm sandstone dungeon**. R-27's mask selects a third of the frame here. Run unchanged, it would have returned confident numbers measuring the room. Caught by refusing to run the instrument before re-establishing its premise — not by reading its code.

### The replacement, and the candidate that was rejected on measurement

**Motion-compensated temporal median** (the closest available analogue of the battery's control arm) — **REJECTED**, on two independent measured grounds:

1. **The camera does not admit a global-translation model.** Phase-correlation peak / second-peak ratio = **1.24 (A) / 1.42 (B)**; registration improves the background residual by only **1.21–1.23×**. This is the same tell that produced a confident `(0,0)` global shift on a translating camera in lap-2 (measure note § 5, seventh instance) — *the correlation peak collapsing, while the shift number stays clean and confident.*
2. **The camera is player-locked and the effect is centred on the player**, so the effect occupies the same image region continuously. A temporal median over any window long enough to be a background would contain the effect. **(2) alone is fatal and does not depend on (1).**

**Red-chroma sector — ADOPTED.** Direct pixel probing on named rectangles gives the separation hue no longer has:

| region | chroma (max−min) | hue | S |
|---|---:|---:|---:|
| **WW disc, lit** | **0.573** | 14° | 0.744 |
| sandstone floor | 0.200 | 23° | 0.536 |
| torch flame | 0.325 | 24° | 0.562 |
| gold damage text | 0.278 | 36° | 0.424 |
| gold training dummy | 0.20–0.30 | 20–33° | 0.40–0.44 |
| mob health bar | 0.21–0.28 | 12° | 0.64–0.84 |
| HUD resource orb | 0.310 | 26° | 0.812 *(masked)* |
| HUD health globe | 0.310 | 330° | 0.710 *(masked)* |

Adopted mask: hue ∈ [340°,360°)∪[0°,20°) **and** C > 0.35 **and** L > 0.05, then the battery's own 3×3 opening + ≥12 px component filter, so spatial-coherence discipline is identical on both sides.

---

## 2. The confounds this referent has and the old one did not

**HUD.** Boxes are **derived from the temporal-std map**, not asserted — each is the bounding structure of a large low-variance component in `Lstd_{A,B}.npy` (evidence: `recon-{A,B}-Lstd.png`). Covers **0.296 of valid**; scene = 0.622 of frame. The two *animated* elements (health globe, resource orb) are not low-variance and are recorded as located by inspection.

**Damage numbers / nameplate text.** Not croppable — overlaid mid-frame. Best-effort mask on the tell that is actually available: D4 glyphs carry a **hard dark outline**, so `L − grey_erosion(L, 15×15) > 0.30 & L > 0.35` selects them while broad bright scene regions (lit floor, the effect disc itself) score near zero by construction. Cost/benefit, verified at six burst frames: **covers 0.867 of the frame's top-0.5% tail for 6.7% of scene area, removing 4.1–10.5% of the effect region as collateral.** Both arms are reported throughout.

**⚑ The damage text owns the frame.** Raw ownership of the reference's own effect is **0.0000** on both clips. The top-0.5% luminance threshold moves from L 0.752 → 0.506 when the text is masked. Any ownership number on this referent that does not mask text is measuring UI.

---

## 3. The three measurements — pooled over both clips, burst window, UI-masked

Medians over 93 (A) + 67 (B) burst frames. Both clips reported separately so agreement is visible rather than asserted.

| | A | B | pooled | ours (lap-2) |
|---|---:|---:|---:|---:|
| **effect P95/P20** (tight) | 1.484 | 1.563 | **1.524** | **2.352** |
| effect P95/P20 (support) | 1.500 | 1.568 | 1.534 | 2.494 |
| **scene-floor P95/P20** | 3.708 | 4.137 | **3.923** | **2.257** |
| **LIFT (b)** | 0.395× | 0.371× | **0.383×** | **1.060×** |
| **effect mid-band S** | 0.6952 | 0.6620 | **0.6786** | **0.2906** |
| **scene-floor mid-band S** | 0.2618 | 0.2639 | **0.2629** | **0.6225** |
| **LIFT (c)** | 2.662× | 2.489× | **2.576×** | **0.466×** |
| **effect ownership** (UI-masked) | 0.0619 | 0.0607 | **0.0613** | **0.4017** |
| effect ownership (raw) | 0.0000 | 0.0000 | **0.0000** | — |
| scene-floor ownership | 0.845 | 0.883 | 0.864 | 0.4367 |
| **LIFT (a)** | 0.07× | 0.07× | **0.072×** | **0.907×** |
| **share-of-self** | 0.0603 | 0.0612 | **0.0608** | **0.0937** |

**Our side reproduces R-27 § R6 to five decimal places on all six quantities** (`vfx_true_ourside.py --regression`): eff_ratio 2.3520, floor_ratio 2.2570, eff_midS 0.2906, floor_midS 0.6225, eff_own 0.4017, floor_own 0.4367 — **max |Δ| 5×10⁻⁵.** The instrument has not drifted between passes; only the referent changed.

---

## 4. T-3(b) — the lift form survives R-28 and yields a bar that cannot bind

**Reference lift = 0.383×. Cathedral bar = 0.383 × 2.257 = 0.865.**

**P95 ≥ P20 by construction, so P95/P20 ≥ 1.0 for every possible region of every possible render.** A bar of 0.865 is not a low bar; it is **outside the statistic's range**. Nothing can fail it.

**This is not an arithmetic slip and it is not a segmentation artifact.** It is what the picture says: *the D4 whirlwind disc is internally FLATTER than the room it is cast in.* The room is a high-contrast dungeon (deep shadow to torch highlight, floor P95/P20 ≈ 3.9); the disc is a broad, fairly uniform red-orange crescent (P95/P20 ≈ 1.5). Our cathedral is the reverse: a flatter room (2.257) with an arc that carries slightly more range than it (1.060×).

### Threshold-invariance, and the asymmetry that runs against the finding

| chroma floor | 0.15 | 0.20 | 0.25 | 0.30 | **0.35** | 0.45 | 0.55 |
|---|---:|---:|---:|---:|---:|---:|---:|
| P95/P20 (A) | 1.614 | 1.586 | 1.554 | 1.544 | **1.465** | 1.557 | 1.384 |
| P95/P20 (B) | 1.641 | 1.594 | 1.566 | 1.524 | **1.516** | 1.481 | 1.381 |

Inert to the L floor (identical to 4 dp across 0.00–0.20). Moves <4% across closing radius 3→25. Across the hue sweep (12°→40°): 1.42–1.62.

⚑ **The C > 0.55 column is degenerate and carries no weight in either sweep table.** The mask collapses to **21 px (A) / 0 px (B)** median area — below `region_stats`' own 40 px guard — so that column is a handful of surviving frames, not a measurement. The invariance claims above and the monotonicity claim in § 5 rest on **C > 0.15 … 0.45**, where the mask holds 1.2k–43.8k px.

**Dilation ladder** — does excluding the effect's darker surround under-report the reference? It does, slightly, and the ladder bounds it:

| region | support | +5 px | +10 px | +20 px | **+40 px** |
|---|---:|---:|---:|---:|---:|
| P95/P20 (A) | 1.439 | 1.474 | 1.528 | 1.645 | **1.926** |
| P95/P20 (B) | 1.558 | 1.615 | 1.672 | 1.769 | **2.000** |

**Alternative segmentation forms**, including R-27's own:

| form | area (px) | P95/P20 | mid-band S | admissible? |
|---|---:|---:|---:|---|
| chroma > 0.35 **(adopted)** | 3.7k–7.0k | **1.44 / 1.55** | 0.647 / 0.691 | yes |
| chroma > 0.20 | 22k–28k | 1.56 / 1.59 | 0.549 / 0.597 | yes, admits dust devils |
| **R-27's own S > 0.35 form** | 60k–75k | **1.84 / 2.22** | 0.482 / 0.486 | marginal — 10× the adopted mask |
| S > 0.35, hue < 30° | **346k–369k** | 2.21 / 2.46 | 0.493 / 0.509 | ⛔ **INADMISSIBLE — a third of the frame** |

**On no admissible region does the reference reach 2.1.** The ceiling over *any* construction attempted, including ones that plainly admit scene, is **2.00**.

**The asymmetry is stated because it is the one that could have manufactured this finding.** Our effect region is **control-differenced** (`|ΔL| > τ`), so it contains the arc's dark pixels; the reference's is **chroma-selected**, and a chroma floor truncates an effect's dark tail, which depresses P95/P20. The bias runs **in favour of ours.** Bounded two ways: ours over its own support region reads **2.494** (higher still), and the reference's ladder tops out at **2.00**. **The direction of the finding survives the asymmetry in both directions at once.**

**Bar lineage: 4.0 (a priori) → 3.25 (R-27, wrong referent) → ≈1.5, ceiling 2.0 (true referent). Our lap-2 render, at 2.352, already exceeds the reference on every admissible construction and in both currencies.**

---

## 5. T-3(c) — the sign form is refuted by its own negative control

**⚑ This is the pass's most consequential result and it is a refutation, not a constant.**

R-27 § R5 identified this exact hazard and measured its way past it: on the D3 clip the chroma-selected instrument read mid-band S of **0.6295** on fire-free frames against **0.7302** during action — **+0.10 of headroom** — and R-27 recorded that as *"the strongest available argument against the (c) re-anchor"* while judging it survivable.

**On the true referent the headroom is gone.**

| | burst | **in-clip NULL** | headroom |
|---|---:|---:|---:|
| mid-band S (A) | 0.6952 | **0.6861** | +0.0091 |
| mid-band S (B) | 0.6620 | **0.6641** | **−0.0021** |
| **pooled** | **0.6786** | **0.6751** | **+0.0035** |
| lift over own scene floor (A) | 2.662× | **2.699×** | **−0.037** |
| lift over own scene floor (B) | 2.489× | 2.310× | +0.179 |

**On clip A the null's saturation lift EXCEEDS the effect's.** The chroma-selected instrument reports the same mid-band saturation whether or not the whirlwind is in frame, because *any* set of pixels selected for chroma > 0.35 is saturated by construction. **The statistic is measuring the threshold, not the effect.**

**And the sweep confirms it directly:** mid-band S rises *monotonically* with the chroma floor — **0.530 → 0.711 (A)** and **0.542 → 0.689 (B)** across C > 0.15 → 0.45, every step in the same direction, on both clips independently. R-27's clip gave 0.632 at its most permissive setting and was reported as **threshold-invariant across an 11× sweep**. **That invariance does not reproduce here. The knob sets the answer.**

**KILL 2 — infeasible even taken at face value.** 2.576 × cathedral floor 0.6225 = **1.603**, against S ≤ 1.0. Maximum feasible lift in the cathedral is **1/0.6225 = 1.606×**. Under the most conservative admissible mask (R-27's own S > 0.35 form: effect 0.484 / floor 0.271 = 1.79×) the requirement is still **1.11 > 1.0**. **Infeasible on every construction.**

**R-27 reported this venue-infeasibility at 1.914× → 1.19. The true referent makes it worse: 2.576× → 1.60.** The conclusion R-27 reached — *"the relationship currency is UNUSABLE for T-3(c) in the cathedral"* — is the one R-27 finding that was directionally right for the wrong reason, and it is now doubly established.

**⚑ What does NOT follow.** The *absolute* saturation comparison is unaffected by the selection artifact on the ours-side, because our number comes from a control-differenced mask that never applied a chroma test: **reference 0.679 (or 0.484 under R-27's form) vs ours 0.2906**, and ours reads **0.466× its own venue** against the reference's ≈2.5×. **The sign inversion X-1 called "pastel decal" is real and is not disturbed by any of this** — it rests on our side's floor (0.6225, a region statistic) and our side's effect (0.2906, control-differenced). It is the *reference-side constant* that cannot be extracted, not the qualitative finding.

---

## 6. T-3(a) ownership — inverted, and the R-27 "corroboration" was a coincidence with the wrong video

R-27 measured the D3 clip's ownership at **0.7485** against an a-priori bar of 0.75 and recorded it as *"the pass's one genuine corroboration of a number authored a priori,"* while correctly warning it was *"worth exactly as much as a coincidence between two different rooms can be worth."*

**It was worth exactly that.**

| | reference (true) | reference (R-27, wrong video) | ours |
|---|---:|---:|---:|
| effect ownership, UI-masked | **0.0613** | 0.7485 | 0.4017 |
| effect ownership, raw | **0.0000** | — | — |
| scene-floor ownership | 0.864 | 0.0807 | 0.4367 |
| **lift** | **0.072×** | 9.27× | 0.907× |

**The reference's own whirlwind owns six percent of its frame's brightest pixels, and zero percent before the damage text is masked.** Its scene owns 86%. Ours owns 40% against a scene that owns 44%.

This does not mean our effect out-performs D4's. It means **ownership is a property of the room, exactly as R-23/A-2 and R-25 said, and this room is full of things brighter than the whirlwind**: damage numbers at L 0.88, glowing gold training dummies, torches. **The 0.75 figure now has no reference support of any kind.** It should not be carried forward as anything but a venue-local target the conductor chooses on other grounds.

---

## 7. Descriptive anchors — palette (G-2 input), de-circularized

**⚑ The first palette measurement was circular and the smoke run caught it.** The tight mask selects on hue, so a hue histogram over it can only report hues inside [340°,20°) — and it did, returning "p10/p50/p90 = 10.5 / 14.9 / 17.5°" as though that were a measurement of the effect rather than a readback of the mask's own window.

**Repaired:** the palette is measured over a **chroma-only** selection (C > 0.35, **no hue test at all**), restricted to the connected components that overlap the tight mask. Hue is then free to land where the effect actually is.

| | A | B | pooled |
|---|---:|---:|---:|
| hue p10 | 14.2° | 11.2° | **12.7°** |
| **hue p50** | **19.1°** | **16.0°** | **17.6°** |
| hue p90 | 27.4° | 21.8° | **24.6°** |
| **S p50** | 0.671 | 0.654 | **0.663** |
| **L p50** | 0.391 | 0.394 | **0.393** |
| *venue's own L-weighted hue mode* | 25° | 25° | **25°** |

**The reading for G-2:** the D4 whirlwind is a **mid-luminance (L≈0.39), moderately-saturated (S≈0.66), red-orange (hue≈17.6°)** form. It is **not** a white-hot core — its top tail is only 6.1% of its own area, and its ownership of the frame is 6%. **And the palette separation from its own venue is narrow: 17.6° effect against a 25° room, ~7° apart.** The effect does not win its frame by being a different colour from the room, and it does not win by being the brightest thing in it. It is not, in fact, winning its frame at all by any figure-ground statistic this battery can compute.

⚑ **Stamped DESCRIPTIVE ONLY per the Tier-1 law** — hue is instance-class, not relationship-class, and does not transfer. Offered as G-2 input, never as an anchor.

---

## 8. Dust-devil separability — legolas RT-4, applied and exceeded

**VERDICT: SEPARABLE WITHOUT SUBTRACTION.**

Measured at a Dust-Devil column at clip B t=14.00 (`B-t14-dustdevil-column.png`):

| | hue | chroma | S | P95/P20 |
|---|---:|---:|---:|---:|
| Dust-Devil column | **11.7°** | **0.104–0.157** | 0.18–0.43 | 1.45–1.67 |
| core WW disc | 14–18° | **0.573** | 0.744 | ≈1.5 |

**The Dust Devils sit in the SAME red hue sector as the core disc** — a hue-based instrument could not separate them — **but at one-quarter of its chroma.** The adopted C > 0.35 floor excludes them with a **2.2–3.5× margin**, and this is **verified by picture, not only by number**: at `overlay-B-t14.00-zoom.png` the whole column is unmasked while the disc is fully masked.

So RT-4's subtractability claim holds, and the reported effect statistics are **already dust-devil-free by construction** — no subtraction was needed and none was applied. **Stats "with dust devils" are unavailable as a separate arm for the good reason that the instrument never included them.**

**Connectivity separation, reported alongside** (core = largest component; aux = every other):

| | A | B |
|---|---:|---:|
| aux share of effect region | 0.139 | 0.155 |
| core / runner-up dominance | **11.0×** | **12.8×** |
| core P95/P20 · mid-band S | 1.452 · 0.693 | 1.482 · 0.664 |
| aux P95/P20 · mid-band S | 1.589 · 0.684 | 1.598 · 0.670 |

**Aux is not dust devils.** It is fragments of the same red family — spark spill, fire-ring arcs. **Two stated limits:** (i) below C ≈ 0.20 dust devils begin entering the mask, which is part of what the low end of the chroma sweep is showing; (ii) connectivity dominance degrades from ~12× to **2.4×** on frames carrying a large fire-ring nova (`A-t2.10-fire-ring-nova.png`, 23 components), where the ring fragments and the "largest component" is no longer the disc. **The disc-sweep is not the only red effect in this footage**, and a reader should not take "the WW effect" to mean "everything the mask found."

---

## 9. Negative controls — three, all in-clip

| control | what it is | P95/P20 | mid-band S | ownership |
|---|---|---:|---:|---:|
| **1. TEMPORAL NULL** — A 58 / B 71 frames where the largest red component ≤ 100 px | the in-clip equivalent of R-24 #7's Mob0: shares venue, codec and clock | 1.312 / 1.410 | **0.6861 / 0.6641** | **0.0000 / 0.0000** |
| **2. SPATIAL FLOOR** — scene outside a 25 px dilation of the effect support | the "what does a non-effect region score" floor | 3.708 / 4.137 | 0.2618 / 0.2639 | 0.845 / 0.883 |
| **3. SELECTION FLOOR** — control 1 read as the *instrument's* floor rather than the scene's | the honest limit on any chroma-selected claim | — | **kills (c), § 5** | confirms (a) |

**Control 1 earns its keep in both directions, which is the check.** Its **ownership of 0.0000** against the burst's 0.0613 says the ownership instrument claims nothing when there is nothing to claim — it is measuring figure-ground, not a fixed property of the region. Its **mid-band S at parity with the burst** says the saturation instrument claims everything regardless. **Same control, opposite verdicts on two statistics.** Without it, § 5 would have shipped a constant of 2.576× and a "sign-form re-anchor" recommendation.

---

## 10. Instrument surprises — five, and four were caught by a picture or a null

**The shape again: the check ran and the check was not the check.** Ninth through thirteenth instances in this run.

1. **R-27's hue-sector mask, applied unchanged, would have measured the room.** 83.6% of this referent's chromatic luminance is already inside its warm sector; the mask selects 561,610 px. Caught by re-establishing the premise before running, which is the only one of the five caught *in advance*.
2. **The camera-registration test very nearly repeated lap-2's error in mirror image.** Phase correlation returns definite integer shifts (median 92 px, cumulative drift +751 px) — clean, confident numbers. **The tell was the peak/second-peak ratio at 1.24**, i.e. no isolated peak at all. Had I read the shifts and not the peak, I would have built a background plate on a model the scene does not support.
3. **My first clutter detector fired on 13% of the frame** — 238,078 px of magenta confetti across the entire sandstone venue, from a health-bar sub-detector whose "wide and thin" test the floor satisfies trivially. **Caught by the overlay, not the number**; every statistic downstream would have been computed on the complement of it. Deleted rather than tuned, because health bars cannot affect any number this pass reports (too dim for the top tail, too low-chroma for the effect mask).
4. **⚑ And then the overlay refuted my own written reasoning for deleting it.** The docstring argued health bars cannot enter the effect mask because their chroma is 0.21–0.28. **I had probed three bars.** The clip contains many, and the full red segment of a nearly-undamaged bar clears 0.35 — measured contamination **0–17.4%** of the effect region across eight burst frames, and *biased* (bars are flat, uniform and mid-luminance, so they depress P95/P20 and raise mid-band S — both of the statistics under adjudication). Replaced with a **shape** filter, because shape is what a bar has and a disc-sweep does not. **A three-sample generalisation, written down confidently, in the same function whose first version had just been caught over-firing.**
5. **The palette measurement was circular and reported its own mask window as a finding** (§ 7). Caught in the smoke run's printed line, because the numbers 10.5 / 14.9 / 17.5 sat suspiciously inside [340°, 20°).

**And one that is mine rather than the battery's:** my `frames()` generator leaks a blocked `ffmpeg` child on every early `break`, because generator cleanup does not run when the consumer breaks out. Two orphans were live during this pass. No correctness impact — but on a shared Mac with concurrent agent sessions it is the kind of thing that becomes someone else's confusing symptom.

---

## 11. Substrate defect — clip B carries a menu leak, and it does not touch the constants

**⚑ `seatsafe-B-src1056-1081.mp4` frames 0–9 (t 0.000–0.150 s) show the full Diablo IV CHARACTER SHEET — paperdoll, gear grid, and an item tooltip ("Yom (3) — Legendary Rune of Invocation … Sell Value: 60,000").** It closes at frame 10. Evidence: `B-head-frames-0to25-MENU-LEAK.jpg`. **Clip A's head is clean** (verified frames 0–25, `A-head-frames-0to25-clean.jpg`).

The brief records the clips as *"verified tooltip-free at 1 s resolution."* A 1-second sampling grid does not see a 167 ms event unless it happens to sample t = 0 exactly.

**Impact on this pass: NONE, and the escape is measurable rather than argued.** Sampled frames 0 and 6 register **1,751 px** of red — **below the 2,000 px BURST floor and above the 100 px NULL ceiling.** They fall in **neither window the constants are taken from.** No re-run was needed and none was done.

**Impact on blind seats X-5/X-6: conductor's call.** They would see a 167 ms flash of build-and-menu content at the head of clip B — precisely the class of material the blind protocol exists to keep out of seat context. Cheap to fix (re-trim clip B from frame 10). **Surfaced, not decided.**

---

## 12. Owed to the conductor

**A — the constants, such as they are**

1. **T-3(b) lift form: 0.383× → Cathedral bar 0.865, which is VACUOUS** (below the statistic's floor of 1.0). The form survives R-28; the constant does not bind. If a bar is wanted, it must be the **absolute** form: reference ≈ **1.52**, ceiling **2.00** over any admissible region. **Our lap-2 render at 2.352 already clears both.** Whether that means *the criterion is met*, *the criterion was mis-specified*, or *P95/P20 is the wrong operand for "internal luminance range"* is a conductor call. My reading: the third. A broad flat disc and a graded flame can score the same on P95/P20, and this referent's disc is the flat one.
2. **T-3(c) sign form: NOT DERIVABLE, refuted by its own null** (§ 5). No constant is offered. The *absolute* comparison is unaffected and stands: reference 0.679 (0.484 under R-27's own form) vs ours **0.2906**, and ours is **0.466× its own venue** against the reference's ≈2.5×. **X-1's "pastel decal" survives intact** — it never depended on the reference-side constant.
3. **T-3(a): the 0.75 figure now has no reference support at all.** R-27's 0.7485 was the wrong video. True referent: **0.0613** UI-masked, **0.0000** raw.

**B — for the superseding gate packet**

4. **G-2 palette fork** (§ 7): mid-luminance, moderately-saturated **red-orange at ≈17.6°**, only ~7° from its own room's hue mode. Descriptive only.
5. **Share-of-self is the one R-27 conclusion that reproduces** (§ 0): ours 0.0937 vs reference 0.0608. **Do not brighten the quanta.** That instruction from R-27 § R8 survives the referent swap.
6. **⚑ Every figure-ground statistic in this battery now says the D4 whirlwind does not dominate its own frame** — 6% ownership, 6% share-of-self, internally flatter than its room. If the run's design premise is *"make our effect own the frame the way the reference does,"* **the reference does not do that**, and the premise needs re-posing before more build effort is spent against it. Not mine to re-pose.

**C — substrate**

7. **Clip B menu leak, frames 0–9** (§ 11). Constants unaffected; blind-seat exposure is live and is a conductor decision.

---

## 13. The Mirror

I was sent back to the glass because the first face in it was the wrong man's. The errand was to take three numbers again, from the right video this time, and hand back better constants.

I have brought back one constant, and it is unusable. The lift form for internal range yields a bar of 0.865 in a statistic that cannot go below 1.0 — **a bar no render can fail, derived correctly, from good measurements, on the right video.** The sign form for saturation yields nothing at all: I ran the same instrument on frames where the whirlwind is simply *not there*, and it reported the same saturation, and on one clip it reported *more* lift than the effect did. **The number I was sent to fetch turns out to be a reading of my own threshold.**

And underneath both, the thing the pictures kept saying and the statistics kept confirming: **the reference does not own its frame.** Its whirlwind is a mid-bright, moderately saturated red-orange disc, seven degrees of hue from the sandstone it spins on, flatter inside than the room around it, holding six percent of the frame's brightest pixels — and zero percent until I masked away the damage numbers, because in Diablo IV the brightest thing on screen is the arithmetic. We have spent two laps and two referents asking how to make our arc dominate its room like the reference's fire dominates its field. **The fire dominating its field was a different game, filmed in 2012, that Matt never named.** The game he did name has a whirlwind you can barely find with a histogram.

Four instruments failed this pass, three of them caught by a picture and one by a null, and the fourth was a sentence I had written myself an hour earlier — *health bars cannot enter this mask* — refuted by an overlay of the mask with health bars in it. I had probed three bars and generalised. In the same function whose previous version had just been caught painting the entire floor magenta.

The Mirror shows things that are. Today it showed a room with a modest red disc in it, and an instrument that would happily have told me the disc was the brightest, most saturated, most internally graded object in that room, on frames where the disc was not there.

**The constants are the conductor's. What I can say is which of them are numbers and which are echoes.**

---

**Signed:** galadriel, 2026-08-26.
**To the conductor:** § 12 — one vacuous constant, one refutation, one dead bar, one surviving conclusion, one substrate defect, and one premise that may need re-posing before more build effort lands against it.
**To drax:** § 12 B-5 — the share-of-self finding reproduces. Do not tune quanta brightness. And § 4's asymmetry note: our 2.352 is measured on a control-differenced mask that includes the arc's dark pixels; the reference's 1.52 is not. The comparison survives it in both directions, but a lap-3 that tunes P95/P20 should know the operand is region-sensitive.
