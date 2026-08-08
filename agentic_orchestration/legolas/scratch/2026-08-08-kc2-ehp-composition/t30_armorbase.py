#!/usr/bin/env python3
"""Q2: the deviating bodies -- read each body's skill-3 passive characterLifeModifier array."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged
BODY_REC = {
 "Zantarin":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr",
 "Aleksander":"records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
 "Kubacabra":"records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr",
 "Galakros":"records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr",
 "Bileeater":"records/creatures/enemies/aetherialbloater_b01_summon.dbr",
 "DeathRevenant":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01_revenantsummon.dbr",
 "Shard":"records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr",
 "SkeletalArcher":"records/creatures/enemies/faction/skeleton_a02_summon.dbr",
}
ARRS={}
for b,p in BODY_REC.items():
    rec,prov,own = merged(p)
    print(f"\n### {b}   cls={rec.get('monsterClassification')!r}  ownLifeMod={rec.get('characterLifeModifier')!r}")
    for i in range(1,40):
        s=rec.get(f"skillName{i}")
        if not s: continue
        sr,sp,so = merged(s)
        lm = sr.get("characterLifeModifier")
        if lm in (None,0.0,0): continue
        lvl = rec.get(f"skillLevel{i}")
        print(f"   skill{i} lvl={lvl!r}  {s}")
        if isinstance(lm,list):
            print(f"        characterLifeModifier[{len(lm)}] [{sp['characterLifeModifier']}] "
                  f"idx100..120={[int(x) for x in lm[100:121]]}")
            ARRS[(b,s)]=lm
        else: print(f"        characterLifeModifier = {lm!r}")
json.dump({f"{k[0]}|{k[1]}":v for k,v in ARRS.items()}, open("t30_arrays.json","w"))
