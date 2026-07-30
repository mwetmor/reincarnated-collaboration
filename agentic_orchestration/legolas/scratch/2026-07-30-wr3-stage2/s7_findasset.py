#!/usr/bin/env python3
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
root = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")
pat = re.compile(sys.argv[1], re.I)
for p in sorted(root.rglob("*.arc")):
    try: a = ArcArchive(p)
    except Exception as e: continue
    hits = [n for n in a.names() if pat.search(n)]
    if hits:
        print(f"## {p.relative_to(root)}  ({len(hits)} hits of {len(a.names())})")
        for h in hits[:40]: print("   ", h)
