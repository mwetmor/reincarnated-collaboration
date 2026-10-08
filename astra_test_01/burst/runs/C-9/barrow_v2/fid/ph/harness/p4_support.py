#!/usr/bin/env python3
"""P4 SNOW MINIMUM-SUPPORT RULE, calibrated on v1 subsamples (R-C9-272; jack-ryan pilot-4 Gate-2 § 4: "calibrated on v1's
own low-support chunks ... for Phase 3' only, never applied to pilot 4"). v1 has no low-support chunk (min 40 P4 windows),
so v1's chunks are SUBSAMPLED: support k = the number of P4 spectrum windows (p4_texture.windows: 64 px, >= 90 % snow, step
64) a chunk's snow offers; a k-window subsample's snow mask = the union of k random windows of that chunk. For each k, 60
draws per v1 chunk; each draw is scored against the pool of the OTHER 15 chunks with the frozen § 3 bars (hist 0.281, spec
0.097). W_min = the smallest k at which >= 95 % of v1's own draws PASS. A Phase 3' chunk with fewer than W_min snow windows
is reported 'snow: insufficient support' (not judged), never PASS. -> results/p4_support_rule.json"""
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa
import p4_texture as T

KS = (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 40, 60, 80, 100, 120)
DRAWS = 60


def main(cls="snow", min_chunk_windows=40):
    masks, static = T.v1_classes()
    P = load_rgb(BF / "paint/barrow_full_painted.png")
    lab, gray = rgb_to_lab(P), luma(P)
    per = T.v1_pool(P, masks, static)
    bars = T.v1_bars(per)
    hb, sb = bars[cls]["hist"], bars[cls]["spec"]
    rng = np.random.default_rng(272)
    res = {k: [] for k in KS}
    nwin = {}
    for key, (x0, y0, x1, y1) in T.v1_chunks():
        m = ndimage.binary_erosion(masks[cls][y0:y1, x0:x1], iterations=3)
        wins = T.windows(m)
        if len(wins) < min_chunk_windows:
            continue
        ph, ps = T.pooled(per, cls, exclude=key)
        if ph is None or ps is None:
            continue
        nwin[key] = len(wins)
        L, G = lab[y0:y1, x0:x1], gray[y0:y1, x0:x1]
        for k in KS:
            if k > len(wins):            # k beyond this chunk's own support: only chunks that have >= k windows enter
                continue
            for _ in range(DRAWS):
                pick = [wins[i] for i in rng.choice(len(wins), k, replace=False)]
                sub = np.zeros_like(m)
                for (wy, wx) in pick:
                    sub[wy:wy + T.WIN, wx:wx + T.WIN] = m[wy:wy + T.WIN, wx:wx + T.WIN]
                dh = T.hellinger(T.lab_hist(L[sub]), ph)
                sp = T.spectrum_shape(G, pick)
                ds = float(np.sqrt(np.mean((sp - ps) ** 2)))
                res[k].append(dh <= hb and ds <= sb)
    table = {k: round(float(np.mean(v)), 4) for k, v in res.items() if v}
    ndraw = {k: len(v) for k, v in res.items()}
    wmin = next((k for k in table if table[k] >= 0.95 and all(table[j] >= 0.95 for j in table if j >= k)), None)
    out = {"_what": __doc__.split("\n")[0], "class": cls, "v1_chunk_windows": nwin, "min_chunk_windows": min_chunk_windows,
           "bars": {"hist": hb, "spec": sb}, "draws_per_chunk_per_k": DRAWS,
           "v1_pass_rate_by_k": table, "draws_by_k": ndraw, "W_min": wmin,
           "rule": "Phase 3' only: a chunk with < W_min P4 %s windows -> '%s: insufficient support' (not judged); never applied to pilot 4" % (cls, cls)}
    dump(out, str(PH / ("results/p4_support_rule.json" if cls == "snow" else "results/p4_support_rule_%s.json" % cls)))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "snow"
    main(c, int(sys.argv[2]) if len(sys.argv) > 2 else 40)
