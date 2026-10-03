#!/usr/bin/env bash
set -uo pipefail
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad
R=$S/h3h5b/rt
ENG=$S/h3h5/g3/engine/src
dfcheck() { local f; f=$(df -g / | tail -1 | awk '{print $4}'); echo "[q] df free ${f} GiB"; [ "$f" -ge 20 ] || { echo "[q] DISK HALT"; exit 9; }; }
dfcheck
echo "[q] G3 port side on my own oracle traces (oracle frozen)"
bash $R/kc2_runtime/tools/kc2rt_g3_run25.sh V311-FULL $ENG $S/h3h5b/g3 shadow "M0:3,W1:2,M-POL-2:2,M0:0" > $S/h3h5b/g3_run.txt 2>&1
echo "[q] g3 rc=$?"; cat $S/h3h5b/g3_run.txt
dfcheck
echo "[q] G3 fresh oracle+port W1 s2 with the new oracle tool"
bash $R/kc2_runtime/tools/kc2rt_g3_run25.sh V311-FULL $ENG $S/h3h5b/g3_fresh shadow "W1:2" > $S/h3h5b/g3_fresh_run.txt 2>&1
echo "[q] g3 fresh rc=$?"; cat $S/h3h5b/g3_fresh_run.txt
dfcheck
echo "[q] suite"
bash $R/kc2_runtime/run_kc2_runtime_suite.sh > $S/h3h5b/suite.txt 2>&1
echo "[q] suite rc=$?"
echo "[q] DONE"
