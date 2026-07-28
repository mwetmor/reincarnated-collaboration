import importlib.util, math, collections, sys
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G
T=R.tags()
paths={}
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/creatures/enemies/") and "/bios/" not in p: paths[p]=a
_rc={}
def rd(p):
    if p not in _rc:
        try:_rc[p]=R.rec(p)
        except Exception:_rc[p]=None
    return _rc[p]
PAK=R.pak_vals(); PL=PAK["characterLifeModifier"]
OPS={
 "A_pak35":  lambda L,f,s: (L+f)*(1+(s+35)/100),
 "C_pak50":  lambda L,f,s: (L+f)*(1+(s+50)/100),
 "D_mult":   lambda L,f,s: (L+f)*(1+s/100)*(1+PL/100),
 "E_nopak":  lambda L,f,s: (L+f)*(1+s/100),
}
TARGETS=[4702,1820,813,649,434,326,58]
hits=collections.defaultdict(list)
for p in paths:
    m=rd(p)
    if not m or m.get("Class")!="Monster": continue
    bio=m.get("characterAttributeEquations")
    b=rd(bio) if bio else None
    if not b or not b.get("characterLife"): continue
    cle=m.get("charLevel") or "charLevel*1"
    for spawn in range(1,31):
        _cl=R.evaleq(cle,spawn)
        if _cl is None: continue
        cl=int(_cl)
        if cl<1 or cl>60: continue
        L=R.evaleq(b["characterLife"],cl)
        if L is None: continue
        s=0.0; f=0.0
        for i in range(1,13):
            sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
            if not sn: continue
            rk=R.evaleq(sl,cl) if isinstance(sl,str) else sl
            rk=0 if rk is None else int(rk)
            if rk<1: continue
            sk=rd(sn)
            if not sk or sk.get("Class")!="Skill_Passive": continue
            v=R.arr(sk.get("characterLifeModifier"),rk)
            if isinstance(v,(int,float)): s+=v
            v2=R.arr(sk.get("characterLife"),rk)
            if isinstance(v2,(int,float)): f+=v2
        for h,fn in OPS.items():
            val=fn(L,f,s)
            if val<=0: continue
            fl=math.floor(val)
            for t in TARGETS:
                if fl==t: hits[(h,t)].append((p,cl,round(val,3),m.get("monsterClassification"),T.get(m.get("description"),"")))
for h in OPS:
    for t in TARGETS:
        v=hits[(h,t)]
        print(f"{h:9s} t={t:6d} n={len(v)}")
        if t in (4702,1820) and v:
            for row in v[:20]: print("      ",row)
