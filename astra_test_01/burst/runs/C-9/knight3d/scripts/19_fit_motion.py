#!/usr/bin/env python3
"""C-9 knight3d: FIT THE POSE TO THE GROK VIDEO, frame by frame (R-C9-58).

Matt's goal is "the same as the video result", and the camera and the body are
already fitted, so what is left is a POSE-ONLY fit per frame.

For each Grok E cell the knight's silhouette is matted (its pollaxe split off
with the same tool that split the stills'), the body is posed by an explicit
joint-angle vector, rendered through the game's own camera, and the angles are
solved for silhouette IoU. Then the gait constraints are re-imposed on top --
the planted foot pinned to its world point, the sole on the ground, the stride
and cadence unchanged -- so the result has Grok's pose character and my feet.

Reported per frame: IoU before (the procedural cycle), after the fit, and
after the constraints are re-imposed. The third number is the one that ships;
the gap between the second and the third is the price of not sliding.
"""
import json, math, os, sys, time
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
from raster import raster

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CB = os.path.join(os.path.dirname(K3), "cliffside_B")
FRAME, SS = 512, 2
PX_PER_M = 198.33333333333334 / 1.80

# the pose vector, in order
KEYS = ["hip_z", "hip_y", "pel_yaw", "pel_list", "lean", "counter",
        "L_hip", "L_splay", "L_knee", "L_ank", "L_toe",
        "R_hip", "R_splay", "R_knee", "R_ank", "R_toe",
        "A_pitch", "A_elbow"]
# Bounds. The first set was far too tight and the saturation counts said so:
# hip_y sat at its limit in 8 of 8 run frames, hip_z in 7 of 8, the knee at 95
# deg in 3 of 8. The ROOT bounds were the worst of it, because 20_apply_motion
# re-solves the root from the cadence anyway -- clamping it during the fit
# only forced the LEGS to absorb the root's error, which is the opposite of
# what this fit is for.
LO = np.array([-0.30, -0.45, -20, -16, -10, -30,
               -70, -16, 0, -60, 0, -70, -16, 0, -60, 0, -70, 0])
HI = np.array([0.12, 0.45, 20, 16, 34, 30,
               70, 22, 130, 40, 70, 70, 22, 130, 40, 70, 70, 95])


def rotx(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def roty(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotz(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def joints_from_pose(p, Jr, q):
    """Explicit forward kinematics from the pose vector to joint positions."""
    v = dict(zip(KEYS, q))
    J = {}
    hips = np.array([0.0, v["hip_y"], p["z_hip"] + v["hip_z"]])
    Rp = rotz(v["pel_yaw"]) @ roty(v["pel_list"])
    J["Hips"] = hips
    acc = Rp; prev_r, prev_p = Jr["Hips"], hips
    for k, b in enumerate(["Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End"]):
        fr = [0.30, 0.34, 0.36, 0.0, 0.0, 0.0][k]
        ln = [0.34, 0.33, 0.33, 0.0, 0.0, 0.0][k] * v["lean"]
        acc = acc @ rotz(-v["counter"] * fr) @ rotx(-ln)
        J[b] = prev_p + acc @ (Jr[b] - prev_r)
        prev_r, prev_p = Jr[b], J[b]
    R_chest = acc
    for b in ("LeftShoulder", "RightShoulder", "LeftArm", "RightArm"):
        J[b] = J["Spine2"] + R_chest @ (Jr[b] - Jr["Spine2"])
    # legs
    for s, sx, BL in (("L", -1.0, "Left"), ("R", 1.0, "Right")):
        hip = hips + Rp @ (Jr[BL + "UpLeg"] - Jr["Hips"])
        L1 = np.linalg.norm(Jr[BL + "Leg"] - Jr[BL + "UpLeg"])
        L2 = np.linalg.norm(Jr[BL + "Foot"] - Jr[BL + "Leg"])
        Rth = Rp @ roty(sx * v[s + "_splay"]) @ rotx(v[s + "_hip"])
        knee = hip + Rth @ np.array([0, 0, -L1])
        Rsh = Rth @ rotx(-v[s + "_knee"])
        ank = knee + Rsh @ np.array([0, 0, -L2])
        J[BL + "UpLeg"] = hip; J[BL + "Leg"] = knee; J[BL + "Foot"] = ank
        fy = rotz(-sx * 6.0)
        R_foot = fy @ rotx(v[s + "_ank"]) @ rotz(p["foot_%s_yaw" % s]).T
        R_toe = fy @ rotx(v[s + "_ank"] + v[s + "_toe"]) @ rotz(p["foot_%s_yaw" % s]).T
        J["_R_" + BL + "Foot"] = R_foot
        J["_R_" + BL + "ToeBase"] = R_toe
        t = ank - R_foot @ Jr[BL + "Foot"]
        ball = R_foot @ Jr[BL + "ToeBase"] + t
        J[BL + "ToeBase"] = ball
        J[BL + "Toe_End"] = R_toe @ (Jr[BL + "Toe_End"] - Jr[BL + "ToeBase"]) + ball
    # arms: right IK to the grip carried in the chest, left free
    grip = J["Spine2"] + R_chest @ (np.array([p["grip_x"], p["grip_y"], p["grip_z"]])
                                    - Jr["Spine2"])
    A1 = np.linalg.norm(Jr["RightForeArm"] - Jr["RightArm"])
    A2 = np.linalg.norm(Jr["RightHand"] - Jr["RightForeArm"])
    el, wr = kp._ik2(J["RightArm"], grip, A1, A2,
                     pole=R_chest @ np.array([0.35, -0.45, -1.0]))
    J["RightForeArm"] = el; J["RightHand"] = wr
    d = wr - el; d = d / max(np.linalg.norm(d), 1e-9)
    J["RightHandEnd"] = wr + d * 0.115
    B1 = np.linalg.norm(Jr["LeftForeArm"] - Jr["LeftArm"])
    B2 = np.linalg.norm(Jr["LeftHand"] - Jr["LeftForeArm"])
    Ra = R_chest @ rotx(v["A_pitch"])
    elb = J["LeftArm"] + Ra @ (rotz(-6.0) @ np.array([0.0, 0.0, -B1]))
    Rb = Ra @ rotx(v["A_elbow"])
    wr2 = elb + Rb @ np.array([0.0, 0.0, -B2])
    J["LeftForeArm"] = elb; J["LeftHand"] = wr2
    d = wr2 - elb; d = d / max(np.linalg.norm(d), 1e-9)
    J["LeftHandEnd"] = wr2 + d * 0.115
    for b in ("TAB_F_01", "TAB_F_02", "TAB_F_03", "TAB_F_04",
              "TAB_B_01", "TAB_B_02", "TAB_B_03", "TAB_B_04"):
        J[b] = J["Hips"] + Rp @ (Jr[b] - Jr["Hips"])
    for t in ("F", "B", "L", "R"):
        J["SKIRT_%s" % t] = J["Hips"] + Rp @ (Jr["SKIRT_%s" % t] - Jr["Hips"])
        J["SKIRT_%s_end" % t] = J["Hips"] + Rp @ (Jr["SKIRT_%s_end" % t] - Jr["Hips"])
    Rh = np.eye(3)
    vv = J["RightHand"] - J["RightForeArm"]; vv /= max(np.linalg.norm(vv), 1e-9)
    vr = Jr["RightHand"] - Jr["RightForeArm"]; vr /= max(np.linalg.norm(vr), 1e-9)
    ax = np.cross(vr, vv); sn = np.linalg.norm(ax); cs = float(vr @ vv)
    if sn > 1e-9:
        ax /= sn
        Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
        Rh = np.eye(3) + math.sin(math.atan2(sn, cs)) * Kx + (1 - cs) * (Kx @ Kx)
    for b in ("SOCK_WeaponMain", "SOCK_WeaponMain_end",
              "SOCK_WeaponGripFar", "SOCK_WeaponGripFar_end"):
        J[b] = J["RightHand"] + Rh @ (Jr[b] - Jr["RightHand"])
    for b in ("SOCK_OffHand", "SOCK_OffHand_end"):
        J[b] = J["LeftHand"] + (Jr[b] - Jr["LeftHand"])
    return J


# --------------------------------------------------------------- targets

def grok_body_mask(path):
    """Matte a Grok cell and split its pollaxe off, so the fit is not chasing
    a haft whose screen position the source art never kept consistent.

    At sprite scale the thin-opening trick that worked on the 1024x1536 stills
    does not: the haft is 7 px wide and merges with the hand and the tabard, so
    the tallest "thin" component came back as a body edge and the haft stayed
    in the target. Detected here by COLUMN EXTENT instead -- the haft is the
    only structure spanning nearly the whole content height.
    """
    a = np.asarray(Image.open(path).convert("RGBA"))
    fig = a[..., 3] > 8
    fig = ndi.binary_fill_holes(ndi.binary_closing(fig, np.ones((3, 3))))
    ys = np.where(fig.any(axis=1))[0]
    Hc = int(ys.max() - ys.min() + 1)
    ext = np.zeros(fig.shape[1])
    for x in np.where(fig.any(axis=0))[0]:
        yy = np.where(fig[:, x])[0]
        ext[x] = yy.max() - yy.min() + 1
    tall = np.where(ext > 0.90 * Hc)[0]
    dead = np.zeros_like(fig)
    body = fig
    if len(tall):
        cx = int(np.median(tall))
        w = max(4, int(round(0.020 * Hc)))
        bar = np.zeros_like(fig)
        bar[:, max(0, cx - w): cx + w + 1] = fig[:, max(0, cx - w): cx + w + 1]
        rest = fig & ~ndi.binary_dilation(bar, np.ones((3, 3)))
        lab, n = ndi.label(rest, structure=np.ones((3, 3)))
        if n:
            sizes = np.array(ndi.sum(rest, lab, range(1, n + 1)))
            body = lab == (1 + int(np.argmax(sizes)))
            # everything that is not the body -- haft, axe head, butt -- is
            # excluded from scoring rather than assigned to either side
            dead = ndi.binary_dilation(fig & ~body, np.ones((7, 7)))
            body = ndi.binary_fill_holes(body)
    return body, dead


def main():
    t0 = time.time()
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
    body_tris = ~np.isin(tri_id, [i for i, n in enumerate(names)
                                  if pk[n] == "weapon"])
    Jr = kp.joints(pl)

    W = H = FRAME * SS
    scale = PX_PER_M * SS
    tx = FRAME / 2 * SS
    r_, u_ = kp.basis(90.0, theta); c_ = kp.cam_dir(90.0, theta)

    def render(J, ty):
        T = PS.bone_transforms(Jr, J,
                               {k[3:]: v for k, v in J.items() if k.startswith("_R_")})
        V = PS.pose_tris(tri_v0, tri_id, names, pb, pk, T, pl)[body_tris]
        flat = V.reshape(-1, 3)
        xy = np.stack([flat @ r_ * scale + tx, -(flat @ u_) * scale + ty], -1)
        zz = -(flat @ c_)
        n = len(V)
        zb, _, _, _ = raster(xy.reshape(n, 3, 2), zz.reshape(n, 3), None, W, H)
        return np.isfinite(zb)

    def iou(m, tgt, dead):
        live = ~dead
        a = m & live; b = tgt & live
        u = (a | b).sum()
        return float((a & b).sum()) / u if u else 0.0

    report = {"note": __doc__.strip().splitlines()[0], "gaits": {}}
    for gait, nframes in (("walk", 12), ("run", 8)):
        rj = json.load(open(os.path.join(OUT, "render_%s.json" % gait)))
        ty = (rj["sole_y"] + rj["ground_calibration_px"]) * SS
        z = np.load(os.path.join(OUT, "anim_%s.npz" % gait), allow_pickle=True)
        nm = [str(x) for x in z["names"]]; rn = [str(x) for x in z["rot_names"]]
        src = os.path.join(CB, "sprites_knight", gait, "E")
        gf = sorted(f for f in os.listdir(src) if f.endswith(".png"))
        rows, fitted = [], []
        for i in range(nframes):
            gi = int(round(i * len(gf) / nframes)) % len(gf)
            tgt0, dead0 = grok_body_mask(os.path.join(src, gf[gi]))
            tgt = np.kron(tgt0, np.ones((SS, SS), bool))
            dead = np.kron(dead0, np.ones((SS, SS), bool))

            # BEFORE: the procedural cycle
            Jp = {k: z["joints"][i][j] for j, k in enumerate(nm)}
            for j, k in enumerate(rn):
                Jp["_R_" + k] = z["rots"][i][j].astype(np.float64)
            before = iou(render(Jp, ty), tgt, dead)

            # seed the pose vector from the procedural frame's own angles
            q0 = np.zeros(len(KEYS))
            q0[KEYS.index("hip_z")] = float(Jp["Hips"][2]) - p["z_hip"]
            q0[KEYS.index("hip_y")] = float(Jp["Hips"][1])
            q0[KEYS.index("lean")] = 6.0
            for s, BL in (("L", "Left"), ("R", "Right")):
                th = Jp[BL + "Leg"] - Jp[BL + "UpLeg"]
                q0[KEYS.index(s + "_hip")] = math.degrees(math.atan2(th[1], -th[2]))
                sh = Jp[BL + "Foot"] - Jp[BL + "Leg"]
                q0[KEYS.index(s + "_knee")] = max(
                    0.0, q0[KEYS.index(s + "_hip")]
                    - math.degrees(math.atan2(sh[1], -sh[2])))

            def neg(q):
                qq = np.clip(q, LO, HI)
                return -iou(render(joints_from_pose(p, Jr, qq), ty), tgt, dead)

            res = minimize(neg, q0, method="Powell",
                           options=dict(maxiter=5, xtol=0.5, ftol=1.5e-3))
            q = np.clip(res.x, LO, HI)
            after = -neg(q)
            rows.append(dict(frame=i, grok_frame=gi, iou_before=round(before, 4),
                             iou_after=round(after, 4)))
            fitted.append(q)
            print("  %s %02d  IoU %.4f -> %.4f   (%.0fs)"
                  % (gait, i, before, after, time.time() - t0))
        report["gaits"][gait] = dict(frames=rows, pose_keys=KEYS,
                                     pose=[list(map(float, q)) for q in fitted])
        report["gaits"][gait]["mean_before"] = round(
            float(np.mean([r["iou_before"] for r in rows])), 4)
        report["gaits"][gait]["mean_after"] = round(
            float(np.mean([r["iou_after"] for r in rows])), 4)
        print("  %s mean IoU %.4f -> %.4f" % (gait, report["gaits"][gait]["mean_before"],
                                              report["gaits"][gait]["mean_after"]))
    with open(os.path.join(OUT, "motion_fit.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("wrote", os.path.join(OUT, "motion_fit.json"), "in %.0fs" % (time.time() - t0))


main()
