#!/bin/zsh
# Lightweight waiter for a detached wave: blocks until "WAVE DONE" appears in the log (or the timeout in minutes passes).
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad
LOG=$S/$1.log; LIMIT=$(( ${2:-55} * 4 )); n=0
until grep -q "WAVE DONE" $LOG 2>/dev/null; do sleep 15; n=$((n+1)); [ $n -ge $LIMIT ] && { echo "TIMEOUT waiting on $LOG"; exit 2; }; done
tail -2 $LOG | cut -c1-220
