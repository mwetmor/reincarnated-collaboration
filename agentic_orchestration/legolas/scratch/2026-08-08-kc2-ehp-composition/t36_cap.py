#!/usr/bin/env python3
"""Q5: what is the max player level in this corpus (GDX3 cap raise)?"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
for pat in ("experiencelevelcontrol","playerlevels","levelcontrol"):
    for p in sorted(find(pat)):
        rec,prov,own = merged(p)
        print(f"\n### {p} owners={own}")
        for k in sorted(rec):
            v=rec[k]
            if isinstance(v,list): print(f"   {k:34s} len={len(v)} [{prov[k]}] first={v[:4]} last={v[-4:]}")
            else: print(f"   {k:34s} = {v!r} [{prov[k]}]")
