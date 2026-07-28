import csv,json,bisect,collections,math,statistics as st,pathlib
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
r1=[d for d in D if d["regime"]=="R1"]
print("R1 by player level:")
for lv in (1,2):
    v=sorted(d["mag"] for d in r1 if d["level"]==lv)
    print(f"  pL{lv}: n={len(v)} {v}")
print("\nR1 by engagement (t, mag):")
for e in sorted(set(d["eng_id"] for d in r1)):
    ds=sorted([d for d in r1 if d["eng_id"]==e], key=lambda x:x["t"])
    w=W[e]
    print(f"  eng{e} pt{w['play_time_start']}-{w['play_time_end']} cov={w['coverage']} maxhp={w['max_hp_modal']} kills={w['kills']}: "
          + " ".join(f"{d['mag']}@{d['t']:.2f}" for d in ds))
# composite-rate consistency with numAttackSlots=4
ds=sorted([d for d in r1 if d["eng_id"]==8], key=lambda x:x["t"])
gaps=[ds[i+1]["t"]-ds[i]["t"] for i in range(len(ds)-1)]
print(f"\neng8 drop-event rate = {len(ds)/(ds[-1]['t']-ds[0]['t']):.2f} events/s over {ds[-1]['t']-ds[0]['t']:.2f}s")
print(f"  P(k>=2 aliased | frame) implied by observed 2x-band share: {4/25:.2f}")
for lam in (2,3,4,5,6):
    f=1/15.0
    p1=lam*f*math.exp(-lam*f); p2=(lam*f)**2/2*math.exp(-lam*f)
    print(f"  Poisson lambda={lam}/s -> P(2 in frame)/P(1 in frame) = {p2/p1:.3f}")
