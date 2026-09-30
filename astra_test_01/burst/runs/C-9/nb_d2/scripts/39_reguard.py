# Replace shield_guard_L with the pose chosen by the sweep.
#
#   blender -b -noaudio --python scripts/39_reguard.py -- <in.glb> <out.glb>
#
# The first guard came from Meshy 580 "Sword and Shield Alert Turn", whose left
# arm is a LOW FORWARD carry: the boss sat 0.324 m BELOW the sternum and only
# 0.130 m in front, so the disc hung beside his waist and showed 0.057 m2 of
# face from the south -- about a tenth of the disc. It was a carry, not a guard.
#
# This one is block1's left arm at 0.70 weight, chosen from a sweep:
#   boss  +0.331 m above the sternum, +0.576 m in front, still 0.143 m BELOW
#         the head, so the full block at weight 1.00 stays visibly different
#   face  0.309 m2 visible from the south -- 56% of the disc, against 10% before
#   body  12 of 1829 sampled vertices inside the torso, the same as before
# 0.60 was rejected despite sitting nicely: from the south-east the disc turns
# exactly edge-on, 0.002 m2, and vanishes.
import bpy, json, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("39_reguard.py")][0]))
sys.path.insert(0, HERE)
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
ROOT = os.path.dirname(HERE)
guard = json.load(open(os.path.join(ROOT, "work", "guard_pose.json")))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
old = bpy.data.actions.get("shield_guard_L")
if old:
    for t in list(arm.animation_data.nla_tracks):
        if any(s.action is old for s in t.strips):
            arm.animation_data.nla_tracks.remove(t)
    bpy.data.actions.remove(old)
    print("removed the old shield_guard_L")
g = bpy.data.actions.new("shield_guard_L")
arm.animation_data.action = g
for f in (0, 1):
    sc.frame_set(f)
    for bn, flat in guard.items():
        pb = arm.pose.bones[bn]
        pb.matrix_basis = Matrix([flat[i * 4:(i + 1) * 4] for i in range(4)])
        pb.rotation_mode = 'QUATERNION'
        pb.keyframe_insert("rotation_quaternion", frame=f)
        pb.keyframe_insert("location", frame=f)
g.use_fake_user = True
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
t = arm.animation_data.nla_tracks.new()
t.name = "shield_guard_L"
t.strips.new("shield_guard_L", 0, g)
print("wrote shield_guard_L on %s" % list(guard))
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
import importlib
importlib.import_module("52_weapon_bones").ensure(DST)  # T12: the base rig's weapon bones, after every export
L = importlib.import_module("21_lint_export").lint(DST)
print("wrote %s (%.2f MB)  LINT %s  fails %d" % (DST, os.path.getsize(DST) / 1e6,
                                                 L["verdict"], len(L["fails"])))
print("  clips %s" % sorted(L["clips"]))
print("  morphs %s" % L["morphs"])
assert not L["fails"]
