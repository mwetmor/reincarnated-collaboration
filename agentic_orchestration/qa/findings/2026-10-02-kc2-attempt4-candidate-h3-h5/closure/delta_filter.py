"""Keep scan rows whose line was added/changed in ff6b267..96fc0cc (git diff -U0 new-side line numbers)."""
import re, subprocess, sys
G, scan = sys.argv[1], sys.argv[2]
diff = subprocess.run(["git", "-C", G, "diff", "-U0", "ff6b267", "96fc0cc", "--", "kc2_runtime/sim", "kc2_runtime/loader", "kc2_runtime/native/src"], capture_output=True, text=True).stdout
added, cur = {}, None
for l in diff.split("\n"):
    if l.startswith("+++ "):
        cur = l[6:].replace("kc2_runtime/", "", 1) if l[4:] != "/dev/null" else None
    m = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", l)
    if m and cur:
        a, n = int(m.group(1)), int(m.group(2) or 1)
        added.setdefault(cur, set()).update(range(a, a + n))
for row in open(scan, encoding="utf-8"):
    f, ln = row.split("\t")[:2]
    if int(ln) in added.get(f, ()):
        sys.stdout.write(row)
