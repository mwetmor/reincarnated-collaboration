# WHIRLWIND v3, A FEET-ON-GROUND PIVOT (Matt, 2026-09-30, on v2's paddle turn: "the footwork ... it's horrible. Either
# try text to animation ... or just make it a feet on ground pivot if that wont work. Regarding the head focus during
# whirlwind ... just leave it focused towards the direction of the blades and tilted a bit towards the spinning").
#
#   python3 scripts/j_whirl4.py <body.glb> <pose.json> <out.glb> [--T 1.0] [--half-w 0.11] [--stagger 0.03]
#        [--turnout 8] [--foot-lag 10] [--heel 18] [--drop 0.12] [--bob 0.0] [--lead 15] [--head-yaw 15]
#        [--head-tilt 8] [--json f]
#
# ROUTE (a), text-to-motion, was NOT run: the POST that spends Meshy credits was refused by this session's permission
# system (not by the API); that is Matt's call to make directly, not an agent's. So this is route (b):
#   BOTH FEET stay on the ground and TURN ON THEIR BALLS -- no step, no lift. Each ball sits --half-w m either side of
#            the spin axis (--stagger m fore/aft), the pair turning with the body; the heels are up --heel deg (on the
#            balls), the toes flat, the feet turned out --turnout deg, and the feet LAG the hips by --foot-lag deg -- the
#            hips and torso turn over the feet. A full revolution on the balls cannot keep a ball FIXED in the world
#            (the legs would wind): each ball swivels round a --half-w m circle, in contact throughout. Said, not hidden.
#   the KNEES bent: the hips --drop m below the reference stance, the knee aimed over the foot (pole = the foot's forward)
#   the HIPS squared to the spin (the idle's 37 deg fighting-stance yaw removed), the torso LEADING the hips by --lead deg
#            spread up the spine
#   the ARMS: scripts/j_whirl_pose.py's solved pose (both weapons held out in front of the chest at about shoulder width,
#            the blades turned toward the spin), turned rigidly with the chest -- no whip
#   the HEAD faces where the blades point (--head-yaw deg off the chest toward the spin) and is tilted --head-tilt deg
#            toward the spin. CONSTANT relative to the chest: no spotting, no snap.
# Everything is a function of the phase with period one cycle, so the last key IS the first: the loop closes exactly.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, POSE, OUT = a[:3]
opt = lambda k, d=None: float(a[a.index(k) + 1]) if k in a else d
T = opt('--T', 1.0); N = int(round(T * 30)); T = N / 30.0
HW = opt('--half-w', 0.11); STAG = opt('--stagger', 0.03); TURN = math.radians(opt('--turnout', 8))
FLAG = math.radians(opt('--foot-lag', 10)); HEEL = math.radians(opt('--heel', 18)); DROP = opt('--drop', 0.12); BOB = opt('--bob', 0.0)
LEAD0 = math.radians(opt('--lead', 15)); HYAW = math.radians(opt('--head-yaw', 15)); HTILT = math.radians(opt('--head-tilt', 8))
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


FOOTREF = {s: math.atan2(*(GP[LEG[s]['toe']][:3, 3] - GP[LEG[s]['foot']][:3, 3])[[0, 2]]) for s in LEG}   # the stance foot's heading
BALL0 = {'Left': np.array([HW, 0.0, STAG]), 'Right': np.array([-HW, 0.0, -STAG])}                          # in the spin frame
TOUT = {'Left': TURN, 'Right': -TURN}            # his left is +X: a left foot turned out points toward +X (positive yaw)
keys = np.arange(N + 1) / N
rows, POSES = [], []
for k in range(N + 1):
    p = keys[k] % 1.0; psi = 2 * math.pi * p
    Rw = {}
    for i in SKIN:
        Rw[i] = Ry(psi + SPREAD.get(i, 0.0) * LEAD0) @ REFR[i]
    Rw[HIPS] = Ry(psi - body_ref) @ REFR[HIPS]                        # hips squared to the spin
    for i in ARMS:
        Rw[i] = Ry(psi + LEAD0) @ REFR[i]
    hp = np.array([0.0, hp_ref[1] - DROP + BOB * math.cos(4 * math.pi * p), 0.0])
    fy = psi - FLAG
    row = dict(k=k, p=round(p, 4))
    for s in ('Left', 'Right'):
        B = LEG[s]; yaw = fy + TOUT[s]; d = yaw - FOOTREF[s]
        fwd = np.array([math.sin(yaw), 0.0, math.cos(yaw)]); lat = np.cross(np.array([0.0, 1, 0]), fwd)
        Rw[B['toe']] = Ry(d) @ REFR[B['toe']]                          # the toes flat
        Rw[B['foot']] = W.axis_angle(lat / np.linalg.norm(lat), HEEL) @ Ry(d) @ REFR[B['foot']]   # the heel up, on the ball
        ball = Ry(fy) @ BALL0[s]; ball[1] = min(ball_y.values())            # both balls ON the ground (the stance's lower one)
        Rw, r_ = ik_leg(Rw, hp, B, ball, pole=fwd + 0.25 * (lat if s == 'Right' else -lat))
        row[s.lower() + '_reach'] = round(r_, 3)
    rows.append(row)
    POSES.append((Rw, hp))
# THE HEAD: toward the blades, tilted toward the spin -- constant off the chest
head_err = []
for k in range(N + 1):
    Rw = POSES[k][0]
    cur = (yaw_of(Rw[HEAD]) - yaw_of(Rw[S2]) + math.pi) % (2 * math.pi) - math.pi
    dl = HYAW - cur
    Rw[NECKB] = Ry(0.4 * dl) @ Rw[NECKB]; Rw[HEAD] = Ry(dl) @ Rw[HEAD]
    hy = yaw_of(Rw[HEAD]); hf = np.array([math.sin(hy), 0.0, math.cos(hy)])
    Rw[HEAD] = W.axis_angle(hf, -HTILT) @ Rw[HEAD]                   # the crown toward his left, the way he turns
    head_err.append(math.degrees((yaw_of(Rw[HEAD]) - yaw_of(Rw[S2]) - HYAW + math.pi) % (2 * math.pi) - math.pi))
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
rep = dict(method="authored feet-on-ground pivot (both balls in contact, IK legs) + the solved arms + a constant head; see the header",
           route_a="text-to-motion NOT run: the credit-spending POST was refused by the session's permission system",
           cycle=dict(T=T, keys=N + 1, fps=30, revolution="one, counter-clockwise (his left)"),
           params=dict(half_w_m=HW, stagger_m=STAG, turnout_deg=math.degrees(TURN), foot_lag_deg=math.degrees(FLAG), heel_deg=math.degrees(HEEL),
                       drop_m=DROP, bob_m=BOB, lead_deg=math.degrees(LEAD0), head_yaw_deg=math.degrees(HYAW), head_tilt_deg=math.degrees(HTILT)),
           ball_orbit=dict(radius_m=round(math.hypot(HW, STAG), 3), speed_m_s=round(2 * math.pi * math.hypot(HW, STAG) / T, 3)),
           pose=os.path.basename(POSE), keys=rows,
           head=dict(off_blade_bearing_worst_deg=round(float(np.abs(np.array(head_err[:-1])).max()), 2)),
           leg_reach_max=dict(left=max(r['left_reach'] for r in rows), right=max(r['right_reach'] for r in rows)))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('cycle', 'ball_orbit', 'head', 'leg_reach_max')}))
