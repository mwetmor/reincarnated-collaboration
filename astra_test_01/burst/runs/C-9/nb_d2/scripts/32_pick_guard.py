# Which of the fetched clips actually raises a SHIELD, and what is the guard pose?
#
#   blender -b -noaudio --python scripts/32_pick_guard.py -- <anims_dir>
#        [--json f] [--guard <name>]
#
# "Block1".."Block10" are unlabelled in Meshy's library, so the choice is made
# by measurement, not by the name. A shield block raises the LEFT hand in front
# of the chest and head; a sword parry raises the RIGHT and sweeps it across.
# So the discriminator is the LEFT-minus-RIGHT hand elevation at the clip's
# peak, together with how far forward of the sternum the left hand gets.
#
# Reported for every clip including the ones already chosen, because a clip
# whose name says "Sword and Shield" can still be driving the sword arm.
import bpy, glob, json, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]
ANIMS = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
GUARD = a[a.index('--guard') + 1] if '--guard' in a else None
ARMCH = ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand")


def bone(arm, nm):
    return (arm.matrix_world @ arm.pose.bones[nm].matrix).translation


rows, poses = {}, {}
for p in sorted(glob.glob(os.path.join(ANIMS, "*.glb"))):
    nm = os.path.splitext(os.path.basename(p))[0]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=p)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    acts = [x for x in bpy.data.actions]
    if not acts:
        print("%-14s NO ACTION" % nm)
        continue
    act = acts[0]
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    best = None
    tr = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        ch = bone(arm, "Spine02")
        lh, rh, hd = bone(arm, "LeftHand"), bone(arm, "RightHand"), bone(arm, "Head")
        # forward: the body faces -Y in this rig
        fwd = Vector((0.0, -1.0, 0.0))
        rec = dict(f=f,
                   l_rise=float(lh.z - ch.z), r_rise=float(rh.z - ch.z),
                   l_fwd=float((lh - ch).dot(fwd)), r_fwd=float((rh - ch).dot(fwd)),
                   l_vs_head=float(lh.z - hd.z))
        rec["guard_score"] = (rec["l_rise"] - rec["r_rise"]) + max(rec["l_fwd"], 0.0)
        tr.append(rec)
        if best is None or rec["guard_score"] > best["guard_score"]:
            best = rec
    rows[nm] = dict(frames=[f0, f1], action=act.name,
                    peak=dict((k, round(v, 4)) for k, v in best.items()),
                    l_rise_max=round(max(r["l_rise"] for r in tr), 4),
                    r_rise_max=round(max(r["r_rise"] for r in tr), 4),
                    l_fwd_max=round(max(r["l_fwd"] for r in tr), 4))
    print("%-14s frames %3d  LEFT rise %+0.3f fwd %+0.3f | RIGHT rise %+0.3f | "
          "guard-score %+0.3f at f%d  %s"
          % (nm, f1 - f0 + 1, rows[nm]["l_rise_max"], rows[nm]["l_fwd_max"],
             rows[nm]["r_rise_max"], best["guard_score"], best["f"],
             "<- LEFT ARM LEADS" if best["guard_score"] > 0.15 else ""))
    if GUARD and nm == GUARD:
        sc.frame_set(best["f"])
        bpy.context.view_layer.update()
        poses[nm] = {b: [x for row in arm.pose.bones[b].matrix_basis for x in row]
                     for b in ARMCH}
        print("   captured the left-arm guard pose at frame %d" % best["f"])

if GUARD and poses:
    json.dump(poses[GUARD], open(os.path.join(os.path.dirname(ANIMS), "work",
                                              "guard_pose.json"), "w"), indent=1)
    print("wrote work/guard_pose.json from %s" % GUARD)
if OUTJ:
    json.dump(rows, open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
