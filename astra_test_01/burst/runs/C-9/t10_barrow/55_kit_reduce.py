"""C-9 T10-1b: shrink a kit prop to a triangle count that survives being instanced.

    blender --background --python 55_kit_reduce.py -- <in.glb> <out.glb> [tris] [texpx]

Same as 39_reduce.py, with a harder target and a different reason. There the props were
one-offs: nine assets at 24k triangles each. These six are SCATTER -- the whole point of
the kit is that the ground gets dozens of them -- so the budget is per instance multiplied
by however many the dressing pass wants, and 6-10k is the band the dispatch set.

Tripo returns ~1.5 M triangles and a 4K texture per prop. At 8k that is a 99.5% collapse,
which is where the risk lives: the spear shafts are about three pixels wide in the render
this gets measured in, and a collapse ratio chosen for a rock eats them. 56_kit_measure.py
is what says whether that happened -- silhouette IoU before against after, plus a thin-part
recall that looks only at the parts an opening removes. "It still looks like a spear in the
viewport" is not a measurement.
"""
import sys

import bmesh
import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
TRIS = int(argv[2]) if len(argv) > 2 else 8000
TEXPX = int(argv[3]) if len(argv) > 3 else 1024

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in meshes:
    o.data.calc_loop_triangles()
before = sum(len(o.data.loop_triangles) for o in meshes)

# WELD BEFORE DECIMATING OR THE DECIMATOR SHATTERS THE MESH.
#
# glTF stores one vertex per (position, normal, UV) combination, so an imported Tripo mesh
# is split along every UV seam: the two sides of a seam are topologically SEPARATE there,
# even though they are coincident in space. Collapse decimation cannot collapse an edge
# that does not exist, so at a ratio of 0.005 every UV island decimates alone and comes
# apart -- measured on the stump: ONE connected piece in, 301 pieces out, largest 100 of
# 7365 verts, 6129 boundary edges. The silhouette IoU was 0.978 the whole time, because a
# shattered mesh whose fragments have not moved casts exactly the same outline. That is why
# the island count is measured at all and why IoU alone would have passed this.
#
# Merging by distance first costs the seams a little UV stretch where a collapse now spans
# one. A seam that stretches is a texture artefact; a mesh in 301 pieces is cracks and
# wrong normals at every grazing angle, which is what these props are seen at.
merged = 0
for o in meshes:
    bm = bmesh.new()
    bm.from_mesh(o.data)
    n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    merged += n0 - len(bm.verts)
    bm.to_mesh(o.data)
    bm.free()
    o.data.calc_loop_triangles()
print("[reduce] welded %d coincident verts before decimating" % merged)

for o in meshes:
    n = len(o.data.loop_triangles)
    share = max(1, int(TRIS * n / max(before, 1)))
    if n > share:
        bpy.context.view_layer.objects.active = o
        m = o.modifiers.new("dec", "DECIMATE")
        m.decimate_type = "COLLAPSE"
        m.ratio = share / n
        bpy.ops.object.modifier_apply(modifier=m.name)

for im in bpy.data.images:
    if im.size[0] > TEXPX or im.size[1] > TEXPX:
        s = TEXPX / max(im.size)
        im.scale(max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s)))

after = 0
for o in bpy.context.scene.objects:
    if o.type == "MESH":
        o.data.calc_loop_triangles()
        after += len(o.data.loop_triangles)

bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_image_format="JPEG",
                          export_jpeg_quality=88, export_yup=True)
print("[reduce] %s  tris %d -> %d  textures <= %d px" % (src.split("/")[-1], before, after, TEXPX))
