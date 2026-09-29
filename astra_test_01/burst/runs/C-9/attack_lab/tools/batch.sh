#!/bin/bash
# attack_lab batch: every action x start state, before and after the recentre, + unarmed baseline
LAB=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/attack_lab
OUT=$1
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
cd $LAB
run() { # mode action from stack
  local E=""; [ "$1" = after ] && E="LAB_RECENTRE=1"
  env $E python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot --path godot --resolution 640x360 \
    --script tools/lab.gd -- --action=$2 --from=$3 --rung=R6 --stack=$4 --out=$OUT/$1_s$4 > $OUT/log_$1_$2_$3_s$4.txt 2>&1
}
for mode in before after; do for act in slash chop bash block; do for from in idle run; do run $mode $act $from 4; done; done; done
run before slash idle 0
run before slash run 0
