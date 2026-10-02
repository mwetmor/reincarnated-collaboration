#!/bin/zsh
# so_mx (R-C9-131): prop penetration checks (Blender, so07) for both sets, under one heavy-lock hold (the caller wraps it).
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R
B=/Applications/Blender.app/Contents/MacOS/Blender; TO="python3 ../gear_sets/scripts/to.py"
echo "{\"ev\":\"start\",\"step\":\"S6-prop-checks\",\"t\":$(date +%s)}" >> work/timing.jsonl
${=TO} 1800 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/bm131/so-body_bm131.glb export/bm131 work/props_bm131.json --clips idle,walk,run,cast_fireball_m,cast_meteor,hit,death --who 2>&1 | grep -E "^CHK|^WHO|Error|TIMEOUT" | cut -c1-300
${=TO} 1800 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/st131/so-body.glb export/st131 work/props_st131.json --colliders robe,mantle,belt --props staff --clips idle,walk,run,cast_fireball,cast_meteor,hit,death --who 2>&1 | grep -E "^CHK|^WHO|Error|TIMEOUT" | cut -c1-300
echo "{\"ev\":\"end\",\"step\":\"S6-prop-checks\",\"t\":$(date +%s)}" >> work/timing.jsonl
echo CHECKS_DONE
