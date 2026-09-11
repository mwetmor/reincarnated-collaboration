# E07Z — per-pixel mesh depth in the installed Pixi harness

Changed rendering method after E07D brace discontinuity. Keep its exact prop geometry, materials, camera C and pure state. Test actual installed8.20.1 WebGL depth handling; capability is not assumed from docs. Godot shipping target; Pixi test harness.

Limits30active minutes,0imagegen/paid calls,2adapter revisions,3capture batches,40MB. Batch01 minimal overlapping-mesh depth/clear probe; batch02 existing F01 chamber/prop painter versus depth, native/fresh3× plus part-ID controls; batch03 saved review. Stop if capability unavailable; register source-baked nativeRGBA prop alternative next, without relabelling this test.

Minimal capability: context has actual depth bits, near object wins overlapping pixels in both draw orders, deliberately disabled depth fails reversed order, and depth is cleared correctly on a changed next frame. Each check uses GPU pixels, not reported state flags only.

Scene proof: retain C camera/world/screen≤0.5logicalpx tolerance. Add true perspective clip depth and w to mesh vertices; preserve source geometry/UV/material pixels. CPU ray/triangle intersections through chosen pixel centers provide an independent first-visible-part oracle for visible crate braces/chest bands. Require exact part-ID agreement within2RGB channel values at interior samples. Depth-enabled normal/reversed draw orders must agree on the samples; depth-disabled known-bad sorting must fail at least one. Inspect native960×640 and fresh2880×1920 artwork for continuous braces and no new surface-order defect. Do not claim complete actor motion/transparency/VFX depth or full art/architecture pass from opaque mesh success.

Read-only capability sources: official State API documents depthTest/depthMask; actual installed code exposes them and an ALL depth-clear flag. These do not establish working framebuffer depth until batch01 pixels pass. Keep adapter changes in the named adapter; no Pixi types in source geometry/state/manifests.
