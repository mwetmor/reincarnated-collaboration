# R-C9-119: author `book_carry_L` -- her LEFT arm holding the open grimoire to READ: hand in front at chest-to-waist height,
# palm UP under the spine, the hand (and the spine with it) pointing forward and tilted up toward her face.
#   blender -b -noaudio --python s45_book_carry.py -- <body.glb> <out_anim.glb> <out.json> [--tilt 40] [--centre x,y,z]
# SOLVE: two-bone IK on LeftForeArm (chain 2, a pole out to her left and down) puts the WRIST where the hand frame needs it;
# then the HAND's world rotation is set so its measured frame (gearlib.hand_frame: along wrist->fingers, the palm normal,
# signed by the direction the grip_L morph closes the fingers) lands on the target frame. Only LeftArm, LeftForeArm and
# LeftHand are keyed (frames 0 and 1), so the action layers over any clip through a filter on exactly those bones.
# Blender world: Z up, she faces -Y, her left is +X.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s45_book_carry.py")][0])); sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUTG, OUTJ = a[0], a[1], a[2]
TILT = float(a[a.index('--tilt') + 1]) if '--tilt' in a else 40.0
CEN = np.array([float(x) for x in a[a.index('--centre') + 1].split(',')]) if '--centre' in a else np.array([0.10, -0.33, 1.05])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
arm.animation_data_clear()
for act in list(bpy.data.actions):
    bpy.data.actions.remove(act)
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
bpy.context.view_layer.update()
c, chan, along, palm = G.hand_frame(bo, arm, "LeftHand")
# sign the palm normal by the grip_L morph: the fingers close TOWARD the palm
kb = bo.data.shape_keys.key_blocks
base = np.empty(len(bo.data.vertices) * 3); kb["Basis"].data.foreach_get("co", base)
gk = np.empty(len(bo.data.vertices) * 3); kb["grip_L"].data.foreach_get("co", gk)
Mb = np.array(bo.matrix_world)
d = (gk - base).reshape(-1, 3) @ Mb[:3, :3].T
mv = np.linalg.norm(d, axis=1) > 1e-3
close_dir = d[mv].mean(0)
close_dir -= (close_dir @ along) * along
if close_dir @ palm < 0:
    palm = -palm
chan = np.cross(palm, along)                         # right-handed frame (along, palm, chan) -> recomputed consistently
wrist = np.array(arm.matrix_world @ arm.pose.bones["LeftHand"].head)
Fr = np.stack([along, palm, chan], 1)
t = math.radians(TILT)
along_t = np.array([0.0, -math.cos(t), math.sin(t)])       # forward (-Y) and up
palm_t = np.array([0.0, math.sin(t), math.cos(t)])         # up and back toward her face
chan_t = np.cross(palm_t, along_t)
Ft = np.stack([along_t, palm_t, chan_t], 1)
R = Ft @ Fr.T
wrist_t = CEN - R @ (c - wrist)
# ANALYTIC two-bone solve (v2; Blender's IK constraint flipped the elbow behind her): the elbow in the plane of the shoulder,
# the target wrist and a POLE out to her left and down; each bone turned from its rest direction by the minimal rotation.
def rotm(u, v):
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v); x = np.cross(u, v); s_ = np.linalg.norm(x); c_ = float(u @ v)
    if s_ < 1e-9:
        return np.eye(3)
    k = x / s_; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + s_ * K + (1 - c_) * (K @ K)
def RW(n): return np.array(arm.matrix_world @ arm.data.bones[n].matrix_local)
sh0 = np.array(arm.matrix_world @ arm.data.bones["LeftArm"].head_local)
el0 = np.array(arm.matrix_world @ arm.data.bones["LeftForeArm"].head_local)
wr0 = wrist
l1, l2 = np.linalg.norm(el0 - sh0), np.linalg.norm(wr0 - el0)
D = wrist_t - sh0; dlen = min(np.linalg.norm(D), 0.999 * (l1 + l2)); dh = D / np.linalg.norm(D)
pole_dir = np.array([1.0, 0.25, -1.0]); pole_dir -= (pole_dir @ dh) * dh; pole_dir /= np.linalg.norm(pole_dir)
ca = (l1 * l1 + dlen * dlen - l2 * l2) / (2 * l1 * dlen); ang = math.acos(np.clip(ca, -1, 1))
el_t = sh0 + l1 * (math.cos(ang) * dh + math.sin(ang) * pole_dir)
wr_t = sh0 + dh * dlen
M1 = RW("LeftArm"); R1 = rotm(el0 - sh0, el_t - sh0); A1 = np.eye(4); A1[:3, :3] = R1 @ M1[:3, :3]; A1[:3, 3] = sh0
arm.pose.bones["LeftArm"].matrix = arm.matrix_world.inverted() @ Matrix(A1.tolist()); bpy.context.view_layer.update()
M2 = RW("LeftForeArm"); R2 = rotm(wr0 - el0, wr_t - el_t); A2 = np.eye(4); A2[:3, :3] = R2 @ M2[:3, :3]; A2[:3, 3] = el_t
arm.pose.bones["LeftForeArm"].matrix = arm.matrix_world.inverted() @ Matrix(A2.tolist()); bpy.context.view_layer.update()
hb = arm.pose.bones["LeftHand"]
Mw_rest = np.array(arm.matrix_world @ arm.data.bones["LeftHand"].matrix_local)
head_now = np.array(arm.matrix_world @ hb.head)
Mt = np.eye(4); Mt[:3, :3] = R @ Mw_rest[:3, :3]; Mt[:3, 3] = head_now
hb.matrix = arm.matrix_world.inverted() @ Matrix(Mt.tolist())
bpy.context.view_layer.update()
# --- measure what the solve achieved
def P(n): return np.array(arm.matrix_world @ arm.pose.bones[n].head)
def T(n): return np.array(arm.matrix_world @ arm.pose.bones[n].tail)
sh, el, wr = P("LeftArm"), P("LeftForeArm"), P("LeftHand")
up_dir = (el - sh) / np.linalg.norm(el - sh); fo_dir = (wr - el) / np.linalg.norm(wr - el)
Mh = np.array(arm.matrix_world @ hb.matrix)
Rh = Mh[:3, :3] @ np.linalg.inv(Mw_rest[:3, :3])
c_now = wr + Rh @ (c - wrist)
along_now = Rh @ along; palm_now = Rh @ palm
elbow_flex = math.degrees(math.acos(np.clip(up_dir @ fo_dir, -1, 1)))
wrist_dev = math.degrees(math.acos(np.clip(fo_dir @ along_now, -1, 1)))
shoulder_down = math.degrees(math.acos(np.clip(up_dir @ np.array([0, 0, -1.0]), -1, 1)))
rep = dict(tilt_deg=TILT, target_centre=CEN.round(4).tolist(), achieved_centre=c_now.round(4).tolist(),
           centre_err_m=round(float(np.linalg.norm(c_now - CEN)), 4),
           palm_err_deg=round(math.degrees(math.acos(np.clip(palm_now @ palm_t, -1, 1))), 2),
           elbow_flex_deg=round(elbow_flex, 1), wrist_deviation_deg=round(wrist_dev, 1), upper_arm_from_vertical_deg=round(shoulder_down, 1),
           elbow_world=el.round(4).tolist(), limits_note="elbow flex 0-150 deg, wrist deviation <= 70 deg, upper arm <= 100 deg from vertical: anatomical",
           rest_hand=dict(centre=c.round(5).tolist(), along=along.round(5).tolist(), palm=palm.round(5).tolist(), channel=chan.round(5).tolist(),
                          wrist=wrist.round(5).tolist()), R_rest_to_carry=R.round(6).tolist())
rep["within_limits"] = bool(elbow_flex <= 150 and wrist_dev <= 70 and shoulder_down <= 100)
# --- key the three bones and export the armature with this one action
act = bpy.data.actions.new("book_carry_L"); arm.animation_data_create(); arm.animation_data.action = act
for f in (0, 1):
    for n in ("LeftArm", "LeftForeArm", "LeftHand"):
        pb = arm.pose.bones[n]; pb.rotation_mode = 'QUATERNION'
        pb.keyframe_insert("rotation_quaternion", frame=f); pb.keyframe_insert("location", frame=f)
for o in [o for o in sc.objects if o.type != 'ARMATURE']:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUTG, export_format='GLB', use_selection=True, export_animations=True)
json.dump(rep, open(OUTJ, 'w'), indent=1); print("CARRY", json.dumps({k: v for k, v in rep.items() if k not in ('rest_hand', 'R_rest_to_carry')}))
