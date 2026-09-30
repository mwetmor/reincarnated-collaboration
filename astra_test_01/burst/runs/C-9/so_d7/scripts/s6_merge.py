# Merge her library clips onto her body, each one PROVEN to animate.
#
#   blender -b -noaudio --python scripts/s6_merge.py -- <body.glb> <anims_dir> <out.glb>
#        --clips idle:idle,walk:walk,... [--json f]
#
# THE SLOT (Blender 5). An action binds to an object through a SLOT, and a merged
# action's slot still names the armature it was imported with -- which is deleted
# here. `animation_data.action = act` then binds NOTHING and every measurement is
# the rest pose: the barbarian's planted-idle attempt reported a hip excursion of
# exactly 0.0000 m that way. The fix in 50_planted_idle copies the slot name from
# an action the body already has; this body is freshly rigged and may have NONE.
# So the slot is assigned EXPLICITLY (action_slot = act.slots[0]), which needs no
# reference action -- and then each clip must PROVE it moves a bone before it is
# kept. A clip that does not animate fails the merge; it is not exported.
import bpy, json, os, sys
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
BODY, ANIMS, OUT = a[0], a[1], a[2]
SPEC = [x.split(":") for x in a[a.index('--clips') + 1].split(",")]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
if arm.animation_data is None:
    arm.animation_data_create()
for x in list(bpy.data.actions):          # the body arrives with no clips we want
    bpy.data.actions.remove(x)


def bind(act):
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        try:
            arm.animation_data.action_slot = act.slots[0]
        except Exception as e:
            print("  (action_slot assign: %s)" % e)
    bpy.context.view_layer.update()


def animates(act):
    """Largest rotation any leg or arm bone makes between the first frame and
    any other, in degrees. A merged clip that binds nothing reads 0.00."""
    bind(act)
    f0, f1 = (int(round(v)) for v in act.frame_range)
    sc.frame_set(f0); bpy.context.view_layer.update()
    base = {b: arm.pose.bones[b].matrix.to_quaternion().copy()
            for b in ("LeftUpLeg", "RightUpLeg", "LeftArm", "RightArm", "Spine")}
    best = 0.0
    for f in range(f0, f1 + 1, max(1, (f1 - f0) // 12)):
        sc.frame_set(f); bpy.context.view_layer.update()
        for b, q in base.items():
            best = max(best, q.rotation_difference(arm.pose.bones[b].matrix.to_quaternion()).angle * 57.2958)
    return best


rep = {}
for name, src in SPEC:
    p = os.path.join(ANIMS, "%s.glb" % src)
    before = set(sc.objects)
    known = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=p)
    add = [o for o in sc.objects if o not in before]
    new = [x for x in bpy.data.actions if x not in known]
    act = max(new, key=lambda x: x.frame_range[1] - x.frame_range[0])
    for x in new:
        if x is not act:
            bpy.data.actions.remove(x)
    for o in add:
        bpy.data.objects.remove(o, do_unlink=True)
    act.name = name
    act.use_fake_user = True
    moved = animates(act)
    rep[name] = dict(source=src, frames=[int(round(v)) for v in act.frame_range],
                     proof_it_animates_deg=round(moved, 2))
    print("  %-14s <- %-8s frames %-10s  a limb turns %6.2f deg  %s"
          % (name, src, rep[name]["frames"], moved, "OK" if moved > 0.5 else "DOES NOT ANIMATE"))
    assert moved > 0.5, "%s does not animate the body -- not merging a rest pose" % name
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
for name in rep:
    act = bpy.data.actions[name]
    t = arm.animation_data.nla_tracks.new()
    t.name = name
    s_ = t.strips.new(name, int(round(act.frame_range[0])), act)
    if len(getattr(act, "slots", [])) and hasattr(s_, "action_slot"):
        try:
            s_.action_slot = act.slots[0]
        except Exception:
            pass
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True, export_image_format='AUTO')
print("wrote %s (%.2f MB), %d clips" % (OUT, os.path.getsize(OUT) / 1e6, len(rep)))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
