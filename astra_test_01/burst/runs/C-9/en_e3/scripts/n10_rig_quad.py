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

# ---------------- landmarks ----------------
low = V[V[:, 2] < CFG.get('foot_band', 0.08) * H]
feet = {}
for side, sgn in (('L', 1), ('R', -1)):
    P = low[low[:, 0] * sgn > 0.02]
    c = np.quantile(P[:, 1], [0.1, 0.9])
    for _ in range(20):
        lab = np.abs(P[:, 1, None] - c[None]).argmin(1); c = np.array([P[lab == k, 1].mean() for k in (0, 1)])
    for k, fb in ((0, 'F'), (1, 'B')):
        Q = P[lab == k]
        feet[fb + side] = dict(x=float(np.median(Q[:, 0])), y=float(np.median(Q[:, 1])), toe_y=float(np.quantile(Q[:, 1], 0.03)),
                               heel_y=float(np.quantile(Q[:, 1], 0.97)))
fy_f = (feet['FL']['y'] + feet['FR']['y']) / 2; fy_b = (feet['BL']['y'] + feet['BR']['y']) / 2
mid = V[(np.abs(V[:, 0]) < 0.08) & (V[:, 1] > fy_f + 0.1) & (V[:, 1] < fy_b - 0.1)]
z_belly = float(np.quantile(mid[:, 2], 0.03))
def ztop(y, w=0.08):
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.2)]; return float(np.quantile(S[:, 2], 0.85))
def zmid_at(y, w=0.05):
    S = V[(np.abs(V[:, 1] - y) < w) & (np.abs(V[:, 0]) < 0.15)]; return float((S[:, 2].min() + S[:, 2].max()) / 2), S
jf = CFG.get('joint_frac', 0.35)
z_sh = z_belly + jf * (ztop(fy_f) - z_belly); z_hp = z_belly + jf * (ztop(fy_b) - z_belly)
z_sp_f = z_belly + 0.62 * (ztop(fy_f) - z_belly); z_sp_b = z_belly + 0.62 * (ztop(fy_b) - z_belly)
HL = CFG.get('head_len_frac', 0.22) * LF
y_hb = y0 + HL
zh_c, _ = zmid_at(y0 + 0.5 * HL, 0.06)
_, Ssn = zmid_at(y0 + 0.10 * HL, 0.06)
z_lip = float(Ssn[:, 2].min() + CFG.get('lip_z_frac', 0.45) * np.ptp(Ssn[:, 2]))
y_hinge = y0 + CFG.get('hinge_frac', 0.85) * HL
z_hinge = z_lip + CFG.get('hinge_rise', 0.03)
TLF = CFG.get('tail_frac', 0.27); y_tb = y1 - TLF * LF
z_tb, _ = zmid_at(y_tb, 0.05); z_tt, _ = zmid_at(y1 - 0.04, 0.04)
ank_z = CFG.get('ankle_z', 0.12)
LM.update(H=H, y_snout=y0, y_tail=y1, z_belly=z_belly, z_shoulder=z_sh, z_hip=z_hp, y_head_base=y_hb, z_lip=z_lip, y_hinge=y_hinge, feet=feet)

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
y_sp1 = fy_b - 0.35 * (fy_b - fy_f); y_ch = fy_f + 0.05
bone('pelvis', (0, fy_b + 0.06, z_sp_b), (0, y_sp1, z_sp_b + 0.3 * (z_sp_f - z_sp_b)), 'root')
bone('spine', (0, y_sp1, z_sp_b + 0.3 * (z_sp_f - z_sp_b)), (0, y_ch, z_sp_f), 'pelvis', conn=True)
bone('chest', (0, y_ch, z_sp_f), (0, y_hb + 0.12, zh_c + 0.03), 'spine', conn=True)
bone('neck', (0, y_hb + 0.12, zh_c + 0.03), (0, y_hb - 0.02, zh_c + 0.02), 'chest', conn=True)
bone('head', (0, y_hb - 0.02, zh_c + 0.02), (0, y0 + 0.02, zh_c + 0.04), 'neck', conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.05, z_lip - 0.06), 'head')
bone('tail1', (0, y_tb - 0.1, z_tb + 0.02), (0, y_tb + 0.25 * TLF * LF, z_tb), 'pelvis')
bone('tail2', (0, y_tb + 0.25 * TLF * LF, z_tb), (0, y_tb + 0.62 * TLF * LF, (z_tb + z_tt) / 2), 'tail1', conn=True)
bone('tail3', (0, y_tb + 0.62 * TLF * LF, (z_tb + z_tt) / 2), (0, y1, z_tt), 'tail2', conn=True)
LEGS = ['FL', 'FR', 'BL', 'BR']
for lg in LEGS:
    f = feet[lg]; front = lg[0] == 'F'
    jx = f['x'] * CFG.get('joint_x_frac', 0.75)
    jz = z_sh if front else z_hp
    bend = CFG.get('knee_bend', 0.07) * (1 if front else -1)   # front elbow points back (+y), hind knee forward (-y)
    J = (jx, f['y'] + (0.02 if front else -0.02), jz); K = (f['x'] * 0.92, f['y'] + bend, ank_z + 0.5 * (jz - ank_z))
    A = (f['x'], f['y'] + CFG.get('ankle_back', 0.03), ank_z); T = (f['x'], f['toe_y'] + 0.02, 0.03)
    par = 'chest' if front else 'pelvis'
    bone('leg_%s_1' % lg, J, K, par); bone('leg_%s_2' % lg, K, A, 'leg_%s_1' % lg, conn=True)
    bone('leg_%s_3' % lg, A, T, 'leg_%s_2' % lg, conn=True)
    bone('ik_%s' % lg, A, T, 'root', deform=False)
    pz = 0.35 if front else -0.35
    bone('pole_%s' % lg, (K[0], K[1] + pz, K[2]), (K[0], K[1] + pz, K[2] + 0.1), 'root', deform=False)
    LM['leg_' + lg] = dict(joint=J, knee=K, ankle=A, toe=T, chain_len=round(float((Vector(K) - Vector(J)).length + (Vector(A) - Vector(K)).length), 4), rest_reach=round(float((Vector(A) - Vector(J)).length), 4))
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
bagm.materials.append(mat)
bagm.uv_layers.new(name=body.data.uv_layers.active.name)

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
        lg = n[4:6]; sgn = 1 if lg[1] == 'L' else -1; fy = feet[lg]['y']
        zj = (z_sh if lg[0] == 'F' else z_hp) + 0.06
        g = ((VW[:, 0] * sgn > 0.02) & (np.abs(VW[:, 1] - fy) < 0.32) & (VW[:, 2] < zj)).astype(float)
        if n.endswith('_1'): g = np.maximum(g, 0.3 * ((VW[:, 0] * sgn > 0.05) & (np.abs(VW[:, 1] - fy) < 0.32) & (VW[:, 2] < zj + 0.12)))
    if n.startswith('tail'):
        g = (VW[:, 1] > y_tb - 0.25).astype(float)
    if n in ('head', 'jaw', 'neck'):
        g = (VW[:, 1] < y_hb + 0.25).astype(float)
    Wm[:, j] = g / (dist ** 4 + 1e-6)
# the FOOT BLOCK (below the ankle, inside a leg's gate) rides the foot bone alone, so a bending shin cannot push the sole into the floor
for lg in LEGS:
    j3 = bones_w.index('leg_%s_3' % lg); sgn = 1 if lg[1] == 'L' else -1
    fb = (VW[:, 0] * sgn > 0.02) & (np.abs(VW[:, 1] - feet[lg]['y']) < 0.32) & (VW[:, 2] < ank_z + CFG.get('foot_block_dz', 0.02))
    Wm[fb] = 0.0; Wm[fb, j3] = 1.0
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
    # st: dict of channel -> value.  rotations in degrees about world axes (x = pitch: +nose up ... see sign note), loc in metres
    for n in ('pelvis', 'spine', 'chest', 'neck', 'head', 'jaw', 'tail1', 'tail2', 'tail3'):
        r = st.get(n)
        if r: pb[n].rotation_quaternion = wrot(n, *r)
    if 'pelvis_loc' in st: pb['pelvis'].location = wloc('pelvis', st['pelvis_loc'])
    for lg in LEGS:
        o = st.get('foot_' + lg, (0, 0, 0, 0))
        pb['ik_' + lg].location = wloc('ik_' + lg, o[:3])
        pb['ik_' + lg].rotation_quaternion = wrot('ik_' + lg, o[3] if len(o) > 3 else 0.0)
        if ('fk_' + lg) in st:
            infl, r1, r2, r3 = st['fk_' + lg]
            pb['leg_%s_2' % lg].constraints[0].influence = infl; pb['leg_%s_3' % lg].constraints[0].influence = infl
            pb['leg_%s_1' % lg].rotation_quaternion = wrot('leg_%s_1' % lg, r1)
            pb['leg_%s_2' % lg].rotation_quaternion = wrot('leg_%s_2' % lg, r2)
            pb['leg_%s_3' % lg].rotation_quaternion = wrot('leg_%s_3' % lg, r3)
for p in pb: p.rotation_mode = 'QUATERNION'

# SIGN NOTE: the creature faces -Y. A raw world-X rotation of +deg tips the -Y end DOWN, so wrot() negates rx: in every clip +rx = NOSE UP.
def gait(f, N, v, duty, offs, lift, bob, pitch_amp, flex_amp, lead):
    T = N / FPS; S = v * duty * T; st = {}
    ph = f / N
    for lg in LEGS:
        u = (ph + offs[lg]) % 1.0
        if u < duty:
            s = u / duty; dy = -S / 2 + S * s; dz = 0.0; rx = 0.0
        else:
            s = (u - duty) / (1 - duty); dy = S / 2 - S * ease(s); dz = lift * math.sin(math.pi * s); rx = -12.0 * math.sin(math.pi * s)
        st['foot_' + lg] = (0.0, dy, dz, rx); st.setdefault('_stance', {})[lg] = u < duty
    w = 2 * math.pi * ph
    # REACH: the body sinks exactly as far as the most-extended leg needs (98 % of its chain), so no target is ever out of
    # reach -- an unreachable target is foot slide. This is the gait's own bob, derived rather than typed.
    drop = 0.0
    for lg in LEGS:
        Lm = LM['leg_' + lg]; J, A = Vector(Lm['joint']), Vector(Lm['ankle']); o = st['foot_' + lg]
        hz = math.hypot(A.x - J.x, A.y + o[1] - J.y); vmax = math.sqrt(max((0.98 * Lm['chain_len']) ** 2 - hz ** 2, 1e-6))
        drop = max(drop, (J.z - (A.z + o[2])) - vmax)
    st['_drop'] = drop
    st['pelvis_loc'] = (0.0, 0.0, -drop + bob[0] * math.cos(bob[1] * w))
    st['pelvis'] = (pitch_amp * math.sin(w), 2.0 * math.sin(w), 0.0)
    st['spine'] = (flex_amp * math.sin(w + lead), 0.0, 2.5 * math.sin(w))
    st['chest'] = (-0.6 * flex_amp * math.sin(w + 2 * lead), -2.0 * math.sin(w), -2.0 * math.sin(w))
    st['neck'] = (-0.5 * pitch_amp * math.sin(w + 0.6), 0.0, 1.5 * math.sin(w + 0.4))
    st['head'] = (-0.4 * pitch_amp * math.sin(w + 1.0), 0.0, 0.0)
    st['jaw'] = (-1.0 - 2.0 * (0.5 + 0.5 * math.sin(2 * w)), 0.0, 0.0)
    st['tail1'] = (2.0 * math.sin(w), 0.0, 9.0 * math.sin(w + 0.8)); st['tail2'] = (0.0, 0.0, 12.0 * math.sin(w + 1.6)); st['tail3'] = (0.0, 0.0, 14.0 * math.sin(w + 2.4))
    return st

def clip_state(name, f):
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name)
    if k == 'idle':
        w = 2 * math.pi * f / N; st = {}
        st['pelvis_loc'] = (0, 0, -0.012 * (0.5 - 0.5 * math.cos(w)))
        st['spine'] = (1.2 * math.sin(w), 0, 0); st['chest'] = (1.5 * math.sin(w), 0, 0)
        st['neck'] = (-1.0 * math.sin(w) + 1.5 * math.sin(2 * w) * 0.3, 0, 3.0 * math.sin(w + 0.5))
        st['head'] = (1.0 * math.sin(2 * w), 2.0 * math.sin(w), 0)
        tw = math.exp(-((f / N - 0.62) * 14) ** 2)                       # one twitch per cycle: a jaw snap and a head jerk
        st['jaw'] = (-1.0 - 12.0 * tw, 0, 0); st['head'] = (st['head'][0] + 5 * tw, st['head'][1], 6 * tw)
        st['tail1'] = (0, 0, 6 * math.sin(w)); st['tail2'] = (0, 0, 8 * math.sin(w + 0.9)); st['tail3'] = (0, 0, 10 * math.sin(w + 1.8))
        return st
    if k == 'walk':
        return gait(f, N, c['speed'], 0.65, dict(BL=0.0, FL=0.75, BR=0.5, FR=0.25), 0.10, (0.015, 2), 2.0, 2.0, 0.5)
    if k == 'run':
        return gait(f, N, c['speed'], c.get('duty', 0.35), dict(FL=0.0, FR=0.12, BL=0.55, BR=0.67), 0.16, (0.04, 1), 6.0, 7.0, 1.2)
    if k == 'bite':
        cf = c['contact']; tw = c.get('twist', 0.0)
        st = {}
        st['pelvis_loc'] = (0, kf([(0, 0), (cf - 5, 0.10), (cf, -0.20), (cf + 4, -0.16), (N, 0)], f), kf([(0, 0), (cf - 5, -0.03), (cf, -0.07), (N, 0)], f))
        st['pelvis'] = (kf([(0, 0), (cf - 5, 6), (cf, -6), (N, 0)], f), 0, 0)
        st['chest'] = (kf([(0, 0), (cf - 5, 10), (cf, -8), (cf + 4, -6), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (cf - 5, 14), (cf, -10), (N, 0)], f), 0, kf([(0, 0), (cf - 3, -tw), (cf, tw), (cf + 4, -tw * 0.5), (N, 0)], f))
        st['head'] = (kf([(0, 0), (cf - 4, 12), (cf, -6), (N, 0)], f), kf([(0, 0), (cf, tw * 0.6), (N, 0)], f),
                      kf([(0, 0), (cf + 1, 8), (cf + 2, -8), (cf + 3, 6), (cf + 5, 0), (N, 0)], f))
        st['jaw'] = (kf([(0, -3), (cf - 5, -38), (cf - 2, -42), (cf, 0), (cf + 5, -4), (N, -3)], f), 0, 0)
        st['tail1'] = (kf([(0, 0), (cf - 4, 10), (cf, -6), (N, 0)], f), 0, 0)
        return st
    if k == 'spit':
        rf = c['release']; st = {}
        heave = 0.0 if f < 14 or f > rf - 6 else math.sin((f - 14) / (rf - 20) * 3 * 2 * math.pi)
        st['pelvis_loc'] = (0, kf([(0, 0), (12, 0.12), (rf - 3, 0.14), (rf, -0.10), (rf + 7, -0.08), (N, 0)], f), kf([(0, 0), (12, -0.02), (rf, -0.05), (N, 0)], f))
        st['pelvis'] = (kf([(0, 0), (12, 5), (rf, -4), (N, 0)], f), 0, 0)
        st['spine'] = (kf([(0, 0), (12, 6), (rf, -4), (N, 0)], f) + 6 * heave, 0, 0)
        st['chest'] = (kf([(0, 0), (12, 14), (rf - 4, 16), (rf, -8), (rf + 7, -8), (N, 0)], f) - 5 * heave, 0, 0)
        st['neck'] = (kf([(0, 0), (12, 18), (rf - 4, 20), (rf, -12), (rf + 7, -10), (N, 0)], f), 0, kf([(rf, 0), (rf + 2, 5), (rf + 4, -5), (rf + 6, 3), (rf + 8, 0)], f))
        st['head'] = (kf([(0, 0), (12, 10), (rf - 4, 8), (rf, -14), (rf + 7, -12), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (12, -12), (rf - 6, -18), (rf - 1, -50), (rf + 7, -48), (rf + 11, -6), (N, -3)], f) - 6 * abs(heave), 0, 0)
        st['tail1'] = (kf([(0, 0), (12, 12), (rf, -8), (N, 0)], f), 0, 0)
        return st
    if k == 'hit':
        st = {}
        st['pelvis_loc'] = (kf([(0, 0), (3, 0.04), (N, 0)], f), kf([(0, 0), (3, 0.09), (N, 0)], f), kf([(0, 0), (3, -0.02), (N, 0)], f))
        st['pelvis'] = (kf([(0, 0), (3, -4), (N, 0)], f), kf([(0, 0), (3, 7), (N, 0)], f), 0)
        st['chest'] = (kf([(0, 0), (3, 10), (N, 0)], f), 0, kf([(0, 0), (3, 8), (N, 0)], f))
        st['neck'] = (kf([(0, 0), (3, 14), (N, 0)], f), 0, kf([(0, 0), (3, 12), (N, 0)], f))
        st['head'] = (kf([(0, 0), (2, 16), (N, 0)], f), kf([(0, 0), (3, -8), (N, 0)], f), 0)
        st['jaw'] = (kf([(0, -3), (2, -22), (8, -6), (N, -3)], f), 0, 0)
        st['tail1'] = (0, 0, kf([(0, 0), (3, -14), (N, 0)], f))
        return st
    if k == 'death':
        st = {}; c0, c1 = 6, 18
        roll = kf([(0, 0), (c0, -6), (c1, 78), (N, 82)], f)
        st['pelvis_loc'] = (kf([(0, 0), (c0, -0.03), (c1, 0.10), (N, 0.10)], f), kf([(0, 0), (c0, 0.06), (N, 0.08)], f), 0.0)
        st['pelvis'] = (kf([(0, 0), (c0, 6), (c1, 0), (N, 0)], f), roll, 0)
        st['chest'] = (kf([(0, 0), (c0, 14), (c1, -4), (N, -6)], f), 0, kf([(0, 0), (c1, 8), (N, 10)], f))
        st['neck'] = (kf([(0, 0), (c0, 18), (c1, -16), (N, -20)], f), 0, kf([(0, 0), (c1, 10), (N, 14)], f))
        st['head'] = (kf([(0, 0), (c0, 14), (c1, -10), (N, -14)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (c0, -40), (c1, -26), (N, -30)], f), 0, 0)
        st['tail1'] = (0, 0, kf([(0, 0), (c1, 18), (N, 24)], f)); st['tail2'] = (0, 0, kf([(0, 0), (c1, 14), (N, 20)], f))
        infl = kf([(0, 1.0), (c0, 1.0), (c0 + 7, 0.0), (N, 0.0)], f)
        for lg in LEGS:
            fr = lg[0] == 'F'; cur = kf([(0, 0), (c0, 0), (c1, 1), (N, 1.1)], f)
            st['fk_' + lg] = (infl, (-35 if fr else 30) * cur, (60 if fr else -55) * cur, (-30) * cur)
        return st
    raise KeyError(k)

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
            pb['pelvis'].location = pb['pelvis'].location + wloc('pelvis', (0, 0, -need - 0.002)); bpy.context.view_layer.update()
        ikerr = max([((arm.matrix_world @ pb['leg_%s_2' % lg].tail) - (arm.matrix_world @ pb['ik_' + lg].head)).length
                    for lg in LEGS if pb['leg_%s_2' % lg].constraints[0].influence > 0.99], default=0.0)
        ikmax = max(ikmax, ikerr) if f else ikerr
        mz, co = mesh_minz()
        for _ in range(4):
            if not (c.get('ground_solve') and mz < 0.0): break
            l = pb['pelvis'].location.copy(); pb['pelvis'].location = l + wloc('pelvis', (0, 0, -mz + 0.003)); bpy.context.view_layer.update()
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
            if n in ('pelvis', 'root'): p.location = l; p.keyframe_insert('location', frame=f, group=n)
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
