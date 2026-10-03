#!/bin/bash
# C-9 R-C9-139: every character x every light (current / the cliffside's rig / candidates), stills + masks at the play
# camera under the PHONE's renderer (Compatibility on ANGLE, the web branches on). One heavy-lock hold for the lot.
#   tools/charlight_probe_all.sh OUTDIR "tags" "whos"     e.g. ... take/build/charlight "cur ref a b c" "barbarian sorceress warlord"
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=${1:?outdir}; TAGS=${2:-"cur ref a b c"}; WHOS=${3:-"barbarian sorceress warlord"}
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
[ "$FREE" -ge 20 ] || { echo "HALT: under 20 GiB free"; exit 9; }
if [ -z "${C9_LOCKED:-}" ]; then
  exec env C9_LOCKED=1 python3 "$HOME/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py" C-9 -- bash "$0" "$@"
fi
mkdir -p "$OUT/logs"
cd "$HERE/../godot"
for who in $WHOS; do
  for tag in $TAGS; do
    X=""
    case "$tag" in ref) X="--ref cliff";; cur) X="";; *) X="--charlight $tag";; esac
    FULL=""; [ "${CL_FULL:-0}" = 1 ] && FULL="--full"
    perl -e 'alarm shift; exec @ARGV' 300 "$GODOT" --path . --resolution 1920x1080 --rendering-method gl_compatibility \
      --rendering-driver opengl3_angle --fixed-fps 60 --script tools/probe_charlight.gd -- --as-web --c $who $X \
      --out "$OUT" --tag $tag $FULL > "$OUT/logs/${tag}_${who}.log" 2>&1
    echo "$who $tag exit $? $(grep -a -c -E 'SCRIPT ERROR|SHADER ERROR' "$OUT/logs/${tag}_${who}.log") errors; $(grep -a '^\[barrow_painted\] web:' "$OUT/logs/${tag}_${who}.log" | grep -o 'charlight=[^ ]*')"
  done
done
