#!/usr/bin/env python3
"""Segment the w152 30 Hz plate scan into held-plate runs; report rank colour.

Reads the skull-plate pass's plate-w152.json (523 frames, 697.8 -> 715.2 @30Hz),
which carries plate metrics only (no census). Segmentation follows
eor_platebind.spans2 semantics: split on name ink-count jump or rank-colour drift.
"""
import json
import sys

P = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-08-kc2-w152-skull-plate/work/plate-w152.json"

d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else P))
rows = d["rows"]
print("frames", len(rows), "t", rows[0]["t"], "->", rows[-1]["t"])


def is_plate(p):
    return p["name_px"] >= 40 and p["name_rows"] >= 6


segs, cur, miss = [], None, 0
for f in rows:
    if not is_plate(f) or not f["name_rgb"]:
        miss += 1
        if cur and miss > 2:
            segs.append(cur); cur = None
        continue
    miss = 0
    if cur is None:
        cur = {"fr": [f]}; continue
    q = cur["fr"][-1]
    dpx = abs(f["name_px"] - q["name_px"]) / max(1, q["name_px"])
    dc = max(abs(a - b) for a, b in zip(f["name_rgb"], q["name_rgb"]))
    if dpx > 0.13 or dc > 9:
        segs.append(cur); cur = {"fr": [f]}
    else:
        cur["fr"].append(f)
if cur:
    segs.append(cur)

print(f"{'seg':>3} {'t0':>9} {'t1':>9} {'n':>3}  {'RGB':>16} {'R-B':>5} {'G-B':>5}"
      f"  {'rank':<10} {'namebbox':>12} {'lvlpx':>5} {'fillend':>7}")
out = []
for i, s in enumerate(segs):
    fr = s["fr"]
    n = len(fr)
    mr = [round(sum(f["name_rgb"][k] for f in fr) / n) for k in range(3)]
    rb, gb = mr[0] - mr[2], mr[1] - mr[2]
    if rb <= 8 and gb <= -8:
        rank = "VIOLET/boss"
    elif rb > 55:
        rank = "orange?"
    elif rb > 30:
        rank = "yellow?"
    else:
        rank = "white?"
    x0 = min(f["name_x0"] for f in fr)
    x1 = max(f["name_x1"] for f in fr)
    lp = round(sum(f["lvl_px"] for f in fr) / n)
    fe = [f["fill_end"] for f in fr if f["fill_end"]]
    print(f"{i:>3} {fr[0]['t']:>9.4f} {fr[-1]['t']:>9.4f} {n:>3}  {str(tuple(mr)):>16}"
          f" {rb:>5} {gb:>5}  {rank:<10} {f'{x0}..{x1}':>12} {lp:>5}"
          f" {(str(min(fe)) + '-' + str(max(fe))) if fe else '-':>9}")
    out.append({"i": i, "t0": fr[0]["t"], "t1": fr[-1]["t"], "n": n, "rgb": mr,
                "rb": rb, "gb": gb, "name_x0": x0, "name_x1": x1, "lvl_px": lp,
                "ts": [f["t"] for f in fr],
                "fill_end": [f["fill_end"] for f in fr]})
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "/tmp/segs.json", "w"), indent=1)
