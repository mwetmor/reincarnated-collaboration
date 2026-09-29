#!/bin/zsh
# T10 Barrow paint driver (conductor tooling): two groups via wave.sh, with a disk guard before each group (R-C9-70: pause below 42 GiB).
D=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/conductor_scripts
S=$HOME/astra-burst/logs/C-9; mkdir -p $S; LOG=$S/t10_drive.log
G=("T10P-A:GENERATE T10P-B:GENERATE T10P-C:GENERATE T10P-D:GENERATE T10P-E:GENERATE T10T-bark:GENERATE"
   "T10T-snow:GENERATE T10T-path:GENERATE T10T-rock:GENERATE T10T-ice:GENERATE T10T-heather:GENERATE")
i=0
for grp in "${G[@]}"; do
  i=$((i+1))
  until [ $(df -g /System/Volumes/Data | tail -1 | awk '{print $4}') -ge 42 ]; do echo "$(date -u +%FT%TZ) DISK GUARD: waiting (<42 GiB)" >> $LOG; sleep 120; done
  echo "$(date -u +%FT%TZ) GROUP $i START $grp" >> $LOG
  zsh $D/wave.sh t10_g$i ${=grp}
  echo "$(date -u +%FT%TZ) GROUP $i DONE" >> $LOG
done
echo "$(date -u +%FT%TZ) DRIVE DONE" >> $LOG
