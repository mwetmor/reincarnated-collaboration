#!/usr/bin/env python3
"""N4 — for ProjectileRing skills, census projectileExplosionRadius + linked projectile actorRadius/velocity/distance. READ-ONLY."""
import pathlib, sys
from collections import Counter
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[ArzArchive(p) for p in ARZS]
def get(n):
    for a in ars:
        if n in a.records: return a.read_record(n)
    return None
er=Counter(); pr=Counter(); miss=0
for a in ars:
    for r in list(a.records):
        t=a.record_type(r)
        if t and 'ProjectileRing' in t:
            rec=a.read_record(r)
            v=rec.get('projectileExplosionRadius',None)
            er[v if not isinstance(v,list) else 'LIST']+=1
            p=rec.get('skillProjectileName')
            if p:
                prec=get(p)
                if prec: pr[(prec.get('actorRadius'),prec.get('projectileVelocity'),prec.get('projectileDistance'),prec.get('explodeOnMiss'),prec.get('notificationRadius'))]+=1
                else: miss+=1
print("projectileExplosionRadius histogram across ProjectileRing skills:")
for k,v in sorted(er.items(), key=lambda x:-x[1])[:18]: print(f"  {k!r:12s} {v}")
print(f"\nlinked-projectile (actorRadius, velocity, distance, explodeOnMiss, notificationRadius) top 15  [unresolved projectiles: {miss}]")
for k,v in sorted(pr.items(), key=lambda x:-x[1])[:15]: print(f"  {k}  x{v}")
