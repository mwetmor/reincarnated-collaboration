#!/usr/bin/env python3
"""V6 - the XP channel + gameascendant + gameengine challenge wiring. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ars=[("base",ArzArchive(ROOT/"database/database.arz")),("gdx1",ArzArchive(ROOT/"gdx1/database/GDX1.arz")),
     ("gdx2",ArzArchive(ROOT/"gdx2/database/GDX2.arz")),("gdx3",ArzArchive(ROOT/"gdx3/database/GDX3.arz"))]
def dump(n,keys=None):
    for nm,a in ars:
        if n not in a.records: continue
        rec=a.read_record(n)
        print("="*100); print(f"{n}   [{nm}]  Class={rec.get('Class')} tpl={rec.get('templateName')} ({len(rec)} fields)"); print("="*100)
        for k in sorted(rec):
            v=rec[k]
            if keys and not any(t in k.lower() for t in keys): continue
            if isinstance(v,list): v = v[0] if len(set(v))==1 else v
            if v in (0,0.0,None,''): continue
            print(f"   {k:46s} {v}")
        print()

dump("records/game/experienceformulas.dbr")
dump("records/game/gameascendant.dbr")
dump("records/game/gameengine.dbr", keys=["challenge","experience","champion","hero","mutator","spawn","difficulty"])

# XP arithmetic: normal vs challenge equations at the referent's parameters
print("="*100); print("XP EQUATION EVALUATION"); print("="*100)
import re
a=ars[0][1]; rec=a.read_record("records/game/experienceformulas.dbr")
eqs={k:v for k,v in rec.items() if isinstance(v,str) and ("Equation" in k or "equation" in k)}
for k,v in eqs.items(): print(f"  {k}\n      {v}")
def evaluate(expr, monsterLevel, averagePartyLevel, monsterExperience):
    e=expr.replace("^","**").replace("monsterLevel",str(monsterLevel)) \
          .replace("averagePartyLevel",str(averagePartyLevel)).replace("monsterExperience",str(monsterExperience))
    return eval(e)
print()
base=eqs.get("normalExperienceEquation") or eqs.get("experienceEquation")
chal=eqs.get("challengeExperienceEquation")
print(f"  {'mL':>4s} {'aPL':>4s} {'mExp':>5s} {'normal':>10s} {'challenge':>10s} {'ratio':>7s}")
for mL,aPL in ((13,13),(15,13),(16,13),(18,13),(19,13),(20,13),(13,12)):
    for mE in (0,50,100):
        if base and chal:
            b=evaluate(base,mL,aPL,mE); c=evaluate(chal,mL,aPL,mE)
            print(f"  {mL:4d} {aPL:4d} {mE:5d} {b:10.3f} {c:10.3f} {c/b:7.4f}")
