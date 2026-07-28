import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G=R.G
seen=set()
for a in R.ARCS:
    for p in G.arc(a).records:
        if "archetype" in p.lower(): seen.add((a,p))
for a,p in sorted(seen): print(a,p)
