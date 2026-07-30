#!/usr/bin/env python3
"""C6 — difficulty AttributePak slot-0 (Normal / 1-player) values, all non-zero. READ-ONLY."""
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
for rn in ["records/game/balancingadjustment_mp+difficulty_enemies01.dbr"]:
    nm,rec=get(rn); print(f"=== {rn} [{nm}] fields={len(rec)}")
    print("--- ALL array fields, slot0 (Normal/1p) and full vector ---")
    for k in sorted(rec):
        v=rec[k]
        if isinstance(v,list):
            print(f"  {k:46s} slot0={v[0]!r:9} full={[round(x,1) for x in v]}")
    print("--- scalar non-zero ---")
    for k in sorted(rec):
        v=rec[k]
        if not isinstance(v,list) and v not in (0,0.0,False,''):
            print(f"  {k:46s} {v!r}")
