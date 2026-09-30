# The assembled character at rest, every piece on, lit -- front / side / back / 3-quarter.
#   blender -b -noaudio --python scripts/s9_look_all.py -- <exportdir> <out.png> [--close]
import bpy, glob, math, os, sys
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
D, OUT = a[0], a[1]
CLOSE = '--close' in a
bpy.ops.wm.read_factory_settings(use_empty=True)
files = [os.path.join(D, "so-body.glb")] + sorted(p for p in glob.glob(os.path.join(D, "*.glb")) if not p.endswith("so-body.glb"))
for p in files:
    bpy.ops.import_scene.gltf(filepath=p)
sc = bpy.context.scene
for o in list(sc.objects):
    if o.type == 'MESH' and not o.vertex_groups:
        bpy.data.objects.remove(o, do_unlink=True)
# REST, genuinely. Clearing the active action is not enough: the body carries its clips as
# NLA tracks, and those still evaluate -- the first look rendered her in a clip's pose while
# every piece sat at rest on its own armature, and read as a misfit that was not there.
for o in sc.objects:
    if o.type == 'ARMATURE':
        if o.animation_data:
            o.animation_data.action = None
            o.animation_data.use_nla = False
        for pb in o.pose.bones:
            pb.matrix_basis.identity()
bpy.context.view_layer.update()
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.world = bpy.data.worlds.new("w"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.86, 0.88, 0.90, 1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.9
sun = bpy.data.objects.new("s", bpy.data.lights.new("s", 'SUN')); sc.collection.objects.link(sun)
sun.data.energy = 3.0; sun.rotation_euler = (math.radians(35), 0, math.radians(-35))
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
ctr = Vector((0, 0, 1.52 if CLOSE else 0.90)); cam.data.ortho_scale = 0.55 if CLOSE else 2.05
sc.render.resolution_x, sc.render.resolution_y = 420, 520
tiles = []
for i, az in enumerate((0, 45, 90, 180)):
    r = math.radians(az); el = math.radians(12)
    cam.location = ctr + Vector((math.sin(r) * math.cos(el), -math.cos(r) * math.cos(el), math.sin(el))) * 10
    cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
    f = OUT.replace(".png", "_%d.png" % i); sc.render.filepath = f
    bpy.ops.render.render(write_still=True); tiles.append(f)
print("TILES", ",".join(tiles))
