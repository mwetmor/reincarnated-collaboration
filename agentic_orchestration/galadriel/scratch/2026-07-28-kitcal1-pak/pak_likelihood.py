#!/usr/bin/env python3
"""Profile-likelihood over player per-region protection p, for both pak readings.
Model: monster rolls d ~ U[lo,hi]; taken = d - 0.70*min(d,p); globe shows round(taken).
galadriel 2026-07-28."""
import csv,json,bisect,collections,math,pathlib
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

def pmf(lo,hi,p,jmax=200):
    """P(round(taken)=j) for d~U[lo,hi]; taken(d)=0.3d if d<=p else d-0.7p (monotone)."""
    def inv(t):
        return t/0.30 if t <= 0.30*p else t+0.70*p
    def F(t):
        return min(1.0, max(0.0, (inv(t)-lo)/(hi-lo)))
    out=collections.defaultdict(float)
    for j in range(0, jmax+1):
        q=F(j+0.5)-F(max(j-0.5,0.0))
        if q>0: out[j]=q
    return out

def loglik(obs,lo,hi,p,eps=1e-4):
    P=pmf(lo,hi,p)
    return sum(math.log(max(P.get(v,0.0),eps)) for v in obs)

def profile(obs,lo,hi,label):
    best=None
    for pi in range(0,301):
        p=pi/10.0
        ll=loglik(obs,lo,hi,p)
        if best is None or ll>best[1]: best=(p,ll)
    P=pmf(lo,hi,best[0])
    pred={j:round(P[j],3) for j in sorted(P) if P[j]>0.005}
    print(f"  {label:16} band[{lo:5.2f},{hi:5.2f}]  best p={best[0]:5.1f}  logL={best[1]:9.2f} "
          f" logL@p=0={loglik(obs,lo,hi,0.0):9.2f}")
    print(f"    predicted pmf @bestp: {pred}")
    return best

print("=== R1 / player level 1-2 : atomic candidates (drops with mag>2, mag<8 excluded? no) ===")
r1=[d["mag"] for d in D if d["regime"]=="R1"]
atomic=[v for v in r1 if v>2]           # strip DoT/regen-net (mag<=2)
print("  all R1 drops:",sorted(r1))
print("  atomic candidate set (mag>2), n=",len(atomic),":",sorted(atomic))
print("  observed counts:",dict(sorted(collections.Counter(atomic).items())))
# exclude the composite tail (>= 2x the additive band lower edge x2 = >=8) for the 1x likelihood
one=[v for v in atomic if v<8]
print("  single-hit set (mag 3-7), n=",len(one),":",dict(sorted(collections.Counter(one).items())))
for cl in (1,2):
    print(f"\n charLevel {cl}, tier-01 (Default Phys Dmg for Normal Enemies):")
    for rd,lab in (("add","ADDITIVE"),("mult","MULTIPLICATIVE")):
        lo,hi=PB[str(cl)]["1"][rd]; profile(one,lo,hi,lab)

print("\n=== Bayes-factor style comparison at charLevel 1, tier-01, single-hit set ===")
lo_a,hi_a=PB["1"]["1"]["add"]; lo_m,hi_m=PB["1"]["1"]["mult"]
la=max(loglik(one,lo_a,hi_a,p/10) for p in range(0,301))
lm=max(loglik(one,lo_m,hi_m,p/10) for p in range(0,301))
print(f"  max logL ADDITIVE       = {la:.3f}")
print(f"  max logL MULTIPLICATIVE = {lm:.3f}")
print(f"  delta logL (add - mult) = {la-lm:.3f}   -> likelihood ratio = {math.exp(la-lm):.3g}")
la0=loglik(one,lo_a,hi_a,0.0); lm0=loglik(one,lo_m,hi_m,0.0)
print(f"  at p=0 (physically correct for a level-1-2 character):")
print(f"    logL ADDITIVE={la0:.3f}  logL MULT={lm0:.3f}  delta={la0-lm0:.3f}")

# ---- supplementary levels ----
print("\n=== supplementary: mid-run bands (contaminated; directional only) ===")
for name,a,b,cl,himax in (("L3-4",3,4,3,12),("L7-8",7,8,7,26),("L9",9,9,9,32)):
    v=[d["mag"] for d in D if d["level"] is not None and a<=d["level"]<=b and 2<d["mag"]<himax]
    if len(v)<8: print(f" {name}: n={len(v)} too few"); continue
    print(f" {name} n={len(v)} counts={dict(sorted(collections.Counter(v).items()))}")
    for rd,lab in (("add","ADDITIVE"),("mult","MULTIPLICATIVE")):
        lo,hi=PB[str(cl)]["1"][rd]; profile(v,lo,hi,lab)
