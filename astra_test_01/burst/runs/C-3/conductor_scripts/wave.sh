#!/bin/zsh
# Parallel wave runner (R-13) for Run C-3: wave.sh <logname> <id:TYPE> [...]; TOOLING must be launched alone.
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad
LOG="$S/$1.log"; shift
echo "$(date -u +%FT%TZ) WAVE START: $*" >> "$LOG"
for spec in "$@"; do
  b="${spec%%:*}"; ty="${spec##*:}"
  ( python3 lane/run_burst.py --run C-3 --burst-id "$b" --type "$ty" --task "briefs/C-3/$b.task.json" > "$S/${b}_run.json" 2> "$S/${b}_run.err"; echo "$(date -u +%FT%TZ) END $b jsonexit=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[\"exit\"])" "$S/${b}_run.json" 2>/dev/null) $(head -c 300 "$S/${b}_run.json") ERR:$(head -c 200 "$S/${b}_run.err")" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) WAVE DONE" >> "$LOG"
