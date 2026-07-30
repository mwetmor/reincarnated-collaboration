#!/usr/bin/env python3
"""C4 — ranks 3..6 for every array field on the three target skills. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]
def get(n):
    for nm,a in ars:
        if n in a.records: return nm,a.read_record(n)
    return None,None
for rn in ["records/skills/nonplayerskills/bossskills/primordian_wave.dbr",
           "records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr",
           "records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr",
           "records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr",
           "records/skills/itemskills/legendary/item_apocalypse.dbr"]:
    nm,rec=get(rn)
    if rec is None: print(f"=== {rn} NOT FOUND"); continue
    print(f"=== {rn} [{nm}]")
    print(f"    {'field':44s} {'r3':>9s} {'r4':>9s} {'r5':>9s} {'r6':>9s}")
    for k in sorted(rec):
        v=rec[k]
        if isinstance(v,list) and len(v)>=6:
            print(f"    {k:44s} {v[2]:>9} {v[3]:>9} {v[4]:>9} {v[5]:>9}")
        elif isinstance(v,list):
            print(f"    {k:44s} SHORT LIST {v}")
    print()
