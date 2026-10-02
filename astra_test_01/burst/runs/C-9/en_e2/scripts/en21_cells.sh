#!/bin/zsh
# EN-E2: render one acolyte's JOIN-1 cell pack with the shared renderer (join1_render, unchanged) -> join1_pack/en-acolyte-<g>.
#   zsh scripts/en21_cells.sh <m|f>     (run under heavy_lock)
cd "$(dirname "$0")/.."; g=$1; C9=$(cd .. && pwd); K=en-acolyte-$g
mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -12
