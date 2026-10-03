#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
blender -b -noaudio --python scripts/e11_rig_wingquad.py -- builds/gloamwing_prep.glb work/cfg_gloamwing.json builds/gloamwing_rig_v3.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line ' | cut -c1-400
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/gloamwing_rig_v3.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_rig_v3.glb strip work/strip_gloamwing_v3.png 'SW|run:0,run:6,run:12,run:19,walk:19,emerge:0,emerge:5,hit:3,death:30' 2>&1 | grep -i 'error\|sheet'
