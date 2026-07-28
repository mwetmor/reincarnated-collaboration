import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
a=R.rec("records/skills/nonplayerskills/passive/armorbase03.dbr")
b=R.rec("records/skills/nonplayerskills/passive/armorbase05.dbr")
keys=sorted(set(a)|set(b))
for k in keys:
    va,vb=R.arr(a.get(k),13),R.arr(b.get(k),13)
    if va!=vb: print(f"  {k}: ab03={va}  ab05={vb}")
