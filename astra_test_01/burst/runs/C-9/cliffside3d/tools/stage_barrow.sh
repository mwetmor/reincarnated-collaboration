#!/bin/bash
# C-9 T10: put the barrow's review material where Matt looks.
#
# ONE copy of each. The stills are renamed to the order they should be looked at in, because
# a folder listing is the only sequencing a reviewer gets.
#
# THE PREVIOUS SETS ARE DELETED FIRST, by an EXPLICIT LIST rather than a glob. This folder also
# holds the .app, the movie, and other sessions' material (scatter kit.png, snow lab/), and
# `rm *.png` in a directory someone else also writes to is how a review folder loses work that
# took twenty minutes to produce. Anything not on these lists is left alone.
#
#   usage: tools/stage_barrow.sh CAPTURE_DIR
set -euo pipefail

CAP=${1:?usage: stage_barrow.sh CAPTURE_DIR}
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 barrow"}
mkdir -p "$STAGE"

# the stand-in set (15:20) and the T10 integration set (17:33), by name
for old in "1 - play camera, stack ON.png" "2 - play camera, stack OFF.png" \
           "3 - the barrow, stack ON.png" "4 - the barrow, stack OFF.png" \
           "5 - him, before and after the ramp.png" "6 - snow layer off.png" \
           "7 - ink pass off.png" "8 - fog off.png" \
           "1 - play camera, the look stack ON.png" "2 - play camera, the look stack OFF.png" \
           "3 - the barrow and the stone ring.png" "4 - the barrow and the ring, stack OFF.png" \
           "5 - him beside a tall stone, for scale.png" "6 - him, before and after the ramp.png" \
           "7 - his outline, BOTH pens (the 15-20 build).png" "8 - the snow layer off.png" \
           "9 - the ink pass off.png" "10 - the fog off.png"; do
  rm -f "$STAGE/$old"
done

cp_if() { [ -f "$1" ] && cp -f "$1" "$2" || echo "   (missing: $(basename "$1"))" >&2; }

cp_if "$CAP/barrow_stack_on.png"                  "$STAGE/1 - play camera, AFTER - 3D snow, no veil.png"
cp_if "$CAP/barrow_veil_before.png"               "$STAGE/2 - play camera, BEFORE - the veil.png"
cp_if "$CAP/barrow_wide_on.png"                   "$STAGE/3 - the barrow, wide.png"
cp_if "$CAP/paint_vs_render_side_by_side.png"     "$STAGE/4 - the painting and the render, side by side.png"
cp_if "$CAP/paint_vs_render_overlay50.png"        "$STAGE/5 - the render at 50 percent over the painting.png"
cp_if "$CAP/paint_coverage_map.png"               "$STAGE/6 - coverage per class, bright = placed, dim = missed.png"
cp_if "$CAP/barrow_scale_beside_stone.png"        "$STAGE/7 - him beside a tall stone, for scale.png"
cp_if "$CAP/barrow_stack_off.png"                 "$STAGE/8 - play camera, the look stack OFF.png"
# T10-1c: the two single-variable A/Bs, each against still 1 (same run, same frame)
cp_if "$CAP/barrow_instancing_off.png"            "$STAGE/9 - A-B for 1, the same props drawn one node each.png"
cp_if "$CAP/barrow_rocks_upright.png"             "$STAGE/10 - A-B for 2, the rocks upright as in T10-1b.png"
# and the warmth, where the painting has heather: painting | the --before capture | this one
[ -f "$CAP/warmth_before_after.png" ] && cp -f "$CAP/warmth_before_after.png" \
  "$STAGE/11 - heather - the painting, before, after.png"
rm -f "$STAGE/11 - warmth - the painting, T10-1b, T10-1c.png"
# T10-1d: the shadow before the bands (T10-1c's ramp) against still 1, and the heather film
cp_if "$CAP/barrow_shadow_before_bands.png"       "$STAGE/12 - A-B for the shadow, before the bands as in T10-1c.png"
[ -f "$CAP/C-9 barrow heather in the wind.mp4" ] && cp -f "$CAP/C-9 barrow heather in the wind.mp4" \
  "$STAGE/C-9 barrow heather in the wind.mp4"
[ -f "$CAP/heather_stats.json" ] && cp -f "$CAP/heather_stats.json" "$STAGE/measurements - heather texture and clustering.json"
[ -f "$CAP/C-9 barrow walk.mp4" ] && cp -f "$CAP/C-9 barrow walk.mp4" "$STAGE/C-9 barrow walk.mp4"
cp_if "$CAP/barrow.json"                          "$STAGE/measurements - scene.json"
cp_if "$CAP/barrow_metrics.json"                  "$STAGE/measurements - frames.json"
cp_if "$CAP/paint_coverage.json"                  "$STAGE/measurements - painting coverage.json"
xattr -dr com.apple.quarantine "$STAGE" 2>/dev/null || true
echo "== staged -> $STAGE"
ls -la "$STAGE"
