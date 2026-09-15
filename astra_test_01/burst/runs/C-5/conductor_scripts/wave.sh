#!/bin/zsh
# Parallel wave runner (R-13) for Run C-5: wave.sh <logname> <id:TYPE> [...]; TOOLING must be launched alone.
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/3f302aea-abba-4d7f-aaef-b6efd7c3cfa9/scratchpad
LOG="$S/$1.log"; shift
echo "$(date -u +%FT%TZ) WAVE START: $*" >> "$LOG"
for spec in "$@"; do
  b="${spec%%:*}"; ty="${spec##*:}"
  ( python3 lane/run_burst.py --run C-5 --burst-id "$b" --type "$ty" --task "briefs/C-5/$b.task.json" > "$S/${b}_run.json" 2> "$S/${b}_run.err"; echo "$(date -u +%FT%TZ) END $b jsonexit=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[\"exit\"])" "$S/${b}_run.json" 2>/dev/null) $(head -c 300 "$S/${b}_run.json") ERR:$(head -c 200 "$S/${b}_run.err")" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) WAVE DONE" >> "$LOG"
