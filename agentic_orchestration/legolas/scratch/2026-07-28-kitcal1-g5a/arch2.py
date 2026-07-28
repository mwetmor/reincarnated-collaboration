import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G
ps=set()
for a in R.ARCS:
    for p in G.arc(a).records:
        if "archetypes/" in p and "passivestatmodifier" in p: ps.add(p)
for p in sorted(ps):
    r=R.rec(p)
    lm=r.get("characterLifeModifier"); lf=r.get("characterLife")
    def sl(v): return (v[:8] if isinstance(v,list) else v)
    print(f"{p.split('/')[-1]:42s} Class={r.get('Class')} lifeMod={sl(lm)} lifeFlat={sl(lf)}")
