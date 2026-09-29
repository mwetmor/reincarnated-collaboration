"""C-9 T10: the dead birch, built as geometry instead of reconstructed from pictures.

    blender --background --python 35_birch_procedural.py -- <out.glb> [bark.png] [seed]

WHY THIS EXISTS. The T10P-D sheet scored **0.67 and 0.68** mirror IoU across its two
variants, with self-symmetry 0.20-0.28 -- by far the worst of the nine assets, and worse
than the T9 snag that prompted the fallback in the first place. A bare birch is the case
a photogrammetric reconstructor is least able to do: its silhouette is mostly gaps, and
its twigs are thinner than the voxel grid that has to contain them. Four views of one do
not constrain a solid, so Tripo gets a lump where the branches are and nothing where the
twigs are.

Geometry does not have that problem. A branch skeleton is a few hundred tapered tubes, each
exactly as thin as it should be, and the silhouette comes out right because it was never
inferred. The surface is still ours: the bark tile is painted by Astra in the same hand as
everything else, wrapped cylindrically.

THE ADDON IS NOT USED. Sapling is the obvious tool and it is a Blender add-on that may or
may not be enabled in a given install, which makes it a dependency that fails at the point
of use and not at the point of writing. This grows the skeleton directly: ~90 lines, no
addon, and every parameter is visible.

PARAMETERS ARE MEASURED, not chosen: 3.36 m tall and 1.38 m across is the concept's own
birch, read off the painting through K = 140.86 px/m (24_identity_plates.py). The lean is
the one thing the brief asks for that the measurement cannot give, so it is a stated
constant like the heightfield's four.
"""
import math
import random
import sys

import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
BARK = argv[1] if len(argv) > 1 and argv[1] != "-" else None
SEED = int(argv[2]) if len(argv) > 2 else 3

HEIGHT_M = 3.36          # measured off the concept
SPREAD_M = 1.38          # measured off the concept
TRUNKS = 3               # the concept shows a multi-stemmed mountain birch
LEAN = math.radians(14)  # stated: years of one wind
LEVELS = 4
BASE_RADIUS = 0.055
TAPER = 0.62             # radius multiplier per level
SPLIT = (2, 3)           # children per branch
RINGS = 6                # cross-section resolution at the trunk, dropping with level

random.seed(SEED)
bpy.ops.wm.read_factory_settings(use_empty=True)

verts, faces, uvs = [], [], []


def tube(p0, p1, r0, r1, n, v0, v1):
    """One tapered segment, as a ring-to-ring band. UV v runs along the branch so the bark
    tile wraps around and repeats up -- which is the axis the seam test says bark_a is
    clean on (0.81 horizontally, cleaner than its own interior)."""
    d = (p1 - p0)
    if d.length < 1e-6:
        return
    up = Vector((0, 0, 1))
    axis = d.normalized()
    ref = up if abs(axis.dot(up)) < 0.95 else Vector((1, 0, 0))
    x = axis.cross(ref).normalized()
    y = axis.cross(x).normalized()
    base = len(verts)
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        verts.append(p0 + (x * c + y * s) * r0)
        uvs.append((i / n, v0))
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        verts.append(p1 + (x * c + y * s) * r1)
        uvs.append((i / n, v1))
    for i in range(n):
        faces.append((base + i, base + i + 1, base + n + 2 + i, base + n + 1 + i))


def grow(p, direction, length, radius, level, v):
    n = max(3, RINGS - level)
    steps = max(2, 4 - level)
    cur = p
    dirv = direction.copy()
    for s in range(steps):
        # the lean accumulates: the whole tree is pushed the same way
        dirv = (dirv + Vector((math.sin(LEAN), 0, 0)) * 0.10).normalized()
        dirv = (dirv + Vector((random.uniform(-.10, .10), random.uniform(-.10, .10),
                               random.uniform(0.02, .16)))).normalized()
        nxt = cur + dirv * (length / steps)
        r0 = radius * (1 - s / (steps + 1.0) * 0.35)
        r1 = radius * (1 - (s + 1) / (steps + 1.0) * 0.35)
        tube(cur, nxt, r0, r1, n, v + s * 0.6, v + (s + 1) * 0.6)
        cur = nxt
    if level >= LEVELS:
        return
    for _ in range(random.randint(*SPLIT)):
        # NARROW. The first pass used 28-62 deg and grew a tree 4.27 m across
        # against the concept's measured 1.38 m -- a birch is a fountain, not a
        # shrub, and the angle is what says which. Checked by the grown aspect
        # ratio printed below, not by eye.
        ang = random.uniform(math.radians(14), math.radians(34))
        azi = random.uniform(0, 2 * math.pi)
        ref = dirv.cross(Vector((0, 0, 1)))
        if ref.length < 1e-5:
            ref = dirv.cross(Vector((1, 0, 0)))
        ref.normalize()
        nd = (Matrix.Rotation(azi, 3, dirv) @ (Matrix.Rotation(ang, 3, ref) @ dirv)).normalized()
        grow(cur, nd, length * random.uniform(0.52, 0.72), radius * TAPER, level + 1,
             v + steps * 0.6)


for t in range(TRUNKS):
    a = 2 * math.pi * t / TRUNKS + random.uniform(-0.3, 0.3)
    off = Vector((math.cos(a), math.sin(a), 0)) * random.uniform(0.02, 0.09)
    d0 = (Vector((0, 0, 1)) + Vector((math.sin(LEAN), 0, 0)) * 0.55
          + Vector((math.cos(a), math.sin(a), 0)) * 0.10).normalized()
    grow(off, d0, HEIGHT_M * random.uniform(0.40, 0.50),
         BASE_RADIUS * random.uniform(0.82, 1.0), 1, 0.0)

me = bpy.data.meshes.new("birch")
me.from_pydata([tuple(v) for v in verts], [], faces)
me.update()
uvl = me.uv_layers.new(name="UVMap")
for poly in me.polygons:
    for li in poly.loop_indices:
        uvl.data[li].uv = uvs[me.loops[li].vertex_index]
ob = bpy.data.objects.new("birch", me)
bpy.context.collection.objects.link(ob)

# TRUE SCALE, forced from the measurement rather than trusted from the growth parameters:
# the recursion's randomness makes the final height an outcome, not an input.
bpy.context.view_layer.update()
bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
zs = [p.z for p in bb]
xs = [p.x for p in bb]
ys = [p.y for p in bb]
cur_h = max(zs) - min(zs)
cur_w = max(max(xs) - min(xs), max(ys) - min(ys))
s = HEIGHT_M / max(cur_h, 1e-6)
ob.scale = (s, s, s)
bpy.context.view_layer.update()
print("[birch] grown %.2f m x %.2f m -> scaled x%.3f to %.2f m; %d verts, %d faces"
      % (cur_h, cur_w, s, HEIGHT_M, len(verts), len(faces)))

mat = bpy.data.materials.new("bark")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.92
if BARK:
    img = bpy.data.images.load(BARK)
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.extension = "REPEAT"
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
else:
    bsdf.inputs["Base Color"].default_value = (0.86, 0.85, 0.80, 1.0)
ob.data.materials.append(mat)

bpy.ops.object.select_all(action="DESELECT")
ob.select_set(True)
bpy.context.view_layer.objects.active = ob
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_image_format="JPEG",
                          export_jpeg_quality=88, export_yup=True, use_selection=True)
print("[birch] -> %s" % OUT)
