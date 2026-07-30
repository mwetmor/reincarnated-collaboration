#!/usr/bin/env python3
"""S6 — resolve display tags from Text_EN.arc across all pins. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file
ROOT = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARCS = [ROOT/"resources/Text_EN.arc", ROOT/"gdx1/resources/Text_EN.arc",
        ROOT/"gdx2/resources/Text_EN.arc", ROOT/"gdx3/resources/Text_EN.arc"]
pat = re.compile(sys.argv[1], re.I)
for p in ARCS:
    a = ArcArchive(p)
    for nm in a.names():
        if not nm.lower().endswith(".txt"): continue
        try: pairs = parse_tag_file(a.read_file(nm))
        except Exception: continue
        for k, v in pairs:
            if pat.search(k):
                print(f"{p.parent.parent.name}/{nm}\t{k}\t{v}")
