#!/usr/bin/env python3
"""C-9 T10-1d -- THE HEATHER'S TEXTURE, TONE, CONTRAST AND CLUSTERING, against the painting's.

Mean colour matched the painting's heather to dE 0.62 and the heather still read as golden
popcorn: bright round blobs, evenly spread. A mean cannot see either failure. So four more
questions, each asked of both images by the SAME rule:

  TEXTURE     how busy the image is where the heather is: local std of L* (7 px window) and
              edge density (Sobel |grad L*| over a threshold), sampled at heather pixels
  TONE        the spread of the heather's own L* and C* (p10 / p50 / p90): a painted tuft has
              dark sprigs and snow crumbs in it; a flat-lit blob is one colour
  CONTRAST    heather against the open snow right beside it (a 5-25 px ring): dL*, dC*
  CLUSTERING  the pair correlation g(r) of the heather mask at 0.25 / 0.5 / 1 / 2 screen-m
              (FFT autocorrelation, frame-edge corrected): g >> 1 across 0.5-1.5 m is heather
              in PATCHES, g ~ 1 an even scatter -- and the in-patch share: heather pixels in
              1-screen-m quadrats that are over 30% heather

Masks, as barrow_paint_compare.py: painting heather = shrub class & rust (a* > 5, b* > 13);
render heather = heather's ID in the OCCLUDED ID frame (the pixels the eye can see).
Distances are SCREEN metres (140.86 px/m at the painting's framing) -- both images share one
projection, so the comparison is like for like; ground distances up-screen are x1.25 these.

THE INSTRUMENT IS CHECKED FIRST on cases whose answer is known: an even scatter of discs and
the same discs gathered into patches must separate on g(r) and in-patch share, and the
painting's heather flattened to its own mean colour must lose its texture and tone spread.

  python3 barrow_heather_stats.py --painting P.png --classes C.png \
      [--render NAME=CAPDIR ...] [--play NAME=CAPDIR ...] --out OUT.json

  --render  the painting's framing (barrow_painting_frame.png + barrow_painting_ids_occl.png)
  --play    the PLAY camera's framing (look_play.png + look_play_ids_occl.png, or the capture's
            barrow_stack_on.png + barrow_play_ids_occl.png), at 100.6 px per screen metre --
            where the fill outside the painting is seen; there is no painting there, so its
            clustering is reported beside the painting's, in the same screen metres
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

K = 140.86                      # px per screen metre at the painting's framing
K_PLAY = 100.617553710938       # ... and at the play camera (zoom 1.0)
RADII_M = [0.25, 0.5, 1.0, 2.0]
EDGE_T = [3.0, 6.0]             # L* per pixel


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def pair_correlation(mask, roi, k=K):
    """g(r) of `mask` inside `roi`, radially averaged, edge-corrected by the ROI's own
    autocorrelation: g = (M*M)(d) / ((R*R)(d) rho^2)."""
    h, w = mask.shape
    H, W = 2 * h, 2 * w
    M = np.zeros((H, W)); M[:h, :w] = mask
    R = np.zeros((H, W)); R[:h, :w] = roi
    fm = np.fft.rfft2(M); fr = np.fft.rfft2(R)
    acm = np.fft.irfft2(fm * np.conj(fm), s=(H, W))
    acr = np.fft.irfft2(fr * np.conj(fr), s=(H, W))
    rho = mask.sum() / max(roi.sum(), 1)
    yy = np.fft.fftfreq(H) * H
    xx = np.fft.fftfreq(W) * W
    dist = np.hypot(yy[:, None], xx[None, :])
    out = {}
    for rm in RADII_M:
        r = rm * k
        ring = (dist >= r * 0.93) & (dist <= r * 1.07)
        num = acm[ring].sum()
        den = acr[ring].sum() * rho * rho
        out[f"{rm}"] = round(float(num / den), 3) if den > 0 else None
    return out


def in_patch_share(mask, q=int(round(K)), thr=0.3):
    q = int(q)
    h, w = mask.shape
    tot = mask.sum()
    if tot == 0:
        return None
    inp = 0
    for y in range(0, h - q + 1, q):
        for x in range(0, w - q + 1, q):
            blk = mask[y:y + q, x:x + q]
            if blk.mean() > thr:
                inp += blk.sum()
    return round(float(inp) / float(tot), 4)


def stats(rgb, heather, objects, ice, anchors=None, k=K):
    L = srgb_to_lab(rgb.astype(np.float64) / 255.0)
    l, a, b = L[..., 0], L[..., 1], L[..., 2]
    c = np.hypot(a, b)
    mu = ndimage.uniform_filter(l, 7)
    var = np.maximum(ndimage.uniform_filter(l * l, 7) - mu * mu, 0.0)
    lstd = np.sqrt(var)
    gx = ndimage.sobel(l, axis=1) / 8.0
    gy = ndimage.sobel(l, axis=0) / 8.0
    gm = np.hypot(gx, gy)
    hv = heather
    n = int(hv.sum())
    if n < 50:
        return {"heather_px": n, "_": "too few heather pixels"}
    # TEXTURE IS READ IN THE INTERIOR: a 7 px window at a region's rim is half snow, and the
    # std of THAT is the rim, not the heather. 3 px in from every edge, on both images.
    core = ndimage.binary_erosion(hv, iterations=3)
    if core.sum() < 50:
        core = hv
    ring = ndimage.binary_dilation(hv, iterations=25) & ~ndimage.binary_dilation(hv, iterations=5)
    snow = ring & ~objects & ~ice
    pct = lambda v: [round(float(x), 2) for x in np.percentile(v, [10, 50, 90])]
    out = {
        "heather_px": n,
        "texture_interior": {
            "px": int(core.sum()),
            "local_std_L_median": round(float(np.median(lstd[core])), 2),
            "grad_L_mean": round(float(gm[core].mean()), 2),
            **{f"edge_density_T{t:g}": round(float((gm[core] > t).mean()), 4) for t in EDGE_T},
        },
        "tone": {"L_p10_p50_p90": pct(l[hv]), "C_p10_p50_p90": pct(c[hv]),
                 "L_spread_p90_minus_p10": round(float(np.percentile(l[hv], 90) - np.percentile(l[hv], 10)), 2)},
        "contrast_vs_adjacent_snow": None,
        "clustering": {"g_r_screen_m": pair_correlation(hv.astype(np.float64), (~ice).astype(np.float64), k),
                       "in_patch_share_1m_q_gt30pct": in_patch_share(hv, int(round(k)))},
    }
    # WHERE IT GROWS: the painting's heather gathers at edges -- stone bases, outcrops, the
    # mound's rocks. Distance from each heather pixel to the nearest stone / rock / tree pixel,
    # in screen metres; an even scatter over open snow sits far from all of them.
    if anchors is not None and anchors.any():
        dist = ndimage.distance_transform_edt(~anchors) / k
        # heather more than 1 screen-m from any stone, rock or tree: the "open snow" share
        out["clustering"]["share_over_1m_from_anchor"] = round(float((dist[hv] > 1.0).mean()), 4)
        out["clustering"]["dist_to_stone_rock_tree_m_p25_p50_p75"] = [
            round(float(v), 3) for v in np.percentile(dist[hv], [25, 50, 75])]
    g = out["clustering"]["g_r_screen_m"]
    vals = [g[k] for k in ("0.5", "1.0") if g.get(k) is not None]
    out["clustering"]["cluster_index_mean_g_0.5_1m"] = round(float(np.mean(vals)), 3) if vals else None
    if snow.sum() > 50:
        out["contrast_vs_adjacent_snow"] = {
            "snow_ring_px": int(snow.sum()),
            "heather_L_C": [round(float(l[hv].mean()), 2), round(float(c[hv].mean()), 2)],
            "snow_L_C": [round(float(l[snow].mean()), 2), round(float(c[snow].mean()), 2)],
            "dL": round(float(l[hv].mean() - l[snow].mean()), 2),
            "dC": round(float(c[hv].mean() - c[snow].mean()), 2)}
    return out


def painting_masks(prgb, pcls):
    """The painting's heather as a REGION, not as its rust pixels: a painted tuft is rust
    strokes with dark sprigs and snow crumbs between them, and the rust-pixel mask alone is a
    lace -- its texture is its own boundary and its clustering is its own strokes. The region
    is the shrub-class pixels within 2 px of a rust one, closed by 3 px; the render's heather
    is solid geometry and needs no such step. (Mean colour stays on the rust pixels, in
    barrow_paint_compare.py: that question is "what hue", this one is "what it looks like".)"""
    L = srgb_to_lab(prgb.astype(np.float64) / 255.0)
    rust = (L[..., 1] > 5) & (L[..., 2] > 13)
    shrub = pcls == 3
    reg = shrub & ndimage.binary_dilation(shrub & rust, iterations=2)
    reg = ndimage.binary_closing(reg, iterations=3) & shrub
    objects = pcls != 0
    ice = (L[..., 2] < -6) & (pcls == 0)
    anchors = (pcls == 1) | (pcls == 2) | (pcls == 4)
    return reg, objects, ice, anchors


def render_masks(beauty, ids_occl):
    a = ids_occl.astype(np.int32)
    heather = (np.abs(a[..., 0] - 255) < 40) & (a[..., 1] < 60) & (np.abs(a[..., 2] - 255) < 40)
    objects = a.sum(-1) > 60
    L = srgb_to_lab(beauty.astype(np.float64) / 255.0)
    ice = (L[..., 2] < -6) & ~objects
    # stone red, rock green, tree yellow -- barrow_world.ID_COLOURS
    red = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] < 60)
    green = (a[..., 0] < 60) & (a[..., 1] > 200) & (a[..., 2] < 60)
    yellow = (a[..., 0] > 200) & (a[..., 1] > 200) & (a[..., 2] < 60)
    heather = ndimage.binary_closing(heather, iterations=1)
    return heather, objects, ice, (red | green | yellow)


def discs(shape, centres, r):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.zeros(shape, bool)
    for (cx, cy) in centres:
        x0, x1 = max(int(cx - r - 1), 0), min(int(cx + r + 2), w)
        y0, y1 = max(int(cy - r - 1), 0), min(int(cy + r + 2), h)
        m[y0:y1, x0:x1] |= (xx[y0:y1, x0:x1] - cx) ** 2 + (yy[y0:y1, x0:x1] - cy) ** 2 <= r * r
    return m


def known_cases(shape, n_px, ice):
    """The instrument on answers known in advance."""
    rng = np.random.default_rng(7)
    r = 0.15 * K                                     # a 0.3 m clump
    n = int(n_px / (np.pi * r * r))
    h, w = shape
    # even scatter: a jittered grid over the non-ice frame
    ok = np.argwhere(~ice)
    step = np.sqrt(ok.shape[0] / n)
    cen = []
    for y in np.arange(step / 2, h, step):
        for x in np.arange(step / 2, w, step):
            jx, jy = x + rng.uniform(-step * 0.3, step * 0.3), y + rng.uniform(-step * 0.3, step * 0.3)
            if 0 <= int(jy) < h and 0 <= int(jx) < w and not ice[int(jy), int(jx)]:
                cen.append((jx, jy))
    even = discs(shape, cen[:n], r)
    # the same number of discs gathered into 14 patches of 0.7 screen-m radius
    pc = ok[rng.choice(ok.shape[0], 14, replace=False)][:, ::-1]
    cen2 = []
    while len(cen2) < n:
        p = pc[rng.integers(14)]
        ang, rad = rng.uniform(0, 2 * np.pi), 0.7 * K * np.sqrt(rng.uniform())
        cen2.append((p[0] + np.cos(ang) * rad, p[1] + np.sin(ang) * rad))
    patchy = discs(shape, cen2, r)
    roi = (~ice).astype(np.float64)
    res = {}
    for nm, m in (("even_scatter", even), ("same_discs_in_patches", patchy)):
        g = pair_correlation((m & ~ice).astype(np.float64), roi)
        res[nm] = {"px": int(m.sum()), "g_r_screen_m": g,
                   "cluster_index_mean_g_0.5_1m": round((g["0.5"] + g["1.0"]) / 2, 3),
                   "in_patch_share_1m_q_gt30pct": in_patch_share(m)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--painting", required=True)
    ap.add_argument("--classes", required=True)
    ap.add_argument("--render", action="append", default=[], help="NAME=CAPDIR")
    ap.add_argument("--play", action="append", default=[], help="NAME=CAPDIR")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    prgb = np.asarray(Image.open(args.painting).convert("RGB"))
    pcls = np.asarray(Image.open(args.classes))
    ph, pobj, pice, panc = painting_masks(prgb, pcls)
    rep = {"_defn": __doc__.split("Masks,")[0].strip().splitlines()[-12:]}
    # ---- the instrument on known cases ----
    rep["instrument_check"] = {"clustering": known_cases(ph.shape, int(ph.sum()), pice)}
    flat = prgb.copy()
    flat[ph] = prgb[ph].reshape(-1, 3).mean(0).astype(np.uint8)
    rep["instrument_check"]["painting_heather_flattened_to_its_mean"] = {
        k: v for k, v in stats(flat, ph, pobj, pice).items() if k in ("texture_interior", "tone")}
    rep["instrument_check"]["_expect"] = ("patches g(0.5-1 m) well above the even scatter's ~1 and a far "
                                          "higher in-patch share; the flattened heather's texture and tone "
                                          "spread near zero against the painting's own")
    rep["painting"] = stats(prgb, ph, pobj, pice, panc)
    for spec in args.render:
        nm, d = spec.split("=", 1)
        d = pathlib.Path(d)
        beauty = np.asarray(Image.open(d / "barrow_painting_frame.png").convert("RGB"))
        ids = np.asarray(Image.open(d / "barrow_painting_ids_occl.png").convert("RGB"))
        rh, robj, rice, ranc = render_masks(beauty, ids)
        rep[nm] = stats(beauty, rh, robj, rice, ranc)
    for spec in args.play:
        nm, d = spec.split("=", 1)
        d = pathlib.Path(d)
        pairs = [("look_play.png", "look_play_ids_occl.png"), ("barrow_stack_on.png", "barrow_play_ids_occl.png")]
        for bn, iname in pairs:
            if (d / bn).exists() and (d / iname).exists():
                beauty = np.asarray(Image.open(d / bn).convert("RGB"))
                ids = np.asarray(Image.open(d / iname).convert("RGB"))
                rh, robj, rice, ranc = render_masks(beauty, ids)
                rep["play:" + nm] = stats(beauty, rh, robj, rice, ranc, K_PLAY)
                break
    pathlib.Path(args.out).write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep["instrument_check"], indent=None))
    for k in rep:
        if k in ("_defn", "instrument_check"):
            continue
        print(k, json.dumps(rep[k]))


if __name__ == "__main__":
    main()
