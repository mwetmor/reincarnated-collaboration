#!/usr/bin/env python3
"""BV2F PT (R-C9-247, read-only): every internal join of a prefix's chunk grid -- the overlap MAD (P5's measure: mean abs
difference between the two chunks' renditions of the shared 256-px strip), the strip's TEXTURE (Laplacian variance of the
neighbour's pixels there), and the share of the strip that is BRIGHT LOW-CHROMA (snow/ice: smooth) vs not. Also the
texture STEP at each context boundary in the chunk (HF std of the 32 px after the boundary over the 32 px before, on bright
low-chroma pixels; 1.0 = same grain).
    python3 fid/pt/tools/join_mad_survey.py <prefix> <cols> <rows>  -> fid/pt/r247/join_mad_<prefix>.json"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A9 = os.path.abspath(os.path.join(FID, "..", "..", "artifacts"))
P, C, R = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
LAP = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)


def src(k):
    for d in ("%s-%s-r1" % (P, k), "%s-%s" % (P, k)):
        p = "%s/%s/%s-%s.png" % (A9, d, P, k)
        if os.path.exists(p):
            return p


im = {}
for r in range(R):
    for c in range(C):
        p = src("%d_%d" % (c, r))
        if p:
            im[(c, r)] = np.asarray(Image.open(p).convert("RGB")).astype(np.float64)
smooth = lambda a: (a.mean(-1) > 150) & ((a.max(-1) - a.min(-1)) < 70)
lv = lambda a: float(ndimage.convolve(a.mean(-1), LAP)[2:-2, 2:-2].var())
rows = []
for (c, r), a in im.items():
    for (nc, nr, A_, B_) in ((c + 1, r, (slice(None), slice(1280, 1536)), (slice(None), slice(0, 256))),
                             (c, r + 1, (slice(768, 1024), slice(None)), (slice(0, 256), slice(None)))):
        if (nc, nr) not in im:
            continue
        b = im[(nc, nr)]
        sa, sb = a[A_], b[B_]
        mad = float(np.abs(sa - sb).mean())
        # texture step INSIDE the neighbour chunk at its context boundary
        hpb = b.mean(-1) - ndimage.gaussian_filter(b.mean(-1), 3)
        ok = smooth(b)
        if nc != c:
            pre, post, mp, mq = hpb[:, 224:256], hpb[:, 256:288], ok[:, 224:256], ok[:, 256:288]
        else:
            pre, post, mp, mq = hpb[224:256], hpb[256:288], ok[224:256], ok[256:288]
        step = round(float(post[mq].std() / max(pre[mp].std(), 1e-6)), 3) if mp.sum() > 500 and mq.sum() > 500 else None
        rows.append({"join": "%d_%d%s%d_%d" % (c, r, "|" if nc != c else "/", nc, nr), "mad": round(mad, 2),
                     "strip_Lv": round(lv(sa), 1), "smooth_share": round(float(smooth(sa).mean()), 3), "texture_step": step})
rows.sort(key=lambda x: -x["mad"])
m = np.array([x["mad"] for x in rows]); t = np.array([x["strip_Lv"] for x in rows])
summ = {"joins": len(rows), "mad_min_med_max": [round(float(m.min()), 2), round(float(np.median(m)), 2), round(float(m.max()), 2)],
        "over_13.09": int((m > 13.09).sum()), "corr_mad_vs_strip_texture": round(float(np.corrcoef(m, t)[0, 1]), 3),
        "corr_mad_vs_smooth_share": round(float(np.corrcoef(m, [x["smooth_share"] for x in rows])[0, 1]), 3)}
os.makedirs(os.path.join(FID, "pt", "r247"), exist_ok=True)
json.dump({"_what": __doc__.strip().splitlines()[0], "prefix": P, "summary": summ, "joins": rows},
          open(os.path.join(FID, "pt", "r247", "join_mad_%s.json" % P), "w"), indent=1)
print(P, summ)
for x in rows:
    print("  ", x)
