#!/bin/bash
# C-9 T10-2: run one Godot command on the barrow_full sandbox, behind the shared heavy lock,
# after the disk check the run's rules require (the conductor's gate: halt under DISK_GATE_GIB free,
# 25 GiB since 2026-09-30; it was 42 when this was written).
#   usage: tools/godot_locked.sh LOGFILE -- <godot args...>
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
LOG=${1:?usage: godot_locked.sh LOGFILE -- args}
shift; [ "${1:-}" = "--" ] && shift
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
GATE=${DISK_GATE_GIB:-20}
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
echo "== free disk: ${FREE} GiB (gate ${GATE})" | tee "$LOG"
if [ "$FREE" -lt "$GATE" ]; then echo "HALT: under ${GATE} GiB free" | tee -a "$LOG"; exit 9; fi
cd "$HERE/../godot"
rc=0
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" "$@" >> "$LOG" 2>&1 || rc=$?
echo "== exit $rc" >> "$LOG"
exit $rc
