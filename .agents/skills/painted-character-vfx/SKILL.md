---
name: painted-character-vfx
description: Create consistent painted directional character sprites, character animations and matching animated spell VFX, with measured asset gates and engine-ready packaging. Use for ASTRA sprite tests and related painted raster asset production.
---

# Painted characters and animated VFX

Read the user's asset brief and [measured lessons](references/measured-lessons.md).
For the active ASTRA campaign, also read [campaign](references/astra-campaign.md).
Keep this skill as the single workflow source; AGENTS.md only routes here.

## Establish the contract

Declare the generation tool, actual available controls and Python capabilities.
Use available image-generation tooling for painted artwork; geometry guides are
references, never replacement deliverables. Preserve originals, prompts, reference
roles, actual dimensions, alpha mode and hashes. Do not promise seed/mask controls
that the tool does not expose. Never upscale undersized artwork.

Separate artwork failures, preparation failures, invalid measurements and missing
verification. Preserve literal tests and report supplementary diagnostics separately.
Keep required frame counts and numerical thresholds fixed. Do not count a software
unit-test pass as an art pass. Freeze metrics before evaluating candidates, including
the cross-animation reference, alpha support threshold and loop comparison rule.

## Character preparation

Qualify one master with all required identity features. Simplify only incidental
ornamentation. Condition every direction on that master and a fixed camera guide;
rotate the body while retaining screen-space light. Never mirror directions.

Qualify alpha before scaling production. Preserve genuine native alpha. An explicitly
requested uniform chroma plate may be extracted when the user authorizes deterministic
matting. Never remove a checkerboard by thresholding dark pixels. Inspect edges on
dark, light and colored backgrounds. Keep matte cleanup appropriate to the subject.

Use uniform downscale and translation for registration when authorized. Derive
anchors from reviewed full-resolution support contacts; do not estimate a midpoint
from a thumbnail. For overlapping soles use explicit foot-specific polygons or
visible contour annotations. Never let a crop boundary become a measured sole.
Independently inspect output contacts and uncertainty after registration. Translation
cannot change the anatomical pose; do not use per-frame scaling to conceal drift.

Finish preparation before freezing a full turnaround checkpoint. A diagnostic
failure is still recorded even when repaired before the checkpoint. Repair identified
defects as a set. Advance animation only on a complete passing turnaround.

## Character animation

Prove a complete pilot direction before expanding. Use approved direction art plus
master identity references and explicit key poses; retain the original idle-00.
Fix physical scale per direction, track support contacts/root independently, and inspect the
feet and staff grip in motion. Generate enough native pixels for every packed cell.
If the generator changes whole-frame magnification, estimate framing scale from
unchanged hood/face landmarks against the approved direction, retaining the raw
scale and fit error. Do not fit to pose-dependent silhouette height or normalize
individual limbs. Visually verify that body proportions still agree.

Plan closed cycles with neighboring first/last phases. Do not duplicate static poses,
shuffle frames or invent motion to satisfy counts or reduce a seam metric. Test idle
and walk drift against the fixed cast comparator and report every adjacent difference,
including the seam. Check cast poses early for light-centroid failures caused by
spell illumination. Freeze a time-based cast schedule with explicit spawn index.

For a localized closing-pose edit in an unchanged source canvas, inherit the original
frame's full registration transform. Re-centering on the edited toe can shift the
entire body. Independently check the output contacts against the original tolerance;
do not inherit a passing measurement. Inspect actual alternating leg leads and
source-cell effect margins separately from the loop numbers.

## VFX animation

First qualify a painted frost sample against the actual character release frame at
the same scale. Then produce the required cast, travel and impact sequences with
consistent palette, brush edges and temporal evolution. Preserve separate particles,
shards and glow; largest-component character cleanup is unsafe for this art.

Record alpha edge statistics and inspect normal/additive composites across multiple
backgrounds. A bright mean alone does not prove absence of dark fringe. Derive
emissive masks from actual generated energy, retaining its soft boundaries. Verify
travel symmetry/loop closure and complete impact fade. Keep CHARACTER and VFX
verdicts independent; missing integration evidence is not a VFX style failure.

## Package, verify and improve

Pack actual frames, sheets and contacts with exact rects, canvas, pivot, fps, loop and
spawn metadata. Synchronize character/VFX by elapsed time, not equal frame indices.
Verify staff-tip attachment, release and cast→travel→impact from every required
integration direction in the preview. Record browser unavailability honestly and
continue independent production and checks while resolving it.

Keep a durable run state, immutable accepted milestones and rejected evidence.
After an observed failure, update measured lessons with cause, correction, evidence
and confidence. Promote only demonstrated guidance into this entrypoint. Preserve
the user's retry limits; if the user explicitly authorizes a continuing campaign,
archive failed attempts and proceed with a reasoned correction within that scope.
Do not reset counters to disguise failure or repeat unchanged expensive calls.
Stop dependent production only for a failed prerequisite, unavailable necessary
capability, exhausted explicit budget, or no remaining meaningful authorized repair.
