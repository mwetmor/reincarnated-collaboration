#!/bin/zsh
# BV2F PT R-C9-384: the SITE_PH4 BUILD (6656 x 4864 = the site_ph3 plate + the 768 px north band) -- site_build.sh's steps
# on fid/pt/site4 (set up by site4_setup.py):
#   paint | ids | export | light | take | heather | bake | prep (+reeds) | lineage | guide
# bake: ONLY models whose plate reaches the band (ph4 screen rect top < 776 px, from the export) + one CONTROL model far
# from it (its ph4 bake must be byte-identical to its ph3 bake: proof that a carried-over bake is the right bake); every
# other model keeps its ph3 bake (cloned by site4_setup.py) -- their mesh and the painting under their plate are unchanged.
# Every Godot run goes through pt_godot.py (heavy lock, timeout, first script error fatal); disk >= 21 GiB before each step.
#   zsh fid/pt/tools/site4_build.sh [first_step] [last_step]
set -u
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9
FID=$C9/barrow_v2/fid; T=$FID/pt/tools; P=$FID/pt/site4; V=$FID/v1tools; GP=$C9/barrow_full/godot
G=/Applications/Godot.app/Contents/MacOS/Godot
pg() { python3 $T/pt_godot.py "$@"; }
export BV2F_VARIANT=art BV2F_UNGROUP=1 BV2F_PILOT=site_ph4 PT_BUILD_DIR=pt/site4
PAINT_SHA=$(python3 -c "import json;print(json.load(open('$FID/pt/north/final/identity.json'))['ph4_file_sha256'])")
CONTROL=crags__crags_0
echo "site4 build | pilot $BV2F_PILOT | dir $P | painting ${PAINT_SHA:0:12}"
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
      [ -f $P/painting.png ] || cp -c $FID/pt/north/final/painting_ph4_full.png $P/painting.png
      python3 -c "import hashlib,sys;s=hashlib.sha256(open('$P/painting.png','rb').read()).hexdigest();print('painting',s[:12]);sys.exit(0 if s=='$PAINT_SHA' else 1)" || fail $s 7 ;;
    ids)
      mkdir -p $P/ids_built
      pg --log $P/ids_built/capture.log --timeout-s 900 -- env HEAVY_LOCK=$T/lock_held.py bash $V/godot_run.sh $GP tierB/barrow_full/godot/tools/capture_ids.gd -- --out $P/ids_built --frame-grid $P/frame_grid.site4.json || fail $s $?
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
      python3 - $P $CONTROL <<'EOF' || fail bake-list 1
import json, os, sys
P, ctl = sys.argv[1], sys.argv[2]
M = os.path.join(P, "root/work/meshes")
ids = sorted(l.strip() for l in open(os.path.join(P, "work/real_ids.txt")) if l.strip())
prev = json.load(open(os.path.join(P, "bake_report_ph3_prev.json")))["pieces"]
band = [i for i in ids if json.load(open(os.path.join(M, i + ".json")))["screen_rect_px"][1] < 768 + 8]
new = [i for i in ids if i not in prev]
only = sorted(set(band) | set(new) | {ctl})
open(os.path.join(P, "work/bake_only.txt"), "w").write("\n".join(only) + "\n")
json.dump({"band_reaching": band, "new_models": new, "control": ctl, "rebaked": only, "carried_over": [i for i in ids if i not in only],
           "dropped_from_ph3": [i for i in prev if i not in ids]}, open(os.path.join(P, "work/bake_plan.json"), "w"), indent=1)
print("re-bake", len(only), "of", len(ids), only)
EOF
      PT_BAKE_ONLY=$P/work/bake_only.txt PT_BAKE_PREV=$P/bake_report_ph3_prev.json python3 $T/pt_bake.py > $P/bake.log 2>&1 || fail $s $?
      cmp $P/root/work/bakes/$CONTROL.png $FID/pt/site/root/work/bakes/$CONTROL.png && echo "CONTROL bake $CONTROL byte-identical to ph3" || { echo "CONTROL bake $CONTROL DIFFERS from ph3"; fail control 5; } ;;
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
