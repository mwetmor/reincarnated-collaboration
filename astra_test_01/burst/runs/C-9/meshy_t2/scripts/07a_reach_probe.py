# C-9 meshy_t2 step 5a: measure the USABLE stance excursion, with the joint
# limits in force.
#
#   blender -b -noaudio --python scripts/07a_reach_probe.py -- <rigged.blend> <out.json>
#
# Chain length said the walk stride fitted and the solve still reported 0.094 m
# of residual on planted frames. Chain length is the wrong instrument: it
# answers "could a straight line reach it", and the paw joint's 16 deg limit
# means the chain is never straight -- the toe keeps its angle to the cannon by
# design, because a hound's toe does. So the reach is measured with the solver
# that will actually be used, limits and all, by sweeping the toe target along
# the ground and recording where the residual leaves 5 mm.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("07a_reach_probe.py")][0]))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("c7", os.path.join(HERE, "07_clips.py"))
# 07_clips.py runs main() at import, so the solver is copied in rather than
# imported. Keeping ONE copy would be better; this file exists to be deleted
# once the excursion is fixed, so the duplication is deliberate and scoped.
a = sys.argv[sys.argv.index('--') + 1:]
BLEND, OUTP = a[0], a[1]

HIND = {"R": ["thigh.R", "shin.R", "hcannon.R", "hpaw.R"],
        "L": ["thigh.L", "shin.L", "hcannon.L", "hpaw.L"]}
FORE = {"R": ["shoulder.R", "upperarm.R", "forearm.R", "fcannon.R", "fpaw.R"],
        "L": ["shoulder.L", "upperarm.L", "forearm.L", "fcannon.L", "fpaw.L"]}
LIMITS = dict(hind=[42, 48, 48, 16], fore=[15, 42, 44, 48, 16])

bpy.ops.wm.open_mainfile(filepath=BLEND)
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
for b in arm.pose.bones:
    b.rotation_mode = 'XYZ'
sys.path.insert(0, HERE)


def chain_plane(arm, chain):
    pb = [arm.pose.bones[b] for b in chain]
    n = (arm.matrix_world.to_3x3() @ pb[0].x_axis).normalized()
    O = arm.matrix_world @ pb[0].head
    ref = Vector((0, 1, 0))
    u = (ref - n * ref.dot(n))
    if u.length < 1e-6:
        ref = Vector((0, 0, 1)); u = ref - n * ref.dot(n)
    u.normalize()
    return O, n, u, n.cross(u)


def to2(P, O, u, w):
    d = P - O
    return np.array([d.dot(u), d.dot(w)])


def solve_leg(arm, chain, target_world, limits_deg, iters=140, damp=0.6, floor=0.12):
    pb = [arm.pose.bones[b] for b in chain]
    for b in pb:
        b.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()
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
    lim = np.radians(np.array(limits_deg, dtype=float))

    def fk(ang):
        p = [pts[0]]
        for l, aa in zip(L, ang):
            p.append(p[-1] + l * np.array([math.cos(aa), math.sin(aa)]))
        return np.array(p)

    for _ in range(iters):
        p = fk(ang)
        for i in range(len(ang) - 1, -1, -1):
            cur = p[-1] - p[i]; to = tgt - p[i]
            if np.linalg.norm(cur) < 1e-7 or np.linalg.norm(to) < 1e-7:
                continue
            d = math.atan2(to[1], to[0]) - math.atan2(cur[1], cur[0])
            d = (d + math.pi) % (2 * math.pi) - math.pi
            ang[i:] += damp * d
            rel = ang[i] - (ang[i - 1] if i else 0.0)
            r0 = rel_rest[i]
            if abs(r0) > 1e-4:
                s = math.copysign(1.0, r0)
                lo, hi = s * max(abs(r0) * floor, abs(r0) - lim[i]), s * (abs(r0) + lim[i])
                lo, hi = min(lo, hi), max(lo, hi)
            else:
                lo, hi = -lim[i], lim[i]
            rel_c = min(max(rel, lo), hi)
            if rel_c != rel:
                ang[i:] += (rel_c - rel)
            p = fk(ang)
        if np.linalg.norm(p[-1] - tgt) < 2e-4:
            break
    p = fk(ang)
    d_abs = ang - a_rest
    local = np.concatenate([[d_abs[0]], np.diff(d_abs)])
    return [float(s * v) for s, v in zip(sgn, local)], float(np.linalg.norm(p[-1] - tgt))


out = {}
for foot in ("fpaw.R", "hpaw.R"):
    chain = (HIND if foot.startswith("hpaw") else FORE)[foot[-1]]
    lim = LIMITS["hind"] if foot.startswith("hpaw") else LIMITS["fore"]
    rest = (arm.matrix_world @ arm.pose.bones[foot].tail).copy()
    root = arm.matrix_world @ arm.pose.bones[chain[0]].head
    rows = []
    for dy in np.arange(-0.60, 0.61, 0.02):
        tgt = Vector((rest.x, root.y + float(dy), rest.z))
        loc, res = solve_leg(arm, chain, tgt, lim)
        rows.append([round(float(dy), 3), round(res, 5)])
    for b in chain:
        arm.pose.bones[b].rotation_euler = (0, 0, 0)
    ok = [r[0] for r in rows if r[1] < 0.005]
    out[foot] = dict(root_y=round(root.y, 4), rest_toe_y=round(rest.y, 4),
                     toe_z=round(rest.z, 4), sweep=rows,
                     ok_dy=[round(min(ok), 3), round(max(ok), 3)] if ok else None,
                     usable_excursion_m=round(max(ok) - min(ok), 4) if ok else 0.0)
    print("%s: root y %.3f  residual<5mm for dy in [%.3f, %.3f] -> usable excursion %.3f m"
          % (foot, root.y, min(ok), max(ok), max(ok) - min(ok)))

json.dump(out, open(OUTP, "w"), indent=1)
print("wrote", OUTP)
