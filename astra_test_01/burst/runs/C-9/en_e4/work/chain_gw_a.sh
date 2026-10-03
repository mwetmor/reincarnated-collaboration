#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/gloamwing_tripo.glb builds/gloamwing_prep.glb 5.6 --flip --minisland 0.0003 --faces 45000 2>&1 | grep '^{' | cut -c1-400
blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_prep.glb look work/look_gloamwing_prep.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/e11_rig_wingquad.py -- builds/gloamwing_prep.glb work/cfg_gloamwing.json builds/gloamwing_rig_v1.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line ' | cut -c1-300
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/gloamwing_rig_v1.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_rig_v1.glb strip work/strip_gloamwing_v1.png 'SW|idle:0,walk:7,walk:21,run:6,attack_claw:12,attack_peck:13,cast_breath:26,cast_breath:50,cast_roar:12,emerge:5,emerge:28,hit:3,death:30' 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_rig_v1.glb strip work/strip_gloamwing_v1_side.png 'W|idle:0,walk:7,run:6,attack_claw:12,cast_breath:26,cast_roar:12,emerge:5,death:30' --side 2>&1 | grep -i 'error\|sheet'
