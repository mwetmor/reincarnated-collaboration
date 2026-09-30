#!/usr/bin/env python3
"""C-9 lane B: read a meteor perf JSON (the scene's own frame-by-frame record) and print the budget lines.
   perf_report.py <perf.json> [label]"""
import json, sys, statistics as st
d = json.load(open(sys.argv[1]))
lab = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
fr = d.get("frames") or {}
ms, t, ph, dc, gpu, cpu, fx = (fr.get(k, []) for k in ("ms", "t", "phase", "dc", "gpu", "cpu", "fx_us"))
ev = d.get("events", [])
names = {0: "idle", 1: "cold first cast", 2: "casts 2-20 (fx on)", 3: "casts 1-20 (fx OFF, control)"}
def s(a):
    if not a: return "-"
    a = sorted(a); n = len(a)
    return f"mean {st.mean(a):6.2f}  p50 {a[n//2]:6.2f}  p95 {a[min(n-1,int(n*.95))]:6.2f}  p99 {a[min(n-1,int(n*.99))]:6.2f}  max {a[-1]:6.2f}  (n={n})"
print(f"== {lab}: renderer={d.get('renderer')} web={d.get('web')} render_px={d.get('render_px')} vsync={d.get('vsync')}")
for p, nm in names.items():
    idx = [i for i in range(len(ms)) if ph[i] == p]
    print(f"  {nm:30s} frame ms  {s([ms[i] for i in idx])}")
    print(f"  {'':30s} gpu ms    {s([gpu[i] for i in idx])}")
    print(f"  {'':30s} dc        {s([float(dc[i]) for i in idx])}")
    print(f"  {'':30s} fx script {s([fx[i]/1000 for i in idx])}")
    print(f"  {'':30s} frames > 20 ms: {sum(1 for i in idx if ms[i] > 20)}   > 33 ms: {sum(1 for i in idx if ms[i] > 33.4)}")
# windows: frames from 20 ms before to 150 ms after each event
for kind in ("cast", "release", "impact"):
    for p in (1, 2, 3):
        es = [e for e in ev if e["kind"] == kind and e["phase"] == p]
        worst = 0.0; worst_dc = 0
        for e in es:
            for i in range(len(ms)):
                if e["t"] - 20 <= t[i] <= e["t"] + 150:
                    worst = max(worst, ms[i]); worst_dc = max(worst_dc, dc[i])
        if es:
            print(f"  window {kind:8s} {names[p]:30s} events {len(es):2d}  worst frame {worst:6.2f} ms  max dc {worst_dc}")
on = [ms[i] for i in range(len(ms)) if ph[i] in (1, 2)]
off = [ms[i] for i in range(len(ms)) if ph[i] == 3]
gon = [gpu[i] for i in range(len(ms)) if ph[i] in (1, 2)]
goff = [gpu[i] for i in range(len(ms)) if ph[i] == 3]
if on and off:
    print(f"  EFFECT COST over the 20-cast runs: frame {st.mean(on) - st.mean(off):+.3f} ms/frame (on {st.mean(on):.3f} vs off {st.mean(off):.3f});"
          f" gpu {st.mean(gon) - st.mean(goff):+.3f} ms/frame; fx script mean {st.mean([fx[i]/1000 for i in range(len(ms)) if ph[i] in (1,2)]):.3f} ms")
    dmax_on = max(dc[i] for i in range(len(ms)) if ph[i] in (1, 2)); dmax_off = max(dc[i] for i in range(len(ms)) if ph[i] == 3)
    print(f"  DRAW CALLS peak: fx on {dmax_on}, fx off {dmax_off}: added at peak {dmax_on - dmax_off}")
