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
def ll(o,lo,hi,p,eps=1e-6):
    P=pmf(lo,hi,p); return sum(math.log(max(P.get(v,0.0),eps)) for v in o)
ps=[0.1*i for i in range(0,401)]
SPECS=[("W1",1,2,1,8),("W2",3,4,3,12),("W3",5,6,5,18),("W4",7,8,7,26),
       ("W5",9,9,9,32),("W6",10,11,10,40),("W7",12,13,12,46)]
print(f"{'win':4} {'pL':>6} {'nAll':>5} {'nAtom':>6} {'DoT<=2':>7} {'cov_min':>8} {'cov_max':>8} "
      f"{'dLogL':>9} {'LR':>12} {'p_add':>6} {'p_mult':>7}")
for name,a,b,cl,cap in SPECS:
    allv=[d for d in D if d["level"] is not None and a<=d["level"]<=b]
    o=[d["mag"] for d in allv if 2<d["mag"]<cap]
    covs=[W[e]["coverage"] for e in sorted(set(d["eng_id"] for d in allv))]
    dot=sum(1 for d in allv if d["mag"]<=2)/max(len(allv),1)
    if len(o)<5:
        print(f"{name:4} {f'{a}-{b}':>6} {len(allv):>5} {len(o):>6} {dot:>6.0%} {min(covs):>8.2f} {max(covs):>8.2f}  (no power)")
        continue
    lo_a,hi_a=PB[str(cl)]["1"]["add"]; lo_m,hi_m=PB[str(cl)]["1"]["mult"]
    pa=max(ps,key=lambda p: ll(o,lo_a,hi_a,p)); pm=max(ps,key=lambda p: ll(o,lo_m,hi_m,p))
    la=ll(o,lo_a,hi_a,pa); lm=ll(o,lo_m,hi_m,pm); d_=la-lm
    lr = f"{math.exp(d_):.3g} : 1" if d_>=0 else f"1 : {math.exp(-d_):.3g}"
    print(f"{name:4} {f'{a}-{b}':>6} {len(allv):>5} {len(o):>6} {dot:>6.0%} {min(covs):>8.2f} {max(covs):>8.2f} "
          f"{d_:>9.2f} {lr:>12} {pa:>6.1f} {pm:>7.1f}")
