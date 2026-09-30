#!/bin/bash
# THE HANDOVER, as one verified pass -- run ONLY when the coordinator releases cliffside3d.
#   1 pre-state checks (nobody changed what this replaces)   4 build the cliffside 3D app
#   2 install the approved FOOT-LOCK set, md5 after copy     5 build the Barrow app
#   3 re-import                                              6 the armed Barrow walk capture
# Stops at the first failure. Both build scripts take the heavy lock THEMSELVES -- they are run
# bare; wrapping them in heavy_lock.py deadlocks (it happened once).
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/footlock
GLB=$B/nb_d2/export_staging/A_damped/nb-body.glb
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/drax-atk/handover
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 42 ] || fail "disk below 42 GiB"

echo "== 1 pre-state: what is there now must be what the candidate was built on"
REL=astra_test_01/burst/runs/C-9/cliffside3d/godot
# the candidate is built on EXACTLY f2140e680's knight.gd and character.json (via cd6c2169 and
# fc9b4c9a); if either file in cliffside3d is anything else, the install would overwrite a change
for f in scripts/knight.gd data/character.json; do
  [ "$(md5 -q $C/$f)" = "$(git -C $R show f2140e680:$REL/$f | md5 -q)" ] || fail "cliffside3d $f is not f2140e680's -- someone changed it"
done
[ "$(md5 -q $C/models/gear/nb-body.glb)" = "f1017ee14dfe055bc77d54bb393fccbb" ] || fail "cliffside3d GLB is not the recentred f1017ee1..."
[ -e $C/scripts/foot_lock.gd ] && fail "a foot_lock.gd already exists in cliffside3d"
echo "   ok: knight.gd and character.json are f2140e680's, GLB f1017ee1, no foot_lock.gd yet"

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_handover" && mv "$dst.tmp_handover" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $GLB $C/models/gear/nb-body.glb 07ccabd602963548619c1e63201ab52b
inst $ST/knight.gd $C/scripts/knight.gd d993b8ff9f338f5d6c554fae1daced21
inst $ST/foot_lock.gd $C/scripts/foot_lock.gd a99b40f06b6ab7fbd37507270f9d84fe
inst $ST/character.json $C/data/character.json 3b85f1b3e46f7ea04d65d42d7f64258a

echo "== 3 re-import"
python3 $LOCK C-9 -- $GODOT --path $C --headless --import > $S/import.log 2>&1
echo "   script errors: $(grep -ac 'SCRIPT ERROR' $S/import.log)"
[ "$(grep -ac 'SCRIPT ERROR' $S/import.log)" = "0" ] || { grep -a -A3 'SCRIPT ERROR' $S/import.log | head -12; fail "import has script errors"; }

echo "== 4 build the cliffside 3D app"
bash $B/cliffside3d/tools/build_app.sh > $S/build_cliffside.log 2>&1; RC=$?
tail -14 $S/build_cliffside.log; [ $RC -eq 0 ] || fail "cliffside build exit $RC"
LL=$B/cliffside3d/app/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LL), recentre warnings $(grep -ac 'from the origin and never nearer' $LL), WARNING lines $(grep -ac 'WARNING' $LL)"
cp $LL $S/launch_cliffside.log

echo "== 5 build the Barrow app"
bash $B/cliffside3d/tools/build_app_barrow.sh > $S/build_barrow.log 2>&1; RC=$?
tail -14 $S/build_barrow.log; [ $RC -eq 0 ] || fail "barrow build exit $RC"
LB=$B/cliffside3d/app_barrow/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LB), recentre warnings $(grep -ac 'from the origin and never nearer' $LB), WARNING lines $(grep -ac 'WARNING' $LB)"
cp $LB $S/launch_barrow.log

echo "== 6 the armed Barrow walk, play camera, --fixed-fps 24"
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); [ "$FREE" -ge 42 ] || fail "disk below 42 GiB before the capture"
cp $ST/shot_barrow_armed.gd $C/../godot/tools/shot_barrow_armed.gd
python3 $LOCK C-9 -- $GODOT --path $C --fixed-fps 24 --resolution 640x360 --script tools/shot_barrow_armed.gd -- --out $S/walk > $S/walk.log 2>&1
grep -aE "^\[armed\]|SCRIPT ERROR|WATCHDOG" $S/walk.log | cut -c1-240
N=$(ls $S/walk/frames 2>/dev/null | wc -l | tr -d ' ')
ffmpeg -v error -y -framerate 24 -i $S/walk/frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/barrow_walk_armed.mp4"
if [ -s "$DEST/barrow_walk_armed.mp4" ] && [ "$N" -gt 0 ]; then find $S/walk/frames -name 'f_*.jpg' -delete; echo "   $N frames -> barrow_walk_armed.mp4 ($(du -h "$DEST/barrow_walk_armed.mp4" | cut -f1)), frames deleted"; else echo "   KEPT frames: encode failed"; fi
echo "== done"
