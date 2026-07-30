#!/usr/bin/env python3
"""S2 — extract named files out of an ARC to scratch. READ-ONLY on vendor tree."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
arc, pat, out = sys.argv[1], re.compile(sys.argv[2], re.I), pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
a = ArcArchive(arc)
for nm in a.names():
    if pat.search(nm):
        data = a.read_file(nm)
        dest = out / nm.replace("/", "__")
        dest.write_bytes(data)
        print(f"{nm} -> {dest.name}  {len(data)} B")
