#!/usr/bin/env python3
"""N3 — census every Skill_AttackProjectileRing / fan-like record: launchNumber vs launchRotation. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
rows=[]
for p in ARZS:
    a=ArzArchive(p)
    for r in a.records:
        t=a.record_type(r)
        if t and 'ProjectileRing' in t:
            rec=a.read_record(r)
            n=rec.get('projectileLaunchNumber'); rot=rec.get('projectileLaunchRotation')
            rows.append((p.name,r,n,rot))
from collections import Counter
print(f"total ProjectileRing records: {len(rows)}")
print("\n(launchNumber, launchRotation) histogram:")
for k,v in sorted(Counter((n if not isinstance(n,list) else tuple(n)[:1], rot) for _,_,n,rot in rows).items(), key=lambda x:-x[1]):
    print(f"  {str(k):28s} {v}")
print("\nrecords with launchRotation != 360:")
for nm,r,n,rot in rows:
    if rot != 360.0: print(f"  {nm}\t{r}\tN={n}\trot={rot}")
