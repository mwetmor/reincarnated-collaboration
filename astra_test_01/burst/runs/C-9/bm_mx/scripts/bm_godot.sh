#!/bin/bash
# bm_mx Godot render (film_rt = a copy of wl_e1's harness):
#   bm_godot.sh stills <expdir> <outdir> <cfg.json>   |   bm_godot.sh film <expdir> <out.mp4> <scale> <cfg.json>
# Every run goes through the shared heavy lock. Env passes through (BM_CHAR, GS_BIND_BY_NAME, GS_FILM_STACK).
cd "$(dirname "$0")/.."; R=$PWD
MODE=$1; EXP=$(cd "$2" && pwd)
export GS_PKG=$R/work GS_CHAR=${BM_CHAR:-character_bm.json} GS_EXP=$EXP GS_BODY=$EXP/bm_body.glb
if [ "$MODE" = stills ]; then mkdir -p "$3"; export GS_OUT=$(cd "$3" && pwd) GS_CFG=$R/$4
else export GS_CFG=$R/$5 GS_FILM=$R/$3 GS_FILM_SCALE=$4; fi
python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 -- perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $R/film_rt 2>&1 | grep -E "\[gs\]|ERROR|SCRIPT|heavy_lock" | head -30
