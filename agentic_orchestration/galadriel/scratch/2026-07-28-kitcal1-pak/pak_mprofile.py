#!/usr/bin/env python3
"""Reading-agnostic estimate of the EFFECTIVE total-damage multiplier m at charLevel 1,
profiled over unknown player per-hit protection p. galadriel 2026-07-28."""
import csv,json,bisect,collections,math,pathlib
ROOT=pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel")
W={w["eng_id"]:w for w in json.load(open(ROOT/"captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json"))["windows"]}
D=[json.loads(x) for x in open(ROOT/"captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl")]
for d in D: d["regime"]=W[d["eng_id"]]["regime"]
obs=[d["mag"] for d in D if d["regime"]=="R1" and 2<d["mag"]<8]
print("R1 single-hit set:",dict(sorted(collections.Counter(obs).items())),"n=",len(obs))

PMIN,PMAX,DEXM = 18.0, 25.0, 1.0640   # zombie_a01 damagebase_physical01 rank 1 x dexMult(charLevel 1)
def pmf(m,p):
    lo,hi=PMIN*m*DEXM, PMAX*m*DEXM
    inv=lambda t: t/0.30 if t<=0.30*p else t+0.70*p
    F=lambda t: min(1.0,max(0.0,(inv(t)-lo)/(hi-lo)))
    return {j:F(j+0.5)-F(max(j-0.5,0.0)) for j in range(0,40)}
EPS=0.05          # contamination mixture: unmodelled sources, uniform over the 3..7 support
def ll(m,p,eps=EPS):
    P=pmf(m,p); bg=eps/5.0
    return sum(math.log((1-eps)*P.get(v,0.0)+bg) for v in obs)

ms=[0.10+0.0005*i for i in range(1001)]          # 0.100 .. 0.600
ps=[0.1*i for i in range(0,301)]                 # 0 .. 30
prof=[(m,max(ll(m,p) for p in ps)) for m in ms]
best=max(prof,key=lambda x:x[1])
thr=best[1]-1.92                                  # 95% profile-likelihood (chi2_1/2)
inside=[m for m,v in prof if v>=thr]
print(f"\nMLE effective multiplier m_hat = {best[0]:.4f}  (logL={best[1]:.3f})")
print(f"95% profile-likelihood interval for m: [{min(inside):.4f}, {max(inside):.4f}]")
for name,mv in (("ADDITIVE  (1 + (-55-25)/100)",0.2000),("MULTIPLICATIVE ((1-0.55)*(1-0.25))",0.3375)):
    v=max(ll(mv,p) for p in ps)
    print(f"  {name:36} m={mv:.4f}  profile logL={v:9.3f}  dLogL vs MLE={v-best[1]:8.3f}"
          f"  {'INSIDE 95%' if v>=thr else 'EXCLUDED'}")
lr=math.exp(max(ll(0.2000,p) for p in ps)-max(ll(0.3375,p) for p in ps))
print(f"\n  likelihood ratio ADD:MULT (p profiled out) = {lr:.1f} : 1")

# hard feasibility: band must sit inside [3.5,5.5] to yield exactly {4,5}
print("\nHard-feasibility (band entirely within [3.5,5.5], i.e. zero 3s and zero 6s possible):")
feas=[(m,p) for m in ms for p in ps
      if (PMIN*m*DEXM-0.70*min(PMIN*m*DEXM,p))>=3.5 and (PMAX*m*DEXM-0.70*min(PMAX*m*DEXM,p))<=5.5]
if feas:
    print(f"  feasible m range: [{min(f[0] for f in feas):.4f}, {max(f[0] for f in feas):.4f}]")
    print(f"  feasible p range: [{min(f[1] for f in feas):.2f}, {max(f[1] for f in feas):.2f}]")
    print(f"  ADDITIVE m=0.2000 feasible? {any(abs(f[0]-0.2000)<3e-4 for f in feas)}")
    print(f"  MULTIPLICATIVE m=0.3375 feasible? {any(abs(f[0]-0.3375)<3e-4 for f in feas)}")
# best achievable under MULT
bp=max(ps,key=lambda p: ll(0.3375,p))
print(f"\nMULTIPLICATIVE best case: p={bp:.1f}, pmf="
      +str({j:round(v,3) for j,v in pmf(0.3375,bp).items() if v>0.004}))
print(f"  -> predicts {1-sum(v for j,v in pmf(0.3375,bp).items() if j in (4,5)):.1%} of hits outside {{4,5}}; "
      f"observed 0/{len(obs)}.  P(0 outside | n={len(obs)}) = "
      f"{(sum(v for j,v in pmf(0.3375,bp).items() if j in (4,5)))**len(obs):.2e}")
ba=max(ps,key=lambda p: ll(0.2000,p))
print(f"ADDITIVE best case: p={ba:.1f}, pmf="+str({j:round(v,3) for j,v in pmf(0.2000,ba).items() if v>0.004}))
json.dump(dict(m_hat=best[0],ci=[min(inside),max(inside)],
               ll_add=max(ll(0.2,p) for p in ps),ll_mult=max(ll(0.3375,p) for p in ps),
               n=len(obs),obs=dict(collections.Counter(obs))),open("m-profile.json","w"),indent=1)
