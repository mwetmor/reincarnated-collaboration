#!/usr/bin/env python3
"""Lane SO (R-C9-224): a drop-in GODOT for build_web_painted.sh and r152_05_join_v5.sh -- every Godot run guarded.
    GODOT=/abs/path/r152_06_godot_guard.py bash .../build_web_painted.sh
  * WALL-CLOCK TIMEOUT per Godot run (GG_TIMEOUT_S, default 1200): the whole process group is killed (exit 124);
  * SCRIPT ERRORS ARE FATAL: the first line with "SCRIPT ERROR" or "Parse Error" kills the group (exit 125), so a
    harness erroring every frame cannot hold the shared C-9 heavy lock (the 85-min hang, conductor 2026-10-07);
  * output passes through to stdout unchanged (the caller's own log redirection keeps working).
The heavy lock itself is taken once around the whole build by the caller (heavy_lock.py C-9 -- ...).
Shape after lane PT's barrow_v2/fid/pt/tools/pt_godot.py."""
import os, signal, subprocess, sys, time

REAL = os.environ.get("GG_REAL_GODOT", "/Applications/Godot.app/Contents/MacOS/Godot")
TIMEOUT = float(os.environ.get("GG_TIMEOUT_S", "1200"))
p = subprocess.Popen([REAL] + sys.argv[1:], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
os.set_blocking(p.stdout.fileno(), False)
out = sys.stdout.buffer
t0, buf, why = time.time(), b"", None
while True:
    rc = p.poll()
    try:
        chunk = os.read(p.stdout.fileno(), 1 << 16)
    except BlockingIOError:
        chunk = b""
    if chunk:
        out.write(chunk)
        out.flush()
        buf = (buf + chunk)[-4096:]
        if why is None and (b"SCRIPT ERROR" in buf or b"Parse Error" in buf):
            why = ("script_error", 125)
    if rc is not None and not chunk:
        break
    if why is None and time.time() - t0 > TIMEOUT:
        why = ("timeout", 124)
    if why is not None and rc is None:
        try:
            os.killpg(p.pid, signal.SIGTERM)
            time.sleep(2)
            if p.poll() is None:
                os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait()
        break
    if not chunk:
        time.sleep(0.05)
if why is not None:
    sys.stderr.write("godot_guard: KILLED (%s after %.0f s): %s\n" % (why[0], time.time() - t0, " ".join(sys.argv[1:])[:200]))
    out.write(("\ngodot_guard: KILLED (%s)\n" % why[0]).encode())
    sys.exit(why[1])
sys.exit(p.returncode)
