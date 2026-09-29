# C-9 T5: look at the baked texture on the model.
#
#   blender -b -noaudio --python scripts/07_view.py -- <blend> <texture.png>
#          <outdir> [--elev 52.95] [--n 16] [--subject body|head] [--res 384]
#
# Per R-C9-68 the game camera sees this creature at 52.95 deg, so that is the
# elevation the texture is judged at and 19.77 is the secondary check.
#
# Unlit, like every other render in this pipeline: the question is what the
# PAINT does, and a lighting rig would put its own gradient over the answer.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
BLEND, TEX, OUTDIR = a[0], a[1], a[2]
ELEV = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
N = int(a[a.index("--n") + 1]) if "--n" in a else 16
SUBJ = a[a.index("--subject") + 1] if "--subject" in a else "body"
RES = int(a[a.index("--res") + 1]) if "--res" in a else 384
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import t2lib_ref as T

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == 'MESH']
# swap the base-colour image for the baked one, then unlit it
img = bpy.data.images.load(os.path.abspath(TEX))
swapped = 0
for o in objs:
    for s in o.material_slots:
        m = s.material
        if not m or not m.node_tree:
            continue
        for nd in m.node_tree.nodes:
            if nd.type == 'TEX_IMAGE':
                nd.image = img
                nd.image.colorspace_settings.name = 'sRGB'
                swapped += 1
print("swapped %d image node(s) to %s" % (swapped, os.path.basename(TEX)))
assert swapped, "no image texture node found -- nothing would show the bake"
T.unlit(objs)

P = []
for o in objs:
    Mw = np.array(o.matrix_world.to_3x3()).T
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    P.append(co.reshape(-1, 3) @ Mw + np.array(o.matrix_world.translation))
P = np.vstack(P)
if SUBJ == "head":
    zmin, zmax = P[:, 2].min(), P[:, 2].max()
    ymax, ymin = P[:, 1].max(), P[:, 1].min()
    Q = P[(P[:, 2] > zmin + 0.80 * (zmax - zmin)) & (P[:, 1] > ymax - 0.45 * (ymax - ymin))]
else:
    Q = P

cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
eng = [i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
el = math.radians(ELEV)
base = Vector((0.0, 0.0, float(P[:, 2].max() + P[:, 2].min()) * 0.5))
os.makedirs(OUTDIR, exist_ok=True)
worst = 0.0
for k in range(N):
    az = math.radians(360.0 * k / N)
    d = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = base + d * 20.0
    cam.rotation_euler = (base - cam.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    R = np.array(cam.matrix_world.to_3x3())
    right, up = R[:, 0], R[:, 1]
    x, y = Q @ right, Q @ up
    cx, cy = 0.5 * (x.max() + x.min()), 0.5 * (y.max() + y.min())
    aim = base + Vector(right.tolist()) * (cx - base.dot(Vector(right.tolist()))) \
               + Vector(up.tolist()) * (cy - base.dot(Vector(up.tolist())))
    cam.location = aim + d * 20.0
    cam.rotation_euler = (aim - cam.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    span = max(x.max() - x.min(), y.max() - y.min())
    cam.data.ortho_scale = span * 1.10
    worst = max(worst, span)
    sc.render.filepath = os.path.join(OUTDIR, "v_%02d.png" % k)
    bpy.ops.render.render(write_still=True)
print("%d frames at elev %.2f, subject %s, into %s" % (N, ELEV, SUBJ, OUTDIR))
