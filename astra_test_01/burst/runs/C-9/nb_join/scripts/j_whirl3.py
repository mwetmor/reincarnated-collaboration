# WHIRLWIND v2, AUTHORED FOOTWORK (Matt, 2026-09-30: "a double baseball swing with a battle/baseball stance and good
# footwork to show a real spin. It's all in the feet ... The head should follow the direction of travel").
#
#   python3 scripts/j_whirl3.py <body.glb> <pose.json> <out.glb> [--T 1.0] [--steps 3] [--plant 0.55] [--r-paddle 0.52]
#        [--rel-land -65] [--step-h 0.10] [--drop 0.10] [--bob 0.02] [--lead 15] [--lead-amp 5] [--whip 20]
#        [--whip-ahead 8] [--neck 80] [--snap-keys 3] [--head-share 0.6] [--json f]
#
# WHY AUTHORED. The library was tried first (scripts/j_whirl2.py on Meshy 238 "Axe Spin Attack", fetched on his rig; 91
# "Double Blade Spin" kneels, leaps and travels 2 m). 238 is a single pivot-and-kick attack: its body orbits the pivot
# foot by 0.24 m and its trail leg swings 0.5 m high; looped and foot-locked, its feet still slid (0.35 m/s median in
# stance) and the orbit sent the blades along their own length (edge cos down to 0.4). So the feet are AUTHORED here, with
# IK, as the dispatch's fallback allows -- a PADDLE TURN, the dancer's way to turn on the spot:
#   the PIVOT foot (his left, the side he turns to) stands under his hips, its ball pinned on the spin axis, the foot
#            turning on the ball with the body -- "pivot on the lead foot"
#   the PADDLE foot (his right) steps round him --steps times a revolution: it lands --rel-land deg off his forward at
#            --r-paddle m out, stays PLANTED (ball pinned) for --plant of the step while the body turns past it, then
#            lifts --step-h m and swings round to the next landing -- "the trail foot stepping around"
#   the stance is low: the hips --drop m below the reference stance's, bobbing --bob m with each paddle step
# THE REST OF THE BODY turns uniformly about the vertical through his hips, one revolution per cycle, counter-clockwise:
#   the torso LEADS the hips by --lead deg (+/- --lead-amp), spread up the spine
#   the ARMS: the double baseball swing (scripts/j_whirl_pose.py --baseball 0: both blades level, side by side, out along
#            the chest's forward, edges along the CCW tangent), turned with the chest's yaw plus a WHIP of --whip deg:
#            they trail the chest, then swing through it, once a revolution
#   the HEAD spots the travel bearing (his forward): counter-turning the spin within --neck deg of the chest, then
#            snapping round over --snap-keys keys to the other side (scripts/j_whirl2.py's schedule)
# Everything is a function of the phase with period one cycle, so the last key IS the first: the loop closes exactly.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, POSE, OUT = a[:3]
opt = lambda k, d=None: float(a[a.index(k) + 1]) if k in a else d
T = opt('--T', 1.0); N = int(round(T * 30)); T = N / 30.0
NS = int(opt('--steps', 3)); PLANT = opt('--plant', 0.55); RP = opt('--r-paddle', 0.52); REL = math.radians(opt('--rel-land', -65))
HSTEP = opt('--step-h', 0.10); DROP = opt('--drop', 0.10); BOB = opt('--bob', 0.02)
LEAD0 = math.radians(opt('--lead', 15)); LEADA = math.radians(opt('--lead-amp', 5)); WHIP = math.radians(opt('--whip', 20))
WHIPF = math.radians(opt('--whip-ahead', 8))      # the arms may swing AHEAD of the chest only this far: further, the sword's
                                                    # pommel ran into his body (40 of 1254 sampled vertices at +20 deg)
NECK = math.radians(opt('--neck', 80)); SNAPK = int(opt('--snap-keys', 3)); HSH = opt('--head-share', 0.6)
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


def ik_leg(Rw, hp, B, toe_target):
    G = fk(Rw, hp)
    off = G[B['toe']][:3, 3] - G[B['foot']][:3, 3]; A = toe_target - off
    H, K, Fp = G[B['up']][:3, 3], G[B['leg']][:3, 3], G[B['foot']][:3, 3]
    l1, l2 = np.linalg.norm(K - H), np.linalg.norm(Fp - K)
    dv = A - H; d = float(np.linalg.norm(dv)); u = dv / d; reach = d
    d = min(max(d, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    n = (K - H) - ((K - H) @ u) * u; n = n / np.linalg.norm(n)
    aa = (l1 * l1 - l2 * l2 + d * d) / (2 * d); hh = math.sqrt(max(l1 * l1 - aa * aa, 0.0))
    Kn = H + aa * u + hh * n; An = H + d * u
    R1 = rmin(K - H, Kn - H); Rw[B['up']] = R1 @ Rw[B['up']]
    R2 = rmin(R1 @ (Fp - K), An - Kn); Rw[B['leg']] = R2 @ (R1 @ Rw[B['leg']])
    return Rw, reach / (l1 + l2)


ss = lambda x: x * x * (3 - 2 * x)
keys = np.arange(N + 1) / N
rows, POSES = [], []
for k in range(N + 1):
    p = keys[k] % 1.0; psi = 2 * math.pi * p
    lead = LEAD0 + LEADA * math.sin(2 * math.pi * p)
    Rw = {}
    for i in SKIN:
        Rw[i] = Ry(psi + SPREAD.get(i, 0.0) * lead) @ REFR[i]
    sw_ = math.sin(2 * math.pi * p); whip = (WHIP if sw_ < 0 else WHIPF) * sw_
    for i in ARMS:
        Rw[i] = Ry(psi + lead + whip + (chest_ref - chest_ref)) @ REFR[i]
    hp = np.array([0.0, hp_ref[1] - DROP + BOB * math.cos(2 * math.pi * NS * p), 0.0])
    # the pivot foot: its ball on the axis, the foot turning on it with the body
    Rw[LEG['Left']['foot']] = Ry(psi) @ REFR[LEG['Left']['foot']]
    Rw[LEG['Left']['toe']] = Ry(psi) @ REFR[LEG['Left']['toe']]
    Rw, rl = ik_leg(Rw, hp, LEG['Left'], np.array([0.0, ball_y['Left'], 0.0]))
    # the paddle foot: step i lands at phase i / NS, planted for PLANT of the step, then swings to the next landing
    q = p * NS; i = int(math.floor(q)) % NS; f = q - math.floor(q)
    land = 2 * math.pi * i / NS
    if f < PLANT:
        ang, yawf, lift, mode = land + REL, land, 0.0, 'planted'
    else:
        u = ss((f - PLANT) / (1 - PLANT)); nxt = land + 2 * math.pi / NS
        ang, yawf, lift, mode = land + REL + u * (nxt - land), land + u * (nxt - land), HSTEP * math.sin(math.pi * u), 'swing'
    tgt = np.array([RP * math.sin(ang), ball_y['Right'] + lift, RP * math.cos(ang)])
    Rw[LEG['Right']['foot']] = Ry(yawf) @ REFR[LEG['Right']['foot']]
    Rw[LEG['Right']['toe']] = Ry(yawf) @ REFR[LEG['Right']['toe']]
    Rw, rr = ik_leg(Rw, hp, LEG['Right'], tgt)
    rows.append(dict(k=k, p=round(p, 4), mode=mode, pivot_reach=round(rl, 3), paddle_reach=round(rr, 3)))
    POSES.append((Rw, hp))
# THE HEAD spots his forward
rel = []
for k in range(N + 1):
    chest = yaw_of(POSES[k][0][S2]); rel.append(max(-NECK, min(NECK, (0.0 - chest + math.pi) % (2 * math.pi) - math.pi)))
for k in range(1, N + 1):
    if rel[k - 1] <= -NECK + 1e-6 and rel[k] >= NECK - 1e-6:
        for s_ in range(SNAPK):
            rel[(k - SNAPK // 2 + s_) % N] = -NECK + 2 * NECK * (s_ + 1) / (SNAPK + 1)
rel[N] = rel[0]
head_err = []
for k in range(N + 1):
    Rw = POSES[k][0]
    cur = (yaw_of(Rw[HEAD]) - yaw_of(Rw[S2]) + math.pi) % (2 * math.pi) - math.pi
    dl = rel[k] - cur
    Rw[NECKB] = Ry((1 - HSH) * dl) @ Rw[NECKB]; Rw[HEAD] = Ry(dl) @ Rw[HEAD]
    head_err.append(math.degrees((yaw_of(Rw[HEAD]) + math.pi) % (2 * math.pi) - math.pi))
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
he = np.array(head_err[:-1])
rep = dict(method="authored paddle turn (IK feet) + the baseball swing (solved arms) + head spotting; see the header",
           cycle=dict(T=T, keys=N + 1, fps=30, revolution="one, counter-clockwise (his left)"),
           params=dict(steps=NS, plant=PLANT, r_paddle_m=RP, rel_land_deg=math.degrees(REL), step_h_m=HSTEP, drop_m=DROP, bob_m=BOB,
                       lead_deg=math.degrees(LEAD0), lead_amp_deg=math.degrees(LEADA), whip_trail_deg=math.degrees(WHIP), whip_ahead_deg=math.degrees(WHIPF),
                       neck_deg=math.degrees(NECK), snap_keys=SNAPK, head_share=HSH),
           pose=os.path.basename(POSE), keys=rows,
           head=dict(within_10_share=round(float(np.mean(np.abs(he) <= 10)), 3), within_30_share=round(float(np.mean(np.abs(he) <= 30)), 3),
                     worst_deg=round(float(np.abs(he).max()), 1)),
           leg_reach_max=dict(pivot=max(r['pivot_reach'] for r in rows), paddle=max(r['paddle_reach'] for r in rows)))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('cycle', 'head', 'leg_reach_max')}))
