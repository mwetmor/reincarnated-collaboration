#!/bin/zsh
# so_mx R-C9-134 fix, pass 2: the parity re-measure (so07 --parity, Blender's 24 fps frames) still found the orb staff in her
# body at 3 Fire Ball frames (8 sampled verts) and 1 run frame (1 vert) -- between the 60 Hz clamp keys. Re-clamp those two
# clips on a 120 Hz grid (from ss_c8's unclamped clips, chained onto ss_c9 -> ss_c10), then re-measure. Caller holds heavy_lock.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R
B=/Applications/Blender.app/Contents/MacOS/Blender; TO="python3 ../gear_sets/scripts/to.py"
cp work/ss_c9.glb work/ss_c10.glb
for c in cast_fireball_m run; do
  ${=TO} 2400 $B -b -noaudio --python scripts/so21_weapon_clamp.py -- work/ss_c10.glb work/ss_c10.glb work/layers_none.json --state $c --clip $c \
     --sword export/ss134b/orbstaff.glb --hz 120 --floor-tol 0 --json work/clamp120_$c.json 2>&1 | grep -E "clamped keys|Error|Traceback|TIMEOUT" | cut -c1-260
done
mkdir -p export/ss134d; cp export/ss134c/* export/ss134d/; cp work/ss_c10.glb export/ss134d/so-body_ss134.glb
${=TO} 2700 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/ss134d/so-body_ss134.glb export/ss134d work/props_ss134d_parity.json --colliders "" --props orbstaff --clips walk,run,cast_fireball_m,cast_meteor,death --step 1 --parity --who 2>&1 | grep -E "^CHK|^WHO|Error|Traceback" | cut -c1-400
echo PASS2_DONE
