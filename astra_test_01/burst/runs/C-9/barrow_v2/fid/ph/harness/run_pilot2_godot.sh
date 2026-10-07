#!/bin/zsh
# BV2F lane PH: Godot runs on PT's REBUILT pilot (R-C9-194 hand-back 0b72461db): P9 life (heather view + sea/floe view,
# --no-wind and --floe-red REDs), P10 perf (start + sea view, 20 ms burn RED). Heavy lock + 21 GiB gate.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/pilot2
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
run $R/life_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_sea uv:-29,-5.5
run $R/life_sea_floered --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_sea_floered uv:-29,-5.5 --floe-red
run $R/life --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life uv:-3,11.7
run $R/life_nowind --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_nowind uv:-3,11.7 --no-wind
run $R/perf_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf_sea uv:-29,-5.5
run $R/perf --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf uv:0,0
run $R/perf_burn --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/perf_burn uv:0,0 --burn-ms 20
