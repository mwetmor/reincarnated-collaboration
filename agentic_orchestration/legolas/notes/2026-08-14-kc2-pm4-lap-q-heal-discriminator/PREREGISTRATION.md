# RUN KC2-PM4 · LAP Q · PRE-REGISTRATION — THE HEAL DISCRIMINATOR (`U-P-N-1`)

> **Seat:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Date:** 2026-08-14
> **Commission:** charter row `R-PM4-44` part 2; pre-named at `L-32`; trigger met at `L-35`
> (`U_P_N_1.verdict_divergent = True`).
> **Laws in force:** GL-12 ENTIRE — DECODE-NEVER-ESTIMATE (unmeasured = UNREACHED, never estimated) ·
> OUTCOME-FIREWALLED (this lap reports measurements; it does not shape them toward any predicted
> outcome, and has read no I-18 sim output beyond the single boolean that fired its trigger) ·
> GL-6 FULL 64-hex digests on all inputs and outputs · READ-ONLY on every source.
>
> **THIS FILE IS WRITTEN AND HASHED BEFORE ANY INSTRUMENT IS RUN OVER THE FULL VIDEO.**
> Everything below the line "PRE-REGISTRATION ENDS" was fixed before extraction. Departures are
> reported in the findings under a DECLARED DEPARTURES heading, never silently.

---

## 0 — The question

`U-P-N-1` (Lap P § 4.3): does the monster stat `defensiveSlowLifeLeach` ("Life Leech Resist", printed
on the character sheet, confirmed by the `players01[8] = −25.0` positive control) **gate the player's
Attack-Damage-Converted-to-Health heal** —

* **COUPLED** — `adcth_mult = max(0, 1 − res/100)`; or
* **DECOUPLED** — the field gates only the `offensiveSlowLifeLeach` DoT damage type, and ADCTH is
  untouched.

The corpus declares **no equation** joining them (Lap P `ABSENT-1`). The gap is a factor ≈ 4 at the
median body and infinite at 48 of 790 bodies.

---

## 1 — Inputs, pinned by digest BEFORE use

| input | identity |
|---|---|
| **referent video** | `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` · 479,438,089 B · 1920×1080 · 60/1 fps · 1034.10 s · 62,046 frames · **sha256 `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8`** — computed by this lap; Laps H-2 / M / N / R declared it NOT COMPUTED and pinned identity by path + byte size only. |
| **leech board** | `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-p-sustain-engine/pm4p_leech_resistance.csv` · sha256 `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` — **VERIFIED EXACT against the commission before use** · 7,900 rows |
| **Lap N FCT stream** | `…/2026-08-14-kc2-pm4-lap-n-crit-and-collision/pm4n_fct_events.csv` · sha256 `cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2` · 2,328 rows |
| **wave timeline** | Lap H-2 `OBS-H2-6` boundaries as carried in Lap R `pm4r_contact_occupancy.csv` (±0.25 s): 151 [683.0, 698.6] · 152 [698.6, 714.9] · 153 [714.9, 729.8] · 154 [729.8, 744.0] · 155 [744.0, 760.2] · 156 [760.2, 780.4] · 157 [780.4, 799.7] · 158 [799.7, 812.7] · 159 [812.7, 839.0] · 160 [839.0, 864.0] |
| **contact occupancy** | Lap R `pm4r_contact_occupancy.csv` — per-wave nameplate contact counts at R = 150 ground px (declared LOWER BOUND by Lap H-2) |
| **OCR engine** | Apple Vision `VNRecognizeTextRequest`, `.accurate`, `usesLanguageCorrection = false`, `recognitionLanguages = ["en-US"]`, `minimumTextHeight = 0.004` — byte-identical copy of Lap N's `method/ocr.swift`, recompiled; source + binary digests recorded in `pm4q_digests.json` |

---

## 2 — ⚑ A POWER DECLARATION MADE FROM THE INPUT ALONE, BEFORE ANY VIDEO MEASUREMENT

The commission's step 3 specifies the discriminating join as *heal events → waves → wave-roster leech
tiers*. **That join is UNDERPOWERED BY CONSTRUCTION, and this is provable from `pm4p_leech_resistance.csv`
alone without touching the video:**

| wave | n bodies | mean `adcth_mult_COUPLED` | median | share with mult = 0 |
|---|---|---|---|---|
| 151…160 (**all ten, identical**) | 790 | **0.2522** | 0.250 | **6.08 %** |

The 7,900 rows are the **candidate roster replicated per wave** — the same 790 bodies at the same
resistance tiers in every one of the ten waves. **Across-wave contrast in mean COUPLED multiplier is
exactly 1.000 (max/min).** No statistic computed on a wave→tier join can discriminate COUPLED from
DECOUPLED on this board, at any heal-event yield, because the predictor is constant.

Per-**body** attribution would restore contrast, but it is not reachable: Lap H-2's plate census is
purely geometric (`pm4h2_tracks.csv` carries no monster identity), and nothing in the run's artifacts
maps a video body to a roster record.

**Consequence, fixed here:** the pre-registered wave-join comparison statistic is declared
**UNDERPOWERED (ρ undefined; predictor variance zero)** and is reported as such regardless of what the
video yields. The discriminating weight of this lap moves to **Limb 2**, which is an **absolute-magnitude**
test needing no wave contrast at all.

---

## 3 — The two arms' predicted magnitudes (computed from Lap P's own emitted columns, wave 151 = every wave)

Restricted to bodies returning non-zero life; `hit_rate ∈ [11.387, 12.250] /s` (Lap P § 3.3);
`health_max = 20,005` (sheet, Lap A).

| quantity | **COUPLED** | **DECOUPLED** |
|---|---|---|
| heal per hit per body — **median body** | **561 – 1,436** | **2,150 – 5,398** |
| heal per hit per body — board p5 … p95 | 224 … 2,054 | 1,458 … 5,870 |
| heal per hit per body — board min … max (non-zero) | 130 … 2,092 | 372 … 5,977 |
| **HPS at 1 body, median body** | **6,388 – 17,587 HP/s** | **24,477 – 66,126 HP/s** |
| time to refill the full 20,005 bar at 1 body | 1.14 – 3.13 s | **0.30 – 0.82 s** |
| bodies returning ZERO life | 49 / 790 (6.2 %) | 23 / 790 |

**The median-body HPS bands DO NOT OVERLAP** (17,587 < 24,477). That non-overlap is the discriminator.

---

## 4 — Instruments, fixed

### I-Q1 · player-HP trace (the primary discriminator)

* ROI, fixed screen position, verified stable at t = 690 / 750 / 786 / 845 s: **x ∈ [520, 780), y ∈ [996, 1026)** (the health-orb bar readout), extracted by `ffmpeg crop=260:30:520:996` then `scale=1040:120` Lanczos.
* Cadence **60 fps** (the container's native rate) over the combat span **t ∈ [683.0, 864.0]** → 10,861 samples.
* OCR each crop; **accept a read iff it matches `^(\d{1,5})/20005$`** — the denominator is a decoded
  constant (`health_max = 20,005`, Lap A sheet), so it is a free per-sample validator. Every rejected
  read and every distinct denominator observed is censused and published.
* **PC-3 (instrument gate, must PASS):** ≥ 95 % of samples accepted. Below that the limb is
  **UNREACHED-INSTRUMENT** and no verdict is drawn from it.

### I-Q2 · FCT colour census (the commissioned heal-FCT existence question)

* Full-frame OCR at **1.0 s cadence** over t ∈ [683.0, 864.0] → 182 frames, **plus** targeted frames
  (§ 5.3).
* Per OCR box, glyph-stroke colour = **mean RGB of the pixels at or above the 88th luminance percentile
  inside the box** (Lap N's convention, retained so the two laps are comparable).
* Text classes by regex: `pair` `^\(?[\d,]+\s*/\s*[\d,]+\)?$` · `crit` `^(\d[\d,]{0,9})\s*\(x(\d\.\d{2})\)$` ·
  `bare` `^\d[\d,]{0,9}$` · `signed` `^[+-]\d[\d,]{0,9}$` · else `other`.
* Colour classes on the glyph mean: `red_taken` R/G ≥ 1.6 · `cream_dealt` 1.02 ≤ R/G < 1.6 ·
  **`green_candidate` G − max(R,B) ≥ 20 and G ≥ 80** · `blue_candidate` B − max(R,G) ≥ 20 and B ≥ 80 ·
  else `neutral`.
* **The green threshold is deliberately LOOSE (high recall, low precision).** It is set from a 4-frame
  exploratory sample — **disclosed**: on that sample the only genuinely green screen element inside an
  OCR box was the *energy-bar background* behind white glyphs, i.e. a false positive of a box-level
  test, which is exactly why the statistic is glyph-stroke-based and why every candidate is
  hand-adjudicated below.
* **Positive controls for I-Q2 (both must PASS or the limb is UNREACHED-INSTRUMENT):**
  * **PC-1** ≥ 100 `cream_dealt` numeric boxes (`bare` ∪ `crit`) — proves numeric FCT is detected.
  * **PC-2** ≥ 5 `red_taken` numeric boxes — proves a **non-cream coloured** numeric FCT class is
    within the pipeline's reach. Without PC-2, an absence of green is uninterpretable.

### I-Q3 · hand adjudication

Every `green_candidate` numeric box is cropped at native resolution, upscaled ×4 Lanczos, saved to
`evidence/`, and **read by eye**. Verdict per candidate ∈ {`TRUE_GREEN_FCT`, `FALSE_green_background`,
`FALSE_vfx_contamination`, `FALSE_ocr_garbage`}, recorded in the emitted CSV.

---

## 5 — Decision rules, fixed

### 5.1 Heal FCT displayed?

On **adjudicated-TRUE** green numeric FCT boxes only:

| adjudicated TRUE count | verdict |
|---|---|
| ≥ 10 | **DISPLAYED** → extract magnitudes; run § 5.2 wave join (already declared underpowered) and per-event work |
| 1 – 9 | **MARGINAL** — publish every crop, draw no verdict from magnitudes |
| 0 | **NOT DISPLAYED** → the commissioned heal-FCT limb lands **UNREACHED**, exactly as `R-PM4-44` part 2 provides |

### 5.2 The commissioned wave-join statistic (retained, pre-declared underpowered)

Per wave: `heal_per_damage(w) = Σ heal / Σ player-dealt damage`; predictor `mean_mult_COUPLED(w)`.
Spearman ρ over n = 10. **Because the predictor has zero variance (§ 2), ρ is undefined and the test is
reported as UNDERPOWERED, not as a result.**

### 5.3 ⚑ The primary discriminator — HP-trace magnitude (Limb 2)

From the accepted 60 fps trace `h(t)`, `deficit d(t) = 20005 − h(t)`:

* **Recovery window** := a maximal run of consecutive accepted samples with non-decreasing `h`, of
  duration ≥ 0.20 s, beginning at `d ≥ 5,000` (so the full-health cap cannot bind the slope).
* `net_rate = (h_end − h_start) / (t_end − t_start)` HP/s. **S := max net_rate over all recovery windows.**
* **Single-tick steps:** all one-frame positive `Δh` at 60 fps taken from samples with `d ≥ 3,000`.
* **Damage-corrected gross rate:** for the **top-5 recovery windows by `net_rate`**, full-frame OCR at
  60 fps across the window ± 0.25 s; `damage_taken` := Σ of `red_taken` numeric boxes, deduplicated by
  (value, ±40 px position) across the FCT lifetime;
  `gross_rate = (Δh + damage_taken) / Δt`. Those same window frames are ALSO the highest-yield place to
  look for green heal FCT and are fed to I-Q2/I-Q3.

**Verdict rules (fired without discretion, in this order):**

1. **DECOUPLED** if `gross_rate ≥ 24,477 × N_hi_window` HP/s in ≥ 2 of the top-5 windows, where
   `N_hi_window` = the maximum nameplate contact count at R = 150 gpx observed in that wave
   (Lap R / Lap H-2, a declared LOWER BOUND on true bodies, so this test is **conservative against
   DECOUPLED**).
2. **COUPLED** if in ≥ 2 of the top-5 windows `gross_rate ≤ 17,587 × N_lo_window` with
   `N_lo_window = 1`, **and** the 5th percentile of single-tick steps is < 1,458 (DECOUPLED's board p5),
   **and** those small steps survive the damage filter (no `red_taken` numeric FCT within ±0.5 s).
3. Otherwise **UNDECIDED**, publishing every measured number and naming which rule failed and why.

**⚑ THE ASYMMETRY, DECLARED IN ADVANCE, BEFORE ANY NUMBER IS SEEN.** Incoming damage biases every
observed rate **downward**. Rule 1 is therefore robust: a *fast* measured recovery cannot be
manufactured by the confound. Rule 2 is **not** symmetric — a *slow* measured recovery is also what
DECOUPLED-plus-heavy-incoming-damage looks like — which is precisely why rule 2 carries the
damage-correction and small-step conditions. **If the damage correction cannot be applied (red-FCT
capture fails PC-2, or the windows carry unnumbered damage sources), rule 2 is UNAVAILABLE and the
landing is UNDECIDED. A slow recovery alone will NOT be reported as COUPLED.**

### 5.4 Confounds named in advance, to be reported not hidden

1. Heal FCT, if displayed, may **aggregate** ADCTH + regen (129.38 hp/s) + procs + potions; per-hit
   attribution to a single body is not expected to be possible.
2. **Potions** (`skillLifePercent = 35`, Lap G/P) and **Menhir's Will** (+120 hp/s below 33 % health)
   are non-ADCTH heal sources that can inflate any recovery window. Every top-5 window is inspected for
   a potion-flash / proc icon and the finding is stated.
3. `N_bodies` is a **lower bound** (nameplate census; large bodies under-counted, Lap H-2's own caveat).
   Lower `N` makes rule 1 easier to fire and rule 2 harder — i.e. the bias runs **against** the
   COUPLED reading, which is the direction that protects this lap from confirming Lap P's own lean.
4. `U-P-N-2` (pre- vs post-mitigation basis, ~9 % on this board) and `U-P-N-5` (crit uplift, **not**
   folded into Lap P's bands) both sit inside the predicted magnitudes. **`U-P-N-5` matters here:**
   Lap N measured a mean effective crit multiplier on crit events and the sheet line is pre-crit, so
   the true heal per hit may exceed both bands' face values. This is stated as a **known upward bias on
   both arms alike** and is carried into the verdict discussion; if a measured rate lands between the
   bands, crit uplift is the first named explanation, not a tiebreaker for either arm.
5. The video is one run, one build, waves 151–160. Nothing here generalises to Grim Dawn at large.

---

## 6 — What this lap will NOT do

* Will not read I-18/I-17 sim output, gamora landing notes, batons, or the charter scorecard beyond the
  single trigger boolean already quoted in the commission.
* Will not average the two arms, or pick one by plausibility. Absent a rule firing, the landing is
  UNDECIDED and `U-P-N-1` stays bracketed.
* Will not modify any source. Read-only throughout.

**PRE-REGISTRATION ENDS.**
