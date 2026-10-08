#!/usr/bin/env python3
"""BV2F PT: heavy_lock.py's interface (<run> -- <cmd...>) for a command whose caller ALREADY holds the C-9 heavy lock
(pt_godot.py). Used as HEAVY_LOCK for fid/v1tools/godot_run.sh under pt_godot.py, so the frozen runner does not try to
take the same lock a second time (it would wait on itself forever). Runs the command; nothing else."""
import os, sys
cmd = sys.argv[sys.argv.index("--") + 1:]
os.execvp(cmd[0], cmd)
