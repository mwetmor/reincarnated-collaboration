#!/usr/bin/env python3
"""probe12 — brute-force: scan EVERY record in all four archives for a length-9 numeric array
that is strictly increasing and bounded by ~60 (candidate mastery-tier milestone table).
Also report any field whose NAME contains 'milestone' with a numeric value.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]

hits9, milestone_fields = [], []
for p in ARZS:
    a = ArzArchive(p)
    n = 0
    for r in a.records:
        try:
            rec = a.read_record(r)
        except Exception:
            continue
        n += 1
        for k, v in rec.items():
            if "milestone" in k.lower():
                milestone_fields.append((p.name, r, k, v))
            if isinstance(v, list) and len(v) == 9 and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
                if all(v[i] < v[i + 1] for i in range(8)) and 0 < v[0] and v[-1] <= 60:
                    hits9.append((p.name, r, k, v))
    print(f"scanned {p.name}: {n} records", flush=True)

print("\n=== fields named *milestone* ===")
for row in milestone_fields:
    print("  ", row)

print(f"\n=== strictly-increasing length-9 numeric arrays, max<=60  (n={len(hits9)}) ===")
for name, r, k, v in hits9[:80]:
    print(f"  {name}  {r}  {k} = {v}")
