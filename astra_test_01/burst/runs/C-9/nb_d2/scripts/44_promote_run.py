# Lock the retargeted run's wrist and promote it to `run_armed`.
#
#   blender -b -noaudio --python scripts/44_promote_run.py -- <in.glb> <out.glb>
import bpy, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("44_promote_run.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
PAIRS = (("RightHand", "RightForeArm"), ("LeftHand", "LeftForeArm"))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
A = bpy.data.actions
tg = {p: G.mean_joint_rot(arm, A["idle"], *p) for p in PAIRS}
for p in PAIRS:
    G.carry_lock(arm, A["run_armed_t2m"], p[0], p[1], tg[p], alpha=0.60)
print("locked run_armed_t2m at alpha 0.60")
A["run_armed"].name = "run_armed_locked"
A["run_armed_t2m"].name = "run_armed"
print("run_armed <- the text-to-motion clip, retargeted (travel 8.66 m in 2.0 s)")
print("run_armed_locked <- the unarmed run with the wrist locked, kept")
for t in list(arm.animation_data.nla_tracks):
    for s_ in t.strips:
        t.name = s_.action.name
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
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
print("wrote %s (%.2f MB) LINT %s fails %d" % (DST, os.path.getsize(DST) / 1e6,
                                               L["verdict"], len(L["fails"])))
print("  clips %s" % sorted(L["clips"]))
print("  morphs %s" % L["morphs"])
assert not L["fails"]
