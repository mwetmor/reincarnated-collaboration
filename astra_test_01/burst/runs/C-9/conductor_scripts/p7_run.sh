#!/bin/zsh
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; L=$HOME/astra-burst/logs/C-9/p7_run.log
typeset -A SEED; SEED=(S seed_S_v2 SW seed_SW_v2 W seed_W NW seed_NW N seed_N NE seed_NE E seed_E SE seed_SE)
dirs=(S SW W NW N NE E SE); i=1
while [ $i -le 8 ]; do for j in 0 1 2 3; do k=$((i+j)); d=${dirs[$k]}
  zsh $B/runs/C-9/conductor_scripts/grok_clip.sh ${d}_run $B/runs/C-9/artifacts/seeds/${SEED[$d]}.png "" >> $L 2>&1 & done; wait; i=$((i+4)); done
echo "$(date -u +%FT%TZ) RUN CLIPS DONE" >> $L
