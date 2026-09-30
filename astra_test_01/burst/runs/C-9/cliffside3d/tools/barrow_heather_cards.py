#!/usr/bin/env python3
"""C-9 T10-1d -- THE PAINTING'S OWN HEATHER TUFTS, CUT OUT AS ALPHA CARDS.

    python3 barrow_heather_cards.py --classes paint_classes.png --out-png ATLAS.png --out-json CARDS.json

One of the two heather representations T10-1d chooses between by measurement (the other is the
generated stems in scripts/barrow_heather.gd). A card here is not painted to look like the
painting's heather: it IS the painting's heather -- an isolated tuft cut out of
T10C-barrow_a.png, its snow keyed to alpha, at the painting's own scale (140.86 px/m).

WHICH TUFTS. The heather region is the painting's shrub class within 2 px of a rust pixel
(the same region tools/barrow_heather_stats.py measures), closed by 2 px. A component is a card
when it is one tuft and stands alone: 250-5000 px, no wider than 1.3 m and no taller than
0.9 m of screen, no taller than it is wide, at least 60% rust, not cut by the frame, at most 0.85 x 0.6 m, and the ring 4-12 px around
it at least 70% open snow -- a tuft against a stone would carry the stone's paint into the card.

ALPHA. Inside the tuft's box: 1 on region pixels, 0 on everything that is snow (bright and
low-chroma, or the blue of snow in shadow) -- the snow between the sprigs is keyed out so the
game's own snow shows through -- and a 1 px feather at the rim.

The atlas is tiles of 128 x 128, each tuft scaled uniformly to fit with its base on the tile's
bottom edge; the JSON records per tile its uv rectangle, its size in screen metres, and where
across the tile its base is.
"""
import argparse
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
ART_DEFAULT = HERE.parent.parent / "artifacts" / "T10C-barrow" / "T10C-barrow_a.png"
K = 140.86
TILE = 128
COLS = 8
# ONE BY HAND, written down so it can be checked: a juniper clump grown into the tuft, which
# the colour rules pass (the tuft is 89% rust) and the eye does not
EXCLUDE_SRC_BOXES = [[473, 462, 524, 505]]


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--painting", default=str(ART_DEFAULT))
    ap.add_argument("--classes", required=True)
    ap.add_argument("--out-png", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--max", type=int, default=24)
    a = ap.parse_args()
    rgb8 = np.asarray(Image.open(a.painting).convert("RGB"))
    rgb = rgb8.astype(np.float64) / 255.0
    cls = np.asarray(Image.open(a.classes))
    L = srgb_to_lab(rgb)
    l, aa, bb = L[..., 0], L[..., 1], L[..., 2]
    c = np.hypot(aa, bb)
    rust = (aa > 5) & (bb > 13)
    shrub = cls == 3
    reg = shrub & ndimage.binary_dilation(shrub & rust, iterations=2)
    reg = ndimage.binary_closing(reg, iterations=2) & shrub
    snow = ((l > 74) & (c < 17)) | ((l > 52) & (bb < -3) & (c < 22))
    lab_r, n = ndimage.label(reg)
    cands = []
    for i, sl in enumerate(ndimage.find_objects(lab_r), start=1):
        if sl is None:
            continue
        m = lab_r[sl] == i
        area = int(m.sum())
        if area < 250 or area > 5000:
            continue
        h_px = sl[0].stop - sl[0].start
        w_px = sl[1].stop - sl[1].start
        # 0.85 m wide at most: the two wider "tufts" are bare birch saplings standing in heather
        if w_px > 0.85 * K or h_px > 0.6 * K or w_px < 18 or h_px < 14:
            continue
        # a component cut by the frame is a fragment -- and at the left edge, a rock's lichen
        if (sl[0].start <= 3 or sl[1].start <= 3 or sl[0].stop >= cls.shape[0] - 3
                or sl[1].stop >= cls.shape[1] - 3):
            continue
        # isolation: the ring round it must be mostly open snow
        y0, y1 = max(sl[0].start - 12, 0), min(sl[0].stop + 12, cls.shape[0])
        x0, x1 = max(sl[1].start - 12, 0), min(sl[1].stop + 12, cls.shape[1])
        big = np.zeros((y1 - y0, x1 - x0), bool)
        big[sl[0].start - y0:sl[0].stop - y0, sl[1].start - x0:sl[1].stop - x0] = m
        ring = ndimage.binary_dilation(big, iterations=12) & ~ndimage.binary_dilation(big, iterations=4)
        if ring.sum() == 0:
            continue
        open_share = float(snow[y0:y1, x0:x1][ring].mean())
        if open_share < 0.70:
            continue
        # HEATHER, not a rock chip or a dead sapling: at least 45% of the tuft rust, and no
        # taller than it is wide (the saplings in the painting are tall thin branch fans)
        rust_share = float(rust[sl][m].mean())
        if rust_share < 0.60 or h_px > 1.1 * w_px:
            continue
        bx = [sl[1].start - 2, sl[0].start - 2, sl[1].stop + 2, sl[0].stop + 2]
        if any(abs(bx[0] - e[0]) <= 3 and abs(bx[1] - e[1]) <= 3 for e in EXCLUDE_SRC_BOXES):
            continue
        cands.append({"i": i, "sl": sl, "area": area, "open": open_share, "w": w_px, "h": h_px,
                      "rust": rust_share})
    # the most isolated, then the biggest -- a varied set of sizes
    cands.sort(key=lambda d: (-round(d["open"], 1), -d["area"]))
    cands = cands[:a.max]
    rows = (len(cands) + COLS - 1) // COLS
    atlas = np.zeros((rows * TILE, COLS * TILE, 4), np.uint8)
    tiles = []
    for t, d in enumerate(cands):
        sl = d["sl"]
        y0, y1 = sl[0].start - 2, sl[0].stop + 2
        x0, x1 = sl[1].start - 2, sl[1].stop + 2
        y0, x0 = max(y0, 0), max(x0, 0)
        y1, x1 = min(y1, cls.shape[0]), min(x1, cls.shape[1])
        m = lab_r[y0:y1, x0:x1] == d["i"]
        alpha = (m & ~snow[y0:y1, x0:x1]).astype(np.float64)
        alpha = np.maximum(alpha, 0.5 * (ndimage.binary_dilation(alpha > 0.5, iterations=1) & ~snow[y0:y1, x0:x1]))
        crop = np.dstack([rgb8[y0:y1, x0:x1], (alpha * 255).astype(np.uint8)])
        hh, ww = crop.shape[:2]
        # never upscaled past 1.5x: a 30 px tuft blown up to a tile is a blur, not a sprig
        s = min((TILE - 2) / ww, (TILE - 2) / hh, 1.5)
        tw, th = max(int(round(ww * s)), 1), max(int(round(hh * s)), 1)
        im = Image.fromarray(crop, "RGBA").resize((tw, th), Image.LANCZOS)
        r, cc = divmod(t, COLS)
        ox = cc * TILE + (TILE - tw) // 2
        oy = r * TILE + (TILE - th)                     # base on the tile's bottom edge
        atlas[oy:oy + th, ox:ox + tw] = np.asarray(im)
        ys, xs = np.nonzero(m)
        base_u = float(xs[ys >= ys.max() - 2].mean()) / float(ww)
        tiles.append({"name": "tuft_%02d" % t, "src_box_px": [int(x0), int(y0), int(x1), int(y1)],
                      "uv": [ox / atlas.shape[1], oy / atlas.shape[0], (ox + tw) / atlas.shape[1], (oy + th) / atlas.shape[0]],
                      "w_m": round(ww / K, 4), "h_m": round(hh / K, 4), "base_u": round(base_u, 3),
                      "ring_open_snow": round(d["open"], 3), "area_px": d["area"],
                      "rust_share": round(d["rust"], 3)})
    Image.fromarray(atlas, "RGBA").save(a.out_png)
    pathlib.Path(a.out_json).write_text(json.dumps({"_what": __doc__.strip().splitlines()[0], "K_px_per_m": K,
                                                    "tile_px": TILE, "candidates": len(cands), "tiles": tiles}, indent=1))
    print(json.dumps({"tiles": len(tiles), "atlas": list(atlas.shape),
                      "w_m": [t["w_m"] for t in tiles], "h_m": [t["h_m"] for t in tiles]}))


if __name__ == "__main__":
    main()
