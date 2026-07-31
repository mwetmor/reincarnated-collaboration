#!/usr/bin/env python3
"""SHADOW-CAL: diagnostic panel for SC-1 -- frame | plate | rho | mask.

Rendered before any number is believed.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageDraw

import sc_shadow as S


def colormap_rho(rho, lo=0.4, hi=1.3):
    t = np.clip((rho - lo) / (hi - lo), 0, 1)
    # blue = dark, grey = 1.0, yellow = bright
    r = np.clip(2 * t, 0, 1)
    g = np.clip(1.4 * t, 0, 1)
    b = np.clip(1.6 - 1.6 * t, 0, 1)
    return (np.stack([r, g, b], -1) * 255).astype(np.uint8)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--idx", type=int, default=None)
    ap.add_argument("--box", type=int, nargs=4, required=True,
                    help="x0 y0 x1 y1 crop in frame coords")
    ap.add_argument("--zoom", type=float, default=2.0)
    a = ap.parse_args()

    paths = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir)
                   if f.endswith((".png", ".jpg")))
    st = S.load(paths)
    plate = S.plate_median(st)
    i = a.idx if a.idx is not None else len(paths) // 2
    r = S.separate(st[i], plate)
    sh, _, _ = S.clean(r["shadow"])
    sp, _, _ = S.clean(r["sprite"], min_px=60)

    x0, y0, x1, y1 = a.box
    sl = (slice(y0, y1), slice(x0, x1))

    tiles = []
    tiles.append(("frame", st[i][sl].astype(np.uint8)))
    tiles.append(("plate (temporal median)", plate[sl].astype(np.uint8)))
    tiles.append(("rho = L_frame / L_plate", colormap_rho(r["rho"])[sl]))
    ov = st[i].copy()
    ov[sh] = ov[sh] * 0.25 + np.array([255, 30, 30]) * 0.75
    ov[sp] = ov[sp] * 0.25 + np.array([30, 150, 255]) * 0.75
    tiles.append(("red = SHADOW   blue = SPRITE", ov[sl].astype(np.uint8)))

    w = x1 - x0
    h = y1 - y0
    z = a.zoom
    tw, th = int(w * z), int(h * z)
    canvas = Image.new("RGB", (2 * tw, 2 * th + 20), (12, 12, 12))
    d = ImageDraw.Draw(canvas)
    for k, (lab, img) in enumerate(tiles):
        rr, cc = divmod(k, 2)
        im = Image.fromarray(img).resize((tw, th), Image.LANCZOS)
        canvas.paste(im, (cc * tw, rr * th + (10 if rr else 0)))
        d.text((cc * tw + 6, rr * th + (12 if rr else 2)), lab,
               fill=(255, 255, 0))
    canvas.save(a.out, quality=92)
    print("->", a.out, "  shadow px", int(sh.sum()), " sprite px", int(sp.sum()))
