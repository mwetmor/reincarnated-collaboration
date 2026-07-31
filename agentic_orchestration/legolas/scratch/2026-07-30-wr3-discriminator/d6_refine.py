#!/usr/bin/env python3
"""D6 - resolve the top trash-tier threats at their ACTUAL charLevel/rank at player level 13. READ-ONLY."""
import sys, pathlib, re
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

def ev(expr, cl):
    if expr is None: return None
    s=str(expr).replace("charLevel",str(cl))
    try: return int(eval(s))
    except Exception: return None

# spawn tiers at averagePlayerLevel 13 (from envelope note SS1b, MEASURED)
SPAWN={"Common":(12,13),"Champion":(14,14),"Hero":(15,16),"Quest":(16,17)}

TARGS=["records/creatures/enemies/bounties/dc_bounty06.dbr",
       "records/creatures/enemies/bounties/dc_bounty15.dbr",
       "records/creatures/enemies/boss&quest/payingtribute_silas_01.dbr",
       "records/creatures/enemies/devotion/slith_h08.dbr",
       "records/creatures/enemies/humanchthonic_cultist_c02.dbr",
       "records/creatures/enemies/zombie_g01.dbr",
       "records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr",
       "records/creatures/enemies/boss&quest/warden01.dbr"]
print(f"{'monster':44s} {'cls':9s} {'spawn':>7s} {'charL':>5s} {'AB':>4s} {'S2fac':>6s}  best ability @ real rank")
print("="*140)
for t in TARGS:
    if t not in a.records: print(f"  MISSING {t}"); continue
    rec=a.read_record(t)
    cls=str(rec.get('monsterClassification'))
    lo,hi=SPAWN.get(cls,(13,13))
    cl=ev(rec.get('charLevel'), hi) or hi
    sk=[rec.get(f'skillName{i}') for i in range(1,25)]; sk=[s for s in sk if s]
    ab=None
    for s in sk:
        m=re.search(r'armorbase(\d\d)',s)
        if m: ab=int(m.group(1))
    tier='trash' if ab in (1,2) else 'boss'
    dm=(-56+cl) if tier=='trash' else (-91+cl)
    f2=(1+(dm+8)/100.0)*0.75
    best=(0.0,None,None,None)
    for s in sk:
        if s not in a.records: continue
        srec=a.read_record(s)
        if not str(srec.get('Class','')).startswith('Skill_'): continue
        lvlexpr=None
        for i in range(1,25):
            if rec.get(f'skillName{i}')==s: lvlexpr=rec.get(f'skillLevel{i}')
        rk=ev(lvlexpr, cl) or 1
        rk=max(1,rk)
        tot,p=inst(srec,rk)
        if tot>best[0]: best=(tot,s,rk,p)
    tot,s,rk,p=best
    ps=" ".join(f"{k}{v:.0f}" for k,v in sorted(p.items(),key=lambda x:-x[1])) if p else ""
    print(f"{t.split('enemies/')[-1]:44s} {cls:9s} {hi:7d} {cl:5d} {str(ab):>4s} {f2:6.4f}  "
          f"{(s or '-').split('nonplayerskills/')[-1]:42s} r{rk} raw {tot:6.1f} | S1 {tot*0.75:6.1f} | S2 {tot*f2:6.1f}   {ps}")

print()
print("="*140)
print("SPAWN-REACHABILITY of the two outlaw threats: which proxies place them, and at what player level?")
print("="*140)
for name in ("dc_bounty06","dc_bounty15","payingtribute_silas_01"):
    users=[]
    for r in a.records:
        if not r.startswith("records/proxies/"): continue
        rec=a.read_record(r)
        for k,v in rec.items():
            if isinstance(v,str) and name in v: users.append((r,k)); break
    print(f"  {name}: referenced by {len(users)} proxy record(s)")
    for r,k in users[:6]:
        rec=a.read_record(r)
        gates={kk:vv for kk,vv in rec.items() if 'PlayerLevel' in kk and vv}
        print(f"      {r.split('proxies/')[-1]:60s} {k}  gates={gates}")
