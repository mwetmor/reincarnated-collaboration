#!/usr/bin/env python3
"""P9 - survivalinfo.dbr = wave/tier schedule? + spawnbeacon/spawnpoint entities. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
for k,p in [("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),("sm1","survivalmode1/database/SurvivalMode1.arz"),
            ("sm2","survivalmode2/database/SurvivalMode2.arz"),("sm3","survivalmode3/database/SurvivalMode3.arz")]:
    a=ArzArchive(ROOT/p)
    for tgt in ("records/game/survivalinfo.dbr","records/game/gameproxies.dbr"):
        if tgt in a.records:
            rec=a.read_record(tgt)
            print(f"\n===== {k} :: {tgt}  ({len(rec)} fields)")
            for kk,vv in sorted(rec.items()): print(f"   {kk} = {str(vv)[:300]}")
print("\n\n===== spawnbeacon / spawnpoint / tierNNspawnpoint (sm_mod)")
a=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")
for t in ["records/scriptentities/spawnbeacon_01.dbr","records/scriptentities/spawnpoint02.dbr",
          "records/scriptentities/tier14spawnpoint01.dbr","records/scriptentities/defensepoint_01.dbr"]:
    if t in a.records:
        rec=a.read_record(t); print(f"\n--- {t} ({len(rec)} fields)")
        for kk,vv in sorted(rec.items()): print(f"   {kk} = {str(vv)[:220]}")
