# BV2F lane PH — the v1-parity harness, calibrated (Phase 0 task 0.4)

**Lane:** PH (galadriel). **Charter:** BV2F v0.3 (§ 9, § 12 Gate-1 folds, § 13 Gate-2 folds). **Status:** Phase 0 CLOSED (Gate-2 PASS-WITH-FOLDS, R-C9-173); the folds are recorded in § 11. Rulings R-C9-167 through R-C9-171 are folded in §§ 7–10. v1 passes every measured row. R-C9-159 fails P1–P4, P6b and P8. R-C9-158 fails P5 and P9. Every row has a constructed failure that reads RED. **P6a binding = fallback (a), conductor triage by eye with the layout overlay (§ 10, § 11). P11 = ABX, binding (R-C9-171); v1 GREEN confirmed (R-C9-175, § 12).**
**Machine-readable:** `calibration.json`. **Harness + run commands:** `harness/README.md`. **Per-row evidence:** `results/*.json`.

Rule applied throughout: thresholds come from v1's own distribution; a quality row that cannot separate v1 from its
negative control is **re-instrumented or discarded, never threshold-tuned**; every row shows a constructed failure.

## 1. The table

`value **verdict**` per cell. "—" = not applicable or not measured (§ 4).

<!-- CALIBRATION-TABLE -->
| Row | Kind | Negative control | Threshold | v1 | R-C9-159 | R-C9-158 | Constructed fail | Other |
|---|---|---|---|---|---|---|---|---|
| P1 | quality | R-C9-159 | ≤ 1.05 on every static surface | 1.0 **PASS** | 4.353 **FAIL** | 1.0 **PASS** | 2.0 **FAIL** | — |
| P2 | quality | R-C9-159 | 100% | 1.0 **PASS** | 0.1818 **FAIL** | 1.0 **PASS** | 0.9643 **FAIL** | constructed_foreign: 0.9643 **FAIL** |
| P3 | quality | R-C9-159 | ≤ 15.5 for every class | 13.57 **PASS** | 107.97 **FAIL** | — | 25.38 **FAIL** | — |
| P4 | quality | R-C9-159 | each ≤ v1's own leave-one-chunk-out maximum (snow hist 0.281 / spec 0.097; rock 0.481 / 0.190; ice 0.126 / 0.031) | 0 **PASS** | 28 **FAIL** | — | 16 **FAIL** | constructed (patchwork): 0 **PASS** |
| P5 | quality | R-C9-158 (Gate-1 W-1) | (a) ≤ 13.09; (b) ≤ 0.799 | 13.09 / 0.799 **PASS** | 6.87 / 0.891 **FAIL** | 15.29 / 1.274 **FAIL** | 14.07 / 1.250 **FAIL** | — |
| P6 | quality | R-C9-155 BVR blocks (invention, Gate-1 W-1); R-C9-159 (silhouettes) | (a) inventions = 0, T = 32 (v1's own ceiling); (b) ≥ 0.513 (v1 median) | 0 inv / IoU 0.513 **PASS** | IoU 0.102 **FAIL** | — | 1 inv / IoU 0.290 **FAIL** | BVR hall (T2a, 7_5..8_7): 18 inventions **FAIL**; BVR barrow door (T2b, 4_0..6_1): 0 inventions **PASS** |
| P7 | constraint | constructed (RED) | floor ≤ v1 quadrant max (tuft 0.0040, clutter 0.0013); lanes ≤ v1 segment max (tuft 0.0245, clutter 0.0793) | 0.0019 / 0.0005 **PASS** | 0.0006 / 0.0002 **PASS** | — | 0.0219 / 0.0125 **FAIL** | — |
| P8 | constraint | constructed (RED, graded) | every chunk with heather (≥ 2000 drawn px) ≥ 0.4476 = v1's minimum chunk | min 0.4476, 0/15 below **PASS** | min 0.0009, 6/6 below **FAIL** | — | min 0.4119, 3/15 below **FAIL** | — |
| P9 | constraint | R-C9-158; constructed (RED) | (a),(b) ≥ 3× noise and ≥ 0.25× v1 heather sway (2.06); (c) ≤ 0.25 px; (d) ≥ 0.99 | sway 8.26; trail 1.00 **PASS** | sway 13.06; flow 6.48; drift 1.913 px; trail 0.81 **FAIL** | trail 0.00; no SnowField, no wind, static sea **FAIL** | sway 0.00 (v1, wind held); flow 0.206 (159 sea, motion layers hidden) **FAIL** | — |
| P10 | constraint | constructed (RED) | ≤ 16.7 ms | 14.87 **PASS** | 13.55 **PASS** | — | 21.33 **FAIL** | — |
| P11 | quality | R-C9-159 | ABX accuracy ≤ 65% (≤ 26/40); judge void if repeat inconsistency > 25% | ABX 55% (inconsistency 10%) **PASS** | ABX 100% (inconsistency 0%) **FAIL** | ABX 90% (inconsistency 10%) **FAIL** | ABX 92% (inconsistency 0%) **FAIL** | constructed (G2, fixed generator): ABX 82% (inconsistency 20%) **FAIL** |
<!-- /CALIBRATION-TABLE -->

## 2. Thresholds and their v1 sources

| Row | Threshold | v1 source |
|---|---|---|
| P1 | every static surface ratio ≤ 1.05 | play camera PPM 100.6176 (`barrow_full.gd` cam.size = rows/PPM); v1 painting 5376 px over u −28.715..24.715 = 100.6176 px/m; v1 bakes from the painting through the game camera (`bake_heroes.py:28,45`), seen-texel density ≥ painting (`take/build/bake_report.json`) |
| P2 | 100% of static textures resolve to the painting sha | `godot/data/painted/manifest.json`, `take/take_report.json` painting sha `eecb4266…`, plates = painting crops (pixel-exact) |
| P3 | ≤ 15.5 per class | `take/build/mini_overlay.json` summary unlit 15.5 (lit 40.7) |
| P4 | ≤ v1's leave-one-chunk-out maximum per class and statistic | v1's 16 paint chunks |
| P5 | overlap MAD ≤ 13.09; seam \|log2\| ≤ 0.799 | v1's 24 canvas overlaps (reproduces the recorded 2.7–13.1) and 6 stitched seams |
| P6 | inventions = 0 at T = 32; IoU ≥ 0.513 | T = largest L* at which v1's painting shows no undeclared opening (sweep 16–40: 0 through 32, 1 at 33); v1 per-piece IoU median over 53 pieces |
| P7 | floor ≤ v1 quadrant max; lanes ≤ v1 segment max | v1 arena disc (r 7 m) quadrants; v1 path + door corridor in 2 m segments |
| P8 | per chunk: every chunk with heather ≥ 0.4476 (v1's minimum chunk; R-C9-169, like-for-like W-3) | `take/build/overlay_check.json` per_chunk, 16 chunks 0.4476–0.5783; reproduced exactly by PT (`fid/pc/results.json` T3) and by PH |
| P9 | sway ≥ 3× noise and ≥ 0.25× v1; flow ≥ 3× noise; floe drift ≤ 0.25 px; trail coverage ≥ 0.99 | v1 in-engine pair; v1 SnowField covers 100% of its floor |
| P10 | p99 ≤ 16.7 ms | plan § 4 P10 (the 10.9–12.4 ms target is withdrawn, W-2) |
| P11 | ABX accuracy ≤ 65% (≤ 26/40); judge void if repeat inconsistency > 25% | plan § 4 P11; R-C9-168/171; power (n = 40): P(pass) = 0.98 at p = 0.50, 0.79 at 0.60, 0.56 at 0.65, 0.30 at 0.70, 0.10 at 0.75, 0.02 at 0.80 |

## 3. Discarded and re-instrumented

**Discarded.**
- **P4 (3) cellularity** (spectral peak excess, 6–20 px). It cannot see a constructed failure built the way R-C9-159's bakes were built: a patchwork of 12 px Voronoi cells drawn from four offset copies of v1's own painting. On rock windows that scores p95 0.417, against v1 rock's own 0.402 and a bar of 0.681. A ±15% tone stamp scores 0.391. R-C9-159's bakes do score higher (medians 0.30–0.52, against 0.11 for v1's bakes), but an instrument that cannot see its own constructed failure decides nothing. The score is still computed and reported, and it is non-binding. **Consequence:** the harness has no binding instrument for cellularity. P4 still fails R-C9-159, on Lab histogram and spectrum shape, and P11 is the remaining perceptual guard.
- **P9b film instrument** (registered water-vs-snow residual on walk and pan films). It cannot separate R-C9-159's animated sea (median ratio 1.71–1.82) from R-C9-158's static sea (1.38): the film compression and the pans drown the signal. The in-engine static pair is binding in its place.

**Re-instrumented.**
- **P6a.** The first instrument used unsmoothed L* < 25 with a 20 px opening. It found only the declared door in the BVR hall: 1 opening, 0 inventions, so it could not see R-C9-155. It was re-instrumented to L* on a 0.1 m Gaussian, because a door interior is textured (planks, smoke, embers). T = 32 is computed from v1 alone, with a 0.2 m opening and ≥ 0.5 m². It flags both invented features of the R-C9-155 hall (§ 9 truth: plate (10311, 4925) and the gable-end opening at items 08/11), plus 15 material flags (`figures/p6a_bvr_hall_flags.jpg`).
- **P5 constructed input.** A 12 px half-frame shift is invisible to (b): it scores 0.772 against a bar of 0.799. v1's partition-of-unity stitch cannot make a hard seam, so the constructed input is now a 6 px misregistered blend, which is the stitch's ghosting failure. It scores (b) 1.250. Measure (a) carries the hard and second-hand cases.

**Known false-positive mode (P6a).** The detector also flags 15 dark material candidates in the BVR hall (§ 9 truth), since v1 contained no dark material. Their disposition is triage by eye (§ 10, § 11).

## 4. What each control is, and what is still pending

- **Negative controls per row (W-1):**
  - P1–P4 and P11: R-C9-159.
  - P5: R-C9-158 (`section_sw` canvases BVSW-*).
  - P6a: the R-C9-155 BVR re-test-2 blocks (`artifacts/BVR-*`). Declared openings come from **layout v5** (git `b267b9b00`), the layout those blocks were painted from. It is copied to `inputs/`.
  - P6b: R-C9-159 silhouettes.
  - P9: R-C9-158.
- **Godot measurements done:**
  - P3 v1 reproduces its record: stones 11.38 (recorded 11.26), kit 13.57 (13.53), projected classes ≈ 0.
  - P9 in-engine pairs: v1 sway 8.26 against noise 0.003; with the wind held, 0.00.
  - P10: v1 p99 14.87 ms; the 20 ms burn gives 21.33 ms.
- **P10 for R-C9-159 is informational only** (P10 is a constraint row): p99 13.55 ms, PASS.
- **P9c floe UV drift has a RED** (R-C9-159, 1.91 px median over 5 floes) **but no positive control.** v1 has no floes, and no rest-pose implementation exists yet. DEV-5's first build will be its positive control.
- **P8** is final (§ 8, § 11 W-3).
- **P11** is ABX, binding; the calibration sets are judged (§ 10). The v1 GREEN sets (G2-B2) are built and await judges (§ 11).
- **v1 stills:** P11 uses `section_v1cam/v1ref/V1_*.png` (record time) and PT's `fid/pc/v1_stills/` (HEAD). `barrow_full/captures/still_*.png` are **blockout** stills and are excluded; I checked them by eye.

## 5. State

See `../RESUME_PH.md`.

## 6. For the conductor to rule

All six items raised at the first hand-back are RULED (R-C9-167 to R-C9-171, §§ 7–10). One standing note: P5 also flags R-C9-159's stitched seams (2 over v1's ghosting bar). P5's negative control is R-C9-158, so this is evidence, not calibration.

## 7. Conductor rulings R-C9-167 and R-C9-168, folded

**R-C9-167 (1) Cellularity: the discard STANDS.** The cellular-bake defect is guarded by three rows:
- by **cause**: P2's lineage chain. A bake painted from a separate model sheet cannot resolve to the painting's sha, so R-C9-159 reads 18%.
- by **statistics**: P4's Lab histogram and spectrum shape. R-C9-159 fails 28 class × chunk samples.
- by **eye**: P11.

The cellularity score is still computed and reported in `results/p4.json` as `cellularity_pass_DISCARDED_non_binding`. It is non-binding.

**R-C9-167 (2) P6a re-instrumentation: acceptance NOT MET. This is a HALT for a ruling.** The conductor's priors are implemented in `harness/p6_geometry.py`: `openings(prior=…, dark_mask=…)`, `zonemap_dark_mask()` and `r167_variants()`. They are:
- a door-shape prior: projected height ≥ 1.8 m and h/w ≥ 0.8;
- a lighter-frame prior: the ring 0.1–0.3 m around the blob, median L* minus interior mean ≥ 0.5 × v1's own door contrast, 23.9, so ≥ 11.9 (fixed before scoring);
- a wall/ground surface hook: a mask from an ID render. BVR has no ID render, so the hook is unused here;
- a known-dark-class hook. The class map for BVR is the zone map the blocks were painted from (`paint/barrow_v2_zonemap.png`, 08:48). Its hall, porch, gable and palisade marks are footprints, so each is extruded up-screen by its layout-v5 height as a stand-in for the ID render.

T stays at 32. Each variant was scored on v1, on the stamped doorway, and on both BVR blocks:

| Variant | v1 inventions | stamp | invented door (10311, 4925) flagged | other hall flags | BVR barrow | acceptance |
|---|---|---|---|---|---|---|
| C0 v0.1 (no prior) | 0 | 1 | yes | 17 | 0 | not met |
| C1 shape prior (h >= 1.8 m, h/w >= 0.8) | 0 | 1 | yes | 13 | 0 | not met |
| C1F shape + lighter frame (>= 11.9) | 0 | 1 | **no** | 8 | 0 | not met |
| C2 shape + dark structures (hall/porch/gable/palisade, extruded) | 0 | 1 | **no** | 0 | 0 | not met |
| C4 C2 + ash ground dark | 0 | 1 | **no** | 0 | 0 | not met |

**Why no combination meets it.** The invented door and the charred timber are the same thing to every prior on the list:
- **Location.** All 17 candidates lie inside the burnt hall's screen region, the invented door included. It is painted on the hall's west wall, which is exactly why it is an invention. A dark-class mask over the charred structure therefore removes the defect together with the timber.
- **Shape.** The shape prior removes 4 timber flags; 13 remain.
- **Frame.** The invented door's frame contrast is 11.8. The 13 timber blobs that pass the shape prior read 9.0–17.5, so the door sits inside their range. Its frame is open dark door-leaves and charred wall, not a lighter surround.

Any threshold that keeps the door and drops the timber would be fitted to this one negative. The binding detector therefore stays **v0.1**, unchanged: it fails BVR correctly and passes v1, with 17 false flags on a burnt hall. The priors remain in the code, off by default.

Options for the ruling:
- **(a)** Keep v0.1 and triage flags inside declared charred structures by eye at the per-chunk QA step.
- **(b)** Make the invention check judged: a fresh blind judge counts openings per chunk against the layout's declared count. This is the same mechanism as P11.
- **(c)** In Phase 1 and later, rely on the ID render. The hall becomes a real model with exactly one declared door, so a dark opening on its ID silhouette that is not at the declared door is an invention. Charred timber that the model actually has also lies on the silhouette, though, so (c) faces the same ambiguity unless the model's own unlit ID-render shading supplies the reference.

**R-C9-167 (3) P4 new classes, mapped to v1. ADVISORY in Phase 2 W-B; BINDING in Phase 3 against the M2-passed W-B chunks' own distribution.**

| New class | v1 reference | Bar |
|---|---|---|
| wood | v1 lintel, posts and logs, pooled | piece bootstrap over 5 pieces, 400 draws, 95th percentile: hist 0.269. Only 1 piece is large enough for spectrum windows, so wood has no spectrum statistic |
| shingle | v1 shore_rock | piece bootstrap over 10 pieces: hist 0.097, spec 0.029 |
| sea, shore ice | v1 tarn ice | chunk leave-one-out: hist 0.126, spec 0.031 |

On R-C9-159 (advisory, not part of the row verdict), no sample falls inside its mapped bar: wood 0/3, shingle 0/11, sea 0/12, shore ice 0/5. Evidence is in `results/p4.json` → `new_classes_advisory`.

**R-C9-167 (4) P8: re-based on the recorded quantity.** The record, `take/build/overlay_check.json:1781` = 0.5221, is `overlay_check.py`'s **precision_drawn_on_painted**: of the pixels the 3D heather is drawn on, the share that are painted-tuft pixels, over the whole window.

My first metric was a different quantity. **Share** asks whether a spray stands within 24 px of any painted tuft. It is an instance-level placement-validity rate and reads 1.00 for v1. Precision is lower (0.52) because a spray's drawn pixels spill past its tuft's painted pixels. The two agree on pass/fail for every calibration input.

Precision is now **binding**, measured from PH's own v1 capture. It reproduces the record **exactly: 0.5221 over 934,936 drawn px**, which equals the recorded `drawn_heather_px`. Results:
- v1: 0.5221, PASS.
- R-C9-159: 0.0212, FAIL. Its painting has no plants, so its heather cannot stand on painted tufts.
- constructed (heather shifted 4 m): 0.1061, FAIL.

The bar is provisional at 0.4567: the record minus half of v1's chunk-to-chunk range. It re-bases on PT's reproduced value when that lands. Share is still reported.

**R-C9-167 (5) P9c is non-binding until DEV-5's first build. The P9b film discard stands.**

**R-C9-167 (6) and R-C9-168 (P11).** The conductor scored v0.1's three judges with `p11_pairs.py score`. The answers are kept as evidence in `p11/answers/`:
- v1 vs 159: 100%, null false-alarm 0. FAIL, correct.
- v1 vs half-density: 86.7%, null false-alarm 0.1. FAIL, correct.
- v1 vs 158: 13.3%, null false-alarm 0.4. The judge is UNRELIABLE. It told the builds apart by register but named v1's warm register "lower fidelity". The brief's quality word carried a prior about which build was better.

**Re-instrumented as a direction-free ABX test** in `harness/p11_abx.py`. Each trial image is A | B | X. A and B come from the two builds, and which build is A is randomised per trial. X comes from one of the two builds: the same class, a different location, and 20/20 balanced between the builds. A degraded copy of a v1 still counts as that still's location, so a trial never pairs a crop with its own degraded copy. There are 40 trials plus 10 repeats with A and B exchanged, 50 images in all, metadata-stripped and named `trial_NN.png`. The brief asks only "is X from the same build as A or as B?", with no quality words.
- **Score:** ABX accuracy. PASS (indistinguishable from v1) if ≤ 65%, i.e. ≤ 26/40.
- **Reliability:** if more than 25% of the repeat pairs name different builds for X, the judge is VOID.
- **Scorer checks:** an oracle answer file scores 100% with 0% inconsistency; random answers score 40–55%; all-"A" answers void the judge.
- **Power:** P(pass) = 0.98 at p = 0.50, 0.79 at 0.60, 0.56 at 0.65, 0.30 at 0.70, 0.10 at 0.75, 0.02 at 0.80, 0.00 at ≥ 0.90.
- **Judge directories:** `p11/abx_cal_v1_vs_159/`, `p11/abx_cal_v1_vs_158/`, `p11/abx_cal_v1_vs_constructed_halfdensity/`. Keys are in `p11/keys/abx_*.json`. Score with `python3 p11_abx.py score <set> <answers.json>`, and drop the answers in `p11/answers/abx_<set>.json` so that `calibrate.py` picks them up.
- **Crop pool note:** reaching 40 trials needed OVERLAP 0.5 within one location (3 v1 stills). Lower it to 0.25 when PT's v1 stills enlarge the pool.

## 8. Conductor ruling R-C9-169, folded

**P6a becomes option (b), scoped, on top of v0.1.** The pipeline is in `harness/p6_judge.py`.
1. The v0.1 detector (T = 32, no prior) stays the binding candidate generator. Declared openings are matched and dropped.
2. A candidate **outside** the declared dark-structure regions fails the chunk automatically.
3. A candidate **inside** one goes to a fresh blind judge. Each item shows the painting crop beside the guide crop at the same pixels. The judge is asked one question: "does the painting show a doorway, opening or structure the guide does not?" A "yes" fails the chunk.
   - In Phase 1 and later, the declared dark-structure regions come from the ID render's hall, porch, gable, palisade and char classes.
   - For calibration they come from the zone-map extrusion. All 18 BVR hall candidates lie inside it.
4. If the calibration fails its acceptance, the fallback is (a): the conductor triages the stage-3 candidates by eye, logged per chunk.

**The calibration set is built: `p6_judge/`.** It holds 20 items (`item_01..item_20.png`, 512 px crops = 5.1 m, metadata-stripped), JUDGE.md with only the ruling's question, and the key in `keys/p6_judge.json`, outside the judge directory.
- **Positives (2):** the R-C9-155 invented door, plate (10311, 4925), shown with the BVR zone map; and the stamped doorway on v1, shown with v1's guide.
- **Negatives:** v1's declared barrow door (1), shown with v1's guide; and the 17 BVR hall timber candidates, shown with the BVR zone map.
- **Acceptance:** both positives "yes", v1's door "no", and at most 2 "yes" on the timber.
- **Scoring:** `python3 p6_judge.py score <answers.json>`.

Two things to expect from this particular calibration set:
- **The guide is a flat map, so timber may draw false "yes" answers.** The BVR guide is the flat zone map the painter was given, with structures as ground-plane footprints. Roof-level timber, painted above the hall footprint, therefore sits over "snow" in the guide crop. Of the 17 timber items, 6 are centred over land_snow or rock_face in the zone map. In Phase 1 the guide is a greybox render with walls and roofs, so this case does not arise there.
- **The guide marks something dark at the invented door.** In the zone map a dark brazier mark sits beside the porch outline at that spot, and a judge may read it as "the guide shows an opening here". If the door is missed, that is the likely cause.

**P8 is final, no longer provisional.** The bar is v1's minimum chunk value, **0.4476**. PT reproduced all 16 chunk values and the 0.5221 whole-window value exactly (T3). Results: v1 0.5221 PASS, R-C9-159 0.0212 FAIL, constructed 0.1061 FAIL.

**P11.** PT's six v1 stills and `views.json` are in `fid/pc/v1_stills/`. They join the ABX pool, with OVERLAP 0.25, only **after** the current ABX judges return. The three ABX sets are not regenerated before then.

## 9. P6a ground truth, re-derived from the layout (R-C9-170). Written BEFORE any re-scoring.

**Why it is re-derived.** The key's "invented door at (10311, 4925)" came from the v0.1 detector's own flags, so scoring the detector against it was circular. The truth below is derived instead from (i) layout v5's declared openings (git `b267b9b00`, the layout the BVR blocks were painted from, `inputs/layout_v2_at_b267b9b00_v5.json`) projected by the BVP plate law, (ii) the zone map the painter was actually given (`paint/barrow_v2_zonemap.png`, 08:48, drawn from v5 by `bvp_zonemap.py` at `79716d1e9`), and (iii) **Matt's review sheet** for R-C9-155, `paint/test/T2a_hall_compare.jpg`, middle panel.

**Declared on the hall by layout v5.** Exactly one opening system: the porch and the great door it leads to.
- `hall_great_door`: footprint px x 10559–10953, y 4685–5017 at z 0, rising 4.8 m (291 px). 4.5 × 4.5 m.
- `hall_porch`: footprint corners (10514, 5022), (10954, 4646), (10733, 4482), (10294, 4858). Mouth centre (44.19, 3.89) → px (10513, 4670) at z 0. The opening is "between the front posts", 4.5 m clear.
- Two braziers flank the porch: `brazier_sw` at px (10331, 4985) and `brazier_ne` at (10894, 4503).

**In the zone map:**
- The **only** door-coloured mark (40, 30, 28) on the hall is at x 10771–10952, y 4392–4512: the great door's height outline.
- The dark disc next to (10311, 4925) is the **brazier_sw** mark (60, 44, 36), lying inside the porch's 9 m height outline (the orange "capsule"). **It is not a door mark.**
- At (10350, 5423) and (10184, 5392) the map shows plain hall fill with no marker.

**In the painting.** The declared great door is painted where the layout puts it: the big gable with open double doors at plate ≈ (10862, 4452), braziers on either side. v0.1's candidate there, (10808, 4435), was matched to it and dropped, so it is not in the judge set.

**On Matt's sheet** ("two large open doors"), at review scale, exactly two large open doorways read:
1. the declared porch and great door (top);
2. the doorway at (10311, 4925): an open door leaf, jambs, embers and smoke, a brazier on each side, 4.4 m from the declared porch mouth (beyond the 3.75 m match radius).

The painter evidently read the brazier_sw disc and the porch outline corner as a second door. The gable-end opening at items 08/11 does **not** read as a large open door at review scale, being under fallen beams. At full resolution it is a framed opening (carved jambs) into a burning interior that the layout does not declare.

**Truth table** (the 18 v0.1 candidates in the judge set, ordered up-screen to down-screen). INVENTED = a doorway or opening the layout does not declare. MATERIAL = dark material of a declared structure.

| item | plate px | zone map under it | the painting shows | truth |
|---|---|---|---|---|
| item_16 | [10799, 4220] | land_snow + rock_face | timber of the DECLARED porch gable (finials, roof) above the declared great door; the door itself is in the crop | **MATERIAL** |
| item_02 | [11082, 4328] | land_snow | roof timber of the declared porch's long side; the declared door is at the crop's edge | **MATERIAL** |
| item_14 | [10351, 4345] | rock_face + land_snow | hall roof edge and timber at the NW gable | **MATERIAL** |
| item_20 | [11303, 4467] | land_snow + rock_face | hall roof purlins and thatch | **MATERIAL** |
| item_19 | [11453, 4641] | hall | hall roof purlins and thatch | **MATERIAL** |
| item_01 | [11556, 4709] | land_snow + hall | hall roof purlins and thatch | **MATERIAL** |
| item_15 | [11711, 4762] | land_snow + rock_face | hall roof purlins and thatch | **MATERIAL** |
| item_17 | [10311, 4925] | hall_yard_ash + brazier_sw disc, inside the porch height-outline | an OPEN DOORWAY: a door leaf swung open, carved jambs, dark interior with embers and smoke, a brazier at each side, on the hall's west side SW of the porch | **INVENTED** |
| item_09 | [11023, 4998] | hall | fallen rafters over the yard-side wall | **MATERIAL** |
| item_05 | [11526, 5005] | hall | hall eave and charred wall boards | **MATERIAL** |
| item_07 | [10575, 5191] | hall | collapsed roof: a hole through fallen rafters showing the interior, embers inside; no jambs, no door leaf | **MATERIAL** |
| item_11 | [10184, 5392] | hall | the same gable-end opening, 1.7 m west: a carved jamb post and the dark doorway behind it, smoke, embers | **INVENTED** |
| item_08 | [10350, 5423] | hall | the lower section's GABLE-END WALL: a framed opening (carved jamb posts) into a dark interior with smoke and embers, fallen beams across it | **INVENTED** |
| item_03 | [10634, 5748] | hall | palisade and fallen rafters at the lower section's end | **MATERIAL** |
| item_10 | [10234, 5753] | hall | roofless interior of the lower section, wall posts | **MATERIAL** |
| item_12 | [10098, 5757] | hall | roofless interior of the lower section, wall posts | **MATERIAL** |
| item_06 | [9862, 5849] | hall | roofless interior and the end wall of the lower section | **MATERIAL** |
| item_04 | [9946, 5972] | hall | roofless interior of the lower section, wall posts | **MATERIAL** |
| item_18 | stamped (constructed) | v1 guide: open snow | a 2.2 × 2.6 m dark doorway stamped on snow | **INVENTED** (constructed) |
| item_13 | v1 barrow door | v1 guide: the door | v1's declared barrow door | **DECLARED** |

**Adjudication of item_07: MATERIAL.** It is a hole through collapsed rafters showing the interior, with embers. There are no jambs and no leaf, it is in the roof plane rather than a wall, and it is not visible as a door on Matt's sheet.

**Adjudication of items 08 and 11: INVENTED, as ONE feature** (two candidates 1.7 m apart, one opening). Confidence is moderate: the opening is half hidden by fallen beams, and Matt's "two" at review scale are the porch and item_17. The layout declares exactly one opening on the hall, so any other framed opening into the hall is an invention by the layout's own standard.

**Ground truth, summarised:**
- Invented features in the BVR hall block: **2** (item_17; items 08 + 11).
- Material candidates: **15** (all the others, item_07 included).
- Constructed positive: item_18. Declared negative: item_13.

## 10. Re-scored against the § 9 truth (R-C9-170), and P11 v2 binding (R-C9-171)

**P6a re-score.** Evidence: `results/p6_rescore_v2.json`, `p11/answers/p6_judge_G.json`; scorer `p6_judge.py score2`.

| | invented: doorway by brazier_sw (item_17) | invented: gable-end opening (items 08/11) | stamp | v1 declared door | material "yes"/flags |
|---|---|---|---|---|---|
| v0.1 detector | flagged | flagged | flagged | not flagged | **15 / 15 material flagged** |
| judge G | **missed** ("no") | flagged (both 08 and 11 "yes") | flagged | not flagged | **1 / 15** (item_07) |

- The **judge meets the material bound** (1 false "yes", within ≤ 2) and keeps the declared door clear. It **misses item_17**: the doorway sits on the guide's brazier_sw disc inside the porch's height outline, so it reads as declared. This is the guide ambiguity flagged in § 8, and the same one that misled the painter.
- The **v0.1 detector sees both invented features** but carries 15 material false flags.
- **Acceptance (all invented flagged, declared clear, ≤ 2 material "yes") is not met by the judge.** Under R-C9-169 the fallback is **(a), conductor triage by eye, logged per chunk.**
- An observation for the ruling: a union rule ("fail the chunk if the detector flags a candidate OUTSIDE dark structures, or the judge says yes INSIDE") would still have missed item_17. Item_17 is inside the extruded porch/hall region and was judged "no". The miss comes from the guide (a brazier disc drawn like a door), not from the detector.
- **Phase 1 note.** The Phase 1 guide is a greybox render: braziers are small 3D props, and the ID render separates door from brazier. The disc-reads-as-door confusion should not recur there. This calibration cannot show that, though.

**P11 v2 ABX: BINDING (R-C9-171).** The conductor's judges scored as follows; answers are in `p11/answers/abx_<set>.json`:

| set | correct / 40 | repeat inconsistency | verdict |
|---|---|---|---|
| v1 vs R-C9-159 | 40 | 0.00 | FAIL (correct) |
| v1 vs half density | 37 | 0.00 | FAIL (correct) |
| v1 vs R-C9-158 | 36 | 0.10 | FAIL (correct) |

**Disclosure.** PT's six v1 stills (`fid/pc/v1_stills/`) were **already in the pool** when these three sets were built: `p11_pairs.V1_STILLS` globs that directory, and the stills had landed before the build. They are at play zoom: `views.json` gives ortho_size 10.7337 m on 1080 rows, which is 100.6 px/m, the same as v1ref. So the calibration is unaffected, but the record states it.

**Generator fixes for every future set** (`harness/p11_abx.py`). The three calibration sets were built before these fixes and stand as evidence.
1. **Repeats use a different X.** A repeat trial keeps the same A and B crops with sides swapped, and takes a **different X** from the same build: same class, new location, clear of every used crop. Reliability is now cross-crop consistency, not recall. The half-density judge had answered the identical-X repeats from memory.
2. **X crops are spaced apart.** An X crop may share at most 25% of its area with any crop already used (X_OVERLAP = 0.25). v0 allowed 50%, and trials 06/43 of the half-density set had X crops 128 px apart.
3. **Content control.** The 158 judge reported that foliage type and water type always fell on opposite sides.
   - Trials are drawn only from classes v1 has (snow, rock, standing stone, ice, heather/shrub, wood), class-matched within a trial.
   - Crops with **open sea, wreck, hall or cliff faces** are excluded.
   - From pixels alone only snow, ice and heather-on-snow are separable. Rock, standing stone and wood are drawn **only** from stills that ship a class mask (`<still>.classes.png` + `.json`; Phase 1+: from the ID render), because pixels cannot tell v1's outcrops from barrow_v2's cliffs, crags or hull.
4. **Underpowered sets are marked.** A set with fewer than 40 trials is flagged `UNDERPOWERED`, and must not go to a judge until stills (or class masks) are added.
5. **Pool.** v1 stills = v1ref + PT's six. Half-density constructed sources are made from every v1 still.

**Dry run of the fixed generator** (scratchpad only; the calibration sets were not rebuilt):
- v1 vs 159: **12** trials (UNDERPOWERED). R-C9-159's three stills are mostly cliffs and sea.
- v1 vs 158: **29** trials (UNDERPOWERED).
- v1 vs half density: 40 trials.

**Requirement for the fid level's P11:** at least about 12 play-camera stills, with ID-render class masks, so that 40 content-controlled trials exist. Lane PT/LV should plan the M1 and M2 stills with this in mind.

**Known limitation (constructed sets only).** v1ref's `V1_ring` and PT's `stone_ring` are different stills of the same place. The location guard works per still, so a v1 crop and a half-density crop of the same stones can meet in one constructed-set trial. Candidate builds are separate levels, so this does not arise for them.

## 11. Phase 0 Gate-2 folds (charter § 13, R-C9-173)

**G2-B2: P11 v1 GREEN, on the fixed generator.** Two judge-ready sets (keys in `p11/keys/`, outside the judge dirs):
- `p11/abx_g2_v1rec_vs_v1head/`: record-time v1 (`section_v1cam/v1ref/`, 3 stills) against HEAD v1 (PT's `fid/pc/v1_stills/`, 6 stills). 40 trials + 10 repeats, 50 images.
- `p11/abx_g2_v1_vs_halfdensity/`: all 9 v1 stills against their half-density copies. 40 trials + 10 repeats.

Both pass the scorer self-test: the key scores 100% with 0 inconsistency, random answers score 50%. No trial pairs two crops of the same place, and no repeat re-uses its X.

**Two generator refinements were needed to reach 40 trials from 9 stills**, recorded as re-instrumentation of the generator (no threshold moves):
1. **A within-trial world-location guard.** A crop maps to ground (u, v) from its still's camera centre (v1ref: `v2sw_run.gd` park points; PT: `views.json`). Within one trial, A, B and X are never within 3.5 m of each other, because V1_ring and stone_ring show the same stones.
2. **X crops are guarded against other X crops only** (≤ 25% overlap), not against every crop. An X near another trial's A or B leaks nothing, because the judge never learns which build A is. Without this the record-time set reached 18 trials, then 28.

**UNDERPOWERED (< 40) = VOID.** Neither set is underpowered. Results will be recorded in `calibration.json`, the v1 cell included, when the answers arrive.

**G2-B1: P6a overlay tooling and the overlay truth set.** `harness/p6_overlay.py`:
- **Declared openings** come from the layout and are projected to plate px: layout v5 for BVR, and LV's v7 declared-opening list in Phase 1 (schema in the docstring). Each is drawn as its wall-plane quad, cyan.
- **Distance** is in screen metres to the quad's **centroid**. The match radius is half-width + 1.0 m. The distance is measured to the centroid rather than the quad edge because, by edge, the invented doorway sits 1.3 m from the porch quad's corner and would match; it is 4.4 m from the centre.
- **`truthset`** gives `p6_overlay_judge/`: the 20 § 9 items, each a painting crop beside the same crop greyed with the declared openings outlined. JUDGE.md asks one question: "does the painting show a doorway or opening that is NOT inside a cyan outline?" The key, with the truth and the nearest declared opening, is in `keys/p6_overlay_judge.json`. Score with `p6_overlay.py score <answers>`.
  - By the overlay rule, one material candidate is auto-declared (old item_14, 2.47 m from the porch).
  - No invented candidate matches a declared opening. The nearest is item_17 at 4.38 m against a radius of 3.25 m.
- **`triage`** is the per-chunk tool for fallback (a). For each v0.1 candidate it renders crop | overlay, auto-classifies (declared if matched; invented if outside the declared dark structures; otherwise PENDING), and writes `results/p6a_triage_<window>.jsonl` rows: {chunk, candidate, candidate_px, inside_dark_structure, crop_sha, overlay_sha, nearest_declared, distance_m, match_radius_m, verdict, evidence, reader, ts}.
- **`record`** writes the reader's verdict.
- **Demo on BVR:** `results/p6a_triage_bvr_demo.jsonl` has 18 rows, 17 PENDING and 1 auto-declared. `record` was tested on a scratch copy of that file.
- **Caveat.** On BVR the painting does not register to the layout: the painter moved the porch about 4 m. In Phase 1 the painting is painted over the ID render of real models, so it registers to within a few px.

**W-3: P8 is now like-for-like.** The binding form is **per chunk**: every chunk with heather (≥ 2000 drawn px) must be ≥ 0.4476, v1's minimum chunk. This replaces whole-window against v1's chunk minimum, which mixed scales.
- v1 has 15 chunks with heather, from 0.4476 to 0.5783: PASS. The 16th chunk has under 2000 drawn px.
- **Graded constructed RED** (v1's drawn heather shifted): 0.1 m gives 3/15 chunks below the bar (min 0.4119); 0.25 m gives 13/15; 1 m gives 15/15.
- R-C9-159: 6/6 chunks below (min 0.0009): FAIL.
- The whole-window value (0.5221, reproduced exactly) is still reported.

**I-4.** Stale lines in §§ 0–6 are updated: the status header, the P8 and P11 threshold rows, P6a's flag count, the pending list, and § 6.

## 12. Ruling R-C9-175: the G2 judges, recorded

Answers are saved as evidence in `p11/answers/` (`abx_g2_v1rec_vs_v1head.json`, `abx_g2_v1_vs_halfdensity.json`, `p6_overlay_J.json`). Each was scored with the harness's own scorer.

**P11 v1 cell, GREEN.** The record-time v1 against HEAD v1 test scores **22/40 = 55%** (the bar is ≤ 65%), with repeat inconsistency 0.10, so the judge is valid. **PASS**: the judge cannot tell v1 from itself beyond chance.

**P11 constructed, on the fixed generator.** v1 against half density scores **33/40 = 82.5%**, with repeat inconsistency 0.20, so the judge is valid. **FAIL**, which is correct.

**P11 counts from W-A on** (R-C9-175).

**P6a overlay judge (J)** (`results/p6_overlay_score_J.json`): both invented features flagged (the doorway by brazier_sw and the gable-end opening), declared door not flagged, **stamp missed**, material "yes" **5/15** (old items 04, 06, 07, 10, 12). **Acceptance not met.** The conductor reads P6a candidates by eye under charter § 13, using the triage tool and its jsonl record.

## 13. Phase 1 support: P6 for LV's v7c guide and ID render, against the layout_v7c polygons

Tool: `harness/p6_phase1.py`. Result: `results/p6_phase1_v7c.json`. Inputs:
- `fid/lv/guide_v7c/ids_v7c.png` (48 ids, `guide_manifest.json` id_table; ids_v7b is superseded);
- `fid/lv/layout_v7c.json`;
- the projection law from `declared_openings.json`.

**Measure.**
- Each placed layout object's silhouette is the union of its projected placement prisms: box instances as `bv2f_level.gd` `_place_box` stands them, beams as thick segments.
- It is clipped by every other placed object's ID pixels (occlusion), then compared with the object's ID pixels. A model's own declared-opening curtain counts as the model.
- The same measure was run on v1 (`take/ids` against v1's built footprints) as the like-for-like baseline.

**Overlay check.** The layout prisms sit on their rendered models across the frame. **Containment** (the share of an object's ID pixels inside its own layout prism) has a median of **1.0** (v1: 1.0). No rendered object stands outside its slot.

**IoU.** The median over the 18 rendered objects is **0.457**.
- Against the **ruled bar 0.513: below.**
- Like-for-like v1 baselines: real models excluding trees **0.645** (n 23), slab primitives **0.819**, trees **0.239**.
- The deficit comes from shape fill, not placement. Tripo crags and ruins fill their boxes less than v1's near-box stones, and terrain hides low pieces:
  - structures: longhall 0.71, barrow_front 0.65, stair_cliff 0.58, fallen_gable 0.51, wreck 0.35 (half-sunk, z −1);
  - crags: 0.35–0.64.
- **For the conductor:** whether the binding Phase-1 geometry-agreement statistic is containment (placement) or IoU (shape) against a bar from v1's real models. Containment is 1.0 on every rendered piece.

**Layout objects missing, hidden or extra in the render:**
- **MISSING:**
  - `braziers`: GLB missing (`level.json` sim.glb_missing = godot/models/build/brazier.glb).
  - `rock_outcrop_3`: its 10.6k-px prism at the envelope's top edge shows only snow.
- **HIDDEN / BURIED:**
  - `standing_stones`: 3 of 4 stones render 0 px; terrain (snow, mound) covers 98.7% of the prisms. The stones stand below the sculpted ground, a **finding for LV**.
  - `cliff_faces`: 96% covered by the terrain's own rock face.
  - `grave_markers`: 8.8% visible, sunk in the shrub ground.
- **Outside the envelope:** rock_outcrop_6, 9, 12, 13.
- **Extra IDs with no layout model:** blobs_passage_dark, blobs_path, blobs_rock, blobs_shore_ice. These are the layout's sculpt blobs, expected.
- **Not placed by design:** the birch groves (no plants), hall_porch (part of the longhall build), cave_cliff (trimmed in v7c), sea_cave_stair (the stair prisms).

**Check (a), independently from the ID render.** Visible screen m² at the play camera, PH against LV:

| opening | PH | LV | |
|---|---|---|---|
| barrow_door | 21.92 | 22.36 | agrees (−2%) |
| sea_cave_mouth | 22.18 | 21.55 | agrees (+3%) |
| mere_ice | 373.71 | 373.61 | agrees |
| hall_great_door | 8.22 | 6.35 | **+30%** |
| fallen_gable_breach | ≤ 12.83 (upper bound) | 10.98 | not separable from the ID render |
| wreck_rail | ≤ 15.22 (upper bound) | 10.7 | not separable from the ID render |

- **hall_great_door:** the curtain id's area exceeds even LV's own unoccluded reference (6.40), so the curtain geometry and LV's probe differ. The door is visible either way.
- **fallen_gable_breach and wreck_rail:** a horizontal probe inside its own model can be hidden by that model's near side, and an ID render cannot separate the two, so PH's 100% is an upper bound, not a check.
- **All six openings are visible, so check (a) PASS stands.**
- **Inconsistency for LV:** wreck_rail is `faces_camera: false` in `declared_openings.json` but `true` in `check_a.json`.

## 14. P6 re-measured on LV's fixed v7c (d4c59061f, 43 ids; ruling R-C9-178)

Inputs: `ids_v7c.png` sha `49adb3d8…` and `layout_v7c.json` (v7c_r178). Tool `harness/p6_phase1.py`; result `results/p6_phase1_v7c.json`.

**What changed.** LV's fixes to my five findings hold:
- **Missing:** none. The braziers render as a primitive stand-in, and outcrops 3, 6, 9, 12 and 13 were dropped with reasons.
- **Buried:** none. Standing stones and grave markers are now seated on the terrain, and the cliff faces stand clear of the terrain face.
- **Extra IDs:** only the sculpt blobs (blobs_*), as expected.

**Placement:**
- Containment median **1.0**. Every rendered object's ID pixels lie inside its own layout prism (v1: 1.0).
- The share of each object's ID pixels inside its own GLB silhouette placed by the layout is **≥ 0.96 for every object**.

**IoU:** median **0.46** over 20 rendered objects, **below the ruled bar 0.513**. No bar change is proposed (R-C9-178).

**Per-object attribution** of the residual (1 − IoU):
- *organic under-fill* = 1 − IoU(the object's own GLB silhouette rendered alone, its layout prism);
- *occlusion* = IoU(alone) − IoU(observed);
- *placement* = the share of its ID pixels outside its own prism.

| object | IoU observed | < 0.513 | IoU alone (shape vs prism) | under-fill | occlusion | placement | dominant |
|---|---|---|---|---|---|---|---|
| grave_markers | 0.136 | **<** | 0.178 | 0.822 | 0.042 | 0.000 | organic under-fill |
| circle_stones | 0.205 | **<** | 0.528 | 0.472 | 0.323 | 0.000 | organic under-fill |
| logs_and_beams | 0.280 | **<** | 1.000 | 0.000 | 0.720 | 0.041 | occlusion + beam shape (see note) |
| wreck | 0.345 | **<** | 0.412 | 0.588 | 0.067 | 0.000 | organic under-fill |
| rock_outcrop_14 | 0.345 | **<** | 0.560 | 0.440 | 0.215 | 0.000 | organic under-fill |
| rock_outcrop_11 | 0.347 | **<** | 0.534 | 0.466 | 0.187 | 0.000 | organic under-fill |
| rock_outcrop_8 | 0.376 | **<** | 0.533 | 0.467 | 0.157 | 0.000 | organic under-fill |
| rock_outcrop_4 | 0.397 | **<** | 0.550 | 0.450 | 0.153 | 0.000 | organic under-fill |
| palisade | 0.454 | **<** | 1.000 | 0.000 | 0.546 | 0.019 | occlusion + beam shape (see note) |
| rock_outcrop_2 | 0.459 | **<** | 0.614 | 0.386 | 0.155 | 0.000 | organic under-fill |
| rock_outcrop_1 | 0.460 | **<** | 0.513 | 0.487 | 0.053 | 0.000 | organic under-fill |
| standing_stones | 0.461 | **<** | 0.573 | 0.427 | 0.112 | 0.000 | organic under-fill |
| braziers | 0.471 | **<** | 0.703 | 0.297 | 0.232 | 0.000 | organic under-fill |
| fallen_gable | 0.511 | **<** | 0.513 | 0.487 | 0.002 | 0.000 | organic under-fill |
| rock_outcrop_10 | 0.520 |  | 0.586 | 0.414 | 0.066 | 0.000 | organic under-fill |
| cliff_faces | 0.531 |  | 0.663 | 0.337 | 0.132 | 0.000 | organic under-fill |
| stair_cliff | 0.584 |  | 0.648 | 0.352 | 0.064 | 0.000 | organic under-fill |
| rock_outcrop_5 | 0.643 |  | 0.688 | 0.312 | 0.045 | 0.000 | organic under-fill |
| barrow_front | 0.650 |  | 0.758 | 0.242 | 0.108 | 0.000 | organic under-fill |
| longhall | 0.715 |  | 0.685 | 0.315 | 0.000 | 0.000 | organic under-fill |

**Reading the attribution:**
- **Placement contributes nothing.** Its largest value is 0.041, on logs_and_beams.
- **The residual is organic under-fill first.** Even unoccluded, the objects' own shapes fill their layout prisms at a median IoU of **0.579**: Tripo crags and ruins are not boxes. **Occlusion comes second**, a median of 0.122.
- **The beam groups (palisade, logs_and_beams) are an exception.** Each log is modelled as its drawn segment, so all of their residual is booked as occlusion; the beam-shape share cannot be separated from it.
- **Grave markers (0.136)** are shields: thin plates in a box slot, which is under-fill.

**Check (a), re-read with LV's own probe definition** (`level.json` sim.openings[].probe, `bv2f_level.gd` _build_probes):
- **Reference area.** Each probe's unoccluded projected area, computed analytically here, matches LV's probe_only reference within 0.13% for all six openings.
- **Visible area.** PH's recount of LV's probe_with renders gives LV's numbers exactly: barrow door 22.36, hall great door **6.35**, sea cave mouth 21.55, gable breach 10.98, wreck rail 10.70, mere 373.61 m². **All visible: PASS.**
- **The hall-door explanation is ACCEPTED.**
  - My earlier 8.22 m² counted the ID render's dark curtain, which is a 0.3 m-deep box 1.6 m behind the probe plane. Its analytic box silhouette is **83308 px**, against the **83234 px** of curtain ID I counted (within 0.1%).
  - The probe face alone is 64706 px, against LV's reference of 64791 px.
  - So 8.22 m² was the curtain box's front, top and sides, not the opening.
- **The faces-camera rule is consistent.** `declared_openings.json` now carries `check_a_faces_camera`, which equals check_a.json for all six openings. `frame_faces_camera` (wreck rail: false) is a different quantity, the rail's own facing, now named apart.


## 15. P6′ PRE-REGISTRATION (charter v0.4 § 14, G2P1-B1, R-C9-180). Committed BEFORE any v7c re-read.

**Status.** Pre-registered. The definitions and bars below are fixed by this commit. Calibration (§ 16) and the v7c run (§ 17) follow in later commits and may not edit this section. Any change after this commit is a new pre-registration, recorded as one.

**Scope.**
- **Objects:** every layout model the level places with a mesh (its GLB, or a stand-in the level declares) inside the paint envelope. Group models are measured **per instance** wherever the record allows.
- **By-design exclusions** are read from records written before this commit and quoted in the result: the level's `skip_models` (plants), models that are part of another build (hall_porch), models trimmed by a ruling (cave_cliff), and the stair prisms (not a model).
- **Non-model ID pieces** are excluded from "extra" by definition and listed in the result: ground_*, blobs_*, curtain_*, the v1-instrument stubs, stair_*.

**P6′ = four components. Each is evaluated per object, the row PASSES only if every component passes on every object, and an object that cannot be measured FAILS.**

1. **PRESENCE.**
   - (a) **Missing:** an object with zero ID pixels. Bar: **0 missing** (written rule).
   - (b) **Extra:** a model or group ID with no layout model. Bar: **0 extra** (written rule).
   - (c) **Buried or hidden by terrain.**
     - *Own silhouette:* the object's own mesh placed exactly as the level places it (v7c: `bv2f_level.gd` `_place_box`, which stands the AABB bottom-centre on the slot origin, scales it per axis to the slot and applies the yaw; v1: the built record's world transform), rendered alone.
     - *Terrain-hidden share:* the share of the own-silhouette pixels whose ID is ground.
     - **RED if the terrain-hidden share exceeds 0.50, unless the layout records the burial by design** (quoted). Written rule: an object more than half under or behind the ground shows the player less than half of what the layout places. v1 must pass: its ground is flat.
2. **PLACEMENT (in slot).**
   - *Containment:* |ID ∩ slot prism| / |ID| per object. The slot prism is the projected hull of the object's slot: v7c from its layout box or boxes; v1 from its built footprint_uv_low and y range.
   - **Bar = v1's minimum containment** over its pieces with at least 400 ID pixels, on this same measure, computed in § 16 from v1 alone.
3. **SCALE OF RECORD (principle 3, C7).**
   - *Anisotropy* per instance = max(fit_scale) / min(fit_scale), using the level's own recorded fit_scale (v7c: LV's per-instance record, G2P1-W2; v1: built.fit_scale).
   - *Pitch exception:* where, and only where, a record states `pitch_correct: true` with a `pitch_stretch`, the y-scale is divided by that stretch first. This is v1's recorded camera-foreshortening correction, a named mechanism and not a tolerance.
   - **PASS iff anisotropy ≤ 1.10** (written rule, principle 3).
   - An instance with no scale record is UNMEASURED and fails.
   - Cross-check: PH recomputes each v7c scale from its layout box and the GLB's AABB (size / AABB per axis). A recorded value that differs by more than 1% is a FAILED record.
   - Procedurally built primitives with no GLB (v1's slab outcrops, mound and shore rocks) are not normalised, so the component does not apply (N/A, listed).
4. **EXTENT.**
   - The extent rules of the layout validator (`fid/lv/tools/validate_layout_v7.py`, run read-only on a PH copy of the layout) are re-run with each placed model's slot replaced by **its own placed geometry**: footprint = the convex hull of its placed vertices in sim (x, y); height = the maximum placed z minus the slot z. Instances are treated the same way.
   - **PASS iff every R1–R13 check passes.**
   - v1's positive control is its own acceptance record (`barrow_full_layout.json` acceptance: placements, no_squeezes, door, mound_and_door_floor, flood_fill, walks), which `finalize.py` computed from the built models' own footprints. v1 has no layout_v7 schema for this validator to read.

**Calibration owed (§ 16), all before the v7c read:**
- v1 PASS on every component.
- One RED per component:
  - presence: v7c at `2a913e7af`, from its recorded result `results/p6_phase1_v7c.json` at that commit (braziers missing, standing stones buried);
  - placement: a constructed 1.5 m shift;
  - scale: a constructed squash of more than 10%, v6's 3 m porch (layout v6 hall_porch slot against the hall_porch GLB);
  - extent: a constructed shrunk gable that breaks R10 (more than 3.0 m from the edge).

**Reported, non-binding:** IoU against the slot prism, printed beside v1's like-for-like **0.635**.

**Rule:** a P6′ RED on v7c is a HALT for an LV fix, never a bar move.

## 16. P6′ CALIBRATION (§ 15 as registered; `harness/p6prime.py calibrate` → `results/p6prime_calibration.json`). Committed BEFORE the v7c run.

**Bars:**
- presence: 0 missing, 0 extra, terrain-hidden share ≤ 0.50 (written);
- placement: containment ≥ **0.7872** (v1's minimum, from TL_right_2, over 86 pieces with ≥ 400 px);
- scale: anisotropy ≤ 1.10 (written);
- extent: every R1–R13 check passes.

| component | v1 (positive) | RED | RED result |
|---|---|---|---|
| presence | 0 missing, 0 extra, terrain-hidden max 0.2744: **PASS** | v7c at `2a913e7af` (recorded result) | missing: braziers, rock_outcrop_3; terrain-hidden (recorded): standing_stones 0.987, cliff_faces 0.961: **RED** |
| placement | containment min 0.7872 (own-silhouette check: median 1.0 of ID px inside the placed GLB): **PASS** | every v1 slot prism shifted 1.5 m | 85 of 86 pieces below the bar: **RED** |
| scale of record | anisotropy max 1.0441 (birches: pitch-corrected 3.361 / 1.659 against a forced 1.38 m width): **PASS** | v6's 3 m porch: slot [13.207, 11.3, 3.0] m against hall_porch.glb AABB [8.1, 11.3, 3.0] m | fit [1.6305, 1.0, 1.0], anisotropy **1.63: RED** |
| extent | v1 acceptance record (51 PASS flags: placements, no_squeezes, door, mound_and_door_floor, flood_fill, walks): **PASS** | v7c layout with the fallen gable shrunk to 40% about its far point | validator 65/66, **R10 FAIL** (gable more than 3.0 m from the edge): **RED**. The unshrunk layout copy gives 66/66, so the validator runs correctly on PH's copies |

**One gap-fill to the registered text (A1), disclosed.** v1's lintel and raven stand wholly above 1.9 m, so their `footprint_uv_low` is EMPTY by construction. Their slot prism is the convex hull of their own placed vertices over the y range. This affects v1 measurability only and was fixed before the v7c run.

**Reported, non-binding:** IoU against the slot prism, beside v1's like-for-like 0.635.

## 17. P6′ ON v7c (`harness/p6prime.py v7c` → `results/p6prime_v7c.json`; bars from § 16; inputs ids sha `49adb3d894b2…`, layout sha `f8e7b5ab88f0…`, placed_fit sha `521e89e90292…`)

**P6′ = RED** on three of the four components. **Reported, not adjusted (HALT for an LV fix, charter § 14).**

| component | result | detail |
|---|---|---|
| presence | **RED** | 0 missing, 0 extra (non-model ids excluded as registered). **2 instances terrain-hidden above 0.50:** logs_and_beams #5 (yard_beam_2) at 0.545 and #6 (yard_beam_3) at 0.505. These are logs whose centres sit 0.15–0.18 m up with a 0.35 m thickness, about half in the ground, and the layout records no burial by design (status "REUSE v1 kit/log") |
| placement | PASS | every object's containment ≥ 0.7872 (v1's minimum) |
| scale of record | **RED** | 137 of 148 instances have anisotropy above 1.10. PH's size/AABB cross-check agrees with LV's record on every box instance (0 mismatches). Over the bar: standing_stones 2.11–2.38; circle_stones 1.71–4.59; grave_markers 1.98–1.98; rock outcrops 1, 2, 4, 5, 8, 10, 11 1.15–1.77; logs_and_beams 4.54–10.09; palisade 8.90–14.09 (every stake). Within 1.10: the kit-v3 heroes (longhall, barrow_front, wreck, fallen_gable), stair_cliff, cliff_faces, rock_outcrop_14 and the brazier stand-ins |
| extent | **RED** | validator 65/66 on the own-geometry copy. **R11 fails: "the porch rises ABOVE the hall's roofline (slot heights)".** Attribution: the porch is PART OF the longhall build (no mesh of its own), so the hall's own height as registered (maximum placed z = 13.117 m) is the porch top. The hall's roofline and the porch cannot be separated in one mesh, so the rule reads porch 13.117 against "hall" 13.117. Every other R1–R13 check passes on the models' own footprints and heights (longhall, fallen_gable, barrow_front, wreck → wreck_hull, stair_cliff replaced; R10 holds for the gable at its own extent) |

**Harness change disclosed (I-R1, jack-ryan RB re-check).** Between calibration (`48dab5e17`) and this run, commit `44fb98a66` made two changes to `p6prime.py`. Beam instances are now placed as `bv2f_level.gd` `_place_beam` places them, not as drawn segments. "extra" now excludes the non-model prefixes that § 15's scope names. Both conform to § 15, leave the v1 path untouched, and make the check stricter, not looser.

**Reported, non-binding:** IoU against the slot prism, median **0.46**, against v1's like-for-like **0.635**.

**For the conductor.** These are three REDs of different kinds:
1. **Scale, the largest:** the v6-era per-axis fits of the stones, markers, crags and beams. This is C7, as G2P1-W2 anticipated.
2. **Presence:** two yard logs half in the ground.
3. **Extent R11:** an artifact of measuring a two-part build as one height. Per § 14 it is reported as RED, not re-measured. Whether the hall/porch split needs a separate record from LV, or a ruling, is the conductor's call.

## 18. P6′ RE-RUN on LV's R-C9-181 refit (9601add8a). SAME pre-registered bars (§ 16, unchanged)

Inputs: ids `bbff1fa06deb…` (= guide_manifest), layout `4c8a21a56897…`, placed_fit `b852697ee5b9…`. Result: `results/p6prime_v7c.json`.

**Geometry readings brought in line with what the level now builds**, applied identically to v7c and to the calibration REDs:
- **Lying stones:** `lie_z90` turns the model 90° about Z before the uniform fit.
- **Procedural beams:** palisade posts and logs are cylinders at their true diameter along a→b.
- **Scale N/A for procedural primitives:** they normalise no model, the same as § 15 (3) for v1's slabs.
- **R11 read per region of the one hall + porch mesh:**
  - the porch's height = the maximum placed z inside `hall_porch.r11_region_footprint`;
  - the hall body's height = the maximum placed z outside it.
  - Measured by PH from the placed hall mesh: porch **13.117 m** (10,034 vertices), hall body **12.143 m** (24,028 vertices). These match LV's record of 13.12 against 12.14.

**Hidden by design.** Provenance re-cited per I-R2 (jack-ryan, R-C9-182); the earlier test, "the declaration is new in 9601add8a", is withdrawn because a new declaration is weaker evidence than an old one. The burial **predates measurement and pre-registration**: at `d4c59061f` the layout already records circle_stones as "REUSE v1 stone_short (laid flat, sunk flush: top 0.12 m)". It is **required by R13** (FLAT = 0.15 m), Matt's clean-floor ruling **R-C9-155**. It is declared uniformly on all 8 stones. The objects that rely on it:

| object | instance | terrain-hidden share | declaration (layout_v7c.json, 9601add8a) |
|---|---|---|---|
| circle_stones | #2 | 0.918 | "R13 clean floor (R-C9-155): a fallen stone in the walkable floor may stand at most 0.12 m proud; the rest of it lies in the ground" |
| circle_stones | #4 | 0.514 | "R13 clean floor (R-C9-155): a fallen stone in the walkable floor may stand at most 0.12 m proud; the rest of it lies in the ground" |
| circle_stones | #5 | 0.916 | "R13 clean floor (R-C9-155): a fallen stone in the walkable floor may stand at most 0.12 m proud; the rest of it lies in the ground" |

The other 5 circle stones (all 8 carry the declaration) are within 0.50 even without it. **No other object relies on a by-design declaration.**

| component | verdict | detail |
|---|---|---|
| presence | **PASS** | 0 missing, 0 extra, 0 terrain-hidden above 0.50 without a declaration. The yard logs are now seated on the ground |
| placement | **PASS** | containment min 0.9577 (bar 0.7872) |
| scale of record | **PASS** | 148 instances: 0 over 1.10 (box instances by one uniform scale; procedural posts and logs N/A). PH's size/AABB cross-check agrees with LV's record on every box instance (0 mismatches) |
| extent | **PASS** | validator 66/66 on the own-geometry copy, with R11 per region (porch 13.117 > hall body 12.143 + 0.5) |

**P6′ = PASS.**

**The calibration REDs under the same readings** (`results/p6prime_reds_r181.json`):
- **v6's 3 m porch:** still **RED**, anisotropy 1.63. The per-region R11 reading is a height reading and cannot change a fit scale. On v6 the porch was its own model, so per region means per model (11.3 m against 6.5 m), and the RED stands on scale.
- **Shrunk gable:** run through the same own-geometry and per-region extent pipeline, it is still **RED**: validator exit 1, 1 fail(s), **R10 FAIL** (R11 per region: porch 13.117, body 12.143).
- The presence and placement REDs do not involve these readings and stand as in § 16.

**Reported, non-binding:** IoU against the slot prism, median **0.472**, beside v1's like-for-like **0.635**.


## 19. R11 PORCH-REGION READING, PRE-REGISTERED (ruling R-C9-182, on jack-ryan's G2P1-RB1). Committed BEFORE measuring.

**The ruled region, in the conductor's words:** "the porch-width strip over the great door, from the porch's OUTER FACE back to the hall's RIDGE LINE"; the BODY is the rest of the hall roof. LV's 16.5 m `r11_region_footprint` is **not** used.

**Its construction.** Only layout fields that predate § 15 are used: `hall_porch.footprint` and `longhall.pos / godot_rot_y_deg`, identical at `45fb5eaac` and at HEAD.
- **Porch outer face:** the edge of `hall_porch.footprint` farthest from the longhall slot centre, with endpoints P1 and P2 (10.6 m apart, the porch width).
- **Ridge line:** the line through the longhall slot centre (`pos`) along the hall's long axis. That axis is the slot's local x, which `_place_box` maps to sim (cos t, −sin t) with t = `godot_rot_y_deg`.
- **Region:** the quadrilateral P1, P2, foot(P2), foot(P1), where each foot is the perpendicular projection onto the ridge line.

**The reading.** Over the longhall's placed mesh (vertices as `bv2f_level.gd` places them, PH's `placed_vertices`, z relative to the slot z):
- porch_h = max z inside the region;
- body_h = max z outside it;
- **R11 PASS iff porch_h > body_h + 0.5** (the validator's own margin).

**Constructed RED under the same reading:** the in-region vertices' z clipped to ≤ body_h + 0.5. This must FAIL.

**Reported beside it, non-binding:** the registered 1.287 m `hall_porch.footprint` reading (jack-ryan measured 5.10 m: FAIL).

**For the cover clause** (not part of the verdict):
- where the vertices above body_h + 0.5 sit, in metres behind the outer face and in metres along the porch width;
- the porch's height at the door, the max z inside the registered 1.287 m footprint.

**If v7c fails under the ruled region, it is reported as a failure; the region does not move.**

## 20. R11 under the ruled region (§ 19, R-C9-182): `harness/p6prime_r11.py` → `results/p6prime_r11_r182.json`

**The region as constructed.** The outer face runs from (38.09, −3.84) to (43.29, 5.40), 10.6 m wide. The region reaches 8.774 m back to the ridge line and contains 6193 hall-mesh vertices; the body has 27869.

| reading | porch_h | body_h | margin | R11 (> 0.5) |
|---|---|---|---|---|
| **ruled region, v7c (binding)** | 13.117 | 12.2726 | 0.8444 | **PASS** |
| **constructed RED** (in-region vertices clipped to ≤ body + 0.5) | 12.7726 | 12.2726 | 0.5 | **FAIL** |
| registered 1.287 m `hall_porch.footprint` (non-binding) | 5.0955 | 13.117 | -8.0215 | FAIL (49 vertices) |

The constructed RED fails at the boundary: the margin is exactly 0.5 and the rule is strict.

**P6′ extent therefore stands PASS under the ruled reading, and P6′ = PASS on all four components.**

**For the cover clause** (measured, not part of the verdict):
- **The tall part sits behind the door.** The 49 vertices above body + 0.5 m (12.773 m) lie **4.78–8.06 m behind the porch's outer face**, at 3.99–7.78 m along its 10.6 m width: a raised roof bay over the door axis, set back.
- **At the door itself the porch stands 5.1 m**: the maximum z inside the registered 1.287 m-deep porch footprint.

## 21. P6′ on LV's ART blockout (charter § 15/15.1; R-C9-185/186). FROZEN bars from § 16; extent retired

Tool: `harness/p6prime_art.py` → `results/p6prime_art.json`. Inputs:
- `fid/lv/art/layout_bv2art.json` (sha `28f0bcb5f2bb…`);
- `fid/lv/guide_art/ids_art.png` (sha `1b902715b6e8…` = guide_manifest);
- the art `level.json` sim.models;
- `fid/lv/placed_fit_bv2art.json`;
- frame `frame_grid.bv2art.json` (v1's camera-aligned frame, so the same projection law as before).

**Slot cross-check first.** All 34 layout_bv2art placements match a level slot: position within 0.02 m, z, size within 0.01 m. **PASS.** The slots measured are therefore the layout's.

**I-4, the constructed 1.5 m-shift RED on bv2art** (bar 0.7872):
- 5 of 10 objects fall below the bar: slope_stones 0.031, ring_stones 0.029, palisade 0.144, logs 0.000, crags 0.637. **RED.**
- The large models stay above the bar under a 1.5 m shift (wreck 0.988, barrow 1.000, hall 0.975, gable 0.951, cliff_faces 0.988). The row fails on the small pieces.

| component | verdict | detail |
|---|---|---|
| presence | **RED** | 0 missing, 0 extra. **3 instances are terrain-hidden above 0.50:** see the list below |
| placement | PASS | min containment 0.9789 (bar 0.7872) |
| scale of record | PASS | 88 instances, 0 over 1.10; 0 mismatches between LV's record and PH's cross-check (procedural pieces N/A) |
| extent | retired (§ 15) | — |

The three terrain-hidden instances (above 0.50), none declared by design:
- slope_stones #4, 1.0: **frame edge**, only 13 px of its own silhouette lie inside the paint envelope;
- crags #2, 0.6506: **wholly below the sea surface** (top z −7.20 < sea_z −6.0);
- logs #3, 1.0: **wholly below the sea surface** (top z −8.67).

**P6′ on bv2art = RED (presence), reported, not adjusted.** It is a HALT for an LV fix: re-seat the crag and the log above the sea, and the edge stone is LV's call. The frame-edge case is a property of the pre-registered rule, which has no minimum pixel count for (1c); I state that and do not change it.

**Reported, non-binding:** IoU against the slot prism, median 0.475, beside v1's 0.635.

## 22. W-4(2): the minimum pilot window for a 40-trial content-controlled P11 (home ground), bv2art 5 × 5 grid

Tool: `harness/p11_window.py` → `results/p11_window_bv2art.json`. The fixed ABX generator's own selection logic was run without images:
- **v1 pool:** the real v1 crops (v1ref + PT's six).
- **Candidate pool:** classes from LV's class map and ID render at the same pixels. The build-specific exclusions of R-C9-171 apply (sea; char/ash/passage_dark; wreck, longhall, fallen_gable, cliff_faces).
- **Stills:** the window is covered by play-camera stills with the generator's centre exclusion.
- **Classes:** snow, ice and heather only. Rock, stone and wood cannot be class-matched, because v1's stills carry no class mask.

**The home ground** (the start, the 5 ring stones and 3 fallen stones, the mere polygon, the barrow door) spans plate px x 590–3722, y 349–2144.

**Minimum window = 3x3 canvases (9): cols 0–2, rows 0–2, plate px [0, 0, 4096, 2560].** It gives 40 trials and 10 repeats (snow 23, ice 7, heather 10), from 9 stills.

**The binding constraint is the home ground's own extent, not the trial count.** Every 2 × 2 and 2 × 3 sub-block in that corner also reaches 40 + 10, but none contains all four home-ground features. (The mere's west shore at x 590, together with the barrow door at x ≈ 3540, needs three columns.)

**Caveat.** The candidate classes come from the class map, not from painted pixels. Once the pilot is painted, the real generator must be re-run on its stills; the UNDERPOWERED guard applies before any judge.


## 23. P6′ re-run on LV's fix (550682c73): bv2art, frozen bars

Inputs: ids_art `aeaecf49ce26…` (= manifest), layout_bv2art `c30e0d449dfa…`, placed_fit `bba80944e10d…`.
- **Slot cross-check:** 34 of 34 match. PASS.
- **I-4 shift RED:** still FAILS, 5 of 10 objects below the bar.

| component | verdict | detail |
|---|---|---|
| presence | **PASS** | 0 missing, 0 extra, 0 terrain-hidden above 0.50. Crag #2 and log #3 are on the shingle; slope stone #4 is inside the envelope |
| placement | **PASS** | min containment 0.978 (bar 0.7872) |
| scale | **PASS** | 88 instances, 0 over 1.10, 0 record mismatches |

**P6′ = PASS** (presence, placement, scale; extent retired). IoU against the slot prism, reported and non-binding: 0.481 (v1 0.635).

## 24. Phase 2′ pilot prep (R-C9-188/189): run plan + P11 still spec (no image spend)

**Pilot:** the bv2art 5 × 5 grid, cols 0–2 × rows 0–2, plate px [0, 0, 4096, 2560], kept and built in-engine. **All bars are frozen as calibrated.**

**Run plan:** `fid/ph/pilot_run_plan.json`.
- **Rows that bind:** P1, P2, P3, P4, P5, P6a (v0.1 candidates + layout overlay triage + jsonl, read by the conductor by eye), P6′ presence/placement/scale, P8 (per chunk), P9, P10, P11 (40-trial ABX).
- **Retired:** P7 and P6′ extent.
- **Inputs requested from PT:** pilot painting + canvases + seam record; lineage spec; bake report; guide-camera render + heather mask; built ID capture; stills.
- **P6a in the pilot window:** the declared openings are barrow_door and wreck_hull. There is no char/ash, so any candidate that matches no declared opening fails its chunk.

**P11 still spec:** `fid/ph/pilot_p11_spec.json`.
- **The stills:** 12 stills (4 × 3) of 1920 × 1080, wholly inside the painted window. They are captured with PT's own v1 still recipe (`fid/pc/tools/pc_stills.gd`), so the test compares builds, not capture settings.
- **Class masks:** each still has an ID-render class mask (`<name>.classes.png/.json`), so the content control can exclude sea, wreck, hall and cliff by mask.
- **Verified with the fixed generator** on exactly these frames: **40 trials + 10 repeats** (snow 24, heather 13, ice 3), from a candidate pool of {'ice': 607, 'heather': 280, 'snow': 463}. The class-map caveat stands: re-run on the real painted stills before the judge.


## 25. Sea-cave walkability: PH's independent verification (R-C9-191; LV `52e099d05`). `harness/walk_verify.py` → `results/walk_verify_r191.json`

**What is independent.** PH re-derives every bar with its own code from LV's RAW Godot survey (`fid/lv/walk/walk_check.json`): down-ray hits, slopes, body-in-collider flags, free runs to colliders, and the driven track against the level's own colliders. PH does not reuse LV's `analyse()`. Segments come from the layout's own route polygons, not LV's labels; the stair includes the nosing ramp's foot, one tread past the flight polygon, and that is recorded. **Limit:** PH ran no second Godot survey; the down-ray data is LV's instrument.

**Step height.** `knight.gd` is a CapsuleShape3D with r = 0.35 × figure scale (lines 149–153, 808–812) and a single plain `move_and_slide()` (line 1145). It has no floor_max_angle, floor_block_on_wall or step-up code, so Godot's default of 45° applies. A capsule's lower hemisphere meets an edge of height h with its contact normal at acos((r − h) / r) from up. That contact is a floor only while the angle is ≤ 45°, so **h ≤ r (1 − cos 45°) = 0.1025 m. This matches LV's 0.103 m; the derivation is confirmed.**

**Design numbers.** 28 risers × 0.179 m = 5.00 m, which equals the shelf-to-landing drop; atan(riser / tread) = 33.48°, which equals the stated pitch. The 0.179 m visual riser exceeds the step height, but the walk surface is the nosing ramp (33.48°), and the treads lie under it.

**PH's verdict: PASS on all 8 bars.**
- continuous, cave → clifftop: 559 of 559 samples, 0 breaks;
- stair slope 33.48° ≤ 35°;
- shelf slope 0° ≤ 10°;
- maximum riser 0.033 m ≤ 0.1025 m;
- stair clear width minimum 5.25 m ≥ 5;
- shelf clear width minimum 6.15 m ≥ 6;
- cave mouth 6.0 m wide with 7.0 m headroom;
- the drive reaches the clifftop with 0 frames off the floor.

This agrees with LV's tool (PASS).

**Constructed REDs** on the same raw survey, run through PH's analysis and through LV's own tool. **Both FAIL in both tools:**
- **a 0.6 m riser on the shelf:** PH fails continuous + riser; LV fails continuous + riser;
- **a 1 m gap in the shelf floor** (20 samples): PH fails continuous; LV fails continuous.

These are data-level REDs; the knight was not re-driven over them.

**This does not gate the pilot** (R-C9-191).
