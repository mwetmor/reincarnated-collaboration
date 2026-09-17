#!/bin/zsh
# clips_seq2.sh <log> "cell|still|suffix|extra" ... — STOPS ON THE FIRST FAILURE (R-C3-24)
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad
LOG="$S/$1.log"; shift
for spec in "$@"; do
  cell="${spec%%|*}"; rest="${spec#*|}"; still="${rest%%|*}"; rest="${rest#*|}"; suf="${rest%%|*}"; extra="${rest#*|}"
  r=$(/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-6/conductor_scripts/grok_clip.sh "$cell" "$still" "$suf" "$extra"); echo "$r" >> "$LOG"
  if ! echo "$r" | grep -q "ok=true"; then echo "$(date -u +%FT%TZ) STOP: first failure (R-C3-24)" >> "$LOG"; CAUSE=$(grep -h -m1 -E "402|balance|out of budget|budget|Error" ~/astra-burst/grok/C-6/${cell}${suf}/grok_stdout.txt); echo "$CAUSE" >> "$LOG"
    if echo "$CAUSE" | grep -qiE "402|balance|budget"; then
      H=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-6/HALT-P3-grok-budget.md
      printf '# HALT — Run C-6 P3 (F7 external-state: Grok budget)\n\n- ts: %s\n- cell: %s\n- cause: %s\n- cells to date are kept under runs/C-6/; resume is Matt'"'"'s word.\n' "$(date -u +%FT%TZ)" "${cell}${suf}" "$CAUSE" > "$H"
      python3 /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-6/conductor_scripts/cl.py halts "{\"id\":\"H-C6-P3-grok\",\"cell\":\"${cell}${suf}\",\"cause\":\"$(echo $CAUSE | tr -d '"' | cut -c1-160)\",\"packet\":\"runs/C-6/HALT-P3-grok-budget.md\"}" > /dev/null
      echo "$(date -u +%FT%TZ) HALT PACKET WRITTEN: $H" >> "$LOG"
    fi; break; fi
done
echo "$(date -u +%FT%TZ) SEQ DONE" >> "$LOG"
