#!/usr/bin/env python3
"""V10 - encounter-mix arithmetic: Normal vs Veteran pack size, champion count, hero chance.
Player level 13 (the referent). READ-ONLY.

Model (LEAN - engine consumption of championChance is not in the DBR):
  on a pack spawn:  size ~ U[spawnMin, spawnMax]
                    with prob championChance/100 the pack rolls champions,
                    count ~ U[championMin, championMax]
                    each champion drawn from the weighted roster, gated by minPlayerLevelChampionN
  Veteran (records/game/balancingadjustment_challengemode_enemies01.dbr):
                    spawnMaxAdj +1  ->  spawnMax += 1
                    spawnChampionMaxAdj +2 -> championMax += 2
                    (spawnMinAdj / spawnChampionMinAdj are ABSENT on the Veteran record = 0)
"""
import sys, pathlib, statistics as st
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
VET=a.read_record("records/game/balancingadjustment_challengemode_enemies01.dbr")
SMAXADJ=int(VET.get('spawnMaxAdj') or 0); SMINADJ=int(VET.get('spawnMinAdj') or 0)
CMAXADJ=int(VET.get('spawnChampionMaxAdj') or 0); CMINADJ=int(VET.get('spawnChampionMinAdj') or 0)
print(f"Veteran adjustments read from record: spawnMinAdj={SMINADJ} spawnMaxAdj={SMAXADJ} "
      f"spawnChampionMinAdj={CMINADJ} spawnChampionMaxAdj={CMAXADJ}")
ULT=a.records  # placeholder
PL=13

def analyse(rec):
    smin=int(rec.get('spawnMin') or 0); smax=int(rec.get('spawnMax') or 0)
    cc=float(rec.get('championChance') or 0)
    cmin=int(rec.get('championMin') or 0); cmax=int(rec.get('championMax') or 0)
    if not cc or smax<=0: return None
    roster=[]
    for i in range(1,17):
        n=rec.get(f'nameChampion{i}')
        if not n: continue
        w=int(rec.get(f'weightChampion{i}') or 0)
        mpl=rec.get(f'minPlayerLevelChampion{i}')
        mpl=int(mpl) if mpl else 0
        if mpl>PL: continue                      # not eligible at player level 13
        roster.append((n,w,'/hero/' in n))
    W=sum(w for _,w,_ in roster)
    if W==0: return None
    pher=sum(w for _,w,h in roster if h)/W
    def cell(dsmax,dcmax):
        lo=max(smin+SMINADJ*0,smin); hi=smax+dsmax
        Esize=(lo+hi)/2
        clo=cmin; chi=cmax+dcmax
        Ech=(cc/100.0)*((clo+chi)/2)
        # P(>=1 hero in the pack) = P(champ roll) * E[1-(1-p)^n] over n~U[clo,chi]
        ns=list(range(clo,chi+1)) or [0]
        pnohero=sum((1-pher)**n for n in ns)/len(ns)
        Phero=(cc/100.0)*(1-pnohero)
        return Esize,Ech,Phero
    return dict(smin=smin,smax=smax,cc=cc,cmin=cmin,cmax=cmax,pher=pher,nrost=len(roster),
                normal=cell(0,0), vet=cell(SMAXADJ,CMAXADJ))

print()
print("="*126)
print("A. THE REFERENT'S OWN TRASH - Act-1 slith pools, player level 13")
print("="*126)
print(f"  {'pool':40s} {'cc%':>4s} {'pack N':>10s} {'pack V':>10s} {'E[ch] N':>8s} {'E[ch] V':>8s} "
      f"{'P(hero) N':>10s} {'P(hero) V':>10s} {'heroW%':>7s}")
sl=[]
for r in sorted(a.records):
    if not r.startswith("records/proxies/pools/") or "slith" not in r: continue
    d=analyse(a.read_record(r))
    if not d: continue
    sl.append(d)
    n,v=d['normal'],d['vet']
    print(f"  {r.split('pools/')[-1]:40s} {d['cc']:4.0f} {d['smin']}-{d['smax']:<8d} "
          f"{d['smin']}-{d['smax']+SMAXADJ:<8d} {n[1]:8.3f} {v[1]:8.3f} {100*n[2]:9.2f}% {100*v[2]:9.2f}% {100*d['pher']:6.1f}%")
if sl:
    print(f"  {'MEAN (slith pools)':40s} {'':4s} {'':10s} {'':10s} "
          f"{st.mean(d['normal'][1] for d in sl):8.3f} {st.mean(d['vet'][1] for d in sl):8.3f} "
          f"{100*st.mean(d['normal'][2] for d in sl):9.2f}% {100*st.mean(d['vet'][2] for d in sl):9.2f}%")
    print(f"  {'VETERAN UPLIFT':40s} {'':4s} {'':10s} {'':10s} "
          f"{'':8s} {st.mean(d['vet'][1] for d in sl)/st.mean(d['normal'][1] for d in sl):8.3f}x "
          f"{'':9s} {st.mean(d['vet'][2] for d in sl)/st.mean(d['normal'][2] for d in sl):9.3f}x")

print()
print("="*126)
print("B. ALL ACT-1 (area001-referenced) POOLS, player level 13")
print("="*126)
a1=set()
for r in sorted(a.records):
    if not r.startswith("records/proxies/area001/"): continue
    rec=a.read_record(r)
    if str(rec.get('Class'))!='Proxy': continue
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if p: a1.add(p)
rows=[]
for p in sorted(a1):
    if p not in a.records: continue
    d=analyse(a.read_record(p))
    if d: rows.append(d)
print(f"  pools analysed: {len(rows)}")
for lab,idx in (("E[pack size]",0),("E[champions per pack]",1),("P(>=1 HERO per pack)",2)):
    n=st.mean(d['normal'][idx] for d in rows); v=st.mean(d['vet'][idx] for d in rows)
    print(f"  {lab:26s}  Normal {n:8.4f}   Veteran {v:8.4f}   uplift {v/n if n else 0:6.3f}x   (+{100*(v/n-1) if n else 0:.1f}%)")
print(f"  {'championChance (mean)':26s}  {st.mean(d['cc'] for d in rows):8.2f} %  (unchanged by Veteran - it is not a *Chance* adj)")
print(f"  {'hero weight share (mean)':26s}  {100*st.mean(d['pher'] for d in rows):8.2f} %  of the ELIGIBLE champion roster at PL 13")
# compound: monsters per pack that are champion-or-hero
n_tot=st.mean(d['normal'][0] for d in rows); v_tot=st.mean(d['vet'][0] for d in rows)
n_ch =st.mean(d['normal'][1] for d in rows); v_ch =st.mean(d['vet'][1] for d in rows)
print()
print(f"  COMPOUND per pack:   Normal  {n_tot:.2f} common-slots + {n_ch:.3f} champions  = {n_tot+n_ch:.2f} bodies")
print(f"                       Veteran {v_tot:.2f} common-slots + {v_ch:.3f} champions  = {v_tot+v_ch:.2f} bodies "
      f"({(v_tot+v_ch)/(n_tot+n_ch):.3f}x)")
print(f"  ELITE FRACTION of bodies:  Normal {100*n_ch/(n_tot+n_ch):.2f}%   Veteran {100*v_ch/(v_tot+v_ch):.2f}%")

print()
print("="*126)
print("C. THE MEASURED REFERENT MIX  (referent player.gdc play_stats - M)")
print("="*126)
K,C,H = 882, 7, 3
print(f"  kills {K}   championKills {C}   heroKills {H}")
print(f"  champion fraction {100*C/K:.3f}%   hero fraction {100*H/K:.3f}%   combined elite {100*(C+H)/K:.3f}%")
print(f"  common fraction   {100*(K-C-H)/K:.3f}%")
print(f"  NOTE: GD's championKills counter and the pool's 'champion' roster are not the same population -")
print(f"        the roster's hero entries are counted by heroKills, so championKills excludes them.")
