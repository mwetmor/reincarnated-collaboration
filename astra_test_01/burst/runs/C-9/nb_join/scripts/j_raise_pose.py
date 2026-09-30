# THE SHOUT'S RAISED VARIANT, the pose (the conductor's ruling on the shout look call, 2026-09-30: the genre reads a war
# cry through RAISED weapons -- D2's barbarian cries with his arms up). Both arms SOLVED against the shout's own body at
# the cry's peak (the release), so at the peak the weapons stand high over him; the pose rides the shout as a layer that
# blends in over the cry and out after it (j_manifest.py's layer list). The current (guard) shout stays beside it.
#
#   python3 scripts/j_raise_pose.py <body.glb> <out.json> [--clip shout] [--t 1.2] [--layers layers.json --state shout_raised]
#
# The body at the peak is the clip's pose with the layers BELOW the raise already applied (the guards), so the solve sees
# the chest the render will. Variables: Shoulder, Arm, ForeArm and Hand on each side (rotation deltas on that pose).
#   grip        high: the fist over the top of his head (grip y >= head_end + 0.08 m), out from his centre line
#   blade/haft  up: within 25 deg of vertical, leaning OUT (a V over his head), tip above grip
#   clearance   every blade point >= 0.22 m from his head and >= 0.25 m from the other weapon's
#   wrist       within 50 deg of the pose's own hand; elbow bent 10-70 deg; the clavicle within 35 deg of the pose's
import json, math, os, sys
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIP = opt('--clip', 'shout'); T = float(opt('--t', '1.2'))
LAY = [ly for ly in (json.load(open(opt('--layers'))) if opt('--layers') else []) if opt('--state', 'shout_raised') in ly.get('states', []) and ly['name'] != 'raise']
U = np.array([0.0, 1.0, 0.0])
m = C.model(BODY); nid = m['nid']; P = m['parent']
q_of = lambda R: np.array(W.m2q(R), float)
def rv(v):
    ang = float(np.linalg.norm(v)); return np.eye(3) if ang < 1e-12 else W.axis_angle(v / ang, ang)
def locals_at(clip, t):
    loc = {i: [np.array(m['rest'][i][0], float), np.array(m['rest'][i][1], float), np.array(m['rest'][i][2], float)] for i in range(len(m['nodes']))}
    for (n_, p_), (tt, vv) in m['anims'][clip].items():
        k = int(np.searchsorted(tt, t - 1e-6)); k = min(max(k, 0), len(tt) - 1)
        if 0 < k and tt[k] > t:
            u = (t - tt[k - 1]) / (tt[k] - tt[k - 1]); v0, v1 = vv[k - 1], vv[k]
            if p_ == 'rotation':
                if np.dot(v0, v1) < 0: v1 = -v1
                v = (1 - u) * v0 + u * v1; v = v / np.linalg.norm(v)
            else: v = (1 - u) * v0 + u * v1
        else: v = vv[k]
        loc[n_][{'translation': 0, 'rotation': 1, 'scale': 2}[p_]] = np.array(v, float)
    return loc
loc0 = locals_at(CLIP, T)
for ly in LAY:                                                                   # the layers under the raise (the guards)
    pl = locals_at(ly['action'], 0.0)
    for b in ly['bones']: loc0[nid[b]] = pl[nid[b]]
def globals_of(loc):
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if P.get(i) is None else g(P[i]) @ M
        return G[i]
    for i in range(len(m['nodes'])): g(i)
    return G
unit = lambda v: v / np.linalg.norm(v)
SIDES = {'r': dict(chain=["RightShoulder", "RightArm", "RightForeArm", "RightHand"], weapon="weapon_r", out=np.array([-1.0, 0, 0]), L=0.7768),
         'l': dict(chain=["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"], weapon="weapon_l", out=np.array([1.0, 0, 0]), L=0.8089)}
VARS = [(s, b) for s in ('r', 'l') for b in SIDES[s]['chain']]
q0 = {b: loc0[nid[b]][1].copy() for _, b in VARS}
G0 = globals_of(loc0)
head_top = G0[nid['head_end']][:3, 3]; head = G0[nid['Head']][:3, 3]
hips = G0[nid['Hips']][:3, 3]
def pose_from(x):
    loc = {i: list(v) for i, v in loc0.items()}
    for k, (s, b) in enumerate(VARS):
        loc[nid[b]] = [loc0[nid[b]][0], q_of(W.q2m(q0[b]) @ rv(x[3 * k:3 * k + 3])), loc0[nid[b]][2]]
    return loc
def terms(x):
    G = globals_of(pose_from(x)); out = {}; pts = {}
    for s in ('r', 'l'):
        Gw = G[nid[SIDES[s]['weapon']]]; R = Gw[:3, :3] / np.linalg.norm(Gw[:3, :3], axis=0); g = Gw[:3, 3]; Y = R[:, 1]
        sh = G[nid[SIDES[s]['chain'][1]]][:3, 3]; el = G[nid[SIDES[s]['chain'][2]]][:3, 3]
        elbow = math.degrees(math.acos(max(-1, min(1, float(unit(el - sh) @ unit(g - el))))))
        ki = VARS.index((s, SIDES[s]['chain'][3])); kc = VARS.index((s, SIDES[s]['chain'][0]))
        wrist = math.degrees(float(np.linalg.norm(x[3 * ki:3 * ki + 3]))); clav = math.degrees(float(np.linalg.norm(x[3 * kc:3 * kc + 3])))
        tilt = math.degrees(math.acos(max(-1, min(1, float(Y @ U)))))
        lean_out = float(Y @ SIDES[s]['out'])
        P_ = [g + f * SIDES[s]['L'] * Y for f in (0.15, 0.35, 0.55, 0.75, 1.0)]; pts[s] = P_
        out[s] = dict(grip_over_head=float(g[1] - head_top[1]), side_out=float((g - hips) @ SIDES[s]['out']), tilt=tilt, lean_out=lean_out,
                      elbow=elbow, wrist=wrist, clavicle=clav, clear_head=min(float(np.linalg.norm(p - head)) for p in P_))
    wd = min(float(np.linalg.norm(p - q)) for p in pts['r'] for q in pts['l'])
    for s in out: out[s]['clear_other'] = wd
    return out
def cost(x):
    T_ = terms(x); c = 0.0
    for s, v in T_.items():
        c += 30 * max(0.0, 0.08 - v['grip_over_head']) ** 2 + 10 * max(0.0, 0.20 - v['side_out']) ** 2
        c += 0.02 * max(0.0, v['tilt'] - 25.0) ** 2 + 5 * max(0.0, 0.05 - v['lean_out']) ** 2
        c += 0.02 * max(0.0, v['wrist'] - 50.0) ** 2 + 0.02 * max(0.0, 10.0 - v['elbow']) ** 2 + 0.02 * max(0.0, v['elbow'] - 70.0) ** 2
        c += 0.02 * max(0.0, v['clavicle'] - 35.0) ** 2
        c += 80 * max(0.0, 0.22 - v['clear_head']) ** 2 + 80 * max(0.0, 0.25 - v['clear_other']) ** 2
    return c + 0.01 * float(np.sum(x ** 2))
best = None
for seed in range(16):
    xs = np.zeros(3 * len(VARS)) if seed == 0 else np.random.default_rng(seed).normal(0, 0.7, 3 * len(VARS))
    r_ = minimize(cost, xs, method='L-BFGS-B', options=dict(maxiter=4000))
    if best is None or r_.fun < best.fun: best = r_
Tm = terms(best.x); loc = pose_from(best.x)
rep = dict(clip=CLIP, t=T, under=[ly['name'] for ly in LAY], cost=round(float(best.fun), 5),
           terms={s: {k: round(v, 4) for k, v in d.items()} for s, d in Tm.items()},
           locals={m['nodes'][nid[b]]['name']: dict(r=[float(v) for v in loc[nid[b]][1]]) for _, b in VARS})
json.dump(rep, open(OUT, 'w'), indent=1)
for s, d in Tm.items():
    print("  %s: grip %.2f m over the head, %.2f out; blade %.1f deg off vertical, leaning out %.2f; elbow %.0f wrist %.0f clavicle %.0f; clear head %.2f, other weapon %.2f"
          % (s, d['grip_over_head'], d['side_out'], d['tilt'], d['lean_out'], d['elbow'], d['wrist'], d['clavicle'], d['clear_head'], d['clear_other']))
print("  cost %.4f -> %s" % (best.fun, OUT))
