# Does a staff layer on HIT keep her flinch? (s17, the JOIN-1 pack review: "use the arm-only layer if
# the full carry kills the flinch")
#
#   blender -b -noaudio --python scripts/s17_hit_flinch.py -- <combined.glb> <staff_carry.json> <out.json>
#
# The flinch is the upper body's REACTION -- the spine folding and the head snapping back -- so it is
# measured two ways, per layer option, every frame of hit:
#   world    the head's excursion from frame 0 in world metres (includes the stagger of the hips)
#   reaction the head's and chest's excursion IN THE HIPS' OWN FRAME: the part of the flinch the
#            upper body makes on its own, which is exactly what a carry layer over the spine replaces
# Layer options: raw (no layer), arm (the 4 staff-arm bones), chest_arm (Spine02 + the 4), full (the
# carry's 9 bones: Spine02, Spine01, Spine, neck, Head + the 4). COMPOSITE as s12: the clip's pose,
# then the carry pose's LOCAL transforms written over the listed bones.
import bpy, json, sys
import numpy as np
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
SRC, CARRY, OUT = a[0], a[1], a[2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
car = json.load(open(CARRY))
CB = {b: Matrix([m[i * 4:(i + 1) * 4] for i in range(4)]) for b, m in car["bones"].items()}
act = bpy.data.actions['hit']; arm.animation_data.action = act
if len(getattr(act, "slots", [])):
    arm.animation_data.action_slot = act.slots[0]
f0, f1 = (int(round(v)) for v in act.frame_range)
MW = arm.matrix_world
ARM4 = ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]
OPTS = {"raw": [], "arm": ARM4, "chest_arm": ["Spine02"] + ARM4, "full": list(CB)}
rep = {}
for nm, bones in OPTS.items():
    H, C, Hr, Cr, Hq = [], [], [], [], []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        for b in bones:
            arm.pose.bones[b].matrix_basis = CB[b].copy()
        bpy.context.view_layer.update()
        loc, rot, _ = (MW @ arm.pose.bones['Hips'].matrix).decompose()     # RIGID hips frame, world metres
        hi = (Matrix.Translation(loc) @ rot.to_matrix().to_4x4()).inverted()   # (the armature's 0.01 scale made the first cut read cm as m)
        h = MW @ arm.pose.bones['Head'].head; c = MW @ arm.pose.bones['Spine02'].head
        H.append(np.array(h)); C.append(np.array(c)); Hr.append(np.array(hi @ h)); Cr.append(np.array(hi @ c))
        Hq.append((rot.inverted() @ (MW @ arm.pose.bones['Head'].matrix).to_quaternion()).normalized())   # head orientation in the hips frame
    H, C, Hr, Cr = (np.array(x) for x in (H, C, Hr, Cr))
    ex = lambda P: float(np.max(np.linalg.norm(P - P[0], axis=1)))
    snap = max(Hq[0].rotation_difference(q).angle for q in Hq) * 57.29577951308232
    rep[nm] = dict(bones=bones, head_world_m=round(ex(H), 3), head_reaction_m=round(ex(Hr), 3), chest_reaction_m=round(ex(Cr), 3),
                   head_snap_deg=round(float(snap), 2),
                   head_path_world_m=round(float(np.sum(np.linalg.norm(np.diff(H, axis=0), axis=1))), 3))
    print("  %-10s head world %.3f m | reaction (hips frame): head %.3f m, chest %.3f m, head turns %.2f deg"
          % (nm, rep[nm]['head_world_m'], rep[nm]['head_reaction_m'], rep[nm]['chest_reaction_m'], rep[nm]['head_snap_deg']))
for nm in ("arm", "chest_arm", "full"):
    rep[nm]['head_reaction_kept'] = round(rep[nm]['head_reaction_m'] / max(rep['raw']['head_reaction_m'], 1e-9), 3)
    rep[nm]['head_snap_kept'] = round(rep[nm]['head_snap_deg'] / max(rep['raw']['head_snap_deg'], 1e-9), 3)
json.dump(dict(frames=[f0, f1], options=rep), open(OUT, 'w'), indent=1)
