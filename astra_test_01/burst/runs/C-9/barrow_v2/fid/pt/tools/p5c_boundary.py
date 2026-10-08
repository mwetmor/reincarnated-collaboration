#!/usr/bin/env python3
"""BV2F PT (R-C9-251 M-4): the P5(c)-style CONTEXT-BOUNDARY step, ALL classes -- at every chunk's context boundary
(x = 1280c + 256 inside rows r*768..r*768+1024 for c >= 1; y = 768r + 256 inside cols c*1280..c*1280+1536 for r >= 1),
per 128-px segment along it: the low-pass (Gaussian sigma 6) Lab difference dE between the band 8..16 px before and 8..16
px after the line, MINUS the median of the same measure at parallel offsets of +-32, +-64, +-96 px (the texture's own
level there). A positive excess = a step AT the boundary the surroundings do not have. No class mask (the class-masked
join_steps/hf_steps were blind at 1_2|y1792 and 0_2|y1792 x >= 1088).
    python3 fid/pt/tools/p5c_boundary.py <painting.png> [label] [out.json]"""
import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage
P8 = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float64) / 255.0
lab_ = sys.argv[2] if len(sys.argv) > 2 else ""
c_ = np.where(P8 <= 0.04045, P8 / 12.92, ((P8 + 0.055) / 1.055) ** 2.4)
m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
xyz = c_ @ m.T / np.array([0.95047, 1.0, 1.08883])
e, k = 216 / 24389, 24389 / 27
f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
LB = np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
LF = np.stack([ndimage.gaussian_filter(LB[..., i], 6) for i in range(3)], -1)
H, W = LF.shape[:2]


def dE_x(x, y0, y1):
    return float(np.linalg.norm(LF[y0:y1, x - 16:x - 8].mean((0, 1)) - LF[y0:y1, x + 8:x + 16].mean((0, 1))))


def dE_y(y, x0, x1):
    return float(np.linalg.norm(LF[y - 16:y - 8, x0:x1].mean((0, 1)) - LF[y + 8:y + 16, x0:x1].mean((0, 1))))


res = {}
for r in range(3):
    for c in range(3):
        y0r, x0c = r * 768, c * 1280
        if c > 0:
            x = x0c + 256
            segs = []
            for s in range(y0r, y0r + 1024, 128):
                at = dE_x(x, s, s + 128)
                base = np.median([dE_x(x + o, s, s + 128) for o in (-96, -64, -32, 32, 64, 96)])
                segs.append({"seg": [s, s + 128], "dE": round(at, 2), "base": round(float(base), 2), "excess": round(at - float(base), 2)})
            res["%d_%d|x%d" % (c, r, x)] = segs
        if r > 0:
            y = y0r + 256
            segs = []
            for s in range(x0c, x0c + 1536, 128):
                at = dE_y(y, s, s + 128)
                base = np.median([dE_y(y + o, s, s + 128) for o in (-96, -64, -32, 32, 64, 96)])
                segs.append({"seg": [s, s + 128], "dE": round(at, 2), "base": round(float(base), 2), "excess": round(at - float(base), 2)})
            res["%d_%d|y%d" % (c, r, y)] = segs
summ = {k: {"max_excess": max(s["excess"] for s in v), "at": max(v, key=lambda s: s["excess"])["seg"],
            "segments_excess_over_3": sum(1 for s in v if s["excess"] > 3.0)} for k, v in res.items()}
if len(sys.argv) > 3:
    json.dump({"_what": __doc__.strip().splitlines()[0], "painting": sys.argv[1], "label": lab_, "summary": summ, "segments": res},
              open(sys.argv[3], "w"), indent=1)
for k, v in summ.items():
    print(lab_, k, v)
