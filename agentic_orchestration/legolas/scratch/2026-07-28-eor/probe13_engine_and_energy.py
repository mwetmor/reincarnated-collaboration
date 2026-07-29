#!/usr/bin/env python3
"""probe13 — (a) gameengine.dbr across all archives (tier table + override check + spirit->energy),
(b) player creature base record (base energy / regen),
(c) EoR channel semantics from the template.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]}

G = "records/game/gameengine.dbr"
print("=== (a) gameengine.dbr presence + tier/energy fields ===")
for name, a in archives.items():
    if G not in a.records:
        print(f"  {name}: ABSENT (no override)")
        continue
    rec = a.read_record(G)
    print(f"  {name}: PRESENT, fields={len(rec)}")
    for k in sorted(rec):
        if re.search(r"(Tier|tier|[Mm]ana|[Ee]nergy|[Ii]ntelligence|[Ss]pirit|Regen|Mastery)", k):
            v = rec[k]
            s = f"[n={len(v)}] {v}" if isinstance(v, list) else repr(v)
            print(f"      {k:44s} {s}")
    print()

print("=== (b) player creature base records ===")
a = archives["database.arz"]
pcs = [r for r in sorted(a.records) if r.startswith("records/creatures/pc/") and r.count("/") == 3]
for r in pcs[:20]:
    print("   ", r, f"[{a.record_type(r)}]")

for cand in pcs:
    if re.search(r"(male|female)", cand):
        for name, arc in archives.items():
            if cand in arc.records:
                rec = arc.read_record(cand)
                hits = {k: v for k, v in rec.items()
                        if re.search(r"(Mana|Energy|Life|Regen|Intelligence|Strength|Dexterity)", k)
                        and (v if not isinstance(v, list) else any(v))}
                if hits:
                    print(f"\n  --- {name}  {cand}")
                    for k in sorted(hits):
                        print(f"      {k:40s} {hits[k]!r}")
        break

print("\n=== (c) skill_attackradiusspin template: mana-cost / channel semantics ===")
t = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
for n in t.names():
    if "attackradiusspin" in n.lower():
        txt = t.read_file(n).decode("latin-1")
        print(f"  --- {n} ({len(txt)} B)")
        for m in re.finditer(r'name = "([^"]*(?:[Mm]anaCost|Channel|channel|Duration|Interval)[^"]*)"', txt):
            print("      ", m.group(1))
