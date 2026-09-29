#!/usr/bin/env python3
"""T7-B: does the generated world still read as OUR painted register?

"Looks like our painting" is a judgement, but its colour half is measurable. This
takes an 8-colour k-means palette of each image in CIE Lab and reports the mean
nearest-neighbour dE76 from the generated palette to the source palette, weighted by
cluster mass.

A CONTROL matters here, because dE on its own has no scale: two sunset landscapes
will always be closer than a sunset and a kitchen. So the same measure is run against
control images and reported alongside. Low dE vs the source AND clearly lower than the
controls is the only reading that means anything.
"""
import argparse
import json

import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans2

Image.MAX_IMAGE_PIXELS = None


def srgb_to_lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16.0 / 116.0)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]),
                     200 * (f[:, 1] - f[:, 2])], 1)


def palette(path, k=8, n=60000, seed=0):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).reshape(-1, 3).astype(np.float64)
    rng = np.random.default_rng(seed)
    a = a[rng.choice(len(a), min(n, len(a)), replace=False)]
    lab = srgb_to_lab(a)
    ctr, lbl = kmeans2(lab, k, minit="++", seed=seed)
    w = np.bincount(lbl, minlength=k).astype(float)
    return ctr, w / w.sum()


def delta(src, gen, k=8):
    cs, ws = palette(src, k)
    cg, wg = palette(gen, k)
    d = np.linalg.norm(cg[:, None, :] - cs[None, :, :], axis=2)
    return float((d.min(axis=1) * wg).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--generated", required=True, nargs="+")
    ap.add_argument("--control", nargs="*", default=[])
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    rep = {"source": a.source,
           "generated_dE76": {g: round(delta(a.source, g), 2) for g in a.generated},
           "control_dE76": {c: round(delta(a.source, c), 2) for c in a.control},
           "note": "mass-weighted mean nearest-neighbour dE76, 8-colour Lab k-means "
                   "palette, generated -> source. Lower is closer to our register."}
    print(json.dumps(rep, indent=1))
    if a.out:
        open(a.out, "w").write(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
