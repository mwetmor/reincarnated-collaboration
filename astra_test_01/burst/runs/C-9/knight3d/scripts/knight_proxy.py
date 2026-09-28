#!/usr/bin/env python3
"""C-9 knight3d: the parametric knight proxy, shared by the fitter and the
Blender builder, so the thing that is FITTED and the thing that is BUILT are
the same body.

Coordinate frame (Blender convention, Z up):
    +X = the figure's RIGHT      +Y = the figure's FACING          +Z = up
    origin = on the ground, between the feet.

Camera: ORTHOGRAPHIC, azimuth alpha (deg, about Z) and elevation theta (deg).
    camera-position direction  c = ( sin a cos t,  cos a cos t,  sin t )
    screen right               r = (-cos a,        sin a,        0     )
    screen up                  u = (-sin t sin a, -sin t cos a,  cos t )
    a = 0  -> camera in FRONT of the figure; the figure's right lands on screen
              LEFT (as it does when someone faces you)                    = S
    a = 90 -> camera on the figure's right; the figure's facing lands on
              screen +X                                                   = E
Nominal per-direction azimuths: S 0, SE 45, E 90, NE 135, N 180, NW 225,
W 270, SW 315.

VERIFIED against the stills before any fitting: the pollaxe grip's screen
offset from the body centreline, measured on the eight mattes, is
 S -0.191H, N +0.198H (so the grip is at the figure's RIGHT, gx=+0.195H) and
 E +0.169H, W -0.156H (so the grip is FORWARD of the chest, gy=+0.162H),
which is exactly the sign pattern this basis predicts for a single 3D point.
(The four DIAGONAL views do NOT agree with that point -- see the report.)

Silhouette: the body is a UNION of convex solids, and the silhouette of a
union of solids is the union of their silhouettes, so each solid is projected
independently and its 2D convex hull filled. Exact for convex parts, and it
never needs a renderer inside the optimiser loop.
"""
import math
import numpy as np

# ---------------------------------------------------------------- parameters

# Vertical layout, MEASURED from the E still's joint marks
# (cliffside_B/frames/knight_rig_E.json, probe R-C9-34: crown 414 px, sole 1286
# px, figure height 872 px) and expressed as height above ground in metres for
# a figure whose helm crown is at H_TOTAL.
H_TOTAL = 1.80

DEFAULTS = dict(
    # --- skeleton heights (m above ground) -------------------------------
    z_crown=1.800,      # top of helm       (E still 414 px)
    z_neck=1.470,       # 0.183 H below crown (E still 574)
    z_shoulder=1.350,   # 0.250 H           (E still 632)
    z_elbow=1.185,      # 0.342 H           (E still 712)
    z_waist=1.040,      # 0.422 H           (E still 782)
    z_hip=0.941,        # 0.477 H           (E still 830)
    z_knee=0.565,       # 0.686 H           (E still 1012)
    z_ankle=0.146,      # 0.919 H           (E still 1215)
    # --- widths / depths --------------------------------------------------
    helm_rx=0.112, helm_ry=0.132, helm_rz=0.130, helm_y=0.010,
    visor_r=0.068, visor_y=0.095,
    gorget_r=0.112, gorget_h=0.085,
    chest_rx=0.190, chest_ry=0.132, chest_rz=0.175,
    waist_rx=0.152, waist_ry=0.112,
    fauld_r_top=0.172, fauld_r_bot=0.205, fauld_z_bot=0.860,
    skirt_r_top=0.198, skirt_r_bot=0.240, skirt_z_bot=0.745,
    tabard_half_w=0.185, tabard_y=0.150, tabard_z_bot=0.800, tabard_t=0.022,
    shoulder_x=0.205,   # shoulder joint offset from centreline
    pauldron_r=0.104,
    uparm_r=0.062, forearm_r=0.053, gauntlet_r=0.068,
    arm_len_upper=0.300, arm_len_fore=0.275,
    hip_x=0.098,        # hip joint offset from centreline
    thigh_r=0.090, shin_r=0.070, poleyn_r=0.082,
    foot_len=0.310, foot_w=0.100, foot_h=0.100, toe_frac=0.38,
    foot_heel_back=0.25,   # heel BEHIND the ankle, as a fraction of foot_len
                           # (the first fit had none, and the overlays showed it)
    # --- rest pose (deg) ---------------------------------------------------
    arm_L_pitch=6.0, arm_L_roll=7.0,      # the free (left) arm, hanging
    fore_L_pitch=10.0,
    # the pollaxe (right) arm is solved by IK to the MEASURED grip point
    # (gx = +0.195 H, gy = +0.162 H from the eight mattes; gz from the E still's
    # grip mark at 0.3005 H below the crown -- knight_rig_E.json)
    grip_x=0.351, grip_y=0.292, grip_z=1.259,
    leg_L_pitch=0.0, leg_L_splay=4.0, foot_L_yaw=14.0,
    leg_R_pitch=0.0, leg_R_splay=4.0, foot_R_yaw=-14.0,
    knee_L_pitch=0.0, knee_R_pitch=0.0,
)

# parameters the shape optimiser is allowed to move, with bounds (m or deg)
SHAPE_KEYS = [
    "helm_rx", "helm_ry", "helm_rz",
    "chest_rx", "chest_ry", "chest_rz",
    "fauld_r_top", "fauld_r_bot",
    "skirt_r_bot", "skirt_z_bot",
    "tabard_half_w", "tabard_y", "tabard_z_bot",
    "shoulder_x", "pauldron_r",
    "uparm_r", "forearm_r", "gauntlet_r",
    "thigh_r", "shin_r", "poleyn_r",
    "foot_len", "foot_w", "foot_heel_back",
    "hip_x",
]
SHAPE_BOUNDS = {k: (0.55 * DEFAULTS[k], 1.75 * DEFAULTS[k]) for k in SHAPE_KEYS}
SHAPE_BOUNDS["tabard_z_bot"] = (0.62, 0.95)
SHAPE_BOUNDS["skirt_z_bot"] = (0.60, 0.88)
SHAPE_BOUNDS["tabard_y"] = (0.10, 0.24)

POSE_KEYS = ["arm_L_pitch", "arm_L_roll", "fore_L_pitch",
             "grip_x", "grip_y", "grip_z",
             "leg_L_pitch", "leg_R_pitch", "knee_L_pitch", "knee_R_pitch",
             "leg_L_splay", "leg_R_splay", "foot_L_yaw", "foot_R_yaw"]


# ------------------------------------------------------------------- helpers

def _rot(axis, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _ellipsoid_pts(centre, radii, R=None, n=9):
    """Surface samples of an ellipsoid (optionally rotated by R)."""
    u = np.linspace(0, 2 * np.pi, n * 2, endpoint=False)
    v = np.linspace(0, np.pi, n)
    uu, vv = np.meshgrid(u, v)
    p = np.stack([np.sin(vv) * np.cos(uu), np.sin(vv) * np.sin(uu),
                  np.cos(vv)], -1).reshape(-1, 3) * np.asarray(radii)
    if R is not None:
        p = p @ R.T
    return p + np.asarray(centre)


def _capsule_pts(a, b, ra, rb=None, n=9):
    """Surface samples of a tapered capsule from a to b (radius ra -> rb).

    The ring layout is IDENTICAL to prim_capsule() in 04_build_blender.py -- if
    the fitter's solid and the built mesh are different shapes then the fit
    proves nothing about the thing that gets animated (measured: they differed
    by 6.6 % IoU before this was aligned).
    """
    a = np.asarray(a, float); b = np.asarray(b, float)
    rb = ra if rb is None else rb
    d = b - a
    L = np.linalg.norm(d)
    if L < 1e-9:
        return _ellipsoid_pts(a, (ra, ra, ra), n=n)
    w = d / L
    tmp = np.array([0, 0, 1.0]) if abs(w[2]) < 0.9 else np.array([1.0, 0, 0])
    e1 = np.cross(w, tmp); e1 /= np.linalg.norm(e1)
    e2 = np.cross(w, e1)
    seg = 16
    ang = np.linspace(0, 2 * np.pi, seg, endpoint=False)
    ring = np.cos(ang)[:, None] * e1 + np.sin(ang)[:, None] * e2
    out = []
    for c, r in ((a - w * ra * 0.65, ra * 0.55), (a, ra),
                 (b, rb), (b + w * rb * 0.65, rb * 0.55)):
        out.append(c + r * ring)
    return np.concatenate(out, 0)


def _cone_pts(z0, r0, z1, r1, centre_xy=(0.0, 0.0), n=20):
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    out = []
    for z, r in ((z0, r0), (z1, r1)):
        out.append(np.stack([centre_xy[0] + r * np.cos(ang),
                             centre_xy[1] + r * np.sin(ang),
                             np.full(n, z)], -1))
    return np.concatenate(out, 0)


def _ik2(root, target, l1, l2, pole):
    """Two-bone IK. Returns (elbow, wrist); the elbow is placed on the side of
    the root->target line that `pole` points to."""
    root = np.asarray(root, float); target = np.asarray(target, float)
    d = target - root
    L = np.linalg.norm(d)
    L = min(L, (l1 + l2) * 0.999)
    L = max(L, abs(l1 - l2) * 1.001)
    n = d / max(np.linalg.norm(d), 1e-9)
    # projection of the elbow along the chain, and its offset from it
    a = (l1 * l1 - l2 * l2 + L * L) / (2 * L)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    pv = np.asarray(pole, float)
    pv = pv - n * (pv @ n)
    if np.linalg.norm(pv) < 1e-6:
        pv = np.array([0, 0, -1.0]) - n * (n[2] * -1.0)
    pv /= np.linalg.norm(pv)
    elbow = root + n * a + pv * h
    wrist = root + n * L
    return elbow, wrist


def _box_pts(centre, half, R=None):
    s = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)],
                 float) * np.asarray(half)
    if R is not None:
        s = s @ R.T
    return s + np.asarray(centre)


# --------------------------------------------------------------- the proxy

def build(p):
    """build_parts + prehull: what the fitter should use."""
    return prehull(build_parts(p))


def build_parts(p):
    """Return [(name, bone, Nx3 point cloud), ...] for the given parameter dict."""
    g = lambda k: p.get(k, DEFAULTS[k])
    parts = []

    z_crown, z_neck = g("z_crown"), g("z_neck")
    z_sh, z_el = g("z_shoulder"), g("z_elbow")
    z_waist, z_hip = g("z_waist"), g("z_hip")
    z_knee, z_ank = g("z_knee"), g("z_ankle")

    # --- head ------------------------------------------------------------
    hrz = g("helm_rz")
    hz = z_crown - hrz
    parts.append(("helm", "Head", _ellipsoid_pts((0, g("helm_y"), hz),
                                                 (g("helm_rx"), g("helm_ry"), hrz))))
    parts.append(("visor", "Head", _ellipsoid_pts((0, g("visor_y"), hz - 0.012),
                                                  (g("visor_r") * 0.85, g("visor_r"),
                                                   g("visor_r") * 0.78))))
    parts.append(("gorget", "Neck", _cone_pts(z_neck - g("gorget_h") / 2, g("gorget_r") * 0.86,
                                              z_neck + g("gorget_h") / 2, g("gorget_r"))))

    # --- torso ------------------------------------------------------------
    z_chest = 0.5 * (z_sh + z_waist) + 0.02
    parts.append(("breastplate", "Spine2",
                  _ellipsoid_pts((0, 0.008, z_chest),
                                 (g("chest_rx"), g("chest_ry"), g("chest_rz")))))
    parts.append(("waist", "Spine",
                  _ellipsoid_pts((0, 0.0, z_waist - 0.02),
                                 (g("waist_rx"), g("waist_ry"), 0.085))))
    parts.append(("fauld", "Hips",
                  _cone_pts(z_hip + 0.055, g("fauld_r_top"), g("fauld_z_bot"), g("fauld_r_bot"))))
    parts.append(("mail_skirt", "Hips",          # deforms; proxy is a cone
                  _cone_pts(z_hip - 0.02, g("skirt_r_top"), g("skirt_z_bot"), g("skirt_r_bot"))))

    # tabard: two panels front and back, hanging from the shoulders
    tw, ty, tzb, tt = g("tabard_half_w"), g("tabard_y"), g("tabard_z_bot"), g("tabard_t")
    for sgn, nm in ((1, "tabard_front"), (-1, "tabard_back")):
        parts.append((nm, "Tabard_01",
                      _box_pts((0, sgn * ty, 0.5 * (z_sh + 0.03 + tzb)),
                               (tw, tt, 0.5 * (z_sh + 0.03 - tzb)))))

    # --- arms -------------------------------------------------------------
    for side, sx in (("L", -1.0), ("R", 1.0)):
        sh = np.array([sx * g("shoulder_x"), 0.0, z_sh])
        if side == "R":
            # the pollaxe arm: 2-bone IK to the MEASURED grip point, so the
            # hand is where the stills put it rather than where a guess puts it
            tgt = np.array([g("grip_x"), g("grip_y"), g("grip_z")])
            el, wr = _ik2(sh, tgt, g("arm_len_upper"), g("arm_len_fore"),
                          pole=np.array([0.35, -0.45, -1.0]))
        else:
            R1 = _rot("z", -sx * g("arm_%s_roll" % side)) @ _rot("x", g("arm_%s_pitch" % side))
            el = sh + R1 @ np.array([0, 0, -g("arm_len_upper")])
            R2 = R1 @ _rot("x", g("fore_%s_pitch" % side))
            wr = el + R2 @ np.array([0, 0, -g("arm_len_fore")])
        parts.append(("pauldron_%s" % side, "%sArm" % ("Left" if side == "L" else "Right"),
                      _ellipsoid_pts(sh + np.array([sx * 0.03, 0, 0.015]),
                                     (g("pauldron_r"), g("pauldron_r") * 1.10,
                                      g("pauldron_r") * 0.95))))
        parts.append(("rerebrace_%s" % side, "%sArm" % ("Left" if side == "L" else "Right"),
                      _capsule_pts(sh, el, g("uparm_r"), g("uparm_r") * 0.86)))
        parts.append(("couter_%s" % side, "%sForeArm" % ("Left" if side == "L" else "Right"),
                      _ellipsoid_pts(el, (g("uparm_r") * 0.95,) * 3)))
        parts.append(("vambrace_%s" % side, "%sForeArm" % ("Left" if side == "L" else "Right"),
                      _capsule_pts(el, wr, g("forearm_r"), g("forearm_r") * 0.82)))
        d = wr - el
        d = d / max(np.linalg.norm(d), 1e-9)
        hand = wr + d * 0.055
        parts.append(("gauntlet_%s" % side, "%sHand" % ("Left" if side == "L" else "Right"),
                      _ellipsoid_pts(hand, (g("gauntlet_r") * 0.8, g("gauntlet_r"),
                                            g("gauntlet_r") * 1.05))))

    # --- legs -------------------------------------------------------------
    for side, sx in (("L", -1.0), ("R", 1.0)):
        hip = np.array([sx * g("hip_x"), 0.0, z_hip])
        Rl = _rot("z", 0.0) @ _rot("y", sx * g("leg_%s_splay" % side)) \
            @ _rot("x", g("leg_%s_pitch" % side))
        knee = hip + Rl @ np.array([0, 0, -(z_hip - z_knee)])
        Rk = Rl @ _rot("x", g("knee_%s_pitch" % side))
        ank = knee + Rk @ np.array([0, 0, -(z_knee - z_ank)])
        BL = "Left" if side == "L" else "Right"
        parts.append(("cuisse_%s" % side, "%sUpLeg" % BL,
                      _capsule_pts(hip, knee, g("thigh_r"), g("thigh_r") * 0.80)))
        parts.append(("poleyn_%s" % side, "%sLeg" % BL,
                      _ellipsoid_pts(knee, (g("poleyn_r"), g("poleyn_r") * 0.95,
                                            g("poleyn_r") * 0.88))))
        parts.append(("greave_%s" % side, "%sLeg" % BL,
                      _capsule_pts(knee, ank, g("shin_r") * 1.02, g("shin_r") * 0.72)))
        # foot: heel block on Foot, pointed toe on ToeBase (the toe MUST break)
        fy = _rot("z", g("foot_%s_yaw" % side))
        fl, fw, fh, tf = g("foot_len"), g("foot_w"), g("foot_h"), g("toe_frac")
        hb = g("foot_heel_back")
        heel_c = ank + fy @ np.array([0, fl * ((1 - tf) / 2 - hb), -(z_ank - fh / 2)])
        parts.append(("sabaton_%s" % side, "%sFoot" % BL,
                      _box_pts(heel_c, (fw / 2, fl * (1 - tf) / 2, fh / 2), fy)))
        toe_c = ank + fy @ np.array([0, fl * (1 - tf / 2 - hb), -(z_ank - fh * 0.40)])
        toe_pts = np.array([
            [-fw / 2, -fl * tf / 2, -fh * 0.40], [fw / 2, -fl * tf / 2, -fh * 0.40],
            [-fw / 2, -fl * tf / 2, fh * 0.42], [fw / 2, -fl * tf / 2, fh * 0.42],
            [-fw * 0.06, fl * tf / 2, -fh * 0.34], [fw * 0.06, fl * tf / 2, -fh * 0.34],
            [-fw * 0.06, fl * tf / 2, fh * 0.02], [fw * 0.06, fl * tf / 2, fh * 0.02]])
        parts.append(("sabaton_toe_%s" % side, "%sToeBase" % BL,
                      (toe_pts @ fy.T) + toe_c))
    return parts


# ------------------------------------------------------------- projection

def basis(alpha_deg, theta_deg):
    a = math.radians(alpha_deg); t = math.radians(theta_deg)
    r = np.array([-math.cos(a), math.sin(a), 0.0])
    u = np.array([-math.sin(t) * math.sin(a), -math.sin(t) * math.cos(a), math.cos(t)])
    return r, u


def cam_dir(alpha_deg, theta_deg):
    a = math.radians(alpha_deg); t = math.radians(theta_deg)
    return np.array([math.sin(a) * math.cos(t), math.cos(a) * math.cos(t), math.sin(t)])


def project(pts, alpha_deg, theta_deg):
    r, u = basis(alpha_deg, theta_deg)
    return np.stack([pts @ r, pts @ u], -1)


from scipy.spatial import ConvexHull as _CH, QhullError as _QE


def _hull(xy):
    """2D convex hull vertices in order (qhull; C speed -- this runs inside
    the fitter's inner loop tens of thousands of times)."""
    try:
        h = _CH(xy)
        return xy[h.vertices]
    except Exception:
        return xy


def prehull(parts):
    """Reduce each part's point cloud to its 3D convex-hull vertices once, so
    the fitter projects a few dozen points per part instead of a few hundred.
    The silhouette is unchanged: a convex body's outline is decided by its
    hull vertices."""
    out = []
    for name, bone, pts in parts:
        if len(pts) > 12:
            try:
                pts = pts[_CH(pts).vertices]
            except Exception:
                pass
        out.append((name, bone, np.ascontiguousarray(pts)))
    return out


def rasterize(parts, alpha, theta, scale, tx, ty, W, H, exclude=()):
    """Silhouette of the union, as a bool image of size (H, W).
    scale = pixels per metre; (tx, ty) = image position of the world origin."""
    from PIL import Image, ImageDraw
    im = Image.new("1", (W, H), 0)
    dr = ImageDraw.Draw(im)
    r_, u_ = basis(alpha, theta)
    M = np.stack([r_ * scale, -u_ * scale], -1)          # 3x2
    off = np.array([tx, ty])
    for name, bone, pts in parts:
        if name in exclude:
            continue
        xy = pts @ M + off
        h = _hull(xy)
        if len(h) >= 3:
            dr.polygon([tuple(v) for v in h], fill=1)
    return np.asarray(im, dtype=bool)
