#!/usr/bin/env python3
"""BV2F PT (R-C9-247) PROTOTYPE, read-only on the paint, OFF the build: the Tier-B DEV-23 stitch + a GRAIN match
(proposed DEV-25) -- per chunk, at each context boundary, the high-frequency amplitude (detail = image - Gaussian sigma
GRAIN_SIGMA) of the NEW paint's first 48 px is scaled toward that of the context strip's last 48 px (ratio measured on
bright low-chroma = snow/ice pixels, smoothed along the boundary sigma 56, clipped 0.5..1.5) and the scaling fades to 1
over 300 px into the chunk. Structure is not moved (no blur, no warp): only the amplitude of the existing grain changes.
    python3 fid/pt/tools/grain_match_proto.py <cfg.json> <out.png>"""
import json, os, runpy, sys
import numpy as np
from scipy import ndimage
FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRAIN_SIGMA, BAND, FADE, SIG = 3.0, 48, 300, 56.0
REP = {}


def _fade(n):
    t = np.clip(np.arange(n) / float(FADE), 0.0, 1.0)
    return 1.0 - t * t * (3.0 - 2.0 * t)


def _smooth(a):
    return (a.mean(-1) > 150) & ((a.max(-1) - a.min(-1)) < 70)


def _ratio_along(ctx_d, new_d, ctx_m, new_m):
    # per line along the boundary: std of the detail on smooth pixels, context / new; normalised smoothing along it
    def s(d, m):
        n = m.sum(1)
        mu = (d * m[..., None]).sum(1) / np.maximum(n, 1)[:, None]
        v = (((d - mu[:, None, :]) ** 2) * m[..., None]).sum(1) / np.maximum(n, 1)[:, None]
        return np.sqrt(v.mean(-1)), n
    sc, nc = s(ctx_d, ctx_m)
    sn, nn = s(new_d, new_m)
    w = ((nc >= 12) & (nn >= 12)).astype(float)
    k = np.where(w > 0, sc / np.maximum(sn, 1e-6), 1.0)
    gw = ndimage.gaussian_filter1d(w, SIG, mode="constant")
    ks = ndimage.gaussian_filter1d(k * w, SIG, mode="constant") / np.maximum(gw, 1e-6)
    ks = np.where(gw > 0.05, ks, 1.0)
    return np.clip(ks, 0.5, 1.5)


def grain(im, c, r):
    rep = {}
    OV = 256
    det = im - np.stack([ndimage.gaussian_filter(im[..., i], GRAIN_SIGMA) for i in range(3)], -1)
    sm = _smooth(im)
    H, W = im.shape[:2]
    if c > 0:
        k = _ratio_along(det[:, OV - BAND:OV], det[:, OV:OV + BAND], sm[:, OV - BAND:OV], sm[:, OV:OV + BAND])
        g = 1.0 + (k[:, None] - 1.0) * _fade(W - OV)[None, :]
        im = im.copy(); im[:, OV:] += det[:, OV:] * (g[..., None] - 1.0)
        rep["left_k_median"] = round(float(np.median(k)), 3)
        det = im - np.stack([ndimage.gaussian_filter(im[..., i], GRAIN_SIGMA) for i in range(3)], -1)
    if r > 0:
        T = lambda a: np.swapaxes(a, 0, 1)
        k = _ratio_along(T(det[OV - BAND:OV]), T(det[OV:OV + BAND]), T(sm[OV - BAND:OV]), T(sm[OV:OV + BAND]))
        g = 1.0 + (k[None, :] - 1.0) * _fade(H - OV)[:, None]
        im = im.copy(); im[OV:, :] += det[OV:, :] * (g[..., None] - 1.0)
        rep["top_k_median"] = round(float(np.median(k)), 3)
    REP["%d_%d" % (c, r)] = rep
    return im


# run the Tier-B stitch with its _bv2f_tone wrapped: tone match (DEV-23) THEN grain match
st = os.path.join(FID, "v1tools", "tierB", "conductor_scripts", "guided_stitch.py")
src = open(st).read()
a = "        im = _bv2f_tone(im, c, r)   # BV2F DEV-23\n"
assert src.count(a) == 1
src = src.replace(a, a + "        im = __grain(im, c, r)\n")
sys.argv = [st, sys.argv[1], sys.argv[2]]
g = {"__name__": "__main__", "__grain": grain, "__file__": st}
exec(compile(src, st, "exec"), g)
print("grain", REP)
