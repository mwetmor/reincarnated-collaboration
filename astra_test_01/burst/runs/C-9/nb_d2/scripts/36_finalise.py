# Apply the wrist lock to the fetched armed clips and settle the clip names.
#
#   blender -b -noaudio --python scripts/36_finalise.py -- <in.glb> <out.glb> [--json f]
#
# WHY BOTH. Measured on the merged build, right wrist in the forearm's frame:
#
#                                      deg/s p95   reversals
#   idle              (unarmed)             71.2       1
#   walk              (unarmed)            209.5       5
#   walk_armed        (unarmed + lock)      10.4       0
#   walk_armed_m      (Meshy armed walk)    68.8       3
#   idle_armed        (Meshy Axe Stance)   159.6       4
#
# Meshy's armed walk is genuinely armed MOTION -- the whole body carries a
# weapon stance, which a wrist metric cannot see and a locked unarmed gait
# cannot fake. But its wrist still reverses three times a cycle, and its Axe
# Stance idle reverses FOUR times, worse than the plain idle. So neither source
# wins outright: take Meshy's posture and put the lock on top of it.
import bpy, json, os, sys
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("36_finalise.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ALPHA = 0.95
PAIRS = (("RightHand", "RightForeArm"), ("LeftHand", "LeftForeArm"))
LOCK = ("idle_armed", "walk_armed_m", "run_armed_L", "run_armed_R")
RENAME = {"walk_armed_m": "walk_armed", "walk_armed": "walk_armed_unarmedsrc"}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
ACT = {x.name: x for x in bpy.data.actions}
tg = {p: G.mean_joint_rot(arm, ACT["idle"], *p) for p in PAIRS}
rep = {}
for cn in LOCK:
    if cn not in ACT:
        continue
    for p in PAIRS:
        G.carry_lock(arm, ACT[cn], p[0], p[1], tg[p], alpha=ALPHA)
    rep[cn] = "locked at alpha %.2f" % ALPHA
    print("locked %s" % cn)
# rename in a safe order: the incumbent moves aside first
if "walk_armed" in ACT and "walk_armed_m" in ACT:
    ACT["walk_armed"].name = "walk_armed_unarmedsrc"
    ACT["walk_armed_m"].name = "walk_armed"
    print("walk_armed  <- Meshy 'Walk Fight Forward' + lock")
    print("walk_armed_unarmedsrc <- the unarmed walk + lock (kept; it is calmer "
          "at the wrist but its posture is not armed)")
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
print("\nwrote %s (%.2f MB)" % (DST, os.path.getsize(DST) / 1e6))
print("  LINT %s" % L["verdict"])
for f_ in L["fails"]:
    print("  FAIL %s" % f_)
print("  clips  %s" % sorted(L["clips"]))
print("  morphs %s" % L["morphs"])
assert not L["fails"]
if OUTJ:
    json.dump(dict(locked=rep, alpha=ALPHA, clips=sorted(L["clips"]),
                   morphs=L["morphs"], verdict=L["verdict"]),
              open(OUTJ, "w"), indent=1)
