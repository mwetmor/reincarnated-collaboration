#!/bin/zsh
# C-9 painter bake-off (Matt R-C9-49): run a wave with the lane's pinned profile TEMPORARILY pointed at gpt-6-sol.
# The lane reads the model from ~/.codex/astra-burst.config.toml at run time and ledgers model + profile sha per burst,
# so attribution stays exact. The profile is restored on ANY exit (trap) and the restore is verified by sha.
# Refuses to start if another lane burst is running (a concurrent Astra burst must never run as Sol).
P=$HOME/.codex/astra-burst.config.toml; BK=$HOME/.codex/astra-burst.config.toml.astra-bak
C=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/conductor_scripts
if pgrep -f "lane/run_burst.py" >/dev/null; then echo "REFUSE: a lane burst is running"; exit 3; fi
ORIG=$(shasum -a 256 $P | cut -c1-64); cp -p $P $BK
restore() { cp -p $BK $P; NOW=$(shasum -a 256 $P | cut -c1-64); [ "$NOW" = "$ORIG" ] && echo "PROFILE RESTORED (astra) $NOW" || echo "!!! PROFILE RESTORE MISMATCH $NOW != $ORIG"; }
trap restore EXIT INT TERM
sed 's/^model = "gpt-6-astra"/model = "gpt-6-sol"/' $BK > $P
grep -q '^model = "gpt-6-sol"' $P || { echo "swap failed"; exit 4; }
echo "profile -> gpt-6-sol"
zsh $C/wave.sh "$@"
