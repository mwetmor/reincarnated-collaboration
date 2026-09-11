# E03M — explicit runtime masks for opaque painted assets

Registered after E03 pillar-v1 intake failed native alpha, before masked runtime renders. Retain E03's native-alpha FAIL. The observed built-in imagegen output is RGB with a baked checkerboard. A runtime geometric/silhouette mask is a different representation, not recovered alpha and not an art edit. Original pixels remain byte-identical.

Test one manually annotated pillar silhouette and, only if its native alpha also fails, one manually annotated character silhouette. Every renderer consumes identical source-space polygon vertices. Godot uses a textured Polygon2D, Pixi a Graphics mask, Phaser a GeometryMask. No Python painting/matting and no automatic threshold extraction. Concave polygons and explicit internal holes must be represented if needed; do not fill visible gaps with background. Annotation uncertainty is reported in source pixels and transformed into native screen pixels.

Acceptance: at native 960×640, unintended background fringe or removed silhouette ≤1px along inspected contour; zero large enclosed background patches. Inspect both dark and light controls plus 3× enlarged native captures. Projected pillar base silhouette vs expected geometric footprint ≤3px. Source alpha verdict stays FAIL even if runtime-mask composition passes. Masked RGB limits fine hair, translucency, cloth motion and gear decomposition; it is not automatically a scalable character pipeline.

Use the existing E03 time/disk/generation/capture counters; no reset or new generation allowance. Record all three engines' results. If this mask representation fails, retain the comparison and identify the blocked assets rather than silently passing placeholders. Final painted quality remains provisional pending Matt review.
