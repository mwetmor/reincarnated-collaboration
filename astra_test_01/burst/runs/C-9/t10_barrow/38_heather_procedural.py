"""C-9 T10: heather tussocks as GEOMETRY, not as bushes and not as alpha cards.

    blender --background --python 38_heather_procedural.py -- <out.glb> [heather.png] [seed]

The 19 heather clumps were standing in with the juniper model, which is a bush where the
concept has low ground cover. Two ways to fix it: a sheet plus a Tripo build, or code.
Code, because ground cover is repetitive small structure and that is the thing code does
better than reconstruction -- the same argument that made the birch procedural, one scale
down.

NO ALPHA CARDS. Crossed billboards are the usual cheap answer and they would break rule 1
(real sculpted form) and rule 4 (one ink line around a real silhouette): an alpha-cut card
has an outline the renderer's depth-and-normal edge pass cannot find. These are real stems
-- tapered tubes, a few hundred triangles a clump -- so they are lit, they cast, and they
are outlined like everything else in the scene.

Sized from the object list: the 19 clumps measure 0.39 to 2.19 m with a MEDIAN of 0.81 m,
and the tall end of that is almost certainly juniper the classifier put in the wrong bin.
The model is built at the median and scaled per instance.
"""
import math, random, sys
import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
TEX = argv[1] if len(argv) > 1 and argv[1] != "-" else None
SEED = int(argv[2]) if len(argv) > 2 else 5

HEIGHT_M = 0.81          # the measured median clump
SPREAD = 0.62            # how far the stems lean out, as a fraction of height
STEMS = 22
LEVELS = 2
BASE_R = 0.008
RINGS = 4

random.seed(SEED)
bpy.ops.wm.read_factory_settings(use_empty=True)
verts, faces, uvs = [], [], []


def tube(p0, p1, r0, r1, n, v0, v1):
    d = p1 - p0
    if d.length < 1e-6:
        return
    ax = d.normalized()
    ref = Vector((0, 0, 1)) if abs(ax.z) < 0.95 else Vector((1, 0, 0))
    x = ax.cross(ref).normalized(); y = ax.cross(x).normalized()
    b = len(verts)
    for (p, r, vv) in ((p0, r0, v0), (p1, r1, v1)):
        for i in range(n + 1):
            a = 2 * math.pi * i / n
            verts.append(p + (x * math.cos(a) + y * math.sin(a)) * r)
            uvs.append((i / n, vv))
    for i in range(n):
        faces.append((b + i, b + i + 1, b + n + 2 + i, b + n + 1 + i))


def grow(p, d, length, radius, level, v):
    steps = 2
    cur, dirv = p, d.copy()
    for s in range(steps):
        dirv = (dirv + Vector((random.uniform(-.2, .2), random.uniform(-.2, .2),
                               random.uniform(-.12, .05)))).normalized()
        nxt = cur + dirv * (length / steps)
        tube(cur, nxt, radius * (1 - s * .3), radius * (1 - (s + 1) * .3), RINGS - level,
             v + s * .8, v + (s + 1) * .8)
        cur = nxt
    if level >= LEVELS:
        return
    for _ in range(random.randint(1, 2)):
        ref = dirv.cross(Vector((0, 0, 1)))
        if ref.length < 1e-5:
            ref = dirv.cross(Vector((1, 0, 0)))
        nd = (Matrix.Rotation(random.uniform(0, 2 * math.pi), 3, dirv)
              @ (Matrix.Rotation(random.uniform(.3, .8), 3, ref.normalized()) @ dirv)).normalized()
        grow(cur, nd, length * random.uniform(.5, .7), radius * .6, level + 1, v + steps * .8)


for i in range(STEMS):
    a = 2 * math.pi * i / STEMS + random.uniform(-.25, .25)
    rr = random.uniform(0, 0.10)
    base = Vector((math.cos(a) * rr, math.sin(a) * rr, 0))
    lean = random.uniform(0.35, SPREAD)
    d0 = Vector((math.cos(a) * lean, math.sin(a) * lean, 1.0)).normalized()
    grow(base, d0, HEIGHT_M * random.uniform(0.45, 0.62), BASE_R * random.uniform(.8, 1.2), 1, 0.0)

me = bpy.data.meshes.new("heather")
me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
uvl = me.uv_layers.new(name="UVMap")
for poly in me.polygons:
    for li in poly.loop_indices:
        uvl.data[li].uv = uvs[me.loops[li].vertex_index]
ob = bpy.data.objects.new("heather", me)
bpy.context.collection.objects.link(ob)
bpy.context.view_layer.update()
bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
zs = [p.z for p in bb]; xs = [p.x for p in bb]; ys = [p.y for p in bb]
h = max(zs) - min(zs); w = max(max(xs) - min(xs), max(ys) - min(ys))
s = HEIGHT_M / max(h, 1e-6)
ob.scale = (s, s, s)
print("[heather] grown %.2f m tall x %.2f m across -> scaled x%.3f to %.2f m; %d verts, %d faces"
      % (h, w, s, HEIGHT_M, len(verts), len(faces)))

mat = bpy.data.materials.new("heather"); mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.94
if TEX:
    t = mat.node_tree.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(TEX); t.extension = "REPEAT"
    mat.node_tree.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
else:
    bsdf.inputs["Base Color"].default_value = (0.42, 0.31, 0.17, 1.0)
ob.data.materials.append(mat)
bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True)
bpy.context.view_layer.objects.active = ob
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_image_format="JPEG",
                          export_jpeg_quality=88, export_yup=True, use_selection=True)
print("[heather] -> %s" % OUT)
