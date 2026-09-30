#!/bin/bash
# T12_8 -- THE CORRECTED CLIPS, the guard re-solved on them, the bash and chop guards -- INSTALL.
# STAGED, NOT RUN: run by the conductor on Matt's word, at a cliffside3d window.
#
# THE PRE-STATE IS NAMED, TWICE. Matt may install T12_7 first, so this passes only when the nine
# installed files match EXACTLY one of two known lists -- today's installed set (A) or T12_7's (B) --
# and it prints which one it found. Anything else (a mix, a third state) stops it before a byte moves.
#   A  installed 2026-09-30: knight bf23c13e, character b3b62c63, the D2 GLBs (nb-body 07ccabd6)
#   B  T12_7 (attack_lab/staged/t12_guard/install.sh): knight ef8ebfb4, character bfaf4997,
#      nb-body 8c5b43d7 and the T12_2 mount pieces
# THE SET:
#   knight.gd       ea761ba8  = attack_lab/tools/strike_release_patch.py (pose_for) over
#                               attack_lab/tools/axeguard_patch.py over the installed bf23c13e
#   character.json  b676c2a3  = T12_7's + strike_release.pose_for (the bash, the chop's release)
#   nb-body.glb     8a59acf9  = nb_d2/export_staging/T12_8_guard: walk_armed, idle_armed, block,
#                               shield_bash, chop_overhead_92 re-grafted from body-rig sources (55),
#                               the guard poses re-solved (54 pose --replace, + the bash and chop
#                               guards), the weapon_r channel re-solved (54 channel --replace)
#   six pieces                = the T12_2 mount set (unchanged since T12_7)
# ROLLBACK to A: staged/speed_split/{knight.gd,character.json} + attack_lab/t12/godot/models/gear_orig/;
#          to B: staged/t12_guard/{knight.gd,character.json} + nb_d2/export_staging/T12_7_guard/.
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/t12_8
GL=$B/nb_d2/export_staging/T12_8_guard
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/t12_8_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 25 ] || fail "disk below the 25 GiB gate"

FILES=(scripts/knight.gd data/character.json models/gear/nb-body.glb models/gear/axe.glb models/gear/bracers.glb
       models/gear/byrnie.glb models/gear/helmet.glb models/gear/mantle.glb models/gear/shield.glb)
PRE_A=(bf23c13e1ac58c4dfcbf90e0a081b3ea b3b62c633f9e7a05862b02cb418efd27 07ccabd602963548619c1e63201ab52b
       960c398c08330f5a56599ad5aa96ab32 1f2a1b147ecb2a3218876130293f140d bf4750af62f23c686ef807084d444c9a
       9b8421429fd25e9a6abeaf619dc56faf 0e96a2c8a83841119e7c9067463f88d8 0eb899d48c58651a6b2632b8cf033973)
PRE_B=(ef8ebfb463f039994736c86261f967ee bfaf499789c3fc304ff37285b7a20da8 8c5b43d7a415ac8b9dfd98318eac80c8
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540)

echo "== 1 pre-state: the nine installed files against the two known lists"
# (bash 3.2, macOS's /bin/bash: no namerefs -- both lists counted in one pass)
NA=0; NB=0; TABLE=""
for i in "${!FILES[@]}"; do
  got=$(md5 -q "$C/${FILES[$i]}" 2>/dev/null || echo MISSING)
  [ "$got" = "${PRE_A[$i]}" ] && NA=$((NA + 1))
  [ "$got" = "${PRE_B[$i]}" ] && NB=$((NB + 1))
  TABLE="$TABLE   ${FILES[$i]}  $got  (A ${PRE_A[$i]:0:8}, B ${PRE_B[$i]:0:8})\n"
done
if [ $NA -eq ${#FILES[@]} ]; then echo "   found A: today's installed set (knight bf23c13e), $NA of ${#FILES[@]} files"
elif [ $NB -eq ${#FILES[@]} ]; then echo "   found B: T12_7 (knight ef8ebfb4), $NB of ${#FILES[@]} files"
else printf "$TABLE"; fail "the installed files match neither A ($NA of ${#FILES[@]}) nor B ($NB of ${#FILES[@]}) exactly"
fi
chk() { local f=$1 want=$2; local got; got=$(md5 -q "$f") || fail "missing $f"; [ "$got" = "$want" ] || fail "$f is $got, want $want"; }
chk $ST/knight.gd ea761ba8c1359209f39234e2953b1d3c
chk $ST/character.json b676c2a3239d514badcef2543f8fe883
chk $GL/nb-body.glb 8a59acf95c749b7c8344d547ba11ac12
echo "   staged sources ok"

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd ea761ba8c1359209f39234e2953b1d3c
inst $ST/character.json $C/data/character.json b676c2a3239d514badcef2543f8fe883
inst $GL/nb-body.glb $C/models/gear/nb-body.glb 8a59acf95c749b7c8344d547ba11ac12
inst $GL/axe.glb $C/models/gear/axe.glb d7762e1b40dc37a238d9da761cf4ec95
inst $GL/bracers.glb $C/models/gear/bracers.glb 5254292e1d894902a60f4749c3cc7abb
inst $GL/byrnie.glb $C/models/gear/byrnie.glb d1fe5c22eb60be92dc26cc1fff21a802
inst $GL/helmet.glb $C/models/gear/helmet.glb 185ca9f74af564da3f2443195c0c030f
inst $GL/mantle.glb $C/models/gear/mantle.glb 54669c6f2298950c9dc0ffcd8d936f70
inst $GL/shield.glb $C/models/gear/shield.glb cdf1c9e12a521531e79ee24f8c1a1540

echo "== 3 re-import"
python3 $LOCK C-9 -- $GODOT --path $C --headless --import > $S/import.log 2>&1
N=$(grep -ac 'SCRIPT ERROR' $S/import.log); echo "   script errors: $N"
[ "$N" = "0" ] || { grep -a -A3 'SCRIPT ERROR' $S/import.log | head -12; fail "import has script errors"; }

echo "== 4 build the cliffside 3D app"
bash $B/cliffside3d/tools/build_app.sh > $S/build_cliffside.log 2>&1; RC=$?
tail -6 $S/build_cliffside.log; [ $RC -eq 0 ] || fail "cliffside build exit $RC"
LL=$B/cliffside3d/app/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LL), WARNING lines $(grep -ac 'WARNING' $LL), $(grep -a 'axe guard layer' $LL | tail -1), $(grep -a 'strike release' $LL | tail -1)"

echo "== 5 build the Barrow app"
bash $B/cliffside3d/tools/build_app_barrow.sh > $S/build_barrow.log 2>&1; RC=$?
tail -8 $S/build_barrow.log; [ $RC -eq 0 ] || fail "barrow build exit $RC"
LB=$B/cliffside3d/app_barrow/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LB), $(grep -a 'foot_lock nodes' $LB | tail -1), $(grep -a 'strike release' $LB | tail -1)"

echo "== 6 the armed Barrow walk, play camera, --fixed-fps 24"
python3 $LOCK C-9 -- $GODOT --path $C --fixed-fps 24 --resolution 640x360 --script tools/shot_barrow_armed.gd -- --out $S/walk > $S/walk.log 2>&1
grep -aE "^\[armed\]|SCRIPT ERROR|WATCHDOG" $S/walk.log | cut -c1-200
N=$(ls $S/walk/frames 2>/dev/null | wc -l | tr -d ' ')
ffmpeg -v error -y -framerate 24 -i $S/walk/frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/barrow_walk_armed_t12_8.mp4"
if [ -s "$DEST/barrow_walk_armed_t12_8.mp4" ] && [ "$N" -gt 0 ]; then find $S/walk/frames -name 'f_*.jpg' -delete; echo "   $N frames -> barrow_walk_armed_t12_8.mp4, frames deleted"; else echo "   KEPT frames: encode failed"; fi
echo "== done"
