# EN-E3 stage 3+4 for the RIFT HORROR (R-C9-135; n19 + three clip kinds: impale, cast, drain -- the great bone-spike arms drive the
# melee and the casts; the six back tentacles ride the chest). n19's header follows.
# EN-E3 stage 3+4 for an UPRIGHT HUNCHED BIPED (the glutton; from n15: plantigrade legs, a belly bone, long arms, no tail).
# n15's header follows. EN-E3 stage 3+4 for the RAPTOR (n10 with a horizontal-biped skeleton: digitigrade hind legs + toes, forelimbs; the jaw cut, mouth
# bag, weights, bake, lint and export are n10's own). Original n10 header follows.
# EN-E3 stage 3+4 for a QUADRUPED: fit a skeleton to the cleaned mesh, weight it, key the cycles procedurally, export the GLB.
#   blender -b -noaudio --python scripts/n10_rig_quad.py -- <prep.glb> <cfg.json> <out.glb>
#
# THE SKELETON is a 4-leg, 3-segment-per-leg chain (the shape of the bundled basic_quadruped metarig: spine, neck, head, tail,
# 3-bone legs), built here from LANDMARKS MEASURED ON THE MESH rather than by dragging the metarig by hand: feet are the four
# clusters of the low band, joints sit above them at a measured fraction of the body column, the head and jaw are cut at the
# lip line. The metarig itself is not used because its generated rig is ~300 control bones and none of that survives a GLB;
# what ships is 26 deform bones. The landmarks are written to <out>.rig.json so they can be checked (and are, by n11_rigplot).
#
# MOTION is control-driven and then BAKED to the deform bones: per frame the clip sets the control layer (pelvis, spine, head,
# jaw, tail rotations; four IK foot targets with poles), Blender solves the IK, and the solved pose of every deform bone is
# read back and keyed. Then constraints and controls are deleted, so the GLB carries plain FK keys on deform bones only.
#
# NO FOOT SLIDE BY CONSTRUCTION: root motion is stripped (the root never moves); in stance a foot target moves BACKWARD at
# exactly the ground speed v, so in the world (root moving forward at v) it is stationary. n10 MEASURES it anyway (footlock row).
# GROUND: every frame of every clip is checked for vertices below z=0 (penetration row); the death clip SOLVES its own ground
# contact (the body is raised by exactly the measured penetration, frame by frame).
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector, Matrix, Quaternion, Euler

a = sys.argv[sys.argv.index('--') + 1:]
IN, CFGP, OUT = a[0], a[1], a[2]
CFG = json.load(open(CFGP))
FPS = 30
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=IN)
sc = bpy.context.scene; sc.render.fps = FPS
body = next(o for o in sc.objects if o.type == 'MESH')
V = np.array([v.co[:] for v in body.data.vertices]) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
H = float(V[:, 2].max()); y0, y1 = float(V[:, 1].min()), float(V[:, 1].max()); LF = y1 - y0
LM = {}

# ---------------- landmarks (UPRIGHT HUNCHED BIPED: two plantigrade legs, a gut, long arms, a low head; no tail) ----------------
low = V[V[:, 2] < CFG.get('foot_band', 0.05) * H]
feet = {}
for side, sgn in (('L', 1), ('R', -1)):
    P = low[(low[:, 0] * sgn > 0.03) & (np.abs(low[:, 0]) < CFG.get('foot_x_max', 0.85))]   # not the claw tips hanging beside the feet
    feet[side] = dict(x=float(np.median(P[:, 0])), y=float(np.median(P[:, 1])), toe_y=float(np.quantile(P[:, 1], 0.02)), heel_y=float(np.quantile(P[:, 1], 0.98)))
fy = (feet['L']['y'] + feet['R']['y']) / 2
z_hip = CFG.get('hip_z_frac', 0.38) * H
def ztop(y, w=0.08):
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.2)]; return float(np.quantile(S[:, 2], 0.85))
legj = {}
for side, sgn in (('L', 1), ('R', -1)):
    fx = feet[side]['x']
    Lp = V[(np.abs(V[:, 0] - fx) < CFG.get('leg_col_r', 0.22)) & (np.abs(V[:, 1] - feet[side]['y']) < 0.35) & (V[:, 2] < z_hip)]
    kz = Lp[(Lp[:, 2] > 0.40 * z_hip) & (Lp[:, 2] < 0.62 * z_hip)]
    K = (float(np.median(kz[:, 0])), float(np.median(kz[:, 1])) - 0.05, float(np.median(kz[:, 2])))
    A = (fx, feet[side]['heel_y'] - 0.06, CFG.get('ankle_z', 0.12))
    legj[side] = dict(K=K, A=A)
# the head: the front-most mass in the upper body band
UP = V[V[:, 2] > CFG.get('head_band', 0.55) * H]
y0 = float(UP[:, 1].min())
HB = UP[UP[:, 1] < y0 + CFG.get('head_len', 0.42)]
zh_c = float(np.median(HB[:, 2])); HL = CFG.get('head_len', 0.42); y_hb = y0 + HL
FRn = HB[HB[:, 1] < y0 + 0.06]
z_lip = float(FRn[:, 2].min() + CFG.get('lip_z_frac', 0.45) * np.ptp(FRn[:, 2]))
y_hinge = y0 + CFG.get('hinge_frac', 0.80) * HL
z_hinge = z_lip + CFG.get('hinge_rise', 0.03)
# chest: the shoulder hump -- the highest body point behind the head
BK = V[(np.abs(V[:, 0]) < 0.3) & (V[:, 1] > y_hb)]
sh = BK[np.argmax(BK[:, 2])]; y_ch = float(sh[1]) - 0.05; z_ch = float(sh[2]) - CFG.get('chest_drop', 0.30)
arms = {}
for side, sgn in (('L', 1), ('R', -1)):
    Ap = V[(V[:, 0] * sgn > CFG.get('arm_x_min', 0.55)) & (V[:, 2] > 0.06) & (V[:, 2] < z_ch + 0.1)]
    tip = Ap[np.argmin(Ap[:, 2])]
    shp = np.array([sgn * CFG.get('shoulder_x', 0.45), y_ch, z_ch])
    top_arm = Ap[Ap[:, 2] > np.quantile(Ap[:, 2], 0.9)].mean(0)
    def at(t, Ap=Ap, a=top_arm, b=tip):
        p = a + (b - a) * t; m = np.abs(Ap[:, 2] - p[2]) < 0.06
        return (float(np.median(Ap[m, 0])), float(np.median(Ap[m, 1])), float(p[2])) if m.sum() > 5 else tuple(map(float, p))
    arms[side] = dict(sh=tuple(map(float, shp)), el=at(0.45), wr=at(0.85), tip=tuple(map(float, tip)))
y1 = float(V[:, 1].max()); y_tb = y1 + 1.0; TLF = 0.0
LM.update(H=H, y_snout=y0, z_hip=z_hip, z_chest=z_ch, y_head_base=y_hb, z_lip=z_lip, y_hinge=y_hinge, feet=feet, arms=arms, legj=legj)
ank_z = CFG.get('ankle_z', 0.12)

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
y_hp = fy + CFG.get('hip_back', 0.05)
bone('Hips', (0, y_hp, z_hip), (0, (y_hp + y_ch) / 2, (z_hip + z_ch) / 2), 'root')
bone('spine', (0, (y_hp + y_ch) / 2, (z_hip + z_ch) / 2), (0, y_ch, z_ch), 'Hips', conn=True)
bone('chest', (0, y_ch, z_ch), (0, (y_ch + y_hb) / 2, (z_ch + zh_c) / 2 + 0.05), 'spine', conn=True)
bone('neck', (0, (y_ch + y_hb) / 2, (z_ch + zh_c) / 2 + 0.05), (0, y_hb, zh_c + 0.02), 'chest', conn=True)
bone('head', (0, y_hb, zh_c + 0.02), (0, y0 + 0.03, zh_c + 0.02), 'neck', conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.05, z_lip - 0.06), 'head')
bone('belly', (0, y_hp - 0.05, z_hip + 0.25), (0, fy - CFG.get('belly_fwd', 0.45), z_hip), 'spine')   # the gut: sways and heaves
LEGS = ['L', 'R']
for lg in LEGS:
    f = feet[lg]; sgn = 1 if lg == 'L' else -1
    J = (sgn * CFG.get('hip_x', 0.22), y_hp, z_hip - 0.05); K = legj[lg]['K']; A = legj[lg]['A']
    Tt = (f['x'], f['toe_y'] + 0.03, 0.03)
    bone('leg_%s_1' % lg, J, K, 'Hips'); bone('leg_%s_2' % lg, K, A, 'leg_%s_1' % lg, conn=True)
    bone('leg_%s_3' % lg, A, Tt, 'leg_%s_2' % lg, conn=True)
    bone('ik_%s' % lg, A, Tt, 'root', deform=False)
    bone('pole_%s' % lg, (K[0], K[1] - 0.6, K[2]), (K[0], K[1] - 0.6, K[2] + 0.1), 'root', deform=False)
    LM['leg_' + lg] = dict(joint=J, knee=K, ankle=A, toe=Tt, chain_len=round(float((Vector(K) - Vector(J)).length + (Vector(A) - Vector(K)).length), 4),
                           rest_reach=round(float((Vector(A) - Vector(J)).length), 4))
for s_ in ('L', 'R'):
    a_ = arms[s_]
    bone('arm_%s_1' % s_, a_['sh'], a_['el'], 'chest'); bone('arm_%s_2' % s_, a_['el'], a_['wr'], 'arm_%s_1' % s_, conn=True)
    bone('arm_%s_3' % s_, a_['wr'], a_['tip'], 'arm_%s_2' % s_, conn=True)
bpy.ops.object.mode_set(mode='OBJECT')
DEF = [b.name for b in arm.data.bones if b.use_deform]

# ---------------- mouth: a real CUT along the lip plane, a dark mouth bag, then weights ----------------
# v1 defect (measured on the stills): Bone Heat failed on the raw Tripo mesh (68 islands: teeth and spurs are separate shells),
# so the body did not follow the skeleton at all, and the fused lips stretched into long streaks when the jaw opened.
# Fix 1: the head is BISECTED along the lip plane in front of the hinge and the cut edges are SPLIT, so the jaw is free.
# Fix 2: weights are solved by Bone Heat on a VOXEL-REMESHED PROXY (one watertight shell) and TRANSFERRED to the real mesh
#        by nearest-face interpolation; the jaw/head side of the cut is then assigned by which side of the plane a vertex's faces lie.
lipA = Vector((0, y0, z_lip)); lipB = Vector((0, y_hinge, z_hinge))
pn = Vector((0, -(lipB.z - lipA.z), (lipB.y - lipA.y))).normalized()          # normal of the lip plane, pointing up
if pn.z < 0: pn = -pn
me = body.data
bm = bmesh.new(); bm.from_mesh(me)
mw = body.matrix_world.copy(); mwi = mw.inverted()
co_l = mwi @ lipA; n_l = (mwi.to_3x3() @ pn).normalized()
hfaces = [f for f in bm.faces if (mw @ f.calc_center_median()).y < y_hinge - 0.01]
geom = list({v for f in hfaces for v in f.verts}) + list({e for f in hfaces for e in f.edges}) + hfaces
res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co_l, plane_no=n_l, dist=1e-6)
cut = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge) and (mw @ ((e.verts[0].co + e.verts[1].co) / 2)).y < y_hinge - 0.02]
bmesh.ops.split_edges(bm, edges=cut)
bm.verts.index_update()
side = {}
for v in bm.verts:
    p = mw @ v.co
    if p.y < y_hinge + 0.04:
        if v.link_faces:
            cmean = sum(((mw @ f.calc_center_median()) for f in v.link_faces), Vector()) / len(v.link_faces)
        else:
            cmean = p
        side[v.index] = (cmean - lipA).dot(pn) < 0
bm.to_mesh(me); bm.free(); me.update()
LM['mouth_cut_edges'] = len(cut)

hw = float(np.quantile(np.abs(V[(V[:, 1] < y0 + 0.5 * HL) & (np.abs(V[:, 2] - z_lip) < 0.05)][:, 0]), 0.9))
bm = bmesh.new()
yA, yB = y0 + CFG.get('bag_y0_frac', 0.22) * HL, y_hinge - 0.03; wA, wB = CFG.get('bag_w', (0.16, 0.26))[0] * hw, CFG.get('bag_w', (0.16, 0.26))[1] * hw; dz = CFG.get('bag_half_h', 0.035)
def lipz(y): return z_lip + CFG.get('bag_zoff', 0.0) + (z_hinge - z_lip) * (y - y0) / max(y_hinge - y0, 1e-6)
pts = [(-wA, yA, lipz(yA) + dz), (wA, yA, lipz(yA) + dz), (wB, yB, lipz(yB) + dz), (-wB, yB, lipz(yB) + dz),
       (-wA, yA, lipz(yA) - dz), (wA, yA, lipz(yA) - dz), (wB, yB, lipz(yB) - dz), (-wB, yB, lipz(yB) - dz)]
vs = [bm.verts.new(p) for p in pts]
for q in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): bm.faces.new([vs[i] for i in q])
bm.normal_update()
bagm = bpy.data.meshes.new('bag'); bm.to_mesh(bagm); bm.free()
bag = bpy.data.objects.new('bag', bagm); sc.collection.objects.link(bag)
mat = bpy.data.materials.new('maw_interior')
mat.use_nodes = True
bs = mat.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value = CFG.get('mouth_rgba', (0.24, 0.05, 0.05, 1)); bs.inputs['Roughness'].default_value = 1.0
mat.use_backface_culling = False
if CFG.get('mouth_texture'):
    # a PAINTED interior (n21_mouth_tex), one full 0..1 square per face of the bag, embedded like the body texture
    _mi = bpy.data.images.load(os.path.abspath(CFG['mouth_texture'])); _mi.colorspace_settings.name = 'sRGB'
    _tn = mat.node_tree.nodes.new('ShaderNodeTexImage'); _tn.image = _mi
    mat.node_tree.links.new(_tn.outputs['Color'], bs.inputs['Base Color'])
bagm.materials.append(mat)
_uv = bagm.uv_layers.new(name=body.data.uv_layers.active.name)
for _poly in bagm.polygons:
    for _k, _li in enumerate(_poly.loop_indices): _uv.data[_li].uv = ((0, 0), (1, 0), (1, 1), (0, 1))[_k % 4]

# GEOMETRIC WEIGHTS (v2 finding: Bone Heat fails on this mesh AND on its voxel proxy -- the remesh of the open Tripo shell came back
# as 309 shells of 142 faces). So weights are solved here, deterministically: w_b = gate_b(v) / (d(v, segment_b)^4 + eps), top 4,
# normalised. Leg bones are GATED to their own leg (same side of the midline, within 0.32 m of the foot along the body), so a
# left leg never pulls the right flank; the body chain takes every vertex. Inverse-4th-power gives smooth blends at the joints.
for n in DEF:
    if n not in [g.name for g in body.vertex_groups]: body.vertex_groups.new(name=n)
VW = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
bones_w = [n for n in DEF if n != 'root']
Wm = np.zeros((len(VW), len(bones_w)))
for j, n in enumerate(bones_w):
    bh = np.array(arm.data.bones[n].head_local[:]); bt = np.array(arm.data.bones[n].tail_local[:])
    d = bt - bh; t = np.clip(((VW - bh) @ d) / max(d @ d, 1e-9), 0, 1); dist = np.linalg.norm(VW - (bh + t[:, None] * d), axis=1)
    g = np.ones(len(VW))
    def _chain_d(prefix):
        dd = np.full(len(VW), 1e9)
        for k_ in (1, 2, 3):
            b_ = arm.data.bones['%s_%d' % (prefix, k_)]; h_ = np.array(b_.head_local[:]); t_ = np.array(b_.tail_local[:]); d_ = t_ - h_
            tt = np.clip(((VW - h_) @ d_) / max(d_ @ d_, 1e-9), 0, 1); dd = np.minimum(dd, np.linalg.norm(VW - (h_ + tt[:, None] * d_), axis=1))
        return dd
    if n.startswith('leg_'):
        # TUBE GATE (v1 finding: flank and rag vertices inside a leg's column stretched into sheets): only vertices within leg_r of
        # the leg's own bone chain may take a leg bone
        g = (_chain_d(n[:5]) < CFG.get('leg_r', 0.24)).astype(float)
    if n.startswith('arm_'):
        # the hand's claws splay wide: the tube widens toward the tip (arm_r at the shoulder, hand_r at the claws)
        dA = _chain_d(n[:5]); a_ = arms[n[4]]; zt = a_['tip'][2]; zs = a_['sh'][2]
        rr = CFG.get('arm_r', 0.17) + (CFG.get('hand_r', 0.32) - CFG.get('arm_r', 0.17)) * np.clip((zs - VW[:, 2]) / max(zs - zt, 1e-6), 0, 1)
        g = (dA < rr).astype(float)
    if n in ('head', 'jaw'):
        g = ((VW[:, 1] < y_hb + 0.1) & (VW[:, 2] > CFG.get('head_band', 0.55) * H - 0.05)).astype(float)
    if n == 'belly':
        g = ((VW[:, 1] < fy - 0.1) & (VW[:, 2] < z_hip + 0.45) & (np.abs(VW[:, 0]) < CFG.get('arm_x_min', 0.55) - 0.05)).astype(float)
    if n in ('Hips', 'spine', 'chest', 'neck'):
        g = ~((VW[:, 2] < z_hip * 0.85) & (np.abs(VW[:, 0]) > 0.12) & (VW[:, 1] > fy - 0.3)) * 1.0   # thighs/shins are leg, never torso
    Wm[:, j] = g / (dist ** 4 + 1e-6)
# the FOOT BLOCK (below the ankle, inside a leg's gate) rides the foot bone alone, so a bending shin cannot push the sole into the floor
for lg in LEGS:
    j3 = bones_w.index('leg_%s_3' % lg); sgn = 1 if lg == 'L' else -1
    fb = (np.abs(VW[:, 0] - feet[lg]['x']) < CFG.get('leg_col_r', 0.22) + 0.05) & (np.abs(VW[:, 1] - feet[lg]['y']) < 0.4) & (VW[:, 2] < CFG.get('foot_block_z', 0.10))
    Wm[fb] = 0.0; Wm[fb, j3] = 1.0          # the foot block (toes on the ground) rides the planted metatarsus
# UNWEIGHTED FALLBACK (v5 finding: 'neutral_bone' in the GLB -- ~550 vertices of hip/thigh flesh outside every gate stayed at rest
# and stretched into planks): a vertex no gate admits takes the nearest TORSO/LEG bone, ungated
_z = Wm.sum(1) <= 0
if _z.any():
    for j, n_ in enumerate(bones_w):
        if n_.startswith('arm_') or n_ in ('head', 'jaw'): continue
        bh = np.array(arm.data.bones[n_].head_local[:]); bt = np.array(arm.data.bones[n_].tail_local[:]); d_ = bt - bh
        tt = np.clip(((VW[_z] - bh) @ d_) / max(d_ @ d_, 1e-9), 0, 1); dd = np.linalg.norm(VW[_z] - (bh + tt[:, None] * d_), axis=1)
        Wm[_z, j] = 1.0 / (dd ** 4 + 1e-6)
LM['unweighted_fallback_verts'] = int(_z.sum())
# WEIGHT SMOOTHING over the mesh's own edges (v6 finding: 692 edges tore from 3 cm to 27 cm -- every GATE boundary is a weight
# discontinuity, and a 1/d^4 weight lets the gated bone dominate right up to it). Normalise, then diffuse over the edge graph.
Wm = Wm / np.maximum(Wm.sum(1, keepdims=True), 1e-12)
_E = np.array([e.vertices[:] for e in body.data.edges])
_deg = np.zeros(len(VW)); np.add.at(_deg, _E[:, 0], 1); np.add.at(_deg, _E[:, 1], 1)
for _ in range(CFG.get('weight_smooth', 8)):
    _acc = np.zeros_like(Wm); np.add.at(_acc, _E[:, 0], Wm[_E[:, 1]]); np.add.at(_acc, _E[:, 1], Wm[_E[:, 0]])
    Wm = np.where(_deg[:, None] > 0, 0.5 * Wm + 0.5 * _acc / np.maximum(_deg[:, None], 1), Wm)
top = np.argsort(-Wm, 1)[:, :4]
for i in range(len(VW)):
    ws = Wm[i, top[i]]; s_ = ws.sum()
    if s_ <= 0: continue
    for j, w in zip(top[i], ws / s_):
        if w > 1e-3: body.vertex_groups[bones_w[j]].add([i], float(w), 'REPLACE')
heat_ok = False
LM['weights_method'] = 'geometric: gated inverse-distance^4 to bone segments, top 4'
vg = {g.name: g for g in body.vertex_groups}
me = body.data; njaw = 0
for v in me.vertices:
    if v.index not in side: continue
    p = body.matrix_world @ v.co
    if p.z < z_lip - 0.40 or p.z > zh_c + 0.6: continue
    w = 1.0 if p.y < y_hinge else (y_hinge + 0.04 - p.y) / 0.04
    tgt = 'jaw' if side[v.index] else 'head'
    if tgt == 'jaw': njaw += 1
    for g in list(v.groups): g.weight = g.weight * (1 - w)
    vg[tgt].add([v.index], w, 'ADD')
# limit to 4 influences, normalise
for v in me.vertices:
    gs = sorted(v.groups, key=lambda g: -g.weight)
    for g in gs[4:]: g.weight = 0.0
    s = sum(g.weight for g in gs[:4])
    if s > 0:
        for g in gs[:4]: g.weight /= s
unweighted = sum(1 for v in me.vertices if sum(g.weight for g in v.groups) < 1e-6)
gh = bag.vertex_groups.new(name='head'); gj = bag.vertex_groups.new(name='jaw')
gh.add([0, 1, 2, 3], 1.0, 'REPLACE'); gj.add([4, 5, 6, 7], 1.0, 'REPLACE')
for o in sc.objects: o.select_set(False)
bag.select_set(True); body.select_set(True); bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
body = bpy.context.active_object
for m in list(body.modifiers): body.modifiers.remove(m)
md = body.modifiers.new('rig', 'ARMATURE'); md.object = arm
body.parent = arm
LM['weights'] = dict(method=LM['weights_method'], jaw_verts=njaw,
                     unweighted_verts=unweighted, groups=len(body.vertex_groups))

# ---------------- IK + pole angle solve ----------------
pb = arm.pose.bones
for n in DEF: pb[n].rotation_mode = 'QUATERNION'
for lg in LEGS:
    c = pb['leg_%s_2' % lg].constraints.new('IK'); c.target = arm; c.subtarget = 'ik_' + lg
    c.pole_target = arm; c.pole_subtarget = 'pole_' + lg; c.chain_count = 2
    c2 = pb['leg_%s_3' % lg].constraints.new('COPY_ROTATION'); c2.target = arm; c2.subtarget = 'ik_' + lg
    rest = arm.data.bones['leg_%s_1' % lg].matrix_local.copy()
    best = None
    for ang in np.radians(np.arange(-180, 180, 2.0)):
        c.pole_angle = float(ang); bpy.context.view_layer.update()
        d = (pb['leg_%s_1' % lg].matrix.to_3x3() - rest.to_3x3()); e = float(sum(abs(x) for r in d for x in r))
        if best is None or e < best[0]: best = (e, float(ang))
    c.pole_angle = best[1]; LM['leg_' + lg]['pole_angle_deg'] = round(math.degrees(best[1]), 1); LM['leg_' + lg]['pole_rest_err'] = round(best[0], 5)

def M3(n): return arm.data.bones[n].matrix_local.to_3x3()
def wrot(n, rx=0.0, ry=0.0, rz=0.0):
    # a rotation given about WORLD axes (degrees), expressed in the bone's rest frame
    R = Euler((math.radians(-rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix()
    m = M3(n); return (m.inverted() @ R @ m).to_quaternion()
def wloc(n, v):
    return M3(n).inverted() @ Vector(v)

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def kf(keys, f):
    # keys: [(frame, value), ...] with smoothstep between them (zero tangents: holds read as holds, snaps as snaps)
    if f <= keys[0][0]: return keys[0][1]
    for (fa, va), (fb, vb) in zip(keys, keys[1:]):
        if f <= fb:
            if isinstance(va, (tuple, list)): return tuple(x + (y - x) * ease((f - fa) / max(fb - fa, 1e-9)) for x, y in zip(va, vb))
            return va + (vb - va) * ease((f - fa) / max(fb - fa, 1e-9))
    return keys[-1][1]

# ---------------- clips ----------------
CL = CFG['clips']
def pose_reset():
    for p in pb:
        p.location = (0, 0, 0); p.rotation_quaternion = (1, 0, 0, 0); p.rotation_euler = (0, 0, 0); p.scale = (1, 1, 1)
    for lg in LEGS:
        pb['leg_%s_2' % lg].constraints[0].influence = 1.0; pb['leg_%s_3' % lg].constraints[0].influence = 1.0

def apply(st):
    # channels: body chain + tail + forelimbs (rotations about WORLD axes, +rx = the -Y end UP), Hips location, two feet (IK), fk overrides
    for n in ('Hips', 'spine', 'chest', 'neck', 'head', 'jaw', 'belly',
              'arm_L_1', 'arm_L_2', 'arm_L_3', 'arm_R_1', 'arm_R_2', 'arm_R_3'):
        r = st.get(n)
        if r: pb[n].rotation_quaternion = wrot(n, *r)
    if 'pelvis_loc' in st: pb['Hips'].location = wloc('Hips', st['pelvis_loc'])
    for lg in LEGS:
        o = st.get('foot_' + lg, (0, 0, 0, 0))
        pb['ik_' + lg].location = wloc('ik_' + lg, o[:3])
        pb['ik_' + lg].rotation_quaternion = wrot('ik_' + lg, o[3] if len(o) > 3 else 0.0)
        if ('fk_' + lg) in st:
            infl, r1, r2, r3 = st['fk_' + lg]
            pb['leg_%s_2' % lg].constraints[0].influence = infl; pb['leg_%s_3' % lg].constraints[0].influence = infl
            pb['leg_%s_1' % lg].rotation_quaternion = wrot('leg_%s_1' % lg, *r1)
            pb['leg_%s_2' % lg].rotation_quaternion = wrot('leg_%s_2' % lg, *r2)
            pb['leg_%s_3' % lg].rotation_quaternion = wrot('leg_%s_3' % lg, *r3)
for p in pb: p.rotation_mode = 'QUATERNION'

ARM_K = 1.0
def arms_(st, l1, l2, l3, r1=None, r2=None, r3=None):
    # (n19) the long arms hang against the belly: a big arm swing tears the shared skin into streaks, so every clip's arm
    # rotation is scaled by ARM_K (set per clip in clip_state); the thrash keeps its full swing
    k_ = ARM_K; sc_ = lambda t: tuple(v * k_ for v in t) if t is not None else None
    l1, l2, l3, r1, r2, r3 = sc_(l1), sc_(l2), sc_(l3), sc_(r1), sc_(r2), sc_(r3)
    st['arm_L_1'], st['arm_L_2'], st['arm_L_3'] = l1, l2, l3
    st['arm_R_1'], st['arm_R_2'], st['arm_R_3'] = (r1 or (l1[0], -l1[1], -l1[2])), (r2 or (l2[0], -l2[1], -l2[2])), (r3 or (l3[0], -l3[1], -l3[2]))

def gait(f, N, v, duty, offs, lift, bob, pitch_amp, flex_amp, lead):
    T = N / FPS; S = v * duty * T; st = {}
    ph = f / N
    for lg in LEGS:
        u = (ph + offs[lg]) % 1.0
        if u < duty:
            s = u / duty; dy = -S / 2 + S * s; dz = 0.0; rx = 0.0
        else:
            s = (u - duty) / (1 - duty); dy = S / 2 - S * ease(s); dz = lift * math.sin(math.pi * s); rx = 0.0   # a digitigrade meta is long: no toe-down
        st['foot_' + lg] = (0.0, dy, dz, rx); st.setdefault('_stance', {})[lg] = u < duty
    w = 2 * math.pi * ph
    st['pelvis_loc'] = (0.04 * math.sin(w), 0.0, bob[0] * math.cos(2 * w))
    st['Hips'] = (pitch_amp * math.sin(2 * w), 4.0 * math.sin(w), 4.0 * math.sin(w))
    st['spine'] = (-0.5 * pitch_amp * math.sin(2 * w + 0.4), 0, -2.0 * math.sin(w))
    st['chest'] = (0, -2.0 * math.sin(w), -2.0 * math.sin(w + 0.3))
    st['neck'] = (-0.6 * pitch_amp * math.sin(2 * w + 0.8), 0, -1.5 * math.sin(w + 0.5))      # the head is stabilised against the bob
    st['head'] = (-0.4 * pitch_amp * math.sin(2 * w + 1.2), 0, 0)
    st['jaw'] = (-2.0 - 2.0 * (0.5 + 0.5 * math.sin(2 * w)), 0, 0)
    st['tail1'] = (2.0 * math.sin(2 * w), 0, -6.0 * math.sin(w + 0.6)); st['tail2'] = (1.5 * math.sin(2 * w + 0.5), 0, -8.0 * math.sin(w + 1.2)); st['tail3'] = (0, 0, -10.0 * math.sin(w + 1.8))
    sw = math.sin(w)
    arms_(st, (10 + flex_amp * sw, 0, 0), (-15, 0, 0), (-10, 0, 0), (10 - flex_amp * sw, 0, 0), (-15, 0, 0), (-10, 0, 0))
    return st

def clip_state(name, f):
    global ARM_K
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name)
    ARM_K = CFG.get('arm_k_thrash', 0.7) if k in ('thrash', 'impale', 'cast') else CFG.get('arm_k', 0.35)
    if k in ('walk', 'run'):
        # a lumbering waddle: wide body roll, the gut swinging a beat behind the hips, arms hanging and swinging long
        st = gait(f, N, c['speed'], c.get('duty', 0.62 if k == 'walk' else 0.40), dict(L=0.0, R=0.5), 0.12 if k == 'walk' else 0.18,
                  (0.03 if k == 'walk' else 0.05, 2), 2.0, 14.0 if k == 'walk' else 22.0, 0)
        w = 2 * math.pi * f / N
        st['pelvis_loc'] = (0.07 * math.sin(w), st['pelvis_loc'][1], st['pelvis_loc'][2])
        st['Hips'] = (st['Hips'][0], 7.0 * math.sin(w), 5.0 * math.sin(w))
        st['belly'] = (4.0 * math.sin(2 * w - 1.0), 6.0 * math.sin(w - 1.2), 0)
        return st
    if k == 'idle':
        w = 2 * math.pi * f / N; st = {}
        st['pelvis_loc'] = (0, 0, -0.02 * (0.5 - 0.5 * math.cos(w)))
        st['chest'] = (2.5 * math.sin(w), 0, 2.0 * math.sin(w + 0.5)); st['belly'] = (3.0 * math.sin(w - 0.8), 2.0 * math.sin(2 * w), 0)
        burp = math.exp(-((f / N - 0.6) * 12) ** 2)
        st['neck'] = (2.0 * math.sin(w) + 10 * burp, 0, 8.0 * math.sin(w + 0.3)); st['jaw'] = (-2.0 - 24.0 * burp, 0, 0)
        arms_(st, (4 + 3 * math.sin(w), 0, 0), (-6, 0, 0), (-4, 0, 0))
        return st
    if k == 'bite':
        # the CHARGING BITE: lean back, then the whole body pitches forward and down, the head thrusts out and the jaw SNAPS at contact
        cf = c['contact']; st = {}; a0 = max(3, cf - 8)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.12), (cf, -0.35), (cf + 6, -0.25), (N, 0)], f), kf([(0, 0), (a0, 0.02), (cf, -0.10), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (a0, 8), (cf, -14), (cf + 6, -10), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (a0, 10), (cf, -12), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (a0, 16), (cf, -4), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (a0, -10), (cf - 2, -48), (cf, 0), (cf + 4, -6), (N, -2)], f), 0, 0)
        st['belly'] = (kf([(0, 0), (a0, -6), (cf, 10), (cf + 4, -6), (N, 0)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, -20), (cf, 40), (N, 0)], f), 0, 10), (kf([(0, 0), (cf, -20), (N, 0)], f), 0, 0), (0, 0, 0))
        return st
    if k == 'thrash':
        # a flailing double rake: both long arms swing up and slash across and down at the contact, the torso twisting with them
        cf = c['contact']; st = {}; a0 = max(3, cf - 9)
        st['Hips'] = (kf([(0, 0), (a0, 6), (cf, -8), (N, 0)], f), 0, kf([(0, 0), (a0, 16), (cf, -18), (cf + 8, 10), (cf + 14, 0), (N, 0)], f))
        st['chest'] = (kf([(0, 0), (a0, 10), (cf, -10), (N, 0)], f), 0, kf([(0, 0), (a0, 12), (cf, -14), (N, 0)], f))
        st['jaw'] = (kf([(0, -2), (cf - 2, -30), (cf + 5, -4), (N, -2)], f), 0, 0)
        st['belly'] = (0, kf([(0, 0), (a0, -10), (cf, 12), (cf + 8, -8), (N, 0)], f), 0)
        arms_(st, (kf([(0, 0), (a0, 95), (cf, -20), (cf + 8, 40), (cf + 14, -10), (N, 0)], f), 0, kf([(0, 0), (a0, 20), (cf, -30), (N, 0)], f)),
                  (kf([(0, 0), (a0, -30), (cf, 10), (N, 0)], f), 0, 0), (kf([(0, 0), (cf, 25), (N, 0)], f), 0, 0),
              (kf([(0, 0), (a0, 60), (cf + 2, 95), (cf + 8, -20), (N, 0)], f), 0, kf([(0, 0), (cf + 2, -20), (cf + 8, 30), (N, 0)], f)),
                  (kf([(0, 0), (cf + 2, -30), (cf + 8, 10), (N, 0)], f), 0, 0), (kf([(0, 0), (cf + 8, 25), (N, 0)], f), 0, 0))
        return st
    if k in ('vomit', 'vomit3'):
        # the gut HEAVES (belly pumps in and out), the torso rears back, then pitches forward and the jaw gapes at the release;
        # vomit holds the spray; vomit3 heaves three times, the release on the first
        rf = c['release']; st = {}; a0 = max(3, rf - 9); ho = c.get('hold', 14)
        pump = math.sin((f - a0) / 4.0 * math.pi) if a0 <= f <= rf + ho else 0.0
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.10), (rf, -0.12), (rf + ho, -0.10), (N, 0)], f), 0)
        st['Hips'] = (kf([(0, 0), (a0, 8), (rf, -8), (rf + ho, -6), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (a0, 14), (rf, -14), (rf + ho, -12), (N, 0)], f) + 3 * pump, 0, 0)
        st['neck'] = (kf([(0, 0), (a0, 12), (rf, -8), (rf + ho, -8), (N, 0)], f), 0, kf([(rf, 0), (rf + 5, 6), (rf + 10, -6), (rf + ho, 0)], f))
        st['jaw'] = (kf([(0, -2), (a0, -8), (rf - 1, -55), (rf + ho, -50), (rf + ho + 5, -4), (N, -2)], f) - 4 * abs(pump), 0, 0)
        st['belly'] = (8 * pump, 0, 0)
        arms_(st, (kf([(0, 0), (a0, 20), (rf, 30), (N, 0)], f), 0, 15), (-30, 0, 0), (-10, 0, 0))
        return st
    if k == 'impale':
        # the IMPALE: both great arms rise high and back over the shoulders, the body rears, then the spikes are DRIVEN forward and down
        # into the target at the contact (the hit frame), held there a beat, wrenched out, recover
        cf = c['contact']; st = {}; a0 = max(3, cf - 14); ho = c.get('hold', 6)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.10), (cf, -0.28), (cf + ho, -0.26), (N, 0)], f), kf([(0, 0), (a0, 0.02), (cf, -0.08), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (a0, 10), (cf, -14), (cf + ho, -12), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (a0, 16), (cf, -16), (cf + ho, -14), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (a0, 10), (cf, -6), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (a0, -6), (cf - 2, -30), (cf + ho, -20), (N, -2)], f), 0, 0)
        up = kf([(0, 0), (a0, 120), (cf - 3, 125), (cf, 35), (cf + ho, 30), (cf + ho + 6, 40), (N, 0)], f)
        el = kf([(0, 0), (a0, -50), (cf, -5), (cf + ho, -5), (N, 0)], f)
        arms_(st, (up, 0, kf([(0, 0), (a0, 10), (cf, -12), (N, 0)], f)), (el, 0, 0), (kf([(0, 0), (cf, 10), (N, 0)], f), 0, 0))
        return st
    if k == 'cast':
        # the RIFT CAST (aoe / vortex): the great arms sweep up and OUT, the body swells upright, then the arms throw forward at the
        # release (the rift opens at the target -- runtime VFX), hold, recover
        rf = c['release']; st = {}; a0 = max(3, rf - 12); ho = c.get('hold', 10)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.06), (rf, -0.10), (rf + ho, -0.08), (N, 0)], f), kf([(0, 0), (a0, 0.06), (rf, 0.0), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (a0, 10), (rf, -6), (rf + ho, -5), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (a0, 18), (rf, -8), (rf + ho, -6), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (a0, 14), (rf, -4), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (a0, -12), (rf, -40), (rf + ho, -36), (rf + ho + 5, -4), (N, -2)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, 70), (rf, 80), (rf + ho, 70), (N, 0)], f), 0, kf([(0, 0), (a0, 55), (rf, 5), (rf + ho, 5), (N, 0)], f)),
                  (kf([(0, 0), (a0, -20), (rf, -5), (N, 0)], f), 0, 0), (0, 0, 0))
        return st
    if k == 'drain':
        # the LIFE DRAIN (nova around itself): the arms spread wide and low, the body hunches and SHUDDERS as it pulls, the nova
        # fires at the release (runtime VFX); held, then recover
        rf = c['release']; st = {}; a0 = max(3, rf - 16); ho = c.get('hold', 10)
        sh = math.sin(f * 2.2) if a0 <= f <= rf + ho else 0.0
        st['pelvis_loc'] = (0, 0, kf([(0, 0), (a0, -0.06), (rf, -0.12), (rf + ho, -0.12), (N, 0)], f))
        st['chest'] = (kf([(0, 0), (a0, 8), (rf, 14), (rf + ho, 12), (N, 0)], f) + 2 * sh, 0, 2 * sh)
        st['neck'] = (kf([(0, 0), (a0, 18), (rf, 24), (rf + ho, 20), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (a0, -20), (rf, -50), (rf + ho, -46), (rf + ho + 4, -4), (N, -2)], f), 0, 0)
        st['belly'] = (3 * sh, 0, 0)
        arms_(st, (kf([(0, 0), (a0, 20), (rf, 30), (rf + ho, 28), (N, 0)], f), 0, kf([(0, 0), (a0, 60), (rf, 75), (rf + ho, 70), (N, 0)], f)),
                  (kf([(0, 0), (a0, -10), (N, 0)], f), 0, 0), (0, 0, 0))
        return st
    if k == 'hit':
        st = {}
        st['pelvis_loc'] = (kf([(0, 0), (3, 0.05), (N, 0)], f), kf([(0, 0), (3, 0.14), (N, 0)], f), 0)
        st['chest'] = (kf([(0, 0), (3, 14), (N, 0)], f), 0, kf([(0, 0), (3, 10), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (3, 18), (N, 0)], f), 0, kf([(0, 0), (3, 12), (N, 0)], f))
        st['jaw'] = (kf([(0, -2), (2, -28), (8, -4), (N, -2)], f), 0, 0)
        st['belly'] = (kf([(0, 0), (2, -10), (5, 8), (N, 0)], f), 0, 0)
        arms_(st, (kf([(0, 0), (3, 35), (N, 0)], f), 0, 20), (kf([(0, 0), (3, -30), (N, 0)], f), 0, 0), (0, 0, 0))
        return st
    if k == 'death':
        # it COLLAPSES in place onto its gut (kept compact for the canvas): the knees buckle, the body sinks and slumps forward over
        # the belly, the head lolls, the long arms flop to the floor; held. Ground solved.
        st = {}; c0, c1 = 8, 30
        st['pelvis_loc'] = (0, kf([(0, 0), (c0, 0.06), (N, 0.10)], f), kf([(0, 0), (c0, 0.02), (c1, -z_hip * 0.55), (N, -z_hip * 0.58)], f))
        st['Hips'] = (kf([(0, 0), (c0, 6), (c1, -28), (N, -30)], f), kf([(0, 0), (c1, 8), (N, 9)], f), 0)
        st['chest'] = (kf([(0, 0), (c0, 12), (c1, -22), (N, -24)], f), 0, kf([(0, 0), (c1, 10), (N, 12)], f))
        st['neck'] = (kf([(0, 0), (c0, 22), (c1, -20), (N, -26)], f), 0, kf([(0, 0), (c1, 18), (N, 22)], f))
        st['jaw'] = (kf([(0, -2), (c0, -40), (N, -26)], f), 0, 0)
        st['belly'] = (kf([(0, 0), (c0, -8), (c1, 6), (N, 6)], f), 0, 0)
        arms_(st, (kf([(0, 0), (c0, 30), (c1, 10), (N, 8)], f), 0, kf([(0, 0), (c1, 25), (N, 28)], f)), (kf([(0, 0), (c1, -15), (N, -18)], f), 0, 0), (0, 0, 0))
        return st
    raise KeyError(k)

# MOTION SCALE: the clips' typed body offsets (lunges, the leap's 1.1 m rise, the hit shove) are metres for the 5.47 m build; a
# creature scaled to fit the canvas scales them with it. Gait offsets are NOT scaled (they are the foot-lock stride, set by speed)
# and the derived drops (reach, death to the floor) already follow the mesh.
_clip_state_raw = clip_state
def clip_state(name, f):
    st = _clip_state_raw(name, f); ms = CFG.get('motion_scale', 1.0); k = CL[name].get('kind_fn', name)
    if ms != 1.0 and k not in ('walk', 'run', 'death'):
        if 'pelvis_loc' in st: st['pelvis_loc'] = tuple(v * ms for v in st['pelvis_loc'])
        for lg in LEGS:
            if 'foot_' + lg in st: o = st['foot_' + lg]; st['foot_' + lg] = (o[0] * ms, o[1] * ms, o[2] * ms) + tuple(o[3:])
    return st

dg = None
def mesh_minz():
    d = bpy.context.evaluated_depsgraph_get(); e = body.evaluated_get(d); m = e.to_mesh()
    co = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', co); e.to_mesh_clear()
    co = co.reshape(-1, 3) @ np.array(body.matrix_world.to_3x3()).T + np.array(body.matrix_world.translation)
    return float(co[:, 2].min()), co

ROOTREST = {n: arm.data.bones[n].matrix_local.copy() for n in DEF}
def readback():
    out = {}
    for n in DEF:
        b = pb[n]; p = b.parent
        if p is None: B = ROOTREST[n].inverted() @ b.matrix
        else: B = (ROOTREST[p.name].inverted() @ ROOTREST[n]).inverted() @ (p.matrix.inverted() @ b.matrix)
        l, q, s = B.decompose(); out[n] = (l.copy(), q.copy(), s.copy())
    return out

BAKED, LINT = {}, {}
rest_verts = None
for name, c in CL.items():
    N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    frames, minz, ankles, verts0 = [], [], {lg: [] for lg in LEGS}, None
    for f in range(N + 1):
        pose_reset(); st = clip_state(name, f); apply(st); bpy.context.view_layer.update()
        # REACH SOLVE on the POSED skeleton (the analytic drop in gait() ignores pelvis/chest rotation): sink the body until every
        # IK leg's target is within 98.5 % of its chain from its posed joint. Two passes; the residual is measured below.
        for _ in range(3):
            need = 0.0
            for lg in LEGS:
                if pb['leg_%s_2' % lg].constraints[0].influence < 0.5: continue
                Jw = arm.matrix_world @ pb['leg_%s_1' % lg].head; Tw = arm.matrix_world @ pb['ik_' + lg].head
                Lc = LM['leg_' + lg]['chain_len'] * 0.985; dxy = math.hypot(Tw.x - Jw.x, Tw.y - Jw.y)
                if (Tw - Jw).length > Lc and dxy < Lc: need = max(need, (Jw.z - Tw.z) - math.sqrt(Lc * Lc - dxy * dxy))
            if need < 1e-4: break
            pb['Hips'].location = pb['Hips'].location + wloc('Hips', (0, 0, -need - 0.002)); bpy.context.view_layer.update()
        ikerr = max([((arm.matrix_world @ pb['leg_%s_2' % lg].tail) - (arm.matrix_world @ pb['ik_' + lg].head)).length
                    for lg in LEGS if pb['leg_%s_2' % lg].constraints[0].influence > 0.99], default=0.0)
        ikmax = max(ikmax, ikerr) if f else ikerr
        mz, co = mesh_minz()
        # CONTACT SOLVE (raptor): a TAIL or a FORELIMB that would go through the floor is lifted 2 deg at a time at its root bone
        # (tail1 / arm_<S>_1) until its lowest point sits on the ground -- the kick's counter-balanced tail, the leap's landing claws.
        for _ in range(40):
            if mz >= -0.003: break
            wv = co[int(np.argmin(co[:, 2]))]
            if abs(wv[0]) > 0.2 and wv[1] < fy + 0.2: ch = 'arm_%s_1' % ('L' if wv[0] > 0 else 'R')   # a claw on the floor: lift the arm
            else: break
            r = st.get(ch, (0, 0, 0)); st[ch] = (r[0] + (-2.0 if ch == 'tail1' else 2.0), r[1], r[2])   # the tail points +Y: lifting its tip is -rx
            apply(st); bpy.context.view_layer.update(); mz, co = mesh_minz()
        for _ in range(4):
            if not (c.get('ground_solve') and mz < 0.0): break
            l = pb['Hips'].location.copy(); pb['Hips'].location = l + wloc('Hips', (0, 0, -mz + 0.003)); bpy.context.view_layer.update()
            mz, co = mesh_minz()
        if f == 0: verts0 = co.copy()
        if f == N: vN = co.copy()
        minz.append(mz)
        if mz <= min(minz): worst = (f, [round(float(x), 3) for x in co[int(np.argmin(co[:, 2]))]])
        for lg in LEGS: ankles[lg].append(tuple(arm.matrix_world @ pb['leg_%s_2' % lg].tail) + (float(st.get('_stance', {}).get(lg, False)),))
        frames.append(readback())
    BAKED[name] = frames
    L = dict(frames=len(frames), ik_residual_max_m=round(ikmax, 4), min_z_m=round(min(minz), 4), worst_frame_vertex=worst, penetration_frames=int(sum(1 for z in minz if z < -0.01)))
    if c['kind'] == 'loop':
        L['loop_seam_max_vert_m'] = round(float(np.abs(vN - verts0).max()), 5)
    if c.get('speed'):
        v = c['speed']; slide = []
        for lg in LEGS:
            P = np.array(ankles[lg]); P[:, 1] -= v * np.arange(len(P)) / FPS     # world = local + root travel (-y)
            st_ = P[:, 3] > 0.5                                                   # stance as the gait declares it
            runs, cur = [], []
            for i, s in enumerate(st_):
                if s: cur.append(i)
                elif cur: runs.append(cur); cur = []
            if cur: runs.append(cur)
            for r in runs:
                if len(r) > 1: slide.append(float(np.linalg.norm(P[r][:, :2] - P[r[0]][:2], axis=1).max()))
        L['footlock_max_slide_m'] = round(max(slide) if slide else 0.0, 4); L['stance_runs'] = len(slide)
    LINT[name] = L
    print('clip %-14s %s' % (name, L))

# ---------------- strip controls, key deform bones ----------------
pose_reset()
for p in pb:
    for cn in list(p.constraints): p.constraints.remove(cn)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
for n in [b.name for b in arm.data.edit_bones if not b.use_deform]: arm.data.edit_bones.remove(arm.data.edit_bones[n])
bpy.ops.object.mode_set(mode='OBJECT')
pb = arm.pose.bones
ad = arm.animation_data_create()
for name, frames in BAKED.items():
    act = bpy.data.actions.new(name); act.use_fake_user = True; ad.action = act
    prev = {}
    for f, fr in enumerate(frames):
        for n, (l, q, s) in fr.items():
            if n in prev and prev[n].dot(q) < 0: q = -q
            prev[n] = q
            p = pb[n]; p.rotation_quaternion = q; p.keyframe_insert('rotation_quaternion', frame=f, group=n)
            if n in ('Hips', 'root'): p.location = l; p.keyframe_insert('location', frame=f, group=n)
    ad.action = None
    tr = ad.nla_tracks.new(); tr.name = name; tr.strips.new(name, 0, act); tr.mute = False
for p in pb: p.location = (0, 0, 0); p.rotation_quaternion = (1, 0, 0, 0)
ad.action = None

# PAINTED TEXTURE, EMBEDDED (the e42 lesson: a texture used by the renders but never written into the file is not shipped). The bake
# was made on the prep mesh's UVs; the mouth cut interpolates UVs, so the same map applies.
if CFG.get('texture'):
    img = bpy.data.images.load(os.path.abspath(CFG['texture'])); img.colorspace_settings.name = 'sRGB'; nset = 0
    m0 = body.data.materials[0]
    for nd in m0.node_tree.nodes:
        if nd.type == 'TEX_IMAGE': nd.image = img; nset += 1
    assert nset, 'no image node on the body material'
    LM['texture'] = dict(path=CFG['texture'], nodes=nset)
for o in sc.objects: o.select_set(o in (arm, body))
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_selection=True, export_animations=True, export_animation_mode='NLA_TRACKS',
                          export_def_bones=True, export_image_format='JPEG', export_jpeg_quality=92, export_morph=False)
LM['deform_bones'] = DEF
json.dump(dict(landmarks=LM, lint=LINT, clips={k: {kk: vv for kk, vv in v.items()} for k, v in CL.items()}), open(OUT.replace('.glb', '.rig.json'), 'w'), indent=1,
          default=lambda x: list(x) if hasattr(x, '__iter__') else str(x))
print('wrote', OUT)
