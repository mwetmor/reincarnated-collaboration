#!/usr/bin/env python3
"""D12 — full w152 census join under the SOLVED life model + the hero-offset falsification.
Edition-II pin. READ-ONLY."""
import sys, csv, collections, json
sys.path.insert(0,".")
import lib2
E2=lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})
SURV=E2.merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")[0]["characterLifeModifier"]
DIFF=E2.merged("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")[0]["characterLifeModifier"][8]
_c={}
def model(p,L,wave=152):
    if (p,L) in _c: return _c[(p,L)]
    r,_=E2.merged(p); out=None
    if r:
        bp=r.get("characterAttributeEquations")
        if bp:
            b,_=E2.merged(bp if isinstance(bp,str) else bp[0])
            if b and "characterLife" in b:
                base=ev(b["characterLife"],L); extra=0.0
                for i in range(1,30):
                    sn=r.get(f"skillName{i}"); sl=r.get(f"skillLevel{i}")
                    if not sn: continue
                    s,_=E2.merged(sn)
                    if not s: continue
                    lm=s.get("characterLifeModifier")
                    if lm is None: continue
                    if isinstance(lm,list):
                        idx=int(ev(sl,L))-1 if sl is not None else 0
                        if 0<=idx<len(lm): extra+=lm[idx]
                    else: extra+=lm
                sig=DIFF+SURV[wave-1]+extra
                out=(base*(1+sig/100), sig, r.get("monsterClassification"), b["characterLife"], r.get("charLevel"))
    _c[(p,L)]=out; return out

print("=== A. HERO-OFFSET FALSIFICATION — the six w152 hero names, HP at L107 / L108 ===")
HEROES=[("Mudflinger ~ Reflective","records/creatures/enemies/hero/swampcrab_h03.dbr"),
        ("Chaosshell ~ Voidtouched","records/creatures/enemies/hero/swampcrab_h04.dbr"),
        ("Rotmouth","records/creatures/enemies/hero/basilisk_h02.dbr"),
        ("Aregos ~ Corrupted","records/creatures/enemies/hero/basilisk_h03.dbr"),
        ("Chillslither ~ Arctic","records/creatures/enemies/hero/basiliskfrost_h01.dbr"),
        ("Vanallius the Voracious","records/creatures/enemies/hero/aetherialcorruption_h02.dbr")]
for nm,p in HEROES:
    r,_=E2.merged(p)
    if not r:
        cand=[q for q in E2.idx if q.startswith("records/creatures/enemies/hero/") and "basilisk" in q and ("frost" in q or "gdx3" in q)]
        print(f"   {nm:26s} [record path not found: {p}]  candidates: {cand[:6]}"); continue
    a=model(p,107); b=model(p,108)
    print(f"   {nm:26s} charLevel={r.get('charLevel'):14s} L107={a[0]:11,.0f}  L108={b[0]:11,.0f}")

print("\n=== B. full w152 census join, SOLVED model, integer levels 100..112 ===")
CSV="/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv"
rows=[r for r in csv.DictReader(open(CSV)) if int(r["global_wave"])==152]
mons=set()
for r in rows:
    for c in ("roster_records","champ_records"):
        for x in (r.get(c) or "").split("|"):
            if x.strip(): mons.add(x.strip().lower())
sk2b={}
for p in E2.idx:
    if not p.startswith("records/skills"): continue
    r,_=E2.merged(p)
    if r:
        v=r.get("spawnObjects") or r.get("petObjects")
        if v: sk2b[p]=[x.lower() for x in (v if isinstance(v,list) else [v]) if isinstance(x,str) and x.endswith(".dbr")]
add=set()
for m in list(mons):
    r,_=E2.merged(m)
    if r:
        for k,v in r.items():
            if isinstance(v,str) and v.lower() in sk2b: add|=set(sk2b[v.lower()])
mons|={a for a in add if a in E2.idx}
CENSUS=[(302934,1),(42798,4),(43548,3),(443554,4),(242124,2),(237258,1),(91696,1),(93599,2),
        (453883,2),(369770,1),(2050807,1),(472732,2)]
res={}
for fp,mult in CENSUS:
    hits=collections.defaultdict(list)
    for p in mons:
        for L in range(100,113):
            m=model(p,L)
            if not m: continue
            if abs(m[0]-fp)/fp*100 < 0.05: hits[(L,m[2])].append(p)
    print(f"\n  {fp:>9,} x{mult}")
    if hits:
        for (L,cls),ps in sorted(hits.items()):
            print(f"       L{L} {str(cls):<9} n={len(ps):3d}   {', '.join(sorted(ps)[:3])}{' ...' if len(ps)>3 else ''}")
        res[fp]=sorted({L for L,_ in hits})
    else:
        print("       -- no w152-reachable record within 0.05 % --")
        res[fp]=[]
json.dump(res, open("w152_fingerprint_levels.json","w"), indent=1)
print("\n  resolved:", sum(1 for v in res.values() if v), "/", len(CENSUS))
