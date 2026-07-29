#!/usr/bin/env python3
"""probe10 — open database/templates.arc and read skillpanebase.tpl / skill.tpl / skill_mastery.tpl.
Hunting the mastery-tier milestone values that the .dbr does not carry.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive

CANDIDATES = [
    pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc"),
]
for p in CANDIDATES:
    if not p.exists():
        print(f"ABSENT: {p}")
        continue
    a = ArcArchive(p)
    names = a.names()
    print(f"=== {p}  entries={len(names)}")
    hits = [n for n in names if re.search(r"(skillpane|skillbutton|mastery|skilltree|experiencelevel)", n, re.I)]
    for n in sorted(hits):
        print("   ", n)
    print()
    for n in sorted(hits):
        if re.search(r"(skillpanebase|experiencelevelcontrol|skill_mastery|skilltree)", n, re.I):
            payload = a.read_file(n).decode("latin-1")
            print(f"--- {n}  ({len(payload)} B)")
            for line in payload.splitlines():
                if re.search(r"(milestone|Milestone|tier|Tier|skillModifier|initialSkill)", line):
                    print("    ", line.strip())
            print()
