#!/bin/zsh
# BV2F lane PH, R-C9-201: (1) P10 traces (3 fresh runs, start view, trace.json per run); (2) P3 sea at rest / base / RED.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/pilot6
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
for i in 1 2 3; do run $R/trace_start_$i --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/trace_start_$i uv:0,0; done
run $R/p3_sea --path . --resolution 640x360 --script $H/ph_p3_sea.gd -- --out $R/p3_sea
