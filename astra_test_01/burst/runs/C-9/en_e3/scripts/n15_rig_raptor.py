# EN-E3 stage 3+4 for the RAPTOR (n10 with a horizontal-biped skeleton: digitigrade hind legs + toes, forelimbs; the jaw cut, mouth
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

# ---------------- landmarks (RAPTOR: a horizontal biped -- two digitigrade hind legs, two forelimbs, long neck, head, long tail) ----------------
low = V[V[:, 2] < CFG.get('foot_band', 0.05) * H]
feet = {}
for side, sgn in (('L', 1), ('R', -1)):
    P = low[low[:, 0] * sgn > 0.02]
    feet[side] = dict(x=float(np.median(P[:, 0])), y=float(np.median(P[:, 1])), toe_y=float(np.quantile(P[:, 1], 0.02)), heel_y=float(np.quantile(P[:, 1], 0.98)))
fy = (feet['L']['y'] + feet['R']['y']) / 2
T_ = V[(np.abs(V[:, 0]) < 0.15) & (np.abs(V[:, 1] - fy) < 0.2)]
z_back = float(np.quantile(T_[:, 2], 0.97))
z_hip = CFG.get('hip_frac', 0.80) * z_back
def ztop(y, w=0.08):
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.2)]; return float(np.quantile(S[:, 2], 0.85))
def zmid_at(y, w=0.05):
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.15)]; return float((S[:, 2].min() + S[:, 2].max()) / 2), S
legj = {}
for side, sgn in (('L', 1), ('R', -1)):
    Lp = V[(V[:, 0] * sgn > CFG.get('leg_x_min', 0.06)) & (np.abs(V[:, 1] - feet[side]['y']) < 0.7) & (V[:, 2] < z_hip)]
    kz = Lp[(Lp[:, 2] > 0.40 * z_hip) & (Lp[:, 2] < 0.70 * z_hip)]; az = Lp[(Lp[:, 2] > 0.10 * z_hip) & (Lp[:, 2] < 0.36 * z_hip)]
    K = (float(np.median(kz[:, 0])), float(np.quantile(kz[:, 1], 0.08)) + 0.06, float(np.median(kz[:, 2])))
    A = (float(np.median(az[:, 0])), float(np.quantile(az[:, 1], 0.92)) - 0.05, float(np.median(az[:, 2])))
    legj[side] = dict(K=K, A=A)
HL = CFG.get('head_len_frac', 0.11) * LF
y_hb = y0 + HL
zh_c, _ = zmid_at(y0 + 0.5 * HL, 0.06)
_, Ssn = zmid_at(y0 + 0.10 * HL, 0.06)
z_lip = float(Ssn[:, 2].min() + CFG.get('lip_z_frac', 0.45) * np.ptp(Ssn[:, 2]))
y_hinge = y0 + CFG.get('hinge_frac', 0.85) * HL
z_hinge = z_lip + CFG.get('hinge_rise', 0.03)
TLF = CFG.get('tail_frac', 0.45); y_tb = y1 - TLF * LF
def zmid_up(y, w=0.06):
    # the TAIL's mid height, legs excluded: v2 took the slice's min z from the legs below it, put the tail bone at knee height
    # and the tail took 1046 foot vertices -- the feet stood still while their bones walked (the stretched 'box' in the strips)
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.15) & (V[:, 2] > 0.55 * z_hip)]
    return float((S[:, 2].min() + S[:, 2].max()) / 2) if len(S) > 3 else z_hip
z_tb = zmid_up(y_tb); z_tt = zmid_up(y1 - 0.08)
ank_z = None
arms = {}
for side, sgn in (('L', 1), ('R', -1)):
    Ap = V[(V[:, 0] * sgn > CFG.get('arm_x_min', 0.10)) & (V[:, 1] < fy - CFG.get('arm_y_off', 0.35)) & (V[:, 1] > y_hb) & (V[:, 2] > 0.25 * z_back) & (V[:, 2] < 0.95 * z_back)]
    tip = Ap[np.argmin(Ap[:, 2])]; top = Ap[np.argmax(Ap[:, 2] - 2.0 * np.abs(Ap[:, 0]))]
    sh = np.array([top[0] * 0.55, top[1], top[2] - 0.05])
    def at(t):
        p = sh + (tip - sh) * t; m = np.abs(Ap[:, 2] - p[2]) < 0.06
        return (float(np.median(Ap[m, 0])), float(np.median(Ap[m, 1])), float(p[2])) if m.sum() > 5 else tuple(map(float, p))
    arms[side] = dict(sh=tuple(map(float, sh)), el=at(0.45), wr=at(0.80), tip=tuple(map(float, tip)))
y_ch = float(np.mean([arms[s]['sh'][1] for s in arms])); z_ch = ztop(y_ch) - 0.18
LM.update(H=H, y_snout=y0, y_tail=y1, z_back=z_back, z_hip=z_hip, y_head_base=y_hb, z_lip=z_lip, y_hinge=y_hinge, feet=feet, arms=arms, legj=legj)

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
y_hp = fy + CFG.get('hip_back', 0.05); y_sp = (y_hp + y_ch) / 2
bone('Hips', (0, y_hp + 0.15, z_hip), (0, y_sp, (z_hip + z_ch) / 2), 'root')
bone('spine', (0, y_sp, (z_hip + z_ch) / 2), (0, y_ch, z_ch), 'Hips', conn=True)
y_nk = (y_ch + y_hb) / 2; z_nk = (z_ch + zh_c) / 2 + 0.08
bone('chest', (0, y_ch, z_ch), (0, y_nk, z_nk), 'spine', conn=True)
bone('neck', (0, y_nk, z_nk), (0, y_hb + 0.02, zh_c + 0.03), 'chest', conn=True)
bone('head', (0, y_hb + 0.02, zh_c + 0.03), (0, y0 + 0.03, zh_c + 0.03), 'neck', conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.06, z_lip - 0.05), 'head')
tl = y1 - y_tb
bone('tail1', (0, y_hp + 0.15, z_hip), (0, y_tb, z_tb), 'Hips')
bone('tail2', (0, y_tb, z_tb), (0, y_tb + 0.40 * tl, z_tb + 0.40 * (z_tt - z_tb)), 'tail1', conn=True)
bone('tail3', (0, y_tb + 0.40 * tl, z_tb + 0.40 * (z_tt - z_tb)), (0, y1, z_tt), 'tail2', conn=True)
LEGS = ['L', 'R']
for lg in LEGS:
    f = feet[lg]; sgn = 1 if lg == 'L' else -1
    J = (sgn * CFG.get('hip_x', 0.20), y_hp, z_hip - 0.05); K = legj[lg]['K']; A = legj[lg]['A']
    B = (f['x'], f['y'] + 0.02, 0.07); Tt = (f['x'], f['toe_y'] + 0.03, 0.03)
    bone('leg_%s_1' % lg, J, K, 'Hips'); bone('leg_%s_2' % lg, K, A, 'leg_%s_1' % lg, conn=True)
    bone('leg_%s_3' % lg, A, B, 'leg_%s_2' % lg, conn=True); bone('leg_%s_4' % lg, B, Tt, 'leg_%s_3' % lg, conn=True)
    bone('ik_%s' % lg, A, B, 'root', deform=False)
    bone('pole_%s' % lg, (K[0], K[1] - 0.6, K[2]), (K[0], K[1] - 0.6, K[2] + 0.1), 'root', deform=False)   # the knee points FORWARD
    LM['leg_' + lg] = dict(joint=J, knee=K, ankle=A, toe=Tt, ball=B, chain_len=round(float((Vector(K) - Vector(J)).length + (Vector(A) - Vector(K)).length), 4),
                           rest_reach=round(float((Vector(A) - Vector(J)).length), 4))
for s_ in ('L', 'R'):
    a_ = arms[s_]
    bone('arm_%s_1' % s_, a_['sh'], a_['el'], 'chest'); bone('arm_%s_2' % s_, a_['el'], a_['wr'], 'arm_%s_1' % s_, conn=True)
    bone('arm_%s_3' % s_, a_['wr'], a_['tip'], 'arm_%s_2' % s_, conn=True)
bpy.ops.object.mode_set(mode='OBJECT')
DEF = [b.name for b in arm.data.bones if b.use_deform]
ank_z = min(LM['leg_L']['ankle'][2], LM['leg_R']['ankle'][2])

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
    if n.startswith('leg_'):
        sgn = 1 if n[4] == 'L' else -1
        g = ((VW[:, 0] * sgn > 0.03) & (np.abs(VW[:, 1] - feet[n[4]]['y']) < 0.8) & (VW[:, 2] < z_hip + 0.05)).astype(float)
        if n.endswith('_1'): g = np.maximum(g, 0.3 * ((VW[:, 0] * sgn > 0.05) & (np.abs(VW[:, 1] - feet[n[4]]['y']) < 0.8) & (VW[:, 2] < z_hip + 0.2)))
    if n.startswith('arm_'):
        sgn = 1 if n[4] == 'L' else -1
        g = ((VW[:, 0] * sgn > 0.05) & (VW[:, 1] < y_ch + 0.25) & (VW[:, 1] > y_hb - 0.05) & (VW[:, 2] < z_ch + 0.1)).astype(float)
    if n.startswith('tail'):
        g = ((VW[:, 1] > y_hp) & (VW[:, 2] > 0.5 * z_hip)).astype(float)
    if n in ('head', 'jaw'):
        g = (VW[:, 1] < y_hb + 0.25).astype(float)
    Wm[:, j] = g / (dist ** 4 + 1e-6)
# the FOOT BLOCK (below the ankle, inside a leg's gate) rides the foot bone alone, so a bending shin cannot push the sole into the floor
for lg in LEGS:
    j3 = bones_w.index('leg_%s_3' % lg); j4 = bones_w.index('leg_%s_4' % lg); sgn = 1 if lg == 'L' else -1
    fb = (VW[:, 0] * sgn > 0.02) & (np.abs(VW[:, 1] - feet[lg]['y']) < 0.6) & (VW[:, 2] < CFG.get('foot_block_z', 0.10))
    Wm[fb] = 0.0; Wm[fb, j3] = 1.0          # the foot block (toes on the ground) rides the planted metatarsus
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
    for n in ('Hips', 'spine', 'chest', 'neck', 'head', 'jaw', 'tail1', 'tail2', 'tail3',
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

def arms_(st, l1, l2, l3, r1=None, r2=None, r3=None):
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
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name)
    if k == 'idle':
        w = 2 * math.pi * f / N; st = {}
        st['pelvis_loc'] = (0, 0, -0.02 * (0.5 - 0.5 * math.cos(w)))
        st['Hips'] = (1.5 * math.sin(w), 0, 2.0 * math.sin(w))
        st['chest'] = (2.0 * math.sin(w), 0, 0)
        st['neck'] = (3.0 * math.sin(w + 0.5), 0, 14.0 * math.sin(w))                     # scanning: the head sweeps left and right
        snap = math.exp(-((f / N - 0.62) * 12) ** 2)
        st['head'] = (2.0 * math.sin(2 * w) + 6 * snap, 4.0 * math.sin(w), 6.0 * math.sin(w + 0.7))
        st['jaw'] = (-3.0 - 20.0 * snap, 0, 0)
        st['tail1'] = (2.0 * math.sin(w), 0, 8.0 * math.sin(w + 0.9)); st['tail2'] = (0, 0, 10.0 * math.sin(w + 1.6)); st['tail3'] = (0, 0, 12.0 * math.sin(w + 2.3))
        arms_(st, (12 + 4 * math.sin(w), 0, 0), (-18 - 6 * math.sin(w + 1), 0, 0), (-15 + 10 * snap, 0, 0))
        return st
    if k == 'walk':
        return gait(f, N, c['speed'], c.get('duty', 0.6), dict(L=0.0, R=0.5), 0.16, (0.03, 2), 2.5, 8.0, 0)
    if k == 'run':
        return gait(f, N, c['speed'], c.get('duty', 0.35), dict(L=0.0, R=0.5), 0.30, (0.06, 2), 5.0, 14.0, 0)
    if k == 'swipe':
        # double forelimb RAKE: both arms wind back and up, the chest lunges forward and down, the claws rake down through the
        # target at the contact frame (left leads, right one frame behind); the jaw opens with it
        cf = c['contact']; st = {}
        st['pelvis_loc'] = (0, kf([(0, 0), (cf - 6, 0.12), (cf, -0.25), (cf + 5, -0.20), (N, 0)], f), kf([(0, 0), (cf - 6, 0.02), (cf, -0.12), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (cf - 6, 6), (cf, -12), (cf + 5, -8), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (cf - 6, 10), (cf, -8), (N, 0)], f), 0, kf([(0, 0), (cf - 1, 8), (cf + 1, -8), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (cf - 6, 18), (cf, 2), (N, 0)], f), 0, 0)
        st['head'] = (kf([(0, 0), (cf - 6, 8), (cf, 4), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (cf - 3, -35), (cf + 2, -35), (cf + 6, -3), (N, -3)], f), 0, 0)
        st['tail1'] = (kf([(0, 0), (cf - 6, -6), (cf, 14), (N, 0)], f), 0, 0)
        arms_(st, (kf([(0, 0), (cf - 6, 70), (cf, -40), (cf + 5, -25), (N, 0)], f), 0, kf([(0, 0), (cf - 6, 30), (cf, -10), (N, 0)], f)),
                  (kf([(0, 0), (cf - 6, -30), (cf, 10), (N, 0)], f), 0, 0), (kf([(0, 0), (cf - 6, -20), (cf, 30), (N, 0)], f), 0, 0),
              (kf([(0, 0), (cf - 5, 70), (cf + 1, -40), (cf + 6, -25), (N, 0)], f), 0, kf([(0, 0), (cf - 5, -30), (cf + 1, 10), (N, 0)], f)),
                  (kf([(0, 0), (cf - 5, -30), (cf + 1, 10), (N, 0)], f), 0, 0), (kf([(0, 0), (cf - 5, -20), (cf + 1, 30), (N, 0)], f), 0, 0))
        return st
    if k == 'kick':
        # the SICKLE KICK: weight onto the left leg, the right foot lifts high and forward, then stabs down and forward at the contact
        cf = c['contact']; st = {}
        st['pelvis_loc'] = (kf([(0, 0), (cf - 10, 0.12), (cf + 6, 0.12), (N, 0)], f), kf([(0, 0), (cf - 6, 0.10), (cf, -0.15), (N, 0)], f), kf([(0, 0), (cf - 6, 0.05), (cf, -0.08), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (cf - 6, 14), (cf, -6), (N, 0)], f), kf([(0, 0), (cf - 10, -8), (cf + 6, -8), (N, 0)], f), 0)
        st['neck'] = (kf([(0, 0), (cf - 6, -10), (cf, 6), (N, 0)], f), 0, 0)
        st['tail1'] = (kf([(0, 0), (cf - 6, 16), (cf, -4), (N, 0)], f), 0, kf([(0, 0), (cf, -10), (N, 0)], f))
        st['foot_R'] = (0.0, kf([(0, 0), (cf - 10, 0), (cf - 4, -0.35), (cf, -0.75), (cf + 6, -0.75), (N, 0)], f),
                        kf([(0, 0), (cf - 10, 0), (cf - 4, 0.75), (cf, 0.08), (cf + 6, 0.0), (N, 0)], f), kf([(0, 0), (cf - 4, 12), (cf, -6), (cf + 6, 0), (N, 0)], f))
        arms_(st, (kf([(0, 0), (cf - 6, 30), (cf, 10), (N, 0)], f), 0, 20), (-20, 0, 0), (-10, 0, 0))
        return st
    if k == 'leap':
        # crouch, LAUNCH (the body rises, both feet leave the floor and tuck), and land in a deep impact crouch at the release frame.
        # The leap's TRAVEL (10-19 m) is the runtime's: root motion stays stripped, the clip is the vertical arc and the landing.
        rf = c['release']; st = {}; t0 = 7
        up = kf([(0, 0), (t0, -0.30), (t0 + 3, 0.30), (t0 + 7, 1.10), (rf - 2, 0.30), (rf, -0.35), (rf + 3, -0.30), (N, 0)], f)
        st['pelvis_loc'] = (0, 0, up)
        st['Hips'] = (kf([(0, 0), (t0, -8), (t0 + 5, 10), (rf - 2, 4), (rf, -10), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (t0, -6), (t0 + 5, 8), (rf, -12), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (t0 + 5, -30), (rf, -40), (rf + 4, -5), (N, -3)], f), 0, 0)
        st['tail1'] = (kf([(0, 0), (t0, -10), (t0 + 6, 18), (rf, -6), (N, 0)], f), 0, 0)
        lift = max(0.0, up) if (t0 + 1) < f < rf else 0.0
        for lg in LEGS:
            st['foot_' + lg] = (0.0, -0.25 * min(1.0, lift / 1.1), lift * 0.75, 0.0)
        arms_(st, (kf([(0, 0), (t0, -20), (t0 + 6, 60), (rf, -30), (N, 0)], f), 0, 15), (kf([(0, 0), (t0 + 6, -30), (rf, 10), (N, 0)], f), 0, 0), (kf([(0, 0), (rf, 30), (N, 0)], f), 0, 0))
        return st
    if k == 'hit':
        st = {}
        st['pelvis_loc'] = (kf([(0, 0), (3, 0.06), (N, 0)], f), kf([(0, 0), (3, 0.14), (N, 0)], f), kf([(0, 0), (3, -0.05), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (3, 6), (N, 0)], f), kf([(0, 0), (3, 6), (N, 0)], f), 0)
        st['chest'] = (kf([(0, 0), (3, 10), (N, 0)], f), 0, kf([(0, 0), (3, 10), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (3, 18), (N, 0)], f), 0, kf([(0, 0), (3, 14), (N, 0)], f))
        st['jaw'] = (kf([(0, -3), (2, -28), (8, -6), (N, -3)], f), 0, 0)
        st['tail1'] = (0, 0, kf([(0, 0), (3, -16), (N, 0)], f))
        arms_(st, (kf([(0, 0), (3, 40), (N, 0)], f), 0, 10), (kf([(0, 0), (3, -30), (N, 0)], f), 0, 0), (0, 0, 0))
        return st
    if k == 'death':
        st = {}; c0, c1 = 10, 30
        roll = kf([(0, 0), (c0, -6), (c1, 80), (N, 85)], f)
        st['pelvis_loc'] = (kf([(0, 0), (c0, -0.05), (c1, 0.25), (N, 0.25)], f), kf([(0, 0), (c0, 0.15), (N, 0.2)], f), kf([(0, 0), (c0, 0.05), (c1, -z_hip), (N, -z_hip)], f))
        st['Hips'] = (kf([(0, 0), (c0, 10), (c1, 0), (N, 0)], f), roll, 0)
        st['chest'] = (kf([(0, 0), (c0, 14), (c1, -6), (N, -8)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (c0, 30), (c1, -10), (N, -18)], f), 0, 0)
        st['head'] = (kf([(0, 0), (c0, 14), (c1, -10), (N, -12)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (c0, -45), (c1, -25), (N, -28)], f), 0, 0)
        # (rest-frame rotations reinterpret after the 85 deg roll: a tail YAW became a pitch and stood the tail up -- so no tail/neck yaw here)
        infl = kf([(0, 1.0), (c0, 1.0), (c0 + 10, 0.0), (N, 0.0)], f); cur = kf([(0, 0), (c0, 0), (c1, 1), (N, 1.05)], f)
        for lg in LEGS:
            st['fk_' + lg] = (infl, (-40 * cur, 0, 0), (70 * cur, 0, 0), (-50 * cur, 0, 0))
        arms_(st, (kf([(0, 0), (c0, 40), (c1, -20), (N, -25)], f), 0, 0), (kf([(0, 0), (c1, -40), (N, -45)], f), 0, 0), (0, 0, 0))
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
            if wv[1] > y_hp + 0.4: ch = 'tail1'
            elif wv[1] < fy - 0.25 and wv[2] < 0.6: ch = 'arm_%s_1' % ('L' if wv[0] > 0 else 'R')
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
