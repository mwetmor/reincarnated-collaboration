#!/usr/bin/env python3
"""D8 — pin the mode-wide multiplier from the EXACT hits; then corpus-wide exact join. READ-ONLY."""
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

ANCH=[("Haraxis  (Quest)",   "records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr", 2050807),
      ("aetherialphantom_h01 (Hero)","records/creatures/enemies/devotion/aetherialphantom_h01.dbr", 453883),
      ("aethcorruption_c01_summon (Champion)","records/creatures/enemies/aetherialcorruption_c01_summon.dbr", 472732),
      ("swampcrab_c01_summon (Champion)","records/creatures/enemies/swampcrab_c01_summon.dbr", 302934)]
print("=== implied mode-wide multiplier at charLevel 108, per anchor ===")
Ms=[]
for lbl,p,hp in ANCH:
    eq,cls=bio_of(p); b=ev(eq,108)
    M=hp/b; Ms.append((lbl,M))
    print(f"  {lbl:40s} eq={eq:28s} base(108)={b:14,.4f}  M={M:.8f}")
print(f"\n  spread across anchors: {min(m for _,m in Ms):.8f} .. {max(m for _,m in Ms):.8f}"
      f"  ({(max(m for _,m in Ms)/min(m for _,m in Ms)-1)*100:.4f} %)")
M = Ms[0][1]

print(f"\n=== corpus-wide EXACT join for the two low fingerprints at M={M:.6f} ===")
bios={}
for p in E2.idx:
    if not p.startswith("records/creatures/enemies/"): continue
    got=bio_of(p)
    if got: bios[p]=got
print(f"  enemy records with a life equation: {len(bios)}")
for fp in (42798,43548,93599,237258):
    print(f"\n  -- fingerprint {fp:,}")
    hits=[]
    for p,(eq,cls) in bios.items():
        for L in range(100,113):
            hp=ev(eq,L)*M
            d=(hp-fp)/fp*100
            if abs(d)<0.30: hits.append((abs(d),d,L,cls,p,hp))
    hits.sort()
    seen=set()
    for _,d,L,cls,p,hp in hits[:14]:
        key=(round(hp,1),L)
        print(f"      {d:+7.4f} %  L{L}  {cls:<9} {hp:12,.1f}  {p}")
