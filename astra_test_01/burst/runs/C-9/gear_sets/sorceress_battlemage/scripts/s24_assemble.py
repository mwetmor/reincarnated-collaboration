# R-C9-98 stage 2: fit the battle-mage set onto her SHIPPED body (so_d7/export/so-body.glb, read-only) the gear way and
# export one skinned GLB per piece on her 26 joints. THE BODY IS NOT RE-EXPORTED: it carries binary-patched clips and
# channels, and a Blender round trip has resampled and reordered clips before (55_clip_graft's warning). Every piece
# is exported with the same armature, so the scene binds it exactly as gear.gd binds the D7 costume.
#
#   blender -b -noaudio --python s24_assemble.py -- <so-body.glb> <pieces_dir> <builds_dir> <staff.glb> <out_dir> [--json f]
#
#   deforming   gown, legs, breastplate, hood, gauntlets   weld -> decimate -> hem overlap -> push off the body -> skin
#               (weights from the nearest body point, s9_assemble's method). gauntlets also carry grip_R / grip_L,
#               transferred from the body's own keys (each gauntlet vertex moves as its nearest body hand vertex), so a
#               gloved fist closes exactly as the bare one and the body's fingers never come out through the steel.
#   weapon      wand          on weapon_r, AT THE STAFF'S MOUNT: its axis along the shipped staff's axis, its grip centre
#               where the staff's axis passes the fist, its crystal toward the staff's crown. The staff's mount was
#               solved with the T12 method (seat, roll, carry layers); the wand inherits all of it by construction.
#   carried     grimoire      26 cm, rigid on Hips, hung outside her LEFT hip below the belt (the Fire Ball is thrown by
#               her LEFT hand, so the book cannot live in that hand), front cover outward.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s24_assemble.py")][0]))
sys.path.insert(0, HERE)
import gearlib as G

a = sys.argv[sys.argv.index('--') + 1:]
BODY, PIECES, BUILDS, STAFF, OUT = a[:5]
OUTJ = a[a.index('--json') + 1] if '--json' in a else os.path.join(OUT, "assemble.json")
os.makedirs(OUT, exist_ok=True)
rep = dict(pieces={})

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
body = [o for o in sc.objects if o.type == 'MESH' and o.vertex_groups]
for o in [o for o in sc.objects if o.type == 'MESH' and not o.vertex_groups]:
    bpy.data.objects.remove(o, do_unlink=True)
arm.animation_data.action = None
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
bo = body[0]
BV, BT, names, W, tree = G.body_sampler(bo)
H = float(BV[:, 2].max() - BV[:, 2].min())
print("body %s: %.4f m, %d verts" % (bo.name, H, len(BV)))


def extend_boundary(pc, dist):
    """s9_assemble's HEM OVERLAP: boundary vertices moved `dist` outward along the surface, so two pieces cut from one
    shell OVERLAP at their shared edge instead of meeting at a hairline the body shows through."""
    bm = bmesh.new(); bm.from_mesh(pc.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.verts.ensure_lookup_table(); bm.normal_update()
    move = {}
    for e in bm.edges:
        if not e.is_boundary or not e.link_faces:
            continue
        f = e.link_faces[0]
        a_, b_ = e.verts[0].co, e.verts[1].co
        t = (b_ - a_).normalized(); o = t.cross(f.normal).normalized()
        if (f.calc_center_median() - (a_ + b_) * 0.5).dot(o) > 0:
            o = -o
        for v in e.verts:
            move.setdefault(v.index, Vector((0, 0, 0))); move[v.index] += o
    for vi, o in move.items():
        if o.length > 1e-9:
            bm.verts[vi].co += o.normalized() * dist
    bm.to_mesh(pc.data); bm.free(); pc.data.update()
    return len(move)


def weld(pc):
    bm = bmesh.new(); bm.from_mesh(pc.data); n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    n1 = len(bm.verts); bm.to_mesh(pc.data); bm.free(); pc.data.update()
    return n0, n1


def world(o):
    dg = bpy.context.evaluated_depsgraph_get(); oe = o.evaluated_get(dg); me = oe.to_mesh()
    co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", co); oe.to_mesh_clear()
    M = np.array(o.matrix_world)
    return co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]


made = []
# (name, face target, push-off offset m, hem overlap m). The breastplate goes on at 12 mm so its edges ride OUTSIDE the
# gown's (6 mm) where the two were cut apart; the legs are tight leggings (4 mm); the hood is wool over hair (8 mm).
DEFORM = [("gown", 30000, 0.006, 0.006), ("legs", 22000, 0.004, 0.004), ("breastplate", 18000, 0.012, 0.004),
          ("hood", 22000, 0.008, 0.004), ("gauntlets", 16000, 0.005, 0.004)]
for nm, faces, offs, hem in DEFORM:
    before = set(sc.objects)
    pc = G.import_piece(os.path.join(PIECES, "%s.glb" % nm), before)
    f0 = len(pc.data.polygons)
    wv = weld(pc)
    G.decimate(pc, faces)
    nb = extend_boundary(pc, hem)
    P, pushed = G.clear_body(pc, tree, offs)
    ok = G.skin_to_body(pc, P, BV, BT, names, W, tree, arm)
    keys = {}
    grip_dW = None
    if nm == "gauntlets":
        # the body's grip keys as WORLD displacements of each gauntlet vertex's nearest body vertex. Applied AFTER
        # align_space (v2): a mesh with shape keys keeps its Basis key's coordinates when vertices are moved, so keys
        # added before align_space shipped the gauntlets as a 1 cm speck at the origin (probe_v1: rest extent 8 mm).
        from mathutils.kdtree import KDTree
        Mb = np.array(bo.matrix_world)
        kb = bo.data.shape_keys.key_blocks
        base = np.empty(len(bo.data.vertices) * 3); kb["Basis"].data.foreach_get("co", base); base = base.reshape(-1, 3)
        kd = KDTree(len(BV))
        for i, q in enumerate(BV):
            kd.insert(Vector(q.tolist()), i)
        kd.balance()
        near = np.array([kd.find(Vector(p.tolist()))[1] for p in P])
        grip_dW = {}
        for kn in ("grip_R", "grip_L"):
            kco = np.empty(len(bo.data.vertices) * 3); kb[kn].data.foreach_get("co", kco); kco = kco.reshape(-1, 3)
            grip_dW[kn] = ((kco - base) @ Mb[:3, :3].T)[near]
    if nm == "gown" and os.environ.get("SKIRT_RAMP", "0") == "1":
        # SKIRT RAMP (v2; OFF by default since v5: re-weighting the hanging skirt to the pelvis let the body's upper thigh
        # swing out from behind it in the run -- cover beats stretch, as D7's accepted robe chose): below the hip joints, the tabard and mail skirt took nearest-point weights from ONE thigh each,
        # so the strip between her legs stretched up to 34 cm in the idle (probe_v1, 424 edges > 5 cm) -- the dotted
        # shadow lines. A skirt hangs from the pelvis: weight goes to Hips at the midline, blending to the same-side
        # UpLeg over 12 cm outward, and the blend fades in from the hip joints down over 8 cm.
        hz = float(np.array(arm.matrix_world @ arm.pose.bones["LeftUpLeg"].head)[2])
        mx_ = float(np.array(arm.matrix_world @ arm.pose.bones["Hips"].head)[0])
        gi = {g.name: g.index for g in pc.vertex_groups}
        ramped = 0
        for i, p in enumerate(P):
            if p[2] > hz:
                continue
            fade = min(1.0, (hz - p[2]) / 0.08)
            side = "LeftUpLeg" if p[0] > mx_ else "RightUpLeg"
            other = "RightUpLeg" if side == "LeftUpLeg" else "LeftUpLeg"
            lat = min(1.0, abs(p[0] - mx_) / 0.18)   # v4: 18 cm (12 cm tore the tabard hem in the Fire Ball lunge)
            cur = {g.group: g.weight for g in pc.data.vertices[i].groups}
            leg_w = cur.get(gi[side], 0.0) + cur.get(gi[other], 0.0)
            if leg_w <= 0:
                continue
            new_side = (1 - fade) * cur.get(gi[side], 0.0) + fade * leg_w * lat
            new_other = (1 - fade) * cur.get(gi[other], 0.0)
            new_hips = cur.get(gi["Hips"], 0.0) + (leg_w - new_side - new_other)
            pc.vertex_groups[side].add([i], float(new_side), 'REPLACE')
            pc.vertex_groups[other].add([i], float(new_other), 'REPLACE')
            pc.vertex_groups["Hips"].add([i], float(new_hips), 'REPLACE')
            ramped += 1
        keys["skirt_ramp"] = dict(verts=ramped, below_z=round(hz, 4), lateral_m=0.18, fade_m=0.08)
        print("    gown skirt ramp: %d verts below z %.3f re-weighted toward Hips at the midline" % (ramped, hz))
    if nm == "hood":
        # A CAPE FOLLOWS THE SHOULDER, not the arm (v3): 75% of each Arm weight moves to its Shoulder. probe v2: the cape
        # over the left shoulder stretched 46 edges > 2x in the walk where nearest-point weights changed abruptly.
        moved_w = 0
        for side in ("Left", "Right"):
            ga, gs_ = pc.vertex_groups.get(side + "Arm"), pc.vertex_groups.get(side + "Shoulder")
            if ga is None or gs_ is None:
                continue
            for v in pc.data.vertices:
                w = next((g.weight for g in v.groups if g.group == ga.index), 0.0)
                if w <= 0:
                    continue
                ws = next((g.weight for g in v.groups if g.group == gs_.index), 0.0)
                ga.add([v.index], 0.25 * w, 'REPLACE'); gs_.add([v.index], ws + 0.75 * w, 'REPLACE'); moved_w += 1
        keys["arm_to_shoulder"] = dict(verts=moved_w, fraction=0.75)
    if nm == "breastplate":
        # A STEEL PLATE MOVES WITH THE CHEST (v4): within 14 cm of the midline the plate takes Spine02/Spine01 only; the
        # spaulders keep their shoulder/arm weights; the smoothing below blends the boundary. probe v3: the plate copied
        # the skin's shoulder weights and tore across the collar in the Fire Ball (118 edges > 2x at frame 25).
        mx_ = float(np.array(arm.matrix_world @ arm.pose.bones["Hips"].head)[0])
        gs2, gs1 = pc.vertex_groups["Spine02"], pc.vertex_groups["Spine01"]
        rig = 0
        for i, p in enumerate(P):
            if abs(p[0] - mx_) >= 0.14:
                continue
            for g in list(pc.data.vertices[i].groups):
                pc.vertex_groups[g.group].remove([i])
            gs2.add([i], 0.7, 'REPLACE'); gs1.add([i], 0.3, 'REPLACE'); rig += 1
        keys["rigid_torso_plate"] = dict(verts=rig, within_m_of_midline=0.14, weights={"Spine02": 0.7, "Spine01": 0.3})
    if nm in ("gown", "hood", "breastplate"):
        # WEIGHT SMOOTHING (v3): nearest-point weights jump where the sleeve meets the torso (probe v2: 70 gown edges at
        # the left underarm stretched > 2x in the idle). Laplacian smoothing over the mesh, then normalise and keep 4.
        # (numpy: the vertex_group_smooth operator's poll fails in background mode)
        ng, nv = len(pc.vertex_groups), len(pc.data.vertices)
        Wm = np.zeros((nv, ng), np.float32)
        for v in pc.data.vertices:
            for g in v.groups:
                Wm[v.index, g.group] = g.weight
        ed = np.empty(len(pc.data.edges) * 2, int); pc.data.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
        deg = np.bincount(ed.ravel(), minlength=nv).astype(np.float32)[:, None]
        for _ in range(10):
            acc = np.zeros_like(Wm); np.add.at(acc, ed[:, 0], Wm[ed[:, 1]]); np.add.at(acc, ed[:, 1], Wm[ed[:, 0]])
            Wm = 0.5 * Wm + 0.5 * np.where(deg > 0, acc / np.maximum(deg, 1), Wm)
        top = np.argsort(-Wm, axis=1)[:, :4]
        keep = np.zeros_like(Wm, bool); np.put_along_axis(keep, top, True, axis=1)
        Wm = np.where(keep & (Wm > 0.002), Wm, 0.0); Wm /= np.maximum(Wm.sum(1, keepdims=True), 1e-9)
        for gi_ in range(ng):
            grp = pc.vertex_groups[gi_]
            grp.remove(list(range(nv)))
            nz = np.nonzero(Wm[:, gi_])[0]
            for vi in nz:
                grp.add([int(vi)], float(Wm[vi, gi_]), 'REPLACE')
        keys["weight_smooth"] = dict(factor=0.5, repeat=10, limit=4, method="numpy Laplacian over mesh edges")
    G.align_space(pc, bo)
    if grip_dW is not None:
        Mi3 = np.linalg.inv(np.array(bo.matrix_world)[:3, :3])
        pc.shape_key_add(name="Basis", from_mix=False)
        co = np.empty(len(pc.data.vertices) * 3); pc.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
        for kn, dW in grip_dW.items():
            k = pc.shape_key_add(name=kn, from_mix=False); k.value = 0.0
            k.data.foreach_set("co", (co + dW @ Mi3.T).ravel())
            moved = int((np.linalg.norm(dW, axis=1) > 1e-5).sum())
            keys[kn] = dict(verts_moved=moved, max_m=round(float(np.linalg.norm(dW, axis=1).max()), 4))
            print("    %s on the gauntlets: %d verts move, max %.4f m (local-space key, after align_space)" % (kn, moved, keys[kn]["max_m"]))
    pc.name = nm
    made.append((nm, [pc]))
    rep["pieces"][nm] = dict(mode="skin", faces=[f0, len(pc.data.polygons)], welded=list(wv), offset_m=offs, hem_overlap_m=hem,
                             boundary_verts_extended=int(nb), pushed=int(pushed), skinned_verts=int(ok), keys=keys)
    print("  %-11s skinned: %d -> %d faces, %d pushed off the body by %.3f m" % (nm, f0, len(pc.data.polygons), pushed, offs))

# ---- the staff's mount, read from the shipped staff.glb (rest pose) ----------------------------------------
before = set(sc.objects)
bpy.ops.import_scene.gltf(filepath=STAFF)
added = [o for o in sc.objects if o not in before]
sarm = next((o for o in added if o.type == 'ARMATURE'), None)
if sarm and sarm.animation_data:
    sarm.animation_data.action = None
if sarm:
    for pb in sarm.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
SW = np.vstack([world(o) for o in added if o.type == 'MESH' and len(o.data.vertices) > 200])
for o in added:
    bpy.data.objects.remove(o, do_unlink=True)
sc_ = SW.mean(0)
_, _, vt = np.linalg.svd((SW - sc_)[:: max(1, len(SW) // 5000)], full_matrices=False)
U = vt[0] / np.linalg.norm(vt[0])
fist, _chan, _al, _palm = G.hand_frame(bo, arm, "RightHand")
t_f = float((fist - sc_) @ U)
ends = (SW - sc_) @ U
# v6: the crown is the NEAR end from the fist -- stills v5 showed the wand crystal-DOWN in the idle carry, where the shipped
# staff stands crown-UP: the staff's grip fraction (0.55) is measured from its crown, not its foot
crown_sign = 1.0 if abs(ends.max() - t_f) < abs(ends.min() - t_f) else -1.0
U = U * crown_sign
gp = sc_ + U * ((fist - sc_) @ U)          # where the staff's axis passes the fist
print("  staff: length %.3f m, axis %s (to the crown), grip point %s, fist %.4f m off the axis"
      % (float(ends.max() - ends.min()), np.round(U, 3), np.round(gp, 4), float(np.linalg.norm(fist - gp))))

# ---- the wand on weapon_r -------------------------------------------------------------------------------
WAND_L = 0.35
before = set(sc.objects)
pc = G.import_piece(os.path.join(BUILDS, "wand.glb"), before)
G.decimate(pc, 8000)
V = world(pc)
lo, hi = V[:, 2].min(), V[:, 2].max()
s = WAND_L / float(hi - lo)
# the grip's centre: 0.21 of the length from the butt (sheet GS-SWAND_a: wrap 0.107-0.312 of the wand from the butt)
c_axis = np.array([np.median(V[:, 0]), np.median(V[:, 1])])
butt = np.array([c_axis[0], c_axis[1], lo])
R = Vector((0, 0, 1)).rotation_difference(Vector(U.tolist())).to_matrix().to_4x4()
gripc_local = np.array([0, 0, 0.21 * WAND_L])
M = Matrix.Translation(Vector(gp.tolist())) @ R @ Matrix.Translation(Vector((-gripc_local).tolist())) \
    @ Matrix.Scale(s, 4) @ Matrix.Translation(Vector((-butt).tolist()))
pc.matrix_world = M @ pc.matrix_world
bpy.ops.object.select_all(action='DESELECT'); pc.select_set(True); bpy.context.view_layer.objects.active = pc
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
gW = world(pc)
g_ = pc.vertex_groups.new(name="weapon_r"); g_.add(list(range(len(pc.data.vertices))), 1.0, 'REPLACE')
m_ = pc.modifiers.new('arm', 'ARMATURE'); m_.object = arm
G.align_space(pc, bo)
pc.name = "wand"
made.append(("wand", [pc]))
tip = gW[np.argmax((gW - gp) @ U)]; bt = gW[np.argmin((gW - gp) @ U)]
rep["pieces"]["wand"] = dict(mode="bone", bone="weapon_r", length_m=WAND_L, grip_centre_from_butt_m=round(0.21 * WAND_L, 4),
                             mount="the shipped staff's: axis along the staff, grip centre where the staff's axis passes the fist",
                             axis_world=[round(x, 4) for x in U], grip_point=[round(x, 4) for x in gp],
                             crystal_tip=[round(float(x), 4) for x in tip], butt=[round(float(x), 4) for x in bt],
                             fist_off_axis_m=round(float(np.linalg.norm(fist - gp)), 4))
print("  wand: %.3f m on weapon_r, tip at %s, butt at %s" % (WAND_L, np.round(tip, 3), np.round(bt, 3)))

# ---- the grimoire on Hips ---------------------------------------------------------------------------------
BOOK_H = 0.26
before = set(sc.objects)
pc = G.import_piece(os.path.join(BUILDS, "book.glb"), before)
G.decimate(pc, 9000)
V = world(pc)
lo, hi = V.min(0), V.max(0)
s = BOOK_H / float(hi[2] - lo[2])
# its front cover faces +X in the build (preview: the medallion seen from +X); +X is her LEFT, so it faces outward as is
belt_z = float(BV[:, 2].min()) + 0.585 * H          # the sash/belt line on the sheet (zf ~0.58-0.60)
# v7 PLACEMENT, by search (s30_book_search.py over every frame of every clip, a 26 cm box + 8 mm margin): her RIGHT hip,
# behind -- x -0.26, y +0.14 (she faces -Y), 6 cm under the belt line, turned so the front cover faces out and back (yaw
# 120 about Z from the build's +X cover). Zero body vertices within 8 mm in every frame of idle/walk/run/Fire Ball/Meteor/
# hit/death; the right hand under the staff carry 9.7 cm clear, the raw Fire Ball arm 14.9, the Meteor 4.7. The first
# placement (outside the LEFT hip) was inside her every idle frame: the left hand hangs there and throws the Fire Ball.
BOOK_C = (-0.26, 0.14, 0.06); BOOK_YAW = 120.0
x_out = float("nan"); y_hip = float("nan")
target = np.array([BOOK_C[0], BOOK_C[1], belt_z - BOOK_C[2]])
ctr = (lo + hi) / 2
M = (Matrix.Translation(Vector(target.tolist())) @ Matrix.Rotation(math.radians(BOOK_YAW), 4, 'Z') @ Matrix.Scale(s, 4)
     @ Matrix.Translation(Vector((-ctr).tolist())))
pc.matrix_world = M @ pc.matrix_world
bpy.ops.object.select_all(action='DESELECT'); pc.select_set(True); bpy.context.view_layer.objects.active = pc
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
g_ = pc.vertex_groups.new(name="Hips"); g_.add(list(range(len(pc.data.vertices))), 1.0, 'REPLACE')
m_ = pc.modifiers.new('arm', 'ARMATURE'); m_.object = arm
G.align_space(pc, bo)
pc.name = "grimoire"
made.append(("grimoire", [pc]))
rep["pieces"]["grimoire"] = dict(mode="bone", bone="Hips", height_m=BOOK_H, size_m=[round(float(x) * s, 4) for x in (hi - lo)],
                                 centre=[round(float(x), 4) for x in target], belt_z=round(belt_z, 4), yaw_deg=BOOK_YAW,
                                 carry="hung at the back of her RIGHT hip under the belt, front cover out and back; rigid on Hips (s30 search)")
print("  grimoire: %.2f m tall, centre %s, yaw %.0f" % (BOOK_H, np.round(target, 3), BOOK_YAW))


def export(objs, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    arm.select_set(True); bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False,
                              export_morph=True, export_image_format='AUTO')
    return round(os.path.getsize(path) / 1e6, 2)


for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bpy.context.view_layer.update()
keep_objs = {o for _, objs in made for o in objs} | set(body)
stray = [o for o in sc.objects if o.type == 'MESH' and o not in keep_objs]
rep["stray_meshes_removed"] = [o.name for o in stray]
for o in stray:
    bpy.data.objects.remove(o, do_unlink=True)
rep["files"] = {}
for nm, objs in made:
    rep["files"]["%s.glb" % nm] = export(objs, os.path.join(OUT, "%s.glb" % nm))
    print("wrote %-16s %6.2f MB" % (nm + ".glb", rep["files"]["%s.glb" % nm]))
rep["body"] = dict(file=BODY, height_m=round(H, 4), not_reexported=True)
json.dump(rep, open(OUTJ, "w"), indent=1)
