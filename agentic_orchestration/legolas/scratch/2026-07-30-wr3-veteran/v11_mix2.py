#!/usr/bin/env python3
"""V11 - encounter mix, CORRECTED: resolve each champion-slot entry's own monsterClassification.
The champion SLOT frequently spawns a Common-classified creature at a higher level-variance, so
'champion slot' != 'Champion monster'. READ-ONLY."""
import sys, pathlib, statistics as st
from collections import Counter
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive
ROOT=pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
a=ArzArchive(ROOT/"database/database.arz")
VET=a.read_record("records/game/balancingadjustment_challengemode_enemies01.dbr")
SMAXADJ=int(VET.get('spawnMaxAdj') or 0); CMAXADJ=int(VET.get('spawnChampionMaxAdj') or 0)
PL=13
_cls={}
def cls(rec_name):
    if rec_name in _cls: return _cls[rec_name]
    v='?'
    if rec_name in a.records:
        v=str(a.read_record(rec_name).get('monsterClassification') or 'Common')
    _cls[rec_name]=v; return v

def analyse(rec):
    smin=int(rec.get('spawnMin') or 0); smax=int(rec.get('spawnMax') or 0)
    cc=float(rec.get('championChance') or 0)
    cmin=int(rec.get('championMin') or 0); cmax=int(rec.get('championMax') or 0)
    if not cc or smax<=0: return None
    W=0.0; wch=0.0; whe=0.0
    for i in range(1,17):
        n=rec.get(f'nameChampion{i}')
        if not n: continue
        w=float(rec.get(f'weightChampion{i}') or 0)
        mpl=rec.get(f'minPlayerLevelChampion{i}'); mpl=int(mpl) if mpl else 0
        if mpl>PL: continue
        W+=w
        c=cls(n)
        if c=='Hero': whe+=w
        elif c=='Champion': wch+=w
    if W<=0: return None
    p_he=whe/W; p_ch=wch/W
    def cell(dsmax,dcmax):
        Esize=(smin+smax+dsmax)/2
        ns=list(range(cmin,cmax+dcmax+1)) or [0]
        En=sum(ns)/len(ns)
        Eslots=(cc/100.0)*En
        return Esize, Eslots, Eslots*p_ch, Eslots*p_he, \
               (cc/100.0)*(1-sum((1-p_he)**n for n in ns)/len(ns))
    return dict(cc=cc,smin=smin,smax=smax,cmin=cmin,cmax=cmax,p_ch=p_ch,p_he=p_he,
                normal=cell(0,0), vet=cell(SMAXADJ,CMAXADJ))

# ---- classification census of champion-slot entries across Act 1 ----
a1=set()
for r in sorted(a.records):
    if not r.startswith("records/proxies/area001/"): continue
    rec=a.read_record(r)
    if str(rec.get('Class'))!='Proxy': continue
    for i in range(1,9):
        p=rec.get(f'pool{i}')
        if p: a1.add(p)
cnt=Counter(); wcnt=Counter()
rows=[]
for p in sorted(a1):
    if p not in a.records: continue
    rec=a.read_record(p)
    for i in range(1,17):
        n=rec.get(f'nameChampion{i}')
        if not n: continue
        mpl=rec.get(f'minPlayerLevelChampion{i}'); mpl=int(mpl) if mpl else 0
        if mpl>PL: continue
        cnt[cls(n)]+=1; wcnt[cls(n)]+=float(rec.get(f'weightChampion{i}') or 0)
    d=analyse(rec)
    if d: rows.append(d)
print("="*118)
print("A. WHAT ACTUALLY SITS IN A 'CHAMPION SLOT'  (Act-1 pools, entries eligible at player level 13)")
print("="*118)
tw=sum(wcnt.values()); tc=sum(cnt.values())
for k in sorted(cnt, key=lambda x:-wcnt[x]):
    print(f"   monsterClassification {k:10s}  entries {cnt[k]:4d} ({100*cnt[k]/tc:5.1f}%)   "
          f"weight {wcnt[k]:9.0f} ({100*wcnt[k]/tw:5.1f}% of draw probability)")
print("   >>> the champion SLOT is not a champion GUARANTEE: a large share of its weight is on")
print("       Common-classified creatures spawned at a higher level-variance equation.")
print()

print("="*118)
print(f"B. NORMAL vs VETERAN, Act-1 pools, player level 13   (n={len(rows)} pools)")
print("="*118)
LB=[("E[pack size] (common slots)",0),("E[champion SLOTS per pack]",1),
    ("E[Champion-classified per pack]",2),("E[Hero-classified per pack]",3),
    ("P(>=1 HERO in the pack)",4)]
for lab,idx in LB:
    n=st.mean(d['normal'][idx] for d in rows); v=st.mean(d['vet'][idx] for d in rows)
    print(f"   {lab:34s} Normal {n:8.4f}   Veteran {v:8.4f}   uplift {v/n if n else 0:6.3f}x  (+{100*(v/n-1) if n else 0:5.1f}%)")
n_sz=st.mean(d['normal'][0] for d in rows); v_sz=st.mean(d['vet'][0] for d in rows)
n_sl=st.mean(d['normal'][1] for d in rows); v_sl=st.mean(d['vet'][1] for d in rows)
n_ch=st.mean(d['normal'][2] for d in rows); v_ch=st.mean(d['vet'][2] for d in rows)
n_he=st.mean(d['normal'][3] for d in rows); v_he=st.mean(d['vet'][3] for d in rows)
nb=n_sz+n_sl; vb=v_sz+v_sl
print()
print(f"   BODIES PER PACK        Normal {nb:6.3f}      Veteran {vb:6.3f}      {vb/nb:6.3f}x  (+{100*(vb/nb-1):.1f}%)")
print(f"   elite share of bodies  Normal {100*(n_ch+n_he)/nb:5.2f}%     Veteran {100*(v_ch+v_he)/vb:5.2f}%")
print(f"   champion share         Normal {100*n_ch/nb:5.2f}%     Veteran {100*v_ch/vb:5.2f}%")
print(f"   hero share             Normal {100*n_he/nb:5.2f}%     Veteran {100*v_he/vb:5.2f}%")
print()
print("="*118)
print("C. AGAINST THE MEASURED REFERENT MIX (player.gdc play_stats, M)")
print("="*118)
K,C,H=882,7,3
print(f"   measured: kills {K}  championKills {C} ({100*C/K:.3f}%)  heroKills {H} ({100*H/K:.3f}%)  "
      f"elite {100*(C+H)/K:.3f}%")
print(f"   modelled (Veteran, PL13, pack spawns only): champion {100*v_ch/vb:.3f}%  hero {100*v_he/vb:.3f}%  "
      f"elite {100*(v_ch+v_he)/vb:.3f}%")
print(f"   modelled (Normal , PL13, pack spawns only): champion {100*n_ch/nb:.3f}%  hero {100*n_he/nb:.3f}%  "
      f"elite {100*(n_ch+n_he)/nb:.3f}%")
print()
print("   Reconciliation: the model is a PL-13 upper bound (every minPlayerLevel gate open) over pack")
print("   spawns only, while the measured 882 kills accumulated from level 1 with most gates shut and")
print("   include set-piece / ambush / quest spawns. Use the UPLIFT RATIOS, not the absolute rates.")
