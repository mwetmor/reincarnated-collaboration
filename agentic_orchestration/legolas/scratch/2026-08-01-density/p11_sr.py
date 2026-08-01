#!/usr/bin/env python3
"""P11 - Shattered Realm: ProxyEndless + EndlessDungeonFloor + generator/ruleset schemas. READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
g2=ArzArchive(ROOT/"gdx2/database/GDX2.arz"); g3=ArzArchive(ROOT/"gdx3/database/GDX3.arz")
M={}
for k,a in [("gdx2",g2),("gdx3",g3),("base",ArzArchive(ROOT/"database/database.arz")),
            ("gdx1",ArzArchive(ROOT/"gdx1/database/GDX1.arz"))]:
    for r in a.records: M.setdefault(r,(k,a))
def get(p):
    e=M.get(p); return e[1].read_record(p) if e else None

def show(cls,arc,name,n=2):
    got=0
    for r in sorted(arc.records):
        rec=arc.read_record(r)
        if str(rec.get('Class'))!=cls: continue
        print(f"\n--- [{name}] {r}  ({len(rec)} fields)  Class={cls}")
        for k,v in sorted(rec.items()): print(f"     {k} = {str(v)[:260]}")
        got+=1
        if got>=n: break

show('EndlessDungeonGenerator',g2,'gdx2',1)
show('EndlessDungeonFloor',g2,'gdx2',2)
show('ProxyEndless',g2,'gdx2',2)

print("\n\n### field union for ProxyEndless (gdx2+gdx3)")
fu=collections.Counter(); n=0
for a in (g2,g3):
    for r in a.records:
        rec=a.read_record(r)
        if str(rec.get('Class'))=='ProxyEndless':
            n+=1
            for k in rec: fu[k]+=1
print(f"n={n}")
for k,v in fu.most_common(40): print(f"   {k:36s} {v}")

print("\n### field union for EndlessDungeonFloor (gdx2+gdx3)")
fu=collections.Counter(); n=0
for a in (g2,g3):
    for r in a.records:
        rec=a.read_record(r)
        if str(rec.get('Class'))=='EndlessDungeonFloor':
            n+=1
            for k in rec: fu[k]+=1
print(f"n={n}")
for k,v in fu.most_common(40): print(f"   {k:36s} {v}")

print("\n### endlessdungeon/rulesets + difficultyscaling (gdx2)")
for r in sorted(g2.records):
    if "endlessdungeon/rulesets" in r or "endlessdungeon/difficultyscaling" in r:
        rec=g2.read_record(r); print(f"\n--- {r} ({len(rec)} fields) Class={rec.get('Class')}")
        for k,v in sorted(rec.items()): print(f"     {k} = {str(v)[:200]}")
