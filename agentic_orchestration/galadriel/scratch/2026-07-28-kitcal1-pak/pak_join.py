#!/usr/bin/env python3
"""KIT-CAL-1 item 3 — join G-5a's predicted monster hit band against the fixture's
measured HP-drop distribution. Read-only over existing artifacts. galadriel 2026-07-28."""
import csv, json, math, statistics as st, collections, pathlib

ROOT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel")
TA   = ROOT/"captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv"
WIN  = ROOT/"captures/2026-07-26-gd-playtest-v1-tb/tb-intake-windows.json"
DROP = ROOT/"captures/2026-07-28-gd-playtest-v1-g2c/g2c-drops.jsonl"

# ---------- 1. level series from the T-A ledger (panel max_level, forward-filled on pts) ----------
ta = []
for r in csv.DictReader(open(TA)):
    try: pts = float(r["pts_s"])
    except: continue
    ml = r["max_level"].strip()
    pt = r["play_time"].strip()
    ta.append((pts, int(ml) if ml.isdigit() else None, int(pt) if pt.isdigit() else None))
ta.sort()
def ffill(idx):
    out, last = [], None
    for row in ta:
        v = row[idx]
        if v is not None: last = v
        out.append(last)
    return out
LVL = ffill(1); PTM = ffill(2)
PTS = [r[0] for r in ta]
import bisect
def at(pts, series):
    i = bisect.bisect_right(PTS, pts) - 1
    return series[max(i,0)] if PTS else None

# ---------- 2. windows ----------
W = {w["eng_id"]: w for w in json.load(open(WIN))["windows"]}

# ---------- 3. drops ----------
drops = [json.loads(l) for l in open(DROP)]
for d in drops:
    w = W[d["eng_id"]]
    d["regime"]   = w["regime"]
    d["coverage"] = w["coverage"]
    d["play_time"]= at(d["t"], PTM)
    d["level"]    = at(d["t"], LVL)
print(f"drops loaded: {len(drops)}  (expected 468)")

# ---------- 4. level-band partition ----------
def band(l):
    if l is None: return "?"
    if l <= 2:  return "L1-2"
    if l <= 4:  return "L3-4"
    if l <= 6:  return "L5-6"
    if l <= 8:  return "L7-8"
    if l <= 9:  return "L9"
    if l <= 11: return "L10-11"
    return "L12+"
for d in drops: d["band"] = band(d["level"])

ORDER = ["L1-2","L3-4","L5-6","L7-8","L9","L10-11","L12+"]

def summ(v):
    if not v: return dict(n=0)
    v = sorted(v)
    q = lambda p: v[min(len(v)-1, int(round(p*(len(v)-1))))]
    return dict(n=len(v), min=v[0], p25=q(.25), p50=q(.50), p75=q(.75), p90=q(.90),
                max=v[-1], mean=round(st.mean(v),2),
                mode=collections.Counter(v).most_common(3))

print("\n=== drop magnitude by player-level band (all regimes) ===")
print(f"{'band':7} {'regime-mix':22} {'n':>4} {'min':>4} {'p25':>4} {'p50':>4} {'p75':>4} {'p90':>4} {'max':>5} {'mean':>7}  modes")
for b in ORDER:
    v = [d["mag"] for d in drops if d["band"]==b]
    rx = collections.Counter(d["regime"] for d in drops if d["band"]==b)
    s = summ(v)
    if not s["n"]: continue
    print(f"{b:7} {str(dict(rx)):22} {s['n']:>4} {s['min']:>4} {s['p25']:>4} {s['p50']:>4} {s['p75']:>4} {s['p90']:>4} {s['max']:>5} {s['mean']:>7}  {s['mode']}")

print("\n=== level transitions covered by drops ===")
c = collections.Counter((d["level"], d["regime"]) for d in drops)
for k in sorted(c, key=lambda x:(x[0] or 0, x[1])): print("  level",k[0],k[1],c[k])

# ---------- 5. ASCII histograms per band ----------
def hist(vals, title, hi=None, w=60):
    if not vals: print(f"\n{title}: EMPTY"); return
    hi = hi or max(vals)
    print(f"\n{title}   n={len(vals)}  max={max(vals)}")
    bins = collections.Counter(v for v in vals if v<=hi)
    top = max(bins.values())
    for k in range(1, min(hi,60)+1):
        n = bins.get(k,0)
        if n or k<=30:
            print(f"  {k:>3} | {'#'*int(round(w*n/top)):<{w}} {n}")
    ov = [v for v in vals if v>min(hi,60)]
    if ov: print(f"  >{min(hi,60)} | {sorted(ov)}")

for b in ORDER:
    v = [d["mag"] for d in drops if d["band"]==b]
    if v: hist(v, f"HIST {b}")
