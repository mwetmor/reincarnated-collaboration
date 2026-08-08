#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index, archives
# sweep every record owned by an sm archive for level-ish fields with non-trivial values
from collections import Counter
seen=Counter(); ex={}
for k,a in archives():
    if not k.startswith("sm"): continue
    for r in a.records:
        rec=a.read_record(r)
        for f,v in rec.items():
            fl=f.lower()
            if "level" in fl and v not in (None,0,0.0,"",False):
                seen[(k,f)]+=1
                ex.setdefault((k,f), (r,v))
for (k,f),n in seen.most_common(60):
    r,v=ex[(k,f)]
    vv = (str(v)[:70]+"...") if len(str(v))>70 else v
    print(f"  [{k}] {f:38s} n={n:5d}  eg {r}\n         = {vv!r}")
