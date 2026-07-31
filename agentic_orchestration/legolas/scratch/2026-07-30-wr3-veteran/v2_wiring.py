#!/usr/bin/env python3
"""V2 - where is the Veteran record referenced from, and what template fields exist? READ-ONLY."""
import sys, pathlib, re
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[("base",ROOT/"database/database.arz"),("gdx1",ROOT/"gdx1/database/GDX1.arz"),
      ("gdx2",ROOT/"gdx2/database/GDX2.arz"),("gdx3",ROOT/"gdx3/database/GDX3.arz")]
ars=[(n,ArzArchive(p)) for n,p in ARZS]

NEEDLES=["balancingadjustment_challengemode_enemies01","balancingadjustment_ultramode_enemies01",
         "balancingadjustment_mp+difficulty_enemies01"]
print("="*100); print("INBOUND REFERENCES (which records point AT the mutator paks)"); print("="*100)
for nm,a in ars:
    for r in a.records:
        try: rec=a.read_record(r)
        except Exception: continue
        for k,v in rec.items():
            if not isinstance(v,str): continue
            for nd in NEEDLES:
                if nd in v:
                    print(f"  [{nm}] {r}\n        {k} = {v}")
print()

print("="*100); print("EXPERIENCE / spawn* FIELD SWEEP across ALL records"); print("="*100)
xp={}; spawn={}
for nm,a in ars:
    for r in a.records:
        try: rec=a.read_record(r)
        except Exception: continue
        for k,v in rec.items():
            kl=k.lower()
            if "experience" in kl or "expmodifier" in kl or kl.startswith("xp"):
                if isinstance(v,str) or v or (isinstance(v,list) and any(v)):
                    xp.setdefault(k,[]).append((nm,r,v))
            if kl.startswith("spawn"):
                spawn.setdefault(k,[]).append((nm,r,v))
print("--- experience-family field names seen (with count + up to 6 examples) ---")
for k in sorted(xp):
    print(f"  {k}  (n={len(xp[k])})")
    for nm,r,v in xp[k][:6]:
        print(f"        [{nm}] {r}  = {v}")
print()
print("--- spawn* field names seen ---")
for k in sorted(spawn):
    nz=[(nm,r,v) for nm,r,v in spawn[k] if (v if not isinstance(v,list) else any(v))]
    print(f"  {k:34s} total={len(spawn[k]):6d}  nonzero={len(nz)}")
    for nm,r,v in nz[:8]:
        print(f"        [{nm}] {r}  = {v}")
