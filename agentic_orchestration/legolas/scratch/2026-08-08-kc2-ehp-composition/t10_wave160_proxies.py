#!/usr/bin/env python3
"""Re-verify the wave-160 spawn-point proxies from source (do not inherit). READ-ONLY."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, index

pats = sorted(p for p in index() if "tier16waves" in p and "w10" in p)
print(f"{len(pats)} wave-160 (tier16 w10) proxy records:")
for p in pats:
    rec, prov, own = merged(p)
    print(f"\n== {p}   owners={own}   fields={len(rec)}")
    for f in sorted(rec):
        print(f"     {f:42s} = {str(rec[f])[:88]}   [{prov[f]}]")
