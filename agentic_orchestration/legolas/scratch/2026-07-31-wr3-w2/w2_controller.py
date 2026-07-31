#!/usr/bin/env python3
"""W2 - full field dump of ControllerMonster* records + value distributions. READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
CTRL={"ControllerMonster","ControllerStationaryMonster","ControllerMonsterHidden",
      "ControllerTotem","ControllerMonsterSynergy","ControllerNpc","ControllerNpc2",
      "ControllerSpirit","ControllerGraeae","ControllerPet","ControllerPlayer"}
recs=[]
for nm,p in ARZS:
    if not p.exists(): continue
    a=ArzArchive(p)
    for r in a.records:
        try: rec=a.read_record(r)
        except Exception: continue
        if rec.get("Class") in CTRL: recs.append((nm,r,rec))
print(f"TOTAL controller records: {len(recs)}")
bycls=collections.Counter(r[2].get("Class") for r in recs)
print("by class:",bycls.most_common())

# 1. one exemplar full dump
print("\n"+"="*110+"\nEXEMPLAR full field dump (first ControllerMonster)\n"+"="*110)
for nm,r,rec in recs:
    if rec.get("Class")=="ControllerMonster":
        print(f"{r}  [{nm}]  {len(rec)} fields")
        for k in sorted(rec): print(f"   {k:44s} {rec[k]}")
        break

# 2. field census + value distribution over ControllerMonster only
cm=[x for x in recs if x[2].get("Class")=="ControllerMonster"]
print("\n"+"="*110+f"\nFIELD VALUE DISTRIBUTION over {len(cm)} ControllerMonster records\n"+"="*110)
fv=collections.defaultdict(collections.Counter)
for nm,r,rec in cm:
    for k,v in rec.items():
        sv=v[0] if isinstance(v,list) and v else v
        fv[k][str(sv)]+=1
for k in sorted(fv):
    top=fv[k].most_common(10)
    print(f"\n{k}  (present in {sum(fv[k].values())})")
    print(f"   {top}")
