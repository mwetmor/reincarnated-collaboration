#!/usr/bin/env python3
"""Per-window verdict table under a contamination-mixture likelihood.
P(v) = (1-eps)*P_model(v) + eps/|support|   -- eps absorbs unmodelled sources
(DoT stragglers, composites below the k=2 band, off-roster protos). galadriel 2026-07-28."""
import csv,json,bisect,collections,math,pathlib
ROOT=pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel")
ta=[]
for r in csv.DictReader(open(ROOT/"captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv")):
    try: pts=float(r["pts_s"])
    except: continue
    ml=r["max_level"].strip(); ta.append((pts,int(ml) if ml.isdigit() else None))
ta.sort(); PTS=[x[0] for x in ta]; L=[];l=None
for x in ta:
    if x[1] is not None: l=x[1]
    L.append(l)
def lvl(t): return L[max(bisect.bisect_right(PTS,t)-1,0)]
W={w["eng_id"]:w for w in json.load(open(ROOT/"captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json"))["windows"]}
D=[json.loads(x) for x in open(ROOT/"captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl")]
for d in D: d["regime"]=W[d["eng_id"]]["regime"]; d["level"]=lvl(d["t"])
PB=json.load(open("predicted-bands.json"))["bands"]
def pmf(lo,hi,p,jmax=400):
    inv=lambda t: t/0.30 if t<=0.30*p else t+0.70*p
    F=lambda t: min(1.0,max(0.0,(inv(t)-lo)/(hi-lo)))
    return {j:F(j+0.5)-F(max(j-0.5,0.0)) for j in range(0,jmax+1)}
def ll(o,lo,hi,p,cap,eps):
    P=pmf(lo,hi,p); bg=eps/(cap-3+1)
    return sum(math.log((1-eps)*P.get(v,0.0)+bg) for v in o)
ps=[0.1*i for i in range(0,401)]
SPECS=[("W1",1,2,1,8),("W2",3,4,3,12),("W3",5,6,5,18),("W4",7,8,7,26),
       ("W5",9,9,9,32),("W6",10,11,10,40),("W7",12,13,12,46)]
for eps in (0.02,0.05,0.10):
  print(f"\n===== contamination eps = {eps:.2f} =====")
  print(f"{'win':4} {'pL':>6} {'nAll':>5} {'nAtom':>6} {'DoT<=2':>7} {'cov':>11} {'dLogL':>8} {'LR (add:mult)':>16} {'p_add':>6} {'p_mult':>7}")
  for name,a,b,cl,cap in SPECS:
    allv=[d for d in D if d["level"] is not None and a<=d["level"]<=b]
    o=[d["mag"] for d in allv if 2<d["mag"]<cap]
    covs=[W[e]["coverage"] for e in sorted(set(d["eng_id"] for d in allv))]
    dot=sum(1 for d in allv if d["mag"]<=2)/max(len(allv),1)
    cv=f"{min(covs):.2f}-{max(covs):.2f}"
    if len(o)<5:
        print(f"{name:4} {f'{a}-{b}':>6} {len(allv):>5} {len(o):>6} {dot:>6.0%} {cv:>11}   (no power)"); continue
    lo_a,hi_a=PB[str(cl)]["1"]["add"]; lo_m,hi_m=PB[str(cl)]["1"]["mult"]
    pa=max(ps,key=lambda p: ll(o,lo_a,hi_a,p,cap,eps)); pm=max(ps,key=lambda p: ll(o,lo_m,hi_m,p,cap,eps))
    la=ll(o,lo_a,hi_a,pa,cap,eps); lm=ll(o,lo_m,hi_m,pm,cap,eps); d_=la-lm
    lr=f"{math.exp(d_):.3g} : 1" if d_>=0 else f"1 : {math.exp(-d_):.3g}"
    print(f"{name:4} {f'{a}-{b}':>6} {len(allv):>5} {len(o):>6} {dot:>6.0%} {cv:>11} {d_:>8.2f} {lr:>16} {pa:>6.1f} {pm:>7.1f}")

# W1 headline under the mixture, plus p=0 case
print("\n===== W1 headline (charLevel 1, tier-01), mixture eps sensitivity =====")
o=[d["mag"] for d in D if d["regime"]=="R1" and 2<d["mag"]<8]
lo_a,hi_a=PB["1"]["1"]["add"]; lo_m,hi_m=PB["1"]["1"]["mult"]
for eps in (0.0001,0.02,0.05,0.10,0.20):
    pa=max(ps,key=lambda p: ll(o,lo_a,hi_a,p,8,eps)); pm=max(ps,key=lambda p: ll(o,lo_m,hi_m,p,8,eps))
    la=ll(o,lo_a,hi_a,pa,8,eps); lm=ll(o,lo_m,hi_m,pm,8,eps)
    l0a=ll(o,lo_a,hi_a,0.0,8,eps); l0m=ll(o,lo_m,hi_m,0.0,8,eps)
    print(f" eps={eps:<7} profiled: dLogL={la-lm:6.2f} LR={math.exp(la-lm):9.1f}:1 (p_add={pa:.1f} p_mult={pm:.1f})"
          f" | at p=0: dLogL={l0a-l0m:7.2f} LR={math.exp(min(l0a-l0m,700)):.3g}:1")
