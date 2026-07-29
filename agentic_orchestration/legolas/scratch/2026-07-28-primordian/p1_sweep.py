#!/usr/bin/env python3
"""P1 — exhaustive 'primordian' sweep across ALL 8 .arz archives in the Edition-II corpus.

Sweeps: (a) record paths, (b) full string tables (catches field VALUES referencing the name).
READ-ONLY.
"""
import sys, pathlib, hashlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [
    ("base",           ROOT / "database/database.arz"),
    ("gdx1",           ROOT / "gdx1/database/GDX1.arz"),
    ("gdx2",           ROOT / "gdx2/database/GDX2.arz"),
    ("gdx3",           ROOT / "gdx3/database/GDX3.arz"),
    ("survivalmode",   ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
    ("survivalmode1",  ROOT / "survivalmode1/database/SurvivalMode1.arz"),
    ("survivalmode2",  ROOT / "survivalmode2/database/SurvivalMode2.arz"),
    ("survivalmode3",  ROOT / "survivalmode3/database/SurvivalMode3.arz"),
]

NEEDLES = ["primordian", "primorian", "slith_wightmirecave01", "slithbossb02"]

archives = {}
print("=== ARCHIVE CENSUS ===")
for tag, p in ARZS:
    if not p.exists():
        print(f"{tag:15s} MISSING {p}")
        continue
    a = ArzArchive(p)
    archives[tag] = a
    sha = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    print(f"{tag:15s} records={len(a.records):7,d}  strings={len(a.strings):7,d}  sha256[:16]={sha}  {p.name}")

print("\n=== RECORD-PATH HITS ===")
for tag, a in archives.items():
    for rp in sorted(a.records):
        low = rp.lower()
        if any(n in low for n in NEEDLES):
            print(f"{tag:15s} {a.records[rp]['rtype']:28s} {rp}")

print("\n=== STRING-TABLE HITS (value references) ===")
for tag, a in archives.items():
    for s in a.strings:
        low = s.lower()
        if any(n in low for n in NEEDLES):
            print(f"{tag:15s} {s}")
