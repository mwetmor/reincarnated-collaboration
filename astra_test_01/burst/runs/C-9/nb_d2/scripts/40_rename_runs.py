# The diagonal blend FAILED the straightness test, so it must not ship as
# `run_armed`. Put the honest clip back under that name.
#
# Measured body yaw, hips' forward axis against world forward:
#   run_armed_L      -38.79 deg
#   run_armed_R      -14.91 deg
#   50/50 blend      -32.40 deg   <- still angled
#
# The blend premise was that a left-forward and a right-forward run average to
# straight. IT IS FALSE FOR THESE CLIPS: both are angled THE SAME WAY, by
# different amounts, so their mean is the mean angle and not zero. The lateral
# root-drift metric had said the blend was a 32% improvement (0.046 -> 0.032 m)
# and it was measuring SWAY, not HEADING -- an instrument answering a question
# it was not asked, caught this time before it shipped rather than after.
import bpy, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("40_rename_runs.py")][0]))
sys.path.insert(0, HERE)
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
A = bpy.data.actions
if "run_armed" in A and "run_armed_unarmedsrc" in A:
    A["run_armed"].name = "run_armed_diagblend_REJECTED"
    A["run_armed_unarmedsrc"].name = "run_armed"
    print("run_armed <- the unarmed run with the wrist locked (yaw 0, it works)")
    print("run_armed_diagblend_REJECTED <- the 50/50 diagonal blend, -32.4 deg off")
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
assert not L["fails"]
