# E1: the MACE on his right hand, the TWO-HANDED GRIP TAKEN FROM THE CLIP. In the armed walk's held pose (the pose the
# idle/run hold copies) the haft is laid through BOTH fists (deformed hand-vertex centroids): the right fist on the mid grip
# (0.68 m from the butt), the head beyond it. That placement is expressed in RightHand's frame (G) and
# re-applied at REST, the mace skinned 1.0 to RightHand (52_weapon_bones later rebinds it to weapon_r, coincident).
#   blender -b -noaudio --python e10_mace_mount.py -- <body.glb> <mace_tripo.glb> <out_piece.glb> --clip walk --t 0.8667
#        [--length 1.45] [--json f]
import bpy, bmesh, json, math, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
BODY, MACE, OUT = a[:3]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIP, T, LEN = opt('--clip', 'walk'), float(opt('--t', '0.8667')), float(opt('--length', '1.45'))
RIGHT_FROM_BUTT = 0.68   # the right fist on the mid-haft grip (sheet: mid grip 0.42-0.52 of the length from the butt)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene; FPS = sc.render.fps / sc.render.fps_base
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = max([o for o in sc.objects if o.type == 'MESH' and o.vertex_groups], key=lambda o: len(o.data.vertices))
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]: bpy.data.objects.remove(o, do_unlink=True)
act = bpy.data.actions[next(n for n in [x.name for x in bpy.data.actions] if n == CLIP or n.startswith(CLIP))]
arm.animation_data.action = act
if hasattr(arm.animation_data, 'action_slot') and act.slots: arm.animation_data.action_slot = act.slots[0]
sc.frame_set(int(T * FPS), subframe=(T * FPS) % 1.0); bpy.context.view_layer.update()
def fist(bone):
    dg = bpy.context.evaluated_depsgraph_get(); be = body.evaluated_get(dg); me = be.to_mesh()
    gi = body.vertex_groups[bone].index
    idx = [v.index for v in body.data.vertices if any(g.group == gi and g.weight > 0.3 for g in v.groups)]
    M = np.array(body.matrix_world); co = np.array([me.vertices[i].co[:] for i in idx])
    W = co @ M[:3, :3].T + M[:3, 3]; be.to_mesh_clear(); return W.mean(0)
R, Lh = fist('RightHand'), fist('LeftHand')
RH_pose = arm.matrix_world @ arm.pose.bones['RightHand'].matrix
d = (R - Lh) / np.linalg.norm(R - Lh)   # left fist -> right fist; the head lies beyond the RIGHT fist
sep = float(np.linalg.norm(R - Lh))
# the mace: weld, haft = longest PCA axis, head = the wider end; butt at origin, +Y to head, length LEN
bpy.ops.import_scene.gltf(filepath=MACE)
mo = [o for o in sc.objects if o.type == 'MESH' and o != body and not o.vertex_groups]
bpy.ops.object.select_all(action='DESELECT')
for o in mo: o.select_set(True)
bpy.context.view_layer.objects.active = mo[0]
if len(mo) > 1: bpy.ops.object.join()
m = bpy.context.view_layer.objects.active; m.parent = None
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
co = np.empty(len(m.data.vertices) * 3); m.data.vertices.foreach_get('co', co); V = co.reshape(-1, 3)
c = V.mean(0); _, _, vt = np.linalg.svd((V - c)[::max(1, len(V) // 5000)], full_matrices=False); ax = vt[0]
s = (V - c) @ ax; lo_, hi_ = s.min(), s.max(); L0 = hi_ - lo_
def width(lo, hi):
    k = (s > lo) & (s < hi); P = (V[k] - c) - np.outer(s[k], ax); return np.linalg.norm(P, axis=1).max() if k.any() else 0
if width(hi_ - 0.25 * L0, hi_) < width(lo_, lo_ + 0.25 * L0): ax = -ax; s = -s; lo_, hi_ = -hi_, -lo_
butt = c + ax * lo_
# local frame: +Y = ax; X = any perpendicular
x0 = np.cross(ax, [0, 0, 1.0]); x0 = x0 / np.linalg.norm(x0) if np.linalg.norm(x0) > 1e-3 else np.array([1.0, 0, 0]); z0 = np.cross(x0, ax)
B = np.eye(4); B[:3, 0], B[:3, 1], B[:3, 2], B[:3, 3] = x0, ax, z0, butt
k = LEN / L0
Mloc = np.diag([k, k, k, 1.0]) @ np.linalg.inv(B)          # mace verts -> canonical (butt origin, +Y to head, metres)
# canonical -> world in the HOLD pose: right fist at RIGHT_FROM_BUTT from the butt, +Y along d (left -> right fist)
x1 = np.cross(d, [0, 0, 1.0]); x1 = x1 / np.linalg.norm(x1); z1 = np.cross(x1, d)
Wm = np.eye(4); Wm[:3, 0], Wm[:3, 1], Wm[:3, 2] = x1, d, z1; Wm[:3, 3] = R - d * RIGHT_FROM_BUTT
G = np.linalg.inv(np.array(RH_pose)) @ Wm                   # the grip, in RightHand's frame
# at REST
arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis.identity()
bpy.context.view_layer.update()
RH_rest = np.array(arm.matrix_world @ arm.pose.bones['RightHand'].matrix)
Mrest = RH_rest @ G @ Mloc
m.data.transform(Matrix(Mrest.tolist())); m.data.update()
vg = m.vertex_groups.new(name='RightHand'); vg.add(list(range(len(m.data.vertices))), 1.0, 'REPLACE')
m.parent = arm; m.matrix_parent_inverse = arm.matrix_world.inverted(); md = m.modifiers.new('arm', 'ARMATURE'); md.object = arm
m.name = 'mace'
bpy.data.objects.remove(body, do_unlink=True)
for x in list(bpy.data.actions): bpy.data.actions.remove(x)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_animations=False, export_image_format='JPEG', export_jpeg_quality=92)
head_len = None
rep = dict(clip=CLIP, t=T, fist_R=R.tolist(), fist_L=Lh.tolist(), fist_sep_m=round(sep, 4),            haft_dir_world=d.round(4).tolist(), length_m=LEN, right_fist_from_butt_m=RIGHT_FROM_BUTT, left_fist_from_butt_m=round(RIGHT_FROM_BUTT - sep, 4), G_righthand_local=np.round(G, 6).tolist(), source_length_units=round(float(L0), 5))
print(json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
