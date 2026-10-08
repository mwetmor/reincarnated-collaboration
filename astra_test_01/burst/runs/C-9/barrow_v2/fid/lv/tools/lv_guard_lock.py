#!/usr/bin/env python3
"""BV2F LV (R-C9-226 rules): a DROP-IN for heavy_lock.py -- same argv (`<run> -- <cmd...>`) -- that runs the command
under the shared C-9 heavy lock with pt_godot.py's guards (fid/pt/tools/pt_godot.py, the conductor's one way to run Godot):
  * disk gate: >= 21 GiB free on /System/Volumes/Data, else exit 9;
  * WALL-CLOCK TIMEOUT after the lock is acquired (env LV_TIMEOUT_S, default 1200): process group killed, exit 124;
  * SCRIPT ERRORS FATAL: the first line with "SCRIPT ERROR" or "Parse Error" kills the group, exit 125;
  * output passes through to stdout (callers redirect it to their own logs), capped at 32 MB (exit 126 past it).
Used as   python3 lv_guard_lock.py C-9 -- <cmd>   or, for the frozen godot_run.sh, HEAVY_LOCK=<this file>."""
import os
import shutil
import signal
import subprocess
import sys
import time

HL = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py"
a = sys.argv[1:]
if "--" not in a or a.index("--") < 1:
    sys.exit("usage: lv_guard_lock.py <run> -- <cmd...>")
run, cmd = a[0], a[a.index("--") + 1:]
TIMEOUT = float(os.environ.get("LV_TIMEOUT_S", "1200"))
CAP = 32 * 1024 * 1024
free = shutil.disk_usage("/System/Volumes/Data").free / 2 ** 30
if free < 21:
    print("lv_guard_lock: HALT disk %.1f GiB < 21" % free, flush=True)
    sys.exit(9)
p = subprocess.Popen(["python3", HL, run, "--"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
t_run, written, why, buf = None, 0, None, b""
os.set_blocking(p.stdout.fileno(), False)
out = sys.stdout.buffer
while True:
    rc = p.poll()
    try:
        chunk = os.read(p.stdout.fileno(), 1 << 16)
    except BlockingIOError:
        chunk = b""
    if chunk:
        buf += chunk
        *lines, buf = buf.split(b"\n")
        for ln in lines:
            if t_run is None and b"heavy_lock: acquired" in ln:
                t_run = time.time()
            if written < CAP:
                out.write(ln + b"\n")
                written += len(ln) + 1
            if (b"SCRIPT ERROR" in ln or b"Parse Error" in ln) and why is None:
                why = ("script_error", 125, ln.decode("utf-8", "replace")[:200])
        out.flush()
        if written >= CAP and why is None:
            why = ("log_cap", 126, "%d bytes" % written)
    if rc is not None and not chunk:
        break
    if why is None and t_run is not None and time.time() - t_run > TIMEOUT:
        why = ("timeout", 124, "%.0f s after the lock" % (time.time() - t_run))
    if why is not None and rc is None:
        os.killpg(p.pid, signal.SIGTERM)
        time.sleep(2)
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL)
    time.sleep(0.05)
if buf and written < CAP:
    out.write(buf)
    out.flush()
if why is not None:
    print("lv_guard_lock: KILLED (%s: %s)" % (why[0], why[2]), flush=True)
    sys.exit(why[1])
sys.exit(p.returncode)
