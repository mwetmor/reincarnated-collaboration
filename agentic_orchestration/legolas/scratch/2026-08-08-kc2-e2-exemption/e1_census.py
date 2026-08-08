#!/usr/bin/env python3
"""E-2 / S1 -- ignoreGameBalance census over Crucible proxypool records. READ-ONLY.

Three populations are measured separately because my own prior notes disagree
(U-9 said "74 of 632", P-E6 said "74 of 635") and the disagreement is a
POPULATION difference, not an arithmetic one:

  POP-A  base-difficulty view      : pools reachable via pool{i}          on proxy_w*_p*<any>.dbr
                                     (this is the U-9 q5 population)
  POP-B  Gladiator view            : pools reachable via poolLegendary{i} if the point declares
                                     any, else pool{i}   -- on proxy_w*_p*a.dbr
                                     (this is the P-E6 s4/s8 population -> the pools CSV)
  POP-C  union over all three difficulty slots (pool / poolEpic / poolLegendary)

Field-presence is tracked explicitly: PRESENT(value) vs ABSENT(-> template default 0).
proxypool.tpl declares:  ignoreGameBalance  class="variable" type="bool" defaultValue="0"
"""
import sys, pathlib, re, collections, json, csv

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
# EXACT archive order used by P-E6 s4_extract.py -- last writer wins.
ORDER = [("base", "database/database.arz"), ("gdx1", "gdx1/database/GDX1.arz"),
         ("gdx2", "gdx2/database/GDX2.arz"), ("gdx3", "gdx3/database/GDX3.arz"),
         ("sm_mod", "mods/survivalmode/database/SurvivalMode.arz"),
         ("sm1", "survivalmode1/database/SurvivalMode1.arz"),
         ("sm2", "survivalmode2/database/SurvivalMode2.arz"),
         ("sm3", "survivalmode3/database/SurvivalMode3.arz")]

M = {}
ARCS = {}
for k, rel in ORDER:
    a = ArzArchive(ROOT / rel)
    ARCS[k] = a
    n = 0
    for r in a.records:
        M[r] = (k, a)
        n += 1
    print(f"  [{k:7s}] {n:7d} records  {rel}")
print(f"resolved record namespace: {len(M)} distinct paths\n")

_c = {}
def get(p):
    p = str(p)
    if p in _c: return _c[p]
    e = M.get(p)
    _c[p] = e[1].read_record(p) if e else None
    return _c[p]
def own(p):
    e = M.get(str(p)); return e[0] if e else None
def rtype(p):
    e = M.get(str(p))
    try: return e[1].record_type(str(p)) if e else None
    except Exception: return None
def num(v, d=0.0):
    try: return float(v)
    except Exception: return d

def igb_of(p):
    """-> (state, value) where state in PRESENT / ABSENT / NORECORD."""
    r = get(p)
    if r is None: return ("NORECORD", None)
    if "ignoreGameBalance" in r:
        return ("PRESENT", r["ignoreGameBalance"])
    return ("ABSENT", None)

# ------------------------------------------------------------------ proxy sweep
PAT_ANY = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)([a-z]*)\.dbr$")
PAT_A   = re.compile(r"^records/proxies/tier(\d+)waves/proxy_w(\d+)_p(\d+)a\.dbr$")

popA, popB, popC = set(), set(), set()
proxies_any, proxies_a = 0, 0
suffixes = collections.Counter()
point_rows = []   # (gwave, tier, wave, pt, proxy, cls, slot, pool)

for path in sorted(M):
    m = PAT_ANY.match(path)
    if not m: continue
    tier, w, pt, sfx = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
    suffixes[sfx] += 1
    proxies_any += 1
    rec = get(path)
    if rec is None: continue

    # POP-A : U-9 q5 -- base pool{i} over ALL suffixes, i in 1..8
    for i in range(1, 9):
        p = rec.get(f"pool{i}")
        if p and get(str(p)) is not None:
            popA.add(str(p))

    if not PAT_A.match(path):
        continue
    proxies_a += 1

    # POP-C : union over the three difficulty slots, i in 1..12 (P-E6 s4 loop bound)
    slots = {}
    for slot, pfx in (("aspirant", "pool"), ("challenger", "poolEpic"), ("gladiator", "poolLegendary")):
        got = []
        for i in range(1, 13):
            p = rec.get(f"{pfx}{i}")
            if not p: continue
            got.append(str(p))
            if get(str(p)) is not None:
                popC.add(str(p))
        slots[slot] = got

    # POP-B : Gladiator view -- poolLegendary if the record declares any, else base pool
    glad = slots["gladiator"] or slots["aspirant"]
    for p in glad:
        if get(p) is not None:
            popB.add(p)
            point_rows.append(dict(gwave=(tier - 1) * 10 + w, tier=tier, wave=w, pt=pt,
                                   proxy=path, cls=rtype(path),
                                   slot=("poolLegendary" if slots["gladiator"] else "pool"),
                                   pool=p))

print(f"proxy records matched (any suffix): {proxies_any}   suffix histogram: {dict(suffixes)}")
print(f"proxy records matched ('a' only) : {proxies_a}\n")

def fam(p):
    return pathlib.Path(p).parent.name

def census(name, pop):
    st = collections.Counter()
    fams = collections.defaultdict(lambda: [0, 0, 0])   # fam -> [n, igb0, igb1]
    vals = collections.Counter()
    for p in sorted(pop):
        s, v = igb_of(p)
        st[s] += 1
        on = 1 if (s == "PRESENT" and num(v, 0) != 0) else 0
        vals[(s, str(v))] += 1
        f = fams[fam(p)]
        f[0] += 1; f[1 + on] += 1
    n1 = sum(v[2] for v in fams.values())
    print(f"=== {name}: {len(pop)} distinct pools | field-state {dict(st)} | IGB=1 -> {n1}")
    print(f"    raw value histogram: { {f'{k[0]}:{k[1]}': c for k, c in sorted(vals.items())} }")
    print(f"    {'family':22s} {'n':>4s} {'IGB=0':>6s} {'IGB=1':>6s}")
    tot = [0, 0, 0]
    for f in sorted(fams):
        n, z, o = fams[f]
        tot[0] += n; tot[1] += z; tot[2] += o
        print(f"    {f:22s} {n:4d} {z:6d} {o:6d}")
    print(f"    {'TOTAL':22s} {tot[0]:4d} {tot[1]:6d} {tot[2]:6d}\n")
    return dict(n=len(pop), igb1=n1, fams={k: v for k, v in fams.items()}, states=dict(st))

R = {}
R["POP_A_base_all_suffixes"] = census("POP-A  base pool{i}, all proxy suffixes  (U-9 q5 population)", popA)
R["POP_B_gladiator_view_a"]  = census("POP-B  Gladiator view, proxy_*a only     (P-E6 pools-CSV population)", popB)
R["POP_C_union_all_slots_a"] = census("POP-C  union of pool/poolEpic/poolLegendary, proxy_*a only", popC)

print("=== set relations ===")
print(f"  |A|={len(popA)} |B|={len(popB)} |C|={len(popC)}")
print(f"  B \\ A ({len(popB - popA)}): {sorted(popB - popA)}")
print(f"  A \\ B ({len(popA - popB)}): {sorted(popA - popB)}")
print(f"  C \\ B ({len(popC - popB)}): {sorted(popC - popB)}")
print(f"  A \\ C ({len(popA - popC)}): {sorted(popA - popC)}")

json.dump(dict(census=R,
               popA=sorted(popA), popB=sorted(popB), popC=sorted(popC),
               igb={p: dict(state=igb_of(p)[0], value=(None if igb_of(p)[1] is None else str(igb_of(p)[1])),
                            owner=own(p), rtype=rtype(p))
                    for p in sorted(popA | popB | popC)}),
          open("e1_census.json", "w"), indent=1)
json.dump(point_rows, open("e1_points_gladiator.json", "w"), indent=1)
print("\n[wrote e1_census.json, e1_points_gladiator.json]")
