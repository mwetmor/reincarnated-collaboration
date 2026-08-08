#!/usr/bin/env python3
"""F-8 RIDER / part 3 -- CORRECT template Include expansion.
GD templates declare includes as   Variable { name="Include File" type="include"
defaultValue="database/templates/..." }   -- not as an Include{} block.  READ-ONLY."""
import sys, re, pathlib, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive

T = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
def norm(p):
    """GD templates mix 'database/templates/x.tpl', 'database\\Templates\\TemplateBase\\X.tpl'
    and bare 'x.tpl'.  Normalise to a lowercase forward-slash basename + full-ish key."""
    q = str(p).replace("\\", "/").lower()
    q = re.sub(r"^database/templates/", "", q)
    return q
BY = {}
for n in T.names():
    BY[norm(n)] = n
    BY[norm(n).rsplit("/", 1)[-1]] = n

VARBLK = re.compile(r'Variable\s*\{(.*?)\}', re.S)
def fld(blk, k):
    m = re.search(rf'{k}\s*=\s*"([^"]*)"', blk)
    return m.group(1) if m else ""

def load(name):
    key = BY.get(norm(name)) or BY.get(norm(name).rsplit("/", 1)[-1])
    return T.read_file(key).decode("latin-1") if key else None

def expand(name, seen=None, depth=0, out=None, trace=None):
    seen = set() if seen is None else seen
    out = {} if out is None else out
    trace = [] if trace is None else trace
    key = norm(name).rsplit("/", 1)[-1]
    if key in seen: return out, trace
    seen.add(key)
    txt = load(name)
    if txt is None:
        trace.append(("  " * depth + name, "!! MISSING")); return out, trace
    blks = VARBLK.findall(txt)
    incs = []
    n_own = 0
    for b in blks:
        nm, ty, df = fld(b, "name"), fld(b, "type"), fld(b, "defaultValue")
        if ty == "include" or nm == "Include File":
            incs.append(df); continue
        if not nm: continue
        n_own += 1
        out.setdefault(nm, dict(src=name, cls=fld(b, "class"), typ=ty,
                                desc=fld(b, "description"), dflt=df))
    trace.append(("  " * depth + name, f"{n_own} own vars, {len(incs)} includes"))
    for i in incs:
        expand(i, seen, depth + 1, out, trace)
    return out, trace

TARGETS = [("Soulfire", "skillsecondary_attackprojectileorbiting.tpl"),
           ("Eye of Reckoning (base)", "skill_attackradiusspin.tpl"),
           ("Aether Ray (base)", "skill_attackspellbeam.tpl"),
           ("Disintegration (modifier)", "skill_modifier.tpl")]
COST = ("skillManaCost", "skillManaCostReduction", "skillManaCostReductionModifier",
        "skillActiveManaCost", "skillActiveManaCostPerSecond", "skillManaCostPct")

RES = {}
for label, tname in TARGETS:
    d, tr = expand(tname)
    RES[tname] = d
    print("=" * 106)
    print(f"{label}   {tname}   -> {len(d)} variables after FULL include expansion")
    for a, b in tr: print(f"    {a:66s} {b}")
    print("-" * 106)
    for f in COST:
        if f in d:
            v = d[f]
            print(f"    DECLARED     {f:32s} [{v['src']}]  class={v['cls']:9s} type={v['typ']:8s} "
                  f"default={v['dflt']!r:6s}  desc={v['desc']!r}")
        else:
            print(f"    NOT DECLARED {f:32s}")
    ce = sorted(k for k in d if re.search(r"mana|energy|cost", k, re.I))
    print(f"    every cost/energy variable reachable: {ce}")
    print()

print("=" * 106)
print("DIFFERENTIAL:  which template contributes skillManaCost, and does the Soulfire chain reach it?")
print("=" * 106)
for tname, d in RES.items():
    hit = d.get("skillManaCost")
    print(f"  {tname:46s} skillManaCost -> {('DECLARED by ' + hit['src']) if hit else 'UNREACHABLE'}")

# where does skillManaCost live, corpus-wide?
print("\n  --- every template in templates.arc that declares skillManaCost ---")
for n in sorted(T.names()):
    if not n.lower().endswith(".tpl"): continue
    try: txt = T.read_file(n).decode("latin-1")
    except Exception: continue
    for b in VARBLK.findall(txt):
        if fld(b, "name") == "skillManaCost":
            print(f"     {n:56s} class={fld(b,'class'):9s} type={fld(b,'type'):8s} "
                  f"default={fld(b,'defaultValue')!r:6s} desc={fld(b,'description')!r}")

print("\n  --- and skill_secondary.tpl in full (the branch Soulfire actually sits on) ---")
txt = load("templatebase/skill_secondary.tpl")
print(txt if txt else "  <missing>")
