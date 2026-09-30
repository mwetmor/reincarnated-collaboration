#!/bin/bash
# fps_probe.sh <app executable> <label> [seconds]
# Fullscreen, vsync forced off, --print-fps; the first 8 s are warm-up (shaders, first loads)
# and are dropped. Prints the median ms per frame of the rest.
EXE=$1; LABEL=$2; SECS=${3:-30}
OUT=$(mktemp -t fpsprobe)
"$EXE" --fullscreen --disable-vsync --print-fps > "$OUT" 2>&1 &
PID=$!
sleep "$SECS"
kill "$PID" 2>/dev/null; sleep 2; kill -9 "$PID" 2>/dev/null
python3 - "$OUT" "$LABEL" <<'PY'
import re, sys, statistics
lines = open(sys.argv[1], errors="replace").read().splitlines()
ms = [float(m.group(2)) for l in lines for m in [re.search(r"Project FPS: (\d+) \(([\d.]+) mspf\)", l)] if m]
use = ms[8:] if len(ms) > 12 else ms
errs = sum(1 for l in lines if "SCRIPT ERROR" in l)
print("[fps] %s: %d samples after warm-up, median %.2f ms/frame (%.0f fps), p90 %.2f ms; script errors in its log: %d"
      % (sys.argv[2], len(use), statistics.median(use) if use else -1, 1000.0 / statistics.median(use) if use else 0,
         sorted(use)[int(len(use) * 0.9)] if use else -1, errs))
PY
rm -f "$OUT"
