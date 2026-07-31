#!/usr/bin/env python3
"""W9 - join Monster records -> controller DBR -> aggro params, binned by monsterClassification. READ-ONLY."""
import sys, pathlib, collections, statistics
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
allrec={}; ctrl={}
for nm,p in ARZS:
    if not p.exists(): continue
    a=ArzArchive(p)
    for r in a.records:
        try: rec=a.read_record(r)
        except Exception: continue
        c=rec.get("Class","")
        if c=="Monster": allrec[r.lower()]=rec
        if c and c.startswith("Controller"): ctrl[r.lower()]=rec
print(f"Monster records: {len(allrec)}   Controller records: {len(ctrl)}")

# which Monster field points at a controller dbr?
ptr=collections.Counter()
for r,rec in allrec.items():
    for k,v in rec.items():
        vv=v[0] if isinstance(v,list) and v else v
        if isinstance(vv,str) and vv.lower() in ctrl: ptr[k]+=1
print("Monster fields pointing at controller records:",ptr.most_common())

FIELDS=["ViewDistance","InnerViewDistance","MaxYViewDistance","AngerTolerance","SightAngerRate",
        "InnerSightAngerRate","AttackedAnger","AllyAttackedAnger","ProjectileAnger","ForgiveRate",
        "MaxPursuitDistance","PursuitTime","ChanceToRespondToDistressCall","DistressResponseBehavior",
        "RandomAngerChance","enemyTooClose","ResetOriginAfterFleeing","ClearAngerWhenFleeing"]
MFIELDS=["distressCall","distressCallRange","distressCallTime","maxDistressCalls","distressCallGroup"]
PKEY=ptr.most_common(1)[0][0] if ptr else None
print("join key:",PKEY)

bins=collections.defaultdict(lambda: collections.defaultdict(list))
mbins=collections.defaultdict(lambda: collections.defaultdict(list))
counts=collections.Counter()
for r,rec in allrec.items():
    cls=rec.get("monsterClassification","(none)")
    if isinstance(cls,list): cls=cls[0] if cls else "(none)"
    counts[cls]+=1
    for f in MFIELDS:
        v=rec.get(f)
        if isinstance(v,list): v=v[0] if v else None
        if v is not None: mbins[cls][f].append(v)
    cp=rec.get(PKEY) if PKEY else None
    if isinstance(cp,list): cp=cp[0] if cp else None
    cr=ctrl.get(str(cp).lower()) if cp else None
    if not cr: continue
    for f in FIELDS:
        v=cr.get(f)
        if isinstance(v,list): v=v[0] if v else None
        if v is not None: bins[cls][f].append(v)

print("\nmonsterClassification counts:",counts.most_common())
def summarize(d,label):
    print("\n"+"="*100); print(label); print("="*100)
    for cls in sorted(d, key=lambda c:-counts[c]):
        print(f"\n--- {cls}  (n={counts[cls]}) ---")
        for f in sorted(d[cls]):
            vals=d[cls][f]
            if not vals: continue
            if all(isinstance(x,(int,float)) for x in vals):
                md=statistics.median(vals); mo=collections.Counter(vals).most_common(3)
                print(f"   {f:32s} n={len(vals):5d} median={md:<10} mode={mo}")
            else:
                print(f"   {f:32s} n={len(vals):5d} {collections.Counter(map(str,vals)).most_common(4)}")
summarize(bins,"CONTROLLER AI PARAMS by monsterClassification (joined via %s)"%PKEY)
summarize(mbins,"MONSTER-SIDE distressCall PARAMS by monsterClassification")
