#!/usr/bin/env python3
"""Q1: variant-record hunt for Zantarin / Aleksander / Galakros + full wave-160 pool enumeration."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, owners, find, read, index

print("="*100); print("Q1a — corpus-wide record hunt by name token"); print("="*100)
for tok in ("zantarin","aleksander","galakros","kubacabra","bileeater","revenant","shard"):
    hits = find(tok)
    print(f"\n### {tok!r}  -> {len(hits)} paths")
    for h in hits:
        print(f"   {h}   owners={owners(h)}")
