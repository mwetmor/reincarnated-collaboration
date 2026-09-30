# Build the armed barbarian: merge the fetched Meshy clips, re-place the shield
# as a centre-grip shield, and author the guard layer.
#
#   blender -b -noaudio --python scripts/33_assemble.py -- <body.glb> <anims_dir>
#        <out.glb> [--json f] [--shield-out <shield.glb>]
#
# EVERY MERGED CLIP GOES THROUGH THE SAME HYGIENE as the originals: joint scale
# tracks stripped, and any clip that moves is re-grounded from its feet. Meshy's
# Idle shipped a 1.176471 Hips scale and it reached the player. These eleven get
# the same treatment on the way in, whatever the lint said about them.
#
# The shield gets BOTH corrections, because the grip alone is not the fix:
#   TRANSLATE  boss onto the fist (measured 0.4656 m; the fist was at 109.4% of
#              the radius, i.e. off the disc entirely)
#   ROTATE     face outward-and-forward at the guard pose, so in the S view it
#              reads as a shield held toward the enemy and not a plank at the
#              waist. Rotation is about the FIST, so it cannot undo the grip.
import bpy, glob, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector, Quaternion
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("33_assemble.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, ANIMS, OUT = a[0], a[1], a[2]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
SHOUT = a[a.index('--shield-out') + 1] if '--shield-out' in a else None
ROOT = os.path.dirname(HERE)
rep = dict(merged={}, hygiene={}, shield={}, guard={})

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
BD = body[0]
have = {x.name for x in bpy.data.actions}
print("body arrives with: %s" % sorted(have))

# ---- merge the fetched clips ----------------------------------------------
MERGE = json.load(open(os.path.join(ROOT, "work", "merge_plan.json")))
for nm, src in MERGE.items():
    p = os.path.join(ANIMS, "%s.glb" % src)
    if not os.path.exists(p):
        print("  (%s missing: %s)" % (nm, p))
        continue
    before = set(sc.objects)
    known = {x.name for x in bpy.data.actions}
    bpy.ops.import_scene.gltf(filepath=p)
    add = [o for o in sc.objects if o not in before]
    new = [x for x in bpy.data.actions if x.name not in known]
    if not new:
        print("  (%s brought no action)" % nm)
        for o in add:
            bpy.data.objects.remove(o, do_unlink=True)
        continue
    act = max(new, key=lambda x: x.frame_range[1] - x.frame_range[0])
    act.name = nm
    act.use_fake_user = True
    for o in add:
        bpy.data.objects.remove(o, do_unlink=True)
    for x in new:
        if x is not act:
            bpy.data.actions.remove(x)
    rep["merged"][nm] = dict(source=src,
                             frames=[int(round(v)) for v in act.frame_range])
    print("  merged %-14s from %-14s frames %s"
          % (nm, src, rep["merged"][nm]["frames"]))

# ---- hygiene on EVERYTHING -------------------------------------------------
st = G.strip_bone_scale(bpy.data.actions)
rep["hygiene"]["stripped"] = st
if st:
    print("  stripped joint scale tracks: %s" % json.dumps(st))
for act in [x for x in bpy.data.actions if x.name in st]:
    r = G.reground_from_feet(arm, body, act)
    rep["hygiene"].setdefault("grounded", {})[act.name] = r
    print("  re-grounded %-14s by %+.4f m, worst frame %.2f cm"
          % (act.name, r["dz"], r["after"]["worst_cm"]))
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()

# ---- the guard layer -------------------------------------------------------
GP = os.path.join(ROOT, "work", "guard_pose.json")
guard = json.load(open(GP)) if os.path.exists(GP) else {}


def apply_pose(pose_d, rigs):
    for A in rigs:
        for bn, flat in pose_d.items():
            if bn in A.pose.bones:
                A.pose.bones[bn].matrix_basis = Matrix(
                    [flat[i * 4:(i + 1) * 4] for i in range(4)])
    bpy.context.view_layer.update()


def clear_pose(rigs):
    for A in rigs:
        if A.animation_data:
            A.animation_data.action = None
        for pb in A.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()


# ---- the shield ------------------------------------------------------------
SH = SH_ARM = None
sp = os.path.join(ROOT, "export", "shield.glb")
if os.path.exists(sp):
    before = set(sc.objects)
    bpy.ops.import_scene.gltf(filepath=sp)
    add = [o for o in sc.objects if o not in before]
    SH = next(o for o in add if o.type == 'MESH' and o.vertex_groups)
    SH_ARM = next(o for o in add if o.type == 'ARMATURE')
    for o in [o for o in add if o.type == 'MESH' and o is not SH]:
        bpy.data.objects.remove(o, do_unlink=True)
    for x in [y for y in bpy.data.actions if y.name not in
              set(rep["merged"]) | have]:
        bpy.data.actions.remove(x)
RIGS = [arm] + ([SH_ARM] if SH_ARM else [])
kb = BD.data.shape_keys.key_blocks if BD.data.shape_keys else {}
for n_ in ("grip_L", "grip_R"):
    if n_ in kb:
        kb[n_].value = 1.0


def fist_c():
    gi = {vg.index: vg.name for vg in BD.vertex_groups}
    idx = [v.index for v in BD.data.vertices if v.groups and
           gi.get(max(v.groups, key=lambda x: x.weight).group) == "LeftHand"
           and max(v.groups, key=lambda x: x.weight).weight >= 0.30]
    return G.world_verts(BD)[idx].mean(axis=0)


def disc():
    V = G.world_verts(SH)
    c = V.mean(axis=0)
    ev, evec = np.linalg.eigh(np.cov((V - c).T))
    n = evec[:, 0] / np.linalg.norm(evec[:, 0])
    ip = evec[:, 1:]
    return c, n, ip, float(np.linalg.norm((V - c) @ ip, axis=1).max()), \
        float(np.ptp((V - c) @ n))


def inside(step=4):
    dg = bpy.context.evaluated_depsgraph_get()
    bt = BVHTree.FromObject(BD, dg)
    binv = BD.evaluated_get(dg).matrix_world.inverted()
    up = Vector((0.0, 0.0, 1.0))
    V = G.world_verts(SH)
    n_in = 0
    for q in V[::step]:
        o = binv @ Vector(q.tolist())
        h_, g_ = 0, 0
        while g_ < 24:
            g_ += 1
            hit = bt.ray_cast(o, up, 10.0)
            if hit[0] is None:
                break
            h_ += 1
            o = hit[0] + up * 1e-4
        if h_ % 2 == 1:
            n_in += 1
    return n_in, len(V[::step])


def bake(M4):
    """Apply a world-space 4x4 to the shield's vertex data, at the CURRENT pose.
    Only valid while the rig is at rest, where object space and world space
    differ by the object transform alone -- posed, the bone's rotation sits in
    the armature modifier and is not in matrix_world. That distinction cost a
    wrong answer earlier in this run (a 'centre grip' that measured 75.4% of
    the radius at the carry pose)."""
    co = np.empty(len(SH.data.vertices) * 3)
    SH.data.vertices.foreach_get("co", co)
    P = co.reshape(-1, 3)
    M = np.array(SH.matrix_world)
    R, t = M[:3, :3], M[:3, 3]
    W = P @ R.T + t
    A = np.array(M4)
    W2 = W @ A[:3, :3].T + A[:3, 3]
    SH.data.vertices.foreach_set("co", ((W2 - t) @ np.linalg.inv(R).T).ravel())
    SH.data.update()
    bpy.context.view_layer.update()


if SH is not None:
    clear_pose(RIGS)
    fc = fist_c()
    c, n, ip, rad, th = disc()
    spine = np.array((arm.matrix_world @ arm.pose.bones["Spine02"].matrix).translation)
    out_n = n if float(np.dot(c - spine, n)) > 0 else -n
    off0 = float(np.linalg.norm((fc - c) @ ip))
    stand = th * 0.5 + 0.02
    shift = (fc + out_n * stand) - c
    print("\nSHIELD radius %.4f m; fist was %.4f m from the boss = %.1f%% of radius"
          % (rad, off0, 100 * off0 / rad))
    base_pen = {}
    for tag, pd in (("rest", {}), ("carry", None), ("guard", guard)):
        if pd is None:
            cp = os.path.join(ROOT, "work", "carry_pose.json")
            pd = json.load(open(cp)) if os.path.exists(cp) else {}
        clear_pose(RIGS)
        if pd:
            apply_pose(pd, RIGS)
        base_pen[tag] = inside()[0]
    bake(Matrix.Translation(Vector(shift.tolist())))
    clear_pose(RIGS)
    print("  translated %.4f m: fist now %.1f%% of radius"
          % (float(np.linalg.norm(shift)),
             100 * float(np.linalg.norm((fist_c() - disc()[0]) @ disc()[2])) / rad))

    # ---- face it forward at the guard -------------------------------------
    if guard:
        clear_pose(RIGS)
        H0 = arm.pose.bones["LeftHand"].matrix.to_3x3().copy()
        apply_pose(guard, RIGS)
        H = arm.pose.bones["LeftHand"].matrix.to_3x3().copy()
        c2, n2, ip2, _, _ = disc()
        sp2 = np.array((arm.matrix_world @ arm.pose.bones["Spine02"].matrix).translation)
        now = Vector((n2 if float(np.dot(c2 - sp2, n2)) > 0 else -n2).tolist())
        # a shield in guard faces the enemy: forward (-Y here), canted outward
        want = Vector((0.30, -0.95, 0.08)); want.normalize()
        Rw = now.rotation_difference(want).to_matrix()
        R_hand = H.inverted() @ Rw @ H
        R_rest = H0 @ R_hand @ H0.inverted()
        rep["shield"]["face_before_world"] = [round(float(x), 4) for x in now]
        rep["shield"]["face_target_world"] = [round(float(x), 4) for x in want]
        rep["shield"]["turn_deg"] = round(math.degrees(now.angle(want)), 2)
        print("  face was %s, wants %s -- a %.1f deg turn"
              % ([round(float(x), 3) for x in now],
                 [round(float(x), 3) for x in want], math.degrees(now.angle(want))))
        clear_pose(RIGS)
        piv = Vector(fist_c().tolist())
        bake(Matrix.Translation(piv) @ R_rest.to_4x4() @ Matrix.Translation(-piv))
        apply_pose(guard, RIGS)
        c3, n3, ip3, _, _ = disc()
        sp3 = np.array((arm.matrix_world @ arm.pose.bones["Spine02"].matrix).translation)
        got = Vector((n3 if float(np.dot(c3 - sp3, n3)) > 0 else -n3).tolist())
        rep["shield"]["face_after_world"] = [round(float(x), 4) for x in got]
        rep["shield"]["residual_deg"] = round(math.degrees(got.angle(want)), 2)
        print("  after the turn the face is %s (%.2f deg off target)"
              % ([round(float(x), 3) for x in got], math.degrees(got.angle(want))))

    pen = {}
    for tag, pd in (("rest", {}), ("carry", None), ("guard", guard)):
        if pd is None:
            cp = os.path.join(ROOT, "work", "carry_pose.json")
            pd = json.load(open(cp)) if os.path.exists(cp) else {}
        clear_pose(RIGS)
        if pd:
            apply_pose(pd, RIGS)
        nin, samp = inside()
        fo = 100 * float(np.linalg.norm((fist_c() - disc()[0]) @ disc()[2])) / rad
        pen[tag] = dict(inside_before=base_pen[tag], inside_after=nin,
                        sampled=samp, fist_pct_radius=round(fo, 1))
        print("  %-5s: inside %d -> %d of %d sampled; fist at %.1f%% of radius"
              % (tag, base_pen[tag], nin, samp, fo))
    rep["shield"].update(radius_m=round(rad, 4), thickness_m=round(th, 4),
                         fist_before_pct=round(100 * off0 / rad, 1),
                         shift_m=round(float(np.linalg.norm(shift)), 4),
                         standoff_m=round(stand, 4), penetration=pen)
    clear_pose(RIGS)
    if SHOUT:
        bpy.ops.object.select_all(action='DESELECT')
        SH.select_set(True)
        SH_ARM.select_set(True)
        bpy.context.view_layer.objects.active = SH_ARM
        bpy.ops.export_scene.gltf(filepath=SHOUT, export_format='GLB',
                                  use_selection=True, export_animations=False,
                                  export_image_format='AUTO')
        print("  wrote %s (%.2f MB)" % (SHOUT, os.path.getsize(SHOUT) / 1e6))
    bpy.data.objects.remove(SH, do_unlink=True)
    bpy.data.objects.remove(SH_ARM, do_unlink=True)

# ---- guard as a layer, like shield_carry_L ---------------------------------
clear_pose([arm])
if guard:
    gact = bpy.data.actions.new("shield_guard_L")
    arm.animation_data.action = gact
    for f in (0, 1):
        sc.frame_set(f)
        for bn, flat in guard.items():
            pb = arm.pose.bones[bn]
            pb.matrix_basis = Matrix([flat[i * 4:(i + 1) * 4] for i in range(4)])
            pb.rotation_mode = 'QUATERNION'
            pb.keyframe_insert("rotation_quaternion", frame=f)
            pb.keyframe_insert("location", frame=f)
    gact.use_fake_user = True
    arm.animation_data.action = None
    clear_pose([arm])
    tr = arm.animation_data.nla_tracks.new()
    tr.name = "shield_guard_L"
    tr.strips.new("shield_guard_L", 0, gact)
    rep["guard"] = dict(bones=list(guard), clip="shield_guard_L")
    print("added shield_guard_L on %s" % list(guard))

for nm in rep["merged"]:
    act = bpy.data.actions.get(nm)
    if act and not any(s.action is act for t in arm.animation_data.nla_tracks
                       for s in t.strips):
        t = arm.animation_data.nla_tracks.new()
        t.name = nm
        t.strips.new(nm, int(round(act.frame_range[0])), act)

for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
arm.animation_data.action = None
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in body + [arm]:
    o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True,
                          export_animations=True, export_morph=True,
                          export_image_format='AUTO')
print("\nwrote %s (%.2f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
import importlib
L = importlib.import_module("21_lint_export").lint(OUT)
for f_ in L["fails"]:
    print("  LINT FAIL %s" % f_)
print("  LINT %s -- clips %s" % (L["verdict"], sorted(L["clips"])))
print("  morphs %s" % L["morphs"])
rep["lint"] = dict(verdict=L["verdict"], fails=L["fails"], clips=sorted(L["clips"]),
                   morphs=L["morphs"])
assert not L["fails"], "export lint failed"
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
    print("wrote %s" % OUTJ)
