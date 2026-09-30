# WAR CRY v2 (Matt, 2026-09-30, relayed by the conductor): "raised, but with arms wider and more of an obviously muscle-
# flexing motion: arms outstretched to the sky, then pumping muscles with a slight elbow lower during the pump."
#
#   python3 scripts/j_warcry.py <src body.glb> <into body.glb> <out.glb> [--clip-flex wc388] [--clip-sky wc49]
#        [--head-back 22] [--wrist-max 80] [--out 0.7] [--drop-clips a,b] [--json f]
#
# TWO LIBRARY CLIPS, fetched on his rig and grafted (55_clip_graft):
#   FLEX  Meshy 388 "Show Both Arm Muscles": from rest the arms fling out wide, come up, and set into a double-biceps
#         flex (the elbows below the shoulders), then release
#   SKY   Meshy 49 "Motivational Cheer", its 4.2..6.6 s: both arms thrown up and WIDE to the sky (the fists 0.2 m over
#         the head, 1.15 m apart), held, then brought down
# COMPOSED per key in WORLD space (each joint's rotation away from rest, slerped): the HIPS AND LEGS are the flex clip's
# throughout (one stance, no foot slide from a blend), the upper body (spine, neck, head, both arms) crossfades from the
# flex clip's fling INTO the sky pose and back OUT of it into the flex clip's own flex, which is then PUMPED by its own
# time: the flex clip's arms-high moment and its set flex, played there and back twice -- the forearms curl in and the
# elbows drop, rise, drop.  The CRY'S PEAK (release_s) is the key where the fists stand highest in the sky, and the head
# is tipped back up to --head-back deg around it.
# The weapons ride their mounts: nothing here keys a weapon bone.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
sys.path.insert(0, HERE); B = __import__('j_blend')
a = sys.argv[1:]; SRC, INTO, OUT = a[:3]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CF, CS = opt('--clip-flex', 'wc388'), opt('--clip-sky', 'wc49'); HB = math.radians(float(opt('--head-back', '22')))
m = C.model(SRC); nid = m['nid']; P = m['parent']; names = [nd.get('name') for nd in m['nodes']]
# the TIME MAPS (knots: output time -> source time, piecewise linear) and the sky weight, in the grafted clips' own time
FLEX = [(0.00, 0.00), (0.40, 0.40), (1.25, 0.58), (1.45, 0.62),          # rest -> arms flung wide -> (under the sky) -> arms high
        (1.72, 0.84), (1.90, 0.66), (2.17, 0.88),                        # PUMP 1 down, back up, PUMP 2 down
        (2.40, 1.10), (3.00, 1.90)]                                      # release to rest
SKY = [(0.30, 0.25), (1.45, 1.40)]                                       # the arms thrown up to the sky and held
WSKY = [(0.30, 0.0), (0.55, 1.0), (1.25, 1.0), (1.50, 0.0)]              # the upper body's share of the sky clip
TEND = FLEX[-1][0]


def pl(knots, t):
    xs = [k[0] for k in knots]; ys = [k[1] for k in knots]
    return float(np.interp(t, xs, ys))


def smooth_w(t):
    xs = [k[0] for k in WSKY]; ys = [k[1] for k in WSKY]
    if t <= xs[0]: return ys[0]
    if t >= xs[-1]: return ys[-1]
    i = int(np.searchsorted(xs, t)) ; u = (t - xs[i - 1]) / (xs[i] - xs[i - 1]); u = u * u * (3 - 2 * u)
    return ys[i - 1] + (ys[i] - ys[i - 1]) * u


def nrm(X):
    return X / np.linalg.norm(X, axis=0)


def L4(t, R, s):
    X = np.eye(4); X[:3, :3] = R * s; X[:3, 3] = t; return X


order = []
def visit(i):
    if i in order: return
    if P.get(i) is not None: visit(P[i])
    order.append(i)
for i in range(len(m['nodes'])): visit(i)
GR = {}
for i in order:
    tr, q, s = m['rest'][i]; X = L4(tr, W.q2m(q), s); GR[i] = X if P.get(i) is None else GR[P[i]] @ X
AJ = sorted({n for (n, p) in m['anims'][CF] if p == 'rotation'})
LOWER = {nid[b] for b in ("Hips", "LeftUpLeg", "LeftLeg", "LeftFoot", "LeftToeBase", "RightUpLeg", "RightLeg", "RightFoot", "RightToeBase")}
HIPS, NECK, HEAD = nid['Hips'], nid['neck'], nid['Head']
N = int(round(TEND * 30)); keys = np.arange(N + 1) / 30.0
WR, HP = [], []
for t in keys:
    Gf = C.globals_at(m, CF, pl(FLEX, t)); w = smooth_w(t)
    Gs = C.globals_at(m, CS, pl(SKY, t)) if w > 0 else None
    Rw = {}
    for j in AJ:
        df = nrm(Gf[j][:3, :3]) @ nrm(GR[j][:3, :3]).T
        if Gs is not None and j not in LOWER:
            ds = nrm(Gs[j][:3, :3]) @ nrm(GR[j][:3, :3]).T
            qf, qs = np.array(W.m2q(df), float), np.array(W.m2q(ds), float)
            df = W.q2m(B.slerp(qf, qs, w))
        Rw[j] = df @ nrm(GR[j][:3, :3])
    WR.append(Rw); HP.append(Gf[HIPS][:3, 3].copy())


def fk(Rw, hp):
    G = {}
    for i in order:
        tr, q, s = m['rest'][i]; Rl = W.q2m(q)
        if i in Rw:
            Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3); Rl = Rp.T @ Rw[i]
        if i == HIPS: tr = (np.linalg.inv(G[P[i]]) @ np.append(hp, 1.0))[:3]
        X = L4(tr, Rl, s); G[i] = X if P.get(i) is None else G[P[i]] @ X
    return G


# THE WEAPONS UP AND OUT through the flex: the library's flex brings the fists in beside his face, and the blades --
# rigid in the fists -- then cross in front of his head. Each hand turns (at most --wrist-max deg) so its blade points
# up and out to its own side, eased in as the arms come down from the sky and out again in the release
WMAX = math.radians(float(opt('--wrist-max', '80'))); WOUT = float(opt('--out', '0.7'))
WW = [(1.20, 0.0), (1.45, 1.0), (2.35, 1.0), (2.75, 0.0)]


def ww(t):
    xs = [k[0] for k in WW]; ys = [k[1] for k in WW]
    if t <= xs[0] or t >= xs[-1]: return 0.0
    i = int(np.searchsorted(xs, t)); u = (t - xs[i - 1]) / (xs[i] - xs[i - 1]); u = u * u * (3 - 2 * u)
    return ys[i - 1] + (ys[i] - ys[i - 1]) * u


def rmin(u, v):
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v); ax = np.cross(u, v); sn = np.linalg.norm(ax)
    if sn < 1e-9: return np.zeros(3)
    return ax / sn * math.atan2(sn, float(u @ v))


turned = []
for k in range(N + 1):
    w = ww(keys[k])
    if w <= 0: turned.append(0.0); continue
    G = fk(WR[k], HP[k]); tk = 0.0
    for hand, wb, out in (('RightHand', 'weapon_r', -1.0), ('LeftHand', 'weapon_l', 1.0)):
        Y = nrm(G[nid[wb]][:3, :3])[:, 1]
        d = np.array([WOUT * out, 1.0, 0.0])
        v = rmin(Y, d); ang = float(np.linalg.norm(v))
        if ang > WMAX: v = v / ang * WMAX
        WR[k][nid[hand]] = W.axis_angle(v / max(ang, 1e-9), min(ang, WMAX) * w) @ WR[k][nid[hand]] if ang > 1e-9 else WR[k][nid[hand]]
        tk = max(tk, math.degrees(min(ang, WMAX) * w))
    turned.append(round(tk, 1))

# the CRY'S PEAK: the key where both fists stand highest over the head
hi = []
for k in range(N + 1):
    G = fk(WR[k], HP[k]); hy = G[HEAD][1, 3]
    hi.append(min(G[nid['LeftHand']][1, 3], G[nid['RightHand']][1, 3]) - hy)
kpk = int(np.argmax(hi)); tpk = float(keys[kpk])
# the head tipped back around the peak (about his own left-right axis, world X: he faces +Z)
for k in range(N + 1):
    u = max(0.0, 1.0 - abs(keys[k] - tpk) / 0.45); u = u * u * (3 - 2 * u)
    if u <= 0: continue
    Rb = W.axis_angle(np.array([1.0, 0, 0]), -HB * u)
    WR[k][NECK] = W.axis_angle(np.array([1.0, 0, 0]), -0.4 * HB * u) @ WR[k][NECK]
    WR[k][HEAD] = Rb @ WR[k][HEAD]
LOC, HL = [], []
for k in range(N + 1):
    G = fk(WR[k], HP[k]); Lq = {}
    for i in AJ:
        Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
        Lq[i] = np.array(W.m2q(Rp.T @ WR[k][i]), float)
        if k and np.dot(Lq[i], LOC[-1][i]) < 0: Lq[i] = -Lq[i]
    LOC.append(Lq); HL.append((np.linalg.inv(G[P[HIPS]]) @ np.append(HP[k], 1.0))[:3])
js, b0 = L.load_glb(INTO); bn = bytearray(b0); tnid = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def accs(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1
ti = accs(keys.reshape(-1, 1), 'SCALAR', True)
samplers, channels = [], []
for i in AJ:
    samplers.append(dict(input=ti, output=accs(np.array([LOC[k][i] for k in range(N + 1)]), 'VEC4'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=tnid[names[i]], path='rotation')))
samplers.append(dict(input=ti, output=accs(np.array(HL), 'VEC3'), interpolation='LINEAR'))
channels.append(dict(sampler=len(samplers) - 1, target=dict(node=tnid['Hips'], path='translation')))
drop = set((opt('--drop-clips') or '').split(',')) - {''}
js['animations'] = [x for x in js['animations'] if x.get('name') != 'shout' and x.get('name') not in drop] + [dict(name='shout', samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
rep = dict(method="composed from two library clips (see the header)", T=round(float(keys[-1]), 4), keys=N + 1,
           flex_map=FLEX, sky_map=SKY, sky_weight=WSKY, head_back_deg=math.degrees(HB),
           release=dict(key=kpk, t_s=round(tpk, 4), fists_over_head_m=round(float(hi[kpk]), 3),
                        definition="the cry's peak: the key where both fists stand highest over the head (the arms thrown to the sky)"),
           fists_over_head_by_key=[round(float(x), 3) for x in hi], dropped_clips=sorted(drop),
           weapons_up_and_out=dict(window=WW, wrist_max_deg=math.degrees(WMAX), out=WOUT, turned_deg_by_key=turned))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('T', 'keys', 'release')}))
