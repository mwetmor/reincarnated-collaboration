#!/bin/zsh
# rime wolf: Tripo built the far legs as a ghost pair under the belly (footprint grid: contact at y 0.2-0.5, |x| < 0.32, between the
# fore feet (y -1.0) and the hind feet (y 0.9)) -> n04b cull, re-rig v3, fit, canvas on the culled prep
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
gate() { local g=$(df -k /System/Volumes/Data | tail -1 | awk '{print int($4/1048576)}'); echo "df ${g} GiB"; if [ $g -lt 21 ]; then echo "HALT disk ${g} GiB < 21"; exit 3; fi; }
gate
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n04b_cull_box.py -- builds/rimewolf_prep42.glb builds/rimewolf_prep42_c.glb -0.32 0.32 0.1 0.6 -0.01 0.58 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/rimewolf_prep42_c.glb work/cfg_rimewolf.json builds/rimewolf_rig_v3.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/rimewolf_rig_v3.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/t5_01_paint_sheet.py -- builds/rimewolf_prep42_c.glb work/canvas_rimewolf_G.png --layout packed --canvas 1536x1024 --elev 52.95 --name rimewolf_G --yaw 180 2>&1 | grep -i 'PAINT SHEET\|Error'
blender -b -noaudio --python scripts/n05_render.py -- builds/rimewolf_rig_v3.glb strip work/strip_rw_v3.png 'SW|idle:0,walk:6,run:4,attack_snap:10,attack_bigbite:56,cast_breath:26,hit:4,death:60' 2>&1 | grep -i 'error\|sheet'
"
python3 scripts/02_compose.py rimewolf_G work/canvas_rimewolf_G.png | tail -1
echo CHAIN_RW_D_DONE
