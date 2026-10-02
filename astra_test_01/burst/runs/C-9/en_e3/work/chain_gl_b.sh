#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/glutton_prep.glb work/canvas_glutton_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name glutton_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
python3 scripts/02_compose.py glutton_G work/canvas_glutton_G.png | tail -1
