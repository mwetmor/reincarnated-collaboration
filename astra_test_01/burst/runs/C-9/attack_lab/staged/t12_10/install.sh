#!/bin/bash
# T12_10 -- T12_9 WITH THE TEXT-TO-MOTION LOOPS ON THEIR SOURCE CLOCK AND THEIR SEAMS BLENDED (run_armed, both strafes),
# FOOT-LOCK SPEEDS, THE MANIFEST SPEED UNIT FIXED, THE MANIFEST'S PROVENANCE CORRECTED -- INSTALL.
# STAGED, NOT RUN: run by the conductor on Matt's word, at a cliffside3d window.
#
# THE PRE-STATE IS NAMED, FOUR TIMES. Matt may install T12_7, T12_8 or T12_9 first, so this passes only when
# the ten installed files match EXACTLY one of four known lists -- today's installed set (A), T12_7's (B),
# T12_8's (C) or T12_9's (D) -- and it prints which one it found. Anything else (a mix, a fifth state) stops
# it before a byte moves. The tenth file is data/gear_manifest.json: no earlier set installs it, so it is
# d498cb6a in all four; T12_10 installs it (the scene reads its locomotion speeds from it).
#   A  installed 2026-09-30: knight bf23c13e, character b3b62c63, the D2 GLBs (nb-body 07ccabd6)
#   B  T12_7 (attack_lab/staged/t12_guard/install.sh): knight ef8ebfb4, character bfaf4997,
#      nb-body 8c5b43d7 and the T12_2 mount pieces
#   C  T12_8 (attack_lab/staged/t12_8/install.sh): knight ea761ba8, character b676c2a3,
#      nb-body 8a59acf9 and the same six pieces
#   D  T12_9 (attack_lab/staged/t12_9/install.sh): knight ea761ba8, character b676c2a3,
#      nb-body 91e3c4f8 and the same six pieces
# THE SET:
#   knight.gd          fb35d9d0  = attack_lab/tools/manifest_speed_patch.py then declared_filter_patch.py over
#                                  T12_9's ea761ba8: a manifest speed is stated at the reference scale like every
#                                  other px/s (it drove every manifest-priced clip at 0.799 of its speed); the axe
#                                  guard's filter is its DECLARED bone set (the coordinator's ruling)
#   character.json     45d757b5  = T12_9's + clip_px_s for the strafes and run_armed (the foot-lock speeds)
#   gear_manifest.json aa557a50  = nb_d2/export_staging/T12_10_strafes: the export manifest with
#                                  locomotion_in_place re-derived (foot-lock, source clock) and clip_sources
#                                  corrected (the wrong-rig provenance); 48_manifest_lint 0 mismatches
#   nb-body.glb        eb8a3837  = nb_d2/export_staging/T12_10_strafes: T12_9's body with run_armed and both
#                                  strafes re-timed to the t2m source's 30 fps and their seams blended
#                                  (58_loop_blend.py); every other clip byte-identical
#   six pieces                   = the T12_2 mount set (unchanged since T12_7)
# ROLLBACK to A: staged/speed_split/{knight.gd,character.json} + attack_lab/t12/godot/models/gear_orig/;
#          to B: staged/t12_guard/{knight.gd,character.json} + nb_d2/export_staging/T12_7_guard/;
#          to C: staged/t12_8/{knight.gd,character.json} + nb_d2/export_staging/T12_8_guard/;
#          to D: staged/t12_9/{knight.gd,character.json} + nb_d2/export_staging/T12_9_loops/;
#          and, for any of them, data/gear_manifest.json back to d498cb6a (tracked in git at
#          cliffside3d/godot/data/gear_manifest.json, ff29a8819; a copy at attack_lab/t12/godot/data/gear_manifest_t12_9.json).
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/t12_10
GL=$B/nb_d2/export_staging/T12_10_strafes
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/t12_10_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 20 ] || fail "disk below the 20 GiB gate (R-C9-88)"

FILES=(scripts/knight.gd data/character.json models/gear/nb-body.glb models/gear/axe.glb models/gear/bracers.glb
       models/gear/byrnie.glb models/gear/helmet.glb models/gear/mantle.glb models/gear/shield.glb data/gear_manifest.json)
PRE_A=(bf23c13e1ac58c4dfcbf90e0a081b3ea b3b62c633f9e7a05862b02cb418efd27 07ccabd602963548619c1e63201ab52b
       960c398c08330f5a56599ad5aa96ab32 1f2a1b147ecb2a3218876130293f140d bf4750af62f23c686ef807084d444c9a
       9b8421429fd25e9a6abeaf619dc56faf 0e96a2c8a83841119e7c9067463f88d8 0eb899d48c58651a6b2632b8cf033973
       d498cb6adba3fd40cedfe4fbe15455fd)
PRE_B=(ef8ebfb463f039994736c86261f967ee bfaf499789c3fc304ff37285b7a20da8 8c5b43d7a415ac8b9dfd98318eac80c8
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540
       d498cb6adba3fd40cedfe4fbe15455fd)
PRE_C=(ea761ba8c1359209f39234e2953b1d3c b676c2a3239d514badcef2543f8fe883 8a59acf95c749b7c8344d547ba11ac12
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540
       d498cb6adba3fd40cedfe4fbe15455fd)
PRE_D=(ea761ba8c1359209f39234e2953b1d3c b676c2a3239d514badcef2543f8fe883 91e3c4f846692d6f1e0f2f5175f534f3
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540
       d498cb6adba3fd40cedfe4fbe15455fd)

echo "== 1 pre-state: the ten installed files against the four known lists"
# (bash 3.2, macOS's /bin/bash: no namerefs -- all four lists counted in one pass)
NA=0; NB=0; NC=0; ND=0; TABLE=""
for i in "${!FILES[@]}"; do
  got=$(md5 -q "$C/${FILES[$i]}" 2>/dev/null || echo MISSING)
  [ "$got" = "${PRE_A[$i]}" ] && NA=$((NA + 1))
  [ "$got" = "${PRE_B[$i]}" ] && NB=$((NB + 1))
  [ "$got" = "${PRE_C[$i]}" ] && NC=$((NC + 1))
  [ "$got" = "${PRE_D[$i]}" ] && ND=$((ND + 1))
  TABLE="$TABLE   ${FILES[$i]}  $got  (A ${PRE_A[$i]:0:8}, B ${PRE_B[$i]:0:8}, C ${PRE_C[$i]:0:8}, D ${PRE_D[$i]:0:8})\n"
done
if [ $NA -eq ${#FILES[@]} ]; then echo "   found A: today's installed set (knight bf23c13e), $NA of ${#FILES[@]} files"
elif [ $NB -eq ${#FILES[@]} ]; then echo "   found B: T12_7 (knight ef8ebfb4), $NB of ${#FILES[@]} files"
elif [ $NC -eq ${#FILES[@]} ]; then echo "   found C: T12_8 (knight ea761ba8, nb-body 8a59acf9), $NC of ${#FILES[@]} files"
elif [ $ND -eq ${#FILES[@]} ]; then echo "   found D: T12_9 (knight ea761ba8, nb-body 91e3c4f8), $ND of ${#FILES[@]} files"
else printf "$TABLE"; fail "the installed files match none of A ($NA), B ($NB), C ($NC) or D ($ND) of ${#FILES[@]} exactly"
fi
chk() { local f=$1 want=$2; local got; got=$(md5 -q "$f") || fail "missing $f"; [ "$got" = "$want" ] || fail "$f is $got, want $want"; }
chk $ST/knight.gd fb35d9d0846ea0d5f4968fe6738eeb94
chk $ST/character.json 45d757b57395717ecb91560d1f38b0be
chk $GL/gear_manifest.json aa557a50014b8a758f05083db5925c5b
chk $GL/nb-body.glb eb8a3837229ac59d39097a073da2f04e
echo "   staged sources ok"

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd fb35d9d0846ea0d5f4968fe6738eeb94
inst $ST/character.json $C/data/character.json 45d757b57395717ecb91560d1f38b0be
inst $GL/gear_manifest.json $C/data/gear_manifest.json aa557a50014b8a758f05083db5925c5b
inst $GL/nb-body.glb $C/models/gear/nb-body.glb eb8a3837229ac59d39097a073da2f04e
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
ffmpeg -v error -y -framerate 24 -i $S/walk/frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/barrow_walk_armed_t12_10.mp4"
if [ -s "$DEST/barrow_walk_armed_t12_10.mp4" ] && [ "$N" -gt 0 ]; then find $S/walk/frames -name 'f_*.jpg' -delete; echo "   $N frames -> barrow_walk_armed_t12_10.mp4, frames deleted"; else echo "   KEPT frames: encode failed"; fi
echo "== done"
