# THE NORMAL ATTACK, HAND-AUTHORED FROM HIS GUARD (the conductor 2026-10-01, v7 style, 0 credits): named, keyed edits on the
# RIGHT ARM (the sword arm) and the chest only; the off hand holds its guard throughout; no solver.
#
#   python3 scripts/j_attack_auth.py <body.glb> <out.glb> [--name attack_auth] [--json f] [--keys k.json]
#
# THE STANCE: one frame of his battle stance as the body holds it -- idle_guard at 0.5 s with the guard layers at weight 1
# (the guard clips join_guard_R/L_idle in THIS body) -- held for the whole clip; every key starts from it.
# THE EDITS, each a world rotation through the joint, the angle a function of time:
#   shoulder  the upper arm turned about his side-to-side axis (the levelled shoulder line): + raises it forward and up
#             (flexion), - takes it down and back (extension) -- no turn in or out, so the arm stays in its own (right) plane
#   elbow     the forearm about the elbow's hinge (the normal of the upper-arm / forearm plane at the stance): + bends, - opens
#   chest     Spine02 about the same side-to-side axis: + leans the chest forward over the blow, - back
# THE KEYS (deg, t in s; between keys each angle is eased -- the strike ACCELERATES into contact, smoothstep elsewhere):
#   guard 0 -> wind-up (the sword raised up and back over his RIGHT shoulder) -> CONTACT (the arm down and forward, the
#   elbow open, the sword low in front of his right hip) -> follow-through -> back to the guard.
# Contact at 0.30 s of 0.6333 s (47.4%: the packet's tick 7 of 15). The pose is keyed on the 30 fps grid (Godot's bake).
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; BODY, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
NAME = opt('--name', 'attack_auth')
KEYS = json.load(open(opt('--keys'))) if opt('--keys') else [
    dict(t=0.0, shoulder=0, elbow=0, chest=0, ease='smooth'),
    dict(t=0.2, shoulder=150, elbow=35, chest=-8, ease='smooth'),        # wind-up: up and back over the right shoulder
    dict(t=0.3, shoulder=55, elbow=-55, chest=12, ease='in'),            # CONTACT: down and forward, the elbow open
    dict(t=0.3667, shoulder=45, elbow=-60, chest=14, ease='out'),        # follow-through
    dict(t=0.6333, shoulder=0, elbow=0, chest=0, ease='smooth')]         # back to the guard
m = C.model(BODY); nid = m['nid']; P = m['parent']; N = len(m['nodes'])


def locals_of(clip, t):
    loc = {i: [np.array(v, float) for v in m['rest'][i]] for i in range(N)}
    for (n, p), (tt, vv) in m['anims'][clip].items():
        k = int(np.argmin(np.abs(tt - t))); loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = np.array(vv[k], float)
    return loc


base = locals_of('idle_guard', 0.5)
for sd, bones in (('R', ["RightShoulder", "RightArm", "RightForeArm", "RightHand"]), ('L', ["LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand"])):
    g = locals_of('join_guard_%s_idle' % sd, 0.0)
    for b in bones: base[nid[b]] = g[nid[b]]
nrm = lambda X: X / np.linalg.norm(X, axis=0)


def globals_of(loc):
    G = {}
    def gg(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if P.get(i) is None else gg(P[i]) @ M
        return G[i]
    for i in range(N): gg(i)
    return G


def set_world(loc, G, i, R):
    Rp = nrm(G[P[i]][:3, :3]) if P.get(i) is not None else np.eye(3)
    loc[i] = [loc[i][0], np.array(W.m2q(Rp.T @ R), float), loc[i][2]]


G0 = globals_of(base); La, Ra = G0[nid['LeftArm']][:3, 3], G0[nid['RightArm']][:3, 3]; LT = La - Ra; LT[1] = 0; LT /= np.linalg.norm(LT)
sh, el, wr = (G0[nid[b]][:3, 3] for b in ('RightArm', 'RightForeArm', 'RightHand'))
HINGE = np.cross(el - sh, wr - el); HINGE /= np.linalg.norm(HINGE)    # the stance's elbow hinge (in world, carried by the arm)


def pose(sa, ea, ca):
    loc = {i: list(v) for i, v in base.items()}
    G = globals_of(loc); i = nid['Spine02']; set_world(loc, G, i, W.axis_angle(LT, math.radians(ca)) @ nrm(G[i][:3, :3]))
    G = globals_of(loc); i = nid['RightArm']
    Rc = W.axis_angle(LT, math.radians(ca))                             # the chest turn carries the shoulder's axes with it
    set_world(loc, G, i, W.axis_angle(Rc @ LT, -math.radians(sa)) @ nrm(G[i][:3, :3]))   # -angle about +left = forward/up
    G = globals_of(loc); i = nid['RightForeArm']
    hinge = nrm(G[nid['RightArm']][:3, :3]) @ (nrm(G0[nid['RightArm']][:3, :3]).T @ HINGE)
    set_world(loc, G, i, W.axis_angle(hinge, math.radians(ea)) @ nrm(G[i][:3, :3]))
    return loc


def ease(u, kind):
    if kind == 'in': return u * u * u                                   # accelerates into contact
    if kind == 'out': return 1 - (1 - u) ** 2
    return u * u * (3 - 2 * u)


TEND = KEYS[-1]['t']; grid = np.round(np.arange(int(round(TEND * 30)) + 1) / 30.0, 6)   # every 30 fps key, the end included
def angles(t):
    for k in range(1, len(KEYS)):
        if t <= KEYS[k]['t'] + 1e-9:
            a0, a1 = KEYS[k - 1], KEYS[k]; u = ease((t - a0['t']) / (a1['t'] - a0['t']), a1['ease'])
            return [a0[q] + (a1[q] - a0[q]) * u for q in ('shoulder', 'elbow', 'chest')]
    return [KEYS[-1][q] for q in ('shoulder', 'elbow', 'chest')]


SKIN = [i for i in range(N) if m['nodes'][i].get('name') not in ('weapon_r', 'weapon_l') and i in set(m['joints'])]
LOCS = [pose(*angles(float(t))) for t in grid]
js, b0 = L.load_glb(BODY); bn = bytearray(b0)
def put(data):
    while len(bn) % 4: bn.append(0)
    o = len(bn); bn.extend(data); return o
def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(v) for v in np.atleast_1d(arr.min(0))]; ac['max'] = [float(v) for v in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1
ti = acc(grid.reshape(-1, 1), 'SCALAR', True); samplers, channels = [], []
for i in SKIN:
    Q = np.array([LOCS[k][i][1] for k in range(len(grid))], float)
    for k in range(1, len(Q)):
        if Q[k] @ Q[k - 1] < 0: Q[k] = -Q[k]
    samplers.append(dict(input=ti, output=acc(Q, 'VEC4'), interpolation='LINEAR'))
    channels.append(dict(sampler=len(samplers) - 1, target=dict(node=i, path='rotation')))
hips = nid['Hips']
samplers.append(dict(input=ti, output=acc(np.array([LOCS[k][hips][0] for k in range(len(grid))]), 'VEC3'), interpolation='LINEAR'))
channels.append(dict(sampler=len(samplers) - 1, target=dict(node=hips, path='translation')))
js['animations'] = [x for x in js['animations'] if x.get('name') != NAME] + [dict(name=NAME, samplers=samplers, channels=channels)]
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
# the sword tip and the right wrist through the clip (his frame: +X his left, +Z his forward)
mm = C.model(OUT); n2 = mm['nid']; rows = []
for t in grid:
    G = C.globals_at(mm, NAME, float(t)); R = nrm(G[n2['weapon_r']][:3, :3]); tp = G[n2['weapon_r']][:3, 3] + 0.7768 * R[:, 1]
    rows.append(dict(t=round(float(t), 4), tip=[round(float(x), 3) for x in tp], wrist=[round(float(x), 3) for x in G[n2['RightHand']][:3, 3]]))
kc = [k['t'] for k in KEYS].index(0.3) if 0.3 in [k['t'] for k in KEYS] else 2
TEND = float(grid[-1])
rep = dict(clip=NAME, T_s=TEND, keys=len(grid), edits=KEYS, contact=dict(t_s=KEYS[2]['t'], fraction=round(KEYS[2]['t'] / TEND, 3)), path=rows)
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print(json.dumps(dict(clip=NAME, T=TEND, contact=rep['contact'], tip_y=[r['tip'][1] for r in rows], tip_x=[r['tip'][0] for r in rows], tip_z=[r['tip'][2] for r in rows])))
