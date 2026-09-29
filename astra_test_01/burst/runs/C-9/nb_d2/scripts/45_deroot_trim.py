# Trim run_armed to ONE gait cycle, and take the root motion out of the clips
# that should not have it.
#
#   blender -b -noaudio --python scripts/45_deroot_trim.py -- <in.glb> <out.glb>
#        [--json f]
#
# From the scene: run_armed held ~4 gait cycles in 2.5 s, which breaks a
# walk/run sync group that assumes one cycle per clip, and its planted foot
# slid 316 mm through a crossover. One cycle fixes both -- a crossover is two
# cycles meeting, so there is no crossover inside a single one.
#
# And root motion turned up in clips nobody thought had any: idle_armed drifts
# 0.8994 m over its own loop, attack_chop 0.7519 m. A drifting idle is a defect
# whatever the consumer does about it. Locomotion goes out IN PLACE with its
# speed in the manifest, because a speed a consumer can read is worth more than
# root motion it has to strip.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("45_deroot_trim.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
FPS = 30.0
CONTACT = 0.05
LOCO = ("walk_armed", "run_armed", "strafe_L_armed", "strafe_R_armed")
STILL = ("idle_armed",)
KEEP_ROOT = ("attack_chop",)   # the scene roots the lunge on purpose

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
A = {x.name: x for x in bpy.data.actions}
BONES = [b.name for b in arm.pose.bones]
rep = {}


def sample(act):
    arm.animation_data.action = act
    f0, f1 = (int(round(v)) for v in act.frame_range)
    rows = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        rows.append(dict(
            f=f,
            basis={b: arm.pose.bones[b].matrix_basis.copy() for b in BONES},
            hips=(arm.matrix_world @ arm.pose.bones["Hips"].matrix).translation.copy(),
            lf=(arm.matrix_world @ arm.pose.bones["LeftFoot"].matrix).translation.z,
            rf=(arm.matrix_world @ arm.pose.bones["RightFoot"].matrix).translation.z))
    return rows, f0, f1


def onsets(rows, key):
    """Frames where a foot ARRIVES on the ground -- not every frame it is down.

    The threshold is RELATIVE to this clip's own foot range, not a fixed 0.05 m.
    A fixed one found no contacts at all in run_armed: its feet span 0.000 to
    0.104 m, so 0.05 sits mid-swing and the foot crosses it four times a stride
    in each direction. Adaptive, at the bottom third of the range, it finds the
    plants."""
    z = [r[key] for r in rows]
    lo, hi = min(z), max(z)
    thr = lo + 0.35 * (hi - lo)
    out, was = [], True
    for r in rows:
        down = r[key] < thr
        if down and not was:
            out.append(r["f"])
        was = down
    return out


def write(act, rows, idx, deroot, name):
    """Rebuild an action from sampled poses. deroot: kill horizontal root."""
    new = bpy.data.actions.new(name)
    new.use_fake_user = True
    arm.animation_data.action = new
    base = None
    for j, i in enumerate(idx):
        sc.frame_set(j)
        for b in BONES:
            pb = arm.pose.bones[b]
            pb.rotation_mode = 'QUATERNION'
            pb.matrix_basis = rows[i]["basis"][b].copy()
        bpy.context.view_layer.update()
        if deroot:
            # DE-ROOT IN ARMATURE SPACE, NOT BASIS SPACE. The first version
            # zeroed matrix_basis.translation.x/y, which is the bone's own REST
            # BASIS -- a rotated frame -- so the world drift survived it
            # untouched: idle_armed still drifted 0.8994 m and the lint still
            # flagged it. pose_bone.matrix is armature space, whose horizontal
            # axes are the world's.
            hb = arm.pose.bones["Hips"]
            m = hb.matrix.copy()
            if base is None:
                base = m.translation.copy()
            m.translation = Vector((base.x, base.y, m.translation.z))
            hb.matrix = m
            bpy.context.view_layer.update()
        for b in BONES:
            pb = arm.pose.bones[b]
            pb.keyframe_insert("rotation_quaternion", frame=j)
            if b == "Hips":
                pb.keyframe_insert("location", frame=j)
    return new


for nm in list(A):
    if nm not in LOCO + STILL + KEEP_ROOT:
        continue
    rows, f0, f1 = sample(A[nm])
    h0, h1 = rows[0]["hips"], rows[-1]["hips"]
    net = float(Vector((h1.x - h0.x, h1.y - h0.y, 0)).length)
    info = dict(frames_in=[f0, f1], net_root_travel_m=round(net, 4))
    if nm in KEEP_ROOT:
        info["action"] = "left rooted on purpose (the scene roots the lunge)"
        rep[nm] = info
        continue
    idx = list(range(len(rows)))
    if nm == "run_armed":
        on = onsets(rows, "lf") or onsets(rows, "rf")
        if len(on) >= 2:
            ia = on[0] - f0
            ib = on[1] - f0
            idx = list(range(ia, ib))
            c0, c1 = rows[ia]["hips"], rows[ib]["hips"]
            cyc = float(Vector((c1.x - c0.x, c1.y - c0.y, 0)).length)
            info["cycle_frames"] = ib - ia
            info["cycle_seconds"] = round((ib - ia) / FPS, 3)
            info["cycle_travel_m"] = round(cyc, 4)
            info["speed_m_s"] = round(cyc / max((ib - ia) / FPS, 1e-6), 3)
            info["contacts_found"] = on
            print("  %s: gait cycle %d..%d = %d frames (%.3f s), %.4f m, %.2f m/s"
                  % (nm, on[0], on[1], ib - ia, (ib - ia) / FPS, cyc, info["speed_m_s"]))
        else:
            print("  %s: could not find two same-foot contacts; left whole" % nm)
    if nm in LOCO and "speed_m_s" not in info:
        dur = (len(idx)) / FPS
        info["speed_m_s"] = round(net / max(dur, 1e-6), 3)
    old = A[nm]
    for t in list(arm.animation_data.nla_tracks):
        if any(s_.action is old for s_ in t.strips):
            arm.animation_data.nla_tracks.remove(t)
    new = write(old, rows, idx, True, nm + "__tmp")
    bpy.data.actions.remove(old)
    new.name = nm
    tr = arm.animation_data.nla_tracks.new()
    tr.name = nm
    tr.strips.new(nm, 0, new)
    info["frames_out"] = [int(round(v)) for v in new.frame_range]
    info["derooted"] = True
    rep[nm] = info
    print("  %-16s net root travel %.4f m -> in place; frames %s -> %s%s"
          % (nm, net, info["frames_in"], info["frames_out"],
             "  speed %.2f m/s" % info["speed_m_s"] if "speed_m_s" in info else ""))

for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=DST, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
import importlib
L = importlib.import_module("21_lint_export").lint(DST)
print("\nwrote %s (%.2f MB) LINT %s fails %d"
      % (DST, os.path.getsize(DST) / 1e6, L["verdict"], len(L["fails"])))
for w in L["warns"]:
    if "drifts" in w:
        print("  STILL DRIFTS: %s" % w.split("clip '")[1].split("'")[0])
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"], clips=sorted(L["clips"]))
assert not L["fails"]
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
