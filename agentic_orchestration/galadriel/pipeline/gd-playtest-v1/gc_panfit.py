#!/usr/bin/env python3
"""GAL-CAM: read pitch, roll, scale-gradient and zoom-drift off the pan record.

INPUT  gc_pan.py output (per-frame-pair, per-band camera pan vectors)

PRODUCTS
--------
1. k = sin(pitch), as the AXIS RATIO of the pan-vector cloud.
   Falsifiability check built in: if the cloud is really an ellipse (i.e. if
   ground speed is isotropic and the projection is a linear ground map), then
   the axis ratio measured at the 50th, 75th, 90th and 98th speed percentile
   must AGREE. If they disagree the cloud is not an ellipse and the pitch number
   must be withdrawn. The check is reported whether it passes or fails.

2. Camera ROLL, as the cross-term of a general origin-centred conic fit.
   a*u^2 + b*u*w + c*w^2 = 1;  roll = 0.5*atan2(b, a-c).

3. SCALE GRADIENT with screen row: robust slope of band-j pan against the
   reference band's pan. Orthographic predicts every ratio == 1 exactly. Any
   systematic departure is the perspective foreshortening gradient, measured
   without positing a camera model.

4. ZOOM DRIFT: the semi-major axis A refitted per sampled window. A is
   (ground speed) x (px per metre), so a change in A is a change in zoom OR in
   the player's run speed -- the two are NOT separable by this instrument alone,
   and the report says so rather than crediting one of them.
"""
import argparse
import json
import math

import numpy as np


def ellipse_axes(U, Wv, nb=36, q=98.0, vmin=1.5):
    """Origin-centred axis-aligned ellipse through the per-direction q-quantile."""
    sp = np.hypot(U, Wv)
    m = sp > vmin
    U, Wv, sp = U[m], Wv[m], sp[m]
    if len(sp) < 200:
        return None
    ph = np.arctan2(Wv, U) % (2 * math.pi)
    b = np.floor(ph / (2 * math.pi) * nb).astype(int) % nb
    P, R = [], []
    for i in range(nb):
        s = sp[b == i]
        if len(s) < 8:
            continue
        P.append((i + 0.5) * 2 * math.pi / nb)
        R.append(np.percentile(s, q))
    if len(P) < 12:
        return None
    P = np.array(P); R = np.array(R)
    # 1/rho^2 = cos^2/A^2 + sin^2/B^2   (linear in 1/A^2, 1/B^2)
    M = np.vstack([np.cos(P) ** 2, np.sin(P) ** 2]).T
    sol, *_ = np.linalg.lstsq(M, 1.0 / R ** 2, rcond=None)
    if sol[0] <= 0 or sol[1] <= 0:
        return None
    A, B = 1 / math.sqrt(sol[0]), 1 / math.sqrt(sol[1])
    pred = 1.0 / np.sqrt(M @ sol)
    res = float(np.sqrt(np.mean((R - pred) ** 2)) / R.mean())
    return dict(A=A, B=B, k=B / A, nbin=len(P), relres=res)


def conic(U, Wv, q=98.0, nb=36, vmin=1.5):
    """General origin-centred conic -> camera roll from the cross term."""
    sp = np.hypot(U, Wv)
    m = sp > vmin
    U, Wv, sp = U[m], Wv[m], sp[m]
    ph = np.arctan2(Wv, U) % (2 * math.pi)
    b = np.floor(ph / (2 * math.pi) * nb).astype(int) % nb
    pu, pw = [], []
    for i in range(nb):
        s = np.nonzero(b == i)[0]
        if len(s) < 8:
            continue
        r = np.percentile(sp[s], q)
        a = (i + 0.5) * 2 * math.pi / nb
        pu.append(r * math.cos(a)); pw.append(r * math.sin(a))
    pu = np.array(pu); pw = np.array(pw)
    M = np.vstack([pu ** 2, pu * pw, pw ** 2]).T
    sol, *_ = np.linalg.lstsq(M, np.ones(len(pu)), rcond=None)
    a, bb, c = sol
    roll = 0.5 * math.atan2(bb, a - c)
    ev = np.linalg.eigvalsh(np.array([[a, bb / 2], [bb / 2, c]]))
    if (ev <= 0).any():
        return dict(roll_deg=math.degrees(roll), k=None)
    ax = 1 / np.sqrt(ev)          # semi-axes, ascending eigenvalue -> descending axis
    return dict(roll_deg=math.degrees(roll), k=float(min(ax) / max(ax)),
                A=float(max(ax)), B=float(min(ax)))


def robust_ratio(Vj, Vr, vmin=4.0):
    """Median-of-ratios slope of band j pan against reference band pan."""
    sp = np.hypot(*Vr.T)
    m = sp > vmin
    if m.sum() < 50:
        return None
    num = (Vj[m] * Vr[m]).sum(axis=1)
    den = (Vr[m] * Vr[m]).sum(axis=1)
    r = num / den
    return dict(n=int(m.sum()), med=float(np.median(r)),
                p16=float(np.percentile(r, 16)), p84=float(np.percentile(r, 84)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", type=int, default=440)
    ap.add_argument("--pkmin", type=float, default=0.02)
    args = ap.parse_args()

    d = json.load(open(args.pan))
    bands = d["bands"]
    rows = d["rows"]
    print(f"{len(rows)} pairs, bands {bands}, band height {d['bh']}")

    V = {b: np.array([r[f"b{b}"][:2] for r in rows]) for b in bands}
    PK = {b: np.array([r[f"b{b}"][2] for r in rows]) for b in bands}
    SS = np.array([r["ss"] for r in rows])

    out = dict(bands=bands, bh=d["bh"], n_pairs=len(rows))

    # --- 1/2. ellipse + roll per band, with the percentile-invariance check ---
    out["per_band"] = {}
    for b in bands:
        g = PK[b] > args.pkmin
        U, Wv = V[b][g, 0], V[b][g, 1]
        rec = dict(n=int(g.sum()), peak_med=float(np.median(PK[b])))
        for q in (50, 75, 90, 98):
            e = ellipse_axes(U, Wv, q=q)
            if e:
                rec[f"q{q}"] = e
        c = conic(U, Wv)
        rec["conic"] = c
        out["per_band"][str(b)] = rec
        ks = [rec[f"q{q}"]["k"] for q in (50, 75, 90, 98) if f"q{q}" in rec]
        print(f"\nband y={b}-{b+d['bh']}  n={rec['n']}  peakmed={rec['peak_med']:.3f}")
        for q in (50, 75, 90, 98):
            if f"q{q}" in rec:
                e = rec[f"q{q}"]
                print(f"   q{q:<3d} A={e['A']:7.3f} B={e['B']:7.3f} k={e['k']:.4f} "
                      f"pitch={math.degrees(math.asin(min(1,e['k']))):.2f}deg "
                      f"relres={e['relres']:.3f}")
        if ks:
            print(f"   k spread over percentiles: {min(ks):.4f}-{max(ks):.4f}")
        print(f"   conic roll={c['roll_deg']:+.2f} deg  k_conic="
              f"{c['k'] if c['k'] else float('nan'):.4f}")

    # --- 3. scale gradient across bands ---
    ref = args.ref
    out["gradient"] = {}
    print(f"\nSCALE GRADIENT (relative to band y={ref}):")
    for b in bands:
        g = (PK[b] > args.pkmin) & (PK[ref] > args.pkmin)
        r = robust_ratio(V[b][g], V[ref][g])
        out["gradient"][str(b)] = r
        if r:
            print(f"   band {b:4d} (centre y={b+d['bh']//2:4d})  ratio="
                  f"{r['med']:.4f} [{r['p16']:.4f},{r['p84']:.4f}]  n={r['n']}")

    # --- 4. zoom drift per window ---
    print("\nPER-WINDOW SEMI-AXES (band y=%d):" % ref)
    out["windows"] = []
    for ss in sorted(set(SS.tolist())):
        m = (SS == ss) & (PK[ref] > args.pkmin)
        if m.sum() < 100:
            continue
        e = ellipse_axes(V[ref][m, 0], V[ref][m, 1], nb=24, q=95, vmin=1.5)
        if not e:
            continue
        out["windows"].append(dict(ss=float(ss), **e, n=int(m.sum())))
        print(f"   ss={ss:6.0f}  A={e['A']:6.3f}  B={e['B']:6.3f}  k={e['k']:.4f}"
              f"  relres={e['relres']:.3f}  n={int(m.sum())}")
    if out["windows"]:
        A = np.array([w["A"] for w in out["windows"]])
        K = np.array([w["k"] for w in out["windows"]])
        print(f"\n   A across windows: med={np.median(A):.3f} "
              f"p10={np.percentile(A,10):.3f} p90={np.percentile(A,90):.3f} "
              f"min={A.min():.3f} max={A.max():.3f} cv={A.std(ddof=1)/A.mean():.3f}")
        print(f"   k across windows: med={np.median(K):.4f} "
              f"p10={np.percentile(K,10):.4f} p90={np.percentile(K,90):.4f}")
        out["drift"] = dict(A_med=float(np.median(A)), A_min=float(A.min()),
                            A_max=float(A.max()),
                            A_p10=float(np.percentile(A, 10)),
                            A_p90=float(np.percentile(A, 90)),
                            A_cv=float(A.std(ddof=1) / A.mean()),
                            k_med=float(np.median(K)),
                            k_p10=float(np.percentile(K, 10)),
                            k_p90=float(np.percentile(K, 90)))

    json.dump(out, open(args.out, "w"), indent=1)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
