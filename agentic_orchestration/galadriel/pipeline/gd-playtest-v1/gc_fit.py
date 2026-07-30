#!/usr/bin/env python3
"""GAL-CAM: global camera fit to the nova ring under a PINHOLE ground model.

THE MODEL
---------
Ground plane y=0. Camera at height h, pitched down by theta, no roll. Put the
screen principal point P=(px0,py0) at the ground point the optical axis hits, and
measure ground offsets from that point: X to screen-right, Z away-from-camera
(up-screen). With D = camera-to-that-point distance and f the focal length in px:

    sx =  (f/D) * X          / (1 + (Z cos t)/D)
    sy = -(f/D) * Z * sin t  / (1 + (Z cos t)/D)

Reparametrised with s0 = f/D (px per metre AT the principal point) and q = 1/D:

    sx =  s0 * X          / (1 + q Z cos t)
    sy = -s0 * Z * sin t  / (1 + q Z cos t)

q = 0 is the ORTHOGRAPHIC limit exactly (infinitely distant camera, no
foreshortening gradient). So the pinhole-vs-ortho question is a one-parameter
hypothesis test on q, not a model swap. That is the whole reason for this
parametrisation.

THE DATA
--------
Skill_AttackProjectileRing: 16 projectiles, 22.5 deg apart, 14 m/s, 12 m range
(legolas .arz extraction; charter E-1). Head i at frame f sits on the ground at
    (X0 + R cos(phi + i*2pi/16),  Z0 + R sin(phi + i*2pi/16)),  R = 14 (f-t0)/60
so ONE rigid 16-point figure of known metric size sweeps the whole play area
across ~56 frames. That is the calibration target.

Free: s0, theta, q, X0, Z0, phi, t0   (7)
Fixed by choice: principal point (960,540) = viewport centre. Sensitivity to
that choice is reported separately by --px0/--py0 sweeps, NOT assumed away.

A constant sprite-height offset (heads drawn above the ground plane) is, to first
order, a pure screen-y translation and is therefore absorbed by Z0. It does not
bias theta or q at the level this fit resolves them.

ASSIGNMENT
----------
EM: predict 16 head positions, assign each detected blob to its nearest
prediction inside a gate, refit, repeat. Robust loss (soft_l1) so a surviving
trail fragment or a terrain sparkle cannot drag the geometry.
"""
import argparse
import json
import math
import os

import numpy as np
from scipy.optimize import least_squares

NPROJ = 16
VPROJ = 14.0   # m/s
FPS = 60.0


def predict(par, f, px0, py0, nproj=NPROJ):
    s0, t, q, X0, Z0, phi, t0 = par
    R = VPROJ * (f - t0) / FPS
    a = phi + np.arange(nproj) * (2 * math.pi / nproj)
    X = X0 + R * np.cos(a)
    Z = Z0 + R * np.sin(a)
    den = 1.0 + q * Z * math.cos(t)
    den = np.where(np.abs(den) < 1e-3, np.sign(den) * 1e-3, den)
    sx = s0 * X / den
    sy = -s0 * Z * math.sin(t) / den
    return px0 + sx, py0 + sy, R


def assign(par, frames, pts, px0, py0, gate):
    """pts: dict f -> (N,2) array of blob xy. Returns list of (f, xy, k)."""
    out = []
    for f in frames:
        P = pts.get(f)
        if P is None or len(P) == 0:
            continue
        mx, my, R = predict(par, f, px0, py0)
        d = np.hypot(P[:, 0][:, None] - mx[None, :], P[:, 1][:, None] - my[None, :])
        k = np.argmin(d, axis=1)
        dm = d[np.arange(len(P)), k]
        g = gate(R)
        sel = dm < g
        for i in np.nonzero(sel)[0]:
            out.append((f, P[i], int(k[i])))
    return out


def resid(par, matches, px0, py0):
    r = []
    byf = {}
    for f, xy, k in matches:
        byf.setdefault(f, []).append((xy, k))
    for f, lst in byf.items():
        mx, my, _ = predict(par, f, px0, py0)
        for xy, k in lst:
            r.append(xy[0] - mx[k])
            r.append(xy[1] - my[k])
    return np.array(r)


def fit(frames, pts, px0, py0, p0, fix_q=False, iters=8, gatef=None):
    if gatef is None:
        gatef = lambda R: max(25.0, 0.20 * 63.0 * max(R, 0.5))
    par = np.array(p0, float)
    lo = np.array([20.0, 0.25, -0.20, -30, -30, -math.pi, 309000.0])
    hi = np.array([200.0, 1.45, 0.20, 30, 30, math.pi, 309120.0])
    matches = []
    for _ in range(iters):
        matches = assign(par, frames, pts, px0, py0, gatef)
        if len(matches) < 20:
            break
        if fix_q:
            def fn(p6):
                p = np.array([p6[0], p6[1], 0.0, p6[2], p6[3], p6[4], p6[5]])
                return resid(p, matches, px0, py0)
            i6 = [0, 1, 3, 4, 5, 6]
            r = least_squares(fn, par[i6], loss="soft_l1", f_scale=6.0,
                              bounds=(lo[i6], hi[i6]), max_nfev=4000)
            par = np.array([r.x[0], r.x[1], 0.0, r.x[2], r.x[3], r.x[4], r.x[5]])
        else:
            r = least_squares(resid, par, args=(matches, px0, py0),
                              loss="soft_l1", f_scale=6.0, bounds=(lo, hi),
                              max_nfev=6000)
            par = r.x
    matches = assign(par, frames, pts, px0, py0, gatef)
    rr = resid(par, matches, px0, py0)
    rms = float(np.sqrt(np.mean(rr ** 2))) if len(rr) else float("nan")
    med = float(np.median(np.abs(rr))) if len(rr) else float("nan")
    return par, matches, rms, med


def load_pts(path, f0, f1, minpx, exclude):
    d = json.load(open(path))
    pts = {}
    for row in d["rows"]:
        f = row["f"]
        if f < f0 or f > f1 or f in exclude:
            continue
        P = [(b["cx"], b["cy"]) for b in row["blobs"] if b["n"] >= minpx]
        if P:
            pts[f] = np.array(P, float)
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--heads", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--f0", type=int, default=309089)
    ap.add_argument("--f1", type=int, default=309140)
    ap.add_argument("--minpx", type=int, default=10)
    ap.add_argument("--px0", type=float, default=960.0)
    ap.add_argument("--py0", type=float, default=540.0)
    ap.add_argument("--boot", type=int, default=400)
    args = ap.parse_args()

    exclude = set()
    pts = load_pts(args.heads, args.f0, args.f1, args.minpx, exclude)
    frames = sorted(pts)
    print(f"frames {len(frames)}  blobs {sum(len(v) for v in pts.values())}")

    # seed from GAL-3: s0~63 px/m, k=sin t ~0.72, centre (1025,568), ortho
    best = None
    for phi0 in np.linspace(0, 2 * math.pi / NPROJ, 8, endpoint=False):
        p0 = [63.0, math.asin(0.72), 0.0,
              (1025.0 - args.px0) / 63.0,
              -(568.0 - args.py0) / (63.0 * 0.72), phi0, 309084.0]
        par, m, rms, med = fit(frames, pts, args.px0, args.py0, p0, fix_q=False)
        print(f"  phi0={phi0:.3f} -> rms={rms:.2f} n={len(m)} "
              f"s0={par[0]:.2f} t={math.degrees(par[1]):.2f} q={par[2]:.5f}")
        if best is None or (len(m) > 40 and rms < best[2]):
            best = (par, m, rms, med)
    par, matches, rms, med = best
    s0, t, q, X0, Z0, phi, t0 = par
    print("\nBEST (pinhole):")
    print(f"  s0={s0:.3f} px/m   pitch={math.degrees(t):.2f} deg   "
          f"k=sin={math.sin(t):.4f}")
    print(f"  q={q:.6f} /m  -> D={1/q if abs(q)>1e-9 else float('inf'):.1f} m")
    print(f"  X0={X0:.3f} Z0={Z0:.3f} phi={math.degrees(phi):.2f} t0={t0:.3f}")
    print(f"  matched {len(matches)} blobs, rms {rms:.2f} px, medabs {med:.2f} px")

    # ortho-constrained fit for the model comparison
    p0o = list(par); p0o[2] = 0.0
    paro, mo, rmso, medo = fit(frames, pts, args.px0, args.py0, p0o, fix_q=True)
    print("\nORTHO (q==0):")
    print(f"  s0={paro[0]:.3f} px/m  pitch={math.degrees(paro[1]):.2f} deg  "
          f"k={math.sin(paro[1]):.4f}  rms={rmso:.2f} n={len(mo)}")

    # profile likelihood in q -> bound on the camera distance D
    prof = []
    for qv in np.linspace(-0.06, 0.06, 25):
        pq = list(par); pq[2] = qv
        # refit everything else with q pinned
        def fn(p6):
            p = np.array([p6[0], p6[1], qv, p6[2], p6[3], p6[4], p6[5]])
            return resid(p, mm, args.px0, args.py0)
        pp = np.array(pq)
        for _ in range(6):
            mm = assign(pp, frames, pts, args.px0, args.py0,
                        lambda R: max(25.0, 0.20 * 63.0 * max(R, 0.5)))
            i6 = [0, 1, 3, 4, 5, 6]
            r = least_squares(fn, pp[i6], loss="soft_l1", f_scale=6.0, max_nfev=3000)
            pp = np.array([r.x[0], r.x[1], qv, r.x[2], r.x[3], r.x[4], r.x[5]])
        mm = assign(pp, frames, pts, args.px0, args.py0,
                    lambda R: max(25.0, 0.20 * 63.0 * max(R, 0.5)))
        rq = resid(pp, mm, args.px0, args.py0)
        prof.append(dict(q=float(qv), D=float(1 / qv) if abs(qv) > 1e-9 else None,
                         rms=float(np.sqrt(np.mean(rq ** 2))), n=len(mm),
                         s0=float(pp[0]), pitch_deg=float(math.degrees(pp[1]))))
        print(f"  q={qv:+.4f} D={prof[-1]['D'] if prof[-1]['D'] else 0:9.1f} "
              f"rms={prof[-1]['rms']:.3f} n={prof[-1]['n']} "
              f"s0={pp[0]:.2f} pitch={math.degrees(pp[1]):.2f}")

    # bootstrap over FRAMES (the correlated unit) for uncertainty
    rng = np.random.default_rng(7)
    boots = []
    for b in range(args.boot):
        fs = list(rng.choice(frames, size=len(frames), replace=True))
        sub = {}
        for i, f in enumerate(fs):
            sub[f + 0.0001 * i] = pts[f]   # unique keys, same f content
        # rebuild with integer-frame semantics: use a list-based fit instead
        bf = fs
        bpts = pts
        try:
            pb, mb, rb, _ = fit(bf, bpts, args.px0, args.py0, par, iters=3)
            boots.append([float(pb[0]), float(math.degrees(pb[1])), float(pb[2]),
                          float(math.sin(pb[1]))])
        except Exception:
            pass
    B = np.array(boots) if boots else np.zeros((0, 4))
    qs = {}
    if len(B):
        for j, nm in enumerate(["s0", "pitch_deg", "q", "k"]):
            qs[nm] = dict(p2_5=float(np.percentile(B[:, j], 2.5)),
                          p16=float(np.percentile(B[:, j], 16)),
                          p50=float(np.percentile(B[:, j], 50)),
                          p84=float(np.percentile(B[:, j], 84)),
                          p97_5=float(np.percentile(B[:, j], 97.5)))
        print("\nBOOTSTRAP (n=%d):" % len(B))
        for nm, v in qs.items():
            print(f"  {nm:9s} 2.5%={v['p2_5']:.4f} 50%={v['p50']:.4f} "
                  f"97.5%={v['p97_5']:.4f}")

    json.dump(dict(px0=args.px0, py0=args.py0, f0=args.f0, f1=args.f1,
                   minpx=args.minpx, n_frames=len(frames),
                   best=dict(s0=float(s0), pitch_deg=float(math.degrees(t)),
                             k=float(math.sin(t)), q=float(q),
                             D=float(1 / q) if abs(q) > 1e-9 else None,
                             X0=float(X0), Z0=float(Z0),
                             phi_deg=float(math.degrees(phi)), t0=float(t0),
                             rms=rms, medabs=med, n_matched=len(matches)),
                   ortho=dict(s0=float(paro[0]),
                              pitch_deg=float(math.degrees(paro[1])),
                              k=float(math.sin(paro[1])), rms=rmso,
                              n_matched=len(mo)),
                   q_profile=prof, bootstrap=qs, n_boot=len(B)),
              open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
