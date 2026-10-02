#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/glutton_tripo.glb builds/glutton_prep.glb ${GL_H:-2.3} --height --yaw ${GL_YAW:--90} --minisland 0.0003 --faces 40000 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n19_rig_biped.py -- builds/glutton_prep.glb work/cfg_glutton.json builds/glutton_rig_${GL_V:-v1}.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/glutton_rig_${GL_V:-v1}.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/glutton_rig_${GL_V:-v1}.glb strip work/strip_gl_${GL_V:-v1}.png 'W|idle:0,walk:8,walk:22,run:5,attack_bite:14,attack_thrash:13,cast_vomit:18,cast_vomit3:15,hit:4,death:25,death:49,idle:26' --side 2>&1 | grep -i 'error\|sheet'
