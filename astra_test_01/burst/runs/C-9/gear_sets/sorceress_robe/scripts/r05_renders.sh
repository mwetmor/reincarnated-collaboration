#!/bin/zsh
# R-C9-119 final renders + R-C9-120 robe/gown before/after renders, every Godot run under heavy_lock + to.py.
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
S=$C9/gear_sets/sorceress_battlemage; R=$C9/gear_sets/sorceress_robe
Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
F=$S/film_rt
filt() { grep -E "\[gs\] (stack|film)|heavy_lock: acq|ERROR|TIMEOUT|SCRIPT" }
ts() { echo "{\"ts\":\"$(date -u +%FT%TZ)\",\"step\":\"$1\"}" >> $R/timing.jsonl }
mkdir -p $S/stills/r119f_bmc $S/stills/r119f_bmd $S/film/r119f $R/stills/{before,after,gown_before,gown_after} $R/film
ts R120-renders_start
for v in bmd bmc; do echo "== R119 stills $v"
  GS_PKG=$S/scene_pkg GS_EXP=$S/export_${v}119 GS_BODY=$S/body119/so-body_bm119.glb GS_CHAR=character_sorceress_${v}119_full.json GS_OUT=$S/stills/r119f_$v GS_CFG=$F/stills_r119.json $HL 2700 $Gd --path $F 2>&1 | filt; done
echo "== R119 film 1x"
GS_PKG=$S/scene_pkg GS_EXP=$S/export_bmd119 GS_BODY=$S/body119/so-body_bm119.glb GS_CHAR=character_sorceress_bmd119.json GS_FILM=$S/film/r119f/battlemage_bmd119_film_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$S/film GS_CFG=$F/film_r119.json $HL 1800 $Gd --path $F 2>&1 | filt
for w in before:$C9/so_d7/export after:$R/export_r120; do echo "== R120 robe stills ${w%%:*}"
  GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=${w#*:} GS_OUT=$R/stills/${w%%:*} GS_CFG=$R/film_rt_cfg/stills_r120.json $HL 1800 $Gd --path $F 2>&1 | filt; done
for w in before:$C9/so_d7/export after:$R/export_r120; do echo "== R120 robe film ${w%%:*}"
  GS_PKG=$R/work/pkg GS_CHAR=character_sorceress_r120.json GS_EXP=${w#*:} GS_FILM=$R/film/robe_${w%%:*}_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/film_rt_cfg/film_r120.json $HL 1800 $Gd --path $F 2>&1 | filt; done
for w in gown_before:$S/export_bmd119 gown_after:$S/export_bmd120; do echo "== R120 gown stills ${w%%:*}"
  GS_PKG=$S/scene_pkg GS_EXP=${w#*:} GS_BODY=$S/body119/so-body_bm119.glb GS_CHAR=character_sorceress_bmd119_full.json GS_OUT=$R/stills/${w%%:*} GS_CFG=$R/film_rt_cfg/stills_r120.json $HL 1800 $Gd --path $F 2>&1 | filt; done
ts R120-renders_done
echo ALL_DONE
