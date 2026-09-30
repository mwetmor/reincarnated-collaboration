#!/bin/bash
# T12_11 -- T12_10 WITH STRIKE TRAILS, THE SLASH RE-CUT ON ITS SOURCE'S OWN KEYS, THE SHIELD ARM LAYER ON ITS DECLARED
# SET, AND THE LOCOMOTION SPEEDS RE-DERIVED BY THE SCENE'S FOOT-LOCK RULE -- INSTALL.
# STAGED, NOT RUN: run by the conductor on Matt's word, at a cliffside3d window.
#
# THE PRE-STATE IS NAMED, FIVE TIMES. Matt may install T12_7, T12_8, T12_9 or T12_10 first, so this passes only when
# the ten installed files match EXACTLY one of five known lists -- the 2026-09-30 morning set (A), T12_7's (B),
# T12_8's (C), T12_9's (D) or T12_10's (E, installed 2026-09-30, 32043e5a6) -- and it prints which one it found.
# Anything else (a mix, a sixth state) stops it before a byte moves. The tenth file is data/gear_manifest.json:
# d498cb6a in A-D (none of them installs it); T12_10 installed aa557a50; T12_11 installs 0a81b2af.
#   A  installed 2026-09-30: knight bf23c13e, character b3b62c63, the D2 GLBs (nb-body 07ccabd6)
#   B  T12_7 (attack_lab/staged/t12_guard/install.sh): knight ef8ebfb4, character bfaf4997,
#      nb-body 8c5b43d7 and the T12_2 mount pieces
#   C  T12_8 (attack_lab/staged/t12_8/install.sh): knight ea761ba8, character b676c2a3,
#      nb-body 8a59acf9 and the same six pieces
#   D  T12_9 (attack_lab/staged/t12_9/install.sh): knight ea761ba8, character b676c2a3,
#      nb-body 91e3c4f8 and the same six pieces
#   E  T12_10 (attack_lab/staged/t12_10/install.sh): knight fb35d9d0, character 45d757b5,
#      nb-body eb8a3837, the same six pieces, gear_manifest aa557a50
# THE SET:
#   knight.gd          86141f65  = over T12_10's fb35d9d0, three patches in order (attack_lab/tools/):
#                                  arm_layer_declared_patch.py -- the shield arm layer's filter is its DECLARED bone set
#                                    (shield_carry_L's rest-valued shoulder and wrist tracks, which a runtime import drops,
#                                    can no longer fall out of it; identical filter and pose under the editor import);
#                                  strike_trail_patch.py -- THE STRIKE TRAIL (a brushed stroke behind the weapon's edge
#                                    through each strike's active swing, faded over 0.15 s after it; T12_11b: a two-tone --
#                                    a shade body in the painter's shadow hue under a pale edge -- so it reads on the snow);
#                                  strike_hold_release_patch.py -- a strike listed in strike_release.from_swing_end is
#                                    released from its swing-end pose HELD (the re-cut slash's follow-through would put
#                                    the axe through his head 11 ms after its swing)
#   character.json     ca2ce1ca  = T12_10's 45d757b5 + strike_trail (the two-tone style), strike_release at_s.attack 0.708333
#                                  (re-derived on the re-cut; was 0.75), over_s 0.16 (was 0.08) and from_swing_end {attack: 0.16},
#                                  clip_px_s fallbacks at the new speeds
#   gear_manifest.json 0a81b2af  = nb_d2/export_staging/T12_11_trails: T12_10's with locomotion_in_place speeds by the
#                                  SCENE's foot-lock rule (run_armed 3.5451, strafe_L 0.6976, strafe_R 0.2896 m/s; were
#                                  3.2749, 0.7237, 0.3100) and the attack's provenance; 48_manifest_lint 0 mismatches
#   nb-body.glb        3e32a9fc  = nb_d2/export_staging/T12_11_trails: T12_10's body with ONE clip changed -- attack, re-cut
#                                  on nbt_attack.glb's own 30 fps keys (55_clip_graft) with its weapon_r channel re-solved
#                                  (weapon_channel_solve.gd STRIKES, reshaped by 61_strike_ramp.py); 24 clips byte-identical
#   six pieces                   = the T12_2 mount set (unchanged since T12_7)
# AND ONE SETTING, NOT A FILE COPY: models/gear/nb-body.glb.import gets the editor importer's animation optimizer OFF
#   (_subresources {} -> nodes/PATH:AnimationPlayer/optimizer/enabled false), so the clips the scene plays are the file's own
#   keys (the re-cut slash: 4.17 deg -> 0.000). Edited in place -- its uid and everything else kept -- and md5-checked
#   before (fb0e47c5) and after (9002fe85). Rollback: put `_subresources={}` back and re-import.
# ROLLBACK to E: staged/t12_10/{knight.gd,character.json} + nb_d2/export_staging/T12_10_strafes/ (nb-body.glb,
#          gear_manifest.json and the six pieces); to A-D as staged/t12_10/install.sh lists them, and
#          data/gear_manifest.json back to d498cb6a (cliffside3d/godot/data/gear_manifest.json at ff29a8819).
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/t12_11
GL=$B/nb_d2/export_staging/T12_11_trails
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/t12_11_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
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
PRE_E=(fb35d9d0846ea0d5f4968fe6738eeb94 45d757b57395717ecb91560d1f38b0be eb8a3837229ac59d39097a073da2f04e
       d7762e1b40dc37a238d9da761cf4ec95 5254292e1d894902a60f4749c3cc7abb d1fe5c22eb60be92dc26cc1fff21a802
       185ca9f74af564da3f2443195c0c030f 54669c6f2298950c9dc0ffcd8d936f70 cdf1c9e12a521531e79ee24f8c1a1540
       aa557a50014b8a758f05083db5925c5b)

echo "== 1 pre-state: the ten installed files against the five known lists"
# (bash 3.2, macOS's /bin/bash: no namerefs -- all five lists counted in one pass)
NA=0; NB=0; NC=0; ND=0; NE=0; TABLE=""
for i in "${!FILES[@]}"; do
  got=$(md5 -q "$C/${FILES[$i]}" 2>/dev/null || echo MISSING)
  [ "$got" = "${PRE_A[$i]}" ] && NA=$((NA + 1))
  [ "$got" = "${PRE_B[$i]}" ] && NB=$((NB + 1))
  [ "$got" = "${PRE_C[$i]}" ] && NC=$((NC + 1))
  [ "$got" = "${PRE_D[$i]}" ] && ND=$((ND + 1))
  [ "$got" = "${PRE_E[$i]}" ] && NE=$((NE + 1))
  TABLE="$TABLE   ${FILES[$i]}  $got  (A ${PRE_A[$i]:0:8}, B ${PRE_B[$i]:0:8}, C ${PRE_C[$i]:0:8}, D ${PRE_D[$i]:0:8}, E ${PRE_E[$i]:0:8})\n"
done
if [ $NE -eq ${#FILES[@]} ]; then echo "   found E: T12_10 (knight fb35d9d0, nb-body eb8a3837), $NE of ${#FILES[@]} files"
elif [ $NA -eq ${#FILES[@]} ]; then echo "   found A: the 2026-09-30 morning set (knight bf23c13e), $NA of ${#FILES[@]} files"
elif [ $NB -eq ${#FILES[@]} ]; then echo "   found B: T12_7 (knight ef8ebfb4), $NB of ${#FILES[@]} files"
elif [ $NC -eq ${#FILES[@]} ]; then echo "   found C: T12_8 (knight ea761ba8, nb-body 8a59acf9), $NC of ${#FILES[@]} files"
elif [ $ND -eq ${#FILES[@]} ]; then echo "   found D: T12_9 (knight ea761ba8, nb-body 91e3c4f8), $ND of ${#FILES[@]} files"
else printf "$TABLE"; fail "the installed files match none of A ($NA), B ($NB), C ($NC), D ($ND) or E ($NE) of ${#FILES[@]} exactly"
fi
chk() { local f=$1 want=$2; local got; got=$(md5 -q "$f") || fail "missing $f"; [ "$got" = "$want" ] || fail "$f is $got, want $want"; }
chk $ST/knight.gd 86141f65fec86dfb4b9f9ca296e93218
chk $ST/character.json ca2ce1ca12c1c99fd546d5c35768b099
chk $GL/gear_manifest.json 0a81b2afbda88a518b882a90dbecf771
chk $GL/nb-body.glb 3e32a9fc7c9bcb5f12449c2b5bc927d6
chk $GL/axe.glb d7762e1b40dc37a238d9da761cf4ec95
chk $GL/bracers.glb 5254292e1d894902a60f4749c3cc7abb
chk $GL/byrnie.glb d1fe5c22eb60be92dc26cc1fff21a802
chk $GL/helmet.glb 185ca9f74af564da3f2443195c0c030f
chk $GL/mantle.glb 54669c6f2298950c9dc0ffcd8d936f70
chk $GL/shield.glb cdf1c9e12a521531e79ee24f8c1a1540
echo "   staged sources ok"
IMP=$C/models/gear/nb-body.glb.import
IMP_PRE=fb0e47c5d432c4fdd26ca08fd1486911; IMP_POST=9002fe85b0f6722699f6270bbbfb1d30
got=$(md5 -q $IMP) || fail "missing $IMP"
if [ "$got" = "$IMP_POST" ]; then echo "   nb-body.glb.import: optimizer already off ($got)"
elif [ "$got" = "$IMP_PRE" ]; then echo "   nb-body.glb.import: $got, the optimizer on (default) -- will be turned off"
else fail "$IMP is $got: neither the known default ($IMP_PRE) nor the optimizer-off form ($IMP_POST)"
fi
[ $DRY -eq 1 ] && { echo "== DRY RUN: pre-state and sources verified; nothing copied"; exit 0; }

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd 86141f65fec86dfb4b9f9ca296e93218
inst $ST/character.json $C/data/character.json ca2ce1ca12c1c99fd546d5c35768b099
inst $GL/gear_manifest.json $C/data/gear_manifest.json 0a81b2afbda88a518b882a90dbecf771
inst $GL/nb-body.glb $C/models/gear/nb-body.glb 3e32a9fc7c9bcb5f12449c2b5bc927d6
inst $GL/axe.glb $C/models/gear/axe.glb d7762e1b40dc37a238d9da761cf4ec95
inst $GL/bracers.glb $C/models/gear/bracers.glb 5254292e1d894902a60f4749c3cc7abb
inst $GL/byrnie.glb $C/models/gear/byrnie.glb d1fe5c22eb60be92dc26cc1fff21a802
inst $GL/helmet.glb $C/models/gear/helmet.glb 185ca9f74af564da3f2443195c0c030f
inst $GL/mantle.glb $C/models/gear/mantle.glb 54669c6f2298950c9dc0ffcd8d936f70
inst $GL/shield.glb $C/models/gear/shield.glb cdf1c9e12a521531e79ee24f8c1a1540
if [ "$(md5 -q $IMP)" = "$IMP_PRE" ]; then
  python3 - "$IMP" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
assert s.count('_subresources={}\n') == 1, "the import's _subresources line is not the default"
s = s.replace('_subresources={}\n', '_subresources={\n"nodes": {\n"PATH:AnimationPlayer": {\n"optimizer/enabled": false\n}\n}\n}\n')
open(p + '.tmp_install', 'w').write(s)
PYEOF
  mv $IMP.tmp_install $IMP
fi
got=$(md5 -q $IMP); [ "$got" = "$IMP_POST" ] || fail "$IMP is $got after the edit, want $IMP_POST"
echo "   nb-body.glb.import  $got  ok (animation optimizer off)"

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

echo "== 6 the strikes in the painted Barrow, play camera, play speed (the installed scene; frames straight to ffmpeg)"
python3 $LOCK C-9 -- $GODOT --path $C --resolution 640x360 --fixed-fps 60 --script $B/attack_lab/t12/godot/tools/film_trails_scene.gd -- \
  --out "$DEST" --tag barrow_strikes_installed_t12_11 --hold 1 --label "INSTALLED -- T12_11" > $S/strikes.log 2>&1
grep -aE "^\[scene\]|SCRIPT ERROR|WATCHDOG" $S/strikes.log | cut -c1-200
echo "== done"
