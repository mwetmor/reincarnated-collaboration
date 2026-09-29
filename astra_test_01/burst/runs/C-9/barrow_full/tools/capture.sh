#!/bin/bash
# C-9 T10-2 step 1: capture + measure the blockout (behind the heavy lock, after the disk
# check), then finalize: acceptance numbers, the layout merge, the map, the paint staging.
# Stills are written by Godot straight to PNG; there is no frame dump.
#   usage: tools/capture.sh [extra capture args, e.g. --no-walks --no-cost]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$(cd "$HERE/.." && pwd)/captures
mkdir -p "$OUT/logs"
"$HERE/godot_locked.sh" "$OUT/logs/capture.log" -- --path . --resolution 640x360 \
  --script tools/capture_blockout.gd -- --out "$OUT" "$@"
grep -E "^\[capture\]|SCRIPT ERROR|Parse Error|ERROR" "$OUT/logs/capture.log" | head -40
python3 "$HERE/finalize.py"
