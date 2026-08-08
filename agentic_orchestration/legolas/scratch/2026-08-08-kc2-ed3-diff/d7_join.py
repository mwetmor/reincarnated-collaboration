#!/usr/bin/env python3
"""D7 — w152 census fingerprint -> (record, level) join at a mode-wide multiplier.
Edition-II pin. READ-ONLY."""
import sys, csv, collections
sys.path.insert(0,".")
import lib2
E2 = lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})
def life_eq(p):
    r,_=E2.merged(p)
    if not r: return None
    bp=r.get("characterAttributeEquations")
    if not bp: return None
    b,_=E2.merged(bp if isinstance(bp,str) else bp[0])
    if not b or "characterLife" not in b: return None
    return b["characterLife"], r.get("charLevel","charLevel*1"), r.get("monsterClassification")

CSV="/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv"
rows=[r for r in csv.DictReader(open(CSV)) if int(r["global_wave"])==152]
mons=set()
for r in rows:
    for c in ("roster_records","champ_records"):
        for x in (r.get(c) or "").split("|"):
            if x.strip(): mons.add(x.strip().lower())
# every summon body reachable from a rostered body's skills (one hop)
sk2body={}
for p in E2.idx:
    if not p.startswith("records/skills"): continue
    r,_=E2.merged(p)
    if not r: continue
    v=r.get("spawnObjects") or r.get("petObjects")
    if v:
        vs=v if isinstance(v,list) else [v]
        sk2body[p]=[x.lower() for x in vs if isinstance(x,str) and x.endswith(".dbr")]
add=set()
for m in list(mons):
    r,_=E2.merged(m)
    if not r: continue
    for k,v in r.items():
        if isinstance(v,str) and v.lower() in sk2body:
            add |= set(sk2body[v.lower()])
mons |= {a for a in add if a in E2.idx}
print(f"w152 rostered + one-hop summon bodies: {len(mons)}")

CENSUS=[302934,42798,43548,443554,242124,237258,91696,93599,453883,369770,2050807,472732]
MULT=[("Haraxis-anchored 11.0900", 2050807/ (ev('((charLevel*30)^1.5)+500',108)))]
LEVELS=list(range(102,111))
for label,M in MULT:
    print(f"\n=== mode-wide M = {M:.4f} ({label}); level sweep {LEVELS[0]}..{LEVELS[-1]}, offsets NOT applied ===")
    for fp in CENSUS:
        best=[]
        for p in sorted(mons):
            got=life_eq(p)
            if not got: continue
            eq,cl,cls=got
            for L in LEVELS:
                hp=ev(eq,L)*M
                d=(hp-fp)/fp*100
                if abs(d)<1.2: best.append((abs(d),d,p,cls,L,hp))
        best.sort()
        if best:
            print(f"  {fp:>9,} :")
            for _,d,p,cls,L,hp in best[:4]:
                print(f"        {d:+7.3f} %  L{L}  {cls:<9} {hp:11,.0f}  {p}")
        else:
            print(f"  {fp:>9,} :  no record within 1.2 %")
