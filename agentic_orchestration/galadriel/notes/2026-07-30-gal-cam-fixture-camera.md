# GAL-CAM — the effective camera of Matt's Grim Dawn play-session footage

**Cell:** GAL-CAM · conductor **gandalf** (presentation session) · **Agent:** galadriel
**Date:** 2026-07-30 · **Status:** CURRENT · **Mode:** read-only measurement; no godot/engine writes
**Source:** `/Users/admin/gd-scratch/play_test_2026-07-26.mp4` (1920×1080, 60.000 fps CFR, 6816.5 s)
**Evidence:** `agentic_orchestration/galadriel/captures/2026-07-30-gal-cam/`
**Instruments:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/gc_*.py`
**Companion:** `notes/2026-07-29-wr1-gal3-death2-range.md` (same fixture) — § 7.1 revises its scale anchors

---

> ## PRESENTATION CAMERA ONLY — ZERO SIM SEMANTICS
> These operands place a virtual camera. They change no range, radius, hit test
> or damage operator. One of them inside a sim expression is a defect.

---

## 0. VERDICT

> **Pinhole, not orthographic** — the assumption every earlier cell made. Ground
> scale grows **55%** top-to-bottom of frame.
>
> **Pitch ≈ 53°. 54.5 px/m at the player's row. Player anchored 55 px below frame
> centre = 1.27 m of ground.**
>
> **Decision surface ±17.6 m across, +15.2 m up-screen, −7.0 m down-screen** —
> asymmetric, not square.
>
> **The 12 m nova reach does not fit — 30% of that ring was never on screen.**

| confidence | on |
|---|---|
| HIGH | pinhole-not-ortho · scale · horizontal extent |
| MEDIUM | absolute pitch (one assumption, § 6.2) |
| MEDIUM-LOW | the far (up-screen) extent |

---

## 1. Per-row results

| # | Quantity | Value | 95% band | Method | Grade |
|---|---|---|---|---|---|
| 1 | **Pitch** | **52.96°** | [45.3, 62.3]° | row 1a ÷ G, with the principal row assumed (§ 6.2) | MEASURED (assumption-dependent) |
| 1a | axis ratio g_y/g_x at the player's row | **0.816** | [0.736, 0.912] | two independent anchors that share no input, § 3 | MEASURED |
| 1b | k = sin(pitch) | 0.798 | [0.717, 0.890] | as row 1 | MEASURED |
| 1c | pitch from a nova ground-circle ellipse | — | — | only 2 of 16 lances trackable; the fan is one-sided (`look-sheet.jpg`). A 24°-wide pair cannot pin an axis ratio | **CANNOT-ANSWER** |
| 2 | **Scale g_x at the player's row** | **54.47 px/m** | [52.5, 56.5] | nova rectified against the measured horizon; 14 m/s known from the `.arz` | MEASURED |
| 2a | g_y at the player's row | 44.44 px/m | [41.3, 48.4] | row 2 × row 1a | MEASURED |
| 2b | g_x at frame top (row 0) | 41.74 px/m | ±5% | g_x = A·(y − y_h), § 1.1 | MEASURED |
| 2c | g_x at frame bottom (row 1079) | 64.83 px/m | ±5% | ditto | MEASURED |
| 2d | GAL-3's banked 62.8 / 63.4 px/m | **superseded** | — | both assumed ortho + k = 0.72; k at that lance's row is really 0.87. See § 7.1 | REVISED |
| 3 | **Horizon row y_h** | **−1950** | [−2500, −1500] | three routes on the grid motion field, § 2 | MEASURED (systematic-limited) |
| 4 | **Player screen anchor** | **(962, 595)** px | ±10 / ±20 px | median-stack over running windows + registration residual | MEASURED |
| 4a | offset from frame centre (960, 540) | **(+2, +55) px** | — | = (+0.04 m, −1.27 m) of ground; below centre, as folklore says, but now measured | MEASURED |
| 5 | **Zoom drift** | **none detected** | ±10% floor | § 8, two indicators | MEASURED (null) |
| 6 | Camera roll | **0** | ±3° | conic cross-term on the pan cloud | MEASURED (null) |

### 1.1 The scale field — the operand, in full

```
g_x(y) = A · (y − y_h)        A = 0.021404    px per metre of ground-X
g_y(y) = C · (y − y_h)²       C = 6.861e-06   px per metre of ground-Z
y_h = −1950     px0 = 960     player ground anchor (962, 595)
```

| screen row | g_x px/m | m per px across | m per px up-screen |
|---|---|---|---|
| 0 (top) | 41.74 | 0.0240 | 0.0383 |
| 595 (player) | 54.47 | 0.0184 | 0.0225 |
| 1079 (bottom) | 64.83 | 0.0154 | 0.0159 |

---

## 2. Orthographic is rejected

Horizontal pan ratio between rows, same camera motion. Ortho predicts 1.000.

| screen row | ρ_x vs row 470 (clean columns) | ortho rejected? |
|---|---|---|
| 190 | 0.9114 | **YES** |
| 330 | 0.9575 | **YES** |
| 470 | 1.0000 | reference |
| 610 | 1.0484 | **YES** |
| 750 | 1.1112 | **YES** |

| | |
|---|---|
| n per row | 1,582–1,584 frame pairs, 73 windows; boot-95% CIs exclude 1.000 at every non-reference row |
| clean columns | grid x = 430/650/1290. Columns 870/1090 dropped: they hold the player sprite and its screen-locked dev label, and register at exactly (0,0) |
| linearity | **rms 0.0054** across the five rows — the pinhole prediction — reaching zero at y_h = −2400 (`evidence/calib-horizon.jpg`) |

| horizon route | what it uses | n | median y_h | boot-95% |
|---|---|---|---|---|
| divergence: (∂Δx/∂x′)/Δy = 1/(y−y_h) | field shape only — scale, pitch and camera motion all cancel | 8,438 | −1491 | [−1512, −1468] |
| sqrt(Δy) linear in row | Δy ∝ G² | 1,460 | −2051 | [−2117, −2003] |
| \|Δx\| linear in row | Δx ∝ G | 1,582 | −2393 | [−2508, −2305] |

**Systematically disagreeing by ±25%.** Adopted −1950, band [−2500, −1500].

---

## 3. Two independent anchors on the axis ratio

| anchor | what it measures | independent of | result |
|---|---|---|---|
| **A — pan-episode ellipse** | 85 steady-run episodes over 1h53m; constant ground run speed traces the ground-scale ellipse | the nova entirely, all skill data, the ring centre, the launch frame | 0.816 (row 400) · 0.804 (row 700) · 0.829 (row 820) |
| **B — rectified nova** | 2 lance tracks + the known 14 m/s, rectified against y_h | player movement, run speed, any isotropy assumption | **0.816** at the player's row |

Agreement **≈1%**, sharing no input.

| check | prediction | measured | verdict |
|---|---|---|---|
| **free check** — A and C were solved from projectile SPEED alone; the ring is 16 rays at 22.5°, so implied ground azimuths must differ by a multiple of 22.5° | multiple of 22.5° | separation −24.44°, residual **−1.94°** [−5.8, +1.4] | PASS — nothing was fitted to make this land |
| **model check** — rectified coordinates must be linear in frame number though the screen tracks are visibly curved | linear | rms **0.45% / 0.98%** of span (28-frame lance); 2.1% (10-frame lance) | PASS (`calib-rectify.jpg`) |
| **roll** — conic cross-term on the pan cloud | 0° | +3.1° | PASS once the small perspective shear is allowed |

---

## 4. The decision surface

| surface | definition |
|---|---|
| **FRUSTUM** | what the projection put on the display |
| **DECISION** | frustum minus opaque HUD (rows < 60 boss plate, rows > 950 globes + skill bar) — ground under the skill bar was in nobody's decision |

| | FRUSTUM | 95% | DECISION | 95% |
|---|---|---|---|---|
| left (−X) | −17.67 m | [−18.4, −17.0] | **−17.66 m** | [−18.4, −16.9] |
| right (+X) | +17.57 m | [16.9, 18.3] | **+17.57 m** | [16.9, 18.3] |
| far (up-screen, +Z) | +17.42 m | [15.0, 20.5] | **+15.21 m** | [13.1, 17.9] |
| near (down-screen, −Z) | −9.17 m | [−10.5, −8.0] | **−7.02 m** | [−8.2, −6.0] |
| half-width at the far edge | 22.98 m | [21.4, 24.8] | 22.29 m | [20.9, 23.9] |
| half-width at the near edge | 14.79 m | [14.0, 15.6] | 15.45 m | [14.7, 16.2] |

**Box: ±17.6 m horizontal · +15.2 m far / −7.0 m near**, at the player's own row
— the honest reading of "within X metres of me".

| sanity floor | horizontal | far | near |
|---|---|---|---|
| pinhole (adopted) | ±17.6 m | +17.4 m | −9.2 m |
| orthographic solve of the same two lances | ±15.7 m | +11.8 m | −9.6 m |
| **difference** | 12% | **48%** | 4% |

**The far side is the operand CAM-LOCK should treat as least settled.**

---

## 5. Sim fight geometry against the measured surface

| sim quantity | metres | px across | px up/down | fits L | fits R | fits FAR | fits NEAR |
|---|---|---|---|---|---|---|---|
| nova reach (`primordian_frigidring`) | 12.0 | 653.7 | 536.0 | ✔ | ✔ | ✔ | **✘** |
| nova explosion radius | 1.5 | 81.7 | 67.0 | ✔ | ✔ | ✔ | ✔ |
| melee separation | 1.6 | 87.2 | 71.5 | ✔ | ✔ | ✔ | ✔ |
| death-2 measured range (GAL-3) | 1.26 | 68.6 | 56.3 | ✔ | ✔ | ✔ | ✔ |

Ground ring centred on the player:

| ring radius | far edge at row | near edge at row | % inside frame | % inside play area |
|---|---|---|---|---|
| 1.6 m | 526 | 668 | 100.0 | 100.0 |
| 5.0 m | 391 | 838 | 100.0 | 100.0 |
| 8.0 m | 283 | 1008 | 100.0 | **84.0** |
| 10.0 m | 217 | 1133 | 86.8 | **74.9** |
| **12.0 m** | **154** | **1270** | **77.6** | **69.9** |

The 12 m reach overruns the frame by **191 rows** near-side.

---

## 6. Godot operands for CAM-LOCK

Monte-Carlo over every measured input, n = 40,000.

| operand | median | 68% | 95% |
|---|---|---|---|
| pitch below horizontal | **52.95°** | [49.0, 57.4] | [45.3, 62.3] |
| vertical FOV | **31.8°** | [26.7, 38.2] | [22.8, 46.4] |
| horizontal FOV (16:9) | **53.7°** | [45.7, 63.2] | [39.5, 74.7] |
| camera → look-at distance | **35.6 m** | [29.2, 42.7] | [23.7, 50.1] |
| camera height above the ground plane | **28.3 m** | [24.2, 32.9] | [20.6, 36.8] |
| player offset from look-at, along-ground | **−1.27 m** (nearer camera) | [−1.34, −1.20] | [−1.43, −1.13] |
| player offset from look-at, lateral | +0.04 m | — | [0.035, 0.038] |

| recommendation | |
|---|---|
| trust directly | pitch, and the two ground offsets |
| treat as a **coupled pair** | FOV ↔ distance — they trade along the y_h uncertainty; the pair reproducing the § 1.1 scale field matters more than either alone |
| validate by | rendering 5 m and 12 m ground rings and checking their screen rows against § 5 — far tighter than matching FOV |

### 6.1 Pitch sensitivity — it cancelled for GAL-3, it does not cancel here

GAL-3's 42% k-swing moved the death-2 range **2%** — offset and calibrating lance
shared an azimuth, so k cancelled. That belongs to a **ratio**; it does not
survive camera reproduction, where k appears alone.

| axis-ratio input | pitch | vertical FOV | camera distance | camera height |
|---|---|---|---|---|
| 0.771 (−5.5%) | 48.97° | 27.99° | 40.7 m | 30.7 m |
| **0.816 (adopted)** | **52.97°** | **32.08°** | **35.2 m** | **28.1 m** |
| 0.861 (+5.5%) | 57.39° | 37.46° | 29.9 m | 25.2 m |

**±5.5% on the axis ratio → ±4.4° pitch, ±17% FOV, ∓15% distance.** A 2% nuisance
for range; the dominant term here.

### 6.2 The one assumption

| assumption | why | sensitivity | what depends on it |
|---|---|---|---|
| principal row = 540 (viewport centre) | normal convention for a full-viewport game render | rows 500→580 move k by ±0.7% | **pitch and FOV only** |

§ 4 is **independent** of it: (A, C, y_h) fix the ground-metre field alone.

---

## 7. Secondary recoveries

### 7.1 GAL-3's scale anchors are superseded; its verdicts are not

| | GAL-3 | GAL-CAM | change |
|---|---|---|---|
| death-2 separation at the damage frame | 1.257 m | **1.390 m** | +10.5% |
| inside 1.804 m? | YES | **YES** | unchanged |
| inside 3.919 m? | YES | **YES** | unchanged |
| in the 2.50–3.919 m window? | NO | **NO** | unchanged |
| P(r ≥ 5.0 m) | 0.0% | 0.0% | unchanged |

Re-derived from GAL-3's own endpoints. **Every threshold verdict survives** —
1.390 m is 23% inside the ≤ 1.804 m window M-12b rests on, and inside GAL-3's own
[0.96, 1.61] band. The estimate moves; nothing concluded from it moves.

### 7.2 Two instruments failed, and are kept

| instrument | failure | cause, found by looking |
|---|---|---|
| `gc_fit.py` — global pinhole fit to nova head **positions** | rms 35 px; returned k = 0.39 against GAL-3's 0.72 | the cold blobs ride the projectile **trails**, not the heads (`look-309104.jpg`). A position fit was fitting a smear |
| `gc_panfit.py` — envelope-percentile ellipse per band | failed its own built-in check: axis ratio varied 0.28–0.86 across speed percentiles; roll returned 47–66° | the reference band contained the player and the screen-locked dev label and registered at exactly (0,0) |

Kept legible per GAL-3 precedent. Neither number was used.

### 7.3 CANNOT-ANSWER rows

| question | verdict | why |
|---|---|---|
| pitch from a nova ground-circle ellipse | **CANNOT-ANSWER** | 2 usable lances, 24° apart. See row 1c |
| horizon row from the nova alone | **CANNOT-ANSWER** | the long lance spans rows 673→831, over which G changes only **6.1%**; the grid instrument spans 190→750, **26.8%**. Lance-track curvature is consistent with anything from y_h = −1400 to orthographic. Not a contradiction of § 2 — a leverage shortfall, quantified |
| attribute the one elevated drift window to zoom vs movement speed | **CANNOT-ANSWER** | pan magnitude cannot separate them; the horizon row stayed flat through that window, which argues against a lens change without proving it |

---

## 8. Zoom band

| indicator | across the session | reading |
|---|---|---|
| direction-corrected pan p90, 12 chunks | 6.69–8.20 px/frame in 9 of 10 live chunks; one chunk 9.91 | flat to **±10%** |
| pan-episode ellipse semi-axis, 3 chunks with enough episodes | 6.76 / 7.50 / 7.82 | spread 14%, inside sampling noise (n = 12–22 episodes) |
| horizon row per chunk, 6 chunks | −1533 to −1742 | spread 13%, flat |
| dead chunks 1823–2364 s, 5609–6150 s | player stationary | instrument **void**, not zero |

**Operand = the modal value, g_x 54.5 px/m at the player's row. Band = context,
±10%, the detection floor, not a measured drift.** A dolly zoom moves scale only;
an FOV zoom moves both. Neither moved.

---

## 9. Evidence index

| artefact | path under `captures/2026-07-30-gal-cam/` |
|---|---|
| visible-box overlay, ground rings on a representative frame | `evidence/surface-overlay.jpg` |
| calibration — rectification straightens the curved lance tracks | `evidence/calib-rectify.jpg` |
| calibration — ortho rejected; g_x linear in row; the horizon | `evidence/calib-horizon.jpg` |
| the mask look that overturned the position fit | `evidence/look-309104.jpg` |
| one-sided fan across the nova lifetime | `evidence/look-sheet.jpg` |
| player anchor — median stacks at 3 session points | `evidence/anchor-zoom.jpg` |
| player locus — registration residual | `evidence/player-locus.jpg` |
| HUD occlusion extents | `evidence/hud-bottom.jpg`, `evidence/hud-top.jpg` |
| solved camera, free check, sensitivities | `ring.json`, `ring-boot.json` |
| decision surface with Monte-Carlo bands | `surface.json`, `rings.json` |
| Godot operands | `godot-spec.json` |
| horizon routes · drift | `geom.json` · `drift.json` |
| failed instruments, kept | `camfit-p960-540.json`, `panfit.json`, `hodo.json`, `cam.json` |

| instrument | purpose |
|---|---|
| `gc_heads.py` | full-frame nova head census (GAL-3's window clipped the mature ring) |
| `gc_look.py` | render mask + detections before believing any fit |
| `gc_fit.py` | global position fit — **failed**, kept |
| `gc_hodo.py` | nova hodograph — under-determined, kept |
| `gc_pan.py` · `gc_panfit.py` · `gc_cam.py` | banded camera pan; percentile ellipse — **failed**, kept |
| `gc_grid.py` · `gc_geom.py` | grid motion field; three horizon routes |
| `gc_lance.py` | per-lance tip tracks with an alive-window gate |
| `gc_ring.py` | rectified nova solve for A and C, plus the 22.5° free check |
| `gc_surface.py` | decision surface with Monte-Carlo bands |
| `gc_overlay.py` | draw the solved camera back onto the footage |
| `gc_drift.py` · `gc_anchor.py` · `gc_hud.py` | zoom drift; player anchor; occlusion |

Every number regenerates from the committed scripts plus the source MP4. The
three raw motion dumps (~17 MB) are gitignored, exactly regenerable, commands in
that `.gitignore`.

---

## 10. Mirror

Every cell before this saw a flat map — one scale, the same everywhere. The
Mirror found a horizon in it, 1,950 rows above the frame, off in the dark where
nothing is drawn, bending everything.

And the ring he died inside did not fit. Its near arc ran off the bottom of the
display, under the skill bar, into nothing. The sim knew where the edge of the
nova was. The camera never showed him.
