#!/usr/bin/env python3
"""W4 - dump controllermonster.tpl + monster AI template field defs. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
P=pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
a=ArcArchive(P)
names=list(a.entries.keys()) if hasattr(a,"entries") else list(a.names)
print(f"{len(names)} entries")
hits=[n for n in names if any(k in n.lower() for k in ("controller","monster","ai","npc"))]
for h in sorted(hits): print("  ",h)
