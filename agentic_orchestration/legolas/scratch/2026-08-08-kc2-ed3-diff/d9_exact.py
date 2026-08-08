#!/usr/bin/env python3
"""D9 — (a) is charLevel 108 uniquely determined by the 3-anchor joint solve?
       (b) corpus-wide EXACT (<0.02 %) join for every w152 fingerprint. READ-ONLY."""
import sys, collections
sys.path.insert(0,".")
import lib2
E2=lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})
def bio_of(p):
    r,_=E2.merged(p)
    if not r: return None
    bp=r.get("characterAttributeEquations")
    if not bp: return None
    b,_=E2.merged(bp if isinstance(bp,str) else bp[0])
    if not b or "characterLife" not in b: return None
    return b["characterLife"], r.get("monsterClassification")

A=[("Haraxis p1.5","((charLevel*30)^1.5)+500",2050807),
   ("phantom p1.50","((charLevel*11)^1.50)-20",453883),
   ("aethcorr_c01 p1.33","((charLevel*28)^1.33)+50",472732)]
print("=== (a) joint solve: sweep charLevel, report max/min implied-M disagreement ===")
best=None
for L10 in range(1000,1160):
    L=L10/10
    Ms=[hp/ev(eq,L) for _,eq,hp in A]
    spread=(max(Ms)/min(Ms)-1)*100
    if best is None or spread<best[0]: best=(spread,L,Ms)
    if L==int(L):
        print(f"   L={L:6.1f}  M = {Ms[0]:12.6f} {Ms[1]:12.6f} {Ms[2]:12.6f}   spread {spread:8.4f} %")
print(f"\n   MINIMUM disagreement at charLevel {best[1]}  spread {best[0]:.6f} %   M={sum(best[2])/3:.6f}")

M = 2050807/ev("((charLevel*30)^1.5)+500",108)
CENSUS=[302934,42798,43548,443554,242124,237258,91696,93599,453883,369770,2050807,472732]
bios={p:bio_of(p) for p in E2.idx if p.startswith("records/creatures/enemies/")}
bios={k:v for k,v in bios.items() if v}
print(f"\n=== (b) corpus-wide EXACT join, |d| < 0.02 %, M={M:.6f}, L in 100..112 ({len(bios)} records) ===")
for fp in CENSUS:
    hits=collections.defaultdict(list)
    for p,(eq,cls) in bios.items():
        for L in range(100,113):
            hp=ev(eq,L)*M
            if abs(hp-fp)/fp*100 < 0.02: hits[(L,round(hp,1),cls)].append(p)
    if hits:
        print(f"  {fp:>9,}  EXACT:")
        for (L,hp,cls),ps in sorted(hits.items()):
            print(f"        L{L} {cls:<9} {hp:12,.1f}  n={len(ps):3d}  e.g. {ps[0]}")
    else:
        print(f"  {fp:>9,}  -- NO exact record at any integer level --")
