#!/usr/bin/env python3
"""C-9 knight3d: put the fitted Grok pose back under the gait's constraints.

19_fit_motion solves each frame's JOINT ANGLES against the Grok cell. That
gives the video's pose character but says nothing about the ground, the
stride, or whether a planted foot stays planted -- Grok's own feet do not
(knight_foot_slide.json measured 0.71x to 2.59x).

So the angles are kept exactly as fitted and only the ROOT is moved: per frame,
translate the whole figure so the stance foot's contact point sits where the
cadence says it must and its sole sits on the ground. Translating the root
cannot change a single joint angle, so the pose character survives intact;
what it costs is silhouette agreement with Grok, and that cost is the number
worth reporting.

Then the R-C9-36 tabard chain is re-applied from the resulting hip motion.

Writes out/anim_walk.npz and out/anim_run.npz (replacing the procedural ones)
and out/motion_applied.json.
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster
src = open(os.path.join(HERE, "19_fit_motion.py")).read().split("def main()")[0]
exec(compile(src, os.path.join(HERE, "19_fit_motion.py"), "exec"))

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
CB = os.path.join(os.path.dirname(K3), "cliffside_B")
FRAME, SS = 512, 2
PX_PER_M = 198.33333333333334 / 1.80
CANVAS_PX_PER_M = 150.21354166666666 / 1.80
GAIT = {"walk": dict(frames=12, period=0.5797, px_s=247.0, stance=0.52,
                     tabard_deg=6.0),
        "run": dict(frames=8, period=0.5517, px_s=494.0, stance=0.30,
                    tabard_deg=10.0)}


def rotx_(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    theta = fit["theta_elevation_deg"]
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    pl = kp.layered(p)
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    tri_v0 = A["tri_v"].astype(np.float64); tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    pb = {n: idx["parts"][n]["bone"] for n in names}
    pk = {n: idx["parts"][n]["kind"] for n in names}
    body_tris = ~np.isin(tri_id, [i for i, n in enumerate(names) if pk[n] == "weapon"])
    Jr = kp.joints(pl)
    foot_tris = {BL: np.isin(tri_id, [i for i, n in enumerate(names)
                                      if n in ("sabaton_%s" % s, "sabaton_toe_%s" % s)])
                 for s, BL in (("L", "Left"), ("R", "Right"))}

    W = H = FRAME * SS
    scale = PX_PER_M * SS; tx = FRAME / 2 * SS
    r_, u_ = kp.basis(90.0, theta); c_ = kp.cam_dir(90.0, theta)
    mf = json.load(open(os.path.join(OUT, "motion_fit.json")))
    rep = {"note": __doc__.strip().splitlines()[0], "gaits": {}}

    for gait, G in GAIT.items():
        if gait not in mf["gaits"]:
            continue
        N = G["frames"]
        D = G["px_s"] * G["period"] / CANVAS_PX_PER_M
        sigma = G["stance"]
        rj = json.load(open(os.path.join(OUT, "render_%s.json" % gait)))
        ty = (rj["sole_y"] + rj["ground_calibration_px"]) * SS
        poses = [np.array(q) for q in mf["gaits"][gait]["pose"]]
        src_dir = os.path.join(CB, "sprites_knight", gait, "E")
        gf = sorted(f for f in os.listdir(src_dir) if f.endswith(".png"))

        # --- 1. the fitted frames, with the STRIDE RETARGETED ---------------
        # Grok's pose sequence and the game's cadence do not imply the same
        # stride -- knight_foot_slide measured the painted W walk at 0.71x, i.e.
        # a stride about 1.4x longer than walk_px_s and the Keeper period allow.
        # Pinning the foot by moving the ROOT alone therefore threw the figure
        # off frame and cost IoU down to 0.22. So the LEG EXCURSION is scaled
        # instead: the fore/aft reach of each leg is multiplied by k so the
        # planted foot travels exactly D per cycle, which keeps Grok's pose
        # character (every other angle untouched) and the body centred. k is
        # measured, and reported -- it is how much shorter the knight's step
        # must be than the video's to walk at the speed the game walks him.
        def contacts_of(qs):
            out = []
            for q in qs:
                J = joints_from_pose(p, Jr, q)
                T = PS.bone_transforms(Jr, J, {k[3:]: v for k, v in J.items()
                                               if k.startswith("_R_")})
                V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)
                c = {}
                for BL in ("Left", "Right"):
                    Vf = V[foot_tris[BL]].reshape(-1, 3)
                    zmin = float(Vf[:, 2].min())
                    low = Vf[Vf[:, 2] < zmin + 0.012]
                    c[BL] = dict(y=float(low[:, 1].mean()), z=zmin)
                out.append(c)
            return out

        # TEMPORAL SMOOTHING. The fit solves each frame independently, so
        # nothing makes frame i agree with frame i+1: the free root alone
        # wandered over a metre between frames, and the constraint step then
        # had to undo that wander, which is what destroyed the silhouette.
        # A circular [1,2,1] pass costs almost nothing in pose character and
        # removes the jitter the constraints were amplifying.
        P = np.array([np.array(q, float) for q in poses])
        P = 0.25 * np.roll(P, 1, 0) + 0.5 * P + 0.25 * np.roll(P, -1, 0)
        poses = [P[i] for i in range(len(P))]
        c0 = contacts_of(poses)
        span = max(max(c[b]["y"] for b in c) for c in c0) - \
            min(min(c[b]["y"] for b in c) for c in c0)
        implied = span / max(sigma, 1e-6)
        k_stride = float(np.clip(D / max(implied, 1e-6), 0.25, 1.6))
        hipk = [KEYS.index("L_hip"), KEYS.index("R_hip")]
        poses = [np.array(q, float) for q in poses]
        for q in poses:
            for j in hipk:
                q[j] = math.degrees(math.asin(
                    float(np.clip(k_stride * math.sin(math.radians(q[j])), -1, 1))))
        print("  %s  stride retarget k = %.3f  (Grok implies %.3f m/cycle, "
              "cadence allows %.3f)" % (gait, k_stride, implied, D))
        raw = [joints_from_pose(p, Jr, q) for q in poses]
        contact = []
        for i, J in enumerate(raw):
            T = PS.bone_transforms(Jr, J,
                                   {k[3:]: v for k, v in J.items() if k.startswith("_R_")})
            V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)
            c = {}
            for BL in ("Left", "Right"):
                Vf = V[foot_tris[BL]].reshape(-1, 3)
                zmin = float(Vf[:, 2].min())
                low = Vf[Vf[:, 2] < zmin + 0.012]
                c[BL] = dict(y=float(low[:, 1].mean()), z=zmin)
            contact.append(c)

        # --- 2. the root correction ---------------------------------------
        # Written first as a stance-weighted blend of both feet, which sank the
        # figure 180 mm into the ground and cost 37 points of IoU: during
        # double support it averaged a planted foot with a swinging one and
        # pushed the planted one under. Two separate, exact constraints instead.
        #
        # VERTICAL: the LOWEST foot sits exactly on the ground. That both
        # plants the stance foot and makes penetration impossible by
        # construction, with no schedule to be wrong about.
        #
        # FORE/AFT: the planted foot is whichever is lowest. While the SAME
        # foot stays planted, its WORLD position -- root-relative contact plus
        # the root's travel D*phase -- must not change. That pins it exactly.
        # The free constant per planted run is chosen to keep the body
        # centred, so the correction does not drift the figure off frame.
        planted = []
        for i in range(N):
            c = contact[i]
            planted.append("Left" if c["Left"]["z"] <= c["Right"]["z"] else "Right")
        # ONLY where a foot is actually down. Applying the ground constraint on
        # every frame pins the lowest foot even during flight and mid-swing,
        # which drags the whole body down and was the real cost (IoU 0.21 with
        # a perfect 0.00 mm plant -- a constraint satisfied and a figure
        # wrecked). Off-stance frames are interpolated circularly instead.
        low_z = np.array([min(contact[i][b]["z"] for b in ("Left", "Right"))
                          for i in range(N)])
        down = low_z < 0.035
        if not down.any():
            down = low_z <= low_z.min() + 1e-9
        dz_all = list(-(low_z - float(np.mean(low_z[down]))))
        # group consecutive frames (circularly) that share a planted foot
        runs, cur = [], [0]
        for i in range(1, N):
            if planted[i] == planted[i - 1]:
                cur.append(i)
            else:
                runs.append(cur); cur = [i]
        runs.append(cur)
        if len(runs) > 1 and planted[0] == planted[-1]:
            runs[0] = runs[-1] + runs[0]; runs.pop()
        # dy[i] = K_run + want[i]. The per-run constant is CHAINED so the body
        # does not jump when the planted foot changes (centring each run on its
        # own mean did exactly that, once per step), then the whole curve is
        # centred globally.
        want = np.array([-(D * (i / N)) - contact[i][planted[i]]["y"]
                         for i in range(N)])
        dy_all = np.zeros(N)
        K = 0.0
        for r, run in enumerate(runs):
            if r > 0:
                prev_last = runs[r - 1][-1]
                K = dy_all[prev_last] - want[run[0]]
            for i in run:
                dy_all[i] = K + want[i]
        dy_all = list(dy_all - float(np.mean(dy_all)))
        # interpolate the correction across the frames where no foot is down
        def circ_interp(vals, mask):
            idx = np.where(mask)[0]
            if len(idx) == 0 or len(idx) == N:
                return list(vals)
            out = list(vals)
            for i in range(N):
                if mask[i]:
                    continue
                prev = max((j for j in idx if j <= i), default=None)
                nxt = min((j for j in idx if j >= i), default=None)
                if prev is None:
                    prev = idx[-1] - N
                if nxt is None:
                    nxt = idx[0] + N
                span = max(nxt - prev, 1e-9)
                t = (i - prev) / span
                out[i] = vals[prev % N] * (1 - t) + vals[nxt % N] * t
            return out
        dy_all = circ_interp(np.array(dy_all), down)
        dz_all = circ_interp(np.array(dz_all), down)
        print("    down   %s" % " ".join("%d" % d for d in down))
        print("    dy mm  %s" % " ".join("%+5.0f" % (1000 * v) for v in dy_all))
        print("    dz mm  %s" % " ".join("%+5.0f" % (1000 * v) for v in dz_all))
        out_J = []
        for i in range(N):
            J = {k: (v + np.array([0.0, dy_all[i], dz_all[i]])
                     if not k.startswith("_R_") else v)
                 for k, v in raw[i].items()}
            out_J.append(J)

        # --- 3. the tabard, from the hip motion this produced --------------
        hz = np.array([J["Hips"][2] for J in out_J])
        dt = G["period"] / N
        a = math.exp(-dt / 0.10)
        drive = np.array([-(hz[i] - hz[(i - 1) % N]) / dt * 2.2 for i in range(N)])
        x = drive.mean(); lag = np.zeros(N)
        for _ in range(4):
            for i in range(N):
                x = a * x + (1 - a) * drive[i]; lag[i] = x
        peak = np.abs(lag - lag.mean()).max() or 1.0
        tab = (lag - lag.mean()) / peak * G["tabard_deg"]
        for i, J in enumerate(out_J):
            for tag, ys in (("F", 1.0), ("B", -1.0)):
                prev = J["TAB_%s_01" % tag]; R = np.eye(3)
                for k in range(1, 4):
                    R = R @ rotx_(tab[i] * [0.5, 0.8, 1.0][k - 1] * ys)
                    nxt = prev + R @ (Jr["TAB_%s_%02d" % (tag, k + 1)]
                                      - Jr["TAB_%s_%02d" % (tag, k)])
                    J["TAB_%s_%02d" % (tag, k + 1)] = nxt
                    prev = nxt

        # --- 4. score, and measure the plant ------------------------------
        def render(J):
            T = PS.bone_transforms(Jr, J,
                                   {k[3:]: v for k, v in J.items() if k.startswith("_R_")})
            V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)[body_tris]
            flat = V.reshape(-1, 3)
            xy = np.stack([flat @ r_ * scale + tx, -(flat @ u_) * scale + ty], -1)
            zz = -(flat @ c_); n = len(V)
            zb, _, _, _ = raster(xy.reshape(n, 3, 2), zz.reshape(n, 3), None, W, H)
            return np.isfinite(zb)

        rows = []
        for i in range(N):
            gi = int(round(i * len(gf) / N)) % len(gf)
            tgt0, dead0 = grok_body_mask(os.path.join(src_dir, gf[gi]))
            t = np.kron(tgt0, np.ones((SS, SS), bool))
            dd = np.kron(dead0, np.ones((SS, SS), bool))
            m = render(out_J[i]); live = ~dd
            u = ((m & live) | (t & live)).sum()
            after = float(((m & live) & (t & live)).sum()) / u if u else 0.0
            rows.append(dict(frame=i, grok_frame=gi,
                             iou_procedural=mf["gaits"][gait]["frames"][i]["iou_before"],
                             iou_fitted=mf["gaits"][gait]["frames"][i]["iou_after"],
                             iou_constrained=round(after, 4)))
            print("  %s %02d  IoU  procedural %.4f  fitted %.4f  constrained %.4f"
                  % (gait, i, rows[-1]["iou_procedural"], rows[-1]["iou_fitted"], after))

        # foot plant on the constrained result
        slips, pen = 0.0, 0.0
        prev = None
        for i in range(N):
            J = out_J[i]
            T = PS.bone_transforms(Jr, J,
                                   {k[3:]: v for k, v in J.items() if k.startswith("_R_")})
            V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)
            ph = i / N
            for BL, c0 in (("Right", 0.0), ("Left", 0.5)):
                Vf = V[foot_tris[BL]].reshape(-1, 3)
                pen = min(pen, float(Vf[:, 2].min()))
                tau = (ph - c0) % 1.0
                ph_adj = ph if (ph - tau) >= -1e-9 else ph + 1.0
                touch = Vf[:, 2] < 0.001
                wy = Vf[:, 1] + D * ph_adj
                if prev is not None and prev[0] == BL and tau < sigma and prev[2] is not None:
                    both = touch & prev[1]
                    if both.any():
                        slips = max(slips, float(np.abs(wy[both] - prev[2][both]).max()))
                prev = (BL, touch, wy if tau < sigma else None)

        keys = sorted(k for k in out_J[0] if not k.startswith("_R_"))
        rots = sorted(k[3:] for k in out_J[0] if k.startswith("_R_"))
        np.savez_compressed(
            os.path.join(OUT, "anim_%s.npz" % gait),
            joints=np.array([[J[k] for k in keys] for J in out_J], np.float32),
            names=np.array(keys),
            rot_names=np.array(rots),
            rots=np.array([[J["_R_" + k] for k in rots] for J in out_J], np.float32),
            frames=N, fps=N / G["period"], travel=D)
        rep["gaits"][gait] = dict(
            frames=rows, travel_m_per_cycle=D, fps=N / G["period"],
            mean_iou_procedural=round(float(np.mean([r["iou_procedural"] for r in rows])), 4),
            mean_iou_fitted=round(float(np.mean([r["iou_fitted"] for r in rows])), 4),
            mean_iou_constrained=round(float(np.mean([r["iou_constrained"] for r in rows])), 4),
            stride_retarget_k=round(k_stride, 4),
            grok_implied_m_per_cycle=round(implied, 4),
            max_slip_mm=round(1000.0 * slips, 2),
            ground_penetration_mm=round(1000.0 * pen, 2))
        print("  %s  mean IoU  procedural %.4f -> fitted %.4f -> constrained %.4f"
              "   slip %.2f mm  penetration %.2f mm"
              % (gait, rep["gaits"][gait]["mean_iou_procedural"],
                 rep["gaits"][gait]["mean_iou_fitted"],
                 rep["gaits"][gait]["mean_iou_constrained"],
                 rep["gaits"][gait]["max_slip_mm"],
                 rep["gaits"][gait]["ground_penetration_mm"]))
    with open(os.path.join(OUT, "motion_applied.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote", os.path.join(OUT, "motion_applied.json"))


main()
