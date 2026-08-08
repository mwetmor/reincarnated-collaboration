#!/usr/bin/env python3
"""Q2: focused -- every characterLife* MODIFIER in records/game/, with wave-160-relevant indices."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
paths = sorted(p for p in set(find("records/game/")) if p.endswith(".dbr"))
KEYS=("characterLifeModifier","characterLifeMultModifier","characterLife")
for p in paths:
    rec,prov,own = merged(p)
    out=[]
    for k in KEYS:
        v=rec.get(k)
        if v in (None,0.0,0,'') : continue
        out.append((k,v,prov[k]))
    if not out: continue
    print(f"\n### {p}   owners={own}")
    for k,v,pr in out:
        if isinstance(v,list):
            print(f"    {k} [{pr}] len={len(v)} min={min(v)} max={max(v)}")
            print(f"       [0:12]  = {v[:12]}")
            if len(v)>=166: print(f"       [155:166]= {v[155:166]}")
        else:
            print(f"    {k} [{pr}] = {v!r}")
