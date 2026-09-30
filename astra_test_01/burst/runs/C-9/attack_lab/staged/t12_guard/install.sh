#!/bin/bash
# T12 (c) -- THE AXE ARM'S GUARD, THE RECOVERY RELEASE, THE RE-SOURCED CHOP -- INSTALL.
# STAGED, NOT RUN: run by the conductor on Matt's word, at a cliffside3d window.
# Mirrors the speed-split install: pre-state check, atomic md5-verified install, re-import, both
# app builds with their launch checks, the armed Barrow walk capture. Stops at the first failure.
#   knight.gd       ef8ebfb4  = attack_lab/tools/strike_release_patch.py over
#                               attack_lab/tools/axeguard_patch.py over the installed bf23c13e
#   character.json  bfaf4997  = the installed b3b62c63 + arm_layer_armed_R (weight 0.85, block 1.0),
#                               clips_armed.idle -> idle_guard, weapon_r in upper_armed.bones,
#                               strike_release (the slash 0.75 s, the chop 0.578 s, the bash held),
#                               clips_armed.chop -> chop_overhead_92
#   nb-body.glb     8c5b43d7  = nb_d2/export_staging/T12_7_guard: the T12_2 mount rig + the guard
#                               poses + the weapon_r channel at 0.85 (T12_5) + chop_overhead_92
#                               (Meshy 92's first cut, 55_clip_graft.py) and its roll
#   six pieces                = the T12_2 mount set (weapon_r / weapon_l in every skeleton)
# ROLLBACK: staged/speed_split/{knight.gd,character.json} and the seven GLBs in
# attack_lab/t12/godot/models/gear_orig/ are the pre-state, byte for byte (md5s below).
set -uo pipefail
R=/Users/admin/Games/reincarnated-collaboration
B=$R/astra_test_01/burst/runs/C-9
C=$B/cliffside3d/godot
ST=$B/attack_lab/staged/t12_guard
GL=$B/nb_d2/export_staging/T12_7_guard
LOCK=$B/../C-7/conductor_scripts/heavy_lock.py
GODOT=/Applications/Godot.app/Contents/MacOS/Godot
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/t12_guard_install
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
mkdir -p $S
fail() { echo "HALT: $*"; exit 1; }
FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); echo "== disk ${FREE} GiB"; [ "$FREE" -ge 25 ] || fail "disk below the 25 GiB gate"

echo "== 1 pre-state: the set was built and measured on exactly these"
chk() { local f=$1 want=$2; local got; got=$(md5 -q "$f") || fail "missing $f"; [ "$got" = "$want" ] || fail "$f is $got, want $want"; }
chk $C/scripts/knight.gd bf23c13e1ac58c4dfcbf90e0a081b3ea
chk $C/data/character.json b3b62c633f9e7a05862b02cb418efd27
chk $C/models/gear/nb-body.glb 07ccabd602963548619c1e63201ab52b
chk $C/models/gear/axe.glb 960c398c08330f5a56599ad5aa96ab32
chk $C/models/gear/bracers.glb 1f2a1b147ecb2a3218876130293f140d
chk $C/models/gear/byrnie.glb bf4750af62f23c686ef807084d444c9a
chk $C/models/gear/helmet.glb 9b8421429fd25e9a6abeaf619dc56faf
chk $C/models/gear/mantle.glb 0e96a2c8a83841119e7c9067463f88d8
chk $C/models/gear/shield.glb 0eb899d48c58651a6b2632b8cf033973
chk $ST/knight.gd ef8ebfb463f039994736c86261f967ee
chk $ST/character.json bfaf499789c3fc304ff37285b7a20da8
chk $GL/nb-body.glb 8c5b43d7a415ac8b9dfd98318eac80c8
echo "   ok"

echo "== 2 install (atomic rename), md5 verified after each copy"
inst() { local src=$1 dst=$2 want=$3
  cp "$src" "$dst.tmp_install" && mv "$dst.tmp_install" "$dst"
  local got; got=$(md5 -q "$dst"); [ "$got" = "$want" ] || fail "$dst is $got, want $want"
  echo "   $(basename $dst)  $got  ok"; }
inst $ST/knight.gd $C/scripts/knight.gd ef8ebfb463f039994736c86261f967ee
inst $ST/character.json $C/data/character.json bfaf499789c3fc304ff37285b7a20da8
inst $GL/nb-body.glb $C/models/gear/nb-body.glb 8c5b43d7a415ac8b9dfd98318eac80c8
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
echo "   launch.log: SCRIPT ERROR $(grep -ac 'SCRIPT ERROR' $LB), $(grep -a 'foot_lock nodes' $LB | tail -1), $(grep -a 'axe guard layer' $LB | tail -1)"

echo "== 6 the armed Barrow walk, play camera, --fixed-fps 24"
python3 $LOCK C-9 -- $GODOT --path $C --fixed-fps 24 --resolution 640x360 --script tools/shot_barrow_armed.gd -- --out $S/walk > $S/walk.log 2>&1
grep -aE "^\[armed\]|SCRIPT ERROR|WATCHDOG" $S/walk.log | cut -c1-200
N=$(ls $S/walk/frames 2>/dev/null | wc -l | tr -d ' ')
ffmpeg -v error -y -framerate 24 -i $S/walk/frames/f_%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/barrow_walk_armed_t12_guard.mp4"
if [ -s "$DEST/barrow_walk_armed_t12_guard.mp4" ] && [ "$N" -gt 0 ]; then find $S/walk/frames -name 'f_*.jpg' -delete; echo "   $N frames -> barrow_walk_armed_t12_guard.mp4, frames deleted"; else echo "   KEPT frames: encode failed"; fi
echo "== done"
