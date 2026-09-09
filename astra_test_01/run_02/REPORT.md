# ASTRA TEST 01 — revised process, run 02

Status: COMPLETE TEST RUN — CHARACTER FAIL; VFX PARTIAL / NOT TESTED. Generation stopped after two complete failed turnaround checkpoints. Prior run remains unchanged.

## 1. Toolchain declaration

Built-in `image_gen.imagegen`, with local reference images. Backend model and hard resolution limits are not exposed. No seed, mask or alpha-output control is exposed. Actual image mode, resolution and source hashes are recorded per call. System Python with Pillow 10.3.0, numpy 2.4.6 and scipy is available. No CLI image-generation fallback or subagents.

## 2. Consistency method

The user authorized the revised process on 2026-09-08: qualified master, verified alpha extraction, deterministic uniform scale/translation, visual pose guides, one-variable repairs and key-pose animation. All files in this run live below `astra_test_01/run_02/`.

Generate a new, simpler master under the original register, keeping every required character feature. Prefer genuine transparency. When generation produces opaque art, use an explicitly requested uniform green extraction plate, followed by documented chroma matting. The plate is an intermediate, not the final background. The character palette contains no saturated green. Verify the matte against several backgrounds before commissioning the turnaround. Never key by darkness, never remove checkerboard through brightness thresholding, never mirror a direction, and never upscale source art.

Registration is a uniform downscale plus translation, based on annotated landmarks. Master body standing height is 240 px. A direction's base scale is established once and reused for that direction's subsequent frames; animation geometry cannot be normalized independently frame by frame to hide drift. Raw and registered metrics are both retained. Registration-generated pivot equality is reported separately from independently inspected contact accuracy.

Pose guides are procedural reference images, visibly marked GUIDE. They are not painted deliverables. Projection uses an orthographic 45-degree-elevation view with vertical image compression of 1/sqrt(2), yielding the requested 2:1 projected ground grid; projection constants are fixed. Character pose rotates while screen-upper-left lighting stays fixed.

Literal gates remain authoritative. Supplementary body-mask measurements may diagnose a misleading light centroid but cannot replace a failed literal gate. Foot/root anchors are annotated independently of atlas metadata. For static stance the anchor is the midpoint of the two ground support points; during animation a root anchor and planted-foot contacts are tracked separately. At most two complete turnaround checkpoint evaluations; repairs are completed and evaluated as a set before claiming a second checkpoint. No animation production before turnaround PASS.

## 3. Turnaround checkpoint

Checkpoint 1: FAIL, saved before further generation. Height S=240, SW=249 (+3.75%), W=240, NW=265 (+10.42%), N=240, NE=240, E=240, SE=240 px. NW independent foot midpoint is (261,401), failing the ±4 px tolerance by 1 px on x. Other maximum contact errors are 0.75–3 px. All eight pass literal light-centroid, right-hand, 64 px read and alpha checks. Exact numbers and immutable frames: `evidence/checkpoint_1/checks.json`.

Repair plan: lower the intact staff through the stationary right-hand grip in SW and NW; keep body appearance, stance and lighting. Correct the NW registration anchor using independently observed sole contacts. Evaluate the complete repaired set once, preserving both checkpoints.


Checkpoint 2: FAIL. Staff repairs brought all silhouette heights within tolerance. The manually estimated SW anchor introduced a 5.25 px horizontal error, exceeding tolerance by 1.25 px. This was a preparation error, not evidence that the image model cannot meet pivot lock.

| Direction | Height px | Deviation | Foot error x/y px (v1) | Brightest-5% centroid | Bbox center | Light |
|---|---:|---:|---|---|---|---|
| S | 240 | +0.00% | 2.75 / 0.50 | 227.58, 224.25 | 246.00, 295.50 | PASS |
| SW | 241 | +0.42% | 5.25 / 0.00 | 228.44, 238.92 | 247.00, 298.00 | PASS |
| W | 240 | +0.00% | 1.75 / 1.00 | 248.28, 241.77 | 256.00, 292.50 | PASS |
| NW | 240 | +0.00% | 2.00 / 0.00 | 227.13, 227.58 | 243.50, 285.50 | PASS |
| N | 240 | +0.00% | 1.50 / 0.00 | 250.93, 217.48 | 262.50, 284.50 | PASS |
| NE | 240 | +0.00% | 3.00 / 0.00 | 268.59, 234.71 | 272.50, 295.50 | PASS |
| E | 240 | +0.00% | 0.75 / 0.50 | 249.24, 223.51 | 255.50, 296.50 | PASS |
| SE | 240 | +0.00% | 3.00 / 0.00 | 228.42, 229.88 | 248.00, 295.50 | PASS |

A post-stop instrument audit found that the v1 sole locator accepted review regions
that intersected contacts at their boundaries. W, NW, NE and E pivot readings above
are therefore **unverified**, even though v1 marked them passed. The stricter audit
still confirms SW fails and S/N/SE pass. See `evidence/instrument_audit.json`. No
checkpoint was overwritten or relabeled. The original checker is preserved as
`evidence/checkpoint_checker_v1.py`; current `check.py` rejects clipped sole regions.

Gate 1 PASS (240–241 px, maximum +0.42%); gate 2 FAIL / some readings unverified;
gate 3 PASS (all eight centroids above and left of their bbox centers); gate 4 PASS
(visual anatomical-right grip); gate 7 PASS (hood/staff readable in saved 64 px
strip). Handedness and direction observations are in `visual_review.json`.

Alpha format: all eight frames have more than 50% transparent pixels, no opaque
border pixel, and zero measured green-contaminated partial-alpha pixels. Native S
alpha was preserved; seven views were extracted from intentionally green plates.
Dark, light and blue comparisons are retained in `prepared/*/edge_review.png`.
This is a character matte result, not a VFX gate-9 result. Camera accuracy remains
visual and approximate; reference guides do not prove exact generated geometry.

## 4. Animation results

Not generated after the second failed turnaround. Gates 5–6 NOT TESTED. Required counts unchanged: idle 8, walk 8, cast 12 per direction. Cast spawn index 5 (sixth frame). Loop comparisons use alpha-composited RGB over the fixed dark preview background, with both full-canvas and foreground-union results recorded. The cross-animation comparison frame is fixed to cast release index 5 before measuring drift. Loop seam is tested against the minimum internal adjacent-pair difference, following the literal wording “no larger than any other pair.”

## 5. VFX results

No VFX art was generated after the mandatory stop. Gates 8–10 NOT TESTED; cast/travel/impact requirements remain 8/6/10. There is no actual character release frame for the style comparison or S/E spawn composite. VFX quality cannot be inferred from the character outcome.

## 6. Scope reductions

The delivered character contains 8 idle-00 frames out of 224 required frames. Missing:
56 further idle frames, 64 walk frames and 96 cast frames. Missing VFX: all 24 frames
and emissive masks. Sprint and Godot remain optional and unattempted. The viewer is
a static checkpoint comparison with direction, attempt and background selectors;
playback and combined mode are explicitly disabled. Atlas metadata records actual
counts, intended counts and rejected status, without padding frames or fake loops.

The original brief's rule “If consistency collapses (turnaround fails twice), stop,
write up what failed and why, and deliver what exists” was reached. This is the
reason for stopping generation, not a claimed tool limitation or permission block.

## 7. CHARACTER verdict

**FAIL.** The revised process substantially improved the measurable turnaround:
all final heights and literal light tests pass, and all eight mattes are usable
RGBA instead of painted checkerboards. SW still misses pivot tolerance, and four
other contact readings need better inspection regions. My manual anchor estimation
and permissive ROI validation were preparation defects. The incomplete animation
set cannot qualify as the requested character asset.

## 8. VFX verdict

**PARTIAL — NOT TESTED.** No frost modules exist in this run. There is no evidence
for a style, alpha or composite pass/fail, and the character outcome does not show
that VFX generation would fail. The required stop prevented reaching this section.

## 9. Timing and generation calls

Session started approximately 2026-09-09 00:25 UTC; packaging completed around
01:00 UTC (about 35 minutes including analysis, tool latency and validation).
Built-in generation: 10 calls, 266.2 seconds measured tool time: master 1 call /
36.2 s; remaining seven directions 7 calls / 180.3 s; staff repairs 2 calls / 49.7 s.
Animation and VFX: zero calls. Exact prompts, source paths and per-call timing:
`generation_log.json` and `prompts/`. Model/backend and seeds are not exposed.

## 10. Further changes

Implemented a qualified-master workflow, fixed pose-reference projection, native
alpha / green-plate handling, uniform registration, immutable full-set checkpoints,
raw-versus-prepared measurements, stricter contact validation, packaging and a
review viewer. `PROCESS.md` documents how to use these tools and the remaining
animation/VFX sequence; the latter has not been validated on generated motion.

The next process change is to **derive source anchors from reviewed sole regions**
using `registration_preflight.measured_anchor`, then inspect independent output
regions before committing a full checkpoint. The helper and clipped-region guard
are implemented and pass synthetic tests, but have not been used to claim a third
art checkpoint. Manual thumbnail anchor estimates should not decide pass/fail.
For overlapping feet, explicit contact annotation and uncertainty are necessary.
Do not loosen the tolerance or redefine the silhouette to rescue this run.

Validation: seven Python instrument tests pass, covering known-alpha matting,
native-alpha dark interiors, checkerboard rejection, upscaling rejection, measured
registration, clipped-contact rejection, and wrong-side light/clipping detection.
The browser runtime returns an empty browser list, so interactive browser QA is
unavailable. Preview JavaScript syntax and local asset/atlas integrity are checked
separately; neither is represented as visual browser verification.

Delivery: `character/`, `preview/index.html`, both immutable evidence directories,
source artwork, prompts, scripts and JSON measurements. PNGs and ZIP are local
artifacts under the existing ignore policy. The local archive includes them; the
source/evidence records are committed without unrelated workspace files. No push.

