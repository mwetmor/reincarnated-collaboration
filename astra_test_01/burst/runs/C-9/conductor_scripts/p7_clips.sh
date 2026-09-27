#!/bin/zsh
# P7: fire the remaining idle/walk clips, 4 at a time; log to ~/astra-burst/logs/C-9/p7_clips.log
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; L=$HOME/astra-burst/logs/C-9/p7_clips.log
cells=(SW_idle SW_walk W_idle W_walk NW_idle NW_walk N_idle N_walk NE_idle NE_walk E_idle E_walk SE_idle SE_walk)
i=1
while [ $i -le ${#cells} ]; do
  for j in 0 1 2 3; do k=$((i+j)); [ $k -le ${#cells} ] || break; c=${cells[$k]}; d=${c%%_*}
    zsh $B/runs/C-9/conductor_scripts/grok_clip.sh $c $B/runs/C-9/artifacts/seeds/seed_$d.png "" >> $L 2>&1 & done
  wait; i=$((i+4))
done
echo "$(date -u +%FT%TZ) P7 CLIPS DONE" >> $L
