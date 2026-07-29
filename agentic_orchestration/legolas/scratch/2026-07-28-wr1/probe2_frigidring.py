#!/usr/bin/env python3
"""probe2 (WR1 E-1) — full field dump of Primordian's skill loadout + the monster record's
skillName/specialAttack wiring. Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT/"database/database.arz", ROOT/"gdx1/database/GDX1.arz",
        ROOT/"gdx2/database/GDX2.arz", ROOT/"gdx3/database/GDX3.arz"]
archives = [(p.name, ArzArchive(p)) for p in ARZS]

TARGETS = [
 "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_wave.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_icearmor.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_passive.dbr",
 "records/skills/nonplayerskills/bossskills/primordian_arcticblast.dbr",
 "records/skills/nonplayerskills/heroskills/chillbane_blizzard.dbr",
]
for t in TARGETS:
    hit = False
    for name, a in archives:
        if t in a.records:
            hit = True
            print(f"\n{'='*90}\n=== {t}  [{name}] type={a.record_type(t)}\n{'='*90}")
            rec = a.read_record(t)
            for k in sorted(rec):
                v = rec[k]
                if isinstance(v, list) and len(v) > 1:
                    print(f"  {k:44s} [n={len(v)}] {v}")
                else:
                    print(f"  {k:44s} {v!r}")
    if not hit:
        print(f"\n!!! NOT FOUND: {t}")
