#!/bin/zsh
# BV2F lane PH: R-C9-197 pre-registered P9c (calibration.md s31): depth-test-off marker, 5 pairs, rest-pose + RED.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/${PH_RDIR:-pilot3}
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
for v in "$@"; do
  case $v in
    p9c) run $R/p9c_rest --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_rest uv:-29,-5.5 --floe-pairs 5
         run $R/p9c_red --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/p9c_red uv:-29,-5.5 --floe-pairs 5 --floe-red ;;
    flow) run $R/life_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_sea uv:-29,-5.5 ;;
    perf) run $R/perf --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf uv:0,0
          run $R/perf_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf_sea uv:-29,-5.5 ;;
  esac
done
