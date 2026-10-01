# WHIRLWIND v4, A NORMAL BATTLE STANCE TURNING AS ONE (Matt, 2026-09-30, on v3: "just make it a normal battle stance with
# normal planted feet and normal arms at about shoulder width ... The spinning on balls of feet doesn't look great. Also,
# the tilt of the blades made the elbow joints bend backwards ... the speed of the spin needs to be somewhere around 3X
# the current speed. And the blades of the weapons need to be pointed more upwards like a normal prepared battle stance,
# maybe half way between how outstretched they are now and a normal battle stance").
#
#   python3 scripts/j_whirl5.py <body.glb> <pose.json> <out.glb> [--T 0.3333] [--head-tilt 8] [--json f]
#
# THE BODY is the solved pose (scripts/j_whirl_pose.py on his battle stance, idle_guard: both feet FLAT and planted
# where that stance puts them, knees as it bends them, the chest squared; the arms at about shoulder width, elbows bent
# the way the stance bends them, both blades pitched up and forward, no turn into the spin at wrist or elbow) turned
# RIGIDLY about the vertical through his hips, one counter-clockwise revolution per cycle (the conductor: "the whole
# body turns as one on the spin; that's accepted now"). The HEAD faces the blades' bearing, tilted --head-tilt deg toward
# the spin -- set once on the pose (its facing read from the head's own front marker, headfront), then turned with him.
# Every key is the pose under Ry(psi): the last key IS the first, the loop closes exactly, and a key-to-key slerp of a
# turn about one axis is exact, so the runtime's 30 fps rebake reproduces it.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, POSE, OUT = a[:3]
opt = lambda k, d=None: float(a[a.index(k) + 1]) if k in a else d
T = opt('--T', 1.0); N = int(round(T * 30)); T = N / 30.0
HTILT = math.radians(opt('--head-tilt', 8))
m = C.model(BODY); nid = m['nid']; P = m['parent']; names = [nd.get('name') for nd in m['nodes']]


def Ry(t):
    c, s = math.cos(t), math.sin(t); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def nrm(X):
    return X / np.linalg.norm(X, axis=0)


def yaw_of(R):
    f = R @ np.array([0.0, 0, 1]); return math.atan2(f[0], f[2])


def rmin(u, v):
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v); ax = np.cross(u, v); s = np.linalg.norm(ax)
    if s < 1e-9: return np.eye(3)
    return W.axis_angle(ax / s, math.atan2(s, float(u @ v)))


def L4(t, R, s):
    X = np.eye(4); X[:3, :3] = R * s; X[:3, 3] = t; return X


order = []
def visit(i):
    if i in order: return
    if P.get(i) is not None: visit(P[i])
    order.append(i)
for i in range(len(m['nodes'])): visit(i)
pz = json.load(open(POSE))['locals']
GP = {}
for i in order:
    nd = pz.get(names[i]); tr, q, s = (np.array(nd['t']), np.array(nd['r']), np.array(nd['s'])) if nd else m['rest'][i]
    X = L4(tr, W.q2m(q), s); GP[i] = X if P.get(i) is None else GP[P[i]] @ X
SKIN = sorted({j for sk in [0] for j in m['joints']} - {nid['weapon_r'], nid['weapon_l']})
HIPS, S0, S1, S2, NECKB, HEAD = nid['Hips'], nid['Spine'], nid['Spine01'], nid['Spine02'], nid['neck'], nid['Head']
ARMS = [nid[b] for b in ("RightShoulder", "RightArm", "RightForeArm", "RightHand", "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand")]
LEG = {s: dict(up=nid[s + 'UpLeg'], leg=nid[s + 'Leg'], foot=nid[s + 'Foot'], toe=nid[s + 'ToeBase']) for s in ('Left', 'Right')}
REFR = {i: nrm(GP[i][:3, :3]) for i in order}
hp_ref = GP[HIPS][:3, 3].copy()
chest_ref = yaw_of(REFR[S2]); body_ref = yaw_of(REFR[HIPS])
ball_y = {s: float(GP[LEG[s]['toe']][1, 3]) for s in LEG}
SPREAD = {S0: 0.3, S1: 0.6, S2: 1.0, NECKB: 1.0, HEAD: 1.0}


def fk(Rw, hp):
    G = {}
    for i in order:
        tr, q, s = m['rest'][i]; Rl = W.q2m(q)
        if i in Rw:
            Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
            Rl = Rp.T @ Rw[i]
        if i == HIPS:
            tr = (np.linalg.inv(G[P[i]]) @ np.append(hp, 1.0))[:3]
        X = L4(tr, Rl, s); G[i] = X if P.get(i) is None else G[P[i]] @ X
    return G


def ik_leg(Rw, hp, B, toe_target, pole=None):
    G = fk(Rw, hp)
    off = G[B['toe']][:3, 3] - G[B['foot']][:3, 3]; A = toe_target - off
    H, K, Fp = G[B['up']][:3, 3], G[B['leg']][:3, 3], G[B['foot']][:3, 3]
    l1, l2 = np.linalg.norm(K - H), np.linalg.norm(Fp - K)
    dv = A - H; d = float(np.linalg.norm(dv)); u = dv / d; reach = d
    d = min(max(d, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    pv = (K - H) if pole is None else pole
    n = pv - (pv @ u) * u; n = n / np.linalg.norm(n)
    aa = (l1 * l1 - l2 * l2 + d * d) / (2 * d); hh = math.sqrt(max(l1 * l1 - aa * aa, 0.0))
    Kn = H + aa * u + hh * n; An = H + d * u
    R1 = rmin(K - H, Kn - H); Rw[B['up']] = R1 @ Rw[B['up']]
    R2 = rmin(R1 @ (Fp - K), An - Kn); Rw[B['leg']] = R2 @ (R1 @ Rw[B['leg']])
    return Rw, reach / (l1 + l2)


# THE HEAD: toward the blades' bearing, tilted toward the spin -- on the pose, once
def hb(v):
    return math.atan2(v[0], v[2])


blade = sum(nrm(GP[nid[w]][:3, :3])[:, 1] for w in ('weapon_r', 'weapon_l'))
face = GP[nid['headfront']][:3, 3] - GP[HEAD][:3, 3]
dl = (hb(blade) - hb(face) + math.pi) % (2 * math.pi) - math.pi
NOHEAD = '--no-head' in a                                                # v7 (R-C9-108): the stance's own head, untouched
if NOHEAD: dl = 0.0
REFR[NECKB] = Ry(0.4 * dl) @ REFR[NECKB]; REFR[HEAD] = Ry(dl) @ REFR[HEAD]
hf = np.array([math.sin(hb(blade)), 0.0, math.cos(hb(blade))])
if not NOHEAD: REFR[HEAD] = W.axis_angle(hf, -HTILT) @ REFR[HEAD]                      # the crown toward his left, the way he turns
keys = np.arange(N + 1) / N
POSES = []
for k in range(N + 1):
    psi = 2 * math.pi * (keys[k] % 1.0)
    POSES.append(({i: Ry(psi) @ REFR[i] for i in SKIN}, np.array([0.0, hp_ref[1], 0.0])))
Gh = fk(POSES[0][0], POSES[0][1])
face2 = Gh[nid['headfront']][:3, 3] - Gh[HEAD][:3, 3]
head_off = math.degrees((hb(face2) - hb(blade) + math.pi) % (2 * math.pi) - math.pi)
LOC, HL = [], []
for k in range(N + 1):
    Rw, hp = POSES[k]; G = fk(Rw, hp); Lq = {}
    for i in SKIN:
        Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
        Lq[i] = np.array(W.m2q(Rp.T @ Rw[i]), float)
    LOC.append(Lq); HL.append((np.linalg.inv(G[P[HIPS]]) @ np.append(hp, 1.0))[:3])
for i in SKIN:
    LOC[N][i] = LOC[0][i].copy()
    for k in range(1, N + 1):
        if np.dot(LOC[k][i], LOC[k - 1][i]) < 0: LOC[k][i] = -LOC[k][i]
HL[N] = HL[0].copy()
js, b0 = L.load_glb(BODY); bn = bytearray(b0); tnid = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def accs(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1
ti = accs((keys * T).reshape(-1, 1), 'SCALAR', True)
samplers, channels = [], []
for i in SKIN:
    samplers.append(dict(input=ti, output=accs(np.array([LOC[k][i] for k in range(N + 1)]), 'VEC4'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=tnid[names[i]], path='rotation')))
samplers.append(dict(input=ti, output=accs(np.array(HL), 'VEC3'), interpolation='LINEAR'))
channels.append(dict(sampler=len(samplers) - 1, target=dict(node=tnid['Hips'], path='translation')))
js['animations'] = [x for x in js['animations'] if x.get('name') != 'whirlwind'] + [dict(name='whirlwind', samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
rep = dict(method="his battle stance (the solved pose) turned rigidly about the vertical through his hips; see the header",
           cycle=dict(T=T, keys=N + 1, fps=30, revolution="one, counter-clockwise (his left)", rev_per_s=round(1 / T, 3)),
           params=dict(head_tilt_deg=math.degrees(HTILT)), pose=os.path.basename(POSE),
           head=dict(facing_off_blade_bearing_deg=round(head_off, 2), facing_from="headfront - Head", tilt_deg=0.0 if NOHEAD else math.degrees(HTILT), untouched=NOHEAD))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('cycle', 'head')}))
