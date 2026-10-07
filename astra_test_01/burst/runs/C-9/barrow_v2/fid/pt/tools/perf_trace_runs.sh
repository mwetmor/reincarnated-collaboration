#!/bin/zsh
# BV2F PT (R-C9-201): N fresh traced P10 runs at a view (pt_perf_trace.gd = ph_life perf + full frame trace), disk-gated + heavy lock
TAG=$1; N=${2:-3}; VIEW=${3:-0,0}
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; G=/Applications/Godot.app/Contents/MacOS/Godot; LOCK=$C9/../C-7/conductor_scripts/heavy_lock.py
O=$FID/pt/perf/$TAG; export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
for r in $(seq 1 $N); do
  mkdir -p $O/trace_run$r; gate
  (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G --path . --resolution 1920x1080 --script res://tools/bv2f/pt_perf_trace.gd -- --out $O/trace_run$r --view $VIEW > $O/trace_run$r/log.txt 2>&1); echo "trace run$r rc=$?"
  python3 -c "
import json;t=json.load(open('$O/trace_run$r/trace.json'));print('run$r',t['measured'],'spikes',[(s['f'],s['ms'],s.get('uv'),s['proc'],s['phys']) for s in t['spikes']][:12])"
done
echo ALLDONE
