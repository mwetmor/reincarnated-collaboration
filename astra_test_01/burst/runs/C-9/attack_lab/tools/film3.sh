#!/bin/bash
# film3.sh off|on -- foot lock before/after: slash, chop, bash, block from idle and from a run,
# quarter speed, play | side camera. Same code both ways; only LAB_FOOTLOCK differs.
MODE=$1
R=/Users/admin/Games/reincarnated-collaboration
LAB=$R/astra_test_01/burst/runs/C-9/attack_lab
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/drax-atk/film3
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
LOCK=$R/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
export LAB_WATCHDOG_S=1200
export LAB_FOOTLOCK=$([ "$MODE" = on ] && echo 1 || echo 0)
TAG=$([ "$MODE" = on ] && echo after || echo before)
mkdir -p $S "$DEST"; cd $LAB
echo "$MODE: glb $(md5 -q godot/models/gear/nb-body.glb) knight $(md5 -q godot/scripts/knight.gd) foot_lock $(md5 -q godot/scripts/foot_lock.gd)"
for act in slash chop bash block; do for from in idle run; do
  FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); [ "$FREE" -lt 42 ] && { echo "STOP: ${FREE} GiB"; exit 3; }
  NAME="footlock_${TAG}_${act}_from_${from}"; O=$S/$NAME
  python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot --path godot --resolution 640x360 --script tools/lab.gd -- \
    --action=$act --from=$from --rung=R6 --film --out=$O "--label=FOOT LOCK $(echo $MODE | tr a-z A-Z)   $act from $from   QUARTER SPEED" > $O.log 2>&1
  N=$(ls $O/frames 2>/dev/null | wc -l | tr -d ' ')
  ffmpeg -v error -y -framerate 24 -i $O/frames/f_%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/$NAME.mp4"
  if [ -s "$DEST/$NAME.mp4" ] && [ "$N" -gt 0 ]; then find $O/frames -name 'f_*.jpg' -delete; else echo "  KEPT frames for $NAME"; fi
  echo "  $NAME: $N frames"
done; done
