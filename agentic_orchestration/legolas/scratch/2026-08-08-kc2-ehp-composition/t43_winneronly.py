#!/usr/bin/env python3
"""Q5: re-read wave-160 pools WINNER-ONLY. Does the winning archive change levelVarianceEquation?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import read, owners, merged
POOLS={"p01":"records/proxies/poolsboss/nemesis_all.dbr",
 "p02":"records/proxies/poolsbossgdx1/nemesis_all_noaetherialvanguard.dbr",
 "p03":"records/proxies/poolsbossgdx1/nemesis_wendigooraetherialvanguard.dbr",
 "p04a":"records/proxies/poolsbossgdx1/aetherialcolossus_galakros.dbr",
 "p04b":"records/proxies/poolsbossgdx2/korvaaktombguardian.dbr",
 "p06":"records/proxies/poolsherogdx1/wendigocannibal_hero.dbr"}
for t,p in POOLS.items():
    o=owners(p)
    print(f"\n### {t} {p}  owners={o}")
    for k in o:
        r,_=read(p,which=k)
        lv={f:v for f,v in r.items() if "levelVariance" in f}
        nm={f:v for f,v in r.items() if f.startswith("name")}
        print(f"   [{k}] {len(r)} fields | levelVariance={lv} | n_names={len(nm)}")
    w,_=read(p)
    print(f"   WINNER({o[-1]}): names={sorted((f,v) for f,v in w.items() if f.startswith('name'))}")
