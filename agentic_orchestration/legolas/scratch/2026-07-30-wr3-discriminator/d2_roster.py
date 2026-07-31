#!/usr/bin/env python3
"""D2 - what could produce a 260-274 single hit? Inverse arithmetic + encounter-history checks. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]
def get(n):
    for nm,a in ars:
        if n in a.records: return nm,a.read_record(n)
    return None,None

print("="*78)
print("A. ENCOUNTER-HISTORY CHECKS  (does the save say Warden Krieg was killed?)")
print("="*78)
for rn in ["records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr",
           "records/creatures/enemies/boss&quest/warden01.dbr",
           "records/creatures/enemies/boss&quest/dp_wardenphase2.dbr"]:
    nm,rec=get(rn)
    if rec is None:
        # try to find it
        cands=[r for _,a in ars for r in a.records if 'warden' in r.lower() and 'creatures' in r]
        print(f"  MISS {rn}; candidates: {cands[:8]}")
        continue
    print(f"  {rn.split('/')[-1]:28s} class={rec.get('monsterClassification')!r:12s} "
          f"charLevel={rec.get('charLevel')!r} nameTag={rec.get('description') or rec.get('monsterDisplayName')!r}")

print()
print("="*78)
print("B. PLAGUE WALKER (tagEnemyZombieG01) - the named lastMonsterHitBy entity")
print("="*78)
hits=[]
for nm,a in ars:
    for r in a.records:
        if a.record_type(r)!='Monster': continue
        rec=a.read_record(r)
        if rec.get('description')=='tagEnemyZombieG01' or rec.get('monsterDisplayName')=='tagEnemyZombieG01':
            hits.append((nm,r,rec))
for nm,r,rec in hits:
    print(f"  [{nm}] {r}")
    print(f"      class={rec.get('monsterClassification')!r} charLevel={rec.get('charLevel')!r}")
    sk=[(rec.get(f'skillName{i}'),rec.get(f'skillLevel{i}')) for i in range(1,25) if rec.get(f'skillName{i}')]
    for s,l in sk: print(f"        skill {s}  lvl={l}")
    for k in ('specialAttackSkillName','specialAttack2SkillName','specialAttack3SkillName','specialAttack4SkillName'):
        if rec.get(k): print(f"        {k} = {rec[k]}")
