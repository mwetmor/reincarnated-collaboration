#!/bin/zsh
# C-9 Phase 2 T10-2 step 2 driver (R-C9-75/86): paint the full Barrow area over its greybox, 4x4 chunks, in dependency waves.
# Each wave = every chunk whose neighbours are painted; stage -> brief -> refs_guard -> wave.sh (parallel) -> check.
# A chunk whose burst is not exit 0 gets ONE retry (SUF=-r1); a second failure HALTs (lane two-attempt rule).
# Disk guard: lane bursts are light (a few MB each), so painting may run down to 41 GiB (KC2 halts at 40); heavy work stays paused below 42.
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-9/conductor_scripts; CFG=$C/cfg_t10bf.json
L=$HOME/astra-burst/logs/C-9; mkdir -p $L; LOG=$L/t10bf_drive.log
cd $B
echo "$(date -u +%FT%TZ) T10BF DRIVE START" >> $LOG
typeset -A tried
while true; do
  until [ $(df -g /System/Volumes/Data | tail -1 | awk '{print $4}') -ge 41 ]; do echo "$(date -u +%FT%TZ) DISK GUARD: waiting (<41 GiB)" >> $LOG; sleep 120; done
  ready=($(python3 $C/guided_paint.py $CFG ready))
  [ ${#ready} -eq 0 ] && { echo "$(date -u +%FT%TZ) T10BF DRIVE DONE (nothing ready)" >> $LOG; break; }
  specs=()
  for k in $ready; do
    suf=""; [ -n "${tried[$k]}" ] && suf="-r1"
    SUF=$suf python3 $C/guided_paint.py $CFG stage $k >> $LOG 2>&1
    SUF=$suf python3 $C/guided_paint.py $CFG brief $k >> $LOG 2>&1
    if ! python3 $C/refs_guard.py briefs/C-9/T10BF-$k$suf.task.json >> $LOG 2>&1; then
      echo "$(date -u +%FT%TZ) HALT H-guard on T10BF-$k$suf" >> $LOG; exit 3; fi
    specs+=("T10BF-$k$suf:GENERATE")
  done
  wl="t10bf_w$(date +%s)"
  zsh $C/wave.sh $wl ${specs[@]}
  for s in $specs; do
    bid=${s%%:*}; k=${${bid#T10BF-}%-r1}
    ex=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['exit'])" $L/${bid}_run.json 2>/dev/null)
    echo "$(date -u +%FT%TZ) $bid exit=$ex" >> $LOG
    if [ "$ex" != "0" ]; then
      if [ -n "${tried[$k]}" ]; then echo "$(date -u +%FT%TZ) HALT: $k failed twice" >> $LOG; exit 2; fi
      tried[$k]=1
    fi
  done
done
