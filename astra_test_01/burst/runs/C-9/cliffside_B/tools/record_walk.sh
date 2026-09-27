#!/bin/bash
# C-9: record the knight's 8-direction walk loop in style B and mux it to MP4.
#
#   usage: tools/record_walk.sh <output.mp4> [seconds]
#   env:   GODOT, HEAVY_LOCK, REC_FPS (default 30), REC_POS
#
# The Godot side needs a real window, so this does NOT pass --headless; it DOES pass
# --fixed-fps, which must equal REC_FPS or the movie plays back at the wrong speed.
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)
MP4=${1:?usage: record_walk.sh <output.mp4> [seconds]}
SECONDS_LEN=${2:-12}
FPS=${REC_FPS:-30}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
FRAMES=${REC_FRAMES:-$(mktemp -d "${TMPDIR:-/tmp}/c9_walk_frames.XXXXXX")}

echo "== frames -> $FRAMES  (${SECONDS_LEN}s @ ${FPS}fps)"
rm -f "$FRAMES"/f_*.jpg
REC_OUT="$FRAMES" REC_FPS="$FPS" REC_SECONDS="$SECONDS_LEN" \
  python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$SRC" \
    --resolution 1920x1080 --fixed-fps "$FPS" --script tools/record_walk.gd

N=$(ls "$FRAMES"/f_*.jpg 2>/dev/null | wc -l | tr -d ' ')
WANT=$(python3 -c "print(int(round($SECONDS_LEN*$FPS/8))*8)")
echo "== captured $N frames (want $WANT)"
[ "$N" = "$WANT" ] || { echo "FAIL: frame count $N != $WANT" >&2; exit 4; }

mkdir -p "$(dirname "$MP4")"
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FRAMES/f_%04d.jpg" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart "$MP4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
echo "== $MP4   $(du -h "$MP4" | cut -f1)   ${DUR}s"
python3 - "$DUR" "$SECONDS_LEN" <<'PY'
import sys
got, want = float(sys.argv[1]), float(sys.argv[2])
if abs(got - want) > 0.4:
    sys.exit(f"FAIL: mp4 is {got:.2f}s, expected {want:.2f}s -- --fixed-fps and REC_FPS disagree?")
print(f"   ok   duration {got:.2f}s within 0.4s of {want:.2f}s")
PY
