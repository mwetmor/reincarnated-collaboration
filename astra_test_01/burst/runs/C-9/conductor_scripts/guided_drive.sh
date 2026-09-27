#!/bin/zsh
# guided_drive.sh <cfg.json> <logname>: paint a guided layer in dependency waves; one retry per panel then HALT.
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-9/conductor_scripts; CFG=$1
L=$HOME/astra-burst/logs/C-9; LOG=$L/$2.log; P=$(python3 -c "import json;print(json.load(open('$CFG'))['prefix'])")
cd $B; echo "$(date -u +%FT%TZ) DRIVE START $P" >> $LOG; typeset -A tried
while true; do
  ready=($(python3 $C/guided_paint.py $CFG ready))
  [ ${#ready} -eq 0 ] && { echo "$(date -u +%FT%TZ) DRIVE DONE $P" >> $LOG; break; }
  specs=()
  for k in $ready; do suf=""; [ -n "${tried[$k]}" ] && suf="-r1"
    SUF=$suf python3 $C/guided_paint.py $CFG stage $k >> $LOG 2>&1; SUF=$suf python3 $C/guided_paint.py $CFG brief $k >> $LOG 2>&1
    python3 $C/refs_guard.py briefs/C-9/$P-$k$suf.task.json >> $LOG 2>&1 || { echo "HALT H-guard $P-$k$suf" >> $LOG; exit 3; }
    specs+=("$P-$k$suf:GENERATE"); done
  zsh $C/wave.sh ${2}_w$(date +%s) ${specs[@]}
  for s in $specs; do bid=${s%%:*}; k=${${bid#$P-}%-r1}
    ex=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['exit'])" $L/${bid}_run.json 2>/dev/null); echo "$(date -u +%FT%TZ) $bid exit=$ex" >> $LOG
    if [ "$ex" != "0" ]; then [ -n "${tried[$k]}" ] && { echo "HALT: $k failed twice" >> $LOG; exit 2; }; tried[$k]=1; fi; done
done
