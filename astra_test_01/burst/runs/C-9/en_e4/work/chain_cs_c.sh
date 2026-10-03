#!/bin/zsh
# EN-E4 resume: coilseer rig v3 (hand gate 0.24, walk/run amp 0.13/0.16) + the paint canvas (prep unchanged: v2 s_fit 1.079 >= 1)
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
blender -b -noaudio --python scripts/e10_rig_coil.py -- builds/coilseer_prep.glb work/cfg_coilseer.json builds/coilseer_rig_v3.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line ' | cut -c1-500
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/coilseer_rig_v3.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/coilseer_rig_v3.glb strip work/strip_coilseer_v3.png 'SW|idle:0,walk:10,walk:20,run:6,attack_claw:5,attack_claw:13,cast_bolt:25,cast_nova:18,cast_nova:30,attack_taillash:13,attack_taillash:23,hit:3,death:20,death:36' 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/coilseer_prep.glb work/canvas_coilseer_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name coilseer_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
python3 scripts/02_compose.py coilseer_G work/canvas_coilseer_G.png | tail -1
