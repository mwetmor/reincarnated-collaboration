#!/usr/bin/env python3
"""P8 - is there a wave->tier mapping record? survivalmode game/ + scriptentities. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
for k,p in [("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),("sm1","survivalmode1/database/SurvivalMode1.arz"),
            ("sm2","survivalmode2/database/SurvivalMode2.arz"),("sm3","survivalmode3/database/SurvivalMode3.arz")]:
    a=ArzArchive(ROOT/p)
    print(f"\n##### {k}")
    for r in sorted(a.records):
        if r.startswith("records/game/") or r.startswith("records/scriptentities/"):
            print("  ",r)
    for r in sorted(a.records):
        if r.startswith("records/game/"):
            rec=a.read_record(r)
            print(f"\n  --- {r} ({len(rec)} fields)")
            for kk,vv in sorted(rec.items()):
                s=str(vv)
                print(f"      {kk} = {s[:200]}")
            break
