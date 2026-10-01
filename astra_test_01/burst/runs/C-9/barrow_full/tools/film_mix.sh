#!/bin/bash
# C-9 -- her DEFAULT Meteor, film for Matt (godot/tools/film_meteor.gd): play speed then quarter speed. MIX v3 (the
# default): the ball of fire with its dark core, A's painted burst, the crater, the warp, no ring, the shadow on.
# METEOR=mix2 / mix1 films the earlier mixes; TAG names the file.
# 1280 x 720, the phone page's look. Movie Maker writes one MJPEG .avi at a fixed 30 fps (no frame
# dump); it is encoded to MP4 here. The .avi is left for the cleanup manifest (no rm).
#   usage: tools/film_fireball.sh OUT_DIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../godot
OUT=${1:?usage: film_fireball.sh OUT_DIR}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
mkdir -p "$OUT"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" >&2; exit 9; fi
METEOR=${METEOR:-}
TAG=${TAG:-MIX v3 - ball of fire with dark core, A painted impact, crater, warp}
SLUG=$(echo "${METEOR:-mix3}" | tr -c "a-z0-9" "_")
AVI="$OUT/meteor_${SLUG}film.avi"
LOG="$OUT/film_${SLUG}.log"
MP4="$OUT/C-9 sorceress Meteor $TAG - play speed then quarter speed.mp4"
python3 "$HEAVY_LOCK" C-9 -- perl -e 'alarm shift; exec @ARGV' 900 "$GODOT" --path "$SRC" --resolution 1280x720 \
  --rendering-method gl_compatibility --rendering-driver opengl3_angle --fixed-fps 30 \
  --write-movie "$AVI" --script tools/film_meteor.gd -- --as-web --c sorceress ${METEOR:+--meteor $METEOR} > "$LOG" 2>&1 || true
grep -E "\[film\]|SCRIPT ERROR|Parse Error" "$LOG" | head -10
TRIM=$(grep -o '"trim_frames":[0-9]*' "$LOG" | head -1 | cut -d: -f2)
[ -n "$TRIM" ] || { echo "HALT: no trim reported" >&2; exit 6; }
ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" \
  -an -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart "$MP4"
ffprobe -v error -show_entries stream=width,height,nb_frames -show_entries format=duration -of compact "$MP4"
