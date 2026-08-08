#!/usr/bin/env python3
"""Overlay semantics: is an .arz record a WHOLE-RECORD replacement or a field patch?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import read, owners, merged
CASES=["records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr",
       "records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr",
       "records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr",
       "records/creatures/enemies/aetherialbloater_b01_summon.dbr",
       "records/creatures/enemies/faction/skeleton_a02_summon.dbr"]
for p in CASES:
    print(f"\n### {p}")
    prev=None
    for k in owners(p):
        r,_=read(p,which=k)
        fs=set(r)
        extra = "" if prev is None else f"  (+{len(fs-prev)} / -{len(prev-fs)} vs previous)"
        print(f"   [{k}] {len(fs)} fields{extra}")
        if prev is not None and (prev-fs):
            miss=sorted(prev-fs)
            print(f"        DROPPED: {miss[:8]}{' ...' if len(miss)>8 else ''}")
        prev=fs
print("\n\n### CONSEQUENCE CHECK — do bio / charLevel / armorbase change under WINNER-ONLY vs FIELD-MERGE?")
BODY={"Zantarin":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr",
 "Aleksander":"records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
 "Kubacabra":"records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr",
 "Galakros":"records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr",
 "Bileeater":"records/creatures/enemies/aetherialbloater_b01_summon.dbr",
 "DeathRevenant":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01_revenantsummon.dbr",
 "Shard":"records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr",
 "SkeletalArcher":"records/creatures/enemies/faction/skeleton_a02_summon.dbr"}
for n,p in BODY.items():
    w,_=read(p); m,_,o=merged(p)
    diffs=[k for k in ("characterAttributeEquations","charLevel","characterLifeModifier","skillName3","skillLevel3","skillName2","poolToSpawnOnDeath")
           if w.get(k)!=m.get(k)]
    print(f"  {n:16s} winner={o[-1]:6s} identical-on-key-fields={not diffs}  diffs={diffs}")
    if diffs:
        for k in diffs: print(f"        {k}: winner={w.get(k)!r}   merged={m.get(k)!r}")
