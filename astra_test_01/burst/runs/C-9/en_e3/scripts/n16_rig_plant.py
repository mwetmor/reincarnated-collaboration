# EN-E3 stage 3+4 for the STATIONARY PLANT (n10 with a stem/head/leaf-rosette skeleton; no legs, never rotates; the sprout is a
# GROWTH by the stem-foot bone's scale; jaw cut / mouth bag / weights / bake / lint / export are n10's own). n10 header follows.
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

# ---------------- landmarks (PLANT: a floor rosette of leaves, one stem, a head with a horizontal mouth facing -Y) ----------------
NLEAF = CFG.get('leaves', 6)
slices = []
for z in np.arange(0.2 * H, H, 0.04):
    S = V[np.abs(V[:, 2] - z) < 0.025]
    if len(S) > 10: slices.append((z, float(np.ptp(S[:, 1])), float(np.ptp(S[:, 0]))))
z_hb = next(z for z, ly, lx in slices if ly > CFG.get('head_min_len', 0.5) and z > 0.4 * H) - 0.02
HV = V[V[:, 2] > z_hb]
y0 = float(HV[:, 1].min()); yb = float(HV[:, 1].max()); HL = yb - y0
zh_c = float((HV[:, 2].min() + HV[:, 2].max()) / 2)
FR = HV[HV[:, 1] < y0 + 0.08 * HL]
z_lip = float(FR[:, 2].min() + CFG.get('lip_z_frac', 0.5) * np.ptp(FR[:, 2]))
y_hinge = y0 + CFG.get('hinge_frac', 0.80) * HL
z_hinge = z_lip + CFG.get('hinge_rise', 0.02)
y_hb = yb
ST = V[(V[:, 2] > 0.3 * z_hb) & (V[:, 2] < 0.9 * z_hb)]
sx, sy = float(np.median(ST[:, 0])), float(np.median(ST[:, 1]))
LW = V[V[:, 2] < CFG.get('leaf_band', 0.14) * H]
ang = np.arctan2(LW[:, 1] - sy, LW[:, 0] - sx); rad = np.hypot(LW[:, 0] - sx, LW[:, 1] - sy)
LW, ang, rad = LW[rad > 0.25], ang[rad > 0.25], rad[rad > 0.25]
cang = np.linspace(-math.pi, math.pi, NLEAF, endpoint=False) + math.pi / NLEAF
for _ in range(30):
    dd = np.abs(np.angle(np.exp(1j * (ang[:, None] - cang[None]))))
    lab = dd.argmin(1)
    cang = np.array([np.angle(np.exp(1j * ang[lab == k]).mean()) if (lab == k).any() else cang[k] for k in range(NLEAF)])
leaves = {}
for k in range(NLEAF):
    P = LW[lab == k]
    if len(P) < 20: continue
    tip = P[np.argmax(np.hypot(P[:, 0] - sx, P[:, 1] - sy))]
    leaves['leaf%d' % k] = dict(ang=float(cang[k]), tip=tip.tolist(), n=int(len(P)))
LM.update(H=H, z_head_base=z_hb, y_snout=y0, y_head_back=yb, z_lip=z_lip, y_hinge=y_hinge, stem_xy=[sx, sy], leaves=leaves)
LEGS = []
ank_z = 0.0

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
hx, hy = sx, sy
bone('Hips', (hx, hy, 0.02), (hx, hy, 0.30 * z_hb), 'root')                    # the stem's foot: the GROWTH bone (scaled in the sprout)
bone('stem1', (hx, hy, 0.30 * z_hb), (hx, hy, 0.62 * z_hb), 'Hips', conn=True)
bone('stem2', (hx, hy, 0.62 * z_hb), (hx, hy, z_hb), 'stem1', conn=True)
hc = (0, (y0 + yb) / 2, zh_c)
bone('neck', (hx, hy, z_hb), hc, 'stem2', conn=True)
bone('head', hc, (0, y0 + 0.03, zh_c), 'neck', conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.05, z_lip - 0.06), 'head')
for nm, Lf in leaves.items():
    a_ = Lf['ang']; r0 = 0.22; tip = Lf['tip']
    root_ = (hx + r0 * math.cos(a_), hy + r0 * math.sin(a_), 0.06); mid = ((root_[0] + tip[0]) / 2, (root_[1] + tip[1]) / 2, 0.07)
    bone(nm + '_1', root_, mid, 'Hips'); bone(nm + '_2', mid, (tip[0], tip[1], max(tip[2], 0.05)), nm + '_1', conn=True)
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
hfaces = [f for f in bm.faces if (mw @ f.calc_center_median()).y < y_hinge - 0.01 and (mw @ f.calc_center_median()).z > z_hb]   # plant: head only
geom = list({v for f in hfaces for v in f.verts}) + list({e for f in hfaces for e in f.edges}) + hfaces
res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co_l, plane_no=n_l, dist=1e-6)
cut = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge) and (mw @ ((e.verts[0].co + e.verts[1].co) / 2)).y < y_hinge - 0.02]
bmesh.ops.split_edges(bm, edges=cut)
bm.verts.index_update()
side = {}
for v in bm.verts:
    p = mw @ v.co
    if p.y < y_hinge + 0.04 and p.z > z_hb:
        if v.link_faces:
            cmean = sum(((mw @ f.calc_center_median()) for f in v.link_faces), Vector()) / len(v.link_faces)
        else:
            cmean = p
        side[v.index] = (cmean - lipA).dot(pn) < 0
bm.to_mesh(me); bm.free(); me.update()
LM['mouth_cut_edges'] = len(cut)

hw = float(np.quantile(np.abs(V[(V[:, 1] < y0 + 0.5 * HL) & (np.abs(V[:, 2] - z_lip) < 0.05) & (V[:, 2] > z_hb)][:, 0]), 0.9))
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
    if n.startswith('leaf'):
        a_ = leaves[n.split('_')[0]]['ang']; da = np.abs(np.angle(np.exp(1j * (np.arctan2(VW[:, 1] - sy, VW[:, 0] - sx) - a_))))
        g = ((VW[:, 2] < CFG.get('leaf_zmax', 0.40)) & (da < math.pi / NLEAF * 1.3) & (np.hypot(VW[:, 0] - sx, VW[:, 1] - sy) > 0.30)).astype(float)
    if n in ('head', 'jaw'):
        g = (VW[:, 2] > z_hb - 0.05).astype(float)
    if n in ('Hips', 'stem1', 'stem2', 'neck'):
        g = ~((VW[:, 2] < CFG.get('leaf_zmax', 0.40)) & (np.hypot(VW[:, 0] - sx, VW[:, 1] - sy) > 0.32)) * 1.0   # the curled leaf rims (up to 0.4 m) are leaf, never stem
    Wm[:, j] = g / (dist ** 4 + 1e-6)
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
    if p.z < max(z_lip - 0.40, z_hb) or p.z > zh_c + 0.6: continue
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
    # channels: Hips/stem1/stem2/neck/head/jaw rotations (+rx = the head end goes BACK/UP), leaf rotations (+rx = the leaf tip curls UP),
    # 'grow' = the stem-foot bone's uniform scale (the sprout)
    for n in ('Hips', 'stem1', 'stem2', 'neck', 'head', 'jaw'):
        r = st.get(n)
        if r: pb[n].rotation_quaternion = wrot(n, *r)
    for nm in leaves:
        c_ = st.get('leaf_curl', 0.0) + st.get(nm, 0.0)
        if c_:
            # curl = rotation about the leaf's own horizontal side axis, so every leaf lifts its tip toward the stem
            for k in (1, 2):
                b = arm.data.bones['%s_%d' % (nm, k)]; dv = (b.tail_local - b.head_local); dv.z = 0; ax = dv.normalized().cross(Vector((0, 0, 1))).normalized()   # d x Z: + lifts the tip, for every leaf
                m = b.matrix_local.to_3x3(); R = Quaternion(ax, math.radians(c_ * (0.6 if k == 1 else 1.0))).to_matrix()
                pb['%s_%d' % (nm, k)].rotation_quaternion = (m.inverted() @ R @ m).to_quaternion()
    if 'grow' in st: pb['Hips'].scale = (st['grow'],) * 3
for p in pb: p.rotation_mode = 'QUATERNION'

def leafwave(st, w, amp):
    for i, nm in enumerate(sorted(leaves)):
        st[nm] = amp * (0.5 + 0.5 * math.sin(w + i * 1.05))      # curl UP only: a leaf lying on the floor cannot dip into it

def clip_state(name, f):
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name)
    if k == 'idle':
        w = 2 * math.pi * f / N; st = {}
        st['stem1'] = (2.5 * math.sin(w), 0, 2.0 * math.sin(2 * w)); st['stem2'] = (2.5 * math.sin(w + 0.7), 0, 3.0 * math.sin(2 * w + 0.6))
        st['neck'] = (3.0 * math.sin(w + 1.4), 0, 5.0 * math.sin(w + 0.3)); st['head'] = (2.0 * math.sin(2 * w), 2.5 * math.sin(w), 0)
        snap = math.exp(-((f / N - 0.55) * 14) ** 2)
        st['jaw'] = (-3.0 - 6.0 * (0.5 - 0.5 * math.cos(2 * w)) - 18.0 * snap, 0, 0)     # breathing jaw, one hungry snap
        leafwave(st, 2 * w, 4.0)
        return st
    if k == 'bite':
        cf = c['contact']; st = {}
        st['stem1'] = (kf([(0, 0), (cf - 6, 12), (cf - 1, -16), (cf + 4, -12), (N, 0)], f), 0, 0)
        st['stem2'] = (kf([(0, 0), (cf - 6, 14), (cf - 1, -18), (cf + 4, -14), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (cf - 6, 18), (cf - 1, -8), (cf + 4, -6), (N, 0)], f), 0, kf([(0, 0), (cf, 0), (cf + 2, 8), (cf + 4, -8), (cf + 6, 0), (N, 0)], f))
        st['head'] = (kf([(0, 0), (cf - 6, 10), (cf - 1, 12), (cf, 2), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (cf - 6, -25), (cf - 1, -58), (cf, -4), (cf + 4, -6), (N, -3)], f), 0, 0)
        st['leaf_curl'] = kf([(0, 0), (cf - 6, 8), (cf, 0), (N, 0)], f)
        return st
    if k == 'spit':
        # swell back, then HEAVE the head up and forward and lob the seed (a mortar shot) at the release, mouth gaping upward
        rf = c['release']; st = {}
        pump = 0.0 if f < 4 or f > rf - 3 else math.sin((f - 4) / (rf - 7) * 2 * 2 * math.pi)
        st['stem1'] = (kf([(0, 0), (rf - 6, 14), (rf, -10), (rf + 6, -6), (N, 0)], f) + 3 * pump, 0, 0)
        st['stem2'] = (kf([(0, 0), (rf - 6, 16), (rf, -12), (rf + 6, -8), (N, 0)], f) + 3 * pump, 0, 0)
        st['neck'] = (kf([(0, 0), (rf - 6, 10), (rf, 18), (rf + 6, 10), (N, 0)], f), 0, 0)
        st['head'] = (kf([(0, 0), (rf - 6, -6), (rf, 22), (rf + 6, 12), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -3), (rf - 6, -10), (rf - 1, -55), (rf + 4, -55), (rf + 10, -5), (N, -3)], f) - 4 * abs(pump), 0, 0)
        st['leaf_curl'] = kf([(0, 0), (rf - 6, 10), (rf, 0), (N, 0)], f)
        return st
    if k == 'hit':
        st = {}
        st['stem1'] = (kf([(0, 0), (3, 10), (N, 0)], f), 0, kf([(0, 0), (3, 6), (N, 0)], f)); st['stem2'] = (kf([(0, 0), (4, 12), (N, 0)], f), 0, 0)
        st['neck'] = (kf([(0, 0), (3, 16), (N, 0)], f), 0, kf([(0, 0), (3, 12), (N, 0)], f))
        st['jaw'] = (kf([(0, -3), (2, -30), (8, -6), (N, -3)], f), 0, 0)
        st['leaf_curl'] = kf([(0, 0), (3, 14), (N, 0)], f)
        return st
    if k == 'death':
        # WILT: the stem sags forward in stages, the head drops toward the floor, the jaw falls slack, the leaves curl up; held
        st = {}; c0, c1 = 10, 44
        st['stem1'] = (kf([(0, 0), (c0, 6), (c1, -28), (N, -30)], f), 0, kf([(0, 0), (c1, 10), (N, 12)], f))
        st['stem2'] = (kf([(0, 0), (c0, 8), (c1, -38), (N, -42)], f), 0, kf([(0, 0), (c1, 8), (N, 9)], f))
        st['neck'] = (kf([(0, 0), (c0, 14), (c1, -30), (N, -34)], f), 0, 0)
        st['head'] = (kf([(0, 0), (c0, 10), (c1, -20), (N, -24)], f), kf([(0, 0), (c1, 16), (N, 18)], f), 0)
        st['jaw'] = (kf([(0, -3), (c0, -40), (c1, -22), (N, -26)], f), 0, 0)
        st['leaf_curl'] = kf([(0, 0), (c0, 0), (c1, 28), (N, 30)], f)
        return st
    if k == 'sprout':
        # the p05 EMERGENCE: the plant GROWS up out of the floor (the stem foot scales 0.03 -> 1 with a small overshoot), the leaves
        # unfurl from a tight bud, the head lifts and opens once at the end. No translation below the floor: a sprite has no floor.
        st = {}
        st['grow'] = kf([(0, 0.03), (int(N * 0.75), 1.06), (N, 1.0)], f)
        st['leaf_curl'] = kf([(0, 45), (int(N * 0.6), 14), (N, 0)], f)
        st['stem1'] = (kf([(0, 8), (int(N * 0.7), -4), (N, 0)], f), 0, 0); st['stem2'] = (kf([(0, 10), (int(N * 0.7), -5), (N, 0)], f), 0, 0)
        st['head'] = (kf([(0, -30), (int(N * 0.7), 12), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (int(N * 0.8), -2), (int(N * 0.9), -30), (N, -4)], f), 0, 0)
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
            pb['Hips'].location = pb['Hips'].location + wloc('Hips', (0, 0, -need - 0.002)); bpy.context.view_layer.update()
        ikerr = max([((arm.matrix_world @ pb['leg_%s_2' % lg].tail) - (arm.matrix_world @ pb['ik_' + lg].head)).length
                    for lg in LEGS if pb['leg_%s_2' % lg].constraints[0].influence > 0.99], default=0.0)
        ikmax = max(ikmax, ikerr) if f else ikerr
        mz, co = mesh_minz()
        # STEM SOLVE (plant): a head/stem that would sag through the floor is straightened 2 deg at a time (stem1, then stem2):
        # a rooted plant is never LIFTED to clear the floor. Leaves lying on the floor stop at it the same way (less curl-down).
        for _ in range(70):
            if mz >= -0.003: break
            # straighten whichever of stem1 / stem2 / neck / head is bent the most, 2 deg toward upright
            cand = [(abs(st.get(n_, (0, 0, 0))[0]), n_) for n_ in ('stem1', 'stem2', 'neck', 'head') if abs(st.get(n_, (0, 0, 0))[0]) >= 2.0]
            if not cand: break
            n_ = max(cand)[1]; r = st[n_]; st[n_] = (r[0] - 2.0 * math.copysign(1, r[0]), r[1], r[2])
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
            if n == 'Hips': p.scale = s; p.keyframe_insert('scale', frame=f, group=n)
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
