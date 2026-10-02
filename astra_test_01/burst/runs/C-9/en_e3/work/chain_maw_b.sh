#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/maw_tripo.glb builds/maw_prep.glb 2.64 --flip 2>&1 | grep '^{'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/maw_prep.glb work/canvas_maw_A.png --layout packed --canvas 1536x1024 --elev 19.77 --name maw_A --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
python3 scripts/02_compose.py maw_A work/canvas_maw_A.png | tail -1
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/maw_prep.glb work/cfg_maw.json builds/maw_rig_v8.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n05_render.py -- builds/maw_rig_v8.glb strip work/strip_maw_v8.png 'W|idle:0,walk:4,walk:9,run:3,attack_bite:6,attack_bite:11,cast_spit:37,hit:3,death:10,death:26,attack_bite_b:12,cast_spit:44' --side 2>&1 | grep -i 'error\|sheet'
