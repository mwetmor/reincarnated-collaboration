#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/blightsac_tripo.glb builds/blightsac_prep.glb 1.6 --maxext --yaw -90 --minisland 0.0003 --faces 40000 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n18_rig_float.py -- builds/blightsac_prep.glb work/cfg_blightsac.json builds/blightsac_rig_${BS_V:-v1}.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/blightsac_rig_${BS_V:-v1}.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/blightsac_rig_${BS_V:-v1}.glb strip work/strip_bs_${BS_V:-v1}.png 'W|idle:0,walk:10,run:6,cast_breath:19,cast_orb:14,cast_aura:43,hit:4,death:20,death:55,idle:30,walk:20,cast_breath:30' --side 2>&1 | grep -i 'error\|sheet'
