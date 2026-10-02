#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n16_rig_plant.py -- builds/bloom_prep.glb work/cfg_bloom.json builds/bloom_rig_v5.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n05_render.py -- builds/bloom_rig_v5.glb strip work/strip_bloom_v5.png 'SW|idle:0,idle:60,attack_bite:8,attack_bite:12,attack_bite:13,cast_spit:19,hit:3,death:30,death:62,spawn:0,spawn:20,spawn:45' 2>&1 | grep -i 'error\|sheet'
