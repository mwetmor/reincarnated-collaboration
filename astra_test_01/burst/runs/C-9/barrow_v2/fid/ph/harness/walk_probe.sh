#!/bin/zsh
# R-C9-272: P10 walk-validity probes (not P10 readings): ph_life perf with --loop, position trace in trace.json. Heavy lock.
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
G=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$C9/barrow_v2/fid/ph/harness/godot
R=$C9/barrow_v2/fid/ph/renders/${PH_WP_DIR:-walk_probe}
S=res://scenes/bv2f_pilot_painted.tscn
export BV2F_VARIANT=art BV2F_PILOT=${PH_WP_PILOT:-rp4}   # s61: site_ph3
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
while [ $# -ge 2 ]; do
  name=$1; loop=$2; shift 2
  mkdir -p $R/$name; gate
  (cd $C9/barrow_full/godot && python3 $LOCK C-9 -- $G --path . --resolution 1920x1080 --script $H/ph_life.gd -- perf $S $R/$name uv:0,0 --loop "$loop" > $R/$name/log.txt 2>&1)
  echo "$name rc=$?"
done
