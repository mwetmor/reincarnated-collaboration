#!/usr/bin/env python3
"""C-9 knight3d: solve the WHOLE CYCLE at once, with the plant inside the
objective (R-C9-59).

The previous attempt fitted each frame's pose on its own and then tried to pin
the feet afterwards. That cannot work, and the diagnosis was: a silhouette
barely constrains fore/aft position, so a free root wanders over a metre
between frames, and the pinning step then has to undo that wander -- which is
what moved the figure off its own outline. Four different pinning
constructions each satisfied their constraint exactly and each destroyed the
silhouette.

The structural fix, in three parts:

1. THE ROOT IS NEVER FREE. It is not a search variable at all. Given a cycle
   of joint angles, the root trajectory is DETERMINED by the constraints and
   recovered by a small linear least squares:

       root_y[i] + contact_y_f(i) + D*phase_i  =  W_f     (foot f in stance)
       root_z[i] + contact_z_f(i)              =  0       (foot f in stance)

   with one pin W_f per foot per cycle, a smoothness term that carries the
   root through flight frames, and a zero-mean term that keeps the figure
   centred. Fourteen unknowns, solved exactly, every objective evaluation.

   The RESIDUAL of that solve is the slip -- the amount by which the pose's own
   stance width disagrees with the stride it is being asked to cover -- and it
   is added to the cost. So the optimiser is pushed toward angles whose pins
   are mutually consistent, instead of being handed an inconsistency to paper
   over afterwards.

2. PERIODICITY BY CONSTRUCTION. Each joint channel is a truncated Fourier
   series in cycle phase, so frame N is frame 0 by identity, and the world has
   advanced exactly one stride because the root solve is written in terms of
   D*phase. Nothing has to be stitched at the loop point.

3. COARSE TO FINE. Harmonics are added in stages (DC+1st, then 2nd, then 3rd),
   each stage warm-started from the last, and the whole thing warm-started
   from the per-frame fit already in out/motion_fit.json via its own FFT.

The fit runs on the ANALYTIC hull silhouette (knight_proxy's own solids, ~7 ms
a frame) rather than the atlas mesh (~60 ms); 05_verify_blender measured those
two agreeing at 0.980 IoU, so the cheap one is safe to optimise against. The
frames that ship are rendered from the mesh.
"""
import json, math, os, sys, time
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import knight_proxy as kp
import pose as PS
_src = open(os.path.join(HERE, "19_fit_motion.py")).read().split("def main()")[0]
exec(compile(_src, os.path.join(HERE, "19_fit_motion.py"), "exec"))

K3 = os.path.dirname(HERE); OUT = os.path.join(K3, "out"); WORK = os.path.join(K3, "work")
CB = os.path.join(os.path.dirname(K3), "cliffside_B")
FRAME = 512
PX_PER_M = 198.33333333333334 / 1.80
CANVAS_PX_PER_M = 150.21354166666666 / 1.80
GAIT = {"walk": dict(N=12, period=0.5797, px_s=247.0, stance=0.52,
                     contact={"Right": 0.0, "Left": 0.5}),
        "run": dict(N=8, period=0.5517, px_s=494.0, stance=0.30,
                    contact={"Right": 0.0, "Left": 0.5})}
# the angle channels that are solved (the root is NOT among them)
CH = ["pel_yaw", "pel_list", "lean", "counter",
      "L_hip", "L_splay", "L_knee", "L_ank", "L_toe",
      "R_hip", "R_splay", "R_knee", "R_ank", "R_toe", "A_pitch", "A_elbow"]
LAM_SLIP = float(os.environ.get("K3D_LAMSLIP", 2.4))   # per metre of rms pin residual
LAM_PEN = float(os.environ.get("K3D_LAMPEN", 6.0))     # per metre of penetration
ONLY = os.environ.get("K3D_ONLY", "")                  # solve one gait only
TAG = os.environ.get("K3D_TAG", "")                    # suffix for the outputs


def stance_weight(ph, c0, sigma):
    tau = (ph - c0) % 1.0
    if tau >= sigma:
        return 0.0
    e = min(tau, sigma - tau) / max(sigma * 0.18, 1e-9)
    return float(np.clip(e, 0.0, 1.0))


class Cycle:
    def __init__(self, gait):
        G = dict(GAIT[gait])
        if os.environ.get("K3D_STANCE"):
            G["stance"] = float(os.environ["K3D_STANCE"])
        self.G = G
        self.N = G["N"]
        self.D = G["px_s"] * G["period"] / CANVAS_PX_PER_M
        self.gait = gait
        fit = json.load(open(os.path.join(WORK, "fit_result.json")))
        self.theta = fit["theta_elevation_deg"]
        self.p = dict(kp.DEFAULTS); self.p.update(fit["params"])
        self.pl = kp.layered(self.p)
        self.Jr = kp.joints(self.pl)
        rj = json.load(open(os.path.join(OUT, "render_%s.json" % gait)))
        self.ty = rj["sole_y"] + rj["ground_calibration_px"]
        self.scale = PX_PER_M
        self.tx = FRAME / 2.0
        # rest part clouds, and which bone each belongs to
        # Pre-hull ONCE. A rigid transform cannot change which points are on
        # a body's convex hull, so re-running prehull() inside every objective
        # evaluation was recomputing 29 three-dimensional hulls per frame for
        # an answer that never changes.
        self.parts = kp.prehull(kp.build_parts(self.pl))
        self.foot_parts = {"Left": ["sabaton_L", "sabaton_toe_L"],
                           "Right": ["sabaton_R", "sabaton_toe_R"]}
        # targets
        src = os.path.join(CB, "sprites_knight", gait, "E")
        gf = sorted(f for f in os.listdir(src) if f.endswith(".png"))
        self.gf = gf
        self.tgt, self.dead, self.gidx = [], [], []
        for i in range(self.N):
            gi = int(round(i * len(gf) / self.N)) % len(gf)
            b, d = grok_body_mask(os.path.join(src, gf[gi]))
            self.tgt.append(b); self.dead.append(d); self.gidx.append(gi)
        self.ph = np.arange(self.N) / self.N

    # ---------------------------------------------------------------- pose
    def posed_parts(self, J):
        T = PS.bone_transforms(self.Jr, J,
                               {k[3:]: v for k, v in J.items() if k.startswith("_R_")})
        out = []
        for name, bone, pts in self.parts:
            R, t = T.get(bone, T["Hips"])
            out.append((name, bone, pts @ R.T + t))
        return out

    def contacts(self, posed):
        d = {}
        by = {n: q for n, _, q in posed}
        for BL, names in self.foot_parts.items():
            V = np.concatenate([by[n] for n in names], 0)
            zmin = float(V[:, 2].min())
            low = V[V[:, 2] < zmin + 0.012]
            d[BL] = (float(low[:, 1].mean()), zmin)
        return d

    # ------------------------------------------- the root, by linear solve
    def solve_root(self, C):
        """C[i][BL] = (contact_y, contact_z) in body-local coords.

        Unknowns: root_y[0..N-1], W_Left, W_Right  (and root_z separately).
        Rows: one per (frame, foot in stance), plus smoothness, plus zero mean.
        """
        N, D = self.N, self.D
        sig = self.G["stance"]
        Wt = {i: {BL: stance_weight(self.ph[i], self.G["contact"][BL], sig)
                  for BL in ("Left", "Right")} for i in range(N)}
        # ---- fore/aft
        rows, rhs, wts = [], [], []
        for i in range(N):
            for k, BL in enumerate(("Left", "Right")):
                w = Wt[i][BL]
                if w <= 0:
                    continue
                r = np.zeros(N + 2); r[i] = 1.0; r[N + k] = -1.0
                rows.append(r); rhs.append(-C[i][BL][0] - D * self.ph[i]); wts.append(w)
        for i in range(N):          # smoothness, circular second difference
            r = np.zeros(N + 2)
            r[i] = -2.0; r[(i - 1) % N] += 1.0; r[(i + 1) % N] += 1.0
            rows.append(r); rhs.append(0.0); wts.append(0.45)
        r = np.zeros(N + 2); r[:N] = 1.0 / N
        rows.append(r); rhs.append(0.0); wts.append(3.0)
        A = np.array(rows) * np.array(wts)[:, None]
        b = np.array(rhs) * np.array(wts)
        sol, *_ = np.linalg.lstsq(A, b, rcond=None)
        root_y = sol[:N]
        # the pin residual: how far a planted foot actually moves in world
        res = []
        for i in range(N):
            for k, BL in enumerate(("Left", "Right")):
                if Wt[i][BL] > 0:
                    res.append(Wt[i][BL] * (root_y[i] + C[i][BL][0]
                                            + D * self.ph[i] - sol[N + k]))
        slip = float(np.sqrt(np.mean(np.square(res)))) if res else 0.0
        # ---- vertical
        rows, rhs, wts = [], [], []
        for i in range(N):
            for BL in ("Left", "Right"):
                w = Wt[i][BL]
                if w <= 0:
                    continue
                r = np.zeros(N); r[i] = 1.0
                rows.append(r); rhs.append(-C[i][BL][1]); wts.append(w)
        for i in range(N):
            r = np.zeros(N); r[i] = -2.0
            r[(i - 1) % N] += 1.0; r[(i + 1) % N] += 1.0
            rows.append(r); rhs.append(0.0); wts.append(0.30)
        A = np.array(rows) * np.array(wts)[:, None]
        b = np.array(rhs) * np.array(wts)
        root_z, *_ = np.linalg.lstsq(A, b, rcond=None)
        pen = 0.0
        for i in range(N):
            for BL in ("Left", "Right"):
                pen = min(pen, root_z[i] + C[i][BL][1])
        return root_y, root_z, slip, -float(pen)

    # ------------------------------------------------------------ evaluate
    def frames_from(self, ang):
        """ang: (N, len(CH)) -> posed joint dicts with the root solved in."""
        Js, Cs, posed = [], [], []
        for i in range(self.N):
            q = np.zeros(len(KEYS))
            for j, c in enumerate(CH):
                q[KEYS.index(c)] = ang[i, j]
            J = joints_from_pose(self.p, self.Jr, q)
            P = self.posed_parts(J)
            Js.append(J); posed.append(P); Cs.append(self.contacts(P))
        ry, rz, slip, pen = self.solve_root(Cs)
        out = []
        for i in range(self.N):
            sh = np.array([0.0, ry[i], rz[i]])
            J = {k: (v + sh if not k.startswith("_R_") else v)
                 for k, v in Js[i].items()}
            out.append((J, [(n, b, q + sh) for n, b, q in posed[i]]))
        return out, slip, pen, ry, rz

    def iou_of(self, posed, i):
        m = kp.rasterize(posed, 90.0, self.theta, self.scale,
                         self.tx, self.ty, FRAME, FRAME)
        live = ~self.dead[i]
        a = m & live; b = self.tgt[i] & live
        u = (a | b).sum()
        return float((a & b).sum()) / u if u else 0.0

    def score(self, ang, detail=False):
        fr, slip, pen, ry, rz = self.frames_from(ang)
        ious = [self.iou_of(P, i) for i, (_, P) in enumerate(fr)]
        mean = float(np.mean(ious))
        cost = -mean + LAM_SLIP * slip + LAM_PEN * pen
        if detail:
            return cost, mean, ious, slip, pen, fr, ry, rz
        return cost


# ------------------------------------------------------- Fourier packing

def unpack(x, N, nch, H):
    """x -> (N, nch) angles, via a truncated Fourier series in phase."""
    co = x.reshape(nch, 2 * H + 1)
    ph = np.arange(N) / N
    out = np.tile(co[:, 0][None, :], (N, 1))
    for h in range(1, H + 1):
        c = np.cos(2 * np.pi * h * ph)[:, None]
        s = np.sin(2 * np.pi * h * ph)[:, None]
        out = out + c * co[:, 2 * h - 1][None, :] + s * co[:, 2 * h][None, :]
    return out


def pack_from_angles(ang, H):
    """FFT an (N, nch) angle table down to 2H+1 coefficients per channel."""
    N = len(ang)
    ph = np.arange(N) / N
    co = []
    for j in range(ang.shape[1]):
        y = ang[:, j]
        row = [y.mean()]
        for h in range(1, H + 1):
            row.append(2.0 * np.mean(y * np.cos(2 * np.pi * h * ph)))
            row.append(2.0 * np.mean(y * np.sin(2 * np.pi * h * ph)))
        co.append(row)
    return np.array(co).ravel()


# ------------------------------------------------------------------ main

def run_gait(gait, report):
    t0 = time.time()
    cy = Cycle(gait)
    N, nch = cy.N, len(CH)
    mf = json.load(open(os.path.join(OUT, "motion_fit.json")))
    # warm start: the per-frame fit's own angles, FFT'd
    P = np.array(mf["gaits"][gait]["pose"])
    ang0 = np.zeros((N, nch))
    for j, c in enumerate(CH):
        ang0[:, j] = P[:, KEYS.index(c)]
    # procedural and unconstrained references, for the report
    z = np.load(os.path.join(OUT, "anim_%s.npz" % gait), allow_pickle=True)
    nm = [str(x) for x in z["names"]]; rn = [str(x) for x in z["rot_names"]]
    proc = []
    for i in range(N):
        J = {k: z["joints"][i][j] for j, k in enumerate(nm)}
        for j, k in enumerate(rn):
            J["_R_" + k] = z["rots"][i][j].astype(np.float64)
        proc.append(cy.iou_of(cy.posed_parts(J), i))
    unc = []
    for i in range(N):
        J = joints_from_pose(cy.p, cy.Jr, P[i])
        unc.append(cy.iou_of(cy.posed_parts(J), i))
    print("  %s  procedural %.4f   unconstrained per-frame fit %.4f"
          % (gait, float(np.mean(proc)), float(np.mean(unc))))

    lo = np.array([LO[KEYS.index(c)] for c in CH])
    hi = np.array([HI[KEYS.index(c)] for c in CH])

    def clipped(ang):
        return np.clip(ang, lo[None, :], hi[None, :])

    best = None
    x = None
    warm = os.path.join(OUT, "cycle_x_%s.npy" % gait)
    for H in (1, 2, 3):
        if x is None:
            if os.path.exists(warm):
                w = np.load(warm)
                if len(w) == nch * (2 * 3 + 1):
                    x = pack_from_angles(clipped(unpack(w, N, nch, 3)), H)
                    print("    warm start from the previous solve")
            if x is None:
                x = pack_from_angles(ang0, H)
        else:
            a = clipped(unpack(x, N, nch, H - 1))
            x = pack_from_angles(a, H)
        f = lambda v: cy.score(clipped(unpack(v, N, nch, H)))
        c0 = f(x)
        res = minimize(f, x, method="Powell",
                       options=dict(maxiter=3, xtol=0.35, ftol=1.2e-3))
        x = res.x
        c1 = f(x)
        print("    H=%d  cost %.4f -> %.4f   (%.0fs)" % (H, c0, c1, time.time() - t0))
        if best is None or c1 < best[0]:
            best = (c1, x.copy(), H)
    cost, x, H = best
    if H < 3:
        x = pack_from_angles(clipped(unpack(x, N, nch, H)), 3); H = 3
    np.save(os.path.join(OUT, "cycle_x_%s.npy" % gait), x)
    ang = clipped(unpack(x, N, nch, H))
    cost, mean, ious, slip, pen, fr, ry, rz = cy.score(ang, detail=True)
    print("  %s  CONSTRAINED mean IoU %.4f   slip %.2f mm   penetration %.2f mm"
          % (gait, mean, 1000 * slip, 1000 * pen))

    # write the cycle
    Js = [J for J, _ in fr]
    keys = sorted(k for k in Js[0] if not k.startswith("_R_"))
    rots = sorted(k[3:] for k in Js[0] if k.startswith("_R_"))
    np.savez_compressed(
        os.path.join(OUT, "anim_fit_%s%s.npz" % (gait, TAG)),
        joints=np.array([[J[k] for k in keys] for J in Js], np.float32),
        names=np.array(keys), rot_names=np.array(rots),
        rots=np.array([[J["_R_" + k] for k in rots] for J in Js], np.float32),
        frames=N, fps=N / cy.G["period"], travel=cy.D)
    report["gaits"][gait] = dict(
        frames=[dict(frame=i, grok_frame=cy.gidx[i],
                     iou_procedural=round(proc[i], 4),
                     iou_unconstrained_fit=round(unc[i], 4),
                     iou_constrained_solve=round(ious[i], 4)) for i in range(N)],
        mean_iou_procedural=round(float(np.mean(proc)), 4),
        mean_iou_unconstrained=round(float(np.mean(unc)), 4),
        mean_iou_constrained=round(mean, 4),
        slip_rms_mm=round(1000 * slip, 3), penetration_mm=round(1000 * pen, 3),
        harmonics=H, travel_m_per_cycle=cy.D, fps=N / cy.G["period"],
        root_y_mm=[round(1000 * v, 1) for v in ry],
        root_z_mm=[round(1000 * v, 1) for v in rz],
        seconds=round(time.time() - t0, 1))
    for r in report["gaits"][gait]["frames"]:
        print("    %02d  proc %.4f  fit %.4f  solved %.4f"
              % (r["frame"], r["iou_procedural"], r["iou_unconstrained_fit"],
                 r["iou_constrained_solve"]))


def main():
    rep = {"note": "C-9 knight3d R-C9-59: whole-cycle solve with the plant "
                   "constraint inside the objective and the root eliminated "
                   "by a linear solve rather than searched.",
           "lambda_slip": LAM_SLIP, "lambda_penetration": LAM_PEN,
           "channels": CH, "gaits": {}}
    for g in ("walk", "run"):
        if ONLY and g != ONLY:
            continue
        run_gait(g, rep)
    with open(os.path.join(OUT, "cycle_solve%s.json" % TAG), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote", os.path.join(OUT, "cycle_solve.json"))


main()
