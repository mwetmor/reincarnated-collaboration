#!/bin/zsh
# drive_waves.sh <log> <size> <TYPE> <bid>... : runs sequential waves of <size>
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad
LOG=$1; N=$2; T=$3; shift 3; ids=($@); i=1
while [ $i -le ${#ids} ]; do
  batch=(); for j in $(seq $i $((i+N-1))); do [ $j -le ${#ids} ] && batch+=("${ids[$j]}:$T"); done
  $S/wave.sh $LOG $batch; i=$((i+N))
done
echo "$(date -u +%FT%TZ) DRIVE DONE" >> $S/$LOG.log
