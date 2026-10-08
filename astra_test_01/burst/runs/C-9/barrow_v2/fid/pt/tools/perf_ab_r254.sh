#!/bin/zsh
# BV2F PT (R-C9-254): P10 A/B profiling -- PH's own probe (ph_life.gd perf, s34: 3 fresh runs per cell), one subsystem off
# at a time (env BV2F_PROF_OFF, an instrument the pilot build ignores when unset), each run its own short heavy-lock hold
# (pt_godot.py). Out: fid/pt/perf/r254/<toggle>_<view>_<i>/perf.json
#   zsh fid/pt/tools/perf_ab_r254.sh "<toggle> ..." "<view> ..."   toggle = baseline | <off,list> | try-<try,list>
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; G=/Applications/Godot.app/Contents/MacOS/Godot; H=$FID/ph/harness/godot
S=res://scenes/bv2f_pilot_painted.tscn; O=$FID/pt/perf/r254
export BV2F_VARIANT=art BV2F_PILOT=rp3
typeset -A VIEW; VIEW=(start uv:0,0 sea uv:-29,-5.5)
for t in ${=1}; do for v in ${=2}; do for i in 1 2 3; do
  d=$O/${PILOTSET:+${PILOTSET}_}${t}_${v}_$i; mkdir -p $d
  off=$t; try=""; [ "$t" = "baseline" ] && off=""
  case $t in try-*) off=""; try=${t#try-};; esac   # try-<a,b>: BV2F_PROF_TRY candidate fixes
  [ -n "${PILOTSET:-}" ] && export BV2F_PILOT=$PILOTSET   # PILOTSET=rp2: the previous pilot, same probe
  (cd $C9/barrow_full/godot && BV2F_PROF_OFF=$off BV2F_PROF_TRY=$try python3 $FID/pt/tools/pt_godot.py --log $d/log.txt --timeout-s 600 -- $G --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $d ${VIEW[$v]}) > /dev/null
  python3 -c "import json;p=json.load(open('$d/perf.json'));print('$t $v $i', p['p50_ms'], p['p99_ms'], p['max_ms'])" 2>/dev/null || echo "$t $v $i FAILED"
done; done; done
