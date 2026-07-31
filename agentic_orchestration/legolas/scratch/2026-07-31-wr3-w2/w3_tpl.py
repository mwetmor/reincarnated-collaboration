#!/usr/bin/env python3
"""W3 - pull controllermonster.tpl + monster.tpl from templates.arc, dump field defs. READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import gd_arc_reader_2026_07_26 as arc
P=pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
print("reader API:", [n for n in dir(arc) if not n.startswith("_")])
