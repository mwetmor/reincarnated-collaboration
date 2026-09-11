# E07L · Geometry-derived pilot floor shadow

Godot shipping target; existing Pixi harness.45active minutes,0generation,3implementation revisions,4capture batches,50MB. Reuse E07N chamber, E07K painted pilot, E05J rig/painting and E05Q sampling. No source art edits.

Prove a directional-key floor shadow from the same skinned geometry/pose, heading, gear visibility and root transform as the visible pilot. Shared neutral key direction; map projected silhouette union into a bounded floor mask. Reduce only the occluded directional contribution, retaining ambient and point light. This is a flat-floor opaque caster mechanism, not full lighting art, soft area-light shadows, self/vertical-receiver shadows, translucent VFX or production performance. Root-height0.5m is an explicit diagnostic pose offset, not implemented jumping gameplay.

Batch1 asymmetric offscreen orientation/union/clear preflight. Source mask2048×1024 over world[-8,-4,8,4], no repeated darkening from overlapping triangles. Verify actual bounds/texel resolution;8MiB RGBA arithmetic is not measured VRAM. Refuse off-map projected geometry.

Batch2 native960×640: F01grounded idle, sparse cast, raised idle0.5m, translated idle; F02grounded idle. Save shadow-on/off art and binary floor-shadow diagnostic. Independent CPU actor ray/triangle shadow oracle plus camera floor visibility supplies>=6shadow and6lit interior witnesses per case with9pixel-neighbor guard; diagnostic RGBwithin2. Missing-shadow and stale-root controls must each fail>=1positive witness. Compare actual floor material pixels: directional shadow darkens, unaffected samples remain unchanged. Original source minimumZ/root contact retained; no animation inventory expansion.

Batch3 selected fresh2880×1920 grounded/raised/F02 controls. Batch4 savedreview and actual UI. Inspect native/fresh grounding and edges; report hard/aliased artifacts candidly. All previous failures preserved. Full pilot/door/chamber art remains unqualified regardless of mechanism outcome.
