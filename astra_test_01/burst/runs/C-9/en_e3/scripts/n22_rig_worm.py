# EN-E3 stage 3+4 for the WORM (the void parasite: a centreline segment chain, a cut sucker maw, a travelling-wave crawl; from n18).
# n18's header follows. EN-E3 stage 3+4 for the FLOATER (the blight sac: no legs, a hovering sac + a front mouth + a ring of tendrils; built from n16).
# n16's header follows. EN-E3 stage 3+4 for the STATIONARY PLANT (n10 with a stem/head/leaf-rosette skeleton; no legs, never rotates; the sprout is a
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

# ---------------- landmarks (WORM: a centreline chain from the maw (-Y) to the tail tip (+Y); a sucker maw cut at the front) ----------------
NS = CFG.get('segments', 8)
y0 = float(V[:, 1].min()); y1 = float(V[:, 1].max()); LF = y1 - y0
ys = np.linspace(y0 + 0.02, y1 - 0.02, NS + 1)
cl = []
for y in ys:
    S = V[np.abs(V[:, 1] - y) < max(0.04, 0.5 * LF / NS)]
    cl.append((float(np.median(S[:, 0])), float(y), float((S[:, 2].min() + S[:, 2].max()) / 2)))
HL = CFG.get('mouth_depth', 0.25)
FRn = V[V[:, 1] < y0 + 0.06]
z_lip = float(FRn[:, 2].min() + CFG.get('lip_z_frac', 0.5) * np.ptp(FRn[:, 2]))
y_hinge = y0 + HL; z_hinge = z_lip + CFG.get('hinge_rise', 0.0)
y_hb = y0 + HL; z_hb = -1.0; zh_c = cl[0][2]
LM.update(H=H, y_snout=y0, y_tail=y1, z_lip=z_lip, y_hinge=y_hinge, centreline=cl)
LEGS = []; ank_z = 0.0; sx, sy = 0.0, (y0 + y1) / 2

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
# Hips = the segment at the body's widest third (the pivot the rear-up lifts about); the chain runs FORWARD to the maw (seg_f*) and BACK
# to the tail (seg_b*), so a front rear-up and a tail lash are both short chains from the middle
im = max(1, int(round(NS * CFG.get('hips_frac', 0.45))))
bone('Hips', cl[im], cl[im - 1], 'root')
prev = 'Hips'
for i in range(im - 1, 0, -1):
    nm = 'seg_f%d' % (im - 1 - i + 1); bone(nm, cl[i], cl[i - 1], prev, conn=True); prev = nm
FRONT = [n for n in ['seg_f%d' % k for k in range(1, im)]]
head_parent = prev
bone('head', cl[0], (cl[0][0], cl[0][1] - 0.15, cl[0][2]), head_parent, conn=True)
bone('jaw', (0, y_hinge, z_hinge), (0, y0 + 0.04, z_lip - 0.08), 'head')
prev = 'Hips'; BACK = []
for i in range(im, NS):
    nm = 'seg_b%d' % (i - im + 1); bone(nm, cl[i], cl[i + 1], prev, conn=(i > im)); prev = nm; BACK.append(nm)
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
hfaces = [f for f in bm.faces if (mw @ f.calc_center_median()).y < y_hinge - 0.01 and (mw @ f.calc_center_median()).z > z_hb]   # worm: the maw end
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
    if n in ('head', 'jaw'):
        g = (VW[:, 1] < y_hinge + 0.10).astype(float)
    Wm[:, j] = g / (dist ** 4 + 1e-6)
Wm = Wm / np.maximum(Wm.sum(1, keepdims=True), 1e-12)
_E = np.array([e.vertices[:] for e in body.data.edges])
_deg = np.zeros(len(VW)); np.add.at(_deg, _E[:, 0], 1); np.add.at(_deg, _E[:, 1], 1)
for _ in range(CFG.get('weight_smooth', 12)):
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
    for n in ['Hips', 'head', 'jaw'] + FRONT + BACK:
        r = st.get(n)
        if r: pb[n].rotation_quaternion = wrot(n, *r)
    if 'pelvis_loc' in st: pb['Hips'].location = wloc('Hips', st['pelvis_loc'])
for p in pb: p.rotation_mode = 'QUATERNION'

def wave(st, w, amp_z, amp_x=0.0, lift=0.0):
    # a TRAVELLING wave down the body: each segment yaws (rz) a phase step behind the one in front; FRONT bones point -Y so +rx lifts
    # them; BACK bones point +Y so a lift there is -rx
    chain = list(reversed(FRONT)) + ['Hips'] + BACK      # head end first
    for i, n in enumerate(chain):
        ph = w - 0.9 * i
        st[n] = (st.get(n, (0, 0, 0))[0], 0.0, st.get(n, (0, 0, 0))[2] + amp_z * math.sin(ph))
    return st

def clip_state(name, f):
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name); w = 2 * math.pi * f / N; st = {}
    if k == 'idle':
        st['seg_f1' if FRONT else 'Hips'] = (3.0 + 2.0 * math.sin(w), 0, 0)
        st['head'] = (2.0 * math.sin(w + 0.7), 0, 6.0 * math.sin(w))
        snap = math.exp(-((f / N - 0.6) * 12) ** 2); st['jaw'] = (-3.0 - 25.0 * snap, 0, 0)
        return wave(st, w, 3.0)
    if k in ('walk', 'run'):
        st['head'] = (3.0, 0, 0)
        st['jaw'] = (-2.0 - 3.0 * (0.5 + 0.5 * math.sin(2 * w)), 0, 0)
        return wave(st, (2 if k == 'run' else 1) * w, 9.0 if k == 'walk' else 12.0)
    if k == 'lunge':
        # the FRONT rears up and back, then STRIKES forward and down onto the target, the maw open, fastening at the contact; holds
        cf = c['contact']; a0 = max(3, cf - 8)
        up = kf([(0, 0), (a0, 22), (cf, -6), (cf + 8, -4), (N, 0)], f)
        for i, n in enumerate(reversed(FRONT)): st[n] = (up * (0.5 + 0.25 * i), 0, 0)
        st['head'] = (kf([(0, 0), (a0, 10), (cf, -14), (N, 0)], f), 0, 0)
        st['jaw'] = (kf([(0, -2), (a0, -10), (cf - 2, -55), (cf, -45), (cf + 8, -45), (cf + 12, -4), (N, -2)], f), 0, 0)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.15), (cf, -0.35), (cf + 8, -0.30), (N, 0)], f), 0)
        for i, n in enumerate(BACK): st[n] = (0, 0, kf([(0, 0), (a0, 8), (cf, -10), (N, 0)], f) * (1 if i % 2 else -1))
        return st
    if k in ('spit', 'drain'):
        # rear the front high, the maw opens at the release (spit: a sharp pump; drain: holds open while the life is drawn)
        rf = c['release']; a0 = max(3, rf - 10); ho = c.get('hold', 6 if k == 'spit' else 14)
        up = kf([(0, 0), (a0, 26), (rf, 18), (rf + ho, 18), (N, 0)], f)
        for i, n in enumerate(reversed(FRONT)): st[n] = (up * (0.5 + 0.25 * i), 0, 0)
        st['head'] = (kf([(0, 0), (a0, -6), (rf, -16), (rf + ho, -16), (N, 0)], f), 0, kf([(rf, 0), (rf + 4, 6), (rf + 8, -6), (rf + ho, 0)], f) if k == 'drain' else 0)
        st['jaw'] = (kf([(0, -2), (a0, -8), (rf - 1, -55), (rf + ho, -50), (rf + ho + 5, -4), (N, -2)], f), 0, 0)
        st['pelvis_loc'] = (0, kf([(0, 0), (a0, 0.10), (rf, -0.08), (N, 0)], f), 0)
        return wave(st, w, 3.0)
    if k == 'hit':
        for i, n in enumerate(reversed(FRONT)): st[n] = (kf([(0, 0), (3, 12), (N, 0)], f), 0, kf([(0, 0), (3, 14), (N, 0)], f) * (1 if i % 2 else -1))
        st['jaw'] = (kf([(0, -2), (2, -30), (8, -4), (N, -2)], f), 0, 0)
        st['pelvis_loc'] = (0, kf([(0, 0), (3, 0.12), (N, 0)], f), 0)
        for i, n in enumerate(BACK): st[n] = (0, 0, kf([(0, 0), (4, 16), (N, 0)], f) * (1 if i % 2 else -1))
        return st
    if k == 'death':
        # it WRITHES (a hard, fast lateral wave), curls into a C, rolls a little onto its side, and goes still; held
        c1 = int(N * 0.6); e = kf([(0, 1.0), (c1, 1.0), (N, 0.0)], f)
        for i, n in enumerate(list(reversed(FRONT)) + BACK):
            st[n] = (0, 0, e * 20.0 * math.sin(3 * w - 1.1 * i) + kf([(0, 0), (c1, 22), (N, 26)], f))
        st['Hips'] = (0, kf([(0, 0), (c1, 30), (N, 40)], f), 0)
        st['jaw'] = (kf([(0, -2), (int(N * 0.3), -50), (N, -30)], f), 0, 0)
        return st
    raise KeyError(k)

def floor_fix(st, co):
    # a segment that dips into the floor: lift the front chain (or, for the back, ease the yaw) -- 2 deg of front lift per pass
    for n in reversed(FRONT):
        r = st.get(n, (0, 0, 0)); st[n] = (r[0] + 1.0, r[1], r[2])
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
        # FLOOR SOLVE (floater): curl the tendril that touches the floor; never lift the sac (its hover is the clip's)
        for _ in range(60):
            if mz >= -0.003 or CL[name].get('kind_fn', name) == 'death': break
            st = floor_fix(st, co); apply(st); bpy.context.view_layer.update(); mz, co = mesh_minz()
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
