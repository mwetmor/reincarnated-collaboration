#!/usr/bin/env python3
"""C-9 image bake-off, JOB 3: the texture repaint EDIT over sheet A's projection (T8P-B).

    python3 07_score_j3.py

THE D1 INSTRUMENT IS GONE; THIS IS ITS NEAREST NEIGHBOUR, AND IT IS A CLOSE ONE. D1 (milestone
M-C9-T8-D1, nb_t8/scripts/t5_08_agree.py) baked sheet A and sheet B into the UV texture and
measured how far the two disagree on the texels BOTH painted: mean 15.38 / contested 11.92 /
17.0% over 24 for T8P-B_a, against T5's 34.24 when B was painted blind. Its bake arrays
(_raw.npy, _wsum.npy) and the surface file were scratch and no longer exist; rebuilding them
means re-rasterising a 289k-triangle model per candidate.

But T8P-B's CANVAS -- IMAGE 1, t8_sheet_b_canvas.png -- IS sheet A's paint projected onto the
model and rendered at the game camera. So a repaint's per-pixel colour distance from its
canvas, over the figure, is the SAME comparison D1 makes (B's paint against A's paint on the
same surface point), sampled in screen pixels instead of texels. The metric is D1's: sRGB
Euclidean distance / sqrt(3) on 0-255, with mean, median, p90 and the share over 8 and 24.
Differences stated: screen weighting instead of texel density x facing^4, and no "contested"
split (that needs the per-sheet weights). Astra's B_a is scored too, so the proxy sits next
to its own D1 value.

Plus REGISTRATION, because a repaint that slid 5 px would score as disagreement everywhere
while having repainted nothing: the integer shift within +-10 px that minimises the mean,
reported with the mean at that shift. A large gap between the two means the model moved the
figure; a small one means the disagreement is paint.
"""
import json
import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
C9 = HERE.parent
CANVAS = C9 / "artifacts/CS9-guides/t8_sheet_b_canvas.png"
REPAINTS = {"astra_a": C9 / "artifacts/T8P-B/T8P-B_a.png", "astra_b": C9 / "artifacts/T8P-B/T8P-B_b.png",
            "nb_a": HERE / "out/J3_nb_a.png", "nb_b": HERE / "out/J3_nb_b.png",
            "nbp_a": HERE / "out/J3_nbp_a.png", "nbp_b": HERE / "out/J3_nbp_b.png"}
D1_ANCHOR = {"astra_a": {"mean": 15.376, "median": 10.046, "p90": 32.852, "pct_over_24": 17.013}}


def stats(d):
    return {"mean": round(float(d.mean()), 2), "median": round(float(np.median(d)), 2),
            "p90": round(float(np.percentile(d, 90)), 2),
            "pct_over_8": round(float((d > 8).mean() * 100), 1),
            "pct_over_24": round(float((d > 24).mean() * 100), 1)}


def grad_energy(rgb, mask):
    L = rgb.mean(-1)
    L = ndimage.gaussian_filter(L, 0.8)
    g = np.hypot(ndimage.sobel(L, 0), ndimage.sobel(L, 1))
    return float(g[mask].mean())


def main() -> None:
    can = np.asarray(Image.open(CANVAS).convert("RGB")).astype(np.float32)
    H, W = can.shape[:2]
    green = np.abs(can - np.array([0, 255, 0])).max(-1) <= 60
    fig = ndimage.binary_erosion(~green, np.ones((5, 5), bool))       # 2 px clear of the outline
    ring = ndimage.binary_dilation(~green, np.ones((25, 25), bool)) & green
    rep = {}
    for name, p in REPAINTS.items():
        im = Image.open(p).convert("RGB")
        size = list(im.size)
        rp = np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32)
        d0 = np.linalg.norm(rp - can, axis=2) / np.sqrt(3.0)
        best = (1e9, 0, 0)
        for dy in range(-10, 11, 2):
            for dx in range(-10, 11, 2):
                sh = np.roll(np.roll(rp, dy, 0), dx, 1)
                m = float((np.linalg.norm(sh - can, axis=2) / np.sqrt(3.0))[fig].mean())
                if m < best[0]:
                    best = (m, dy, dx)
        # paint outside the outline: the repaint's non-plate pixels in a 12 px ring OUTSIDE
        # the canvas figure -- "stay inside every outline"
        spill = float((np.abs(rp - np.array([0, 255, 0])).max(-1) > 60)[ring].mean())
        # DISAGREEMENT ALONE REWARDS DOING NOTHING. A model that hands the canvas back
        # untouched scores the lowest disagreement there is, and this pass exists to ADD the
        # hand -- ink line, hatching, washes -- to a smooth projection render. So the second
        # number is how much painted detail the repaint carries against its canvas: mean
        # gradient energy over the figure, repaint over canvas. A pass-through reads ~1.0.
        gain = grad_energy(rp, fig) / max(grad_energy(can, fig), 1e-6)
        rep[name] = {"size": size, "screen_disagreement": stats(d0[fig]),
                     "detail_gain": round(gain, 3),
                     "best_shift_px": [best[1], best[2]], "mean_at_best_shift": round(best[0], 2),
                     "spill_outside_outline": round(spill, 3)}
        if name in D1_ANCHOR:
            rep[name]["d1_texture_space"] = D1_ANCHOR[name]
        s = rep[name]["screen_disagreement"]
        print("%-8s mean %5.2f  median %5.2f  p90 %5.2f  >24 %4.1f%% | detail gain %.2f | best shift %s -> %.2f | spill %.3f | %s"
              % (name, s["mean"], s["median"], s["p90"], s["pct_over_24"], gain, [best[1], best[2]],
                 best[0], spill, size))
    (HERE / "score_j3.json").write_text(json.dumps(rep, indent=1) + "\n")


if __name__ == "__main__":
    main()
