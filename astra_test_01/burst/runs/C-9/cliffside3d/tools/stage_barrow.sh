#!/bin/bash
# C-9 T10: put the barrow's review material where Matt looks.
#
# ONE copy of each, per the brief. The stills are renamed to the order they should be looked
# at in, because a folder listing is the only sequencing a reviewer gets, and "stack on"
# beside "stack off" alphabetically is not the pair anyone wants to compare first.
#
#   usage: tools/stage_barrow.sh CAPTURE_DIR
set -euo pipefail

CAP=${1:?usage: stage_barrow.sh CAPTURE_DIR}
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 barrow"}
mkdir -p "$STAGE"

cp -f "$CAP/barrow_stack_on.png"            "$STAGE/1 - play camera, stack ON.png"
cp -f "$CAP/barrow_stack_off.png"           "$STAGE/2 - play camera, stack OFF.png"
cp -f "$CAP/barrow_wide_on.png"             "$STAGE/3 - the barrow, stack ON.png"
cp -f "$CAP/barrow_wide_off.png"            "$STAGE/4 - the barrow, stack OFF.png"
[ -f "$CAP/barrow_char_before_after.png" ] && \
  cp -f "$CAP/barrow_char_before_after.png" "$STAGE/5 - him, before and after the ramp.png"
cp -f "$CAP/barrow_snow_off.png"            "$STAGE/6 - snow layer off.png"
cp -f "$CAP/barrow_ink_off.png"             "$STAGE/7 - ink pass off.png"
cp -f "$CAP/barrow_fog_off.png"             "$STAGE/8 - fog off.png"
[ -f "$CAP/C-9 barrow walk.mp4" ] && cp -f "$CAP/C-9 barrow walk.mp4" "$STAGE/C-9 barrow walk.mp4"
cp -f "$CAP/barrow.json"                    "$STAGE/measurements - scene.json"
cp -f "$CAP/barrow_metrics.json"            "$STAGE/measurements - frames.json"
xattr -dr com.apple.quarantine "$STAGE" 2>/dev/null || true
echo "== staged -> $STAGE"
ls -la "$STAGE"
