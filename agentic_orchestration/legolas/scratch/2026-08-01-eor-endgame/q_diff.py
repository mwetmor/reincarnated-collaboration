#!/usr/bin/env python3
"""Endgame-difficulty-axis probe. READ-ONLY over the Edition-II .arz fetch."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")

print("="*70); print("A. gameproxies.dbr — base vs SurvivalMode overlays")
for k,p in [("BASE","database/database.arz"),
            ("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),
            ("sm1","survivalmode1/database/SurvivalMode1.arz"),
            ("sm2","survivalmode2/database/SurvivalMode2.arz"),
            ("sm3","survivalmode3/database/SurvivalMode3.arz")]:
    a=ArzArchive(ROOT/p)
    t="records/game/gameproxies.dbr"
    if t in a.records:
        rec=a.read_record(t)
        print(f"\n-- {k} :: {t}")
        for kk,vv in sorted(rec.items()): print(f"   {kk} = {vv}")

print("\n"+"="*70); print("B. survivalinfo.dbr (sm_mod) — difficulty-related fields")
a=ArzArchive(ROOT/"mods/survivalmode/database/SurvivalMode.arz")
rec=a.read_record("records/game/survivalinfo.dbr")
for kk,vv in sorted(rec.items()): print(f"   {kk} = {str(vv)[:250]}")

print("\n"+"="*70); print("C. records matching 'difficult' / 'aspirant' / 'challenger' / 'gladiator' across archives")
for k,p in [("BASE","database/database.arz"),("sm_mod","mods/survivalmode/database/SurvivalMode.arz"),
            ("sm1","survivalmode1/database/SurvivalMode1.arz"),("sm2","survivalmode2/database/SurvivalMode2.arz"),
            ("sm3","survivalmode3/database/SurvivalMode3.arz")]:
    a=ArzArchive(ROOT/p)
    hits=[r for r in a.records if any(t in r.lower() for t in ("aspirant","challenger","gladiator","difficulty"))]
    print(f" {k}: {len(hits)} -> {hits[:20]}")

print("\n"+"="*70); print("D. SoT floor5wave3 ambush + its pool, verbatim")
a=ArzArchive(ROOT/"database/database.arz")
for t in ["records/proxies/boss&quest/proxy_areab_stepsoftorment_floor5wave3.dbr"]:
    rec=a.read_record(t); print(f"\n-- {t}")
    for kk,vv in sorted(rec.items()): print(f"   {kk} = {str(vv)[:250]}")
    for kk,vv in sorted(rec.items()):
        if kk.startswith("pool") and isinstance(vv,str) and vv.endswith(".dbr"):
            pr=a.read_record(vv); print(f"\n   -- POOL {vv}")
            for k2,v2 in sorted(pr.items()): print(f"      {k2} = {str(v2)[:250]}")

print("\n"+"="*70); print("E. crucible tier13w06 / tier14w06 spawn-point pools championChance")
