# Why do N and S read bigger? Measure the screen silhouette per facing.
#
#   blender -b -noaudio --python scripts/19_silhouette.py -- <base.glb> <tex>
#     <out.json> [--gear "<spec>"] [--elev 52.95] [--res 512]
#
# Height, WIDTH and AREA, because the complaint is bulk and height alone was
# already measured flat (154-157 px across facings by the scene). A broadside
# shoulder span, a fur mantle and a shield all present their widest face on the
# body's own axes -- so if the cause is width, N and S will show it and E/W
# will not.
#
# ONE camera distance and ONE ortho scale for every facing, so a difference in
# the numbers is a difference in the figure and not in the framing.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("19_silhouette.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BASE, TEX, OUTJ = a[0], a[1], a[2]
SPEC = a[a.index("--gear") + 1] if "--gear" in a else ""
EL = float(a[a.index("--elev") + 1]) if "--elev" in a else 52.95
RES = int(a[a.index("--res") + 1]) if "--res" in a else 512
ROOT = os.path.dirname(HERE)
TMP = os.path.join(ROOT, "work", "_sil")
os.makedirs(TMP, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BASE)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0])
worn = []
CARRY = None
cp = os.path.join(ROOT, "work", "carry_pose.json")
SPECS = dict(axe=dict(axis_world=(0, 0, 1), face_world=(0, -1, 0)),
             shield=dict(axis_world=(0.50, -0.87, 0.0), face_world=(0, 0, 1),
                         offset_world=(0.02, -0.06, 0.0), anchor="normal"))
for item in [x for x in SPEC.split(",") if x]:
    parts = item.split(":")
    nm, mode = parts[0], parts[1]
    bones = parts[2].split("|") if len(parts) > 2 and parts[2] else []
    split = len(parts) > 3 and parts[3] == "split"
    faces = dict(helmet=12000, bracers=12000, byrnie=26000, mantle=24000,
                 axe=9000, shield=9000).get(nm, 16000)
    offs = dict(helmet=0.0, bracers=0.002, byrnie=0.005, mantle=0.008,
                axe=0.0, shield=0.0).get(nm, 0.004)
    if nm == "shield" and os.path.exists(cp):
        CARRY = json.load(open(cp))
        for bn, flat in CARRY.items():
            arm.pose.bones[bn].matrix_basis = Matrix(
                [flat[i * 4:(i + 1) * 4] for i in range(4)])
        bpy.context.view_layer.update()
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(ROOT, "builds" if mode == "socket" else "pieces",
                                     "%s.glb" % nm), before)
    if mode != "socket":
        G.rescale_piece(pc, float(BV[:, 2].max() - BV[:, 2].min()) / 1.70)
    G.decimate(pc, faces)
    if offs > 0:
        P, _ = G.clear_body(pc, tree, offs)
    else:
        co = np.empty(len(pc.data.vertices) * 3)
        pc.data.vertices.foreach_get("co", co); P = co.reshape(-1, 3)
    if mode == "socket":
        G.socket_weapon2(pc, arm, bones[0], float(parts[3]), float(parts[4]),
                         **SPECS[nm])
        G.align_space(pc, body[0]); made = [(pc, bones[0])]
    elif mode == "skin":
        G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
        G.align_space(pc, body[0]); made = [(pc, "skin")]
    else:
        made = G.bone_bind(pc, arm, bones, split)
        for o, _ in made:
            G.align_space(o, body[0])
    if CARRY:
        for pbx in arm.pose.bones:
            pbx.matrix_basis = Matrix.Identity(4)
        bpy.context.view_layer.update()
    worn += [o for o, _ in made]
allm = body + worn
for o in allm:
    for s_ in o.material_slots:
        m_ = s_.material
        if not m_ or not m_.node_tree:
            continue
        nt = m_.node_tree
        b_ = next((x for x in nt.nodes if x.type == 'BSDF_PRINCIPLED'), None)
        o_ = next(x for x in nt.nodes if x.type == 'OUTPUT_MATERIAL')
        em = nt.nodes.new('ShaderNodeEmission')
        L_ = b_.inputs['Base Color'].links if b_ else []
        if L_:
            nt.links.new(L_[0].from_socket, em.inputs['Color'])
        nt.links.new(em.outputs['Emission'], o_.inputs['Surface'])
eng = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.type = 'ORTHO'
H = float(BV[:, 2].max() - BV[:, 2].min())
cam.data.ortho_scale = H * 1.45           # ONE scale for every facing
ctr = Vector((0.0, 0.0, H * 0.5))
FAC = {'S': 0, 'SE': 45, 'E': 90, 'NE': 135, 'N': 180, 'NW': 225, 'W': 270, 'SW': 315}
el = math.radians(EL)
acts = {x.name: x for x in bpy.data.actions}
poses = [("rest", None, 0)]
if "walk" in acts:
    poses.append(("walk_pass", "walk", 6))
for pname, act, fr in poses:
    if act:
        arm.animation_data.action = acts[act]
        f0 = int(acts[act].frame_range[0])
        sc.frame_set(f0 + fr)
        if CARRY:
            for bn, flat in CARRY.items():
                arm.pose.bones[bn].matrix_basis = Matrix(
                    [flat[i * 4:(i + 1) * 4] for i in range(4)])
            bpy.context.view_layer.update()
    for f in FAC:
        az = math.radians((360 - FAC[f]) % 360)
        pos = ctr + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
                            math.sin(el))) * (10 * H)
        cam.location = pos
        cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(TMP, "%s_%s.png" % (pname, f))
        bpy.ops.render.render(write_still=True)
json.dump(dict(dir=TMP, poses=[p[0] for p in poses], facings=list(FAC),
               ortho_scale=cam.data.ortho_scale, res=RES, gear=SPEC),
          open(OUTJ, "w"), indent=1)
print("rendered %d poses x %d facings" % (len(poses), len(FAC)))
