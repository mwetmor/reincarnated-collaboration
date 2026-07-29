#!/usr/bin/env python3
"""probe1 — dump eyeofreckoning1.dbr full field set from Edition-II corpus.
Read-only. Reuses the ArzArchive reader from gd_arz_adapter_2026_07_24.py."""
import sys, pathlib, json
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [
    ROOT / "database/database.arz",
    ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz",
    ROOT / "gdx3/database/GDX3.arz",
]
TARGET = "records/skills/playerclass09/eyeofreckoning1.dbr"

for p in ARZS:
    a = ArzArchive(p)
    if TARGET in a.records:
        print(f"=== FOUND in {p.name}  (rt_count={a.rt_count}, strings={len(a.strings)})")
        print(f"    recordType = {a.record_type(TARGET)}")
        rec = a.read_record(TARGET)
        print(f"    field count = {len(rec)}")
        for k in sorted(rec):
            v = rec[k]
            if isinstance(v, list):
                print(f"    {k:44s} [n={len(v)}] {v}")
            else:
                print(f"    {k:44s} {v!r}")
        print()
