#!/usr/bin/env python3
"""BV2F PT (R-C9-247, read-only): trace a chunk's pasted context strip through the pipeline and measure its SHARPNESS
(variance of the 3x3 Laplacian of luminance, Lv) and FIDELITY (response vs request, the same pixels):
  N  = the painted neighbour's own pixels for the strip (its delivered PNG)
  Q  = the REQUEST canvas strip (artifacts/CS9-guides/<bid>_canvas.png) -- must equal N where the paste rule put N
  R  = the RESPONSE strip (the chunk's delivered PNG, cols 0..255 / rows 0..255) and Rn = the response's NEW paint next
       to it (cols 256..511 / rows 256..511)
  RAW = the image service's own output file (provenance path), compared byte for byte with the delivered PNG
For every left (and top) strip of every chunk of a prefix: Lv(N), Lv(Q), Lv(R), Lv(Rn), Lv(R)/Lv(N) (the redraw's
sharpness ratio on identical content), Lv(Rn)/Lv(R) (the step at the boundary), MAD(R - Q) and the high-pass correlation
of R with Q (does the model redraw the strip or keep it?).
    python3 fid/pt/tools/strip_trace.py <prefix> [<prefix> ...]  -> fid/pt/r247/strip_trace_<prefix>.json"""
import glob, hashlib, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A9 = os.path.abspath(os.path.join(FID, "..", "..", "artifacts"))
OUT = os.path.join(FID, "pt", "r247")
os.makedirs(OUT, exist_ok=True)
SX, SY, OV = 1280, 768, 256
LAP = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
lum = lambda a: a.astype(np.float64).mean(-1)
lv = lambda a: round(float(ndimage.convolve(lum(a), LAP)[2:-2, 2:-2].var()), 1)
hp = lambda a: lum(a) - ndimage.gaussian_filter(lum(a), 2)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def src(P, k):
    for d in ("%s-%s-r1" % (P, k), "%s-%s" % (P, k)):
        p = "%s/%s/%s-%s.png" % (A9, d, P, k)
        if os.path.exists(p):
            return p, d


for P in sys.argv[1:]:
    keys = sorted({os.path.basename(d)[len(P) + 1:].replace("-r1", "") for d in glob.glob("%s/%s-*" % (A9, P))
                   if os.path.isdir(d) and os.path.basename(d)[len(P) + 1:].replace("-r1", "").count("_") == 1})
    res = {}
    for k in keys:
        c, r = map(int, k.split("_"))
        p, d = src(P, k)
        im = np.asarray(Image.open(p).convert("RGB"))
        cp = "%s/CS9-guides/%s_canvas.png" % (A9, d)
        can = np.asarray(Image.open(cp).convert("RGB")) if os.path.exists(cp) else None
        raw = []
        for f in glob.glob("%s/%s/*.provenance.json" % (A9, d)):
            rp = json.load(open(f))["path"]
            raw.append({"raw": os.path.basename(rp), "exists": os.path.exists(rp),
                        "delivered_is_raw_bytes": os.path.exists(rp) and sha(rp) == sha(p),
                        "size": list(Image.open(rp).size) if os.path.exists(rp) else None})
        e = {"delivered": os.path.relpath(p, A9), "size": list(im.shape[1::-1]), "canvas_size": list(can.shape[1::-1]) if can is not None else None,
             "raw": raw}
        for side, nk, Nsl, Rsl, Rnsl in (("left", "%d_%d" % (c - 1, r), (slice(None), slice(SX, SX + OV)), (slice(None), slice(0, OV)), (slice(None), slice(OV, 2 * OV))),
                                         ("top", "%d_%d" % (c, r - 1), (slice(SY, SY + OV), slice(None)), (slice(0, OV), slice(None)), (slice(OV, 2 * OV), slice(None)))):
            if (side == "left" and c == 0) or (side == "top" and r == 0):
                continue
            n = src(P, nk)
            if n is None:
                continue
            N = np.asarray(Image.open(n[0]).convert("RGB"))[Nsl]
            R = im[Rsl]
            Rn = im[Rnsl]
            Q = can[Rsl] if can is not None else None
            hq, hr = (hp(Q), hp(R)) if Q is not None else (None, None)
            e[side] = {"Lv_N": lv(N), "Lv_Q": lv(Q) if Q is not None else None, "Lv_R": lv(R), "Lv_Rnew": lv(Rn),
                       "Q_equals_N_px_share": round(float((Q == N).all(-1).mean()), 4) if Q is not None else None,
                       "R_over_N": round(lv(R) / max(lv(N), 1e-6), 3), "Rnew_over_R": round(lv(Rn) / max(lv(R), 1e-6), 3),
                       "MAD_R_Q": round(float(np.abs(R.astype(float) - Q.astype(float)).mean()), 2) if Q is not None else None,
                       "hp_corr_R_Q": round(float(np.corrcoef(hq.ravel(), hr.ravel())[0, 1]), 3) if Q is not None else None}
        res[k] = e
    json.dump({"_what": __doc__.strip().splitlines()[0], "prefix": P, "chunks": res}, open(os.path.join(OUT, "strip_trace_%s.json" % P), "w"), indent=1)
    for k, e in res.items():
        print(P, k, e["size"], e["canvas_size"], "raw==delivered:", [x["delivered_is_raw_bytes"] for x in e["raw"]],
              {s: {q: e[s][q] for q in ("Lv_N", "Lv_Q", "Lv_R", "Lv_Rnew", "Q_equals_N_px_share", "R_over_N", "Rnew_over_R", "MAD_R_Q", "hp_corr_R_Q")} for s in ("left", "top") if s in e})
