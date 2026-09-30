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
CONTACT = 0.05
# The sets were the barbarian's clip names, hard-coded. They are ARGUMENTS now (D7), with
# his as the defaults so his invocation is unchanged: --loco / --still / --keep-root.
def _set(flag, dflt):
    return tuple(a[a.index(flag) + 1].split(",")) if flag in a else dflt
LOCO = _set("--loco", ("walk_armed", "run_armed", "strafe_L_armed", "strafe_R_armed"))
STILL = _set("--still", ("idle_armed",))
KEEP_ROOT = _set("--keep-root", ("attack_chop",))   # the scene roots the lunge on purpose

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene
# FPS IS READ, NOT ASSUMED. A hard-coded 30.0 here (Blender's scene is 24) plus
# dividing by the KEY count instead of the INTERVAL count put run_armed's
# duration at 0.667 s when the shipped file says 0.7917, and its speed at 4.74
# m/s when it is 3.99 -- a 19% error, which is the foot slide the scene then
# measured. Durations below are (keys - 1) / fps, and the manifest's numbers
# are re-read from the shipped GLB afterwards by scripts/46_clip_timing.py.
FPS = float(sc.render.fps) / float(getattr(sc.render, 'fps_base', 1.0) or 1.0)
print("scene fps: %.4f" % FPS)
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
A = {x.name: x for x in bpy.data.actions}
BONES = [b.name for b in arm.pose.bones]
# the Hips' REST position in armature space -- the point every consumer stands the body on
_hl = arm.data.bones["Hips"].head_local
REST_XY = np.array([_hl.x, _hl.y])


def action_fcurves(act):
    """Every fcurve of an action, on either action API. Blender 4.4+ moved them into
    layers -> strips -> channelbags (slotted actions) and later removed Action.fcurves;
    this script has to run on the Blender that is installed, whichever that is."""
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []):
                out.extend(cb.fcurves)
    return out


def shift_root(act, dx, dy):
    """Move a clip RIGIDLY by a constant horizontal (armature-space) offset, without
    resampling anything: the delta is carried into the Hips bone's own BASIS space (for a
    root bone, armature translation = matrix_local.3x3 @ basis.location + matrix_local.t) and
    added to its location keys and their handles. Used for KEEP_ROOT clips, whose lunge
    must survive, so they START at the rest position instead of wherever the take began."""
    hb = arm.data.bones["Hips"]
    d = hb.matrix_local.to_3x3().inverted() @ Vector((dx, dy, 0.0))
    n = 0
    for fc in action_fcurves(act):
        if fc.data_path != 'pose.bones["Hips"].location':
            continue
        for kp in fc.keyframe_points:
            kp.co[1] += d[fc.array_index]
            kp.handle_left[1] += d[fc.array_index]
            kp.handle_right[1] += d[fc.array_index]
            n += 1
        fc.update()
    return n
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
            hips_arm=arm.pose.bones["Hips"].matrix.translation.copy(),
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
    # DE-ROOT REMOVES THE LINEAR TREND ONLY.
    #
    # The first version pinned the hips to their frame-0 horizontal position,
    # which took the net travel AND the sway with it: every armed clip came
    # back with 0.000 m of horizontal hip excursion against 0.060 and 0.039 for
    # the untouched unarmed walk and run. That sway is the weight shifting from
    # foot to foot; without it he glides. Subtracting a least-squares line over
    # the cycle removes the travel and leaves the oscillation.
    # The line is the FIRST-TO-LAST line, not a least-squares fit. A
    # least-squares line minimises total error but does not pass through the
    # endpoints, so the residual still ends somewhere other than where it
    # started: idle_armed came back with enough net travel left to trip the
    # drift rule again. The endpoint line makes residual[0] == residual[-1] by
    # construction, so net travel is exactly zero and the oscillation about it
    # is untouched.
    H = np.array([[rows[i]["hips_arm"].x, rows[i]["hips_arm"].y] for i in idx])
    t = np.linspace(0.0, 1.0, len(idx))[:, None]
    FIT = H[0][None, :] + (H[-1] - H[0])[None, :] * t
    # THE ANCHOR IS THE REST POSITION, NOT THE CLIP'S FIRST FRAME. (Fixed 2026-09-29, attack_lab.)
    # This used to add back FIT[0] -- wherever the clip happened to start -- so every clip was
    # de-rooted ABOUT ITS OWN STARTING POINT and shipped standing there: Meshy's Axe Stance
    # starts 1.135 m off, and run_armed's trimmed cycle came from 1.874 m along a travelling
    # take. Every consumer stands the body at the origin, so those clips were drawn a metre
    # or two away from his capsule and every blend in or out of them dragged him across the
    # ground (Matt's chop/attack glitch). The residual H - FIT is the sway with the travel
    # taken out; centring ITS MEAN on the rest position keeps the sway and puts the clip where
    # the body stands. 49_recentre.py and the lint's offset rule remain as guards; on this
    # script's output they find nothing to do.
    RESID = H - FIT
    ANCHOR = REST_XY - RESID.mean(axis=0)
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
            m.translation = Vector((m.translation.x - FIT[j][0] + ANCHOR[0],
                                    m.translation.y - FIT[j][1] + ANCHOR[1],
                                    m.translation.z))
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
        # the lunge is kept (the scene roots it) -- but the clip must START where the body
        # stands. attack_chop's take begins 0.487 m off; shift it rigidly to rest.
        a0 = rows[0]["hips_arm"]
        dx, dy = REST_XY[0] - a0.x, REST_XY[1] - a0.y
        keys = shift_root(A[nm], dx, dy)
        info["action"] = "left rooted on purpose (the scene roots the lunge); start moved to rest"
        info["start_shift_m"] = round(float(np.hypot(dx, dy) * arm.matrix_world.to_scale()[0]), 4)
        info["hips_location_keys_shifted"] = keys
        rep[nm] = info
        print("  %-16s rooted lunge kept; first frame moved %.4f m onto the rest position (%d keys)"
              % (nm, info["start_shift_m"], keys))
        continue
    idx = list(range(len(rows)))
    # only trim while the clip STILL has real travel -- a second pass over an
    # already-trimmed, already-de-rooted clip would find its two contacts and
    # cut it in half again
    if nm == "run_armed" and net > 0.5:
        on = onsets(rows, "lf") or onsets(rows, "rf")
        if len(on) >= 2:
            ia = on[0] - f0
            ib = on[1] - f0
            # INCLUSIVE of the closing contact. 20 keys spanning ia..ib-1 is
            # 19 intervals, but the cycle is 20 intervals long -- so the clip
            # declared 0.7917 s while its travel covered 0.8333 s, and any
            # consumer dividing one by the other got a speed 5% high. With the
            # closing key the declared duration IS the cycle period and the
            # last key repeats the first key's phase, which is how a loop is
            # normally authored anyway.
            idx = list(range(ia, ib + 1))
            c0, c1 = rows[ia]["hips"], rows[ib]["hips"]
            cyc = float(Vector((c1.x - c0.x, c1.y - c0.y, 0)).length)
            info["cycle_frames"] = ib - ia
            # (keys - 1) intervals, not keys
            info["cycle_keys"] = ib - ia + 1
            info["cycle_intervals"] = ib - ia
            info["cycle_seconds"] = round((ib - ia) / FPS, 4)
            info["cycle_travel_m"] = round(cyc, 4)
            info["speed_m_s"] = round(cyc / max((ib - ia) / FPS, 1e-6), 3)
            info["contacts_found"] = on
            print("  %s: gait cycle %d..%d = %d frames (%.3f s), %.4f m, %.2f m/s"
                  % (nm, on[0], on[1], ib - ia, (ib - ia) / FPS, cyc, info["speed_m_s"]))
        else:
            print("  %s: could not find two same-foot contacts; left whole" % nm)
    if nm in LOCO and "speed_m_s" not in info:
        dur = max(len(idx) - 1, 1) / FPS
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
