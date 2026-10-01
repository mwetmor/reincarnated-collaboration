# R-C9-98: run a command with a hard timeout (no coreutils `timeout` on this Mac). to.py <seconds> <cmd...>
import subprocess, sys
try:
    sys.exit(subprocess.run(sys.argv[2:], timeout=float(sys.argv[1])).returncode)
except subprocess.TimeoutExpired:
    print("TO.PY TIMEOUT after %s s: %s" % (sys.argv[1], " ".join(sys.argv[2:])), file=sys.stderr); sys.exit(124)
