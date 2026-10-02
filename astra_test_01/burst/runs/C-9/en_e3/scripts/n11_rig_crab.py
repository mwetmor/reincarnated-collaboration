# EN-E3 stage 3+4 for the CRAB (a copy of n10_rig_quad.py with the landmarks, skeleton, weights and clips of a shelled many-legged body):
# EN-E3 stage 3+4 for a QUADRUPED (the n10 original's header follows): fit a skeleton to the cleaned mesh, weight it, key the cycles procedurally, export the GLB.
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

# ---------------- landmarks (CRAB: a rigid shell, legs radiating from its rim, two claws in front) ----------------
def kmeans2(P, k, minit=None, seed=3):
    # Blender's python has no scipy: a plain Lloyd k-means, seeded on y quantiles (legs sort front-to-back)
    c = np.array([P[np.argsort(P[:, 1])[int((i + 0.5) / k * len(P))]] for i in range(k)], float)
    for _ in range(50):
        l = np.argmin(((P[:, None, :] - c[None]) ** 2).sum(-1), 1)
        c = np.array([P[l == i].mean(0) if (l == i).any() else c[i] for i in range(k)])
    return c, l
NL = CFG.get('legs_per_side', 3)
low = V[V[:, 2] < CFG.get('foot_band', 0.05) * H]
feet = {}
for side, sgn in (('L', 1), ('R', -1)):
    P = low[low[:, 0] * sgn > 0.05]
    c, l = kmeans2(P[:, :2], NL, minit='++', seed=3)
    order = np.argsort(c[:, 1])                                   # front (most -y) first
    for k, ci in enumerate(order):
        Q = P[l == ci]
        feet['%s%d' % (side, k + 1)] = dict(x=float(np.median(Q[:, 0])), y=float(np.median(Q[:, 1])), n=int(len(Q)))
core = V[(np.abs(V[:, 0]) < 0.35) & (V[:, 2] > 0.45 * H)]
cy = float(np.median(core[:, 1]))
U = V[(np.abs(V[:, 0]) < 0.25) & (np.abs(V[:, 1] - cy) < 0.3)]
z_under = float(np.quantile(U[:, 2], 0.03)); z_top = float(np.quantile(U[:, 2], 0.97))
RB = CFG.get('shell_r', 0.55); zb = z_under + 0.35 * (z_top - z_under)
LM.update(H=H, cy=cy, z_under=z_under, z_top=z_top, feet=feet)
def corridor_z(r, f, t0, t1, w=0.10, q=0.9):
    d = f - r; L = np.linalg.norm(d); u = d / L
    rel = V[:, :2] - r; t = rel @ u / L; perp = np.abs(rel @ np.array([-u[1], u[0]]))
    m = (t > t0) & (t < t1) & (perp < w) & (V[:, 2] > 0.05)
    return float(np.quantile(V[m, 2], q)) if m.sum() > 5 else None

# ---------------- armature ----------------
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm = bpy.context.active_object; arm.name = 'rig'; arm.data.name = 'rig'
eb = arm.data.edit_bones; eb.remove(eb[0])
def bone(name, h, t, parent=None, deform=True, conn=False):
    b = eb.new(name); b.head = Vector(h); b.tail = Vector(t); b.use_deform = deform
    if parent: b.parent = eb[parent]; b.use_connect = conn
    b.roll = 0.0; return name
bone('root', (0, 0, 0), (0, -0.25, 0))
bone('Hips', (0, cy + 0.35, zb), (0, cy - 0.35, zb), 'root')          # the shell: rigid, one bone
LEGS = sorted(feet.keys())
for lg in LEGS:
    f = feet[lg]; sgn = 1 if lg[0] == 'L' else -1
    F = np.array([f['x'], f['y']]); C = np.array([0.0, cy]); u = (F - C) / np.linalg.norm(F - C)
    R0 = C + u * RB
    zk = corridor_z(R0, F, 0.25, 0.55) or (z_top * 0.9); za = corridor_z(R0, F, 0.80, 0.92, q=0.5) or 0.25
    K = R0 + (F - R0) * 0.40; A = R0 + (F - R0) * 0.86
    J = (float(R0[0]), float(R0[1]), z_under + 0.08); Kp = (float(K[0]), float(K[1]), zk - 0.04); Ap = (float(A[0]), float(A[1]), za)
    Tp = (f['x'], f['y'], 0.02)
    bone('leg_%s_1' % lg, J, Kp, 'Hips'); bone('leg_%s_2' % lg, Kp, Ap, 'leg_%s_1' % lg, conn=True)
    bone('leg_%s_3' % lg, Ap, Tp, 'leg_%s_2' % lg, conn=True)
    bone('ik_%s' % lg, Ap, Tp, 'root', deform=False)
    bone('pole_%s' % lg, (Kp[0], Kp[1], Kp[2] + 0.6), (Kp[0], Kp[1], Kp[2] + 0.7), 'root', deform=False)
    LM['leg_' + lg] = dict(joint=J, knee=Kp, ankle=Ap, toe=Tp, chain_len=round(float((Vector(Kp) - Vector(J)).length + (Vector(Ap) - Vector(Kp)).length), 4),
                           rest_reach=round(float((Vector(Ap) - Vector(J)).length), 4))
CLAWS = []
for side, sgn in (('L', 1), ('R', -1)):
    S_ = V[(V[:, 0] * sgn > 0.02) & (np.abs(V[:, 0]) < CFG.get('claw_xmax', 0.85)) & (V[:, 1] < cy - CFG.get('claw_y0', 0.6)) & (V[:, 2] > 0.12) & (V[:, 2] < z_top)]
    tip = S_[np.argmin(S_[:, 1])]
    sh = np.array([sgn * 0.28, cy - RB * 0.8, z_under + 0.05])
    def at(t):
        p = sh + (tip - sh) * t; m = (np.abs(S_[:, 1] - p[1]) < 0.08)
        return (float(np.median(S_[m, 0])), float(p[1]), float(np.median(S_[m, 2]))) if m.sum() > 5 else tuple(map(float, p))
    E_, W_ = at(0.35), at(0.62)
    n = 'claw_%s' % side
    bone(n + '_1', tuple(map(float, sh)), E_, 'Hips'); bone(n + '_2', E_, W_, n + '_1', conn=True); bone(n + '_3', W_, tuple(map(float, tip)), n + '_2', conn=True)
    CLAWS.append(side); LM[n] = dict(shoulder=sh.tolist(), elbow=E_, wrist=W_, tip=tip.tolist())
bpy.ops.object.mode_set(mode='OBJECT')
DEF = [b.name for b in arm.data.bones if b.use_deform]

# ---------------- weights: the shell is RIGID (an ellipse core takes the body bone alone); legs and claws by gated distance ----------------
for o in sc.objects: o.select_set(False)
body.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type='ARMATURE_NAME')
for n in DEF:
    if n not in [g.name for g in body.vertex_groups]: body.vertex_groups.new(name=n)
VW = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
bones_w = [n for n in DEF if n != 'root']
Wm = np.zeros((len(VW), len(bones_w)))
ex, ey = CFG.get('core_ellipse', (0.70, 0.72))
incore = (((VW[:, 0] / ex) ** 2 + ((VW[:, 1] - cy) / ey) ** 2 < 1.0) & (VW[:, 2] > z_under - 0.05)) | \
         ((np.abs(VW[:, 0]) < CFG.get('eye_x', 0.35)) & (VW[:, 2] > z_under + 0.18) & (VW[:, 1] > cy - ey - 0.45))   # the eye stalks ride the shell
for j, n in enumerate(bones_w):
    bh = np.array(arm.data.bones[n].head_local[:]); bt = np.array(arm.data.bones[n].tail_local[:])
    d = bt - bh; t = np.clip(((VW - bh) @ d) / max(d @ d, 1e-9), 0, 1); dist = np.linalg.norm(VW - (bh + t[:, None] * d), axis=1)
    if n == 'Hips':
        Wm[:, j] = np.where(incore, 1e6, 1.0 / (dist ** 4 + 1e-6)); continue
    sgn = 1 if ('_L' in n) else -1
    g = ((VW[:, 0] * sgn > 0.0) & ~incore).astype(float)
    Wm[:, j] = g / (dist ** 4 + 1e-6)
top = np.argsort(-Wm, 1)[:, :3]
for i in range(len(VW)):
    ws = Wm[i, top[i]]; s_ = ws.sum()
    if s_ <= 0: continue
    for j, w in zip(top[i], ws / s_):
        if w > 1e-3: body.vertex_groups[bones_w[j]].add([i], float(w), 'REPLACE')
for m in list(body.modifiers): body.modifiers.remove(m)
md = body.modifiers.new('rig', 'ARMATURE'); md.object = arm
body.parent = arm
LM['weights'] = dict(method='rigid shell core (ellipse %.2f x %.2f m) + gated inverse-distance^4, top 3' % (ex, ey), core_verts=int(incore.sum()))
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
    # channels: Hips (the shell: rotation + 'pelvis_loc'), claw_<S>_<1..3> rotations about WORLD axes (+rx = tip UP, see wrot), feet
    r = st.get('Hips')
    if r: pb['Hips'].rotation_quaternion = wrot('Hips', *r)
    if 'pelvis_loc' in st: pb['Hips'].location = wloc('Hips', st['pelvis_loc'])
    for s_ in CLAWS:
        for k in (1, 2, 3):
            r = st.get('claw_%s_%d' % (s_, k))
            if r: pb['claw_%s_%d' % (s_, k)].rotation_quaternion = wrot('claw_%s_%d' % (s_, k), *r)
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

def claws(st, l1, l2, l3, r1=None, r2=None, r3=None):
    st['claw_L_1'], st['claw_L_2'], st['claw_L_3'] = l1, l2, l3
    st['claw_R_1'], st['claw_R_2'], st['claw_R_3'] = (r1 or (l1[0], -l1[1], -l1[2])), (r2 or (l2[0], -l2[1], -l2[2])), (r3 or (l3[0], -l3[1], -l3[2]))

# SIGN NOTE: the creature faces -Y; wrot() negates rx, so +rx tips a forward-pointing bone UP. rz + turns a -Y bone toward -X (its right).
def gait(f, N, v, duty, offs, lift, bob, pitch_amp, flex_amp, lead):
    T = N / FPS; S = v * duty * T; st = {}
    ph = f / N
    for lg in LEGS:
        u = (ph + offs[lg]) % 1.0
        if u < duty:
            s = u / duty; dy = -S / 2 + S * s; dz = 0.0
        else:
            s = (u - duty) / (1 - duty); dy = S / 2 - S * ease(s); dz = lift * math.sin(math.pi * s)
        st['foot_' + lg] = (0.0, dy, dz, 0.0); st.setdefault('_stance', {})[lg] = u < duty
    w = 2 * math.pi * ph
    st['pelvis_loc'] = (0.0, 0.0, bob[0] * math.cos(bob[1] * w))
    st['Hips'] = (pitch_amp * math.sin(2 * w), 2.5 * math.sin(2 * w + 0.5), 3.0 * math.sin(w))
    sw = math.sin(w)
    claws(st, (8 + 5 * sw, 0, 6), (-6 - 4 * sw, 0, 0), (4 * math.sin(w + 1), 0, 0), (8 - 5 * sw, 0, -6), (-6 + 4 * sw, 0, 0), (4 * math.sin(w + 1 + math.pi), 0, 0))
    return st

def tripod(n_side):
    # an alternating gait for 3 or 4 legs a side: neighbours on a side are half a cycle apart; the two sides are opposite
    o = {}
    for lg in LEGS:
        k = int(lg[1:]) - 1; o[lg] = ((k % 2) * 0.5 + (0.5 if lg[0] == 'R' else 0.0) + 0.08 * k) % 1.0
    return o

def clip_state(name, f):
    c = CL[name]; N = c['frames'] - 1 if c['kind'] == 'oneshot' else c['frames']
    k = c.get('kind_fn', name)
    if k == 'idle':
        w = 2 * math.pi * f / N; st = {}
        st['pelvis_loc'] = (0, 0, -0.015 * (0.5 - 0.5 * math.cos(w)))
        st['Hips'] = (1.2 * math.sin(w), 1.0 * math.sin(w + 1), 2.0 * math.sin(w))
        snap = math.exp(-((f / N - 0.6) * 12) ** 2)
        claws(st, (6 + 4 * math.sin(w), 0, 4 + 3 * math.sin(w)), (-5 - 6 * snap, 0, 0), (4 * snap, 0, 0),
              (6 + 4 * math.sin(w + 1.3), 0, -4 - 3 * math.sin(w + 1.3)), (-5, 0, 0), (2 * math.sin(2 * w), 0, 0))
        for lg in LEGS:
            st['foot_' + lg] = (0, 0, 0.02 * max(0.0, math.sin(w * 2 + int(lg[1:]) * 1.7 + (0 if lg[0] == 'L' else 2))) ** 8, 0)   # a restless toe-tap
        return st
    if k == 'walk':
        return gait(f, N, c['speed'], c.get('duty', 0.55), tripod(NL), 0.14, (0.02, 2), 2.0, 0, 0)
    if k == 'run':
        return gait(f, N, c['speed'], c.get('duty', 0.45), tripod(NL), 0.18, (0.03, 2), 3.0, 0, 0)
    if k == 'slam':
        # both claws rise high over the shell, then SLAM to the ground in front at the roster's contact frame, the shell pitching down
        cf = c['contact']; st = {}
        up = lambda a, b, d: kf([(0, a), (cf - 6, b), (cf, d), (cf + 4, d), (N, a)], f)
        st['pelvis_loc'] = (0, kf([(0, 0), (cf - 6, 0.08), (cf, -0.08), (N, 0)], f), kf([(0, 0), (cf - 6, 0.06), (cf, -0.05), (cf + 4, -0.04), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (cf - 6, 12), (cf, -5), (cf + 4, -4), (N, 0)], f), 0, 0)
        claws(st, (up(0, 70, c.get('slam_down', -6)), 0, up(0, 8, 4)), (up(0, 30, -8), 0, 0), (up(0, 15, -4), 0, 0))
        return st
    if k == 'strike':
        # a single-claw (LEFT) side-swing thrust: the shell twists, the claw sweeps across the front and stabs at contact
        cf = c['contact']; st = {}
        st['Hips'] = (kf([(0, 0), (cf - 6, 4), (cf, -4), (N, 0)], f), 0, kf([(0, 0), (cf - 6, 24), (cf, -26), (cf + 5, -20), (N, 0)], f))
        st['pelvis_loc'] = (0, kf([(0, 0), (cf - 6, 0.06), (cf, -0.14), (N, 0)], f), 0)
        claws(st, (kf([(0, 0), (cf - 6, 35), (cf, 5), (N, 0)], f), 0, kf([(0, 0), (cf - 6, 40), (cf, -30), (cf + 5, -25), (N, 0)], f)),
                  (kf([(0, 0), (cf - 6, 20), (cf, -10), (N, 0)], f), 0, 0), (kf([(0, 0), (cf - 6, 20), (cf, -15), (N, 0)], f), 0, 0),
                  (10, 0, -8), (-10, 0, 0), (0, 0, 0))
        return st
    if k == 'breath':
        # rear back, claws spread wide, then the shell tips forward and holds while the freezing mist pours from the mouth (release)
        rf = c['release']; st = {}
        st['pelvis_loc'] = (0, kf([(0, 0), (rf - 6, 0.10), (rf, -0.04), (rf + 22, -0.04), (N, 0)], f), kf([(0, 0), (rf - 6, 0.10), (rf, 0.04), (rf + 22, 0.04), (N, 0)], f))
        sh = 0.0 if f < rf or f > rf + 22 else math.sin((f - rf) * 1.3) * 1.5
        st['Hips'] = (kf([(0, 0), (rf - 6, 24), (rf, 10), (rf + 22, 10), (N, 0)], f) + sh, 0, 0)
        claws(st, (kf([(0, 0), (rf - 6, 40), (rf, 25), (rf + 22, 25), (N, 0)], f), 0, kf([(0, 0), (rf - 6, 60), (rf, 55), (rf + 22, 55), (N, 0)], f)),
                  (kf([(0, 0), (rf - 6, 20), (rf + 22, 20), (N, 0)], f), 0, 0), (kf([(0, 0), (rf - 4, 25), (rf + 22, 25), (N, 0)], f), 0, 0))
        return st
    if k == 'lob':
        # both claws scoop low, rise overhead, and FLING forward at the release (the lobbed water/ice spout)
        rf = c['release']; st = {}
        st['Hips'] = (kf([(0, 0), (rf - 8, -6), (rf - 2, 10), (rf, -4), (N, 0)], f), 0, 0)
        st['pelvis_loc'] = (0, kf([(0, 0), (rf - 8, -0.04), (rf - 2, 0.08), (rf, -0.06), (N, 0)], f), kf([(0, 0), (rf - 8, -0.06), (rf - 2, 0.06), (N, 0)], f))
        claws(st, (kf([(0, 0), (rf - 8, -4), (rf - 2, 75), (rf, 30), (rf + 4, 10), (N, 0)], f), 0, kf([(0, 0), (rf - 8, 10), (rf, 4), (N, 0)], f)),
                  (kf([(0, 0), (rf - 8, -2), (rf - 2, 30), (rf, 0), (N, 0)], f), 0, 0), (kf([(0, 0), (rf - 2, 20), (rf, -10), (N, 0)], f), 0, 0))
        return st
    if k == 'hit':
        st = {}
        st['pelvis_loc'] = (kf([(0, 0), (3, 0.05), (N, 0)], f), kf([(0, 0), (3, 0.10), (N, 0)], f), kf([(0, 0), (3, -0.04), (N, 0)], f))
        st['Hips'] = (kf([(0, 0), (3, 8), (N, 0)], f), kf([(0, 0), (3, -7), (N, 0)], f), kf([(0, 0), (3, 6), (N, 0)], f))
        claws(st, (kf([(0, 0), (3, 25), (N, 0)], f), 0, kf([(0, 0), (3, 18), (N, 0)], f)), (kf([(0, 0), (3, 15), (N, 0)], f), 0, 0), (kf([(0, 0), (3, 10), (N, 0)], f), 0, 0))
        return st
    if k == 'death':
        # the legs SPLAY: every foot slides outward along its own leg line while the shell drops onto the ground (IK stays on, so
        # each leg buckles at its knee, no leg flips); the shell tilts and the claws fall slack; last frame held. Ground solved.
        st = {}; c0, c1 = 4, 13
        st['pelvis_loc'] = (0, kf([(0, 0), (c0, 0.04), (N, 0.05)], f), kf([(0, 0), (c0, 0.05), (c1, -(z_under - 0.02)), (N, -(z_under - 0.02))], f))
        st['Hips'] = (kf([(0, 0), (c0, 8), (c1, -5), (N, -6)], f), kf([(0, 0), (c1, 7), (N, 8)], f), kf([(0, 0), (c1, 5), (N, 6)], f))
        spl = kf([(0, 0), (c0, 0), (c1, 0.12), (N, 0.14)], f)
        for lg in LEGS:
            Lm = LM['leg_' + lg]; d = Vector(Lm['toe']) - Vector(Lm['joint']); d.z = 0; d.normalize()
            st['foot_' + lg] = (d.x * spl, d.y * spl, 0.25 * spl, 0.0)
        claws(st, (kf([(0, 0), (c0, 20), (c1, -8), (N, -10)], f), 0, kf([(0, 0), (c1, 15), (N, 18)], f)), (kf([(0, 0), (c1, -12), (N, -14)], f), 0, 0), (0, 0, 0))
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
        # CLAW CONTACT SOLVE: a claw that would go into the floor is lifted (its shoulder pitched up 2 deg at a time) until its lowest
        # point sits on the ground -- so a slam lands ON the floor at the contact frame instead of through it.
        for _ in range(40):
            if mz >= -0.003: break
            wv = co[int(np.argmin(co[:, 2]))]
            if wv[1] > cy - 0.5: break
            sd = 'L' if wv[0] > 0 else 'R'; r = st.get('claw_%s_1' % sd, (0, 0, 0)); st['claw_%s_1' % sd] = (r[0] + 2.0, r[1], r[2])
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
