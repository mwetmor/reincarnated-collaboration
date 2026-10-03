#!/usr/bin/env bash
# jack-ryan H-3 RUNS fork: hit grid (port), emission probe, the full suite, the fresh w151-160 shadow runs per arm.
# Every Godot invocation is behind the heavy lock. Writes only to scratch.
set -uo pipefail
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad
R=$S/h3h5/rt
OUT=$S/h3h5/g3
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
H=$OUT/hitgrid/src/reincarnated/simulation/output/join1-hitchance-grid-v1
dfcheck() { local f; f=$(df -g / | tail -1 | awk '{print $4}'); echo "[queue_b] df free ${f} GiB"; [ "$f" -ge 20 ] || { echo "[queue_b] DISK HALT"; exit 9; }; }

dfcheck
echo "[queue_b] hitgrid"
( cd $R && python3 $LOCK JR-hitgrid -- perl -e "alarm shift; exec @ARGV" 900 $GODOT --headless --path . --script kc2_runtime/tools/kc2rt_hitgrid.gd -- grid=$H out=$OUT/hitgrid_port.json ) > $OUT/hitgrid_port.log 2>&1
echo "[queue_b] hitgrid rc=$?"

dfcheck
echo "[queue_b] emission probe"
( cd $R && python3 $LOCK JR-emission -- perl -e "alarm shift; exec @ARGV" 1800 $GODOT --headless --path . --script kc2_runtime/tests/kc2rt_emission_probe.gd ) > $OUT/emission_probe.log 2>&1
echo "[queue_b] emission rc=$?"

dfcheck
echo "[queue_b] suite"
bash $R/kc2_runtime/run_kc2_runtime_suite.sh > $OUT/suite.txt 2>&1
echo "[queue_b] suite rc=$?"

mkdir -p $OUT/shadow_fresh
for ARM in M0 M-POL-2 M-POL-2-NULL W1 W1-NULL; do
  dfcheck
  echo "[queue_b] shadow fresh $ARM"
  ( cd $OUT/proj && python3 $LOCK JR-shadow-$ARM -- perl -e "alarm shift; exec @ARGV" 3600 $GODOT --headless --path . --script jr/jr_shadow_fresh.gd -- arm=$ARM salt=0 waves=151-160 contact=shadow out=$OUT/shadow_fresh/${ARM}_s0.json ) > $OUT/shadow_fresh/${ARM}_s0.log 2>&1
  echo "[queue_b] shadow $ARM rc=$?"
done
echo "[queue_b] DONE"
