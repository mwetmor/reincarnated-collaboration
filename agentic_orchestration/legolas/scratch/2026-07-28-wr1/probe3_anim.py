#!/usr/bin/env python3
"""probe3 (WR1 E-1/E-3) — anm_slith.dbr: does the animation table carry timing?
Plus: hunt Roar/special animation entries. Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives = [(p.name, ArzArchive(p)) for p in ARZS]
T = "records/creatures/enemies/anm/anm_slith.dbr"
for name, a in archives:
    if T in a.records:
        rec = a.read_record(T)
        print(f"=== {T} [{name}] type={a.record_type(T)}  fields={len(rec)}")
        for k in sorted(rec):
            if re.search(r'special|roar|attack|unarmed', k, re.I):
                print(f"  {k:44s} {rec[k]!r}")
        break
