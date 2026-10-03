#!/bin/bash
# barrow_v2 (lane BX): the greybox stills and the walk film, behind the heavy lock and the disk gate.
#   tools/greybox_godot.sh views     -> greybox/V*.png (ZOOM-GD 25 x 18 m windows + one plate-scale start)
#   tools/greybox_godot.sh establish -> greybox/E0_establishing.png (the whole site, 1800 x 1440, labels off)
#   tools/greybox_godot.sh film      -> greybox/barrow_v2_greybox_walk.mp4 (Movie Maker MJPEG -> x264)
# HALTS (exit 9) under DISK_GATE_GIB (21, conductor 2026-10-03) free. The film's intermediate .avi is written to the session
# scratch dir given as SCRATCH (never into the repo) and is NOT deleted here (no deletions in this lane).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
MODE=${1:?usage: greybox_godot.sh views|film}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-21}
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
echo "== free disk: ${FREE} GiB (gate ${GATE})"
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free"; exit 9; fi
OUT="$ROOT/greybox"
mkdir -p "$OUT"
if [ "$MODE" = views ]; then
  python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$ROOT/godot" --resolution 1920x1080 \
    --script tools/greybox_run.gd -- views "$OUT" 2>&1 | tee "$OUT/views.log" | grep -E "\[bv2\]|ERROR|Parse" || true
elif [ "$MODE" = establish ]; then
  python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$ROOT/godot" --resolution 1800x1440 \
    --script tools/greybox_run.gd -- establish "$OUT" 2>&1 | tee "$OUT/establish.log" | grep -E "\[bv2\]|ERROR|Parse" || true
else
  SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir outside the repo for the intermediate .avi}
  AVI="$SCRATCH/bv2_walk.avi"
  MP4="$OUT/barrow_v2_greybox_walk.mp4"
  python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$ROOT/godot" --resolution 1280x720 --fixed-fps 24 \
    --write-movie "$AVI" --script tools/greybox_run.gd -- film > "$OUT/film.log" 2>&1 || true
  grep -E "\[bv2\]|ERROR|Parse" "$OUT/film.log" | head -20
  TRIM=$(grep -o '"trim_frames":[0-9]*' "$OUT/film.log" | head -1 | cut -d: -f2)
  [ -n "$TRIM" ] || { echo "HALT: no trim reported"; exit 6; }
  ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" \
    -an -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -movflags +faststart "$MP4"
  ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration -of compact "$MP4"
  echo "== film: $(du -h "$MP4" | cut -f1); intermediate kept at $AVI ($(du -h "$AVI" | cut -f1))"
fi
