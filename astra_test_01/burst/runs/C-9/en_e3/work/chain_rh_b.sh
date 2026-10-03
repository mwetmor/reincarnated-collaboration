#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n04_prep.py -- builds/rifthorror_tripo.glb builds/rifthorror_prep20.glb 2.0 --height --yaw -90 --minisland 0.0003 --faces 45000 2>&1 | grep '^{' | cut -c1-200
blender -b -noaudio --python scripts/n24_rig_horror.py -- builds/rifthorror_prep20.glb work/cfg_rifthorror.json builds/rifthorror_rig_v2.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rifthorror_rig_v2.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/rifthorror_prep20.glb work/canvas_rifthorror_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name rifthorror_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
"
python3 scripts/02_compose.py rifthorror_G work/canvas_rifthorror_G.png | tail -1
echo CHAIN_RH_B_DONE
