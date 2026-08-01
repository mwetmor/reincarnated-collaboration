#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
b=ArzArchive(ROOT/"database/database.arz")
hits=[r for r in b.records if "skeletonkey" in r.lower() or "skeleton_key" in r.lower()]
print("skeleton key records:",hits)
for h in hits[:4]:
    rec=b.read_record(h); print("--",h)
    for k,v in sorted(rec.items()):
        if k in ("itemLevel","levelRequirement","itemClassification","itemNameTag","itemText","Class","description","itemCostName","maxStackSize"): print("   ",k,"=",v)
print()
sot=[r for r in b.records if "stepsoftorment" in r.lower()]
print("stepsoftorment records:",len(sot))
for r in sorted(sot): print("  ",r)
print()
for eq in ("lv3_strong","lv4_champion"):
    rec=b.read_record(f"records/proxies/{eq}.dbr")
    print(eq, {k:v for k,v in rec.items() if "quation" in k or "Equation" in k or k.startswith("level")})
