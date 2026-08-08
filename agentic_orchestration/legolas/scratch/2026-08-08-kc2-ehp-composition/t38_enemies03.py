#!/usr/bin/env python3
"""Q5: full non-zero field dump of the Gladiator survival pack + gameengine overlay check."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners
for p in ("records/game/balancingadjustment_survivalmode_enemies03.dbr",):
    rec,prov,own = merged(p); print(f"### {p} owners={own}  ({len(rec)} fields)")
    for k in sorted(rec):
        v=rec[k]
        if v in (None,0,0.0,"",False): continue
        if isinstance(v,list):
            if all(x in (0,0.0) for x in v): continue
            print(f"   {k:44s} len={len(v)} [{prov[k]}] idx159={v[159] if len(v)>159 else '-'} min={min(v)} max={max(v)}")
        else: print(f"   {k:44s} = {v!r} [{prov[k]}]")
print("\n### gameengine.dbr — owners + monsterAttributePak + any level field")
rec,prov,own = merged("records/game/gameengine.dbr"); print("  owners=",own)
for k in sorted(rec):
    if "pak" in k.lower() or "evel" in k.lower() or "survival" in k.lower():
        print(f"   {k:44s} = {rec[k]!r} [{prov[k]}]")
