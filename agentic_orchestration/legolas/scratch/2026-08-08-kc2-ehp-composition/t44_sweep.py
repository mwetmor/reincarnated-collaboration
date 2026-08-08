#!/usr/bin/env python3
"""Final Q5 sweep: EVERY proxylevelvarianceequation record in the corpus, any archive."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from t0_lib import archives, owners
found={}
for k,a in archives():
    for r in a.records:
        rec=a.read_record(r)
        if rec.get("templateName","").lower().endswith("proxylevelvarianceequation.tpl"):
            found.setdefault(r.lower(),[]).append((k,rec))
print(f"{len(found)} distinct level-variance records corpus-wide")
sm=[p for p,l in found.items() if any(k.startswith("sm") for k,_ in l)]
print(f"  carried by ANY survivalmode archive: {len(sm)} -> {sm}")
nonzero_epic=[]
for p,l in found.items():
    for k,rec in l:
        for f in ("minVarianceEquationEpic","maxVarianceEquationEpic","minVarianceEquationLegendary","maxVarianceEquationLegendary"):
            if rec.get(f): nonzero_epic.append((p,k,f,rec[f]))
print(f"  records populating Epic/Legendary branches: {len(nonzero_epic)}")
for x in nonzero_epic[:10]: print("   ",x)
# any equation referencing gameDifficulty anywhere?
gd=[]
for p,l in found.items():
    for k,rec in l:
        for f,v in rec.items():
            if isinstance(v,str) and "gameDifficulty" in v: gd.append((p,k,f,v))
print(f"  equations referencing gameDifficulty: {len(gd)}")
for x in gd[:10]: print("   ",x)
