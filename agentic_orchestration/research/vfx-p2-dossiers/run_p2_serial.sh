#!/bin/bash
# VFX archetype-binding run — P2 serial Codex dossier lane (ledger L-6 mechanics; R-2 first live workload).
# LAW: strictly serial — ONE codex exec at a time, NEVER parallel (one-auth.json serialization, U-4).
# Usage: ./run_p2_serial.sh <start_index> <end_index>   (1-based, inclusive, over jobs/NN-*.prompt.md)
set -u
cd "$(dirname "$0")"
START=${1:-1}; END=${2:-26}
RUNLOG="usage/_run-log.tsv"
touch "$RUNLOG"
i=0
for f in jobs/[0-9][0-9]-*.prompt.md; do
  i=$((i+1))
  [ "$i" -lt "$START" ] && continue
  [ "$i" -gt "$END" ] && break
  base=$(basename "$f" .prompt.md)
  aid=${base#[0-9][0-9]-}
  # Idempotency: skip jobs whose dossier already exists and is non-trivial
  if [ -s "dossiers/${aid}.md" ] && [ "$(wc -c < "dossiers/${aid}.md")" -gt 500 ]; then
    printf '%s\t%s\tSKIP-EXISTS\t-\n' "$(date -u +%FT%TZ)" "$base" >> "$RUNLOG"
    continue
  fi
  t0=$(date -u +%FT%TZ)
  codex exec --json --ephemeral --skip-git-repo-check -s read-only \
    -c tools.web_search=true \
    -o "dossiers/${aid}.md" \
    - < "$f" > "usage/${base}.jsonl" 2> "usage/${base}.err"
  rc=$?
  t1=$(date -u +%FT%TZ)
  bytes=$( [ -f "dossiers/${aid}.md" ] && wc -c < "dossiers/${aid}.md" || echo 0 )
  printf '%s\t%s\trc=%d\tstart=%s end=%s dossier_bytes=%s\n' "$t1" "$base" "$rc" "$t0" "$t1" "$bytes" >> "$RUNLOG"
done
echo "P2 serial lane pass complete (jobs $START..$END)."
