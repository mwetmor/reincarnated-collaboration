#!/bin/bash
# C-9 T10-2 step 4 -- THE FILM FOR MATT'S LOOK: him on the tarn path, through a ring stone's
# painted shadow, past the door, a slash beside a stone (godot/tools/film_painted.gd).
#
# Movie Maker writes the frames into ONE .avi (MJPEG, no frame dump) at a fixed 24 fps; it is
# encoded to MP4 here and the .avi deleted. FULLSCREEN, so the frame is the play frame itself
# (1920 x 1080 on this display, the 16:9 lock). The settling frames (the scene building) are trimmed
# at the count the film script prints. No audio: Movie Maker's track is silence.
#
#   usage: tools/film_painted.sh OUT_DIR
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../godot
OUT=${1:?usage: film_painted.sh OUT_DIR}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
mkdir -p "$OUT"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" >&2; exit 9; fi
AVI="$OUT/painted_film.avi"
LOG="$OUT/film_painted.log"
MP4="$OUT/C-9 barrow painted - the tarn path, a stone's shadow, the door, a slash.mp4"
rm -f "$AVI"
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$SRC" --fullscreen --fixed-fps 24 \
  --write-movie "$AVI" --script tools/film_painted.gd > "$LOG" 2>&1 || true
grep -E "\[film\]|SCRIPT ERROR|Parse Error|ERROR:" "$LOG" | head -20
[ -f "$AVI" ] || { echo "HALT: no movie written" >&2; exit 5; }
TRIM=$(grep -o '"trim_frames":[0-9]*' "$LOG" | head -1 | cut -d: -f2)
[ -n "$TRIM" ] || { echo "HALT: the film never reported its trim (did it finish?)" >&2; rm -f "$AVI"; exit 6; }
ffmpeg -y -loglevel error -i "$AVI" -vf "trim=start_frame=${TRIM},setpts=PTS-STARTPTS" \
  -an -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -movflags +faststart "$MP4"
rm -f "$AVI"
ffprobe -v error -show_entries stream=width,height,nb_frames,r_frame_rate -show_entries format=duration -of compact "$MP4"
echo "== film: $(du -h "$MP4" | cut -f1), trimmed ${TRIM} settling frames, movie file removed"
