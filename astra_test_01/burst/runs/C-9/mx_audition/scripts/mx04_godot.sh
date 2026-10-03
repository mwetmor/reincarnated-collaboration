#!/bin/bash
# MX audition (R-C9-149): Godot stills / film of an AUDITION GLB (work/aud_<tag>.glb) in mx_audition/film_rt (a copy of en_e2's
# harness: play camera ortho, pitch 52.9535 deg, yaw 47 deg, 100.617 px/m x scale). Each call is ONE short heavy-lock job.
#   bash scripts/mx04_godot.sh stills <tag> <cfg.json>            -> stills/<tag>/   (beauty only)
#   bash scripts/mx04_godot.sh film   <tag> <cfg.json> <out.mp4>  -> 1x play scale, 960x540
cd "$(dirname "$0")/.."; R=$PWD; MODE=$1; TAG=$2
export GS_PKG=$R/work GS_CHAR=character_en.json GS_EXP=$R/work GS_BODY=$R/work/aud_${GLB_TAG:-$TAG}.glb GS_CFG=$R/$3 GS_BEAUTY_ONLY=1
if [ "$MODE" = stills ]; then mkdir -p stills/$TAG; export GS_OUT=$R/stills/$TAG
else export GS_FILM=$R/$4 GS_FILM_SCALE=1; fi
HL="python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 --"; [ -n "$MX_NOLOCK" ] && HL=""   # MX_NOLOCK: the caller (mx07_batch.sh) already holds the lock
$HL perl -e 'alarm shift; exec @ARGV' 1500 /Applications/Godot.app/Contents/MacOS/Godot --path $R/film_rt 2>&1 | grep -E "\[gs\]|ERROR|SCRIPT|heavy_lock" | head -20
