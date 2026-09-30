#!/bin/bash
# C-9 T10: capture + measure the barrow stack, then encode the walk straight to MP4.
#
# THREE OPERATIONAL FACTS THIS SCRIPT EXISTS TO HANDLE, none of them about the stack:
#
# 1. THE WORKING TREE IS SHARED AND knight.gd IS BEING EDITED BY ANOTHER SESSION (the armed
#    motion set). A capture that starts while that file is half-written dies on a parse error
#    twelve minutes in. So the scripts are parse-checked first and the run WAITS for them,
#    rather than failing and being mistaken for a defect in this scene.
#
# 2. THIS IS AN 8 GB M2 AND THERE ARE OTHER GODOT PROCESSES. An unlocked run competed with
#    two of them and made no progress at 3.5% CPU. Heavy work goes through the shared
#    advisory lock so the runs serialise.
#
# 3. DISK. ~56 GiB free and another run halts at 40. The walk frames are written to the
#    session scratchpad, encoded, and DELETED -- no frame dump survives the run.
#
#   usage: tools/barrow_capture.sh OUT_DIR [WALK_FRAMES]
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)/godot
OUT=${1:?usage: barrow_capture.sh OUT_DIR [WALK_FRAMES]}
WALK=${2:-380}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
FRAMES="$OUT/frames"

mkdir -p "$OUT"
FREE=$(df -g /Users/admin | awk 'NR==2{print $4}')
echo "== free disk: ${FREE} GiB"
# the storage gate is 25 GiB since R-C9-87 (Matt, 2026-09-29); it was 42
if [ "$FREE" -lt 20 ]; then echo "HALT: under 20 GiB free (R-C9-88)" >&2; exit 9; fi

# --- 1. wait for the shared scripts to parse -------------------------------
cat > "$SRC/tools/drax_parse.gd" <<'EOF'
extends SceneTree
func _initialize() -> void:
	var bad := 0
	for p in ["res://scripts/knight.gd", "res://scripts/gear.gd", "res://scripts/paint_stack.gd",
			  "res://scripts/barrow_stand_in.gd", "res://scripts/barrow_flat.gd",
			  "res://scripts/snow_field.gd", "res://scripts/barrow_instancer.gd",
			  "res://scripts/barrow_heather.gd",
			  "res://scripts/barrow_heightfield.gd", "res://scripts/barrow_world.gd",
			  "res://tools/shot_barrow.gd"]:
		if load(p) == null:
			print("PARSE_FAIL %s" % p)
			bad += 1
	print("PARSE_BAD=%d" % bad)
	quit(0)
EOF
for i in $(seq 1 40); do
  LOG=$("$GODOT" --headless --path "$SRC" --script tools/drax_parse.gd 2>&1 || true)
  if echo "$LOG" | grep -q "PARSE_BAD=0" && ! echo "$LOG" | grep -q "Parse Error"; then
    echo "== scripts parse clean (attempt $i)"; break
  fi
  echo "== attempt $i: shared scripts not parseable yet (another session is mid-edit); waiting 45 s"
  echo "$LOG" | grep -E "Parse Error|PARSE_FAIL" | head -3
  if [ "$i" -eq 40 ]; then rm -f "$SRC/tools/drax_parse.gd"; echo "HALT: scripts never became parseable" >&2; exit 8; fi
  sleep 45
done
# the parse probe is scratch, not a work-product; it lives in the project only because
# Godot can only load scripts through res://
rm -f "$SRC/tools/drax_parse.gd" "$SRC/tools/drax_parse.gd.uid"

# --- 2. capture, under the lock -------------------------------------------
# The OS window is small on purpose: every still and every movie frame is read from a
# 1920x1080 SubViewport, so the window renders nothing that is kept and paying for it twice
# on a shared GPU buys nothing. The camera law reads its rows from the SubViewport, and the
# report states which -- if `viewport_rows` ever comes back 360 the whole capture is at the
# wrong scale and the number says so.
echo "== capture (heavy lock)"
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$SRC" --resolution 640x360 \
  --script tools/shot_barrow.gd -- --out "$OUT" --frames "$FRAMES" --walk "$WALK" 2>&1 \
  | grep -vE "^\s*$|Godot Engine v|Metal 3\.2 -" | tail -40

[ -f "$OUT/barrow.json" ] || { echo "HALT: no barrow.json produced" >&2; exit 5; }

# --- 3. the walk, straight to MP4, frames deleted -------------------------
N=$(ls "$FRAMES"/f_*.jpg 2>/dev/null | wc -l | tr -d ' ')
echo "== encode $N frames -> MP4"
if [ "$N" -gt 8 ]; then
  ffmpeg -y -loglevel error -framerate 24 -i "$FRAMES/f_%04d.jpg" \
    -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart \
    "$OUT/C-9 barrow walk.mp4"
  rm -f "$FRAMES"/f_*.jpg
  rmdir "$FRAMES" 2>/dev/null || true
  echo "== mp4: $(du -h "$OUT/C-9 barrow walk.mp4" | cut -f1), frames removed"
else
  echo "WARN: only $N frames; no MP4" >&2
fi

# --- 4. the numbers --------------------------------------------------------
echo "== metrics"
python3 "$(dirname "$0")/barrow_metrics.py" --dir "$OUT" --json "$OUT/barrow_metrics.json" \
  > /dev/null
echo "== done: $OUT"
ls -la "$OUT"
