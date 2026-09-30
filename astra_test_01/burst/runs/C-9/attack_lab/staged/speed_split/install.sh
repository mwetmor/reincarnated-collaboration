#!/bin/bash
# The armed-speed split INSTALL, run by the conductor on Matt's word ("Yes, install the armed speed fix").
# Mirrors the foot-lock handover: pre-state check, atomic install md5-verified, re-import, both app
# builds with their launch checks (the Barrow's now requires "[barrow] foot_lock nodes=0"), and the
# armed Barrow walk capture. Stops at the first failure. The build scripts take the heavy lock themselves.
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/speed_split
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/speed_split_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 25 ] || fail "disk below the 25 GiB gate"

echo "== 1 pre-state: the pair was built on exactly these"
[ "$(md5 -q $C/scripts/knight.gd)" = "d993b8ff9f338f5d6c554fae1daced21" ] || fail "cliffside3d knight.gd is not d993b8ff -- someone changed it"
[ "$(md5 -q $C/data/character.json)" = "ec39ac32881cb458ec2a409f08288795" ] || fail "cliffside3d character.json is not the rollback ec39ac32"
[ "$(md5 -q $ST/knight.gd)" = "bf23c13e1ac58c4dfcbf90e0a081b3ea" ] || fail "staged knight.gd is not bf23c13e"
[ "$(md5 -q $ST/character.json)" = "b3b62c633f9e7a05862b02cb418efd27" ] || fail "staged character.json is not b3b62c63"
echo "   ok"

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd bf23c13e1ac58c4dfcbf90e0a081b3ea
inst $ST/character.json $C/data/character.json b3b62c633f9e7a05862b02cb418efd27

echo "== 3 re-import"
python3 $LOCK C-9 -- $GODOT --path $C --headless --import > $S/import.log 2>&1
N=$(grep -ac 'SCRIPT ERROR' $S/import.log); echo "   script errors: $N"
[ "$N" = "0" ] || { grep -a -A3 'SCRIPT ERROR' $S/import.log | head -12; fail "import has script errors"; }

echo "== 4 build the cliffside 3D app"
bash $B/cliffside3d/tools/build_app.sh > $S/build_cliffside.log 2>&1; RC=$?
tail -6 $S/build_cliffside.log; [ $RC -eq 0 ] || fail "cliffside build exit $RC"
LL=$B/cliffside3d/app/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LL), WARNING lines $(grep -ac 'WARNING' $LL)"

echo "== 5 build the Barrow app"
bash $B/cliffside3d/tools/build_app_barrow.sh > $S/build_barrow.log 2>&1; RC=$?
tail -8 $S/build_barrow.log; [ $RC -eq 0 ] || fail "barrow build exit $RC"
LB=$B/cliffside3d/app_barrow/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LB), $(grep -a 'foot_lock nodes' $LB | tail -1)"

echo "== 6 the armed Barrow walk, play camera, --fixed-fps 24"
python3 $LOCK C-9 -- $GODOT --path $C --fixed-fps 24 --resolution 640x360 --script tools/shot_barrow_armed.gd -- --out $S/walk > $S/walk.log 2>&1
grep -aE "^\[armed\]|SCRIPT ERROR|WATCHDOG" $S/walk.log | cut -c1-200
N=$(ls $S/walk/frames 2>/dev/null | wc -l | tr -d ' ')
ffmpeg -v error -y -framerate 24 -i $S/walk/frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/barrow_walk_armed_speed_split.mp4"
if [ -s "$DEST/barrow_walk_armed_speed_split.mp4" ] && [ "$N" -gt 0 ]; then find $S/walk/frames -name 'f_*.jpg' -delete; echo "   $N frames -> barrow_walk_armed_speed_split.mp4, frames deleted"; else echo "   KEPT frames: encode failed"; fi
echo "== done"
