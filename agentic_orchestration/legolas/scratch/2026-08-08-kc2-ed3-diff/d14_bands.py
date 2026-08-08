#!/usr/bin/env python3
"""D14 — ITEM 1: re-run join-note 3.3/3.4 ratio bands with BOTH corrections
(a) record charLevel additive term, (b) the level-indexed passive characterLifeModifier.
Edition-II pin. READ-ONLY."""
import sys, csv, collections
sys.path.insert(0,".")
import lib2
E2=lib2.E2
def ev(e,L): return eval(str(e).replace("^","**").replace("charLevel",f"({L})"),{"__builtins__":{}},{})
SURV=E2.merged("records/game/balancingadjustment_survivalmode_enemies03.dbr")[0]["characterLifeModifier"]
DIFF=E2.merged("records/game/balancingadjustment_mp+difficulty_enemies01.dbr")[0]["characterLifeModifier"][8]
def hp(p,L,wave):
    r,_=E2.merged(p)
    if not r: return None
    bp=r.get("characterAttributeEquations")
    if not bp: return None
    b,_=E2.merged(bp if isinstance(bp,str) else bp[0])
    if not b or "characterLife" not in b: return None
    extra=0.0
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
    return ev(b["characterLife"],L)*(1+(DIFF+SURV[wave-1]+extra)/100)

CSV="/Users/admin/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv"
def roster(w):
    mons=set()
    for r in csv.DictReader(open(CSV)):
        if int(r["global_wave"])!=w: continue
        for c in ("roster_records","champ_records"):
            for x in (r.get(c) or "").split("|"):
                if x.strip(): mons.add(x.strip().lower())
    sk2b={}
    for p in E2.idx:
        if not p.startswith("records/skills"): continue
        rr,_=E2.merged(p)
        if rr:
            v=rr.get("spawnObjects") or rr.get("petObjects")
            if v: sk2b[p]=[x.lower() for x in (v if isinstance(v,list) else [v]) if isinstance(x,str) and x.endswith(".dbr")]
    add=set()
    for m in list(mons):
        rr,_=E2.merged(m)
        if rr:
            for k,v in rr.items():
                if isinstance(v,str) and v.lower() in sk2b: add|=set(sk2b[v.lower()])
    return mons | {a for a in add if a in E2.idx}

LEVELS=list(range(102,109))   # the DERIVED admissible band at apl in [103.0,103.92)
for w in (152,157):
    mons=roster(w)
    print(f"\n=== wave {w} — {len(mons)} life-bearing candidates; CORRECTED same-record ratio bands ===")
    for dL in (1,2,3):
        rs=[]
        for p in sorted(mons):
            for L in LEVELS:
                if L+dL>LEVELS[-1]+3: continue
                a,b=hp(p,L,w), hp(p,L+dL,w)
                if a and b: rs.append((b/a-1)*100)
        if rs:
            print(f"   dL={dL}:  {min(rs):.3f} % .. {max(rs):.3f} %   (n={len(rs)})")
    # OLD published bands for reference
print("\n=== 3.4 RE-VERDICT — the six measured inter-class deltas ===")
DELTAS=[(152,"42,798 -> 43,548 (LOW PAIR)",42798,43548),(152,"91,696 -> 93,599",91696,93599),
        (152,"237,258 -> 242,124",237258,242124),(157,"233,250 -> 238,068",233250,238068),
        (157,"398,226 -> 406,243",398226,406243),(157,"411,440 -> 414,837",411440,414837),
        (157,"414,837 -> 419,839",414837,419839)]
band={}
for w in (152,157):
    mons=roster(w)
    for dL in (1,2,3):
        rs=[(hp(p,L,w),hp(p,L+dL,w)) for p in sorted(mons) for L in LEVELS]
        rs=[(b/a-1)*100 for a,b in rs if a and b]
        band[(w,dL)]=(min(rs),max(rs))
for w,lbl,a,b in DELTAS:
    d=(b/a-1)*100
    verdicts=[f"dL={k}" for k in (1,2,3) if band[(w,k)][0]-1e-9<=d<=band[(w,k)][1]+1e-9]
    print(f"   w{w} {lbl:32s} D={d:6.3f} %  ->  {'ONE RECORD, '+' or '.join(verdicts) if verdicts else 'NOT one record at any dL in 1..3'}")
    for k in (1,2,3): print(f"        band dL={k}: {band[(w,k)][0]:6.3f} .. {band[(w,k)][1]:6.3f} %")
