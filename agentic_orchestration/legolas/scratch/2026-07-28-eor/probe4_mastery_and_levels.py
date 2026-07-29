#!/usr/bin/env python3
"""probe4 — (a) dump the Oathkeeper mastery-bar record _classtraining_class09.dbr,
(b) hunt for the tier-threshold table and the player level->skillpoint table.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]
archives = {p.name: ArzArchive(p) for p in ARZS}

def dump(name, a, rec_path, prefix="    "):
    rec = a.read_record(rec_path)
    print(f"=== {name}  {rec_path}  [{a.record_type(rec_path)}]  fields={len(rec)}")
    for k in sorted(rec):
        v = rec[k]
        if isinstance(v, list):
            print(f"{prefix}{k:36s} [n={len(v)}] {v}")
        else:
            print(f"{prefix}{k:36s} {v!r}")
    print()

# (a) mastery bar
T = "records/skills/playerclass09/_classtraining_class09.dbr"
for name, a in archives.items():
    if T in a.records:
        dump(name, a, T)

# (b) hunt for tier / levelling tables
print("=== record-type census for likely 'tier'/'level' config records ===")
seen = {}
for name, a in archives.items():
    for r in a.records:
        rt = a.record_type(r)
        if rt in ("SkillTree",):
            continue
        low = r.lower()
        if (low.startswith("records/game/") or "levelrequirement" in low
                or "playerlevel" in low or "experience" in low
                or "skilltier" in low or "masterytier" in low):
            seen.setdefault((name, rt), []).append(r)
for (name, rt), rs in sorted(seen.items()):
    print(f"  {name:14s} {rt:34s} n={len(rs)}   e.g. {rs[:4]}")
