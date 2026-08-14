# RUN KC2-PM4 · LAP Q · FINDINGS — THE HEAL DISCRIMINATOR

> **Seat:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Date:** 2026-08-14
> **Commission:** charter `R-PM4-44` part 2 · pre-named `L-32` · trigger met `L-35`
> **Pre-registration:** `PREREGISTRATION.md`, sha256 **`da62709f2887df1e2874f7cc1baa0ef2cd901ea47ce555678b9d4d98c07dfa77`**
> — written and hashed **before** any instrument ran over the full video; **hash re-verified UNCHANGED
> at banking.**
> **Laws:** GL-12 ENTIRE — decode-never-estimate · outcome-firewalled · GL-6 full 64-hex digests ·
> READ-ONLY on every source.

---

## 0 — HEADLINE

| # | finding |
|---|---|
| **1** | **HEAL FLOATING COMBAT TEXT IS *NOT DISPLAYED* IN MATT'S SETTINGS.** 679 full frames, 17,908 OCR observations, 2,352 non-HUD numeric FCT boxes. **Zero** adjudicated green heal numbers (40 loose candidates → 18 distinct → **18/18 FALSE**, all white glyphs over green VFX). **Zero** `+N` heal strings (3 `signed` reads → **3/3 OCR garbage**, hand-adjudicated). Both positive controls PASS, so the absence is **measured, not assumed**. The commissioned heal-FCT limb is **UNREACHED**, exactly as `R-PM4-44` part 2 provides. |
| **2** | **⚑ THE COMMISSIONED WAVE→TIER JOIN IS UNDERPOWERED BY CONSTRUCTION — provable from the input CSV alone, before any video measurement.** `pm4p_leech_resistance.csv`'s 7,900 rows are the same 790-body candidate roster replicated in every wave: `mean adcth_mult_COUPLED = 0.2522` and `zero-share = 6.08 %` in **all ten waves**. Across-wave contrast is **exactly 1.000**. No statistic on that join can discriminate, at any heal yield. |
| **3** | **⚑ A DIFFERENT INSTRUMENT REACHED THE ANSWER: the player's own HP readout, OCR'd at 60 fps.** 10,861 samples, **100.00 % accepted** against the decoded denominator. The trace resolves to **1 HP and 1 frame** and separates cleanly into a regeneration **drip** (+2/+3 HP per frame) and discrete ADCTH **leech ticks**. The tick magnitude *is* the quantity `U-P-N-1` disagrees about. |
| **4** | **⚑ VERDICT — `U-P-N-1` = COUPLED.** Fired by pre-registered rule 5.3 rule 2 without discretion (rule 1 did not fire, 0/5). Observed clean tick median **820.8 HP**, INSIDE COUPLED's median band [561, 1436]; **0.38×** *below* DECOUPLED's band [2150, 5398]. **8 of 19** damage-filtered ticks fall **below DECOUPLED's absolute board MINIMUM of 371.8** — a value no body among the 790 can produce under that arm at N ≥ 1. Gross recovery rate **4,289–10,690 HP/s** in all five windows, against a DECOUPLED floor of **≥ 195,816 HP/s**. |
| **5** | **⚑ THE STRONGEST FORM: the measurement RECOVERS the weapon-damage basis, and only COUPLED recovers the right one.** Inverting the heal formula on the observed median tick gives an implied `D_weapon` of **15,315 – 44,670** under COUPLED (tier-dependent) — bracketing the sheet's own camera-measured `weapon damage per hit = 16,972 – 40,930` — versus **5,360 under DECOUPLED, 3.2× below the sheet's minimum**, and **1,012 (17× below) on the smallest filtered tick.** The verdict is therefore not merely "the numbers are smaller than DECOUPLED"; it is that COUPLED reproduces an independently camera-measured quantity that DECOUPLED misses by a factor of 3–17. |
| **6** | **Three free decodes fell out of the same trace, each an independent check on Lap P.** (a) **Regeneration measured 124.67 HP/s** on the uncontaminated sub-33 %-health subset vs Lap P's decoded **129.38 HP/s** — residual **−3.64 %**. (b) **Hit cadence measured 11.408 ticks/s** (mean inter-tick gap 5.259 frames) — **inside Lap L's decoded bracket [11.387, 12.250]**, at its LO edge. (c) **Menhir's Will is MEASURED-ABSENT**: below 33 % health the drip stays at 124.67 HP/s, not the 249.38 HP/s its `+120 hp/s` circuit-breaker would produce. |
| **7** | **⚑ NEW, unmodelled anywhere in the run: the player's MAX HEALTH is not constant.** For one contiguous **8.283 s** episode, `t = 713.383 – 721.650` (straddling the w152→w153 boundary), the readout denominator is **16,368**, not 20,005 — a **−18.18 %** max-health reduction (Δ = −3,637 HP). Recorded as `D-Q1`; the sim models `health_max` as a constant. |
| **8** | The referent video now has a **full sha256** — `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8`. Laps H-2 / M / N / R all recorded it as NOT COMPUTED. |

---

## 1 — Inputs, all re-hashed before use (GL-6)

| input | sha256 | check |
|---|---|---|
| referent MP4 (479,438,089 B · 1920×1080 · 60 fps · 1034.10 s) | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` | **computed by this lap** (prior laps: NOT COMPUTED) |
| `pm4p_leech_resistance.csv` (7,900 rows) | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` | **EXACT** vs the commission |
| `pm4n_fct_events.csv` (2,328 rows) | `cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2` | recorded |
| `method/ocr.swift` | `1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1` | **byte-identical to Lap N's** |
| `PREREGISTRATION.md` | `da62709f2887df1e2874f7cc1baa0ef2cd901ea47ce555678b9d4d98c07dfa77` | **UNCHANGED between pre-registration and banking** |

Wave boundaries: Lap H-2 `OBS-H2-6` as carried in Lap R (±0.25 s). Contact counts: Lap H-2
`pm4h2_ring_density.csv` `max_R150` — wave 159 = 9, wave 160 = 8, a **declared LOWER BOUND**.

---

## 2 — LIMB 1 · IS HEAL FCT DISPLAYED? — **NO** (the commissioned limb, UNREACHED)

### 2.1 What was run

679 full frames OCR'd: a **1.0 s census** across the whole combat span `t ∈ [683.0, 864.0]` (181 frames)
**plus 60 fps capture across the five pre-registered maximum-healing windows** (498 frames) — the
highest-yield place in the entire recording for a heal number to appear, chosen by Limb 2's trace, not
by eye. 17,908 OCR observations; 2,352 non-HUD numeric FCT boxes.

### 2.2 The positive controls — both PASS, which is what makes the absence readable

| control | requirement | measured | verdict |
|---|---|---|---|
| **PC-1** numeric FCT is detected at all | ≥ 100 cream numeric boxes | **1,712** | **PASS** |
| **PC-2** a **non-cream coloured** numeric FCT class is within reach | ≥ 5 red numeric boxes | **16** | **PASS** |
| **PC-3** HP-trace instrument | ≥ 95 % accepted reads | **100.00 %** | **PASS** |

**PC-2 is the load-bearing one.** Damage-*taken* floating text IS rendered in this footage in a distinct
red, and this pipeline finds it. So "no green heal text" is a statement about the game's output, not
about the instrument's colour reach.

### 2.3 Adjudication — 18/18 FALSE

The loose green rule (`G − max(R,B) ≥ 20 and G ≥ 80` on glyph strokes) returned 40 boxes → **18 distinct
events**. Every one was cropped at native resolution, upscaled ×4 and **read by eye** (`evidence/g00…g17`).
**All 18 are white/cream glyphs sitting on a bright green VFX plume**; not one has green strokes. Class
`FALSE_vfx_contamination`, 18/18.

The three `signed` reads were adjudicated too (`evidence/SIGNED_0..2`): `+9481` is **`19481`** with the
leading `1` mis-read as `+`; `−32909` is **`32909`** with a spurious stroke; `−22421` likewise.
`FALSE_ocr_garbage`, 3/3.

**A trap this lap walked into and reports rather than hides:** the first green "detection" was the
**energy bar's green background** behind white digits (`1548/2576`, box-level green fraction 0.193 —
`evidence/hud-energy-bar-green-background-750.png`). A box-level colour test would have called that a
green heal number. That is precisely why the pre-registered statistic is **glyph-stroke**, and why every
candidate is adjudicated by eye.

### 2.4 The honest limit of Limb 1

If Grim Dawn rendered heal text in the *same* cream as damage-dealt text, this instrument could not tell
them apart. Limb 2 answers that too: across the five windows the player gained **27,954 HP** in
discrete steps, and **not one cream numeric FCT box matches any observed HP step.** There is no
displayed heal number of any colour.

**LIMB 1 LANDING: heal FCT NOT DISPLAYED → the commissioned limb is UNREACHED.**

---

## 3 — LIMB 1b · THE COMMISSIONED WAVE JOIN — **UNDERPOWERED BY CONSTRUCTION**

Declared in the pre-registration **from the input alone**, before any video measurement:

| wave | n | mean `adcth_mult_COUPLED` | median | zero-share |
|---|---|---|---|---|
| **151 … 160 — all ten identical** | 790 | **0.2522** | 0.250 | **6.08 %** |

The predictor has **zero variance**. Spearman ρ is undefined; `heal_per_damage(w)` cannot correlate with
a constant. Per-**body** attribution would restore contrast and is **UNREACHED**: Lap H-2's plate census
is purely geometric (`pm4h2_tracks.csv` carries no monster identity) and nothing in the run maps a video
body to a roster record.

The per-wave measured tick magnitudes are published anyway (`§ 5.4`), beside a predictor that does not
move — that is the honest way to deliver the join, not a correlation coefficient computed on a constant.

---

## 4 — LIMB 2 · THE INSTRUMENT THAT REACHED IT

### 4.1 The trace

ROI `x ∈ [520,780), y ∈ [996,1026)` — the health-orb bar readout, position-stable across the fight
(`evidence/hud-player-health-readout-750.png`). 60 fps, `t ∈ [683.0, 864.0]`, 10,861 crops, Apple Vision
OCR. Reads validated against the **decoded** denominator (`health_max`, Lap A sheet): **100.00 % accepted.**

| quantity | value |
|---|---|
| HP min / max | 5,360 / 20,005 |
| frames at full health | 4,653 (**42.84 %**) — 57 % of the fight is spent below full |
| frames below 50 % / 33 % of max | 376 (3.46 %) / 109 (1.00 %) |
| frames showing an HP **decrease** | 1,491 (**13.73 %**) |
| `health_max` values observed | **{20,005 · 16,368}** — see `D-Q1`, § 6 |

### 4.2 ⚑ Instrument positive controls — the trace reproduces two of Lap P/L's independent decodes

| control | decoded elsewhere | measured here | residual |
|---|---|---|---|
| **health regeneration** (drip, sub-33 %-health subset — the only stretch uncontaminated by sub-50 HP leech ticks) | Lap P § 5.5 sheet **129.38 HP/s** | **124.67 HP/s** (n = 90; 87 × +2 HP/frame) | **−3.64 %** |
| **EoR hit cadence** (mean inter-tick gap 5.259 frames) | Lap L bracket **11.387 – 12.250 /s** | **11.408 ticks/s** | **INSIDE the bracket**, at LO edge |
| **Menhir's Will** `+120 hp/s` below 33 % health (Lap G circuit-breaker) | would give 249.38 HP/s | **124.67 HP/s** | **MEASURED-ABSENT** |

*(The naive whole-trace drip reads 178.40 HP/s — that figure is **contaminated** by leech ticks smaller
than the 50 HP separator and is reported here only so nobody later mistakes it for regeneration.
Reported, not buried.)*

The mode of the inter-tick gap is 6 frames (10.0 /s); the **mean** over gaps ≤ 7 frames is 5.259 frames
(11.408 /s). The mode is inflated by ticks that healed nothing and are therefore invisible; the mean over
contiguous runs is the estimator that matches the decode.

---

## 5 — ⚑ THE DISCRIMINATOR AND THE VERDICT

### 5.1 The logic, stated before the numbers

`observed step = (heal per hit per body) × N_bodies`, with `N ≥ 1` whenever a step exists. So
**`observed_step / 1` is an UPPER bound on per-body heal, and larger N only pushes the implied per-body
value DOWN — i.e. further from DECOUPLED.** The confound therefore runs *against* DECOUPLED, not for it,
and incoming damage biases every observed rate **downward** as pre-registered.

### 5.2 The leech-tick census

129 ticks (step ≥ 50 HP, deficit ≥ 3,000 so the cap cannot bind, step not landing on the cap).
**Clean subset** (no HP decrease within ±2 frames — no damage masking): **n = 67**.

| | min | p5 | p25 | **median** | p75 | p95 | max |
|---|---|---|---|---|---|---|---|
| all 129 | 54.8 | 95.8 | 310.8 | **782.8** | 1,303.8 | 2,940.8 | 8,541.8 |
| clean 67 | 60.8 | — | 370.8 | **820.8** | 1,330.8 | — | 5,468.8 |

| arm | median band (per hit per body) | board p5 | board min | **observed clean median 820.8** |
|---|---|---|---|---|
| **COUPLED** | **561 – 1,436** | 224 | 130 | **INSIDE the band** |
| **DECOUPLED** | 2,150 – 5,398 | 1,458 | 372 | **0.38× BELOW the band floor** |

| arm | ticks below board **min** | below board **p5** | below median-band floor |
|---|---|---|---|
| COUPLED | 10 / 129 (7.8 %) | 26 (20.2 %) | 53 (41.1 %) |
| **DECOUPLED** | **38 / 129 (29.5 %)** | **103 (79.8 %)** | **113 (87.6 %)** |

### 5.3 The five pre-registered recovery windows, damage-corrected

| win | wave | span (s) | dur | HP gain | red FCT | damage | **net** | **gross** | DECOUPLED floor | COUPLED@N=1 ceiling |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 160 | 843.383–843.917 | 0.533 | 5,141 | 0 | 0 | 9,639 | **9,639** | ≥ 195,816 | ≤ 17,587 |
| 2 | 160 | 862.167–863.217 | 1.050 | 9,694 | 0 | 0 | 9,232 | **9,232** | ≥ 195,816 | ≤ 17,587 |
| 3 | 160 | 841.483–842.233 | 0.750 | 6,032 | 0 | 0 | 8,043 | **8,043** | ≥ 195,816 | ≤ 17,587 |
| 4 | 159 | 833.067–835.267 | 2.200 | 12,187 | 1 | 11,330 | 5,540 | **10,690** | ≥ 220,293 | ≤ 17,587 |
| 5 | 159 | 822.083–823.350 | 1.267 | 5,433 | 0 | 0 | 4,289 | **4,289** | ≥ 220,293 | ≤ 17,587 |

* **RULE 1 (DECOUPLED)** — needs ≥ 2 windows at or above the floor: **0 / 5 → DOES NOT FIRE.** The
  observed gross rates are **18 – 51× below** the threshold.
* **RULE 2 (COUPLED)** — all three conditions met:
  1. windows at or below the COUPLED@N=1 ceiling: **5 / 5** (needs ≥ 2) ✓
  2. tick p5 **95.8** < DECOUPLED board p5 **1,458.5** ✓
  3. small steps survive the **literal** pre-registered damage filter (no red numeric FCT within ±0.5 s,
     applied inside the OCR-covered windows): 19 ticks pass the filter; **16/19 fall below DECOUPLED's
     board p5 and 8/19 fall below DECOUPLED's absolute board MINIMUM (371.8)** — the smallest being
     **147.8, 150.8, 152.8, 161.8, 162.8, 186.8, 196.8** ✓

**A step of 148 HP cannot be produced by DECOUPLED at N ≥ 1 by any of the 790 bodies on the board.**

**These small ticks are not fragments.** They arrive at `t = 833.100, 833.183, 833.267, 833.350` —
**exactly 5 frames apart, 0.0833 s, 12.0 ticks/s** — i.e. they are *consecutive EoR ticks at the decoded
channel cadence*, each healing 148–187 HP, not one tick split across frames.

### 5.4 ⚑ Inverting the formula — the measurement recovers the weapon-damage basis

`step = 0.21 (ADCTH) × 0.57 (WD-fraction) × 1.22 (healing increase) × leech_mult × D_weapon`

| arm / tier | on the median tick (782.8) | on the smallest filtered tick (147.8) |
|---|---|---|
| **COUPLED @ 0.12** (boss/quest tier) | implied `D_weapon` = **44,670** | 8,436 |
| **COUPLED @ 0.35** (trash floor) | implied `D_weapon` = **15,315** | 2,892 |
| **DECOUPLED** | implied `D_weapon` = **5,360** | **1,012** |
| **the sheet's own camera-measured line (Lap A / Lap L)** | **16,972 – 40,930** | **16,972 – 40,930** |

**COUPLED's tier range brackets the independently camera-measured weapon-damage line. DECOUPLED misses
it low by 3.2× on the median tick and by 17× on the smallest.** For DECOUPLED to hold, the sheet's
`Weapon — damage per hit` would have to be wrong by a factor of 3–17 — and it is corroborated in the same
footage by displayed EoR damage numbers in the tens of thousands, consistent with the sheet's paired
`EoR damage per hit = 43,691 – 59,761`.

### 5.5 **VERDICT: `U-P-N-1` = COUPLED**

Life Leech Resistance (`defensiveSlowLifeLeach`) **gates the player's ADCTH heal.** The community reading
Lap P cited — *"resistance to Attack Damage Converted to Health"* — is confirmed against the referent's
own frames. Lap P's `adcth_mult_COUPLED = max(0, 1 − res/100)` is the arm the measurement supports;
`adcth_mult_DECOUPLED` is **excluded** at every one of the five windows and on 8 damage-filtered ticks by
absolute board-minimum violation.

**Operative consequence for the board, restated from Lap P's own emitted columns (not re-derived here):**
the ladder 65/75/83/88/105/115/565/588 % applies to the heal; **490 of 7,900 body-waves return ZERO
life**; the median body returns a quarter of face value.

---

## 6 — DECLARED DEPARTURES, DEFECTS AND NEW GAPS

| id | statement |
|---|---|
| **DEP-Q1** | **Departure from PREREGISTRATION § 5.3, declared with reason.** Red-FCT dedup was specified as `(value, ±40 px)`; GD floating text **drifts upward** over its ~1.2–1.5 s lifetime (Lap N measured the lifetime), so a positional key does not hold one string together and **over-counts damage — which would have biased the gross rate UPWARD, toward DECOUPLED.** Replaced by: cluster values within 5 % inside a 2.0 s neighbourhood. The replacement is the conservative rule for this lap's own lean. |
| **DEP-Q2** | Same clause: a damage-**taken** read above `health_max` cannot be a hit the player survived (he never died in the referent), so such reads are rejected as OCR merges. This caught **`113856`** at `t = 833.950`, which had inflated window 4's damage to 136,522 HP — a **12× over-count**. Self-caught by hand-adjudicating the crops; reported, not silently patched. |
| **DEP-Q3** | Rule 2's small-step damage filter was pre-registered as "no red FCT within ±0.5 s". Red-FCT coverage exists only where 60 fps full-frame OCR was run (the five windows). The **literal** filter is applied there (§ 5.3, 19 ticks) and a **broader, stricter** proxy — no HP decrease within ±2 frames — is reported across the whole trace (67 clean ticks). Both agree. |
| **D-Q1** | **⚑ `health_max` IS NOT CONSTANT.** One contiguous 8.283 s episode, `t = 713.383 – 721.650` (straddling w152→w153), reads a denominator of **16,368** — **−18.18 %**, Δ = −3,637 HP. Mechanism **UNDECODED** (a monster "Reduced Target's Health" effect is the obvious candidate; **not** decoded from the corpus by this lap, so it is recorded as a gap, not asserted). The sim models `health_max` as a constant. |
| **D-Q2** | **Regeneration residual −3.64 %** (measured 124.67 vs Lap P's sheet 129.38 HP/s). Small, and it sits beside Lap P's own `D-P2` regen gap; a HUD flooring artefact is an equally live explanation. Not resolved here. |
| **U-Q-1** | `N_bodies` is never independently observed at tick resolution. Lap H-2's plate census is a declared **lower bound**. This does not weaken the verdict — larger `N` moves the inference **away** from DECOUPLED — but it does mean the *absolute* per-body heal is an upper bound, not a point value. |
| **U-Q-2** | The verdict is conditional on Lap P's decoded chain (ADCTH 21 % · WD-fraction 0.57 · healing increase 1.22) and on `U-P-N-4`'s reading of the sheet's weapon-damage line. § 5.4 is the strongest available defence — the measurement *recovers* that line under COUPLED — but it is a recovery, not an independent decode, and `U-P-N-4` stays open. |
| **U-Q-3** | `U-P-N-5` (crit uplift on ADCTH) is **not** folded into either band. If ADCTH inherits crit, both arms' predictions rise, and the gap to DECOUPLED **widens**. The direction is named; the magnitude is not decoded. |
| **U-Q-4** | The heal/damage-ratio check (§ measured 0.0043 aggregate) is **directionally consistent but NOT decisive** and is deliberately not used in the verdict: its numerator is truncated (sub-50 HP ticks and cap-clipped ticks excluded) and its denominator is crit-inflated. Published so the conductor sees what was looked at and rejected. |
| **UNREACHED-1** | Heal FCT magnitudes, per-event heal attribution, and the wave→tier correlation — all UNREACHED, for the reasons in §§ 2 and 3. `pm4q_heal_events.csv` therefore carries **HP-trace-derived** heal events, not FCT-derived ones; its provenance column says so. |

---

## 7 — EMITTED ARTIFACTS

| file | rows | sha256 |
|---|---|---|
| `PREREGISTRATION.md` | — | `da62709f2887df1e2874f7cc1baa0ef2cd901ea47ce555678b9d4d98c07dfa77` |
| `pm4q_heal_events.csv` | 129 | `7f89d2ada0abce3b947406c4ceab7234267cfcdc0a5b7ee4a2fbec8eec71aeab` |
| `pm4q_hp_trace.csv` | 10,861 | `5597e1a8c993fa183adc3f2310570e70e4da47b6c1f882ad62a96583f57090fa` |
| `pm4q_recovery_windows.csv` | 5 | `4a95209b599749357dc8f1f6e766b2a07628f3fceaffa45e8f7c082617f98daa` |
| `pm4q_fct_colour.csv` | 17,908 | `48e12482a173a00eaa695eab5b4c32e98ff12eb623154fc000a71c1aa68958c5` |
| `method/ocr.swift` | — | `1a96036ddbdfe4d55e2be31f534e9a9661db152dc71d4c36e18c684ab8b94ec1` |
| instruments | — | `agentic_orchestration/research/scripts/pm4q_fct_colour_2026_08_14.py`, `pm4q_hp_trace_2026_08_14.py` |
| evidence | 23 files | 18 green adjudication crops · 3 signed-read crops · 2 HUD reference crops |

Full digest ledger incl. inputs: `pm4q_digests.json`.

---

## 8 — WHAT THIS LAP DID NOT DO (the firewall, stated)

Read no I-17/I-18 sim output, no gamora landing note, no baton, no scorecard beyond the single trigger
boolean quoted in the commission. Modified no source. Did not average the arms or pick one by
plausibility — the verdict is the output of a rule fixed before the instruments ran, and rule 1 was given
every chance to fire first, on a threshold deliberately set **conservative against** the arm the
measurement ended up rejecting.
