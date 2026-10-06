#!/bin/bash
# barrow_v2 SECTION SW (R-C9-158, lane BS): the pan film -- the hero runs the coast on the floor (section.json film_route),
# the camera follows at the game camera (ortho, pitch 52.95, yaw 0, ZOOM-GD), the world wearing the painting.
#   SCRATCH=<dir outside the repo> tools/section_sw_film.sh <painting.png> <out.mp4>
# Heavy lock + disk gate 21 GiB; the intermediate MJPEG .avi stays in SCRATCH (not deleted: no deletions in this lane).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PAINT=${1:?painting}; MP4=${2:?out.mp4}
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -lt 21 ] && { echo "HALT disk $FREE GiB"; exit 9; }
AVI="${SCRATCH:?}/section_sw_film_$(basename "$MP4" .mp4).avi"
python3 "$LOCK" C-9 -- "$GODOT" --path "$ROOT/godot" --resolution 1920x1080 --fixed-fps 30 --write-movie "$AVI" \
  --script tools/section_run.gd -- film "paint=$PAINT" > "$ROOT/section_sw/film.log" 2>&1 || true
grep -E "\[sw\]|SCRIPT|Parse" "$ROOT/section_sw/film.log" | head
TRIM=$(grep -o '"trim_frames":[0-9]*' "$ROOT/section_sw/film.log" | head -1 | cut -d: -f2)
ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" -an -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -movflags +faststart "$MP4"
ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration -of compact "$MP4"
echo "film $(du -h "$MP4" | cut -f1); avi kept at $AVI ($(du -h "$AVI" | cut -f1))"
