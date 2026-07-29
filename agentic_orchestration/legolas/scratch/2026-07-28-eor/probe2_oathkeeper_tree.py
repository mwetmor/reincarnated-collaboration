#!/usr/bin/env python3
"""probe2 — enumerate the Oathkeeper (playerclass09) skill tree + find the tier-threshold record.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]

archives = {p.name: ArzArchive(p) for p in ARZS}

# 1) every record path mentioning playerclass09 (non-skill dirs included)
print("=== records referencing playerclass09 (by archive) ===")
for name, a in archives.items():
    hits = [r for r in a.records if "playerclass09" in r]
    print(f"{name}: {len(hits)} records")

# 2) which archive holds the class-level / mastery records (not the per-skill ones)
print("\n=== non-'skills/playerclass09/<skill>' shaped, or containing 'mastery'/'tier' ===")
for name, a in archives.items():
    for r in sorted(a.records):
        low = r.lower()
        if "playerclass09" in low and ("mastery" in low or "tier" in low or "tree" in low
                                      or low.count("/") < 3):
            print(f"  {name}  {r}   [{a.record_type(r)}]")

# 3) global: any record path with 'mastery' at top of skills, plus levelling tables
print("\n=== candidate mastery-tree / class-table records ===")
for name, a in archives.items():
    for r in sorted(a.records):
        low = r.lower()
        if low.startswith("records/skills/") and ("mastertable" in low or "mastery" in low
                                                  or low.endswith("/class09.dbr")
                                                  or "skilltree" in low):
            print(f"  {name}  {r}   [{a.record_type(r)}]")
