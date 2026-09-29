#!/bin/bash
# film.sh MODE  -- every action x start state, quarter speed, play cam | side cam, straight to MP4
MODE=$1
LAB=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/attack_lab
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad/drax-atk/film
DEST="/Users/admin/Desktop/Astra Burst Review - 2026-09-26/C-9 cliffside 3D/attack fix"
LOCK=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py
FONT=/System/Library/Fonts/Supplemental/Arial.ttf
mkdir -p "$DEST" $S
cd $LAB
for act in slash chop bash block; do for from in idle run; do
  FREE=$(df -g /System/Volumes/Data | tail -1 | awk '{print $4}')
  if [ "$FREE" -lt 42 ]; then echo "STOP: only ${FREE} GiB free"; exit 3; fi
  O=$S/${MODE}_${act}_${from}
  python3 $LOCK C-9 -- /Applications/Godot.app/Contents/MacOS/Godot --path godot --resolution 640x360 \
    --script tools/lab.gd -- --action=$act --from=$from --rung=R6 --film --out=$O \
    "--label=$(echo $MODE | tr a-z A-Z)   $act from $from   QUARTER SPEED" > $O.log 2>&1
  N=$(ls $O/frames 2>/dev/null | wc -l | tr -d ' ')
  M4="$DEST/${MODE}_${act}_from_${from}.mp4"
  ffmpeg -v error -y -framerate 24 -i $O/frames/f_%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 20 -movflags +faststart "$M4"
  # DELETE THE FRAMES ONLY IF THE MP4 EXISTS -- the first run deleted them after a failed encode
  if [ -s "$M4" ] && [ "$N" -gt 0 ]; then find $O/frames -name 'f_*.jpg' -delete; else echo "  KEPT frames: encode failed or no frames"; fi
  echo "$MODE $act from $from: $N frames -> $(du -h "$DEST/${MODE}_${act}_from_${from}.mp4" | cut -f1)"
done; done
