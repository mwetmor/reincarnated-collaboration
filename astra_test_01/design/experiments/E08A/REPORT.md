# E08A — neutral frame atlas: scoped pass

[Open the comparison](review.html). All 48 frames reconstruct exactly in RGBA from the packed atlas and archival hidden-RGB sidecar; 102 structural checks pass. The engine-neutral manifest retains 60fps, 0.8s timing, crop-adjusted pivots and original source hashes. The Pixi adapter imports rects and pivots from those fields.

All 48 matched original/atlas GPU composites pass the preregistered tolerance: maximum channel delta 2; worst changed-pixel fraction 0.003478 (0.348%, below 1%). The deliberately shifted pivot is detected (delta137, 4.395% changed). Rect and fps controls are rejected by structural checks. Scope: existing E05B frames at 50/150px in this Chrome/Pixi test, not every renderer.

The runtime atlas is 1024×2048, 1,304,124 compressed PNG bytes. Base-level RGBA texel arithmetic falls from 50,331,648 bytes (48MiB) to 8,388,608 (8MiB), an 83.3% reduction. This is not measured driver memory or production crowd capacity. The archival sidecar preserves invisible RGB beneath zero-alpha exterior pixels; runtime does not load it.

Failure retained: packing v1 included hidden RGB dithering across the entire source canvas, resulting in a 1024×32768 atlas and greater texel cost despite structural correctness. No GPU import was attempted. V2 trims only fully transparent exterior pixels, preserves all visible RGBA unchanged and adjusts pivots mathematically. Original source files remain unchanged.

Visual inspection at 50/150px agrees with the numeric composite result; the long robe still hides the support boots. Packaging does not qualify painted motion, advanced gear or material style. Next: use this manifest/packing method after the next source-art pilot passes, then measure actual target hardware and representative scene loads.
