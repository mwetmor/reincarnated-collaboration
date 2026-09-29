# Re-place the shield as a CENTRE-GRIP Viking round shield: the boss over the
# fist, the face outward -- and measure what that costs in torso clearance,
# because that is the trade the original placement was silently making.
#
#   blender -b -noaudio --python scripts/29_shield_centregrip.py -- <body.glb>
#        <shield.glb> [--json f] [--out <shield.glb>]
#
# HOW THE ORIGINAL WENT WRONG, recorded because I shipped it. The D2 socket
# sweep optimised ONE objective -- shield vertices inside the torso -- and found
# a placement that scored well by holding the disc out at arm's length with its
# RIM near his hand. Nothing in the sweep asked whether his hand was on the
# grip, so nothing stopped it. Then in R-C9-71 I measured "grip bar to left fist
# min 0.0013 m" and reported the grip as closed. That number was TRUE. It was
# the distance to the nearest shield surface, and the nearest surface was the
# RIM. A nearest-surface distance cannot tell you WHICH surface, and I did not
# ask. The fist is 109.4% of the radius from the centre: entirely off the disc.
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("29_shield_centregrip.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, SHIELD = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ROOT = os.path.dirname(HERE)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
BD = body[0]
kb = BD.data.shape_keys.key_blocks if BD.data.shape_keys else {}
if "grip_L" in kb:
    kb["grip_L"].value = 1.0

# bring in the shield and re-bind it to THIS armature, so posing the body moves
# the shield. Its vertex groups already name these bones.
before = set(sc.objects)
bpy.ops.import_scene.gltf(filepath=SHIELD)
add = [o for o in sc.objects if o not in before]
SH = next(o for o in add if o.type == 'MESH' and o.vertex_groups)
for o in [o for o in add if o.type == 'MESH' and o is not SH]:
    bpy.data.objects.remove(o, do_unlink=True)
# DO NOT UNPARENT. The first attempt set SH.parent = None and added an
# armature modifier pointing at the body's rig. That strips the 0.01 object
# scale Meshy ships on the armature, so the mesh reverted to its raw 100x
# vertex data: the shield measured radius 38.6279 m and the fist 265.6% of the
# radius away. Both numbers are internally consistent and completely wrong --
# the same failure gearlib's own header documents for skinned glTF round trips,
# hit again by a different route. Keep the hierarchy; pose BOTH armatures.
SH_ARM = next(o for o in add if o.type == 'ARMATURE')
print("shield kept on its own rig: %d verts" % len(SH.data.vertices))

CP = os.path.join(ROOT, "work", "carry_pose.json")
carry = json.load(open(CP)) if os.path.exists(CP) else {}


def pose(which):
    """Both rigs, identically. They are the same 24 bones, so the shield tracks
    the body only if both are driven."""
    for A in (arm, SH_ARM):
        if A.animation_data:
            A.animation_data.action = None
        for pb in A.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
        if which == "carry":
            for bn, flat in carry.items():
                if bn in A.pose.bones:
                    A.pose.bones[bn].matrix_basis = Matrix(
                        [flat[i * 4:(i + 1) * 4] for i in range(4)])
    bpy.context.view_layer.update()


def fist_centre():
    gi = {vg.index: vg.name for vg in BD.vertex_groups}
    idx = [v.index for v in BD.data.vertices if v.groups and
           gi.get(max(v.groups, key=lambda x: x.weight).group) == "LeftHand"
           and max(v.groups, key=lambda x: x.weight).weight >= 0.30]
    return G.world_verts(BD)[idx].mean(axis=0), len(idx)


def disc_frame():
    V = G.world_verts(SH)
    c = V.mean(axis=0)
    ev, evec = np.linalg.eigh(np.cov((V - c).T))
    n = evec[:, 0] / np.linalg.norm(evec[:, 0])
    ip = evec[:, 1:]
    return c, n, ip, float(np.linalg.norm((V - c) @ ip, axis=1).max()), \
        float(np.ptp((V - c) @ n)), V


def inside_count(step=4):
    """Shield vertices inside the body, by crossing parity: march up and count
    surface crossings; odd is inside, however deep. A nearest-surface distance
    cannot do this -- it was tried in D2 and both an unbounded and a bounded
    version gave answers that were wrong in opposite directions."""
    dg = bpy.context.evaluated_depsgraph_get()
    eb = BD.evaluated_get(dg)
    bt = BVHTree.FromObject(BD, dg)
    binv = eb.matrix_world.inverted()
    up = Vector((0.0, 0.0, 1.0))
    V = G.world_verts(SH)
    n_in = 0
    for q in V[::step]:
        o = binv @ Vector(q.tolist())
        hits, guard = 0, 0
        while guard < 24:
            guard += 1
            h = bt.ray_cast(o, up, 10.0)
            if h[0] is None:
                break
            hits += 1
            o = h[0] + up * 1e-4
        if hits % 2 == 1:
            n_in += 1
    return n_in, len(V[::step])


res = {}
# ONE shift, computed at REST, baked into the vertex data.
#
# The first version recomputed and applied it per pose, and the carry pose came
# back with the fist at 75.4% of the radius instead of 0%. The shift is right;
# the CONVERSION was wrong. It mapped a world-space displacement through
# SH.matrix_world, which does not contain the LeftHand bone's pose rotation --
# that lives in the armature modifier. At rest the bone rotation is identity so
# it worked, and at carry it silently rotated the displacement away from where
# it was aimed. Baking at rest avoids the question entirely: the shield is bound
# 100% to LeftHand, so a rest-frame offset is preserved in EVERY pose by the
# skinning itself.
pose("rest")
fc, nf = fist_centre()
c, n, ip, rad, th, V = disc_frame()
spine = np.array((arm.matrix_world @ arm.pose.bones["Spine02"].matrix).translation)
out_n = n if float(np.dot(c - spine, n)) > 0 else -n
off0 = float(np.linalg.norm((fc - c) @ ip))
stand = th * 0.5 + 0.02
shift = (fc + out_n * stand) - c
print("\nshield radius %.4f m, thickness %.4f m" % (rad, th))
print("fist sits %.4f m from the boss = %.1f%% of the radius  ->  %s"
      % (off0, 100 * off0 / rad,
         "OFF THE DISC ENTIRELY" if off0 > rad else "off-centre"))
print("centre-grip shift: %.4f m, standoff %.4f m behind the face"
      % (float(np.linalg.norm(shift)), stand))

baseline = {}
for which in ("rest", "carry"):
    pose(which)
    inb, samp = inside_count()
    baseline[which] = inb
    print("  BEFORE, %-5s pose: %d of %d sampled shield verts inside the body"
          % (which, inb, samp))

co = np.empty(len(SH.data.vertices) * 3)
SH.data.vertices.foreach_get("co", co)
P = co.reshape(-1, 3)
pose("rest")
M = np.array(SH.matrix_world)
SH.data.vertices.foreach_set("co", (P + (np.linalg.inv(M[:3, :3]) @ shift)).ravel())
SH.data.update()
bpy.context.view_layer.update()

after = {}
for which in ("rest", "carry"):
    pose(which)
    fc2, _ = fist_centre()
    c2, n2, ip2, rad2, th2, _ = disc_frame()
    off2 = float(np.linalg.norm((fc2 - c2) @ ip2))
    ina, samp = inside_count()
    after[which] = dict(fist_inplane_m=round(off2, 4),
                        fist_pct_radius=round(100 * off2 / rad2, 1),
                        inside=ina, sampled=samp)
    print("  AFTER,  %-5s pose: fist %.4f m from the boss (%.1f%% of radius); "
          "inside %d -> %d of %d" % (which, off2, 100 * off2 / rad2,
                                     baseline[which], ina, samp))

res = dict(radius_m=round(rad, 4), thickness_m=round(th, 4),
           fist_before=dict(inplane_m=round(off0, 4),
                            pct_radius=round(100 * off0 / rad, 1),
                            verdict="off the disc entirely"),
           shift_m=[round(float(x), 5) for x in shift],
           shift_len_m=round(float(np.linalg.norm(shift)), 4),
           standoff_m=round(stand, 4),
           inside_before=baseline, after=after)
if OUTJ:
    json.dump(res, open(OUTJ, "w"), indent=1)
    print("\nwrote %s" % OUTJ)
