# MD-B4app-2 — the referent's MOVE / CHANNEL duty cycle, measured off camera

**Date:** 2026-08-25
**Author:** galadriel (visual perception + benchmark seam)
**Commissioned by:** gandalf RUN-CONDUCTOR, ruling `R-L75-4`, KC2 model-completion run charter
**Status:** WORKING — evidentiary note. DERIVED grades only.
**Measurement definition read first:** `reincarnated-engine/src/reincarnated/simulation/math/kc2-mc-b4app-gate-model-2026-08-25.md` § 7 + § 14 (`MD-B4app-2` row); `gandalf/notes/2026-08-25-kc2-mc-wave2-close-drift-critic-verdict.md` `F-11` + Q5.
**Footage:** `~/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (1920×1080, 60 fps, 1034.10 s) — the referent fight. Second board: `~/gd-scratch/eor-test-1/eor-warlord-2026-08-04 21-09-31.mp4`.
**Evidence root:** `galadriel/captures/2026-08-25-md-b4app-2-channel/`
**New pipeline:** `galadriel/pipeline/eor_channel.py`, `galadriel/pipeline/eor_duty.py`
**Read-only on all source material. No engine writes. No pushes.**

---

## TOP LINE

> ## The referent's channel is **83.8 %** of combat time — and it **does not stop when he moves.**
>
> ## `G5` is not an upper bound on a loss the referent takes. On this footage the referent takes **no measurable loss at all**, and the run's exclusion set does not need a policy entry for *channel uptime*. It needs one for **movement**, which is a different quantity and points the other way.

`F-11` asked whether the 151–156-vs-160 residual is a PILOT-POLICY gap: *"the sim pilot never STOPS TO CHANNEL the way Matt visibly does."* Measured against the footage, both halves of that sentence come apart:

| quantity | sim `G0` | sim `G5` (break folded) | **REFERENT (measured)** |
|---|---|---|---|
| channel uptime | 2,700 / 2,700 player ticks | **50 / 2,700 = 1.9 %** | **83.8 %** of combat time |
| channel while moving | 2,368 / 2,700 = 87.7 % | 0 | **P(channel \| moving) = 89.2 %** |
| moving fraction | 785 / 910 = **86.3 %** | — | **62.6 %** |
| stationary fraction | 13.7 % | — | **37.4 %** |

Sim keys quoted from `082b599a…` `⚑ channel_census_per_cell` / `⚑ channel_reports.G0b` via `F-11`'s table; referent figures derived below.

**Three consequences, in the order they bite:**

1. **`G0` is nearer the referent than `G5` is, by a factor of forty.** Folding the channel break moves the sim's channel uptime from 100 % to 1.9 % against a referent measured at 83.8 %. The fold is a move *away* from the referent, not a correction toward it.
2. **He does not stop to channel. He stops to do something else.** 17.0 % of his stationary time carries **zero** drain ticks against 3.0 % of his moving time. His stops are where his *non*-channel actions live.
3. **The real policy divergence is movement, and it is much smaller than the channel one.** The sim moves 86.3 % of ticks; the referent 62.6 %. A 1.38× over-move, not a 40× anything.

---

## 0 · WHAT WAS MEASURED, AND WHAT IT IS NOT

The measurement window is **`682.10 → 864.75` = 182.65 s** — the wave-151 badge flip to the player's death, both taken from my own committed sitting-2 timeline (`galadriel/notes/2026-08-07-eor-sittings-extraction.md` § wave badge; death instant corrected to 864.75 in `…2026-08-08-eor-followup-extraction.md` § 7.1). Ten waves, no prep, no post-death.

Two instruments. Neither asks the player what he intended.

- **MOTION** — camera-pan registration of the play area. Grim Dawn's camera is player-locked, so scene translation *is* player translation. **This measures whether he moved.**
- **ENERGY** — the HUD energy readout `cur/max`, glyph-atlas OCR. **This measures whether he was spending energy at a channel's rate.**

**What neither measures:** which *skill* the energy belongs to, and what the input device was doing. Both are named in § 7 as UNMEASURABLE, with the reason, and neither changes the conclusion.

---

## 1 · THE MOTION INSTRUMENT — and its validation

`eor_channel.py motion`, sampled at **20 Hz**, **3,652 registration intervals** over the window. Sub-pixel phase correlation on the achromatic component of the play-area band `y 150..930, x 40..1620` (HUD, minimap, floating-combat-text column and status strip excluded), 2× downsampled, Hann-windowed, saturated combat VFX down-weighted `1/(1+6·sat)`.

### 1.1 The classification is not a fitted threshold — the distribution is bimodal with an empty valley

Per-interval |d| histogram, all 3,652 intervals:

| |d| (px per 0.05 s) | count | share |
|---|---:|---:|
| < 0.30 | 1,362 | **37.29 %** |
| 0.30 – 2.00 | **56** | **1.53 %** ← the valley |
| ≥ 2.00 | 2,234 | 61.18 % |

The static mode sits at 0.01–0.05 px on 1,067 of the 3,652 intervals — frames that are *pixel-identical* in the background band. The threshold is placed at **1.0 px**, inside a valley that carries 1.5 % of the mass.

**Two guards, both stated, both necessary:**
- **|d| ≥ 1.0 px** per interval, AND
- **net displacement ≥ 3.0 px** over a ±0.30 s window. Grim Dawn applies screen-shake on heavy hits; shake *oscillates* and cancels under integration, translation *accumulates*. The guard costs 0.6 percentage points (62.05 % → 62.65 % moving) — small, but it is the difference between measuring the player and measuring the impact.
- Runs shorter than 3 samples (0.15 s) are absorbed into their neighbour, so one mis-registration cannot split an episode.

### 1.2 Result, with its sensitivity published

**Stationary 0.3735 · Moving 0.6265.**

| swept parameter | range swept | `frac_stationary` |
|---|---|---|
| |d| threshold | 0.3 → 3.0 px | 0.368 → 0.403 |
| net-displacement threshold | 0 → 8 px | 0.354 → 0.412 |

The figure moves by ±0.03 across a tenfold threshold sweep. **It is not a fitted number.**

### 1.3 Validation — endpoint registration, a different reduction

For each of the 42 episodes ≥ 1.5 s, register the episode's **first frame directly against its last** — no chaining, no integration, an independent path to the same claim.

| class | n | median endpoint |d| | p90 | share < 5 px |
|---|---:|---:|---:|---:|
| STATIONARY | 14 | **0.79 px** | 4.49 px | **0.929** |
| MOVING | 28 | 8.64 px | 259.39 px | 0.429 |

⚑ **The honest part.** The MOVING column is a *weak* instrument and I am not leaning on it: at displacements past half the band the correlation wraps and stops locking (lock ratios ≈ 1.0–1.2 = no lock), and out-and-back episodes genuinely end where they start. **The STATIONARY column is strong and it is the half that carries the load** — the seven stationary episodes with a genuine lock (ratio ≥ 2.5) register at 0.01, 0.02, 0.03, 0.04, 0.07, 0.12 and 1.56 px. Stationary episodes are stationary.

### 1.4 Validation — the eye, on an instrument that shares no pixels

`evidence/validate-STATIONARY-810.25-815.05.png` and `evidence/validate-MOVING-817.90-824.05.png` each pair the world view and the **minimap** at an episode's start and end.

- **Stationary (4.8 s):** the minimap's arena plan is in the same place at both ends; only monster icons have moved. The world view shows the same floor geometry.
- **Moving (6.15 s):** the arena plan has translated across the disc and the world view is a different part of the arena.

⚑ **This rules out the one alternative that would have inverted everything: camera rotation.** Grim Dawn's minimap is north-up (established in my 2026-08-08 note § 0). A rotated camera translates the world view and leaves the minimap plan where it is. The plan moved. **He moved.**

### 1.5 REJECTED INSTRUMENT — minimap phase correlation, recorded so it is not retried

I attempted the minimap as a *quantitative* cross-check and it does not work.

- At a 0.05 s baseline the displacement to be measured (~0.5 px) is below the disc's own jitter; median |d| was **0.958 px for MOVING and 0.974 px for STATIONARY** — no discrimination whatever.
- At a 0.5 s baseline the correlation does not lock: it returns 7–11 px on windows where the play area reads 0.5 px of net travel, in both classes (Pearson r against play-area net displacement = **0.204**).

The disc is ~190 px across an arena whose worst-case span is ~76 m — roughly 0.4 m/px — and the icon-clipping mask leaves a dominant circular aperture the correlation prefers to lock onto. **The minimap is a good instrument for counting and placing actors (2026-08-08 § 0) and a bad one for measuring player velocity.** Both statements now have evidence.

---

## 2 · THE ENERGY INSTRUMENT — and the control that makes it specific

`eor_channel.py energy`, **60 Hz**, HUD box `x 1240..1344, y 1004..1030` (located from achromatic-bright column runs, not assumed). Glyph atlas built from **10 hand-read frames** covering all ten digits and `/`; every atlas string was eye-read from a ×6 crop (`work/energy-sheet.png`).

**10,959 samples · 10,503 parsed (95.8 %) · 10,360 passed the `max == 2576` gate · 291 rejected by a neighbour-median filter (a sample >250 from the median of its five nearest neighbours — this catches single-glyph drops such as `1501 → 101`) · 10,069 used.**

### 2.1 The drain tick, and its specificity proven before use

A **drain tick** is `ΔE ≤ −6` between consecutive 1/60 s samples.

⚑ **Control, run before any claim:** two 40-second non-combat windows — `600–640` (pre-run prep, no monsters) and `880–920` (after the death, arena empty). **4,800 samples, 100 % parsed, energy identically `1594` in every one, and ZERO drain ticks.** The detector has no false-positive rate on 80 s of footage from the same recording.

That control also fixes the cap: **1594 is the player's reserved-adjusted energy ceiling** (2576 is the unreserved max). 1594 accounts for 2,791 of the 10,069 in-fight samples (27.7 %).

### 2.2 What the ticks look like

| | in-fight |
|---|---|
| drain ticks in the window | **1,640** |
| median tick size | **−13 to −14** energy |
| median inter-tick interval | **0.083 – 0.100 s** |
| gross drain rate | **≈ −190 energy/s** |

EoR's own tooltip, read off this same recording at t = 215 (`2026-08-08` note § 3): **`176.4 Energy Cost per Second`**, *"deals damage and drains Energy every 0.16 s"* at 100 % Attack Speed. Measured gross drain −190/s against a published 176.4/s, and a measured tick faster than the 0.16 s base — the direction attack speed moves it.

**Graded honestly: the drain is EoR-CONSISTENT, not EoR-IDENTIFIED.** Rate, cadence and combat-exclusivity all match; the HUD cannot name a skill. § 7 carries the residual.

---

## 3 · THE ANSWER — channel uptime

**Channel-active** = a 0.5 s window carrying **≥ 3 drain ticks** (i.e. ≥ 6 /s against a channel's ~10 /s and a control's 0 /s), evaluated on a 0.05 s grid.

**Coverage correction, stated because it moves the number:** windows with few surviving energy samples score artificially low (windows with < 10 of 30 samples score `channel_active = 0.000` by construction). All headline figures are restricted to windows with **≥ 26 of 30** energy samples — **85.77 % of the fight**. The uncorrected figure is 78.9 %; the corrected is 83.8 %. The uncorrected one is the conservative floor.

| statistic | value |
|---|---|
| **channel-active (≥3 ticks / 0.5 s)** | **0.8375** |
| channel-active (≥2 ticks / 0.5 s) | 0.8953 |
| channel-active (≥4 ticks / 0.5 s) | 0.7530 |
| **provably NOT channelling (zero ticks in the window)** | **0.0795** |
| P(channel-active \| STATIONARY) | **0.7376** |
| P(channel-active \| MOVING) | **0.8920** |
| P(zero-tick \| STATIONARY) | **0.1701** |
| P(zero-tick \| MOVING) | **0.0301** |

**The referent's channel is up on 75–90 % of his combat time depending on where the threshold is put, and he is demonstrably idle on under 8 % of it.**

⚑ **And channel uptime is HIGHER while he is moving than while he is standing** — 0.892 vs 0.738, with the zero-tick mass concentrated in his stops by 5.7×.

### 3.1 Per wave

| wave | dur (s) | channel-active | stationary |
|---:|---:|---:|---:|
| 151 | 16.28 | 0.648 | 0.382 |
| 152 | 16.45 | 0.922 | 0.340 |
| 153 | 14.79 | 0.921 | 0.493 |
| 154 | 14.13 | 0.813 | 0.376 |
| 155 | 16.33 | 0.565 | 0.346 |
| 156 | 20.22 | 0.923 | 0.389 |
| 157 | 19.13 | 0.849 | 0.222 |
| 158 | 13.19 | 0.826 | 0.587 |
| 159 | 26.25 | 0.924 | 0.265 |
| **160** | **25.88** | **0.859** | **0.439** |

Wave boundaries from the wave-badge series in my 2026-08-07 note § 6.1. **Channel uptime does not decay as the ladder climbs.** The two low waves are 151 (0.648 — the opening, which contains the approach) and 155 (0.565); wave 160, the wave he died in, runs at 0.859.

---

## 4 · THE MOVEMENT-DOES-NOT-BREAK-THE-CHANNEL RESULT, and how hard I tried to break it

This is the load-bearing claim, so here is every test I ran against it.

### 4.1 Rate conditioned on class — no difference

| class | sampled dur | drain ticks | rate | gross drain |
|---|---:|---:|---:|---:|
| STATIONARY | 59.07 s | 531 | **8.99 /s** | **−190.7 /s** |
| MOVING | 101.93 s | 1,109 | **10.88 /s** | **−188.4 /s** |

### 4.2 Event-locked at movement onset — flat, with no step

38 movement onsets (episodes ≥ 1.0 s), drain-tick rate in 0.2 s bins from −1.0 s to +1.6 s relative to the onset:

```
   -1.0  -0.8  -0.6  -0.4  -0.2 | +0.0  +0.2  +0.4  +0.6  +0.8  +1.0  +1.2  +1.4
    9.68 10.94 10.31  9.88  9.05 | 10.19  8.95 10.41  9.64 12.30 13.30 11.12 10.62   /s
```
Each bin carries 6.4–7.2 s of sampled footage. **There is no edge.** A break with no re-initiation would take this to zero within one bin.

The stop-onset series (20 onsets) is equally flat: 9.03 → 9.11 → 9.38 across the edge.

### 4.3 Per-episode, including the ones that cover ground

The longest moving episodes with their net travel (screen px converted at the GAL-CAM scale, ≈53.3 px/m at mid-screen — a transfer assumption, see § 7):

| episode | dur | net travel | tick rate |
|---|---:|---:|---:|
| 721.10 | 3.15 s | **15.6 m** | 11.80 /s |
| 817.90 | 6.15 s | **13.4 m** | 9.59 /s |
| 717.80 | 2.80 s | 11.9 m | 8.34 /s |
| 702.05 | 2.60 s | 11.2 m | 10.17 /s |
| 706.70 | 1.80 s | 10.8 m | 9.23 /s |

**He crosses thirteen metres at ten drain ticks per second.**

### 4.4 The at-cap sawtooth — I suspected an artifact and tested it

64.6 % of combat time is spent at the 1594 ceiling, where the trace shows a sawtooth rather than a staircase and where a drain tick is refilled immediately. **If that sawtooth were a different mechanism, § 4.1 would be contaminated.** It is not:

| | median tick | median interval | rate | net dE/dt (stationary) | net dE/dt (moving) |
|---|---:|---:|---:|---:|---:|
| at cap (E ≥ 1560) | −14.0 | 0.0833 s | 9.96 /s | +31.4 /s | +33.6 /s |
| below cap | −13.0 | 0.1000 s | 10.59 /s | −81.7 /s | −73.4 /s |

Same tick size, same cadence, same rate. **What decides the drift is whether regeneration has caught up — and that is orthogonal to movement:** the stationary and moving columns agree to within 7 % in both rows.

### 4.5 What survives

**MEASURED:** the referent's energy expenditure runs at ~10 ticks/s of ~−13.5 each, continuously, across movement onsets, across thirteen-metre traverses, and at both energy regimes. **Whatever D-9's `MoveToAction → StopCurrentSkill` does inside the referent's process, its net effect on his channel uptime is below the resolution of a 60 Hz energy readout.**

⚑ **The most likely reconciliation, offered as a hypothesis and NOT as a measurement:** a human holding the attack button re-issues the skill the instant a move command completes, so the break fires and the channel restarts inside one frame. **If that is what happens, `G5` is not a fold of the referent's rule — it is a fold of the rule *with re-initiation removed*, which is a different control scheme.** Deciding this is legolas's seam, not mine; I can only say the energy never pauses.

---

## 5 · THE EPISODE STRUCTURE — and the question the commission actually asked

*Does he plant and channel through spawns, or kite then channel?*

### 5.1 The stop/go cadence

| | STATIONARY | MOVING |
|---|---|---|
| episodes | **86** | 85 |
| total | 68.2 s | 114.4 s |
| mean | 0.793 s | 1.346 s |
| median | 0.45 s | 0.80 s |
| p90 | 2.03 s | 2.78 s |
| max | 4.80 s | 11.00 s |
| ≥ 1 s / ≥ 2 s / ≥ 3 s | 20 / 9 / 4 | 38 / 18 / 7 |

**He stops 86 times in 182.65 s — once every 2.12 s — and the median stop lasts 0.45 s.** This is not a plant-and-hold rhythm. It is a fast, near-continuous stutter: 47 of the 86 stops are under half a second.

### 5.2 He plants at the spawn — this half of `F-11` holds

First 5 s after each wave-badge flip, against the whole-fight stationary fraction of **0.374**:

| wave | stationary, first 5 s | s to first stop ≥0.5 s |
|---:|---:|---:|
| 151 | 0.677 | 0.05 |
| 152 | 0.510 | 1.47 |
| 153 | 0.590 | 0.02 |
| 154 | 0.550 | 0.73 |
| 155 | 0.580 | 0.60 |
| 156 | 0.390 | 0.02 |
| 157 | 0.530 | 0.00 |
| 158 | 0.600 | 0.62 |
| 159 | 0.760 | 0.03 |
| **160** | **0.960** | **0.03** |

**Mean 0.615 against a fight-wide 0.374 — he is 1.6× more likely to be standing in the five seconds after a spawn than at any other time, and in nine waves of ten he is standing within 0.73 s of the flip.** He does not kite first. He plants where he is and lets them come.

**Wave 160 is the extreme of the pattern: 96 % stationary through the first five seconds** — and it is the wave that killed him, in a single blow from full health (2026-08-08 § 9, side-finding B).

---

## 6 · SECOND BOARD — sitting 1, and the finding under the finding

Same player, same build, same skill, a different arena (green cave, no purchased defenses) and much lower waves. Two 30 s windows, motion at 20 Hz, energy at 60 Hz.

| window | frac stationary | channel-active (uncorrected) |
|---|---:|---:|
| s1 waves 4–6 (831.02–861.0) | **0.731** | 0.498 |
| s1 wave 60+ (1613.23–1643.0) | **0.754** | 0.465 |
| **s2 waves 151–160** | **0.374** | 0.789 (uncorr.) / 0.838 (corr.) |

⚑ **The duty cycle is not a fixed habit — it is a pressure gauge, and it moves in the opposite direction from the intuition.** At low and mid Crucible waves he stands for three quarters of the time and channels for half of it; there is idle standing between waves and the pressure does not require him to move. At waves 151–160 his standing time **halves** to 37 % while his channel uptime **rises** to 84 %.

**The read:** as pressure climbs he does not buy safety with standing time — he buys it with movement, and he keeps the channel up while he does. Sitting 1's high stationary fraction is largely *idle*; sitting 2's low one is *displacement under fire.*

**Grade: INDICATIVE, not equal to the sitting-2 figures.** The s1 windows are not wave-segmented, the channel figure is not coverage-corrected, and the arena differs. It is a second board, not a second measurement.

---

## 7 · WHAT IS UNMEASURABLE FROM THIS FOOTAGE, AND WHY

| # | quantity | verdict |
|---|---|---|
| 1 | **Which skill the drain belongs to.** | **UNMEASURABLE.** The HUD publishes a scalar. The drain is EoR-CONSISTENT — −190/s against a published 176.4/s, a 0.083–0.100 s cadence against a 0.16 s base at 100 % attack speed, and zero occurrences in 80 s of non-combat control — but a second combat-only per-second energy sink cannot be excluded from pixels. |
| 2 | **Whether `StopCurrentSkill` fires at all.** | **UNMEASURABLE at 60 Hz.** A break followed by re-initiation inside one frame is indistinguishable from no break. § 4.5 states the consequence: it is the same either way for uptime. |
| 3 | **The input state** — whether the attack button is held, and where the cursor is. | **UNMEASURABLE.** Not on camera. The re-initiation hypothesis in § 4.5 therefore stays a hypothesis. |
| 4 | **Per-tick energy cost against the tooltip.** | **NOT DERIVED.** Measured ≈ −13.5 per ~0.09 s ≈ −150/s against a displayed 176.4/s. Reconcilable by attack speed and energy-cost reduction; I did not derive the reconciliation and do not assert it. |
| 5 | **Metres.** | **TRANSFER ASSUMPTION, named.** Every metre figure uses the GAL-CAM 2026-07-30 scale field (≈53.3 px/m at mid-screen) and assumes the eor sittings share the camera zoom of `play_test_2026-07-26`. **Pixel figures carry no such assumption; the classification uses pixels only.** |
| 6 | **Whether the sim's tick and the referent's second are commensurable.** | **OUT OF SEAM.** I report the referent in seconds of wall-clock footage. Mapping that onto the sim's 2,700 ticks is gamora's, and `F-6`'s scope rider applies to any quote of it. |
| 7 | **Sitting 1 as a like-for-like.** | **NOT EQUIVALENT** — § 6. |

---

## 8 · METHOD + REPRODUCIBILITY

| stage | tool | note |
|---|---|---|
| motion trace | `pipeline/eor_channel.py motion` | 20 Hz, 3,652 intervals; sub-pixel phase correlation, DS=2, Hann, `1/(1+6·sat)` VFX weighting |
| energy trace | `pipeline/eor_channel.py energy` | 60 Hz and 20 Hz; glyph atlas from 10 eye-read frames |
| atlas | `pipeline/eor_channel.py atlas` | same instrument family as `eor_playerhp.py`; the energy box was **located** from column runs, not inherited |
| reduction | `pipeline/eor_duty.py report` | classification, shake guard, de-speckle, episodes, per-wave, onsets, threshold sweeps |
| minimap cross-check | `pipeline/eor_channel.py minimap` | **built, then REJECTED for velocity use** — § 1.5. Kept in the module so the rejection is reproducible. |

**Artifacts** (`captures/2026-08-25-md-b4app-2-channel/`): `work/s2-motion-20hz.json`, `work/s2-energy-60hz.json`, `work/s2-energy-20hz.json`, `work/s2-duty.json`, `work/s2-channel-summary.json`, `work/ctrl-prep.json`, `work/ctrl-post.json`, `work/s1-*.json`, `work/waves.json`, `work/energy-atlas.npz`, `work/atlas-spec.json`.

**Evidence figures:** `evidence/fig-energy-vs-motion-806-826.png` and `-783-800.png` (energy trace with MOVING shaded — the drain staircase visibly does not pause at the shading edges); `evidence/validate-STATIONARY-810.25-815.05.png`, `evidence/validate-MOVING-817.90-824.05.png` (world + minimap at both endpoints); `work/energy-sheet.png` (the ×6 atlas reads).

**One defect caught and recorded rather than silently fixed:** ffmpeg's `crop` on a yuv420p source **silently rounds an odd width down** (105 → 104), which desynchronises a rawvideo byte stream and produced a 1 %-parse pilot. The box constant now carries the rule in a comment.

---

## 9 · WHAT THIS DOES TO THE RUN'S OPEN ROWS — surfaced, not adjudicated

I do not grade the sim and I do not rule on decodes. These are the rows my numbers touch, named so the seats that own them can dispose of them.

1. **`F-11` / `DR-4` / `C-B4app-7`.** `G5` is registered as *"an UPPER BOUND ON THE LOSS, NOT AN ESTIMATE"*, on the stated reasoning that *"the referent's player stops to channel; this pilot walks nearly always."* **The first clause of that reasoning is not what the footage shows.** He walks 62.6 % of the time and channels through 89.2 % of the walking. `MD-B4app-2` was raised to turn the bound into an estimate; the estimate is that **the loss `G5` models is not a loss the referent takes.** → gamora / conductor.
2. **`C-B6-1`'s sign.** B-6 refused the fold and signed it *"↑ player output — the sim keeps a buff the referent drops."* On this footage **the referent does not drop it.** The refusal was correct to refuse; its *sign* is the row that needs re-examining. → gamora.
3. **Baton row #1, *"Movement breaks the channel."*** Ranked the single highest-value row in the wave. **My measurement does not contradict the decoded rule — it contradicts the rule's consequence for a human at the controls.** If drax ships a Godot fight where movement breaks the channel *and the channel does not auto-resume on a held button*, he ships a harsher fight than Matt's, and gandalf's own conclusion — *"a human stops to channel"* — will not be true of the human it was written about. **The clause that must ride with the row is the re-initiation behaviour, and that clause does not exist yet.** → gandalf / drax.
4. **The exclusion set.** It contains no policy entry. On these numbers the policy entry it needs is **movement fraction** (86.3 % sim vs 62.6 % referent, a 1.38× over-move), **not channel uptime** — which the sim, unfolded, gets roughly right. → PM5.
5. **The pressure gradient (§ 6) is a design finding the run does not have.** Stationary time falls 0.74 → 0.37 between mid-ladder and wave 151+, while channel uptime rises 0.47 → 0.84. **The difficulty is not expressed as lost uptime. It is expressed as lost ground.** → gandalf.

---

## 10 · MIRROR VOICE

The run has spent six builds asking what the man was doing that the machine was not, and the answer everyone expected was *he stops*. The Mirror shows him stopping eighty-six times in three minutes and never once for as long as a second in the median case — a stutter, not a stance. And it shows the thing nobody expected: **the spin never stops.** Through thirteen metres of ground, through the wave flips, through the four skulls closing on him at a hundred and sixty, the little green number falls thirteen at a time, ten times a second, and does not pause when he runs.

He was not choosing between moving and killing. He was doing both, all the time, and what the waves took from him was not his uptime — it was his ground. At wave sixty he stood for three quarters of the fight. At wave one-sixty he stood for four tenths of it, and then he stood still for the last five seconds of his life, ninety-six percent of them planted, and something crossed the arena and killed him from full health in a tenth of a second.

**Ship the rule. But ship it with the hand on the button, or you will have built a fight he never fought.**

---

*galadriel, 2026-08-25. MD-B4app-2. Read-only on all source material; no engine writes; no pushes.*
