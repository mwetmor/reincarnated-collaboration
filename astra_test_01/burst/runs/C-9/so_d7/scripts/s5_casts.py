# Choose Fire Ball and Meteor from the library's mage set BY MEASUREMENT, and
# find each one's release_s.
#
#   blender -b -noaudio --python scripts/s5_casts.py -- <anims_dir> <out.json>
#        --throw 132,136,126 --call 129,127,125
#
# Meshy's mage set is "Mage Soell Cast" 0..8 and three "Charged" entries --
# nothing is called Fire Ball or Meteor, and the numbers carry no meaning. The
# W1 block choice showed that a name is not evidence; neither is a thumbnail,
# which only SHORTLISTED these six. So:
#
#   FIRE BALL  a THROW: a hand driven forward from the chest. Scored by the
#              leading hand's peak forward speed, since a throw is defined by
#              the speed of its release, not by how far the arm ends up.
#              release_s = the instant of that peak forward speed.
#   METEOR     a CALL-DOWN: a hand raised above the head and brought down.
#              Scored by (peak height above the head) x (peak downward speed
#              AFTER that peak) -- both halves, because a raise alone is a
#              salute and a drop alone is a slap.
#              release_s = the instant of peak downward speed after the peak.
#
# Times come from the SCENE fps, read -- a hard-coded 30 against Blender's 24
# is what put the barbarian's run speed 19% out.
import bpy, glob, json, math, os, sys
import numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
ANIMS, OUT = a[0], a[1]
THROW = a[a.index('--throw') + 1].split(',')
CALL = a[a.index('--call') + 1].split(',')
FWD = Vector((0.0, -1.0, 0.0))


def track(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    sc = bpy.context.scene
    fps = float(sc.render.fps) / float(getattr(sc.render, 'fps_base', 1.0) or 1.0)
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    act = max(bpy.data.actions, key=lambda x: x.frame_range[1] - x.frame_range[0])
    arm.animation_data.action = act
    f0, f1 = (int(round(v)) for v in act.frame_range)
    P = lambda n: (arm.matrix_world @ arm.pose.bones[n].matrix).translation.copy()
    rows = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        rows.append(dict(f=f, chest=P("Spine"), head=P("Head"),
                         L=P("LeftHand"), R=P("RightHand")))
    return rows, fps, f0, f1


def speeds(rows, fps, key, axis):
    v = []
    for i in range(1, len(rows)):
        d = rows[i][key] - rows[i - 1][key]
        v.append(float(d.dot(axis)) * fps)
    return np.array(v)


res = dict(throw={}, call={})
for aid in THROW:
    rows, fps, f0, f1 = track(os.path.join(ANIMS, "cast%s.glb" % aid))
    best = None
    for hand in ("L", "R"):
        vf = speeds(rows, fps, hand, FWD)
        i = int(np.argmax(vf))
        reach = max(float((r[hand] - r["chest"]).dot(FWD)) for r in rows)
        rec = dict(hand=hand, peak_fwd_speed=round(float(vf[i]), 3),
                   release_frame=rows[i + 1]["f"],
                   release_s=round((rows[i + 1]["f"] - f0) / fps, 4),
                   max_reach_m=round(reach, 4))
        if best is None or rec["peak_fwd_speed"] > best["peak_fwd_speed"]:
            best = rec
    best.update(duration_s=round((f1 - f0) / fps, 4), fps=fps, frames=[f0, f1])
    res["throw"][aid] = best
    print("THROW %-4s %s hand, peak forward %.2f m/s at %.3f s, reach %.3f m, clip %.3f s"
          % (aid, best["hand"], best["peak_fwd_speed"], best["release_s"],
             best["max_reach_m"], best["duration_s"]))
UP = Vector((0.0, 0.0, 1.0))
for aid in CALL:
    rows, fps, f0, f1 = track(os.path.join(ANIMS, "cast%s.glb" % aid))
    best = None
    for hand in ("L", "R"):
        rise = [float(r[hand].z - r["head"].z) for r in rows]
        ip = int(np.argmax(rise))
        vz = speeds(rows, fps, hand, UP)
        after = vz[ip:] if ip < len(vz) else np.array([0.0])
        j = int(np.argmin(after)) + ip
        drop = float(-vz[j]) if len(vz) else 0.0
        score = max(rise[ip], 0.0) * max(drop, 0.0)
        rec = dict(hand=hand, peak_above_head_m=round(rise[ip], 4),
                   peak_s=round((rows[ip]["f"] - f0) / fps, 4),
                   peak_down_speed=round(drop, 3),
                   release_frame=rows[j + 1]["f"],
                   release_s=round((rows[j + 1]["f"] - f0) / fps, 4),
                   score=round(score, 4))
        if best is None or rec["score"] > best["score"]:
            best = rec
    best.update(duration_s=round((f1 - f0) / fps, 4), fps=fps, frames=[f0, f1])
    res["call"][aid] = best
    print("CALL  %-4s %s hand, %.3f m above head at %.3f s, then down %.2f m/s at %.3f s, score %.4f"
          % (aid, best["hand"], best["peak_above_head_m"], best["peak_s"],
             best["peak_down_speed"], best["release_s"], best["score"]))
fb = max(res["throw"], key=lambda k: res["throw"][k]["peak_fwd_speed"])
mt = max(res["call"], key=lambda k: res["call"][k]["score"])
res["pick"] = dict(fireball=fb, meteor=mt)
print("\nPICK  Fire Ball <- %s   Meteor <- %s" % (fb, mt))
json.dump(res, open(OUT, "w"), indent=1)
