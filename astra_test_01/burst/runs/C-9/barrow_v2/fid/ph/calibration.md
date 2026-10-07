# BV2F lane PH — the v1-parity harness, calibrated (Phase 0 task 0.4)

**Lane:** PH (galadriel). **Charter:** BV2F v0.2 (§ 9 C-1..C-3 as amended by § 12 Gate-1 folds W-1, W-7, I-1). **Status:** calibrated. Rulings R-C9-167 and R-C9-168 are folded in § 7. v1 passes every measured row. R-C9-159 fails P1–P4, P6b and P8. R-C9-158 fails P5 and P9. Every row has a constructed failure that reads RED. **Open:** P6a's scoped judge (R-C9-169, § 8) and the P11 ABX test both await the conductor's judges.
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
| P8 | constraint | constructed (RED) | ≥ 0.4476 — v1's minimum chunk value (R-C9-169) | 0.5221 (share 1.00) **PASS** | 0.0212 (share 0.40) **FAIL** | — | 0.1061 (share 0.42) **FAIL** | — |
| P9 | constraint | R-C9-158; constructed (RED) | (a),(b) ≥ 3× noise and ≥ 0.25× v1 heather sway (2.06); (c) ≤ 0.25 px; (d) ≥ 0.99 | sway 8.26; trail 1.00 **PASS** | sway 13.06; flow 6.48; drift 1.913 px; trail 0.81 **FAIL** | trail 0.00; no SnowField, no wind, static sea **FAIL** | sway 0.00 (v1, wind held); flow 0.206 (159 sea, motion layers hidden) **FAIL** | — |
| P10 | constraint | constructed (RED) | ≤ 16.7 ms | 14.87 **PASS** | 13.55 **PASS** | — | 21.33 **FAIL** | — |
| P11 | quality | R-C9-159 | ABX accuracy ≤ 65% (≤ 26/40); judge void if repeat inconsistency > 25% | — | v0.1 directional 100.0% (null FA 0%) **FAIL** | v0.1 directional 13.3% (null FA 40%), judge UNRELIABLE **—** | v0.1 directional 86.7% (null FA 10%) **FAIL** | — |
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
| P8 | precision ≥ 0.4476 (v1's minimum chunk; R-C9-169) | `take/build/overlay_check.json` per_chunk, 16 chunks 0.4476–0.5783, whole window 0.5221; reproduced exactly by PT (`fid/pc/results.json` T3) and by PH |
| P9 | sway ≥ 3× noise and ≥ 0.25× v1; flow ≥ 3× noise; floe drift ≤ 0.25 px; trail coverage ≥ 0.99 | v1 in-engine pair; v1 SnowField covers 100% of its floor |
| P10 | p99 ≤ 16.7 ms | plan § 4 P10 (the 10.9–12.4 ms target is withdrawn, W-2) |
| P11 | identification ≤ 65% (≤ 19/30) | plan § 4 P11; power: P(pass) = 0.95 at p = 0.50, 0.49 at 0.65, 0.27 at 0.70, 0.03 at 0.80, 0.0001 at 0.90 |

## 3. Discarded and re-instrumented

**Discarded.**
- **P4 (3) cellularity** (spectral peak excess, 6–20 px). It cannot see a constructed failure built the way R-C9-159's bakes were built: a patchwork of 12 px Voronoi cells drawn from four offset copies of v1's own painting. On rock windows that scores p95 0.417, against v1 rock's own 0.402 and a bar of 0.681. A ±15% tone stamp scores 0.391. R-C9-159's bakes do score higher (medians 0.30–0.52, against 0.11 for v1's bakes), but an instrument that cannot see its own constructed failure decides nothing. The score is still computed and reported, and it is non-binding. **Consequence:** the harness has no binding instrument for cellularity. P4 still fails R-C9-159, on Lab histogram and spectrum shape, and P11 is the remaining perceptual guard.
- **P9b film instrument** (registered water-vs-snow residual on walk and pan films). It cannot separate R-C9-159's animated sea (median ratio 1.71–1.82) from R-C9-158's static sea (1.38): the film compression and the pans drown the signal. The in-engine static pair is binding in its place.

**Re-instrumented.**
- **P6a.** The first instrument used unsmoothed L* < 25 with a 20 px opening. It found only the declared door in the BVR hall: 1 opening, 0 inventions, so it could not see R-C9-155. It was re-instrumented to L* on a 0.1 m Gaussian, because a door interior is textured (planks, smoke, embers). T = 32 is computed from v1 alone, with a 0.2 m opening and ≥ 0.5 m². It now flags the invented second door at plate (10311, 4925) (`figures/p6a_bvr_hall_flags.jpg`).
- **P5 constructed input.** A 12 px half-frame shift is invisible to (b): it scores 0.772 against a bar of 0.799. v1's partition-of-unity stitch cannot make a hard seam, so the constructed input is now a 6 px misregistered blend, which is the stitch's ghosting failure. It scores (b) 1.250. Measure (a) carries the hard and second-hand cases.

**Known false-positive mode (P6a).** The detector also flags 17 dark charred-timber clumps in the BVR hall. They are not openings, and v1 contained no dark material. A burnt-hall chunk will therefore flag every time. See § 6.

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
- **P8** is provisional until PT's reproduced v1 value lands.
- **P11** is built but not judged (C-3).
- **v1 stills:** P11 uses `section_v1cam/v1ref/V1_*.png`. `barrow_full/captures/still_*.png` are **blockout** stills and are excluded; I checked them by eye. PT's `fid/pc/v1_stills/` join the pool automatically. Regenerate the pairs with OVERLAP 0.25 once they land.

## 5. State

See `../RESUME_PH.md`.

## 6. For the conductor to rule

See the hand-back. Recorded here: (1) the cellularity discard leaves C4's "blotchy cellular bakes" without a binding pixel instrument; (2) P6a's false positives on dark material in the hall chunks; (3) P4 new classes (sea, shingle) and wood (v1 logs are under 20,000 px in every chunk, so there is no v1 spread) have no binding P4 statistic until a nearest v1 class is named; (4) P8's threshold re-bases on PT's value; (5) P9c has no positive control until DEV-5 is built; (6) P5 also flags R-C9-159's stitched seams (2 over v1's ghosting bar). P5's negative control is R-C9-158, so this is evidence, not calibration.

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

