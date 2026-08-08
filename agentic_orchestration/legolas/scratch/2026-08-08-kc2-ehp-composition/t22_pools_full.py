#!/usr/bin/env python3
"""Q1: FULL wave-160 pool-slot enumeration -> actual DBR records, with charLevel/bio/class/name-tag."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners, find, read

POOLS = {
 "p01": "records/proxies/poolsboss/nemesis_all.dbr",
 "p02": "records/proxies/poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr",
 "p03": "records/proxies/poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr",
 "p04a":"records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr",
 "p04b":"records/proxies/poolsbossgdx2/korvaaktombguardian.dbr",
 "p06": "records/proxies/poolsherogdx1/wendigocannibal_hero.dbr",
}
rows=[]
for tag,p in POOLS.items():
    rec,prov,own = merged(p)
    print("="*100); print(f"{tag}  {p}   owners={own}")
    # print all pool-level scalars
    for f in sorted(rec):
        if not (f.startswith("name") or f.startswith("weight") or f.startswith("minPlayerLevel")
                or f.startswith("levelVarianceEquation") or f.startswith("limit")):
            print(f"   [pool] {f:44s} = {rec[f]!r}  [{prov[f]}]")
    for pref in ("name","nameChampion"):
        for i in range(1,40):
            v=rec.get(f"{pref}{i}")
            if not v: continue
            paths = v if isinstance(v,list) else [v]
            lvp = "levelVarianceEquation" if pref=="name" else "levelVarianceEquationChampion"
            for pp in paths:
                if not pp: continue
                mr,mp,mo = merged(pp)
                rows.append(dict(pool=tag,slot=f"{pref}{i}",rec=pp.lower(),
                    weight=rec.get(("weight" if pref=="name" else "weightChampion")+str(i)),
                    minPL=rec.get("minPlayerLevel"+str(i)),
                    lveq=rec.get(f"{lvp}{i}"),
                    charLevel=mr.get("charLevel"), bio=mr.get("characterAttributeEquations"),
                    cls=mr.get("monsterClassification"), lifemod=mr.get("characterLifeModifier"),
                    nametag=mr.get("description") or mr.get("monsterName"),
                    owners=mo, prov_cl=mp.get("charLevel"), prov_bio=mp.get("characterAttributeEquations")))
                print(f"   {pref}{i:<2} w={rec.get(('weight' if pref=='name' else 'weightChampion')+str(i))!r:>6} "
                      f"minPL={rec.get('minPlayerLevel'+str(i))!r:>5} lv={rec.get(f'{lvp}{i}')!r}")
                print(f"        -> {pp}")
                print(f"           charLevel={mr.get('charLevel')!r} [{mp.get('charLevel')}]  "
                      f"cls={mr.get('monsterClassification')!r}  lifemod={mr.get('characterLifeModifier')!r}")
                print(f"           bio={mr.get('characterAttributeEquations')!r} [{mp.get('characterAttributeEquations')}]  "
                      f"desc={mr.get('description')!r}  owners={mo}")
json.dump(rows, open("t22_pools.json","w"), indent=1, default=str)
print(f"\n\n{len(rows)} slot rows -> t22_pools.json")
