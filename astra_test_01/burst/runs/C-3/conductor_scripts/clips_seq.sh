#!/bin/zsh
# Sequential clip runner with the § 8 halt counter: clips_seq.sh <log> <cell:still> ...
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad
LOG="$S/$1.log"; shift; FAILS=0
for spec in "$@"; do
  cell="${spec%%:*}"; still="${spec#*:}"
  r=$($S/grok_clip.sh "$cell" "$still"); echo "$r" >> "$LOG"
  if echo "$r" | grep -q "ok=true"; then FAILS=0; else FAILS=$((FAILS+1)); fi
  if [ $FAILS -ge 3 ]; then echo "$(date -u +%FT%TZ) HALT-CANDIDATE: 3 consecutive Grok failures" >> "$LOG"; break; fi
done
echo "$(date -u +%FT%TZ) SEQ DONE" >> "$LOG"
