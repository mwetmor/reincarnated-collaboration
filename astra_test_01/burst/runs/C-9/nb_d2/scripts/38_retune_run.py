# Two finishing jobs, both decided by measurement.
#
#   blender -b -noaudio --python scripts/38_retune_run.py -- <merged.glb> <out.glb>
#        [--json f] [--alpha 0.6]
#
# (2) SOFTEN THE LOCK. alpha 0.95 put the armed walk at 3.4 deg/s -- twenty
#     times calmer than the idle Matt approved, which is a weld, not a grip.
#     Target: p95 roughly 40-70 deg/s with at most one reversal a cycle. The
#     old sweep was run against the UNARMED walk (baseline 209.5/5); these
#     clips start from Meshy's armed motion (68.8/3), so the numbers do not
#     transfer and the sweep is redone here.
#
# (3) A STRAIGHT ARMED RUN from the two diagonals. Phase-aligned on foot
#     contact, then blended 50/50. The test is whether the lateral components
#     cancel: a left-forward and a right-forward run averaged should travel
#     straight. Measured as the root's LATERAL drift and the planted foot's
#     slide -- a blend that looks fine and skates is the usual failure.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector, Quaternion
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("38_retune_run.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, DST = a[0], a[1]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ALPHA = float(a[a.index('--alpha') + 1]) if '--alpha' in a else 0.60
PAIRS = (("RightHand", "RightForeArm"), ("LeftHand", "LeftForeArm"))
FPS = 30.0


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


def survey(arm, act):
    sc = bpy.context.scene
    prev = arm.animation_data.action
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    tr = {p: [] for p in PAIRS}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        for p in PAIRS:
            tr[p].append(G.joint_rot(arm, *p))
    out = {}
    for p, qs in tr.items():
        rate = [ang(qs[i - 1].rotation_difference(qs[i])) * FPS
                for i in range(1, len(qs))]
        prof = [ang(q.rotation_difference(qs[0])) for q in qs]
        out["%s_in_%s" % p] = dict(p95=round(float(np.percentile(rate, 95)), 1),
                                   rev=int(revs(prof)))
    arm.animation_data.action = prev
    return out


def load():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=SRC)
    sc = bpy.context.scene
    arm = next(o for o in sc.objects if o.type == 'ARMATURE')
    body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
    for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
        bpy.data.objects.remove(o, do_unlink=True)
    return sc, arm, body


LOCKC = ("idle_armed", "walk_armed_m", "run_armed_L", "run_armed_R")
rep = dict(alpha_sweep={}, run_blend={})
sc, arm, body = load()
ACT = {x.name: x for x in bpy.data.actions}
print("ALPHA SWEEP on the armed clips (right wrist p95 / reversals)")
base = {c: survey(arm, ACT[c]) for c in LOCKC if c in ACT}
print("  %-14s %s" % ("alpha 0.00", " ".join(
    "%s %5.1f/%d" % (c, base[c]["RightHand_in_RightForeArm"]["p95"],
                     base[c]["RightHand_in_RightForeArm"]["rev"]) for c in base)))
rep["alpha_sweep"]["0.00"] = {c: base[c]["RightHand_in_RightForeArm"] for c in base}
for al in (0.30, 0.45, 0.60, 0.75):
    sc, arm, body = load()
    ACT = {x.name: x for x in bpy.data.actions}
    tg = {p: G.mean_joint_rot(arm, ACT["idle"], *p) for p in PAIRS}
    row = {}
    for c in LOCKC:
        if c not in ACT:
            continue
        for p in PAIRS:
            G.carry_lock(arm, ACT[c], p[0], p[1], tg[p], alpha=al)
        row[c] = survey(arm, ACT[c])["RightHand_in_RightForeArm"]
    rep["alpha_sweep"]["%.2f" % al] = row
    print("  %-14s %s" % ("alpha %.2f" % al, " ".join(
        "%s %5.1f/%d" % (c, row[c]["p95"], row[c]["rev"]) for c in row)))
print("  (the idle Matt approved: 71.2 / 1)")

# ---- the straight run ------------------------------------------------------
sc, arm, body = load()
ACT = {x.name: x for x in bpy.data.actions}
BONES = [b.name for b in arm.pose.bones]


def sample_act(act):
    sc.frame_set(0)
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    out = []
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        out.append({b: arm.pose.bones[b].matrix_basis.copy() for b in BONES})
    return out, f0, f1


def foot_low(act):
    """Frame of the deepest foot contact -- the phase anchor."""
    arm.animation_data.action = act
    f0, f1 = (int(round(x)) for x in act.frame_range)
    best, bf = 9e9, f0
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        z = min((arm.matrix_world @ arm.pose.bones[b].matrix).translation.z
                for b in ("LeftFoot", "RightFoot"))
        if z < best:
            best, bf = z, f
    return bf - f0


if "run_armed_L" in ACT and "run_armed_R" in ACT:
    pL, pR = foot_low(ACT["run_armed_L"]), foot_low(ACT["run_armed_R"])
    A, a0, a1 = sample_act(ACT["run_armed_L"])
    B, b0, b1 = sample_act(ACT["run_armed_R"])
    N = min(len(A), len(B))
    print("\nSTRAIGHT RUN from the two diagonals")
    print("  foot-contact phase: L at +%d, R at +%d -> shifting R by %d frames"
          % (pL, pR, pL - pR))
    new = ACT["run_armed_L"].copy()
    new.name = "run_armed_fwd"
    new.use_fake_user = True
    arm.animation_data.action = new
    for i in range(N):
        f = a0 + i
        j = (i + (pR - pL)) % len(B)
        sc.frame_set(f)
        for b in BONES:
            mA, mB = A[i][b], B[j][b]
            lA, qA, _ = mA.decompose()
            lB, qB, _ = mB.decompose()
            if qA.dot(qB) < 0:
                qB = -qB
            q = qA.slerp(qB, 0.5)
            pb = arm.pose.bones[b]
            pb.rotation_mode = 'QUATERNION'
            pb.matrix_basis = Matrix.Translation((lA + lB) * 0.5) @ q.to_matrix().to_4x4()
            pb.keyframe_insert("rotation_quaternion", frame=f)
            pb.keyframe_insert("location", frame=f)

    def drift(act):
        arm.animation_data.action = act
        f0, f1 = (int(round(x)) for x in act.frame_range)
        xs, fslide = [], []
        prev = None
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            h = (arm.matrix_world @ arm.pose.bones["Hips"].matrix).translation
            xs.append(float(h.x))
            lo = min((("LeftFoot", "RightFoot")),
                     key=lambda b: (arm.matrix_world @
                                    arm.pose.bones[b].matrix).translation.z)
            p = (arm.matrix_world @ arm.pose.bones[lo].matrix).translation
            z = float(p.z)
            if prev is not None and prev[0] == lo and z < 0.10:
                fslide.append(float((p.xy - prev[1]).length))
            prev = (lo, p.xy.copy())
        return (round(float(np.ptp(xs)), 4),
                round(float(np.mean(fslide)) if fslide else 0.0, 4))

    for nm in ("run_armed_L", "run_armed_R", "run_armed_fwd"):
        d, s_ = drift(ACT.get(nm) or new)
        rep["run_blend"][nm] = dict(lateral_drift_m=d, mean_foot_slide_m=s_)
        print("  %-15s lateral root drift %.4f m | mean planted-foot slide %.4f m"
              % (nm, d, s_))

    # IS IT ACTUALLY STRAIGHT? Lateral drift of the root cannot answer that.
    # These are in-place clips, so a diagonal run is diagonal in the BODY'S
    # FACING, not in travel -- and a facing error is exactly what a drift
    # metric cannot see. Measure the hips' forward axis against world forward.
    def yaw(act):
        arm.animation_data.action = act
        f0, f1 = (int(round(x)) for x in act.frame_range)
        ys = []
        for f in range(f0, f1 + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            m = (arm.matrix_world @ arm.pose.bones["Hips"].matrix).to_3x3()
            # the rig faces -Y; take the hips' own forward and read its yaw
            fwd = (m @ Vector((0, 0, 1))).normalized()
            ys.append(math.degrees(math.atan2(fwd.x, -fwd.y)))
        return round(float(np.mean(ys)), 2), round(float(np.ptp(ys)), 2)

    for nm in ("run_armed_L", "run_armed_R", "run_armed_fwd"):
        act = bpy.data.actions.get(nm) or new
        m_, r_ = yaw(act)
        rep["run_blend"].setdefault(nm, {}).update(mean_yaw_deg=m_, yaw_range_deg=r_)
        print("  %-15s mean body yaw %+7.2f deg (range %.2f)  %s"
              % (nm, m_, r_, "<- STRAIGHT" if abs(m_) < 8 else "<- still angled"))

# ---- final build, PER-CLIP alpha ------------------------------------------
# One alpha cannot serve all four: they start from different baselines, so the
# same blend lands them in different places. walk_armed_m is the awkward one --
# its rate is already inside the target band at alpha 0, and its THREE
# reversals are what needs removing, so any lock that fixes the reversals also
# pushes the rate below the band. Reversals win: that is the complaint metric.
PERCLIP = dict(idle_armed=0.75, walk_armed_m=0.45,
               run_armed_L=0.45, run_armed_R=0.60, run_armed_fwd=0.60)
tg = {p: G.mean_joint_rot(arm, ACT["idle"], *p) for p in PAIRS}
for c, al in PERCLIP.items():
    act = bpy.data.actions.get(c)
    if not act:
        continue
    for p in PAIRS:
        G.carry_lock(arm, act, p[0], p[1], tg[p], alpha=al)
    print("locked %-15s alpha %.2f -> %s" % (
        c, al, survey(arm, act)["RightHand_in_RightForeArm"]))
rep["final_alpha"] = PERCLIP
if "walk_armed" in bpy.data.actions and "walk_armed_m" in bpy.data.actions:
    bpy.data.actions["walk_armed"].name = "walk_armed_unarmedsrc"
    bpy.data.actions["walk_armed_m"].name = "walk_armed"
if "run_armed_fwd" in bpy.data.actions and "run_armed" in bpy.data.actions:
    bpy.data.actions["run_armed"].name = "run_armed_unarmedsrc"
    bpy.data.actions["run_armed_fwd"].name = "run_armed"
for act in bpy.data.actions:
    if not any(s.action is act for t in arm.animation_data.nla_tracks
               for s in t.strips):
        t = arm.animation_data.nla_tracks.new()
        t.name = act.name
        t.strips.new(act.name, int(round(act.frame_range[0])), act)
for t in list(arm.animation_data.nla_tracks):
    for s_ in t.strips:
        t.name = s_.action.name
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
importlib.import_module("52_weapon_bones").ensure(DST)  # T12: the base rig's weapon bones, after every export
L = importlib.import_module("21_lint_export").lint(DST)
print("\nwrote %s (%.2f MB)  LINT %s" % (DST, os.path.getsize(DST) / 1e6, L["verdict"]))
for f_ in L["fails"]:
    print("  FAIL %s" % f_)
print("  clips %s" % sorted(L["clips"]))
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"], clips=sorted(L["clips"]),
                   morphs=L["morphs"])
assert not L["fails"]
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
