#!/usr/bin/env python3
"""P1 - schema dump: Proxy record fields, Crucible wave record fields, Class histogram. READ-ONLY."""
import sys, pathlib, collections, json
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base=ArzArchive(ROOT/"database/database.arz")
sm=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")

print("### Class histogram under records/proxies/ (base)")
cl=collections.Counter()
for r in base.records:
    if r.startswith("records/proxies/"):
        cl[str(base.read_record(r).get('Class'))]+=1
print(dict(cl))

print("\n### Class histogram under records/proxies/ (SurvivalMode mod)")
cl2=collections.Counter()
for r in sm.records:
    if r.startswith("records/proxies/"):
        cl2[str(sm.read_record(r).get('Class'))]+=1
print(dict(cl2))

print("\n### Sample Proxy record (base, area001) FULL FIELDS")
for r in sorted(base.records):
    if r.startswith("records/proxies/area001/") and str(base.read_record(r).get('Class'))=='Proxy':
        rec=base.read_record(r); print(r)
        for k,v in sorted(rec.items()): print(f"   {k} = {v}")
        break

print("\n### Sample wave record (SurvivalMode tier15waves) FULL FIELDS - 3 samples")
waves=[r for r in sorted(sm.records) if "tier15waves" in r]
print("count tier15waves:", len(waves))
for r in waves[:3]:
    rec=sm.read_record(r); print(f"\n--- {r}  ({len(rec)} fields)")
    for k,v in sorted(rec.items()): print(f"   {k} = {v}")

print("\n### Field-name union across ALL tierNNwaves records (sm mod)")
fu=collections.Counter()
nw=0
for r in sm.records:
    if "waves/" in r or "waves" in r.split("/")[2] if r.count("/")>2 else False:
        pass
allw=[r for r in sm.records if r.count("/")>2 and r.split("/")[2].endswith("waves")]
for r in allw:
    nw+=1
    for k in sm.read_record(r): fu[k]+=1
print(f"wave records={nw}")
for k,v in fu.most_common(60): print(f"   {k:34s} {v}")
