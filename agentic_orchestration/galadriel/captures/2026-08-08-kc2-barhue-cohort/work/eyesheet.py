#!/usr/bin/env python3
"""Build x6 eye-read sheets: readout + the bar underneath it, exact-seek frames.

Selection rule, stated so the sheet cannot be accused of cherry-picking: for each
fingerprint asked for, take up to `k` frames the sampler voted GREEN and up to
`k` it voted RED, spread across the fingerprint's span. If the sampler is wrong,
the disagreeing tiles are the ones that show it.
"""
import json
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/"
                   "agentic_orchestration/galadriel/pipeline")
import eor_grid as G   # noqa: E402

V = "/tmp/eor-w150-160.mp4"
OUT = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
       "galadriel/captures/2026-08-08-kc2-barhue-cohort/evidence")
WAVES = {151: (682.10, 5.97), 152: (698.38, 10.23), 153: (714.83, 8.60),
         157: (780.30, 8.63), 158: (799.43, 8.33)}


def spread(rows, k):
    if len(rows) <= k:
        return rows
    step = len(rows) / k
    return [rows[int(i * step)] for i in range(k)]


def jobs_for(w, fps_list, k=2):
    t0, dur = WAVES[w]
    s = json.load(open(f"hue-w{w}.json"))["s"]
    s = [x for x in s if t0 <= x["t"] <= t0 + dur]
    out = []
    for fp in fps_list:
        rs = sorted([x for x in s if x["max"] == fp], key=lambda x: x["t"])
        for hue in ("green", "red", "none"):
            sel = spread([x for x in rs if x["hue"] == hue], k)
            for x in sel:
                out.append({"t": x["t"], "box": x["box"],
                            "label": f"w{w} {fp:,} +{x['t']-t0:.2f} "
                                     f"cur={x['cur']} SAMP={hue} g={x['g']} r={x['r']}"})
    return out


if __name__ == "__main__":
    w = int(sys.argv[1])
    fps_list = [int(a) for a in sys.argv[2].split(",")]
    name = sys.argv[3]
    k = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    j = jobs_for(w, fps_list, k)
    print(f"{len(j)} tiles")
    p = G.sheet(V, j, f"{OUT}/{name}.png", zoom=6, padx=6, above=4, below=34,
                cols=2, per_page=8)
    print("\n".join(p))
