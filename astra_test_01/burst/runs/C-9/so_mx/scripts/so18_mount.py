# so_mx R-C9-133/134: mount the ORB STAFF (right fist, weapon_r) and the SHIELD (left fist, centre grip, weapon_l) on the
# battle mage's rig. Each prop is bound RIGID to its weapon bone at REST and exported alone with the armature.
#   blender -b -noaudio --python so18_mount.py -- <body.glb> <orbst_build.glb> <shld_build.glb> <pose_deltas.json> <out_dir>
#        [--orb-len 0.75] [--shield-h 0.78] [--shield-back 0.035: the fist centre's depth behind the back surface]
# ORB STAFF: s50's wand method -- the GRIP measured on the model (the dark leather band: centre and median radius), the
#   axis along the RIGHT hand's channel (gearlib.hand_frame), the grip centre ON the fist centre; the axis SIGN chosen so the
#   orb points UP in the sword-and-shield idle pose (so17's delta), i.e. held like a one-handed sword, orb up and forward.
# SHIELD: CENTRE GRIP. Measured on the model: its thin axis (PCA), the BOSS side (front) = the side the centre bulges
#   to; the grip point = the boss centre on the BACK surface, 3.5 cm behind it (inside a closed fist). Placed in the BLOCK
#   pose (so17's delta at block_idle): the face normal = her forward (-Y), the shield's long axis = world up, the grip
#   point on the left fist centre; then carried back to REST through the hand's delta and bound to weapon_l.
# Closes with the body's existing D7 fists: grip_R (the staff grip) and grip_L.
import bpy, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_battlemage/scripts")
import gearlib as G
a = sys.argv[sys.argv.index('--') + 1:]
BODY, ORB, SHL, PD, OUT = a[:5]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
ORB_L, SH_H, SH_BACK = opt('--orb-len', 0.75), opt('--shield-h', 0.78), opt('--shield-back', 0.035)
os.makedirs(OUT, exist_ok=True); PDJ = json.load(open(PD))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=BODY)
sc = bpy.context.scene
arm = next(o for o in sc.objects if o.type == 'ARMATURE'); arm.animation_data_clear()
for pb in arm.pose.bones: pb.matrix_basis = Matrix.Identity(4)
bo = next(o for o in sc.objects if o.type == 'MESH' and o.vertex_groups and len(o.data.vertices) > 1000)
for o in [o for o in sc.objects if o.type == 'MESH' and o is not bo]: bpy.data.objects.remove(o, do_unlink=True)
for k in bo.data.shape_keys.key_blocks: k.value = 0.0
bpy.context.view_layer.update()
rep = {}
def wv(o):
    co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world); return co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
def vcolours(o):
    img = next(n.image for s in o.material_slots if s.material and s.material.node_tree for n in s.material.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)
    Wd, Hd = img.size; px = np.array(img.pixels[:], np.float32).reshape(Hd, Wd, img.channels)[..., :3]
    uvl = o.data.uv_layers.active.data; UV = np.empty(len(uvl) * 2); uvl.foreach_get("uv", UV); UV = UV.reshape(-1, 2)
    lp = np.empty(len(o.data.loops), int); o.data.loops.foreach_get("vertex_index", lp)
    VC = np.zeros((len(o.data.vertices), 3)); n = np.zeros(len(o.data.vertices))
    np.add.at(VC, lp, px[np.clip((UV[:, 1] * Hd).astype(int), 0, Hd - 1), np.clip((UV[:, 0] * Wd).astype(int), 0, Wd - 1)])
    np.add.at(n, lp, 1); VC /= np.maximum(n, 1)[:, None]; return VC ** (1 / 2.2) if img.is_float else VC
def place(o, M):
    o.matrix_world = M @ o.matrix_world
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
def bind_rigid(obj, bone):
    for g in list(obj.vertex_groups): obj.vertex_groups.remove(g)
    g = obj.vertex_groups.new(name=bone); g.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    m = obj.modifiers.new('arm', 'ARMATURE'); m.object = arm; G.align_space(obj, bo)
def export(obj, path):
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False, export_morph=False, export_image_format='AUTO')
def load(path):
    before = set(sc.objects); bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in sc.objects if o not in before]; ms = [o for o in new if o.type == 'MESH']
    for o in new:
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    if len(ms) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for o in ms: o.select_set(True)
        bpy.context.view_layer.objects.active = ms[0]; bpy.ops.object.join()
    o = ms[0]
    for x in [x for x in sc.objects if x.type == 'EMPTY']: bpy.data.objects.remove(x, do_unlink=True)
    o.parent = None; G.decimate(o, 12000); return o
# ---------------- ORB STAFF ----------------
cR, chR, alR, paR = [np.array(x) for x in G.hand_frame(bo, arm, "RightHand")]
w = load(ORB); V = wv(w)
cxy = np.median(V[:, :2], axis=0); lo, hi = V[:, 2].min(), V[:, 2].max(); s = ORB_L / float(hi - lo)
VC = vcolours(w); mx = VC.max(1); mn = VC.min(1); sat = (mx - mn) / np.maximum(mx, 1e-6); gr = VC[:, 1] / np.maximum(VC[:, 0], 1e-6)
z = (V[:, 2] - lo) * s
leather = (mx < 0.45) & (sat > 0.25) & (gr > 0.5) & (gr < 0.85) & (z < 0.5 * ORB_L)
zg = float(np.median(z[leather])) if leather.sum() > 50 else 0.25 * ORB_L
rad = np.linalg.norm((V[:, :2] - cxy) * s, axis=1); r_grip = float(np.median(rad[leather])) if leather.sum() > 50 else 0.016
Dr = np.array(PDJ['orb']['delta_world_blender'])[:3, :3]
d = chR if (Dr @ chR)[2] > 0 else -chR                              # the orb UP in the idle pose
M = Matrix.Translation(Vector(cR.tolist())) @ Vector((0, 0, 1)).rotation_difference(Vector(d.tolist())).to_matrix().to_4x4() @ \
    Matrix.Translation((0, 0, -zg)) @ Matrix.Scale(s, 4) @ Matrix.Translation(Vector((-cxy[0], -cxy[1], -lo)))
place(w, M); WV = wv(w)
tip = WV[np.argmax((WV - cR) @ d)]
top = WV[(WV - cR) @ d > (tip - cR) @ d - 0.14]                    # the orb: the top 14 cm
orb_d = float(np.ptp((top - cR) - np.outer((top - cR) @ d, d), axis=0).max())
wr = np.array(arm.matrix_world @ arm.data.bones["weapon_r"].matrix_local)
bind_rigid(w, "weapon_r"); w.name = "orbstaff"; export(w, os.path.join(OUT, "orbstaff.glb"))
rep['orbstaff'] = dict(length_m=ORB_L, scale=round(s, 5), grip_centre_from_butt_m=round(zg, 4), grip_radius_m=round(r_grip, 4),
                       leather_verts=int(leather.sum()), orb_width_m=round(orb_d, 4), orb_tip_from_fist_m=round(float((tip - cR) @ d), 4),
                       axis_world_rest=d.round(4).tolist(), axis_world_in_idle=(Dr @ d).round(4).tolist(),
                       tip_in_weapon_r_local=(np.linalg.inv(wr) @ np.append(tip, 1))[:3].round(4).tolist(), fist_morph="grip_R (D7 staff grip)")
bpy.data.objects.remove(w, do_unlink=True)
# ---------------- SHIELD ----------------
cL, chL, alL, paL = [np.array(x) for x in G.hand_frame(bo, arm, "LeftHand")]
sh = load(SHL); V = wv(sh); c0 = V.mean(0)
_, _, vt = np.linalg.svd((V - c0)[:: max(1, len(V) // 6000)], full_matrices=False)
thin = vt[2] / np.linalg.norm(vt[2]); tall = vt[0] / np.linalg.norm(vt[0])
if tall[2] < 0: tall = -tall                                          # Tripo: up is +Z
across = np.cross(tall, thin)
# the BOSS side: within the central 15% of the face, the side the surface bulges to
q = V - c0; u, v, n = q @ across, q @ tall, q @ thin
ext_u, ext_v = np.ptp(u), np.ptp(v)
cen = (np.abs(u) < 0.08 * ext_u) & (np.abs(v - np.median(v)) < 0.08 * ext_v)
front = thin if n[cen].max() > -n[cen].min() else -thin
nf = q @ front
sc_ = SH_H / ext_v
boss = q[cen][np.argmax(nf[cen])]                                       # the boss apex (shield coords, unscaled)
back_n = float(np.percentile(nf[cen], 3))                               # the back surface behind the boss
grip = c0 + (boss - (boss @ front) * front) + front * (back_n - SH_BACK / sc_)   # 3.5 cm behind the back, behind the boss
# the BLOCK pose: face normal = her forward (-Y), long axis = up (Z), grip on the left fist (posed)
Dl = np.array(PDJ['shield']['delta_world_blender'])
cL_pose = (Dl @ np.append(cL, 1))[:3]
fw = np.array([0.0, -1.0, 0.0]); up = np.array([0.0, 0.0, 1.0]); ac = np.cross(up, fw)
Rsrc = np.stack([np.cross(tall, front), tall, front], 1)               # shield's (across, tall, front) as columns
Rdst = np.stack([np.cross(up, fw), up, fw], 1)
R = Rdst @ Rsrc.T
Mblock = np.eye(4); Mblock[:3, :3] = R * sc_; Mblock[:3, 3] = cL_pose - R @ (grip * sc_)
Mrest = np.linalg.inv(Dl) @ Mblock                                      # back to REST through the hand's delta
place(sh, Matrix(Mrest.tolist()))
SV = wv(sh)
bind_rigid(sh, "weapon_l"); sh.name = "shield"; export(sh, os.path.join(OUT, "shield.glb"))
rep['shield'] = dict(height_m=SH_H, scale=round(sc_, 5), width_m=round(float(ext_u * sc_), 4), depth_m=round(float(np.ptp(nf) * sc_), 4),
                     grip_behind_back_m=SH_BACK, block_pose=PDJ['shield']['clip'] + '@' + str(PDJ['shield']['t']),
                     fist_centre_rest=cL.round(4).tolist(), fist_centre_block=cL_pose.round(4).tolist(), fist_morph="grip_L",
                     mount="centre grip: the boss over the left fist, face = her forward and long axis = up in the BLOCK pose")
json.dump(rep, open(os.path.join(OUT, "mount.json"), "w"), indent=1); print("MOUNT", json.dumps(rep))
