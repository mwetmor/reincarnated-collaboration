#!/usr/bin/env python3
"""V1 - complete dump of every balancingadjustment_* record across all four DBs. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
ars=[(n,ArzArchive(p)) for n,p in ARZS]

# 1. enumerate every balancingadjustment record anywhere
print("="*100)
print("ALL balancingadjustment* RECORDS, ALL FOUR ARCHIVES")
print("="*100)
seen={}
for nm,a in ars:
    for r in a.records:
        if "balancingadjustment" in r.lower():
            seen.setdefault(r,[]).append(nm)
for r in sorted(seen):
    print(f"  {r:80s}  [{','.join(seen[r])}]")
print()

def get(n):
    out=[]
    for nm,a in ars:
        if n in a.records: out.append((nm,a.read_record(n)))
    return out

TARGETS=[r for r in sorted(seen)]
for t in TARGETS:
    for nm,rec in get(t):
        nz={k:v for k,v in rec.items()
            if not isinstance(v,str) and (v if not isinstance(v,list) else any(x for x in v))}
        print("="*100)
        print(f"{t}   [{nm}]   {len(rec)} fields, {len(nz)} nonzero-numeric")
        print(f"   Class={rec.get('Class')}  templateName={rec.get('templateName')}  FileDescription={rec.get('FileDescription')}")
        print("="*100)
        for k in sorted(nz):
            v=nz[k]
            if isinstance(v,list):
                if len(set(v))==1: s=f"{v[0]} (x{len(v)} uniform)"
                else: s=str(v)
            else: s=str(v)
            print(f"   {k:52s} {s}")
        print()
