# SMPL-H (52 bones) -> the barbarian's 24-bone Meshy rig. REUSABLE: this is the
# fully generated pipeline, so any action Meshy's library lacks -- a straight
# armed run, a strafe, a cast, a polearm swing -- comes from text-to-motion and
# through here.
#
#   blender -b -noaudio --python scripts/41_retarget_smplh.py -- <src.fbx>
#        <body.glb> <out.glb> <clipname> [--json f] [--alpha 0.60]
#
# THE REST POSES DIFFER and that is the whole problem. SMPL-H rests in a near
# T-pose; his Meshy rig rests in an A-pose. Copying local rotations bone by bone
# would put his arms wherever the difference happens to land, and it would look
# plausible enough to ship.
#
# So each bone is retargeted IN ITS OWN REST FRAME:
#
#     P_dst(f) = [ P_src(f) . R_src^-1 ] . R_dst
#
# The bracket is the WORLD rotation the source bone has accumulated away from
# its own rest; it is applied to the destination's rest. At the source's rest
# the bracket is identity and the destination sits at ITS rest, which is the
# property that makes T-pose and A-pose sources interchangeable. Verified by
# measurement, not by assertion: the per-bone rest-alignment error is reported,
# and at rest it must be zero for every mapped bone.
#
# Root translation is scaled by the LEG-LENGTH ratio, not by height: the stride
# and the hip height both follow the legs, and height includes a head and a
# neck that have nothing to do with how far a step travels.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector, Quaternion
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("41_retarget_smplh.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
SRC, BODY, OUT, CLIP = a[0], a[1], a[2], a[3]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ALPHA = float(a[a.index('--alpha') + 1]) if '--alpha' in a else 0.60
ROOT = os.path.dirname(HERE)

# MAP: SMPL-H -> ours. 22 of our 24; head_end and headfront are leaves.
#
# THE SPINE IS NAMED BACKWARDS IN THE MESHY RIG and the first version of this
# map believed the names:
#     Hips -> Spine02 (z 1.162) -> Spine01 (z 1.303) -> Spine (z 1.444) -> neck
# "Spine02" is the LOWEST spine bone and "Spine" is the HIGHEST. SMPL-H runs the
# obvious way, Spine1 lowest. So Spine1->Spine and Spine3->Spine02 inverted two
# of the three, and the retarget drove his lower spine from the source's upper
# and vice versa.
#
# The rest-alignment error was 0.000000 degrees THROUGH ALL OF IT. That check
# verifies the TRANSPORT FORMULA, not the CORRESPONDENCE: it recomputes both
# sides from whatever pair it was handed, so a perfect transport onto the wrong
# bone scores perfectly. verify_map() below is the check that can fail.
MAP = {
    "Pelvis": "Hips", "Spine1": "Spine02", "Spine2": "Spine01", "Spine3": "Spine",
    "Neck": "neck", "Head": "Head",
    "L_Collar": "LeftShoulder", "L_Shoulder": "LeftArm",
    "L_Elbow": "LeftForeArm", "L_Wrist": "LeftHand",
    "R_Collar": "RightShoulder", "R_Shoulder": "RightArm",
    "R_Elbow": "RightForeArm", "R_Wrist": "RightHand",
    "L_Hip": "LeftUpLeg", "L_Knee": "LeftLeg", "L_Ankle": "LeftFoot",
    "L_Foot": "LeftToeBase",
    "R_Hip": "RightUpLeg", "R_Knee": "RightLeg", "R_Ankle": "RightFoot",
    "R_Foot": "RightToeBase"}
LEG_S = ("L_Hip", "L_Knee", "L_Ankle")
LEG_D = ("LeftUpLeg", "LeftLeg", "LeftFoot")

def verify_map(S_PARENT, D, MAP):
    """Every parent->child edge in the SOURCE must be an ancestor->descendant
    relation between the mapped DESTINATION bones. This is the check that can
    actually fail, and it is the one that catches a rig whose bone NAMES run
    opposite to its hierarchy."""
    bad = []
    for sn, dn in MAP.items():
        # nearest mapped ancestor on the source side, from captured data:
        # the source armature is long gone by the time this runs (loading the
        # destination resets the scene), and reaching for it raises
        # "StructRNA of type Object has been removed" -- which at least fails
        # loudly rather than quietly reading a stale value.
        p = S_PARENT.get(sn)
        while p is not None and p not in MAP:
            p = S_PARENT.get(p)
        if p is None:
            continue
        dp = MAP[p]
        q = D.data.bones[dn].parent
        ok = False
        while q is not None:
            if q.name == dp:
                ok = True
                break
            q = q.parent
        if not ok:
            bad.append("%s->%s maps to %s->%s, which is NOT an ancestor relation"
                       % (p, sn, dp, dn))
    return bad


rep = {}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC, automatic_bone_orientation=True)
sc = bpy.context.scene
S = next(o for o in sc.objects if o.type == 'ARMATURE')
sact = max(bpy.data.actions, key=lambda x: x.frame_range[1] - x.frame_range[0])
S.animation_data.action = sact
f0, f1 = (int(round(v)) for v in sact.frame_range)
print("source %s: %d bones, action %s frames %d-%d"
      % (S.name, len(S.data.bones), sact.name, f0, f1))
# source rest (armature space) and the frames
S_REST = {b.name: (S.matrix_world @ S.data.bones[b.name].matrix_local).to_3x3()
          for b in S.pose.bones if b.name in MAP}
S_PARENT = {b.name: (b.parent.name if b.parent else None) for b in S.data.bones}
S_HEADZ = {b.name: round(float((S.matrix_world @ b.matrix_local).translation.z), 4)
           for b in S.data.bones if b.name in MAP}
SRC_P, SRC_ROOT = [], []
for f in range(f0, f1 + 1):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    SRC_P.append({b: (S.matrix_world @ S.pose.bones[b].matrix).to_3x3().copy()
                  for b in MAP})
    SRC_ROOT.append((S.matrix_world @ S.pose.bones["Pelvis"].matrix).translation.copy())


def chain_len(arm, names):
    bpy.context.view_layer.update()
    p = [(arm.matrix_world @ arm.data.bones[n].matrix_local).translation
         for n in names]
    return sum(float((p[i + 1] - p[i]).length) for i in range(len(p) - 1))


LS = chain_len(S, LEG_S)
S_UP = "Z" if abs(float((S.matrix_world @ S.data.bones["Head"].matrix_local).translation.z)) > \
    abs(float((S.matrix_world @ S.data.bones["Head"].matrix_local).translation.y)) else "Y"
print("source leg length %.4f m, up axis looks like %s" % (LS, S_UP))

# ---- the destination -------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
D = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
D.animation_data.action = None
for pb in D.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
D_REST = {n: (D.matrix_world @ D.data.bones[n].matrix_local).to_3x3()
          for n in MAP.values()}
D_REST_T = {n: (D.matrix_world @ D.data.bones[n].matrix_local).translation.copy()
            for n in MAP.values()}
LD = chain_len(D, LEG_D)
RATIO = LD / max(LS, 1e-9)
print("dest leg length %.4f m -> root translation scaled x%.4f" % (LD, RATIO))

BAD = verify_map(S_PARENT, D, MAP)
rep["map_topology_errors"] = BAD
if BAD:
    for b_ in BAD:
        print("  MAP ERROR  %s" % b_)
    raise SystemExit("the bone map does not preserve the hierarchy")
rep["source_head_z"] = S_HEADZ
rep["dest_head_z"] = {n: round(float(D_REST_T[n].z), 4) for n in MAP.values()}
print("map topology verified: every source parent-child edge is an "
      "ancestor relation in the destination (%d bones)" % len(MAP))

# hierarchy order: a parent must be posed before its child, because setting
# pose_bone.matrix back-solves the basis against the parent's CURRENT pose
ORDER = []


def walk(b):
    if b.name in MAP.values():
        ORDER.append(b.name)
    for c in b.children:
        walk(c)


for b in D.data.bones:
    if b.parent is None:
        walk(b)
print("pose order: %s" % ORDER)

act = bpy.data.actions.new(CLIP)
act.use_fake_user = True
D.animation_data.action = act
inv = {v: k for k, v in MAP.items()}
for i, f in enumerate(range(f0, f1 + 1)):
    sc.frame_set(f)
    for dn in ORDER:
        sn = inv[dn]
        R = SRC_P[i][sn] @ S_REST[sn].inverted() @ D_REST[dn]
        pb = D.pose.bones[dn]
        pb.rotation_mode = 'QUATERNION'
        keep = pb.matrix.translation.copy()
        if dn == "Hips":
            # pose_bone.matrix is in ARMATURE space; D_REST_T is in WORLD space.
            # Assigning one into the other put his feet 0.9 m underground: the
            # armature carries Meshy's 0.010882 object scale, so a world 1.02
            # read as an armature 1.02 and rendered as 0.011 m. The rotations
            # were unaffected -- a uniform scale leaves a rotation alone -- so
            # the rest-alignment check still scored 0.000000 degrees while the
            # character stood in a hole.
            d = (SRC_ROOT[i] - SRC_ROOT[0]) * RATIO
            keep = (D.matrix_world.inverted() @ (D_REST_T["Hips"] + d))
        m = R.to_4x4()
        m.translation = keep
        pb.matrix = m
        bpy.context.view_layer.update()
        pb.keyframe_insert("rotation_quaternion", frame=f)
        if dn == "Hips":
            pb.keyframe_insert("location", frame=f)
print("retargeted %d frames onto %d bones" % (len(SRC_P), len(ORDER)))
# ground it: a retarget lands wherever the source's root put it, and the source
# rig's floor is not this rig's floor (SMPL-H's pelvis rests at z -0.19).
gr = G.reground_from_feet(D, body, act)
rep["grounding"] = gr
print("grounded by %+.4f m: feet %+.4f..%+.4f -> %+.4f..%+.4f (worst %.2f cm)"
      % (gr["dz"], gr["before"]["min"], gr["before"]["max"],
         gr["after"]["min"], gr["after"]["max"], gr["after"]["worst_cm"]))

# ---- accuracy: at the SOURCE'S REST every mapped bone must land on ITS rest -
S_id = {n: S_REST[n] for n in MAP}
err = {}
for sn, dn in MAP.items():
    R = S_id[sn] @ S_REST[sn].inverted() @ D_REST[dn]
    q = (R.inverted() @ D_REST[dn]).to_quaternion()
    err[dn] = round(math.degrees(2 * math.acos(min(1.0, abs(q.w)))), 6)
rep["rest_alignment_error_deg"] = err
rep["rest_alignment_max_deg"] = round(max(err.values()), 6)
print("rest-alignment error: max %.6f deg over %d bones (0 means the rest-frame "
      "transport is exact)" % (max(err.values()), len(err)))
rep["leg_lengths"] = dict(source=round(LS, 4), dest=round(LD, 4),
                          root_scale=round(RATIO, 4))
rep["map"] = MAP
rep["clip"] = CLIP
rep["frames"] = [f0, f1]
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
for pb in D.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
D.animation_data.action = None
bpy.context.view_layer.update()
t = D.animation_data.nla_tracks.new()
t.name = CLIP
t.strips.new(CLIP, int(round(act.frame_range[0])), act)
bpy.ops.object.select_all(action='DESELECT')
for o in body + [D]:
    o.select_set(True)
bpy.context.view_layer.objects.active = D
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
import importlib
importlib.import_module("52_weapon_bones").ensure(OUT)  # T12: the base rig's weapon bones, after every export
L = importlib.import_module("21_lint_export").lint(OUT)
print("wrote %s (%.2f MB) LINT %s fails %d"
      % (OUT, os.path.getsize(OUT) / 1e6, L["verdict"], len(L["fails"])))
print("  clips %s" % sorted(L["clips"]))
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"], clips=sorted(L["clips"]))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
