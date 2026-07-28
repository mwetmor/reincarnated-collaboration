#!/usr/bin/env python3
"""Armor-marginalised comb-lift test: which pak reading explains the measured
HP-drop comb, and at what implied player protection. galadriel 2026-07-28."""
import csv, json, bisect, collections, statistics as st, pathlib
ROOT=pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel")
ta=[]
for r in csv.DictReader(open(ROOT/"captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv")):
    try: pts=float(r["pts_s"])
    except: continue
    ml=r["max_level"].strip(); ta.append((pts,int(ml) if ml.isdigit() else None))
ta.sort(); PTS=[x[0] for x in ta]
L=[];l=None
for x in ta:
    if x[1] is not None: l=x[1]
    L.append(l)
def lvl(t): return L[max(bisect.bisect_right(PTS,t)-1,0)]
W={w["eng_id"]:w for w in json.load(open(ROOT/"captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json"))["windows"]}
D=[json.loads(x) for x in open(ROOT/"captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl")]
for d in D: d["regime"]=W[d["eng_id"]]["regime"]; d["level"]=lvl(d["t"])
PB=json.load(open("predicted-bands.json"))["bands"]

def mit(x,p): return x-0.70*min(x,p)
def comb(lo,hi,p,kmax=4,cap=200):
    """integer set explained by k independent mitigated hits, k=1..kmax"""
    tl,th=mit(lo,p),mit(hi,p)
    S=set()
    for k in range(1,kmax+1):
        a,b=k*tl,k*th
        for v in range(max(1,int(a-0.5+1e-9)), min(cap,int(b+0.5))+1):
            if a-0.5<=v<=b+0.5: S.add(v)
    return S,(tl,th)

def score(vals,lo,hi,p,kmax=4):
    cap=max(vals)
    S,band=comb(lo,hi,p,kmax,cap)
    dom=[v for v in range(3,cap+1)]
    if not dom: return 0,0,0,band
    null=len([v for v in dom if v in S])/len(dom)
    exp=sum(1 for v in vals if v in S)/len(vals)
    lift=exp/null if null>0 else 0
    return exp,null,lift,band

# atomic candidate set: strip DoT (mag<=2) and the G-2c big-hit / burst tail (>=10% EHP proxy: mag>=60)
def pool(lvmin,lvmax):
    return [d["mag"] for d in D if d["level"] is not None and lvmin<=d["level"]<=lvmax
            and d["mag"]>2 and d["mag"]<60]

BANDS=[("L1-2",1,2,1),("L3-4",3,4,3),("L5-6",5,6,5),("L7-8",7,8,7),("L9",9,9,9),
       ("L10-11",10,11,10),("L12+",12,13,12)]
print(f"{'band':7} {'n':>4} | {'reading':6} {'bestP':>6} {'exp':>6} {'null':>6} {'lift':>6} {'1x-band(mit)':>16} | {'lift@p=0':>9}")
res={}
for name,a,b,cl in BANDS:
    v=pool(a,b)
    if len(v)<5: print(f"{name:7} {len(v):>4} | (too few)"); continue
    row={}
    for rd in ("add","mult"):
        lo,hi=PB[str(cl)]["1"][rd]
        best=None
        for pi in range(0,401):
            p=pi/10
            e,n,li,bd=score(v,lo,hi,p)
            if best is None or li>best[2] or (li==best[2] and e>best[0]): best=(e,n,li,bd,p)
        e0,n0,l0,_=score(v,lo,hi,0.0)
        print(f"{name if rd=='add' else '':7} {len(v) if rd=='add' else '':>4} | {rd:6} {best[4]:>6.1f} "
              f"{best[0]:>6.2f} {best[1]:>6.2f} {best[2]:>6.2f} {f'{best[3][0]:.1f}-{best[3][1]:.1f}':>16} | {l0:>9.2f}")
        row[rd]=dict(bestP=best[4],exp=best[0],null=best[1],lift=best[2],
                     band_mit=[round(x,2) for x in best[3]],lift_p0=round(l0,3),exp_p0=round(e0,3),
                     band_raw=[round(lo,2),round(hi,2)])
    res[name]=dict(n=len(v),**row)
    print()
json.dump(res,open("comb-lift.json","w"),indent=1)

# ---- histogram overlay for the decisive window ----
print("=== R1 / player L1-2 : observed comb vs both predicted 1x bands (p=0) ===")
v=sorted(d["mag"] for d in D if d["regime"]=="R1")
c=collections.Counter(v)
lo_a,hi_a=PB["1"]["1"]["add"]; lo_m,hi_m=PB["1"]["1"]["mult"]
for k in range(1,16):
    mark=""
    if lo_a-0.5<=k<=hi_a+0.5: mark+=" <ADD 1x"
    if lo_m-0.5<=k<=hi_m+0.5: mark+=" <MULT 1x"
    if 2*lo_a-0.5<=k<=2*hi_a+0.5: mark+=" <ADD 2x"
    print(f" {k:>3} | {'#'*c.get(k,0):<14} {c.get(k,0):>2}{mark}")
