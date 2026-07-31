#!/usr/bin/env python3
"""V3 - proxy-pool anatomy: what fields carry density + champion/hero chance, and the
Wightmire-region pools specifically. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")

print("="*100); print("A. FULL DUMP of the Primordian's own proxy"); print("="*100)
for r in ["records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr"]:
    rec=a.read_record(r)
    print(f"{r}  Class={rec.get('Class')} tpl={rec.get('templateName')}  ({len(rec)} fields)")
    for k in sorted(rec):
        v=rec[k]
        if isinstance(v,list): v=v[0] if len(set(v))==1 else v
        if v in (0,0.0,None,''): continue
        print(f"   {k:44s} {v}")
print()

print("="*100); print("B. Wightmire / slith pools — every proxy pool naming a slith or wightmire"); print("="*100)
hits=[]
for r in a.records:
    if not r.startswith("records/proxies/"): continue
    if not ("wightmire" in r.lower() or "slith" in r.lower()): continue
    hits.append(r)
for r in sorted(hits):
    rec=a.read_record(r)
    names=[(rec.get(f'name{i}'),rec.get(f'weight{i}')) for i in range(1,13) if rec.get(f'name{i}')]
    print(f"  {r}")
    print(f"      Class={rec.get('Class')}  spawnMin={rec.get('spawnMin')} spawnMax={rec.get('spawnMax')} "
          f"championChance={rec.get('championChance')} heroChance={rec.get('heroChance')}")
    for n,w in names:
        print(f"        w={w}  {n}")
print()

print("="*100); print("C. FIELD SURFACE of the proxy-pool class (union over all pool records)"); print("="*100)
from collections import Counter
fields=Counter(); cls=Counter(); ex={}
for r in a.records:
    if not r.startswith("records/proxies/"): continue
    rec=a.read_record(r)
    cls[str(rec.get('Class'))]+=1
    for k,v in rec.items():
        nz = (any(v) if isinstance(v,list) else bool(v))
        if nz:
            fields[k]+=1
            ex.setdefault(k,(r,v if not isinstance(v,list) else (v[0] if len(set(v))==1 else v)))
print("  classes:", dict(cls))
print()
for k,c in fields.most_common():
    if re.match(r'^(name|weight)\d+$',k): continue
    r,v=ex[k]
    print(f"   {k:40s} n={c:5d}   e.g. {str(v)[:60]}")
