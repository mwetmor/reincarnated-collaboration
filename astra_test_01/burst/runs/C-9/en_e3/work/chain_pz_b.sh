#!/bin/zsh
# EN-E3 R-C9-135: the D7 paint canvas (sheet A at the game pitch) for the parasite mesh shared by the larva (0.9 m) and the worm (2.8 m)
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
H=../../C-7/conductor_scripts/heavy_lock.py
python3 $H C-9 -- blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/worm_prep.glb work/canvas_parasite_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name parasite_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
python3 scripts/02_compose.py parasite_G work/canvas_parasite_G.png | tail -1
