#!/usr/bin/env python3
"""probe9 — dump the class09 UI panel records that might carry tier thresholds.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx2/database/GDX2.arz"]}

for t in ["records/ui/skills/class09/classtable.dbr",
          "records/ui/skills/class09/classtraining.dbr",
          "records/ui/skills/class09/classtrainingbar.dbr",
          "records/ui/skills/classcommon/skills_classpanelconfiguration.dbr",
          "records/ui/skills/class09/skill31.dbr",
          "records/ui/skills/class09/skill18.dbr"]:
    for name, a in archives.items():
        if t in a.records:
            rec = a.read_record(t)
            print(f"=== {name}  {t}  fields={len(rec)}")
            for k in sorted(rec):
                v = rec[k]
                s = f"[n={len(v)}] {v}" if isinstance(v, list) else repr(v)
                print(f"    {k:36s} {s}")
            print()
