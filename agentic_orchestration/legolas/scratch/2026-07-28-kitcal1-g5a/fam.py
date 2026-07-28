import importlib.util, sys
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G; T=R.tags()
def terms(p,cl):
    m=R.rec(p); b=R.rec(m["characterAttributeEquations"])
    L=R.evaleq(b["characterLife"],cl); s=0.0;f=0.0
    for i in range(1,13):
        sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
        if not sn or not R.has(sn): continue
        rk=R.evaleq(sl,cl) if isinstance(sl,str) else sl
        rk=0 if rk is None else int(rk)
        if rk<1: continue
        sk=R.rec(sn)
        if sk.get("Class")!="Skill_Passive": continue
        v=R.arr(sk.get("characterLifeModifier"),rk)
        if isinstance(v,(int,float)): s+=v
        v2=R.arr(sk.get("characterLife"),rk)
        if isinstance(v2,(int,float)): f+=v2
    return m,L,s,f
pats=sys.argv[1].split(",")
lo,hi=int(sys.argv[2]),int(sys.argv[3])
seen=set()
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/creatures/enemies/") and any(x in p for x in pats) and "summon" not in p and "/bios/" not in p:
            seen.add(p)
for p in sorted(seen):
    try: m,L,s,f=terms(p,10)
    except Exception: continue
    if m.get("Class")!="Monster": continue
    row=[]
    for cl in range(lo,hi+1):
        m,L,s,f=terms(p,cl)
        if L is None: continue
        row.append(f"{cl}:{(L+f)*(1+(s+50)/100):.0f}")
    print(f"{p.split('/')[-1]:34s} {str(T.get(m.get('description'),''))[:24]:25s} {str(m.get('monsterClassification')):9s} {m.get('charLevel'):16s} "+" ".join(row))
