import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
for k,p in [("BASE","database/database.arz"),("sm_mod","mods/survivalmode/database/SurvivalMode.arz")]:
    a=ArzArchive(ROOT/p)
    hits=[r for r in a.records if "merit" in r.lower()]
    print("="*60); print(k,"merit hits:",len(hits))
    for h in sorted(hits):
        print("  ",h)
    for h in sorted(hits):
        rec=a.read_record(h)
        print("\n-- ",h)
        for kk,vv in sorted(rec.items()): print("     %s = %s"%(kk,str(vv)[:200]))
