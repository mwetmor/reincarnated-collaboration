#!/bin/zsh
# so_mx R-C9-134: Godot stills (4 headings, 1x/2x) and the play-speed film of the battle mage + orb staff + shield, heavy_lock + to.py.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; C9=${R:h}
F=$C9/gear_sets/sorceress_battlemage/film_rt; Gd=/Applications/Godot.app/Contents/MacOS/Godot
HL=(python3 $C9/../C-7/conductor_scripts/heavy_lock.py C-9 -- python3 $C9/gear_sets/scripts/to.py)
filt() { grep -E "\[gs\] (stack|film)|heavy_lock: acq|ERROR|TIMEOUT|SCRIPT" }
TAG=${1:-ss134}; WHAT=${2:-all}
echo "{\"ev\":\"start\",\"step\":\"S134-renders-$TAG-$WHAT\",\"t\":$(date +%s)}" >> $R/work/timing.jsonl
if [[ $WHAT == all || $WHAT == stills ]]; then mkdir -p $R/look/$TAG
GS_PKG=$R/work GS_CHAR=character_sorceress_ss134.json GS_EXP=$R/export/$TAG GS_BODY=$R/export/$TAG/so-body_ss134.glb GS_OUT=$R/look/$TAG GS_CFG=$R/work/stills_ss134.json $HL 2400 $Gd --path $F 2>&1 | filt; fi
if [[ $WHAT == all || $WHAT == film ]]; then
GS_PKG=$R/work GS_CHAR=character_sorceress_ss134.json GS_EXP=$R/export/$TAG GS_BODY=$R/export/$TAG/so-body_ss134.glb GS_FILM=$R/film/${TAG}_film_1x.mp4 GS_FILM_SCALE=1 GS_OUT=$R/film GS_CFG=$R/work/film_ss134.json $HL 1800 $Gd --path $F 2>&1 | filt; fi
echo "{\"ev\":\"end\",\"step\":\"S134-renders-$TAG-$WHAT\",\"t\":$(date +%s)}" >> $R/work/timing.jsonl
echo ALL_DONE
