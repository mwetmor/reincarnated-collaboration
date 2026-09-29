#!/bin/bash
# film2.sh before|after -- task 1 (idle + strikes from idle) and task 2 (block), quarter speed.
# BEFORE = promoted GLB + HEAD knight.gd/character.json; AFTER = staged A GLB + staged candidates.
MODE=$1
R=/Users/admin/Games/reincarnated-collaboration
LAB=$R/astra_test_01/burst/runs/C-9/attack_lab
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/drax-atk/film2
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
LOCK=$R/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
C=astra_test_01/burst/runs/C-9/cliffside3d/godot
export LAB_WATCHDOG_S=900
mkdir -p $S "$DEST"; cd $LAB
if [ "$MODE" = before ]; then
  cp $R/astra_test_01/burst/runs/C-9/nb_d2/export/nb-body.glb godot/models/gear/nb-body.glb
  git -C $R show HEAD:$C/scripts/knight.gd > godot/scripts/knight.gd
  git -C $R show HEAD:$C/data/character.json > godot/data/character.json
else
  cp $R/astra_test_01/burst/runs/C-9/nb_d2/export_staging/A_damped/nb-body.glb godot/models/gear/nb-body.glb
  cp staged/knight.gd godot/scripts/knight.gd
  cp staged/character.json godot/data/character.json
fi
echo "$MODE: glb $(md5 -q godot/models/gear/nb-body.glb)  knight $(md5 -q godot/scripts/knight.gd)"
python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot --path godot --headless --import > $S/imp_$MODE.txt 2>&1
for spec in "1 idle idle" "1 slash idle" "1 bash idle" "2 block idle" "2 block run"; do
  set -- $spec; T=$1; ACT=$2; FROM=$3
  FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}'); [ "$FREE" -lt 42 ] && { echo "STOP: ${FREE} GiB"; exit 3; }
  NAME="task${T}_${MODE}_${ACT}"; [ "$ACT" != idle ] && NAME="${NAME}_from_${FROM}"
  O=$S/$NAME
  python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot --path godot --resolution 640x360 --script tools/lab.gd -- \
    --action=$ACT --from=$FROM --rung=R6 --film --out=$O "--label=TASK $T $(echo $MODE | tr a-z A-Z)   $ACT$( [ $ACT != idle ] && echo " from $FROM")   QUARTER SPEED" > $O.log 2>&1
  N=$(ls $O/frames 2>/dev/null | wc -l | tr -d ' ')
  ffmpeg -v error -y -framerate 24 -i $O/frames/f_%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$DEST/$NAME.mp4"
  if [ -s "$DEST/$NAME.mp4" ] && [ "$N" -gt 0 ]; then find $O/frames -name 'f_*.jpg' -delete; else echo "  KEPT frames for $NAME"; fi
  echo "  $NAME: $N frames"
done
