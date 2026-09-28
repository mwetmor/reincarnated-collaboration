#!/usr/bin/env python3
"""C-9 knight3d step 2: fit the orthographic camera the eight approved stills
were painted from, and fit the knight proxy's shape to them at the same time.

Free parameters
  theta      elevation, SHARED by all eight views (one camera, one game view)
  alpha_D    azimuth, one per view (nominal S 0, SE 45, E 90 ... SW 315)
  s,tx,ty    per view: pixels-per-metre and the image position of the world
             origin. Nuisance parameters -- the stills were painted at slightly
             different figure sizes -- and the spread of the fitted `s` is
             itself reported as a finding.
  shape      ~30 body dimensions + the rest pose, SHARED by all eight views.
  stage 3    per-view LEG and ARM pose deltas, to separate "the camera is
             wrong" from "this still's stance is not the other stills' stance".

Objective: silhouette IoU against the matted body masks, with the pollaxe and
the cut-ambiguity band excluded from BOTH sides (never assigned by guesswork).

Instrument note: IoU is not the whole check. 03_overlays.py draws the overlays
so the pose and the camera can be LOOKED at; a high IoU cannot tell a right
camera from a body that is merely the right size.
"""
import json, os, sys, math, time
import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
WORK = os.path.join(ROOT, "knight3d", "work")
MASKS = os.path.join(WORK, "masks")
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
NOMINAL = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
DS = 4                      # work at 1/4 resolution: the figure is ~222 px tall


def load_targets(ds=DS):
    T = {}
    for d in DIRS:
        body = np.load(os.path.join(MASKS, "%s_body.npy" % d))
        axe = np.load(os.path.join(MASKS, "%s_axe.npy" % d))
        amb = np.load(os.path.join(MASKS, "%s_amb.npy" % d))
        dead = ndi.binary_dilation(axe | amb, np.ones((9, 9)))
        b = body[::ds, ::ds]
        k = dead[::ds, ::ds]
        ys = np.where(b.any(axis=1))[0]
        T[d] = dict(body=np.ascontiguousarray(b), dead=np.ascontiguousarray(k),
                    H=b.shape[0], W=b.shape[1],
                    y_top=int(ys.min()), y_bot=int(ys.max()), area=int(b.sum()))
    return T


def iou(a, b, dead):
    live = ~dead
    A = a & live; B = b & live
    u = (A | B).sum()
    return float((A & B).sum()) / u if u else 0.0


def project_extent(parts, alpha, theta):
    allp = np.concatenate([p for _, _, p in parts], 0)
    xy = kp.project(allp, alpha, theta)
    return xy[:, 0].min(), xy[:, 0].max(), xy[:, 1].min(), xy[:, 1].max()


def fit_view(parts, tgt, alpha, theta, refine=2, seed=None):
    """Align the proxy to one target mask; return (iou, s, tx, ty)."""
    if seed is None:
        u0, u1, v0, v1 = project_extent(parts, alpha, theta)
        hpx = tgt["y_bot"] - tgt["y_top"] + 1
        s = hpx / max(v1 - v0, 1e-6)
        ty = tgt["y_top"] + v1 * s
        tx = float(np.where(tgt["body"])[1].mean()) - 0.5 * (u0 + u1) * s
    else:
        s, tx, ty = seed
    best = (iou(kp.rasterize(parts, alpha, theta, s, tx, ty, tgt["W"], tgt["H"]),
                tgt["body"], tgt["dead"]), s, tx, ty)
    step_s, step_t = 0.035, 4.0
    for _ in range(refine):
        improved = True
        while improved:
            improved = False
            b_i, b_s, b_x, b_y = best
            for ds_ in (-step_s, 0.0, step_s):
                for dx in (-step_t, 0.0, step_t):
                    for dy in (-step_t, 0.0, step_t):
                        if ds_ == dx == dy == 0.0:
                            continue
                        s2 = b_s * (1 + ds_); x2 = b_x + dx; y2 = b_y + dy
                        m = kp.rasterize(parts, alpha, theta, s2, x2, y2,
                                         tgt["W"], tgt["H"])
                        i2 = iou(m, tgt["body"], tgt["dead"])
                        if i2 > best[0]:
                            best = (i2, s2, x2, y2); improved = True
        step_s *= 0.4; step_t *= 0.4
    return best


def fit_all(parts, T, theta, half=20.0, coarse=4.0, fine=1.0):
    out = {}
    for d in DIRS:
        tgt = T[d]; best = None; n = NOMINAL[d]
        for a in np.arange(n - half, n + half + 1e-9, coarse):
            r = fit_view(parts, tgt, float(a), theta, refine=1)
            if best is None or r[0] > best[0]:
                best = (r[0], float(a)) + r[1:]
        a0 = best[1]
        for a in np.arange(a0 - coarse, a0 + coarse + 1e-9, fine):
            r = fit_view(parts, tgt, float(a), theta, refine=2)
            if r[0] > best[0]:
                best = (r[0], float(a)) + r[1:]
        out[d] = dict(iou=best[0], alpha=best[1], scale=best[2], tx=best[3], ty=best[4])
    return out


def fit_all_fixed(parts, T, theta, cur, refine=1):
    """Cheap re-fit: keep each view's azimuth, re-solve placement only."""
    out = {}
    for d in DIRS:
        f = cur[d]
        r = fit_view(parts, T[d], f["alpha"], theta, refine=refine,
                     seed=(f["scale"], f["tx"], f["ty"]))
        out[d] = dict(iou=r[0], alpha=f["alpha"], scale=r[1], tx=r[2], ty=r[3])
    return out


def score(fits):
    return float(np.mean([f["iou"] for f in fits.values()]))


# per-view pose keys, stage 3
PERVIEW_POSE = ["leg_L_pitch", "leg_R_pitch", "leg_L_splay", "leg_R_splay",
                "knee_L_pitch", "knee_R_pitch", "foot_L_yaw", "foot_R_yaw",
                "arm_L_pitch", "arm_L_roll", "fore_L_pitch",
                "grip_x", "grip_y", "grip_z"]

SHAPE_DESCENT = kp.SHAPE_KEYS + [
    "grip_x", "grip_y", "grip_z",
    "arm_L_pitch", "arm_L_roll", "fore_L_pitch",
    "leg_L_splay", "leg_R_splay", "leg_L_pitch", "leg_R_pitch",
    "foot_L_yaw", "foot_R_yaw",
    "z_hip", "z_knee", "z_shoulder", "z_neck", "z_waist",
    "arm_len_upper", "arm_len_fore", "gorget_r", "waist_rx", "waist_ry",
    "visor_r", "visor_y", "helm_y", "foot_h", "toe_frac", "foot_heel_back",
    "z_ankle", "tabard_t", "fauld_z_bot", "skirt_r_top",
]


def descend(p, T, theta, cur, keys, fracs, tag, t0):
    best_s = score(cur)
    for rnd, frac in enumerate(fracs):
        for k in keys:
            base = p[k]
            step = abs(base) * frac if abs(base) > 1e-6 else frac
            if k.endswith(("pitch", "roll", "yaw", "splay")):
                step = max(4.0 * (0.6 ** rnd), 0.8)
            for delta in (+step, -step):
                v = base + delta
                lo, hi = kp.SHAPE_BOUNDS.get(k, (None, None))
                if lo is not None and not (lo <= v <= hi):
                    continue
                q = dict(p); q[k] = v
                f = fit_all_fixed(kp.build(q), T, theta, cur)
                sc = score(f)
                if sc > best_s + 1e-5:
                    p, best_s, cur, base = q, sc, f, v
        print("   %s round %d: mean IoU %.4f  (%.0fs)" % (tag, rnd, best_s, time.time() - t0))
    return p, cur, best_s


def main():
    t0 = time.time()
    T = load_targets()
    p = dict(kp.DEFAULTS)
    if os.environ.get("K3D_WARM") and os.path.exists(os.path.join(WORK, "fit_result.json")):
        prev = json.load(open(os.path.join(WORK, "fit_result.json")))
        for k, v in prev["params"].items():
            if k in p:
                p[k] = v
        print("warm start from the previous fit_result.json")

    # ELEVATION IS PINNED, not searched.
    #
    # A free elevation is very nearly degenerate with the body's aspect ratio
    # times the per-view scale, and both of those are also free here. Evidence,
    # from the free-theta run kept at work/fit_freetheta.log: sweeping theta
    # from 0 to 40 deg moved the mean IoU only from 0.6507 to 0.6836 -- a flat
    # 0.033 over forty degrees -- while the fitted azimuths wandered by ten
    # degrees. That optimum is not a measurement of the camera.
    #
    # 02b_elevation_probe.py measures theta from GROUND CONTACTS only (the two
    # soles are ground points; their screen separation in each view is fixed by
    # one stance and one elevation), which no body parameter can absorb:
    #   theta = 19.77 deg, leave-one-out range 18.2 - 23.1 deg.
    probe = json.load(open(os.path.join(WORK, "elevation_probe.json")))
    theta = float(os.environ.get("K3D_THETA", probe["ground_contact_lsq"]["theta_deg"]))
    print("elevation PINNED at %.2f deg (ground-contact probe)" % theta)

    print("pass 1: azimuth + placement at the pinned elevation")
    cur = fit_all(kp.build(p), T, theta, half=26, coarse=4, fine=1)
    print("   start mean IoU %.4f  alphas %s" %
          (score(cur), " ".join("%s:%.0f" % (d, cur[d]["alpha"]) for d in DIRS)))

    print("pass 2: shape descent (elevation held)")
    for cycle in range(3):
        p, cur, best_s = descend(p, T, theta, cur, SHAPE_DESCENT,
                                 (0.12, 0.05), "shape c%d" % cycle, t0)
        cur = fit_all(kp.build(p), T, theta, half=8, coarse=2, fine=0.5)
        best_s = score(cur)
        print("   cycle %d: mean IoU %.4f  (%.0fs)" % (cycle, best_s, time.time() - t0))

    print("pass 3: final azimuth refine at fitted elevation")
    parts = kp.build(p)
    cur = fit_all(parts, T, theta, half=10, coarse=2, fine=0.5)
    canon = {d: dict(cur[d]) for d in DIRS}
    canon_score = score(cur)
    print("   canonical (one body, one pose) mean IoU %.4f" % canon_score)

    print("pass 4: per-view pose deltas (how much the stills disagree)")
    perview = {}
    for d in DIRS:
        q = dict(p); f = dict(canon[d]); bs = f["iou"]
        for rnd, st in enumerate((6.0, 2.5, 1.0)):
            for k in PERVIEW_POSE:
                base = q[k]
                step = st if k.endswith(("pitch", "roll", "yaw", "splay")) else 0.03 * (0.5 ** rnd)
                for delta in (+step, -step):
                    q2 = dict(q); q2[k] = base + delta
                    r = fit_view(kp.build(q2), T[d], f["alpha"], theta, refine=1,
                                 seed=(f["scale"], f["tx"], f["ty"]))
                    if r[0] > bs + 1e-5:
                        q, bs, base = q2, r[0], base + delta
                        f.update(iou=r[0], scale=r[1], tx=r[2], ty=r[3])
            # let the azimuth move again now that the pose is this view's own
            for a in np.arange(f["alpha"] - 6, f["alpha"] + 6.01, 1.0):
                r = fit_view(kp.build(q), T[d], float(a), theta, refine=1,
                             seed=(f["scale"], f["tx"], f["ty"]))
                if r[0] > bs + 1e-5:
                    bs = r[0]; f.update(iou=r[0], alpha=float(a), scale=r[1], tx=r[2], ty=r[3])
        perview[d] = dict(f, delta={k: round(q[k] - p[k], 4) for k in PERVIEW_POSE
                                    if abs(q[k] - p[k]) > 1e-6})
        print("   %-3s canonical %.4f -> pose-fitted %.4f  alpha %.1f (nominal %d)" %
              (d, canon[d]["iou"], bs, f["alpha"], NOMINAL[d]))

    print("pass 5: elevation sensitivity at the fitted body (reported, not used)")
    sens = {}
    for th in [0, 5, 10, 15, 20, 25, 30, 35, 40]:
        f = fit_all(kp.build(p), T, float(th), half=8, coarse=2, fine=1)
        sens[th] = score(f)
        print("   theta=%4.1f  mean IoU %.4f" % (th, sens[th]))

    res = dict(
        theta_sensitivity=sens,
        theta_source="02b_elevation_probe.py ground-contact least squares",
        note="C-9 knight3d M-a: fitted orthographic camera + fitted knight proxy. "
             "IoU is silhouette IoU against the matted still, with the pollaxe "
             "and the cut-ambiguity band excluded from BOTH sides. Working "
             "resolution 1/%d of the 1024x1536 stills." % DS,
        downsample=DS,
        theta_elevation_deg=theta,
        canonical=dict(
            mean_iou=canon_score,
            views={d: dict(canon[d], nominal_alpha=NOMINAL[d],
                           alpha_residual=float(((canon[d]["alpha"] - NOMINAL[d] + 180) % 360) - 180),
                           scale_px_per_m_fullres=canon[d]["scale"] * DS) for d in DIRS}),
        pose_fitted=dict(
            mean_iou=float(np.mean([perview[d]["iou"] for d in DIRS])),
            views={d: dict(perview[d], nominal_alpha=NOMINAL[d],
                           alpha_residual=float(((perview[d]["alpha"] - NOMINAL[d] + 180) % 360) - 180),
                           scale_px_per_m_fullres=perview[d]["scale"] * DS) for d in DIRS}),
        params=p,
        seconds=time.time() - t0,
    )
    with open(os.path.join(WORK, "fit_result.json"), "w") as f:
        json.dump(res, f, indent=1)
    print("wrote fit_result.json in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
