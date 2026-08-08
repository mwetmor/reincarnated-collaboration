#!/usr/bin/env python3
"""Q1/Q5: re-derive wave-160 composition from the wave record; hunt for Crucible level machinery."""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import merged, find, index
# 1) locate survival wave records
waves=[p for p in index() if re.search(r"tier\d+waves?/",p) or "survivalwave" in p or ("/waves/" in p and p.endswith(".dbr"))]
print(f"wave-ish records: {len(waves)}")
cands=[p for p in waves if "160" in p or "tier16" in p]
for p in sorted(cands)[:40]: print("   ",p)
