#!/bin/zsh
# BV2F lane PH, pilot 3 (PT 72a9a0ec5; scene default BV2F_PILOT=rp4): P3 sea base-only capture, P9 life (sway + no-wind RED;
# sea view with the geometry mask), P10 under the s34 rule. Heavy lock per step; 21 GiB gate per step.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/pilot_ps4
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art BV2F_PILOT=rp4
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
run() { local out=$1; shift; mkdir -p $out; gate; (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G "$@" > $out/log.txt 2>&1); echo "$out rc=$?"; }
run $R/p3_sea --path . --resolution 640x360 --script $H/ph_p3_sea.gd -- --out $R/p3_sea
run $R/life --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life uv:-3,11.7
run $R/life_nowind --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_nowind uv:-3,11.7 --no-wind
run $R/life_sea --path . --resolution 1920x1080 --script $H/ph_life.gd -- life $S $R/life_sea uv:-29,-5.5
