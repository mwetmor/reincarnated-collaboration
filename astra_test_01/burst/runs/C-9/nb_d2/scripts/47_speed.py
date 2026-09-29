# Locomotion speed, two ways, measured BEFORE the de-root (afterwards there is
# no travel left to measure).
#
#   blender -b -noaudio --python scripts/47_speed.py -- <rooted.glb> <clips>
#
# NET     total horizontal displacement / total duration.
# STEPPING  displacement accumulated only over intervals where a foot is on the
#           ground, divided by the duration of those intervals.
#
# They differ when a clip has stationary portions, and strafe_R has them: net
# 0.34 m/s against the scene's contact-filtered 0.562. strafe_L has none, which
# is why both methods agree there (0.756 against their 0.767). A locomotion
# blend wants the STEPPING speed -- the speed while he is actually travelling --
# so that is what the manifest carries, with net beside it.
import bpy, json, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
SRC, CLIPS = a[0], a[1].split(",")
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
FPS = float(sc.render.fps) / float(getattr(sc.render, 'fps_base', 1.0) or 1.0)
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
A = {x.name: x for x in bpy.data.actions}
out = {}
for cn in CLIPS:
    if cn not in A:
        continue
    arm.animation_data.action = A[cn]
    f0, f1 = (int(round(v)) for v in A[cn].frame_range)
    P, Z = [], []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        h = (arm.matrix_world @ arm.pose.bones["Hips"].matrix).translation
        P.append(Vector((h.x, h.y, 0)))
        Z.append(min((arm.matrix_world @ arm.pose.bones[b].matrix).translation.z
                     for b in ("LeftFoot", "RightFoot")))
    thr = min(Z) + 0.35 * (max(Z) - min(Z))
    n = len(P) - 1
    net = float((P[-1] - P[0]).length)
    dur = n / FPS
    step_d, step_n = 0.0, 0
    for i in range(n):
        if Z[i] < thr and Z[i + 1] < thr:
            step_d += float((P[i + 1] - P[i]).length)
            step_n += 1
    out[cn] = dict(
        keys=len(P), intervals=n, seconds=round(dur, 4),
        net_travel_m=round(net, 4), net_speed_m_s=round(net / dur, 3),
        stepping_intervals=step_n,
        stepping_seconds=round(step_n / FPS, 4),
        stepping_speed_m_s=(round(step_d / (step_n / FPS), 3) if step_n else None))
    r = out[cn]
    print("  %-16s %2d keys %6.4f s | net %.4f m = %.3f m/s | stepping %d/%d "
          "intervals = %s m/s" % (cn, r["keys"], r["seconds"], r["net_travel_m"],
                                  r["net_speed_m_s"], r["stepping_intervals"],
                                  r["intervals"], r["stepping_speed_m_s"]))
if OUTJ:
    json.dump(dict(fps=FPS, clips=out), open(OUTJ, "w"), indent=1)
