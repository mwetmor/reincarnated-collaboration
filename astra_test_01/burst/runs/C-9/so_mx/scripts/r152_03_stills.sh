#!/bin/zsh
# R-C9-152 stills: the live kit (ss138a, hood_hair morph) and the fix (ss152a, hood cap), hood on and off, 8 headings,
# idle / walk / Fire Ball, play scale 1 and 3x, through the gear_stills harness with GS_CULL_BACK=1 (the Barrow's culling). Heavy lock.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; C9=${R:h}
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 21 ] || { echo "HALT: under 21 GiB"; exit 9; }
if [[ ${1:-} != b ]]; then mkdir -p $R/look/r152_live_cb $R/look/r152_fix_cb
python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- zsh -c "
GS_CULL_BACK=1 GS_PKG=$R/work GS_CHAR=character_sorceress_ss138.json GS_EXP=$R/export/ss138a GS_BODY=$R/export/ss138a/so-body_ss138.glb GS_OUT=$R/look/r152_live_cb GS_CFG=$R/work/stills_r152.json $Gd --path $F 2>&1 | grep -E '\[gs\] (stack|cull)|ERROR|SCRIPT'
GS_CULL_BACK=1 GS_PKG=$R/work GS_CHAR=character_sorceress_ss152.json GS_EXP=$R/export/ss152a GS_BODY=$R/export/ss152a/so-body_ss152.glb GS_OUT=$R/look/r152_fix_cb GS_CFG=$R/work/stills_r152.json $Gd --path $F 2>&1 | grep -E '\[gs\] (stack|cull)|ERROR|SCRIPT'"
echo STILLS_DONE; fi
# option B (ss152b: cap above 1.30 m + the hood_braid morph): zsh r152_03_stills.sh b
if [[ ${1:-} == b ]]; then mkdir -p $R/look/r152_fixb_cb
python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- env GS_CULL_BACK=1 GS_PKG=$R/work GS_CHAR=character_sorceress_ss152b.json GS_EXP=$R/export/ss152b GS_BODY=$R/export/ss152b/so-body_ss152.glb GS_OUT=$R/look/r152_fixb_cb GS_CFG=$R/work/stills_r152.json $Gd --path $F 2>&1 | grep -E '\[gs\] (stack|cull)|ERROR|SCRIPT'; echo STILLS_B_DONE; fi
