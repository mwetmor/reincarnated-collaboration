#!/usr/bin/env python3
"""C-9 knight3d: fit the pollaxe head's BEARING about the haft (R-C9-57).

The stills agree unanimously on the SIGN -- the fan is outboard and forward,
the fluke on the near side -- but not on the magnitude, because the image model
drew the head at nearly the same orientation in every view regardless of yaw
(the same defect as the haft's fixed screen offset, work/pollaxe_consistency).
So a single number cannot be read off any one view.

What CAN be done is to put both through the SAME instrument. 15_blade_side
measures, per view, the signed area asymmetry of the head either side of the
haft. Here the weapon mesh is rendered alone at each of the eight fitted
cameras for a range of bearings and measured the same way, and the bearing
that best reproduces the stills' eight-view profile wins.
"""
import json, math, os, sys
import numpy as np
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp
from raster import raster

K3 = os.path.dirname(HERE)
OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
spec = importlib.util.spec_from_file_location("e7", os.path.join(HERE, "07_export_parts.py"))
E7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(E7)
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]


def asym_of_mask(mask, haft_cx_fn, haft_w, y0, y1):
    yy, xx = np.where(mask[y0:y1 + 1])
    if not len(yy):
        return 0.0, 0, 0
    off = xx - haft_cx_fn(yy + y0)
    keep = np.abs(off) > haft_w * 0.6
    o = off[keep]
    ap, an = int((o > 0).sum()), int((o < 0).sum())
    return ((ap - an) / max(ap + an, 1)), ap, an


def render_weapon(p, bearing, alpha, theta, scale, tx, ty, W, H):
    pieces = E7.pollaxe(p, bearing_deg=bearing)
    r, u = kp.basis(alpha, theta); c = kp.cam_dir(alpha, theta)
    masks, zs = [], []
    tv, tz = [], []
    for nm, pts in pieces.items():
        v, f = E7.hull_mesh(pts)
        for tri in f:
            tv.append(v[tri]); tz.append(nm)
    tv = np.array(tv)
    flat = tv.reshape(-1, 3)
    xy = np.stack([flat @ r * scale + tx, -(flat @ u) * scale + ty], -1).reshape(len(tv), 3, 2)
    z = (-(flat @ c)).reshape(len(tv), 3)
    zb, ib, _, _ = raster(xy, z, None, W, H)
    solid = np.isfinite(zb)
    haft_only = np.array([n.endswith("_haft") for n in tz])
    zbh, _, _, _ = raster(xy[haft_only], z[haft_only], None, W, H)
    return solid, np.isfinite(zbh)


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta, ds = fit["theta_elevation_deg"], fit["downsample"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    ref = json.load(open(os.path.join(OUT, "blade_side.json")))
    target = {}
    for r in ref["per_view"]:
        ap, an = r["area_fwdside_px"], r["area_backside_px"]
        target[r["view"]] = (ap - an) / (ap + an)

    W, H = 1024, 1536
    best = None
    curve = {}
    for bearing in range(0, 181, 5):
        errs, got = [], {}
        for d in DIRS:
            v = fit["canonical"]["views"][d]
            s = v["scale"] * ds; tx = v["tx"] * ds; ty = v["ty"] * ds
            solid, haft = render_weapon(p, float(bearing), v["alpha"], theta,
                                        s, tx, ty, W, H)
            ys = np.where(solid.any(axis=1))[0]
            if not len(ys):
                continue
            wid = np.array([int(solid[y].sum()) for y in ys])
            hw = float(np.median([int(haft[y].sum()) for y in np.where(haft.any(axis=1))[0]]))
            head = ys[wid > hw * 2.2]
            if not len(head):
                got[d] = 0.0; errs.append(target[d] ** 2); continue
            hy = np.where(haft.any(axis=1))[0]
            hx = np.array([float(np.where(haft[y])[0].mean()) for y in hy])
            m, c = np.polyfit(hy.astype(float), hx, 1)
            a, _, _ = asym_of_mask(solid, lambda Y: m * Y + c, hw,
                                   int(head.min()), int(head.max()))
            got[d] = a
            errs.append((a - target[d]) ** 2)
        rms = float(np.sqrt(np.mean(errs)))
        curve[bearing] = dict(rms=rms, asym={k: round(v, 4) for k, v in got.items()})
        if best is None or rms < best[1]:
            best = (bearing, rms)
        print("  bearing %3d deg   rms %.4f   S %+.3f E %+.3f N %+.3f W %+.3f"
              % (bearing, rms, got.get("S", 0), got.get("E", 0),
                 got.get("N", 0), got.get("W", 0)))
    print("\nbest bearing %d deg (rms %.4f)" % best)
    print("stills:  S %+.3f E %+.3f N %+.3f W %+.3f"
          % (target["S"], target["E"], target["N"], target["W"]))
    out = dict(note=__doc__.strip().splitlines()[0],
               instrument="signed area asymmetry of the head either side of the haft",
               stills_target=target, best_bearing_deg=best[0], best_rms=best[1],
               sweep=curve)
    with open(os.path.join(OUT, "blade_bearing.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", os.path.join(OUT, "blade_bearing.json"))


main()
