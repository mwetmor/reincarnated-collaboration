#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/maw_prep.glb work/cfg_maw.json export/maw/maw.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb strip work/strip_maw_bite.png 'SW|attack_bite:3,attack_bite:6,attack_bite:9,attack_bite:11,attack_bite:14,attack_bite:20,attack_bite_b:12,cast_spit:37,idle:10,idle:20,idle:25,hit:3' 2>&1 | grep -i 'error\|sheet'
