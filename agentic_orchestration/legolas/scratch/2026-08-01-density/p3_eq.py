#!/usr/bin/env python3
"""P3 - proxyPoolEquation semantics; controllers; levelVarianceEquation; wave-structure naming. READ-ONLY."""
import sys, pathlib, collections, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base=ArzArchive(ROOT/"database/database.arz")
sm=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")

print("### proxypoolequation records (base)")
for r in sorted(base.records):
    if "proxypoolequation" in r.lower():
        rec=base.read_record(r); print(f"\n {r}")
        for k,v in sorted(rec.items()): print(f"    {k} = {v}")

print("\n### levelVarianceEquation targets (records/proxies/lv*.dbr) - 3 samples")
for r in sorted(base.records):
    if re.match(r"records/proxies/lv\d", r):
        rec=base.read_record(r); print(f"\n {r}")
        for k,v in sorted(rec.items()): print(f"    {k} = {v}")

print("\n### SurvivalMode controllers list (full)")
ctl=[r for r in sorted(sm.records) if r.startswith("records/controllers/")]
for r in ctl: print("  ",r)
