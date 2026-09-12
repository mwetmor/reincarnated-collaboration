# T0-b gate port

Run from the burst directory:

```
PYTHONDONTWRITEBYTECODE=1 python3 gates/run_gates.py --frames-dir /path/to/character/frames --master /path/to/idle/S/idle_S_00.png --out checks.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Every gate returns the SPEC section 1 envelope (some return multiple envelopes).
`common.measure`, `common.difference`, and `register` retain the run_02/run_03
measurement definitions. Empty foreground union is represented by null rather
than a non-JSON NaN. Invalid reviewed region bounds are rejected explicitly.

`matte.extract` returns `(image, details)` with run_02 character dust cleanup by
default. `preserve_particles=True` retains detached particles. The single-call
`remove_chroma_key` returns the image. No dark-interior RGB classification is used.

`guides.PROJECTION_C` contains the complete numerical E01 candidate C record and
is `DEFAULT_PROJECTION`; `RUN_02` preserves the old affine constants. `constants(name)` returns an independent copy of either set. No camera geometry
is inferred from these records.

G1 compares measured alpha bbox height to the supplied S master. G3 uses stable
sorting of the brightest 5 percent. G5 includes closure in the adjacent set and
compares canvas MAD against frame zero versus cast 05. Both canvas and foreground
union MAD are retained in notes. G6 is literal minimum-internal; G6b uses the median.
`drift48` reduces RGBA with LANCZOS before applying the same composite and comparator.

G2 has three distinct outputs: independent reviewed root anchor, visible two-sole
midpoint, and reviewed planted-sole trajectory. `run(..., regions=, anchors=,
plants=)` accepts explicit annotations; nothing is loaded implicitly. Region and
anchor keys are `animation/direction/filename.png`; plant keys are `animation/direction`.
Planted points have shape T x F x 2 with persistent foot IDs; planted flags are
T x F. Optional `expected_leads` tests a supplied reviewed schedule. This is a
trajectory instrument, not an inferred anatomical gait classifier. Root and plant
verdicts remain null when annotations are absent. The legacy midpoint is not a root.

G9 records clipping, green edge contamination, and partial-alpha mean RGB. The
allowed source provides a visual dark-fringe judgment, not a calibrated numeric
cutoff. `dark_threshold` enables an explicit caller-calibrated edge-mean screen;
without it the fringe verdict is null. Localized halos still require visual review.
Silhouette64 returns seven Hu moments and centroid/area-aligned IoU and contour
distance. `distance(a,b)` is 1 minus aligned IoU. Verdict thresholds are caller-set.

`pack.package(frames_dir, out_dir)` preserves the character sheet/atlas/contact
layout, including missing-frame availability. `composite_sockets` preserves the
blue-frost selector and the two reviewed recovery sockets. `vfx_atlas` preserves
package.py metadata and accepts an explicit packing callback: its original
`vfx.py` pixel packer is outside the authorized source list, so equivalent VFX
pixel packing is not claimed. `review.build_review` embeds the original playback
HTML, with JSON script escaping; supply character, VFX, and socket dictionaries.
Place the output under preview/ beside the character/ and vfx/ folders.

## Regression evidence

The test compares 1,880 recorded quantities at 0.001 tolerance. Six differences
remain, all in walk/SE/walk_SE_07.png sole coordinates/midpoint. The legacy source
consults output_contact_regions.json, which was not authorized for reading. The
port uses the literal automatic fallback and does not derive annotations from
expected results. The strict regression test intentionally remains red. Full
values are in tests/gates_regression_diff.json; height, pair MAD, and cross-cast
MAD match. tests/gates_current_checks.json is actual CLI output, not copied evidence.

Existing lane tests use test-owned contract fixtures because production register
and receipt schema files were outside this burst's read allowlist. Their v1.1 type
expectations and temporary-directory locations were amended; all existing lane
tests remain green. No production schema validation is claimed by that fixture test.
