#!/bin/bash
# C-9 T10-1d -- the heather film: him wading through a heather patch in the wind.
#
# Movie Maker writes the frames into ONE .avi (no frame dump); it is encoded to MP4 here and
# the .avi deleted. The first frames (the scene building) are trimmed off.
#
#   usage: tools/film_heather.sh OUT_DIR [heather_mode]
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
OUT=${1:?usage: film_heather.sh OUT_DIR [heather_mode]}
MODE=${2:-}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
mkdir -p "$OUT"
FREE=$(df -g /Users/admin | awk 'NR==2{print $4}')
if [ "$FREE" -lt 20 ]; then echo "HALT: under 20 GiB free (R-C9-88)" >&2; exit 9; fi
AVI="$OUT/heather_film.avi"
rm -f "$AVI"
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$SRC" --resolution 1280x720 --fixed-fps 24 \
  --write-movie "$AVI" --script tools/film_heather.gd 2>&1 \
  | grep -E "\[film\]|SCRIPT ERROR|ERROR:|at: " | head -20
[ -f "$AVI" ] || { echo "HALT: no movie written" >&2; exit 5; }
ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=81,setpts=PTS-STARTPTS" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart \
  "$OUT/C-9 barrow heather in the wind.mp4"
rm -f "$AVI"
echo "== film: $(du -h "$OUT/C-9 barrow heather in the wind.mp4" | cut -f1), movie file removed"
