#!/usr/bin/env python3
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
for p in sorted(find("proxypoolequation")):
    rec,prov,own = merged(p)
    print(f"\n### {p} owners={own}")
    for k in sorted(rec): print(f"   {k:40s} = {rec[k]!r} [{prov[k]}]")
