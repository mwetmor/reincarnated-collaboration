#!/bin/zsh
# EN-E4 resume: gloamwing max-fit re-prep (5.6 x 0.68 = 3.808 m), rig v2 (leg gate 0.52, motion_scale 0.68), fit check, strips, paint canvas
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/gloamwing_tripo.glb builds/gloamwing_prep.glb 3.808 --flip --minisland 0.0003 --faces 45000 2>&1 | grep '^{' | cut -c1-400
blender -b -noaudio --python scripts/e11_rig_wingquad.py -- builds/gloamwing_prep.glb work/cfg_gloamwing.json builds/gloamwing_rig_v2.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line ' | cut -c1-400
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/gloamwing_rig_v2.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_rig_v2.glb strip work/strip_gloamwing_v2.png 'SW|idle:0,walk:7,walk:21,run:6,attack_claw:12,attack_peck:8,attack_peck:13,cast_breath:26,cast_breath:50,cast_roar:12,emerge:5,emerge:28,hit:3,death:30' 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/gloamwing_prep.glb work/canvas_gloamwing_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name gloamwing_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
python3 scripts/02_compose.py gloamwing_G work/canvas_gloamwing_G.png | tail -1
