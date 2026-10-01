# E1 STAGE G (a), adapted from the sorceress lane's s42_under_legs.py (copied; that file untouched): the under-layer is
# RESTRICTED to the BACK of his legs between the hem and the hips (normal facing backward, +Y in Blender, dot > 0.25) -- his
# legs are bare plate, not under armour, so a whole-leg layer would repaint the legs; here only the surface the cape hides
# at rest gets it, coloured as the CAPE's dark indigo, so a leg that pokes through the cape reads as cape, not gilt plate.
# R-C9-98 follow-up (conductor 2026-10-01: peach patches at her knees and boot tops at 2x): a DARK UNDER-LAYER.
#   blender -b -noaudio --python s42_under_legs.py -- <body.glb> <out.glb> [--offset 0.0015] [--json f]
# The under_battlemage morph is computed at REST; in motion a knee bends the skin out past the cuisse/greave edges and the
# boot top opens a gap, and the peach skin shows (the whole-leg v9 morph changed nothing: s11 counts equal or higher).
# So the fix is a layer that moves WITH THE SKIN: a copy of her own leg faces (from just under the boot top to the hip),
# pushed 1.5 mm out along the normals and carrying the body's own skin weights vertex for vertex -- it can never be
# inside the skin, and where the skin would show past the armour, dark legging shows instead. Boot leather (sampled from
# her texture) is excluded, so the boots keep their own surface. Flat dark charcoal (sRGB 0.16, 0.15, 0.15), matte.
import bpy, bmesh, json, os, sys
import numpy as np
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUT = a[0], a[1]
OFF = float(a[a.index('--offset') + 1]) if '--offset' in a else 0.0015
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '.json')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
arm.animation_data_clear()
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not bo]:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.context.view_layer.update()
me = bo.data
M = np.array(bo.matrix_world)
co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
W = co @ M[:3, :3].T + M[:3, 3]
z0, z1 = W[:, 2].min(), W[:, 2].max(); zf = (W[:, 2] - z0) / (z1 - z0)
gi = {g.index: g.name for g in bo.vertex_groups}
dom = np.array([gi[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else "" for v in me.vertices])
# per-vertex texture colour (to exclude boot leather)
img = next(n.image for s in bo.material_slots if s.material and s.material.node_tree
           for n in s.material.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)
Wd, Hd = img.size
px = np.array(img.pixels[:], np.float32).reshape(Hd, Wd, img.channels)[..., :3]
uvl = me.uv_layers.active.data
UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
loops = np.empty(len(me.loops), int); me.loops.foreach_get("vertex_index", loops)
VC = np.zeros((len(W), 3), np.float32); cnt = np.zeros(len(W))
np.add.at(VC, loops, px[np.clip((UV[:, 1] * Hd).astype(int), 0, Hd - 1), np.clip((UV[:, 0] * Wd).astype(int), 0, Wd - 1)])
np.add.at(cnt, loops, 1); VC /= np.maximum(cnt, 1)[:, None]
if img.is_float:
    VC = VC ** (1 / 2.2)
mx, mn = VC.max(1), VC.min(1); sat = (mx - mn) / np.maximum(mx, 1e-6); gr = VC[:, 1] / np.maximum(VC[:, 0], 1e-6)
boot = (mx < 0.50) & (sat > 0.35) & (gr > 0.55) & (gr < 0.82) & (zf < 0.33)
_nm = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('normal', _nm); _nm = _nm.reshape(-1, 3) @ M[:3, :3].T; _nm /= np.maximum(np.linalg.norm(_nm, axis=1, keepdims=True), 1e-9)
legs = np.isin(dom, ["LeftUpLeg", "RightUpLeg", "LeftLeg", "RightLeg", "Hips"]) & (zf > 0.10) & (zf < 0.56) & (_nm[:, 1] > 0.25)
# keep FACES whose three vertices are all in
bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
keepf = [f for f in bm.faces if all(legs[v.index] for v in f.verts)]
dup = bo.copy(); dup.data = me.copy(); sc.collection.objects.link(dup); dup.name = "under_legs"
bm2 = bmesh.new(); bm2.from_mesh(dup.data); bm2.faces.ensure_lookup_table()
kill = [f for i, f in enumerate(bm2.faces) if not all(legs[v.index] for v in f.verts)]
bmesh.ops.delete(bm2, geom=kill, context='FACES')
bmesh.ops.delete(bm2, geom=[v for v in bm2.verts if not v.link_faces], context='VERTS')
bm2.normal_update()
for v in bm2.verts:
    v.co += v.normal * (OFF / float(np.mean(np.abs(np.diag(M)[:3]))))     # offset in the mesh's own (0.01-scaled) units
bm2.to_mesh(dup.data); bm2.free(); bm.free()
if dup.data.shape_keys:
    keys = [k.name for k in dup.data.shape_keys.key_blocks]
    dup.shape_key_clear()
mat = bpy.data.materials.new("under_legs_dark"); mat.use_nodes = True
bs = mat.node_tree.nodes.get("Principled BSDF")
bs.inputs["Base Color"].default_value = (0.0144, 0.0137, 0.0368, 1)   # sRGB ~0.12/0.12/0.21: the cape's dark indigo
bs.inputs["Roughness"].default_value = 0.95
dup.data.materials.clear(); dup.data.materials.append(mat)
for m in dup.modifiers:
    if m.type == 'ARMATURE':
        m.object = arm
bpy.ops.object.select_all(action='DESELECT'); dup.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=False, export_morph=False)
rep = dict(body=BODY, out=OUT, offset_m=OFF, faces=len(dup.data.polygons), verts=len(dup.data.vertices),
           band_zf=[0.10, 0.56], back_facing='normal . +Y > 0.25', boot_verts_excluded=int((boot & (zf > 0.04) & (zf < 0.56)).sum()),
           colour_srgb=[0.12, 0.12, 0.21], weights="the body's own, vertex for vertex (a copy of its faces)",
           mb=round(os.path.getsize(OUT) / 1e6, 2))
json.dump(rep, open(OUTJ, 'w'), indent=1); print("UNDER", json.dumps(rep))
