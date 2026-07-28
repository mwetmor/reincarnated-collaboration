import importlib.util
spec = importlib.util.spec_from_file_location("g5a", "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-07-28-kitcal1-g5a/g5a_resolve.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
for p in ["records/creatures/enemies/trollhalfswamp_b02.dbr","records/creatures/enemies/trollhalfswamp_a02.dbr","records/creatures/enemies/slitha_melee_b01.dbr"]:
    m=R.rec(p)
    print(p.split('/')[-1], m.get("monsterClassification"), [(m.get(f"skillName{i}","").split('/')[-1], m.get(f"skillLevel{i}")) for i in range(1,7) if m.get(f"skillName{i}")])
print()
# scan Primordian's skills for ANY field == -15 at resolved rank
m=R.rec("records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr")
for i in range(1,13):
    sn=m.get(f"skillName{i}"); sl=m.get(f"skillLevel{i}")
    if not sn or not R.has(sn): continue
    rk=R.evaleq(sl,13) if isinstance(sl,str) else sl
    rk=0 if rk is None else int(rk)
    if rk<1: continue
    s=R.rec(sn)
    for k,v in s.items():
        val=R.arr(v,rk)
        if isinstance(val,(int,float)) and abs(val+15)<1e-9:
            print("  -15 FOUND", sn.split('/')[-1], "rank",rk, k, val)
print("scan done")
