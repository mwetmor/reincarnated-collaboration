#!/bin/zsh
# clips_seq2.sh <log> "cell|still|suffix|extra" ... — STOPS ON THE FIRST FAILURE (R-C3-24)
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/423f7949-3b86-43e3-82bd-845c71630541/scratchpad
LOG="$S/$1.log"; shift
for spec in "$@"; do
  cell="${spec%%|*}"; rest="${spec#*|}"; still="${rest%%|*}"; rest="${rest#*|}"; suf="${rest%%|*}"; extra="${rest#*|}"
  r=$($S/grok_clip.sh "$cell" "$still" "$suf" "$extra"); echo "$r" >> "$LOG"
  if ! echo "$r" | grep -q "ok=true"; then echo "$(date -u +%FT%TZ) STOP: first failure (R-C3-24)" >> "$LOG"; grep -h -m1 -E "402|balance|Error" ~/astra-burst/grok/C-3/${cell}${suf}/grok_stdout.txt >> "$LOG"; break; fi
done
echo "$(date -u +%FT%TZ) SEQ DONE" >> "$LOG"
