# Matt: the axe "waffles back and forth awkwardly.. not the way someone should
# hold a weapon." Measure the waffle.
#
#   blender -b -noaudio --python scripts/26_wrist.py -- <x.glb> [--json f]
#
# The axe is bound 100% to RightHand, so the axe's world orientation IS
# RightHand's. The waffle is therefore the WRIST: the rotation of Hand relative
# to ForeArm. Measured as the local rotation's angle per frame, and its rate.
#
# Measuring the axe mesh would answer the same question with more machinery and
# more ways to be wrong; the mesh is rigid and single-bound, so the bone carries
# all of it. Reported for the LEFT arm too, because the shield has the same
# problem and the same cause.
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
CLIP = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
FPS = 30.0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')


def math_ang(q):
    """Signed-free rotation magnitude in degrees, 0..180."""
    import math
    w = min(1.0, max(-1.0, abs(q.w)))
    return math.degrees(2.0 * math.acos(w))


def count_reversals(seq):
    """Direction changes in a scalar track -- how many times it doubles back.
    A weapon held properly tracks the arm; a flopping one reverses repeatedly
    inside a single stride. Ignores reversals under 1 degree so sampling noise
    does not count as flop."""
    n, last = 0, 0
    for i in range(1, len(seq)):
        d = seq[i] - seq[i - 1]
        if abs(d) < 1.0:
            continue
        s = 1 if d > 0 else -1
        if last and s != last:
            n += 1
        last = s
    return n


def local_rot(child, parent):
    """Child's rotation expressed in the parent's frame -- the joint angle."""
    pc = arm.pose.bones[child].matrix
    pp = arm.pose.bones[parent].matrix
    return (pp.to_3x3().inverted() @ pc.to_3x3()).to_quaternion()


PAIRS = (("RightHand", "RightForeArm"), ("LeftHand", "LeftForeArm"),
         ("RightForeArm", "RightArm"), ("LeftForeArm", "LeftArm"))
out = {}
for act in sorted(bpy.data.actions, key=lambda x: x.name):
    if act.name == "shield_carry_L":
        continue
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    tr = {p: [] for p in PAIRS}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for p in PAIRS:
            tr[p].append(local_rot(*p))
    rec = {}
    for p, qs in tr.items():
        # angle swept between consecutive frames, in degrees per second
        rate = []
        for i in range(1, len(qs)):
            d = qs[i - 1].rotation_difference(qs[i])
            rate.append(abs(math_ang(d)) * FPS)
        # total angular EXCURSION of the joint over the clip: the spread of the
        # joint angle itself, which is what reads as flop
        ang = [math_ang(q.rotation_difference(qs[0])) for q in qs]
        rec["%s_in_%s" % p] = dict(
            rate_mean=round(float(np.mean(rate)), 2),
            rate_p95=round(float(np.percentile(rate, 95)), 2),
            rate_max=round(float(np.max(rate)), 2),
            excursion_deg=round(float(np.max(ang) - np.min(ang)), 2),
            reversals=int(count_reversals(ang)))
        rec["%s_in_%s" % p]["_n"] = len(qs)
    out[act.name] = rec
    print("  %-8s %s" % (act.name, json.dumps(
        {k: dict(rate_p95=v['rate_p95'], excursion=v['excursion_deg'],
                 reversals=v['reversals']) for k, v in rec.items()})))
if OUTJ:
    json.dump(dict(file=CLIP, fps=FPS, clips=out), open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
