#!/usr/bin/env python3
"""Q1: read the ACTUAL wave-160 spawn proxies (tier16 w10) + their pool references."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
for w in ("w09","w10"):
    ps=sorted(p for p in find(f"tier16waves/proxy_{w}_"))
    print(f"\n{'#'*90}\n# tier16 {w}  ({len(ps)} spawn points)\n{'#'*90}")
    for p in ps:
        rec,prov,own = merged(p)
        print(f"\n-- {p}  owners={own}")
        for k in sorted(rec):
            if k in ("templateName",): continue
            print(f"     {k:34s} = {rec[k]!r} [{prov[k]}]")
