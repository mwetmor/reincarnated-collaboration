#!/usr/bin/env python3
"""BV2F lane PT: THE ONE WAY PT RUNS GODOT (conductor, after PID 78315 held the shared heavy lock for 85 min).
    python3 fid/pt/tools/pt_godot.py --log LOG [--timeout-s 900] [--max-errors 1] [--log-cap-mb 16] -- <godot argv...>
  * disk gate (>= 21 GiB free on /System/Volumes/Data, else exit 9) and the C-9 heavy lock (heavy_lock.py) around the run;
  * WALL-CLOCK TIMEOUT: the whole process group (lock wrapper + Godot) is killed after --timeout-s (exit 124);
  * SCRIPT ERRORS ARE FATAL: on the --max-errors'th line containing "SCRIPT ERROR" or "Parse Error" the group is killed
    (exit 125) -- a harness erroring every frame can never hold the lock again;
  * LOG CAP: at most --log-cap-mb MB is written to LOG; past it, output is dropped and the run is killed (exit 126).
Exit = Godot's own code otherwise. Every PT Godot run goes through this (absolute paths, one command per call)."""
import os, shutil, signal, subprocess, sys, time

a = sys.argv[1:]
if "--" not in a:
    sys.exit("usage: pt_godot.py --log LOG [--timeout-s N] [--max-errors N] [--log-cap-mb N] -- <godot argv>")
opts, cmd = a[:a.index("--")], a[a.index("--") + 1:]
opt = lambda k, d: opts[opts.index(k) + 1] if k in opts else d
LOG = opt("--log", None)
TIMEOUT = float(opt("--timeout-s", 900))
MAXERR = int(opt("--max-errors", 1))
CAP = int(float(opt("--log-cap-mb", 16)) * 1024 * 1024)
HL = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py"
if LOG is None:
    sys.exit("pt_godot: --log is required")
free = shutil.disk_usage("/System/Volumes/Data").free / 2 ** 30
if free < 21:
    print("pt_godot: HALT disk %.1f GiB < 21" % free)
    sys.exit(9)
p = subprocess.Popen(["python3", HL, "C-9", "--"] + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     start_new_session=True, env=os.environ.copy())
t0 = time.time()
t_run = None
written, errs, why = 0, 0, None
os.set_blocking(p.stdout.fileno(), False)
buf = b""
with open(LOG, "wb") as f:
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
                    f.write(ln + b"\n")
                    written += len(ln) + 1
                if b"SCRIPT ERROR" in ln or b"Parse Error" in ln:
                    errs += 1
                    if errs >= MAXERR and why is None:
                        why = ("script_error", 125, ln.decode("utf-8", "replace")[:200])
            f.flush()
            if written >= CAP and why is None:
                why = ("log_cap", 126, "%d bytes" % written)
        if rc is not None and not chunk:
            break
        # the lock wait is not run time: the clock starts once Godot owns the lock (heavy_lock prints 'acquired')
        if why is None and t_run is not None and time.time() - t_run > TIMEOUT:
            why = ("timeout", 124, "%.0f s after the lock" % (time.time() - t_run))
        if why is not None and rc is None:
            os.killpg(p.pid, signal.SIGTERM)
            time.sleep(2)
            if p.poll() is None:
                os.killpg(p.pid, signal.SIGKILL)
        time.sleep(0.05)
    if buf and written < CAP:
        f.write(buf)
if why is not None:
    print("pt_godot: KILLED (%s: %s) -- log %s" % (why[0], why[2], LOG))
    sys.exit(why[1])
print("pt_godot: exit %d -- log %s (%d bytes)" % (p.returncode, LOG, written))
sys.exit(p.returncode)
