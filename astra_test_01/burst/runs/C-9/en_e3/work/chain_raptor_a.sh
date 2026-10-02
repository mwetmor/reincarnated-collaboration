#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n15_rig_raptor.py -- builds/raptor_prep.glb work/cfg_raptor.json builds/raptor_rig_v7.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n05_render.py -- builds/raptor_rig_v7.glb strip work/strip_raptor_v7.png 'W|idle:0,walk:7,walk:22,run:4,attack_swipe:8,attack_swipe:14,attack_kick:18,attack_kick:22,attack_leap:13,attack_leap:19,hit:3,death:56' --side 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- builds/raptor_rig_v7.glb strip work/strip_raptor_legs7.png 'W|walk:3,walk:13,run:4,attack_kick:22,attack_swipe:8,attack_leap:13' --side --legs 2>&1 | grep -i 'error\|sheet'
