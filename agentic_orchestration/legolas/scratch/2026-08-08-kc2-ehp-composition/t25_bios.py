#!/usr/bin/env python3
"""Q2/Q3: resolve the summon creature records + their bios + charLevel forms."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners
TAGS=json.load(open("t23_tags.json"))
SUM = {
 "F5? Death Revenant (Zantarin pet)":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01_revenantsummon.dbr",
 "F7? Skeletal Archer (Zantarin pet)":"records/creatures/enemies/faction/skeleton_a02_summon.dbr",
 "F6? Aleksander's Shard":"records/skills/nonplayerskillsgdx1/bossskills/nemesis/aetherialvanguard_crystal.dbr",
 "F4? Aetherial Bileeater (Galakros pet)":"records/creatures/enemies/aetherialbloater_b01_summon.dbr",
 "     Aetherial bloater C01 (Galakros pet2)":"records/creatures/enemies/aetherialbloater_c01_summon.dbr",
}
for lab,p in SUM.items():
    rec,prov,own = merged(p)
    if not rec: print(f"!! MISSING {p}"); continue
    d=rec.get("description")
    print("="*100); print(f"{lab}\n  {p}  owners={own}")
    print(f"  desc={d!r} -> {TAGS.get(d,'?')!r}")
    for k in ("charLevel","monsterClassification","characterAttributeEquations","characterLifeModifier",
              "characterLife","minLevel","maxLevel","templateName","petBonusName","isPet","characterLevel"):
        if k in rec: print(f"  {k:34s} = {rec[k]!r} [{prov[k]}]")
    b=rec.get("characterAttributeEquations")
    if b:
        br,bp,bo = merged(b)
        print(f"  --BIO {b}  owners={bo}")
        for k in sorted(br):
            if "ife" in k or "evel" in k: print(f"      {k:34s} = {br[k]!r} [{bp[k]}]")
print("="*100); print("ALL BIOS ON BOARD — full life fields")
BIOS=["records/creatures/enemies/bios/bio_boss_nemesis_01.dbr",
 "records/creatures/enemies/bios/bio_boss_nemesis3phase_01.dbr",
 "records/creatures/enemies/bios/bio_boss_nemesis3phase_02.dbr",
 "records/creatures/enemies/bios/bio_boss_nemesis3phase_03.dbr",
 "records/creatures/enemies/bios/bio_boss_aetherial_colossusgalakros.dbr",
 "records/creatures/enemies/bios/bio_hero_standard_01.dbr"]
for b in BIOS:
    br,bp,bo=merged(b); print(f"\n-- {b} owners={bo}")
    for k in sorted(br):
        if "ife" in k.lower(): print(f"     {k:36s} = {br[k]!r} [{bp[k]}]")
