#!/usr/bin/env python3
"""WR1-GAL-3 fit v2 — nova ring as self-calibrating scale bar (corrected).

Fixes over v1:
  * HUD mana globe (blue, bottom-right) excluded by box; boss frost aura ABOVE the
    caster excluded by using only the LOWER half-plane of the ellipse (y > cy),
    where the lance fan is unoccluded in this fixture.
  * frames restricted to the post-stall span. The client stalls at f309086-309088
    (play-area mean |delta| 119/209 vs 800-6000 typical) -- the death hitch -- so
    frame index is NOT proportional to sim time across it. Expansion rate is
    fitted on f309089+ only.
  * leading-edge statistic is max rho, not a percentile: the furthest-travelled
    lance IS the ring radius, and a lance that dies early can only pull the
    statistic DOWN, never up, so max is the correct (and conservative) estimator.

Outputs cx, cy (caster ground point in screen px), k (=sin pitch),
A (px per frame along X), hence s = A*60/14 px per metre along screen X.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def head_pixels(f, root, bright, box):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    return xs.astype(np.float64) + x0, ys.astype(np.float64) + y0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309089)
    ap.add_argument("--f1", type=int, default=309110)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--bright", type=int, default=200)
    ap.add_argument("--lower", action="store_true", default=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    box = (500, 1400, 300, 900)
    frames = list(range(args.f0, args.f1 + 1))
    P = {f: head_pixels(f, args.root, args.bright, box) for f in frames}

    best = None
    for cx in np.arange(990, 1081, 2.0):
        for cy in np.arange(535, 616, 2.0):
            for k in np.arange(0.34, 0.76, 0.01):
                ah = []
                ok = True
                for f in frames:
                    x, y = P[f]
                    sel = y > cy
                    if sel.sum() < 30:
                        ok = False
                        break
                    rho = np.sqrt((x[sel] - cx) ** 2 + ((y[sel] - cy) / k) ** 2)
                    ah.append(rho.max())
                if not ok:
                    continue
                ah = np.array(ah)
                t = np.array(frames, float)
                c = np.polyfit(t, ah, 1)
                pred = np.polyval(c, t)
                r2 = 1 - ((ah - pred) ** 2).sum() / ((ah - ah.mean()) ** 2).sum()
                rmse = float(np.sqrt(((ah - pred) ** 2).mean()))
                if c[0] <= 0:
                    continue
                if best is None or r2 > best["r2"]:
                    best = dict(r2=float(r2), rmse=rmse, cx=float(cx), cy=float(cy), k=float(k),
                                A=float(c[0]), b=float(c[1]), a_hat=ah.tolist())
    b = best
    t0 = -b["b"] / b["A"]
    s = b["A"] * 60.0 / 14.0
    b.update(t0_frame=t0, s_px_per_m_x=s, s_px_per_m_y=s * b["k"],
             frames=frames, box=box, bright=args.bright)
    json.dump(b, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in b.items() if q not in ("a_hat", "frames")}, indent=1))
    print("a_hat:", [round(v, 1) for v in b["a_hat"]])


if __name__ == "__main__":
    main()
