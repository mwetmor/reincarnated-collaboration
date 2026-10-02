#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/rimethorn_tripo.glb builds/rimethorn_prep.glb ${RT_LEN:-3.0} --minisland 0.0003 --faces 45000 ${RT_FLIP:-} 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/rimethorn_prep.glb work/cfg_rimethorn.json builds/rimethorn_rig_${RT_V:-v1}.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rimethorn_rig_${RT_V:-v1}.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/rimethorn_rig_${RT_V:-v1}.glb strip work/strip_rim_${RT_V:-v1}.png 'W|idle:0,attack_swipe:20,cast_impale:18,cast_shards:31,hit:4,idle:40' --side --legs 2>&1 | grep -i 'error\|sheet'
