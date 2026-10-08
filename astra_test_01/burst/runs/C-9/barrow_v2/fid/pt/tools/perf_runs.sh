#!/bin/zsh
# usage: perf_runs.sh TAG  -- 3 PH P10 runs (ph_life.gd perf at uv:0,0) + 1 PT frame split, all disk-gated + heavy lock
PG=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_v2/fid/pt/tools/pt_godot.py   # every PT Godot run: lock + timeout + fatal script errors + log cap
TAG=$1
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=$C9/../C-7/conductor_scripts/heavy_lock.py
H=$FID/ph/harness/godot; S=res://scenes/bv2f_pilot_painted.tscn; O=$FID/pt/perf/$TAG
export BV2F_VARIANT=art
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
mkdir -p $O
for r in 1 2 3; do
  mkdir -p $O/p10_run$r; gate
  (cd $C9/barrow_full/godot && python3 $PG --log $O/p10_run$r/log.txt -- $G --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $O/p10_run$r uv:0,0); echo "p10 run$r rc=$?"
done
gate
(cd $C9/barrow_full/godot && python3 $PG --log $O/split.log -- $G --path . --resolution 1920x1080 --script res://tools/bv2f/pt_perf_split.gd -- --out $O/split --view 0,0); echo "split rc=$?"
python3 -c "
import json
for r in (1,2,3):
    p=json.load(open('$O/p10_run%d/perf.json'%r)); print('run',r,'p50',p['p50_ms'],'p99',p['p99_ms'],'max',p['max_ms'])"
echo ALLDONE
