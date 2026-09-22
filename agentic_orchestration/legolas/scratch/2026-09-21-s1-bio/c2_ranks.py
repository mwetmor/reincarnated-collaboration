#!/usr/bin/env python3
"""C-2: enumerate +skill bonuses across every equipped item and affix. READ-ONLY."""
import sys, re; sys.path.insert(0,'.')
import gdcg7 as G, arz
SAVE="/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-05-eorwarlguts-parse/player.gdc"
res=G.parse(SAVE)
inv=res["blocks"]["inventory"]
srcs=[]
for grp in ("equipment","weapon1","weapon2"):
    for it in inv.get(grp,[]):
        if not it.get("baseName"): continue
        srcs.append((grp,"base",it["baseName"]))
        for f in ("prefixName","suffixName","modifierName","transmuteName","componentName","augmentName","relicBonus"):
            if it.get(f): srcs.append((grp,f,it[f]))
print(f"{'slot':10s} {'part':14s} {'record':56s}  bonus")
for grp,part,rec in srcs:
    n,d=arz.find(rec)
    if d is None: print(f"{grp:10s} {part:14s} {rec:56s}  NOT-FOUND"); continue
    out=[]
    if d.get("augmentAllLevel"): out.append(f"ALL +{d['augmentAllLevel']}")
    for i in range(1,9):
        m=d.get(f"augmentMasteryName{i}"); lv=d.get(f"augmentMasteryLevel{i}")
        if m and lv: out.append(f"MASTERY {m.split('/')[-1]} +{lv}")
        s=d.get(f"augmentSkillName{i}"); sl=d.get(f"augmentSkillLevel{i}")
        if s and sl: out.append(f"SKILL {s.replace('records/skills/','')} +{sl}")
    if out:
        print(f"{grp:10s} {part:14s} {rec.replace('records/items/',''):56s}  {' | '.join(out)}")
