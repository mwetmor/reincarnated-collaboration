#!/usr/bin/env python3
"""BV2F DEV-28 (R-C9-257 (c)): GUIDE SHADOW SMOOTHING -- fill and soften the renderer's PCF shadow dither in the
layout guide, before a canvas is cropped from it. Guide-only: the painting, the stitch and every other tool are
untouched. guided_paint.py (Tier-B) calls smooth() only when BV2F_DEV28=1; unset = v1's guide, byte for byte.

WHAT IT CHANGES. Godot's soft-shadow filter leaves a screen-door pattern where a shadow meets lit ground: lit and
shadowed pixels of ONE surface alternating at a 2-4 px period. The painter copies it as a dotted shadow. A dither
pixel is found by its 2x2 checker energy (the alternation, which a single straight edge does not have), counted only
where at least MIN_DENS of them crowd a 5 x 5 window (a hard edge's corner fires 1-4), and only pixels within DIL px
of one are touched.

WHAT IT CANNOT CHANGE. Each touched pixel becomes a Gaussian mean (sigma SIGMA) of neighbours that are (1) the SAME
object in the guide's ID render and (2) the same SHADOW-INVARIANT chromaticity: the guide's own shadow ratio k
(shadowed / lit per channel, measured on its dither; one sun, one ambient) is found first, and the chromaticity
component along k's tint is removed, so a lit, a half-lit and a shadowed pixel of one surface match and two
materials do not. So no colour crosses a silhouette or a material boundary: a rock never bleeds into the snow, the path never
bleeds into the snow. Silhouette rims (any pixel whose 3 x 3 window holds two IDs) and the pen's ink (grey < INK_GREY)
are PROTECTED: never changed and never averaged in. Pixels outside the dither zone are returned byte for byte.

  smooth(guide: PIL.Image RGB, ids: PIL.Image RGB same size) -> (PIL.Image RGB, report dict)
  python3 dev28.py <guide.png> <ids.png> <out.png>      (standalone, for tests)
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

T_CHECK = 3.0     # 2x2 checker energy (grey levels) that marks a dither pixel
MIN_DENS = 8      # dither pixels needed in a 5 x 5 window: a PATTERN, not the lone corner of a hard edge
DIL = 2           # px around a dither pixel that may change
SIGMA = 1.6       # Gaussian sigma, px
RAD = 4           # kernel radius, px (9 x 9)
TOL_CHROMA = 0.015  # max |r/(r+g+b) - ...| difference for a neighbour to count as the same surface
INK_GREY = 70     # pixels darker than this are the pen's ink: never changed, never averaged in


def detect(a: np.ndarray) -> tuple:
    g = a.astype(np.float32).mean(-1)
    cb = np.abs(g[:-1, :-1] - g[1:, :-1] - g[:-1, 1:] + g[1:, 1:]) / 4.0
    e = np.zeros_like(g)
    for dy in (0, 1):
        for dx in (0, 1):   # a pixel's energy = the max over the four 2x2 blocks that contain it
            sl = e[dy:dy + cb.shape[0], dx:dx + cb.shape[1]]
            np.maximum(sl, cb, out=sl)
    d0 = e >= T_CHECK
    d0 &= ndimage.uniform_filter(d0.astype(np.float32), 5) * 25.0 >= MIN_DENS - 0.5
    zone = ndimage.binary_dilation(d0, iterations=DIL) if d0.any() else d0
    return e, d0, zone


def shadow_tint(af: np.ndarray, seg: np.ndarray, d0: np.ndarray) -> np.ndarray:
    """The guide's shadow ratio (shadowed / lit, per channel) measured on its own dither: neighbouring pixel pairs of
    one object, both in the dither, luminance ratio 0.3..0.9, the lit one > 120. One sun and one ambient -> one ratio."""
    ys, xs = np.nonzero(d0[:-1, :-1])
    rs = []
    for dy, dx in ((0, 1), (1, 0)):
        p = af[ys, xs]; q = af[ys + dy, xs + dx]
        lp = p.mean(-1); lq = q.mean(-1)
        hi = np.where((lp > lq)[:, None], p, q); lo = np.where((lp > lq)[:, None], q, p)
        lr = np.minimum(lp, lq) / np.maximum(np.maximum(lp, lq), 1.0)
        m = (seg[ys, xs] == seg[ys + dy, xs + dx]) & (lr > 0.3) & (lr < 0.9) & (np.maximum(lp, lq) > 120)
        rs.append(lo[m] / np.maximum(hi[m], 1.0))
    r = np.concatenate(rs) if rs else np.zeros((0, 3))
    return np.median(r, 0) if len(r) >= 1000 else np.ones(3, np.float32)


def smooth(guide: Image.Image, ids: Image.Image):
    a = np.asarray(guide.convert("RGB"))
    b = np.asarray(ids.convert("RGB"))
    if a.shape != b.shape:
        raise ValueError("DEV-28: guide %s and ID render %s differ in size" % (a.shape, b.shape))
    H, W, _ = a.shape
    seg = (b[..., 0].astype(np.int32) << 16) | (b[..., 1].astype(np.int32) << 8) | b[..., 2].astype(np.int32)
    af = a.astype(np.float32)
    e, d0, zone = detect(a)
    k = shadow_tint(af, seg, d0)
    # SHADOW-INVARIANT surface signature: the chromaticity with its component along the shadow's own tint removed, so a
    # lit pixel and a shadowed (or half-shadowed) pixel of the same surface match, while two materials do not
    d = k / k.mean() - 1.0
    d = d / max(float(np.linalg.norm(d)), 1e-6)
    c = af / np.maximum(af.sum(-1, keepdims=True), 1.0)
    chroma = c - (c @ d)[..., None] * d
    # PROTECTED: a 3 x 3 window holding two IDs (a silhouette and its antialiased rim) and the pen's dark ink lines
    border = ndimage.maximum_filter(seg, size=3) != ndimage.minimum_filter(seg, size=3)
    protect = border | (af.mean(-1) < INK_GREY)
    zone = zone & ~protect
    ys, xs = np.nonzero(zone)
    acc = np.zeros((ys.size, 3), np.float32)
    wsum = np.zeros(ys.size, np.float32)
    s0 = seg[ys, xs]
    c0 = chroma[ys, xs]
    for oy in range(-RAD, RAD + 1):
        for ox in range(-RAD, RAD + 1):
            w = np.float32(np.exp(-(ox * ox + oy * oy) / (2.0 * SIGMA * SIGMA)))
            yy = np.clip(ys + oy, 0, H - 1)
            xx = np.clip(xs + ox, 0, W - 1)
            ok = (seg[yy, xx] == s0) & (np.abs(chroma[yy, xx] - c0).max(-1) <= TOL_CHROMA) & ~protect[yy, xx]
            ok &= (ys + oy >= 0) & (ys + oy < H) & (xs + ox >= 0) & (xs + ox < W)
            wk = w * ok
            acc += af[yy, xx] * wk[:, None]
            wsum += wk
    out = a.copy()
    out[ys, xs] = np.clip(np.rint(acc / wsum[:, None]), 0, 255).astype(np.uint8)   # wsum >= 1 (the pixel itself)
    rep = {"params": {"T_CHECK": T_CHECK, "MIN_DENS": MIN_DENS, "DIL": DIL, "SIGMA": SIGMA, "RAD": RAD, "TOL_CHROMA": TOL_CHROMA, "INK_GREY": INK_GREY},
           "shadow_tint_k": [round(float(x), 4) for x in k], "px": [W, H], "dither_px": int(d0.sum()), "zone_px": int(zone.sum()),
           "changed_px": int((out != a).any(-1).sum()), "zone_share": float(zone.mean())}
    return Image.fromarray(out), rep


if __name__ == "__main__":
    import json
    im, rep = smooth(Image.open(sys.argv[1]), Image.open(sys.argv[2]))
    im.save(sys.argv[3])
    print(json.dumps(rep))
