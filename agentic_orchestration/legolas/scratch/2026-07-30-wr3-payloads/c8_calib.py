#!/usr/bin/env python3
"""C8 — calibrate the outgoing-damage composition against the envelope's own L13 monster ledger. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ars=[ArzArchive(ROOT/"database/database.arz"),ArzArchive(ROOT/"gdx1/database/GDX1.arz"),
     ArzArchive(ROOT/"gdx2/database/GDX2.arz"),ArzArchive(ROOT/"gdx3/database/GDX3.arz")]
def get(n):
    for a in ars:
        if n in a.records: return a.read_record(n)
    return None
def find(sub):
    out=[]
    for a in ars:
        for r in a.records:
            if sub in r.lower() and a.record_type(r)=='Monster': out.append(r)
    return out
for q in ('walkingdead','plaguewalker','riftscourge'):
    print(f"### search {q}: {find(q)[:6]}")
