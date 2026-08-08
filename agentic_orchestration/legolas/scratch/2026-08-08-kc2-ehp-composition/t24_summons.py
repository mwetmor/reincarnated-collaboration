#!/usr/bin/env python3
"""Q3: are F4-F7 SUMMONS? Trace summoner skill -> spawned creature record -> bio."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners, find
TAGS=json.load(open("t23_tags.json"))
def nm(t): return TAGS.get(t, t)

SUMMONERS = {
 "Zantarin  (nemesis_orderdeathsvigil_01)":"records/creatures/enemies/nemesis/nemesis_orderdeathsvigil_01.dbr",
 "Aleksander(nemesis_aetherialvanguard_01)":"records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
 "Galakros  (aetherialcolossus_galakros)":"records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr",
 "Kubacabra (nemesis_beast_01_p1)":"records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr",
}
for label,p in SUMMONERS.items():
    rec,prov,own = merged(p)
    print("="*100); print(f"{label}\n  {p}  owners={own}")
    print(f"  desc={rec.get('description')} -> {nm(rec.get('description',''))!r}")
    print(f"  charLevel={rec.get('charLevel')!r} [{prov.get('charLevel')}]  cls={rec.get('monsterClassification')!r}")
    print(f"  levelRequirement={rec.get('levelRequirement')!r}  monsterLevel*={{k:v for k,v in rec.items() if 'evel' in k}}")
    for k in sorted(rec):
        if 'evel' in k: print(f"     [lvl-field] {k} = {rec[k]!r} [{prov[k]}]")
    for i in range(1,40):
        s=rec.get(f"skillName{i}")
        if not s: continue
        sl=rec.get(f"skillLevel{i}")
        srec,sprov,sown = merged(s)
        cls=srec.get("Class") or srec.get("skillClass")
        tgt = {k:v for k,v in srec.items() if 'pet' in k.lower() or 'spawn' in k.lower() or 'summon' in k.lower()}
        interesting = srec.get("petBonusName") or srec.get("spawnObjects") or srec.get("petObjects")
        print(f"   skill{i:<2} lvl={sl!r} {s}")
        print(f"        Class={cls!r}")
        if tgt:
            for k,v in sorted(tgt.items()): print(f"        {k} = {v!r}")
