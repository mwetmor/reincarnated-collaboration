#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py; V=${FH_V:-v2}
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n04b_cull_box.py -- builds/frosthorn_prep.glb builds/frosthorn_prep_c.glb -0.5 0.5 -0.3 0.38 -0.01 0.42 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/frosthorn_prep_c.glb work/cfg_frosthorn.json builds/frosthorn_rig_$V.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/frosthorn_rig_$V.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/frosthorn_rig_$V.glb strip work/strip_fh_$V.png 'SW|idle:0,walk:6,run:4,attack_gore:12,attack_gore:19,attack_charge:20,cast_roar:15,cast_roar:18,hit:4,death:60' --side --legs 2>&1 | grep -i 'error\|sheet'
"
