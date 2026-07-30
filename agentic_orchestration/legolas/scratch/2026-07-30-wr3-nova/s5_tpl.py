#!/usr/bin/env python3
"""S5 — list/dump templates from the legacy pin templates.arc. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
P = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
a = ArcArchive(P)
names = a.names()
if sys.argv[1] == "ls":
    pat = re.compile(sys.argv[2], re.I)
    for n in sorted(names):
        if pat.search(n): print(n)
    print(f"-- total entries {len(names)}")
else:
    for n in names:
        if n.lower().endswith(sys.argv[1].lower()):
            txt = a.read_file(n).decode('utf-8','replace')
            print(f"=== {n} ({len(txt)} chars)")
            for m in re.finditer(r'Variable\s*\{(.*?)\}', txt, re.S):
                blk = m.group(1)
                nm = re.search(r'name\s*=\s*"([^"]*)"', blk)
                dv = re.search(r'defaultValue\s*=\s*"([^"]*)"', blk)
                de = re.search(r'description\s*=\s*"([^"]*)"', blk)
                ty = re.search(r'type\s*=\s*"([^"]*)"', blk)
                if nm:
                    print(f"  {nm.group(1):40s} type={ty.group(1) if ty else '':10s} default={(dv.group(1) if dv else None)!r:12s} desc={de.group(1) if de else ''}")
