#!/bin/zsh
# Parallel wave runner (R-13) for Run C-7: wave.sh <logname> <id:TYPE> [...]; TOOLING must be launched alone.
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/4e83a458-9b8a-45f0-8e0c-8487cc714a21/scratchpad
LOG="$S/$1.log"; shift
echo "$(date -u +%FT%TZ) WAVE START: $*" >> "$LOG"
for spec in "$@"; do
  b="${spec%%:*}"; ty="${spec##*:}"
  ( LOCK=""; [ "$ty" = "TOOLING" ] && LOCK="python3 runs/C-7/conductor_scripts/heavy_lock.py C-7 --"; $=LOCK python3 lane/run_burst.py --run C-7 --burst-id "$b" --type "$ty" --task "briefs/C-7/$b.task.json" > "$S/${b}_run.json" 2> "$S/${b}_run.err"; echo "$(date -u +%FT%TZ) END $b jsonexit=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[\"exit\"])" "$S/${b}_run.json" 2>/dev/null) $(head -c 300 "$S/${b}_run.json") ERR:$(head -c 200 "$S/${b}_run.err")" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) WAVE DONE" >> "$LOG"
