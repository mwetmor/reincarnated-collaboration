# D2 fix 1: does the shield clear the torso, in every clip?
#
#   blender -b -noaudio --python scripts/16_shield_clear.py -- <base.glb>
#     <out.json> [--out 0.09] [--fwd 0.0] [--up -0.13] [--tilt 0.25]
#     [--radius 0.25] [--length 0.87] [--still run:12:path.png]
#
# THE CAPSULE TURNS WITH HIM. The torso is a segment from the hips to the top
# of the spine with a radius, and both ends are read from the POSED bones every
# frame, so it yaws and pitches with the body. A world-axis box does not: this
# character is yawed 47 degrees and more through these clips, and an AABB lets
# the torso rattle around inside it -- which is how a shield can look clear and
# be through his ribs.
#
# The offset is expressed in the FOREARM's own rest frame (outward / forward /
# up), not in world axes, because that is the frame the bind actually lives in
# once the arm starts moving.
#
# TWO MEASURES, and the second is the one that decides. A cylinder about the
# spine counts everything within 0.25 m of that line -- INCLUDING the space
# directly in front of his chest, which is exactly where a shield belongs. It
# cannot tell "covering his chest" from "through his ribs", and it reported
# hundreds of vertices inside on frames where the shield is plainly in front of
# him. The capsule is kept because it is what the scene measured and the
# numbers must be comparable; the verdict is taken from the POSED BODY MESH,
# where a vertex inside the surface is a real intersection and nothing else is.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("16_shield_clear.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BASE, OUTJ = a[0], a[1]
OUTW = float(a[a.index("--out") + 1]) if "--out" in a else 0.09
FWD = float(a[a.index("--fwd") + 1]) if "--fwd" in a else 0.0
UP = float(a[a.index("--up") + 1]) if "--up" in a else -0.13
TILT = float(a[a.index("--tilt") + 1]) if "--tilt" in a else 0.25
RAD = float(a[a.index("--radius") + 1]) if "--radius" in a else 0.25
LEN = float(a[a.index("--length") + 1]) if "--length" in a else 0.87
BONE = a[a.index("--bone") + 1] if "--bone" in a else "LeftForeArm"
STILL = a[a.index("--still") + 1] if "--still" in a else None
ROOT = os.path.dirname(HERE)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
# REST POSE BEFORE FITTING. socket_weapon2 and bone_bind read the bone's
# POSED head, and a glTF import leaves the armature on whatever action it
# picked -- so a piece could be bound against frame 1 of some clip instead of
# the rest pose. Two baselines of the same shield disagreed (idle 3 against
# 117) and that disagreement is the only reason it was found.
arm.animation_data.action = None
for _pb in arm.pose.bones:
    _pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0])
BH = float(BV[:, 2].max() - BV[:, 2].min())
PSCALE = BH / 1.70

# the forearm's rest frame: outward (away from the midline), forward, up
pb = arm.pose.bones[BONE]
bh = np.array(arm.matrix_world @ pb.head)
mid = float(np.median(BV[:, 0]))
outward = np.array([1.0 if bh[0] > mid else -1.0, 0.0, 0.0])
fwd_v = np.array([0.0, -1.0, 0.0])
up_v = np.array([0.0, 0.0, 1.0])
off = outward * OUTW + fwd_v * FWD + up_v * UP

before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "builds", "shield.glb"), before)
G.decimate(pc, 9000)
info = G.socket_weapon2(pc, arm, BONE, LEN, 0.50,
                        axis_world=tuple(outward + np.array([0, TILT, 0])),
                        face_world=(0, -1, 0), offset_world=tuple(off),
                        anchor="normal")
G.align_space(pc, body[0])
bpy.context.view_layer.update()
print("shield: %d tris, offset outward %.3f fwd %.3f up %.3f, tilt %.2f, "
      "length %.2f" % (len(pc.data.polygons), OUTW, FWD, UP, TILT, LEN))

acts = {x.name: x for x in bpy.data.actions}
rep = {}
for nm in ("idle", "walk", "run", "attack"):
    if nm not in acts:
        continue
    arm.animation_data.action = acts[nm]
    f0, f1 = (int(v) for v in acts[nm].frame_range)
    worst = (-1, 0, 0.0, 0, 0.0)
    cap_worst = [0, 0.0]
    per = []
    for i in range(f1 - f0):
        sc.frame_set(f0 + i)
        dg = bpy.context.evaluated_depsgraph_get()
        # the capsule, from the POSED bones
        A = np.array(arm.matrix_world @ arm.pose.bones["Hips"].head)
        B = np.array(arm.matrix_world @ arm.pose.bones["Spine02"].tail)
        ab = B - A
        L2 = float(ab @ ab) or 1e-9
        eo = pc.evaluated_get(dg); me = eo.to_mesh()
        cv = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", cv)
        V = (cv.reshape(-1, 3) @ np.array(eo.matrix_world.to_3x3()).T
             + np.array(eo.matrix_world.translation))
        eo.to_mesh_clear()
        t = np.clip(((V - A) @ ab) / L2, 0, 1)[:, None]
        d = np.linalg.norm(V - (A + t * ab), axis=1)
        inside = d < RAD
        n = int(inside.sum())
        deep = float(RAD - d.min()) if n else 0.0
        # the mesh test: is the vertex actually inside the posed body surface?
        eb = body[0].evaluated_get(dg)
        bt = BVHTree.FromObject(eb, dg)
        binv = eb.matrix_world.inverted()
        nm_in, nm_deep = 0, 0.0
        # INSIDE BY CROSSING PARITY, which needs no distance at all.
        #
        # Two nearest-surface versions failed first, in opposite directions.
        # Unbounded, find_nearest returns the closest surface however far away
        # and the sign of its normal there is meaningless: 970 vertices
        # "inside" at a depth of 0.001 m. Bounded to 0.12 m to kill that noise,
        # it reported ZERO everywhere -- because a shield vertex buried at the
        # spine is further than 0.12 m from any surface, so the bound excluded
        # precisely the deepest penetrations, which ARE the defect. A test that
        # cannot see the worst case is worse than no test.
        #
        # Parity has neither failure: march a ray and count how many times it
        # crosses the surface. Odd is inside, however deep.
        upd = Vector((0.0, 0.0, 1.0))
        for q in V[::4]:
            o = binv @ Vector(q.tolist())
            n_hit, guard = 0, 0
            while guard < 24:
                guard += 1
                h = bt.ray_cast(o, upd, 10.0)
                if h[0] is None:
                    break
                n_hit += 1
                o = h[0] + upd * 1e-4
            if n_hit % 2 == 1:
                nm_in += 1
                hn = bt.find_nearest(binv @ Vector(q.tolist()))
                if hn[0] is not None:
                    nm_deep = max(nm_deep, float(
                        (eb.matrix_world @ hn[0] - Vector(q.tolist())).length))
        per.append((n, nm_in))
        if nm_in > worst[1] or (worst[0] < 0 and n > worst[3]):
            worst = (i, nm_in, nm_deep, n, deep)
        cap_worst[0] = max(cap_worst[0], n)
        cap_worst[1] = max(cap_worst[1], deep)
    rep[nm] = dict(frames=f1 - f0, verts=len(V), sampled=len(V[::4]),
                   worst_frame=worst[0], mesh_inside=worst[1],
                   mesh_depth_m=round(worst[2], 4),
                   capsule_inside=worst[3], capsule_depth_m=round(worst[4], 4),
                   capsule_worst_any_frame=cap_worst[0],
                   capsule_worst_depth_m=round(cap_worst[1], 4))
    print("   %-7s worst frame %3d: MESH %4d of %d sampled inside the body "
          "(deepest %.3f m) | capsule %5d, %.3f m"
          % (nm, worst[0], worst[1], len(V[::4]), worst[2], cap_worst[0],
             cap_worst[1]))
json.dump(dict(offset=dict(outward=OUTW, forward=FWD, up=UP, tilt=TILT),
               radius=RAD, length=LEN, socket=info, clips=rep),
          open(OUTJ, "w"), indent=1)
