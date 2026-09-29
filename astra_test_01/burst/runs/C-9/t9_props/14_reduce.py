"""C-9 T9-1a: shrink each prop model to something the size it is drawn at.

    blender --background --python 14_reduce.py -- <in.glb> <out.glb> [tris] [texpx]

Tripo returns ~46 MB per prop: a 4K texture and a mesh built for a hero asset. These props
are 48 to 178 SCREEN PIXELS tall in the frame they exist for -- the raven is 17 -- so the
texture is carrying about thirty times the detail any pixel can show, and five of them
would put a quarter of a gigabyte into a review build whose whole point is that Matt can
open it.

Decimation is capped rather than aggressive, and the reason is the snag: it has bare twigs
a few millimetres thick, and a collapse ratio chosen for a solid trunk eats them. The
silhouette check after this step is what says whether that happened -- 15_check_reduce.py
compares before and after through the same camera and reports the IoU, because "it still
looks like a tree in the viewport" is not a measurement.

Textures go to JPEG: these meshes are closed and their maps carry no alpha, so the alpha
channel is bytes spent on nothing.
"""
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
src, dst = argv[0], argv[1]
TRIS = int(argv[2]) if len(argv) > 2 else 30000
TEXPX = int(argv[3]) if len(argv) > 3 else 1024

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
before = sum(len(o.data.loop_triangles) if o.data.loop_triangles else 0 for o in meshes)
if before == 0:
    for o in meshes:
        o.data.calc_loop_triangles()
    before = sum(len(o.data.loop_triangles) for o in meshes)

for o in meshes:
    o.data.calc_loop_triangles()
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
