#!/usr/bin/env python3
"""probe17 — settle whether skillManaCost on a channelled skill is per-tick or per-second.
Triangulate EoR against Flames of Ignaffar and Albrecht's Aether Ray (both channelled),
using their .arz costs + their developer-authored description text + the banked corpus tick interval.
Read-only."""
import sys, pathlib, re, sqlite3
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
archives = {p.name: ArzArchive(p) for p in [
    ROOT / "database/database.arz", ROOT / "gdx1/database/GDX1.arz",
    ROOT / "gdx2/database/GDX2.arz", ROOT / "gdx3/database/GDX3.arz"]}

TARGETS = {
    "EoR":  "records/skills/playerclass09/eyeofreckoning1.dbr",
    "FoI":  "records/skills/playerclass07/purifyingflame1.dbr",
    "AAR":  "records/skills/playerclass05/aetherray1.dbr",
}
desc_tags = {}
for label, rp in TARGETS.items():
    for name, a in archives.items():
        if rp in a.records:
            rec = a.read_record(rp)
            print(f"=== {label}  {rp}   <-{name}   [{rec.get('Class')}]")
            print(f"    skillManaCost   {rec.get('skillManaCost')}")
            print(f"    timeBetweenAttacks {rec.get('timeBetweenAttacks')}   duration {rec.get('duration')}")
            print(f"    descTag {rec.get('skillBaseDescription')}")
            desc_tags[label] = rec.get("skillBaseDescription")
            print()

print("=== developer description text ===")
for p in sorted(ROOT.rglob("Text_EN.arc")):
    try:
        arc = ArcArchive(p)
    except Exception:
        continue
    for n in arc.names():
        try:
            pairs = parse_tag_file(arc.read_file(n))
        except Exception:
            continue
        for k, v in pairs:
            for label, tag in desc_tags.items():
                if tag and k == tag:
                    print(f"  [{label}] {k}:")
                    for sent in re.split(r"(?<=\.)\s+", v):
                        if re.search(r"(Energy|drain|second|0\.\d)", sent, re.I):
                            print(f"      >> {sent.strip()}")
                    print()

print("=== corpus kit_numeric rows for FoI (tick interval + energy) ===")
DB = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/curated/corpus.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
for row in con.execute(
        "SELECT * FROM kit_numeric WHERE lower(coalesce(metric_key,''))"
        " LIKE '%tick%' OR lower(coalesce(metric_key,'')) LIKE '%energy%'"
        " OR lower(coalesce(metric_key,'')) LIKE '%mana%'"):
    print("  ", row)
con.close()
