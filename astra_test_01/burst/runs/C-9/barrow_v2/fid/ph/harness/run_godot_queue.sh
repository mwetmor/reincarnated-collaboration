#!/bin/zsh
# BV2F lane PH: every Godot run the harness needs, each behind the shared heavy lock, after the disk gate (21 GiB).
# Read-only on barrow_full/godot (scripts run from fid/ph/harness/godot or v1's own tools; frames go to fid/ph/renders).
#   run_godot_queue.sh [capture|life|perf|all]
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders
what=${1:-all}
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
if [[ $what == capture || $what == all ]]; then
  run $R/v159 --path . --resolution 640x360 --script $H/ph_capture.gd -- res://scenes/barrow_v2_sw.tscn $R/v159
  run $R/v1 --path . --resolution 640x360 --script tools/capture_painted.gd -- --out $R/v1 --guide --variants as_painted --quiet
fi
if [[ $what == life || $what == all ]]; then
  run $R/life_v1 --path . --resolution 1920x1080 --script $H/ph_life.gd -- life res://scenes/barrow_painted.tscn $R/life_v1 uv:-9,4
  run $R/life_v1_nowind --path . --resolution 1920x1080 --script $H/ph_life.gd -- life res://scenes/barrow_painted.tscn $R/life_v1_nowind uv:-9,4 --no-wind
  run $R/life_v159 --path . --resolution 1920x1080 --script $H/ph_life.gd -- life res://scenes/barrow_v2_sw.tscn $R/life_v159 xz:-27,31
fi
if [[ $what == perf || $what == all ]]; then
  run $R/perf_v1 --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf res://scenes/barrow_painted.tscn $R/perf_v1 uv:0,1
  run $R/perf_v1_burn --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf res://scenes/barrow_painted.tscn $R/perf_v1_burn uv:0,1 --burn-ms 20
  run $R/perf_v159 --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf res://scenes/barrow_v2_sw.tscn $R/perf_v159 xz:-24.4,26.4
fi
