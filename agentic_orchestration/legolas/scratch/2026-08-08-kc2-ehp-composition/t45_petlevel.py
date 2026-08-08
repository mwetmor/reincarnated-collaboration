#!/usr/bin/env python3
"""Q3/Q5: the summon-level rule. Any petLevel field? Any other record bearing the Bileeater tag?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import read, owners, archives
print("== records whose description == tagGDX1EnemyAetherialBloater_B01 / tagEnemySkeletonC04 / ..._Crystal ==")
WANT={"tagGDX1EnemyAetherialBloater_B01","tagEnemySkeletonC04","tagGDX1Nemesis_Aetherial01_Crystal","tagEnemySkeletonA02"}
for k,a in archives():
    for r in a.records:
        rec=a.read_record(r)
        if rec.get("description") in WANT:
            print(f"  [{k}] {r}\n       desc={rec.get('description')} bio={(rec.get('characterAttributeEquations') or '').split('/')[-1]} "
                  f"charLevel={rec.get('charLevel')!r} cls={rec.get('monsterClassification')!r} lifemod={rec.get('characterLifeModifier')!r}")
print("\n== summon skills: every field mentioning level / pet ==")
for s in ("records/skills/nonplayerskillsgdx1/bossskills/galakros_summonbloater_secondary.dbr",
          "records/skills/nonplayerskills/bossskills/nemesis/zantarin_summonrevenant.dbr",
          "records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_summonshard.dbr",
          "records/skills/nonplayerskills/bossskills/nemesis/zantarin_reactivesummonskeletalarcher.dbr"):
    r,_=read(s); print(f"\n  {s}")
    for f in sorted(r):
        if any(t in f.lower() for t in ("level","pet","spawn")) and r[f] not in (None,0,0.0,False,''):
            v=r[f]; v=(str(v)[:60]+"...") if len(str(v))>60 else v
            print(f"     {f:32s} = {v!r}")
