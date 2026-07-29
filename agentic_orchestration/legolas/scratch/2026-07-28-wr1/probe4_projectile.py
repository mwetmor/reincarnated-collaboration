#!/usr/bin/env python3
"""probe4 (WR1 E-1) — icebolt_nova projectile fx record: speed/lifetime => ring expansion timing.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives = [(p.name, ArzArchive(p)) for p in ARZS]
for t in ["records/fx/skillsother/projectile/icebolt_nova_fxprojectile.dbr"]:
    for name, a in archives:
        if t in a.records:
            rec = a.read_record(t)
            print(f"=== {t} [{name}] type={a.record_type(t)} fields={len(rec)}")
            for k in sorted(rec):
                print(f"  {k:44s} {rec[k]!r}")
            break
