import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G = R.G
# list all records under records/game/
seen={}
for a in R.ARCS:
    for p in G.arc(a).records:
        if p.startswith("records/game/"): seen.setdefault(p,[]).append(a)
for p,v in sorted(seen.items()): print(p, v)
