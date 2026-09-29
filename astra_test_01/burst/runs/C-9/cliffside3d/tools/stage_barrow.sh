#!/bin/bash
# C-9 T10: put the barrow's review material where Matt looks.
#
# ONE copy of each. The stills are renamed to the order they should be looked at in, because
# a folder listing is the only sequencing a reviewer gets.
#
# THE OLD NUMBERED STILLS ARE DELETED FIRST, and by an EXPLICIT LIST rather than a glob. The
# set changed with the T10 integration -- the stand-in's hill is gone, a scale shot and an
# outline before/after are new -- so a `cp -f` over the old names would leave any still whose
# number no longer exists sitting in the folder looking current. A glob would be the obvious
# way to clear them and is the wrong one: this folder also holds the .app and the movie, and
# `rm *.png` in a directory someone else also writes to is how a review folder loses work
# that took twenty minutes to produce.
#
#   usage: tools/stage_barrow.sh CAPTURE_DIR
set -euo pipefail

CAP=${1:?usage: stage_barrow.sh CAPTURE_DIR}
STAGE=${STAGE:-"$HOME/Desktop/Astra Burst Review - 2026-09-26/C-9 barrow"}
mkdir -p "$STAGE"

# the previous set, by name. Anything not on this list is left alone.
for old in "1 - play camera, stack ON.png" "2 - play camera, stack OFF.png" \
           "3 - the barrow, stack ON.png" "4 - the barrow, stack OFF.png" \
           "5 - him, before and after the ramp.png" "6 - snow layer off.png" \
           "7 - ink pass off.png" "8 - fog off.png"; do
  rm -f "$STAGE/$old"
done

cp_if() { [ -f "$1" ] && cp -f "$1" "$2" || echo "   (missing: $(basename "$1"))" >&2; }

cp_if "$CAP/barrow_stack_on.png"            "$STAGE/1 - play camera, the look stack ON.png"
cp_if "$CAP/barrow_stack_off.png"           "$STAGE/2 - play camera, the look stack OFF.png"
cp_if "$CAP/barrow_wide_on.png"             "$STAGE/3 - the barrow and the stone ring.png"
cp_if "$CAP/barrow_wide_off.png"            "$STAGE/4 - the barrow and the ring, stack OFF.png"
cp_if "$CAP/barrow_scale_beside_stone.png"  "$STAGE/5 - him beside a tall stone, for scale.png"
cp_if "$CAP/barrow_char_before_after.png"   "$STAGE/6 - him, before and after the ramp.png"
cp_if "$CAP/barrow_stack_on_2pens.png"      "$STAGE/7 - his outline, BOTH pens (the 15-20 build).png"
cp_if "$CAP/barrow_snow_off.png"            "$STAGE/8 - the snow layer off.png"
cp_if "$CAP/barrow_ink_off.png"             "$STAGE/9 - the ink pass off.png"
cp_if "$CAP/barrow_fog_off.png"             "$STAGE/10 - the fog off.png"
[ -f "$CAP/C-9 barrow walk.mp4" ] && cp -f "$CAP/C-9 barrow walk.mp4" "$STAGE/C-9 barrow walk.mp4"
cp_if "$CAP/barrow.json"                    "$STAGE/measurements - scene.json"
cp_if "$CAP/barrow_metrics.json"            "$STAGE/measurements - frames.json"
xattr -dr com.apple.quarantine "$STAGE" 2>/dev/null || true
echo "== staged -> $STAGE"
ls -la "$STAGE"
