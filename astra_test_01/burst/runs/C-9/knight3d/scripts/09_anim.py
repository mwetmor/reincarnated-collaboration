#!/usr/bin/env python3
"""C-9 knight3d step 3b: the walk and run cycles, keyed on the skeleton.

Cadence is BINDING (R-C9-52): walk 12 frames per 0.5797 s stride, run 8 per
0.5517 s; walk_px_s 247, run_px_s 494 in canvas pixels, and the knight's
canvas figure height is 150.2136 px for 1.80 m, so

    walk  1.7161 m per cycle (0.8580 m per step) at 20.700 fps
    run   3.2661 m per cycle (1.6330 m per step) at 14.500 fps

What the cycle carries, one clause per defect Matt named:

  FOOT PLANT (defect 1).  A stance foot is a rigid body pinned to a WORLD
  point; it never translates, it only rotates about whichever part of it is
  touching -- heel, then the whole sole, then the toe. So the plant has zero
  slide BY CONSTRUCTION rather than by tuning, and 09 re-measures it anyway.
  The sabaton's toe section rotates back by the same angle the foot rotates
  forward at toe-off, so the toe stays flat while the heel lifts: that is the
  break a one-piece cut-out sabaton cannot do.

  HIPS WITH LEGS (defect 2).  The pelvis height is not an invented sine. Each
  frame it is the LOWEST of (a) a nominal carriage height and (b) the highest
  the pelvis may be for both legs to still reach their planted feet. The bob
  is therefore caused by the stride, which is what "coordination between the
  leg movement and the hips/body" means. Pelvis yaw, list, torso
  counter-rotation and arm swing all key off the same phase.

  GRIP (defect 3).  The pollaxe is parented to SOCK_WeaponMain on the right
  hand, and the right arm is IK-solved to a grip point carried in the CHEST's
  frame. Hand and haft are one rigid body; there is nothing to drift. The free
  left arm swings with the gait and is never steered toward the haft, which is
  what made the cut-out read as reaching-but-not-gripping.

  TABARD (R-C9-36).  Heavy wool: rigid above the waist, and below it a 3-link
  chain driven by the pelvis's own motion through a one-pole lag of 0.10 s,
  scaled so the walk peaks inside the 4-8 deg band. No flutter term exists.

Writes out/anim_walk.npz, out/anim_run.npz (posed joint positions per frame)
and out/anim_report.json (including the measured foot slide).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knight_proxy as kp

ROOT = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
K3 = os.path.join(ROOT, "knight3d")
WORK = os.path.join(K3, "work"); OUT = os.path.join(K3, "out")

# ---- the binding cadence ---------------------------------------------------
CANVAS_PX_PER_M = 150.21354166666666 / 1.80          # 83.452 canvas px per metre
GAITS = {
    "walk": dict(frames=12, period=0.5797, px_s=247.0, stance=0.52,
                 heel_pitch=17.0, toe_pitch=38.0, swing_lift=0.105,
                 pelvis_yaw=6.0, pelvis_list=3.2, torso_counter=0.85,
                 torso_lean=4.0, arm_swing=22.0, arm_elbow=16.0,
                 tabard_deg=6.0, skirt_deg=3.5, foot_yaw=6.0),
    "run": dict(frames=8, period=0.5517, px_s=494.0, stance=0.30,
                heel_pitch=9.0, toe_pitch=46.0, swing_lift=0.20,
                pelvis_yaw=9.0, pelvis_list=4.0, torso_counter=0.95,
                torso_lean=13.0, arm_swing=38.0, arm_elbow=52.0,
                tabard_deg=10.0, skirt_deg=5.5, foot_yaw=3.0),
}


def rotx(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def roty(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotz(d):
    a = math.radians(d); c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def circ_smooth(x, k=3):
    w = np.ones(k) / k
    n = len(x)
    return np.array([np.dot(w, [x[(i + j - k // 2) % n] for j in range(k)])
                     for i in range(n)])


def foot_state(phi, contact, G, D, fl, hb, tf, z_ank, cal):
    """Where the foot is at phase `phi`, and how it is rotated.

    Returns (ankle_y_rel_root, ankle_z, pitch_deg, toe_break_deg, planted,
             contact_y_rel_root or None).
    The stance foot is pinned to a world point: relative to the root, which
    advances D per cycle, that point slides back by D*(phi-contact).
    """
    sigma = G["stance"]
    tau = (phi - contact) % 1.0
    heel_off = cal["heel_y"]                 # measured on the sabaton mesh
    toe_off = cal["toe_y"]
    ank_local = np.array([0.0, 0.0, z_ank])  # ankle above the sole, flat foot
    # heel strike places the HEEL at +F so that mid-stance sits under the hip
    F = D * sigma / 2.0 - hb * fl

    if tau < sigma:                                   # ---------------- stance
        u = tau / sigma
        h1, h2 = 0.16, 0.72
        if u < h1:                                    # heel only, rolling down
            pitch = G["heel_pitch"] * (1.0 - smoothstep(u / h1))
            pivot = np.array([0.0, F, 0.0])
            rest_off = ank_local - np.array([0.0, heel_off, 0.0])
        elif u < h2:                                  # flat
            pitch = 0.0
            pivot = np.array([0.0, F, 0.0])
            rest_off = ank_local - np.array([0.0, heel_off, 0.0])
        else:                                         # toe only, heel lifting
            # The foot rotates about the BALL -- where the toe section joins
            # the rest of the sabaton -- and the toe section counter-rotates
            # by the same angle so it stays flat on the ground. That is the
            # break a one-piece cut-out sabaton cannot do (Matt defect 1).
            k = smoothstep((u - h2) / (1 - h2))
            pitch = -G["toe_pitch"] * k
            pivot = np.array([0.0, F + (toe_off - heel_off), 0.0])
            # the ankle sits toe_off BEHIND the ball in the foot's own frame,
            # not (toe_off - heel_off): writing the latter jumped the whole
            # foot forward by |heel_off| = 78 mm at the flat-to-toe boundary,
            # and the slip test caught it at 39.8 mm.
            rest_off = ank_local - np.array([0.0, toe_off, 0.0])
        R = rotx(pitch)
        ank = pivot + R @ rest_off
        slide = D * tau
        toe_break = -pitch if pitch < 0 else 0.0      # the toe stays FLAT
        # Where the ankle WOULD be with the foot flat about the same pivot.
        # During toe-off the toe section is pinned to the ground, so its bone
        # must be placed from this flat configuration; placing it from the
        # rotating foot instead pins it to a point that is itself moving, and
        # the plant -- exact through the whole flat phase -- slipped 26 mm in
        # precisely the two frames where the toe is the thing on the ground.
        ank_flat = pivot + rest_off
        return (ank[1] - slide, ank[2], pitch, toe_break, True, F - slide,
                ank_flat[1] - slide, ank_flat[2],
                pivot[1] - slide, rest_off)
    # ------------------------------------------------------------------ swing
    w = (tau - sigma) / (1.0 - sigma)
    # where it left, and where it must next strike
    y_off, z_off, p_off = foot_state(contact + sigma - 1e-6, contact, G,
                                     D, fl, hb, tf, z_ank, cal)[:3]
    y_on = F + hb * fl + D * (1.0 - 1e-9)   # next strike, one cycle ahead
    y_on = F - D * 1.0 + hb * fl + D        # == F + hb*fl  (root-relative)
    # heel strike pose: pitched up about the heel
    R0 = rotx(G["heel_pitch"])
    a0 = np.array([0.0, F, 0.0]) + R0 @ (np.array([0.0, 0.0, z_ank])
                                         - np.array([0.0, heel_off, 0.0]))
    y_on, z_on = a0[1], a0[2]
    e = smoothstep(w)
    y = y_off + (y_on - y_off) * e
    lift = G["swing_lift"] * math.sin(math.pi * min(max(w, 0.0), 1.0)) ** 0.9
    z = z_off + (z_on - z_off) * e + lift
    # dorsiflex through mid-swing so the toe clears, then present the heel
    pitch = p_off + (G["heel_pitch"] - p_off) * smoothstep(min(1.0, w * 1.5))
    pitch += 10.0 * math.sin(math.pi * w) * (1 - e)
    return y, z, pitch, 0.0, False, None, y, z, None, None


def calibrate_foot(p):
    """Read the heel, the toe and the sole height off the SABATON MESH.

    foot_state() pivots the foot about its heel and its toe. Those were taken
    from the parameters (heel at -hb*fl, sole at z_ankle), but the mesh is a
    convex hull of a point cloud and its true lowest and rearmost points are
    not exactly there -- the sabaton sank 16 mm into the ground. Measure them.
    """
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    names = [str(n) for n in A["names"]]
    tri_v = A["tri_v"].astype(np.float64); tri_id = A["tri_id"]
    q = kp.layered(p)
    J = kp.joints(q)
    ank = J["RightFoot"]
    yaw = q.get("foot_R_yaw", kp.DEFAULTS["foot_R_yaw"])
    Rz = rotz(-yaw)
    ids = [i for i, n in enumerate(names) if n in ("sabaton_R", "sabaton_toe_R")]
    V = tri_v[np.isin(tri_id, ids)].reshape(-1, 3)
    L = (V - ank) @ Rz.T
    sole = float(-L[:, 2].min())                    # sole below the ankle
    bottom = L[L[:, 2] < L[:, 2].min() + 0.012]
    heel_y = float(bottom[:, 1].min())
    toe_ids = [i for i, n in enumerate(names) if n == "sabaton_toe_R"]
    Vt = tri_v[np.isin(tri_id, toe_ids)].reshape(-1, 3)
    Lt = (Vt - ank) @ Rz.T
    bt = Lt[Lt[:, 2] < Lt[:, 2].min() + 0.012]
    toe_y = float(bt[:, 1].min())        # the BALL: the toe section's rear edge
    return dict(sole_drop=sole, heel_y=heel_y, toe_y=toe_y)


def build_gait(name, p):
    G = GAITS[name]
    N, T = G["frames"], G["period"]
    D = G["px_s"] * T / CANVAS_PX_PER_M              # metres per cycle
    cal = calibrate_foot(p)
    fl, hb, tf = p["foot_len"], p["foot_heel_back"], p["toe_frac"]
    z_ank = cal["sole_drop"]                     # measured off the mesh
    Jr = kp.joints(kp.layered(p))
    L1 = np.linalg.norm(Jr["RightLeg"] - Jr["RightUpLeg"])
    L2 = np.linalg.norm(Jr["RightFoot"] - Jr["RightLeg"])
    hip_x = p["hip_x"]
    z_hip0 = p["z_hip"]

    phis = np.arange(N) / N
    contact = {"R": 0.0, "L": 0.5}

    # --- 1. feet first, then let the feet decide the pelvis ---------------
    feet = {s: [foot_state(ph, contact[s], G, D, fl, hb, tf, z_ank, cal)
                for ph in phis] for s in "RL"}
    h_reach = np.zeros(N)
    for i in range(N):
        lim = []
        for s in "RL":
            y, z = feet[s][i][0], feet[s][i][1]
            reach = (L1 + L2) * 0.985
            dy2 = y * y
            if reach * reach - dy2 <= 0:
                lim.append(z + 0.02)
            else:
                lim.append(z + math.sqrt(reach * reach - dy2))
        h_reach[i] = min(lim)
    h_nom = z_hip0 - 0.012
    h = np.minimum(h_nom, h_reach)
    h = circ_smooth(h, 3)
    drop = float(z_hip0 - h.min())

    # --- 2. the rest of the body, all off the same phase -------------------
    frames = []
    pelvis_y = np.zeros(N)
    for i, ph in enumerate(phis):
        # pelvis: yaw toward the swinging leg, list toward the swing side
        yaw = G["pelvis_yaw"] * math.sin(2 * math.pi * (ph - 0.25))
        lst = G["pelvis_list"] * math.sin(2 * math.pi * (ph - 0.5))
        Rp = rotz(yaw) @ roty(lst)
        hips = np.array([0.0, pelvis_y[i], h[i]])

        J = {}
        J["Hips"] = hips
        # spine: counter-rotate the torso against the pelvis, lean forward
        chain = ["Spine", "Spine1", "Spine2", "Neck", "Head", "HeadTop_End"]
        cnt = -G["torso_counter"] * yaw
        acc = Rp
        prev_rest, prev_pos = Jr["Hips"], hips
        for k, b in enumerate(chain):
            frac = [0.30, 0.34, 0.36, 0.0, 0.0, 0.0][k]
            lean = [0.34, 0.33, 0.33, 0.0, 0.0, 0.0][k] * G["torso_lean"]
            acc = acc @ rotz(cnt * frac) @ rotx(-lean)
            pos = prev_pos + acc @ (Jr[b] - prev_rest)
            J[b] = pos
            prev_rest, prev_pos = Jr[b], pos
        R_chest = acc                                  # frame of Spine2/Neck
        # keep a torso frame for the arms and the weapon
        for b in ("LeftShoulder", "RightShoulder"):
            J[b] = J["Spine2"] + R_chest @ (Jr[b] - Jr["Spine2"])
        for b in ("LeftArm", "RightArm"):
            J[b] = J["Spine2"] + R_chest @ (Jr[b] - Jr["Spine2"])

        # --- legs: 2-bone IK to the planted ankles ------------------------
        for s, sx, BL in (("R", 1.0, "Right"), ("L", -1.0, "Left")):
            y, z, pitch, toe_break, planted, cpt, yf, zf, piv_y, rest_off = feet[s][i]
            hip = hips + Rp @ np.array([sx * hip_x, 0.0, 0.0])
            fx = sx * hip_x + sx * 0.004
            fy = rotz(G["foot_yaw"] * sx * -1.0)
            if planted:
                # Place the foot in ONE frame: the ground pivot, then the foot's
                # own yaw and pitch. foot_state works un-yawed; applying the yaw
                # only to the MESH afterwards left the heel edge 16 mm adrift at
                # heel strike, which is exactly the frame the eye reads as a
                # skid.
                pivot3 = np.array([fx, piv_y, 0.0])
                ankle = pivot3 + fy @ (rotx(pitch) @ rest_off)
                ank_flat3 = pivot3 + fy @ rest_off
            else:
                ankle = np.array([fx, y, z])
                ank_flat3 = ankle
            knee, ank = kp._ik2(hip, ankle, L1, L2,
                                pole=np.array([sx * 0.22, 1.0, 0.05]))
            J[BL + "UpLeg"] = hip
            J[BL + "Leg"] = knee
            J[BL + "Foot"] = ank
            Rf = fy @ rotx(pitch)
            # the REST foot already has its own yaw baked into the mesh, so the
            # transform that carries the rest sabaton to this frame must undo it
            rest_yaw = rotz(p["foot_%s_yaw" % s])
            R_foot = Rf @ rest_yaw.T
            R_toe = Rf @ rotx(toe_break) @ rest_yaw.T
            J["_R_" + BL + "Foot"] = R_foot
            J["_R_" + BL + "ToeBase"] = R_toe
            # The ball and the toe tip come from the FOOT'S OWN TRANSFORM, not
            # from a second formula in the parameters. Written the other way
            # first, the toe mesh sat a few mm off the joint the foot pivots
            # about, and the plant -- exact through the whole flat phase --
            # slipped 26 mm and sank 11 mm at toe-off, i.e. only in the frames
            # where the toe is the thing on the ground.
            # the toe is pinned from the FLAT-foot configuration about the
            # same ground pivot, so it does not ride the rotating foot
            R_flat = fy @ rest_yaw.T
            t_flat = ank_flat3 - R_flat @ Jr[BL + "Foot"]
            ball = R_flat @ Jr[BL + "ToeBase"] + t_flat
            J[BL + "ToeBase"] = ball
            J[BL + "Toe_End"] = R_toe @ (Jr[BL + "Toe_End"] - Jr[BL + "ToeBase"]) + ball

        # --- right arm: IK to the grip carried in the CHEST's frame -------
        grip_rest = np.array([p["grip_x"], p["grip_y"], p["grip_z"]])
        grip = J["Spine2"] + R_chest @ (grip_rest - Jr["Spine2"])
        A1 = np.linalg.norm(Jr["RightForeArm"] - Jr["RightArm"])
        A2 = np.linalg.norm(Jr["RightHand"] - Jr["RightForeArm"])
        el, wr = kp._ik2(J["RightArm"], grip, A1, A2,
                         pole=R_chest @ np.array([0.35, -0.45, -1.0]))
        J["RightForeArm"] = el
        J["RightHand"] = wr
        d = wr - el; d = d / max(np.linalg.norm(d), 1e-9)
        J["RightHandEnd"] = wr + d * 0.115

        # --- left arm: free swing, opposite the left leg ------------------
        sw = G["arm_swing"] * math.sin(2 * math.pi * (ph - contact["L"]))
        fl_e = G["arm_elbow"] * (0.5 + 0.5 * math.cos(2 * math.pi * (ph - contact["L"])))
        Ra = R_chest @ rotx(sw) @ rotz(math.radians(0))
        B1 = np.linalg.norm(Jr["LeftForeArm"] - Jr["LeftArm"])
        B2 = np.linalg.norm(Jr["LeftHand"] - Jr["LeftForeArm"])
        sh = J["LeftArm"]
        elb = sh + Ra @ (rotz(-6.0) @ np.array([0.0, 0.0, -B1]))
        Rb = Ra @ rotx(fl_e)
        wr2 = elb + Rb @ np.array([0.0, 0.0, -B2])
        J["LeftForeArm"] = elb
        J["LeftHand"] = wr2
        d = wr2 - elb; d = d / max(np.linalg.norm(d), 1e-9)
        J["LeftHandEnd"] = wr2 + d * 0.115

        J["_R_chest"] = R_chest
        J["_R_pelvis"] = Rp
        J["_yaw"] = yaw
        frames.append(J)

    # --- 3. tabard and skirt: a damped chain driven by the pelvis ---------
    #   R-C9-36 -- heavy wool, rigid above the waist, a damped pendulum below
    #   lagging 0.08-0.12 s, 4-8 deg on walk, no flutter.
    dt = T / N
    lag = 0.10
    a = math.exp(-dt / lag)
    drive = np.zeros(N)
    for i in range(N):
        j = (i - 1) % N
        dz = (h[i] - h[j]) / dt
        dyaw = (frames[i]["_yaw"] - frames[j]["_yaw"]) / dt
        drive[i] = -dz * 2.2 + 0.010 * dyaw
    lagged = np.zeros(N)
    x = drive.mean()
    for _ in range(4):                       # settle the circular filter
        for i in range(N):
            x = a * x + (1 - a) * drive[i]
            lagged[i] = x
    peak = np.abs(lagged - lagged.mean()).max() or 1.0
    tab = (lagged - lagged.mean()) / peak * G["tabard_deg"]
    skirt = (lagged - lagged.mean()) / peak * G["skirt_deg"]

    for i, J in enumerate(frames):
        Rp = J["_R_pelvis"]
        z_waist, tzb = p["z_waist"], p["tabard_z_bot"]
        for tag, ys in (("F", 1.0), ("B", -1.0)):
            prev = J["Hips"] + Rp @ (Jr["TAB_%s_01" % tag] - Jr["Hips"])
            J["TAB_%s_01" % tag] = prev
            R = Rp
            for k in range(1, 4):
                R = R @ rotx(tab[i] * [0.5, 0.8, 1.0][k - 1] * ys)
                nxt = prev + R @ (Jr["TAB_%s_%02d" % (tag, k + 1)]
                                  - Jr["TAB_%s_%02d" % (tag, k)])
                if k < 3:
                    J["TAB_%s_%02d" % (tag, k + 1)] = nxt
                else:
                    J["TAB_%s_04" % tag] = nxt
                prev = nxt
        for tag, ys in (("F", 1.0), ("B", -1.0), ("L", 0.0), ("R", 0.0)):
            J["SKIRT_%s" % tag] = J["Hips"] + Rp @ (Jr["SKIRT_%s" % tag] - Jr["Hips"])
            R = Rp @ rotx(skirt[i] * ys)
            J["SKIRT_%s_end" % tag] = J["SKIRT_%s" % tag] + R @ (
                Jr["SKIRT_%s_end" % tag] - Jr["SKIRT_%s" % tag])
        # weapon sockets ride the right hand
        Rh = np.eye(3)
        v = J["RightHand"] - J["RightForeArm"]
        v = v / max(np.linalg.norm(v), 1e-9)
        vr = Jr["RightHand"] - Jr["RightForeArm"]
        vr = vr / max(np.linalg.norm(vr), 1e-9)
        ax = np.cross(vr, v); s_ = np.linalg.norm(ax); c_ = float(vr @ v)
        if s_ > 1e-9:
            ax = ax / s_
            K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
            Rh = np.eye(3) + math.sin(math.atan2(s_, c_)) * K + (1 - c_) * (K @ K)
        J["_R_hand"] = Rh
        for b in ("SOCK_WeaponMain", "SOCK_WeaponMain_end",
                  "SOCK_WeaponGripFar", "SOCK_WeaponGripFar_end"):
            J[b] = J["RightHand"] + Rh @ (Jr[b] - Jr["RightHand"])
        for b in ("SOCK_OffHand", "SOCK_OffHand_end"):
            J[b] = J["LeftHand"] + (Jr[b] - Jr["LeftHand"])

    return frames, dict(name=name, frames=N, period_s=T, fps=N / T,
                        travel_m_per_cycle=D, step_m=D / 2,
                        travel_canvas_px_per_cycle=G["px_s"] * T,
                        stance_fraction=G["stance"],
                        pelvis_height_m=[round(float(v), 4) for v in h],
                        pelvis_drop_m=round(drop, 4),
                        pelvis_drop_pct_of_height=round(100 * drop / 1.80, 2),
                        tabard_deg_peak=round(float(np.abs(tab).max()), 2),
                        skirt_deg_peak=round(float(np.abs(skirt).max()), 2),
                        tabard_lag_s=lag)


def measure_slide(frames, meta, p):
    """Re-measure what the construction claims: does a planted foot move?

    Measured on the SABATON MESH, not on joints, and in WORLD space, not
    root-relative. For every frame, take the sabaton's vertices that are on
    the ground (z < 12 mm), take their centroid, and add the root's travel to
    get a world position. A planted foot's world position must not change.

    Two things the first version of this got wrong and which the numbers then
    hid: it measured JOINT positions (the toe joint sits 50 mm above the sole,
    so "lowest point 0.036 m" read like floating feet when nothing was
    floating), and it de-rotated the root travel with the frame's own phase,
    which is wrong for the left foot -- its stance begins half a cycle earlier,
    so the frames near phase 0 belong to the PREVIOUS cycle and came out one
    whole stride adrift (1.71 m "slide" on a 1.72 m stride).
    """
    A = np.load(os.path.join(OUT, "mesh_atlas.npz"), allow_pickle=True)
    idx = json.load(open(os.path.join(OUT, "parts_index.json")))
    import pose as PS
    tri_v0 = A["tri_v"].astype(np.float64); tri_id = A["tri_id"]
    names = [str(n) for n in A["names"]]
    part_bone = {n: idx["parts"][n]["bone"] for n in names}
    part_kind = {n: idx["parts"][n]["kind"] for n in names}
    Jr = kp.joints(kp.layered(p))
    G = GAITS[meta["name"]]; N = meta["frames"]; D = meta["travel_m_per_cycle"]
    sigma = G["stance"]
    foot_tris = {}
    for s_, BL in (("L", "Left"), ("R", "Right")):
        ids = [i for i, n in enumerate(names)
               if n in ("sabaton_%s" % s_, "sabaton_toe_%s" % s_)]
        foot_tris[BL] = np.isin(tri_id, ids)

    posed = []
    for i in range(N):
        ov = {k[3:]: v for k, v in frames[i].items() if k.startswith("_R_")}
        T = PS.bone_transforms(Jr, frames[i], ov)
        posed.append(PS.pose_tris(tri_v0, tri_id, names, part_bone, part_kind, T,
                                  kp.layered(p)))
    out = {}
    lowest = []
    for s_, BL, c in (("R", "Right", 0.0), ("L", "Left", 0.5)):
        # A MATERIAL POINT that is touching the ground in two consecutive
        # frames must not move. Centroid-of-contact does NOT test this: the
        # contact patch legitimately travels heel-to-toe across stance, which
        # is why the first version reported 216 mm of "slide" for a foot that
        # was pinned (216 mm is the heel-to-toe distance, and it was the same
        # number for both feet and both gaits -- a constant is a tell).
        zs, slips, nsl = [], 0.0, 0
        prev = None
        for i in range(N):
            ph = i / N
            V = posed[i][foot_tris[BL]].reshape(-1, 3)
            zs.append(float(V[:, 2].min()))
            tau = (ph - c) % 1.0
            ph_adj = ph if (ph - tau) >= -1e-9 else ph + 1.0
            # 1 mm, not 4. At 4 mm the test also catches vertices 13 mm ahead
            # of the heel edge while the foot is still rotating down onto it --
            # they are SUPPOSED to move, and the test reported their rotation
            # as 16 mm of slide. A contact test with slack in it measures the
            # slack.
            touch = V[:, 2] < 0.001
            wy = V[:, 1] + D * ph_adj
            if tau < sigma and prev is not None and prev[0] is not None:
                both = touch & prev[1]
                if both.any():
                    d = np.abs(wy[both] - prev[0][both])
                    slips = max(slips, float(d.max())); nsl += int(both.sum())
            prev = (wy if tau < sigma else None, touch)
        lowest += zs
        out[BL] = dict(max_slip_of_a_touching_vertex_mm=round(1000.0 * slips, 3),
                       vertex_pairs_tested=nsl,
                       sabaton_min_z_mm=round(1000.0 * min(zs), 2),
                       sabaton_max_z_mm=round(1000.0 * max(zs), 2))
    out["ground_penetration_mm"] = round(1000.0 * min(lowest), 2)

    # The construction test, at 8x the frame rate. With 8 run frames and a 30 %
    # stance there are barely two consecutive stance frames to compare, so the
    # per-frame test above can report "0 slip, 0 pairs tested" -- which is not
    # a pass, it is an empty check. This one samples the same construction
    # densely and tests it directly.
    cal = calibrate_foot(p)
    fl, hb, tf = p["foot_len"], p["foot_heel_back"], p["toe_frac"]
    dense = {}
    for s_, c in (("R", 0.0), ("L", 0.5)):
        M = N * 8
        ys = []
        for j in range(M):
            ph = j / M
            tau = (ph - c) % 1.0
            if tau >= sigma:
                continue
            cpt = foot_state(ph, c, GAITS[meta["name"]], D, fl, hb,
                             tf, cal["sole_drop"], cal)[5]
            ph_adj = ph if (ph - tau) >= -1e-9 else ph + 1.0
            ys.append(cpt + D * ph_adj)
        dense[s_] = round(1000.0 * (max(ys) - min(ys)), 4) if len(ys) > 1 else None
    out["contact_world_y_spread_mm_at_8x_framerate"] = dense
    return out


def main():
    fit = json.load(open(os.path.join(WORK, "fit_result.json")))
    p = dict(kp.DEFAULTS); p.update(fit["params"])
    rep = {"note": __doc__.strip().splitlines()[0],
           "canvas_px_per_m": CANVAS_PX_PER_M, "gaits": {}}
    order = None
    for name in ("walk", "run"):
        frames, meta = build_gait(name, p)
        meta["foot_plant"] = measure_slide(frames, meta, p)
        rep["gaits"][name] = meta
        keys = [k for k in frames[0] if not k.startswith("_")]
        order = sorted(keys)
        arr = np.array([[f[k] for k in order] for f in frames], np.float32)
        ovk = sorted(k[3:] for k in frames[0] if k.startswith("_R_"))
        ova = np.array([[f["_R_" + k] for k in ovk] for f in frames], np.float32)
        np.savez_compressed(os.path.join(OUT, "anim_%s.npz" % name),
                            joints=arr, names=np.array(order),
                            rot_names=np.array(ovk), rots=ova,
                            frames=meta["frames"], fps=meta["fps"],
                            travel=meta["travel_m_per_cycle"])
        print("%-5s %2d frames @ %.3f fps, %.4f m/cycle, pelvis drop %.3f m (%.1f %%)"
              % (name, meta["frames"], meta["fps"], meta["travel_m_per_cycle"],
                 meta["pelvis_drop_m"], meta["pelvis_drop_pct_of_height"]))
        for k, v in meta["foot_plant"].items():
            print("      %-10s %s" % (k, v))
    with open(os.path.join(OUT, "anim_report.json"), "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote out/anim_walk.npz, out/anim_run.npz, out/anim_report.json")


if __name__ == "__main__":
    main()
