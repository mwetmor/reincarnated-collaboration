#!/bin/bash
LAB=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/attack_lab
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/drax-atk/fade
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
mkdir -p $S; cd $LAB
L15="attack:0.1667,attack_chop:0.1667,shield_bash:0.1667"
v() { local name=$1; shift
  env LAB_LABEL=$name LAB_OUT=$S/$name.json LAB_WATCHDOG_S=900 "$@" python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot \
    --path godot --resolution 640x360 --script tools/lab_fade.gd > $S/$name.log 2>&1
  grep -aE "^\[fade\]|LAB:|SCRIPT ERROR|WATCHDOG" $S/$name.log; }
v V0_shipped
v V1_damped+lead LAB_DAMP_IDLE=0.10 LAB_LEADIN=$L15 LAB_IDLE_T=3.062
v V2_breathe LAB_BREATHE=1
v V3_breathe+lead LAB_BREATHE=1 LAB_LEADIN=$L15 LAB_IDLE_T=4.238
v V4_breathe+sized LAB_BREATHE=1 LAB_LEADIN=attack:0.22,attack_chop:0.1667,shield_bash:0.44 LAB_IDLE_T=4.238
