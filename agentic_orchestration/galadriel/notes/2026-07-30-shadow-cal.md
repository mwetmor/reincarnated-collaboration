# SHADOW-CAL — what the Grim Dawn fixture's own shadows measure

**Cell:** SHADOW-CAL · conductor **gandalf** (LR/presentation session, Scope 13) · **Agent:** galadriel
**Date:** 2026-07-30 · **Status:** CURRENT · **Mode:** read-only measurement; zero writes to `reincarnated-godot/`
**Source:** `/Users/admin/gd-scratch/play_test_2026-07-26.mp4` (1920×1080, 60.000 fps CFR, 6816.5 s) — the same
fixture GAL-CAM solved; camera operands consumed from `captures/2026-07-30-gal-cam/godot-spec.json`
**Evidence:** `agentic_orchestration/galadriel/captures/2026-07-30-shadow-cal/`
**Instruments:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/sc_*.py`
**Companion:** `notes/2026-07-30-gal-cam-fixture-camera.md` (same fixture, the camera this cell measures through)

---

> ## PRESENTATION GEOMETRY ONLY — ZERO SIM SEMANTICS
> Nothing here is a range, radius, hit test or damage operator. One of these
> numbers inside a sim expression is a defect.

---

## 0. VERDICT

> **The conductor's ruling is not overturned. It is not confirmed either — and
> the reason is the fixture, not the hypothesis.**
>
> Four questions were asked. **One is answered with a controlled instrument,
> one is answered in the direction that matters and refused in degrees, and two
> are CANNOT-ANSWER.** The corpus is a 1h53m play session in which **75.4% of
> keyframes have a UI panel open**, most zones are volumetric-fogged, and the
> character shadow is a **low-contrast multiplicative wash that is not visible
> without a luma stretch** (`evidence/shadow-visible-only-under-stretch.jpg`).
>
> **What did land, on two visually verified segmentations and one controlled
> whole-session statistic:** the referent's character shadow is a
> **multiplicative darkening to ρ ≈ 0.48–0.57 of the local floor**, it casts
> **up-screen and to the left**, and there is a **systematic left-dark
> asymmetry at the player across the whole session (paired-control Wilcoxon
> p = 5.1 × 10⁻⁸)**.
>
> **The single most useful output of this cell is negative and actionable:**
> a **60-second purpose-shot clip** — walk past a torch, no menus, no fog zone —
> would answer all four questions to two significant figures. This 1h53m corpus
> cannot, and no further processing of it will change that.

| confidence | on |
|---|---|
| HIGH | shadow is MULTIPLICATIVE, not a pinned-black overlay · corpus composition · the two verified ρ measurements |
| MEDIUM | the left-dark asymmetry being the shadow (paired control passed; sprite asymmetry not fully excluded) |
| **CANNOT-ANSWER** | azimuth in degrees + variance · population length ratio · torch-pass contrast curve · secondary lobe |

---

## 1. Answers to the four questions

| # | question | answer | grade |
|---|---|---|---|
| **a** | shadow azimuth constancy | **Direction: up-screen and to the LEFT** (two verified measurements at **+142.7°** and **+107.3°**; world convention +X = screen-right, +Z = up-screen). **Scene-wide left-dark asymmetry confirmed**: paired dA median **+0.0922** [95% CI +0.051, +0.132], positive in **58.5%** of 556 clean keyframes, **Wilcoxon p = 5.07 × 10⁻⁸**, sign test p = 7.7 × 10⁻⁵. **Azimuth mean + variance in degrees: CANNOT-ANSWER** (§ 5.1) | PARTIAL |
| **b** | shadow-length ratio | **CANNOT-ANSWER.** Two ground lengths measured (**4.12 m** and **4.03 m** from the figure's ground contact) but the player is a **modded werewolf** whose sprite top is confounded by a VFX plume; the height denominator is not trustworthy, and the population harvest that would have supplied upright humanoids returned zero (§ 5.2). *Our godot skylight's 1.14× has no referent number to tune against from this fixture.* | **CANNOT-ANSWER** |
| **c** | torch-pass contrast delta | **No torch-pass segment exists in this corpus** (§ 5.3). What the two verified points say, and they say it in the direction that matters: ρ = **0.482** on a floor of **81.9** luma vs ρ = **0.565** on a floor of **38.1** luma. **The shadow interior is NOT constant — it scales with the floor.** n = 2. The ratio curve: **CANNOT-ANSWER** | **CANNOT-ANSWER** (indicative n=2) |
| **d** | secondary lobe / length change | **CANNOT-ANSWER.** Requires the same torch-pass footage as (c). No segment; no measurement. Matt's "maybe the height increased slightly" is **neither confirmed nor refuted** | **CANNOT-ANSWER** |

---

## 2. What the shadow IS, where it could be measured

Two segmentations, each rendered and **judged by eye before its numbers were
kept** (`evidence/seed-3954-segmentation.jpg`, `evidence/seed-4100-segmentation.jpg`).
Both show one connected blob attached at the figure's feet and extending
up-screen-left — the shape a cast shadow has, not the shape a dark terrain
patch has.

| | t = 3954 s (Wightmire, outdoor, overcast) | t = 4100 s (cavern, torch-lit) |
|---|---|---|
| local floor luma (annulus median) | 81.9 | 38.1 |
| shadow interior luma (median) | 39.5 | 21.5 |
| **occlusion ratio ρ** | **0.482** | **0.565** |
| absolute contrast (floor − shadow) | 42.4 luma | 16.6 luma |
| ground length from contact point | 4.12 m | 4.03 m |
| **ground azimuth** | **+142.7°** | **+107.3°** |
| segmented area | 11,386 px | 8,064 px |

**The load-bearing reading.** The shadow interior tracks the floor: on a floor
**2.15× brighter**, the shadow interior is **1.84× brighter**. A shadow whose
interior were *pinned* — the mechanism the Scope-13 ruling describes as "the
shadow's darkness is ~constant" — would have shown ≈ the same 21.5 in both.
It did not.

**Consequence for the ruling, stated precisely.** The conductor's *conclusion*
(the magnification is EMERGENT, not authored) is **supported and in fact
strengthened**; the conductor's *stated mechanism* is **inverted**:

- ruling as written: *shadow darkness ~constant → surround rises → the
  shadow/surround RATIO rises → the shadow pops*
- what the fixture shows: **the RATIO is what holds (~0.5); the ABSOLUTE
  difference is what grows.** On the bright floor the shadow sits 42.4 luma
  below its surround; on the dim floor, 16.6. A 2.6× deeper hole, for free,
  with no per-torch authoring.

Both roads reach "don't author it, let it emerge". They do not reach the same
implementation note, and the difference is the one SHADOW-UNIFY has to build
against — see § 3.

---

## 3. What SHADOW-UNIFY should take, and what it must NOT take

**TAKE (measured):**

1. **A multiplicative shadow, not a darkening decal.** Target
   **ρ ≈ 0.50 of local floor luminance** (measured 0.482 / 0.565; midpoint
   0.52). In Godot terms this is what a shadow-mapped light already does when
   the *shadowed* surface still receives ambient/other lights at their normal
   strength — the thing to check is that the shadow does not clamp to a fixed
   dark value in dim rooms.
2. **The contrast magnification near the Arm-A carried light is free** and needs
   no proximity lever, **provided (1) holds.** Brightening the floor ring around
   the player automatically deepens the absolute hole under him.
3. **Cast direction: up-screen and to the left** of the judge camera, at the
   fixture's own camera orientation. Both verified samples and the whole-session
   asymmetry statistic agree on the sign.

**DO NOT TAKE:**

4. **Do not tune the DirectionalLight3D angle to a referent ratio — this cell
   does not have one.** The Scope-13 spec's *"angle set for ~1.1–1.2× shadow-length
   ratio, matching the measured skylight read"* is our own E2 number
   (`drax/notes/2026-07-30-beauty-corner.md`), not the referent's. It is a
   perfectly good number to ship; it is **not** referent-anchored, and the note
   should not later be read as if it were.
5. **Do not build the "slight height increase near torches" lever yet.** The
   Scope-13 spec already held it as optional-and-test-emergent-first. This cell
   cannot say whether the referent does it. That HOLD is now evidence-backed
   rather than merely prudent.

**Suggested acceptance check for the cell (cheap, and it is the one this cell
could actually run):** render the same figure on a bright floor tile and a dim
floor tile and require the measured ρ to agree within ~10%. That is the
falsifiable statement of (1).

---

## 4. Instruments, and the four that failed

Every instrument here had to earn its verdict on a control. Four did not, and
are committed rather than hidden.

| instrument | what it does | verdict |
|---|---|---|
| `sc_cam.py` | rebuilds the GAL-CAM pinhole as usable geometry | **PASS** — reproduces GAL-CAM's own scale field to **0.04%** (g_x 54.45 vs 54.47 px/m at the player row; 41.83 vs 41.74 at row 0; 64.72 vs 64.83 at row 1079) with none of those numbers used as input; the player anchor round-trips to (962, 595) |
| `sc_synth.py` / `sc_synth2.py` (**SC-C1/C2**) | known-truth boxes + sheared shadows through the same camera; sweeps the base/top/tip estimators | **PASS, and it changed the instrument.** Naive extremes carry **+30% height bias / −12% ratio bias**; the winning triple (base `bottom_q`, top `col_q`, tip `q99`) carries **−4.2% ratio bias, sd 9.2%, azimuth bias 0.00° rms 2.63°**. PCA azimuth **discarded** (rms 9.6°, one 90° failure) |
| `sc_plate.py` | world-registered median plate; consecutive sub-pixel registration, 47-patch quorum, temporal MAD | **PASS on its own control** — cumulative-vs-direct registration **rms 0.05–0.10 px** on good windows; correctly returned `nan` (no control points) when travel exceeded the search radius, and correctly failed loud at **rms 77–110 px** on teleport/fade windows |
| `ui_mask` (in `sc_run.py`) | finds panels/tooltips from long straight axis-aligned edges | **PASS** — clean frames 0.0001–0.0010 of pixels, open panels 0.0140–0.0220: **14× to 140× separation** |
| `sc_asym.py` (**SC-7**) | left/right ground-darkness asymmetry at the measured player anchor, with an in-frame paired control 5 m down-screen | **PASS** — synthetic control returns **+0.187 (shadow left) / −0.174 (shadow right) / +0.005 (up-screen) / +0.005 (down-screen) / +0.005 (no shadow at all)** |
| `sc_seed.py` (**SC-6**) | human names the shadow; instrument does the geometry | **PASS, on verified overlays only** — the two § 2 measurements |
| **`sc_ray.py` (SC-4)** | scene-wide azimuth from ground-plane radial darkness dipoles | **FAILED ITS OWN CONTROL, KEPT.** Positive controls returned azimuth errors of **3–28°** at resultant R **0.28–0.45**; the per-box-random-azimuth NULL returned **R 0.21–0.31**. Signal indistinguishable from null. **No number from it was used.** `evidence/FAILED-sc4-*.jpg` |
| **`sc_shadow.py` + `sc_run.py` (SC-1), `sc_walk.py` (SC-5)** | plate-based figure/shadow harvest | **ZERO YIELD, and the reason is instructive** — see § 5.2. `evidence/FAILED-sc1-firelight-read-as-shadow.jpg` |
| **`sc_player.py` (SC-8)** | automated SC-6 at the player anchor, 8 unbiased seeds | **FAILED VISUAL VERIFICATION TWICE, KEPT.** Pass 1 returned azimuth +96.0° (R 0.54, n=108) — **verification showed the blobs were the character, not its shadow** (`evidence/sc8-verification-v1-FAILED.jpg`). Pass 2 added a sprite-exclusion guard; the answer **flipped to −113.7°** (R 0.39, n=77) because the guard excludes exactly the region an up-screen shadow occupies. **An instrument whose guard determines its answer has not measured anything.** Both passes' JSON kept |

**The SC-8 episode is the cell's sharpest methodological finding.** A single
frame cannot separate "dark ground up-screen of the figure" from "the figure's
own sprite", because a screen pixel above a ground contact point unprojects to
ground *beyond* it. Any single-frame instrument that samples up-screen will
report an up-screen shadow whether or not one exists. This is why § 1(a)
refuses degrees, and why SC-7 measures **only the left/right axis** — the one
axis on which the sprite straddles its own contact point and cannot manufacture
a signal.

---

## 5. The CANNOT-ANSWER rows, with the leverage shortfall quantified

### 5.1 Azimuth in degrees

| route | why it could not deliver |
|---|---|
| single-frame (SC-4, SC-8) | the up-screen/sprite degeneracy above. Structural, not a tuning problem |
| plate-based (SC-1, SC-5) | zero figure/shadow pairs across **56 windows** — § 5.2 |
| hand-seeded (SC-6) | works, but each measurement costs a human read of a stretched view. **n = 2** at this cell's budget |

**What SC-7 does establish, and it is not nothing:** across **556** clean
gameplay keyframes spanning the whole session, the ground immediately LEFT of
the player is systematically darker than the ground immediately right,
*relative to an in-frame control 5 m away that carries the terrain's own
left/right tendencies*. Median dA **+0.0922**, positive in 58.5%,
**p = 5.07 × 10⁻⁸**.

**And the honest complication, declared:** per 700 s block the sign is **not**
constant. Block 4200–4900 s is **88.7% left-dark (p = 2.4 × 10⁻¹⁰)**; block
700–1400 s is significantly **right**-dark (**30.8% positive, p = 0.024**).
Two readings survive and this cell cannot choose between them:

- **(i)** the light azimuth genuinely differs by area — which would **contradict
  the "same azimuth, every room" half of the Scope-13 spec**; or
- **(ii)** per-zone terrain that the 5 m control does not cancel (a corridor
  wall on one side for a whole zone), diluting or reversing a constant signal.

The effect size (0.09) against the frame-to-frame spread (sd 0.33) means single
frames are dominated by terrain either way. **Routed to the conductor as an open
question, not as a refutation.**

### 5.2 Why the plate harvest returned zero — the quantified reason

A world-registered median plate can only reveal what **translates through the
world**. A figure standing still sits inside its own plate and is invisible *by
construction*. Measured consequences:

| condition | measured | consequence |
|---|---|---|
| camera static, actor idle | plate noise floor **0.43–1.06 luma** (excellent) | but only **3,963 changed px** in a whole frame — nobody moved |
| camera moving (player runs) | plate noise floor **13.4 – 38.3 luma** | change threshold rises to 47–134 luma; a 20–40 luma shadow is below it |
| cause of the second row | **parallax**: an object 3 m tall over a 28.3 m camera displaces ~11% of the camera travel; one global shift cannot register ground and scenery together | trimming travel to 3.1–3.9 m still left σ 13–24 |
| fire in frame | σ **8.2–38.3**; without the temporal-MAD floor the mask reads **flicker as shadow** — 342,139 px of false "sprite" | `evidence/FAILED-sc1-firelight-read-as-shadow.jpg` |

56 windows across `sc_batch` / `sc_harvest` / `sc_walk`; **0 verified pairs.**
Not "no shadows" — **nobody moved, or the plate was too noisy to see one.**

### 5.3 Why there is no torch-pass segment

- **1,639 keyframes** censused for warm sources. 581 keyframes carry a warm blob
  within 285 px of the player anchor — but on inspection these are overwhelmingly
  **player-attached VFX** (the werewolf's red aura, the magenta riftgate ring,
  skill fire), not world-fixed torches.
- The corpus is **Act 1 outdoors**: Burrwitch / Wightmire / Foggy Bank / Burial
  Hill / swamp. Torch-and-brazier interiors are a small minority, and in them the
  player's traversals are short and menu-interrupted.
- The one clean torch-lit frame found (t = 4100 s, cavern, torch on a pole) is a
  **single idle frame**, which is why it appears in § 2 as a point and not as a
  curve.

**This is the finding to act on.** A deliberate 60-second capture — one zone,
one torch, walk in and out twice, HUD panels closed, no fog zone — turns (c) and
(d) from CANNOT-ANSWER into two-significant-figure numbers, and would give (a)
and (b) proper n as a by-product.

---

## 6. The corpus, measured

| property | value |
|---|---|
| keyframes (1 per 250 frames = 4.1667 s) | **1,639** over 6816.5 s |
| adjacent keyframe pairs with the camera **static** | **1,392 / 1,638 = 85.0%** (bimodal and decisive: correlation peak 0.517 & MAD 8.4 static vs peak 0.023 & MAD 32.3 moving) |
| keyframes with **no UI panel open** (ui_frac < 0.0022) | **404 / 1,639 = 24.6%** |
| clean gameplay keyframes after also cutting loading screens and near-black frames | **556** |
| scene luma (gameplay band) | mean 47.6, range 16.5 – 125.2 |

The session is mostly **standing still with a panel open**. That single fact is
why every automatic route in this cell starved.

---

## 7. Reproducibility

Every number regenerates from the committed scripts plus the source MP4:

```
sc_grab.py sc_burst.py     frame + burst extraction
sc_survey.py sc_static.py  keyframe census; camera-static classification
sc_cam.py                  the GAL-CAM pinhole as geometry (+ its self-check)
sc_plate.py                world-registered plate, quorum registration, temporal MAD
sc_shadow.py sc_run.py     shadow/sprite separation; UI + debug-label masks
sc_batch.py sc_harvest.py sc_walk.py   the three harvest strategies (all zero-yield)
sc_synth.py sc_synth2.py   SC-C1 / SC-C2 estimator controls
sc_ray.py sc_ray_control.py            SC-4 (failed, kept)
sc_asym.py                 SC-7 left/right asymmetry + paired control
sc_seed.py sc_view.py      SC-6 seeded measurement + stretched view
sc_player.py               SC-8 (failed twice, kept)
```

Intermediate frame caches (~1.5 GB of JPEG bursts and keyframes) are gitignored
and exactly regenerable; the extraction commands are in that `.gitignore`.
Banked JSON: `sc7-asymmetry-clean.json`, `synth-control-sc-c1.json`,
`synth-control-sc-c2.json`, `FAILED-sc8-v1-pass.json`,
`FAILED-sc8-v2-guarded.json`.

---

## 8. Mirror

The Mirror was asked which way the light falls in another man's world, and it
found that the world had its back turned. An hour and fifty-three minutes of
play, and three quarters of it is a man reading his own inventory.

But the shadow was there, under the stretch — not a black shape laid on the
ground, a thinning of it. Half the light, wherever the light was. Carry it into
a bright room and it deepens on its own; carry it into a dark one and it almost
forgives. Nobody had to author that. It is what a shadow is.

What the Mirror could not show is the one thing Matt saw and asked about: the
torch passing. He walked past that fire once, and looked at it, and remembered
it — and the recording kept every menu he opened and not one clean second of it.
