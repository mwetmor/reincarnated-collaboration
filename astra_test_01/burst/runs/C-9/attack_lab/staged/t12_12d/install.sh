#!/bin/bash
# T12_12d -- THE BARBARIAN'S LEGS TAKEN IN (Matt, R-C9-122) ON T12_12c F25L, AND A WALK WITH A HEEL-TO-TOE ROLL -- INSTALL.
#   bash install.sh N25   the stance narrowed by 25% of its excess over hip width
#   bash install.sh N40   by 40%                                                          [--dry-run as a second argument]
# STAGED, NOT RUN: run by the conductor on Matt's word, at a cliffside3d window.
#
# THE PRE-STATE IS EXACTLY F = T12_11 as installed (attack_lab/staged/t12_11/install.sh, 2026-09-30): the ten files
# below at T12_11's md5s AND models/gear/nb-body.glb.import with the animation optimizer off (9002fe85). Anything else
# stops it before a byte moves.
# THE SET (three files change; the other seven are copied and verified, byte-identical to T12_11's):
#   knight.gd          86141f65  = T12_11's, unchanged
#   character.json     09900b76  = T12_12b/c's (T12_11's ca2ce1ca + the axe guard layer at weight 1.0), unchanged
#   nb-body.glb        per variant = nb_d2/export_staging/T12_12d_<variant>: T12_12c F25L's body (23e5fde7) with
#                        walk  = Meshy library 566 'Walking 2' on his rig (55_clip_graft), one cycle on its source keys,
#                                seam blended (58_loop_blend offset w16): heel strike 21.6, toe-off 26.4 deg, rigid 36% of
#                                stance (the T8 walk: rigid 75%, heel held ~11 deg up), step width 0.71 x hip (was 1.48)
#                        idle, idle_guard, block, run, strafe_L_armed, strafe_R_armed narrowed by 66_stance_narrow.py
#                                (hips fixed, feet moved in along the clip's mean pelvis lateral, foot world orientation
#                                and height kept: planted stays planted; foot-lock speeds unchanged)
#   gear_manifest.json 5fdfc147  = T12_11's 0a81b2af + locomotion_in_place.walk (speed_m_s 1.3199, the new walk's foot-lock
#                                speed, which knight.gd prefers over walk_px_s 201.7) -- one file for both variants
#   the six pieces     = the T12_2 mount set, unchanged
# ROLLBACK to F: staged/t12_11/{knight.gd,character.json} + nb_d2/export_staging/T12_11_trails/{nb-body.glb,gear_manifest.json}
#   (gear_manifest 0a81b2af), re-import.
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
VAR=${1:-}
case "$VAR" in N25) BODY_MD5=1a195d9bc84ec3a90673b1e7630c0bb8;; N40) BODY_MD5=5603f68b88c412689514a6dadb585020;; *) echo "usage: install.sh N25|N40 [--dry-run]"; exit 2;; esac
MAN_MD5=5fdfc1474e2b61f0cd07609d1b3b8eb8
ST=$B/attack_lab/staged/t12_12d
GL=$B/nb_d2/export_staging/T12_12d_$VAR
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/t12_12d_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
DRY=0; [ "${2:-}" = "--dry-run" ] && DRY=1
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 20 ] || fail "disk below the 20 GiB gate (R-C9-88)"

FILES=(scripts/knight.gd data/character.json models/gear/nb-body.glb models/gear/axe.glb models/gear/bracers.glb
       models/gear/byrnie.glb models/gear/helmet.glb models/gear/mantle.glb models/gear/shield.glb data/gear_manifest.json)
PRE_F=(86141f65fec86dfb4b9f9ca296e93218 ca2ce1ca12c1c99fd546d5c35768b099 3e32a9fc7c9bcb5f12449c2b5bc927d6
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540
       0a81b2afbda88a518b882a90dbecf771)

echo "== 1 pre-state: the ten installed files and the body's import settings against F (T12_11)"
NF=0; TABLE=""
for i in "${!FILES[@]}"; do
  got=$(md5 -q "$C/${FILES[$i]}" 2>/dev/null || echo MISSING)
  [ "$got" = "${PRE_F[$i]}" ] && NF=$((NF + 1))
  TABLE="$TABLE   ${FILES[$i]}  $got  (F ${PRE_F[$i]:0:8})\n"
done
IMP=$C/models/gear/nb-body.glb.import
IMP_F=9002fe85b0f6722699f6270bbbfb1d30
[ $NF -eq ${#FILES[@]} ] || { printf "$TABLE"; fail "the installed files are not T12_11's: $NF of ${#FILES[@]} match F"; }
[ "$(md5 -q $IMP)" = "$IMP_F" ] || fail "$IMP is $(md5 -q $IMP), not T12_11's optimizer-off form $IMP_F"
echo "   found F: T12_11 (knight 86141f65, nb-body 3e32a9fc), $NF of ${#FILES[@]} files; nb-body.glb.import $IMP_F"
chk() { local f=$1 want=$2; local got; got=$(md5 -q "$f") || fail "missing $f"; [ "$got" = "$want" ] || fail "$f is $got, want $want"; }
chk $ST/knight.gd 86141f65fec86dfb4b9f9ca296e93218
chk $ST/character.json 09900b766cf9646b7f85c9572eaf03c6
chk $GL/gear_manifest.json $MAN_MD5
chk $GL/nb-body.glb $BODY_MD5
chk $GL/axe.glb d7762e1b40dc37a238d9da761cf4ec95
chk $GL/bracers.glb 5254292e1d894902a60f4749c3cc7abb
chk $GL/byrnie.glb d1fe5c22eb60be92dc26cc1fff21a802
chk $GL/helmet.glb 185ca9f74af564da3f2443195c0c030f
chk $GL/mantle.glb 54669c6f2298950c9dc0ffcd8d936f70
chk $GL/shield.glb cdf1c9e12a521531e79ee24f8c1a1540
echo "   staged sources ok"
[ $DRY -eq 1 ] && { echo "== DRY RUN: pre-state and sources verified; nothing copied"; exit 0; }

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd 86141f65fec86dfb4b9f9ca296e93218
inst $ST/character.json $C/data/character.json 09900b766cf9646b7f85c9572eaf03c6
inst $GL/gear_manifest.json $C/data/gear_manifest.json $MAN_MD5
inst $GL/nb-body.glb $C/models/gear/nb-body.glb $BODY_MD5
inst $GL/axe.glb $C/models/gear/axe.glb d7762e1b40dc37a238d9da761cf4ec95
inst $GL/bracers.glb $C/models/gear/bracers.glb 5254292e1d894902a60f4749c3cc7abb
inst $GL/byrnie.glb $C/models/gear/byrnie.glb d1fe5c22eb60be92dc26cc1fff21a802
inst $GL/helmet.glb $C/models/gear/helmet.glb 185ca9f74af564da3f2443195c0c030f
inst $GL/mantle.glb $C/models/gear/mantle.glb 54669c6f2298950c9dc0ffcd8d936f70
inst $GL/shield.glb $C/models/gear/shield.glb cdf1c9e12a521531e79ee24f8c1a1540
got=$(md5 -q $IMP); [ "$got" = "$IMP_F" ] || fail "$IMP changed under the install: $got"

echo "== 3 re-import"
python3 $LOCK C-9 -- $GODOT --path $C --headless --import > $S/import.log 2>&1
N=$(grep -ac 'SCRIPT ERROR' $S/import.log); echo "   script errors: $N"
[ "$N" = "0" ] || { grep -a -A3 'SCRIPT ERROR' $S/import.log | head -12; fail "import has script errors"; }

echo "== 4 build the cliffside 3D app"
bash $B/cliffside3d/tools/build_app.sh > $S/build_cliffside.log 2>&1; RC=$?
tail -6 $S/build_cliffside.log; [ $RC -eq 0 ] || fail "cliffside build exit $RC"
LL=$B/cliffside3d/app/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LL), WARNING lines $(grep -ac 'WARNING' $LL), $(grep -a 'axe guard layer' $LL | tail -1), $(grep -a 'from its swing end HELD' $LL | tail -1)"

echo "== 5 build the Barrow app"
bash $B/cliffside3d/tools/build_app_barrow.sh > $S/build_barrow.log 2>&1; RC=$?
tail -8 $S/build_barrow.log; [ $RC -eq 0 ] || fail "barrow build exit $RC"
LB=$B/cliffside3d/app_barrow/build/logs/launch.log
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LB), $(grep -a 'foot_lock nodes' $LB | tail -1), $(grep -a 'from its swing end HELD' $LB | tail -1)"

echo "== 6 the holds and the strikes in the painted Barrow, play camera, play speed (the installed scene; frames straight to ffmpeg)"
python3 $LOCK C-9 -- $GODOT --path $C --resolution 640x360 --fixed-fps 60 --script $B/attack_lab/t12/godot/tools/film_trails_scene.gd -- \
  --out "$DEST" --tag barrow_installed_t12_12d_$VAR --hold 1 --strikes holds,slash,chop,bash --label "INSTALLED -- T12_12d $VAR" > $S/strikes.log 2>&1
grep -aE "^\[scene\]|SCRIPT ERROR|WATCHDOG" $S/strikes.log | cut -c1-200
echo "== done"
