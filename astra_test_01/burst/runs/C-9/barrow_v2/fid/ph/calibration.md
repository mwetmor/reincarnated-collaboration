# BV2F lane PH — the v1-parity harness, calibrated (Phase 0 task 0.4)

**Lane:** PH (galadriel). **Charter:** BV2F v0.2 (§ 9 C-1..C-3 as amended by § 12 Gate-1 folds W-1, W-7, I-1). **Status:** calibrated. v1 passes every measured row. R-C9-159 fails P1–P4 and P6b. R-C9-158 fails P5 and P9. Every row has a constructed failure that reads RED, except P4's discarded cellularity statistic and P11 (built, judged by the conductor's judge).
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
| P8 | constraint | constructed (RED) | share ≥ 0.9 and tint r ≥ 0.874 — PROVISIONAL (0.90 × v1 measured) until PT's reproduced v1 value lands (Gate-1 W-2) | 1.000 / r 0.97 **PASS** | 0.402 / r 0.03 **FAIL** | — | 0.419 / r 0.05 **FAIL** | — |
| P9 | constraint | R-C9-158; constructed (RED) | (a),(b) ≥ 3× noise and ≥ 0.25× v1 heather sway (2.06); (c) ≤ 0.25 px; (d) ≥ 0.99 | sway 8.26; trail 1.00 **PASS** | sway 13.06; flow 6.48; drift 1.913 px; trail 0.81 **FAIL** | trail 0.00; no SnowField, no wind, static sea **FAIL** | sway 0.00 (v1, wind held); flow 0.206 (159 sea, motion layers hidden) **FAIL** | — |
| P10 | constraint | constructed (RED) | ≤ 16.7 ms | 14.87 **PASS** | None **—** | — | 21.33 **FAIL** | — |
| P11 | quality | R-C9-159 | ≤ 65% (pass if ≤ 19/30) | — | — | — | — | cal_v1_vs_159: None **—**; cal_v1_vs_158: None **—**; cal_v1_vs_constructed_halfdensity: None **—** |
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
| P8 | share ≥ 0.90 × v1, tint r ≥ 0.90 × v1 — **provisional** | v1 `heather.json` (977) measured here; to be re-based on PT's reproduced v1 value (W-2) |
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
- **P10 for R-C9-159 is informational only** (P10 is a constraint row). It is still queued behind the heavy lock (`renders/perf_v159`).
- **P9c floe UV drift has a RED** (R-C9-159, 1.91 px median over 5 floes) **but no positive control.** v1 has no floes, and no rest-pose implementation exists yet. DEV-5's first build will be its positive control.
- **P8** is provisional until PT's reproduced v1 value lands.
- **P11** is built but not judged (C-3).
- **v1 stills:** P11 uses `section_v1cam/v1ref/V1_*.png`. `barrow_full/captures/still_*.png` are **blockout** stills and are excluded; I checked them by eye. PT's `fid/pc/v1_stills/` join the pool automatically. Regenerate the pairs with OVERLAP 0.25 once they land.

## 5. State

See `../RESUME_PH.md`.

## 6. For the conductor to rule

See the hand-back. Recorded here: (1) the cellularity discard leaves C4's "blotchy cellular bakes" without a binding pixel instrument; (2) P6a's false positives on dark material in the hall chunks; (3) P4 new classes (sea, shingle) and wood (v1 logs are under 20,000 px in every chunk, so there is no v1 spread) have no binding P4 statistic until a nearest v1 class is named; (4) P8's threshold re-bases on PT's value; (5) P9c has no positive control until DEV-5 is built; (6) P5 also flags R-C9-159's stitched seams (2 over v1's ghosting bar). P5's negative control is R-C9-158, so this is evidence, not calibration.
