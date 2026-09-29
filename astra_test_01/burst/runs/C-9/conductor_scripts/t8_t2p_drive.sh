#!/bin/zsh
# Sequential group driver (conductor tooling): fires the R-C9-66/69 paint set in groups of 5 via wave.sh; one group at a time.
D=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/conductor_scripts
S=$HOME/astra-burst/logs/C-9; mkdir -p $S; LOG=$S/t8_t2p_drive.log
G=(
 "NB-1:GENERATE T5P-A:GENERATE T2P-walk-S:GENERATE T2P-walk-SW:GENERATE T2P-walk-W:GENERATE"
 "T2P-walk-NW:GENERATE T2P-walk-N:GENERATE T2P-walk-NE:GENERATE T2P-idle-S:GENERATE T2P-idle-SW:GENERATE"
 "T2P-idle-W:GENERATE T2P-idle-NW:GENERATE T2P-idle-N:GENERATE T2P-idle-NE:GENERATE T2P-run-S:GENERATE"
 "T2P-run-SW:GENERATE T2P-run-W:GENERATE T2P-run-NW:GENERATE T2P-run-N:GENERATE T2P-run-NE:GENERATE"
 "T2P-attack-S:GENERATE T2P-attack-SW:GENERATE T2P-attack-W:GENERATE T2P-attack-NW:GENERATE T2P-attack-N:GENERATE T2P-attack-NE:GENERATE"
)
i=0
for grp in "${G[@]}"; do
  i=$((i+1)); echo "$(date -u +%FT%TZ) GROUP $i START $grp" >> $LOG
  zsh $D/wave.sh t8_t2p_g$i ${=grp}
  echo "$(date -u +%FT%TZ) GROUP $i DONE" >> $LOG
done
echo "$(date -u +%FT%TZ) DRIVE DONE" >> $LOG
