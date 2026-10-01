#!/usr/bin/env python3
"""C-9 CRATER v4 (R-C9-109), layer 2 -- THE PAINT-OVER PROJECTED BACK ONTO THE CRATER MESH, as the Barrow's
chunks were (camera projection into the mesh's UVs). drax.

  python3 tools/crater_project.py --heights crater_S_heights.npz --project DIR/project.json \
      --paint painted.png [--mask mask.png] --out OUT_PREFIX [--size 1024]

project.json (godot/tools/crater_guide.gd) holds the screen pixel, in the 1536 x 1024 crop, of every vertex of the
crater's grid at the game camera. Each UV texel is a point of that grid (planar UVs: u = +x, the image's rows from
+y down); its screen pixel is the grid's, interpolated; the painting is sampled there (bilinear). The texel's alpha is
the mesh's skirt (vertex alpha), so the crater feathers into the ground with no edge. The camera is orthographic and
the bowl shallow (its walls rise at most ~25 deg against a 53 deg view), so no texel hides another.
Writes OUT_PREFIX_albedo.png (RGBA) and, with --mask, OUT_PREFIX_emit.png (L).
"""
import argparse
import json

import numpy as np
from PIL import Image


def bilinear(img, x, y):
    h, w = img.shape[:2]
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    if img.ndim == 2:
        img = img[..., None]
    a = img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx
    b = img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--heights", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--paint", required=True)
    ap.add_argument("--mask")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=1024)
    o = ap.parse_args()
    H = np.load(o.heights)
    P = json.load(open(o.project))
    n = int(P["n"])
    px = np.array(P["px"], dtype=np.float64).reshape(n, n, 2)       # [j, i] -> screen (x, y) in the crop
    S = o.size
    cols = np.arange(S) / (S - 1) * (n - 1)
    rows = (1.0 - np.arange(S) / (S - 1)) * (n - 1)
    I, J = np.meshgrid(cols, rows, indexing="xy")
    sp = bilinear(px.transpose(0, 1, 2), I, J)                        # screen px per texel
    paint = np.asarray(Image.open(o.paint).convert("RGB"), dtype=np.float64)
    rgb = bilinear(paint, sp[..., 0], sp[..., 1])
    alpha = bilinear(H["alpha"].astype(np.float64), I, J)[..., 0]
    out = np.dstack([np.clip(rgb, 0, 255), np.clip(alpha * 255, 0, 255)]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(o.out + "_albedo.png")
    rep = {"albedo": o.out + "_albedo.png", "size": S, "screen_px_range": [float(sp[..., 0].min()), float(sp[..., 0].max()),
                                                                           float(sp[..., 1].min()), float(sp[..., 1].max())]}
    if o.mask:
        m = np.asarray(Image.open(o.mask).convert("L"), dtype=np.float64)
        e = bilinear(m, sp[..., 0], sp[..., 1])[..., 0] * alpha
        Image.fromarray(np.clip(e, 0, 255).astype(np.uint8), "L").save(o.out + "_emit.png")
        rep["emit"] = o.out + "_emit.png"
    print(json.dumps(rep))


if __name__ == "__main__":
    main()
