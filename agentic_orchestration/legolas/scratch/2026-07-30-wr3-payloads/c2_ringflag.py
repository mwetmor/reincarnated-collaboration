#!/usr/bin/env python3
"""C2 — control test: does projectileUsesAllDamage appear on launchNumber==1 records? READ-ONLY."""
import sys, pathlib
from collections import Counter
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[ArzArchive(p) for p in ARZS]
c=Counter(); ex1=[]
tot=0
for a in ars:
    for r in a.records:
        rec=None
        t=a.record_type(r)
        if not t: continue
        rec=None
        if 'projectileUsesAllDamage' in (rec or {}): pass
        # only load skill records
        if not t.startswith('Skill'): continue
        rec=a.read_record(r)
        if 'projectileUsesAllDamage' not in rec: continue
        tot+=1
        n=rec.get('projectileLaunchNumber',1)
        if isinstance(n,list): n=max(n)
        u=rec['projectileUsesAllDamage']
        c[(t,n==1,u)]+=1
        if n==1 and u is True and len(ex1)<25: ex1.append((t,r))
print(f"skill records declaring projectileUsesAllDamage: {tot}")
print("\n(Class, launchNumber==1, usesAllDamage) :")
for k,v in sorted(c.items(), key=lambda x:-x[1])[:30]: print(f"  {k[0]:36s} single={k[1]!s:6s} usesAll={k[2]!r:7s} {v}")
print(f"\nEXAMPLES of launchNumber==1 AND usesAllDamage==True  (n={sum(v for k,v in c.items() if k[1] and k[2] is True)}):")
for t,r in ex1: print(f"  {t:34s} {r}")
