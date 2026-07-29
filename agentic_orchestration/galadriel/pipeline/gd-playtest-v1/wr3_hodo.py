#!/usr/bin/env python3
"""WR1-GAL-3: hodograph solve for the camera pitch ratio k, and for s.

The long-lived lance (wedge toward screen lower-left) gives ONE equation:
    (vx/s)^2 + (vy/(s*k))^2 = (14/60)^2
Two unknowns, so k must come from lances pointing in OTHER screen directions.
Most of the 16 die on terrain within ~10 frames, but they are all alive for the
first ~8 frames after launch, and a velocity is all that is needed. So:

  * per wedge, take the frontier (furthest cold pixel in that wedge) per frame
  * fit velocity on the ADVANCING segment only -- a wedge whose frontier has
    stalled is a dead lance and contributes nothing but a frozen point
  * every surviving velocity is a sample of the ellipse
        u(theta) = (14/60) * (s*cos theta, s*k*sin theta)
    so  vx^2/U^2 + vy^2/V^2 = 1  is LINEAR in (vx^2, vy^2)  ->  least squares
    ->  s = U*60/14,  k = V/U.

The stall at f309086-309088 (the death hitch) is excluded by starting at f309089.
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.normpath(os.path.join(HERE, "..", "..", "captures",
                                       "2026-07-29-wr1-gal3", "frames"))


def cold(f, root, bright, box):
    a = np.asarray(Image.open(os.path.join(root, f"f{f:06d}.png")).convert("RGB")).astype(np.int16)
    x0, x1, y0, y1 = box
    sub = a[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > bright) & ((B - R) > 60) & (B >= G - 12)
    ys, xs = np.nonzero(m)
    return xs.astype(float) + x0, ys.astype(float) + y0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309089)
    ap.add_argument("--f1", type=int, default=309098)
    ap.add_argument("--seedx", type=float, default=1028.0)
    ap.add_argument("--seedy", type=float, default=573.0)
    ap.add_argument("--nwedge", type=int, default=20)
    ap.add_argument("--halffrac", type=float, default=0.75)
    ap.add_argument("--minadv", type=float, default=2.5, help="px/frame to count as alive")
    ap.add_argument("--bright", type=int, default=175)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    box = (300, 1750, 320, 930)
    frames = list(range(args.f0, args.f1 + 1))
    P = {f: cold(f, args.root, args.bright, box) for f in frames}

    half = np.pi / args.nwedge * args.halffrac
    tracks = []
    for w in range(args.nwedge):
        th = -np.pi + 2 * np.pi * (w + 0.5) / args.nwedge
        ts, xs, ys = [], [], []
        for f in frames:
            x, y = P[f]
            dx, dy = x - args.seedx, y - args.seedy
            ang = np.arctan2(dy, dx)
            d = np.abs((ang - th + np.pi) % (2 * np.pi) - np.pi)
            sel = d < half
            if sel.sum() < 6:
                continue
            r = np.hypot(dx[sel], dy[sel])
            i = int(np.argmax(r))
            ts.append(f); xs.append(x[sel][i]); ys.append(y[sel][i])
        if len(ts) < 5:
            tracks.append(dict(w=w, theta=round(th, 3), status="short", n=len(ts)))
            continue
        ts = np.array(ts, float); xs = np.array(xs); ys = np.array(ys)
        A = np.vstack([np.ones_like(ts), ts - ts.mean()]).T
        (x0f, vx) = np.linalg.lstsq(A, xs, rcond=None)[0]
        (y0f, vy) = np.linalg.lstsq(A, ys, rcond=None)[0]
        pred_x = x0f + vx * (ts - ts.mean()); pred_y = y0f + vy * (ts - ts.mean())
        rms = float(np.sqrt(((xs - pred_x) ** 2 + (ys - pred_y) ** 2).mean()))
        spd = float(np.hypot(vx, vy))
        tracks.append(dict(w=w, theta=round(th, 3), n=int(len(ts)),
                           v=[round(float(vx), 4), round(float(vy), 4)],
                           speed=round(spd, 3), rms=round(rms, 2),
                           alive=bool(spd >= args.minadv)))

    good = [t for t in tracks if t.get("alive") and t["rms"] < 9.0]
    V = np.array([t["v"] for t in good], float)
    M = np.vstack([V[:, 0] ** 2, V[:, 1] ** 2]).T
    coef, *_ = np.linalg.lstsq(M, np.ones(len(V)), rcond=None)
    U = float(1 / np.sqrt(coef[0])); Vy = float(1 / np.sqrt(coef[1]))
    res = dict(seed=[args.seedx, args.seedy], frames=[args.f0, args.f1],
               nwedge=args.nwedge, n_good=len(good),
               U_px_per_frame=round(U, 4), V_px_per_frame=round(Vy, 4),
               k=round(Vy / U, 4), s_px_per_m_x=round(U * 60 / 14, 3),
               s_px_per_m_y=round(Vy * 60 / 14, 3), tracks=tracks)
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in res.items() if q != "tracks"}, indent=1))
    for t in tracks:
        print(t)


if __name__ == "__main__":
    main()
