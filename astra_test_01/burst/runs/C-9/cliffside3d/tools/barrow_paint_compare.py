#!/usr/bin/env python3
"""C-9 T10-1b -- THE RENDER AGAINST THE PAINTING, measured.

    python3 barrow_paint_compare.py --cap CAPTURE_DIR --seg SEG_DIR

Inputs: the concept painting, its class map (barrow_paint_dress.py), and two frames from the
capture taken at the painting's OWN framing -- the beauty render and the class-ID render
(every prop in its class colour, unshaded, on black, MSAA off).

Outputs:
  paint_vs_render_side_by_side.png   the painting and the render, side by side
  paint_vs_render_overlay50.png      the render at 50% over the painting
  paint_coverage.json                per class: COVERAGE = the share of the painting's pixels
                                     of that class that a 3D object of THE SAME class covers
                                     in the render, which is the acceptance for "placed as
                                     painted"; plus PRECISION (the share of the render's class
                                     pixels that land on painted pixels of that class) so a
                                     class cannot pass by flooding the frame.

The instrument is checked on a known case first: the painting's class map compared against
ITSELF must give coverage 1.0 and precision 1.0 in every class, and against an all-black
render 0.0 -- or the numbers below are about the comparison code, not the scene.
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent.parent / "artifacts" / "T10C-barrow" / "T10C-barrow_a.png"
NAMES = {1: "stone", 2: "rock", 3: "shrub", 4: "tree"}
# the ID pass's colours (barrow_world.ID_COLOURS): stone red, rock green, shrub blue, tree yellow
ID_RGB = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 255), 4: (255, 255, 0)}


def classify_ids(img):
    """Nearest ID colour, with black as 'nothing' and a distance ceiling so a stray grey pixel
    is not forced into a class."""
    a = img.astype(np.int32)
    out = np.zeros(a.shape[:2], np.uint8)
    best = np.full(a.shape[:2], 1 << 30, np.int64)
    for cid, col in list(ID_RGB.items()) + [(0, (0, 0, 0))]:
        d = ((a - np.array(col)) ** 2).sum(-1)
        m = d < best
        best[m] = d[m]
        out[m] = cid
    out[best > 90 ** 2] = 0
    return out


def coverage(paint, render):
    rows = {}
    for cid, nm in NAMES.items():
        p = paint == cid
        r = render == cid
        both = (p & r).sum()
        rows[nm] = {"painting_px": int(p.sum()), "render_px": int(r.sum()),
                    "coverage": round(float(both) / max(int(p.sum()), 1), 4),
                    "precision": round(float(both) / max(int(r.sum()), 1), 4)}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", required=True)
    ap.add_argument("--seg", required=True)
    a = ap.parse_args()
    cap = pathlib.Path(a.cap)
    seg = pathlib.Path(a.seg)
    paint_rgb = np.asarray(Image.open(ART).convert("RGB"))
    paint_cls = np.asarray(Image.open(seg / "paint_classes.png"))
    beauty = np.asarray(Image.open(cap / "barrow_painting_frame.png").convert("RGB"))
    ids = np.asarray(Image.open(cap / "barrow_painting_ids.png").convert("RGB"))
    if beauty.shape[:2] != paint_rgb.shape[:2] or ids.shape[:2] != paint_rgb.shape[:2]:
        raise SystemExit("frame size mismatch: painting %s, render %s, ids %s"
                         % (paint_rgb.shape, beauty.shape, ids.shape))
    rep = {"_defn": {"coverage": "painted pixels of class C covered by a render pixel of class C / painted pixels of class C",
                     "precision": "render pixels of class C on painted pixels of class C / render pixels of class C"}}
    # the instrument, on known cases
    self_cmp = coverage(paint_cls, paint_cls)
    zero_cmp = coverage(paint_cls, np.zeros_like(paint_cls))
    rep["instrument_check"] = {
        "painting_vs_itself_coverage": {k: v["coverage"] for k, v in self_cmp.items()},
        "painting_vs_black_coverage": {k: v["coverage"] for k, v in zero_cmp.items()},
        "_expect": "1.0 in every class against itself, 0.0 against black"}
    rcls = classify_ids(ids)
    rep["classes"] = coverage(paint_cls, rcls)
    # where the misses are: coverage by image third (top = behind the mound, bottom = foreground)
    H = paint_cls.shape[0]
    bands = {}
    for nm_b, (y0, y1) in {"top": (0, H // 3), "middle": (H // 3, 2 * H // 3), "bottom": (2 * H // 3, H)}.items():
        bands[nm_b] = {k: v["coverage"] for k, v in coverage(paint_cls[y0:y1], rcls[y0:y1]).items()}
    rep["coverage_by_band"] = bands
    Image.fromarray(np.concatenate([paint_rgb, beauty], axis=1)).save(cap / "paint_vs_render_side_by_side.png")
    over = (paint_rgb.astype(np.float32) * 0.5 + beauty.astype(np.float32) * 0.5).astype(np.uint8)
    Image.fromarray(over).save(cap / "paint_vs_render_overlay50.png")
    # the ID comparison as a picture too: painting class vs render class, per pixel
    vis = np.zeros(paint_rgb.shape, np.uint8)
    for cid, col in ID_RGB.items():
        p = paint_cls == cid
        r = rcls == cid
        vis[p & r] = np.array(col) // 1
        vis[p & ~r] = (np.array(col) * 0.35).astype(np.uint8)
    Image.fromarray(vis).save(cap / "paint_coverage_map.png")
    (cap / "paint_coverage.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep["classes"]))
    print(json.dumps(rep["instrument_check"]))


if __name__ == "__main__":
    main()
