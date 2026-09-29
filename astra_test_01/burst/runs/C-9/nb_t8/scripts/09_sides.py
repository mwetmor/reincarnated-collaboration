# T8 step 1: does the RIG agree with the GEOMETRY about which side is which?
#
#   blender -b -noaudio --python scripts/09_sides.py -- <glb> [<glb> ...]
#
# The tattoo defect was a sidedness error in the texture. A second, independent
# sidedness error can hide in the rig: Meshy names bones LeftArm / RightArm,
# and if that naming disagrees with the body those names are attached to, then
# every clip plays mirrored and the tattoo ends up on the wrong arm again --
# this time in motion, where it is much harder to see.
#
# Checked by asking where the named bones actually ARE. Facing is re-derived
# here from the feet rather than imported, so this file stands on its own.
#
# ON THE REST POSE, STRICTLY; on a clip, only as a whole-clip average. A first
# version sampled frame one of every clip and duly reported the attack as
# mirrored: LeftArm at x = -0.016 and LeftHand at -0.0008, both sitting on the
# midline because a sword wind-up brings the off hand across the body. That is
# a POSE, not a rig error. "A named bone is on its own side" is a property of
# the bind pose; across an animation only the average can carry it, and an arm
# may legitimately spend frames on the wrong side of the midline. A leg may
# not, so the legs are held to the strict test even in motion.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
rep = {}
for src in a:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    meshes = [o for o in sc.objects if o.type == 'MESH']
    V = []
    for o in meshes:
        co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
        V.append(co.reshape(-1, 3) @ np.array(o.matrix_world.to_3x3()).T
                 + np.array(o.matrix_world.translation))
    V = np.vstack(V); lo, hi = V.min(0), V.max(0); H = hi[2] - lo[2]
    shin = V[(V[:, 2] > lo[2] + 0.10 * H) & (V[:, 2] < lo[2] + 0.20 * H)]
    y_leg = float(np.median(shin[:, 1]))
    feet = V[V[:, 2] < lo[2] + 0.04 * H]
    fdir = 1 if (feet[:, 1].max() - y_leg) > (y_leg - feet[:, 1].min()) else -1
    fwd = np.array([0.0, float(fdir), 0.0])
    rt = np.cross(fwd, np.array([0.0, 0.0, 1.0]))
    act = arm.animation_data.action if arm.animation_data else None
    if act:
        f0, f1 = (int(v) for v in act.frame_range)
        frames = list(range(f0, f1 + 1))
    else:
        frames = [1]
    acc = {b.name: [] for b in arm.pose.bones}
    for f in frames:
        sc.frame_set(f)
        for b in arm.pose.bones:
            acc[b.name].append(float((arm.matrix_world @ b.head).x))
    P = {k: Vector((float(np.mean(v)), 0.0, 0.0)) for k, v in acc.items()}
    animated = act is not None
    rows = {}
    ok = True
    for side in ("Left", "Right"):
        for part in ("Arm", "Hand", "UpLeg", "Foot"):
            bn = side + part
            if bn not in P:
                continue
            x = float(P[bn].x)
            # project onto his own right axis: positive = on his right
            s = x * float(rt[0])
            agree = (s < 0) if side == "Left" else (s > 0)
            # arms cross the midline in an attack; legs do not
            strict = (not animated) or part in ("UpLeg", "Foot")
            if strict:
                ok &= agree
            rows[bn] = dict(mean_x=round(x, 4), on_his_right=bool(s > 0),
                            agrees=bool(agree), strict=bool(strict))
    print("%-15s facing %sY, his right is %sX   rig naming %s"
          % (os.path.basename(src), "+" if fdir > 0 else "-",
             "+" if rt[0] > 0 else "-", "AGREES" if ok else "*** DISAGREES ***"))
    for bn, r in rows.items():
        print("     %-12s mean x %+8.4f  on his right: %-5s  %s%s"
              % (bn, r["mean_x"], r["on_his_right"],
                 "ok" if r["agrees"] else "crosses midline",
                 "" if r["strict"] else "  (not decisive: arms cross)"))
    rep[os.path.basename(src)] = dict(facing="+Y" if fdir > 0 else "-Y",
                                      right="+X" if rt[0] > 0 else "-X",
                                      height=round(float(H), 4),
                                      bones=rows, consistent=bool(ok))
json.dump(rep, open("work/sides.json", "w"), indent=1)
