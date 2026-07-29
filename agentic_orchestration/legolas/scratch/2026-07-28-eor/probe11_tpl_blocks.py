#!/usr/bin/env python3
"""probe11 — print the full Variable blocks for masteryMilestone* and skillModifierPoints.
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive

a = ArcArchive("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")

def blocks(text, keys):
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if re.search(r'name\s*=\s*"(' + "|".join(keys) + r')"', ln):
            lo = max(0, i - 8); hi = min(len(lines), i + 12)
            print("   " + "\n   ".join(l.rstrip() for l in lines[lo:hi]))
            print("   " + "-" * 60)

print("=== ingameui/skillpanebase.tpl ===")
blocks(a.read_file("ingameui/skillpanebase.tpl").decode("latin-1"),
       ["masteryMilestoneValueMax", "masteryMilestoneNumber1"])

print("\n=== experiencelevelcontrol.tpl ===")
blocks(a.read_file("experiencelevelcontrol.tpl").decode("latin-1"),
       ["skillModifierPoints", "initialSkillPoints", "characterModifierPoints"])

print("\n=== skill.tpl-family: hunt skillTier / skillMasteryLevelRequired declarations ===")
for n in a.names():
    if not n.endswith(".tpl"):
        continue
    try:
        t = a.read_file(n).decode("latin-1")
    except Exception:
        continue
    if re.search(r'"(skillTier|skillMasteryLevelRequired)"', t):
        print(f"--- {n}")
        blocks(t, ["skillTier", "skillMasteryLevelRequired"])
        break
