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
    # HELM: a close helm -- ovoid skull, a bellows VISOR that projects forward
    # as a rounded snout below the skull's centre, and a GORGET collar that
    # FLARES outward to a rolled lip. (M-a reported the helm band at 0.819,
    # the second-worst, because the proxy had a plain sphere and a straight
    # collar; R-C9-56 step 0.)
    helm_rx=0.112, helm_ry=0.132, helm_rz=0.130, helm_y=0.010,
    # the painted head is NOT on the body centreline: the M-a overlays show
    # the proxy helm offset from the painted one in the same sense in every
    # view. One (head_x, head_y) for the whole head assembly, fitted.
    head_x=0.0, head_y=0.0,
    helm_apex=0.012,        # the crown rises to a slight point above the ovoid
    visor_r=0.060,          # visor half-height/width at the face
    visor_y=0.070,          # how far forward the visor root sits
    visor_len=0.085,        # how far the snout projects beyond its root
    visor_drop=0.045,       # how far BELOW the skull centre the snout sits
    visor_tip_r=0.034,      # the snout's radius at its front
    gorget_r_top=0.098, gorget_r_bot=0.158, gorget_h=0.105, gorget_z_off=0.012,
    chest_rx=0.190, chest_ry=0.132, chest_rz=0.175,
    waist_rx=0.152, waist_ry=0.112,
    fauld_r_top=0.172, fauld_r_bot=0.205, fauld_z_bot=0.860,
    fauld_ry_scale=1.0, skirt_ry_scale=1.0,   # set by layered(), not fitted
    skirt_r_top=0.198, skirt_r_bot=0.240, skirt_z_bot=0.745,
    tabard_half_w=0.185, tabard_y=0.150, tabard_z_bot=0.800, tabard_t=0.022,
    tabard_arc=0.085,       # how far the drape curves back at its edges
    shoulder_x=0.205,   # shoulder joint offset from centreline
    pauldron_r=0.104,
    uparm_r=0.062, forearm_r=0.053, gauntlet_r=0.068,
    arm_len_upper=0.300, arm_len_fore=0.275,
    hip_x=0.098,        # hip joint offset from centreline
    thigh_r=0.090, shin_r=0.070, poleyn_r=0.098,
    # ARTICULATION (R-C9-58). Real plate does not butt piece to piece at a
    # joint; the lames OVERLAP, and the poleyn is a cup sitting over both the
    # cuisse and the greave. Built as butt joints first, the knee and the
    # ankle opened under bend and the toe tore away from the sabaton. Each
    # piece now runs PAST its joint by these margins, so no bend in the used
    # range can open a gap.
    knee_lap=0.060,     # cuisse past the knee, greave above it
    ankle_lap=0.050,    # greave past the ankle, sabaton up to meet it
    toe_lap=0.040,      # the toe lame slides UNDER the sabaton, not beside it
    foot_len=0.310, foot_w=0.100, foot_h=0.100, toe_frac=0.44,
    toe_tip_w=0.016,        # the sabaton comes to a LONG taper, near a point
    toe_tip_h=0.020,
    toe_rise=0.022,         # and lifts slightly at the very tip
    foot_heel_back=0.25,   # heel BEHIND the ankle, as a fraction of foot_len
                           # (the first fit had none, and the overlays showed it)
    # --- rest pose (deg) ---------------------------------------------------
    arm_L_pitch=6.0, arm_L_roll=7.0,      # the free (left) arm, hanging
    fore_L_pitch=10.0,
    # the pollaxe (right) arm is solved by IK to the MEASURED grip point
    # (gx = +0.195 H, gy = +0.162 H from the eight mattes; gz from the E still's
    # grip mark at 0.3005 H below the crown -- knight_rig_E.json)
    grip_x=0.351, grip_y=0.292, grip_z=1.259,
    # The pollaxe HEAD's bearing about the haft axis, degrees from the
    # figure's FORWARD (+Y) toward its RIGHT (+X). R-C9-57: the first build
    # had the fan on -Y, behind the knight, which is what Matt saw. Three
    # instruments agree on ~70 deg -- fan outboard with a forward lean, fluke
    # on the near side: the head's area centroid over eight mattes (71.7 deg),
    # the same fit on the fan's reach, and a sweep of the rendered head's
    # eight-view asymmetry profile against the stills' (peak 70 deg, flat from
    # 60 to 100 because the stills draw the head at nearly the same
    # orientation whatever the yaw). NOT fitted by the silhouette fitter: the
    # weapon is excluded from the body fit.
    head_bearing_deg=70.0,
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
    "tabard_half_w", "tabard_y", "tabard_z_bot", "tabard_arc",
    "shoulder_x", "pauldron_r",
    "uparm_r", "forearm_r", "gauntlet_r",
    "thigh_r", "shin_r", "poleyn_r", "knee_lap", "ankle_lap", "toe_lap",
    "foot_len", "foot_w", "foot_heel_back",
    "toe_frac", "toe_tip_w", "toe_tip_h", "toe_rise",
    "helm_apex", "visor_r", "visor_y", "visor_len", "visor_drop", "visor_tip_r",
    "gorget_r_top", "gorget_r_bot", "gorget_h", "gorget_z_off",
    "head_x", "head_y",
    "hip_x",
]
SHAPE_BOUNDS = {k: (0.55 * DEFAULTS[k], 1.75 * DEFAULTS[k]) for k in SHAPE_KEYS}
SHAPE_BOUNDS["tabard_z_bot"] = (0.62, 0.95)
SHAPE_BOUNDS["skirt_z_bot"] = (0.60, 0.88)
SHAPE_BOUNDS["tabard_y"] = (0.10, 0.24)
SHAPE_BOUNDS["tabard_arc"] = (0.02, 0.15)
SHAPE_BOUNDS["toe_frac"] = (0.30, 0.58)
SHAPE_BOUNDS["gorget_z_off"] = (-0.03, 0.06)
SHAPE_BOUNDS["toe_rise"] = (0.0, 0.06)
SHAPE_BOUNDS["head_x"] = (-0.10, 0.10)
SHAPE_BOUNDS["head_y"] = (-0.10, 0.10)

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


def _cone_pts(z0, r0, z1, r1, centre_xy=(0.0, 0.0), n=20, ry_scale=1.0):
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    out = []
    for z, r in ((z0, r0), (z1, r1)):
        out.append(np.stack([centre_xy[0] + r * np.cos(ang),
                             centre_xy[1] + r * ry_scale * np.sin(ang),
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
    """build_parts + layer order + prehull: what the fitter should use."""
    return prehull(build_parts(layered(p)))


def layered(p):
    """Apply the LAYER ORDER, which a silhouette fit cannot see.

    A silhouette says how deep the hips are; it does not say whether the depth
    belongs to the fauld or to the tabard hanging over it. The fit put the
    tabard INSIDE the fauld, so in the render the fauld poked through the
    tabard and took the tabard's gold with it.

    The garment order is not in doubt: mail skirt, then fauld, then the tabard
    over both. So: the TABARD becomes the outermost layer at exactly the depth
    the fit measured, and the fauld and skirt are flattened in Y (their X is
    untouched) to sit behind it. The OUTER SILHOUETTE is unchanged in both the
    frontal and the profile views by construction -- only the order changes.
    """
    q = dict(p)
    g = lambda k: q.get(k, DEFAULTS[k])
    t2 = g("tabard_t") / 2.0
    depth = max(g("fauld_r_bot"), g("skirt_r_bot"), g("tabard_y") + t2)
    q["tabard_y"] = depth - t2
    inner = depth - t2 - 0.016              # behind the tabard's inner face
    q["fauld_ry_scale"] = min(1.0, inner / max(g("fauld_r_bot"), 1e-6))
    q["skirt_ry_scale"] = min(1.0, (inner + 0.010) / max(g("skirt_r_bot"), 1e-6))
    return q


def joints(p):
    """The skeleton's joint positions for these parameters.

    ONE definition, used by build_parts(), by the Blender builder and by the
    animator -- the M-a drift (a mesh written twice and fitted once) is not
    going to be repeated for the skeleton.
    """
    g = lambda k: p.get(k, DEFAULTS[k])
    z_sh, z_hip = g("z_shoulder"), g("z_hip")
    z_waist, z_knee, z_ank = g("z_waist"), g("z_knee"), g("z_ankle")
    J = {}
    J["Hips"] = np.array([0.0, 0.0, z_hip])
    J["Spine"] = np.array([0.0, 0.0, z_hip + 0.09])
    J["Spine1"] = np.array([0.0, 0.0, z_waist])
    J["Spine2"] = np.array([0.0, 0.0, 0.5 * (z_waist + z_sh) + 0.02])
    J["Neck"] = np.array([0.0, 0.0, z_sh + 0.055])
    J["Head"] = np.array([g("head_x") * 0.6, g("head_y") * 0.6, g("z_neck")])
    J["HeadTop_End"] = np.array([g("head_x"), g("head_y"), g("z_crown")])
    for side, sx, S in (("Left", -1.0, "L"), ("Right", 1.0, "R")):
        J[side + "Shoulder"] = np.array([sx * 0.045, 0.0, z_sh + 0.045])
        sh = np.array([sx * g("shoulder_x"), 0.0, z_sh])
        J[side + "Arm"] = sh
        if S == "R":
            el, wr = _ik2(sh, np.array([g("grip_x"), g("grip_y"), g("grip_z")]),
                          g("arm_len_upper"), g("arm_len_fore"),
                          pole=np.array([0.35, -0.45, -1.0]))
        else:
            R1 = _rot("z", -sx * g("arm_L_roll")) @ _rot("x", g("arm_L_pitch"))
            el = sh + R1 @ np.array([0, 0, -g("arm_len_upper")])
            R2 = R1 @ _rot("x", g("fore_L_pitch"))
            wr = el + R2 @ np.array([0, 0, -g("arm_len_fore")])
        J[side + "ForeArm"] = el
        J[side + "Hand"] = wr
        d = wr - el
        d = d / max(np.linalg.norm(d), 1e-9)
        J[side + "HandEnd"] = wr + d * 0.115
        hip = np.array([sx * g("hip_x"), 0.0, z_hip])
        Rl = _rot("y", sx * g("leg_%s_splay" % S)) @ _rot("x", g("leg_%s_pitch" % S))
        knee = hip + Rl @ np.array([0, 0, -(z_hip - z_knee)])
        Rk = Rl @ _rot("x", g("knee_%s_pitch" % S))
        ank = knee + Rk @ np.array([0, 0, -(z_knee - z_ank)])
        fy = _rot("z", g("foot_%s_yaw" % S))
        fl, tf, hb = g("foot_len"), g("toe_frac"), g("foot_heel_back")
        toe = ank + fy @ np.array([0, fl * (1 - tf - hb), -(z_ank - g("foot_h") * 0.5)])
        J[side + "UpLeg"] = hip
        J[side + "Leg"] = knee
        J[side + "Foot"] = ank
        J[side + "ToeBase"] = toe
        J[side + "Toe_End"] = toe + fy @ np.array([0, fl * tf, -g("foot_h") * 0.18])
    # non-standard chains (tabard pendulum R-C9-36, mail-skirt quadrants) and
    # the weapon sockets -- here too, so the animator and the Blender builder
    # cannot disagree about where they start.
    z0, z1 = z_waist, g("tabard_z_bot")
    for tag, ys in (("F", 1.0), ("B", -1.0)):
        for i in range(4):
            J["TAB_%s_%02d" % (tag, i + 1)] = np.array(
                [0.0, ys * g("tabard_y"), z0 + (z1 - z0) * i / 3.0])
    for tag, (dx, dy) in (("F", (0, 1)), ("B", (0, -1)), ("L", (-1, 0)), ("R", (1, 0))):
        J["SKIRT_%s" % tag] = np.array([dx * g("skirt_r_top") * 0.6,
                                        dy * g("skirt_r_top") * 0.6, z_hip - 0.02])
        J["SKIRT_%s_end" % tag] = np.array([dx * g("skirt_r_bot") * 0.7,
                                            dy * g("skirt_r_bot") * 0.7, g("skirt_z_bot")])
    J["SOCK_WeaponMain"] = J["RightHand"].copy()
    J["SOCK_WeaponMain_end"] = J["RightHand"] + np.array([0.0, 0.0, 0.12])
    J["SOCK_WeaponGripFar"] = J["RightHand"] + np.array([0.0, 0.0, 0.30])
    J["SOCK_WeaponGripFar_end"] = J["RightHand"] + np.array([0.0, 0.0, 0.42])
    J["SOCK_OffHand"] = J["LeftHand"].copy()
    J["SOCK_OffHand_end"] = J["LeftHand"] + np.array([0.0, 0.0, 0.10])
    return J


def build_parts(p):
    """Return [(name, bone, Nx3 point cloud), ...] for the given parameter dict."""
    g = lambda k: p.get(k, DEFAULTS[k])
    parts = []

    z_crown, z_neck = g("z_crown"), g("z_neck")
    z_sh, z_el = g("z_shoulder"), g("z_elbow")
    z_waist, z_hip = g("z_waist"), g("z_hip")
    z_knee, z_ank = g("z_knee"), g("z_ankle")

    # --- head ------------------------------------------------------------
    hx, hy = g("head_x"), g("head_y")
    hrz = g("helm_rz")
    hz = z_crown - hrz - g("helm_apex")
    skull = _ellipsoid_pts((hx, hy + g("helm_y"), hz),
                           (g("helm_rx"), g("helm_ry"), hrz))
    apex = _ellipsoid_pts((hx, hy + g("helm_y") - 0.012, hz + hrz * 0.55),
                          (g("helm_rx") * 0.42, g("helm_ry") * 0.42,
                           hrz * 0.45 + g("helm_apex")))
    parts.append(("helm", "Head", np.concatenate([skull, apex], 0)))
    # the visor snout: a tapered capsule from the face forward and down
    vroot = np.array([hx, hy + g("visor_y"), hz - g("visor_drop")])
    vtip = vroot + np.array([0.0, g("visor_len"), -g("visor_len") * 0.22])
    parts.append(("visor", "Head",
                  _capsule_pts(vroot, vtip, g("visor_r"), g("visor_tip_r"))))
    gz = z_neck + g("gorget_z_off")
    parts.append(("gorget", "Neck",
                  _cone_pts(gz + g("gorget_h") / 2, g("gorget_r_top"),
                            gz - g("gorget_h") / 2, g("gorget_r_bot"),
                            centre_xy=(hx * 0.6, hy * 0.6))))

    # --- torso ------------------------------------------------------------
    z_chest = 0.5 * (z_sh + z_waist) + 0.02
    parts.append(("breastplate", "Spine2",
                  _ellipsoid_pts((0, 0.008, z_chest),
                                 (g("chest_rx"), g("chest_ry"), g("chest_rz")))))
    parts.append(("waist", "Spine",
                  _ellipsoid_pts((0, 0.0, z_waist - 0.02),
                                 (g("waist_rx"), g("waist_ry"), 0.085))))
    parts.append(("fauld", "Hips",
                  _cone_pts(z_hip + 0.055, g("fauld_r_top"), g("fauld_z_bot"),
                            g("fauld_r_bot"), ry_scale=p.get("fauld_ry_scale", 1.0))))
    parts.append(("mail_skirt", "Hips",          # deforms; proxy is a cone
                  _cone_pts(z_hip - 0.02, g("skirt_r_top"), g("skirt_z_bot"),
                            g("skirt_r_bot"), ry_scale=p.get("skirt_ry_scale", 1.0))))

    # The tabard: two panels front and back, hanging from the shoulders and
    # DRAPED -- each is an arc across the body, deepest on the centreline and
    # curving back at its edges, not a flat slab. Written as a slab first;
    # once layered() moved it outside the fauld (which it must be -- it hangs
    # over it) a slab's corners stuck out in the oblique views and cost 2.4
    # points of IoU. A drape costs nothing, because that is the shape it is.
    tw, ty, tzb, tt = g("tabard_half_w"), g("tabard_y"), g("tabard_z_bot"), g("tabard_t")
    arc = g("tabard_arc")
    ztop = z_sh + 0.03
    for sgn, nm in ((1, "tabard_front"), (-1, "tabard_back")):
        pts = []
        for fx in np.linspace(-1.0, 1.0, 7):
            x = fx * tw
            y = sgn * (ty - arc * fx * fx)
            for z in (ztop, tzb):
                pts.append((x, y + sgn * tt / 2, z))
                pts.append((x, y - sgn * tt / 2, z))
        parts.append((nm, "Tabard_01", np.array(pts)))

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
        kl, al = g("knee_lap"), g("ankle_lap")
        d_th = knee - hip; d_th = d_th / max(np.linalg.norm(d_th), 1e-9)
        d_sh = ank - knee; d_sh = d_sh / max(np.linalg.norm(d_sh), 1e-9)
        # the cuisse runs PAST the knee; the greave starts ABOVE it; the
        # poleyn is a cup over both
        parts.append(("cuisse_%s" % side, "%sUpLeg" % BL,
                      _capsule_pts(hip, knee + d_th * kl,
                                   g("thigh_r"), g("thigh_r") * 0.86)))
        parts.append(("poleyn_%s" % side, "%sLeg" % BL,
                      _ellipsoid_pts(knee + d_sh * 0.004,
                                     (g("poleyn_r"), g("poleyn_r") * 0.96,
                                      g("poleyn_r") * 1.02))))
        parts.append(("greave_%s" % side, "%sLeg" % BL,
                      _capsule_pts(knee - d_sh * kl, ank + d_sh * al,
                                   g("shin_r") * 1.04, g("shin_r") * 0.80)))
        # foot: heel block on Foot, pointed toe on ToeBase (the toe MUST break)
        fy = _rot("z", g("foot_%s_yaw" % side))
        fl, fw, fh, tf = g("foot_len"), g("foot_w"), g("foot_h"), g("toe_frac")
        hb = g("foot_heel_back")
        # the sabaton runs UP past the ankle to overlap the greave
        top = z_ank + g("ankle_lap") * 0.9
        heel_c = ank + fy @ np.array([0, fl * ((1 - tf) / 2 - hb), 0]) \
            - np.array([0, 0, z_ank - top / 2])
        parts.append(("sabaton_%s" % side, "%sFoot" % BL,
                      _box_pts(heel_c, (fw / 2, fl * (1 - tf) / 2, top / 2), fy)))
        # the toe: a LONG taper to a near-point, lifted a little at the tip
        toe_c = ank + fy @ np.array([0, fl * (1 - tf / 2 - hb), -(z_ank - fh * 0.40)])
        tw2, th2, ri = g("toe_tip_w") / 2, g("toe_tip_h") / 2, g("toe_rise")
        tl = g("toe_lap")
        # the toe lame slides UNDER the sabaton: its rear runs back inside the
        # piece behind it and is slightly narrower there, so it nests
        toe_pts = np.array([
            [-fw / 2 * 0.90, -fl * tf / 2 - tl, -fh * 0.26],
            [fw / 2 * 0.90, -fl * tf / 2 - tl, -fh * 0.26],
            [-fw / 2 * 0.86, -fl * tf / 2 - tl, fh * 0.34],
            [fw / 2 * 0.86, -fl * tf / 2 - tl, fh * 0.34],
            [-fw / 2, -fl * tf / 2, -fh * 0.40], [fw / 2, -fl * tf / 2, -fh * 0.40],
            [-fw / 2 * 0.96, -fl * tf / 2, fh * 0.50], [fw / 2 * 0.96, -fl * tf / 2, fh * 0.50],
            # a mid rib so the taper is a curve, not a single straight bevel
            [-fw * 0.30, fl * tf * 0.10, -fh * 0.38], [fw * 0.30, fl * tf * 0.10, -fh * 0.38],
            [-fw * 0.28, fl * tf * 0.10, fh * 0.26], [fw * 0.28, fl * tf * 0.10, fh * 0.26],
            [-tw2, fl * tf / 2, -fh * 0.40 + ri], [tw2, fl * tf / 2, -fh * 0.40 + ri],
            [-tw2, fl * tf / 2, -fh * 0.40 + ri + 2 * th2],
            [tw2, fl * tf / 2, -fh * 0.40 + ri + 2 * th2]])
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


try:
    from scipy.spatial import ConvexHull as _CH
except Exception:          # Blender ships no scipy; it only needs build_parts()
    _CH = None


def _hull(xy):
    """2D convex hull vertices in order (qhull; C speed -- this runs inside
    the fitter's inner loop tens of thousands of times)."""
    if _CH is None:
        raise RuntimeError("_hull needs scipy; run the fitter under system python")
    try:
        return xy[_CH(xy).vertices]
    except Exception:
        return xy


def prehull(parts):
    """Reduce each part's point cloud to its 3D convex-hull vertices once, so
    the fitter projects a few dozen points per part instead of a few hundred.
    The silhouette is unchanged: a convex body's outline is decided by its
    hull vertices."""
    out = []
    for name, bone, pts in parts:
        if _CH is not None and len(pts) > 12:
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
