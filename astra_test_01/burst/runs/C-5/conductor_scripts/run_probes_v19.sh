#!/bin/zsh
# usage: run_probes_v19.sh <godot_project_dir> <out_dir>
G=/Applications/Godot.app/Contents/MacOS/Godot; P=$1; O=$2; mkdir -p $O/stills $O/walk
cp /private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/3f302aea-abba-4d7f-aaef-b6efd7c3cfa9/scratchpad/probe_clearing.gd $P/probe_clearing.gd
cp /private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/3f302aea-abba-4d7f-aaef-b6efd7c3cfa9/scratchpad/probe_walk_clearing.gd $P/probe_walk_clearing.gd
$G --headless --path $P --import > $O/import.log 2>&1; echo "import exit $?"; grep -c 'ERROR\|SCRIPT ERROR' $O/import.log
PROBE_OUT=$O/stills $G --rendering-method gl_compatibility --path $P --script res://probe_clearing.gd > $O/stills.log 2>&1; echo "stills exit $? ($(ls $O/stills | wc -l) files)"
PROBE_OUT=$O/walk $G --rendering-method gl_compatibility --path $P --script res://probe_walk_clearing.gd > $O/walk.log 2>&1; echo "walk exit $? ($(ls $O/walk | wc -l) frames)"
/opt/homebrew/bin/ffmpeg -y -loglevel error -framerate 20 -i $O/walk/walk_%04d.png -vf "scale=1280:-2" -pix_fmt yuv420p $O/walk_clearing.mp4 && echo "mp4 ok"
