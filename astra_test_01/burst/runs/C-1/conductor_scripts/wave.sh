#!/bin/zsh
# Parallel wave runner (R-13): wave.sh <logname> <id:TYPE> [<id:TYPE> ...] — launches all bursts concurrently, waits for all.
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/aeac7498-ff42-4a34-aa6b-c086de5fd422/scratchpad
LOG="$S/$1.log"; shift
echo "$(date -u +%FT%TZ) WAVE START: $*" >> "$LOG"
for spec in "$@"; do
  b="${spec%%:*}"; ty="${spec##*:}"
  ( python3 lane/run_burst.py --run C-1 --burst-id "$b" --type "$ty" --task "briefs/$b.task.json" > "$S/${b}_run.json" 2> "$S/${b}_run.err"; echo "$(date -u +%FT%TZ) END $b exit=$? $(head -c 140 "$S/${b}_run.json")" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) WAVE DONE" >> "$LOG"
