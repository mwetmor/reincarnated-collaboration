#!/usr/bin/env python3
"""GAL-CAM: LOOK FIRST. Render a frame at full res with the head mask and the
detected blob centroids drawn on it, plus optional model ellipses.

No fitting here. This exists so that a fit is never trusted before the picture
that produced it has been looked at.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def cold_mask(a, bmin=150, brmin=60, gtol=12):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (B > bmin) & ((B - R) > brmin) & (B >= G - gtol)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--minpx", type=int, default=10)
    ap.add_argument("--cx", type=float, default=1024.7)
    ap.add_argument("--cy", type=float, default=568.5)
    ap.add_argument("--ks", type=float, nargs="*", default=[0.40, 0.55, 0.72])
    ap.add_argument("--s", type=float, default=62.8)
    ap.add_argument("--t0", type=float, default=309085.0)
    ap.add_argument("--mask", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0)
    args = ap.parse_args()

    cols = [(255, 60, 60), (255, 200, 0), (0, 255, 255), (255, 0, 255)]
    tiles = []
    for f in args.frames:
        a = np.asarray(Image.open(os.path.join(FRAMES, f"f{f:06d}.png")).convert("RGB"))
        ai = a.astype(np.int16)
        cm = cold_mask(ai)
        head = cm & (ai[:, :, 2] > args.bright)
        head[:30] = False
        head[940:] = False
        base = a.copy()
        if args.mask:
            base = (base * 0.35).astype(np.uint8)
            base[head] = (255, 255, 255)
        im = Image.fromarray(base)
        d = ImageDraw.Draw(im)
        lab, n = ndimage.label(head)
        if n:
            sizes = ndimage.sum(head, lab, range(1, n + 1))
            coms = ndimage.center_of_mass(head, lab, range(1, n + 1))
            for i in range(n):
                if sizes[i] >= args.minpx:
                    y, x = coms[i]
                    r = 3 + min(9, sizes[i] ** 0.5)
                    d.ellipse([x - r, y - r, x + r, y + r], outline=(0, 255, 0), width=2)
        R = 14.0 * (f - args.t0) / 60.0
        aa = args.s * R
        for j, k in enumerate(args.ks):
            bb = aa * k
            d.ellipse([args.cx - aa, args.cy - bb, args.cx + aa, args.cy + bb],
                      outline=cols[j % len(cols)], width=2)
        d.line([args.cx - 12, args.cy, args.cx + 12, args.cy], fill=(255, 255, 0), width=2)
        d.line([args.cx, args.cy - 12, args.cx, args.cy + 12], fill=(255, 255, 0), width=2)
        d.text((12, 12), f"f{f}  R={R:.2f} m  a={aa:.0f}px  k="
               + "/".join(f"{k:.2f}" for k in args.ks), fill=(255, 255, 255))
        tiles.append(im)
    W, H = tiles[0].size
    sc = args.scale
    tw, th = int(W * sc), int(H * sc)
    ncol = 1 if len(tiles) == 1 else 2
    nrow = (len(tiles) + ncol - 1) // ncol
    sheet = Image.new("RGB", (tw * ncol, th * nrow), (0, 0, 0))
    for i, im in enumerate(tiles):
        sheet.paste(im.resize((tw, th), Image.LANCZOS), ((i % ncol) * tw, (i // ncol) * th))
    sheet.save(args.out, quality=92)
    print("wrote", args.out, sheet.size)


if __name__ == "__main__":
    main()
