#!/bin/zsh
# C-6 P5 headless proof (run under heavy_lock.py): import → movement probe (8 walks + jump) → east-cast probe. usage: run_p5_proof.sh <project> <out>
G=/Applications/Godot.app/Contents/MacOS/Godot; P=$1; O=$2; mkdir -p $O
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
cp $B/runs/C-6/conductor_scripts/probe_move_c6.gd $P/probe_move_c6.gd; cp $B/runs/C-5/conductor_scripts/probe_events.gd $P/probe_events.gd
$G --headless --path $P --import > $O/import.log 2>&1; echo "import exit $?  errors: $(grep -c 'ERROR\|SCRIPT ERROR' $O/import.log)" | tee $O/summary.txt
WALKABLE=$B/runs/C-5/artifacts/CS-parallax-in-v10/walkable.json $G --headless --path $P --script res://probe_move_c6.gd > $O/move.log 2>&1; echo "move exit $?" | tee -a $O/summary.txt; grep "^DIR\|^JUMP" $O/move.log | tee -a $O/summary.txt
KIT_CYCLES=9 FACE=move_right $G --headless --path $P --script res://probe_events.gd > $O/events.log 2>&1; echo "events exit $?" | tee -a $O/summary.txt; grep -i "contact\|hit\|target\|dummy" $O/events.log | head -12 | tee -a $O/summary.txt
echo "PROOF DONE" >> $O/summary.txt
