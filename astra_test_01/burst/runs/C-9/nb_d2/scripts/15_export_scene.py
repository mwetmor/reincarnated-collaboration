# D2 step 3: export the assembled character for the 3D cliffside.
#
#   blender -b -noaudio --python scripts/15_export_scene.py -- <clip.glb>
#     <bodytex.png> <outdir> --gear "<same spec as 10_swap>" [--height 1.85]
#
# ONE assembled scene, then one export per piece plus one for the body. Pieces
# are never exported alone and re-imported: Meshy ships the body at 0.01 object
# scale, and a piece built in metres and parented to that armature collapses to
# a 1.7 cm speck -- in the FILE. Everything here is fitted in this session and
# written out with the body's transform already baked in.
#
# The body carries the `helmet_on` shape key, so the consumer toggles the
# helmet and the hair compresses with it: reversible, and no repaint.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath(
    [x for x in sys.argv if x.endswith("15_export_scene.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
CLIP, TEX, OUT = a[0], a[1], a[2]
SPEC = a[a.index("--gear") + 1] if "--gear" in a else ""
HGT = float(a[a.index("--height") + 1]) if "--height" in a else 1.85
ROOT = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CLIP)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
img = bpy.data.images.load(os.path.abspath(TEX))
for o in body:
    for s_ in o.material_slots:
        if s_.material and s_.material.node_tree:
            for nd in s_.material.node_tree.nodes:
                if nd.type == 'TEX_IMAGE':
                    nd.image = img
                    nd.image.colorspace_settings.name = 'sRGB'
# REST POSE BEFORE FITTING. socket_weapon2 and bone_bind read the bone's
# POSED head, and a glTF import leaves the armature on whatever action it
# picked -- so a piece could be bound against frame 1 of some clip instead of
# the rest pose. Two baselines of the same shield disagreed (idle 3 against
# 117) and that disagreement is the only reason it was found.
arm.animation_data.action = None
for _pb in arm.pose.bones:
    _pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
BV, BT, names, W, tree = G.body_sampler(body[0])
PIECE_REF_H = 1.70                # the rig the pieces were isolated against
BH_NOW = float(BV[:, 2].max() - BV[:, 2].min())
PSCALE = BH_NOW / PIECE_REF_H
print("body is %.4f m; pieces were built against %.2f m -> scaling each by "
      "x%.5f" % (BH_NOW, PIECE_REF_H, PSCALE))
made_all, manifest = [], []
SPECS = dict(axe=dict(axis_world=(0, 0, 1), face_world=(0, -1, 0)),
             # Chosen by sweep against the posed body mesh across all four
             # clips (scripts/16_shield_clear.py). Offset is outward 0.20,
             # forward 0.18, down 0.13 in the forearm's rest frame; the 0.70
             # tilt lays the disc's normal back so its rim sweeps past him
             # rather than through him. Idle 110 -> 3 vertices inside, attack
             # 196 -> 111, walk 285 -> 264. The RUN does not respond: see the
             # report -- his elbow is 0.37-0.47 m from the spine and this
             # shield's radius is 0.41 m, so the rim reaches the torso whatever
             # the bind does, and the run's arm swing rolls the disc through
             # him. That needs a smaller shield or a different run clip.
             # THE SHIELD IS BOUND IN THE CARRY POSE, to LeftHand. A rest-pose
             # bind is the wrong bind for a carried shield: socketed at rest and
             # then carried, the forearm swings across his chest and takes the
             # disc with it (idle 117 -> 277 vertices inside). Bound in the pose
             # it is carried in, with its normal outward-and-forward at that
             # moment, the layer clears him: walk 313 -> 3, run 389 -> 14.
             shield=dict(axis_world=(0.50, -0.87, 0.0), face_world=(0, 0, 1),
                         offset_world=(0.02, -0.06, 0.0), anchor="normal"))
for item in [x for x in SPEC.split(",") if x]:
    parts = item.split(":")
    nm, mode = parts[0], parts[1]
    bones = parts[2].split("|") if len(parts) > 2 and parts[2] else []
    split = len(parts) > 3 and parts[3] == "split"
    faces = dict(helmet=12000, bracers=12000, byrnie=26000, mantle=24000,
                 axe=9000, shield=9000).get(nm, 16000)
    offs = dict(helmet=0.0, bracers=0.002, byrnie=0.005, mantle=0.008,
                axe=0.0, shield=0.0).get(nm, 0.004)
    CARRY = None
    if nm == "shield" and os.path.exists(os.path.join(ROOT, "work", "carry_pose.json")):
        CARRY = json.load(open(os.path.join(ROOT, "work", "carry_pose.json")))
        for bn, flat in CARRY.items():
            arm.pose.bones[bn].matrix_basis = Matrix(
                [flat[i * 4:(i + 1) * 4] for i in range(4)])
        bpy.context.view_layer.update()
        print("   posed the left arm to shield_carry_L before socketing")
    before = set(sc.objects)
    src = "builds" if mode == "socket" else "pieces"
    pc = G.import_piece(os.path.join(ROOT, src, "%s.glb" % nm), before)
    if mode != "socket":
        G.rescale_piece(pc, PSCALE)       # sockets are sized from --length
    G.decimate(pc, faces)
    if offs > 0:
        P, pushed = G.clear_body(pc, tree, offs)
    else:
        co = np.empty(len(pc.data.vertices) * 3)
        pc.data.vertices.foreach_get("co", co)
        P, pushed = co.reshape(-1, 3), 0
    if mode == "socket":
        ln = float(parts[3]) if len(parts) > 3 else 0.82
        gr = float(parts[4]) if len(parts) > 4 else 0.3
        info = G.socket_weapon2(pc, arm, bones[0], ln, gr, **SPECS[nm])
        G.align_space(pc, body[0])
        made = [(pc, bones[0])]
    elif mode == "skin":
        G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
        G.align_space(pc, body[0])
        made = [(pc, "skinned")]
    else:
        made = G.bone_bind(pc, arm, bones, split)
        for o, _ in made:
            G.align_space(o, body[0])
    if nm == "axe":
        e, ep, nedge = G.axe_edge_marker(pc, arm, bones[0])
        print("   axe_edge empty at %s from %d edge vertices"
              % (np.round(ep, 4).tolist(), nedge))
        manifest_extra = dict(edge_marker="axe_edge",
                              edge_world=[round(float(v), 4) for v in ep])
    if nm == "axe":
        _off = G.centre_shaft_on_fist(pc, body[0], arm, bones[0])
        print("   axe shaft moved %.4f m to pass through the fist" % _off)
    if CARRY:
        for pbx in arm.pose.bones:
            pbx.matrix_basis = Matrix.Identity(4)
        bpy.context.view_layer.update()
    if nm == "helmet":
        mv, ca, kk = G.helmet_on_key(body[0], made[0][0], arm)
        kk.value = 0.0                    # OFF by default; the consumer sets it
        print("   helmet_on key on the body: %d of %d vertices" % (mv, ca))
    for i, (o, b) in enumerate(made):
        o.name = "%s_%02d" % (nm, i) if len(made) > 1 else nm
    made_all.append((nm, mode, made))
    entry = dict(piece=nm, mode=mode, bones=[b for _, b in made],
                 objects=[o.name for o, _ in made], faces=faces,
                 offset_m=offs, glb="%s.glb" % nm)
    if nm == "axe":
        entry.update(manifest_extra)
    manifest.append(entry)
    print("  + %-8s %-6s %d object(s)" % (nm, mode, len(made)))

# scale the whole assembly to the declared height, measured on the BODY
co = np.empty(len(body[0].data.vertices) * 3)
body[0].data.vertices.foreach_get("co", co)
BW = (co.reshape(-1, 3) @ np.array(body[0].matrix_world.to_3x3()).T
      + np.array(body[0].matrix_world.translation))
H0 = float(BW[:, 2].max() - BW[:, 2].min())
s = HGT / H0
for o in list(sc.objects):
    if o.parent is None:
        o.matrix_world = Matrix.Scale(s, 4) @ o.matrix_world
bpy.context.view_layer.update()
print("scaled x%.5f: body height %.4f -> %.4f m" % (s, H0, H0 * s))


def export(objs, path, anim=False, extra=()):
    bpy.ops.object.select_all(action='DESELECT')
    for o in list(objs) + list(extra):
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB',
                              use_selection=True, export_animations=anim,
                              export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


# ---- grip morphs: close the hands round the weapons ------------------------
# The rig has 24 bones and NO FINGERS, so the hands cannot be posed and Meshy
# ships them open and flat. An open flat hand cannot hold anything however
# perfectly the weapon is bound -- and the binding was already right (axe 100%
# RightHand, shield 100% LeftHand, zero multi-group vertices). So the hands are
# closed with morphs, driven by the equipment like helmet_on.
_made = {nm: (m[0][0], m[0][1]) for nm, mode, m in made_all if mode == "socket"}
for _nm, _key, _bone in (("axe", "grip_R", "RightHand"),
                         ("shield", "grip_L", "LeftHand")):
    if _nm not in _made:
        continue
    _pc = _made[_nm][0]
    if _nm == "shield" and CARRY:
        for bn, flat in CARRY.items():
            arm.pose.bones[bn].matrix_basis = Matrix(
                [flat[i * 4:(i + 1) * 4] for i in range(4)])
        bpy.context.view_layer.update()
    _c, _chan, _al, _pal = G.hand_frame(body[0], arm, _bone)
    if _nm == "axe":
        _r, _ = G.shaft_radius(_pc, arm, _bone)
        _r = float(min(max(_r, 0.012), 0.028))
    else:
        _r = 0.016
    _k, _mv, _mx = G.grip_key(body[0], arm, _bone, _c, _chan, _r + 0.010, _key)
    if _k:
        _k.value = 0.0                    # OFF by default; the scene drives it
    print("   %s: closes to %.4f m, %d vertices moved, max %.4f m"
          % (_key, _r + 0.010, _mv, _mx))
    if _nm == "shield":
        # closing the left fist pulls it OFF the shield -- the disc has no bar
        # where the hand is, so the fingers close on air and the minimum gap
        # goes 0 -> 15 mm. The hand is now the right shape, so the shield comes
        # to meet it. Both sides measured POSED: comparing the shield's bind
        # data against a posed fist computed 0.9 mm for a 15 mm gap.
        _k.value = 1.0
        bpy.context.view_layer.update()
        _dg = bpy.context.evaluated_depsgraph_get()
        _eb = body[0].evaluated_get(_dg); _me = _eb.to_mesh()
        _cv = np.empty(len(_me.vertices) * 3); _me.vertices.foreach_get("co", _cv)
        _BW = (_cv.reshape(-1, 3) @ np.array(_eb.matrix_world.to_3x3()).T
               + np.array(_eb.matrix_world.translation))
        _eb.to_mesh_clear()
        _gi = body[0].vertex_groups[_bone].index
        _hand = [v.index for v in body[0].data.vertices
                 if any(g.group == _gi and g.weight > 0.30 for g in v.groups)]
        _fist = _BW[_hand]
        _eo = _pc.evaluated_get(_dg); _m2 = _eo.to_mesh()
        _sv = np.empty(len(_m2.vertices) * 3); _m2.vertices.foreach_get("co", _sv)
        _SWp = (_sv.reshape(-1, 3) @ np.array(_eo.matrix_world.to_3x3()).T
                + np.array(_eo.matrix_world.translation))
        _eo.to_mesh_clear()
        _d = np.linalg.norm(_SWp[::4, None, :] - _fist[None, ::12, :], axis=2)
        _i, _j = np.unravel_index(np.argmin(_d), _d.shape)
        _dp = _fist[::12][_j] - _SWp[::4][_i]
        _pbL = arm.pose.bones[_bone]
        _Rp = arm.matrix_world.to_3x3() @ _pbL.matrix.to_3x3()
        _Rr = arm.matrix_world.to_3x3() @ _pbL.bone.matrix_local.to_3x3()
        _st = np.array((_Rr @ _Rp.inverted() @ Vector(_dp.tolist())).to_tuple()) * 0.92
        _co2 = np.empty(len(_pc.data.vertices) * 3)
        _pc.data.vertices.foreach_get("co", _co2)
        _Pp = _co2.reshape(-1, 3)
        _Wp = (_Pp @ np.array(_pc.matrix_world.to_3x3()).T
               + np.array(_pc.matrix_world.translation)) + _st
        _Mi2 = _pc.matrix_world.inverted()
        _pc.data.vertices.foreach_set(
            "co", (_Wp @ np.array(_Mi2.to_3x3()).T + np.array(_Mi2.translation)).ravel())
        _pc.data.update()
        print("   shield nudged %.4f m to meet the closed fist"
              % float(np.linalg.norm(_st)))
        _k.value = 0.0
    if _nm == "shield" and CARRY:
        for pbx in arm.pose.bones:
            pbx.matrix_basis = Matrix.Identity(4)
        bpy.context.view_layer.update()

# the shield's arm layer, authored in scripts/17_shield_carry.py and passed in
# as pose matrices so the search is not repeated and so this script -- the one
# that also builds helmet_on -- is the single source of the finished body.
CP = os.path.join(ROOT, "work", "carry_pose.json")
if os.path.exists(CP):
    cp = json.load(open(CP))
    cact = bpy.data.actions.new("shield_carry_L")
    prev = arm.animation_data.action if arm.animation_data else None
    arm.animation_data.action = cact
    for f in (0, 1):
        sc.frame_set(f)
        for bn, flat in cp.items():
            pbx = arm.pose.bones[bn]
            pbx.matrix_basis = Matrix([flat[i * 4:(i + 1) * 4] for i in range(4)])
            pbx.rotation_mode = 'QUATERNION'
            pbx.keyframe_insert("rotation_quaternion", frame=f)
            pbx.keyframe_insert("location", frame=f)
    cact.use_fake_user = True
    arm.animation_data.action = prev
    for pbx in arm.pose.bones:
        pbx.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    tr = arm.animation_data.nla_tracks.new()
    tr.name = "shield_carry_L"
    tr.strips.new("shield_carry_L", 0, cact)
    print("added shield_carry_L on %s" % list(cp))

mb = export(body, os.path.join(OUT, "nb-body.glb"), anim=True)
print("wrote nb-body.glb (%.2f MB) with the helmet_on morph and the clips" % mb)
edge_empty = bpy.data.objects.get("axe_edge")
for nm, mode, made in made_all:
    p = os.path.join(OUT, "%s.glb" % nm)
    sz = export([o for o, _ in made], p,
                extra=[edge_empty] if (nm == "axe" and edge_empty) else ())
    print("wrote %-12s %.2f MB" % (os.path.basename(p), sz))
json.dump(dict(body="nb-body.glb", height_m=HGT, scale_applied=round(float(s), 6),
               facing="-Y", his_right="-X", up="+Z",
               body_shape_keys=["helmet_on"],
               binding_note=("every piece, sockets included, is a SKINNED mesh "
                             "on the same 24 bones; the scene binds all of them "
                             "to the body's Skeleton3D"),
               helmet_on="set to 1 when the helmet is equipped, 0 when removed",
               layer_order=["body", "byrnie", "mantle", "bracers", "helmet",
                            "shield", "axe"],
               world_scale_rule=dict(factor=1.25178,
                                     world_height_m=round(HGT * 1.25178, 5)),
               pieces=manifest), open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
print("wrote manifest.json")
