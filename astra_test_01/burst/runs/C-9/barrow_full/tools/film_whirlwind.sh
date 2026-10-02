#!/bin/bash
# C-9 R-C9-128 -- the ported whirlwind (the Eye of Reckoning) on the dark knight (godot/tools/film_whirlwind.gd): play speed then quarter speed.
# 1280 x 720 at 60 fps (the arc is 10 samples at 60 fps in the source), the phone page's look; Movie Maker's .avi encoded to MP4 here (the .avi left for the cleanup manifest).
#   usage: TINT=red|original [WHO=warlord] [PLACE=u,v,F] tools/film_whirlwind.sh OUT_DIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../godot
OUT=${1:?usage: film_whirlwind.sh OUT_DIR}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
mkdir -p "$OUT"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" >&2; exit 9; fi
TINT=${TINT:-red}; ARMOR=${ARMOR:-}; PLACE=${PLACE:-0.8,-1.2,S}; WHO=${WHO:-warlord}; ACT=${ACT:-shield_bash}
SLUG=$(echo "${WHO}_${ARMOR}_${TINT}${SLUGX:-}" | tr -c "a-z0-9" "_")
AVI="$OUT/ww_${SLUG}film.avi"; LOG="$OUT/film_ww_${SLUG}.log"
MP4="$OUT/C-9 ${NAME:-dark knight} Eye of Reckoning (ported whirlwind) - ${TINT} - play speed then quarter speed.mp4"
python3 "$HEAVY_LOCK" C-9 -- perl -e 'alarm shift; exec @ARGV' 600 "$GODOT" --path "$SRC" --resolution 1280x720 \
  --rendering-method gl_compatibility --rendering-driver opengl3_angle --fixed-fps 60 \
  --write-movie "$AVI" --script tools/film_whirlwind.gd -- --as-web --c $WHO ${ARMOR:+--armor $ARMOR} --eortint $TINT --action $ACT --place $PLACE ${EXTRA:-} > "$LOG" 2>&1 || true
grep -E "\[film\]|SCRIPT ERROR|Parse Error|ERROR" "$LOG" | head -12
TRIM=$(grep -o '"trim_frames":[0-9]*' "$LOG" | head -1 | cut -d: -f2)
[ -n "$TRIM" ] || { echo "HALT: no trim reported" >&2; exit 6; }
ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" \
  -an -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart "$MP4"
ffprobe -v error -show_entries format=duration -of compact "$MP4"
