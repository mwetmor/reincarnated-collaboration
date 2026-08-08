#!/usr/bin/env python3
"""Q5: where does the monster LEVEL come from? Re-read every level proxy with full overlay resolution."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find
print("== all records/proxies/lv*.dbr ==")
for p in sorted(find("records/proxies/lv")):
    rec,prov,own = merged(p)
    print(f"\n### {p}  owners={own}")
    for k in sorted(rec):
        if k=="templateName": continue
        print(f"    {k:36s} = {rec[k]!r}  [{prov[k]}]")
print("\n== survival-tree level proxies (any archive) ==")
for p in sorted(set(find("lv")) - set(find("records/proxies/lv"))):
    if "/lv" in p and p.endswith(".dbr") and "proxies" in p:
        rec,prov,own = merged(p)
        print(f"\n### {p} owners={own}")
        for k in sorted(rec):
            if "quation" in k or "evel" in k: print(f"    {k:36s} = {rec[k]!r} [{prov[k]}]")
