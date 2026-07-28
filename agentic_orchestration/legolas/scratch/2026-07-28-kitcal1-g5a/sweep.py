import importlib.util, math, json, collections, sys
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G = R.G

# collect creature records (later archive overrides)
paths = {}
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/creatures/enemies/") and "/bios/" not in p:
            paths[p] = a
print("creature records:", len(paths), file=sys.stderr)

_rc = {}
def rd(p):
    if p not in _rc:
        try: _rc[p] = R.rec(p)
        except Exception: _rc[p] = None
    return _rc[p]

PAK = R.pak_vals()
PAKLIFE = PAK.get("characterLifeModifier", 0.0)

TARGETS = [58, 326, 434, 649, 813, 1820, 4702, 14812]
hits = collections.defaultdict(list)

for p in paths:
    m = rd(p)
    if not m or m.get("Class") != "Monster": continue
    bio = m.get("characterAttributeEquations")
    if not bio: continue
    b = rd(bio)
    if not b: continue
    eqL = b.get("characterLife")
    if not eqL: continue
    cle = m.get("charLevel") or "charLevel*1"
    for spawn in range(1, 26):
        _cl = R.evaleq(cle, spawn)
        if _cl is None: continue
        cl = int(_cl)
        if cl < 1 or cl > 60: continue
        life = R.evaleq(eqL, cl)
        if life is None: continue
        smod = 0.0; sflat = 0.0
        for i in range(1, 13):
            sn = m.get(f"skillName{i}"); sl = m.get(f"skillLevel{i}")
            if not sn: continue
            rk = R.evaleq(sl, cl) if isinstance(sl, str) else sl
            rk = 0 if rk is None else int(rk)
            if rk < 1: continue
            s = rd(sn)
            if not s or s.get("Class") != "Skill_Passive": continue
            v = R.arr(s.get("characterLifeModifier"), rk)
            if isinstance(v,(int,float)): smod += v
            v2 = R.arr(s.get("characterLife"), rk)
            if isinstance(v2,(int,float)): sflat += v2
        cand = {
            "H1_add":  (life+sflat)*(1+(smod+PAKLIFE)/100.0),
            "H2_mult": (life+sflat)*(1+smod/100.0)*(1+PAKLIFE/100.0),
            "H3_nopak":(life+sflat)*(1+smod/100.0),
            "H4_raw":  (life+sflat),
        }
        for h, val in cand.items():
            if val is None or val <= 0: continue
            f = math.floor(val)
            for t in TARGETS:
                if f == t:
                    hits[(h,t)].append((p, cl, round(val,3), smod))

for (h,t), v in sorted(hits.items()):
    print(f"### {h} target={t}  n={len(v)}")
    for row in v[:12]: print("   ", row)
