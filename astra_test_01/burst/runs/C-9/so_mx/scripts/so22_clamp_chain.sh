#!/bin/zsh
# so_mx R-C9-134 fix: the orb staff (weapon_r) clamped out of her body (so21 = the JOIN lane's weapon clamp, 60 Hz grid)
# in cast_fireball_m, cast_meteor, death, walk, run -- one clip per Blender run, chained in-place on work/ss_c9.glb.
# The caller wraps this script in heavy_lock.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R
B=/Applications/Blender.app/Contents/MacOS/Blender; TO="python3 ../gear_sets/scripts/to.py"
cp work/ss_c8.glb work/ss_c9.glb
for c in cast_fireball_m cast_meteor death walk run; do
  ${=TO} 2400 $B -b -noaudio --python scripts/so21_weapon_clamp.py -- work/ss_c9.glb work/ss_c9.glb work/layers_none.json --state $c --clip $c \
     --sword export/ss134b/orbstaff.glb --hz 60 --floor-tol 0 --json work/clamp_$c.json 2>&1 | grep -E "clamped keys|Error|Traceback|TIMEOUT" | cut -c1-260
done
echo CLAMP_DONE
