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
#
# SAMPLED AT THE CLIP'S OWN KEYS (2026-09-30, s17's run re-cut). This sampled the scene's INTEGER
# frames over round(frame_range). Every D7 clip was 24 fps from 0, so the integers WERE the keys and
# nothing was wrong -- until the run was re-cut on Meshy's own 30 fps cycle (0.7333 s = 17.6
# frames): round() made that 18 frames, the last sample fell 1/60 s past the clip's end (a held
# pose read as a slow foot), and the 24 fps grid read the source between its keys. It reported
# 4.146 on a clip whose keys give 3.986. Now it samples every keyframe time the action holds
# (fractional frames via subframe) and divides by the true step. On a 24 fps clip from 0 that is
# the same set of frames as before: walk 1.449 and the pre-re-cut run 3.928 reproduce exactly.
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
    try:
        fcs = list(act.fcurves)                                    # legacy (Blender < 5)
    except AttributeError:
        fcs = [fc for ly in act.layers for st in ly.strips for cb in st.channelbags for fc in cb.fcurves]
    frames = sorted({round(k.co.x, 4) for fc in fcs for k in fc.keyframe_points})
    f0, f1 = frames[0], frames[-1]
    tr = {b: [] for b in ("LeftFoot", "RightFoot")}
    for f in frames:
        sc.frame_set(int(math.floor(f)), subframe=f - math.floor(f)); bpy.context.view_layer.update()
        for b in tr:
            tr[b].append((arm.matrix_world @ arm.pose.bones[b].matrix).translation.copy())
    v = []
    per_foot = {}
    for b, P in tr.items():
        z = np.array([p.z for p in P]); thr = z.min() + 0.25 * (z.max() - z.min())
        vb = [float(-(P[i + 1] - P[i]).dot(FWD)) * FPS / (frames[i + 1] - frames[i]) for i in range(len(P) - 1)
              if z[i] < thr and z[i + 1] < thr]
        per_foot[b] = dict(planted_intervals=len(vb), median_back_speed=round(float(np.median(vb)), 3) if vb else None)
        v += vb
    spd = float(np.median(v)) if v else 0.0
    out[cn] = dict(foot_lock_speed_m_s=round(spd, 3), planted_intervals=len(v), keys=len(frames),
                   seconds=round((f1 - f0) / FPS, 4), per_foot=per_foot,
                   spread_m_s=round(float(np.percentile(v, 75) - np.percentile(v, 25)), 3) if v else None)
    print("  %-6s foot-lock speed %.3f m/s  (%d planted intervals, IQR %.3f)  L %s  R %s"
          % (cn, spd, len(v), out[cn]["spread_m_s"] or 0, per_foot["LeftFoot"]["median_back_speed"],
             per_foot["RightFoot"]["median_back_speed"]))
if OUTJ:
    json.dump(dict(fps=FPS, clips=out), open(OUTJ, "w"), indent=1)
