#!/bin/zsh
# R-C9-140: the face opening close up (scale 6), hood on/off after (ss138a) and the hood before (ss134f), heavy lock.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; C9=${R:h}
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT: under 20 GiB"; exit 9; }
mkdir -p $R/look/r140_face_before $R/look/r140_face_after
$HL 1800 zsh -c "
GS_PKG=$R/work GS_CHAR=character_sorceress_ss134.json GS_EXP=$R/export/ss134f GS_BODY=$R/export/ss134f/so-body_ss134.glb GS_OUT=$R/look/r140_face_before GS_CFG=$R/work/stills_r140_face.json $Gd --path $F 2>&1 | grep -E '\[gs\] stack|ERROR|SCRIPT'
GS_PKG=$R/work GS_CHAR=character_sorceress_ss138.json GS_EXP=$R/export/ss138a GS_BODY=$R/export/ss138a/so-body_ss138.glb GS_OUT=$R/look/r140_face_after GS_CFG=$R/work/stills_r140_face.json $Gd --path $F 2>&1 | grep -E '\[gs\] stack|ERROR|SCRIPT'"
echo FACE_DONE
