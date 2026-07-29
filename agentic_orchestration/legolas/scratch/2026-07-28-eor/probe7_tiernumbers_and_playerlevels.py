#!/usr/bin/env python3
"""probe7 — dump classtiernumber1..9 UI records and records/creatures/pc/playerlevels.dbr.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]
archives = {p.name: ArzArchive(p) for p in ARZS}

print("=== classtiernumber1..9 ===")
for i in range(1, 10):
    T = f"records/ui/skills/classcommon/classtiernumber{i}.dbr"
    for name, a in archives.items():
        if T in a.records:
            rec = a.read_record(T)
            print(f"  {name}  tier{i}: {rec}")

print("\n=== records/creatures/pc/playerlevels.dbr ===")
P = "records/creatures/pc/playerlevels.dbr"
for name, a in archives.items():
    if P not in a.records:
        print(f"--- {name}: ABSENT")
        continue
    rec = a.read_record(P)
    print(f"=== {name}  [{a.record_type(P)}]  fields={len(rec)}")
    for k in sorted(rec):
        v = rec[k]
        if isinstance(v, list):
            print(f"    {k:34s} [n={len(v)}] {v}")
        else:
            print(f"    {k:34s} {v!r}")
    print()
