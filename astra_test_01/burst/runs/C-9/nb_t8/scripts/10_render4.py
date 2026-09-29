# T8: four flat ortho views of a model, height-normalised, for the IoU pass
# against the painted NB-1_b plates, plus mesh statistics.
#
#   blender -b -noaudio --python scripts/10_render4.py -- <glb> <outdir> <tag>
#
# Elevation 0 because the plates are flat paintings and an IoU against them has
# to be measured in their own projection (T6's reasoning, kept).
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT, TAG = a[0], a[1], a[2]
RES = 640
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
for o in meshes:
    for s in o.material_slots:
        m = s.material
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        em = nt.nodes.new('ShaderNodeEmission')
        L = b.inputs['Base Color'].links if b else []
        if L:
            nt.links.new(L[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
# ---- mesh statistics, after an exact-position weld (glTF splits at UV seams)
tri = vert = 0
bm = bmesh.new()
for o in meshes:
    me = o.data.copy()
    me.transform(o.matrix_world)
    bm.from_mesh(me)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
bmesh.ops.triangulate(bm, faces=bm.faces)
bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
tri, vert = len(bm.faces), len(bm.verts)
boundary = sum(1 for e in bm.edges if len(e.link_faces) < 2)
nonman = sum(1 for e in bm.edges if len(e.link_faces) > 2)
# islands
seen = set(); islands = []
for v in bm.verts:
    if v.index in seen:
        continue
    stack, comp = [v], 0
    seen.add(v.index)
    while stack:
        w = stack.pop(); comp += 1
        for e in w.link_edges:
            u = e.other_vert(w)
            if u.index not in seen:
                seen.add(u.index); stack.append(u)
    islands.append(comp)
islands.sort(reverse=True)
V = np.array([list(v.co) for v in bm.verts])
bm.free()
lo, hi = V.min(0), V.max(0); H = float(hi[2] - lo[2])
stats = dict(tag=TAG, tris=tri, verts=vert, boundary_edges=boundary,
             non_manifold_edges=nonman, islands=len(islands),
             island_sizes=islands[:6],
             watertight=bool(boundary == 0 and nonman == 0),
             height=round(H, 5),
             bbox_lo=[round(float(v), 4) for v in lo],
             bbox_hi=[round(float(v), 4) for v in hi])
print(json.dumps(stats))
# ---- four flat views, camera at azimuth 0/90/180/270 about the model -------
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = H * 1.10
ctr = Vector(((lo + hi) / 2).tolist())
os.makedirs(OUT, exist_ok=True)
for k, az in enumerate((0, 90, 180, 270)):
    A = math.radians(az)
    pos = ctr + Vector((math.sin(A), -math.cos(A), 0.0)) * (10 * H)
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, "%s_az%03d.png" % (TAG, az))
    bpy.ops.render.render(write_still=True)
json.dump(stats, open(os.path.join(OUT, "%s_stats.json" % TAG), "w"), indent=1)
