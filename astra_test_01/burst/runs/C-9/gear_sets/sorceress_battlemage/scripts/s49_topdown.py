# R-C9-119: two orthographic WORKBENCH views of a GLB, from +Z (above) and -Z (below), for the open book's pages and covers.
import bpy, math, sys
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0]); sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x = 640; sc.render.resolution_y = 480; sc.world = bpy.data.worlds.new("w"); sc.world.color = (1, 1, 1)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 0.5
for k, z in enumerate((1, -1)):
    cam.location = Vector((0, 0.14, 2.0 * z)); cam.rotation_euler = (0 if z > 0 else math.pi, 0, 0)
    sc.render.filepath = a[1] + ".%d.png" % k; bpy.ops.render.render(write_still=True)
