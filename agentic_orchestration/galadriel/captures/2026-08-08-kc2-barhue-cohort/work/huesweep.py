#!/usr/bin/env python3
"""huesweep.py — run eor_platebind.bar_hue over a fourth-extraction CENSUS json.

The fifth extraction's huescan.py consumed a `platebind.scan` json (frames ->
"rd"). This consumes an `eor_cohort.census` json (flat "rows"), which is the
EXACT record the fourth-extraction cohort tables were computed from. Sampling
that record row-for-row means the hue verdict lands on the same readouts that
were counted, not on a re-detection that might differ.

Primary sampler: PB.bar_hue, UNCHANGED from the fifth extraction, so w153's
published numbers stay comparable.

Secondary sampler (`strict`): same band, but reports BOTH channel counts at the
row of maximum total ink, plus a green/red ratio, so a contaminated scene shows
its contamination instead of hiding inside a modal vote.

  sweep <census.json> <video> <t_lo> <t_hi> <out.json>
"""
import json
import subprocess
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/"
                   "agentic_orchestration/galadriel/pipeline")
import eor_platebind as PB   # noqa: E402

W, H = 1920, 1080


def strict(fr, box, lo=8, hi=26, pad=12):
    """Both channels at the row of maximum total (red+green) ink."""
    a = fr.astype(np.int16)
    x0, y0, x1, y1 = box
    best = (0, 0, 0, None)   # tot, g, r, y
    for y in range(y1 + lo, min(y1 + hi, a.shape[0])):
        row = a[y, max(0, x0 - pad):min(a.shape[1], x1 + pad)]
        R, G, B = row[:, 0], row[:, 1], row[:, 2]
        g = int(((G > 70) & (G - R > 25) & (G - B > 25)).sum())
        r = int(((R > 70) & (R - G > 35) & (R - B > 35)).sum())
        if g + r > best[0]:
            best = (g + r, g, r, y)
    return best[1], best[2], best[3]


def run(census_path, video, t_lo, t_hi, out):
    d = json.load(open(census_path))
    rows = [r for r in d["rows"]
            if r["kind"] in ("full", "lclip") and r["max"]
            and t_lo <= r["t"] <= t_hi]
    byt = defaultdict(list)
    for r in rows:
        byt[round(r["t"], 4)].append(r)

    t0, t1, fps = d["t0"], d["t1"], d["fps"]
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", f"{t1-t0}", "-i",
           video, "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3)
    nb = W * H * 3
    samples = []
    i = 0
    while True:
        buf = p.stdout.read(nb)
        if len(buf) < nb:
            break
        t = round(t0 + i / fps, 4)
        i += 1
        rs = byt.get(t)
        if not rs:
            continue
        fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
        for r in rs:
            k, n, y = PB.bar_hue(fr, r["box"])
            g, rr, ys = strict(fr, r["box"])
            samples.append({"t": t, "max": r["max"], "cur": r["cur"],
                            "kind": r["kind"], "box": r["box"],
                            "hue": k or "none", "n": n, "y": y,
                            "g": g, "r": rr, "ys": ys})
    p.stdout.close(); p.wait()
    json.dump({"census": census_path, "t_lo": t_lo, "t_hi": t_hi,
               "n": len(samples), "s": samples}, open(out, "w"))
    print(f"sampled {len(samples)} readouts over {len(byt)} frames")
    return samples


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]),
        sys.argv[5])
