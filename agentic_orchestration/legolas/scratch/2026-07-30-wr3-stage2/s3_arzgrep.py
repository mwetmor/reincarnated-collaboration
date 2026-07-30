#!/usr/bin/env python3
"""S3 — grep record names across all pinned .arz archives. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
pat = re.compile(sys.argv[1], re.I)
for p in ARZS:
    a = ArzArchive(p)
    hits = [r for r in a.records if pat.search(r)]
    for h in sorted(hits):
        print(f"{p.name}\t{h}")
