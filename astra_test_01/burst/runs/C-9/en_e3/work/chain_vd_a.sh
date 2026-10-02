#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/voiddrone_tripo.glb builds/voiddrone_prep.glb ${VD_LEN:-3.6} --minisland 0.00005 --faces 50000 ${VD_FLIP:-} 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/voiddrone_prep.glb work/cfg_voiddrone.json builds/voiddrone_rig_${VD_V:-v1}.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/voiddrone_rig_${VD_V:-v1}.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/voiddrone_rig_${VD_V:-v1}.glb strip work/strip_vd_${VD_V:-v1}.png 'SW|idle:0,walk:6,run:4,attack_impale:12,attack_impale:18,attack_slash:12,cast_spit:16,cast_rear:28,hit:3,death:15,death:29,walk:18' 2>&1 | grep -i 'error\|sheet'
