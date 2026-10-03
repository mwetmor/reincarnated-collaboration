# EN-E4 stage 3+4 for the COILSEER (R-C9-137): a HYBRID rig -- an UPRIGHT humanoid torso, neck, head, jaw and two 3-bone arms
# (n19's upper body) standing on a SERPENT BODY that lies along the ground behind it (n22's centreline segment chain, travelling-wave
# locomotion). No legs, no IK. Built from en_e3/scripts/n19_rig_biped.py + n22_rig_worm.py (copied, never edited in place);
# the jaw cut, mouth bag, gated geometric weights + edge smoothing, the readback/bake, the texture embed and the GLB export are
# theirs, unchanged in method.
#   blender -b -noaudio --python scripts/e10_rig_coil.py -- <prep.glb> <cfg.json> <out.glb>
#
# FRAME: the creature faces -Y; the ORIGIN is the torso base (n04 --anchor_upper puts the upright column over (0, 0)); the serpent body
# runs from there toward +Y. Root motion is stripped (the root never moves).
#
# SERPENTINE LOCOMOTION, NO SLIP BY CONSTRUCTION: the body's lateral wave is a TRAVELLING wave whose shape moves backward along the
# body at exactly the ground speed v (wavelength lambda = v * T for a loop of period T). In the world (root moving forward at v)
# the wave is then stationary: every point of the belly follows the one path laid down ahead of it, which is how a snake moves.
# The lint MEASURES it anyway: the lateral world offset of each chain joint, sampled when it passes the same world y, must agree
# (path_slip_m).
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
H = float(V[:, 2].max()); LM = {}

# ---------------- landmarks ----------------
z_low = CFG.get('low_band_z', 0.55)                     # the serpent body lies below this
ARMX = CFG.get('arm_x_min', 0.30)
# the upright column: the torso base sits at the origin (n04 --anchor_upper); its base height = where the column meets the coil
z_base = CFG.get('base_z', 0.30)
# the serpent centreline from the torso base back to the tail tip
low = V[V[:, 2] < z_low]
yb0 = CFG.get('coil_y0', 0.0); y_tail = float(low[:, 1].max())
NS = CFG.get('segments', 8)
ys = np.linspace(yb0, y_tail - 0.03, NS + 1)
cl = []
for y in ys:
    S = low[np.abs(low[:, 1] - y) < max(0.04, 0.5 * (y_tail - yb0) / NS)]
    cl.append((float(np.median(S[:, 0])), float(y), float(max(0.04, (S[:, 2].min() + S[:, 2].max()) / 2))))
cl[0] = (0.0, yb0, z_base)
# the upper body: chest at the shoulder line, head at the top, snout = front-most point of the head band
UP = V[V[:, 2] > CFG.get('head_band', 0.82) * H]
y0 = float(UP[:, 1].min()); HL = CFG.get('head_len', 0.30)
HB = UP[UP[:, 1] < y0 + HL]
zh_c = float(np.median(HB[:, 2])); y_hb = y0 + HL
FRn = HB[HB[:, 1] < y0 + 0.05]
z_lip = float(FRn[:, 2].min() + CFG.get('lip_z_frac', 0.40) * np.ptp(FRn[:, 2]))
y_hinge = y0 + CFG.get('hinge_frac', 0.80) * HL; z_hinge = z_lip + CFG.get('hinge_rise', 0.02)
z_sh = CFG.get('shoulder_z_frac', 0.72) * H
COL = V[(np.abs(V[:, 0]) < ARMX) & (V[:, 2] > z_base + 0.2) & (V[:, 2] < z_sh)]
y_col = float(np.median(COL[:, 1]))
z_ch = z_sh - CFG.get('chest_drop', 0.10)
arms = {}
for side, sgn in (('L', 1), ('R', -1)):
    Ap = V[(V[:, 0] * sgn > ARMX) & (V[:, 2] > z_low * 0.6) & (V[:, 2] < z_sh + 0.05)]
    tip = Ap[np.argmin(Ap[:, 2])]
    shp = np.array([sgn * CFG.get('shoulder_x', 0.20), y_col, z_sh - 0.03])
    def at(t, Ap=Ap, a=shp, b=tip):
        p = a + (b - a) * t; m = np.linalg.norm(Ap[:, [0, 2]] - p[[0, 2]], axis=1) < 0.06
        return (float(np.median(Ap[m, 0])), float(np.median(Ap[m, 1])), float(np.median(Ap[m, 2]))) if m.sum() > 5 else tuple(map(float, p))
    arms[side] = dict(sh=tuple(map(float, shp)), el=at(0.48), wr=at(0.86), tip=tuple(map(float, tip)))
LM.update(H=H, y_snout=y0, y_tail=y_tail, z_base=z_base, z_shoulder=z_sh, z_lip=z_lip, y_hinge=y_hinge, y_col=y_col, arms=arms, centreline=cl)
LEGS = []

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
z_w = z_base + CFG.get('waist_rise', 0.35)
bone('Hips', (0, 0.0, z_base), (0, y_col * 0.5, z_w), 'root')
bone('spine', (0, y_col * 0.5, z_w), (0, y_col, 0.5 * (z_w + z_ch)), 'Hips', conn=True)
bone('chest', (0, y_col, 0.5 * (z_w + z_ch)), (0, y_col, z_ch), 'spine', conn=True)
z_nk = z_sh + CFG.get('neck_rise', 0.10)
bone('neck', (0, y_col, z_ch), (0, 0.5 * (y_col + y_hb), z_nk), 'chest', conn=True)
bone('head', (0, 0.5 * (y_col + y_hb), z_nk), (0, y0 + 0.03, zh_c), 'neck', conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.04, z_lip - 0.04), 'head')
prev = 'Hips'; BACK = []
for i in range(NS):
    nm = 'seg_b%d' % (i + 1); bone(nm, cl[i], cl[i + 1], prev, conn=(i > 0)); prev = nm; BACK.append(nm)
for s_ in ('L', 'R'):
    a_ = arms[s_]
    bone('arm_%s_1' % s_, a_['sh'], a_['el'], 'chest'); bone('arm_%s_2' % s_, a_['el'], a_['wr'], 'arm_%s_1' % s_, conn=True)
    bone('arm_%s_3' % s_, a_['wr'], a_['tip'], 'arm_%s_2' % s_, conn=True)
bpy.ops.object.mode_set(mode='OBJECT')
DEF = [b.name for b in arm.data.bones if b.use_deform]
SEGL = [float(np.linalg.norm(np.array(cl[i + 1]) - np.array(cl[i]))) for i in range(NS)]

# ---------------- mouth: a real CUT along the lip plane, a dark mouth bag (n19, unchanged) ----------------
lipA = Vector((0, y0, z_lip)); lipB = Vector((0, y_hinge, z_hinge))
pn = Vector((0, -(lipB.z - lipA.z), (lipB.y - lipA.y))).normalized()
if pn.z < 0: pn = -pn
me = body.data
bm = bmesh.new(); bm.from_mesh(me)
mw = body.matrix_world.copy(); mwi = mw.inverted()
co_l = mwi @ lipA; n_l = (mwi.to_3x3() @ pn).normalized()
z_hb = CFG.get('head_band', 0.82) * H - 0.05
hfaces = [f for f in bm.faces if (mw @ f.calc_center_median()).y < y_hinge - 0.01 and (mw @ f.calc_center_median()).z > z_hb]
geom = list({v for f in hfaces for v in f.verts}) + list({e for f in hfaces for e in f.edges}) + hfaces
res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co_l, plane_no=n_l, dist=1e-6)
cut = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge) and (mw @ ((e.verts[0].co + e.verts[1].co) / 2)).y < y_hinge - 0.02]
bmesh.ops.split_edges(bm, edges=cut)
bm.verts.index_update()
side = {}
for v in bm.verts:
    p = mw @ v.co
    if p.y < y_hinge + 0.04 and p.z > z_hb:
        cmean = (sum(((mw @ f.calc_center_median()) for f in v.link_faces), Vector()) / len(v.link_faces)) if v.link_faces else p
        side[v.index] = (cmean - lipA).dot(pn) < 0
bm.to_mesh(me); bm.free(); me.update()
LM['mouth_cut_edges'] = len(cut)
hw = float(np.quantile(np.abs(V[(V[:, 1] < y0 + 0.5 * HL) & (np.abs(V[:, 2] - z_lip) < 0.05) & (V[:, 2] > z_hb)][:, 0]), 0.9))
bm = bmesh.new()
yA, yB = y0 + CFG.get('bag_y0_frac', 0.22) * HL, y_hinge - 0.03; wA, wB = CFG.get('bag_w', (0.16, 0.26))[0] * hw, CFG.get('bag_w', (0.16, 0.26))[1] * hw; dz = CFG.get('bag_half_h', 0.02)
def lipz(y): return z_lip + (z_hinge - z_lip) * (y - y0) / max(y_hinge - y0, 1e-6)
pts = [(-wA, yA, lipz(yA) + dz), (wA, yA, lipz(yA) + dz), (wB, yB, lipz(yB) + dz), (-wB, yB, lipz(yB) + dz),
       (-wA, yA, lipz(yA) - dz), (wA, yA, lipz(yA) - dz), (wB, yB, lipz(yB) - dz), (-wB, yB, lipz(yB) - dz)]
vs = [bm.verts.new(p) for p in pts]
for q in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): bm.faces.new([vs[i] for i in q])
bm.normal_update()
bagm = bpy.data.meshes.new('bag'); bm.to_mesh(bagm); bm.free()
bag = bpy.data.objects.new('bag', bagm); sc.collection.objects.link(bag)
mat = bpy.data.materials.new('maw_interior'); mat.use_nodes = True
bs = mat.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value = CFG.get('mouth_rgba', (0.16, 0.05, 0.06, 1)); bs.inputs['Roughness'].default_value = 1.0
mat.use_backface_culling = False
bagm.materials.append(mat)
_uv = bagm.uv_layers.new(name=body.data.uv_layers.active.name)
for _poly in bagm.polygons:
    for _k, _li in enumerate(_poly.loop_indices): _uv.data[_li].uv = ((0, 0), (1, 0), (1, 1), (0, 1))[_k % 4]

# ---------------- weights: gated inverse-distance^4, edge-smoothed (n19/n22) ----------------
for n in DEF:
    if n not in [g.name for g in body.vertex_groups]: body.vertex_groups.new(name=n)
VW = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
bones_w = [n for n in DEF if n != 'root']
Wm = np.zeros((len(VW), len(bones_w)))
def _seg_d(n):
    b_ = arm.data.bones[n]; h_ = np.array(b_.head_local[:]); t_ = np.array(b_.tail_local[:]); d_ = t_ - h_
    tt = np.clip(((VW - h_) @ d_) / max(d_ @ d_, 1e-9), 0, 1); return np.linalg.norm(VW - (h_ + tt[:, None] * d_), axis=1)
def _chain_d(prefix):
    return np.min([_seg_d('%s_%d' % (prefix, k_)) for k_ in (1, 2, 3)], 0)
in_coil = (VW[:, 2] < z_low) & (VW[:, 1] > CFG.get('coil_gate_y', 0.12))      # the serpent body behind the torso base
for j, n in enumerate(bones_w):
    dist = _seg_d(n); g = np.ones(len(VW))
    if n.startswith('arm_'):
        dA = _chain_d(n[:5]); a_ = arms[n[4]]; zt = a_['tip'][2]; zs = a_['sh'][2]
        rr = CFG.get('arm_r', 0.10) + (CFG.get('hand_r', 0.16) - CFG.get('arm_r', 0.10)) * np.clip((zs - VW[:, 2]) / max(zs - zt, 1e-6), 0, 1)
        g = ((dA < rr) & (VW[:, 0] * (1 if n[4] == 'L' else -1) > CFG.get('arm_gate_x', 0.14))).astype(float)
    elif n in ('head', 'jaw'):
        g = (VW[:, 2] > z_hb).astype(float)
    elif n in ('spine', 'chest', 'neck'):
        g = (~in_coil & (VW[:, 2] > z_base)).astype(float)
    elif n.startswith('seg_b'):
        g = in_coil.astype(float) if n != 'seg_b1' else (VW[:, 2] < z_low + 0.1).astype(float)
    Wm[:, j] = g / (dist ** 4 + 1e-6)
_z = Wm.sum(1) <= 0
if _z.any():
    for j, n_ in enumerate(bones_w):
        if n_.startswith('arm_') or n_ in ('head', 'jaw'): continue
        Wm[_z, j] = 1.0 / (_seg_d(n_)[_z] ** 4 + 1e-6)
LM['unweighted_fallback_verts'] = int(_z.sum())
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
LM['weights_method'] = 'geometric: gated inverse-distance^4 to bone segments, edge-smoothed, top 4'
vg = {g.name: g for g in body.vertex_groups}
njaw = 0
for v in me.vertices:
    if v.index not in side: continue
    p = body.matrix_world @ v.co
    if p.z < z_lip - 0.25 or p.z > zh_c + 0.4: continue
    w = 1.0 if p.y < y_hinge else (y_hinge + 0.04 - p.y) / 0.04
    tgt = 'jaw' if side[v.index] else 'head'
    if tgt == 'jaw': njaw += 1
    for g in list(v.groups): g.weight = g.weight * (1 - w)
    vg[tgt].add([v.index], w, 'ADD')
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
LM['weights'] = dict(method=LM['weights_method'], jaw_verts=njaw, unweighted_verts=unweighted, groups=len(body.vertex_groups))

pb = arm.pose.bones
for p in pb: p.rotation_mode = 'QUATERNION'
def M3(n): return arm.data.bones[n].matrix_local.to_3x3()
def wrot(n, rx=0.0, ry=0.0, rz=0.0):
    # a rotation about WORLD axes (degrees; +rx = the -Y end UP, as n10), expressed in the bone's rest frame
    R = Euler((math.radians(-rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix()
    m = M3(n); return (m.inverted() @ R @ m).to_quaternion()
def wloc(n, v): return M3(n).inverted() @ Vector(v)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def kf(keys, f):
    if f <= keys[0][0]: return keys[0][1]
    for (fa, va), (fb, vb) in zip(keys, keys[1:]):
        if f <= fb:
            if isinstance(va, (tuple, list)): return tuple(x + (y - x) * ease((f - fa) / max(fb - fa, 1e-9)) for x, y in zip(va, vb))
            return va + (vb - va) * ease((f - fa) / max(fb - fa, 1e-9))
    return keys[-1][1]

CL = CFG['clips']
def pose_reset():
    for p in pb:
        p.location = (0, 0, 0); p.rotation_quaternion = (1, 0, 0, 0); p.scale = (1, 1, 1)
CHAN = ['Hips', 'spine', 'chest', 'neck', 'head', 'jaw'] + BACK + ['arm_%s_%d' % (s, k) for s in 'LR' for k in (1, 2, 3)]
def apply(st):
    for n in CHAN:
        r = st.get(n)
        if r: pb[n].rotation_quaternion = wrot(n, *r)
    if 'pelvis_loc' in st: pb['Hips'].location = wloc('Hips', st['pelvis_loc'])

def arms_(st, l1, l2, l3, r1=None, r2=None, r3=None):
    st['arm_L_1'], st['arm_L_2'], st['arm_L_3'] = l1, l2, l3
    st['arm_R_1'], st['arm_R_2'], st['arm_R_3'] = (r1 or (l1[0], -l1[1], -l1[2])), (r2 or (l2[0], -l2[1], -l2[2])), (r3 or (l3[0], -l3[1], -l3[2]))

def serp(st, t_frac, lam, amp, k_env=1.0):
    # the TRAVELLING WAVE: lateral offset x(s, t) = A(s) sin(2 pi (s / lam + t_frac)); s = arc length back from the torso base.
    # The wave moves toward +s (backward) at lam per period = the ground speed. Each segment takes its local heading
    # theta(s) = atan(dx/ds); the rotation keyed on a segment is its heading minus its parent's (a chain of relative yaws).
    # A(s) ramps from 0 at the torso base (the torso stays steady) to amp at 35 % of the body.
    sL = np.cumsum([0.0] + SEGL); Ltot = sL[-1]
    def A(s): return amp * k_env * min(1.0, s / (0.35 * Ltot))
    def dA(s): return (amp * k_env / (0.35 * Ltot)) if s < 0.35 * Ltot else 0.0
    prev_th = 0.0
    for i, n in enumerate(BACK):
        s = sL[i] + 0.5 * SEGL[i]
        ph = 2 * math.pi * (s / lam + t_frac)
        dx = dA(s) * math.sin(ph) + A(s) * (2 * math.pi / lam) * math.cos(ph)
        th = math.degrees(math.atan(dx))
        r = st.get(n, (0, 0, 0)); st[n] = (r[0], r[1], r[2] + th - prev_th); prev_th = th
    return st

def clip_state(name, f):
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name); w = 2 * math.pi * f / N; st = {}
    if k == 'idle':
        # swaying on its coil: the torso breathes and weaves, the head turns and tastes the air (one jaw flick), a slow tail wave
        st['spine'] = (2.0 * math.sin(w), 0, 3.0 * math.sin(w))
        st['chest'] = (1.5 * math.sin(w + 0.4), 2.0 * math.sin(w + 0.6), 2.0 * math.sin(w + 0.3))
        st['neck'] = (2.0 * math.sin(w + 0.8), 0, -4.0 * math.sin(w + 0.5))
        fl = math.exp(-((f / N - 0.55) * 14) ** 2)
        st['head'] = (3.0 * math.sin(2 * w), 0, 6.0 * math.sin(w + 1.0) + 8 * fl); st['jaw'] = (-1.0 - 14.0 * fl, 0, 0)
        arms_(st, (4 + 3 * math.sin(w), 0, 2), (-8 - 3 * math.sin(w + 0.5), 0, 0), (-6, 0, 0))
        return serp(st, -f / N, CFG.get('idle_lambda', 1.6), CFG.get('idle_amp', 0.06))
    if k in ('walk', 'run'):
        T = N / FPS; lam = c['speed'] * T
        st['Hips'] = (0, 0, CFG.get('hips_yaw', 0.0) * math.sin(w))
        st['spine'] = (-2.0 if k == 'walk' else -6.0, 0, -2.0 * math.sin(w))
        st['chest'] = (-1.0 if k == 'walk' else -4.0, 2.0 * math.sin(w), -1.5 * math.sin(w))
        st['neck'] = (1.0 if k == 'walk' else 4.0, 0, 1.0 * math.sin(w))
        st['head'] = (1.0 if k == 'walk' else 5.0, 0, 0); st['jaw'] = (-1.0, 0, 0)
        sw = math.sin(w); fa = 8.0 if k == 'walk' else 14.0
        arms_(st, (6 + fa * sw, 0, 4), (-12, 0, 0), (-8, 0, 0), (6 - fa * sw, 0, -4), (-12, 0, 0), (-8, 0, 0))
        return serp(st, -f / N, lam, c.get('amp', 0.16 if k == 'walk' else 0.20))
    if k == 'claw':
        # the RIGHT-HAND RAKE: the torso coils back and twists right, the right arm rises high, then slashes across and down through the
        # contact; the head follows; recover. Contact = the roster's RightHandHit frame.
        cf = c['contact']; a0 = max(3, cf - 7)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.06), (cf, -0.18), (cf + 8, -0.12), (N, 0)], f), 0)
        st['spine'] = (kf([(0, 0), (a0, 8), (cf, -12), (cf + 8, -8), (N, 0)], f), 0, kf([(0, 0), (a0, -18), (cf, 16), (cf + 8, 10), (N, 0)], f))
        st['chest'] = (kf([(0, 0), (a0, 6), (cf, -8), (N, 0)], f), 0, kf([(0, 0), (a0, -10), (cf, 12), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (a0, 4), (cf, -6), (N, 0)], f), 0, kf([(0, 0), (a0, 8), (cf, -8), (N, 0)], f))
        st['jaw'] = (kf([(0, -1), (cf - 3, -24), (cf + 4, -4), (N, -1)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, 20), (cf, 10), (N, 0)], f), 0, kf([(0, 0), (a0, 10), (N, 0)], f)), (kf([(0, 0), (a0, -20), (N, 0)], f), 0, 0), (0, 0, 0),
              (kf([(0, 0), (a0, 120), (cf, -10), (cf + 6, -20), (N, 0)], f), 0, kf([(0, 0), (a0, -30), (cf, 40), (cf + 6, 30), (N, 0)], f)),
              (kf([(0, 0), (a0, -40), (cf, 0), (N, 0)], f), 0, 0), (kf([(0, 0), (a0, 20), (cf, -25), (N, 0)], f), 0, 0))
        return serp(st, 0.0, 1.6, kf([(0, 0.04), (cf, 0.10), (N, 0.04)], f))
    if k == 'bolt':
        # the BOLT CAST: draw the right hand back to the shoulder, the left hand forward, then THRUST the right palm out at the target
        # (the bolt leaves the right hand at the release), the jaw hissing open; hold, recover
        rf = c['release']; a0 = max(3, rf - 12); ho = c.get('hold', 6)
        st['spine'] = (kf([(0, 0), (a0, 6), (rf, -8), (rf + ho, -6), (N, 0)], f), 0, kf([(0, 0), (a0, -14), (rf, 12), (rf + ho, 10), (N, 0)], f))
        st['chest'] = (kf([(0, 0), (a0, 4), (rf, -4), (N, 0)], f), 0, kf([(0, 0), (a0, -8), (rf, 6), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (a0, 6), (rf, -6), (N, 0)], f), 0, kf([(0, 0), (a0, 10), (rf, -6), (N, 0)], f))
        st['jaw'] = (kf([(0, -1), (a0, -4), (rf - 1, -30), (rf + ho, -26), (rf + ho + 6, -2), (N, -1)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, 50), (rf, 30), (N, 0)], f), 0, kf([(0, 0), (a0, -20), (N, 0)], f)), (kf([(0, 0), (a0, -30), (N, 0)], f), 0, 0), (0, 0, 0),
              (kf([(0, 0), (a0, 40), (rf, 85), (rf + ho, 85), (N, 0)], f), 0, kf([(0, 0), (a0, 50), (rf, -15), (rf + ho, -15), (N, 0)], f)),
              (kf([(0, 0), (a0, -90), (rf, 0), (rf + ho, 0), (N, 0)], f), 0, 0), (kf([(0, 0), (rf, 20), (rf + ho, 20), (N, 0)], f), 0, 0))
        return serp(st, 0.0, 1.6, 0.04)
    if k == 'nova':
        # the NOVA / AURA CAST: the torso rears up and back, both arms sweep up and wide over the head, the hood-frill and jaw flare in a
        # hiss, then the body DROPS and both arms fling OUT and down at the release (the ring leaves the body); hold, recover
        rf = c['release']; a0 = max(3, rf - 14); ho = c.get('hold', 8)
        st['pelvis_loc'] = (0, 0, kf([(0, 0), (a0, 0.12), (rf, -0.10), (rf + ho, -0.08), (N, 0)], f))
        st['spine'] = (kf([(0, 0), (a0, 14), (rf, -10), (rf + ho, -8), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (a0, 10), (rf, -6), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (a0, 18), (rf, -8), (rf + ho, -6), (N, 0)], f), 0, 0)
        st['head'] = (kf([(0, 0), (a0, 14), (rf, -6), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -1), (a0, -36), (rf, -40), (rf + ho, -30), (rf + ho + 8, -2), (N, -1)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, 70), (rf, 15), (rf + ho, 15), (N, 0)], f), 0, kf([(0, 0), (a0, 40), (rf, 70), (rf + ho, 65), (N, 0)], f)),
              (kf([(0, 0), (a0, -20), (rf, 0), (N, 0)], f), 0, 0), (kf([(0, 0), (rf, 15), (N, 0)], f), 0, 0))
        return serp(st, 0.0, 1.6, kf([(0, 0.04), (rf, 0.12), (N, 0.04)], f))
    if k == 'taillash':
        # the TAIL LASH: the tail swings wide to the right, then WHIPS round to the left and slams down at the release (the wave rolls
        # out ahead of it); the torso counter-twists and leans into it; recover
        rf = c['release']; a0 = max(3, rf - 10)
        sw = kf([(0, 0), (a0, -1.0), (rf, 1.0), (rf + 10, 0.8), (N, 0)], f)
        for i, n in enumerate(BACK[1:]):
            st[n] = (0, 0, sw * CFG.get('lash_deg', 14.0) * (0.4 + 0.6 * i / max(1, len(BACK) - 2)))
        lift = kf([(0, 0), (a0, 1.0), (rf - 2, 1.0), (rf, 0.0), (N, 0)], f)
        if len(BACK) > 3: st[BACK[-3]] = (st[BACK[-3]][0] - 10 * lift, 0, st[BACK[-3]][2])
        st['spine'] = (kf([(0, 0), (a0, 6), (rf, -10), (N, 0)], f), 0, kf([(0, 0), (a0, 14), (rf, -16), (N, 0)], f))
        st['chest'] = (0, 0, kf([(0, 0), (a0, 8), (rf, -10), (N, 0)], f))
        st['jaw'] = (kf([(0, -1), (rf - 2, -26), (rf + 6, -4), (N, -1)], f), 0, 0)
        arms_(st, (kf([(0, 0), (a0, 30), (rf, -10), (N, 0)], f), 0, kf([(0, 0), (a0, 30), (N, 0)], f)), (-20, 0, 0), (0, 0, 0))
        return st
    if k == 'hit':
        st['pelvis_loc'] = (0, kf([(0, 0), (3, 0.10), (N, 0)], f), 0)
        st['spine'] = (kf([(0, 0), (3, 14), (N, 0)], f), 0, kf([(0, 0), (3, 10), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (3, 16), (N, 0)], f), 0, kf([(0, 0), (3, -12), (N, 0)], f))
        st['jaw'] = (kf([(0, -1), (2, -26), (8, -3), (N, -1)], f), 0, 0)
        arms_(st, (kf([(0, 0), (3, 30), (N, 0)], f), 0, 20), (kf([(0, 0), (3, -30), (N, 0)], f), 0, 0), (0, 0, 0))
        return serp(st, 0.0, 1.6, kf([(0, 0.03), (3, 0.10), (N, 0.03)], f))
    if k == 'death':
        # it RECOILS, then the upright body topples forward and sideways onto the floor at the base of the coil (spine + chest carry
        # the fall; the coil stays on the ground), the tail thrashes and curls, still; held
        c0, c1 = 6, int(N * 0.65)
        st['spine'] = (kf([(0, 0), (c0, 10), (c1, -55), (N, -60)], f), kf([(0, 0), (c1, 20), (N, 24)], f), 0)
        st['chest'] = (kf([(0, 0), (c0, 6), (c1, -22), (N, -26)], f), 0, kf([(0, 0), (c1, 8), (N, 10)], f))
        st['neck'] = (kf([(0, 0), (c0, 16), (c1, -10), (N, -12)], f), 0, kf([(0, 0), (c1, 20), (N, 24)], f))
        st['jaw'] = (kf([(0, -1), (c0, -36), (N, -22)], f), 0, 0)
        arms_(st, (kf([(0, 0), (c0, 40), (c1, 20), (N, 18)], f), 0, kf([(0, 0), (c1, 30), (N, 34)], f)), (kf([(0, 0), (c1, -20), (N, -24)], f), 0, 0), (0, 0, 0))
        e = kf([(0, 1.0), (c1, 1.0), (N, 0.0)], f)
        for i, n in enumerate(BACK[1:]):
            st[n] = (0, 0, e * 10.0 * math.sin(3 * w - 1.1 * i) + kf([(0, 0), (c1, 10), (N, 12)], f))
        return st
    raise KeyError(k)

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
for name, c in CL.items():
    N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    frames, minz, joints, verts0 = [], [], [], None
    for f in range(N + 1):
        pose_reset(); st = clip_state(name, f); apply(st); bpy.context.view_layer.update()
        mz, co = mesh_minz()
        # CONTACT SOLVE: a hand that dips through the floor lifts its arm 2 deg at a time
        for _ in range(40):
            if mz >= -0.003: break
            wv = co[int(np.argmin(co[:, 2]))]
            if abs(wv[0]) > ARMX and wv[2] < 0 and wv[1] < CFG.get('coil_gate_y', 0.12): ch = 'arm_%s_1' % ('L' if wv[0] > 0 else 'R')
            else: break
            r = st.get(ch, (0, 0, 0)); st[ch] = (r[0] + 2.0, r[1], r[2]); apply(st); bpy.context.view_layer.update(); mz, co = mesh_minz()
        # GROUND SOLVE (the coil rests ON the floor): the Hips are lifted by the measured penetration (all clips; a lift, never a sink)
        for _ in range(4):
            if mz >= -0.002: break
            l = pb['Hips'].location.copy(); pb['Hips'].location = l + wloc('Hips', (0, 0, -mz + 0.002)); bpy.context.view_layer.update()
            mz, co = mesh_minz()
        if f == 0: verts0 = co.copy()
        if f == N: vN = co.copy()
        minz.append(mz)
        if mz <= min(minz): worst = (f, [round(float(x), 3) for x in co[int(np.argmin(co[:, 2]))]])
        joints.append([tuple(arm.matrix_world @ pb[n].head) for n in BACK])
        frames.append(readback())
    BAKED[name] = frames
    L = dict(frames=len(frames), min_z_m=round(min(minz), 4), worst_frame_vertex=worst, penetration_frames=int(sum(1 for z in minz if z < -0.01)))
    if c['kind'] == 'loop':
        L['loop_seam_max_vert_m'] = round(float(np.abs(vN - verts0).max()), 5)
    if c.get('speed'):
        # PATH SLIP: in the world the root travels -y at v. A point of the belly is on the path if, whenever it passes world y = Y,
        # its x is the path's x(Y). Measured: for each chain joint, its world (x, y) track; then the spread of x among all joints at
        # the same world y (binned at 5 cm) is the slip. A travelling wave at exactly v gives 0 (to the bin's resolution).
        v = c['speed']; J = np.array(joints)          # frames x joints x 3
        Yw = J[:, :, 1] - v * np.arange(len(J))[:, None] / FPS; Xw = J[:, :, 0]
        bins = {}
        for yy, xx in zip(Yw.ravel(), Xw.ravel()): bins.setdefault(int(round(yy / 0.05)), []).append(xx)
        L['path_slip_m'] = round(max((max(b) - min(b)) for b in bins.values() if len(b) > 1), 4)
        # SPLIT (EN-E4 resume, judging the 0.26 m): the amplitude RAMP (A(s) from 0 at the torso base to amp at 35 % of the body) is
        # by design off-path -- a joint in the ramp swings less than the path it is on. So the slip is reported twice: the joints
        # past the ramp (must be ~0: the travelling wave proper) and the joints inside it (the price of a steady torso).
        sL_ = np.cumsum([0.0] + SEGL); r_ = 0.35 * sL_[-1]
        for tag, sel in (('path_slip_body_m', [i for i in range(len(BACK)) if sL_[i] >= r_]), ('path_slip_ramp_m', [i for i in range(len(BACK)) if sL_[i] < r_])):
            bb = {}
            for fi in range(len(J)):
                for i in sel: bb.setdefault(int(round(Yw[fi, i] / 0.05)), []).append(Xw[fi, i])
            L[tag] = round(max([max(b) - min(b) for b in bb.values() if len(b) > 1] or [0.0]), 4)
        L['ramp_len_m'] = round(float(r_), 3)
        L['wavelength_m'] = round(v * N / FPS, 4)
    LINT[name] = L
    print('clip %-16s %s' % (name, L))

pose_reset()
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
