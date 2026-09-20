#!/bin/zsh
# usage: run_capture.sh <project> <out> <name>   (run under heavy_lock.py)
G=/Applications/Godot.app/Contents/MacOS/Godot; P=$1; O=$2; N=$3; mkdir -p $O/frames
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
cp $B/runs/C-6/conductor_scripts/probe_walk_c6.gd $P/probe_walk_c6.gd
$G --headless --path $P --import > $O/import.log 2>&1; echo "import exit $?  errors: $(grep -c 'ERROR\|SCRIPT ERROR' $O/import.log)" | tee $O/capture_summary.txt
PROBE_OUT=$O/frames $G --rendering-method gl_compatibility --path $P --script res://probe_walk_c6.gd > $O/walk.log 2>&1; echo "walk exit $? ($(ls $O/frames | wc -l) frames)" | tee -a $O/capture_summary.txt; tail -1 $O/walk.log | tee -a $O/capture_summary.txt
/opt/homebrew/bin/ffmpeg -y -loglevel error -framerate 30 -i $O/frames/walk_%04d.png -vf "scale=1280:-2" -pix_fmt yuv420p $O/$N.mp4 && echo "mp4 ok $O/$N.mp4" | tee -a $O/capture_summary.txt
echo "CAPTURE DONE" >> $O/capture_summary.txt
