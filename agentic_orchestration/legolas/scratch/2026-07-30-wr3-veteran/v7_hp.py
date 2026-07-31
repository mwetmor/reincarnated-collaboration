#!/usr/bin/env python3
"""V7 - Primordian HP chain vs charLevel, with/without Veteran; U-4 adjudication. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
BOSS="records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr"
rec=a.read_record(BOSS)
print("=== boss record: life/level/skill wiring ===")
for k in sorted(rec):
    if re.search(r'(charLevel|characterLife|characterMana|skillName|skillLevel|monsterClassification)',k):
        print(f"   {k:26s} {rec[k]}")
print()

def arr(r,k,rank):
    v=r.get(k)
    if v is None: return 0.0
    if isinstance(v,list): return float(v[min(rank-1,len(v)-1)])
    return float(v)

def ev(expr,cl):
    if expr is None: return None
    try: return int(eval(str(expr).replace("charLevel",str(cl))))
    except Exception: return None

SKILLS=[]
for i in range(1,25):
    s=rec.get(f'skillName{i}')
    if s: SKILLS.append((i,s,rec.get(f'skillLevel{i}')))
print("=== skills and their life contributions by rank ===")
for i,s,lv in SKILLS:
    if s not in a.records: print(f"   slot{i} {s}  (NOT IN BASE DB)"); continue
    sr=a.read_record(s)
    fields={k:v for k,v in sr.items() if 'characterLife' in k or 'characterMana' in k}
    if fields:
        print(f"   slot{i} {s.split('nonplayerskills/')[-1]}  lvExpr={lv}")
        for k,v in fields.items():
            vv = v if not isinstance(v,list) else f"array[{len(v)}] {v[:6]}...{v[-2:]}"
            print(f"        {k:34s} {vv}")
print()

# pak + mutator
pak=a.read_record("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")
vet=a.read_record("records/game/balancingadjustment_challengemode_enemies01.dbr")
PAK_LIFE=pak['characterLifeModifier'][0]      # Normal, 1 player
PAK_LIFEMULT=pak['characterLifeMultModifier'][0]
VET_LIFE=vet['characterLifeModifier']
print(f"pak Normal/1p characterLifeModifier={PAK_LIFE}  characterLifeMultModifier={PAK_LIFEMULT}")
print(f"Veteran characterLifeModifier={VET_LIFE}")
print()

MEAS=15822.0
print("="*104)
print(f"HP PREDICTION vs charLevel (measured greatestMonsterKilledLifeAndMana = {MEAS:.0f})")
print("="*104)
print(f"  {'cl':>3s} {'base life':>10s} {'poolMod%':>9s} {'x(1+pool)':>10s} {'xPak(1.5)':>11s} {'ratio':>7s} "
      f"| {'+Veteran':>11s} {'ratio':>7s}")
for cl in range(10,25):
    baselife=float(rec.get('characterLife') or 0)
    if isinstance(rec.get('characterLife'),list): baselife=float(rec['characterLife'][0])
    pool=0.0; base_from_skill=0.0
    for i,s,lv in SKILLS:
        if s not in a.records: continue
        sr=a.read_record(s)
        rk=max(1, ev(lv,cl) or 1)
        pool+=arr(sr,'characterLifeModifier',rk)
        base_from_skill+=arr(sr,'characterLife',rk)
    B=baselife+base_from_skill
    m=B*(1+pool/100.0)*(1+PAK_LIFE/100.0)
    mv=m*(1+VET_LIFE/100.0)
    print(f"  {cl:3d} {B:10.1f} {pool:9.1f} {B*(1+pool/100):10.1f} {m:11.1f} {m/MEAS:7.3f} | {mv:11.1f} {mv/MEAS:7.3f}")
print()
print("NOTE: 'base life' includes characterLife from the creature record AND from any rank-keyed skill.")
print("      Mana is excluded here; the save field is lifeAndMana, so a mana term may be owed.")
