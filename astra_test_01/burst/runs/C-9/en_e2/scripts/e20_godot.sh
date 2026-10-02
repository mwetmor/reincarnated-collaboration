#!/bin/bash
# EN-E2 (copy of wl_e1 e20) Godot render (wl_e1/film_rt, the barbarian/sorceress film harness): e20_godot.sh stills <expdir> <outdir> | film <expdir> <out.mp4> <scale>
cd "$(dirname "$0")/.."; R=$PWD
MODE=$1; EXP=$(cd "$2" && pwd)
export GS_PKG=$R/work GS_CHAR=${E1_CHAR:-character_en.json} GS_EXP=$EXP GS_BODY=$EXP/${E1_BODY:-body.glb}
if [ "$MODE" = stills ]; then mkdir -p "$3"; export GS_OUT=$(cd "$3" && pwd) GS_CFG=$R/work/${E1_STILLS:-stills_cfg.json}
else export GS_CFG=$R/work/${E1_FILMCFG:-film_cfg.json} GS_FILM=$R/$3 GS_FILM_SCALE=$4; fi
perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $R/film_rt 2>&1 | grep -E "\[gs\]|ERROR|SCRIPT" | head -20
