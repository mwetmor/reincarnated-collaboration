"""T12: THE AXE-ARM GUARD POSE, authored by IK -- and the guard's orientation chosen for READABILITY.

    python3 guard_pose_solve.py <body.glb (26 joints, the mount)> <out.json> [--side L] [--stance-key k] [--box ...] [--chest q]

--side L (JOIN-1, the off-hand axe): the LEFT arm and weapon_l (its mount: 59_offhand_mount.py), outboard is his
LEFT (+X), the grip box and the readability search mirrored; the prior is the fight walk's mean LEFT arm.
--stance-key k: the idle key whose chest the pose is solved at (default: the key whose chest faces most nearly
his forward) -- JOIN solves both arms at idle_guard's stance (key 53 on the re-cut idle).

1. READABILITY. Within the guard predicate (haft 30-60 deg from vertical, leaning forward and
   outboard), the haft direction whose SCREEN projection at the play camera (orthographic, pitch
   52.9535 deg, 77.8 px per metre) keeps the most length in the WORST of the eight direction cells
   (camera yaw 47 + k x 45 deg off his forward). A haft leaning 37 deg toward the camera is
   parallel to its view ray and vanishes -- the forward-guard trap legolas named -- so the worst
   cell is what decides.
2. THE POSE. The right arm solved in the CHEST frame (Spine) so that, at the unarmed idle's mean
   chest, the mounted axe's haft lies on that direction and the grip sits in front of him at
   belly-to-chest height, with the WRIST NEUTRAL (RightHand at its rest rotation) -- so the haft
   stays in the fist's channel and the forearm comes out square to it -- and the arm as near the
   fight walk's own mean arm as those allow (the natural prior). RightShoulder keeps the walk's.
All in glTF units; metres = units x the Armature scale (0.010882)."""
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.normpath(os.path.join(HERE, "..", "..", "nb_d2", "scripts"))
sys.path.insert(0, SCR)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')

F = np.array([0, 0, 1.0]); U = np.array([0, 1.0, 0]); R = np.array([-1.0, 0, 0])
PITCH = math.radians(52.9535411256029)
PX_PER_M = 77.8
SIDE = sys.argv[sys.argv.index('--side') + 1] if '--side' in sys.argv else 'R'
SH, ARM_, FORE, HAND, WB = (("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "weapon_l") if SIDE == 'L' else
                            ("RightShoulder", "RightArm", "RightForeArm", "RightHand", "weapon_r"))
CHAIN = [SH, ARM_, FORE, HAND, WB]
RS = -R if SIDE == 'L' else R                 # OUTBOARD: his right for the right arm, his left for the left


def quat_of(m):
    return W.m2q(m)


def rotvec_to_m(v):
    a = float(np.linalg.norm(v))
    if a < 1e-12:
        return np.eye(3)
    return W.axis_angle(v / a, a)


def slerp_mean(qs):
    ref = qs[0]; acc = np.zeros(4)
    for q in qs:
        q = np.asarray(q, float)
        acc += q if np.dot(q, ref) >= 0 else -q
    return acc / np.linalg.norm(acc)


def cam_axes(yaw_deg):
    y = math.radians(yaw_deg)
    g = math.cos(y) * F + math.sin(y) * R
    v = math.cos(PITCH) * g - math.sin(PITCH) * U
    r = np.cross(v, U); r /= np.linalg.norm(r)
    s = np.cross(r, v); s /= np.linalg.norm(s)
    return r, s


# the camera cells: the Barrow's play camera sits at yaw 47 (cells 47 + 45k off his forward); the JOIN renderer turns
# the character under a yaw-0 camera, exact octants (--cells-offset 0)
CELL0 = float(sys.argv[sys.argv.index('--cells-offset') + 1]) if '--cells-offset' in sys.argv else 47.0
CELLS = [cam_axes(CELL0 + 45 * k) for k in range(8)]


def screen(h):
    out = []
    for r, s in CELLS:
        x, y = float(h @ r), float(h @ s)
        out.append((math.hypot(x, y), math.degrees(math.atan2(x, y))))
    return out


def main():
    body, outp = sys.argv[1], sys.argv[2]
    js, b = L.load_glb(body)
    nodes = js['nodes']
    idx = {n.get('name'): i for i, n in enumerate(nodes)}
    anims = {a['name']: a for a in js['animations']}
    mpu = 0.010882345028221607

    def channel(anim, node, path):
        for ch in anim['channels']:
            if ch['target'].get('node') == node and ch['target'].get('path') == path:
                s = anim['samplers'][ch['sampler']]
                return L.read_accessor(js, b, s['input']).reshape(-1), L.read_accessor(js, b, s['output'])
        return None, None

    def local_at(anim, name, k):
        i = idx[name]
        M = W.trs(nodes[i])
        t, v = channel(anim, i, 'rotation')
        if t is not None:
            M[:3, :3] = W.q2m(v[min(k, len(v) - 1)])
        t2, v2 = channel(anim, i, 'translation')
        if t2 is not None:
            M[:3, 3] = v2[min(k, len(v2) - 1)]
        return M

    # ---- 1. readability -----------------------------------------------------------------------
    best = None
    table = []
    # a MARGIN inside the predicate (tilt 30-60, forward and outboard > 0): the pose rides the
    # chest, and a guard on the boundary fails half the frames of a breathing idle (tested: tilt
    # 60 -> 54% of the idle's frames)
    for tilt in np.arange(35.0, 55.01, 2.5):
        for az in np.arange(15.0, 75.01, 5.0):
            h = (math.cos(math.radians(az)) * F + math.sin(math.radians(az)) * RS) * math.sin(math.radians(tilt)) + U * math.cos(math.radians(tilt))
            sc = screen(h)
            lens = [l for l, _ in sc]
            row = (min(lens), float(np.mean(lens)), tilt, az, sc)
            table.append(row)
            if best is None or (row[0], row[1]) > (best[0], best[1]):
                best = row
    if '--azimuth' in sys.argv:
        # a chosen azimuth (JOIN: the dual-wield guard outboard on both sides; the octant cells make az and az+45 read alike)
        az_f = float(sys.argv[sys.argv.index('--azimuth') + 1])
        tl_f = float(sys.argv[sys.argv.index('--tilt') + 1]) if '--tilt' in sys.argv else best[2]
        best = min(table, key=lambda r: abs(r[3] - az_f) + abs(r[2] - tl_f))
    wmin, wmean, tilt, az, sc = best
    h_world = (math.cos(math.radians(az)) * F + math.sin(math.radians(az)) * RS) * math.sin(math.radians(tilt)) + U * math.cos(math.radians(tilt))
    if '--pitch-fwd' in sys.argv:
        # T12_12c (Matt R-C9-115: 'the blade/tip pointed more forward'): the haft turned TOWARD his forward by this many degrees,
        # in the plane of the haft and his forward -- its tip-forward angle (grip->tip against his aim) falls by exactly that
        pf = math.radians(float(sys.argv[sys.argv.index('--pitch-fwd') + 1]))
        a0 = math.acos(max(-1.0, min(1.0, float(h_world @ F))))
        perp = h_world - float(h_world @ F) * F; perp /= np.linalg.norm(perp)
        a1 = max(a0 - pf, 0.0)
        h_world = math.cos(a1) * F + math.sin(a1) * perp
        tilt = math.degrees(math.acos(float(h_world @ U))); az = math.degrees(math.atan2(float(h_world @ RS), float(h_world @ F)))
        sc = screen(h_world); wmin = min(l for l, _ in sc); wmean = float(np.mean([l for l, _ in sc]))
        print("pitch forward %.0f deg: tip-forward %.1f -> %.1f deg; the haft now tilt %.1f, azimuth %.1f; worst cell %.2f, mean %.2f"
              % (math.degrees(pf), math.degrees(a0), math.degrees(a1), tilt, az, wmin, wmean))
    fwd45 = [r for r in table if abs(r[2] - 45) < 1e-6 and abs(r[3] - 45) < 1e-6][0]
    print("readability: best guard haft tilt %.1f deg, azimuth %.0f deg (forward -> outboard): worst cell %.2f, mean %.2f of true length"
          % (tilt, az, wmin, wmean))
    print("   for scale, the centre of the predicate (tilt 45, azimuth 45): worst cell %.2f, mean %.2f" % (fwd45[0], fwd45[1]))
    HAFT_M = 0.69
    print("   per cell (camera yaw off his forward): " + "  ".join(
        "%d: %.0f px @ %+.0f deg" % (CELL0 + 45 * k, sc[k][0] * HAFT_M * PX_PER_M, sc[k][1]) for k in range(8)))

    # ---- 2. the chest: the unarmed idle's, per frame and mean -----------------------------------
    idle = anims['idle']
    kt, _ = channel(idle, idx['Hips'], 'rotation')
    nk = len(kt)
    chest_R = []
    chest_p = []
    spine_chain = ["Hips", "Spine02", "Spine01", "Spine"]
    for k in range(nk):
        M = np.eye(4)
        for nm in spine_chain:
            M = M @ local_at(idle, nm, k)
        chest_R.append(M[:3, :3] / np.cbrt(np.linalg.det(M[:3, :3])))
        chest_p.append(M[:3, 3])
    # THE IDLE'S STANCE FRAME, not its mean: the unarmed idle is not quiet -- its hips turn up to 49
    # deg and its chest swings over 138 deg of yaw, looking round with the feet planted -- so the new
    # idle holds ONE of its frames (the one whose chest faces most nearly his forward) and keeps
    # only its breathing, damped. The pose is solved at that chest.
    def chest_fwd(Rm):
        best_axis, best = None, -2
        return Rm
    # which chest axis is his forward? the one nearest +Z (his forward) at the mean
    qm0 = slerp_mean([quat_of(Rm) for Rm in chest_R])
    Cm0 = W.q2m(qm0)
    ax = int(np.argmax([abs(float((Cm0 @ e) @ F)) for e in np.eye(3)]))
    sgn = 1.0 if float((Cm0 @ np.eye(3)[ax]) @ F) > 0 else -1.0
    yaws = []
    for Rm in chest_R:
        f = sgn * (Rm @ np.eye(3)[ax]); yaws.append(math.degrees(math.atan2(float(f @ R), float(f @ F))))
    k0 = int(np.argmin([abs(y) for y in yaws]))
    if '--stance-key' in sys.argv:
        k0 = int(sys.argv[sys.argv.index('--stance-key') + 1])
    Cm = chest_R[k0]
    # ANOTHER STATE'S CHEST (the block turns his torso ~50 deg to present the shield): the same
    # guard in HIS frame, the arm solved against that chest instead
    if '--chest' in sys.argv:
        cq = [float(x) for x in sys.argv[sys.argv.index('--chest') + 1].split(',')]
        Cm = W.q2m(np.array(cq))
        print("chest override (skeleton space) %s" % cq)
    print("idle stance frame: key %d (%.3f s) -- its chest faces %+.1f deg off his forward (the idle's range %+.1f..%+.1f)"
          % (k0, float(kt[k0]), yaws[k0], min(yaws), max(yaws)))
    h_c = Cm.T @ h_world                          # the guard haft, in the chest's own frame
    # the fight walk's mean arm, as the natural prior (and its clavicle, kept)
    wk = anims['walk_armed']
    ref = {}
    for nm in [SH, ARM_, FORE]:
        t3, v3 = channel(wk, idx[nm], 'rotation')
        ref[nm] = W.q2m(slerp_mean(list(v3)))
    rest = {nm: W.trs(nodes[idx[nm]]) for nm in CHAIN}

    def chain(q_arm, q_fore):
        Xs = rest[SH].copy(); Xs[:3, :3] = ref[SH]
        Xa = rest[ARM_].copy(); Xa[:3, :3] = q_arm
        Xf = rest[FORE].copy(); Xf[:3, :3] = q_fore
        Xh = rest[HAND]                          # NEUTRAL WRIST: the rest rotation
        Xw = rest[WB]                            # the mount
        M1 = Xs @ Xa
        M2 = M1 @ Xf
        M3 = M2 @ Xh
        M4 = M3 @ Xw
        return M1, M2, M3, M4

    BOX = dict(fwd=(0.25, 0.45), out=(0.12, 0.32), up=(-0.35, -0.08))
    BOX_CHEST = '--box-frame' in sys.argv and sys.argv[sys.argv.index('--box-frame') + 1] == 'chest'
    if '--box' in sys.argv:
        # another state's grip box (the shield bash lunges: the fist rides higher to clear his thigh)
        bx = [float(x) for x in sys.argv[sys.argv.index('--box') + 1].split(',')]
        BOX = dict(fwd=(bx[0], bx[1]), out=(bx[2], bx[3]), up=(bx[4], bx[5]))
        print("grip box override %s" % BOX)

    def terms(x):
        qa = ref[ARM_] @ rotvec_to_m(x[:3])
        qf = ref[FORE] @ rotvec_to_m(x[3:])
        M1, M2, M3, M4 = chain(qa, qf)
        haft = M4[:3, :3] @ np.array([0, 1.0, 0]); haft /= np.linalg.norm(haft)
        edge = M4[:3, :3] @ np.array([0, 0, 1.0]); edge /= np.linalg.norm(edge)
        # metres, relative to the chest joint, in HIS frame at this chest; with --box-frame chest the OUTBOARD component is taken in the
        # CHEST's own frame instead (T12_12 / JOIN v2: the fist's offset from his centreline is the torso's -- at a twisted walk or run
        # chest the two differ), forward and up still in his
        grip_w = Cm @ M4[:3, 3] * mpu
        if BOX_CHEST:
            grip_w = grip_w + (float((M4[:3, 3] * mpu) @ RS) - float(grip_w @ RS)) * RS
        ang = math.degrees(math.acos(max(-1, min(1, float(haft @ h_c)))))
        pen = 0.0
        for key, axis in (("fwd", F), ("out", RS), ("up", U)):
            lo, hi = BOX[key]; v = float(grip_w @ axis)
            pen += max(0.0, lo - v) ** 2 + max(0.0, v - hi) ** 2
        e_w = Cm @ edge
        hd = math.degrees(math.atan2(float(e_w @ RS), float(e_w @ F)))
        epen = max(0.0, abs(hd) - 30.0) ** 2
        prior = float(np.linalg.norm(x[:3])) ** 2 + float(np.linalg.norm(x[3:])) ** 2
        elbow = M1[:3, 3]; wrist = M2[:3, 3]
        fore_dir = (M3[:3, 3] - wrist); fore_dir /= np.linalg.norm(fore_dir)
        up_dir = (wrist - elbow); up_dir /= np.linalg.norm(up_dir)
        return dict(ang=ang, pen=pen, hd=hd, epen=epen, prior=prior, grip=grip_w, haft=haft, edge=edge,
                    fore_haft=math.degrees(math.acos(max(-1, min(1, float(up_dir @ haft))))),
                    elbow_flex=math.degrees(math.acos(max(-1, min(1, float(up_dir @ ((elbow - M1[:3, 3]) if False else up_dir)))))),
                    qa=qa, qf=qf, M=(M1, M2, M3, M4))

    # --elbow-lint MIN: the nb_join joint lint's elbow measure (j_joint_lint.py, read and mirrored, not imported): the forearm's
    # direction in the UPPER ARM's own frame against the hinge direction the lint learned from the library (jlint learned.axes);
    # flexion = bend x cos(phi off that direction). The plain bend angle cannot see a humerus rolled past 90 deg, which reads as
    # the elbow bending backwards (T12_12c: pitched 37+ deg, the solver's cheapest branch put the forearm twist at ~155 and the
    # lint's flexion at -6..-67 while the bend was 95). Penalise flexion under MIN.
    ELB_MIN = float(sys.argv[sys.argv.index('--elbow-lint') + 1]) if '--elbow-lint' in sys.argv else None
    NAT_DIR = np.array([0.4699668394712067, 1.2347127842597921e-05, -0.8826840712536924]) if SIDE != 'L' else \
        np.array([-0.5068919263327467, 2.3524204857310536e-06, -0.8620096142231497])

    def lint_flex(t):
        M1, M2, M3, M4 = t["M"]
        Ru = M1[:3, :3] / np.linalg.norm(M1[:3, :3], axis=0)
        ax = Ru.T @ (M2[:3, 3] - M1[:3, 3]); ax = ax / np.linalg.norm(ax)
        d = Ru.T @ (M3[:3, 3] - M2[:3, 3]); d = d / np.linalg.norm(d)
        th = math.degrees(math.acos(max(-1, min(1, float(d @ ax)))))
        dev = d - (d @ ax) * ax; nd = np.linalg.norm(dev)
        nn = NAT_DIR - (NAT_DIR @ ax) * ax; nn = nn / np.linalg.norm(nn)
        if nd < 1e-9:
            return th
        dv = dev / nd; phi = math.atan2(float(np.cross(nn, dv) @ ax), float(nn @ dv))
        return th * math.cos(phi)

    def obj(x):
        t = terms(x)
        f = t["ang"] ** 2 + 4e4 * t["pen"] + t["epen"] + 40.0 * t["prior"]
        if ELB_MIN is not None:
            f += 100.0 * max(0.0, ELB_MIN - lint_flex(t)) ** 2
        return f

    bestx, bestf = None, 1e18
    rng = np.random.default_rng(7)
    for trial in range(40):
        x0 = rng.normal(0, 0.8, 6) if trial else np.zeros(6)
        r = minimize(obj, x0, method="Nelder-Mead", options=dict(maxiter=6000, xatol=1e-5, fatol=1e-7))
        r = minimize(obj, r.x, method="Powell", options=dict(maxiter=6000))
        if r.fun < bestf:
            bestf, bestx = r.fun, r.x
    t = terms(bestx)
    M1, M2, M3, M4 = t["M"]
    # elbow flexion: the angle between the upper arm (shoulder joint -> elbow) and the forearm
    sh = chain(t["qa"], t["qf"])[0]
    shoulder = rest[SH].copy(); shoulder[:3, :3] = ref[SH]
    p_sh = (shoulder @ rest[ARM_])[:3, 3]
    p_el = M2[:3, 3]; p_wr = M3[:3, 3]
    ua = p_el - p_sh; fa = p_wr - p_el
    flex = math.degrees(math.acos(max(-1, min(1, float(ua @ fa) / (np.linalg.norm(ua) * np.linalg.norm(fa))))))
    fa_n = fa / np.linalg.norm(fa)
    fore_vs_haft = math.degrees(math.acos(max(-1, min(1, float(fa_n @ t["haft"])))))
    print("pose: haft %.2f deg off the guard; grip fwd %+.3f out %+.3f up %+.3f m of the chest (box fwd %s out %s up %s); edge heading %+.1f deg"
          % (t["ang"], t["grip"] @ F, t["grip"] @ RS, t["grip"] @ U, BOX["fwd"], BOX["out"], BOX["up"], t["hd"]))
    print("      elbow flexion as the joint lint reads it: %.1f deg%s" % (lint_flex(t), (" (--elbow-lint %.0f)" % ELB_MIN) if ELB_MIN is not None else ""))
    print("      forearm to haft %.1f deg (square = 90); elbow bend %.1f deg; arm moved from the walk's mean arm by %.1f deg (upper) %.1f deg (fore)"
          % (fore_vs_haft, flex, math.degrees(np.linalg.norm(bestx[:3])), math.degrees(np.linalg.norm(bestx[3:]))))
    # the predicate over the idle's own chest motion (the pose rides the chest)
    ok = 0
    for k in range(nk):
        hw = chest_R[k] @ t["haft"]; ew = chest_R[k] @ t["edge"]
        tl = math.degrees(math.acos(max(-1, min(1, float(hw @ U)))))
        hd = math.degrees(math.atan2(float(ew @ RS), float(ew @ F)))
        if 30 <= tl <= 60 and hw @ F > 0 and hw @ RS > 0 and abs(hd) <= 45:
            ok += 1
    print("      the guard predicate over the unarmed idle's %d frames, riding its chest: %d%%" % (nk, round(100 * ok / nk)))
    tl_ = []; fw_ = []; ou_ = []; hd_ = []; cang = []
    for k in range(nk):
        hw = chest_R[k] @ t["haft"]; ew = chest_R[k] @ t["edge"]
        tl_.append(math.degrees(math.acos(max(-1, min(1, float(hw @ U)))))); fw_.append(float(hw @ F)); ou_.append(float(hw @ RS))
        hd_.append(math.degrees(math.atan2(float(ew @ RS), float(ew @ F))))
        dq = W.m2q(chest_R[k] @ Cm.T); cang.append(math.degrees(2 * math.acos(min(1.0, abs(float(dq[3]))))))
    print("      over the idle: tilt %.1f..%.1f, fwd %+.2f..%+.2f, out %+.2f..%+.2f, edge %+.0f..%+.0f; the chest wanders %.1f deg (max) from its mean"
          % (min(tl_), max(tl_), min(fw_), max(fw_), min(ou_), max(ou_), min(hd_), max(hd_), max(cang)))
    out_stance = dict(key=k0, t=float(kt[k0]), chest_yaw=yaws[k0])
    out = dict(stance=out_stance, readability=dict(tilt=tilt, azimuth=az, worst=wmin, mean=wmean,
                                per_cell=[dict(cell_yaw=CELL0 + 45 * k, screen_px=round(sc[k][0] * HAFT_M * PX_PER_M, 1),
                                               screen_angle=round(sc[k][1], 1)) for k in range(8)],
                                centre_45_45=dict(worst=fwd45[0], mean=fwd45[1])),
               guard_world_his_frame=list(map(float, h_world)),
               side=SIDE,
               pose={SH: list(map(float, quat_of(ref[SH]))),
                     ARM_: list(map(float, quat_of(t["qa"]))),
                     FORE: list(map(float, quat_of(t["qf"]))),
                     HAND: list(map(float, quat_of(rest[HAND][:3, :3] / np.cbrt(np.linalg.det(rest[HAND][:3, :3])))))},
               checks=dict(haft_off_guard_deg=t["ang"], grip_m=list(map(float, t["grip"])), edge_heading=t["hd"],
                           forearm_to_haft_deg=fore_vs_haft, elbow_bend_deg=flex,
                           predicate_idle_pct=round(100 * ok / nk)))
    json.dump(out, open(outp, "w"), indent=1)
    print("wrote %s" % outp)


if __name__ == "__main__":
    main()
