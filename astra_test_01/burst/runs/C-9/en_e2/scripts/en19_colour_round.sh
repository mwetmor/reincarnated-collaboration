#!/bin/zsh
# EN-E2 one colour round for one acolyte: embed <tex> into a scratch copy of the shipped body, render idle+walk at 8 headings
# (beauty + class with the region-ID texture) at the play camera, measure region Lab vs the sheet.
#   zsh scripts/en19_colour_round.sh <m|f> <tex.png> <tag>      (run under heavy_lock)
cd "$(dirname "$0")/.."; g=$1; TEX=$2; T=$3
mkdir -p work/col_$T; cp export/final_$g/en_${g}_body.glb work/col_$T/en_${g}_body.glb
python3 scripts/e42_embed_tex.py work/col_$T/en_${g}_body.glb work/col_$T/en_${g}_body.glb $TEX | cut -c1-80
echo '{"shots": [["idle", 0.5], ["walk", 0.3]], "headings": [0, 45, 90, 135, 180, 225, 270, 315], "scales": [1], "watchdog_s": 900, "settle_frames": 4}' > work/stills_colour.json
mkdir -p views/col_$T
GS_CLASS_TEX=$PWD/work/${g}_regions.png E1_BODY=en_${g}_body.glb E1_STILLS=stills_colour.json bash scripts/e20_godot.sh stills work/col_$T views/col_$T
python3 scripts/en18_colour_measure.py $g views/col_$T --json work/col_$T/colour.json
