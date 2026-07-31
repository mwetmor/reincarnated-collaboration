#!/usr/bin/env python3
"""D5 - trash/champion-tier reachable ceiling (monsters carrying armorbase01/02), base-campaign only. READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
COMPS=["Physical","Pierce","Fire","Cold","Lightning","Aether","Chaos","Life","Magical","Elemental"]
def inst(rec,rank):
    p={}
    for c in COMPS:
        for suf in ("Max","Min"):
            k=f"offensive{c}{suf}"
            if k not in rec: continue
            v=rec[k]
            if isinstance(v,list): v=v[min(rank-1,len(v)-1)]
            if v: p[c]=max(p.get(c,0.0),float(v))
    return sum(p.values()),p
cache={}
def skillmax(sn):
    if sn in cache: return cache[sn]
    if sn not in a.records: cache[sn]=(0.0,None,None); return cache[sn]
    rec=a.read_record(sn)
    best=0.0;bp=None;br=None
    for rk in range(1,7):
        t,p=inst(rec,rk)
        if t>best: best,bp,br=t,p,rk
    cache[sn]=(best,bp,br); return cache[sn]

rows=[]
for r in a.records:
    if not r.startswith("records/creatures/enemies/"): continue
    if a.record_type(r)!="Monster": continue
    rec=a.read_record(r)
    sk=[rec.get(f'skillName{i}') for i in range(1,25)]
    sk=[s for s in sk if s]
    tier=None
    for s in sk:
        if 'armorbase01' in s or 'armorbase02' in s: tier='trash'
        elif 'armorbase0' in s: tier='boss'
    if tier!='trash': continue
    best=0.0;bs=None;bp=None;br=None
    for s in sk:
        t,p,rk=skillmax(s)
        if t>best: best,bs,bp,br=t,s,p,rk
    if best>0: rows.append((best,r,bs,bp,br,rec.get('monsterClassification')))
rows.sort(reverse=True,key=lambda x:x[0])
print("="*100)
print("TRASH/CHAMPION-TIER (armorbase01/02) REACHABLE CEILING - base campaign creatures, top 18")
print("  S2 factor at charLevel 13 = x0.4875 ; need raw 534.4 to land 260.498")
print("="*100)
print(f"  {'raw':>7s} {'S1x.75':>8s} {'S2x.4875':>9s}  {'class':10s} monster / best ability")
for best,r,bs,bp,br,cls in rows[:18]:
    ps=" ".join(f"{k}{v:.0f}" for k,v in sorted(bp.items(),key=lambda x:-x[1]))
    print(f"  {best:7.1f} {best*0.75:8.1f} {best*0.4875:9.1f}  {str(cls):10s} {r.split('enemies/')[-1]:44s} <- {bs.split('nonplayerskills/')[-1]:40s} {ps}")
print()
print(f"  TRASH CEILING (raw)     = {rows[0][0]:.1f}")
print(f"  under S2 (x0.4875)      = {rows[0][0]*0.4875:.1f}   vs measured 260.498 ->  {'REACHES' if rows[0][0]*0.4875>=260.498 else 'CANNOT REACH'}")
print(f"  under S1 (x0.75)        = {rows[0][0]*0.75:.1f}   vs measured 260.498 ->  {'REACHES' if rows[0][0]*0.75>=260.498 else 'CANNOT REACH'}")
