#!/usr/bin/env python3
"""WR1-GAL-3: per-lance track solve — the cross-check instrument.

Independent of the whole-ring fits. Each of the 16 projectiles leaves the caster
on a straight ground-plane ray at a constant 14 m/s, so under a fixed camera its
HEAD traces a straight SCREEN line at constant screen velocity, and all 16 lines
pass through the caster's ground point. Two products fall out:

  (1) CASTER GROUND POINT = least-squares intersection of the lance lines.
  (2) SCALE. The 16 screen velocity vectors are 16 samples of the ellipse
      u(theta) = (s*cos(theta), s*k*sin(theta)) * 14/60.
      Fitting that ellipse gives s (px per metre along X) and k (= sin pitch)
      with no reliance on where the ring centre is.

Head extraction per direction: take the cold-mask pixel FURTHEST from a seed
centre within a narrow screen-angle wedge. Trails lie behind the head, so the
furthest pixel in a wedge IS that lance's head. Wedges with a dead/stalled lance
show as a track whose velocity collapses; they are reported, not silently kept.
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


def fit_line_t(ts, xs, ys):
    """least-squares constant-velocity track; returns (p0, v, rms)"""
    ts = np.asarray(ts, float)
    A = np.vstack([np.ones_like(ts), ts - ts.mean()]).T
    cx, vx = np.linalg.lstsq(A, xs, rcond=None)[0]
    cy, vy = np.linalg.lstsq(A, ys, rcond=None)[0]
    rx = xs - (cx + vx * (ts - ts.mean()))
    ry = ys - (cy + vy * (ts - ts.mean()))
    rms = float(np.sqrt((rx ** 2 + ry ** 2).mean()))
    return (float(cx), float(cy)), (float(vx), float(vy)), float(ts.mean()), rms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--f0", type=int, default=309092)
    ap.add_argument("--f1", type=int, default=309110)
    ap.add_argument("--seedx", type=float, default=1028.0)
    ap.add_argument("--seedy", type=float, default=573.0)
    ap.add_argument("--nwedge", type=int, default=16)
    ap.add_argument("--bright", type=int, default=190)
    ap.add_argument("--root", default=FRAMES)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    box = (400, 1500, 280, 900)
    frames = list(range(args.f0, args.f1 + 1))
    P = {f: cold(f, args.root, args.bright, box) for f in frames}

    half = np.pi / args.nwedge
    tracks = []
    for w in range(args.nwedge):
        th = -np.pi + (2 * np.pi) * (w + 0.5) / args.nwedge
        ts, xs, ys = [], [], []
        for f in frames:
            x, y = P[f]
            dx, dy = x - args.seedx, y - args.seedy
            ang = np.arctan2(dy, dx)
            d = np.abs((ang - th + np.pi) % (2 * np.pi) - np.pi)
            sel = d < half * 0.7
            if sel.sum() < 12:
                continue
            r = dx[sel] ** 2 + dy[sel] ** 2
            i = int(np.argmax(r))
            ts.append(f)
            xs.append(x[sel][i])
            ys.append(y[sel][i])
        if len(ts) < 6:
            tracks.append(dict(wedge=w, theta_screen=th, n=len(ts), status="too-few"))
            continue
        p0, v, tm, rms = fit_line_t(ts, np.array(xs), np.array(ys))
        tracks.append(dict(wedge=w, theta_screen=round(th, 4), n=len(ts),
                           p0=[round(p0[0], 2), round(p0[1], 2)], t_mean=tm,
                           v=[round(v[0], 4), round(v[1], 4)],
                           speed=round(float(np.hypot(*v)), 3), rms=round(rms, 2),
                           frames=[ts[0], ts[-1]],
                           pts=[[int(a), round(b, 1), round(c, 1)] for a, b, c in zip(ts, xs, ys)]))
    good = [t for t in tracks if t.get("rms") is not None and t["rms"] < 12 and t["speed"] > 2.0]

    # (1) least-squares intersection of the lance lines
    A, b = [], []
    for t in good:
        vx, vy = t["v"]
        n = np.array([-vy, vx]) / np.hypot(vx, vy)   # unit normal
        p = np.array(t["p0"])
        A.append(n)
        b.append(n @ p)
    inter = None
    if len(A) >= 2:
        A = np.array(A); b = np.array(b)
        inter = np.linalg.lstsq(A, b, rcond=None)[0]
        resid = float(np.sqrt(((A @ inter - b) ** 2).mean()))

    # (2) hodograph ellipse: vx^2/U^2 + vy^2/V^2 = 1  ->  linear in (vx^2, vy^2)
    V = np.array([t["v"] for t in good], float)
    M = np.vstack([V[:, 0] ** 2, V[:, 1] ** 2]).T
    coef = np.linalg.lstsq(M, np.ones(len(V)), rcond=None)[0]
    U = float(1 / np.sqrt(coef[0])) if coef[0] > 0 else float("nan")
    Vy = float(1 / np.sqrt(coef[1])) if coef[1] > 0 else float("nan")
    s = U * 60.0 / 14.0
    k = Vy / U

    res = dict(seed=[args.seedx, args.seedy], frames=[args.f0, args.f1],
               n_tracks=len(tracks), n_good=len(good),
               caster_ground_px=[round(float(inter[0]), 2), round(float(inter[1]), 2)] if inter is not None else None,
               intersection_rms_px=round(resid, 2) if inter is not None else None,
               hodograph=dict(U_px_per_frame_x=round(U, 4), V_px_per_frame_y=round(Vy, 4),
                              s_px_per_m_x=round(s, 3), k=round(k, 4),
                              s_px_per_m_y=round(s * k, 3)),
               tracks=tracks)
    json.dump(res, open(args.out, "w"), indent=1)
    print(json.dumps({q: v for q, v in res.items() if q != "tracks"}, indent=1))
    for t in tracks:
        print(t.get("wedge"), t.get("n"), t.get("p0"), t.get("v"), t.get("rms"), t.get("status", ""))


if __name__ == "__main__":
    main()
