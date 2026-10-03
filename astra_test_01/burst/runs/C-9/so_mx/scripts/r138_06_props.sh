#!/bin/zsh
# R-C9-138: the orb staff against her body after the re-aim (so07, the clamp's parity inside test, every key, no carry layer),
# before (ss134f) and after (ss138a), heavy lock + to.py.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R
B=/Applications/Blender.app/Contents/MacOS/Blender; TO=(python3 ../gear_sets/scripts/to.py)
HL=(python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 --)
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 20 ] || { echo "HALT: under 20 GiB"; exit 9; }
CL=idle,walk,run,hit,block,block_idle,cast_fireball_m,cast_meteor
$HL zsh -c "
${TO[*]} 2700 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/ss134f/so-body_ss134.glb export/ss134f work/r138_props_ss134f.json --colliders '' --props orbstaff --clips $CL --step 1 --parity --no-carry --who 2>&1 | grep -E '^CHK|^WHO|Error|Traceback' | cut -c1-300
${TO[*]} 2700 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/ss138a/so-body_ss138.glb export/ss138a work/r138_props_ss138a.json --colliders '' --props orbstaff --clips $CL,idle_ss4 --step 1 --parity --no-carry --who 2>&1 | grep -E '^CHK|^WHO|Error|Traceback' | cut -c1-300
"
echo PROPS_DONE
