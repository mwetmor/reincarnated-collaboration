# A PLANTED armed idle: merge Meshy 335 "Axe Breathe and Look Around" as idle_armed, and keep
# the Axe Stance as idle_armed_stance.
#
# ==> NOT STAGED, AND WHY (attack_lab, 2026-09-29). The merge below is 33_assemble's own, and it
# does NOT preserve this clip's planting in this rig. Source, own rig: feet wander 0.006 / 0.003 m.
# Merged: 0.37 / 0.48 m -- each foot keeps its distance to the hips (0.983-1.027 m against the
# source's 0.983-1.023 x 1.088) while the pair ends up 10 cm wider and ORBITS the hips: the
# source's thighs counter-rotate against the look-around yaw, and copied as Blender basis
# rotations onto bones whose frames differ (~122 deg on the UpLegs) they no longer cancel.
# walk_fight survives the same merge exactly (x1.088), so this is specific, not pipeline-wide.
# Bringing breathe in faithfully needs a FRAME-AWARE retarget. Output kept as evidence in
# work/planted_idle_attempt/, not in export_staging/.
#
# Blender 5 note, fixed here: a merged action's SLOT still names the deleted source armature, so
# `animation_data.action = act` (all gearlib does) binds nothing and every measurement is the rest
# pose. The slot is renamed to the body's own identifier and the script proves the clip animates.
#
#   blender -b -noaudio --python-exit-code 1 --python scripts/50_planted_idle.py -- \
#       <body.glb> <anims/axe_breathe.glb> <out.glb> [--json f]
#
# WHY (attack_lab, 2026-09-29). An armed idle should stand planted. Meshy 85 "Axe Stance" does
# not: it is a FOOTWORK loop. Its feet are on the ground in 10 of 147 frames, they wander 1.71 m
# (left) and 1.03 m (right) over the loop, and on the frames they are down they slide 38 mm a
# frame in the source. Damping its hips to 0.10 m -- asked for, and measured -- meets the hip
# number and leaves the feet wandering 1.37 m around a pelvis that no longer follows them.
# "Axe Breathe and Look Around", fetched in W1 and never used: feet wander 0.006 m and 0.003 m
# over an 11.3 s loop, down on every frame, hips within 0.084 m of rest. It is what an armed
# idle standing planted looks like.
#
# THE MERGE IS 33_assemble's OWN: import the Meshy clip beside the body, take its action by bone
# name, rename it. Then the same hygiene every merged clip gets -- joint scale stripped,
# re-grounded from the feet (mode min) -- and the placement rule 45 now uses: the clip's MEAN hip
# position on the rest position, as a constant shift of the Hips location keys (no resample).
# Nothing else in the file is touched on purpose; the export round-trip is checked clip by clip
# by the caller.
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("50_planted_idle.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, SRC, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
rep = {}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
print("scene fps %.3f; body arrives with %d actions" % (sc.render.fps / (sc.render.fps_base or 1.0), len(bpy.data.actions)))

# ---- merge, exactly as 33_assemble merges a fetched clip -------------------------------
old = bpy.data.actions["idle_armed"]
old.name = "idle_armed_stance"
old.use_fake_user = True
before = set(sc.objects)
known = {x.name for x in bpy.data.actions}
bpy.ops.import_scene.gltf(filepath=SRC)
add = [o for o in sc.objects if o not in before]
new = [x for x in bpy.data.actions if x.name not in known]
assert new, "the source brought no action"
act = max(new, key=lambda x: x.frame_range[1] - x.frame_range[0])
act.name = "idle_armed"
act.use_fake_user = True
for o in add:
    bpy.data.objects.remove(o, do_unlink=True)
for x in new:
    if x is not act:
        bpy.data.actions.remove(x)
# THE SLOT. Blender 5 binds an action to an object through a SLOT, and the merged action's slot
# still names the Meshy armature that was just deleted -- so `animation_data.action = act`
# (which is all gearlib does) binds NOTHING, and every measurement taken on it is the rest
# pose. The first run of this script re-grounded and placed the clip from the rest pose and
# reported a hip excursion of exactly 0.0000 m. Give it the identifier the body's own actions
# use, so every existing helper binds it the way it binds them.
ref = next((x for x in bpy.data.actions if x is not act and len(getattr(x, "slots", []))), None)
if len(getattr(act, "slots", [])) and ref is not None:
    before_id = act.slots[0].identifier
    act.slots[0].name_display = ref.slots[0].name_display
    print("  slot %s -> %s (the body's own)" % (before_id, act.slots[0].identifier))
    rep["slot"] = dict(was=before_id, now=act.slots[0].identifier)
# ...and prove it animates before anything is measured on it
arm.animation_data.action = act
sc.frame_set(int(act.frame_range[0])); bpy.context.view_layer.update()
q0 = arm.pose.bones["LeftUpLeg"].matrix.to_quaternion()
sc.frame_set(int(act.frame_range[0] + (act.frame_range[1] - act.frame_range[0]) * 0.5)); bpy.context.view_layer.update()
q1 = arm.pose.bones["LeftUpLeg"].matrix.to_quaternion()
moved = q0.rotation_difference(q1).angle * 57.2958
print("  idle_armed drives the body: LeftUpLeg turns %.2f deg between frame 0 and mid-clip" % moved)
assert moved > 0.5, "the merged action does not animate the body armature"
arm.animation_data.action = None
rep["merged"] = dict(source=os.path.basename(SRC), frames=[int(round(v)) for v in act.frame_range],
                     kept_as="idle_armed_stance (the Axe Stance, unchanged)",
                     proof_it_animates_deg=round(moved, 2))
print("  merged idle_armed from %s, frames %s" % (os.path.basename(SRC), rep["merged"]["frames"]))

# ---- hygiene: joint scale, then ground from the feet ------------------------------------
rep["stripped_scale"] = {k: {b: sorted(v) for b, v in d.items()} for k, d in (G.strip_bone_scale([act]) or {}).items()}
r = G.reground_from_feet(arm, body, act)
rep["reground"] = r
print("  re-grounded by %+.4f m, worst frame %.2f cm" % (r["dz"], r["after"]["worst_cm"]))

# ---- placement: MEAN hips over the rest position, a rigid shift, nothing resampled -------
arm.animation_data.action = act
f0, f1 = (int(round(v)) for v in act.frame_range)
H = []
for f in range(f0, f1 + 1):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    H.append(arm.pose.bones["Hips"].matrix.translation.copy())
H = np.array([[h.x, h.y] for h in H])
hl = arm.data.bones["Hips"].head_local
rest = np.array([hl.x, hl.y])
mpu = float(arm.matrix_world.to_scale()[0])
net = float(np.linalg.norm(H[-1] - H[0]) * mpu)
d = rest - H.mean(axis=0)
db = arm.data.bones["Hips"].matrix_local.to_3x3().inverted() @ Vector((d[0], d[1], 0.0))
n = 0
for fc in G.act_fcurves(act):
    if fc.data_path != 'pose.bones["Hips"].location':
        continue
    for kp in fc.keyframe_points:
        kp.co[1] += db[fc.array_index]
        kp.handle_left[1] += db[fc.array_index]
        kp.handle_right[1] += db[fc.array_index]
        n += 1
    fc.update()
exc = float(np.max(np.linalg.norm(H - H.mean(axis=0), axis=1)) * mpu)
rep["placement"] = dict(net_travel_m=round(net, 4), mean_shift_m=round(float(np.linalg.norm(d) * mpu), 4),
                        hips_excursion_about_mean_m=round(exc, 4), hips_location_keys_shifted=n)
print("  net travel %.4f m; mean moved %.4f m onto rest; hips excursion about the mean %.4f m"
      % (net, np.linalg.norm(d) * mpu, exc))

# ---- export, as 43/45 export -------------------------------------------------------------
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True, export_image_format='AUTO')
import importlib
importlib.import_module("52_weapon_bones").ensure(OUT)  # T12: the base rig's weapon bones, after every export
L = importlib.import_module("21_lint_export").lint(OUT)
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"], warns=len(L["warns"]))
print("wrote %s (%.2f MB) LINT %s fails %d" % (OUT, os.path.getsize(OUT) / 1e6, L["verdict"], len(L["fails"])))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1, default=str)
assert not L["fails"], L["fails"]
