#!/usr/bin/env python3
"""probe1 (WR1 E-2) — dump gameengine.dbr + combatformulas.dbr full field sets.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
TARGETS = ["records/game/gameengine.dbr", "records/game/combatformulas.dbr"]

archives = [(p.name, ArzArchive(p)) for p in ARZS]
for t in TARGETS:
    for name, a in archives:
        if t in a.records:
            print(f"\n{'='*78}\n=== {t}  IN {name}  type={a.record_type(t)}\n{'='*78}")
            rec = a.read_record(t)
            for k in sorted(rec):
                v = rec[k]
                if isinstance(v, list) and len(v) > 1:
                    print(f"  {k:46s} [n={len(v)}] {v}")
                else:
                    print(f"  {k:46s} {v!r}")
