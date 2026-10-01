# R-C9-123 (A): NARROW THE BASE -- his rest stands heel-to-heel 1.63x hip width, and every clip on his rig inherits the splay.
# The thighs are ADDUCTED at the hip (about his forward axis, through each hip joint) until heel-to-heel = --target x hip width,
# and each foot is counter-rotated by the same angle so the sole stays flat; the posed body is baked as the new REST mesh (to be
# re-rigged by Meshy), and every gear isolation (static, same rest space) is carried by the SAME deformation: each vertex moves by
# the inverse-distance mean displacement of its 8 nearest body vertices.
#   blender -b -noaudio --python e41_narrow_base.py -- <rigged.glb> <out_body.glb> --target 1.10 --pieces a.glb,b.glb [--suffix _narrow] [--json f]
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.kdtree import KDTree
a = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
TGT = float(opt('--target', '1.10')); PIECES = [p for p in opt('--pieces', '').split(',') if p]; SUF = opt('--suffix', '_narrow')
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene; arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = max([o for o in sc.objects if o.type == 'MESH' and o.vertex_groups], key=lambda o: len(o.data.vertices))
for o in [o for o in sc.objects if o.type == 'MESH' and o is not body]: bpy.data.objects.remove(o, do_unlink=True)
if arm.animation_data: arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
AW = arm.matrix_world.copy(); AWi = AW.inverted()
def wpos(n): return AW @ arm.pose.bones[n].head
def worldverts(o):
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    V = np.array([(o.matrix_world @ v.co)[:] for v in me.vertices]); oe.to_mesh_clear(); return V
V0 = worldverts(body)
hipL, hipR, fL, fR = wpos('LeftUpLeg'), wpos('RightUpLeg'), wpos('LeftFoot'), wpos('RightFoot')
hipw = abs(hipL.x - hipR.x); h2h0 = abs(fL.x - fR.x)
def rotate_world(pbname, axis_w, ang, pivot_w):
    pb = arm.pose.bones[pbname]
    Mw = AW @ pb.matrix
    R = Matrix.Translation(pivot_w) @ Matrix.Rotation(ang, 4, axis_w) @ Matrix.Translation(-pivot_w)
    pb.matrix = AWi @ R @ Mw; bpy.context.view_layer.update()
rep = dict(hip_width_m=round(hipw, 4), heel_to_heel_before=round(h2h0 / hipw, 3), target=TGT, legs={})
for side, up, foot, sign in (('L', 'LeftUpLeg', 'LeftFoot', 1), ('R', 'RightUpLeg', 'RightFoot', -1)):
    hip = wpos(up); ft = wpos(foot); want_x = (hipL.x + hipR.x) / 2 + (1 if ft.x > (hipL.x + hipR.x) / 2 else -1) * TGT * hipw / 2
    # find the angle about world forward (Y) that puts the foot at want_x (bisection on the actual pose)
    lo, hi = -0.6, 0.6; base = [b.matrix_basis.copy() for b in arm.pose.bones]
    def footx(ang):
        for b_, m_ in zip(arm.pose.bones, base): b_.matrix_basis = m_
        bpy.context.view_layer.update(); rotate_world(up, Vector((0, 1, 0)), ang, hip); return wpos(foot).x
    f_lo, f_hi = footx(lo) - want_x, footx(hi) - want_x
    for _ in range(40):
        mid = (lo + hi) / 2; fm = footx(mid) - want_x
        if (fm > 0) == (f_lo > 0): lo, f_lo = mid, fm
        else: hi = mid
    ang = (lo + hi) / 2; footx(ang)
    rotate_world(foot, Vector((0, 1, 0)), -ang, wpos(foot))           # the sole back to flat
    rep['legs'][side] = dict(adduction_deg=round(math.degrees(ang), 2))
fL2, fR2 = wpos('LeftFoot'), wpos('RightFoot'); rep['heel_to_heel_after'] = round(abs(fL2.x - fR2.x) / hipw, 3)
V1 = worldverts(body); D = V1 - V0
rep['feet_floor_shift_m'] = round(float(V1[:, 2].min() - V0[:, 2].min()), 4)
# bake the posed body as a static mesh (no armature), keep material/UVs
dg = bpy.context.evaluated_depsgraph_get(); me2 = bpy.data.meshes.new_from_object(body.evaluated_get(dg))
nb = bpy.data.objects.new('body_narrow', me2); sc.collection.objects.link(nb); nb.matrix_world = body.matrix_world.copy()
kd = KDTree(len(V0))
for i, p in enumerate(V0): kd.insert(Vector(p), i)
kd.balance()
def carry(path):
    bpy.ops.object.select_all(action='DESELECT'); before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in sc.objects if o not in before and o.type == 'MESH']
    moved = []
    for o in new:
        for v in o.data.vertices:
            pw = o.matrix_world @ v.co; nn = kd.find_n(pw, 8); w = np.array([1.0 / max(d, 1e-5) for _, _, d in nn]); w /= w.sum()
            dv = sum(w[k] * D[nn[k][1]] for k in range(len(nn))); v.co = o.matrix_world.inverted() @ (pw + Vector(dv)); moved.append(float(np.linalg.norm(dv)))
        o.data.update()
    out = path.replace('.glb', SUF + '.glb')
    bpy.ops.object.select_all(action='DESELECT')
    for o in new: o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_image_format='AUTO')
    for o in [o for o in sc.objects if o not in before]: bpy.data.objects.remove(o, do_unlink=True)
    return out, (round(float(np.median(moved)), 4), round(float(np.max(moved)), 4)) if moved else None
for p in PIECES:
    o_, mv = carry(p); rep.setdefault('pieces', {})[os.path.basename(p)] = dict(out=o_, moved_median_max_m=mv)
bpy.ops.object.select_all(action='DESELECT'); nb.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='JPEG', export_jpeg_quality=92)
print('NARROW', json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
