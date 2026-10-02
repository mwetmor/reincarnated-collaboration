#!/bin/zsh
# EN-E2: re-render one acolyte's two films (after a VFX re-bake), no stills.
cd "$(dirname "$0")/.."; g=$1
GS_VFX=$PWD/vfx/en_${g}_cold_frames.json E1_BODY=en_${g}_body.glb E1_FILMCFG=film_$g.json bash scripts/e20_godot.sh film export/final_$g film/en_${g}_playscale.mp4 1
GS_VFX=$PWD/vfx/en_${g}_cold_frames.json E1_BODY=en_${g}_body.glb E1_FILMCFG=film_$g.json bash scripts/e20_godot.sh film export/final_$g film/en_${g}_2x.mp4 2
