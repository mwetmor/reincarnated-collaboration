# D2: fit an isolated gear piece to the base rig.
#
#   blender -b -noaudio --python scripts/08_fit_gear.py -- <piece.glb>
#     <base.glb> <out.glb> --mode skin|bone [--bone Head] [--split]
#     [--faces 24000] [--offset 0.004]
#
# SKIN: the garment is bound to the SAME 24 bones as the body, by taking each
# garment vertex's weights from the nearest point on the base mesh, barycentric
# across that triangle. A garment has no weights of its own -- it was cut out
# of a static Tripo build -- and the body beneath it is the only thing that
# knows how this bone system moves.
#
# BONE: a rigid piece is parented to one bone. With --split the piece's
# connected components are separated first and each goes to the nearer of two
# bones, which is how a pair of bracers finds its own forearm without anyone
# naming which lump is which.
#
# OFFSET pushes the garment out along its own normals. The pieces were cut from
# a build of the DRESSED body, and the body beneath is a DIFFERENT generation,
# so the two surfaces interpenetrate by a few millimetres before anything
# animates. Offsetting first means the poke-through measured afterwards is the
# animation's, not the generator's.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index('--') + 1:]
PIECE, BASE, OUT = a[0], a[1], a[2]
MODE = a[a.index("--mode") + 1] if "--mode" in a else "skin"
BONE = a[a.index("--bone") + 1] if "--bone" in a else "Head"
BONES2 = a[a.index("--bones") + 1].split(",") if "--bones" in a else None
SPLIT = "--split" in a
FACES = int(a[a.index("--faces") + 1]) if "--faces" in a else 24000
OFFSET = float(a[a.index("--offset") + 1]) if "--offset" in a else 0.004

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
barm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups)
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
body.data.calc_loop_triangles()
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co)
BV = co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
BT = np.array([list(t.vertices) for t in body.data.loop_triangles])
gnames = [g.name for g in body.vertex_groups]
Wt = np.zeros((len(BV), len(gnames)), np.float32)
for vi, v in enumerate(body.data.vertices):
    for gel in v.groups:
        Wt[vi, gel.group] = gel.weight
tree = BVHTree.FromPolygons([Vector(p) for p in BV.tolist()],
                            [list(map(int, f)) for f in BT])
print("base: %d verts, %d tris, %d groups" % (len(BV), len(BT), len(gnames)))

bpy.ops.import_scene.gltf(filepath=PIECE)
new = [o for o in sc.objects if o.type == 'MESH' and o is not body]
bpy.ops.object.select_all(action='DESELECT')
for o in new:
    o.select_set(True)
bpy.context.view_layer.objects.active = new[0]
if len(new) > 1:
    bpy.ops.object.join()
pc = bpy.context.view_layer.objects.active
pc.name = os.path.basename(OUT).replace(".glb", "")
# A SKINNED MESH MUST CARRY NO OBJECT TRANSFORM OF ITS OWN. glTF skinning is
# joint_world x inverseBind x vertex, and Blender's exporter builds inverseBind
# from the rest pose assuming the mesh sits in the armature's space. A piece
# imported from its own GLB arrives with its own object matrix, and exporting
# it skinned bakes that matrix in twice: the helmet came back collapsed to a
# 2 mm speck at the origin, in the FILE, not on import. Bake the transform into
# the mesh data first, so the object matrix is identity.
bpy.ops.object.select_all(action='DESELECT')
pc.select_set(True); bpy.context.view_layer.objects.active = pc
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
n0 = len(pc.data.polygons)
if n0 > FACES:
    m = pc.modifiers.new('dec', 'DECIMATE'); m.ratio = FACES / n0
    bpy.ops.object.modifier_apply(modifier='dec')
print("piece: %d -> %d faces" % (n0, len(pc.data.polygons)))

# offset outward along the piece's own normals, then clear any残 penetration
pc.data.calc_loop_triangles()
co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("co", co)
PV = co.reshape(-1, 3)
nm = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("normal", nm)
NV = nm.reshape(-1, 3)
PV = PV + NV * OFFSET
pushed = 0
for i, p in enumerate(PV):
    hit = tree.find_nearest(Vector(p.tolist()))
    if hit[0] is None:
        continue
    v = Vector(p.tolist()) - hit[0]
    if v.dot(hit[1]) < 0:                     # inside the body: push it out
        PV[i] = np.array((hit[0] + hit[1] * OFFSET).to_tuple()); pushed += 1
pc.data.vertices.foreach_set("co", PV.ravel()); pc.data.update()
print("offset %.1f mm; %d vertices were inside the body and were pushed out"
      % (1000 * OFFSET, pushed))

if MODE == "skin":
    for gn in gnames:
        pc.vertex_groups.new(name=gn)
    A, B, C = BV[BT[:, 0]], BV[BT[:, 1]], BV[BT[:, 2]]
    assigned = 0
    for i, p in enumerate(PV):
        hit = tree.find_nearest(Vector(p.tolist()))
        if hit[0] is None:
            continue
        ti = hit[2]
        t = BT[ti]
        q = np.array(hit[0].to_tuple())
        a0, b0, c0 = BV[t[0]], BV[t[1]], BV[t[2]]
        n = np.cross(b0 - a0, c0 - a0)
        A2 = np.dot(n, n) or 1e-12
        w0 = np.dot(np.cross(b0 - q, c0 - q), n) / A2
        w1 = np.dot(np.cross(c0 - q, a0 - q), n) / A2
        w2 = 1.0 - w0 - w1
        w = np.clip([w0, w1, w2], 0, 1)
        w = w / max(w.sum(), 1e-9)
        wv = w[0] * Wt[t[0]] + w[1] * Wt[t[1]] + w[2] * Wt[t[2]]
        s = wv.sum()
        if s <= 0:
            continue
        wv = wv / s
        for gi in np.where(wv > 0.002)[0]:
            pc.vertex_groups[gnames[gi]].add([i], float(wv[gi]), 'REPLACE')
        assigned += 1
    print("skinned: weights transferred to %d of %d verts" % (assigned, len(PV)))
    pc.parent = barm
    pc.matrix_parent_inverse = Matrix.Identity(4)
    mod = pc.modifiers.new('arm', 'ARMATURE'); mod.object = barm
else:
    if SPLIT and BONES2:
        bpy.ops.object.select_all(action='DESELECT')
        pc.select_set(True); bpy.context.view_layer.objects.active = pc
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE'); bpy.ops.object.mode_set(mode='OBJECT')
        parts = [o for o in sc.objects if o.type == 'MESH' and o is not body]
        for o in parts:
            bpy.ops.object.select_all(action='DESELECT')
            o.select_set(True); bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        print("split into %d parts" % len(parts))
    else:
        parts = [pc]
    for o in parts:
        cov = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", cov)
        ctr = (cov.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
               + np.array(o.matrix_world.translation)).mean(0)
        cands = BONES2 or [BONE]
        best = min(cands, key=lambda bn: np.linalg.norm(
            ctr - np.array(barm.matrix_world @ barm.pose.bones[bn].head)))
        g = o.vertex_groups.new(name=best)
        g.add(list(range(len(o.data.vertices))), 1.0, 'REPLACE')
        o.parent = barm
        o.matrix_parent_inverse = Matrix.Identity(4)
        m = o.modifiers.new('arm', 'ARMATURE'); m.object = barm
        print("   %-18s -> bone %s" % (o.name, best))
        o.name = os.path.basename(OUT).replace(".glb", "") + ("_%s" % best)

bpy.ops.object.select_all(action='DESELECT')
for o in [o for o in sc.objects if o.type == 'MESH' and o is not body]:
    o.select_set(True)
barm.select_set(True)
bpy.context.view_layer.objects.active = barm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=False, export_image_format='AUTO')
json.dump(dict(piece=os.path.basename(PIECE), mode=MODE, faces=len(pc.data.polygons),
               offset_m=OFFSET, pushed_out=pushed),
          open(OUT.replace(".glb", ".json"), "w"), indent=1)
print("wrote %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
