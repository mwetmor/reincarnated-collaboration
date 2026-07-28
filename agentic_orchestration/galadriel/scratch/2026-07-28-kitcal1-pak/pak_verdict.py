#!/usr/bin/env python3
"""Comb / atomic-quantum test + per-regime verdict. galadriel 2026-07-28."""
import csv, json, math, collections, bisect, statistics as st, pathlib
ROOT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel")
ta=[]
for r in csv.DictReader(open(ROOT/"captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv")):
    try: pts=float(r["pts_s"])
    except: continue
    ml=r["max_level"].strip(); pt=r["play_time"].strip()
    ta.append((pts, int(ml) if ml.isdigit() else None, int(pt) if pt.isdigit() else None))
ta.sort(); PTS=[x[0] for x in ta]
def ff(i):
    o,l=[],None
    for x in ta:
        if x[i] is not None: l=x[i]
        o.append(l)
    return o
LVL,PTM=ff(1),ff(2)
def at(t,s): return s[max(bisect.bisect_right(PTS,t)-1,0)]
W={w["eng_id"]:w for w in json.load(open(ROOT/"captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json"))["windows"]}
D=[json.loads(l) for l in open(ROOT/"captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl")]
for d in D:
    d["regime"]=W[d["eng_id"]]["regime"]; d["level"]=at(d["t"],LVL); d["play_time"]=at(d["t"],PTM)

PB=json.load(open("predicted-bands.json"))["bands"]
def bandv(cl,tier,rd): return PB[str(cl)][str(tier)][rd]

# ---------- inter-drop interval structure (attack vs DoT) ----------
print("=== inter-drop intervals within engagement, by regime ===")
for reg in ("R1","R2","R3"):
    gaps=collections.defaultdict(list)
    byeng=collections.defaultdict(list)
    for d in D:
        if d["regime"]==reg: byeng[d["eng_id"]].append(d)
    g=[]
    for e,v in byeng.items():
        v.sort(key=lambda x:x["t"])
        g += [round(v[i+1]["t"]-v[i]["t"],3) for i in range(len(v)-1)]
    if not g: continue
    near1 = sum(1 for x in g if 0.90<=x<=1.10)
    print(f" {reg}: n_gaps={len(g)} median={st.median(g):.3f}s  p10={sorted(g)[len(g)//10]:.3f} "
          f"p90={sorted(g)[int(len(g)*0.9)]:.3f}  share in [0.90,1.10]s (1 Hz DoT signature) = {near1/len(g):.1%}")
# DoT signature: mag==1 share
print("\n=== mag==1 share (1 HP/frame DoT decay signature, per T-B s.2) by regime ===")
for reg in ("R1","R2","R3"):
    v=[d["mag"] for d in D if d["regime"]==reg]
    print(f" {reg}: n={len(v)}  mag==1: {sum(1 for x in v if x==1)} ({sum(1 for x in v if x==1)/len(v):.1%})  mag<=2: {sum(1 for x in v if x<=2)/len(v):.1%}")

# ---------- R1 comb test ----------
print("\n=== R1 (player L1-2) comb / atomic-quantum test ===")
r1=sorted(d["mag"] for d in D if d["regime"]=="R1")
print(" magnitudes:", r1)
def comb_fit(vals, lo, hi, kmax=4):
    """fraction of observations explained as k*[lo,hi] for some k<=kmax, plus per-k assignment"""
    ok=0; assign=collections.Counter(); unexp=[]
    for v in vals:
        hit=None
        for k in range(1,kmax+1):
            if k*lo-0.5 <= v <= k*hi+0.5: hit=k; break
        if hit: ok+=1; assign[hit]+=1
        else: unexp.append(v)
    return ok/len(vals), dict(assign), unexp
for rd,label in (("add","ADDITIVE"),("mult","MULTIPLICATIVE")):
    for cl in (1,2):
        lo,hi=bandv(cl,1,rd)
        frac,asg,un=comb_fit(r1,lo,hi)
        # 1x-band capture: how many obs fall in the 1x band
        one=sum(1 for v in r1 if lo-0.5<=v<=hi+0.5)
        print(f" {label:15} charL={cl} 1x band [{lo:.2f},{hi:.2f}] -> 1x-captures {one}/{len(r1)}"
              f" ({one/len(r1):.0%}); comb(k<=4) explains {frac:.0%}; k-mix {asg}; unexplained {un}")

# ---------- atomic-hit mode per level band, DoT/composite stripped ----------
print("\n=== atomic-hit mode per player level, with predicted bands (pre-mitigation) ===")
def qbands(cl):
    return {rd: (bandv(cl,1,rd), bandv(cl,2,rd)) for rd in ("add","mult")}
print(f"{'pL':>3} {'reg':>6} {'n':>4} {'n>2':>4} {'mode(>2)':>9} {'p50(>2)':>8} {'p25-p75(>2)':>12} | "
      f"{'ADD t1':>13} {'ADD t2':>13} | {'MULT t1':>13} {'MULT t2':>13}")
rows=[]
for lv in range(1,14):
    v=[d["mag"] for d in D if d["level"]==lv]
    if not v: continue
    reg=collections.Counter(d["regime"] for d in D if d["level"]==lv).most_common(1)[0][0]
    a=[x for x in v if x>2]
    if not a: a=v
    a_s=sorted(a); md=collections.Counter(a).most_common(1)[0]
    cl=lv  # proxy-pool spawn level tracks pL (lv1_weak pL-1 .. lv3_strong pL); use pL and pL-1
    b=qbands(max(cl-1,1)); b2=qbands(cl)
    q=lambda p: a_s[min(len(a_s)-1,int(round(p*(len(a_s)-1))))]
    fmt=lambda t:f"{t[0]:5.1f}-{t[1]:5.1f}"
    print(f"{lv:>3} {reg:>6} {len(v):>4} {len(a):>4} {str(md):>9} {st.median(a):>8.0f} "
          f"{str((q(.25),q(.75))):>12} | {fmt(b['add'][0]):>13} {fmt(b['add'][1]):>13} | "
          f"{fmt(b['mult'][0]):>13} {fmt(b['mult'][1]):>13}")
    rows.append(dict(level=lv,regime=reg,n=len(v),n_gt2=len(a),mode=md[0],mode_n=md[1],
                     p50=st.median(a),p25=q(.25),p75=q(.75),
                     add_t1=b['add'][0],add_t2=b['add'][1],mult_t1=b['mult'][0],mult_t2=b['mult'][1]))
json.dump(rows, open("verdict-rows.json","w"), indent=1)

# ---------- armor offset required to reconcile each reading ----------
print("\n=== implied player per-region protection p required for each reading to match observed p50 ===")
print("   taken = d - 0.70*min(d,p)  =>  for d>p: p = (d_mid - taken)/0.70")
for r in rows:
    for rd,key in (("ADD","add_t1"),("MULT","mult_t1")):
        dmid=(r[key][0]+r[key][1])/2
        p=(dmid-r["p50"])/0.70
        print(f"  pL{r['level']:>2} {rd:5} d_mid={dmid:6.2f} observed p50={r['p50']:5.1f} -> implied p = {p:7.2f}"
              + ("   <-- NEGATIVE: reading UNDER-predicts observed intake" if p<0 else ""))
