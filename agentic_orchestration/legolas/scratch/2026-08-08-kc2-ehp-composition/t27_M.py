#!/usr/bin/env python3
"""Q2: source M = 11.29 from the DB adjustment layer. Enumerate every life-modifier array."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners, find
paths = sorted(set(find("balancingadjustment")) | set(find("records/game/")))
paths = [p for p in paths if p.endswith(".dbr")]
print(f"{len(paths)} records under records/game/ + balancingadjustment*")
hits=[]
for p in paths:
    rec,prov,own = merged(p)
    for k,v in rec.items():
        if "life" not in k.lower(): continue
        hits.append((p,k,v,prov[k],own))
for p,k,v,pr,own in hits:
    if isinstance(v,list):
        print(f"\n{p}\n   {k}  [{pr}] len={len(v)} owners={own}")
        print(f"     first16={v[:16]}")
        print(f"     idx155..165={v[155:166] if len(v)>165 else 'n/a'}")
        print(f"     min={min(v)} max={max(v)}")
        for target in (449,229,349,449.0):
            if target in v: print(f"     *** {target} at indices {[i for i,x in enumerate(v) if x==target]}")
    else:
        print(f"\n{p}\n   {k} = {v!r} [{pr}] owners={own}")
