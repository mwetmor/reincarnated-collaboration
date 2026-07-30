#!/usr/bin/env python3
"""S1 — index Creatures.arc; find slith animation assets. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
p = pathlib.Path(sys.argv[1])
a = ArcArchive(p)
names = a.names()
print(f"ARC {p}  entries={len(names)}")
pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
n = 0
for nm in names:
    if pat is None or pat.search(nm):
        e = a.entries[nm]
        print(f"{nm}\tcomp={e['comp_size']}\tdecomp={e['decomp_size']}\tparts={e['num_parts']}")
        n += 1
print(f"-- matched {n}")
