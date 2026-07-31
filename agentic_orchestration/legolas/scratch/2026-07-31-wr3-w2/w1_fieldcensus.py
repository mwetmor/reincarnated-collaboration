#!/usr/bin/env python3
"""W1 - census every FIELD NAME across all GD archives matching aggro/leash/social keywords. READ-ONLY."""
import sys, pathlib, collections
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]

KEYS=["aggro","leash","social","awareness","aware","perception","notice","alert","flee",
      "pursu","chase","territor","tether","retreat","wander","roam","sight","detect","radius",
      "distance","range","group","pack","spawn","call","help","assist","threat","hate","taunt",
      "return","home","reset","regen"]

fieldcount=collections.Counter()
fieldvals=collections.defaultdict(collections.Counter)
fieldrecs=collections.defaultdict(list)
classes_with=collections.defaultdict(collections.Counter)

for nm,p in ARZS:
    if not p.exists(): continue
    a=ArzArchive(p)
    print(f"[{nm}] {len(a.records)} records", file=sys.stderr)
    for r in a.records:
        try: rec=a.read_record(r)
        except Exception: continue
        cls=rec.get("Class","?")
        for k,v in rec.items():
            lk=k.lower()
            if any(key in lk for key in KEYS):
                fieldcount[k]+=1
                classes_with[k][cls]+=1
                sv = v[0] if isinstance(v,list) and v else v
                fieldvals[k][str(sv)]+=1
                if len(fieldrecs[k])<6: fieldrecs[k].append((nm,r))

print("="*110)
print("FIELD-NAME CENSUS - keyword-matching fields across all four archives")
print("="*110)
for k,c in fieldcount.most_common():
    cls=", ".join(f"{a}:{b}" for a,b in classes_with[k].most_common(4))
    print(f"\n{k}   (n={c})   classes[{cls}]")
    tv=fieldvals[k].most_common(8)
    print(f"   top values: {tv}")
