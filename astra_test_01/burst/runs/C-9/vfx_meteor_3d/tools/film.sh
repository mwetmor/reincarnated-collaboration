#!/bin/bash
# C-9 VFX BAKE-OFF, LANE B -- THE FILM: her Meteor, 3D first, in the painted Barrow, from the start of
# the cast to the burn's end: once at play speed, once at quarter speed, then both in one file.
#
# Movie Maker steps the engine at a fixed 60 fps and writes ONE MJPEG .avi per pass (compressed; no
# frame dump) into the session's scratch dir; each is encoded to MP4 here and the .avi removed (it is
# this script's own intermediate). FULLSCREEN: the frame is the play frame (1920 x 1080 on this
# display, the 16:9 lock). The settling frames are trimmed at the count the scene prints.
#
#   usage: tools/film.sh OUT_DIR SCRATCH_DIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../godot
OUT=${1:?usage: film.sh OUT_DIR SCRATCH_DIR}
TMP=${2:?usage: film.sh OUT_DIR SCRATCH_DIR}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
mkdir -p "$OUT" "$TMP"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" >&2; exit 9; fi
for PASS in play quarter; do
  AVI="$TMP/meteor_b_$PASS.avi"
  LOG="$OUT/film_$PASS.log"
  rm -f "$AVI"
  EXTRA=""
  [ "$PASS" = quarter ] && EXTRA="--slow"
  python3 "$HEAVY_LOCK" C-9 -- python3 "$HERE/tmo.py" 600 -- "$GODOT" --path "$SRC" --fullscreen --fixed-fps 60 \
    --write-movie "$AVI" -- --meteor b --meteor-film $EXTRA > "$LOG" 2>&1 || true
  grep -E "\[film\]|SCRIPT ERROR|Parse Error|^ERROR" "$LOG" | cut -c1-300 | head -8
  [ -f "$AVI" ] || { echo "HALT: no movie written ($PASS)" >&2; exit 5; }
  TRIM=$(grep -o '"trim_frames":[0-9]*' "$LOG" | head -1 | cut -d: -f2)
  [ -n "$TRIM" ] || { echo "HALT: no trim reported ($PASS)" >&2; rm -f "$AVI"; exit 6; }
  ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" \
    -an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart "$OUT/meteor_b_$PASS.mp4"
  rm -f "$AVI"
  ffprobe -v error -show_entries stream=width,height,nb_frames,r_frame_rate -show_entries format=duration -of compact "$OUT/meteor_b_$PASS.mp4"
done
# BOTH IN ONE FILE: play speed, then quarter speed
printf "file '%s'\nfile '%s'\n" "$OUT/meteor_b_play.mp4" "$OUT/meteor_b_quarter.mp4" > "$TMP/concat.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$TMP/concat.txt" -c copy -movflags +faststart \
  "$OUT/C-9 meteor lane B hybrid (3D + painted ground plates) - play speed then quarter speed.mp4"
ffprobe -v error -show_entries format=duration -of compact "$OUT/C-9 meteor lane B hybrid (3D + painted ground plates) - play speed then quarter speed.mp4"
