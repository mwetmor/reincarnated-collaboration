# Acceptance measurement for a retargeted clip.
#
#   blender -b -noaudio --python scripts/42_qa_clip.py -- <body.glb> <clip>
#        [--ref run] [--json f]
#
# Five questions, five instruments, and the third one exists because a lateral
# drift metric already passed a run that was 32 degrees off heading:
#   foot slide  displacement of a foot that is in contact at BOTH ends of the
#               step. Contact at one end only is a foot landing or leaving, and
#               counting it reports skating that is not there.
#   heading     body yaw MINUS travel direction. Either alone is meaningless: a
#               character can face straight while travelling sideways, and
#               travel straight while facing sideways.
#   cadence     frames per stride against a reference clip, so it does not read
#               as slow motion beside his other locomotion.
#   wrist       reversals per cycle -- the waffle metric.
#   ground      lowest foot per frame, so it neither floats nor sinks.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("42_qa_clip.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY = a[0]
CLIPS = a[1].split(",")
REF = a[a.index('--ref') + 1] if '--ref' in a else "run"
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
FPS = 30.0
CONTACT = 0.05

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
MASK = {o.name: G.foot_verts(o) for o in body}
ACT = {x.name: x for x in bpy.data.actions}


def ang(q):
    return math.degrees(2.0 * math.acos(min(1.0, max(-1.0, abs(q.w)))))


def revs(seq):
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


def qa(cn):
    act = ACT[cn]
    arm.animation_data.action = act
    f0, f1 = (int(round(v)) for v in act.frame_range)
    rows = []
    wr = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        fp = {}
        for b in ("LeftFoot", "RightFoot"):
            p = (arm.matrix_world @ arm.pose.bones[b].matrix).translation
            fp[b] = Vector((p.x, p.y, p.z))
        hips = (arm.matrix_world @ arm.pose.bones["Hips"].matrix)
        lo = min(min(G.world_verts(o)[MASK[o.name]][:, 2]) for o in body
                 if len(MASK[o.name]))
        fwd = (hips.to_3x3() @ Vector((0, 0, 1))).normalized()
        rows.append(dict(f=f, feet=fp, root=hips.translation.copy(),
                         yaw=math.degrees(math.atan2(fwd.x, -fwd.y)), low=float(lo)))
        wr.append(G.joint_rot(arm, "RightHand", "RightForeArm"))
    # foot slide: contact at BOTH ends
    slide, nsl = [], 0
    for i in range(1, len(rows)):
        for b in ("LeftFoot", "RightFoot"):
            z0, z1 = rows[i - 1]["feet"][b].z, rows[i]["feet"][b].z
            if z0 < CONTACT and z1 < CONTACT:
                d = rows[i]["feet"][b] - rows[i - 1]["feet"][b]
                slide.append(float(Vector((d.x, d.y, 0)).length))
                nsl += 1
    trav = rows[-1]["root"] - rows[0]["root"]
    trav2 = Vector((trav.x, trav.y, 0))
    # A travel DIRECTION needs travel. walk_armed moves 0.004 m -- it is an
    # in-place clip -- and the direction of 4 mm of noise came back as a 176.64
    # degree heading error on a clip that is fine. Gate it: under 0.10 m there
    # is no direction to report, and reporting one is worse than reporting none.
    tdir = math.degrees(math.atan2(trav2.x, -trav2.y)) if trav2.length > 0.10 else None
    yaw = float(np.mean([r["yaw"] for r in rows]))
    # cadence: frames between successive contacts of the same foot
    cad = []
    for b in ("LeftFoot", "RightFoot"):
        on = [r["f"] for r in rows if r["feet"][b].z < CONTACT]
        gaps = [on[i] - on[i - 1] for i in range(1, len(on)) if on[i] - on[i - 1] > 2]
        cad += gaps
    rate = [ang(wr[i - 1].rotation_difference(wr[i])) * FPS for i in range(1, len(wr))]
    prof = [ang(q.rotation_difference(wr[0])) for q in wr]
    lows = [r["low"] for r in rows]
    return dict(
        frames=[f0, f1], seconds=round((f1 - f0 + 1) / FPS, 2),
        foot_slide_mean_m=round(float(np.mean(slide)) if slide else 0.0, 5),
        foot_slide_max_m=round(float(np.max(slide)) if slide else 0.0, 5),
        contact_steps=nsl,
        travel_m=round(float(trav2.length), 4),
        body_yaw_deg=round(yaw, 2),
        travel_dir_deg=(round(tdir, 2) if tdir is not None else None),
        heading_error_deg=(round(abs(yaw - tdir), 2) if tdir is not None else None),
        stride_frames=round(float(np.mean(cad)), 1) if cad else None,
        wrist_p95=round(float(np.percentile(rate, 95)), 1),
        wrist_reversals=int(revs(prof)),
        foot_low_min=round(min(lows), 4), foot_low_max=round(max(lows), 4))


out = {}
for cn in CLIPS + ([REF] if REF not in CLIPS else []):
    if cn not in ACT:
        print("  (no clip %s)" % cn)
        continue
    out[cn] = qa(cn)
    r = out[cn]
    print("%-18s %4.1fs slide mean %.5f max %.5f (%d contacts) | travel %.3f m "
          "yaw %+7.2f dir %s err %s | stride %s fr | wrist %5.1f/%d | foot %.3f..%.3f"
          % (cn, r["seconds"], r["foot_slide_mean_m"], r["foot_slide_max_m"],
             r["contact_steps"], r["travel_m"], r["body_yaw_deg"],
             r["travel_dir_deg"], r["heading_error_deg"], r["stride_frames"],
             r["wrist_p95"], r["wrist_reversals"], r["foot_low_min"],
             r["foot_low_max"]))
if OUTJ:
    json.dump(out, open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
