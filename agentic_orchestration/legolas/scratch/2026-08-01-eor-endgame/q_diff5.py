#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")
recs={t:a.read_record(f"records/game/balancingadjustment_survivalmode_enemies{n}.dbr")
      for n,t in [("01","Aspirant"),("02","Challenger"),("03","Gladiator")]}
def steps(v):
    out=[];prev=None
    for i,x in enumerate(v):
        if x!=prev: out.append((i+1,x)); prev=x
    return out
for key in ("spawnChampionMinAdj","spawnChampionMaxAdj","spawnMinAdj","spawnMaxAdj"):
    print(f"\n### {key} (index+1 = wave, inferred)")
    for t,r in recs.items():
        print(f"  {t:11}: {steps(r[key])}")
print("\n### selected modifiers at waves 150 / 160 / 170 (1-based)")
for key in ("characterLifeModifier","totalDamageModifier","offensiveAbilityModifier","defensiveAbilityModifier",
            "physicalResistanceModifier","armorModifier","armorAbsorptionModifier","retaliationTotalDamageModifier","skillCooldownReduction"):
    if key not in recs["Gladiator"]: continue
    line=[]
    for t,r in recs.items():
        v=r[key]
        line.append(f"{t}={[v[i-1] for i in (150,160,170)]}")
    print(f"  {key:34} " + " | ".join(line))
print("\n### gameengine monsterLevelGapFixer + all keys containing 'level'")
b=ArzArchive(ROOT.parent/"grim-dawn-edition-II-20260724/database/database.arz")
r=b.read_record("records/game/gameengine.dbr")
for k,v in sorted(r.items()): print("   ",k,"=",str(v)[:160])
