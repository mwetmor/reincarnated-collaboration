#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n05_render.py -- builds/rimewolf_prep.glb look work/look_rimewolf_prep.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/rimewolf_prep.glb work/cfg_rimewolf.json builds/rimewolf_rig_v1.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rimewolf_rig_v1.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/rimewolf_rig_v1.glb strip work/strip_rw_v1.png 'W|idle:0,walk:6,run:4,attack_snap:10,attack_bigbite:50,attack_bigbite:56,cast_breath:26,cast_breath:50,hit:4,death:60' 2>&1 | grep -i 'error\|sheet'
"
echo CHAIN_RW_B_DONE
