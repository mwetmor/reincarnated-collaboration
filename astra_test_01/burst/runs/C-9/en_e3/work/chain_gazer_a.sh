#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/gazer_tripo.glb builds/gazer_prep.glb ${GZ_LEN:-4.0} --minisland 0.0003 --faces 40000 --flip 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/gazer_prep.glb work/cfg_gazer.json builds/gazer_rig_v5.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/gazer_rig_v5.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/gazer_rig_v5.glb strip work/strip_gazer_v5.png 'SW|idle:0,walk:7,run:5,cast_glare:16,cast_breath:16,attack_tail:16,cast_spit:21,hit:4,death:36,idle:30,walk:22,cast_glare:28' 2>&1 | grep -i 'error\|sheet'
