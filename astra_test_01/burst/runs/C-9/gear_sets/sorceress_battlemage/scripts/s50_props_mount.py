# R-C9-119: mount the NEW wand (right fist) and the OPEN grimoire (left palm) on her rig, and author their GRIP MORPHS.
#   blender -b -noaudio --python s50_props_mount.py -- <body.glb> <wand_build.glb> <book.glb> <out_dir>
# WAND (weapon_r): 0.52 m. Its GRIP is measured on the model itself -- the dark leather band between the gold collars
#   (texture colour): grip centre = the band's mid-height, grip radius = the band's median radius. The wand's axis runs
#   along the RIGHT hand's CHANNEL (gearlib.hand_frame: the across-palm axis a fist closes round), signed so the crystal
#   leads where the staff's crown did; the grip centre sits ON the fist centre. grip_R_wand closes the hand to the grip
#   radius + 10 mm round that axis.
# BOOK (weapon_l): palm UNDER the spine. Book frame (s48): spine +Y, pages +Z, across +X. +Y -> the LEFT hand's along axis
#   (pages' top toward the fingertips), +Z -> the palm normal (signed by the direction grip_L closes the fingers), so the
#   pages open UP off the palm. The spine centre (the hinge line's midpoint) sits over the palm centre at the palm surface
#   + the spine radius + 3 mm. grip_L_book cups the fingers round the spine axis to the spine radius + 10 mm.
# The body is NOT exported: each new key is dumped as per-vertex deltas (Blender mesh-local) with the basis, so s51 patches
# the glTF binary (clips byte-identical). Each prop is exported alone with the armature, rigid on its weapon bone.
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("s50_props_mount.py")][0])); sys.path.insert(0, HERE)
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, WAND, BOOK, OUT = a[:4]
os.makedirs(OUT, exist_ok=True)
WAND_L = 0.52
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE')
arm.animation_data_clear()
for pb in arm.pose.bones:
    pb.matrix_basis = Matrix.Identity(4)
bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not bo]:
    bpy.data.objects.remove(o, do_unlink=True)
for k in bo.data.shape_keys.key_blocks:
    k.value = 0.0
bpy.context.view_layer.update()
Mb = np.array(bo.matrix_world)
kb = bo.data.shape_keys.key_blocks
base = np.empty(len(bo.data.vertices) * 3); kb["Basis"].data.foreach_get("co", base); base = base.reshape(-1, 3)
BW = base @ Mb[:3, :3].T + Mb[:3, 3]
rep = {}


def signed_frame(bone, key):
    c, chan, along, palm = G.hand_frame(bo, arm, bone)
    g = np.empty(len(bo.data.vertices) * 3); kb[key].data.foreach_get("co", g)
    d = (g.reshape(-1, 3) - base) @ Mb[:3, :3].T
    mv = np.linalg.norm(d, axis=1) > 1e-3
    cd = d[mv].mean(0); cd -= (cd @ along) * along
    if cd @ palm < 0:
        palm = -palm
    chan = np.cross(palm, along)
    gi = bo.vertex_groups[bone].index
    idx = [v.index for v in bo.data.vertices if any(gg.group == gi and gg.weight > 0.3 for gg in v.groups)]
    surf = float(np.percentile((BW[idx] - c) @ palm, 95))      # the palm SURFACE along the palm normal
    return np.array(c), np.array(chan), np.array(along), np.array(palm), surf


def world_verts(o):
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world); return co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]


def vcolours(o):
    img = next(n.image for s in o.material_slots if s.material and s.material.node_tree for n in s.material.node_tree.nodes
               if n.type == 'TEX_IMAGE' and n.image)
    Wd, Hd = img.size; px = np.array(img.pixels[:], np.float32).reshape(Hd, Wd, img.channels)[..., :3]
    uvl = o.data.uv_layers.active.data; UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
    lp = np.empty(len(o.data.loops), int); o.data.loops.foreach_get("vertex_index", lp)
    VC = np.zeros((len(o.data.vertices), 3)); n = np.zeros(len(o.data.vertices))
    np.add.at(VC, lp, px[np.clip((UV[:, 1] * Hd).astype(int), 0, Hd - 1), np.clip((UV[:, 0] * Wd).astype(int), 0, Wd - 1)])
    np.add.at(n, lp, 1); VC /= np.maximum(n, 1)[:, None]
    return VC ** (1 / 2.2) if img.is_float else VC


def export(obj, path):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False, export_morph=False,
                              export_image_format='AUTO')


def bind_rigid(obj, bone):
    for g in list(obj.vertex_groups):
        obj.vertex_groups.remove(g)
    g = obj.vertex_groups.new(name=bone); g.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    m = obj.modifiers.new('arm', 'ARMATURE'); m.object = arm
    G.align_space(obj, bo)


# ---------------- WAND ----------------
cR, chR, alR, paR, surfR = signed_frame("RightHand", "grip_R")
before = set(sc.objects); w = G.import_piece(WAND, before); G.decimate(w, 9000)
V = world_verts(w)
cxy = np.median(V[:, :2], axis=0)
lo, hi = V[:, 2].min(), V[:, 2].max(); s = WAND_L / float(hi - lo)
VC = vcolours(w)
mx = VC.max(1); mn = VC.min(1); sat = (mx - mn) / np.maximum(mx, 1e-6); gr = VC[:, 1] / np.maximum(VC[:, 0], 1e-6)
z = (V[:, 2] - lo) * s
leather = (mx < 0.45) & (sat > 0.25) & (gr > 0.5) & (gr < 0.85) & (z < 0.45 * WAND_L)
zg = float(np.median(z[leather])) if leather.sum() > 50 else 0.19 * WAND_L
rad = np.linalg.norm((V[:, :2] - cxy) * s, axis=1)
r_grip = float(np.median(rad[leather])) if leather.sum() > 50 else 0.0125
crown_hint = np.array([0.415, -0.907, -0.079])                # the shipped staff's crown direction (s24's measurement)
d = chR if chR @ crown_hint > 0 else -chR
Rz = Vector((0, 0, 1)).rotation_difference(Vector(d.tolist())).to_matrix().to_4x4()
M = Matrix.Translation(Vector(cR.tolist())) @ Rz @ Matrix.Translation((0, 0, -zg)) @ Matrix.Scale(s, 4) @ \
    Matrix.Translation(Vector((-cxy[0], -cxy[1], -lo)))
w.matrix_world = M @ w.matrix_world
bpy.ops.object.select_all(action='DESELECT'); w.select_set(True); bpy.context.view_layer.objects.active = w
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
WV = world_verts(w)
tip = WV[np.argmax((WV - cR) @ d)]; butt = WV[np.argmin((WV - cR) @ d)]
crystal_top = float((tip - cR) @ d)
k_w, mv_w, mx_w = G.grip_key(bo, arm, "RightHand", cR, d, r_grip + 0.010, "grip_R_wand")
wr_rest = np.array(arm.matrix_world @ arm.data.bones["weapon_r"].matrix_local)
tip_local = (np.linalg.inv(wr_rest) @ np.append(tip, 1.0))[:3]
bind_rigid(w, "weapon_r"); w.name = "wand"
export(w, os.path.join(OUT, "wand.glb"))
rep["wand"] = dict(length_m=WAND_L, scale=round(s, 5), grip_centre_from_butt_m=round(zg, 4), grip_radius_m=round(r_grip, 4),
                   leather_verts=int(leather.sum()), axis_world=d.round(4).tolist(), fist_centre=cR.round(4).tolist(),
                   crystal_tip_from_fist_m=round(crystal_top, 4), tip_in_weapon_r_local=tip_local.round(4).tolist(),
                   grip_morph=dict(name="grip_R_wand", closes_to_m=round(r_grip + 0.010, 4), verts_moved=int(mv_w), max_travel_m=round(float(mx_w), 4)),
                   fist_centre_off_axis_m=0.0, mount="grip centre ON the fist centre, the axis along the right hand's channel")
# ---------------- BOOK ----------------
cL, chL, alL, paL, surfL = signed_frame("LeftHand", "grip_L")
bj = json.load(open(BOOK.replace('.glb', '.json')))
SPR = bj["spine_radius_m"]; H = bj["height_m"]
before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=BOOK)
_new = [o for o in sc.objects if o not in before]; b = next(o for o in _new if o.type == 'MESH')   # (42 faces: import_piece drops < 200 verts)
for o in _new:
    if o is not b: bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action='DESELECT'); b.select_set(True); bpy.context.view_layer.objects.active = b
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
# v2 (checks): +8 mm for the gauntlet under the palm, and 7 cm toward the fingertips so the 28 cm spine does not run back
# over her wrist and forearm -- the palm sits under the spine's NEAR half
BOOK_FWD, BOOK_UP = 0.07, 0.011
spine_c = cL + paL * (surfL + SPR + BOOK_UP) + alL * BOOK_FWD
Rb = np.stack([np.cross(alL, paL), alL, paL], 1)               # book +X, +Y, +Z -> world
Mb4 = np.eye(4); Mb4[:3, :3] = Rb; Mb4[:3, 3] = spine_c - Rb @ np.array([0, H / 2, 0])
b.matrix_world = Matrix(Mb4.tolist()) @ b.matrix_world
bpy.ops.object.select_all(action='DESELECT'); b.select_set(True); bpy.context.view_layer.objects.active = b
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
k_b, mv_b, mx_b = G.grip_key(bo, arm, "LeftHand", spine_c, alL, SPR + 0.010, "grip_L_book")
dist_palm_to_spine_axis = float(np.linalg.norm((cL - spine_c) - ((cL - spine_c) @ alL) * alL))
bind_rigid(b, "weapon_l"); b.name = "grimoire"
export(b, os.path.join(OUT, "grimoire.glb"))
rep["book"] = dict(spine_offset_toward_fingertips_m=BOOK_FWD, spine_lift_m=BOOK_UP, spine_centre=spine_c.round(4).tolist(), palm_centre=cL.round(4).tolist(), palm_surface_m=round(surfL, 4),
                   palm_centre_to_spine_axis_m=round(dist_palm_to_spine_axis, 4), spine_radius_m=SPR,
                   axes=dict(spine=alL.round(4).tolist(), pages_normal=paL.round(4).tolist()),
                   grip_morph=dict(name="grip_L_book", closes_to_m=round(SPR + 0.010, 4), verts_moved=int(mv_b), max_travel_m=round(float(mx_b), 4)),
                   mount="palm under the spine: spine along the left hand (pages' top toward the fingertips), pages opening up off the palm")
# ---------------- the body's new keys, as deltas for the binary patch ----------------
deltas = {}
for kn in ("grip_R_wand", "grip_L_book"):
    kc = np.empty(len(bo.data.vertices) * 3); kb[kn].data.foreach_get("co", kc)
    deltas[kn] = kc.reshape(-1, 3) - base
np.savez(os.path.join(OUT, "body_key_deltas.npz"), basis_blender_local=base, matrix_world=Mb, **deltas)
json.dump(rep, open(os.path.join(OUT, "mount.json"), "w"), indent=1)
print("MOUNT", json.dumps(rep)[:1400])
