#!/usr/bin/env python3
"""RANK BY GLYPH COLOUR — the fifth extraction's § 3.1 law, applied to w157.

§ 3.1 measurement, reproduced exactly: name-glyph CORE colour = mean RGB over the
brightest quartile of pixels with max-channel > 170, rows 16..36 of the frame.

    white  -> common     G/R 0.98-1.00   B/R 0.93-0.99
    yellow -> champion   G/R 0.91-0.95   B/R 0.40-0.49
    orange -> hero       G/R 0.71-0.79   B/R 0.41-0.48
    violet -> boss       G/R 0.86        B/R 1.04

`plate_metrics.name_rgb` is NOT this measure (it means over min(RGB) > 120, which
is white-biased and compresses the bands). The § 3.1 rule is re-implemented here
so the same numbers the law was stated in are the numbers it is applied in.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/"
                   "agentic_orchestration/galadriel/pipeline")
import eor_platebind as PB   # noqa: E402

V = "/tmp/eor-w150-160.mp4"
X0, X1 = 861.1, 1060.9       # fifth extraction § 2.3 consensus calibration


def grab(t, d="/tmp/kc2bh"):
    os.makedirs(d, exist_ok=True)
    p = f"{d}/g_{t}.png"
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", V,
                        "-frames:v", "1", "-y", p], check=True)
    return np.array(Image.open(p).convert("RGB"))


def glyph_core(fr, y0=16, y1=36, x0=600, x1=1350):
    """§ 3.1: brightest quartile of pixels with max-channel > 170."""
    a = fr[y0:y1, x0:x1].astype(np.float64)
    mx = a.max(2)
    sel = mx > 170
    if sel.sum() < 20:
        return None, 0
    v = a[sel]
    b = mx[sel]
    thr = np.quantile(b, 0.75)
    core = v[b >= thr]
    m = core.mean(0)
    return m, int(sel.sum())


def cls(gr, br):
    if br > 0.90 and gr > 0.96:
        return "white->common"
    if br > 0.90:
        return "violet->boss"
    if gr >= 0.86:
        return "yellow->champion"
    if gr >= 0.62:
        return "orange->hero"
    return "?"


def main(scanpath):
    d = json.load(open(scanpath))
    sps = PB.spans2(d["f"])
    out = []
    for sp in sps:
        if len(sp["fr"]) < 2:
            continue
        mid = sp["fr"][len(sp["fr"]) // 2]
        fr = grab(mid["t"])
        m, n = glyph_core(fr)
        if m is None:
            continue
        gr, br = m[1] / m[0], m[2] / m[0]
        edges = [f["plate"]["fill_end"] for f in sp["fr"]
                 if f["plate"]["fill_end"]]
        fpl = [round((e - X0) / (X1 - X0), 4) for e in edges]
        out.append({"t0": sp["t0"], "t1": sp["t1"], "n": len(sp["fr"]),
                    "rgb": [round(x, 1) for x in m], "gr": round(gr, 3),
                    "br": round(br, 3), "cls": cls(gr, br), "npx": n,
                    "f": fpl, "tmid": mid["t"],
                    "contrast": mid["plate"]["contrast"]})
    json.dump(out, open("w157-spans.json", "w"), indent=1)
    print(f"{len(out)} spans")
    print(f"{'t0':>8} {'t1':>8} {'n':>3} {'contr':>6} {'G/R':>6} {'B/R':>6}  "
          f"{'class':<16} f_plate")
    for r in out:
        print(f"{r['t0']:>8.3f} {r['t1']:>8.3f} {r['n']:>3} "
              f"{r['contrast']:>6.1f} {r['gr']:>6.3f} {r['br']:>6.3f}  "
              f"{r['cls']:<16} {r['f'][:4]}")


if __name__ == "__main__":
    main(sys.argv[1])
