#!/usr/bin/env python3
"""P2 - where do spawnMin/spawnMax actually live? pool schema; wave controllers. READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
base=ArzArchive(ROOT/"database/database.arz")
sm=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")

print("### DOES ANY Class:Proxy RECORD CARRY spawnMin/spawnMax? (base)")
n_prox=0; n_with=0
for r in base.records:
    if not r.startswith("records/proxies/"): continue
    rec=base.read_record(r)
    if str(rec.get('Class'))!='Proxy': continue
    n_prox+=1
    if 'spawnMin' in rec or 'spawnMax' in rec: n_with+=1
print(f"  Class=Proxy records: {n_prox}; carrying spawnMin/spawnMax: {n_with}")

print("\n### Field union by Class, under records/proxies/ (base)")
byclass=collections.defaultdict(collections.Counter)
ccount=collections.Counter()
for r in base.records:
    if not r.startswith("records/proxies/"): continue
    rec=base.read_record(r); c=str(rec.get('Class'))
    ccount[c]+=1
    for k in rec: byclass[c][k]+=1
for c in ['Proxy','None','ProxyAmbush']:
    print(f"\n-- Class={c}  n={ccount[c]}")
    for k,v in byclass[c].most_common(45): print(f"     {k:38s} {v}")

print("\n### Sample Class=None record under proxies/pools (base) FULL")
for r in sorted(base.records):
    if r.startswith("records/proxies/pools/") and str(base.read_record(r).get('Class'))=='None':
        rec=base.read_record(r); print(r)
        for k,v in sorted(rec.items()): print(f"   {k} = {v}")
        break

print("\n### SurvivalMode controllers/ - what's there?")
ctl=[r for r in sorted(sm.records) if r.startswith("records/controllers/")]
print(f" n={len(ctl)}"); 
for r in ctl[:25]: print("  ",r)
print("\n### one controller FULL")
if ctl:
    rec=sm.read_record(ctl[0]); print(ctl[0])
    for k,v in sorted(rec.items()): print(f"   {k} = {v}")
