#!/usr/bin/env python3
"""C-9 knight3d: verify the pollaxe fix (R-C9-57).

Two checks, both on the BUILT mesh, not on the parameters:
  1. SIDE -- render the weapon alone at each of the eight fitted cameras and
     measure the head's signed area asymmetry either side of the haft, the
     same instrument 15_blade_side ran on the stills. The SIGN must match the
     stills in every view; that is what Matt reported wrong.
  2. CLEARANCE -- the closest approach between any weapon vertex and any helm
     or gorget vertex, in the rest pose and across every walk and run frame.
     "The blade no longer overlaps the helm" is a distance, so measure it.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta, ds = fit["theta_elevation_deg"], fit["downsample"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tri_v = A["tri_v"].astype(np.float64); tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    wid = [i for i, n in enumerate(names) if idx["parts"][n]["kind"] == "weapon"]
    hid = [i for i, n in enumerate(names) if n in ("helm", "visor", "gorget")]
    haftid = [i for i, n in enumerate(names) if n == "pollaxe_haft"]
    wsel = np.isin(tri_id, wid); hsel = np.isin(tri_id, hid)
    hafts = np.isin(tri_id, haftid)

    ref = json.load(open(os.path.join(OUT, "blade_side.json")))
    target = {r["view"]: (r["area_fwdside_px"] - r["area_backside_px"]) /
              (r["area_fwdside_px"] + r["area_backside_px"]) for r in ref["per_view"]}

    W, H = 1024, 1536
    side = {}
    ok = True
    for d in DIRS:
        v = fit["canonical"]["views"][d]
        s = v["scale"] * ds; tx = v["tx"] * ds; ty = v["ty"] * ds
        r_, u_ = kp.basis(v["alpha"], theta); c_ = kp.cam_dir(v["alpha"], theta)
        def proj(sel):
            flat = tri_v[sel].reshape(-1, 3)
            xy = np.stack([flat @ r_ * s + tx, -(flat @ u_) * s + ty], -1)
            z = -(flat @ c_)
            n = int(sel.sum())
            return raster(xy.reshape(n, 3, 2), z.reshape(n, 3), None, W, H)[0]
        zw = proj(wsel); zh = proj(hafts)
        solid = np.isfinite(zw); haft = np.isfinite(zh)
        ys = np.where(solid.any(axis=1))[0]
        hy = np.where(haft.any(axis=1))[0]
        hwid = float(np.median([int(haft[y].sum()) for y in hy]))
        widp = np.array([int(solid[y].sum()) for y in ys])
        head = ys[widp > hwid * 2.2]
        hx = np.array([float(np.where(haft[y])[0].mean()) for y in hy])
        m, cc = np.polyfit(hy.astype(float), hx, 1)
        yy, xx = np.where(solid[int(head.min()):int(head.max()) + 1])
        off = xx - (m * (yy + int(head.min())) + cc)
        o = off[np.abs(off) > hwid * 0.6]
        a = float(((o > 0).sum() - (o < 0).sum()) / max(len(o), 1))
        agree = (a > 0) == (target[d] > 0)
        ok &= agree
        side[d] = dict(render_asym=round(a, 4), still_asym=round(target[d], 4),
                       sign_agrees=bool(agree))
        print("  %-3s render %+.3f   still %+.3f   sign %s"
              % (d, a, target[d], "OK" if agree else "MISMATCH"))

    # --- clearance -------------------------------------------------------
    part_bone = {n: idx["parts"][n]["bone"] for n in names}
    part_kind = {n: idx["parts"][n]["kind"] for n in names}
    Jr = kp.joints(kp.layered(p))
    def gap(V):
        wv = V[wsel].reshape(-1, 3); hv = V[hsel].reshape(-1, 3)
        d = np.sqrt(((wv[:, None, :] - hv[None, :, :]) ** 2).sum(-1))
        return float(d.min())
    clear = {"rest_m": round(gap(tri_v), 4)}
    for name in ("walk", "run"):
        f = os.path.join(OUT, "anim_%s.npz" % name)
        if not os.path.exists(f):
            continue
        z = np.load(f, allow_pickle=True)
        nm = [str(x) for x in z["names"]]; rn = [str(x) for x in z["rot_names"]]
        mins = []
        for i in range(len(z["joints"])):
            Jp = {k: z["joints"][i][j] for j, k in enumerate(nm)}
            ov = {k: z["rots"][i][j].astype(np.float64) for j, k in enumerate(rn)}
            T = PS.bone_transforms(Jr, Jp, ov)
            V = PS.pose_tris(tri_v, tri_id, names, part_bone, part_kind, T, kp.layered(p))
            mins.append(gap(V))
        clear["%s_min_m" % name] = round(min(mins), 4)
        clear["%s_per_frame_m" % name] = [round(x, 4) for x in mins]
    print("\n  clearance weapon-to-helm/gorget: rest %.3f m, walk min %.3f m, run min %.3f m"
          % (clear["rest_m"], clear.get("walk_min_m", -1), clear.get("run_min_m", -1)))
    out = dict(note=__doc__.strip().splitlines()[0],
               head_bearing_deg=p["head_bearing_deg"],
               all_signs_agree=bool(ok), per_view=side, clearance=clear)
    with open(os.path.join(OUT, "weapon_verify.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("  ALL EIGHT SIGNS AGREE" if ok else "  SIGN MISMATCH -- not fixed")
    print("wrote", os.path.join(OUT, "weapon_verify.json"))


main()
