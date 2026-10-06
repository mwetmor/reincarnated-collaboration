"""Statement-for-statement check: 66605a1's _pmove_pilot body == 0eacae1's _pmove_propose + _pilot_wraps bodies
(non-blank, non-comment lines, in order). Usage: python3 split_compare.py <old fight.gd> <new fight.gd>"""
import sys
def body(lines, name):
    i = [n for n, l in enumerate(lines) if l.startswith("func %s(" % name)][0]
    out = []
    for l in lines[i + 1:]:
        if l and not l.startswith("\t") and not l.startswith(" "):
            break
        out.append(l)
    return [l for l in out if l.strip() and not l.strip().startswith("#")]
old = open(sys.argv[1]).read().split("\n"); new = open(sys.argv[2]).read().split("\n")
o = body(old, "_pmove_pilot"); n = body(new, "_pmove_propose") + body(new, "_pilot_wraps")
print(len(o), len(n), "EQUAL" if o == n else "DIFFER"); print("new _pmove_pilot:", body(new, "_pmove_pilot"))
