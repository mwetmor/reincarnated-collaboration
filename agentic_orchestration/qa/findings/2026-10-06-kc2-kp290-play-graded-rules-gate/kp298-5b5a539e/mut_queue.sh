#!/usr/bin/env bash
set -uo pipefail
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
for d in play_ok play_mut; do
  f=$(df -g / | tail -1 | awk '{print $4}'); [ "$f" -ge 21 ] || { echo DISK HALT; exit 9; }
  ( cd $S/kp298/$d/kc2_play && python3 $LOCK JR-kp298-$d-audit -- perl -e "alarm shift; exec @ARGV" 1800 $GODOT --headless --path . --script tools/kc2p_config_audit.gd -- seed=0 n=1 ) > $S/kp298/${d}_audit.txt 2>&1; echo "$d audit rc=$?"
  ( cd $S/kp298/$d/kc2_play && python3 $LOCK JR-kp298-$d-s47 -- perl -e "alarm shift; exec @ARGV" 2400 $GODOT --headless --path . --script tools/kc2p_s47_harness.gd -- seeds=0 ablate=arena ) > $S/kp298/${d}_s47_plain_abl.txt 2>&1; echo "$d s47 rc=$?"
done
echo DONE
