#!/usr/bin/env python3
"""C-9 T10: the object list -- every instance, its class, its size in metres, its place.

    python3 23_objects.py --variant a

SIZES COME FROM SCREEN PIXELS, NOT FROM DEPTH, and that is the whole reason this part is
trustworthy while the terrain is provisional. Under this orthographic camera a vertical
object of height h occupies exactly h*cos(pitch)*K screen pixels, and K is fixed by the
barbarian, who is in the painting at a known 1.85 m for this purpose. No depth model is
consulted: a standing stone's height is a ruler reading, and the 1.71x disagreement between
the two depth calibrations does not touch it.

WHAT IS AND IS NOT MEASURABLE:
  height   yes, for anything standing upright, to the accuracy of its mask
  width    yes, across the screen, 1:1 with metres
  depth    NO -- an object's extent along the view direction is exactly what an
           orthographic view cannot see, and it is left out rather than invented. The
           four-view sheets exist to supply it.
  yaw      only where an object has a readable long axis in PLAN (the lintel, a fallen
           trunk). A standing stone's yaw is not in the picture, and is reported as null
           rather than as a number nobody measured.

CLASSES come from the prompted masks where those worked (figure, standing stones, the
barrow door, ice -- verified by eye against the overlay) and from colour and shape where
they did not: evf-sam returned one birch out of several, one juniper, the wrong thing for
"rock", the open snow for "path" and the FIGURE for "raven". A prompted segmenter is
reliable for big distinctive things and unreliable for small repeated ones, so the small
repeated ones are classified here instead.
"""
from __future__ import annotations

import argparse
import glob
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent / "artifacts" / "T10C-barrow"
WORK = HERE / "work"
OUT = HERE / "out"

RIGHT = np.array([0.681998491287231, 0.0, -0.731353580951691])
UP = np.array([-0.583728015422821, 0.60246217250824, -0.54433536529541])
FWD = np.array([-0.440612882375717, -0.798147439956665, -0.410878270864487])
SIN_P, COS_P = 0.798147439956665, 0.602462172508240


def srgb_to_lab(rgb):
    c = rgb.astype(np.float32) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]], np.float32)
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883], np.float32)
    e, k = 216.0 / 24389.0, 24389.0 / 27.0
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16.0) / 116.0)
    return np.stack([116.0 * f[..., 1] - 16.0, 500.0 * (f[..., 0] - f[..., 1]),
                     200.0 * (f[..., 1] - f[..., 2])], -1)


def ground_xz(px: float, py: float, K: float, W: int, H: int, hf, meta) -> tuple:
    """Where a screen pixel's GROUND CONTACT lands in world x/z.

    The object's base is on the terrain, so its height is not free: iterate screen -> world
    assuming h, read the heightfield there, and repeat. Three passes is plenty at this
    scale -- the correction is h*tan(pitch) horizontally and the terrain moves by
    centimetres between iterations after the first."""
    u = (px - W / 2.0) / K
    v = -(py - H / 2.0) / K
    h = 0.0
    x = z = 0.0
    for _ in range(4):
        D = (COS_P * v - h) / SIN_P
        x = RIGHT[0] * u + UP[0] * v + FWD[0] * D
        z = RIGHT[2] * u + UP[2] * v + FWD[2] * D
        if hf is None:
            break
        gx = int(round((x - meta["x0"]) / meta["g"]))
        gz = int(round((z - meta["z0"]) / meta["g"]))
        if 0 <= gz < hf.shape[0] and 0 <= gx < hf.shape[1]:
            h = float(hf[gz, gx])
        else:
            break
    return float(x), float(z), float(h)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="a")
    ap.add_argument("--min-px", type=int, default=400)
    a = ap.parse_args()
    v = a.variant

    rgb = np.asarray(Image.open(ART / ("T10C-barrow_%s.png" % v)).convert("RGB"))
    H, W = rgb.shape[:2]
    lab = srgb_to_lab(rgb)

    hj = OUT / ("height_%s_marigold.json" % v)
    hf = meta = None
    if hj.exists():
        j = json.loads(hj.read_text())
        K = j["figure"]["px_per_metre"]
        img = np.asarray(Image.open(OUT / ("height_%s_marigold.png" % v))).astype(np.float32)
        lo, hi = j["png"]["height_min_m"], j["png"]["height_max_m"]
        hf = lo + img / 65535.0 * (hi - lo)
        meta = {"g": j["png"]["metres_per_pixel"], "x0": 0.0, "z0": 0.0}
    else:
        raise SystemExit("run 21_heightfield.py first (need the scale bar)")

    prompted = {}
    for nm in ("figure", "standing_stones", "barrow_door", "ice", "trees", "juniper"):
        p = WORK / ("evf_%s_%s.png" % (v, nm))
        if p.exists():
            prompted[nm] = np.asarray(Image.open(p).convert("L")) > 127

    objs = []
    for f in sorted(glob.glob(str(WORK / ("sam2_%s_[0-9]*.png" % v)))):
        m = np.asarray(Image.open(f).convert("L")) > 127
        if m.sum() < a.min_px:
            continue
        lab_i, n = ndimage.label(m)
        if n > 1:
            sz = ndimage.sum(m, lab_i, range(1, n + 1))
            m = lab_i == (1 + int(np.argmax(sz)))
        ys, xs = np.nonzero(m)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        if bh > 0.9 * H or bw > 0.9 * W:          # background slabs, not objects
            continue
        # the base: the mask's lowest 3% of rows, their horizontal centre
        base_rows = ys >= (y1 - max(2, int(bh * 0.03)))
        bx, by = float(xs[base_rows].mean()), float(ys[base_rows].mean())
        wx, wz, wh = ground_xz(bx, by, K, W, H, hf, meta)

        L = float(lab[..., 0][m].mean())
        A = float(lab[..., 1][m].mean())
        B = float(lab[..., 2][m].mean())
        chroma = float(np.hypot(A, B))
        fill = float(m.sum()) / (bw * bh)
        aspect = bh / max(bw, 1)

        share = {k: float((m & p).sum()) / m.sum() for k, p in prompted.items()}
        cls = None
        for k in ("figure", "barrow_door", "standing_stones", "ice"):
            if share.get(k, 0) > 0.45:
                cls = k
                break
        if cls is None:
            if fill < 0.30 and L < 78:
                cls = "birch" if (chroma < 16 and aspect > 1.1) else "juniper"
            elif B > 9 and chroma > 13:
                cls = "heather"
            elif aspect > 1.45 and L > 60:
                cls = "standing_stones"
            else:
                cls = "rock_outcrop"

        objs.append({
            "mask": pathlib.Path(f).name, "class": cls,
            "screen_bbox": [x0, y0, x1, y1], "area_px": int(m.sum()),
            "height_m": round(bh / (K * COS_P), 2),
            "width_m": round(bw / K, 2),
            "world_xz": [round(wx, 2), round(wz, 2)], "ground_h_m": round(wh, 2),
            "fill": round(fill, 2), "aspect": round(aspect, 2),
            "Lab": [round(L, 1), round(A, 1), round(B, 1)],
            "prompted_share": {k: round(s, 2) for k, s in share.items() if s > 0.15},
            "yaw_deg": None,
        })

    # the lintel is the one object with a readable plan axis: it lies across the posts
    for o in objs:
        if o["class"] == "barrow_door" and o["width_m"] > 1.5 * o["height_m"]:
            o["yaw_deg"] = round(float(np.degrees(np.arctan2(FWD[2], FWD[0]))) + 90.0, 1)
            o["yaw_note"] = "long axis across the screen; perpendicular to the camera azimuth"

    by_class = {}
    for o in objs:
        by_class.setdefault(o["class"], []).append(o)
    summary = {}
    for k, v2 in sorted(by_class.items()):
        hs = [o["height_m"] for o in v2]
        summary[k] = {"n": len(v2), "height_m": {"min": min(hs), "median": round(float(np.median(hs)), 2),
                                                 "max": max(hs)}}
    rep = {"variant": v, "px_per_metre": K, "n_objects": len(objs),
           "by_class": summary, "objects": objs}
    (OUT / ("objects_%s.json" % v)).write_text(json.dumps(rep, indent=1) + "\n")
    print("%-18s %3s  %-28s" % ("class", "n", "height m  min / median / max"))
    for k, s in summary.items():
        print("%-18s %3d  %5.2f / %5.2f / %5.2f"
              % (k, s["n"], s["height_m"]["min"], s["height_m"]["median"], s["height_m"]["max"]))
    print("-> %s" % (OUT / ("objects_%s.json" % v)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
