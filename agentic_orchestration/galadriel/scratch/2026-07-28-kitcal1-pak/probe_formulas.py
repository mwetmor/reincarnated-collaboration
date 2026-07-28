import importlib.util, pathlib, json, sys
G5 = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
spec = importlib.util.spec_from_file_location("g5a", G5)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
for p in ["records/game/combatformulas.dbr", "records/game/gameengine.dbr"]:
    r = M.rec(p)
    print("=====", p, len(r))
    for k in sorted(r):
        v = r[k]
        if isinstance(v, list) and len(v) > 14:
            v = str(v[:6]) + f"...(n={len(v)})"
        print(f"  {k} = {v}")
