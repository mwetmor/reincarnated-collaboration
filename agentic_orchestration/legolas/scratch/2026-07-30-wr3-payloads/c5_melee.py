#!/usr/bin/env python3
"""C5 — melee chain: boss passives at their derived ranks. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]
def get(n):
    for nm,a in ars:
        if n in a.records: return nm,a.read_record(n)
    return None,None
targets=[("records/skills/nonplayerskills/passive/damage_totaladjuster.dbr",2),
         ("records/skills/nonplayerskills/passive/damagebase_physical04.dbr",16),
         ("records/skills/nonplayerskills/bossskills/primordian_passive.dbr",5),
         ("records/skills/nonplayerskills/passive/armorbase05.dbr",16),
         ("records/skills/nonplayerskills/passive/resists_heroboss.dbr",3)]
def interesting(v):
    if v is False or v==0 or v==0.0 or v=='': return False
    if isinstance(v,list): return any(x not in (0,0.0,False,'') for x in v)
    return True
for rn,rank in targets:
    nm,rec=get(rn)
    print(f"=== {rn} [{nm}]  RANK {rank} (idx {rank-1})")
    for k in sorted(rec):
        v=rec[k]
        if not interesting(v): continue
        if isinstance(v,list):
            i=min(rank-1,len(v)-1)
            print(f"    {k:44s} rank{rank}={v[i]!r}   (len={len(v)}, r1={v[0]!r})")
        else:
            print(f"    {k:44s} {v!r}")
    print()
