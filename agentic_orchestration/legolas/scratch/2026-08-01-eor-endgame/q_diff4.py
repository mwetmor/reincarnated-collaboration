#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base=ArzArchive(ROOT/"database/database.arz")
cands=[r for r in base.records if "balancingadjustment" in r and "sandbox" not in r and "backup" not in r]
print("campaign balancingadjustment records:", len(cands))
for c in sorted(cands):
    rec=base.read_record(c)
    lens={len(v) for v in rec.values() if isinstance(v,list)}
    print(f"  {c}  arraylens={sorted(lens)}")
print()
# which record does gameinfo/difficulty point at?
for t in ["records/game/gameinfo.dbr","records/game/gameengine.dbr"]:
    if t in base.records:
        rec=base.read_record(t)
        print("--",t)
        for k,v in sorted(rec.items()):
            if "adjust" in k.lower() or "difficult" in k.lower() or "level" in k.lower():
                print("   ",k,"=",str(v)[:200])
