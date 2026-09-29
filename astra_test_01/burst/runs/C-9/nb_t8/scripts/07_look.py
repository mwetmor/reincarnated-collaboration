# T8: unlit ortho looks at a GLB with a given texture swapped in.
#   blender -b -noaudio --python scripts/07_look.py -- <glb> <tex.png> <outdir>
#          <facings> [--elev 52.95] [--res 512] [--zoom arm|full]
#
# Facing convention, VERIFIED not inherited (scripts/04_surface.py): the model
# faces -Y, his right is -X. Camera for facing F sits opposite F, so facing S
# shows his front and facing NW shows his back-left -- which is where the
# mirrored tattoo was.
import bpy, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, TEX, OUT, FAC_S = a[0], a[1], a[2], a[3]
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 512
ZOOM = a[a.index("--zoom") + 1] if "--zoom" in a else "full"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
img = bpy.data.images.load(os.path.abspath(TEX)) if TEX != "-" else None
n_sw = 0
for o in objs:
    for s in o.material_slots:
        m = s.material
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if img:
            for n in nt.nodes:
                if n.type == 'TEX_IMAGE':
                    n.image = img; n.image.colorspace_settings.name = 'sRGB'; n_sw += 1
        out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        em = nt.nodes.new('ShaderNodeEmission')
        L = b.inputs['Base Color'].links if b else []
        if L:
            nt.links.new(L[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
print("swapped %d texture node(s)" % n_sw)
V = []
for o in objs:
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
             + np.array(o.matrix_world.translation))
V = np.vstack(V); lo, hi = V.min(0), V.max(0); H = hi[2] - lo[2]
ctr = Vector(((lo + hi) / 2).tolist())
if ZOOM == "arm":        # the upper-arm band, where the tattoo lives
    ctr = Vector((0.0, 0.0, float(lo[2] + 0.735 * H)))
    span = 0.45 * H
else:
    span = H * 1.12
eng = [e.identifier for e in
       bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'; cam.data.ortho_scale = span
FACD = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
# --yaw compensates a model delivered rotated: the Tripo build faces +X where
# this convention expects -Y, so every camera azimuth shifts by the same 90.
YAW = float(a[a.index("--yaw") + 1]) if "--yaw" in a else 0.0
el = math.radians(EL)
os.makedirs(OUT, exist_ok=True)
for f in FAC_S.split(","):
    az = math.radians((360 - FACD[f] + YAW) % 360)
    d = 10 * H
    pos = ctr + Vector((d * math.sin(az) * math.cos(el),
                        -d * math.cos(az) * math.cos(el), d * math.sin(el)))
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, "v_%s.png" % f)
    bpy.ops.render.render(write_still=True)
print("rendered %s at elev %.2f into %s" % (FAC_S, EL, OUT))
