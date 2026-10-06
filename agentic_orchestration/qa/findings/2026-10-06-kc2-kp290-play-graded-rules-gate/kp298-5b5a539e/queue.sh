#!/usr/bin/env bash
set -uo pipefail
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad
R=$S/kp298/rt
ENG=$S/h3h5/g3/engine/src
LOCK=$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
dfcheck() { local f; f=$(df -g / | tail -1 | awk '{print $4}'); echo "[q] df free ${f} GiB"; [ "$f" -ge 21 ] || { echo "[q] DISK HALT"; exit 9; }; }
dfcheck
echo "[q] G3 port side at 0eacae1 on my own oracle traces"
bash $R/kc2_runtime/tools/kc2rt_g3_run25.sh V311-FULL $ENG $S/kp298/g3 shadow "M0:3,W1:2,M-POL-2:2" > $S/kp298/g3_run.txt 2>&1
echo "[q] g3 rc=$?"; cat $S/kp298/g3_run.txt
dfcheck
echo "[q] T-A pre_read at 892bb1c2 (scratch archive; no .app here)"
G3D=$(ls -d $S/kp298/filed/evidence/kc2-play/*/summaries)
( cd $R && python3 $LOCK JR-kp298-preread -- perl -e "alarm shift; exec @ARGV" 3600 $GODOT --headless --path . --script kc2_runtime/tests/kc2rt_ta.gd -- expect_runtime=5b5a539e3bc7474e3d1e7e9220b37944e326dbae33fa80a38dd1dc19368788e9 g3=$G3D run_kind=pre_read ) > $S/kp298/preread.log 2>&1
echo "[q] preread rc=$?"; grep "T-A EMITTED\|ABORT" $S/kp298/preread.log
echo "[q] DONE"
