# E05G — sparse modular gear mechanism

**PASS within the six-pose compositing scope. Full advanced outfit/animation/light qualification remains incomplete.** Godot is the shipping target; Pixi is the test harness.

The starter body and source actions are unchanged. Separate rigid cuirass, four overlapping shoulder pieces and an independently visible helmet are bound to the existing rig. Across all 216 source action samples, maximum attachment drift is 0.000010670m and maximum bone-relative radius variation is 0.004365%, below the registered 1mm/1% limits. This does not establish anatomical fit or visual style.

The sparse render matrix covers idle0, walk0.2/0.4, cast0.3/0.6/0.9 seconds. Body holdout hides rear gear; the adapter composites armor and head layers over the unchanged E05M base frame. No per-pose motion rewriting or starter-image repainting. Gear, fit family, pivots, frames and visibility remain JSON; simulation imports no renderer.

Actual Pixi native-buffer comparison: 36 cases across six poses, helmet shown/hidden and three backgrounds. Worst occupied-pixel mean absolute RGB error 0.838571 levels (limit1); worst fraction with any RGB channel error>8 is1.71115% (limit2%). Errors are measured on occupied sprite pixels, not diluted over the canvas. The20source-pixel bad gear shift is rejected: mean26.08 and42.27%above8. Eleven headless boundary/fit/base-hash checks and three browser checks pass. Helmet hidden preserves the equipped outfit identity.

Batch01 failed the compositing preflight. Investigation found a capture bug: clearing body material slots also reset per-polygon material indices, changing face/hair appearance in the supposed reference. Batch02 restores those indices; camera, source painting, geometry and thresholds are unchanged. Failed capture/code/error locations remain preserved. The resulting match is a bounded approximation, not pixel identity.

Visual inspection: exposed head, torso and arm poses remain recognizable and the shoulder layers follow the arms without being pasted over foreground body. The rounded ivory/brass shells are intentionally plain 3D geometry probes. They do not satisfy the F04 painted advanced-outfit criterion; no full style pass is inferred from clean alpha or numerical matches.

Limits:1of2 source-authoring revisions,4of4 capture batches (sparse source, corrected source, Pixi pixels, saved review),0generation,0paid-service spend. Source tests cover216 poses but raster comparison only6. Gear shadow/diffuse/glossy/transmission/volume ray visibility is disabled in this isolation control: final contact shadows and shared lighting with gear are unqualified. Direction coverage remains one view.

Lessons: preserve polygon material indices when swapping holdouts; an unchanged mesh file does not make a mutated render scene a valid reference. Capture actual canvas buffers for pixel metrics. Fit rejection, cosmetic visibility and render layer order are separate contracts.

Next: retain this measured gear mechanism; register a bounded full motion/view and painted gear transfer proof before scaling. The already measured E05M cast socket also permits a first painted VFX attachment/lifecycle pilot independently of final gear art. Keep all G4/G5 full gates open.
