#!/bin/bash
# BV2F frozen-GD runner (lane PT, Gate-2 W-2(c)). Every BV2F Godot run of a v1 tool goes through this.
#   bash fid/v1tools/godot_run.sh <godot project dir> <tierB/.../tool.gd> [-- tool args...]
# 1. verify.sh must be green; 2. the .gd must be a SHA256SUMS row under tierA/ or tierB/ of THIS v1tools and
# match its shipped sha; 3. Godot runs it by ABSOLUTE path (--script) behind the heavy lock, disk gate 21 GiB.
# Exit 8 = verify failed; 10 = not a frozen tool / sha mismatch; 9 = disk gate; else Godot's exit.
set -uo pipefail
V="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ="${1:?usage: godot_run.sh <project> <tier/path.gd> [-- args]}"; REL="${2:?usage}"; shift 2
[ "${1:-}" = "--" ] && shift
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py}
bash "$V/verify.sh" > /dev/null || { echo "[godot_run] HALT: verify.sh failed" >&2; exit 8; }
case "$REL" in tierA/*.gd|tierB/*.gd) ;; *) echo "[godot_run] HALT: $REL is not under fid/v1tools/tier{A,B}/" >&2; exit 10;; esac
GD="$V/$REL"
want=$(awk -v p="./$REL" '$4 == p {print $1}' "$V/SHA256SUMS")
got=$(shasum -a 256 "$GD" 2>/dev/null | cut -d' ' -f1)
[ -n "$want" ] && [ "$want" = "$got" ] || { echo "[godot_run] HALT: $REL sha ${got:0:12} != SHA256SUMS ${want:0:12}" >&2; exit 10; }
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge 21 ] || { echo "[godot_run] HALT: ${FREE} GiB free (< 21)" >&2; exit 9; }
echo "[godot_run] $REL sha ${got:0:12} on $PROJ" >&2
cd "$PROJ" && python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --path "$PROJ" --resolution 640x360 --script "$GD" -- "$@"
