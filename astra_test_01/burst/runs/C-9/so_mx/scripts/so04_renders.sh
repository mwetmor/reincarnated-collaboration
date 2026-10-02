#!/bin/zsh
# so_mx (R-C9-131): Godot stills (8 headings, 1x/2x) + play-speed films for both sets, through heavy_lock + to.py.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; C9=${R:h}
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
filt() { grep -E "\[gs\] (stack|film)|heavy_lock: acq|ERROR|TIMEOUT|SCRIPT" }
ts() { echo "{\"ev\":\"$1\",\"step\":\"$2\",\"t\":$(date +%s)}" >> $R/work/timing.jsonl }
WHAT=${1:-all}
ts start S5-renders-$WHAT
if [[ $WHAT == all || $WHAT == stills ]]; then
mkdir -p $R/look/bm131 $R/look/st131
GS_PKG=$R/work GS_CHAR=character_sorceress_bm131_full.json GS_EXP=$R/export/bm131 GS_BODY=$R/export/bm131/so-body_bm131.glb GS_OUT=$R/look/bm131 GS_CFG=$R/work/stills_bm131.json $HL 2400 $Gd --path $F 2>&1 | filt
GS_PKG=$R/work GS_CHAR=character_sorceress_st131.json GS_EXP=$R/export/st131 GS_OUT=$R/look/st131 GS_CFG=$R/work/stills_st131.json $HL 2400 $Gd --path $F 2>&1 | filt
fi
if [[ $WHAT == all || $WHAT == films ]]; then
GS_PKG=$R/work GS_CHAR=character_sorceress_bm131.json GS_EXP=$R/export/bm131 GS_BODY=$R/export/bm131/so-body_bm131.glb GS_FILM=$R/film/bm131_film_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/work/film_bm131.json $HL 1800 $Gd --path $F 2>&1 | filt
GS_PKG=$R/work GS_CHAR=character_sorceress_st131.json GS_EXP=$R/export/st131 GS_FILM=$R/film/st131_film_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/work/film_st131.json $HL 1800 $Gd --path $F 2>&1 | filt
fi
ts end S5-renders-$WHAT
echo ALL_DONE
