import importlib.util, math
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G
PAK=R.pak_vals(); PL=PAK["characterLifeModifier"]
_rc={}
def rd(p):
    if p not in _rc:
        try:_rc[p]=R.rec(p)
        except Exception:_rc[p]=None
    return _rc[p]
def life_terms(p, cl):
    m=rd(p); b=rd(m["characterAttributeEquations"])
    L=R.evaleq(b["characterLife"], cl); smod=0.0; sflat=0.0; srcs=[]
    for i in range(1,13):
        sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
        if not sn: continue
        rk=R.evaleq(sl,cl) if isinstance(sl,str) else sl
        rk=0 if rk is None else int(rk)
        if rk<1: continue
        s=rd(sn)
        if not s or s.get("Class")!="Skill_Passive": continue
        v=R.arr(s.get("characterLifeModifier"),rk)
        if isinstance(v,(int,float)) and v: smod+=v; srcs.append((sn.split('/')[-1],rk,v))
        v2=R.arr(s.get("characterLife"),rk)
        if isinstance(v2,(int,float)) and v2: sflat+=v2
    return L,smod,sflat,srcs,m.get("charLevel"),m.get("monsterClassification")

paths=set()
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/creatures/enemies/") and "slith" in p and "/bios/" not in p:
            paths.add(p)
print(len(paths),"slith records")
T=R.tags()
for p in sorted(paths):
    m=rd(p)
    if not m or m.get("Class")!="Monster": continue
    nm=T.get(m.get("description"), m.get("description"))
    row=[]
    for cl in range(7,17):
        L,smod,sflat,srcs,cle,cls=life_terms(p,cl)
        if L is None: continue
        h1=(L+sflat)*(1+(smod+PL)/100)
        h2=(L+sflat)*(1+smod/100)*(1+PL/100)
        h3=(L+sflat)*(1+smod/100)
        row.append(f"{cl}:{h1:.0f}/{h2:.0f}/{h3:.0f}")
    print(f"{p.split('/')[-1]:38s} {str(nm)[:26]:27s} {cls} cle={cle}")
    print("      ", " ".join(row))
