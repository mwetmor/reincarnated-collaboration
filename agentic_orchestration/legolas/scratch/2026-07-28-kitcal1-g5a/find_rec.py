import importlib.util, sys, json
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
G = R.G
targets = set(sys.argv[1:])
for a in R.ARCS:
    arc = G.arc(a)
    for p in arc.records:
        if not p.startswith("records/creatures/"): continue
        try: r = arc.read_record(p)
        except Exception: continue
        d = r.get("description")
        if d in targets:
            print(a, p, d, r.get("monsterClassification"), r.get("charLevel"), r.get("characterAttributeEquations"))
