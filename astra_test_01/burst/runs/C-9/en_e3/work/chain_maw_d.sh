#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/maw_prep.glb work/cfg_maw.json export/maw/maw.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb look work/look_maw_texAT.png 2>&1 | grep -i 'error\|sheet'
zsh scripts/n13_godot_chk.sh $PWD/export/maw/maw.glb $PWD/work/godot_maw "idle:0.0,walk:0.2,attack_bite:0.3667,cast_spit:1.2333,death:0.8667"
