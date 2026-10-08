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

## 26. Phase 2′ PILOT harness run (R-C9-192). FROZEN bars; nothing re-derived from the pilot. `harness/pilot_harness.py` → `results/pilot/*.json`

**Inputs.** PT's pilot as handed over (`fid/pt/pilot/pilot_record.json`; commits 776e265f0 + 47bb1a054): painting sha `901f3087799e`, 4096 × 2560 = bv2art plate px [0, 0, 4096, 2560]; render_guide + heather_mask at the paint camera; ids_built (v1 ID code, 124 ungrouped ids, 31 in the window); bake_report (18 bakes); lineage (20 nodes); the 9 canvases `BV2F-PT-<c>_<r>` (shas checked against `stitch_record.json`); 12 stills + class masks. Chunk rects = v1's grid law (1536 × 1024 on a 1280 × 768 stride, 3 × 3).

**Concurrent edit, disclosed.** During this run PT re-ran `bv2f_prep.py` from a then-uncommitted working copy (tool mtime 11:02, outputs 11:04), since committed as b69a5d6d1 (DEV-17: "pilot payloads unchanged"). Checked: `lit.bin`, `painting.bin` and `snow_grid.bin` on disk still hash to the shas the committed manifest records (76686b759cd8, 901f3087799e, ed05ee26d1be); `manifest.json` / `heather.json` changed only in annotation strings. P2 therefore resolves the lineage **at the handed-over commit 47bb1a054** (every tracked path the spec names materialised from git; untracked payloads such as the bakes read from disk against their manifest shas). At HEAD / on the working tree one link breaks: `lit`'s producer (`lineage.json` records `tool_sha` 5c88e3aa, the 47bb1a054 tool; b69a5d6d1's tool hashes 1cd8d0e1). Recorded in `results/pilot/p2.json` `working_tree`, not counted; **PT's next lineage must cite the tool that produced it.**

| Row | Pilot | Bar (frozen) | Verdict | RED on the same instrument |
|---|---|---|---|---|
| P1 texel density | worst **1.711** (bake barrow_front); cliff_faces_0 1.234; wreck 1.391; the other 15 bakes and the projection 1.000 | every surface ≤ 1.05 | **FAIL (3 bakes)** | — (v1 1.000; calibrated § 1) |
| P2 lineage | 20/20 at 47bb1a054 | 100% | PASS | (calibrated § 1) |
| P3 render vs painting | worst 12.46 (wood, baked: the wreck); rock baked 11.60; ground classes 0.00–0.55 | ≤ 15.5 per class | PASS | pilot lit.bin × pilot shadow_mul re-shade: **FAIL** (rock baked 17.85, wood baked 17.74, mound 16.30) |
| P4 texture (snow, rock, ice) | ice: every ice chunk 0.611–0.671 (bar 0.126); snow: 0_2 0.421, 1_2 0.396 (bar 0.281), 0_0 spectrum 0.102 (bar 0.097); rock all within | v1 LOO maxima | **FAIL (9 chunk-classes)** | (calibrated § 3) |
| P5 seams | overlap MAD max 11.97; seam max 0.585 | ≤ 13.09; ≤ 0.799 | PASS | (calibrated § 3) |
| P6a invention | 6 candidates: 1 = barrow_door (0.75 m from its centre, radius 2.31); 5 in the open sea, chunk 0_2 → **conductor triage R-C9-194: 5 × MATERIAL** (water classes sea/mere = declared dark classes) | 0 invented | **PASS** (after triage) | (calibrated §§ 2, 9–11) |
| P6′ presence / placement / scale | 7 objects in window: 0 missing, 0 extra, 0 terrain-hidden; containment min 0.974 (logs); 89 instances, 0 over 1.10 | as § 16 | PASS | (§ 16, § 21 I-4) |
| P8 heather precision | chunks judged 6: min 0.4884 (1_0), 0.4884–0.5878 | each ≥ 0.4476 | PASS | 1 m shift: FAIL (min 0.000) |
| P9 life — heather sway | 5.967 over 132 304 heather px; noise 0.002 (mere edge, uv −3, 11.7) | ≥ 3× noise and ≥ 2.064 | PASS | --no-wind: sway 0.000, **FAIL** |
| P9 life — water flow | **0.000** over 267 100 px of painted open sea (W coast, uv −29, −5.5); whole frame max \|Δ\| 0 | ≥ 2.064 where open water is in the window (sea 3.5%) | **FAIL** | the pilot's sea IS the calibrated static-sea RED condition |
| P9 trail | coverage 1.000 of 937 m² walkable in the window (snow field area_xz) | ≥ 0.99 | PASS | (§ 6) |
| P10 frame time | p99 16.05 ms (p50 14.59, max 17.03; 900 frames, M2, forward_plus) | p99 ≤ 16.7 ms | PASS (0.65 ms headroom) | 20 ms burn: p99 21.70, **FAIL** |
| P11 ABX | set built: 40 trials + 10 repeats (snow 17, heather 21, ice 2) | ≤ 26/40; repeat inconsistency ≤ 25% | judge-ready (conductor spawns) | (calibrated § 11, § 12) |

**P1, read.** The frozen instrument (`p1_density.v1_surfaces`) gives a bake's displayed density as ppm × √(seen texels / silhouette px). v1's largest bake silhouette was 18 565 px (door_lintel); the pilot's barrow_front is 462 440 px and the wreck 434 433 px, on the same 1024² bake texture (v1's t5_06b, frozen), so their seen texels are spread over 25× the screen area. cliff_faces_0 fails differently: 97.5% of its texels are unseen before fill. **Sensitivity (non-binding), dropping the silhouette px hidden by another piece** (barrow_front 189 195, wreck 181 885): barrow_front 1.315, cliff_faces_0 1.229, wreck 1.060 — all three still over 1.05. The fail is the bake resolution against hero-sized pieces, not the projection.

**P4, read.** The fail is material, not mask or light. (i) The ice class read on its 1 m-eroded core is 0.625–0.695, as on the full mask, so the guide's ice edge is not the cause. (ii) Restricting to lit > 0.8 px leaves every value within 0.04 of the full read, so shadow is not the cause. (iii) Median L\*a\*b\*: pilot ice (68.9, −3.1, −17.7) against v1 tarn ice (55.2, −1.7, −23.7) — the pilot's ice is painted 14 L\* paler and less blue (smooth pale sheet with thin cracks; v1: dark cellular plates). Snow in the south row (0_2, 1_2) is cooler than v1's (b\* 3.2–4.0 against 7.7); snow elsewhere 0.147–0.205. **Advisory new classes (R-C9-167 (3)):** wood 0/2 within, shingle 0/5, sea 0/1, shore ice 0/3 — advisory only.

**P6a, read.** All five unmatched candidates lie in the open sea of chunk 0_2 (guide class `sea` 100% in a 0.6 m window; ID `ground_sea`); the detector's T = 32 L\* threshold finds the dark wave troughs. The window holds no declared dark structure, so the § 11 rule records them as "invented (outside dark structures: auto-fail)". **PH's observation for the conductor (not a verdict):** the crops show open water with whitecaps and an ice floe, no doorway or framed opening. The wreck_hull declared opening yields no candidate. Records: `results/p6a_triage_pilot.jsonl` (crop | overlay at `triage/pilot/<cid>.png`, declared quads cyan, match radius circles, the candidate red). The conductor's read is written with `p6_overlay.py record pilot <cid> <invented|material|declared> <evidence> --reader <name>`.

**P8 / DEV-18 (the conductor's question).** PT plants 3D heather on flat tufts only (flat = |terrain z| < 0.03 m, `bv2f_prep.py`). Painted tufts (v1's classifier on the pilot's ground): 539 687 px. **30.9% of all painted tuft px lie on not-flat ground with no 3D heather within P8's 24 px footprint** (of the not-flat tufts, 0.27% are covered). On ground steeper than 5°: 7.4% of all painted tuft px are bare. Flat tufts without 3D heather: 19.5% (sprays cover 29–38% of tuft cells by PT's placement record). P8 precision (drawn heather on painted tufts) still passes because it measures the drawn heather, not the painted tufts it misses.

**P9, read.** The pilot builds no water mesh: `bv2f_level.gd:179–190` lays the sea as one static plane (`ground_sea`) under the projected painting, so `ph_life.gd`'s hide_water pair cannot run and the calibrated flow instrument's own RED (the sea without its motion layers) is the pilot's state. Measured directly at the W coast (`renders/pilot/life_sea/`, `results/pilot/p9_flow_sea.json`): 0.5 s apart, not one pixel of the frame changes (snowfall is held by ph_life). Floe drift: N/A until DEV-5 (non-binding). Trail coverage reports alongside, non-binding: the field carries snow on 55% of the walkable window (flat ground only, DEV-18 as built). The heather view and perf view used `BV2F_VARIANT=art`, scene `bv2f_pilot_painted.tscn` as committed at 47bb1a054.

**P11.** `p11/abx_pilot_v1_vs_pilot/` (50 PNGs + JUDGE.md, metadata-free), key `p11/keys/abx_pilot_v1_vs_pilot.json` (outside the judge dir). v1 pool: the 9 v1 stills as calibrated. The within-trial same-place guard now also knows the 12 pilot stills' camera centres (`fid/pt/pilot_stills/views.json`). No rock / standing-stone / wood trial: no pilot crop reaches the 0.30 class-mask share with ≥ 2 crops in both pools. Score: `python3 p11_abx.py score pilot_v1_vs_pilot <answers.json>`.

## 27. P4 FORENSIC (R-C9-194): guide or paint? 0 images, no bar changes. `harness/p4_forensic.py` → `results/pilot/p4_forensic.json`, figures `results/pilot/p4_forensic_{ice,snow}.jpg`

**P6a fold.** The conductor's verdicts (`results/p6a_triage_pilot_conductor.jsonl`: 0_2_c001…c005 MATERIAL, "open-sea wave trough… guide class sea") are written into `results/p6a_triage_pilot.jsonl` via `p6_overlay.record`. The rows are marked inside a declared dark class under the R-C9-194 ruling (water classes sea and mere). `results/pilot/p6a.json` now reads PASS: 1 declared, 5 material, 0 invented.

**Masks.** Both sides use P4's own masks, eroded 3 px. The pilot's are the guide class map on ground, less tufts. v1's come from `p4_texture.v1_classes` on v1's guide and painting, which share one frame. Values are medians in L\*a\*b\*.

**Ice: the guide is the same and the paint differs.**

| | guide L\*a\*b\* | painted L\*a\*b\* | paint − guide | painted chroma | P4 Hellinger to the v1 pool |
|---|---|---|---|---|---|
| v1 tarn | (73.0, −1.9, −9.9) | (54.7, −1.8, −24.0) | (**−18.3**, +0.1, **−14.2**) | 24.2 | 0.031 |
| pilot mere | (73.1, −1.5, −9.7) | (68.8, −3.1, −17.7) | (**−4.2**, −1.6, **−8.0**) | 18.1 | 0.616 |

- (a) **The guide matches.**
  - **Tint:** the class tint is identical, ice (0.70, 0.775, 0.84) in both layouts. The guide pixels agree to within 0.4 in every channel.
  - **Light:** the guide's own light is the same. Open-snow L\* is 79.7 in v1 and 79.9 in the pilot; ice sits 6.7 / 6.8 L\* below snow in each.
  - **Brief:** the ice wording ("flat lapis-blue ice with pale cracks") and the IMAGE 2 ref (T10C-barrow_a) are identical in both briefs.
  - **What differs is size and edge.** The mere covers 163 m² against the tarn's 84 m² (bbox 21.2 × 11.8 m against 15.6 × 11.2 m). The pilot guide's ice edge is stair-stepped at the class-map resolution; v1's render edge is soft.
- (b) **The difference is the paint.** v1's painter darkened and saturated the guide's ice by −18 L\* and −14 b\*; the pilot's painter did so by −4 L\* and −8 b\*. The figure shows the hand: v1 painted dark lapis cellular plates with white rims; the pilot painted a pale, even wash with thin cracks.
- (d) **Sketch A's mere** (`sites/BV3r2-A.png`, make_bv2art's MERE polygon, eroded 6 px) has median (71.6, −0.3, −7.4).
  - **By median it is closer to the pilot's ice:** ΔE76 11.0 against 23.7 to v1's tarn.
  - **By histogram it is equally far from both:** Hellinger 0.691 to the pilot and 0.685 to v1. The sketch is a different hand and exposure, with reeds, rock and cracks inside the polygon.
  - So the look of record is pale ice, nearer the pilot than v1. This is an M2′ input, not a bar.

**Snow in 0_2 / 1_2: the guide is the same and the paint differs.**

The guide snow is (79.2–79.9, 1.2–1.7, 5.0–5.5) in every chunk; v1's is (79.7, 1.7, 5.1). The painted b\* shift (paint − guide) is:

| chunk | painted L\*a\*b\* | paint − guide (b\*) | Hellinger | guide lit share > 0.8 |
|---|---|---|---|---|
| v1 (whole) | (93.4, 2.7, 7.7) | +2.6 | — | — |
| 0_0 / 1_0 / 2_0 / 1_1 / 2_1 / 2_2 | (92.4–93.3, 1.8–2.5, 5.4–7.3) | −0.1 … +1.8 | 0.154–0.205 | 0.96–1.00 |
| **0_2** | (91.3, 2.2, **3.6**) | **−1.9** | 0.399 | 0.80 |
| **1_2** | (92.9, 2.0, **4.0**) | **−1.5** | 0.394 | 0.94 |

- (c) The same guide snow was painted about 3 b\* cooler in the two failing chunks. Shade does not account for it: 1_2 is 94% lit, and § 26 already showed the lit-only read still fails.
- Both failing chunks are bottom-row panels whose notes list the shingle beach, the sea cliff and the open sea (0_2). This points to the painter cooling snow in its sea-coast context, but that is a reading from content, not a measured cause.

**Answer.** Both P4 differences originate in the PAINT, not the guide. The guide's ice and snow pixels, tints, light and brief text match v1's. The painter's guide-to-paint transfer differs: ice −4 L\* instead of −18; snow b\* −1.5 to −1.9 instead of about +1 in the two coastal chunks. Bars unchanged.

## 28. P11 on the pilot: VOID × 2 (R-C9-195), plus a void-rule analysis for jack-ryan's Gate-2. No bar change. Evidence `p11/answers/abx_pilot_judge{1,2}.json`; simulation `results/pilot/p11_void_analysis_sim.json`

**Results** (scored by `p11_abx.py score pilot_v1_vs_pilot <answers>`, 40 trials + 10 repeats):

| Judge | Correct | Accuracy | Repeat inconsistency | Verdict |
|---|---|---|---|---|
| judge 1 | 27/40 | 0.675 | 0.50 (5/10) | **VOID** (> 0.25). Would have been FAIL (> 26/40) |
| judge 2 | 24/40 | 0.600 | 0.40 (4/10) | **VOID** (> 0.25). Would have been PASS |

**Every calibration judge on record, on the same scorer.** "Repeat X" is how a repeat trial is built. *Same* means the v0 generator re-used the identical X, so a judge could answer the repeat from recall. *Different* means the fixed generator (R-C9-171) draws a new X from the same build.

| Set | Repeat X | Correct | Repeat inconsistency | A-share |
|---|---|---|---|---|
| cal v1 vs 159 | same | 40/40 | 0.00 | 0.48 |
| cal v1 vs 158 | same | 36/40 | 0.10 | 0.50 |
| cal v1 vs half-density | same | 37/40 | 0.00 | 0.54 |
| G2 v1-rec vs v1-head (v1 vs v1) | different | 22/40 | 0.10 | 0.52 |
| G2 v1 vs half-density | different | 33/40 | 0.20 | 0.48 |
| pilot judge 1 | different | 27/40 | 0.50 | 0.56 |
| pilot judge 2 | different | 24/40 | 0.40 | 0.48 |

**What a pure guesser produces under the fixed generator.**
- **Why a guesser looks inconsistent.** A repeat shows the same A and B with their sides swapped, plus a new X from the same build. Consistency is scored as naming the same BUILD both times.
- **Guesser.** A guesser's two answers are independent, so inconsistency ~ Bin(10, ½)/10. That is a mean of 0.50 with a 5–95% range of 0.2–0.8. **P(inconsistency ≤ 0.25) = P(≤ 2 of 10) = 56/1024 = 5.5%.** The Monte Carlo on the pilot key (20 000 runs) gives 5.3%.
- **Position-biased guesser** (always "A"): inconsistency is 1.0 by construction, because the sides swap.
- **Perceiver.** A judge who picks the correct build with probability p, independently on each trial, shows expected inconsistency 2p(1−p). Monte Carlo on the pilot key:

| p | Mean inconsistency | P(valid) | P(valid and ≤ 26/40) |
|---|---|---|---|
| 0.60 | 0.48 | 0.070 | 0.052 |
| 0.65 | 0.46 | 0.090 | 0.042 |
| 0.75 | 0.38 | 0.208 | 0.010 |
| 0.90 | 0.18 | 0.744 | 0.000 |

**Reading (evidence for Gate-2; no bar moved).**
1. **On the fixed generator, the void gate and the pass bar pull in opposite directions.** A judge validates when it can tell the builds apart. A build passes when the judge cannot.
   - When the builds are truly indistinguishable, an honest judge is a guesser: **VOID about 95% of the time**.
   - **No independent-trial judge reaches "valid and PASS" more than about 5% of the time**, at any p.
   - The pilot's two judges sit where an at-chance-to-modest perceiver lands (inconsistency 0.40–0.50).
2. **The calibration that cleared the void gate cleared it under conditions that no longer hold.**
   - **Same-X calibration rows:** the three v0 sets re-used X, so consistency could come from recall. R-C9-171 removed that, after the half-density judge reported answering the repeat from memory.
   - **G2 v1-vs-v1:** this is the only GREEN on the fixed generator, at 22/40 with inconsistency 0.10. Under pure guessing, P(≤ 1 of 10) = 11/1024 ≈ 1.1%. So that judge was consistent through some stable cue, while being at chance on the build. The cue could be content shared by X and one side, or a consistent preference applied to the A/B pair. Its validity was not the "reliable perceiver" the gate assumes.
3. **What the gate measures now.** The repeat-consistency check as built measures whether a judge's build preference is stable across a different X. Under the null this is not a reliability property; it is chance. This is a re-instrumentation question (e.g. scoring consistency only on trials the judge got right, a fixed-X control, or more repeats), **not a threshold to tune**. It is for the conductor and jack-ryan to rule; PH changes nothing here.

## 29. Rebuilt pilot (R-C9-194 hand-back: f36284352, 2d95cfe5b, 0b72461db): PARTIAL, DISK HALT. Frozen bars. `PH_PILOT_COMMIT=0b72461db PH_PILOT_OUT=results/pilot2 pilot_harness.py p1 p2 p3 p8` → `results/pilot2/`

**Measured** (non-rendering, from files on disk):

| Row | Rebuilt pilot | Bar | Verdict |
|---|---|---|---|
| P1 | every surface 1.000. The three DEV-19 bakes are now 2048² (textures checked: 2048 px, shas = manifest); their seen-texel density is barrow_front 117.6, wreck 144.7 and cliff_faces_0 163.1 px/m | ≤ 1.05 | PASS |
| P2 | 20/20 at 0b72461db; working tree 20/20 | 100% | PASS |
| P3 (informational; not requested) | worst 11.53 (wood, baked); ground rock 5.57, snow 0.77; the reshade RED fails | ≤ 15.5 | PASS, water excluded (below) |
| P8 | min 0.5302 (2_2); chunks judged: 0_0 0.563, 1_0 0.553, 2_0 0.583, 1_1 0.541, 2_1 0.557, 1_2 0.564, 2_2 0.530. As delivered, **0_2 = 0.000** (below) | each chunk ≥ 0.4476 | PASS, water excluded |
| P9 trail | coverage 1.000 (flat 759 m² and not-flat 178 m² both entirely inside the field). Snow-carrying share: flat 0.68, not flat 0.26 (informational) | ≥ 0.99 | PASS |

**P1, read (the conductor's "0.86").** PT's 0.86 is 100.6 / 117.6: the bake's own texel density over the painting's. The frozen instrument displays min(painting ppm, texture ppm), because a bake cannot show more painted detail than the painting it samples. So the displayed ratio floors at 1.000. That is v1's own value, not better than v1. Sensitivity with the hidden silhouette dropped: all 1.000.

**Water in the P3 / P8 inputs: re-instrumentation, as R-C9-159.**
- **What happened.** PT's guide-camera `heather_mask.png` and `render_guide.png` were captured with the animated sea running. In 0_2, all 44 823 "drawn heather" px are sea (44 249) or its edge: the frame-differencing mask sees moving water as heather. The same capture puts the sea class at 39.2 in P3.
- **The fix.** PH now excludes self-moving pixels (the `ground_sea` and `blobs_shore_ice__*` ids from ids_built, dilated 6 px), exactly as R-C9-159's animated sea was excluded in P3 (`v159_rows` `anim`) and in P9 (`selfmove`).
- **Effect.** 44 765 px are removed; 0_2 drops below 2000 drawn px (n/a).
- **What stays the same.** The first pilot had no water, so its results are unchanged. Both the as-delivered and the excluded readings are in `results/pilot2/p8.json`.
- **PT can make the input clean** by capturing the mask with water time held (heather off/on in the same frame).

**DEV-18 (re-measured).** 28.8% of painted tuft px have no 3D heather within 24 px, down from 50.4%. On not-flat ground the figure is 12.3% (was 30.9%), and 60.2% of not-flat tufts are now covered (was 0.27%).

**P9c instrument finding (for the ruling; no bar change).** The calibrated `floe_drift` reads the TEXTURE shift by phase correlation of `luma × core`. Both frames share the same hard 0/1 core window, and that window correlates with itself at zero shift, so the texture shift reads ≈ 0 whatever the texture does. A constructed self-test shows it:
- a textured disc moved 1.36–2.25 px with its texture (rest-pose, true drift 0) reads texture shift (0.00, 0.04) with the hard window;
- so the calibrated instrument would report the full silhouette motion as drift on a CORRECT rest-pose build.

Its RED reading on R-C9-159 (1.91 px) was right for the wrong reason: world-anchored texture also reads 0. A re-instrumented reading is in `pilot_harness.floe_drift_subpx` (mean-removed, Gaussian-tapered window; locally upsampled DFT peak):
- on the self-test it gives drift 0.15–0.25 px for rest-pose and 1.26–2.00 px for world-anchored motion;
- its rest-pose floor (≤ 0.25) sits at the bar, so it does not yet separate a true 0 from the bar;
- on R-C9-159 its per-floe readings are unstable (0.10–6.10 px; the 8-texel checker in mesh UV is periodic on screen).

**P9c is not calibrated to bind.** The positive control run (`--floe-red` RED added to `ph_life.gd`) is pending, and so is a re-instrument ruling.

**PENDING (Godot, DISK HALT).** `harness/run_pilot2_godot.sh` was queued behind the heavy lock (held by JOIN1-J0F-port-emit) and was stopped before it rendered anything; disk is 18–25 GiB, under the 21 GiB gate. Still owed:
- P9 heather sway and its no-wind RED (uv −3, 11.7);
- P9 water flow and floe drift with the `--floe-red` RED (uv −29, −5.5);
- P10 frame time at the start and at the sea, plus the burn RED.

`ph_life.gd` now has the pilot hooks: `water_mat_pt` / `ground_sea` for the water pair, `blobs_shore_ice__*` floes with a plate-space 16 px checker, and `--floe-red`. They are untested in Godot until the run.

## 30. Rebuilt pilot, completed (R-C9-196; PT 8df01abcd for the fixed heather mask). Frozen bars. `results/pilot2/{p8,p9p10}.json`; renders `renders/pilot2/` (1920×1080 PNG pairs only, no film)

**R-C9-196 (1): the § 29 sea exclusion is withdrawn.** It now sits behind `PH_EXCLUDE_SELF_MOVING=1` and is off by default; binding P8 reads PT's mask as delivered. PT's fixed mask has 232 532 drawn px and 0 px on the sea.

| Row | Rebuilt pilot | Bar | Verdict | RED, same instrument |
|---|---|---|---|---|
| P8 | min 0.5302 (2_2). Judged chunks: 0_0 0.563, 1_0 0.553, 2_0 0.583, 1_1 0.541, 2_1 0.557, 1_2 0.564, 2_2 0.530; 0_1 and 0_2 n/a | each ≥ 0.4476 | **PASS** | 1 m shift: min 0.000, FAIL |
| P9 sway | 6.104 over 126 437 heather px; noise 0.002 (uv −3, 11.7) | ≥ 3× noise and ≥ 2.064 | **PASS** | --no-wind 0.000: FAIL |
| P9 flow | **1.524** over 633 887 water px (sea view uv −29, −5.5; frames 857 ms apart); noise 0.165 | > 0 ✓; ≥ 3× noise ✓; **≥ 2.064 ✗** (§ 1 row P9, clause (b)) | **> 0 YES; frozen bar FAIL** | water meshes hidden: 0.058, FAIL |
| P9 trail | coverage 1.000; flat 759 m² and not-flat 178 m² both inside the field | ≥ 0.99 | PASS | (§ 6) |
| P9c floe drift | see below | ≤ 0.25 px | **NON-BINDING** (as ruled) | — |
| P10 | p99 **16.54 ms** at the start (p50 14.65, max 19.34); **15.18 ms** at the sea (p50 12.69); M2, forward_plus, 900 frames | p99 ≤ 16.7 | **PASS** (0.16 ms headroom at the start) | 20 ms burn: 21.74, FAIL |

**P9 flow, read.** The water moves: 1.52 mean |Δ| over the water mask, 9× its noise, against 0.06 with the water meshes hidden. It reaches 74% of the frozen 2.064 floor, which is ¼ of v1's heather sway, from § 1 clause (b). R-C9-159's own sea read 6.48 on the same instrument. PT's water uses R-C9-159's shader verbatim, but with **paint_mix 1.0** (base = the painting, R-C9-194), where R-C9-159 ran 0.75. The motion layers are a smaller share of the pixel, so less of it moves. The capture interval here is 857 ms (R-C9-159's was 0.5 s nominal), so at 0.5 s the reading would be lower, not higher. **No bar moved.** Whether the frozen floor applies to the R-C9-194 water design is for the conductor.

**P10, read.** The start view at 16.54 ms is within 0.16 ms of the bar with water in the build. The sea view is cheaper (15.18 ms) because it has less heather on screen.

**P9c: RE-INSTRUMENTED (R-C9-196 (2)); stays non-binding.** `pilot_harness.floe_drift_v2`, marker in `ph_life.gd`.
- **Marker.** Floes wear a plate-space marker:
  - R = 0.95 constant, the silhouette, read as R − B so the white foam ring (R ≈ B) and the blue sea (R < B) both drop out;
  - G = aperiodic simplex noise, the texture, with no checker periodicity.
- **Shifts.** Silhouette shift is iterative Lucas–Kanade on the soft alpha, weighted to the edge band. Texture shift is the same on G, weighted to the core by a Gaussian taper. A hard shared window was the old instrument's blindness (§ 29).
- **The RED** is `ph_life.gd --floe-red`: the floes' projection is taken after the bob (`v_world += bob`), so the paint is world-anchored and swims.

| | Self-test (constructed, 4× supersampled, the same code path) | Pilot rest-pose (life_sea) | Pilot `--floe-red` (life_sea_floered) |
|---|---|---|---|
| texture shift (px) | moves with the floe / 0 | (−0.857, −0.692); identical in all 4 core quadrants | **(0.000, 0.002)** |
| silhouette shift (px) | = offset ± 0.02 | (−0.329, −0.677) | (−0.001, −0.642) |
| drift, 2-D | rest **0.001–0.007**; RED **0.242–2.231** = the motion | **0.528** | **0.643** |
| drift, horizontal only | — | **0.015** | **0.644** |

1. **The RED fails decisively.** The world-anchored texture reads exactly 0 while the floe moves, so the drift is the floe's motion.
2. **The rest-pose build passes on the horizontal axis (0.015) but not in 2-D (0.528).** The whole residual is vertical: the texture moves −0.86 px, the measured silhouette −0.33.
   - The texture's vertical motion is rigid across all four quadrants, so it is the mesh's.
   - The silhouette is not a rigid reference vertically: its alpha area changes 1.4% between frames. The floe bobs through the sea surface (the bob's world-Y component), so the waterline and foam occlude a different part of its edge in each frame. The two silhouette estimators also disagree by 0.1 px (centroid −0.42 vs LK −0.33).
   - The horizontal bob does not cross the waterline, and there the silhouette is rigid and the separation is clean.
3. **Limits.**
   - **One floe.** Only 1 of the 3 measurable floes lies wholly inside the painted plate in this view. Floes outside it carry clamped-edge streaks, and their vertical texture shift is ill-posed.
   - **Unequal capture intervals.** m0/m1 are 0.5 s apart by request but land on different TIME values per run, so the motion differs between control and RED.
   - **A ruling is needed before P9c can bind:**
     - (a) score the horizontal component only, with this rationale pre-registered;
     - (b) capture the silhouette from a mesh-attached reference that the water cannot occlude (e.g. the floe drawn with depth test off for the marker shots);
     - (c) add more in-plate floes, by taking a view centred on the floe field.

     **(b) is PH's recommendation.** It keeps the 2-D metric and removes the confound at its source.

## 31. P9c PRE-REGISTRATION (R-C9-197): the depth-test-off marker shot. Committed BEFORE measuring.

**Instrument.** `pilot_harness.floe_drift_v2` (§ 30) is unchanged. `p9c_measure(dir, view_uv)` aggregates it.

**Capture.** `ph_life.gd life … --floe-pairs 5 [--floe-red]`. For the marker shots only, each floe material's shader is re-derived from its live code with two changes:
- `depth_test_disabled, unshaded` added to its render_mode;
- `ALPHA = 1.0` added, so it draws in the transparent pass after the opaque sea.

The waterline therefore cannot occlude the bobbing silhouette, and lighting cannot modulate the marker's R channel. Geometry, the bob (TIME) and the UV law are untouched. The marker is as § 30: R = 0.95, G = simplex noise, B = 0.5. hide_floe is taken with the floes hidden.

**The RED** (`--floe-red`) moves the projection's `v_world` by the bob, so the paint is world-anchored and swims.

**View, floes and pairs.**
- **View:** uv (−29, −5.5), the § 30 sea view.
- **Floes:** a floe is measured only if its bbox (+12 px) lies wholly inside the plate's screen rect at ground z = 0. That rect is `plate_rect_on_screen` = (500, 0, 1920, 861) less a 12 px margin. Floes outside the plate wear clamped-edge streaks, not paint.
- **Expected count: 1.** In the pilot plate's ID render only `blobs_shore_ice__blob_11` lies wholly inside; blob_0 is cut by the plate edge, and the other 15 are outside the pilot window.
- **Pairs:** 5 marker pairs, m0 and m1 0.5 s apart, consecutive pairs 0.7 s apart.

**Statistic and bars.** The per-pair median floe drift (2-D, px), then the median over pairs.
- **Rest-pose build:** PASS iff ≤ 0.25 px (the frozen § 1 bar).
- **RED:** must read > 0.25 px, i.e. FAIL.
- **Validity:** a pair whose median silhouette motion is < 0.25 px cannot separate the two, and is reported but not counted.
- **Pass condition for P9c to be "shown":** rest-pose PASS **and** RED FAIL on this protocol. Until then P9c stays non-binding.

**Self-test (§ 30, unchanged):** rest 0.001–0.007 px; RED = the motion ± 0.02.

**§ 31 A1 (amendment, committed BEFORE the measurement that counts).**
- **What failed.** The depth-test-off / unshaded / ALPHA = 1 marker shader drew **no marker**. In `renders/pilot3/p9c_{rest,red}` (first attempt) the floe region of floe_m0 matches hide_floe, apart from the water's own animation. There are no shader errors in the log, and `p9c_measure` finds 0 floes in all 5 pairs of both runs.
- **The mechanism now.** It keeps the floe's own opaque shader, as in § 30. The **sea meshes (`ground_sea`) are hidden for all marker shots and for hide_floe**, so no waterline can occlude the bobbing silhouette, and the background is static between the shots.
- **Unchanged.** Intent, view, floe rule, pairs, statistic and bars are all as § 31. The first-attempt renders are kept as evidence and are not scored.

## 32. PT 9c53bc067 (paint_mix 0.75): P9 flow, P10, and P9c as pre-registered (§ 31 + A1). `results/pilot3/p9c_flow_p10.json`; renders `renders/pilot3/`

| Row | Measured | Bar | Verdict |
|---|---|---|---|
| P9 flow | **1.551** over the water mask (uv −29, −5.5; 886 ms apart); noise 0.165. It was 1.524 at paint_mix 1.0 | ≥ 2.064 and ≥ 3× noise | **FAIL** (frozen bar). Hidden-water RED 0.053 |
| P10 | p99 **16.20 ms** at the start (p50 14.62, max 16.77); **14.49 ms** at the sea | ≤ 16.7 | **PASS** |
| P9c rest-pose | per pair 0.007 / 0.006 / 0.013 / 0.059 (motion 0.94–3.06 px). Pair _2 not counted: motion 0.17 < 0.25. **Median 0.010 px** | ≤ 0.25 | **PASS** |
| P9c RED (swimming) | per pair 0.882 / 2.953 / 0.924 / 2.607, each equal to that pair's motion. **Median 1.766 px** | must be > 0.25 | **FAIL, as required** |

**P9c is shown** under the pre-registered protocol: the rest-pose build passes, the swimming RED fails, and both use one floe (blob_11, the only floe wholly in the plate) over 4 counted pairs.
- With the sea hidden, the silhouette and texture shifts agree to ≤ 0.06 px on the build.
- On the RED, the texture reads 0.000 while the floe moves.
- Whether it now binds is the conductor's call.

**P9 flow, read: the paint_mix fix did not reach the floor.** 0.75 against 1.0 moved flow 1.524 → 1.551 (+2%), so paint_mix was not the driver.
- **Pilot sea:** mostly calm. Per-pixel |Δ| has median 0.33 and p90 11.7, and 18% of px exceed 2.
- **R-C9-159's sea (6.48):** median 0.67, p90 63, and 39% of px exceed 2. It was a smaller water region (131 k px against 851 k) that was mostly foamy shore.
- **So the difference is the sea's composition** in the measured view (open water against surf), not the shader's mix. No bar moved; the next build or view decision is the conductor's.

## 33. PT 8fd69fafc (R-C9-159's foam field ported; paint_mix 0.75): P9 flow, P10, P2. `results/pilot4/p9_flow_p10_p2.json`; renders `renders/pilot4/`

| Row | Measured | Bar | Verdict |
|---|---|---|---|
| P9 flow, **the same water mask** (pilot3's mask, 651 295 px, applied to the 8fd69fafc frames) | **3.444**; hidden-water RED 0.067 | ≥ 2.064 and ≥ 3× noise (0.152) | **PASS** |
| P9 flow, the instrument re-deriving its mask from this run's frames | 1.914 over 623 581 px | same | FAIL (read below) |
| P10 | start: run 1 p99 **17.32** (max 24.14), repeat **16.03** (max 16.48); sea: 13.87, repeat 14.11 | p99 ≤ 16.7 | **run 1 FAIL / repeat PASS**, see below |
| P2 | 20/20 at 8fd69fafc | 100% | PASS |

**Why the two flow readings differ (an instrument leak, not the water).** `sway()` re-derives its exclusions from shots taken at different instants: floes from floe_m0 against hide_floe, heather from f0 against hide_heather. With the foam now animated, the foam moving between those shots is classed as floe or heather and dropped from the water mask.
- **Dropped:** 61 140 px fall out of the mask (49 572 as "floe", 10 083 as "heather").
- **Their motion:** 20.8 mean |Δ|. These are the surf the row exists to see.
- **Confirmation:** taking the floes from the marker's geometry instead (R − B > 40, P9c) gives 4.092 over 757 811 px.
- **Binding reading:** the conductor asked for the same water mask, so 3.444 PASS is the binding reading. The leak is recorded for a re-instrument ruling: exclusions should come from geometry (the marker, ID renders), not cross-time differences.

**P10, read.** The start view's first run had p99 17.32 with one long tail (max 24.14). The repeat on the same build gives 16.03 / max 16.48, so the build costs about 0.1–0.6 ms more than 9c53bc067 (16.20). The frozen protocol is a single 900-frame run; it never specified what a repeat means. I report both and flag the ruling: run 1 as the binding FAIL, or a pre-registered repeat rule. Bars unchanged.

## 34. P10 REPEAT RULE, PRE-REGISTERED (R-C9-199). Committed BEFORE any re-measure.

**Ruling.** On 8fd69fafc, P10 = **FAIL**: 17.32 ms, the first run, as measured. The repeat (16.03) is not used.

**Rule, from the next P10 measurement on:**
- **Runs.** 3 runs of the SAME segment: `ph_life.gd perf` at uv (0, 0), the scripted 4-point walk loop, 900 frames, vsync off, uncapped, 1920 × 1080, `bv2f_pilot_painted.tscn`, `BV2F_VARIANT=art`.
  - Each run is a fresh Godot process under the heavy lock, run back to back (`run_p10_rule.sh`).
- **Statistic.** The **WORST** p99 of the three. **PASS iff worst p99 ≤ 16.7 ms.** This is stricter than a single run, never looser.
- **Reporting.** All three runs are reported (p50, p99, max). No run is discarded or re-taken.
  - If a run crashes or writes no perf.json, P10 is VOID for that build, and the three are re-run as a set.
- **Sea view.** The sea view (uv −29, −5.5) is measured under the same 3-run worst-p99 rule and reported. It binds under the same bar.
- **RED unchanged.** The 20 ms burn must FAIL; it is a single run.

## 35. P10 under the § 34 rule + P2 on PT c578db842 (load-time warm-up); THE PILOT'S FINAL ROW TABLE (for jack-ryan's Gate-2)

**P10 (§ 34 rule; `results/pilot5/p10_rule_p2.json`; `renders/pilot5/p10_rule/`).**

| View | Run 1 p50 / p99 / max | Run 2 | Run 3 | Worst p99 | Verdict |
|---|---|---|---|---|---|
| start uv (0, 0) | 13.42 / **19.40** / 30.55 | 13.55 / 15.21 / 16.13 | 13.47 / 15.40 / 19.79 | **19.40** | **FAIL** |
| sea uv (−29, −5.5) | 11.71 / 13.22 / 13.80 | 11.69 / 13.32 / 13.75 | 11.69 / 13.40 / 14.17 | 13.40 | PASS |

- **Burn RED:** p99 21.55, FAIL as required. **P2:** 20/20 at c578db842.
- **Observation (not a re-take).** The warm-up lowered the median by about 1.1 ms (p50 14.6 → 13.5). The FIRST fresh run of each batch still carries a tail: 17.32 on 8fd69fafc, 19.40 now, with runs 2–3 at 15.2–15.4.
- `ph_life` records no per-frame times, so where the slow frames fall in the 900 is not yet known. A per-frame dump would localise it; that change is to the instrument, not the bar. PT's own runs (15.16 / 15.31 / 15.16) were not first-of-batch runs under the heavy lock.

**P3 on the current inputs (as delivered, no exclusion).** Worst class: **ground: sea 27.77** > 15.5, so FAIL. The guide-camera render carries the animated water (foam and crests over the painting, by design); the other classes are ≤ 12.73. With R-C9-159's animated-pixel exclusion (`v159_rows` `anim`; `PH_EXCLUDE_SELF_MOVING=1`) it is 11.53, PASS. R-C9-196 did not adopt that exclusion for P8; there PT fixed the input instead (water hidden for the shots). **P3 needs the same treatment or a ruling**: render_guide with the water held or hidden.

### The pilot's final row table (Phase 2′, bv2art pilot window, plate px [0, 0, 4096, 2560]; frozen bars)

| Row | Binds | Final reading | Bar | Verdict | Build measured | PH commit (§) |
|---|---|---|---|---|---|---|
| P1 texel density | yes | all 1.000 (DEV-19 bakes 117.6–163.1 px/m) | ≤ 1.05 | **PASS** | f36284352 bakes; re-read c578db842 | 37193eb63 (§ 29); this commit |
| P2 lineage | yes | 20/20 | 100% | **PASS** | 186743b58 | § 37 |
| P3 render vs painting | yes | worst 11.53 (wood, baked); sea 5.73 with the DEV-5 motion layers removed (painted base only); lit-plane RED 22.87 | ≤ 15.5 per class | **PASS** (R-C9-201: water is a mover; § 36) | c578db842 | § 36 (R-C9-201 commit) |
| P4 texture | yes | ice 0.61–0.67 (bar 0.126); snow 0_2/1_2 0.40 (bar 0.281) | v1 LOO maxima | **FAIL** (origin: the paint transfer, § 27) | painting 901f3087 (unchanged) | 4bd299a18 (§ 26), 55099e701 (§ 27) |
| P5 seams | yes | MAD 11.97; seam 0.585 | ≤ 13.09; ≤ 0.799 | **PASS** | painting 901f3087 | 4bd299a18 (§ 26) |
| P6a invention | yes | 1 declared, 5 MATERIAL (conductor triage), 0 invented | 0 invented | **PASS** | painting 901f3087 | 55099e701 (§ 27) |
| P6′ presence / placement / scale | yes | 0 missing / extra / hidden; containment ≥ 0.974; 0 of 89 over 1.10 | § 16 | **PASS** | ids_built 776e265f0; re-read c578db842 | 4bd299a18 (§ 26); this commit |
| P8 heather precision | yes | min 0.5302 (2_2), 7 chunks judged; RED fails | each ≥ 0.4476 | **PASS** | 8df01abcd mask; re-read c578db842 | 2fa1f5229 (§ 30); this commit |
| P9 sway | yes | 6.104; no-wind RED 0 | ≥ 3× noise and ≥ 2.064 | **PASS** | 0b72461db+ (renders/pilot2) | 2fa1f5229 (§ 30) |
| P9 flow | yes | **3.444** on the pre-registered mask; hidden-water RED 0.067 | ≥ 2.064 | **PASS** (R-C9-199) | 8fd69fafc | 4ec1c5bc8 (§ 33) |
| P9 trail | yes | 1.000 (flat 759 m², not-flat 178 m²) | ≥ 0.99 | **PASS** | 0b72461db | 37193eb63 (§ 29) |
| P9c floe drift | **yes** (BINDING since R-C9-198; corrected R-C9-201) | rest-pose 0.010 px; swimming RED 1.766 px | ≤ 0.25 | **PASS** (RED fails) | 9c53bc067 | 3888c0d74, 96509f727, 291a54992 (§§ 31–32) |
| P10 frame time | yes | start worst p99 **16.54** (15.23, 15.06); sea worst 13.10; burn RED fails | worst of 3 ≤ 16.7 (§ 34) | **PASS** (0.16 ms headroom; c578db842 was FAIL at 19.40) | 186743b58 | 02de8260f (§ 34); § 37 |
| P11 ABX | yes | judge 1 27/40, inconsistency 0.50; judge 2 24/40, 0.40 | ≤ 26/40; inconsistency ≤ 0.25 | **VOID × 2**; the void rule needs re-instrumenting (§ 28) | 47bb1a054 stills | f3af8d82c (§ 28) |
| P7 floor/scatter | no | — | — | retired (charter § 15) | — | — |
| P6′ extent | no | — | — | retired (charter § 15) | — | — |
| P6b silhouette IoU | no | — | — | not in the pilot plan | — | — |

**Open for rulings** (items 1–2 superseded by § 36):
1. ~~P3's animated-water input~~: resolved by R-C9-201 (§ 36).
2. ~~P10's first-run tail~~: traced (§ 36); it is a real stutter after control, now with PT.
3. P11's void rule (§ 28).
4. P9c binding.
5. P9 flow's mask derivation (§ 33: exclusions from geometry, not cross-time differences).
6. P4's paint transfer (§ 27; M2′).


## 36. R-C9-201: P10 traces aligned to the load timeline; P3's sea with the motion layers removed; P9c row corrected. `results/pilot6/`; renders `renders/pilot6/`

**(1) P10: where the tail sits.** `ph_life.gd perf` now writes `trace.json`: every pre-roll and window frame time (ms), with zero at ready_done as the tool sees it. These are 3 fresh runs at the start view, c578db842, for diagnosis. They are not a § 34 re-measure; P10 on c578db842 stays FAIL at 19.40.

| Run | ready_done after engine start | Window starts after ready_done | Pre-roll max | p99 / max | Frames > 16.7 ms (time after ready_done) |
|---|---|---|---|---|---|
| 1 | 10.44 s | 2.69 s (after the 180-frame pre-roll) | 81.0 ms | 15.37 / 30.96 | **3 consecutive: 31.0, 29.3, 28.0 ms at 3.30–3.36 s** |
| 2 | 10.47 s | 2.52 s | 98.5 ms | 14.97 / 19.16 | 2 consecutive: 18.5, 19.2 ms at 11.43–11.45 s |
| 3 | 10.29 s | 2.46 s | 30.9 ms | 14.96 / 20.40 | 1: 20.4 ms at 4.86 s |

- **No load frames are captured.** Both tools start the 900-frame window ≥ 2.4 s after ready_done, after a 180-frame driven pre-roll (where the load-adjacent spikes of 31–98 ms sit, uncounted). So no capture definition needs pre-registering.
- **The tail is real, and it comes after control:** short clusters of 1–3 hitches (18–31 ms) while the knight walks the loop, at varying times. A cluster of about 9 or more frames drives the p99 above 16.7; that is what 17.32 and 19.40 were.
- **Reconciled with PT.** PT measured with this same instrument (`ph_life.gd perf`, same segment). PT's own before/after record (`fid/pt/perf/p10_before_after.json`) shows the same first-run tail after the warm-up: p99 18.14, max 32.8, then 15.26 / 15.41. The published 15.16 / 15.31 / 15.16 came from a later batch.
- **For PT:** hitch clusters of 28–31 ms frames 0.6 s into the walk (run 1), with sporadic singles later. The trace files localise them in time.

**(2) P3's sea with the DEV-5 motion layers removed** (`ph_p3_sea.gd`: PT's guide-camera framing; the water shader re-derived; `results/pilot6/p3_sea.json`).

| Reading | Sea mean \|Δ\| | Bar | Verdict |
|---|---|---|---|
| as delivered (motion layers live) | 27.77 | ≤ 15.5 | — (water is a mover: exempt, R-C9-201) |
| motion layers held at rest (TIME = 0, layers drawn) | 21.62 | ≤ 15.5 | — |
| **painted base only** (`ALBEDO = base`: the painting × 0.75 + deep_col × 0.25) | **5.73** | ≤ 15.5 | **PASS** |
| **RED: a lit plane** (StandardMaterial3D, deep_col) in place of the base | **22.87** | ≤ 15.5 | **FAIL, as required** |

- **Binding P3 on that capture:** every class ≤ 15.5. The worst is 11.53 (wood, baked), the same as before; the swap touched only the sea. **P3 PASS.**
- **Why "at rest" still fails:** holding TIME still freezes the layers but does not remove them. The swell darkening, crest bands and foam lace are drawn over the painted base, so the static frame still differs from the painting by 21.6. The base-only read is the one that isolates the painting's own sea.

**(3) Table corrected (§ 35).** P9c has been BINDING since R-C9-198, so it reads PASS: 0.010 px, with the swimming RED failing at 1.766. P3 now reads PASS per (2). Remaining binding FAILs on the pilot (as of § 36): **P4** (paint transfer, § 27) and **P10** (19.40, real stutter after control; superseded by § 37: P10 PASS on 186743b58). P11 is VOID × 2 pending the void-rule ruling (§ 28).

## 37. PT 186743b58 (stutter fix): P10 under § 34, measured independently with PH's tool; the still diff; P2; THE FINAL TABLE (§ 35, as corrected) for Gate-2. `results/pilot7/p10_rule_still_p2.json`

**P10 (§ 34; `ph_life.gd perf` with `trace.json`; `renders/pilot7/p10_rule/`).**

| View | Run 1 p99 / max | Run 2 | Run 3 | Worst p99 | Verdict |
|---|---|---|---|---|---|
| start | **16.54** / 28.58 | 15.23 / 18.24 | 15.06 / 18.89 | **16.54** | **PASS** (0.16 ms headroom) |
| sea | 13.01 / 13.81 | 13.10 / 18.77 | 13.10 / 13.51 | 13.10 | PASS |

- **Burn RED:** 21.68, FAIL as required. **P2:** 20/20 at 186743b58.

**PT's vsync claim, checked against PH's traces.**
- `ph_life` switches vsync off at the start of `_perf`, before the 180-frame pre-roll. Every run's largest pre-roll frame (28–30 ms) is **pre-roll frame 0**, the switch, outside the measured window. This is so on 186743b58, and it was already so on c578db842 (§ 36 traces: frame 0 or 1).
- So the ~30 ms control-start frame PT names was never measured by PH. **No exclusion is used, and none is needed.**
- On c578db842 the pre-roll also had 68–81 ms frames at pre-roll frames 21–23 (first footsteps). On 186743b58 they are gone; PT moved them into load.
- **What still sits on the bar's edge is not the vsync frame.** Start run 1 has a window cluster of 7 frames (16.9–28.6 ms) at 12.35–12.48 s after ready_done, mid-walk. That stutter after control survives, and it is why the start view passes with only 0.16 ms of headroom.

**Look unchanged (still diff, 0 images).** `ph_p3_sea.gd` rg_base on 186743b58 against c578db842, same guide camera, wind held, snow hidden, water base only:
- 48 782 px differ, 23 334 by more than 8 levels;
- of those, 91% are the bobbing floes (`blobs_shore_ice`, 21 334) and 7% the sea around them (1 747). The floes' bob runs on TIME, so the two captures catch a different phase;
- the remaining 2% are shore-ice edges (217), path (34) and snow (2); heather 0.

This is a time-phase difference, not a look change.

**FINAL ROW TABLE: § 35, as corrected by §§ 36–37.**
- **Binding PASS:** P1, P2, P3, P5, P6a, P6′, P8, P9 sway, P9 flow, P9 trail, P9c, P10.
- **Binding FAIL:** **P4** (texture: the ice and the coastal snow; their origin is the paint transfer, not the guide, § 27).
- **VOID:** **P11** × 2, pending the void-rule ruling (§ 28).
- **Retired / not in plan:** P7, P6′ extent, P6b.

## 38. PRE-REGISTRATION before the Phase 2″ repaint (R-C9-203/204/205; jack-ryan pilot Gate-2 folds F-4, F-5). Committed BEFORE any measurement on the repainted build. No bar moves.

### F-4 (a) — P9 flow: the water mask from GEOMETRY (`pilot_harness.flow_geo`; `ph_life.gd` `geo_mask.png`)
**The defect (§ 33).** `sway()` built its water mask from cross-time differences (f0 against hide_water, floe_m0 against hide_floe, f0 against hide_heather). Animated foam that moved between those shots was dropped from W.

**The fix.**
- **Capture.** In the `life` capture, one extra frame, `geo_mask.png`: the sea meshes drawn flat unshaded pure green and the floes flat unshaded pure red, same camera, one frame.
- **Mask.** W = green px (G > 200, R < 60, B < 60), eroded 3 px, minus red dilated 6 px. Membership no longer depends on time.
- **Flow.** Mean |f1 − f0| over W. The RED is the hidden-water pair over the same W.
- **Noise.** Measured outside the green/red geometry (dilated 6 px), the heather and the self-moving px.
- **Bar unchanged:** flow ≥ 2.064 and ≥ 3× noise. The hidden-water RED must FAIL.
- **View.** The P9 flow view is the § 33 sea view (uv −29, −5.5) when the new coast keeps open water there. Otherwise it is the view of the window's largest open-water (ground_sea) area in the new build's ID render, chosen by the same argmax rule as (b) before any capture.

### F-4 (b) — P9c on a floe-field view with n ≥ 3 (`pilot_harness.floe_view_choose`, `p9c_measure_v2`)
- **Floes.** The build's BOBBING floes: the ids it gives a bob phase (`bv2f_pilot.gd` water dress; `blobs_shore_ice__*` today).
- **View.**
  - The plate px of each floe come from the build's own `ids_built.png`. A floe counts if its bbox + 12 px lies wholly inside both the plate and the 1920 × 1080 screen.
  - The view is the 0.5 m-grid centre (uv) with the most counted floes; ties go to the smallest distance to their mean centre.
  - It is decided from the ID render **before** any marker shot, and recorded.
- **n.** P9c requires **≥ 3 floes in that view**; otherwise it is reported n-insufficient and stays non-binding. On today's pilot the rule finds 1 (blob_11), so it is insufficient, as known.
- **Capture.** `ph_life.gd life <view> --floe-pairs 10`, plus `--floe-red`. The marker is § 31 A1: the floes' own shader, sea hidden for the marker shots.
- **Statistic.** Pooled over every (floe, pair) sample with silhouette motion ≥ 0.25 px: the **median drift**. Each floe's own median is reported.
- **Bars as § 31.** The rest-pose build PASSES iff ≤ 0.25 px; the RED must read > 0.25.

### F-5 — P11 v3: embedded catch trials (`p11_abx3.py`; jack-ryan pilot Gate-2 (1))
**Design.**
- The 40 scored trials and 10 repeats are v2's construction.
- **Plus 12 CATCH trials**, format-identical, shuffled in (62 images):
  - **Catch pair:** v1 against R-C9-159. Its own judge scored 40/40 (calibration table § 1 row P11; § 28), the most discriminable pair on record. v1 against half-density scored 37/40 and 33/40.
  - **Content:** the scored trials' own content control and guards, applied set-wide. A/B are guarded at ≤ 50% against every A/B of the set; X at ≤ 25% against every X of the set, so no catch X repeats a scored X (checked: 0 shared).
  - **Balance:** X from v1 in 6 and from R-C9-159 in 6; correct letter A in 6 and B in 6.
- JUDGE.md says "several versions".

**Rule.**
- **VALID iff ≥ 10/12 catches are correct.** An always-A or always-B set scores 6/12, so it is VOID by construction.
- **PASS iff ≤ 26/40 scored** (unchanged).
- Repeat inconsistency is a **reported, non-binding diagnostic**.

**(a) Operating table** (`p11_abx3.py table`; exact binomial, Monte Carlo n = 200 000 agrees to ±0.0005):

| Judge | P(valid) | P(VOID) | P(valid ∧ PASS) | P(valid ∧ FAIL) |
|---|---|---|---|---|
| guesser (catch ½, scored ½) | 0.0193 | **0.9807** (≥ 0.95 ✓) | 0.0189 | 0.0004 |
| always-A | 0 | **1** (6/12) | 0 | 0 |
| attentive (catch 0.95), builds indistinguishable | 0.9804 | 0.0196 | **0.9616** (≥ 0.9 ✓) | 0.0189 |
| attentive (catch 0.99), indistinguishable | 0.9998 | 0.0002 | 0.9806 | 0.0192 |
| attentive (0.95), discriminable p = 0.75 | 0.9804 | 0.0196 | 0.1012 | 0.8792 |
| attentive (0.95), discriminable p = 0.85 | 0.9804 | 0.0196 | 0.0014 | 0.9791 |

**(b) Catch-pair calibration.** The catch pair's per-trial accuracy is measured on the fresh G2-B2 judges below: their catches, pooled, **≥ 0.95**. If it is lower, the catch pair fails calibration and P11 v3 does not bind.

**Risk, disclosed before any judge.** Under content control the catch crops are snow (12/12; the half-density set has 11 snow + 1 heather). The 40/40 calibration judge saw uncontrolled content (sea, cliffs). Whether snow-only catches hold ≥ 0.95 is exactly what (b) measures.

**Self-test on both keys.**
- The key itself scores 40/40 scored and 12/12 catch: valid.
- Always-A scores 6/12 catch: VOID.
- Alternating A/B scores 5–8/12 catch: VOID.

**(c) G2-B2 re-run under v3**, judge-ready (`p11_abx3.py g2`; keys in `p11/keys/abx3_*.json`, outside the judge dirs):
- `p11/abx3_g2v3_v1rec_vs_v1head/` — v1 record-time against v1 HEAD. Must read **valid ∧ PASS**.
- `p11/abx3_g2v3_v1_vs_halfdensity/` — v1 against half-density. Must read **valid ∧ FAIL**.

Scoring: `python3 p11_abx3.py score <set> <answers.json>`.

**Disposition.**
- If (b) or (c) fails, P11 is **recorded as dropped from the parity claim at M3′, not silently absent** (F-5).
- The pilot's two v2 answer sets are **not** re-scored. Pilot P11 stays VOID.

### P4 references after Matt's M2′ answer (R-C9-203: sketch A's ice is a Matt-ruled palette DEV for the ice class)
**ICE** (binding; replaces the v1-tarn reference **for the ice class only**).
- **Reference.** Sketch A's mere (`sites/BV3r2-A.png`, make_bv2art's MERE polygon, eroded 6 px), gated to ice px **b\* ≤ 2**. The gate drops the reeds and rocks inside the polygon: 22% of polygon px. The same gate applies to the painted side.
- **Reference values (frozen now).** Median L\*a\*b\* **(72.9, −1.0, −9.4)**; p10 (54.6, −3.7, −16.5); p90 (85.2, 1.8, −1.6).
- **(i) Palette.** Each painted ice chunk (P4's chunk rects, ice class on ground less tufts, eroded 3 px, gated b\* ≤ 2, ≥ 20 000 px) is compared by median ΔE76 against the sketch median.
  - **Bar: ΔE ≤ 9.40**, sketch A's own leave-one-quadrant-out maximum. Quadrant medians: (73.4, −1.1, −9.5), (69.2, −0.8, −9.9), (79.9, 0.0, −6.5), (70.3, −1.5, −11.0); LOO ΔE 0.82 / 4.47 / 9.40 / 4.76.
- **(ii) Texture at the sketch's own scale.** The painting is box-downsampled to sketch A's 24 px/m (factor 4.192). P4's `spectrum_shape` (64 px windows, ≥ 70% coverage, step 32) gives an RMS distance to the sketch's pooled spectrum.
  - **Bar ≤ 0.116**, the sketch's leave-one-quadrant-out maximum. That quadrant LOO is thin: 9 / 2 / 2 / 11 windows; disclosed.
- **Reported, non-binding.** The Lab-histogram Hellinger against the sketch. The medium and exposure differ: even v1's tarn reads 0.639.
- **Today's readings, for the record (not a measurement of the repaint).**
  - Pilot ice: ΔE ≈ 9.5 (fails by 0.1); spectrum 0.036 (passes); Hellinger 0.66–0.76.
  - v1's tarn: ΔE ≈ 23.4 (fails); spectrum 0.070.

**COASTAL SNOW** (binding; **unchanged reference**).
- Matt's M2′ ruling named the ice class only, and an ice palette ruling does not clear the snow (jack-ryan P-2). So coastal snow, like all snow, binds against **v1's snow** with the frozen § 3 bars: hist ≤ 0.281, spectrum ≤ 0.097, every snow chunk.
- **Reported, non-binding diagnostic.** Each coastal chunk's snow Hellinger against the pilot's own **inland** snow pool, made of the chunks without shingle, sea or shore ice in the new class map. This separates a coastal shift from a global one.
- **Coastal chunks.** Defined from the new guide's class map: any chunk containing shingle, shore_ice or sea ≥ 2% of its px.

## 39. P11 v3 CALIBRATED — BINDING (R-C9-207). `results/p11_abx3_g2_scores.json`; answers `p11/answers/abx3_g2v3_*.json`

| Set | Catch | Valid | Scored | Verdict | Required (§ 38 (c)) | Repeat inconsistency (diagnostic) |
|---|---|---|---|---|---|---|
| v1 record-time vs v1 HEAD | **11/12** | yes | **22/40** | **PASS** | valid ∧ PASS ✓ | 0.20 |
| v1 vs half-density | **12/12** | yes | **35/40** | **FAIL** | valid ∧ FAIL ✓ | 0.20 |

- **(b) Catch pair, pooled over the two fresh judges:** 23/24 = **0.958 ≥ 0.95** ✓. This was the snow-only risk disclosed in § 38; it held.
- **The gate now behaves as designed:** both judges are valid; the null pair passes and the constructed degradation fails. Under v2 the same pair of conditions was reachable ~5% of the time (§ 28).
- **What binds from now on:** P11 is **v3**: `p11_abx3.py build3` for the candidate's stills and `score3` for the answers. It binds at M3′ over the whole site. The pilot's v2 answers stay VOID; they are not re-scored.

## 40. P6′ on LV's M1″ blockout (3686cea98; R-C9-210, before the pilot repaint). Frozen bars (§ 16). `results/p6prime_bv2pp_3686cea98.json` (`harness/p6prime_art.py`)

**Inputs.** `layout_bv2art.json`, `placed_fit_bv2art.json`, `ids_art.png` (sha 5be8c068…, matches the manifest), level.json at 3686cea98.
- The slot crosscheck passes: 52 layout placements against 52 level box slots, 0 mismatches.
- New pieces are measured as slots of the layout's models: the cliff kit, `talus`, `sea_stacks`, the stair blocks (`stair_*`) and the pack ice (`ice_*`).
- `ice_*`, `stair_*`, `mere_*`, `ground_*`, `curtain_*` and `door_*` ids are in the non-model / procedural / slab classes, which P6′ excludes as in § 21.

| Component | Result | Bar | Verdict |
|---|---|---|---|
| I-4 RED (every slot prism shifted 1.5 m) | 6 of 12 objects below containment 0.7872 | must FAIL | **FAILS, as required** |
| presence: missing / extra | 0 / 0 | 0 / 0 | ✓ |
| presence: terrain-hidden ≤ 0.50 unless declared | **ring_stones #5 0.96, #6 1.00, #7 1.00; wreck 0.558** | ≤ 0.50 | **RED** |
| placement: containment | all ≥ 0.9722 (logs); palisade 0.9909; the other 10 objects 1.000 | ≥ 0.7872 | PASS |
| scale: anisotropy | 105 instances, 0 over 1.10; 0 record mismatches against PH | ≤ 1.10 | PASS |

**P6′ = RED (presence).** Reported, not adjusted; per § 15 this is a HALT for an LV fix, not a bar move. No hidden-by-design is declared anywhere in the layout (`burial_by_design`: none), so none is accepted.

**Attribution.**
- **ring_stones #5, #6, #7.** These are the three FALLEN stones (`lie_z90`, slab 1.4 × 0.755 × 0.537 m), still at **z = −0.15**, the old ground level. The R-C9-204 terrain levels raised the ground under them to **3.86 / 5.49 / 4.99 m**, so each lies 3.5–5.1 m under the plateau.
  - Standing stone #4 was re-seated (z 3.54 against terrain 4.21: 0.67 m sunk, within the bar).
  - The fallen ones were missed by the re-seat. **Fix: re-seat them on the new terrain.**
- **wreck.** Seated at **z = −5.2** = ice top − `WRECK["sink"]` 1.0 m (make_bv2art.py:603, "re-seated at the beach foot on the shore ice"). The sloped beach rises around it (terrain −6.5 … −0.6 across its footprint; median −3.38), so the shingle covers the stern side and 55.8% of its silhouette shows ground.
  - The 1 m sink may be design intent ("heeled and half-sunk in the shore ice" is in the brief), but it is **not declared** in the layout.
  - **Fix: either declare `burial_by_design` on the wreck with its reason (accepted only as declared, per R-C9-181), or lower the beach under the hull / raise the hull.**

**Harness note.** `p6prime_art.py`'s attribution read `instances` on a single-GLB model and crashed on the wreck. It now uses `PP._instances()`. This is a reporting-path fix; no measurement changed.

## 41. P6′ on LV's final Phase-1″ render (09ba67b23; R-C9-212). Frozen bars. `results/p6prime_bv2pp_09ba67b23.json`

**Inputs.** The slot crosscheck passes: 60 layout placements against 60 level slots, 0 mismatches. `ids_art.png` sha 3c5ecf04…, matching the manifest.

| Component | Result | Verdict |
|---|---|---|
| I-4 RED (1.5 m shift) | 6 of 12 objects below 0.7872 | **FAILS, as required** |
| missing / extra | 0 / 0 | ✓ |
| terrain-hidden ≤ 0.50 | **ring_stones #5 0.897, #7 0.642**; #6 0.323 ✓, #4 0.375 ✓; **wreck 0.304 ✓** (under the bar even without its declaration) | **RED** |
| placement | min 0.9722 (logs); all others ≥ 0.99 | PASS |
| scale | 113 instances, 0 over 1.10, 0 record mismatches | PASS |

**P6′ = RED (presence), again: two of the three fallen stones.** It is reported, not adjusted, and is a HALT for an LV fix.

**Attribution.** The stones were re-seated, but at a z below the slope they lie on. Neither has a declared burial, so both stay RED.

| Stone | Slab z | Terrain under its footprint | Terrain at its centre | Slab top (lying, 0.537 m thick) | Hidden share |
|---|---|---|---|---|---|
| #5 | 3.366 | 3.53–4.21 | 3.86 | 3.90 | 0.897 |
| #7 | 4.324 | 4.20–5.35 | 4.98 | 4.86 | 0.642 |

- **#5:** the ground covers most of the slab.
- **#7:** the upslope half is under ground.
- **#6 reads correctly:** z 5.127 against terrain 5.15–5.59, hidden 0.323.

**Fix:** seat each fallen slab on the slope (tilt it to the terrain normal, or set z to the footprint's upslope height less a small sink), or declare the burial with its reason.

**The wreck.** Its declared 34.4% cradle reads 0.304 on PH's instrument, under the 0.50 bar. The declaration is not needed for it to pass.

## 42. P6′ on LV's final blockout render (1f9eb1dc7; R-C9-230/231; gates the pilot repaint). Frozen bars. `results/p6prime_bv2pp_1f9eb1dc7.json`

**Inputs.** `ids_art.png` sha 9f01c9a7…, matching the manifest; layout and level at 1f9eb1dc7.

| Component | Result | Verdict |
|---|---|---|
| I-4 RED (1.5 m shift) | 6 of 13 objects below 0.7872 | **FAILS, as required** |
| slot crosscheck (layout of record → level slots) | **61 layout placements against 60 level slots; 1 mismatch: `slope_stone_0`** | **FAIL** |
| missing / extra (over the level's models) | 0 / 0 | ✓ |
| terrain-hidden ≤ 0.50 unless declared | **gully_rock #1 0.738** (gully_col_e_1); gully_rock #0 0.477 (under the bar); wreck 0.327 ✓; ring_stones 0.03–0.17 ✓ | **RED** |
| placement | min 0.9722 | PASS |
| scale | 113 instances, 0 over 1.10, 0 record mismatches | PASS |

**P6′ = RED, two findings.** Both are reported, not adjusted; this is a HALT for an LV fix, and the repaint stays gated.

1. **`slope_stone_0` is in the layout of record but not built.**
   - **Layout:** uv (−7.5, 21.508), z 3.622 (terrain there 4.26), stone_tall, h 2.4 m.
   - **Level:** no slot within 0.02 m. The nearest slope_stones slot is #5 at (−9.010, −19.652), 2.39 m away, at z −0.14 with a different size.
   - **Effect:** the build is missing one layout placement. P6′'s presence check iterates the level's own models, so only the crosscheck can see this; it is why the crosscheck exists (§ 21).
   - **Fix:** re-emit the level slots from the layout, or correct the layout.
2. **`gully_rock` #1 (`gully_col_e_1`, "kit rock in the stair gully's e wall", R-C9-229) is 73.8% terrain-hidden.**
   - Box z −2.85, 5.72 m tall, centred where the terrain stands at 1.38. Its footprint spans −7.5 to 1.99 across the gully wall, so the wall covers most of its silhouette.
   - Setting a rock into a wall may be the intent, but **no `burial_by_design` is declared**, so it is not accepted.
   - **Fix:** declare it with its reason, or pull the rock out of the wall.
   - gully_rock #0 (0.477) sits just under the bar.

**Not counted against the build, noted.** ring_stones has 4 instances; the three fallen slabs of §§ 40–41 are no longer in the layout.

## 43. P6′ on 368cdf791 (LV's presence fold for § 42; R-C9-231). Frozen bars. `results/p6prime_bv2pp_368cdf791.json`

**Inputs.** `ids_art.png` sha eec9fa67…, matching the manifest. Slot crosscheck **PASS**: 59 layout placements against 59 level slots, 0 mismatches. LV dropped `slope_stone_0` (inside the barrow kerb, never built) and `gully_col_e_1`.

| Component | Result | Verdict |
|---|---|---|
| I-4 RED (1.5 m shift) | 6 of 13 objects below 0.7872 | **FAILS, as required** |
| presence | 0 missing, 0 extra, 0 terrain-hidden over 0.50. Worst: gully_rock 0.477, cliff_faces 0.409, barrow_front 0.387, wreck 0.327 | **PASS** |
| placement | min containment 0.9722 (logs) | **PASS** |
| scale | 112 instances, 0 over 1.10, 0 record mismatches | **PASS** |

**P6′ = PASS on 368cdf791.** No hidden-by-design was needed. The repaint gate's P6′ condition is met.

## 44. P5 v2 — RE-INSTRUMENTED and CALIBRATED (jack-ryan pre-ruling 309c4c41b; R-C9-251). Committed BEFORE any pilot-3 P5 value is read. `harness/p5v2.py`, `harness/p5v2_calibrate.py` → `results/p5v2_calibration.json`

**Instrument.** Exactly the pre-ruling's parameters (frozen there; restated in `p5v2.py`'s docstring).
- **a1:** σ 6 tone MAD on the raw shared strip, trim 12 px, 128-px segments.
- **a2:** σ 3 HF-std log-ratio, ε 0.5.
- **b:** unchanged.
- **c:** the context-boundary step at x = 1280c + 256 / y = 768r + 256, 64-px segments, Lab σ 4.
  - T and G over ±[4, 10) / 24 px; excess over the median at offsets ±32 … 96 step 8.
  - Runs of ≥ 2 segments score the minimum; segments whose ±110 px window touches unpainted px are excluded.
- **Bars:** v1's own maximum (T10BF raw canvases; `barrow_full_painted.png`). Stitching uses PT's Tier-B `guided_stitch.py` as committed, run unmodified with env flags.

**v1 bars.**

| a1 | a2 | b | c tone | c grain |
|---|---|---|---|---|
| **9.569** (1_2\|2_2) | 0.676 (1_2/1_3) | 0.799 | 17.417 (y = 2560, chunk 0_3, run at x 448: v1's own visible seam, pre-ruling INFO § 9) | 2.336 (y = 2560, chunk 2_3) |

| Check | Result | Required | |
|---|---|---|---|
| **C1** v1 positive control | a1, a2, b, c PASS by construction. Restitch flags-off **byte-identical** (sha eecb4266… = v1). Restitch **DEV-23 + 25 ON**: b 0.666, c tone 14.21, c grain 1.69 → PASS (b, c). All build flags (23/25/26/27) ON, reported: b 0.492, c 13.22 / 1.55 → PASS | PASS | ✓ |
| **C2** R-C9-158 (BVSW + section_sw_painted) | **FAIL**: a1 3 joins (max 11.85), a2 6 joins (max 1.018), b 1 seam (x = 3968, 1.274), c tone 2 boundaries (max 21.44), c grain 0 (max 1.449); raw MAD max 15.29 | FAIL | ✓ |
| **C3 a1 (i)** 6% hue/tone second hand on 1_1 | a1 13.709 > 9.569 | RED | ✓ |
| **C3 a1 (ii)** +6 sRGB on v1 3_2's strip of 2_2\|3_2 (dense) | a1 **11.05** (unmodified 6.454) > 9.569; raw MAD 15.91 | RED | ✓ |
| — the rejected normalised MAD, for the record | 0.612 vs its v1 max 1.242 (unmodified 0.503) → **GREEN: blind**, as the pre-ruling found. (PH's reading: raw strip MAD / mean of the two strips' σ 3 HF std; not jack-ryan's exact code, whose v1 max was 1.406) | — | — |
| **C3 a2** strip HF × 0.67 on 3_2's 2_2\|3_2 strip (mechanism 1) | a2 **0.631** (unmodified 0.241) ≤ 0.676 → **GREEN** | RED | **a2 DISCARDED** (not tuned) |
| **C3 c (i)** +7.16 dE on 3_2's new-paint side, x = 4096, rows 1920–2176 | tone excess **10.27** ≤ 17.42 → GREEN. **No detection floor ≤ 2× (14.32 dE).** | RED | ✗ |
| **C3 c (ii)** HF × 2.5 on the new-paint side, same place | grain excess **0.696** ≤ 2.336 → GREEN. **No floor ≤ × 5** (log2 5 = 2.32 < bar). | RED | ✗ |
| → **P5(c)** | **neither reads RED at any magnitude ≤ 2× the stated value → (c) DISCARDED** per the pre-ruling. The cause is the v1-max bar: v1 itself carries a 17.4 dE / 2.34 grain seam (y = 2560), so v1 parity admits any step below that. | | **(c) DISCARDED** |
| **C3 masking control** PS3b (`-r1` set) stitched DEV-23 + 25 ON | **FAIL** (a1: 0_1/0_2, 0_2\|1_2, 1_1\|2_1, 2_0/2_1). b 0, c 0, so (c) alone would not have failed it. | FAIL | ✓ (via a1) |
| **C4 specificity** | PS2 0_1/0_2 (raw 13.86): a1 **3.921**, a2 0.155 → PASS. PS3a 1_1/1_2 (raw 14.38): a1 **5.303**, a2 0.353 → PASS | expected PASS | ✓ |

**C5 — the pilot-3 canvas pin** (explicit; never `canvases()`, which would take PS3b's `-r1`):

| chunk | canvas | sha256 |
|---|---|---|
| 0_0 | `BV2F-PS3A-0_0/BV2F-PS3A-0_0.png` | `20321c0b6c4ddb8cf324b770a9f3b76d80e0f4442d188de2063adc8ec79ad881` |
| 0_1 | `BV2F-PS3A-0_1/BV2F-PS3A-0_1.png` | `f46e7fd067fbaf71830e54891254e728e161d710162f7d19754e26953c27465d` |
| 0_2 | `BV2F-PS3A-0_2/BV2F-PS3A-0_2.png` | `9a33d08ff780fe0bd17d51a48b79e82d9882e0184304caf7996538a8d59c310b` |
| 1_0 | `BV2F-PS3A-1_0/BV2F-PS3A-1_0.png` | `d3ff84018601ae6b0e219fd85310bde4ba18ad79b9d9dfd42406d75a913c2b6c` |
| 1_1 | `BV2F-PS3A-1_1/BV2F-PS3A-1_1.png` | `325eeb230ab7109a24ff17385b22a52dcc04aff5765da394acae432f9766bb8c` |
| 1_2 | `BV2F-PS3A-1_2/BV2F-PS3A-1_2.png` | `0a7db5bd51a0819f9781d22931be8998b4ab258e30dd46b688e02fe089101bc6` |
| 2_0 | `BV2F-PS3A-2_0/BV2F-PS3A-2_0.png` | `80d7128ed583f3531e468255a63c9c4cfe4bd1801da610ab207be2e675306e29` |
| 2_1 | `BV2F-PS3A-2_1/BV2F-PS3A-2_1.png` | `fbee10d14e1291bb9f2b931c7470a3f299132e7a72388a1344462da330fcb26a` |
| 2_2 | `BV2F-PS3A-2_2-r1/BV2F-PS3A-2_2.png` | `8d977dbd90d4c0ed7d85051a0769de5cbb1a3bcdac7ed381996d0cc3e22251d9` |
**P5 v2 as it binds on pilot 3 (pre-registered here).**
- **PASS iff** every a1 segment on the pinned raw canvases is ≤ 9.569 **and** every P5(b) seam on the build's flags-ON stitched painting is ≤ 0.799.
- **a2 and c are discarded.** They are computed and REPORTED only, with c flags-off and flags-on.
- **Raw overlap MAD is reported only**, with a 1:1 crop of every join over 13.09.

**What this leaves unguarded (disclosed for the conductor and jack-ryan).** Neither surviving sub-measure is shown to see:
- **mechanism 1**, a strip redraw softer than the new paint (a2 × 0.67 reads GREEN);
- **a straight tone or grain step at the context boundary** smaller than v1's own seam (c reads GREEN at +7.16 dE and × 2.5 grain).

These now rest on the conductor's 1:1 / play-zoom eye stop and on P11 (M-2). A stricter bar than v1's maximum would be a threshold move, so PH does not propose one.

## 45. PILOT 3 harness (PT 72a9a0ec5; painting 2f58f6379e82; R-C9-243/251/253). Frozen bars. `results/pilot3/*.json`; renders `renders/pilot_ps3a/`

**Inputs.**
- **PT:** `fid/pt/pilot/` (PS3A, pinned manifest `build_manifest_ps3a.json` = PH's § 44 C5 pin, all 9 sha256 equal); level `data/bv2f/pilot_rp3/level` (PIN: LV 03306a599; level.json byte-equal to LV's).
- **Palette:** reed (19, still masks 11) and lead (20 → sea) added; `carved_*` ids count as ground.
- **Tier-B stitch in force:** DEV-23/25/26/27 all ON. Records pinned in `results/pilot3/tierB_dev_records.json`: `guided_stitch.py` sha aa83745b… = its SHA256SUMS Tier-B row; dev23/dev25 records, dev26_result, dev27 test/result.
- **Not run:** Godot steps ran under the heavy lock with the 21 GiB gate (22 GiB free). The P11 crop build finished before the P10 runs started.

| Row | Pilot 3 | Bar | Verdict | Negative control / RED (same instrument) |
|---|---|---|---|---|
| P1 texel density | all 1.000 | ≤ 1.05 | **PASS** | (§ 1) |
| P2 lineage | 25/25 at 72a9a0ec5 | 100% | **PASS** | (§ 1) |
| P3 render vs painting | worst 12.36 (wood, baked); sea **5.30** on the painted base (R-C9-201 exemption: as delivered 31.23, motion layers at rest 26.78) | ≤ 15.5 | **PASS** | reshade RED FAIL; lit-plane sea RED 22.55 FAIL |
| P4 texture (§ 38 refs) | **ice vs sketch A: ΔE 11.97–17.27 in all 6 ice chunks** (painted median L\* 84.8–89.1 vs sketch 72.9; spectrum 0.080–0.122). **Snow vs v1: hist 0.331–0.494 in 6 of 9 chunks** (0_0, 1_0, 2_0, 0_1, 1_1, 0_2; bar 0.281). **Rock 2_1: spectrum 0.303** (bar 0.19) | ice ΔE ≤ 9.40, spectrum ≤ 0.116; snow 0.281 / 0.097; rock 0.481 / 0.19 | **FAIL** | (§ 3; § 38) |
| P5 v2 (§ 44) | **a1 max 10.543 at 0_1/0_2** (> 9.569; the y = 1792 bay seam the pre-ruling predicted); all other joins ≤ 8.25. b max 0.789 | a1 ≤ 9.569; b ≤ 0.799 | **FAIL (a1, 0_1/0_2)** | (§ 44 C2/C3) |
| P6a invention | 2 candidates: barrow_door (0.74 m), sea_cave_mouth (3.44 m, radius 4.0) | 0 invented | **PASS** | (§§ 2, 9–11) |
| P6′ (LV 03306a599) | crosscheck 57/57; 0 missing / extra / hidden; containment min 0.9722; scale 0/112 over | § 16 | **PASS** | I-4 1.5 m shift: 7/14 below → FAIL ✓ |
| P8 heather precision | min **0.5704** (2_0); 8 chunks judged | ≥ 0.4476 | **PASS** | 1 m shift RED FAIL |
| P9 sway | 5.781 over 59 763 px; noise 0.001 | ≥ 2.064 and ≥ 3× noise | **PASS** | no-wind 0.019 FAIL |
| P9 flow (F-4 geometry mask) | **7.959** over 675 159 water px (uv −29, −5.5) | ≥ 2.064 and ≥ 3× noise | **PASS** | hidden water 0.000 FAIL |
| P9 trail | 1.000 (flat 149 m², not-flat 964 m²) | ≥ 0.99 | **PASS** | (§ 6) |
| P9c floe drift | **n-insufficient**: 0 of the 7 bobbing floes lie inside the painted pilot plate (ids_built: ice_floes_bob 0 px in window) | § 38 F-4 (b): ≥ 3 floes | **NO READING** (cannot bind on this pilot) | — |
| P10 (§ 34) | start: p99 **22.82 / 18.50 / 25.61** (p50 ≈ 16.3; max 61.5); sea: 13.99 / **17.23** / 13.94 | worst of 3 ≤ 16.7 | **FAIL (start 25.61, sea 17.23)** | burn RED 29.14 FAIL |
| P11 v3 | set built: 40 scored + 10 repeats + 12 catch (6 A / 6 B), 62 images; reed EXCLUDED as build-specific (v1 has no reeds) | valid ≥ 10/12; PASS ≤ 26/40 | **judge pending** (conductor spawns) | (§ 39) |

**Reads.**
- **P4.** The pilot-3 mere is painted much **paler than the sketch-A reference** (L\* ~ 87 vs 72.9): the "pale few-vein mere" paint direction moved it past sketch A, not toward it. Snow is slightly cooler than v1 (b\* 4.9 vs 7.7; median L\* 93.9 vs 93.4) in most chunks.
- **P5.** The FAIL is the one pre-registered and predicted: the real bay seam at 0_1/0_2, y = 1792 (cause diagnosed in R-C9-247/251; remedy = the both-sides blockout fix).
  - **Raw MAD (reported only):** 0_1/0_2 13.81, 1_1/1_2 14.38. 1:1 crops are in `results/pilot3/p5_crops/`; 1_1/1_2 a1 is 5.30.
  - **c (reported only; discarded at calibration):** flags-ON tone max 11.40, none over v1's 17.42. Flags-OFF tone max 17.84 at x = 2816, chunk 2_2, over v1's bar. So the stitch-corrected reading is "PASS (stitch-corrected)" at 2_2 x2816; crop in PT's `ps3a_dry/dev27/`.
- **P10.** The frame cost rose about 2.8 ms at p50 (13.5 → 16.3 at the start) against the Phase-2′ pilot: 264 heather, reeds and the new terrain. Every start run carries ~12 frames over 16.7 ms.
- **P9c.** This pilot cannot exercise P9c: its bobbing floes all sit outside the painted window. P9c needs a build with ≥ 3 in-plate bobbing floes, i.e. Phase 3′'s coast.
- **Evidence-file note.** The pilot-3 life captures first wrote into `renders/pilot3/` (the § 32 directory). Its tracked files were restored from git. The untracked § 32 `life_sea` PNGs were overwritten by the pilot-3 frames, which also sit in `renders/pilot_ps3a/life_sea/`. The § 32 numbers are unaffected (recorded in `results/pilot3/p9c_flow_p10.json`). **That file name now collides with this section's `results/pilot3/`; this section's files are the new ones listed above.**

**P11 v3 crops for the blind judge:** `fid/ph/p11/abx3_pilot3_v1_vs_pilot/` (62 PNG + JUDGE.md, no metadata). Key: `fid/ph/p11/keys/abx3_pilot3_v1_vs_pilot.json` (outside the judge dir). Score: `python3 harness/p11_abx3.py score pilot3_v1_vs_pilot <answers.json>`.

## 46. SNOW PARITY investigation (R-C9-256; P11 pilot 3 = valid FAIL 38/40, the judge's cue being snow). No images, no Godot. `harness/snow_parity.py` → `results/pilot3/snow_parity.json`, sheet `results/pilot3/snow_parity_sheet.jpg`

**Method.**
- **Class.** Open snow on ground, tufts removed, eroded 3 px: v1 `p4_texture.v1_classes`; pilot 3 class_art `snow` on ground.
- **Zoom.** Both plates are 100.6 px/m, so play zoom = 1:1.
- **Grouping.** Per paint chunk: v1's 16 against the pilot's 9. Each pilot value is placed against v1's chunk-to-chunk range and SD.
- **Sheet.** v1 | pilot, 6 patches each, 1:1 and 2×. The pilot's snow is fragmented, so its patches needed a coverage threshold of 0.85 against v1's 0.97, and they cluster in column 2. This is disclosed.

| Measure | v1 chunks (min–max; mean ± sd) | Pilot 3 median [range] | Pilot chunks outside v1 range | z |
|---|---|---|---|---|
| **lit snow a\*** (peach, red side) | 1.83–3.07; 2.50 ± 0.37 | **1.43** [1.10–1.79] | **9/9** | **−2.9** |
| **lit snow b\*** (peach, yellow side) | 5.68–10.24; 8.19 ± 1.30 | **5.05** [3.86–5.86] | **8/9** | **−2.4** |
| **shadow a\*** (violet) | 2.93–4.50; 3.68 ± 0.50 | **1.74** [0.29–2.40] | **9/9** | **−3.9** |
| shadow − lit a\* | 0.79–1.62; 1.18 ± 0.22 | 0.36 | 9/9 | −3.8 |
| **shadow − lit b\*** (blue against the peach) | −23.9 … −14.4; −18.6 ± 2.6 | **−13.5** | **7/9** | **+2.0** |
| shadow − lit L\* | −20.5 … −13.7; −16.8 | −15.2 | 0/9 | +0.9 |
| median L\* | 92.3–94.4 | 92.3 | 4/9 | −1.7 |
| L\* spread (std) | 3.25–8.15 | 6.96 | 1/9 | +1.3 |
| shadow share of snow | 0.03–0.13 | 0.10 | 4/9 | +1.2 |
| shadow blobs per m² | 0.58–4.03; 2.12 ± 0.97 | **6.69** | **6/9** | **+4.7** |
| blob area median / p90 (m²) | 0.005–0.009 / 0.017–0.087 | 0.008 / 0.049 | 4/9, 2/9 | +1.3, +1.0 |
| blob contrast (ΔL\*) | 13.7–20.6 | 15.2 | 0/9 | −1.0 |
| blob edge width (px) | 4.0–6.7 | 5.1 | 0/9 | +0.2 |
| **grain spectrum RMS vs v1 pool** | 0.013–0.091; 0.043 ± 0.021 | **0.116** | **6/9** | **+3.5** |
| **cellular-mosaic p95 (P4 detector)** | 0.39–0.75; 0.57 ± 0.10 | **0.36** | **6/9** | **−2.0** |

**The differences that matter (for the repaint-4 paint direction).**
1. **The peach cast is missing (largest, consistent: 9/9 chunks).** v1's lit snow is warm peach-cream (a\* +2.5, b\* +8.2); the pilot's is cool cream (a\* +1.4, b\* +5.1). Direction: warmer, rosier lit snow, about +1 a\* and +3 b\*.
2. **The shadows are not v1's violet-blue, and contrast less with the lit snow.**
   - v1's shadow blobs are violet-blue (a\* +3.7) and sit about 19 b\* bluer than the peach around them.
   - The pilot's are grey-blue (a\* +1.7) and only about 13 b\* bluer.
   - Lightness drop, size and edge sharpness are all within v1's range; the HUE and the warm/cool SPLIT are what differ.
   - Direction: shadow blobs a clear lavender / violet-blue against peach.
3. **The surface grain lacks v1's cellular "cobble" mosaic.**
   - The spectrum shape is 3.5 sd off v1's pool, and the cellular-mosaic signature is 2 sd low.
   - The pilot's shadows break into many small, soft, low-contrast fragments (6.7 against 2.1 blobs per m²): a mottled wash.
   - v1 groups them into fewer clusters of rounded, cell-like blobs on a fine paper grain.
   - Direction: snow as v1's clustered rounded shadow cells, not an even mottle.

**Not different (so not the cue).** Brightness (median L\*), shadow depth (ΔL\*), blob contrast, blob edge width and shadow coverage are all inside v1's spread.

## 47. PILOT 4 harness (PT 6861bfc32; painting 7105731298ef; R-C9-262/264). Frozen bars, with one Matt-ruled exception (the ice colour reference). `results/pilot4/*.json`; renders `renders/pilot_ps4/`

**Inputs.**
- **Build:** PS4 canvases pinned by `build_manifest_ps4.json` (9/9 sha256 checked in P5); level `data/bv2f/pilot_rp4/level` (PIN: LV b5894d440; level.json byte-equal to LV's art level).
- **Stitch:** DEV-23/25/26/27 ON, and DEV-24 (8 masked local-repaint patches) applied post-stitch.
- **Tier-B records** pinned in `results/pilot4/tierB_dev_records.json`: DEV-23/25/26/27 records, the DEV-24 blocks and proofs, the DEV-28 records, `guided_stitch.py` (sha 5fdcb9e5…, which matches its SHA256SUMS Tier-B row; it changed from pilot 3's aa83745b… with DEV-24's post-stitch hook), and `dev24.py` / `dev28.py` (SHA256SUMS rows).
- **Godot:** every step under the heavy lock; the 21 GiB gate held (26 GiB). P10's first run waited 390 s for a JOIN-1 probe's lock. No PH CPU job overlapped any P10 run (PH's analysis finished 6 min before P10 acquired the lock).

**P4 ICE — MATT-RULED EXCEPTION (R-C9-262), not a re-tune.**
- **Matt kept PS4's blue mere.** The ice palette reference is re-based to the PS4 mere colour: this build's pooled ice median, Lab **(64.58, −2.75, −21.49)**, gated b\* ≤ 2.
- **Unchanged:** the ΔE bar (9.40) and the spectrum reference (sketch A at 24 px/m, bar 0.116).
- **Sketch-A ΔE is reported so the departure stays visible:** 10.05–23.37 per chunk (§ 38's sketch-A median is (72.9, −1.0, −9.4)).

| Row | Pilot 4 | Bar | Verdict | Control / RED |
|---|---|---|---|---|
| P1 | all 1.000 | ≤ 1.05 | **PASS** | (§ 1) |
| P2 | 25/25 at 6861bfc32 | 100% | **PASS** | (§ 1) |
| P3 | worst 11.16 (wood, baked); sea **5.81** on the painted base (as delivered 37.32; at rest 30.32) | ≤ 15.5 | **PASS** | reshade RED FAIL; lit-plane sea 25.84 FAIL |
| P4 ice (Matt-ruled reference) | ΔE vs PS4 mere **0.79–8.81** in all 6 chunks; spectrum 0.059–0.099 | ΔE ≤ 9.40; spectrum ≤ 0.116 | PASS | sketch-A ΔE 10.05–23.37 (reported) |
| P4 snow (v1) | **FAIL in 4 of 9 chunks**: 0_0 (hist 0.290, spec 0.124), 1_0 (0.433, 0.140), 0_1 (spec 0.182), 0_2 (spec 0.133); the other 5 within | hist ≤ 0.281; spec ≤ 0.097 | **FAIL** | (§ 3) |
| P4 rock (v1) | 2_1 spectrum **0.323**; the others within | spec ≤ 0.19 | **FAIL** | (§ 3) |
| → **P4 row** | | | **FAIL** (snow 4 chunks, rock 2_1) | |
| P5 v2 (§ 44) | **a1 19.14 at 2_0/2_1, 13.22 at 1_1\|2_1, 11.27 at 1_0/1_1**; b max 0.724 | a1 ≤ 9.569; b ≤ 0.799 | **FAIL (a1, 3 joins)** | (§ 44 C2/C3) |
| P6a | barrow_door (0.85 m), sea_cave_mouth (3.45 m) | 0 invented | **PASS** | (§§ 2, 9–11) |
| P6′ (LV b5894d440) | crosscheck 57/57; 0 missing / extra / hidden; containment min 0.9722; scale 0/112 | § 16 | **PASS** | I-4 shift 7/14 below → FAIL ✓ |
| P8 | min **0.5777** | ≥ 0.4476 | **PASS** | 1 m shift FAIL |
| P9 sway | 5.330 over 73 725 px; noise 0.001 | ≥ 2.064, ≥ 3× noise | **PASS** | no-wind 0.014 FAIL |
| P9 flow (geometry mask) | **7.520** over 671 371 px | ≥ 2.064 | **PASS** | hidden water 0.000 FAIL |
| P9 trail | 1.000 | ≥ 0.99 | **PASS** | |
| P9c | **n-insufficient**: 0 bobbing floes inside the painted plate | ≥ 3 floes | **NO READING** | |
| P10 (§ 34) | **start: p50 16.17 / 16.30 / 16.26, p99 17.25 / 25.41 / 17.91** (max 35.4; 66 / 176 / 118 frames > 16.7). **sea: p50 12.4, p99 20.64 / 13.92 / 19.38** (bursts of 3–7 frames at 12–13 s, max 50.2) | worst p99 ≤ 16.7 | **FAIL (start 25.41, sea 20.64)** | burn RED 24.81 FAIL |
| P11 v3 | set built: 40 + 10 + 12 catch (6 A / 6 B); scored classes heather 18, ice 13, snow 9; reed excluded | valid ≥ 10/12; ≤ 26/40 | **judge pending** | (§ 39) |

**P4 snow, § 46 measures against v1's chunk spread** (the R-C9-257 fix worked on palette; the grain is still off in the coastal chunks):

| Measure | v1 range | Pilot 4 median [range] | outside v1 | z |
|---|---|---|---|---|
| lit snow a* | 1.83–3.07 | 2.32 [1.41–2.41] | 1/9 | -0.48 |
| lit snow b* | 5.68–10.24 | 7.93 [5.96–8.66] | 0/9 | -0.20 |
| shadow a* | 2.93–4.50 | 2.95 [0.53–3.56] | 4/9 | -1.46 |
| shadow − lit b* | -23.85–-14.42 | -17.27 [-20.35–-15.97] | 0/9 | +0.54 |
| shadow blobs / m² | 0.58–4.03 | 4.89 [1.43–6.04] | 5/9 | +2.87 |
| cellular mosaic p95 | 0.39–0.75 | 0.44 [0.39–0.52] | 1/9 | -1.32 |
| grain spectrum RMS | 0.01–0.09 | 0.07 [0.03–0.18] | 4/9 | +1.47 |
| peach share of lit snow | 0.39–0.99 | 0.81 [0.33–0.93] | 1/9 | — |
**Reads.**
- **P4 snow.**
  - **Palette is now inside v1:** lit a\*/b\* 2.32 / 7.93, peach 0.81. Shadow a\* 2.95 is at v1's minimum, with 4 of 9 chunks below it.
  - **Still off:** the snow failures are the spectrum (grain) in the coastal and upper-left chunks, plus 1_0's histogram. Blobs per m² are still high (4.9 against v1's 0.6–4.0).
- **P5.**
  - **What fails:** the three a1 failures are the **mere ice** at the 1_0/1_1/2_0/2_1 corner. The service's redraw of the shared strip is a different blue: 2_1's rendition of the 2_0/2_1 strip is ΔRGB (−27, −20, −11) darker than 2_0's own (`p5_crops/`).
  - **Why the stitched painting looks fine:** DEV-23 and DEV-27 correct it. c flags-ON max is 9.95 against v1's 17.42 (flags-OFF 12.97), b is 0.724, and the 1:1 crop shows no straight line.
  - **Why it still binds:** a1 binds on the raw canvases by design (pre-ruling M-1), so this is a FAIL, stitch-corrected in the painting.
  - **Raw MAD:** none over 13.09 (max 11.66).
- **P10.** The start view's p50 is 16.2–16.3 ms: the frame budget is spent before any burst. The sea view has 3–7-frame bursts at 12–13 s after ready_done, reaching 50 ms. The cost is the heavier dress (294 sprays, 107 reed cards). Every start run has 66–176 frames over 16.7 ms.
- **P9c.** As on pilot 3: the bobbing floes sit outside the painted window.

**P11 v3 crops for the blind judge:** `fid/ph/p11/abx3_pilot4_v1_vs_pilot/` (62 PNG + JUDGE.md, no metadata). Key: `fid/ph/p11/keys/abx3_pilot4_v1_vs_pilot.json` (outside the judge dir). Score: `python3 harness/p11_abx3.py score pilot4_v1_vs_pilot <answers.json>`.

## 48. PRE-REGISTRATION for Phase 3′ (jack-ryan pilot-4 Gate-2 `2026-10-08-bv2f-pilot4-gate2.md`; R-C9-267/268). Committed BEFORE any Phase 3′ value is read.

### (a) P4 ICE reference FROZEN (C-1)
- **Reference.** The ice palette reference is **Lab (64.58, −2.75, −21.49)**: the PS4 mere colour measured at § 47 under Matt's R-C9-262.
- **Mode.** `pilot_harness.p4_v38` defaults to `PH_ICE_REF=ps4_frozen`. **`self` mode is RETIRED** (it raises).
- **Unchanged.** Bar ΔE ≤ 9.40 (gated b\* ≤ 2, per chunk ≥ 20 000 px); the spectrum stays against sketch A at 24 px/m (≤ 0.116); sketch-A ΔE is still reported.
- **Status.** A Matt-ruled exception, not a re-tune.

### (b) P11 class exclusion by pre-registration (Gate-2 § 2; `p11_abx3.build3(..., rule_exclusion=True)`)
1. **Rule.** A class leaves the **scored and repeat** trials iff (a) v1 has no such class, or (b) a Matt ruling of record moves its look away from v1. The list is fixed by ruling ID; the conductor cannot add to it; it never changes after a judge has read a set built under it.

   | Class | Ground | Substitute guard |
   |---|---|---|
   | **reed** | (a): v1 has no reeds | P4 reed advisory (vs v1 heather tufts) + Matt's eye |
   | **ice** | (b): **R-C9-203 / R-C9-255 / R-C9-262** | P4 ice vs the frozen PS4 Lab (a), ice spectrum vs sketch A, Matt's eye at M3′ |
2. **Mechanics.** An excluded class is never a trial class, and a crop showing ANY of it is never drawn for a scored or repeat trial.
   - With a class mask: as EXCLUDED content.
   - Without one (v1ref stills): the classifier's own ice pixel rule (b\* < −10 ∧ L\* ≥ 45) must cover < 1 % of the crop.
   - **Catch trials are unchanged** (v1 vs R-C9-159, v3 rules).
3. **40 scored trials from the remaining classes;** fewer than 40 → **the set is VOID, never shrunk.**
4. **G2-B2 rebuilt under the new composition and judged once each before P11 binds at M3′:** `p11/abx3_g2v4_v1rec_vs_v1head/` (must read valid ∧ PASS) and `p11/abx3_g2v4_v1_vs_halfdensity/` (must read valid ∧ FAIL); keys in `p11/keys/`.

### (c) P10 discipline (Gate-2 § 3; `harness/p10_disc.py`). The binding bar is unchanged, and no frame is ever excluded from it.
1. **Quiescence precondition, checked BEFORE launch and logged** (`quiescence.json`).
   - Requirement: over 30 s of 1 Hz `ps` samples, no non-Godot process averages > 10 % CPU. The usual offenders: mediaanalysisd, photoanalysisd, mds_stores, backupd.
   - If it is not met: wait and re-check, up to 20 tries, then HALT. A run is never discarded after the fact on this ground.
2. **In-run 1 Hz process log** (`proclog.jsonl`).
   - A run is **VOID** iff a non-Godot process exceeds 25 % CPU for ≥ 1 s while Godot runs.
   - A VOID run → the set of 3 is re-run (§ 34's crash rule). **Two VOID sets → HALT** to the conductor; host-level mitigation is a matt_to_do.
   - **Pre-registered here:** WindowServer and kernel_task are **render-path** processes. They are logged, never VOID triggers, because they serve the Godot window being measured.
3. **Session witness.**
   - v1 `barrow_painted.tscn` at uv (0, 1), 3 runs under (1)–(2), recorded now as the machine reference (`renders/p10_witness/witness.json`; envelope = its p50 range ± 0.5 ms).
   - Every P10 session runs the witness first; a witness p50 outside the envelope → the session is VOID.
4. **Binding statistics.**
   - **worst-of-3 p99 ≤ 16.7 ms**, unchanged;
   - **NEW, binding: DETERMINISTIC HITCH** — a frame > 25 ms recurring within ± 0.5 s of window (walk) time in ≥ 2 of 3 runs = FAIL, whatever the p99.
5. **Reported, non-binding:** burst-excluded p99 (frames in runs of ≥ 2 consecutive frames > 16.7 ms removed), burst count, and > 25 ms timestamps per run.
6. **Engineering target before the Phase 3′ build (not a bar):** start p50 ≤ 15.0 ms.

### (d) P5 a1 for DEV-25c's inner-128 paste (Gate-2 § 6 item 5; `harness/p5v2c_calibrate.py` → `results/p5v2c_calibration.json`)
- **Band.** a1 is computed over ONE 128-px half of the overlap's width. **E** = [0, 128): the newer chunk's canvas edge, the neighbour-interior side. **C** = [128, 256): its interior side. Trim 12 px on the band edges; other a1 parameters as § 44.
- **Which half binds** is DEV-25c's pasted band, **read from DEV-25c's Tier-B paste mask** (not from any reading). **Both bars are derived now** on v1, with the § 44 analogues: C2 R-C9-158 must FAIL; C3 the 6 % second hand on 1_1 and +6 sRGB on 3_2's rendition of the band of 2_2|3_2 must read RED; the masking control PS3b must FAIL. A band failing any of these is not usable.
- **v1's 9.569 (full 256) continues to bind joins painted under the full-256 paste** (the pilot).

### (e) Phase 3′ per-chunk auto-QA, restated (charter Phase 3 "invention check first, then P5–P7"; P7 retired)
1. **P6a** on the chunk (v0.1 detector, declared openings; water-class candidates go to the conductor's triage, R-C9-194);
2. **raw a1 per join** (§ 44, or § 48 (d) for an inner-128 chunk), with the "stitch-corrected" crop rule: a join over the bar whose stitched painting shows no line at 1:1 is reported with its crop and stays a FAIL under M-1;
3. **P4 snow per chunk** (v1 bars; with the § 46 palette measures reported).

## 49. § 48 calibrations and records (computed AFTER the § 48 commit e3afc0cc8; no Phase 3′ value exists)

**(d) a1, inner-128 bands** (`results/p5v2c_calibration.json`). **Both bands are usable**; the binding one is DEV-25c's pasted band, from its paste mask.

| Band | v1 bar (join) | C2 R-C9-158 | C3 second hand 1_1 | C3 +6 dense 2_2\|3_2 (unmod.) | PS3b masking | Specificity PS2 0_1/0_2 / PS3a 1_1/1_2 |
|---|---|---|---|---|---|---|
| **E** [0, 128) (canvas-edge half) | **8.789** (1_2\|2_2) | FAIL (5 joins, max 10.80) ✓ | 13.50 RED ✓ | **10.31** (6.54) RED ✓ | FAIL (4 joins) ✓ | 3.93 / 4.87 |
| **C** [128, 256) (interior half) | **11.045** (1_2\|2_2) | FAIL (3 joins, max 15.70) ✓ | 13.96 RED ✓ | **11.57** (6.29) RED ✓ (margin 0.52) | FAIL (4 joins) ✓ | 4.51 / 5.76 |

**(b) P11 G2-B2 under the class exclusion** (`results/p11_abx3_g2v4_build.json`).

| Set | Result |
|---|---|
| `abx3_g2v4_v1_vs_halfdensity` | 40 scored + 10 repeats + 12 catch (6 / 6), 62 images: **judge-ready** |
| `abx3_g2v4_v1rec_vs_v1head` | **37 scored, 11 catch → VOID (cannot draw 40, rule (b)3; not shrunk)** |

- **Why it is short.** With ice out, record-time v1 offers too few non-ice crops: its 3 v1ref stills (`V1_tarn`, `V1_ring`, `V1_door`) are ice-heavy at the tarn.
- **Consequence.** The v1-vs-v1 control **cannot be built under the new composition from the current pools**, so P11 cannot bind at M3′ until it can.
- **For the conductor / jack-ryan (no change made).** Enlarging the record-time v1 pool needs new v1 stills, which is a capture, not a rule change. Changing the seed to look for a 40 would be shopping and is not done. **The VOID dir is kept and must not go to a judge.**

**(c) P10 session witness: HALT** (`renders/p10_witness/`).
- **Run v1_1** (quiescent after 7 tries) was **VOID**: p50 11.20, p99 13.13 recorded but not counted. Other processes went over 25 % during it: `git` (63 %, from concurrent agent sessions), `mediaanalysisd` (57 %), and `Warp` (the terminal app, 33 %).
- **The re-run set never became quiescent** in 20 tries. The terminal process (Warp, which hosts the agent sessions) averages 16.8 % on its own.
- **Per § 48 (c) 1 → HALT to the conductor.**
- **The witness envelope is NOT recorded:** a VOID run defines nothing.
- **For the conductor / Matt (a matt_to_do candidate).** The § 48 (c) quiescence bar (10 %) is not reachable while the agent sessions' terminal and their git/Python jobs run. Options: (i) a quiet window with the agent sessions paused; (ii) a ruling on whether the session host (Warp) is a render-path-like exemption. That is jack-ryan's to rule, not PH's.

**P4 snow support** (`results/pilot4/p4_snow_support.json`; Gate-2 § 4; report only).
- **v1's 16 chunks:** 40–316 spectrum windows (64 px, ≥ 90 % coverage), 375 k–1.48 M eroded snow px.
- **Pilot 4's four failing chunks have 1–18 windows**: 0_0 18, 1_0 1, 0_1 1, 0_2 2.
- **The passing chunks have 12–130.**
- **No minimum-support rule is proposed:** v1 has no chunk below 40 windows, so it offers nothing to calibrate a lower cut-off on (Gate-2 § 4: calibrated on v1's own low-support chunks, or not at all).

### § 48 (c) AMENDMENT A — P10 quiescence (jack-ryan pilot-4 Gate-2 Addendum A; R-C9-269). Committed BEFORE any quiet-window run. No bar moves.
- **No exemptions.** The session terminal (Warp) is **not** exempt. OS services (mediaanalysisd etc.) are not exempt: the precondition waits for them. The 10 % / 25 % / 20-try numbers stand.
- **When P10 binds.** **P10 binds ONLY inside a scheduled QUIET WINDOW.** The conductor pauses the Sim Session and every other lane: no other Godot or Blender process, no agent git or Python jobs, other sessions idle. PH holds the heavy lock for the whole window.
- **How PH launches it.** Detached, output to file, never streamed to the terminal:
  `nohup python3 harness/p10_disc.py window <base> <scene> <view> --first|--envelope <founding window_log.json> --paused "<what the conductor paused>" > <base>/driver.log 2>&1 &`
  PH's session then waits on `<base>/window_log.json` without polling output.
- **Run order:** **W P W P W P** (W = v1 witness `barrow_painted.tscn` uv (0, 1), P = candidate), as fresh processes, each under the quiescence precondition and the 1 Hz VOID log.
  - **Binding:** the candidate's worst-of-3 p99 ≤ 16.7 ms + the deterministic hitch.
  - **Report-only:** the paired difference P p50 − adjacent W p50.
- **The envelope.**
  - In the **first** window, the three W runs **record** the envelope (W p50 range ± 0.5 ms), and that session's P runs are validated by the per-run rules only.
  - **From the second window on**, a W p50 outside the envelope VOIDs the session.
- **The window record** (`window_log.json`) holds the start/stop times, what was paused, every run's quiescence and VOID result, and the binding readout.
- **If the window cannot reach quiescence in 20 tries → HALT → matt_to_do** (a host-level change). It is not a bar move.
- **Until the conductor calls the first window: no P10 runs.**

**§ 49 (b) follow-up: the v1-vs-v1 control rebuilt with a CAPTURE** (conductor; jack-ryan Addendum A INFO). Five NEW record-time v1 stills were rendered in v1's level with the v1ref recipe copied unchanged in method (`barrow_full/godot/tools/v2sw_run.gd` `v1stills`: `barrow_painted.tscn`, root window 1726 × 971 as the original V1_*.png, him at (u − 1.5, v − 1) facing S, park_camera, settle 10 + 30), only at **non-ice views** (`harness/godot/ph_v1rec_stills.gd`; under the heavy lock).
- **Views:** V1R_se (8, −11), V1R_e (11, −1), V1R_ne (6, 7), V1R_nw (−6, 8), V1R_w (−12, 9). The tarn ellipse stays outside every frame.
- **Output:** `p11/v1rec_ph/` (sha256 in `results/p11_abx3_g2v4b_build.json`).

**`p11/abx3_g2v4b_v1rec_vs_v1head/`:** 40 scored (snow 34, heather 6) + 10 repeats + 12 catch (6 A / 6 B), 62 images; key `p11/keys/abx3_g2v4b_v1rec_vs_v1head.json`.
- **Pool:** record-time v1 = v1ref 3 + the 5 new stills. The same seed rule applies, a new set name, no seed shopping (one build, seed 2683).
- **Self-test:** the key scores valid PASS-format (40/40, 12/12); always-A gives 6/12 → VOID.
- **Judge-ready.** It **supersedes the VOID 37-trial set**, which is never judged.
