#!/bin/zsh
# R-C9-120 probe: re-skin variants -> Godot id stills (heavy_lock) -> visible body pixels. r09_probe.sh <tag> <r02 args...>
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9; R=$C9/gear_sets/sorceress_robe
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
tag=$1; shift
python3 $R/scripts/r02_reskin.py $C9/so_d7/export/robe.glb $C9/so_d7/export/so-body.glb $R/export/robe_$tag.glb "$@" >/dev/null || exit 1
mkdir -p $R/probe/exp_$tag $R/probe/stills_$tag
for f in $C9/so_d7/export/*; do [ $(basename $f) = robe.glb ] || ln -sf $f $R/probe/exp_$tag/; done
ln -sf $R/export/robe_$tag.glb $R/probe/exp_$tag/robe.glb
GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=$R/probe/exp_$tag GS_OUT=$R/probe/stills_$tag GS_CFG=$R/film_rt_cfg/stills_r120_probe.json \
  python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py 900 $Gd --path $F 2>&1 | grep -E "ERROR|TIMEOUT" 
python3 $R/scripts/r03_measure.py $R/export/robe_$tag.glb $C9/so_d7/export/so-body.glb $R/work/measure_robe_$tag.json --clips walk,run | grep MEAS | sed -E "s/'jerk_max_at': \{[^}]*\},//;s/'frames_with[^,]*,//" | cut -c1-200
python3 $R/scripts/r08_idcount.py $R/probe/stills_$tag | sed -E "s#^.*TOTAL#TOTAL#"
