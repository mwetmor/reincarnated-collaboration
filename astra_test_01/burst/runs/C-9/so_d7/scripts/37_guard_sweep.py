# Make the guard a guard: block1's left arm at PARTIAL weight.
#
#   blender -b -noaudio --python scripts/37_guard_sweep.py -- <body.glb>
#        <anims_dir> [--json f] [--write]
#
# 580 "Sword and Shield Alert Turn" gave a LOW FORWARD carry -- the shield ended
# beside his torso, not in front of it. block1 raises the left hand 0.472 m
# above the sternum, which is a full block covering the head. The guard is
# between them, so it is block1's pose at partial weight.
#
# Chosen by measurement, not by eye:
#   penetration   crossing parity, target near the 12 the old guard scored
#   height        the boss at CHEST level, not the waist and not the head
#   forward       the disc in FRONT of the sternum, not beside it
#   visible area  pi r^2 |n . v| from S/SE/E -- exact for a flat disc, and it
#                 needs no render, so the whole sweep costs one Blender run
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector, Quaternion
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("37_guard_sweep.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, ANIMS = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
WRITE = '--write' in a
ROOT = os.path.dirname(HERE)
CHAIN = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand")

# ---- capture block1's left arm at its peak -------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ANIMS, "block1.glb"))
sc = bpy.context.scene
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
bact = max(bpy.data.actions, key=lambda x: x.frame_range[1] - x.frame_range[0])
barm.animation_data.action = bact
best, bf = -9e9, 0
for f in range(int(bact.frame_range[0]), int(bact.frame_range[1]) + 1):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    ch = (barm.matrix_world @ barm.pose.bones["Spine02"].matrix).translation
    lh = (barm.matrix_world @ barm.pose.bones["LeftHand"].matrix).translation
    s_ = float(lh.z - ch.z) + float((lh - ch).dot(Vector((0, -1, 0))))
    if s_ > best:
        best, bf = s_, f
sc.frame_set(bf)
bpy.context.view_layer.update()
FULL = {b: barm.pose.bones[b].matrix_basis.copy() for b in CHAIN}
print("block1 left-arm peak at frame %d (score %+0.3f)" % (bf, best))

# ---- the body + shield ----------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
BD = body[0]
kb = BD.data.shape_keys.key_blocks if BD.data.shape_keys else {}
for n_ in ("grip_L", "grip_R"):
    if n_ in kb:
        kb[n_].value = 1.0
before = set(sc.objects)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "export", "shield.glb"))
add = [o for o in sc.objects if o not in before]
SH = next(o for o in add if o.type == 'MESH' and o.vertex_groups)
SH_ARM = next(o for o in add if o.type == 'ARMATURE')
for o in [o for o in add if o.type == 'MESH' and o is not SH]:
    bpy.data.objects.remove(o, do_unlink=True)
RIGS = [arm, SH_ARM]


def set_w(w):
    for A in RIGS:
        if A.animation_data:
            A.animation_data.action = None
        for pb in A.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
        for b in CHAIN:
            if b not in A.pose.bones:
                continue
            m = FULL[b]
            loc, rot, scl = m.decompose()
            q = Quaternion().slerp(rot, w)
            A.pose.bones[b].matrix_basis = (
                Matrix.Translation(loc * w) @ q.to_matrix().to_4x4())
    bpy.context.view_layer.update()


def measure():
    V = G.world_verts(SH)
    c = V.mean(axis=0)
    ev, evec = np.linalg.eigh(np.cov((V - c).T))
    n = evec[:, 0] / np.linalg.norm(evec[:, 0])
    ip = evec[:, 1:]
    rad = float(np.linalg.norm((V - c) @ ip, axis=1).max())
    ch = np.array((arm.matrix_world @ arm.pose.bones["Spine02"].matrix).translation)
    hd = np.array((arm.matrix_world @ arm.pose.bones["Head"].matrix).translation)
    dg = bpy.context.evaluated_depsgraph_get()
    bt = BVHTree.FromObject(BD, dg)
    binv = BD.evaluated_get(dg).matrix_world.inverted()
    up = Vector((0.0, 0.0, 1.0))
    nin = 0
    for q in V[::4]:
        o = binv @ Vector(q.tolist())
        h_, g_ = 0, 0
        while g_ < 24:
            g_ += 1
            hit = bt.ray_cast(o, up, 10.0)
            if hit[0] is None:
                break
            h_ += 1
            o = hit[0] + up * 1e-4
        if h_ % 2 == 1:
            nin += 1
    el = math.radians(52.95)
    vis = {}
    for fac, deg in (("S", 0), ("SE", 45), ("E", 90)):
        az = math.radians((360 - deg) % 360)
        v = -np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                       math.sin(el)])
        vis[fac] = round(math.pi * rad * rad * abs(float(np.dot(n, v))), 4)
    return dict(inside=nin, sampled=len(V[::4]),
                boss_above_sternum_m=round(float(c[2] - ch[2]), 4),
                boss_below_head_m=round(float(hd[2] - c[2]), 4),
                boss_fwd_of_sternum_m=round(float(np.dot(c - ch, [0, -1, 0])), 4),
                visible_m2=vis, radius_m=round(rad, 4))


rows = {}
for w in (0.0, 0.5, 0.6, 0.7, 0.8, 1.0):
    set_w(w)
    r = measure()
    rows["%.2f" % w] = r
    print("  w=%.2f  inside %3d/%d | boss %+0.3f above sternum, %+0.3f in front, "
          "%0.3f below head | visible S %.3f SE %.3f E %.3f m2"
          % (w, r["inside"], r["sampled"], r["boss_above_sternum_m"],
             r["boss_fwd_of_sternum_m"], r["boss_below_head_m"],
             r["visible_m2"]["S"], r["visible_m2"]["SE"], r["visible_m2"]["E"]))

if OUTJ:
    json.dump(dict(block1_peak_frame=bf, rows=rows), open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
if WRITE:
    w = float(os.environ.get("GUARD_W", "0.7"))
    set_w(w)
    json.dump({b: [x for row in arm.pose.bones[b].matrix_basis for x in row]
               for b in CHAIN},
              open(os.path.join(ROOT, "work", "guard_pose.json"), "w"), indent=1)
    print("wrote work/guard_pose.json at w=%.2f" % w)
