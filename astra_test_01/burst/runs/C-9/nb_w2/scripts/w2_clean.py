# The sword's raw Tripo build -> one clean island, seams welded, decimated. Nothing re-oriented or
# re-scaled here (w3_skin.py does that in numpy, against measured features).
#
#   blender -b -noaudio --python scripts/w2_clean.py -- <builds/sword.glb> <out.glb> [--faces 9000] [--json f]
#
# WELD BEFORE DECIMATING (the D7 pass-2 lesson): glTF cuts a mesh at every UV seam, and the collapse
# decimator thins the two sides of a seam independently -- hairline cracks along every seam. Welding
# co-located vertices first joins the islands (UVs are per face-corner, so every face keeps its own).
# ONE ISLAND: after the weld, every connected component but the largest is reported and dropped.
# Face budget: the axe it shares weapon_r with is 9,000 triangles.
import bpy, bmesh, json, sys
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
FACES = int(a[a.index('--faces') + 1]) if '--faces' in a else 9000
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
assert len(obs) == 1, "expected one mesh, found %d" % len(obs)
ob = obs[0]
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
rep = dict(source=SRC, raw=dict(verts=len(ob.data.vertices), faces=len(ob.data.polygons)))
bm = bmesh.new(); bm.from_mesh(ob.data)
n0 = len(bm.verts)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
rep["welded"] = dict(verts_before=n0, verts_after=len(bm.verts))
# islands
bm.faces.ensure_lookup_table()
seen = set(); comps = []
for f in bm.faces:
    if f.index in seen:
        continue
    stack = [f]; comp = []; seen.add(f.index)
    while stack:
        g = stack.pop(); comp.append(g)
        for e in g.edges:
            for h in e.link_faces:
                if h.index not in seen:
                    seen.add(h.index); stack.append(h)
    comps.append(comp)
comps.sort(key=len, reverse=True)
rep["islands"] = dict(count=len(comps), faces=[len(c) for c in comps[:8]])
drop = [f for c in comps[1:] for f in c]
if drop:
    bmesh.ops.delete(bm, geom=drop, context='FACES')
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
bm.to_mesh(ob.data); bm.free(); ob.data.update()
f1 = len(ob.data.polygons)
m = ob.modifiers.new('dec', 'DECIMATE'); m.ratio = min(1.0, FACES / max(f1, 1))
bpy.ops.object.modifier_apply(modifier='dec')
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris(); bpy.ops.object.mode_set(mode='OBJECT')
rep["kept"] = dict(island_faces_before_decimation=f1, verts=len(ob.data.vertices), faces=len(ob.data.polygons))
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_image_format='AUTO')
print("sword: %s" % json.dumps(rep))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
