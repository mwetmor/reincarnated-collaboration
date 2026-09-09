# ASTRA campaign — run 03

IN PROGRESS. Reuses the ten-call run-02 source artwork and corrects preparation. User authorized a continuing skill-driven campaign; previous failed checkpoints remain immutable. Original gates and required frame counts remain fixed.

Toolchain: built-in imagegen with references (backend/seed/mask controls not exposed), Python/Pillow/numpy/scipy for authorized matting, registration and packing. Source output inspected before use; no upscaling.

## Turnaround: PASS

Existing art corrected by integer translation only (0–6 px horizontally). Eight heights 240–241 px; maximum deviation 0.42%; independently re-detected contact midpoint errors ≤0.5 px on each axis. Light and alpha pass in every direction. Visual right-hand, distinct direction, visible contact and 64 px hood/staff checks pass. Global alpha contours are computed before selecting a foot region, so ROI cropping cannot manufacture a sole edge. The final review overlay was inspected. Evidence: `evidence/turnaround/checks.json` and `review.png`. Zero new image-generation calls for this checkpoint.
