import importlib.util, json
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
ge = R.rec("records/game/gameengine.dbr")
for k,v in sorted(ge.items()):
    print("GE", k, "=", v)
print()
um = R.rec("records/game/balancingadjustment_ultramode_enemies01.dbr")
for k,v in sorted(um.items()):
    if v in (0,0.0,False,"",None): continue
    if isinstance(v,list) and not any(v): continue
    print("ULTRA", k, "=", v)
