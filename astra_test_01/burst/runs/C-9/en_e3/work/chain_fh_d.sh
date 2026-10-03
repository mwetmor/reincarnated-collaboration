#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
H=../../C-7/conductor_scripts/heavy_lock.py
df -h /System/Volumes/Data | tail -1
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n04_prep.py -- builds/frosthorn_tripo.glb builds/frosthorn_prep31.glb 3.1 --minisland 0.0003 --faces 50000 2>&1 | grep '^{' | cut -c1-200
blender -b -noaudio --python scripts/n04b_cull_box.py -- builds/frosthorn_prep31.glb builds/frosthorn_prep31_c.glb -0.3875 0.3875 -0.2325 0.2945 -0.01 0.3255 2>&1 | grep '^{'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/frosthorn_prep31_c.glb work/canvas_frosthorn_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name frosthorn_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
"
python3 scripts/02_compose.py frosthorn_G work/canvas_frosthorn_G.png | tail -1
echo CHAIN_FH_D_DONE
