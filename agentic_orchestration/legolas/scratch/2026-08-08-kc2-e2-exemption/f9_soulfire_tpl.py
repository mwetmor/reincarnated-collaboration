#!/usr/bin/env python3
"""F-8 RIDER / part 2 -- does the ORBITING-PROJECTILE template even DECLARE a cost field?
plus: locate the record that actually owns the '3-20' and the 'per damage interval' clause.
READ-ONLY."""
import sys, pathlib, re, collections
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ORDER = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
         ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
         ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", "survivalmode3/database/SurvivalMode3.arz")]
ARC, WHERE = {}, collections.defaultdict(list)
for k, rel in ORDER:
    ARC[k] = ArzArchive(ROOT / rel)
    for r in ARC[k].records:
        WHERE[r].append(k)
def get(p): return ARC[WHERE[p][-1]].read_record(p) if p in WHERE else None

# ------------------------------------------------------------------ templates (live install; Edition-II ships no templates.arc)
T = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
TN = {n.lower(): n for n in T.names()}
def tpl(name):
    n = TN.get(name.lower())
    return T.read_file(n).decode("latin-1") if n else None

VARBLK = re.compile(r'Variable\s*\{(.*?)\}', re.S)
def declares(txt):
    out = {}
    for blk in VARBLK.findall(txt or ""):
        nm = re.search(r'name\s*=\s*"([^"]*)"', blk)
        if not nm: continue
        out[nm.group(1)] = dict(
            cls=(re.search(r'class\s*=\s*"([^"]*)"', blk) or [None, ""])[1] if re.search(r'class\s*=\s*"([^"]*)"', blk) else "",
            typ=(re.search(r'type\s*=\s*"([^"]*)"', blk).group(1) if re.search(r'type\s*=\s*"([^"]*)"', blk) else ""),
            desc=(re.search(r'description\s*=\s*"([^"]*)"', blk).group(1) if re.search(r'description\s*=\s*"([^"]*)"', blk) else ""),
            dflt=(re.search(r'defaultValue\s*=\s*"([^"]*)"', blk).group(1) if re.search(r'defaultValue\s*=\s*"([^"]*)"', blk) else ""))
    return out

INC = re.compile(r'Include\s*\{[^}]*name\s*=\s*"([^"]*)"', re.S)
def expand(name, seen=None, depth=0):
    """template + transitive Includes"""
    seen = seen if seen is not None else set()
    if name.lower() in seen: return {}, []
    seen.add(name.lower())
    txt = tpl(pathlib.Path(name).name)
    if txt is None: return {}, [(name, "MISSING")]
    d = declares(txt); trace = [(name, f"{len(d)} vars")]
    for inc in INC.findall(txt):
        d2, t2 = expand(inc, seen, depth + 1)
        d.update(d2); trace += [("  " * (depth + 1) + a, b) for a, b in t2]
    return d, trace

for tname in ("skillsecondary_attackprojectileorbiting.tpl", "skill_attackradiusspin.tpl"):
    d, trace = expand(tname)
    print("=" * 104)
    print(f"TEMPLATE  {tname}   -> {len(d)} declared variables after Include expansion")
    for a, b in trace: print(f"    {a:60s} {b}")
    print("=" * 104)
    for f in ("skillManaCost", "skillManaCostReduction", "skillManaCostReductionModifier",
              "skillActiveManaCost", "projectilePeriod", "skillProjectileNumber",
              "skillCooldownTime", "skillActiveDuration", "timeBetweenAttacks"):
        if f in d:
            v = d[f]
            print(f"    DECLARED  {f:34s} class={v['cls']:9s} type={v['typ']:9s} "
                  f"default={v['dflt']!r:8s} desc={v['desc']!r}")
        else:
            print(f"    --------  {f:34s} NOT DECLARED BY THIS TEMPLATE")
    # anything cost-ish at all
    costish = sorted(k for k in d if re.search(r"mana|energy|cost", k, re.I))
    print(f"    all cost/energy-ish variables declared: {costish}")
    print()

# ------------------------------------------------------------------ who owns the 3-20 / 'per damage interval'
print("=" * 104)
print("WHO OWNS THE '3-20' AND THE 'per damage interval' CLAUSE?")
print("=" * 104)
cands = [p for p in WHERE if re.match(r"^records/skills/playerclass05/aetherray", p)]
for p in sorted(cands):
    r = get(p)
    print(f"\n  {p}   archives={WHERE[p]}  Class={r.get('Class')!r}")
    print(f"     skillDisplayName={r.get('skillDisplayName')!r}  skillBaseDescription={r.get('skillBaseDescription')!r}")
    mc = r.get("skillManaCost")
    print(f"     skillManaCost = {mc}")
    if isinstance(mc, list):
        print(f"        len={len(mc)}  min={min(mc)}  max={max(mc)}")

# every skill record whose skillManaCost spans 3..20
print("\n  --- corpus sweep: every skill record with skillManaCost min==3 and max==20 ---")
hits = []
for p, ks in WHERE.items():
    if not p.startswith("records/skills/"): continue
    r = ARC[ks[-1]].read_record(p)
    mc = r.get("skillManaCost")
    if isinstance(mc, list) and len(mc) > 1 and min(mc) == 3 and max(mc) == 20:
        hits.append((p, len(mc), r.get("skillDisplayName")))
for p, n, dn in sorted(hits):
    print(f"     {p:60s} len={n:3d}  displayName={dn!r}")
print(f"     ({len(hits)} records)")

# ------------------------------------------------------------------ does ANY eyeofreckoning record carry a cost?
print("\n" + "=" * 104)
print("EVERY 'eyeofreckoning' RECORD IN THE CORPUS, cost fields only")
print("=" * 104)
for p in sorted(x for x in WHERE if "eyeofreckoning" in x.lower()):
    r = get(p)
    if not p.startswith("records/skills") and "skills" not in p:
        pass
    mc = r.get("skillManaCost")
    keys = [k for k in r if re.search(r"manaCost|manaBurn|activeMana", k, re.I)]
    print(f"  {p:74s} Class={str(r.get('Class'))[:34]:36s} skillManaCost={mc if mc is not None else 'ABSENT'}")
    if keys: print(f"       cost-ish keys: {[(k, r[k]) for k in sorted(keys)]}")
