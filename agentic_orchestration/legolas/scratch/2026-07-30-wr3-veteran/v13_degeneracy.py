#!/usr/bin/env python3
"""V13 - the degeneracy test: is 'cl13/rank4 + Veteran' the same fixture as 'cl18/rank5, no Veteran'?
Run per channel, under both composition readings. Plus the delta vs the S1_PAK regime of record.
READ-ONLY."""
import sys, pathlib
sys.path.insert(0,"/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
exec(open(pathlib.Path(__file__).parent/"v12_grid2.py").read().split("CELLS=[")[0])

def kit2(cl,rk,vet,mitigate,ice_on):
    F,PM=factors(cl,vet); ice=g(ARMR,'offensiveColdModifier',rk) if ice_on else 0.0
    mp=MIT["Physical"] if mitigate else 1.0; mc=MIT["Cold"] if mitigate else 1.0
    blk=lambda p,c: p*mp*PM*F + c*mc*(1+ice/100)*F
    return {
      "nova FAR (140%)": blk(g(RING,'offensivePhysicalMin',rk),g(RING,'offensiveColdMin',rk))*1.4,
      "nova mid (100%)": blk(g(RING,'offensivePhysicalMin',rk),g(RING,'offensiveColdMin',rk)),
      "wave impact":     blk(g(WAVE,'offensivePhysicalMin',rk),g(WAVE,'offensiveColdMin',rk)),
      "blizzard/drop":   blk(g(BLIZ,'offensivePhysicalMin',rk),g(BLIZ,'offensiveColdMin',rk)),
      "melee MIN":       blk(g(MELE,'offensivePhysicalMin',cl),g(PASS,'offensiveColdMin',rk)),
      "melee MAX":       blk(g(MELE,'offensivePhysicalMax',cl),g(PASS,'offensiveColdMax',rk)),
      "nova cold DoT":   g(RING,'offensiveSlowColdMin',rk)*mc*(1+ice/100)*F*(1+PAKSC/100),
      "wave cold DoT":   g(WAVE,'offensiveSlowColdMin',rk)*mc*(1+ice/100)*F*(1+PAKSC/100),
    }

REF = kit2(18,5,'none',True,True)          # the charter's S2_FULL column, no Veteran, cl18/r5
print("="*104)
print("DEGENERACY TEST - every channel, ratio to the charter's S2_FULL cl18/r5 no-Veteran column")
print("="*104)
CAND=[("cl13/r4 VET-own",13,4,'own'),("cl16/r5 VET-own",16,5,'own'),("cl18/r5 VET-own",18,5,'own'),
      ("cl13/r4 VET-pool",13,4,'pooled'),("cl16/r5 VET-pool",16,5,'pooled'),("cl18/r5 VET-pool",18,5,'pooled')]
tabs={n:kit2(cl,rk,v,True,True) for n,cl,rk,v in CAND}
keys=list(REF)
print(f"  {'channel':18s}{'S2 cl18 no-vet':>15s}"+"".join(f"{n:>19s}" for n,_,_,_ in CAND))
for k in keys:
    print(f"  {k:18s}{REF[k]:15.2f}"+"".join(f"{tabs[n][k]:11.2f} ({tabs[n][k]/REF[k]:5.3f})" for n,_,_,_ in CAND))
import statistics as st
print()
for n,_,_,_ in CAND:
    rs=[tabs[n][k]/REF[k] for k in keys]
    print(f"  {n:18s} mean ratio {st.mean(rs):6.3f}   spread {min(rs):.3f}-{max(rs):.3f}   "
          f"max |dev| from mean {100*max(abs(r/st.mean(rs)-1) for r in rs):5.1f}%")
print()
print("="*104)
print("DELTA vs the REGIME OF RECORD (S1_PAK, cl18/r5, no Veteran) - what a Fork-1 re-ruling costs")
print("="*104)
S1={}
F1=(1+PAKT/100)                      # pak only, no pool, no Veteran
ice=g(ARMR,'offensiveColdModifier',5)
blk1=lambda p,c: p*MIT["Physical"]*F1 + c*MIT["Cold"]*(1+ice/100)*F1
S1["nova FAR (140%)"]=blk1(g(RING,'offensivePhysicalMin',5),g(RING,'offensiveColdMin',5))*1.4
S1["nova mid (100%)"]=blk1(g(RING,'offensivePhysicalMin',5),g(RING,'offensiveColdMin',5))
S1["wave impact"]=blk1(g(WAVE,'offensivePhysicalMin',5),g(WAVE,'offensiveColdMin',5))
S1["blizzard/drop"]=blk1(g(BLIZ,'offensivePhysicalMin',5),g(BLIZ,'offensiveColdMin',5))
print(f"  {'channel':18s}{'S1_PAK (now)':>14s}"+"".join(f"{n:>19s}" for n,_,_,_ in CAND))
for k in ["nova FAR (140%)","nova mid (100%)","wave impact","blizzard/drop"]:
    print(f"  {k:18s}{S1[k]:14.2f}"+"".join(f"{tabs[n][k]:11.2f} ({tabs[n][k]/S1[k]:5.3f})" for n,_,_,_ in CAND))
print()
print("  NOTE A-NOVA-2's ratified S1 far-band pin is 269.66; the nova pin without icearmor's cold")
print("  rider. The row above carries the rider ON for comparability with A-WAVE-1/A-BLIZ-1.")
