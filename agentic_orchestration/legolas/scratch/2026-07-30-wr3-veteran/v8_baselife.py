#!/usr/bin/env python3
"""V8 - where does a GD monster's BASE life come from? Find the level-keyed table. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
ge=a.read_record("records/game/gameengine.dbr")
print("=== gameengine.dbr fields mentioning monster/level/life/char ===")
for k in sorted(ge):
    if re.search(r'(monster|level|life|attribute|char|experience|champion|hero)',k,re.I):
        v=ge[k]
        if isinstance(v,list) and len(set(v))==1: v=v[0]
        if v in (0,0.0,None,''): continue
        print(f"   {k:44s} {v}")
print()
print("=== records with a >=50-element characterLife array (candidate base tables) ===")
n=0
for r in a.records:
    try: rec=a.read_record(r)
    except Exception: continue
    v=rec.get('characterLife')
    if isinstance(v,list) and len(v)>=50 and any(v):
        n+=1
        if n<=25:
            print(f"   {r}  len={len(v)}  [1]={v[0]} [13]={v[12]} [16]={v[15]} [18]={v[17]} [19]={v[18]} [-1]={v[-1]}")
print(f"   total such records: {n}")
