#!/usr/bin/env python3
"""C-9 meshy_t1: settle ONE px/m, by measuring (R-C9-61 follow-up).

Three numbers were in play -- 110.185 (mine, BODY_PX/1.80 where BODY_PX came
from knight_fit.json's stored figure_h_src_px), 117.5 (gandalf's) and 114.729
(the integration session's camera fit). A stored constant is not a measurement,
so this measures the Grok cells themselves.

The pollaxe is split off first: it rises well above the helm, so a plain
content bbox measures the weapon, not the knight -- which is how 198.33 and
241 px can both be "the figure height" of the same cell.

Compared like with like: the TALLEST frame of each cycle, because a walk's bob
changes standing height by several px and the crown-to-sole of one arbitrary
frame is not the character's height.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
T1 = os.path.dirname(HERE); C9 = os.path.dirname(T1)
GROK = os.path.join(C9, "cliffside_B", "sprites_knight")


def body_only(path):
    a = np.asarray(Image.open(path).convert("RGBA"))
    fig = a[..., 3] > 8
    fig = ndi.binary_fill_holes(ndi.binary_closing(fig, np.ones((3, 3))))
    ys = np.where(fig.any(axis=1))[0]
    Hc = ys.max() - ys.min() + 1
    ext = np.zeros(fig.shape[1])
    for x in np.where(fig.any(axis=0))[0]:
        yy = np.where(fig[:, x])[0]
        ext[x] = yy.max() - yy.min() + 1
    tall = np.where(ext > 0.90 * Hc)[0]          # the haft spans nearly the frame
    if len(tall):
        cx = int(np.median(tall)); w = max(4, int(round(0.020 * Hc)))
        bar = np.zeros_like(fig)
        bar[:, max(0, cx - w):cx + w + 1] = fig[:, max(0, cx - w):cx + w + 1]
        rest = fig & ~ndi.binary_dilation(bar, np.ones((3, 3)))
        lab, n = ndi.label(rest, structure=np.ones((3, 3)))
        if n:
            sizes = np.array(ndi.sum(rest, lab, range(1, n + 1)))
            fig = ndi.binary_fill_holes(lab == (1 + int(np.argmax(sizes))))
    ys = np.where(fig.any(axis=1))[0]
    return int(ys.min()), int(ys.max())


def main():
    rep = {"note": __doc__.strip().splitlines()[0], "measurements": {}}
    for st in ("walk", "run", "idle"):
        d = os.path.join(GROK, st, "E")
        if not os.path.isdir(d):
            continue
        hs, soles = [], []
        for f in sorted(os.listdir(d)):
            if not f.endswith(".png"):
                continue
            t, b = body_only(os.path.join(d, f))
            hs.append(b - t + 1); soles.append(b)
        rep["measurements"]["grok_" + st] = dict(
            n=len(hs), body_px_max=int(max(hs)), body_px_mean=round(float(np.mean(hs)), 2),
            sole_max=int(max(soles)), sole_mean=round(float(np.mean(soles)), 2))
        print("  grok %-5s body px: max %3d mean %6.2f   sole: max %3d mean %6.2f"
              % (st, max(hs), np.mean(hs), max(soles), np.mean(soles)))
    # the tallest Grok frame anywhere is the closest thing to the character's
    # standing height in this sprite format
    best = max(v["body_px_max"] for v in rep["measurements"].values())
    rep["grok_body_px_tallest"] = best
    for h in (1.80,):
        rep["px_per_m_if_height_%.2f" % h] = round(best / h, 4)
    print("\n  tallest Grok body: %d px  ->  %.3f px/m at a 1.80 m character"
          % (best, best / 1.80))
    for nm, v in (("drax_110.185", 110.185), ("gandalf_117.5", 117.5),
                  ("integration_114.729", 114.729)):
        print("     %-22s implies a Grok body of %.1f px (%+.1f px)"
              % (nm, v * 1.80, v * 1.80 - best))
    json.dump(rep, open(os.path.join(T1, "work", "scale_measure.json"), "w"), indent=1)
    print("  wrote work/scale_measure.json")


main()
