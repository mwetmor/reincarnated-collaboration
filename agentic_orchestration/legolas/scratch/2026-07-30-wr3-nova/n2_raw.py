#!/usr/bin/env python3
"""N2 — print exact named fields (including zero values) for a record. READ-ONLY."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives=[(p.name, ArzArchive(p)) for p in ARZS]
rec_name = sys.argv[1]; keys = [k.lower() for k in sys.argv[2:]]
for name,a in archives:
    if rec_name in a.records:
        rec = a.read_record(rec_name)
        print(f"=== {rec_name} [{name}]")
        for k in sorted(rec):
            if any(q in k.lower() for q in keys):
                print(f"  {k:46s} {rec[k]!r}")
