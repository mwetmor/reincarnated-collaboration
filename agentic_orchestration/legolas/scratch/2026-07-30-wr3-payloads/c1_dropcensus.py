#!/usr/bin/env python3
"""C1 — census Skill_BuffAttackRadiusDrop: launchNumber, usesAllDamage, groundOnly, explosionRadius. READ-ONLY."""
import sys, pathlib
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
rows=[]
for p,a in zip(ARZS,ars):
    for r in a.records:
        t=a.record_type(r)
        if t and 'BuffAttackRadiusDrop' in t:
            rec=a.read_record(r)
            rows.append((p.name,r,rec))
print(f"total Skill_BuffAttackRadiusDrop records: {len(rows)}")
f=lambda rec,k,d=None: rec.get(k,d)
print("\n--- histograms ---")
for key in ('projectileLaunchNumber','projectileUsesAllDamage','skillProjectileTargetGroundOnly',
            'projectileExplosionRadius','skillTargetInterval','skillActiveDuration','dropHeight',
            'dropRadius','dropVariation','skillTargetRadius','skillTargetNumber','targetingMode'):
    c=Counter()
    for _,_,rec in rows:
        v=rec.get(key,'<ABSENT>')
        if isinstance(v,list): v=f'LIST[{v[0]}..{v[-1]}]'
        c[v]+=1
    print(f"\n{key}:")
    for k,v in sorted(c.items(), key=lambda x:-x[1])[:14]: print(f"   {k!r:26s} {v}")
print("\n--- CROSSTAB: groundOnly=True records, does explosionRadius exist? ---")
gt=[(n,r,rec) for n,r,rec in rows if rec.get('skillProjectileTargetGroundOnly') is True]
print(f"groundOnly=True: {len(gt)}")
noexp=[(n,r) for n,r,rec in gt if not rec.get('projectileExplosionRadius')]
print(f"   of those, projectileExplosionRadius absent/0: {len(noexp)}")
for n,r in noexp[:20]: print(f"      {n}\t{r}")
gf=[(n,r,rec) for n,r,rec in rows if rec.get('skillProjectileTargetGroundOnly') is not True]
print(f"groundOnly != True: {len(gf)}")
noexp2=[(n,r) for n,r,rec in gf if not rec.get('projectileExplosionRadius')]
print(f"   of those, projectileExplosionRadius absent/0: {len(noexp2)}")
for n,r in noexp2[:20]: print(f"      {n}\t{r}")
print("\n--- CROSSTAB: launchNumber>1 vs projectileUsesAllDamage ---")
c=Counter()
for _,_,rec in rows:
    n=rec.get('projectileLaunchNumber',1)
    if isinstance(n,list): n=n[0]
    c[(n>1, rec.get('projectileUsesAllDamage','<ABSENT>'))]+=1
for k,v in sorted(c.items(), key=lambda x:-x[1]): print(f"   multi={k[0]!s:6s} usesAllDamage={k[1]!r:10s} {v}")
print("\n--- linked projectile props for groundOnly drops ---")
pc=Counter()
for _,_,rec in rows:
    pn=rec.get('skillProjectileName')
    if not pn: continue
    pr=get(pn)
    if pr: pc[(pr.get('Class'),pr.get('actorRadius'),pr.get('projectileVelocity'),pr.get('projectileDistance'),pr.get('useTrajectory'),pr.get('launchAngle'))]+=1
for k,v in sorted(pc.items(), key=lambda x:-x[1])[:15]: print(f"   {k}  x{v}")
