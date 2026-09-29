#!/bin/bash
# C-9 T10-2: run one Godot command on the barrow_full sandbox, behind the shared heavy lock,
# after the disk check the run's rules require (halt under 42 GiB free).
#   usage: tools/godot_locked.sh LOGFILE -- <godot args...>
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
LOG=${1:?usage: godot_locked.sh LOGFILE -- args}
shift; [ "${1:-}" = "--" ] && shift
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
echo "== free disk: ${FREE} GiB" | tee "$LOG"
if [ "$FREE" -lt 42 ]; then echo "HALT: under 42 GiB free" | tee -a "$LOG"; exit 9; fi
cd "$HERE/../godot"
rc=0
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" "$@" >> "$LOG" 2>&1 || rc=$?
echo "== exit $rc" >> "$LOG"
exit $rc
