#!/bin/bash
# BV2F LV Phase 1.3: the class-tinted guide + ID render of layout v7b through the FROZEN Tier-B tools (godot_run.sh only),
# one guide section at a time (2 x 2 sections of 5888 x 4352 = the 11,776 x 8,704 paint envelope at v1's px/m).
#   bash fid/lv/tools/lv_guide_run.sh [s00 s01 s10 s11]
set -uo pipefail
F=$(cd "$(dirname "$0")/../.." && pwd)            # fid/
G=$(cd "$F/../../barrow_full/godot" && pwd)
SECS=${*:-s00 s01 s10 s11}
for s in $SECS; do
  O=$F/lv/guide/$s; mkdir -p "$O"
  BV2F_SECTION=$s bash "$F/v1tools/godot_run.sh" "$G" tierB/barrow_full/godot/tools/capture_blockout.gd -- --out "$O" --no-walks --no-cost \
    --frame-grid "$F/lv/v7b/frame_grid_$s.json" > "$O/capture.log" 2>&1; rc=$?
  echo "[lv_guide] $s capture rc=$rc $(grep -c 'SCRIPT ERROR' "$O/capture.log") script errors"
  [ $rc -eq 0 ] || exit $rc
  BV2F_SECTION=$s bash "$F/v1tools/godot_run.sh" "$G" tierB/barrow_full/godot/tools/capture_ids.gd -- --out "$O" \
    --frame-grid "$F/lv/v7b/frame_grid_$s.json" > "$O/ids.log" 2>&1; rc=$?
  echo "[lv_guide] $s ids rc=$rc $(grep '\[ids\] ids.png' "$O/ids.log")"
  [ $rc -eq 0 ] || exit $rc
done
