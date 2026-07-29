#!/usr/bin/env python3
"""probe6 — find where the tier->mastery-bar-level threshold lives.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = [ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
        ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]
archives = {p.name: ArzArchive(p) for p in ARZS}

print("=== (1) string-table tokens containing 'tier' (any case), field-name shaped ===")
toks = set()
for name, a in archives.items():
    for s in a.strings:
        if 3 < len(s) < 48 and re.search(r"tier", s, re.I) and " " not in s:
            toks.add(s)
for t in sorted(toks):
    print("   ", t)

print("\n=== (2) records under records/ui/ mentioning skill (candidate tier UI config) ===")
for name, a in archives.items():
    for r in sorted(a.records):
        low = r.lower()
        if low.startswith("records/ui/") and ("skill" in low) and ("tier" in low or "mastery" in low
                                                                   or "allocation" in low):
            print(f"  {name}  {r}  [{a.record_type(r)}]")

print("\n=== (3) record types seen across archives whose name mentions Skill/Level/Game ===")
rts = {}
for name, a in archives.items():
    for r in a.records:
        rt = a.record_type(r)
        if re.search(r"(Level|Game|Mastery|Tier|PlayerLevel)", rt):
            rts.setdefault(rt, []).append((name, r))
for rt, lst in sorted(rts.items()):
    print(f"  {rt:34s} n={len(lst)}  e.g. {lst[:3]}")
