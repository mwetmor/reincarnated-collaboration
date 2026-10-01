#!/bin/zsh
# R-C9-120: film frames  before | v7+A | v7+C  (same frame numbers from the three 1x films), walk and run, 2x nearest.
R=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_robe; cd $R/film
for seg in "walk 50 310 26" "run 320 490 24"; do set -- ${=seg}
  ffmpeg -loglevel error -y -i robe_before_1x.mp4 -i robe_v7A_1x.mp4 -i robe_v7C_1x.mp4 -filter_complex \
   "[0]select='between(n,$2,$3)*not(mod(n,$4))',crop=220:200:380:140[a];[1]select='between(n,$2,$3)*not(mod(n,$4))',crop=220:200:380:140[b];[2]select='between(n,$2,$3)*not(mod(n,$4))',crop=220:200:380:140[c];[a][b][c]hstack=3,scale=iw*2:ih*2:flags=neighbor,tile=2x5:padding=6:color=white" \
   -frames:v 1 $R/stills/robe_${1}_frames_before_v7A_v7C.jpg && echo $R/stills/robe_${1}_frames_before_v7A_v7C.jpg
done
ffmpeg -loglevel error -y -i robe_before_1x.mp4 -i robe_v7A_1x.mp4 -i robe_v7C_1x.mp4 -filter_complex "[0][1][2]hstack=3" -c:v libx264 -crf 20 -pix_fmt yuv420p robe_before_v7A_v7C_1x.mp4 && echo film ok
