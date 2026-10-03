"""jack-ryan H-5: numeric-literal scan of kc2_runtime sim/, loader/, native/src at the candidate (KP-229 (b)).
Strips comments and string literals; reports every numeric literal not in TRIVIAL, with file:line and the code line.
Output: TSV file<TAB>line<TAB>literal<TAB>code."""
import os, re, sys
ROOT = sys.argv[1]
DIRS = ("sim", "loader", "native/src")
TRIVIAL = {"0","1","2","-1","0.0","1.0","2.0","0.5","-1.0"}
num = re.compile(r"(?<![A-Za-z_0-9.])(-?(?:0x[0-9A-Fa-f]+|\d+\.\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+|\d+))(?![A-Za-z_0-9])")
def strip_gd(line):
    out, q, i = [], None, 0
    while i < len(line):
        ch = line[i]
        if q:
            if ch == "\\": i += 2; continue
            if ch == q: q = None
            i += 1; continue
        if ch in "\"'": q = ch; out.append(" "); i += 1; continue
        if ch == "#": break
        out.append(ch); i += 1
    return "".join(out)
def strip_cpp(text):
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    lines = []
    for l in text.split("\n"):
        l = re.sub(r'"(\\.|[^"\\])*"', '""', l)
        l = l.split("//")[0]
        lines.append(l)
    return lines
rows = []
for d in DIRS:
    for dp, _, fs in os.walk(os.path.join(ROOT, d)):
        for f in sorted(fs):
            p = os.path.join(dp, f); rel = os.path.relpath(p, ROOT)
            if f.endswith(".gd"):
                src = open(p, encoding="utf-8").read().split("\n")
                code = [strip_gd(l) for l in src]
            elif f.endswith((".cpp", ".h")):
                src = open(p, encoding="utf-8").read().split("\n")
                code = strip_cpp("\n".join(src))
            else:
                continue
            for i, l in enumerate(code, 1):
                if re.match(r"\s*(@export|extends|class_name)", l): continue
                for m in num.finditer(l):
                    lit = m.group(1)
                    if lit in TRIVIAL: continue
                    # skip array/dict indexing with small ints e.g. [3]
                    rows.append((rel, i, lit, src[i - 1].strip()[:200]))
for r in rows:
    print("\t".join(map(str, r)))
