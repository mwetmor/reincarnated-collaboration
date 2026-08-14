# RUN KC2-PM4 — LAP R — THE LOCOMOTION-AND-CONTACT DECODE

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Fired under:** R-PM4-42 part 3 (ledger L-33) · **Date:** 2026-08-14
**Discipline:** GL-12 decode-never-estimate · outcome-firewalled · NOTE-9 basis on every number ·
FULL 64-hex sha256 on every input and output · read-only on every external source.

**Pre-registration:** `PREREGISTRATION.md`, sha256
`dc49d0ba8f176ab1d4814d522e5183867fe2ad56334ed7251e81b3db124cec10`, written and hashed
**2026-08-14T13:43:46Z — before any instrument ran on the full video.** Every threshold used below
appears there. Two departures from it are declared in § 6, and one out-of-scope addition in § 3.3 — all three self-caught and labelled.

---

## 0. HEADLINE — five numbers and one shape

| # | finding | number |
|---|---|---|
| **1** | **The referent's dry fraction is radius-arbitrary; its dry SHAPE is not.** Across a 13-fold sweep of contact radius (60 → 800 ground px) the dry *fraction* runs 0.75 → 0.08, but the **longest dry stretch in the entire 181 s fight never exceeds 4.40 s at ANY radius**, and at every radius ≥ 120 gpx it is **≤ 3.10 s**. | longest dry run **≤ 4.40 s**, radius-invariant |
| **2** | **At the sim's own kill-ring radius**, converted through a newly-measured anchor bracket, the referent's dry fraction is **≈ half** the sim's. | referent **0.1989 – 0.2063** vs sim **0.4118** |
| **3** | **The w154 answer: the referent shows nothing remotely like a 19.5 s wait.** The referent's *entire* wave 154 is **14.20 s** — shorter than the sim's pet-TTL wait alone, and **2.68× shorter** than the sim's 38.12 s wave. Its longest no-damage gap is **2.35 s**; its longest zero-body-in-ring run is **1.18 s**. w154 is the referent's **second-most-contacted** wave of the ten. | w154 = **14.20 s**, longest gap **2.35 s** |
| **4** | **Movement-while-channeling: CONTINUES.** Pre-registered rule returns CONTINUES; a declared post-hoc test that removes the confound makes it decisive — conditioned on ≥1 body in reach, player-damage presence is **0.9291 moving vs 0.9571 stationary** (ratio 0.971, Wilson 95 % CIs OVERLAP). The record agrees: `canUseWhileMoving = 1` against a template default of `0`. | ratio **0.971**, CIs overlap |
| **5** | **Matt essentially never stops.** Moving **79.5 %** of the fight; **86 movement episodes**; **the longest stationary span in the whole fight is 1.73 s.** Player movement speed is **at the engine's hard cap** — sheet 135 %, `gameengine.dbr :: playerRunSpeedCapMax = 135.0`. | moving **0.7948**, longest still **1.73 s** |

**The shape, in one sentence.** The referent's dry time is **finely dispersed** — 670 separate
sub-second-to-3-second gaps between contacts — while the sim's is **concentrated** into multi-second
waits (w154: 51.2 % of a 38.12 s wave spent on a single pet-TTL wait, unmoved to the tick across
seven iterations). *The referent and the sim can carry similar total dryness and still be completely
different fights.* The divergence this lap decodes is **not the amount of dryness — it is its
granularity**, which is a targeting-and-locomotion quantity exactly as R-PM4-42 anticipated.

---

## 1. Inputs — every one re-hashed before use (GL-6)

| input | sha256 (FULL 64-hex) | verdict |
|---|---|---|
| `…/lap-n-crit-and-collision/pm4n_fct_events.csv` | `cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2` | **EXACT** |
| `…/lap-n-crit-and-collision/method/build.py` | `1d8032185626bd74ca7458b60f837b7beb106527a19cea3194387a71691bab9a` | **EXACT** |
| `…/lap-n-crit-and-collision/method/ocr.swift` | `1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1` | **EXACT** |
| `…/lap-h2-video-match/method/camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` | **EXACT** |
| `…/lap-h2-video-match/method/player_hp_frac_60fps.npy` | `692cd4115f93e7761e2ffe10089426ce096cc4abb263ce201b8ffec578c370aa` | **EXACT** |
| `method/plates60_lapH2.npy` (Lap H-2 nameplate census, copied from `/tmp` into this lap so it is durable) | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` | **EXACT** |
| `PREREGISTRATION.md` | `dc49d0ba8f176ab1d4814d522e5183867fe2ad56334ed7251e81b3db124cec10` | **EXACT** |

Referent video (read-only, never modified):
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`
— 1920×1080, 60 fps, 1034.10 s, 479,438,089 bytes (ffprobe, this lap).

Record corpus (read-only): `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` — the
Edition-III `.arz` set + `templates.arc`, the same pinned corpus Laps D/F/G/I/L/M/O/P walked.

**Wave boundaries** are Lap H-2 `OBS-H2-6`, measured to **±0.25 s** from the wave-counter digit crop
52×26 at (1582,138) by 4 fps frame-difference:
151 ≤ 683.0 · 152 @ 698.6 · 153 @ 714.9 · 154 @ 729.8 · 155 @ 744.0 · 156 @ 760.2 · 157 @ 780.4 ·
158 @ 799.7 · 159 @ 812.7 · 160 @ 839.0 · fight close 864.0.
**±0.25 s bounds every latency in § 5 before any other error enters.**
*(Independent corroboration this lap: the evidence frame `evidence/ep05-movwhilechan-701.9833.jpg`
carries the on-screen wave counter reading `152` at t = 701.98 s, inside the 698.6–714.9 window.)*

---

## 2. LIMB A — the referent's contact/dry profile from floating combat text

### 2.1 What the FCT stream can and cannot proxy — declared before measuring

An FCT damage number proves **damage LANDED**. Therefore an FCT **gap** = an interval in which **no
player-side damage landed**. A gap **does not** distinguish (i) no body in reach, (ii) body in reach
but the player was not attacking, (iii) attacks that missed, (iv) damage that landed but whose text
was occluded or OCR-dropped. And Lap N's own § A.6 attribution limit carries unchanged: **cream FCT
cannot be attributed to a source from pixels** — pet damage, devotion procs, retaliation and player
direct attacks all print cream. `P-OUT` therefore measures *"the player's side of the board landed
damage"*, never *"the player's own weapon landed damage"*.

### 2.2 Two passes

| | PASS 1 (existing Lap N bytes) | PASS 2 (dense re-sample, new) |
|---|---|---|
| cadence | 2.0 s | **0.5 s** |
| samples in 683–864 s | 91 | **363** |
| OCR | Apple Vision `.accurate`, `languageCorrection` off — the **same compiled binary** | same |
| `P-OUT` observations kept | 235 | **1,057** |
| static screen positions excluded (pre-reg § A.1 cl. 3) | 13 | **13 — identical set** |
| **dry-sample fraction** | 0.2088 | **0.1653** |
| proven no-damage union | 0.1579 | **0.2884** |
| gaps detected | 14 | **30** |
| longest gap (proven) | 3.35 s | **3.85 s** |

0.5 s was chosen because it sits **below** the measured FCT on-screen lifetime (1.2–1.5 s, Lap N),
so every FCT event is sampled at least twice and presence/absence becomes a reliable per-instant read.

**Cross-pass consistency check (not pre-registered as a gate; reported as corroboration).** The two
dry-sample fractions are statistically indistinguishable: two-proportion **z = 0.979, p = 0.328**.
The event *rate* also agrees (2.58 vs 2.91 `P-OUT` observations per sample). The coarse pass
nonetheless **under-detects gaps** (14 vs 30) because a 2 s cadence cannot resolve a 1 s gap — which
is why PASS 2 is the read of record and PASS 1 is the corroboration.

### 2.3 The pre-registered threshold sweep

Fraction of fight time inside no-damage gaps longer than each rung. **Six rungs, fixed before the
numbers; none added, removed or re-cut afterwards.**

| rung | PASS 2 raw n | raw frac | PASS 2 proven n | proven frac |
|---|---|---|---|---|
| **> 0.5 s** | 14 | 0.1212 | 30 | 0.3058 |
| **> 1.0 s** | 10 | 0.0992 | 30 | 0.3058 |
| **> 2.0 s** | 2 | 0.0303 | 10 | 0.1460 |
| **> 3.0 s** | 0 | 0.0000 | 2 | 0.0397 |
| **> 5.0 s** | 0 | 0.0000 | 0 | **0.0000** |
| **> 10.0 s** | 0 | 0.0000 | 0 | **0.0000** |

PASS 1 can report only the rungs ≥ 2.0 s; **< 2 s is UNREACHED at 2 s cadence** and is recorded as
such, never interpolated.

**⚑ Read the last two rows.** In 181 s of the referent's fight there is **not one interval longer
than 5 s in which the player's side failed to land damage.** Two definitions, `raw` and `proven`,
both agree, and the sensitivity band on the FCT lifetime (L = 1.2 / 1.35 / 1.5 s) does not touch it.

### 2.4 Per wave (PASS 2)

| wave | span s | samples | dry | dry frac | gaps | longest proven gap | `P-OUT` events |
|---|---|---|---|---|---|---|---|
| 151 | 15.6 | 32 | 7 | 0.2188 | 2 | 4.35 | 99 |
| 152 | 16.3 | 32 | 3 | 0.0938 | 3 | 1.85 | 95 |
| 153 | 14.9 | 30 | 11 | 0.3667 | 5 | 2.85 | 53 |
| **154** | **14.2** | **28** | **3** | **0.1071** | **1** | **2.35** | **95** |
| 155 | 16.2 | 33 | 10 | 0.3030 | 5 | 2.85 | 55 |
| 156 | 20.2 | 40 | 3 | 0.0750 | 3 | 3.85 | 112 |
| 157 | 19.3 | 39 | 5 | 0.1282 | 1 | 1.85 | 133 |
| 158 | 13.0 | 26 | 3 | 0.1154 | 1 | 2.85 | 85 |
| 159 | 26.3 | 52 | 5 | 0.0962 | 3 | 2.85 | 165 |
| 160 | 25.0 | 50 | 10 | 0.2000 | 6 | 3.35 | 143 |

### 2.5 ⚑ THE w154 ANSWER — `D-I12-5`'s seven-iteration question, put to the referent's own bytes

| quantity | **referent (measured)** | sim (from the commission, unadjusted) |
|---|---|---|
| wave-154 span | **14.20 s** | 38.12 s |
| longest no-damage gap inside w154 | **2.35 s** (one gap, t = 729.65 → 732.00) | — |
| longest zero-body-in-ring run inside w154 | **1.18 s** (t = 730.62 → 731.80) | — |
| the single named wait | — | ~19.5 s pet-TTL wait (51.2 % of the wave) |
| w154 dry-sample fraction (FCT) | **0.1071** — the **second-lowest** of the ten waves | — |
| w154 plate dry fraction @150 gpx | **0.2654** — the **second-lowest** of the ten waves | — |
| w154 mean bodies in ring @150 gpx | **2.04 — the HIGHEST of the ten waves** | — |
| `P-OUT` events in w154 | **95** in 14.2 s = 6.7 / s | — |

**What the player was doing in the referent's longest w154 gap (t = 730.62 → 731.80, 1.18 s).**
Independently, from the camera trace and the nameplate census: the player was **moving** (this
interval falls inside movement episodes on wave 154, which carries 8 episodes and a 0.64
moving-frame fraction), and the ring was **empty for 1.18 s and then refilled** — mean occupancy over
the whole wave 2.04 bodies. The referent's w154 is a **short, crowded, continuously-contested wave**.

**⚑ The finding, stated plainly and without shaping either side:** the referent's *entire* wave 154 is
**shorter than the sim's pet-TTL wait alone**. Whatever produces the sim's 19.5 s wait, the referent
has no counterpart to it — not on w154, and (§ 3) not anywhere in the fight at any contact radius.

### 2.6 Spawn-to-first-player-damage latency (FCT arm)

Per wave, from the wave-counter increment to the first `P-OUT` sample. FCT lifetime means the sample
is an **upper bound** (the hit may have landed up to L = 1.35 s earlier); both bounds are printed.

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|
| upper (s) | 3.00 | 0.40 | 1.60 | 0.20 | 0.00 | 0.30 | 2.10 | 1.80 | 0.30 | 0.00 |
| lower (s) | 1.65 | 0.00 | 0.25 | 0.00 | 0.00 | 0.00 | 0.75 | 0.45 | 0.00 | 0.00 |

Median upper bound **0.35 s**. Wave 151's 3.00 s is the run start (the fight begins there).
**Every latency carries the ±0.25 s wave-boundary uncertainty on top.**

---

## 3. THE CONTACT-OCCUPANCY DECODE — the measurement that matches the sim's own definition

The FCT stream measures *damage landing*. The simulation's `dry_fraction` is defined as *no body in
the player's kill disc*. The Lap H-2 nameplate census lets me ask the referent's pixels **the sim's
own question**: at each 60 fps instant, is there a **living body** inside the player's contact ring?

**Bound direction, declared and one-directional:** a nameplate **proves** a living body; its absence
does **not** prove absence (occlusion, VFX saturation, plate-suppressed bodies). Every count is a
**LOWER BOUND** on bodies ⇒ **every dry fraction here is an UPPER BOUND on the referent's true dry
fraction.** Coverage: **10,216 instants** in 683–864 s carrying a detected player plate (Lap H-2
player-plate coverage 94.6 %); instants without one are **excluded, not imputed**.

### 3.1 The full radius curve — published instead of one rung

`R_CONTACT` is the single most sensitive choice in this measurement, so the whole curve is published
and **no rung is preferred**.

| R (ground px) | dry fraction | mean occupancy | median occ | dry runs | **longest dry run (s)** |
|---|---|---|---|---|---|
| 60 | 0.7524 | 0.34 | 0 | — | **4.40** |
| 80 | 0.6705 | 0.51 | 0 | — | **3.60** |
| 100 | 0.5813 | 0.72 | 0 | — | **3.52** |
| 120 | 0.5001 | 0.95 | 0 | — | **3.10** |
| **150** *(pre-registered primary — Lap H-2's visually-calibrated value, imported unchanged)* | **0.4121** | 1.28 | 1 | 670 | **3.10** |
| 180 | 0.3526 | 1.65 | 1 | — | **3.10** |
| 220 | 0.2830 | 2.18 | 2 | — | **3.10** |
| 260 | 0.2261 | 2.83 | 2 | — | **3.10** |
| 300 | 0.1989 | 3.43 | 3 | 347 | **2.75** |
| 350 | 0.1718 | 3.99 | 3 | — | **2.75** |
| 400 | 0.1545 | 4.45 | 4 | — | **2.65** |
| 450 | 0.1397 | 4.94 | 4 | — | **2.30** |
| 500 | 0.1312 | 5.36 | 4 | — | **2.30** |
| 600 | 0.1088 | 6.43 | 6 | — | **2.30** |
| 800 | 0.0788 | 7.41 | 7 | — | **1.18** |

**⚑ Read the last column, not the second.** The dry *fraction* is a free parameter of the radius —
it sweeps 0.75 → 0.08 across the band. The **longest dry run is radius-invariant to within a factor
of 3.7 across a 13-fold radius sweep, and never exceeds 4.40 s.**

**⚠ A coincidence I must name so it is never mistaken for a result.** At the pre-registered radius of
150 ground px the referent's dry fraction is **0.4121** and the sim's `dry_fraction_whole_run` is
**0.4118** — agreement to three decimals. **This is not evidence that the two fights carry the same
dryness.** The radius was genuinely pre-registered (it is Lap H-2's visually-calibrated `R_CONTACT`,
adopted before this lap knew what dry fraction it would produce), but a ±20 % change in that radius
moves the number by ±0.06–0.09. The agreement is a **radius coincidence on a steep curve.** The
decidable comparison is § 3.3, and the durable finding is the shape.

### 3.2 Per wave, at the pre-registered R = 150 ground px

| wave | span s | instants | dry frac | mean occ | median occ | max occ | longest dry run s |
|---|---|---|---|---|---|---|---|
| 151 | 15.6 | 870 | 0.5356 | 0.87 | 0 | 8 | 2.90 |
| 152 | 16.3 | 955 | 0.5372 | 0.77 | 0 | 7 | 1.02 |
| 153 | 14.9 | 836 | 0.6196 | 0.60 | 0 | 4 | 1.53 |
| **154** | **14.2** | **795** | **0.2654** | **2.04** | **2** | **8** | **1.18** |
| 155 | 16.2 | 932 | 0.5322 | 1.01 | 0 | 8 | **3.10** |
| 156 | 20.2 | 1149 | 0.3821 | 1.33 | 1 | 9 | 0.88 |
| 157 | 19.3 | 1068 | 0.3558 | 1.42 | 1 | 10 | 1.38 |
| 158 | 13.0 | 759 | 0.5086 | 0.96 | 0 | 8 | 1.28 |
| 159 | 26.3 | 1503 | 0.2808 | 1.73 | 1 | 9 | 0.70 |
| 160 | 25.0 | 1349 | 0.2809 | 1.62 | 1 | 8 | 0.87 |

Final 20 s (t ≥ 844.0): dry **0.2632**, mean occupancy 1.70. Final 10 % of the fight (t ≥ 845.9):
dry **0.2488**, mean occupancy 1.78. *(The sim's "final-200" is a tick window; the referent's tick
length is not a referent quantity and was not imported. These are the referent's own final-window
reads and are labelled as such, not as the sim's window.)*

**The referent gets MORE contact as it approaches death, not less** — dry falls from a 0.4121
whole-run figure to 0.2488 in the closing window, and mean occupancy rises from 1.28 to 1.78.

### 3.3 ⚑ Ground pixels → metres: Lap H-2's declared gap `OBS-H2-9`, re-opened with two NEW anchors

Lap H-2 declined the metre conversion because its two candidate anchors **disagreed**. This lap
found two different anchors, geometrically unrelated to each other and to Lap H-2's pair, and they
**agree to 4.9 %**. *(Declared: this analysis was NOT in the pre-registration. It is reported as a
CANDIDATE resolution offered to the conductor, graded INDICATIVE, and it is **not ruled** here.)*

| anchor | construction | assumption (named) | gpx/m |
|---|---|---|---|
| **(a) player ground decal** — LO | Lap H-2 `OBS-H2-8`: decal 80 × 43 px at t = 683.500 ⇒ half-major **40 gpx**. Lap F Q4: `records/creatures/pc/{male,female}pc01.dbr :: actorRadius = 0.32`. | the drawn ground decal's radius equals the collision `actorRadius` | **125.0** |
| **(a) player ground decal** — HI | same, with Lap F's HI reading `radius = actorRadius × scale`, `scale = 1.05` | as above, HI limb of Lap F's own undecided LO/HI | **119.0** |
| **(c) FCT × plate cross-calibration** | the radius **R\*** at which the *plate* dry fraction equals the *FCT* dry fraction (0.165289) is **R\* = 368.8 gpx**; set R\* = `eyeofreckoning1 :: skillTargetRadius = 3.0 m` | "no player-side damage landed" ≈ "no body inside 3.0 m" | **122.9** |
| | | **BRACKET** | **119.0 – 125.0** |

**Anchor (c) carries a TWO-SIDED bias and is therefore graded INDICATIVE, not MEASURED.** FCT-lifetime
dilation masks short dry stretches and pushes R\* **down**; pet / devotion-proc / DoT damage landing
from outside the player's own ring pushes R\* **up**. The two biases oppose and **I cannot sign the
net**. Anchor (c)'s value is not its own precision — it is that a *text-presence* instrument and a
*decal-geometry* instrument, sharing no assumption, land 1.7 % apart.

**Consequence — the decidable comparison.** Converting the simulation's own pre-existing constant
`D_ENGAGE_M = 2.400` through the bracket, and measuring the referent **directly at that radius**
(not interpolating the curve):

| gpx/m | R (gpx) | **referent dry fraction** | mean occupancy | dry runs | longest dry run |
|---|---|---|---|---|---|
| 119.0 | 285.7 | **0.2063** | 3.24 | 368 | **2.75 s** |
| 122.3 (bracket mean) | 293.6 | **0.2019** | 3.35 | 352 | **2.75 s** |
| 125.0 | 300.0 | **0.1989** | 3.43 | 347 | **2.75 s** |

> **At the simulation's own kill-ring radius, the referent's dry fraction is 0.199 – 0.206 against
> the sim's 0.4118 — a factor of 2.0 — and the referent's longest dry stretch there is 2.75 s,
> dispersed across ~350 separate runs.**

Neither number was adjusted toward the other. The radius came from the sim's own constant; the
conversion came from two independent referent measurements; the whole curve is published in
`pm4r_contact_occupancy.csv` so any consumer can recompute at any radius they prefer.

---

## 4. LIMB B — video locomotion

### 4.1 The instrument, and why it is a re-use rather than a new build

Lap H-2's enabling find carries this whole limb: **the camera is measured rigidly player-locked**
(`OBS-H2-7` — the player's nameplate-bar left edge held x = 921–924 px across 10,443/11,040 detections
at 60 fps), therefore **camera translation IS the player's world displacement, exactly, in screen
pixels.** The trace is 60 fps phase correlation on the *gradient magnitude* of the terrain band.
Ground-pixel convention (`OBS-H2-8`): `hypot(dx, dy / K)` with **K = 0.537**.

### 4.2 Detector validation — **PASS**, against an independent second instrument

Protocol exactly as pre-registered: 20 instants (10 classified MOVING, 10 STATIONARY) drawn with a
**fixed seed = 154**; at each, normalised cross-correlation template matching of raw-luminance terrain
patches (a **different registration principle** from the trace's FFT phase correlation on gradient
magnitude) over a 0.25 s frame pair, 4 patches, best-confidence patch taken.

| criterion | required | measured | verdict |
|---|---|---|---|
| class agreement | ≥ 16 / 20 | **18 / 20** | PASS |
| median relative magnitude error on MOVING instants | ≤ 0.25 | **0.1427** | PASS |

**Both disagreements are boundary cases inside the Schmitt hysteresis band, and the magnitudes
agree even there** — t = 785.617 (trace 15.4 gpx vs NCC 13.0) and t = 846.533 (57.7 vs 43.2). Both
sit below the 50 gpx/0.25 s class cut while the trigger was still latched ON from a preceding
faster interval. That is the hysteresis behaving as designed, not the trace mis-measuring: on the
class-independent quantity (displacement magnitude) the two instruments agree at both points.
**No threshold was re-tuned after this result.**

### 4.3 Movement episodes

Schmitt trigger `V_ON` / `V_OFF = V_ON / 2`, 0.15 s rolling-median smoothing, 0.25 s minimum
episode, 0.15 s gap merge — all pre-registered.

| `V_ON` (gpx/s) | episodes | total moving s | **moving fraction** | median episode | longest |
|---|---|---|---|---|---|
| 100 | 80 | 150.98 | 0.8342 | 1.29 s | 11.12 s |
| **200 (pre-registered primary)** | **86** | **143.87** | **0.7948** | **1.26 s** | **8.68 s** |
| 400 | 83 | 112.82 | 0.6233 | 1.10 s | 4.25 s |

Smoothed ground-speed percentiles: p10 = 2 · p25 = 180 · **p50 = 418** · p75 = 544 · p90 = 673 ·
p99 = 1798 gpx/s.

**Corroboration against Lap H-2's independently-computed cadence table:** that lap reported
`moving_frac_th200 = 0.757` whole-fight; this lap's segmentation returns **0.7948**. Different
smoothing and a different segmentation rule; the same picture.

**⚑ The longest stationary span in the entire 181 s fight is 1.73 s** (t = 841.62 → 843.35, wave 160).
The ten longest are all ≤ 1.73 s; the top six are 1.73 / 1.65 / 1.47 / 1.28 / 1.23 / 1.15 s.
**Matt is in motion 79.5 % of the fight and never holds still for two seconds.**

Per wave (episodes / moving-frame fraction at `V_ON` = 200):
w151 5/0.76 · w152 8/0.82 · w153 8/0.70 · **w154 8/0.64** · w155 6/0.80 · w156 9/0.76 ·
w157 14/0.71 · w158 3/0.79 · w159 11/0.68 · w160 14/0.70.

Full per-episode rows — start, end, duration, wave, mean/peak speed, path length, net displacement,
straightness, and the channel-probe columns — are in `pm4r_movement_episodes.csv` (86 rows).

### 4.4 ⚑ Movement-while-channeling — **CONTINUES**, decoded from the referent's own frames

**The pre-registered test.** 12 fastest episodes, sampled at 10 fps (148 moving frames), against a
stationary control drawn from the longest stationary spans (120 frames):

| observable | MOVING | STATIONARY | ratio |
|---|---|---|---|
| player-outgoing FCT present | 78/148 = **0.5270** | 91/120 = **0.7583** | 0.6950 |
| player-centred channel-VFX ring ratio (median) | **1.6995** (p25–p75 1.45–2.07) | **1.7456** (p25–p75 1.39–2.20) | 0.974 |

Pre-registered rule ⇒ **CONTINUES** (FCT presence 0.527 ≥ the 0.50 gate **and** ring ratio ≥ 0.9× the
stationary median). **The FCT limb passes by 0.027 — a thin margin, and I report it as thin.**

**⚑ DECLARED POST-HOC — the confound the pre-registration did not anticipate, and its fix.** A drop
in FCT presence during fast relocation has two possible causes and the pre-registered test cannot
separate them: (i) the channel stops, or (ii) **there is simply nothing in reach while relocating**.
The nameplate census removes (ii) by conditioning on occupancy. Run over the **full** dense 0.5 s
pass (355 joined samples, not the 12-episode subset):

| cell | n | FCT present | rate |
|---|---|---|---|
| ALL moving | 255 | 207 | 0.8118 |
| ALL stationary | 100 | 89 | 0.8900 |
| **≥ 1 body in reach & moving** | 141 | 131 | **0.9291** |
| **≥ 1 body in reach & stationary** | 70 | 67 | **0.9571** |
| ≥ 2 bodies in reach & moving | 82 | 76 | 0.9268 |
| ≥ 2 bodies in reach & stationary | 46 | 45 | 0.9783 |
| 0 bodies in reach & moving | 114 | 76 | 0.6667 |
| 0 bodies in reach & stationary | 30 | 22 | 0.7333 |

**Conditioned ratio moving/stationary = 0.9707. Wilson 95 % CIs: moving (0.8744, 0.9610),
stationary (0.8814, 0.9853) — OVERLAP.** At R = 300 gpx the same picture: 0.9184 vs 0.9333,
ratio 0.9840, CIs overlap.

**The entire apparent drop was the confound.** Once you ask only about instants when there was
something to hit, moving and standing still are indistinguishable. **Movement does not interrupt the
player's damage output.**

**Frame evidence — 78 witnessed instants** (60 fps frame numbers in `pm4r_digests.json`), spanning
t = 701.68 → 848.28 s. Saved frames from episode 5 (t = 701.383 → 702.433, mean speed **908 gpx/s** —
the fastest episode in the fight, wave 152) are in `evidence/`:
`ep05-movwhilechan-{701.3833,701.6833,701.9833,702.2833,702.4333}.jpg`. The t = 701.9833 frame
carries four simultaneous cream player-damage numbers — **136114 (x1.67)**, **71052 (x1.67)**,
**25353 (x1.67)**, **18252** — while the terrain is visibly translating; the on-screen wave counter
reads **152**. This **extends** Lap H-2's `OBS-H2-4` (which witnessed one traversal at 805.45–806.05)
to a second, faster, independently-selected episode.

**NOTE-9, declared in advance and honoured:** pixels cannot name **which** skill draws a ring. The
claim ceiling is *"a player-centred channel VFX and player damage output both persist through
movement"* — never *"`eyeofreckoning1` specifically persists"*. The ring detector is additionally
**weak evidence in its own right**: the 60–110 gpx annulus is saturated by VFX from many sources and
cannot isolate one skill's ring. The load-bearing evidence is the occupancy-conditioned FCT test
plus the record (§ 6.3), with the ring as corroboration only.

### 4.5 Spawn-to-first-CONTACT latency (nameplate arm)

Time from the wave-counter increment until the first living monster nameplate falls inside the ring.
**Every count is a LOWER BOUND on bodies, so every latency is an UPPER BOUND.**

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|
| R = 120 | 2.917 | 0.183 | 0.050 | 0.017 | 0.050 | 2.300 | 0.100 | 0.400 | 0.033 | 0.017 |
| **R = 150** | **2.917** | **0.183** | **0.050** | **0.017** | **0.050** | **1.383** | **0.100** | **0.400** | **0.033** | **0.000** |
| R = 180 | 2.850 | 0.183 | 0.050 | 0.017 | 0.050 | 1.383 | 0.100 | 0.400 | 0.033 | 0.000 |

**Median latency 0.117 s at R = 150.** Eight of ten waves have a living body inside the contact ring
within **0.4 s** of the counter incrementing. Wave 151's 2.917 s is the run start; wave 156's 1.383 s
is the only genuine spawn-in delay in the fight.

**⚑ Interpretation, and its limit, stated together.** The Crucible wave counter increments while the
previous wave's survivors are still alive, so a body inside the ring at the increment instant may be
a straggler rather than a fresh spawn — **this instrument cannot distinguish them**, and the latency
is therefore a bound on *"time until the player is in contact with something"*, not on *"time until
the new wave arrives"*. Read that way it is still the load-bearing number: **the referent's board is
essentially never empty at a wave transition.** Both limbs (FCT § 2.6, plates here) agree.

---

## 5. LIMB C — game-side movement-speed terms

Full per-term rows with record path, archive, field name, value, wave, level and basis:
**`pm4r_speed_terms.csv`, 2,073 rows.**

### 5.1 Player movement speed — **AT THE ENGINE'S HARD CAP**

| term | value | source |
|---|---|---|
| player base `characterRunSpeed` | **0.93** | `records/creatures/pc/malepc01.dbr` **and** `femalepc01.dbr` [gdx3] — identical on both, so the record choice is immaterial and is recorded rather than hidden |
| `characterRunSpeedModifier` (base) | 0.0 | same records |
| `characterRunSpeedJitter` (player) | **0.0** | same records — the player has no speed jitter; monsters do (§ 5.2) |
| `maxRotationSpeed` / `minRotationSpeed` (player record) | 40.0 / 10.0 | same records |
| `maxPlayerRotationSpeed` / `minPlayerRotationSpeed` (engine) | 30.0 / 19.0 | `records/game/gameengine.dbr` [base] |
| **`playerRunSpeedCapMax`** | **135.0** | `records/game/gameengine.dbr` |
| `playerRunSpeedCapMin` | 20.0 | same |
| `absoluteRunSpeedCapMax` | 350.0 | same |
| `absoluteRunSpeedCapMin` | [40.0, 30.0, 20.0] | same (per-difficulty array) |
| **the referent's SHEET value** | **135 %** | Lap A `measured-player-sheet.csv` row 35, `run_speed`, screenshot 511 |

> **⚑ The referent player's movement speed is pinned to the engine's player run-speed cap. The
> sheet reads 135 % and `playerRunSpeedCapMax` is 135.0. There is no headroom.**

**The composition, from the played character's own records** (exhaustive walk of every equipped item
base + affix + component + augment, the Warborn set record, both item-granted passives, every
allocated skill at rank > 0, and every one-hop `buffSkillName` / `petSkillName` / `itemSkillName` /
`skillName` / `petBonusName` payload):

| source | record | value |
|---|---|---|
| gear:component (chest) | `records/items/materia/compb_chainsofoleron.dbr` [base] | +6.0 |
| gear:base (feet) | `records/items/upgraded/gearfeet/d007_feet.dbr` [gdx3] | +10.0 |
| devotion | `records/skills/devotion/tier2_02b.dbr` [base] | +6.0 |
| devotion | `records/skills/devotion/tier2_21d.dbr` [base] | +5.0 |
| devotion | `records/skills/devotion/tier1_39b.dbr` [gdx1] | +5.0 |
| devotion | `records/skills/devotion/tier3_20c.dbr` [gdx2] | +6.0 |
| | **permanent-source sum** | **+38.0** |

100 + 38 = **138 %**, against `playerRunSpeedCapMax = 135.0` ⇒ **clipped by 3 points**, and the sheet
prints exactly the cap. *(Lap L's standing ruling holds: where the sheet prints a composed stat, the
**sheet governs**; the table walk is published beside it so every term is visible.)*

**MEASURED-INACTIVE — the error a sum-everything pass would make.** Three further records on this
character carry very large `characterRunSpeedModifier` values and **must not join the permanent
total**, because they are transient movement skills, not passives:

| record | value | why it does not join |
|---|---|---|
| `records/skills/default/defaultevade.dbr` | **+250.0** | the default Evade / dodge-roll — active only for the roll |
| `records/skills/playerclass01/blitz1.dbr` | **+300.0** | Blitz, a charge attack — active only for the charge |
| `records/skills/playerclass09/viremight1.dbr` | **+250.0** | Vire's Might, a charge — active only for the charge |

A naive sum would report 838 % movement speed. This is the same class of error Lap P named on the
ADCTH walk, and it is caught the same way: **emitted MEASURED-INACTIVE rather than dropped**, so the
gap is legible.

**These three are also the measured explanation of the video's speed tail.** The smoothed ground-speed
distribution has p50 = 418 and **p99 = 1798 gpx/s**, a 4.3× tail. Three transient +250 / +300 %
movement layers are exactly the kind of term that produces it. *(I stop at "consistent with". Turning
the ratio into a match would require the ground-px → metre conversion of § 3.3, which is INDICATIVE
and not ruled, and would require knowing whether charge skills are governed by run speed at all —
**U-R-3**, § 8.)*

### 5.2 Monster movement speed — the 151–160 roster

**344 rostered actors over 169 distinct records; `characterRunSpeed` present on 169/169 — ZERO
UNREACHED.** (The frozen roster roll is the run's own `BATON_20W`; the field is a level-independent
scalar, so no equation evaluation enters.)

| statistic | value |
|---|---|
| min / p25 / median / p75 / max | **0.600 / 0.900 / 1.000 / 1.100 / 1.550** |
| mean (per record) | 0.9880 |
| **actor-weighted median / mean** (n = 344 rostered bodies — how the board actually moves) | **1.000 / 0.9874** |
| `characterRunSpeedJitter` | present on 137 records; distinct values **{0, 10, 15, 20, 25, 30}** |

Value histogram (record count): 0.60 ×8 · 0.66 ×8 · 0.70 ×6 · 0.75 ×4 · 0.80 ×12 · 0.85 ×3 ·
0.90 ×15 · **1.00 ×48** · 1.05 ×3 · 1.10 ×25 · 1.12 ×2 · 1.15 ×12 · 1.16 ×1 · 1.20 ×11 · 1.25 ×2 ·
1.30 ×1 · 1.35 ×4 · 1.40 ×2 · 1.45 ×1 · 1.55 ×1.

Slowest: `ghost_{a01,a02,b01,b02,h01,h02}` = **0.60**.
Fastest: `swampgolem_a01` **1.55** · `skeletalgolem_stepsoftorment_01` 1.45 ·
`dermapteran_madqueen` 1.40 · `swampgolem_bargoll` 1.40 · `ro_bounty19` 1.35 · `swampgolem_h01` 1.35.

Per-wave actor-weighted mean `characterRunSpeed`:
w151 **0.820** · w152 1.057 · w153 1.038 · **w154 0.815** · w155 **1.144** · w156 0.997 ·
w157 0.921 · w158 1.054 · w159 1.091 · w160 1.100.

**⚑ Note w154 carries the roster's *slowest* board (0.815, tied-lowest with w151) — and it is
nonetheless the referent's *most-occupied* wave** (mean 2.04 bodies in ring, § 3.2). Slow monsters did
not produce a wait in the referent. Whatever produces the sim's w154 wait, it is not monster speed.

Engine caps for the monster side, also read: `monsterRunSpeedCapMax = 500.0`,
`monsterRunSpeedCapMin = [20.0, 25.0, 30.0]`, `bossRunSpeedCapMax = 500.0`,
`bossRunSpeedCapMin = 40.0`, `maxRotationSpeed = 16.0`, `minRotationSpeed = 8.0`
(all `records/game/gameengine.dbr`).

### 5.3 EoR's movement-while-channeling rule — **independently reproduced from my own seat**

`records/skills/playerclass09/eyeofreckoning1.dbr` [gdx2]:

| field | value | note |
|---|---|---|
| `Class` | `Skill_AttackRadiusSpin` | → `skill_attackradiusspin.tpl` → includes `skillchanneled.tpl` |
| **`canUseWhileMoving`** | **`True`** | `skillchanneled.tpl` **bool, default `0`** — a deliberate, rare authoring decision |
| `delayMovement` | `True` | template description **EMPTY** |
| **`rotationSpeedMultiplier`** | **0.3499999940395355** | *"Multiplier applied to player rotation speed while skill is active"* |
| `skillTargetRadius` | **3.0** (m) | the sim's `EOR_RADIUS_M`, unconverted |
| `timeBetweenAttacks` | 200 (ms) | *"Time between hits to enemies along the path"* |
| `duration` / `useResetsDuration` | 0.25 s / `True` | |
| `characterRunSpeed` · `characterRunSpeedModifier` | **MEASURED-ABSENT** | **there is no movement-speed penalty on the skill; the sim must not invent one** |
| `forceMovement` · `instantCast` · `skillCooldownTime` | **MEASURED-ABSENT** | |

**This reproduces Lap G § 7 exactly, from an independent walk.** The measured law: *you may move at
undiminished speed while channelling, but you re-aim at 35 % rotation speed.* **Turning is the
measured cost of channelling — not translation.**

`D-P-G3` carried unchanged from Lap G: `delayMovement`'s template description is **empty**, and
whether casting another skill (a dash, a potion) **breaks** the channel is engine-internal — no
field in the corpus expresses it. Absence of a field is not evidence of independence.

### 5.4 Crucible spawn geometry — **UNREACHED**

Five candidate record paths probed (`records/game/crucible.dbr`, `records/ui/crucible.dbr`,
`records/creatures/spawnpoints/spawnpoint01.dbr`, `records/game/survivalmode.dbr`,
`records/game/levels/crucible.dbr`); **none resolves.** Arena dimensions and spawn-point placement
are `.map` / `.lvl` **world-asset** content, not `.arz` record-DB content, and world assets were not
opened. **Recorded UNREACHED, as the commission required — not estimated.**

---

## 6. Departures from the pre-registration — both self-caught, both reported

**⚑ D-R-1 — my § A.0 bound-direction claim was WRONG, and I am retracting it.** The pre-registration
asserted that "the FCT dry fraction is an **UPPER BOUND** on the referent's true dry fraction",
reasoning only from the superset condition (truly-dry ⇒ no damage landed). **That reasoning ignores
the § A.3 lifetime dilation, which acts in the opposite direction.** Correctly: a truly-dry instant
*t* need not be FCT-dry (damage may have landed 0.5 s earlier when a body was still in reach), so the
containment fails in both directions and **the FCT dry fraction is not a bound of either sign.** The
two errors — dilation (understates) and superset (overstates) — oppose, and I cannot sign the net.
The FCT numbers in § 2 are therefore reported as a measurement of a **related but different
quantity**, and the quantity that *does* carry a signed bound is the plate census of § 3
(counts are lower bounds ⇒ dry fractions are upper bounds, one-directional).
**No number changed; the claim about the numbers did.**

**⚑ D-R-2 — the § 4.4 occupancy-conditioned test is POST-HOC and is labelled so wherever it
appears.** It does not replace the pre-registered B.3 verdict (which stands, at CONTINUES, with its
thin 0.027 margin reported). It is published beside it because the pre-registered rule carried a
confound the pre-registration did not anticipate, and naming the confound is worth more than
defending the rule. **No pre-registered threshold was altered after seeing a result.**

**Arithmetic convention corrected mid-lap, before any finding was drawn:** the first run of the limb-A
instrument added the FCT lifetime L to a sample-coverage duration, double-counting the half-cadence
margins and summing overlapping proven windows. The emitted table now carries two clean, separately
defined columns — `gap_raw_s` (= n × cadence, sample coverage) and `gap_lifetime_corrected_s`
(= (t_last − t_first) + L, the interval the lifetime **guarantees** carried no landed damage) —
plus a merged **union** total so overlapping proven windows are never double-counted. Both are
published; neither is preferred.

---

## 7. UNREACHED census

| # | term | status |
|---|---|---|
| **UNREACHED-1** | **Crucible spawn geometry** — spawn-point coordinates, arena dimensions, spawn-to-player distance | **UNREACHED.** 5 candidate record paths probed, none resolves. Lives in `.map`/`.lvl` world assets, outside the `.arz` record DB. Not estimated. |
| **UNREACHED-2** | **FCT gap structure below 2.0 s in PASS 1** | **UNREACHED at 2 s cadence** by construction. Resolved by PASS 2 at 0.5 s; the PASS-1 rungs below its cadence are marked and not interpolated. |
| **UNREACHED-3** | **FCT gap structure below 0.5 s** | **UNREACHED** even at the dense cadence. A 0.5 s cadence cannot resolve sub-0.5 s gaps, and the 1.2–1.5 s FCT lifetime masks them regardless of cadence. |
| **UNREACHED-4** | **FCT source attribution** | **UNREACHED and structural** (Lap N § A.6, carried). Player weapon, pet, devotion proc, retaliation and DoT all print cream and cannot be separated from pixels. `P-OUT` = "the player's side landed damage". |
| **UNREACHED-5** | **whether a body inside the ring at a wave increment is a fresh spawn or a straggler** | **UNREACHED.** The nameplate census carries no wave identity per body. The § 4.5 latencies are bounds on *time-to-contact*, not *time-to-new-wave*. |
| **UNREACHED-6** | **which skill draws the player-centred ring** | **UNREACHED and structural** (NOTE-9, pre-declared). The annulus is VFX-saturated; no pixel measurement can attribute a ring to `eyeofreckoning1`. |
| **UNREACHED-7** | **whether casting another skill breaks the EoR channel** | **UNREACHED** — `D-P-G3` from Lap G, carried unchanged. `delayMovement`'s template description is empty; no corpus field expresses channel interruption. |
| **UNREACHED-8** | **monster *effective* in-fight speed** | **UNREACHED.** `characterRunSpeed` is a record scalar; the board's realised speed also carries `characterRunSpeedJitter` (per-body randomisation, values {0,10,15,20,25,30}), any wave-scaling modifier, and the player's own slow/CC application. Only the record scalar is measured here. |

---

## 8. UNDECIDED / uncertain terms — for the conductor's bracket accounting

| # | term | why undecided | what would decide it |
|---|---|---|---|
| **U-R-1** | **ground pixels → metres.** Bracket **119.0 – 125.0 gpx/m**, three anchors, spread 4.9 %. | Anchor (a) assumes the drawn ground decal's radius equals the collision `actorRadius` — and inherits Lap F's own undecided LO/HI on `scale`. Anchor (c) assumes "no player-side damage landed" ≈ "no body inside 3.0 m", with a **two-sided, unsigned** bias. **Graded INDICATIVE. NOT RULED here** — this is a conductor call, and it re-opens Lap H-2's `OBS-H2-9`, which that lap deliberately left open. | one in-frame object of known DB length, or a measured EoR damage-ring outer radius attributable to `skillTargetRadius` |
| **U-R-2** | **which contact radius is the like-for-like comparator to the sim's kill disc.** Dry fraction sweeps 0.75 → 0.08 over the radius band; the whole curve is published so no rung is imposed. | Resolving U-R-1 fixes it. **Every headline in § 0 that depends on it is stated with its radius attached.** | U-R-1 |
| **U-R-3** | **whether GD charge skills (Blitz, Vire's Might, Evade) are governed by `characterRunSpeed` at all**, or translate the actor over a fixed distance independent of it. | Bears on whether the video's p99/p50 = 4.3 speed tail is the measured +250/+300 % layers. I report "consistent with" and stop. | a movement-mechanics field or an in-game controlled measurement; neither available from this seat |
| **U-R-4** | **whether the referent's dry stretches are "no body in reach" or "body in reach but not attacking".** | The FCT and plate instruments bracket it but do not separate it: at 0 bodies in ring & moving, FCT is still present 66.7 % of the time (R = 150) — proof that the player's damage reach materially exceeds the plate ring, but not a decomposition. | a per-body attributable damage stream, which pixels cannot provide (UNREACHED-4) |
| **U-R-5** | **the § 3.1 radius coincidence** — referent 0.4121 @ 150 gpx vs sim 0.4118. | Pre-registered radius, steep curve. **I name it as a coincidence and decline to use it.** Flagged here so it can never be quoted as agreement without its curve. | U-R-1 |
| **U-R-6** | **movement-while-channeling verdict strength.** Pre-registered rule passes by **0.027**; the post-hoc conditioned test is decisive (ratio 0.971, CIs overlap) but is **post-hoc**. | The record's `canUseWhileMoving = 1` (template default 0) is an independent third leg and agrees. I grade the composite verdict **MEASURED-STRONG**, and record that it rests on a thin pre-registered margin plus a declared post-hoc test plus a record field. | a pre-registered replication of the conditioned test on an independent referent capture |

**Carried unchanged from prior laps:** `D-P-G3` (channel-interruption, Lap G) · `OBS-H2-3`
(interpenetration NOT ASSERTABLE) · `OBS-H2-9` (px→m, re-opened here as U-R-1 but **not closed**) ·
Lap N § A.6 (FCT source attribution) · Lap F's `actorRadius` LO/HI on `scale`.

---

## 9. What this lap did NOT do — the firewall, stated

* No simulation output file, baton, findings JSON, landing note or scorecard was opened by any
  instrument in this lap. The commission's quoted sim numbers (`0.4118`, `0.33`, `38.12 s`, `51.2 %`,
  `19.5 s`, `D_ENGAGE_M = 2.400`) are reproduced **verbatim from the commission text** for
  side-by-side reporting and **entered no threshold, no radius, no detector and no verdict rule** —
  except `D_ENGAGE_M = 2.400`, which is used in § 3.3 **as an input radius to measure the referent
  at**, openly and by name, because measuring the referent at the sim's own stated radius is the only
  way to make the comparison decidable. The radius was not chosen to produce a number; the number is
  reported at three radii spanning the anchor bracket.
* **No term was estimated.** Eight UNREACHED entries are recorded as UNREACHED.
* **No threshold was re-tuned after seeing a result.** Two departures from the pre-registration are
  declared in § 6; both are corrections to *claims*, not to *thresholds*.
* **No fitting.** The referent numbers are what the referent's pixels and the game's own records say.

---

## 10. Emitted artifacts

| file | rows | contents |
|---|---|---|
| `pm4r_fct_gaps.csv` | **44** | per-gap rows, both passes: pass tag, cadence, first/last dry sample, n dry samples, raw duration, lifetime-proven duration + its L = 1.2/1.5 band, proven-interval bounds, wave at start/end, boundary-straddle flag |
| `pm4r_movement_episodes.csv` | **86** | per-episode rows at the pre-registered `V_ON` = 200: id, start, end, duration, wave, mean/peak speed, path length, net displacement, straightness, channel-probe columns (probed / frames sampled / frames with player damage / channeling-visible flag) |
| `pm4r_speed_terms.csv` | **2,073** | every player-side and monster-side speed term with side, subject, record path, archive, field name, value, wave, level, **`active_status`** (ACTIVE vs MEASURED-INACTIVE — the three transient movement skills are emitted, not dropped) and basis string |
| `pm4r_contact_occupancy.csv` | **28** | the full dry-fraction-vs-radius curve, the per-wave occupancy table, and the three measured reads at the sim's `D_ENGAGE_M` converted through the anchor bracket |
| `pm4r_findings.md` | — | this document |
| `PREREGISTRATION.md` | — | thresholds, hashed before the instruments ran |
| `pm4r_digests.json` | — | FULL 64-hex sha256 on every input and every output, row counts, and the machine-readable result summary |
| `method/plates60_lapH2.npy` | 109,110 | the Lap H-2 nameplate census, copied out of `/tmp` into this lap so the measurement stays reproducible |
| `evidence/ep05-movwhilechan-*.jpg` | 5 | movement-while-channeling witness frames, episode 5 (fastest in the fight, 908 gpx/s, wave 152) |

**Instruments** (`agentic_orchestration/research/scripts/`):
`pm4r_lib_2026_08_14.py` (shared constants + machinery; every pre-registered threshold is a named
constant) · `pm4r_fct_2026_08_14.py` (limb A) · `pm4r_locomotion_2026_08_14.py` (limb B) ·
`pm4r_contact_2026_08_14.py` (contact occupancy + radius curve + metre anchors) ·
`pm4r_channel_control_2026_08_14.py` (the declared post-hoc conditioned channel test) ·
`pm4r_speed_2026_08_14.py` (limb C).
