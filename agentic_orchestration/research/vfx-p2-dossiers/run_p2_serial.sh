#!/bin/bash
# ============================================================================
# RETIRED AS AN INSTRUMENT — 2026-08-24 (lane spec P-10 / build item D-4).
#
# THIS SCRIPT IS LINEAGE, NOT AN INSTRUMENT. It proved the mechanics — 30/30 jobs
# rc=0, strict serialization, idempotent re-entry — and those semantics now live in
# `agentic_orchestration/factory/jobqueue.py`, which generalises them past this one
# job class. Kept in-tree as the proven-pattern reference: git would have kept the
# text, but a reader comparing the queue's choices against the runner's needs them
# side by side, and `usage/_run-log.tsv` below is still a live leg-3 surface that the
# cross-session busy check reads.
#
# WHAT REPLACED IT:
#     factory lane                          # is a vendor lane free RIGHT NOW? (read-only)
#     factory lane-enqueue <root> <id> <prompt-file> --curator <agent>
#     factory lane-drain   <root>           # idempotent; safe to re-fire
#
# DO NOT RUN THIS. A `codex exec` reached other than through the harness lock is a
# PROTOCOL VIOLATION (P-10), with exactly one standing exception: Matt's personal
# terminal use, which the busy check SEES and does not govern. This script takes no
# lock and writes no row until a job FINISHES, so no other session can tell it is
# running — which is precisely the failure the busy check was built to end.
#
# The retirement takes effect from the queue's first production drain. In the bridge
# window before then, any hand-fire REQUIRES `factory lane --lane codex` first.
# ============================================================================
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
