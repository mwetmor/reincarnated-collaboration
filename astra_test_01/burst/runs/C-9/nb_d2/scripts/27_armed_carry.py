# Build walk_armed / run_armed: the same locomotion with the wrists locked to a
# weapon carry angle, so the axe and shield stop waffling.
#
#   blender -b -noaudio --python scripts/27_armed_carry.py -- <in.glb> <out.glb>
#        [--alpha 0.85] [--sweep] [--json f]
#
# WHY NEW CLIPS AND NOT A LAYER. shield_carry_L works as a two-frame static
# pose because it IS one: a constant arm posture. A wrist lock is not -- the
# correction depends on where the forearm is on that frame, so it is per-frame
# data. A static pose layer cannot express it at all, and a runtime constraint
# would put rig logic in the scene. Baked clips leave `walk` and `run` intact
# for an unarmed barbarian and cost the consumer one animation-name choice.
#
# The target angle comes from the IDLE, because the idle is the clip Matt said
# looks right: "the axe is better when idling."
import bpy, json, os, sys
import numpy as np
from mathutils import Matrix
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("27_armed_carry.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
ALPHA = float(a[a.index('--alpha') + 1]) if '--alpha' in a else 0.85
SWEEP = '--sweep' in a
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
FPS = 30.0
PAIRS = (("RightHand", "RightForeArm"), ("LeftHand", "LeftForeArm"))


def ang(q):
    import math
    return math.degrees(2.0 * math.acos(min(1.0, max(-1.0, abs(q.w)))))


def reversals(seq):
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


def survey(arm, act):
    sc = bpy.context.scene
    prev = arm.animation_data.action
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    out = {}
    tracks = {p: [] for p in PAIRS}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for p in PAIRS:
            tracks[p].append(G.joint_rot(arm, *p))
    for p, qs in tracks.items():
        rate = [ang(qs[i - 1].rotation_difference(qs[i])) * FPS
                for i in range(1, len(qs))]
        prof = [ang(q.rotation_difference(qs[0])) for q in qs]
        out["%s_in_%s" % p] = dict(
            rate_p95=round(float(np.percentile(rate, 95)), 2),
            rate_max=round(float(np.max(rate)), 2),
            excursion_deg=round(float(np.max(prof) - np.min(prof)), 2),
            reversals=int(reversals(prof)))
    arm.animation_data.action = prev
    return out


def load():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
        bpy.data.objects.remove(o, do_unlink=True)
    return sc, arm


res = dict(alpha=ALPHA, before={}, after={}, sweep={}, target={})
sc, arm = load()
acts = {x.name: x for x in bpy.data.actions}
IDLE = acts["idle"]
targets = {p: G.mean_joint_rot(arm, IDLE, *p) for p in PAIRS}
for p, q in targets.items():
    res["target"]["%s_in_%s" % p] = [round(float(x), 6) for x in q]
    print("carry target from the idle, %s in %s: %s"
          % (p[0], p[1], [round(float(x), 4) for x in q]))
res["idle_reference"] = survey(arm, IDLE)
for cn in ("walk", "run"):
    res["before"][cn] = survey(arm, acts[cn])

if SWEEP:
    for al in (0.60, 0.75, 0.85, 0.95, 1.00):
        sc, arm = load()
        acts = {x.name: x for x in bpy.data.actions}
        tg = {p: G.mean_joint_rot(arm, acts["idle"], *p) for p in PAIRS}
        row = {}
        for cn in ("walk", "run"):
            for p in PAIRS:
                G.carry_lock(arm, acts[cn], p[0], p[1], tg[p], alpha=al)
            row[cn] = survey(arm, acts[cn])
        res["sweep"]["%.2f" % al] = row
        print("  alpha %.2f  walk R rev %d rate_p95 %6.1f | run R rev %d rate_p95 %6.1f"
              % (al, row["walk"]["RightHand_in_RightForeArm"]["reversals"],
                 row["walk"]["RightHand_in_RightForeArm"]["rate_p95"],
                 row["run"]["RightHand_in_RightForeArm"]["reversals"],
                 row["run"]["RightHand_in_RightForeArm"]["rate_p95"]))

# final build at the chosen alpha, as NEW clips
sc, arm = load()
acts = {x.name: x for x in bpy.data.actions}
tg = {p: G.mean_joint_rot(arm, acts["idle"], *p) for p in PAIRS}
made = []
for cn in ("walk", "run"):
    new = acts[cn].copy()
    new.name = "%s_armed" % cn
    new.use_fake_user = True
    for p in PAIRS:
        info = G.carry_lock(arm, new, p[0], p[1], tg[p], alpha=ALPHA)
        made.append(dict(clip=new.name, **info))
    res["after"]["%s_armed" % cn] = survey(arm, new)
    tr = arm.animation_data.nla_tracks.new()
    tr.name = new.name
    tr.strips.new(new.name, int(round(new.frame_range[0])), new)
    print("built %s" % new.name)
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in [x for x in sc.objects if x.type in ('MESH', 'ARMATURE')]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
print("wrote %s (%.2f MB)" % (DST, os.path.getsize(DST) / 1e6))
res["locks"] = made
if OUTJ:
    json.dump(res, open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
