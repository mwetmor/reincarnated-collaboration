#!/bin/zsh
# EN-E2 Godot verification + deliverables for one acolyte (runtime GLTFDocument load of the SHIPPED body, the wl_e1 harness):
# 8-heading stills (idle / walk / cast_bolt at release / death at its end), then the play-scale and 2x films with the baked VFX.
#   zsh scripts/en12_godot_all.sh <m|f>
cd "$(dirname "$0")/.."; g=$1; V=${2:-en_${g}_cold}; [ -f work/character_en_$g.json ] && export E1_CHAR=character_en_$g.json
mkdir -p views/stills_$g film
E1_BODY=en_${g}_body.glb E1_STILLS=stills_$g.json bash scripts/e20_godot.sh stills export/final_$g views/stills_$g
GS_VFX=$PWD/vfx/${V}_frames.json E1_BODY=en_${g}_body.glb E1_FILMCFG=film_$g.json bash scripts/e20_godot.sh film export/final_$g film/en_${g}_playscale.mp4 1
GS_VFX=$PWD/vfx/${V}_frames.json E1_BODY=en_${g}_body.glb E1_FILMCFG=film_$g.json bash scripts/e20_godot.sh film export/final_$g film/en_${g}_2x.mp4 2
