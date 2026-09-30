# D2: does the helmet dome actually show, and does hair poke through it?
#
#   blender -b -noaudio --python scripts/12_helmet_measure.py -- <clip.glb>
#     <out.json> [--key 1] [--elev 52.95] [--res 512]
#
# Measured with a FLAT ID PASS, not by eye: the helmet renders pure red, the
# body pure green, and the two are composited by the renderer's own depth. Then
# inside the helmet's own silhouette:
#
#   dome visible   = red pixels / helmet silhouette pixels
#   hair poking    = green pixels inside that silhouette
#
# Run with --key 0 and --key 1 to see what the shape key buys. "It looks like a
# helmet now" is not a number, and the defect it is fixing looked like a
# headband, which also looked like something.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("12_helmet_measure.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
CLIP, OUTJ = a[0], a[1]
KEY = float(a[a.index("--key") + 1]) if "--key" in a else 1.0
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 512
ROOT = os.path.dirname(HERE)
TMP = os.path.join(ROOT, "work", "_idpass")
os.makedirs(TMP, exist_ok=True)


def flat(objs, rgb):
    for o in objs:
        o.data.materials.clear()
        m = bpy.data.materials.new("flat"); m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        em = nt.nodes.new('ShaderNodeEmission')
        em.inputs['Color'].default_value = (*rgb, 1.0)
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
        o.data.materials.append(m)


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
BV, BT, names, W, tree = G.body_sampler(body[0])
before = set(sc.objects)
pc = G.import_piece(os.path.join(ROOT, "pieces", "helmet.glb"), before)
G.decimate(pc, 12000)
made = G.bone_bind(pc, arm, ["Head"], False)
for o, _ in made:
    G.align_space(o, body[0])
mv, ca, key = G.helmet_on_key(body[0], made[0][0], arm)
key.value = KEY
print("shape key at %.1f: %d of %d head vertices moved" % (KEY, mv, ca))
flat([o for o, _ in made], (1.0, 0.0, 0.0))
flat(body, (0.0, 1.0, 0.0))
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
hco = np.empty(len(made[0][0].data.vertices) * 3)
made[0][0].data.vertices.foreach_get("co", hco)
HW = (hco.reshape(-1, 3) @ np.array(made[0][0].matrix_world.to_3x3()).T
      + np.array(made[0][0].matrix_world.translation))
ctr = Vector(((HW.min(0) + HW.max(0)) / 2).tolist())
span = float(np.max(HW.max(0) - HW.min(0)))
cam.data.ortho_scale = span * 2.0
FAC = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
el = math.radians(EL)
rows = {}
for f in FAC:
    az = math.radians((360 - FAC[f]) % 360)
    pos = ctr + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                        math.sin(el))) * 10.0
    cam.location = pos
    cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
    # 1: the helmet alone, for its silhouette
    for o in body:
        o.hide_render = True
    sc.render.filepath = os.path.join(TMP, "h_%s.png" % f)
    bpy.ops.render.render(write_still=True)
    for o in body:
        o.hide_render = False
    sc.render.filepath = os.path.join(TMP, "c_%s.png" % f)
    bpy.ops.render.render(write_still=True)
    rows[f] = dict(pending=True)
json.dump(dict(key=KEY, moved=mv, candidates=ca, frames=TMP,
               facings=list(FAC)), open(OUTJ, "w"), indent=1)
print("rendered ID passes into %s; count them with 13_count_id.py" % TMP)
