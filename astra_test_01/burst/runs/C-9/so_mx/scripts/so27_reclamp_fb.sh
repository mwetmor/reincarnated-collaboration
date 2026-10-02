#!/bin/zsh
# so_mx R-C9-134 flick fix: the Fire Ball's orb-staff clamp re-run with a SLOWER ramp. The 120 Hz pass held the staff back
# 0.09-0.14 s, then let it catch the hand at ~2000 deg/s (0.155-0.17 s): the clamp's rate limit (--rate 10 deg PER KEY)
# is 1200 deg/s at 120 Hz. Re-run from the unclamped Fire Ball channel (ss_c12_in: ss_c11 minus its weapon_r keys) with
# --rate R (deg per key at 120 Hz). Then the flick and penetration re-measure. Caller holds heavy_lock.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/so_mx; cd $R; RATE=${1:-2.5}
B=/Applications/Blender.app/Contents/MacOS/Blender; TO="python3 ../gear_sets/scripts/to.py"
${=TO} 2400 $B -b -noaudio --python scripts/so21_weapon_clamp.py -- work/ss_c12_in.glb work/ss_c12.glb work/layers_none.json --state cast_fireball_m --clip cast_fireball_m \
   --sword export/ss134b/orbstaff.glb --hz 120 --floor-tol 0 --sample-every 7 --rate $RATE --json work/clamp_fb_rate$RATE.json 2>&1 | grep -E "clamped keys|Error|Traceback|TIMEOUT" | cut -c1-260
mkdir -p export/ss134f; cp export/ss134c_final/* export/ss134f/; cp work/ss_c12.glb export/ss134f/so-body_ss134.glb
${=TO} 1800 $B -b -noaudio --python scripts/so07_prop_checks.py -- export/ss134f/so-body_ss134.glb export/ss134f work/props_ss134f_parity.json --colliders "" --props orbstaff --clips cast_fireball_m --step 1 --parity 2>&1 | grep -E "^CHK|Error|Traceback" | cut -c1-300
echo RECLAMP_DONE
