#!/bin/zsh
# R-C9-120: v7 + A (leggings body) and v7C (back shin share) -- id/beauty stills (probe config) and play-speed films, under heavy_lock.
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9; R=$C9/gear_sets/sorceress_robe
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
ts() { echo "{\"ts\":\"$(date -u +%FT%TZ)\",\"step\":\"$1\"}" >> $R/timing.jsonl }
ts R120-AC_renders_start
mkdir -p $R/stills/v7A $R/stills/v7C
GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=$R/export_r120v7 GS_BODY=$R/export/so-body_leggings.glb GS_OUT=$R/stills/v7A GS_CFG=$R/film_rt_cfg/stills_r120_probe.json $HL 900 $Gd --path $F 2>&1 | grep -E "ERROR|TIMEOUT|heavy_lock: acq"
GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=$R/export_r120v7C GS_OUT=$R/stills/v7C GS_CFG=$R/film_rt_cfg/stills_r120_probe.json $HL 900 $Gd --path $F 2>&1 | grep -E "ERROR|TIMEOUT|heavy_lock: acq"
GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=$R/export_r120v7 GS_BODY=$R/export/so-body_leggings.glb GS_FILM=$R/film/robe_v7A_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/film_rt_cfg/film_r120.json $HL 1800 $Gd --path $F 2>&1 | grep -E "ERROR|TIMEOUT|\[gs\] film"
GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=$R/export_r120v7C GS_FILM=$R/film/robe_v7C_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/film_rt_cfg/film_r120.json $HL 1800 $Gd --path $F 2>&1 | grep -E "ERROR|TIMEOUT|\[gs\] film"
ts R120-AC_renders_done
echo ALL_DONE
