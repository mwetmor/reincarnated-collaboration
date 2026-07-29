#!/usr/bin/env python3
"""probe15 — (a) SkillChanneled.tpl (per-second mana semantics), (b) gameengine.dbr full numeric dump
for spirit->energy conversion, (c) localization tags for EoR + the energy-cost UI line.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

t = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
print("=== (a) SkillChanneled.tpl ===")
for n in t.names():
    if n.lower().endswith("skillchanneled.tpl"):
        print(t.read_file(n).decode("latin-1"))
        break

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a = ArzArchive(ROOT / "database/database.arz")
rec = a.read_record("records/game/gameengine.dbr")
print("\n=== (b) gameengine.dbr numeric fields ===")
for k in sorted(rec):
    v = rec[k]
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        print(f"    {k:52s} {v!r}")
    elif isinstance(v, list) and v and isinstance(v[0], (int, float)):
        print(f"    {k:52s} [n={len(v)}] {v}")

print("\n=== (c) localization: EoR tags + energy-cost UI line ===")
res = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
arcs = list(res.rglob("Text_EN.arc"))
want = re.compile(r"(tagGDX2Class09SkillName07A|tagGDX2Class09SkillDescription07A|"
                  r"tagSkill.*(Mana|Energy|Cost|Tier|Mastery))", re.I)
for p in arcs:
    try:
        arc = ArcArchive(p)
    except Exception as e:
        print(f"  {p}: {e}"); continue
    for n in arc.names():
        if not n.lower().endswith(".txt"):
            continue
        try:
            tags = parse_tag_file(arc.read_file(n))
        except Exception:
            continue
        for k, v in tags.items():
            if want.search(k):
                print(f"  {p.parent.parent.name}/{n}  {k} = {v!r}")

# expansion Text_EN.arc live under gdx*/resources
for sub in ("gdx1", "gdx2", "gdx3"):
    for p in (ROOT / sub).rglob("Text_EN.arc"):
        arc = ArcArchive(p)
        for n in arc.names():
            if not n.lower().endswith(".txt"):
                continue
            try:
                tags = parse_tag_file(arc.read_file(n))
            except Exception:
                continue
            for k, v in tags.items():
                if want.search(k):
                    print(f"  {sub}/{n}  {k} = {v!r}")
