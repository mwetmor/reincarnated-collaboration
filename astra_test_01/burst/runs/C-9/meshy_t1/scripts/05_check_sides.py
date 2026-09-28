# C-9 meshy_t1: answer gandalf's two warnings with a measurement, not a look.
#   blender -b -noaudio --python scripts/05_check_sides.py -- <rigged.glb> <outdir>
# Renders the bind pose at the eight game azimuths after the SAME facing
# correction the pipeline uses, so the images can be compared against the
# approved painted stills.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
a = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = a[0], a[1]
FACE_YAW = float(a[2]) if len(a) > 2 else 0.0
AZI = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}
FRAME, BODY_PX, SOLE_Y, ELEV = 512, 198.33333333333334, 398.0, 19.77
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
objs = [o for o in sc.objects if o.type == 'MESH'
        and any(m.type == 'ARMATURE' and m.object == arm for m in o.modifiers)]
for o in list(sc.objects):
    if o.type == 'MESH' and o not in objs:
        bpy.data.objects.remove(o, do_unlink=True)
rot = Matrix.Rotation(math.radians(-FACE_YAW), 4, 'Z')
for o in list(sc.objects):
    if o.parent is None:
        o.matrix_world = rot @ o.matrix_world
for o in objs:
    for slot in o.material_slots:
        m = slot.material
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        em = nt.nodes.new('ShaderNodeEmission')
        if bsdf and bsdf.inputs['Base Color'].links:
            nt.links.new(bsdf.inputs['Base Color'].links[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], outn.inputs['Surface'])
lo = 1e9
for o in objs:
    for v in o.data.vertices:
        lo = min(lo, (o.matrix_world @ v.co).z)
hi = -1e9
for o in objs:
    for v in o.data.vertices:
        hi = max(hi, (o.matrix_world @ v.co).z)
px = BODY_PX / (hi - lo)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = FRAME / px
sc.render.resolution_x = FRAME; sc.render.resolution_y = FRAME
sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'
el = math.radians(ELEV)
aim_z = 0.0
for it in range(3):
    A = math.radians(AZI["E"])
    aim = Vector((0, 0, aim_z))
    pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                        math.sin(el))) * 20.0
    cam.location = pos; cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, "_cal.png"); bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(sc.render.filepath)
    arr = np.array(im.pixels[:]).reshape(FRAME, FRAME, 4)[::-1]; bpy.data.images.remove(im)
    ys = np.where((arr[..., 3] > 0.03).any(axis=1))[0]
    if not len(ys):
        break
    aim_z += (SOLE_Y - float(ys.max())) / (px * math.cos(el))
for d, az in AZI.items():
    A = math.radians(az)
    aim = Vector((0, 0, aim_z))
    pos = aim + Vector((math.sin(A) * math.cos(el), math.cos(A) * math.cos(el),
                        math.sin(el))) * 20.0
    cam.location = pos; cam.rotation_euler = (aim - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, "bind_%s.png" % d)
    bpy.ops.render.render(write_still=True)
os.remove(os.path.join(OUT, "_cal.png"))
json.dump(dict(px_per_m=px, aim_z=aim_z, height=hi - lo, face_yaw=FACE_YAW),
          open(os.path.join(OUT, "bind_meta.json"), "w"), indent=1)
print("bind turnaround written, px/m %.3f height %.4f" % (px, hi - lo))
