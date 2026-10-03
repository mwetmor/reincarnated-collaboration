#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
blender -b -noaudio --python scripts/n04_prep.py -- builds/coilseer_tripo.glb builds/coilseer_prep.glb 2.2 --height --flip --minisland 0.0003 --faces 40000 --anchor_upper 0.9 --tail_compress 0.25,2.3 2>&1 | grep '^{\|tail_compress' | cut -c1-400
blender -b -noaudio --python scripts/n05_render.py -- builds/coilseer_prep.glb look work/look_coilseer_prep.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/e10_rig_coil.py -- builds/coilseer_prep.glb work/cfg_coilseer.json builds/coilseer_rig_v2.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line ' | cut -c1-300
blender -b -noaudio --python scripts/n17_fit_canvas.py -- builds/coilseer_rig_v2.glb 0.05 2>&1 | grep '^{'
blender -b -noaudio --python scripts/n05_render.py -- builds/coilseer_rig_v2.glb strip work/strip_coilseer_v2.png 'SW|idle:0,walk:10,walk:20,run:6,attack_claw:5,attack_claw:13,cast_bolt:25,cast_nova:18,cast_nova:30,attack_taillash:13,attack_taillash:23,hit:3,death:20,death:36' 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- builds/coilseer_rig_v2.glb strip work/strip_coilseer_v2_side.png 'W|idle:0,walk:10,run:6,attack_claw:13,cast_bolt:25,cast_nova:30,attack_taillash:23,death:36' --side 2>&1 | grep -i 'error\|sheet'
[ -f work/look_gloamwing_prep.png ] || blender -b -noaudio --python scripts/n05_render.py -- builds/gloamwing_prep.glb look work/look_gloamwing_prep.png 2>&1 | grep -i 'error\|sheet'
