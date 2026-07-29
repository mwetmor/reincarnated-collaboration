#!/usr/bin/env python3
"""probe14 — energy economy inputs.
(a) malepc01.dbr base energy/regen/attributes
(b) combatformulas.dbr / gameengine.dbr attribute->energy conversion
(c) skill_attackradiusspin.tpl full include chain + skillManaCost declaration site
(d) compute a level-10 pure-Oathkeeper-bar-25 energy pool
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]}

print("=== (a) malepc01.dbr ===")
for name, a in archives.items():
    P = "records/creatures/pc/malepc01.dbr"
    if P not in a.records:
        print(f"  {name}: ABSENT"); continue
    rec = a.read_record(P)
    print(f"  --- {name} fields={len(rec)}")
    for k in sorted(rec):
        if re.search(r"(Mana|Life|Regen|Intelligence|Strength|Dexterity|Level)", k):
            v = rec[k]
            if isinstance(v, list) or v:
                print(f"      {k:44s} {v!r}")

print("\n=== (b) combatformulas.dbr energy-relevant fields ===")
C = "records/game/combatformulas.dbr"
for name, a in archives.items():
    if C not in a.records:
        continue
    rec = a.read_record(C)
    print(f"  --- {name} fields={len(rec)}")
    for k in sorted(rec):
        if re.search(r"(Mana|Energy|Intelligence|Regen)", k):
            print(f"      {k:52s} {rec[k]!r}")

print("\n=== (c) template chain for skill_attackradiusspin ===")
t = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
txt = t.read_file("skill_attackradiusspin.tpl").decode("latin-1")
print(txt[:2600])

print("\n=== (d) where is skillManaCost declared? ===")
for n in t.names():
    if not n.endswith(".tpl"):
        continue
    try:
        s = t.read_file(n).decode("latin-1")
    except Exception:
        continue
    if '"skillManaCost"' in s:
        i = s.index('"skillManaCost"')
        print(f"  --- {n}")
        print("     " + s[max(0, i - 400):i + 260].replace("\n", "\n     "))
        break
