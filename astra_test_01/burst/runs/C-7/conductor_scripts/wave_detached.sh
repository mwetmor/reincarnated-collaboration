#!/bin/zsh
# LD-2 launcher: run wave.sh DETACHED from the conductor's shell (setsid + nohup) so a harness kill of the
# conductor's command cannot take the burst down with it. Usage: wave_detached.sh <logname> <id:TYPE> [...]
# Completion is observed by polling the wave log for "WAVE DONE" (wait_wave.sh), never by process exit.
S=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/4e83a458-9b8a-45f0-8e0c-8487cc714a21/scratchpad
D=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts
nohup zsh $D/wave.sh "$@" > $S/$1.detached.out 2>&1 < /dev/null &!
echo "detached pid $! log $S/$1.log"
