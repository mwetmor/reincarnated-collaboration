#!/bin/zsh
# R-C9-138/140 stills: BEFORE (ss134f, its package) and AFTER (ss138a, hood on and off) at the play camera, 8 headings,
# through the gear_stills harness (gear_sets/sorceress_battlemage/film_rt), heavy lock + to.py. Then the sheets (r138_05).
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; C9=${R:h}
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT: under 20 GiB"; exit 9; }
WHAT=${1:-both}
if [[ $WHAT == both || $WHAT == before ]]; then mkdir -p $R/look/r138_before
GS_PKG=$R/work GS_CHAR=character_sorceress_ss134.json GS_EXP=$R/export/ss134f GS_BODY=$R/export/ss134f/so-body_ss134.glb GS_OUT=$R/look/r138_before GS_CFG=$R/work/stills_r138.json $HL 2400 $Gd --path $F 2>&1 | grep -E "\[gs\] stack|heavy_lock|ERROR|TIMEOUT|SCRIPT"; fi
if [[ $WHAT == both || $WHAT == after ]]; then mkdir -p $R/look/r138_after
GS_PKG=$R/work GS_CHAR=character_sorceress_ss138.json GS_EXP=$R/export/ss138a GS_BODY=$R/export/ss138a/so-body_ss138.glb GS_OUT=$R/look/r138_after GS_CFG=$R/work/stills_r138_after.json $HL 2400 $Gd --path $F 2>&1 | grep -E "\[gs\] stack|heavy_lock|ERROR|TIMEOUT|SCRIPT"; fi
echo STILLS_DONE
