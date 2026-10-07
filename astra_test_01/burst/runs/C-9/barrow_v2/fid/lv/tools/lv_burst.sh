#!/bin/bash
# BV2F LV Phase 1: run ONE BV2F-prefixed Astra burst, behind refs_guard (Tier-A frozen copy), the disk gate and the
# heavy lock; usage/rate-limit text in the run json/err -> exit 7 (charter § 6, DEV-15 regex). Never retries.
#   bash fid/lv/tools/lv_burst.sh BV2F-LV-<name>
set -uo pipefail
BID=${1:?usage: lv_burst.sh BV2F-LV-<name>}
case "$BID" in BV2F-*) ;; *) echo "HALT: not a BV2F burst id"; exit 2;; esac
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
LV=$B/runs/C-9/barrow_v2/fid/lv
TASK=$LV/briefs/$BID.task.json
LOCK=$B/runs/C-7/conductor_scripts/heavy_lock.py
L=$HOME/astra-burst/logs/C-9; mkdir -p "$L"
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ "$FREE" -ge 21 ] || { echo "HALT: ${FREE} GiB free"; exit 9; }
python3 "$B/runs/C-9/barrow_v2/fid/v1tools/tierA/conductor_scripts/refs_guard.py" "$TASK" || { echo "HALT H-guard $BID"; exit 3; }
cd "$B" && python3 "$LOCK" C-9 -- python3 lane/run_burst.py --run C-9 --burst-id "$BID" --type GENERATE --task "$TASK" > "$L/${BID}_run.json" 2> "$L/${BID}_run.err"
rc=$?
if grep -qiE "usage limit|rate limit|weekly limit|quota|too many requests|limit reached" "$L/${BID}_run.json" "$L/${BID}_run.err" 2>/dev/null; then
  echo "HALT USAGE LIMIT seen in $BID"; exit 7; fi
echo "[lv_burst] $BID rc=$rc $(head -c 400 "$L/${BID}_run.json")"
exit $rc
