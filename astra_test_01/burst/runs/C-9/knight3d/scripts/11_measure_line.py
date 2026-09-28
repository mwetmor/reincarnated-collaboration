#!/usr/bin/env python3
"""C-9 knight3d: MEASURE the stills' ink line weight, so the render-time
outline matches the painter's hand instead of a guessed thickness.

Register card LINE: "a crisp DARK sepia-to-near-black pen line, the darkest
marks in the image are this line and its hatching." So: take the dark tail of
the figure's luminance, skeletonise nothing -- just measure the WIDTH of each
dark run along image rows and columns, and report the median. Normalised by
the figure height so it transfers to any output scale.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
MASKS = os.path.join(K3, "work", "masks"); OUT = os.path.join(K3, "out")
SEEDS = os.path.join(ROOT, "artifacts", "seeds")
SEED = {"N": "seed_N.png", "NE": "seed_NE.png", "E": "seed_E.png", "SE": "seed_SE.png",
        "S": "seed_S_v2.png", "SW": "seed_SW_v2.png", "W": "seed_W.png", "NW": "seed_NW.png"}


def runs(mask):
    out = []
    for row in mask:
        d = np.diff(np.concatenate([[0], row.view(np.int8), [0]]))
        s = np.where(d == 1)[0]; e = np.where(d == -1)[0]
        out += list(e - s)
    return out


def main():
    rep = {"note": "Measured ink-line width in the eight approved stills.", "views": {}}
    allw = []
    for d, f in SEED.items():
        rgb = np.asarray(Image.open(os.path.join(SEEDS, f)).convert("RGB")).astype(np.float32)
        body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        H = int(np.ptp(np.where(body.any(axis=1))[0]) + 1)
        lum = rgb @ np.array([0.299, 0.587, 0.114])
        # THE CONTOUR, not the hatching. The darkest-N% trick returns 2 px in
        # every view -- that is the hatching's width, and the hatching is the
        # commonest dark mark in the image, so a median over all dark runs
        # measures IT and not the outline. The outline is the dark band that
        # sits ON the silhouette: march inward from the boundary and count
        # consecutive dark pixels, on rows/columns where the boundary is steep
        # enough for a horizontal/vertical march to be near-perpendicular.
        inside = ndi.binary_erosion(body, np.ones((3, 3)))
        thr = float(np.percentile(lum[inside], 12))
        ink = (lum < thr) & body
        widths = []
        for arr, inkarr in ((body, ink), (body.T, ink.T)):
            for j in range(arr.shape[0]):
                idxs = np.where(arr[j])[0]
                if len(idxs) < 6:
                    continue
                for start, step in ((idxs.min(), 1), (idxs.max(), -1)):
                    n = 0
                    k = start
                    while 0 <= k < arr.shape[1] and inkarr[j, k] and n < 30:
                        n += 1; k += step
                    if 1 <= n <= 30:
                        widths.append(n)
        w = np.array(widths)
        med = float(np.median(w))
        rep["views"][d] = dict(figure_h_px=H, ink_threshold_lum=round(thr, 1),
                               median_width_px=med, p75_width_px=float(np.percentile(w, 75)),
                               ink_area_pct=round(100.0 * ink.sum() / body.sum(), 2),
                               n_samples=int(len(w)),
                               per_1000H=round(1000.0 * med / H, 2))
        allw.append(1000.0 * med / H)
        print("%-3s H=%d thr=%.0f median line %.2f px (%.2f per 1000 H), ink %.2f %% of figure"
              % (d, H, thr, med, 1000.0 * med / H, rep["views"][d]["ink_area_pct"]))
    rep["line_px_per_1000H"] = float(np.median(allw))
    rep["spread_per_1000H"] = [float(min(allw)), float(max(allw))]
    with open(os.path.join(OUT, "line_weight.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    print("median %.2f px per 1000 H  (at the game's 198.3 px body: %.2f px)"
          % (rep["line_px_per_1000H"], rep["line_px_per_1000H"] * 198.33 / 1000))


main()
