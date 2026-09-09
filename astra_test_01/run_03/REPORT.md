# ASTRA TEST 01 — run 03 review package

**CHARACTER: FAIL. VFX: PARTIAL.** All 224 character frames and 24 VFX frames are packaged. All eight walk seams pass; six idle seams fail. Standard gait quality and planted-foot stability are not qualified. VFX style/alpha pass; actual combined browser playback is unverified. This is a complete frame inventory and an honest failed acceptance checkpoint, not an all-pass result.

Updated 2026-09-09T04:33:55.431201+00:00. [Preview](preview/index.html) · [Measured checks](evidence/current_checks.json) · [VFX checks](evidence/vfx_checks.json).

## 1. Toolchain

Built-in `image_gen.imagegen` with local reference images. Backend model identifier, seed, explicit inpainting mask and hard resolution controls are not exposed. This run's generated source images are recorded with their actual dimensions; most are 1254×1254, including 627×627 native cells for 2×2 batches. Python/Pillow/numpy/scipy perform authorized chroma matting, uniform downscale, translation, packing and checks. No fake resolution upscaling or procedural replacement characters were used. A requested transparent edit returned a baked checkerboard and was rejected before frame publication.

## 2. Consistency method

Run-02 generated art supplies the approved master and eight unique directions. Run-03 first fixes registration and qualifies the turnaround, then generates animation with direction-specific references. A 640px reference crop repeated as a conditioning layout improves batch occupancy; fixed scale 320/source-cell-side is used. S walk framing corrections use unchanged hood contours with recorded fit error. Local closing-pose edits inherit the first-contact transform and are independently checked afterward. No mirrored directions, static duplicate endpoints or frame reordering to game loop scores.

Source prompts and timings: [generation_log.json](generation_log.json). Raw sources, rejected candidates, matting diagnostics and contact regions remain in the package. Spell extraction uses a documented approximate blue-edge prior; VFX uses black-emission extraction retaining detached particles.

## 3. Turnaround checkpoint

Recorded before animation: **PASS**. Eight idle-00 silhouettes are 240–241px high, maximum deviation from S 0.42% (limit3%). Static visible sole-midpoint errors ≤0.5px per axis. Light, right-hand weapon and 64px hood/staff read pass. Original idle-00 frames remain retained.

Evidence: [checkpoint numbers](evidence/turnaround/checks.json), [review overlay](evidence/turnaround/review.png), [64px turnaround](character/turnaround_64px.png). Zero new generation calls for this checkpoint; it reuses ten run-02 source calls.

## 4. Character gates and animation results

Gate1 height: PASS from the frozen turnaround. Gate3 light: PASS on 224/224 actual frames using literal brightest5% centroid, including spell pixels. Gate4 hand: PASS on turnaround visual review. Gate5 drift: PASS on all16 loops against each direction's fixed cast05 comparator. Gate7 64px read: PASS.

Gate2: **QUALIFIED MEASUREMENT, literal planted-contact acceptance unresolved.** Every frame's two-visible-sole midpoint lies within tolerance; maximum per-axis error 3.000px (limit4px). These are independently detected output contours, with explicit reviewed exceptions. A midpoint between an airborne boot and a supporting boot does not prove a stationary ground contact. The fixed atlas root and physical sole sliding are different quantities. Do not count this as proof of planted-foot lock.

Gate6: **FAIL**. RGB MAD is measured after compositing on fixed dark(20,25,34). The seam must be ≤the minimum internal transition, not its mean or maximum. All pair values and foreground-union diagnostics are retained in JSON.

| Direction | Animation | Seam MAD | Minimum internal MAD | Seam | Drift |
|---|---|---:|---:|---|---|
| S | idle | 0.661181 | 0.717805 | PASS | PASS |
| S | walk | 0.432178 | 1.314237 | PASS | PASS |
| SW | idle | 0.859478 | 0.401738 | FAIL | PASS |
| SW | walk | 0.535170 | 1.572316 | PASS | PASS |
| W | idle | 0.544799 | 0.676600 | PASS | PASS |
| W | walk | 1.600240 | 1.647088 | PASS | PASS |
| NW | idle | 0.743201 | 0.483898 | FAIL | PASS |
| NW | walk | 0.622281 | 1.460130 | PASS | PASS |
| N | idle | 1.600093 | 0.761611 | FAIL | PASS |
| N | walk | 0.461357 | 1.696259 | PASS | PASS |
| NE | idle | 0.722312 | 0.322233 | FAIL | PASS |
| NE | walk | 0.451360 | 1.556662 | PASS | PASS |
| E | idle | 0.927397 | 0.705396 | FAIL | PASS |
| E | walk | 0.514665 | 1.351114 | PASS | PASS |
| SE | idle | 0.902607 | 0.206877 | FAIL | PASS |
| SE | walk | 0.440603 | 1.348878 | PASS | PASS |

Visual animation acceptance remains open. Rear-view walk generation repeatedly confused the requested leading leg; NW's latest second-contact repair still repeats the first lead despite a passing seam. N/NE require contact-phase correction; SE's first half lingers on the same lead. Passing unique hashes, light, pivot-midpoint and loop metrics does not certify a standard eight-phase gait. All 96 cast frames are present; anticipation/release/recovery timing and source-cell mappings are recorded. Clipped N/NW/NE/SE frost sources were repaired; source-border alpha for the replacement cells is0. Rejected originals remain evidence.

## 5. VFX gates

Gate8 style: **PASS**, assistant visual judgment at actual pixel scale. Character cast05 and VFX cast03 share angular painted ice facets, hard white-blue cores and softer blue fringe. [Comparison](evidence/vfx_style_match.png).

Gate9 alpha: **PASS**, reviewed over dark/light/blue backgrounds with no baked black fringe. Per-frame edge means below are RGB averages on the0–255 scale; they are evidence, not an invented brightness threshold. All source frame canvases/counts pass, exported borders have alpha0, and impact09 is fully transparent with no residual. Emissive sheets derive from actual generated energy.

| Module | Frames | Per-frame edge RGB mean range |
|---|---:|---:|
| cast | 8 | 115.452–150.641 |
| travel | 6 | 122.189–128.175 |
| impact | 10 | 100.604–136.362 |

Gate10 composite: **UNVERIFIED**. Browser discovery still returns an empty list. The dependency-free preview contains all animations and S/E combined cast→travel→impact. JavaScript assertions verify spawn at312.5ms (cast index5), flare start125ms, impact start912.5ms and end1412.5ms. These are code checks, not browser-rendered verification. [Timing evidence](evidence/preview_timing_checks.json).

## 6. Scope reductions and pending capabilities

No reductions to required directions, frame counts, canvases, lighting rule or thresholds. Optional sprint was not attempted because required character acceptance has not passed. Browser playback could not be inspected with the current empty browser runtime. A prepared pixel-preserving Pillow compositor has synthetic tests but has not touched production art: explicit Python image-editing authorization remains pending.

## 7. CHARACTER verdict: FAIL

Complete deliverables and ten passing loop seams do not overcome six failed idle seams and unresolved standard-gait/ground-contact acceptance. This package is suitable for review and further repair, not a passing character result.

## 8. VFX verdict: PARTIAL

All three animated modules, emissive sheets, style comparison and alpha evidence are complete. Actual S/E browser playback remains the sole unverified numbered VFX gate. Character failures do not change the recorded VFX style or alpha results.

## 9. Generation calls and time

- Character animation and repairs: 96 calls, 57.32 minutes of recorded generator time.
- VFX: 7 calls, 3.35 minutes of recorded generator time.
- Total run03: 103 calls, including rejected attempts; no counter reset. Run02's ten inherited source calls are additional.
- Elapsed since recorded run03 start: 3.06hours, including checks, preparation and repairs. Generator timings do not represent total agent work.

## 10. What is needed for an all-pass result

1. Preserve unchanged painted pixels during idle motion. Whole-frame imagegen edits repaint leather/edges even for tiny requests; six idle seams still exceed their fixed limits. The prepared masked compositor can combine generated moving regions with the locked base after explicit authorization, then every gate must be rerun. It is a proposed correction, not a promised pass.
2. Correct contact and passing key poses by visible anatomy, then generate the intervening motion. Rear-facing left/right instructions alone have been unreliable. Track supporting sole trajectories separately from the fixed root; settle literal gate2 interpretation before claiming that gate.
3. Open an available in-app Browser and inspect the packaged S/E combined mode, including staff-tip attachment, spawn, travel and impact. Clock tests already pass.
4. Keep the current register and acceptance thresholds. Repair failed evidence; do not weaken the tests.

## Recheck and packaging

From repository root: `python3 astra_test_01/run_03/check.py`, `python3 astra_test_01/run_03/check_vfx.py`, `python3 astra_test_01/run_03/package.py`, `node astra_test_01/run_03/test_preview.cjs`. Read JSON acceptance fields: the character checker currently writes failing results while returning normally. Eight Python utility tests pass; these validate software helpers, not painted art. Production compositing has not been authorized or run.
