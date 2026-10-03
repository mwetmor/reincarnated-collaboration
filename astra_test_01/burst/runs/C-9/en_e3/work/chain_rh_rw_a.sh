#!/bin/zsh
# EN-E3 R-C9-135: prep the rift horror (upright, by height) and the rime wolf (by length), then a look render of each prep
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
df -h /System/Volumes/Data | tail -1
python3 $H C-9 -- blender -b -noaudio --python scripts/n04_prep.py -- builds/rifthorror_tripo.glb builds/rifthorror_prep.glb 2.4 --height --yaw -90 --minisland 0.0003 --faces 45000 2>&1 | grep '^{'
python3 $H C-9 -- blender -b -noaudio --python scripts/n04_prep.py -- builds/rimewolf_tripo.glb builds/rimewolf_prep.glb 4.4 --minisland 0.0003 --faces 45000 2>&1 | grep '^{'
for N in rifthorror rimewolf; do python3 $H C-9 -- blender -b -noaudio --python scripts/n05_render.py -- builds/${N}_prep.glb look work/look_${N}_prep.png 2>&1 | grep -i 'error\|sheet'; done
