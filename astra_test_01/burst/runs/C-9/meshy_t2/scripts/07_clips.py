# C-9 meshy_t2 step 5: author the four clips on the quadruped rig.
#
#   blender -b -noaudio --python scripts/07_clips.py -- <rigged.blend> <outdir>
#
# The clips are built FEET-FIRST, which is what makes the plant exact rather
# than merely close:
#
#  * The clips are IN PLACE, so the ground runs backwards past the animal at
#    the gait speed v. A planted toe therefore has to travel backwards at
#    exactly v -- so the toe's world target during stance is AUTHORED as
#    y = y_touchdown - v*t, and the leg is solved to reach it. Zero slide is a
#    property of the construction, not an outcome to be tuned; the plant
#    instrument in step 6 then checks the construction survived the solve.
#
#  * The end effector is the TOE, not the heel or the ankle. This animal is
#    digitigrade (a hound stands on its toes), so the toe is the contact.
#    Anchoring the heel instead would have let the toe scrub through the
#    ground every time the paw pitched.
#
#  * IK by damped CCD in the LEG'S OWN SAGITTAL PLANE, whose normal is read
#    from the bone's world X axis rather than assumed to be world X -- the
#    pelvis yaws and rolls in the walk, and the leg plane yaws with it.
#    Joint limits are expressed as "keep the sign of the rest bend, within a
#    range", which is what holds the hind leg's REVERSE HOCK the right way
#    round under every target; an unsigned limit lets CCD flip the hock
#    forwards and produce a horse-legged goat.
#
# Gaits, and why these numbers:
#   WALK  lateral sequence LH -> LF -> RH -> RF, duty 0.70, 12 frames.
#   RUN   rotary gallop LH -> RH -> RF -> LF, duty 0.32, 8 frames, with a
#         suspension phase where no foot is down.
#   IDLE  all four planted; breathing, a head turn and a tail wave, 12 frames.
#   ATTACK lunge-and-bite, 12 frames, hind feet planted throughout.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("07_clips.py")][0]))
sys.path.insert(0, HERE)
import t2lib as T

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTDIR = a[0], a[1]
os.makedirs(OUTDIR, exist_ok=True)

# GROUND, and four measurements to get one number.
#
# The rig's contact point is the toe bone's TAIL at z = 0.010; at rest the
# mesh sole is at z = 0 and the heel pad -- skinned to the CANNON, not the paw
# -- has no clearance at all. So the moment a leg leaves its rest angle the
# heel digs in: 19-22 mm on the walk, 62 mm at the attack's deepest crouch,
# with the lowest vertex owned by `hcannon` on 10 of the walk's 12 frames.
#
# Three fixes were tried and each was measured rather than assumed to work:
#   1. hold the paw at its rest world orientation -> cured the sole, cost the
#      0.11 m of reach the paw was contributing, planted residual 3 -> 57 mm;
#   2. tighten the paw limit 16 -> 6 deg -> no change at all, because the paw
#      was never the bone that owned the lowest vertex;
#   3. raise the stance TARGET by the measured depth -> 22 mm of target bought
#      4 mm of sole. Raising the toe bends the leg, bending the leg rotates
#      the cannon upright, and an upright cannon swings its heel pad back
#      down. The feedback is ~87 % cancelling, so the sole sits ~15 mm below
#      the toe plane at any target height.
#
# So the sole's offset is a PROPERTY OF THE MESH, not an error to solve out.
# The stance target stays at the rest toe height, the sole is measured on
# every planted frame, and the RENDERER puts the ground row on the measured
# sole (clips.json -> ground_ref_z) instead of on the nominal z = 0.
GROUND_CLEARANCE = 0.0

HIND = {"R": ["thigh.R", "shin.R", "hcannon.R", "hpaw.R"],
        "L": ["thigh.L", "shin.L", "hcannon.L", "hpaw.L"]}
# The SCAPULA is part of the front chain, not a separately keyed bone. A dog's
# scapula swings with the stride and supplies a third of the front leg's
# forward reach: measured on this rig, the chain from the shoulder JOINT can
# put the toe inside y in [0.344, 0.946] at 94 % extension, and from the
# scapula top inside [0.118, 0.922] -- 0.60 m of usable excursion instead of
# 0.30 m. With the scapula held fixed, every walk stride over 0.43 m had the
# front foot out of reach, which is exactly what the first solve reported
# (0.104 m residual, peaking at touchdown, the most forward frame).
FORE = {"R": ["shoulder.R", "upperarm.R", "forearm.R", "fcannon.R", "fpaw.R"],
        "L": ["shoulder.L", "upperarm.L", "forearm.L", "fcannon.L", "fpaw.L"]}
FEET = ["fpaw.L", "fpaw.R", "hpaw.L", "hpaw.R"]

# clip table: (frames, period_s, speed_m_s, duty, touchdown phase per foot)
#
# The SPEEDS are derived from the measured reach, not chosen and then forced:
# a usable stance excursion of 0.52 m (inside the 0.60 m the chains can cover
# at 94 % extension) divided by the duty factor gives the stride, and the
# stride over the period gives v. Pick v first and the feet cannot keep up
# with the ground, which is the slide this whole construction exists to avoid.
CLIPS = {
    "walk": dict(n=12, T=0.80, v=0.93, duty=0.70, lift=0.075,
                 phase={"hpaw.L": 0.00, "fpaw.L": 0.25, "hpaw.R": 0.50, "fpaw.R": 0.75},
                 cycle=True),
    "run": dict(n=8, T=0.42, v=4.20, duty=0.27, lift=0.22,
                phase={"hpaw.L": 0.00, "hpaw.R": 0.14, "fpaw.R": 0.44, "fpaw.L": 0.58},
                cycle=True),
    "idle": dict(n=12, T=2.40, v=0.0, duty=1.0, lift=0.0,
                 phase={f: 0.0 for f in FEET}, cycle=True),
    "attack": dict(n=12, T=0.70, v=0.0, duty=1.0, lift=0.0,
                   phase={f: 0.0 for f in FEET}, cycle=False),
}


def set_world_rot(pb, rx, ry, rz):
    """Apply a rotation expressed in WORLD axes to a bone, in its own frame.

    Authored numbers have to mean one thing. They did not: a bone's local X
    comes out of its ROLL, and the roll rule (align to +Y when the bone is
    within 49 deg of vertical, else to +Z) lands local X on world +X for a
    DOWNWARD bone and on world -X for an UPWARD one. So the same -20 deg that
    drops a leg forward tipped the manticore's FACE UP -- the head bone points
    up-forward and silently inverted the sign. It is visible in the first
    attack render: the strike frames raise the muzzle instead of biting with
    it.

    Rather than carry a sign table, each authored triple is a rotation about
    the WORLD axes (x pitch, y roll, z yaw) conjugated into the bone's rest
    frame: L = B^-1 R B. Positive x therefore always turns the bone the same
    way in the world, whichever way the bone happens to point.
    """
    B = pb.bone.matrix_local.to_3x3()
    R = Euler((math.radians(rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix()
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = (B.inverted() @ R @ B).to_quaternion()


# ------------------------------------------------------------------ IK
def chain_plane(arm, chain):
    pb = [arm.pose.bones[b] for b in chain]
    n = (arm.matrix_world.to_3x3() @ pb[0].x_axis).normalized()
    O = arm.matrix_world @ pb[0].head
    ref = Vector((0, 1, 0))
    u = (ref - n * ref.dot(n))
    if u.length < 1e-6:
        ref = Vector((0, 0, 1)); u = ref - n * ref.dot(n)
    u.normalize()
    w = n.cross(u)
    return O, n, u, w


def to2(P, O, u, w):
    d = P - O
    return np.array([d.dot(u), d.dot(w)])


def solve_plane(arm, chain, pb, target_world, limits_deg, iters, damp, seed=None,
                ground_w=None):
    """Damped CCD inside the chain's current plane. Returns the per-bone local
    X rotation in radians and the in-plane residual."""
    O, n, u, w = chain_plane(arm, chain)
    sgn = [1.0 if (arm.matrix_world.to_3x3() @ b.x_axis).normalized().dot(n) > 0 else -1.0
           for b in pb]
    pts = [to2(arm.matrix_world @ b.head, O, u, w) for b in pb]
    pts.append(to2(arm.matrix_world @ pb[-1].tail, O, u, w))
    pts = np.array(pts)
    L = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    a_rest = np.array([math.atan2(d[1], d[0]) for d in np.diff(pts, axis=0)])
    rel_rest = np.concatenate([[a_rest[0]], np.diff(a_rest)])
    tgt = to2(target_world, O, u, w)
    ang = a_rest.copy()
    if seed is not None and len(seed) == len(ang):
        # START FROM LAST FRAME'S ANSWER. CCD has many folded solutions for a
        # 64 %-extended chain and no memory of its own, so consecutive frames
        # can land on different branches. Measured on the gallop: the toe
        # reached its target to within 16 mm while the ELBOW went through the
        # floor -- wrist at z = -0.021 with the toe hooked up at +0.084, a leg
        # that renders as broken. The residual could not see it, because a
        # residual only ever asks about the effector. Seeding each frame with
        # the previous frame's angles holds the sequence on one branch.
        ang = a_rest + np.asarray(seed, dtype=float)
    lim = np.radians(np.array(limits_deg, dtype=float))

    def fk(ang):
        p = [pts[0]]
        for l, aa in zip(L, ang):
            p.append(p[-1] + l * np.array([math.cos(aa), math.sin(aa)]))
        return np.array(p)

    def clamp_rel(i, ang):
        rel = ang[i] - (ang[i - 1] if i else 0.0)
        r0 = rel_rest[i]
        if abs(r0) > 1e-4:
            sg = math.copysign(1.0, r0)
            lo, hi = sg * max(abs(r0) * 0.12, abs(r0) - lim[i]), sg * (abs(r0) + lim[i])
            lo, hi = min(lo, hi), max(lo, hi)
        else:
            lo, hi = -lim[i], lim[i]
        c = min(max(rel, lo), hi)
        if c != rel:
            ang[i:] += (c - rel)

    for _ in range(iters):
        p = fk(ang)
        for i in range(len(ang) - 1, -1, -1):
            cur = p[-1] - p[i]; to = tgt - p[i]
            if np.linalg.norm(cur) < 1e-7 or np.linalg.norm(to) < 1e-7:
                continue
            d = math.atan2(to[1], to[0]) - math.atan2(cur[1], cur[0])
            d = (d + math.pi) % (2 * math.pi) - math.pi
            ang[i:] += damp * d
            clamp_rel(i, ang)
            p = fk(ang)
        if np.linalg.norm(p[-1] - tgt) < 2e-4:
            break
    p = fk(ang)
    d_abs = ang - a_rest
    local = np.concatenate([[d_abs[0]], np.diff(d_abs)])
    # how far the worst INTERMEDIATE joint sits below the ground line: the
    # constraint the leg was missing. Every joint sat on its limit and the
    # slack went into the forearm, driving the carpus to z = -0.045 and
    # hooking the paw back up to reach the toe -- with the toe on target to
    # 16 mm the whole time. A residual only ever asks about the effector, so
    # the depth is reported alongside it and the caller picks on BOTH.
    dig = 0.0
    if ground_w is not None:
        for j in range(1, len(p) - 1):
            dig = max(dig, float(ground_w - p[j][1]))
    return ([float(s * v) for s, v in zip(sgn, local)],
            float(np.linalg.norm(p[-1] - tgt)), n, list(d_abs), dig)


def paw_sole_z(obj, idx):
    """The lowest world z of the vertices this paw drives -- the SOLE."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    M = ev.matrix_world
    lo = 1e9
    for i in idx:
        lo = min(lo, (M @ me.vertices[i].co).z)
    ev.to_mesh_clear()
    return float(lo)


def solve_leg(arm, chain, target_world, limits_deg, iters=200, damp=0.62,
              outer=14, seed=None, ground_z=None):
    """Plane CCD plus ONE abduction degree of freedom at the chain's root.

    Why the extra axis exists, measured rather than guessed: with a purely
    planar solve the planted-foot residual sat at 0.093 m and would not move
    for any iteration count or damping -- because the error was not in the
    plane at all. The walk's spine carries a lateral yaw wave; four yawed
    joints move the scapula ~0.05 m sideways; and a chain whose every joint
    turns about its own X axis cannot change its end effector's lateral
    offset by any amount. The foot could not be where the ground was, in a
    direction the solver had no coordinate for.

    So the root bone (scapula / femur) also turns about its local Z, solved by
    a few secant steps against the measured lateral error. Anatomically this
    is the abduction a real shoulder and hip have; numerically it is the
    missing rank.
    """
    pb = [arm.pose.bones[b] for b in chain]
    for b in pb:
        b.rotation_mode = 'XYZ'
        b.rotation_euler = (0.0, 0.0, 0.0)
    beta = 0.0
    best = None
    for it in range(outer):
        for b in pb:
            b.rotation_euler = (0.0, 0.0, 0.0)
        pb[0].rotation_euler = (0.0, 0.0, beta)
        bpy.context.view_layer.update()
        gw = None
        if ground_z is not None:
            O0, n0, u0, w0 = chain_plane(arm, chain)
            gw = float((Vector((0, 0, ground_z)) - O0).dot(w0))
        # MULTI-START. CCD is greedy and has no memory, so from the rest seed
        # it folded the leg the wrong way and would not leave that branch for
        # any iteration count. Four starts are tried -- rest, the previous
        # frame, a shoulder-folded pose and an extended one -- and the winner
        # is scored on residual AND on how far it buries an intermediate
        # joint, because a solve that satisfies the toe by putting the wrist
        # underground is not a solution.
        cands = [None]
        if seed is not None and len(seed) == len(pb):
            cands.append(list(seed))
        nb = len(pb)
        fold = [0.0] * nb; ext = [0.0] * nb
        if nb >= 3:
            fold[-4 if nb >= 4 else 0] = math.radians(-26)
            fold[-3] = math.radians(22)
            ext[-4 if nb >= 4 else 0] = math.radians(18)
            ext[-3] = math.radians(-12)
        cands += [fold, ext]
        pick = None
        for cd in cands:
            lo_, r2_, n_, da_, dig_ = solve_plane(arm, chain, pb, target_world,
                                                  limits_deg, iters, damp,
                                                  seed=cd, ground_w=gw)
            sc_ = r2_ + 6.0 * max(0.0, dig_)
            if pick is None or sc_ < pick[0]:
                pick = (sc_, lo_, r2_, n_, da_, dig_)
        _, local, res2d, n, dabs, dig = pick
        pb[0].rotation_euler = (local[0], 0.0, beta)
        for i in range(1, len(pb)):
            pb[i].rotation_euler = (local[i], 0.0, 0.0)
        bpy.context.view_layer.update()
        got = arm.matrix_world @ pb[-1].tail
        err = got - target_world
        r = float(np.linalg.norm(err))
        score = r + 6.0 * max(0.0, dig)
        if best is None or score < best[0]:
            best = (score, beta, list(local), list(dabs), r, dig)
        lat = float(err.dot(n))
        arm_len = max((got - (arm.matrix_world @ pb[0].head)).length, 1e-3)
        if abs(lat) < 5e-5:
            break
        # SIGN, derived rather than guessed and then checked against the
        # measurement: a positive turn about the root bone's local Z carries
        # its tail toward -X_local, i.e. toward -n, so a positive lateral
        # error (+n) is cancelled by a POSITIVE beta. Written with a minus
        # first, every correction made the residual worse, `best` kept the
        # beta=0 solve, and the recorded abduction came back 0.000 on every
        # frame -- a correction loop that ran, converged, and did nothing,
        # while reporting the untouched planar residual as if it were final.
        beta += lat / arm_len
    _, beta, local, dabs, r, dig = best
    for b in pb:
        b.rotation_euler = (0.0, 0.0, 0.0)
    pb[0].rotation_euler = (local[0], 0.0, beta)
    for i in range(1, len(pb)):
        pb[i].rotation_euler = (local[i], 0.0, 0.0)
    bpy.context.view_layer.update()
    return local, beta, r, dabs, dig


# ------------------------------------------------------------------ gait
def foot_target(cfg, foot, t, rest_toe, v, centre_y):
    """World-space toe target at cycle fraction t, in the IN-PLACE clip.

    The stance sweep is centred under the LEG'S ROOT JOINT, not on the rest
    toe. Meshy delivered the animal in a stretched show stance -- the front
    toes sit 0.22 m forward of the scapula -- so centring on the rest toe
    spent the whole excursion budget on the one side the chain cannot reach.
    """
    T_, duty, lift = cfg["T"], cfg["duty"], cfg["lift"]
    stance = v * T_ * duty
    y_td = centre_y + stance / 2.0
    ph = (t - cfg["phase"][foot]) % 1.0
    z0 = rest_toe[2] + GROUND_CLEARANCE
    if duty >= 0.999:
        return Vector((rest_toe[0], rest_toe[1], z0)), True
    if ph < duty:
        f = ph / duty
        return Vector((rest_toe[0], y_td - stance * f, z0)), True
    s = (ph - duty) / (1.0 - duty)
    # SWING: fold first, reach later. A symmetric arc -- forward and up
    # together -- asks the leg to be simultaneously extended and raised, and
    # on the gallop that put the fore chain at 64 % extension with a target
    # 0.30 m forward and 0.12 m up: the solver satisfied the toe and sent the
    # wrist through the floor. A real gallop's swing tucks the paw up UNDER
    # the body while the leg is still back, then unfolds forward as it drops.
    # So the lift peaks early (s ** 0.7 inside the sine) and the forward
    # travel is biased late (s ** 1.6).
    e = s ** 1.6
    y = (y_td - stance) + stance * e
    z = z0 + lift * math.sin(math.pi * s ** 0.7)
    return Vector((rest_toe[0], y, z)), False


def body_pose(arm, clip, cfg, t):
    """Everything that is not a leg: root height, pelvis, spine, neck, head,
    tail. Returned as a dict of bone -> (rx, ry, rz) degrees, plus a root
    offset in metres."""
    P = {}
    off = Vector((0, 0, 0))
    tau = 2 * math.pi * t
    if clip == "walk":
        off.z = 0.012 * math.sin(2 * tau + 0.6)
        P["hips"] = (1.2 * math.sin(2 * tau), 3.0 * math.sin(tau), 2.0 * math.sin(tau + 1.2))
        P["spine_01"] = (0.8 * math.sin(2 * tau + 0.5), 0, -1.6 * math.sin(tau + 0.4))
        P["spine_02"] = (0.6 * math.sin(2 * tau + 1.0), 0, -1.8 * math.sin(tau + 0.9))
        P["spine_03"] = (0.5 * math.sin(2 * tau + 1.5), 0, -1.6 * math.sin(tau + 1.4))
        P["chest"] = (-0.6 * math.sin(2 * tau + 1.8), 0, -1.0 * math.sin(tau + 1.8))
        P["neck_01"] = (1.6 * math.sin(2 * tau + 2.4), 0, 2.0 * math.sin(tau + 2.2))
        P["neck_02"] = (1.2 * math.sin(2 * tau + 2.8), 0, 1.6 * math.sin(tau + 2.6))
        P["head"] = (-2.2 * math.sin(2 * tau + 2.9), 0, 2.2 * math.sin(tau + 3.0))
        for i in range(7):
            P["tail_%02d" % (i + 1)] = (1.5 * math.sin(tau + 0.9 * i) * (0.4 + 0.12 * i),
                                        0, 5.0 * math.sin(tau - 0.55 * i) * (0.35 + 0.11 * i))
    elif clip == "run":
        # The back is the engine, and its PHASE is set by the footfalls, not
        # chosen. Stance windows at duty 0.25: hind L 0.00-0.25, hind R
        # 0.14-0.39, fore R 0.44-0.69, fore L 0.58-0.83. A galloping quadruped
        # is FLEXED (back rounded, hindquarters gathered) under the hind pair
        # and EXTENDED (stretched, hollow) under the fore pair, so flexion
        # peaks at t = 0.07 and extension at t = 0.57.
        #
        # Written first as -8*sin(tau+0.35), which peaked flexion at t = 0.57
        # -- under the FORE feet. Five spine joints then lifted the scapula
        # about 24 deg through 0.62 m of back, i.e. a quarter of a metre, at
        # exactly the frames the front foot had to be on the ground: the
        # solver reported 0.166 m of front-foot residual and the animal
        # galloped with its forehand in the air.
        # AMPLITUDE is bounded by the front legs, not by taste. Five joints
        # at 5/6/7/6/-3 deg sum to 21 deg at the chest, and 21 deg through the
        # 0.62 m from sacrum to chest moves the SCAPULA 0.22 m vertically. At
        # the gallop's fore stance that dropped the shoulder to z = 0.70 with
        # the toe 0.17 m in front of it: the chain had to fold to 70 % of its
        # length, every joint hit its limit, and the slack went into the
        # forearm and put the carpus 0.09 m underground. Halved, the chest
        # moves ~0.12 m and the fore chain stays inside its working range.
        fl = math.cos(2 * math.pi * (t - 0.07))
        off.z = 0.030 * math.cos(2 * math.pi * (t - 0.88)) + 0.010
        P["hips"] = (3.0 * fl, 0, 0)
        P["spine_01"] = (3.5 * math.cos(2 * math.pi * (t - 0.09)), 0, 0)
        P["spine_02"] = (4.0 * math.cos(2 * math.pi * (t - 0.11)), 0, 0)
        P["spine_03"] = (3.5 * math.cos(2 * math.pi * (t - 0.13)), 0, 0)
        P["chest"] = (-2.0 * math.cos(2 * math.pi * (t - 0.15)), 0, 0)
        # head held LOW and level: a creepy fast hound, not a rearing horse
        P["neck_01"] = (-6.0 + 4.0 * math.cos(2 * math.pi * (t - 0.20)), 0, 0)
        P["neck_02"] = (-5.0 + 4.0 * math.cos(2 * math.pi * (t - 0.24)), 0, 0)
        P["head"] = (-5.0 - 5.0 * math.cos(2 * math.pi * (t - 0.28)), 0, 0)
        for i in range(7):
            P["tail_%02d" % (i + 1)] = (-7.0 + 3.0 * math.cos(2 * math.pi * (t - 0.1) - 0.5 * i),
                                        0,
                                        2.0 * math.sin(tau - 0.7 * i) * (0.3 + 0.1 * i))
    elif clip == "idle":
        br = math.sin(tau)                       # one breath per cycle
        off.z = 0.007 * br
        P["hips"] = (0.5 * br, 0, 0)
        P["spine_01"] = (-0.7 * br, 0, 0)
        P["spine_02"] = (-1.1 * br, 0, 0)
        P["spine_03"] = (-1.3 * br, 0, 0)
        P["chest"] = (1.0 * br, 0, 0)
        look = math.sin(tau - 0.4)               # a slow head turn, returning
        P["neck_01"] = (0.8 * br, 0, 7.0 * look)
        P["neck_02"] = (0.6 * br, 1.5 * look, 9.0 * look)
        P["head"] = (-1.6 * br + 2.0 * math.sin(tau * 2 + 1.0), 3.0 * look, 11.0 * look)
        for i in range(7):
            P["tail_%02d" % (i + 1)] = (1.0 * math.sin(tau - 0.6 * i) * (0.3 + 0.12 * i), 0,
                                        7.5 * math.sin(tau - 0.72 * i) * (0.25 + 0.13 * i))
    elif clip == "attack":
        # 0-0.25 anticipation (coil back and down), 0.25-0.58 strike,
        # 0.58-1.0 recovery. A single shaped curve drives the whole body so
        # the parts cannot drift out of phase with each other.
        def curve(t):
            if t < 0.25:
                s = t / 0.25
                return -(0.5 - 0.5 * math.cos(math.pi * s))          # -1 coil
            if t < 0.58:
                s = (t - 0.25) / 0.33
                return -1.0 + 2.0 * (s ** 0.65)                      # -1 -> +1 strike
            s = (t - 0.58) / 0.42
            return 1.0 - 1.0 * (0.5 - 0.5 * math.cos(math.pi * s))   # +1 -> 0
        c = curve(t)
        off.z = -0.058 * max(0.0, -c) + 0.030 * max(0.0, c)
        off.y = -0.045 * max(0.0, -c) + 0.160 * max(0.0, c)
        # The COIL drops the forehand; it does not raise it. Written with the
        # spine flexing the other way, the five joints summed to +22 deg at
        # the chest and lifted the shoulders 0.25 m at the deepest crouch --
        # front-foot residual 0.063 m, and a crouch that looked like a rear.
        P["hips"] = (-3.0 * max(0.0, -c) + 2.0 * max(0.0, c), 0, 0)
        P["spine_01"] = (-2.5 * max(0.0, -c) + 3.0 * max(0.0, c), 0, 0)
        P["spine_02"] = (-2.5 * max(0.0, -c) + 3.0 * max(0.0, c), 0, 0)
        P["spine_03"] = (-2.0 * max(0.0, -c) + 2.0 * max(0.0, c), 0, 0)
        P["chest"] = (2.0 * max(0.0, -c) - 2.0 * max(0.0, c), 0, 0)
        P["neck_01"] = (10.0 * max(0.0, -c) - 12.0 * max(0.0, c), 0, 0)
        P["neck_02"] = (9.0 * max(0.0, -c) - 14.0 * max(0.0, c), 0, 0)
        P["head"] = (5.0 * max(0.0, -c) - 20.0 * max(0.0, c), 0, 0)
        for i in range(7):
            P["tail_%02d" % (i + 1)] = (-6.0 * c * (0.3 + 0.12 * i), 0,
                                        3.0 * math.sin(2 * math.pi * t - 0.5 * i)
                                        * (0.2 + 0.1 * i))
    return P, off


def attack_foot(cfg, foot, t, rest_toe):
    """The attack's feet: the hind pair stay planted, the fore pair lift and
    reach during the strike and return."""
    def curve(t):
        if t < 0.25:
            s = t / 0.25
            return -(0.5 - 0.5 * math.cos(math.pi * s))
        if t < 0.58:
            s = (t - 0.25) / 0.33
            return -1.0 + 2.0 * (s ** 0.65)
        s = (t - 0.58) / 0.42
        return 1.0 - (0.5 - 0.5 * math.cos(math.pi * s))
    c = curve(t)
    if foot.startswith("hpaw"):
        return Vector((rest_toe[0], rest_toe[1], rest_toe[2] + GROUND_CLEARANCE)), True
    lift = 0.0
    if 0.20 < t < 0.75:
        s = (t - 0.20) / 0.55
        lift = 0.20 * math.sin(math.pi * s) ** 0.8
    side = 1.0 if foot.endswith("R") else 0.82
    # The fore toes DO NOT move during the coil. Pulling them back 0.07 m
    # while they were still on the ground was a 35 mm/frame scrub -- the plant
    # instrument measured the fore pair travelling backward at 0.37-0.45 m/s
    # on a clip whose authored ground speed is zero. A coiling hound shifts
    # its weight back over planted feet; it does not drag them.
    y = rest_toe[1] + (0.17 * max(0.0, c)) * side
    return Vector((rest_toe[0], y, rest_toe[2] + GROUND_CLEARANCE + lift)), lift < 0.01


def main():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    bpy.context.view_layer.objects.active = arm
    for b in arm.pose.bones:
        b.rotation_mode = 'XYZ'

    obj = next(o for o in sc.objects if o.type == 'MESH'
               and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers))
    paw_verts = {}
    for f in FEET:
        cann = ("hcannon." if f.startswith("hpaw") else "fcannon.") + f[-1]
        want = {obj.vertex_groups[n].index for n in (f, cann)
                if obj.vertex_groups.get(n)}
        idx = []
        for v in obj.data.vertices:
            for gg in v.groups:
                if gg.group in want and gg.weight > 0.30:
                    idx.append(v.index); break
        paw_verts[f] = idx
    rest_toe = {f: (arm.matrix_world @ arm.pose.bones[f].tail).copy() for f in FEET}
    # the stance sweep's centre: under the leg's ROOT joint (scapula top for
    # the fore, hip for the hind), biased a little forward
    centre_y = {}
    for f in FEET:
        chain = (HIND if f.startswith("hpaw") else FORE)[f[-1]]
        root = arm.matrix_world @ arm.pose.bones[chain[0]].head
        centre_y[f] = root.y + (0.06 if f.startswith("fpaw") else -0.02)
    # The PAW limit is 6 deg, not 16. The paw bone's tail is the IK effector
    # but the sole hangs ~10 mm below it, so every degree of paw pitch levers
    # the pads through the floor. At 16 deg the measured sole reached 18 mm
    # under ground on the walk and 44 mm at the attack's deepest crouch.
    # Two other fixes were tried and measured first: holding the paw at its
    # rest world orientation cured the sole and cost the 0.11 m of reach the
    # paw was contributing, taking planted residual from 3 mm to 57 mm; and
    # raising the toe TARGET until the sole measured zero fought its own
    # solve, driving the target 121 mm up while the sole barely moved. The
    # limit is the cause, so the limit is what changes.
    # CANNON limits are 26/30 deg, not 50. At 50 the solver could satisfy the
    # toe target by folding the pastern back under the leg -- the toe landed
    # on the ground (residual 16 mm) while the cannon's own mesh hung 137 mm
    # BELOW it. Rendered, that is a broken wrist: run frames 4 and 5 showed
    # the fore paw dangling a hand's breadth through the floor with the claws
    # hooked forward. The IK residual could not see it, because the residual
    # only ever asks about the effector.
    LIMITS = dict(hind=[42, 48, 30, 6], fore=[15, 42, 44, 26, 6])
    report = {}

    for clip, cfg in CLIPS.items():
        act = bpy.data.actions.new("mc_" + clip)
        arm.animation_data_create()
        arm.animation_data.action = act
        n, v = cfg["n"], cfg["v"]
        rows = []
        seeds = {f: None for f in FEET}
        # TWO PASSES. The first builds the seeds; the second re-solves with
        # the previous frame's answer already in hand, so on a cycle frame 0
        # is seeded from frame n-1 instead of from rest.
        for _pass in range(2):
          rows = []
          for i in range(n):
              t = i / n
              for b in arm.pose.bones:
                  b.rotation_euler = (0, 0, 0)
                  b.rotation_quaternion = (1, 0, 0, 0)
                  b.location = (0, 0, 0)
              P, off = body_pose(arm, clip, cfg, t)
              root = arm.pose.bones["root"]
              root.location = off
              for name, r in P.items():
                  pb = arm.pose.bones.get(name)
                  if pb:
                      set_world_rot(pb, r[0], r[1], r[2])
              bpy.context.view_layer.update()
              frow = {}
              for foot in FEET:
                  chain = (HIND if foot.startswith("hpaw") else FORE)[foot[-1]]
                  lim = LIMITS["hind"] if foot.startswith("hpaw") else LIMITS["fore"]
                  if clip == "attack":
                      tgt, planted = attack_foot(cfg, foot, t, rest_toe[foot])
                  else:
                      tgt, planted = foot_target(cfg, foot, t, rest_toe[foot], v,
                                                 centre_y[foot])
                  loc, beta, res, dabs, dig = solve_leg(
                      arm, chain, tgt, lim, seed=seeds[foot],
                      ground_z=GROUND_CLEARANCE + 0.010)
                  seeds[foot] = dabs
                  sole_dz = paw_sole_z(obj, paw_verts[foot]) if planted else None
                  got = arm.matrix_world @ arm.pose.bones[foot].tail
                  frow[foot] = dict(target=[round(x, 5) for x in tgt],
                                    got=[round(x, 5) for x in got],
                                    residual_m=round(float((got - tgt).length), 5),
                                    abduction_deg=round(math.degrees(beta), 3),
                                    joint_below_ground_m=round(dig, 5),
                                    sole_z_m=(round(sole_dz, 5) if sole_dz is not None
                                              else None),
                                    planted=bool(planted))
              for b in arm.pose.bones:
                  b.keyframe_insert("rotation_quaternion" if b.rotation_mode == 'QUATERNION'
                                    else "rotation_euler", frame=i + 1)
                  b.keyframe_insert("location", frame=i + 1)
              rows.append(frow)
        # (No interpolation pass. Blender 5 moved f-curves behind slotted
        # actions, and it would buy nothing here: every bone is keyed on every
        # frame and the renderer samples integer frames only, so nothing is
        # ever read between keys.)
        report[clip] = dict(frames=n, period_s=cfg["T"], fps=round(n / cfg["T"], 4),
                            speed_m_s=v, stride_m=round(v * cfg["T"], 4),
                            duty=cfg["duty"], phase=cfg["phase"], cycle=cfg["cycle"],
                            stance_excursion_m=round(v * cfg["T"] * cfg["duty"], 4),
                            stance_centre_y={k: round(x, 4) for k, x in centre_y.items()},
                            ik=rows,
                            max_residual_m=round(max(r[f]["residual_m"]
                                                     for r in rows for f in FEET), 5))
        arm.animation_data.action = None
        act.use_fake_user = True
        print("%-7s %2d frames  %.3f s  v=%.2f m/s  stride %.3f m  max IK residual %.4f m"
              % (clip, n, cfg["T"], v, v * cfg["T"], report[clip]["max_residual_m"]))

    soles = [r[f]["sole_z_m"] for c in report.values() for r in c["ik"] for f in r
             if r[f].get("sole_z_m") is not None]
    soles.sort()
    ref = soles[len(soles) // 2]
    for c in report.values():
        ss = [r[f]["sole_z_m"] for r in c["ik"] for f in r
              if r[f].get("sole_z_m") is not None]
        c["sole_z_range_m"] = [round(min(ss), 5), round(max(ss), 5)] if ss else None
    report["ground_ref_z"] = round(float(ref), 5)
    report["ground_ref_note"] = ("median measured sole z over every planted foot of "
                                 "every clip; the renderer puts row 398 here, not on "
                                 "the nominal z=0")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUTDIR, "clips.blend"))
    json.dump(report, open(os.path.join(OUTDIR, "clips.json"), "w"), indent=1)
    print("ground_ref_z = %.5f m  (sole band over all clips %.4f .. %.4f)"
          % (ref, soles[0], soles[-1]))
    print("wrote", os.path.join(OUTDIR, "clips.json"))


main()
