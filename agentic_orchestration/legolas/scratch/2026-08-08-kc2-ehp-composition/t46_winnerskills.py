#!/usr/bin/env python3
"""Re-verify the summon wiring under WINNER-ONLY overlay semantics (engine model)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import read, owners
for lab,p in (("Zantarin","records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr"),
              ("Aleksander","records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr"),
              ("Galakros","records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr")):
    r,k=read(p); print(f"\n### {lab}  WINNER=[{k}]  (owners={owners(p)})")
    for i in range(1,40):
        s=r.get(f"skillName{i}")
        if not s: continue
        sr,_=read(s); cls=sr.get("Class","")
        if "Spawn" in cls or "Pet" in cls:
            print(f"   skill{i} lvl={r.get(f'skillLevel{i}')!r} Class={cls}")
            for kk in ("spawnObjects","spawnObjects2","petLimit","petBurstSpawn"):
                if sr.get(kk) not in (None,0,0.0,''): print(f"        {kk} = {sr[kk]!r}")
    # armorbase used
    for i in range(1,40):
        s=r.get(f"skillName{i}")
        if s and "armorbase" in s: print(f"   [armorbase] skill{i} = {s}  lvl={r.get(f'skillLevel{i}')!r}")
print("\n### armorbase per measured body (WINNER-ONLY)")
for n,p in (("Bileeater","records/creatures/enemies/aetherialbloater_b01_summon.dbr"),
            ("Bileeater-nonsummon","records/creatures/enemies/aetherialbloater_b01.dbr"),
            ("DeathRevenant","records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01_revenantsummon.dbr"),
            ("Shard","records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr"),
            ("SkeletalArcher","records/creatures/enemies/faction/skeleton_a02_summon.dbr")):
    r,k=read(p); ab=[(i,r[f"skillName{i}"],r.get(f"skillLevel{i}")) for i in range(1,40)
                     if r.get(f"skillName{i}") and "armorbase" in r[f"skillName{i}"]]
    print(f"  {n:20s} [{k}] charLevel={r.get('charLevel')!r} bio={(r.get('characterAttributeEquations') or '').split('/')[-1]} armorbase={ab}")
