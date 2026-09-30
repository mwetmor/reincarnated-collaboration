# The staff CARRY POSE: spine up at rest, the staff arm holding the staff UPRIGHT like a walking staff.
#
#   blender -b -noaudio --python scripts/s12_carry.py -- <seated_full.glb> <out.json>
#        [--hand 0.24,0.22,1.08]   (her right, forward, height -- metres, at rest)
#
# Authored against the SEATED staff (weapon_r's rest is the mount: +Y along the shaft to the crown),
# so "upright" is measured on the real thing, not assumed from the hand.
#   1. two-bone IK, ANALYTIC: RightArm + RightForeArm put the hand at the target, elbow down/back
#      (a sweep and Blender's own IK both failed on the shield carry -- 0.22 m short, and an elbow
#      flung to [1.03, 0.61, 0.33]; the closed form cannot do either)
#   2. RightHand turned by the MINIMAL rotation that takes the shaft onto world up
#   3. measured: tilt, hand height, butt and crown heights, staff inside the body (crossing parity)
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector, Quaternion
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s12_carry.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
hx, hy, hz = (float(v) for v in (a[a.index('--hand') + 1] if '--hand' in a else "0.24,0.22,1.08").split(","))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
meshes = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
body = next(o for o in meshes if o.name.startswith("char1"))
staff = next(o for o in meshes if "staff" in o.name.lower())
if arm.animation_data:
    arm.animation_data.action = None; arm.animation_data.use_nla = False
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
MW = arm.matrix_world
W = lambda n: MW @ arm.pose.bones[n].head
# her right is -X and she faces -Y (Blender)
target = Vector((-hx, -hy, hz))
S_, E0, H0 = W("RightArm"), W("RightForeArm"), W("RightHand")
l1, l2 = (E0 - S_).length, (H0 - E0).length
d = min((target - S_).length, (l1 + l2) * 0.999)
# elbow: law of cosines in the plane (S, T, pole); pole = down and back from the shoulder
ax = (target - S_).normalized()
pole = Vector((0.0, 0.35, -1.0)).normalized()
pole = (pole - ax * pole.dot(ax)).normalized()
cosA = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
A = math.acos(max(-1.0, min(1.0, cosA)))
elbow = S_ + (ax * math.cos(A) + pole * math.sin(A)) * l1
hand = S_ + ax * d


def aim(bone, head, tip):
    """Turn a pose bone by the minimal rotation that points it head->tip (world), keeping its roll."""
    pb = arm.pose.bones[bone]
    cur = (MW @ pb.tail - MW @ pb.head).normalized()
    want = (tip - head).normalized()
    R = cur.rotation_difference(want).to_matrix().to_4x4()
    Mw = MW @ pb.matrix
    t = Mw.translation.copy()
    Mn = Matrix.Translation(t) @ R @ Matrix.Translation(-t) @ Mw
    pb.matrix = MW.inverted() @ Mn
    bpy.context.view_layer.update()


aim("RightArm", S_, elbow)
aim("RightForeArm", W("RightForeArm"), hand)
# the shaft: weapon_r's +Y (the mount put the shaft there), in world
def shaft():
    wb = arm.pose.bones["weapon_r"]
    m = (MW @ wb.matrix).to_3x3()
    return (m @ Vector((0, 1, 0))).normalized()
s0 = shaft()
R = s0.rotation_difference(Vector((0, 0, 1))).to_matrix().to_4x4()
pb = arm.pose.bones["RightHand"]
Mw = MW @ pb.matrix; t = Mw.translation.copy()
pb.matrix = MW.inverted() @ (Matrix.Translation(t) @ R @ Matrix.Translation(-t) @ Mw)
bpy.context.view_layer.update()
s1 = shaft()
tilt = math.degrees(math.acos(max(-1, min(1, s1.z))))
# staff extent along its shaft, posed
SV = G.world_verts(staff)
hand_w = W("RightHand")
along = SV @ np.array(s1)
butt = SV[np.argmin(along)]; crown = SV[np.argmax(along)]
# penetration: crossing parity of staff vertices in the body
dg = bpy.context.evaluated_depsgraph_get()
bt = BVHTree.FromObject(body, dg); binv = body.evaluated_get(dg).matrix_world.inverted()
up = Vector((0, 0, 1)); n_in = 0
for q in SV[::3]:
    o = binv @ Vector(q.tolist()); h_ = 0
    for _ in range(24):
        hit = bt.ray_cast(o, up, 10.0)
        if hit[0] is None: break
        h_ += 1; o = hit[0] + up * 1e-4
    n_in += h_ % 2
elbow_ang = math.degrees(((W("RightForeArm") - W("RightArm")).normalized()).angle((W("RightHand") - W("RightForeArm")).normalized()))
print("CARRY: shaft tilt %.2f deg (was %.1f before the hand turn)" % (tilt, math.degrees(s0.angle(Vector((0, 0, 1))))))
print("       hand at %s (target %s), elbow flexion %.0f deg" % ([round(v, 3) for v in hand_w], [round(v, 3) for v in target], elbow_ang))
print("       butt at height %.3f m, crown at %.3f m; staff verts inside the body %d of %d sampled"
      % (butt[2], crown[2], n_in, len(SV[::3])))
BONES = ["Spine02", "Spine01", "Spine", "neck", "Head", "RightShoulder", "RightArm", "RightForeArm", "RightHand"]
json.dump(dict(bones={b: [x for row in arm.pose.bones[b].matrix_basis for x in row] for b in BONES},
               filter_bones=BONES,
               measured=dict(tilt_deg=round(tilt, 3), hand=[round(v, 4) for v in hand_w],
                             elbow_flexion_deg=round(elbow_ang, 1), butt_z=round(float(butt[2]), 4),
                             crown_z=round(float(crown[2]), 4), staff_inside_body=int(n_in),
                             sampled=int(len(SV[::3]))),
               target=[hx, hy, hz]), open(OUT, "w"), indent=1)
print("wrote", OUT)
