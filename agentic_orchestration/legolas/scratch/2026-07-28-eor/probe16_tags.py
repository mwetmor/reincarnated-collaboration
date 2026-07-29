#!/usr/bin/env python3
"""probe16 — localization: EoR display name/description + the energy-cost tooltip line format
(per-second vs per-cast) + mastery-tier requirement phrasing.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
want = re.compile(
    r"(tagGDX2Class09SkillName07A|tagGDX2Class09SkillDescription07A"
    r"|EnergyCost|ManaCost|PerSecond|persecond|MasteryLevel|SkillTier|RequiresMastery)", re.I)

for p in sorted(ROOT.rglob("Text_EN.arc")):
    try:
        arc = ArcArchive(p)
    except Exception as e:
        print(f"  {p}: {e}")
        continue
    label = str(p.relative_to(ROOT))
    for n in arc.names():
        try:
            pairs = parse_tag_file(arc.read_file(n))
        except Exception:
            continue
        for k, v in pairs:
            if want.search(k):
                print(f"  {label} :: {n} :: {k} = {v!r}")
