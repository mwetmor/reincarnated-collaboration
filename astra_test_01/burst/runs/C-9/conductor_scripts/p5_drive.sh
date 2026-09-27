#!/bin/zsh
# C-9 P5 driver: paint the cliffside v4 grid in dependency waves until done or a HALT condition.
# Each wave = every chunk whose neighbours are painted; stage -> brief -> refs_guard -> wave.sh (parallel) -> check.
# A chunk whose burst is not exit 0 gets ONE retry (SUF=-r1); a second failure HALTs the driver (lane two-attempt rule).
B=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst; C=$B/runs/C-9/conductor_scripts
L=$HOME/astra-burst/logs/C-9; mkdir -p $L; LOG=$L/p5_drive.log
cd $B
echo "$(date -u +%FT%TZ) P5 DRIVE START" >> $LOG
typeset -A tried
while true; do
  ready=($(python3 $C/grid_paint_c9.py ready))
  [ ${#ready} -eq 0 ] && { echo "$(date -u +%FT%TZ) P5 DRIVE DONE (nothing ready)" >> $LOG; break; }
  specs=()
  for k in $ready; do
    suf=""; [ -n "${tried[$k]}" ] && suf="-r1"
    SUF=$suf python3 $C/grid_paint_c9.py stage $k >> $LOG 2>&1
    SUF=$suf python3 $C/grid_paint_c9.py brief $k >> $LOG 2>&1
    if ! python3 $C/refs_guard.py briefs/C-9/CS9-$k$suf.task.json >> $LOG 2>&1; then
      echo "$(date -u +%FT%TZ) HALT H-guard on CS9-$k$suf" >> $LOG; exit 3; fi
    specs+=("CS9-$k$suf:GENERATE")
  done
  wl="p5_w$(date +%s)"
  zsh $C/wave.sh $wl ${specs[@]}
  for s in $specs; do
    bid=${s%%:*}; k=${${bid#CS9-}%-r1}
    ex=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['exit'])" $L/${bid}_run.json 2>/dev/null)
    echo "$(date -u +%FT%TZ) $bid exit=$ex" >> $LOG
    if [ "$ex" != "0" ]; then
      if [ -n "${tried[$k]}" ]; then echo "$(date -u +%FT%TZ) HALT: $k failed twice" >> $LOG; exit 2; fi
      tried[$k]=1
    fi
  done
done
