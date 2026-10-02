# R-C9-128 CAPE, the real fix: a CAPE BONE CHAIN for runtime secondary motion (Godot SpringBoneSimulator3D). Three columns -- the
# cape's own three panels (L = his left, B = back, R = his right; split at slit_x) -- of ROWS bones each, from the cape's top edge
# to its hem, the column roots parented to 'Spine' (his chest: the parent of neck and both shoulders on this rig). The cape is
# RE-SKINNED to its column: a vertex between joint k and k+1 belongs to bone k, blended into k+1 over the last BLEND of the
# segment; the top TOPBAND m stays on Spine (fading into bone 0), so the top edge lies where 3a put it. The body skeleton is
# untouched; the cape file carries the 26 body joints + the cape_* bones, which gear.gd adds to the body skeleton at runtime
# (bind by name). Heads are the panel's median point at each joint height, pushed IN by --inset m (toward the body) so the
# chain line lies inside the cloth.
#   blender -b -noaudio --python e50_cape_chain.py -- <body.glb> <cape.glb> <out.glb> --slit 0.1604 [--rows 4] [--json f]
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]; BODY, CAPE, OUT = a[:3]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
SLIT = float(opt('--slit', '0.1604')); ROWS = int(opt('--rows', '4')); TOPBAND = float(opt('--topband', '0.06')); BLEND = float(opt('--blend', '0.30'))
INSET = float(opt('--inset', '0.01'))
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene; arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = max([o for o in sc.objects if o.type == 'MESH' and o.vertex_groups], key=lambda o: len(o.data.vertices))
for o in [o for o in sc.objects if o.type == 'MESH' and o is not body]: bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones: pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=CAPE)
new = [o for o in sc.objects if o not in before]; cape = next(o for o in new if o.type == 'MESH' and o.vertex_groups)
mw = cape.matrix_world.copy()
for o in new:
    if o is not cape: bpy.data.objects.remove(o, do_unlink=True)
cape.parent = None; cape.matrix_world = mw
co = np.array([(cape.matrix_world @ v.co)[:] for v in cape.data.vertices])
AW = arm.matrix_world; cx = float((AW @ arm.pose.bones['Hips'].head).x)
xs = co[:, 0] - cx
# panel per vertex from its faces (as e13 does), so split copies at the slits take their own panel
fl = {}
for poly in cape.data.polygons:
    m_ = float(np.mean([xs[v] for v in poly.vertices])); lab = 'L' if m_ > SLIT else ('R' if m_ < -SLIT else 'B')
    for v in poly.vertices: fl.setdefault(v, []).append(lab)
panel = np.array([max(set(fl.get(i, ['B'])), key=fl.get(i, ['B']).count) for i in range(len(co))])
# --- the chain: per column, ROWS+1 joint heights from the column's top to its hem
bpy.context.view_layer.objects.active = arm; arm.select_set(True); bpy.ops.object.mode_set(mode='EDIT')
eb = arm.data.edit_bones; AWi = AW.inverted(); chains = {}
spine_head_w = AW @ arm.pose.bones['Spine'].head
for col in ('L', 'B', 'R'):
    P = co[panel == col]; ztop, zbot = float(P[:, 2].max()), float(P[:, 2].min())
    zs = np.linspace(ztop - 0.02, zbot, ROWS + 1); joints = []
    for z in zs:
        s = np.abs(P[:, 2] - z) < 0.03; Q = P[s] if s.sum() > 5 else P[np.argsort(np.abs(P[:, 2] - z))[:20]]
        j = np.median(Q, axis=0); j[1] -= INSET                       # toward the body (his back faces +Y in Blender)
        joints.append(Vector(j.tolist()))
    names = []
    for k in range(ROWS):
        nm = 'cape_%s_%d' % (col, k); b = eb.new(nm); b.head = AWi @ joints[k]; b.tail = AWi @ joints[k + 1]
        b.parent = eb['Spine'] if k == 0 else eb[names[-1]]; b.use_connect = k > 0; b.use_deform = True; names.append(nm)
    chains[col] = dict(bones=names, z=zs.tolist(), joints=[list(j) for j in joints])
bpy.ops.object.mode_set(mode='OBJECT')
# --- reskin
for g in list(cape.vertex_groups): cape.vertex_groups.remove(g)
grp = {n: cape.vertex_groups.new(name=n) for col in chains.values() for n in col['bones']}; gs = cape.vertex_groups.new(name='Spine')
cnt = {}
for i, p in enumerate(co):
    c = chains[panel[i]]; zs = c['z']; z = p[2]; ztop = zs[0] + 0.02
    if z >= ztop - TOPBAND:                                            # the top band: on the chest, fading into bone 0
        f = np.clip((ztop - z) / TOPBAND, 0, 1); gs.add([i], 1 - f, 'REPLACE');
        if f > 0: grp[c['bones'][0]].add([i], f, 'REPLACE')
        continue
    k = int(np.clip(np.searchsorted(-np.array(zs), -z) - 1, 0, ROWS - 1))   # segment k: zs[k] >= z > zs[k+1]
    seg = (zs[k] - z) / max(zs[k] - zs[k + 1], 1e-6)
    if k < ROWS - 1 and seg > 1 - BLEND:
        u = (seg - (1 - BLEND)) / BLEND * 0.5; grp[c['bones'][k]].add([i], 1 - u, 'REPLACE'); grp[c['bones'][k + 1]].add([i], u, 'REPLACE')
    else:
        grp[c['bones'][k]].add([i], 1.0, 'REPLACE')
    cnt[c['bones'][k]] = cnt.get(c['bones'][k], 0) + 1
cape.parent = arm; cape.matrix_parent_inverse = arm.matrix_world.inverted(); cape.matrix_world = mw
md = cape.modifiers.new('arm', 'ARMATURE'); md.object = arm
bpy.data.objects.remove(body, do_unlink=True)
for x in list(bpy.data.actions): bpy.data.actions.remove(x)
bpy.ops.object.select_all(action='DESELECT'); cape.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=False, export_image_format='JPEG', export_jpeg_quality=92)
rep = dict(rows=ROWS, slit_x=SLIT, topband_m=TOPBAND, blend=BLEND, inset_m=INSET, chains={k: dict(bones=v['bones'], joint_z=[round(z, 4) for z in v['z']]) for k, v in chains.items()},
           verts_per_bone=cnt, panel_verts={c: int((panel == c).sum()) for c in 'LBR'})
print('CHAIN', json.dumps(rep))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
