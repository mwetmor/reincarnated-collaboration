# (views written as <out>.v0-3.png; stitched outside Blender, whose Python has no PIL)
# R-C9-98: a quick 4-view WORKBENCH preview of a GLB (texture colour, flat light), for a look before isolation.
#   blender -b -noaudio --python s20_preview.py -- <in.glb> <out.png> [--yaw 0]
import bpy, math, sys
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
ms = [o for o in sc.objects if o.type == 'MESH']
lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
for o in ms:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
ctr = (lo + hi) / 2; ext = max(hi - lo)
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x = 512; sc.render.resolution_y = 512
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("w"); sc.world.color = (1, 1, 1)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = ext * 1.1
tiles = []
for k, az in enumerate((0, 90, 180, 270)):
    t = math.radians(az)
    d = Vector((math.sin(t), -math.cos(t), 0))          # camera direction from the centre (az 0 = looking from -Y)
    cam.location = ctr + d * ext * 3
    cam.rotation_euler = (d * -1).to_track_quat('-Z', 'Y').to_euler()
    p = OUT + ".v%d.png" % k
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    tiles.append(p)
print("extent", tuple(round(x, 3) for x in (hi - lo)), "->", OUT)
