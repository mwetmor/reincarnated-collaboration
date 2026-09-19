#!/bin/zsh
# Parallel wave runner (R-13) for Run C-7: wave.sh <logname> <id:TYPE> [...]; TOOLING must be launched alone.
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=$HOME/astra-burst/logs/C-7; mkdir -p $S; M=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c7-shared/scratchpad; mkdir -p $M   # session-independent (Gate-1 WARN-13); M = C-6's c5_*.log glob
LOG="$S/$1.log"; shift
echo "$(date -u +%FT%TZ) WAVE START: $*" | tee -a "$LOG" >> "$M/c5_c7_$(basename $LOG)"
for spec in "$@"; do
  b="${spec%%:*}"; ty="${spec##*:}"
  ( LOCK=""; [ "$ty" = "TOOLING" ] && LOCK="python3 runs/C-7/conductor_scripts/heavy_lock.py C-7 --"; $=LOCK python3 lane/run_burst.py --run C-7 --burst-id "$b" --type "$ty" --task "briefs/C-7/$b.task.json" > "$S/${b}_run.json" 2> "$S/${b}_run.err"; echo "$(date -u +%FT%TZ) END $b jsonexit=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[\"exit\"])" "$S/${b}_run.json" 2>/dev/null) $(head -c 300 "$S/${b}_run.json") ERR:$(head -c 200 "$S/${b}_run.err")" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) WAVE DONE" | tee -a "$LOG" >> "$M/c5_c7_$(basename $LOG)"
