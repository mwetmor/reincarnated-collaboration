#!/usr/bin/env python3
"""P3 — who REFERENCES the Primordian boss pools? Full-corpus reverse-reference sweep.

A pool existing is not reachability. This walks every record in every archive and reports
any record whose field VALUES cite the pool paths (or the monster record directly).
"""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [
    ("base",          ROOT / "database/database.arz"),
    ("gdx1",          ROOT / "gdx1/database/GDX1.arz"),
    ("gdx2",          ROOT / "gdx2/database/GDX2.arz"),
    ("gdx3",          ROOT / "gdx3/database/GDX3.arz"),
    ("survivalmode",  ROOT / "mods/survivalmode/database/SurvivalMode.arz"),
    ("survivalmode1", ROOT / "survivalmode1/database/SurvivalMode1.arz"),
    ("survivalmode2", ROOT / "survivalmode2/database/SurvivalMode2.arz"),
    ("survivalmode3", ROOT / "survivalmode3/database/SurvivalMode3.arz"),
]

TARGETS = [
    "poolsboss/slith_primordian.dbr",
    "boss&quest/slith_wightmirecave01.dbr",
    "p_wightmire_slitha01.dbr",
]

for tag, p in ARZS:
    a = ArzArchive(p)
    # fast pre-filter: does this archive's string table even contain the needle?
    present = {t: any(t in s for s in a.strings) for t in TARGETS}
    if not any(present.values()):
        print(f"\n[{tag}] no target strings present -> no references possible. SKIP.")
        continue
    print(f"\n{'='*88}\n[{tag}] target strings present: {[t for t,v in present.items() if v]}\n{'='*88}")
    for rp in sorted(a.records):
        try:
            r = a.read_record(rp)
        except Exception:
            continue
        for k, v in r.items():
            vals = v if isinstance(v, list) else [v]
            for item in vals:
                if isinstance(item, str) and any(t in item for t in TARGETS):
                    if rp == item:
                        continue  # self
                    print(f"  {rp}\n      {k} = {item}")
