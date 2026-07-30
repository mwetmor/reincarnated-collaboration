#!/usr/bin/env python3
"""C3 — per-record table of every Skill_BuffAttackRadiusDrop, to read dropRadius/Variation semantics. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[ArzArchive(p) for p in ARZS]
def s(v):
    if isinstance(v,list): return f"[{v[0]}..{v[-1]}]"
    return str(v)
rows=[]
for p,a in zip(ARZS,ars):
    for r in a.records:
        t=a.record_type(r)
        if t and 'BuffAttackRadiusDrop' in t:
            rec=a.read_record(r)
            rows.append((r,rec))
print(f"{'record':78s} {'N':>4s} {'dropR':>7s} {'dropH':>6s} {'dropV':>6s} {'tgtR':>6s} {'int':>6s} {'dur':>6s} {'expl':>6s} {'gnd':>5s}")
for r,rec in sorted(rows, key=lambda x: x[0]):
    print(f"{r[-78:]:78s} {s(rec.get('projectileLaunchNumber')):>4s} {s(rec.get('dropRadius')):>7s} {s(rec.get('dropHeight')):>6s} {s(rec.get('dropVariation')):>6s} {s(rec.get('skillTargetRadius')):>6s} {s(rec.get('skillTargetInterval')):>6s} {s(rec.get('skillActiveDuration')):>6s} {s(rec.get('projectileExplosionRadius')):>6s} {s(rec.get('skillProjectileTargetGroundOnly')):>5s}")
