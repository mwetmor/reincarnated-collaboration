#!/bin/bash
# C-9 probe R-C9-34: record the GROK/RIG side-by-side comparison and mux it to MP4.
#   usage: tools/record_rig_ab.sh <output.mp4>
#   env:   GODOT, HEAVY_LOCK, REC_FPS (30), REC_WALK (3.5), REC_IDLE (3.0), REC_POS
# Needs a real window, so no --headless; --fixed-fps must equal REC_FPS or the movie
# plays back at the wrong speed while every frame looks correct.
set -euo pipefail
SRC=$(cd "$(dirname "$0")/.." && pwd)
MP4=${1:?usage: record_rig_ab.sh <output.mp4>}
FPS=${REC_FPS:-30}
WALK=${REC_WALK:-3.5}
IDLE=${REC_IDLE:-3.0}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
FRAMES=${REC_FRAMES:-$(mktemp -d "${TMPDIR:-/tmp}/c9_rig_ab.XXXXXX")}

echo "== frames -> $FRAMES  (2x${WALK}s walk + 2x${WALK}s run + 2x${IDLE}s idle @ ${FPS}fps)"
rm -f "$FRAMES"/f_*.jpg
REC_OUT="$FRAMES" REC_FPS="$FPS" REC_WALK="$WALK" REC_IDLE="$IDLE" \
  python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$SRC" \
    --resolution 1920x1080 --fixed-fps "$FPS" --script tools/record_rig_ab.gd

N=$(ls "$FRAMES"/f_*.jpg 2>/dev/null | wc -l | tr -d ' ')
WANT=$(python3 -c "print(4*round($WALK*$FPS)+2*round($IDLE*$FPS))")
echo "== captured $N frames (want $WANT)"
[ "$N" = "$WANT" ] || { echo "FAIL: frame count $N != $WANT" >&2; exit 4; }

mkdir -p "$(dirname "$MP4")"
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FRAMES/f_%04d.jpg" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart "$MP4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MP4")
echo "== $MP4   $(du -h "$MP4" | cut -f1)   ${DUR}s"
python3 - "$DUR" "$(python3 -c "print(4*$WALK+2*$IDLE)")" <<'PY'
import sys
got, want = float(sys.argv[1]), float(sys.argv[2])
if abs(got - want) > 0.4:
    sys.exit(f"FAIL: mp4 is {got:.2f}s, expected {want:.2f}s -- --fixed-fps and REC_FPS disagree?")
print(f"   ok   duration {got:.2f}s within 0.4s of {want:.2f}s")
PY
