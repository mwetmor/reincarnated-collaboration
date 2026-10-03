#!/usr/bin/env python3
"""C-9 R-C9-139: the character's lit-body luminance from tools/probe_charlight.gd's beauty + mask crops.

Luma = Rec.709 Y' on the 8-bit sRGB pixels (0.2126 R + 0.7152 G + 0.0722 B), the same luma the run's earlier
captures report. Character pixels = the MASK frame's magenta (R > 200, G < 60, B > 200), ERODED by 2 px so the
silhouette's outline (pen / hull ink, and anti-aliased edge blending with the painting) is not counted as body.
Per heading and pooled over the four: mean, p10, p50, p90, n.

  python3 charlight_stats.py DIR tag who [tag who ...] [--json out.json]
"""
import json, sys, os
import numpy as np
from PIL import Image

HEADINGS = ["S", "E", "N", "W"]


def mask_of(path):
    m = np.asarray(Image.open(path).convert("RGB")).astype(int)
    k = (m[..., 0] > 200) & (m[..., 1] < 60) & (m[..., 2] > 200)
    for _ in range(2):  # 4-neighbour erosion
        k = k & np.roll(k, 1, 0) & np.roll(k, -1, 0) & np.roll(k, 1, 1) & np.roll(k, -1, 1)
    return k


def dilate(k, n):
    for _ in range(n):
        k = k | np.roll(k, 1, 0) | np.roll(k, -1, 0) | np.roll(k, 1, 1) | np.roll(k, -1, 1)
    return k


def raw_mask(path):
    m = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return (m[..., 0] > 200) & (m[..., 1] < 60) & (m[..., 2] > 200)


def luma(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2], a


def stats(vals):
    return {"mean": round(float(vals.mean()), 1), "p10": round(float(np.percentile(vals, 10)), 1),
            "p50": round(float(np.percentile(vals, 50)), 1), "p90": round(float(np.percentile(vals, 90)), 1),
            "n": int(vals.size)}


def run(d, tag, who):
    out = {"headings": {}}
    pool, rgb, bgs = [], [], []
    for h in HEADINGS:
        b = os.path.join(d, "%s_%s_h%s" % (tag, who, h))
        if not os.path.exists(b + "_beauty.png"):
            continue
        k = mask_of(b + "_mask.png")
        y, a = luma(b + "_beauty.png")
        v = y[k]
        out["headings"][h] = stats(v)
        rk = raw_mask(b + "_mask.png")
        ring = dilate(rk, 60) & ~dilate(rk, 20)        # the ground around her, 20-60 px out (her shadow mostly inside 20)
        bgs.append(y[ring])
        pool.append(v)
        rgb.append(a[k])
    v = np.concatenate(pool)
    out["pooled"] = stats(v)
    c = np.concatenate(rgb)
    out["pooled"]["mean_rgb"] = [round(float(x), 1) for x in c.mean(0)]
    bg = np.concatenate(bgs)
    out["pooled"]["surround_median"] = round(float(np.median(bg)), 1)
    out["pooled"]["ratio_to_surround"] = round(float(v.mean() / np.median(bg)), 3)
    out["pooled"]["spread_p90_p10"] = round(float(np.percentile(v, 90) - np.percentile(v, 10)), 1)
    hsv = np.asarray(Image.fromarray(c.astype(np.uint8).reshape(-1, 1, 3)).convert("HSV")).reshape(-1, 3).astype(float)
    out["pooled"]["mean_sat"] = round(float(hsv[:, 1].mean()), 1)
    return out


def main():
    a = sys.argv[1:]
    js = None
    if "--json" in a:
        js = a[a.index("--json") + 1]
        a = a[:a.index("--json")]
    d = a[0]
    res = {}
    for i in range(1, len(a), 2):
        tag, who = a[i], a[i + 1]
        r = run(d, tag, who)
        res["%s/%s" % (tag, who)] = r
        p = r["pooled"]
        print("%-6s %-10s mean %6.1f  p10 %6.1f  p50 %6.1f  p90 %6.1f  spread %5.1f  surround %6.1f  ratio %.3f  sat %5.1f  rgb %s" % (
            tag, who, p["mean"], p["p10"], p["p50"], p["p90"], p["spread_p90_p10"], p["surround_median"], p["ratio_to_surround"], p["mean_sat"], p["mean_rgb"]))
    if js:
        json.dump(res, open(js, "w"), indent=1)


if __name__ == "__main__":
    main()
