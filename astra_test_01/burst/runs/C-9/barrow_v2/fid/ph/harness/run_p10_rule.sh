#!/bin/zsh
# BV2F lane PH: P10 under the pre-registered repeat rule (calibration.md s34): 3 fresh runs per view, worst p99 binds.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/${PH_RDIR:?set PH_RDIR}/p10_rule
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
for i in 1 2 3; do run $R/start_$i --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/start_$i uv:0,0; done
for i in 1 2 3; do run $R/sea_$i --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/sea_$i uv:-29,-5.5; done
run $R/burn --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/burn uv:0,0 --burn-ms 20
