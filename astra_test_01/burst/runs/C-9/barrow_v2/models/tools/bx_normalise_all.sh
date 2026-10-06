#!/bin/bash
# lane BX (R-C9-156): normalise the 9 reduced Tripo builds into godot/models/build/<slot>.glb with BVP's
# bvm_normalise_blender.py (front -> +Z, origin = footprint centre on the ground, per-axis metres), behind the
# heavy lock and the disk gate; stills (turntable + game camera) -> models/stills/.
#   usage: models/tools/bx_normalise_all.sh [yaw_fix overrides as name=deg ...]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); M=$(cd "$HERE/.." && pwd); ROOT=$(cd "$M/.." && pwd)
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
mkdir -p "$ROOT/godot/models/build" "$M/stills"
yaw_of() { local n=$1 kv; for kv in $OVR; do [ "${kv%%=*}" = "$n" ] && { echo "${kv#*=}"; return; }; done; echo 0; }
OVR="$*"
ONLY=${ONLY:-}
# name  slot-file      W     D    H
while read -r name slot W D H; do
  F=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$F" -lt 21 ] && { echo "HALT: ${F} GiB free"; exit 9; }
  if [ -n "$ONLY" ] && ! echo " $ONLY " | grep -q " $name "; then continue; fi
  y=$(yaw_of "$name")
  python3 "$LOCK" C-9 -- blender --background --python "$HERE/bvm_normalise_blender.py" -- \
    "$M/reduced/$name.glb" "$ROOT/godot/models/build/$slot.glb" "$W" "$D" "$H" "$y" "$M/stills" "$name" > "$M/work/normalise_$name.log" 2>&1
  echo "$name -> $slot.glb yaw_fix $y : $(grep -h '\[bvm\]' "$M/work/normalise_$name.log" | head -1)"
done <<'TABLE'
hall longhall 24.0 8.0 6.5
porch hall_porch 8.1 3.0 11.3
gable fallen_gable 6.0 8.0 2.8
barrow barrow 22.2 15.0 17.3
wreck wreck 17.0 4.6 8.0
cavecliff cavecliff 19.5 2.0 9.9
staircliff staircliff 16.0 5.0 7.4
cliffplain cliffplain 9.0 6.0 7.4
crag crag 6.0 5.0 3.5
TABLE
