#!/usr/bin/env python3
"""P5 -- SEAMS between paint canvases. Negative control (Gate-1 W-1): R-C9-158 (barrow_v2/section_sw), the attempt
whose seams Matt named.

Two measures, both on v1's own grid law (1536 x 1024 canvases on a 1280 x 768 stride; key "c_r" at (1280c, 768r)):
 (a) OVERLAP MAD -- for each neighbouring pair of RAW canvases, mean |a - b| (sRGB 0-255, all channels) over the
     region both canvases cover (256 px wide side by side; 256 px tall above/below). How much two painters' hands
     disagree where the stitch must reconcile them. (plan § 4 P5: v1 recorded 2.7-13.1)
 (b) STITCHED SEAM VISIBILITY -- on the stitched painting, for each overlap band's centre line, the mean squared
     gradient ACROSS the line (|d/dx| for a vertical seam) within +-2 px, divided by the median of the same
     quantity on parallel lines 160-400 px away on both sides (off-seam baseline, same content class).
     A hard or shifted seam spikes it; the score is |log2 ratio| (a ghosting blur that LOWERS gradient also counts).
THRESHOLDS from v1's own 24 seams: (a) <= max of v1's per-pair MAD; (b) <= max of v1's per-seam |log2 ratio|.
PASS = no pair/seam over either bar ("<= v1's distribution"; failures go to seam repair).
CONSTRUCTED FAILURE: (b) v1's stitched painting with the x = 2688 overlap band re-blended from two copies 6 px out
of register (the partition-of-unity stitch's own failure mode: ghosting); (a) one v1 canvas (1_1) replaced by a
6% hue-and-tone-shifted copy (a second hand).
SCOPE NOTE (measured at calibration, recorded in calibration.md): (b) sees GHOSTING (it lowers the across-line
gradient) and a 12 px whole-half shift is invisible to it on v1's smooth snow (score 0.772 vs bar 0.799); a hard,
unblended seam is also invisible (ratio 1.03) -- v1's stitcher cannot produce one; (a) carries those cases.
"""
import argparse
import glob
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, __import__("os").path.dirname(__file__))
from common import *  # noqa

W, H, SX, SY = 1536, 1024, 1280, 768


def canvases(prefix):
    out = {}
    for d in sorted(glob.glob(str(ART / ("%s-*" % prefix)))):
        name = pathlib.Path(d).name
        key = name[len(prefix) + 1:].split("-")[0]
        cand = sorted(glob.glob(d + "/*.png"))
        if not cand:
            continue
        # a retry (-rN) supersedes the base; the stitchers take the highest rN
        r = 0
        if "-r" in name[len(prefix) + 1:]:
            r = int(name.rsplit("-r", 1)[1])
        if key not in out or r > out[key][0]:
            out[key] = (r, cand[0])
    return {k: v[1] for k, v in out.items()}


def overlap_mads(paths, load=None):
    load = load or (lambda p: np.asarray(Image.open(p).convert("RGB"), np.float32))
    keys = set(paths)
    rows = []
    cache = {}

    def get(k):
        if k not in cache:
            cache[k] = load(paths[k])
        return cache[k]
    for k in sorted(keys):
        c, r = map(int, k.split("_"))
        for dc, dr in ((1, 0), (0, 1)):
            n = "%d_%d" % (c + dc, r + dr)
            if n not in keys:
                continue
            a, b = get(k), get(n)
            if dc:
                d = np.abs(a[:, SX:] - b[:, :W - SX])
            else:
                d = np.abs(a[SY:, :] - b[:H - SY, :])
            rows.append({"pair": "%s|%s" % (k, n), "mad": round(float(d.mean()), 2)})
    return rows


def seam_vis(img, cols, rows):
    g = luma(img).astype(np.float64)
    gx = np.diff(g, axis=1) ** 2              # across vertical seams
    gy = np.diff(g, axis=0) ** 2              # across horizontal seams
    out = []
    for c in range(1, cols):
        x = SX * c + (W - SX) // 2
        line = gx[:, x - 2:x + 3].mean()
        offs = [x + s * o for s in (-1, 1) for o in range(160, 401, 20) if 0 <= x + s * o < gx.shape[1]]
        base = np.median([gx[:, o].mean() for o in offs])
        out.append({"seam": "x=%d" % x, "ratio": round(float(line / base), 3), "score": round(abs(float(np.log2(line / base))), 3)})
    for r in range(1, rows):
        y = SY * r + (H - SY) // 2
        line = gy[y - 2:y + 3, :].mean()
        offs = [y + s * o for s in (-1, 1) for o in range(160, 401, 20) if 0 <= y + s * o < gy.shape[0]]
        base = np.median([gy[o, :].mean() for o in offs])
        out.append({"seam": "y=%d" % y, "ratio": round(float(line / base), 3), "score": round(abs(float(np.log2(line / base))), 3)})
    return out


def grid_of(paths):
    cs = [tuple(map(int, k.split("_"))) for k in paths]
    return max(c for c, r in cs) + 1, max(r for c, r in cs) + 1


SRC = {"v1": ("T10BF", BF / "paint/barrow_full_painted.png"),
       "159": ("BV2M", BF / "godot/data/barrow_v2_sw/painted/ground.png"),
       "158": ("BVSW", B2 / "paint/section_sw/section_sw_painted.png")}


def measure(name, stitched_img=None, paths=None, loader=None):
    prefix, stitched = SRC[name] if name in SRC else (None, None)
    paths = paths or canvases(prefix)
    mads = overlap_mads(paths, loader)
    img = stitched_img if stitched_img is not None else load_rgb(stitched)
    cols, rows = img.shape[1] // SX, img.shape[0] // SY
    vis = seam_vis(img, cols, rows)
    return {"overlap_mad": mads, "seam_visibility": vis}


def bars(v1):
    return {"mad_max": max(r["mad"] for r in v1["overlap_mad"]),
            "vis_max": max(r["score"] for r in v1["seam_visibility"])}


def verdict(m, b):
    mm = max(r["mad"] for r in m["overlap_mad"]) if m["overlap_mad"] else 0.0
    vm = max(r["score"] for r in m["seam_visibility"]) if m["seam_visibility"] else 0.0
    n_mad = sum(r["mad"] > b["mad_max"] for r in m["overlap_mad"])
    n_vis = sum(r["score"] > b["vis_max"] for r in m["seam_visibility"])
    return {"value": {"mad_max": round(mm, 2), "vis_max": round(vm, 3)},
            "over_bar": {"mad_pairs": n_mad, "seams": n_vis}, "pass": n_mad == 0 and n_vis == 0,
            "threshold": "overlap MAD <= %.2f and seam |log2 ratio| <= %.3f (v1's own maxima)" % (b["mad_max"], b["vis_max"])}


def constructed():
    v1 = load_rgb(SRC["v1"][1])
    x = 2 * SX + (W - SX) // 2
    shifted = v1.copy()                    # a 6 px MISREGISTERED blend: the band averages the painting with itself
    band = slice(x - (W - SX) // 2, x + (W - SX) // 2)          # shifted 6 px -- the stitch's ghosting failure
    shifted[:, band] = 0.5 * v1[:, band] + 0.5 * np.roll(v1, 6, axis=0)[:, band]
    paths = canvases("T10BF")
    # a second hand on canvas 1_1: hue/tone shifted 6% (luma kept within the painter's range)

    def loader(p):
        a = np.asarray(Image.open(p).convert("RGB"), np.float32)
        if p == paths["1_1"]:
            a = np.clip(a * np.array([1.06, 0.98, 0.92]), 0, 255)
        return a
    return measure("v1", stitched_img=shifted, paths=paths, loader=loader)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.parse_args()
    res = {k: measure(k) for k in SRC}
    res["constructed"] = constructed()
    b = bars(res["v1"])
    out = {"bars_from_v1": b}
    for k, m in res.items():
        v = verdict(m, b)
        out[k] = dict(m, **v)
        print("P5 %-12s overlap MAD max %6.2f (%d pairs over)  seam |log2| max %.3f (%d over)  -> %s" % (
            k, v["value"]["mad_max"], v["over_bar"]["mad_pairs"], v["value"]["vis_max"], v["over_bar"]["seams"],
            "PASS" if v["pass"] else "FAIL"))
    dump(out, str(PH / "results/p5.json"))
