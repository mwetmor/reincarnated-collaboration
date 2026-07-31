#!/usr/bin/env python3
"""D4 - Plague Walker true payload (poison DoT), Warden weapon term, trap/hazard bypass. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS=[ROOT/"database/database.arz",ROOT/"gdx1/database/GDX1.arz",ROOT/"gdx2/database/GDX2.arz",ROOT/"gdx3/database/GDX3.arz"]
ars=[(p.name,ArzArchive(p)) for p in ARZS]
def get(n):
    for nm,a in ars:
        if n in a.records: return a.read_record(n)
    return None
def show(rn,rank,keys=None):
    rec=get(rn)
    print(f"--- {rn.split('/')[-1]}  rank {rank}")
    if rec is None: print("    NOT FOUND"); return
    for k in sorted(rec):
        if not k.startswith("offensive") and k not in ("Class",): continue
        v=rec[k]
        if isinstance(v,list): v=v[min(rank-1,len(v)-1)]
        if v in (0,0.0,'',False,None): continue
        print(f"    {k:44s} {v}")

print("="*80); print("A. PLAGUE WALKER (zombie_g01) ability payloads at rank 4 (charLevel 13)"); print("="*80)
for rn in ["records/skills/nonplayerskills/path/zombie_barf.dbr",
           "records/skills/nonplayerskills/attackprojectile/poisongib_zombie.dbr",
           "records/skills/nonplayerskills/aoe/acidpool1.dbr",
           "records/skills/nonplayerskills/passive/damagebase_physical01.dbr"]:
    show(rn, 13 if "damagebase" in rn else 4); print()

print("="*80); print("B. WARDEN weapon term"); print("="*80)
for rn in ["records/items/gearweapons/blunt1h/gear_warden_mace.dbr"]:
    rec=get(rn)
    if rec is None:
        cands=[r for nm,a in ars for r in a.records if 'warden' in r.lower() and 'gearweapons' in r]
        print("  candidates:",cands[:10])
    else:
        for k in sorted(rec):
            if k.startswith("offensive") and rec[k]: print(f"    {k:44s} {rec[k]}")

print()
print("="*80); print("C. TRAP / HAZARD BYPASS - do non-Monster damage sources exist in Act 1?"); print("="*80)
COMPS=["Physical","Pierce","Fire","Cold","Lightning","Aether","Chaos","Life","Magical","Elemental"]
def inst(rec,rank):
    t=0.0;p={}
    for c in COMPS:
        for suf in ("Max","Min"):
            k=f"offensive{c}{suf}"
            if k not in rec: continue
            v=rec[k]
            if isinstance(v,list): v=v[min(rank-1,len(v)-1)]
            if v: p[c]=max(p.get(c,0.0),float(v))
    return sum(p.values()),p
rows=[]
seen=set()
for nm,a in ars:
    for r in a.records:
        low=r.lower()
        if not any(t in low for t in ("trap","hazard","spike","barrel","explod","brazier","mine")): continue
        if r in seen: continue
        seen.add(r)
        rec=a.read_record(r)
        cls=str(rec.get("Class") or "")
        if not cls.startswith("Skill_"): continue
        best=0.0;bp=None;br=None
        for rk in range(1,7):
            t,p=inst(rec,rk)
            if t>best: best,bp,br=t,p,rk
        if best>0: rows.append((best,r,br,bp))
rows.sort(reverse=True,key=lambda x:x[0])
print(f"  {len(rows)} trap/hazard-named skill records with instantaneous damage; top 15:")
for best,r,rk,p in rows[:15]:
    ps=" ".join(f"{k}{v:.0f}" for k,v in sorted(p.items(),key=lambda x:-x[1]))
    print(f"    {best:8.1f} r{rk}  {r.split('records/')[-1]:62s} {ps}")
