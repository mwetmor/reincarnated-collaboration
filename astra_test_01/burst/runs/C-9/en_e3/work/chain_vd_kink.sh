#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/voiddrone_prep.glb work/cfg_voiddrone.json builds/voiddrone_rig_v11.glb 2>&1 | grep "penetration_frames.: [1-9]\|wrote\|Error"
blender -b -noaudio --python scripts/n05_render.py -- builds/voiddrone_rig_v11.glb strip work/strip_vd_v11.png 'SW|attack_impale:12,attack_impale:18,attack_slash:12,cast_rear:28,walk:6,idle:0' 2>&1 | grep -i 'sheet\|error'
for c in attack_impale:12 attack_slash:12; do blender -b -noaudio --python $EN3_TMP/stretch.py -- builds/voiddrone_rig_v11.glb ${c%%:*} ${c##*:} 2>&1 | grep -A1 "stretched edges" | cut -c1-200; done
for c in attack_impale:12 attack_slash:12; do blender -b -noaudio --python $EN3_TMP/stretch.py -- builds/voiddrone_rig_v9.glb ${c%%:*} ${c##*:} 2>&1 | grep "stretched edges"; done
