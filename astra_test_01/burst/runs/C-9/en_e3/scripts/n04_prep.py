# EN-E3 cleanup of a Tripo creature build -> one mesh, metres, ground z=0, facing -Y (Blender; = glTF +Z), footprint centred.
#   blender -b -noaudio --python scripts/n04_prep.py -- <in.glb> <out.glb> <target_length_m> [--faces 40000] [--axis y]
# Facing is MEASURED, never assumed: the head end of the long axis is the end whose last 15 % carries more volume (cross-section
# area x length); the tail end is thin. Decimation welds by distance first (the D7 lesson: unwelded UV seams split under
# the collapse and showed pale dots), and keeps the texture. Stray islands < 0.5 % of faces are dropped.
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
IN, OUT, LEN = a[0], a[1], float(a[2])
FACES = int(a[a.index('--faces') + 1]) if '--faces' in a else 40000
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for o in bpy.context.scene.objects: o.select_set(o in meshes)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
for o in list(bpy.context.scene.objects):
    if o is not ob: bpy.data.objects.remove(o, do_unlink=True)
me = ob.data; n0 = len(me.polygons)
# islands
bm = bmesh.new(); bm.from_mesh(me)
bm.faces.ensure_lookup_table()
seen = set(); islands = []
for f in bm.faces:
    if f.index in seen: continue
    st = [f]; isl = []; seen.add(f.index)
    while st:
        g = st.pop(); isl.append(g)
        for e in g.edges:
            for h in e.link_faces:
                if h.index not in seen: seen.add(h.index); st.append(h)
    islands.append(isl)
MINI = float(a[a.index('--minisland') + 1]) if '--minisland' in a else 0.005   # the crab's legs and shell plates are separate shells: keep them
drop = [isl for isl in islands if len(isl) < MINI * n0]
# --dropbox x0,x1,y0,y1,z0,z1 (metres, in the FINAL frame): drop whole islands lying entirely inside it. The raptor's Tripo build read
# the side view's far leg as a SECOND pair of lower legs (two free-standing shins behind the real ones); they are separate shells.
if '--dropbox' in a:
    bx = [float(t) for t in a[a.index('--dropbox') + 1].split(',')]
    keep_after = []
    for isl in islands:
        if isl in drop: continue
        P = np.array([[c for c in v.co] for f in isl for v in f.verts])
        keep_after.append((isl, P))
    DROPBOX = (bx, keep_after)
else:
    DROPBOX = None
bmesh.ops.delete(bm, geom=[f for isl in drop for f in isl], context='FACES')
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
bm.to_mesh(me); bm.free()
V = np.array([v.co[:] for v in me.vertices])
ext = V.max(0) - V.min(0)
ax = int(np.argmax(ext[:2]))            # long horizontal axis (x or y); glTF import is Z-up already
print('extent', ext.round(3), 'long axis', 'xy'[ax])
lo, hi = V[:, ax].min(), V[:, ax].max(); L0 = hi - lo
def endvol(sel):
    P = V[sel]; return float(np.ptp(P[:, 2]) * np.ptp(P[:, 1 - ax])) if len(P) > 3 else 0.0
v_lo = endvol(V[:, ax] < lo + 0.15 * L0); v_hi = endvol(V[:, ax] > hi - 0.15 * L0)
head_at_lo = v_lo > v_hi
if '--flip' in a: head_at_lo = not head_at_lo   # measured override: the volume test is a default, the look sheet is the check
# rotation so the head points to -Y
if ax == 1: yaw = 0.0 if head_at_lo else math.pi
else: yaw = (-math.pi / 2) if head_at_lo else (math.pi / 2)   # x-axis: head at -x -> rotate -90 so -x -> -y
if '--yaw' in a: yaw = math.radians(float(a[a.index('--yaw') + 1]))   # explicit, for bodies with no head/tail asymmetry (the crab)
R = Matrix.Rotation(yaw, 4, 'Z')
me.transform(R)
V = np.array([v.co[:] for v in me.vertices])
s = LEN / (float(max(np.ptp(V[:, 0]), np.ptp(V[:, 1]))) if '--maxext' in a else float(np.ptp(V[:, 1])))
me.transform(Matrix.Scale(s, 4))
V = np.array([v.co[:] for v in me.vertices])
# footprint: centre the LOW band (feet) in x/y, ground at min z
low = V[V[:, 2] < V[:, 2].min() + 0.1 * np.ptp(V[:, 2])]
off = Vector((-float((low[:, 0].min() + low[:, 0].max()) / 2), -float((low[:, 1].min() + low[:, 1].max()) / 2), -float(V[:, 2].min())))
me.transform(Matrix.Translation(off))
me.update()
if DROPBOX:
    bx, _ = DROPBOX
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    seen = set(); kill = []; n_isl = 0
    for f in bm.faces:
        if f.index in seen: continue
        st = [f]; isl = []; seen.add(f.index)
        while st:
            g = st.pop(); isl.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen: seen.add(h.index); st.append(h)
        P = np.array([v.co[:] for g in isl for v in g.verts])
        if (P[:, 0].min() > bx[0] and P[:, 0].max() < bx[1] and P[:, 1].min() > bx[2] and P[:, 1].max() < bx[3] and P[:, 2].min() > bx[4] and P[:, 2].max() < bx[5]):
            kill += isl; n_isl += 1
    bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(me); bm.free(); me.update()
    print('dropbox removed %d islands, %d faces' % (n_isl, len(kill)))
# decimate
n1 = len(me.polygons)
if n1 > FACES:
    md = ob.modifiers.new('dec', 'DECIMATE'); md.ratio = FACES / n1
    bpy.ops.object.modifier_apply(modifier='dec')
# NORMALS: the decimated Tripo shell carries flipped faces; a single-sided material culls them and the body shows HOLES
# (found on the maw's first paint canvas, EEVEE honours glTF single-sidedness; Workbench had hidden it). Recalculate outward per
# island, and ship the material DOUBLE-SIDED so any face the recalculation cannot orient (open teeth/spur shells) still draws.
bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
for m in me.materials:
    if m: m.use_backface_culling = False
V = np.array([v.co[:] for v in me.vertices])
info = dict(src=IN, faces_in=n0, islands=len(islands), islands_dropped=len(drop), faces_out=len(me.polygons), verts_out=len(me.vertices),
            yaw_deg=round(math.degrees(yaw), 1), head_end_volume=[round(v_lo, 4), round(v_hi, 4)], scale=round(s, 5),
            bbox_m=dict(x=[round(float(V[:, 0].min()), 4), round(float(V[:, 0].max()), 4)], y=[round(float(V[:, 1].min()), 4), round(float(V[:, 1].max()), 4)],
                        z=[round(float(V[:, 2].min()), 4), round(float(V[:, 2].max()), 4)]),
            materials=[m.name for m in me.materials])
ob.name = 'body'; me.name = 'body'
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=92)
json.dump(info, open(OUT.replace('.glb', '.json'), 'w'), indent=1)
print(json.dumps(info))
