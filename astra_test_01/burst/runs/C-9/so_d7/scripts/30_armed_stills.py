# Close-up strips at 52.95 deg with the WEAPONS IN FRAME, so the grip and the
# axe's carry angle can be judged by eye and not only by the numbers.
#
#   blender -b -noaudio --python scripts/30_armed_stills.py -- <body.glb>
#        <outdir> [--clips idle,walk_armed,run_armed,attack] [--res 640]
#
# Body, axe and shield each arrive on their own copy of the same 24-bone rig, so
# every rig is driven with the same action on the same frame. Posing only the
# body leaves the weapons in their bind pose beside him -- which looks like a
# grip defect and is not one.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("30_armed_stills.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUT = a[0], a[1]
CLIPS = (a[a.index('--clips') + 1] if '--clips' in a
         else "idle,walk_armed,run_armed,attack").split(",")
RES = int(a[a.index('--res') + 1]) if '--res' in a else 640
ROOT = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
kb = body[0].data.shape_keys.key_blocks if body[0].data.shape_keys else {}
for nm in ("grip_R", "grip_L"):
    if nm in kb:
        kb[nm].value = 1.0
RIGS = [arm]
WORN = []
for nm in ("axe", "shield"):
    p = os.path.join(ROOT, "export", "%s.glb" % nm)
    if not os.path.exists(p):
        continue
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=p)
    add = [o for o in sc.objects if o not in before]
    m = next((o for o in add if o.type == 'MESH' and o.vertex_groups), None)
    for o in [o for o in add if o.type == 'MESH' and o is not m]:
        bpy.data.objects.remove(o, do_unlink=True)
    RIGS.append(next(o for o in add if o.type == 'ARMATURE'))
    WORN.append(m)
    print("loaded %s" % nm)
# which left-arm layer to hold the shield in. The GUARD pose puts the disc in
# front of the torso facing the enemy; the older CARRY pose only kept it off
# his chest. Selected by name so the same script can show either.
LAYER = a[a.index('--layer') + 1] if '--layer' in a else "guard"
carry = {}
for cand in (("guard_pose.json", "carry_pose.json") if LAYER == "guard"
             else ("carry_pose.json",)):
    q = os.path.join(ROOT, "work", cand)
    if os.path.exists(q):
        carry = json.load(open(q))
        print("left-arm layer: %s" % cand)
        break
ACT = {x.name: x for x in bpy.data.actions}

eng = [e.identifier for e in
       bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in eng else 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.color_mode = 'RGBA'
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN'))
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(50), 0, math.radians(35))
sc.collection.objects.link(sun)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = 'ORTHO'
EL = math.radians(52.95)
FAC = dict(S=0, SE=45, E=90, W=270)


def drive(cn, f):
    for A in RIGS:
        if A.animation_data is None:
            A.animation_data_create()
        A.animation_data.action = ACT.get(cn)
        for pb in A.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
    sc.frame_set(f)
    bpy.context.view_layer.update()
    if carry and not cn.startswith("attack"):
        for A in RIGS:
            for bn, flat in carry.items():
                if bn in A.pose.bones:
                    A.pose.bones[bn].matrix_basis = Matrix(
                        [flat[i * 4:(i + 1) * 4] for i in range(4)])
        bpy.context.view_layer.update()


rows = []
for cn in CLIPS:
    if cn not in ACT:
        print("  (no clip %s)" % cn)
        continue
    f0, f1 = (int(round(x)) for x in ACT[cn].frame_range)
    f = (f0 + f1) // 2
    drive(cn, f)
    # frame on the UPPER BODY and the hands: that is what the note is about
    hips = (arm.matrix_world @ arm.pose.bones['Hips'].matrix).translation
    head = (arm.matrix_world @ arm.pose.bones['Head'].matrix).translation
    ctr = Vector((hips.x, hips.y, (hips.z + head.z) * 0.5 + 0.05))
    cam.data.ortho_scale = 1.30
    for fac, deg in FAC.items():
        az = math.radians((360 - deg) % 360)
        pos = ctr + Vector((math.sin(az) * math.cos(EL),
                            -math.cos(az) * math.cos(EL), math.sin(EL))) * 8.0
        cam.location = pos
        cam.rotation_euler = (ctr - pos).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(OUT, "%s_%s.png" % (cn, fac))
        bpy.ops.render.render(write_still=True)
    rows.append(dict(clip=cn, frame=f, range=[f0, f1]))
    print("  %-11s frame %d of %d-%d" % (cn, f, f0, f1))
json.dump(dict(rows=rows, facings=list(FAC), res=RES, elev=52.95,
               ortho_scale=1.30), open(os.path.join(OUT, "stills.json"), "w"),
          indent=1)
