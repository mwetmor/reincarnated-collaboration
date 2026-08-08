#!/usr/bin/env python3
"""Q4: who references the deathspawn pool, and does the survival overlay keep it?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find, archives, read
TGT="records/proxies/poolsdeathspawngdx1/dp_nemesisbeastp01.dbr"
print(f"### {TGT}")
rec,prov,own = merged(TGT)
for k in sorted(rec): print(f"   {k:34s} = {rec[k]!r} [{prov[k]}]")
print("\n### who references it?")
for k,a in archives():
    for r in a.records:
        rr=a.read_record(r)
        for f,v in rr.items():
            vals=v if isinstance(v,list) else [v]
            for x in vals:
                if isinstance(x,str) and x.lower()==TGT:
                    print(f"   [{k}] {r}   field={f}")
print("\n### nemesis_beast_01_p1 — PER-ARCHIVE deathspawn/pool fields (is the wiring overlaid away?)")
P="records/creatures/enemies/nemesis/nemesis_beast_01_p1.dbr"
for k in ("gdx1","sm1"):
    r,_=read(P, which=k)
    if not r: continue
    print(f"  --[{k}] fields containing 'spawn'/'pool'/'death':")
    for f in sorted(r):
        if any(t in f.lower() for t in ("spawn","pool","death")):
            print(f"      {f:34s} = {r[f]!r}")
print("\n### merged view (overlay winner):")
for f in sorted(rec2 := merged(P)[0]):
    if any(t in f.lower() for t in ("spawn","pool","death")):
        print(f"      {f:34s} = {rec2[f]!r} [{merged(P)[1][f]}]")
print("\n### deathspawn pools generally -- template + how the engine finds them")
for p in sorted(find("poolsdeathspawn"))[:12]:
    r,pr,o=merged(p); print(f"   {p} owners={o} name1={r.get('name1')!r} spawnMin={r.get('spawnMin')!r} spawnMax={r.get('spawnMax')!r}")
