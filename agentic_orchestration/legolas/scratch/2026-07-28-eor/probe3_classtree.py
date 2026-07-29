#!/usr/bin/env python3
"""probe3 — dump the Oathkeeper SkillTree record (tier thresholds) from every archive that carries it.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]
TARGET = "records/skills/playerclass09/_classtree_class09.dbr"

for p in ARZS:
    a = ArzArchive(p)
    if TARGET not in a.records:
        print(f"--- {p.name}: ABSENT")
        continue
    print(f"=== {p.name}   [{a.record_type(TARGET)}]")
    rec = a.read_record(TARGET)
    print(f"    field count = {len(rec)}")
    for k in sorted(rec):
        v = rec[k]
        if isinstance(v, list):
            print(f"    {k:36s} [n={len(v)}] {v}")
        else:
            print(f"    {k:36s} {v!r}")
    print()
