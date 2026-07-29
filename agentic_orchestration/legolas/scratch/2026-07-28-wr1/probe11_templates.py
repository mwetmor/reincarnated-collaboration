#!/usr/bin/env python3
"""probe11 (WR1 E-1/E-3) — templates.arc (legacy pin ~/Games/vendor/grim-dawn/database/templates.arc,
NOT the Edition-II pin which ships no templates.arc):
  (a) skill_attackprojectilering.tpl — is any telegraph/windup field defined?
  (b) weapon templates — characterBaseAttackSpeed defaultValue / speed tag defaults
Read-only."""
import sys, pathlib, re
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive
P = pathlib.Path("/Users/admin/Games/vendor/grim-dawn/database/templates.arc")
a = ArcArchive(P)
names = a.names()
print(f"templates.arc entries: {len(names)}")
for want in ("skill_attackprojectilering.tpl","weapon_melee.tpl","weaponmelee.tpl","monster.tpl"):
    hits=[n for n in names if n.lower().endswith(want)]
    print(f"  match {want}: {hits[:4]}")
def show(name, pats):
    try: raw=a.read_file(name)
    except Exception as e:
        print(f"  !! {name}: {e}"); return
    txt=raw.decode('utf-8','replace')
    print(f"\n=== {name} ({len(txt)} chars)")
    for m in re.finditer(r'Variable\s*\{(.*?)\}', txt, re.S):
        blk=m.group(1)
        nm=re.search(r'name\s*=\s*"([^"]*)"', blk)
        if nm and any(p.lower() in nm.group(1).lower() for p in pats):
            dv=re.search(r'defaultValue\s*=\s*"([^"]*)"', blk)
            de=re.search(r'description\s*=\s*"([^"]*)"', blk)
            print(f"  {nm.group(1):40s} default={dv.group(1) if dv else None!r:14s} desc={de.group(1) if de else ''}")
for n in names:
    ln=n.lower()
    if ln.endswith('skill_attackprojectilering.tpl'):
        show(n, ['time','delay','windup','cast','cooldown','duration','anim','charge','projectile','radius'])
    if re.search(r'weapon.*\.tpl$', ln) and 'melee' in ln:
        show(n, ['attackspeed','speed'])
