#!/usr/bin/env python3
"""probe8 — (a) all NON-ZERO fields on the Oathkeeper Skill_Mastery record (GDX2 override),
(b) full listing of records/ui/skills/classcommon/ and records/ui/skills/class09*,
(c) skill-point income curve computed from playerlevels.dbr.
Read-only."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]}

M = "records/skills/playerclass09/_classtraining_class09.dbr"
print("=== (a) non-zero fields on Skill_Mastery (GDX2 override) ===")
rec = archives["GDX2.arz"].read_record(M)
def nonzero(v):
    if isinstance(v, list):
        return any(bool(x) for x in v)
    return bool(v)
for k in sorted(rec):
    v = rec[k]
    if not nonzero(v):
        continue
    if isinstance(v, list):
        print(f"  {k:36s} [n={len(v)}] {v[:8]} ... {v[-3:]}")
    else:
        print(f"  {k:36s} {v!r}")

print("\n=== (b) records/ui/skills/classcommon + class09 ===")
for name, a in archives.items():
    for r in sorted(a.records):
        low = r.lower()
        if low.startswith("records/ui/skills/classcommon/") or low.startswith("records/ui/skills/class09"):
            print(f"  {name}  {r}")

print("\n=== (c) skill-point income (from playerlevels.dbr, GDX2 override) ===")
pl = archives["GDX2.arz"].read_record("records/creatures/pc/playerlevels.dbr")
smp = pl["skillModifierPoints"]
# run-length encode
runs, cur, start = [], smp[0], 0
for i, v in enumerate(smp):
    if v != cur:
        runs.append((start, i - 1, cur)); cur = v; start = i
runs.append((start, len(smp) - 1, cur))
print("  run-length over array index (0-based):")
for s, e, v in runs:
    print(f"    idx {s:3d}..{e:3d}  -> {v} pts")
print(f"  initialSkillPoints={pl['initialSkillPoints']}  characterModifierPoints={pl['characterModifierPoints']}"
      f"  maxPlayerLevel={pl['maxPlayerLevel']}  maxDevotionPoints={pl['maxDevotionPoints']}")

for interp, off in (("index i == points granted ON REACHING level i+1", 1),
                    ("index i == points granted ON REACHING level i", 0)):
    print(f"\n  -- interpretation: {interp}")
    cum = 0
    tbl = {}
    for i, v in enumerate(smp):
        lvl = i + off
        if lvl < 1 or lvl > 100:
            continue
        cum += v
        tbl[lvl] = cum
    for L in (2, 5, 10, 12, 15, 20, 25, 30, 40, 50, 100):
        if L in tbl:
            print(f"     cumulative skill points at level {L:3d} = {tbl[L]}")
