#!/bin/zsh
# C-7 Packet 106 chain: wait for PACK v45 -> stage cliffside_v45 -> headless import -> A/B captures (A=kit index 11, B=kit index 18) -> sheets + clips -> purge.
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; L=$HOME/astra-burst/logs/C-7; G=/Applications/Godot.app/Contents/MacOS/Godot
until grep -q "WAVE DONE" $L/c7_pack_v45.log 2>/dev/null; do sleep 5; done; tail -2 $L/c7_pack_v45.log | cut -c1-200
ls $B/runs/C-7/artifacts/CS-pack-v45/godot/project.godot || { echo "PACK v45 produced no project"; exit 1; }
rm -rf $B/runs/C-7/cliffside_v45; cp -R $B/runs/C-7/artifacts/CS-pack-v45/godot $B/runs/C-7/cliffside_v45
P=$B/runs/C-7/cliffside_v45; O=$B/runs/C-7/t3/AB-v45; mkdir -p $O
python3 $B/runs/C-7/conductor_scripts/heavy_lock.py C-7 -- $G --headless --path $P --import > $O/import_v45.log 2>&1; echo "import exit $? errors $(grep -c ERROR $O/import_v45.log)"
cp $B/runs/C-7/conductor_scripts/probe_cast_ab.gd $B/runs/C-7/conductor_scripts/probe_events.gd $P/
# A/B event traces for the record (one cast each, east)
for spec in A:11 B:18; do IFS=: read arm k <<< "$spec"; KIT_CYCLES=$k FACE=move_right python3 $B/runs/C-7/conductor_scripts/heavy_lock.py C-7 -- $G --headless --path $P --script res://probe_events.gd > $O/events_${arm}_E.log 2>&1; echo "events $arm exit $?"; done
# rendered captures: east x3 casts (accumulating scorches) and west x1 (walkable clamp), both arms
for spec in A:11:E:move_right:3:1020 B:18:E:move_right:3:1020 A:11:W:move_left:1:480 B:18:W:move_left:1:480; do
  IFS=: read arm k tag face casts frames <<< "$spec"; D=$O/${arm}_$tag; mkdir -p $D
  PROBE_OUT=$D KIT_CYCLES=$k START_X=3760 START_Y=640 FACE=$face CASTS=$casts CAPTURE_FRAMES=$frames python3 $B/runs/C-7/conductor_scripts/heavy_lock.py C-7 -- $G --rendering-method gl_compatibility --path $P --script res://probe_cast_ab.gd > $D/cast.log 2>&1
  echo "${arm}_$tag exit $? $(tail -1 $D/cast.log | cut -c1-120)"
done
cd $B && python3 - <<'PY'
import glob, numpy as np
from PIL import Image, ImageDraw
O='runs/C-7/t3/AB-v45'
for run in ('A_E','B_E','A_W','B_W'):
    fr=sorted(glob.glob(f'{O}/{run}/cast_*.png'))
    if not fr: print(run,'no frames'); continue
    n=len(fr); sel=[3,6,9,14,22,36,60,100,140,180,240,300,360,420,470,n-1] if n>480 else [3,6,9,14,22,36,60,100,140,180,220,n-1]
    tiles=[]
    for i in sel:
        i=min(max(i,0),n-1); im=Image.open(fr[i]).convert('RGB').crop((960-640,540-380,960+640,540+380)); d=ImageDraw.Draw(im); d.rectangle((0,0,200,18),fill=(0,0,0)); d.text((6,4),f'{run} f{i*2} t{i*2/60:.1f}s',fill=(255,255,255)); tiles.append(im.resize((480,285)))
    cols=4; rows=(len(tiles)+cols-1)//cols; sheet=Image.new('RGB',(480*cols,285*rows),(20,20,20))
    for k,t in enumerate(tiles): sheet.paste(t,((k%cols)*480,(k//cols)*285))
    sheet.save(f'{O}/{run}_sheet.png'); print(run,'frames',n)
PY
for run in A_E B_E A_W B_W; do D=$O/$run; ffmpeg -v quiet -y -framerate 30 -i $D/cast_%04d.png -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -crf 22 $O/${run}_realtime.mp4; ffmpeg -v quiet -y -framerate 10 -i $D/cast_%04d.png -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -crf 22 $O/${run}_third_speed.mp4 && rm -f $D/cast_*.png; done
echo chain-done
