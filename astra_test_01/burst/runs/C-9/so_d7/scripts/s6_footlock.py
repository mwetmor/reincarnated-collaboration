# Foot-lock speed for IN-PLACE locomotion: the ground speed that pins the planted foot.
#
#   blender -b -noaudio --python scripts/s6_footlock.py -- <x.glb> walk,run [--json f]
#
# Her walk and run are in place AT SOURCE (net root travel 0.000 and 0.004 m), so "speed
# = travel / duration" returns ~0 and says nothing. In an in-place clip the body stays put
# and the planted foot slides BACKWARD at exactly the speed she would travel. So: take every
# interval where a foot is planted at both ends, read that foot's horizontal velocity, and
# the median of its backward component is the speed the scene must move her at for the foot
# to stand still. Drive her slower and the foot skates back; faster and it skates forward.
#
# Contact is RELATIVE to each foot's own height range (bottom 25%), not a fixed height --
# a fixed 0.05 m found no contacts at all in the barbarian's run.
import bpy, json, math, sys
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
FWD = Vector((0.0, -1.0, 0.0))     # she faces -Y
out = {}
for cn in CLIPS:
    act = bpy.data.actions[cn]
    arm.animation_data.action = act
    if len(getattr(act, "slots", [])):
        arm.animation_data.action_slot = act.slots[0]
    f0, f1 = (int(round(v)) for v in act.frame_range)
    tr = {b: [] for b in ("LeftFoot", "RightFoot")}
    for f in range(f0, f1 + 1):
        sc.frame_set(f); bpy.context.view_layer.update()
        for b in tr:
            tr[b].append((arm.matrix_world @ arm.pose.bones[b].matrix).translation.copy())
    v = []
    per_foot = {}
    for b, P in tr.items():
        z = np.array([p.z for p in P]); thr = z.min() + 0.25 * (z.max() - z.min())
        vb = [float(-(P[i + 1] - P[i]).dot(FWD)) * FPS for i in range(len(P) - 1)
              if z[i] < thr and z[i + 1] < thr]
        per_foot[b] = dict(planted_intervals=len(vb), median_back_speed=round(float(np.median(vb)), 3) if vb else None)
        v += vb
    spd = float(np.median(v)) if v else 0.0
    out[cn] = dict(foot_lock_speed_m_s=round(spd, 3), planted_intervals=len(v),
                   seconds=round((f1 - f0) / FPS, 4), per_foot=per_foot,
                   spread_m_s=round(float(np.percentile(v, 75) - np.percentile(v, 25)), 3) if v else None)
    print("  %-6s foot-lock speed %.3f m/s  (%d planted intervals, IQR %.3f)  L %s  R %s"
          % (cn, spd, len(v), out[cn]["spread_m_s"] or 0, per_foot["LeftFoot"]["median_back_speed"],
             per_foot["RightFoot"]["median_back_speed"]))
if OUTJ:
    json.dump(dict(fps=FPS, clips=out), open(OUTJ, "w"), indent=1)
