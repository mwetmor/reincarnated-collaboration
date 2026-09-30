# WHIRLWIND v2 (Matt, 2026-09-30, relayed by the conductor): "a double baseball swing with a battle/baseball stance and
# good footwork to show a real spin. It's all in the feet ... The head should follow the direction of travel while
# channeling the skill." v1 turned ONE constant pose on a turntable (its feet slid at 5.3-5.6 m/s: they circled); this
# builds the spin from a library clip's own feet.
#
#   python3 scripts/j_whirl2.py <src body.glb> <src clip> <pose.json> <into body.glb> <out.glb>
#        [--T 0.8] [--whip 12] [--neck 80] [--snap-keys 3] [--head-share 0.6] [--hips-keep 0.5] [--hips-drop 0.05]
#        [--stance-cm 3.5] [--feather 2] [--json f]
#
# THE BODY: Meshy "Axe Spin Attack" (238, fetched on his rig): its one full revolution grafted (55_clip_graft, window
# 0.167..2.033 s -- the hips turn 356 deg there and both feet come back to their stance). Per key, in WORLD space:
#   MIRRORED left for right across his sagittal plane -- the library turns clockwise and his whirlwind turns counter-
#            clockwise (Matt 2026-09-21): each joint's rotation AWAY FROM REST, dW = R_world . R_rest^-1, becomes M dW M
#            on the mirrored joint (M = diag(-1, 1, 1)), the hips' position M p -- the graft's own retarget idea
#   RE-TIMED so the hips turn UNIFORMLY: phase p plays the source where its hips had turned the share p of the total
#            (the accumulated yaw, made monotone, inverted) -- ONE revolution per cycle, the footwork where the source
#            put it against the turn
#   CLOSED  in the spin-free frame (the uniform turn R_y(360 p) taken out): each upper-body joint's residual at the
#            end against the start, and each FOOT's, is spread linearly over the cycle -- the pivot foot so gains the
#            few tens of degrees it turned short, pivoting on its ball -- and so is the hips' position
#   LOWERED  the stance: the hips' rise and fall kept at --hips-keep of the source's about its mean, then --hips-drop
#            lower (the knees bend: a batting stance, weight low)
#   FEET LOCKED: wherever a toe is within --stance-cm of its lowest it is PLANTED -- its toe joint (the ball) pinned where
#            it stood at the middle of that stance, the ankle placed by that pin and the foot's own orientation, and the
#            thigh and shin solved to it (two-bone IK, the knee in the source's own plane); --feather keys either side
#            ease in and out. A stance that wraps the cycle's seam has ONE pin, so the loop closes on planted feet
# THE ARMS: the double baseball swing -- scripts/j_whirl_pose.py --baseball 0 solved both blades level, side by side,
# pointing out along the chest's forward, the edges along the CCW tangent. Per key the eight arm bones take that pose's
# WORLD orientation turned by the chest's yaw (only its yaw: the blades stay level while the torso pitches and leans)
# plus a WHIP: the arms trail the chest by up to --whip deg and swing through it once a revolution.
# THE HEAD SPOTS THE TRAVEL BEARING (his forward, the cell's direction): its yaw relative to the chest counter-turns the
# spin so the face holds the bearing, up to the neck's --neck limit; then it snaps round over --snap-keys keys to the
# other limit and holds the bearing again. neck takes (1 - share) of the turn, Head the rest.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export'); C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]
SRC, SCLIP, POSE, INTO, OUT = a[:5]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
T = float(opt('--T', '0.8')); N = int(round(T * 30)); T = N / 30.0
WHIP = math.radians(float(opt('--whip', '12'))); NECK = float(opt('--neck', '80')); SNAPK = int(opt('--snap-keys', '3'))
HSH = float(opt('--head-share', '0.6')); HKEEP = float(opt('--hips-keep', '0.5')); HDROP = float(opt('--hips-drop', '0.05'))
STCM = float(opt('--stance-cm', '3.5')) / 100.0; FEATH = int(opt('--feather', '2'))
SWKEEP = float(opt('--swing-keep', '0.4')); EDGE_IT = int(opt('--edge-iters', '3'))
M = np.diag([-1.0, 1.0, 1.0])
m = C.model(SRC); nid = m['nid']; P = m['parent']; names = [nd.get('name') for nd in m['nodes']]


def Ry(t):
    c, s = math.cos(t), math.sin(t); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def nrm(X):
    return X / np.linalg.norm(X, axis=0)


def yaw_of(R):
    f = R @ np.array([0.0, 0, 1]); return math.atan2(f[0], f[2])


def rv_log(R):
    c = max(-1.0, min(1.0, (np.trace(R) - 1) / 2)); ang = math.acos(c)
    if ang < 1e-9: return np.zeros(3)
    if ang > math.pi - 1e-6:
        w, V = np.linalg.eigh(R + R.T); ax = V[:, np.argmax(w)]; return ax * ang
    return np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * math.sin(ang)) * ang


def rv_exp(v):
    ang = float(np.linalg.norm(v)); return np.eye(3) if ang < 1e-12 else W.axis_angle(v / ang, ang)


def rmin(u, v):                                    # the smallest rotation taking direction u to direction v
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v); ax = np.cross(u, v); s = np.linalg.norm(ax); c = float(u @ v)
    if s < 1e-9: return np.eye(3)
    return W.axis_angle(ax / s, math.atan2(s, c))


def L4(t, R, s):
    X = np.eye(4); X[:3, :3] = R * s; X[:3, 3] = t; return X


GR = {}
def grest(i):
    if i in GR: return GR[i]
    tr, q, s = m['rest'][i]; X = L4(tr, W.q2m(q), s)
    GR[i] = X if P.get(i) is None else grest(P[i]) @ X
    return GR[i]
for i in range(len(m['nodes'])): grest(i)
anim = m['anims'][SCLIP]
AJ = sorted({n for (n, p) in anim if p == 'rotation'})
mir = {j: nid.get(names[j].replace('Left', '#').replace('Right', 'Left').replace('#', 'Right'), j) for j in AJ}
tsrc = np.unique(np.round(np.concatenate([v[0] for v in anim.values()]), 6))
order = []
def visit(i):
    if i in order: return
    if P.get(i) is not None: visit(P[i])
    order.append(i)
for i in range(len(m['nodes'])): visit(i)
HIPS = nid['Hips']
SIDES = {s: dict(up=nid[s + 'UpLeg'], leg=nid[s + 'Leg'], foot=nid[s + 'Foot'], toe=nid[s + 'ToeBase']) for s in ('Left', 'Right')}
LEGBONES = {SIDES[s][b] for s in SIDES for b in ('up', 'leg')}
FEETB = {SIDES[s]['foot'] for s in SIDES}


def lat_yaw(G):
    ax = G[nid['LeftUpLeg']][:3, 3] - G[nid['RightUpLeg']][:3, 3]; return math.atan2(ax[0], ax[2])


psi, prev, acc = [], None, 0.0
for t in tsrc:
    y = -lat_yaw(C.globals_at(m, SCLIP, float(t)))
    if prev is not None: acc += (y - prev + math.pi) % (2 * math.pi) - math.pi
    prev = y; psi.append(acc)
psi = np.array(psi) - psi[0]; tot = psi[-1]; psim = np.maximum.accumulate(psi)
if tot < math.radians(340):
    sys.exit("the source window turns %.1f deg after mirroring, not one counter-clockwise revolution" % math.degrees(tot))


def warp(p):
    target = p * psim[-1]
    k = int(np.searchsorted(psim, target, side='left')); k = min(max(k, 1), len(tsrc) - 1)
    a0, a1 = psim[k - 1], psim[k]; u = 0.0 if a1 <= a0 else (target - a0) / (a1 - a0)
    return float(tsrc[k - 1] + u * (tsrc[k] - tsrc[k - 1]))


keys = np.arange(N + 1) / N
spin = [Ry(2 * math.pi * p) for p in keys]
RAW, HP = [], []
for p in keys:
    G = C.globals_at(m, SCLIP, warp(p)); D = {}
    for j in AJ:
        D[mir[j]] = M @ (nrm(G[j][:3, :3]) @ nrm(GR[j][:3, :3]).T) @ M @ nrm(GR[mir[j]][:3, :3])
    RAW.append(D); HP.append(M @ G[HIPS][:3, 3])
# CLOSURE in the spin-free frame: every joint but the thighs and shins (the feet solve those), and the hips' position
closure_deg = {}
for j in AJ:
    if j in LEGBONES: continue
    Q0, QN = spin[0].T @ RAW[0][j], spin[N].T @ RAW[N][j]
    Cj = rv_log(QN.T @ Q0); closure_deg[names[j]] = round(math.degrees(float(np.linalg.norm(Cj))), 2)
    for k in range(N + 1):
        RAW[k][j] = spin[k] @ ((spin[k].T @ RAW[k][j]) @ rv_exp(Cj * keys[k]))
Hs = [spin[k].T @ HP[k] for k in range(N + 1)]; dH = Hs[0] - Hs[N]; closure_hips_m = float(np.linalg.norm(dH))
HP = [spin[k] @ (Hs[k] + dH * keys[k]) for k in range(N + 1)]
cen = np.mean(HP[:-1], axis=0); cen[1] = 0.0
ym = float(np.mean([h[1] for h in HP[:-1]]))
HP = [np.array([h[0] - cen[0], ym + HKEEP * (h[1] - ym) - HDROP, h[2] - cen[2]]) for h in HP]


def fk(Rw, hp):                                    # 4x4 globals from world rotations (+ rest locals for the rest)
    G = {}
    for i in order:
        tr, q, s = m['rest'][i]
        Rl = W.q2m(q)
        if i in Rw:
            Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
            Rl = Rp.T @ Rw[i]
        if i == HIPS:
            Gp = G[P[i]]; tr = (np.linalg.inv(Gp) @ np.append(hp, 1.0))[:3]
        X = L4(tr, Rl, s)
        G[i] = X if P.get(i) is None else G[P[i]] @ X
    return G


# FEET: stance by the toe's height, one pin per stance (a stance across the seam is one), IK to the pins
G0s = [fk(RAW[k], HP[k]) for k in range(N + 1)]
plan = {}
for s, B in SIDES.items():
    ty = np.array([G0s[k][B['toe']][1, 3] for k in range(N)]); lo = ty.min()
    st = ty <= lo + STCM
    runs, k = [], 0
    if st.all():
        runs = [list(range(N))]
    else:
        start = int(np.argmin(st))                 # a swing key: walk the circle from there
        cur = []
        for d in range(1, N + 1):
            kk = (start + d) % N
            if st[kk]: cur.append(kk)
            elif cur: runs.append(cur); cur = []
        if cur: runs.append(cur)
    pins = []
    for r in runs:
        mid = r[len(r) // 2]; tp = G0s[mid][B['toe']][:3, 3].copy(); tp[1] = float(min(ty[x] for x in r))
        pins.append(dict(keys=r, pin=tp))
    plan[s] = dict(lowest=float(lo), stance_keys=int(st.sum()), pins=pins)


def ik_leg(Rw, hp, B, toe_target):
    G = fk(Rw, hp)
    off = G[B['toe']][:3, 3] - G[B['foot']][:3, 3]
    A = toe_target - off
    H, K = G[B['up']][:3, 3], G[B['leg']][:3, 3]; Fp = G[B['foot']][:3, 3]
    l1, l2 = np.linalg.norm(K - H), np.linalg.norm(Fp - K)
    dv = A - H; d = float(np.linalg.norm(dv)); u = dv / d
    d = min(max(d, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    n = (K - H) - ((K - H) @ u) * u
    n = n / np.linalg.norm(n) if np.linalg.norm(n) > 1e-6 else np.array([0.0, 0, 1])
    aa = (l1 * l1 - l2 * l2 + d * d) / (2 * d); hh = math.sqrt(max(l1 * l1 - aa * aa, 0.0))
    Kn = H + aa * u + hh * n; An = H + d * u
    R1 = rmin(K - H, Kn - H); Rw[B['up']] = R1 @ Rw[B['up']]
    Rleg_now = R1 @ Rw[B['leg']]
    R2 = rmin(R1 @ (Fp - K), An - Kn); Rw[B['leg']] = R2 @ Rleg_now
    return Rw


def toe_target(k, s, B):
    # the toe's target at key k: its PIN in stance; eased from the pin over FEATH keys; in the swing the source's own toe
    # path with its height above the stance kept at SWKEEP (a step round, not a kick)
    kk = k % N; lo = plan[s]['lowest']
    raw = G0s[kk][B['toe']][:3, 3].copy()
    sw = raw.copy(); sw[1] = lo + SWKEEP * (raw[1] - lo)
    best = None
    for pin in plan[s]['pins']:
        ks = pin['keys']
        if kk in ks: return pin['pin'], 'stance'
        dist = min(min((kk - x) % N, (x - kk) % N) for x in ks)
        if dist <= FEATH and (best is None or dist < best[0]):
            ek = min(ks, key=lambda x: min((kk - x) % N, (x - kk) % N))
            best = (dist, pin['pin'] - G0s[ek][B['toe']][:3, 3])
    if best is not None:
        return sw + best[1] * (1 - best[0] / (FEATH + 1)), 'feather'
    return sw, 'swing'


foot_mode = {s: [] for s in SIDES}
for k in range(N + 1):
    for s, B in SIDES.items():
        tgt, mode = toe_target(k, s, B)
        RAW[k] = ik_leg(RAW[k], HP[k], B, tgt); foot_mode[s].append(mode)

# THE ARMS
pz = json.load(open(POSE))['locals']
GP = {}
def gpose(i):
    if i in GP: return GP[i]
    nd = pz.get(names[i]); tr, q, s = (np.array(nd['t']), np.array(nd['r']), np.array(nd['s'])) if nd else m['rest'][i]
    X = L4(tr, W.q2m(q), s); GP[i] = X if P.get(i) is None else gpose(P[i]) @ X
    return GP[i]
for i in range(len(m['nodes'])): gpose(i)
ARMS = [nid[b] for b in ("RightShoulder", "RightArm", "RightForeArm", "RightHand", "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand")]
s02, neck, head = nid['Spine02'], nid['neck'], nid['Head']
chest_ref = yaw_of(nrm(GP[s02][:3, :3])); ARM_REF = {i: nrm(GP[i][:3, :3]) for i in ARMS}
lim = math.radians(NECK); rel = []
SIDE_ARMS = {'r': ARMS[:4], 'l': ARMS[4:]}
WEAP = {'r': (nid['weapon_r'], 0.7768), 'l': (nid['weapon_l'], 0.8089)}
chest_k = [yaw_of(RAW[k][s02]) for k in range(N + 1)]
corr = {sd: np.zeros(N + 1) for sd in SIDE_ARMS}


def set_arms():
    for k in range(N + 1):
        whip = WHIP * math.sin(2 * math.pi * keys[k])
        for sd, bones in SIDE_ARMS.items():
            for i in bones:
                RAW[k][i] = Ry(chest_k[k] - chest_ref + whip + corr[sd][k]) @ ARM_REF[i]


edge_log = []
for it in range(EDGE_IT + 1):
    set_arms()
    if it == EDGE_IT: break
    # the EDGES LEAD: per key, turn each arm set about the vertical so its blade stands square to its tip's travel
    # (the body orbits its pivot foot, so "radial from the chest" is not radial from the turn); a few passes, smoothed
    Gk = [fk(RAW[k], HP[k]) for k in range(N)]
    for sd, (wj, Lt) in WEAP.items():
        tips = np.array([Gk[k][wj][:3, 3] + Lt * nrm(Gk[k][wj][:3, :3])[:, 1] for k in range(N)])
        dk = np.zeros(N); worst = 0.0
        for k in range(N):
            v = (tips[(k + 1) % N] - tips[(k - 1) % N]) * (N / (2 * T))
            Y = nrm(Gk[k][wj][:3, :3])[:, 1]; Yh = Y.copy(); Yh[1] = 0; Yh /= np.linalg.norm(Yh)
            t = np.cross(np.array([0.0, 1, 0]), Yh)
            vr, vt = float(v @ Yh), float(v @ t)
            dk[k] = math.atan2(-vr, vt); worst = max(worst, abs(dk[k]))
        sm = np.array([(dk[(k - 1) % N] + 2 * dk[k] + dk[(k + 1) % N]) / 4 for k in range(N)])
        corr[sd][:N] += sm; corr[sd][N] = corr[sd][0]
        edge_log.append(dict(iteration=it, side=sd, worst_misalign_deg=round(math.degrees(worst), 1)))
for k in range(N + 1):
    rel.append(max(-lim, min(lim, (0.0 - chest_k[k] + math.pi) % (2 * math.pi) - math.pi)))
for k in range(1, N + 1):
    if rel[k - 1] <= -lim + 1e-6 and rel[k] >= lim - 1e-6:
        for s_ in range(SNAPK):
            rel[(k - SNAPK // 2 + s_) % N] = -lim + 2 * lim * (s_ + 1) / (SNAPK + 1)
rel[N] = rel[0]
head_err = []
for k in range(N + 1):
    cur = (yaw_of(RAW[k][head]) - yaw_of(RAW[k][s02]) + math.pi) % (2 * math.pi) - math.pi
    dl = rel[k] - cur
    RAW[k][neck] = Ry((1 - HSH) * dl) @ RAW[k][neck]; RAW[k][head] = Ry(dl) @ RAW[k][head]
    head_err.append(math.degrees((yaw_of(RAW[k][head]) + math.pi) % (2 * math.pi) - math.pi))

# locals, the last key = the first, continuous for slerp
LOC, HL = [], []
for k in range(N + 1):
    G = fk(RAW[k], HP[k]); Lq = {}
    for i in AJ:
        Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
        Lq[i] = np.array(W.m2q(Rp.T @ RAW[k][i]), float)
    LOC.append(Lq); HL.append((np.linalg.inv(G[P[HIPS]]) @ np.append(HP[k], 1.0))[:3])
for i in AJ:
    LOC[N][i] = LOC[0][i].copy()
    for k in range(1, N + 1):
        if np.dot(LOC[k][i], LOC[k - 1][i]) < 0: LOC[k][i] = -LOC[k][i]
HL[N] = HL[0].copy()

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
ti = accs((keys * T).reshape(-1, 1), 'SCALAR', True)
samplers, channels = [], []
for i in AJ:
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
rep = dict(source=dict(file=os.path.basename(SRC), clip=SCLIP, turn_deg_after_mirror=round(math.degrees(tot), 2), window_s=[float(tsrc[0]), float(tsrc[-1])]),
           cycle=dict(T=T, keys=N + 1, fps=30, revolution="one, counter-clockwise (his left)"),
           closure=dict(hips_m_spread=round(closure_hips_m, 4), joints_deg_spread=closure_deg), centred_by_m=[round(float(v), 4) for v in cen],
           hips=dict(keep=HKEEP, drop_m=HDROP),
           feet={s: dict(stance_keys=v['stance_keys'], pins=[dict(keys=[int(x) for x in q['keys']], pin=[round(float(c), 4) for c in q['pin']]) for q in v['pins']]) for s, v in plan.items()},
           stance_rule_cm=STCM * 100, feather_keys=FEATH,
           arms=dict(pose=os.path.basename(POSE), whip_deg=round(math.degrees(WHIP), 1), edge_alignment=edge_log,
                     yaw_correction_deg={sd: [round(math.degrees(x), 1) for x in corr[sd][:N]] for sd in corr}),
           swing_keep=SWKEEP, foot_modes=foot_mode,
           head=dict(neck_limit_deg=NECK, snap_keys=SNAPK, share_head=HSH, yaw_err_deg_by_key=[round(x, 1) for x in head_err[:-1]]))
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print(json.dumps({k: rep[k] for k in ('source', 'cycle', 'centred_by_m', 'feet')}))
