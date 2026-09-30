#!/usr/bin/env python3
# tmo.py SECONDS -- cmd...: run cmd, kill its process group after SECONDS (macOS has no `timeout`).
import os, signal, subprocess, sys
secs = float(sys.argv[1]); cmd = sys.argv[sys.argv.index('--') + 1:]
p = subprocess.Popen(cmd, start_new_session=True)
try:
    sys.exit(p.wait(timeout=secs))
except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL); print(f"tmo: killed after {secs:.0f}s", file=sys.stderr); sys.exit(124)
