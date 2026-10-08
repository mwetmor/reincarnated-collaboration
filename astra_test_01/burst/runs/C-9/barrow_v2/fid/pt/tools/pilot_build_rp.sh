#!/bin/zsh
# BV2F PT R-C9-232: the pilot REPAINT, painted -> built. Steps (any failure = stop and report the step):
#   stitch | ids | export | light | take | heather | bake | prep (+reeds) | lineage | guide render | stills (+ class masks)
# Every Godot run goes through pt_godot.py (heavy lock, timeout from lock acquisition, first script error fatal, 16 MB log cap);
# frozen v1 GD tools through godot_run.sh with HEAVY_LOCK=lock_held.py (pt_godot already holds the lock).
#   zsh fid/pt/tools/pilot_build_rp.sh [first_step]
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; T=$FID/pt/tools; P=$FID/pt/pilot; V=$FID/v1tools; GP=$C9/barrow_full/godot
G=/Applications/Godot.app/Contents/MacOS/Godot
pg() { python3 $T/pt_godot.py "$@"; }
CFG=$P/cfg_bv2a_pilot.json
export BV2F_VARIANT=art BV2F_UNGROUP=1 BV2F_PILOT=rp2
STEPS=(stitch ids export light take heather bake prep lineage guide stills)
FIRST=${1:-stitch}; go=0
step() { echo "=== $1 $(date -u +%T)"; }
fail() { echo "HALT at step $1 (rc $2)"; exit 1; }
for s in $STEPS; do
  [ "$s" = "$FIRST" ] && go=1; [ $go -eq 1 ] || continue
  step $s
  case $s in
    stitch)
      # R-C9-242: the Tier-B stitch (DEV-23 low-frequency tone match at the pasted-context boundary)
      python3 $V/tierB/conductor_scripts/guided_stitch.py $CFG $P/painting.png $P/painting_preview.jpg > $P/stitch.log 2>&1 || fail $s $?
      python3 $T/pilot_stitch_record.py || fail $s $?
      # PH P5 (seams): every internal join's overlap MAD must be <= 13.09 (PH threshold; pilot 2 failed 0_1|0_2 at 13.86)
      python3 -c "import json,sys;m=json.load(open('$P/stitch_record.json'))['overlap_mad'];bad={k:v for k,v in m.items() if v>13.09};print('P5 joins over 13.09:',bad or 'none');sys.exit(1 if bad else 0)" || fail $s 5 ;;
    ids)
      mkdir -p $P/ids_built
      pg --log $P/ids_built/capture.log --timeout-s 900 -- env HEAVY_LOCK=$T/lock_held.py bash $V/godot_run.sh $GP tierB/barrow_full/godot/tools/capture_ids.gd -- --out $P/ids_built --frame-grid $P/frame_grid.pilot.json || fail $s $?
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
      python3 $T/bv2f_take.py > $P/take.log 2>&1 || fail $s $? ;;
    heather)
      python3 $V/v1run.py --root $P/root tierA/barrow_full/tools/heather_instances.py > $P/heather_instances.log 2>&1 || fail $s $? ;;
    bake)
      python3 $T/pt_bake.py > $P/bake.log 2>&1 || fail $s $? ;;
    prep)
      python3 $T/bv2f_prep.py > $P/prep.log 2>&1 || fail $s $?
      python3 $T/reeds.py >> $P/prep.log 2>&1 || fail $s $? ;;
    lineage)
      python3 $T/pilot_lineage.py > $P/lineage.log 2>&1 || fail $s $? ;;
    guide)
      pg --log $P/guide_render.log --timeout-s 1200 -- $G --path $GP --resolution 640x360 --script res://tools/bv2f/pt_capture_guide.gd -- --out $P || fail $s $? ;;
    stills)
      mkdir -p $FID/pt/pilot_stills
      python3 -c "import json;d=json.load(open('$FID/ph/pilot_p11_spec.json'));json.dump({'_what':'the 12 P11 views (fid/ph/pilot_p11_spec.json stills)','views':[{k:v[k] for k in ('name','knight_uv','facing','camera_centre_ground_uv')} for v in d['stills']]},open('$P/stills_views.json','w'),indent=1)" || fail $s $?
      pg --log $FID/pt/pilot_stills/capture.log --timeout-s 1800 -- $G --path $GP --resolution 640x360 --script res://tools/bv2f/pt_pilot_stills.gd -- --spec $P/stills_views.json --out $FID/pt/pilot_stills || fail $s $?
      python3 $T/pilot_class_masks.py $FID/pt/pilot_stills > $FID/pt/pilot_stills/class_masks.log 2>&1 || fail $s $? ;;
  esac
done
echo "=== DONE $(date -u +%T)"
