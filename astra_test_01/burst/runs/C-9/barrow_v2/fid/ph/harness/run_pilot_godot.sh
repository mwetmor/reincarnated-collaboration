#!/bin/zsh
# BV2F lane PH: the Godot runs of the Phase 2' pilot harness (P9 life pairs + RED, P10 perf), heavy lock + 21 GiB gate.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/pilot
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
run $R/life --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life uv:-3,11.7
run $R/life_nowind --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_nowind uv:-3,11.7 --no-wind
run $R/perf --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf uv:0,0
run $R/perf_burn --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf_burn uv:0,0 --burn-ms 20
