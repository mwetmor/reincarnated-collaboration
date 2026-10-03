#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
df -h /System/Volumes/Data | tail -1
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n04_prep.py -- builds/frosthorn_tripo.glb builds/frosthorn_prep32.glb 3.2 --minisland 0.0003 --faces 50000 2>&1 | grep '^{' | cut -c1-200
blender -b -noaudio --python scripts/n04b_cull_box.py -- builds/frosthorn_prep32.glb builds/frosthorn_prep32_c.glb -0.4 0.4 -0.24 0.304 -0.01 0.336 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/frosthorn_prep32_c.glb work/cfg_frosthorn.json builds/frosthorn_rig_v3.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/frosthorn_rig_v3.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/frosthorn_rig_v3.glb strip work/strip_fh_v3.png 'SW|idle:0,walk:6,attack_gore:12,attack_gore:19,attack_butt:7,attack_charge:20,cast_roar:10,cast_roar:18,hit:4,death:30,death:60' 2>&1 | grep -i 'error\|sheet'
"
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n24_rig_horror.py -- builds/rifthorror_prep.glb work/cfg_rifthorror.json builds/rifthorror_rig_v1.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rifthorror_rig_v1.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/rifthorror_rig_v1.glb strip work/strip_rh_v1.png 'SW|idle:0,walk:8,run:5,attack_swipe:16,attack_impale:30,attack_impale:45,cast_rift:25,cast_rift:35,cast_drain:48,hit:4,death:49' 2>&1 | grep -i 'error\|sheet'
"
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n05_render.py -- builds/rimewolf_prep.glb look work/look_rimewolf_prep.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/rimewolf_prep.glb work/cfg_rimewolf.json builds/rimewolf_rig_v1.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rimewolf_rig_v1.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/rimewolf_rig_v1.glb strip work/strip_rw_v1.png 'SW|idle:0,walk:6,run:4,attack_snap:10,attack_bigbite:51,attack_bigbite:56,cast_breath:26,cast_breath:50,hit:4,death:60' 2>&1 | grep -i 'error\|sheet'
"
echo CHAIN_C_DONE
