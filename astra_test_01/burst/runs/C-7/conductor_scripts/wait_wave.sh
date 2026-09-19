#!/bin/zsh
# Lightweight waiter for a detached wave: blocks until "WAVE DONE" appears in the log (or the timeout in minutes passes).
S=$HOME/astra-burst/logs/C-7; mkdir -p $S; M=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c7-shared/scratchpad; mkdir -p $M   # session-independent (Gate-1 WARN-13); M = C-6's c5_*.log glob
LOG=$S/$1.log; LIMIT=$(( ${2:-55} * 4 )); n=0
until grep -q "WAVE DONE" $LOG 2>/dev/null; do sleep 15; n=$((n+1)); [ $n -ge $LIMIT ] && { echo "TIMEOUT waiting on $LOG"; exit 2; }; done
tail -2 $LOG | cut -c1-220
