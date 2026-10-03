#!/bin/zsh
# EN-E3 Godot verification of a shipped GLB: n13_godot_chk.sh <abs glb> <abs out prefix> "<clip:time,...>"
# The check project lives in en_e3/godot_chk (nothing is written into reincarnated-godot or cliffside3d).
D=$(cd "$(dirname "$0")/.." && pwd)
export EN3_GLB=$1 EN3_OUT=$2 EN3_SHOTS=$3
perl -e 'alarm shift; exec @ARGV' 300 /Applications/Godot.app/Contents/MacOS/Godot --path $D/godot_chk 2>&1 | grep -E "\[chk\]|ERROR|SCRIPT ERROR" | head -40
