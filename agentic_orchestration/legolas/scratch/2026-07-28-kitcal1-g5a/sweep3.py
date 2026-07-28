import importlib.util, math, collections
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G; T=R.tags()
paths={}
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/creatures/") and "/bios/" not in p: paths[p]=a
_rc={}
def rd(p):
    if p not in _rc:
        try:_rc[p]=R.rec(p)
        except Exception:_rc[p]=None
    return _rc[p]
best=[]
for p in paths:
    m=rd(p)
    if not m or m.get("Class")!="Monster": continue
    bio=m.get("characterAttributeEquations"); b=rd(bio) if bio else None
    if not b or not b.get("characterLife"): continue
    cle=m.get("charLevel") or "charLevel*1"
    for spawn in range(1,36):
        _cl=R.evaleq(cle,spawn)
        if _cl is None: continue
        cl=int(_cl)
        if cl<1 or cl>70: continue
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
            if not sk: continue
            v=R.arr(sk.get("characterLifeModifier"),rk)
            if isinstance(v,(int,float)): s+=v
            v2=R.arr(sk.get("characterLife"),rk)
            if isinstance(v2,(int,float)): f+=v2
        for h,val in (("A35",(L+f)*(1+(s+35)/100)),("C50",(L+f)*(1+(s+50)/100)),
                      ("Dmul",(L+f)*(1+s/100)*1.5),("Eno",(L+f)*(1+s/100)),("raw",L+f)):
            if abs(val-4702.5)<25:
                best.append((round(val,1),h,p,cl,m.get("monsterClassification"),T.get(m.get("description"),"")))
best.sort()
for r in best: print(r)
print("n=",len(best))
