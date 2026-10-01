# R-C9-98 stage 2, step 3 of the isolation: CUT the fitted dressed build into pieces by s22's labels, or PREVIEW the labels.
#
#   blender -b -noaudio --python s23_cut.py -- <dressed_fit.glb> <labels.npz> <outdir> [--preview] [--close 6]
#
# --preview  paints each vertex by its label (body grey, hood red, gauntlets yellow, breastplate cyan, legs blue, gown
#            magenta) and renders four orthographic views to <outdir>/labels.v0-3.png (stitched outside Blender).
# cut        one GLB per piece (<outdir>/<piece>.glb), the build's own UVs and texture kept. CLOSING (07_isolate2's pass-2
#            fix): K rings of dilate-then-erode on the mesh graph re-include faces of holes narrower than ~2K rings, so a
#            rejected speck inside a piece is not a hole the body shows through. Dilation is limited to vertices whose
#            label is NOT body, so a piece never grows over the face, the braid or the boots.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, LAB, OUT = a[0], a[1], a[2]
PREVIEW = "--preview" in a
CLOSE = int(a[a.index("--close") + 1]) if "--close" in a else 6
os.makedirs(OUT, exist_ok=True)
L = np.load(LAB); lab = L["lab"]; names = [str(x) for x in L["names"]]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
d = next(o for o in sc.objects if o.type == 'MESH')
# A glTF round trip SPLITS vertices along UV seams (741,205 welded -> 767,996 on re-import), so labels cannot be matched
# by index. Each imported vertex takes the label of the coincident point of the features file (KD-tree, exact match).
if len(d.data.vertices) != len(lab):
    from mathutils.kdtree import KDTree
    FP = np.load(LAB.replace("_labels.npz", "_feat.npz"))["P"]
    kd = KDTree(len(FP))
    for i, q in enumerate(FP):
        kd.insert(Vector(q.tolist()), i)
    kd.balance()
    co = np.empty(len(d.data.vertices) * 3); d.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    Mw = np.array(d.matrix_world); co = co @ Mw[:3, :3].T + Mw[:3, 3]
    idx = np.empty(len(co), int); far = 0
    for i, q in enumerate(co):
        _, j, dd = kd.find(Vector(q.tolist())); idx[i] = j; far += dd > 1e-5
    print("labels mapped by position: %d imported verts -> %d labelled points (%d farther than 0.01 mm)" % (len(co), len(FP), far))
    lab = lab[idx]

if PREVIEW:
    COL = {-1: (0.55, 0.55, 0.55, 1), 0: (0.9, 0.1, 0.1, 1), 1: (0.95, 0.85, 0.1, 1), 2: (0.1, 0.85, 0.9, 1),
           3: (0.15, 0.3, 0.95, 1), 4: (0.85, 0.2, 0.85, 1)}
    ca = d.data.color_attributes.new("lab", 'FLOAT_COLOR', 'POINT')
    cols = np.array([COL[int(x)] for x in lab], np.float32)
    ca.data.foreach_set("color", cols.ravel())
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'VERTEX'
    sc.render.resolution_x = 512; sc.render.resolution_y = 768
    sc.world = bpy.data.worlds.new("w"); sc.world.color = (1, 1, 1)
    lo = np.array(d.bound_box).min(0); hi = np.array(d.bound_box).max(0)
    ctr = Vector(((lo + hi) / 2).tolist()); ext = float((hi - lo).max())
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = ext * 1.05
    for k, az in enumerate((0, 90, 180, 270)):
        t = math.radians(az); dv = Vector((math.sin(t), -math.cos(t), 0))
        cam.location = ctr + dv * ext * 3
        cam.rotation_euler = (dv * -1).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(OUT, "labels.v%d.png" % k)
        bpy.ops.render.render(write_still=True)
    print("preview written")
    raise SystemExit(0)

edges = np.empty(len(d.data.edges) * 2, int); d.data.edges.foreach_get("vertices", edges); edges = edges.reshape(-1, 2)
e0, e1 = edges[:, 0], edges[:, 1]
allowed = lab >= 0
rep = {}
for k, nm in enumerate(names):
    keep = lab == k
    k0 = int(keep.sum())
    for _ in range(CLOSE):
        kd = keep.copy(); kd[e1[keep[e0]]] = True; kd[e0[keep[e1]]] = True
        keep = kd & allowed
    for _ in range(CLOSE):
        bad = ~keep; ke = keep.copy(); ke[e1[bad[e0]]] = False; ke[e0[bad[e1]]] = False
        keep = ke | (lab == k)                # erosion never removes the piece's own labelled vertices
    bpy.ops.object.select_all(action='DESELECT')
    c = d.copy(); c.data = d.data.copy(); sc.collection.objects.link(c); c.name = nm
    bm = bmesh.new(); bm.from_mesh(c.data); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not keep[v.index]], context='VERTS')
    bm.to_mesh(c.data); bm.free()
    c.select_set(True); bpy.context.view_layer.objects.active = c
    p = os.path.join(OUT, nm + ".glb")
    bpy.ops.export_scene.gltf(filepath=p, export_format='GLB', use_selection=True, export_image_format='AUTO')
    rep[nm] = dict(labelled=k0, after_closing=int(keep.sum()), verts=len(c.data.vertices), faces=len(c.data.polygons),
                   mb=round(os.path.getsize(p) / 1e6, 2))
    print("  %-12s labelled %7d -> closed %7d verts, %7d faces, %.1f MB" % (nm, k0, keep.sum(), len(c.data.polygons), rep[nm]["mb"]))
    bpy.data.objects.remove(c, do_unlink=True)
json.dump(dict(close_rings=CLOSE, pieces=rep), open(os.path.join(OUT, "cut.json"), "w"), indent=1)
