#!/bin/bash
# BV2F R-C9-180: positive control T1-T3 at pin f1aa715ac and at HEAD, each in its own APFS clone.
SP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/df21e264-6571-4d04-96ee-b8e2bd6d97fa/scratchpad
O=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/barrow_full
HL=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
G=/Applications/Godot.app/Contents/MacOS/Godot
gate() { FREE=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}'); if [ "$FREE" -lt 21 ]; then echo "HALT: ${FREE} GiB free < 21"; exit 9; fi; }
for tag in pin head; do
  W=$SP/pc5_$tag/C-9; mkdir -p $W $SP/pc5_$tag/moved_out; cp -Rc $O $W/; BF=$W/barrow_full
  if [ $tag = pin ]; then for p in godot/data/bv2f godot/scripts/bv2f godot/tools/bv2f $(cd $BF && ls godot/scenes/bv2f_*.tscn); do mkdir -p $SP/pc5_pin/moved_out/$(dirname $p); mv $BF/$p $SP/pc5_pin/moved_out/$p; done; fi
  OUT=$SP/pc5_$tag/out; mkdir -p $OUT $BF/work/overlay_new
  # T1
  mv $BF/take/ids $BF/take/ids_v1orig; mkdir -p $BF/take/ids
  (cd $BF/godot && gate; python3 $HL C-9 -- $G --path $BF/godot --resolution 640x360 --script tools/capture_ids.gd -- --out $BF/take/ids) > $OUT/t1.log 2>&1; echo "$tag T1 rc=$?"
  (cd $BF && python3 tools/take_from_paint.py) > $OUT/t1b.log 2>&1; echo "$tag T1b rc=$?"
  # T2
  [ -d $BF/work/overlay ] && mv $BF/work/overlay $SP/pc5_$tag/moved_out/work_overlay_old; mv $BF/work/overlay_new $BF/work/overlay
  (cd $BF/godot && gate; python3 $HL C-9 -- $G --path $BF/godot --resolution 640x360 --script tools/mini_overlay.gd -- --out $BF/work/overlay --ids ring_p155,door_lintel,grave_marker_W,fallen_tree_log_A --bakes $BF/work/bakes) > $OUT/t2.log 2>&1; echo "$tag T2 rc=$?"
  (cd $BF && python3 tools/mini_overlay.py) > $OUT/t2b.log 2>&1; echo "$tag T2b rc=$?"
  # T3
  (cd $BF/godot && gate; python3 $HL C-9 -- $G --path $BF/godot --resolution 640x360 --script tools/capture_painted.gd -- --out $OUT/painted --guide --variants inpainted,as_painted) > $OUT/t3.log 2>&1; echo "$tag T3 rc=$?"
  (cd $BF && python3 tools/overlay_check.py --capture $OUT/painted --out $OUT) > $OUT/t3b.log 2>&1; echo "$tag T3b rc=$?"
  (cd $BF && python3 tools/paint_world_prep.py) > $OUT/t3c.log 2>&1; echo "$tag T3c rc=$?"
done
echo ALLDONE
