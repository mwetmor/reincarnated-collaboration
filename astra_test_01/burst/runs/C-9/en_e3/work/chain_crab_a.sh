#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
mkdir -p export/crab
blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/crab_prep.glb work/cfg_crab.json builds/crab_rig_v5.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n05_render.py -- builds/crab_rig_v5.glb strip work/strip_crab_v5.png 'SW|idle:0,walk:6,walk:12,run:4,attack_slam:6,attack_slam:12,attack_strike:12,cast_breath:20,cast_lob:17,hit:3,death:10,death:20' 2>&1 | grep -i 'error\|sheet'
