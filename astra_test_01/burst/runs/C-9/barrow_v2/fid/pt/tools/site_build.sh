#!/bin/zsh
# BV2F PT R-C9-322: the FULL-SITE BUILD (data set site_ph3, 6656 x 4096 plate), the pilot_build_rp.sh steps on fid/pt/site:
#   paint (sha check of the sea-pass painting) | ids | export | light | take | heather | bake | prep (+reeds) | lineage | guide
# Every Godot run goes through pt_godot.py (heavy lock, timeout, first script error fatal); disk >= 21 GiB before each step.
#   zsh fid/pt/tools/site_build.sh [first_step] [last_step]
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; T=$FID/pt/tools; P=$FID/pt/site; V=$FID/v1tools; GP=$C9/barrow_full/godot
G=/Applications/Godot.app/Contents/MacOS/Godot
pg() { python3 $T/pt_godot.py "$@"; }
export BV2F_VARIANT=art BV2F_UNGROUP=1 BV2F_PILOT=site_ph3 PT_BUILD_DIR=pt/site
PAINT_SHA=901305202936814123d6cea0f9e2137ac4f71e3f1e05c9df0aa08018219e63c1   # R-C9-332: the r332 painting (r328: 3fc04a7d0f63; r321: 3201ad8a9c64)
echo "site build | pilot $BV2F_PILOT | dir $P"
STEPS=(paint ids export light take heather bake prep lineage guide)
FIRST=${1:-paint}; LAST=${2:-guide}; go=0
step() { echo "=== $1 $(date -u +%T)"; }
fail() { echo "HALT at step $1 (rc $2)"; exit 1; }
for s in $STEPS; do
  [ "$s" = "$FIRST" ] && go=1; [ $go -eq 1 ] || continue
  F_=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); [ $F_ -ge 21 ] || { echo "HALT: disk ${F_} GiB < 21 before $s"; exit 9; }
  step $s; echo "disk ${F_} GiB"
  case $s in
    paint)
      python3 -c "import hashlib,sys;s=hashlib.sha256(open('$P/painting.png','rb').read()).hexdigest();print('painting',s[:12]);sys.exit(0 if s=='$PAINT_SHA' else 1)" || fail $s 7 ;;
    ids)
      mkdir -p $P/ids_built
      pg --log $P/ids_built/capture.log --timeout-s 900 -- env HEAVY_LOCK=$T/lock_held.py bash $V/godot_run.sh $GP tierB/barrow_full/godot/tools/capture_ids.gd -- --out $P/ids_built --frame-grid $P/frame_grid.site.json || fail $s $?
      cp $P/ids_built/ids.png $P/ids_built.png ;;
    export)
      mkdir -p $P/work $P/root/work/meshes
      python3 $T/pilot_visible_ids.py > $P/work/ids_visible.txt || fail $s $?
      pg --log $P/work/export.log --timeout-s 900 -- $G --path $GP --resolution 640x360 --script res://tools/bv2f/pt_export_meshes.gd -- --out $P/root/work/meshes --ids $P/work/ids_visible.txt || fail $s $?
      (cd $P/root/work/meshes && ls *.json | sed 's/\.json$//' | sort) > $P/work/real_ids.txt
      echo "real models: $(wc -l < $P/work/real_ids.txt)" ;;
    light)
      mkdir -p $P/root/work/light
      pg --log $P/root/work/light/capture.log --timeout-s 900 -- $G --path $GP --resolution 640x360 --script res://tools/bv2f/pt_capture_light.gd -- --out $P/root/work/light || fail $s $? ;;
    take)
      python3 $T/bv2f_take.py --config $P/fe_take.json > $P/take.log 2>&1 || fail $s $? ;;
    heather)
      python3 $V/v1run.py --root $P/root tierA/barrow_full/tools/heather_instances.py > $P/heather_instances.log 2>&1 || fail $s $? ;;
    bake)
      python3 $T/pt_bake.py > $P/bake.log 2>&1 || fail $s $? ;;
    prep)
      python3 $T/bv2f_prep.py --config $P/fe_prep.json > $P/prep.log 2>&1 || fail $s $?
      python3 $T/reeds.py --config $P/fe_prep.json >> $P/prep.log 2>&1 || fail $s $? ;;
    lineage)
      python3 $T/pilot_lineage.py > $P/lineage.log 2>&1 || fail $s $? ;;
    guide)
      pg --log $P/guide_render.log --timeout-s 1200 -- $G --path $GP --resolution 640x360 --script res://tools/bv2f/pt_capture_guide.gd -- --out $P || fail $s $? ;;
  esac
  [ "$s" = "$LAST" ] && break
done
echo "=== DONE $(date -u +%T)"
