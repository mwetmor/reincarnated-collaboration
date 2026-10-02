# so_mx R-C9-134 COPY of nb_join/scripts/j_weapon_clamp.py, patched: (1) only the weapons passed are clamped (--sword
# alone clamps weapon_r: the orb staff; the shield on weapon_l is left as mounted); (2) --hz H clamps on a uniform H Hz grid
# over the clip (the keys written at that grid), so penetration BETWEEN the clip's 30 fps keys is measured and fixed;
# (3) under_battlemage joins the body morphs (the gown is worn); (4) j_blend from nb_join/scripts.
# THE DEATH'S WEAPON CLAMP (the conductor's ruling on the death look call, 2026-09-30): with both guards blended OUT
# across the fall his arms go slack with the library motion, and the weapons -- rigid in his fists -- go wherever the
# hands take them: through the floor (the sword 0.61 m under it) and through him. So each weapon PIVOTS IN ITS GRIP,
# per key, by the SMALLEST turn that puts it clear: its lowest point on or above the floor (y = 0) and no sampled vertex
# inside his posed body. A weapon that is already clear is not touched. The turns are then smoothed over time and keyed
# as weapon_r / weapon_l ROTATION tracks in the death clip (the grip stays in the fist: translation is the mount's), so
# the last frame reads as a dead man with his weapons fallen beside his hands.
#
#   blender -b -noaudio --python scripts/j_weapon_clamp.py -- <body.glb> <out.glb> <layers.json> --state death
#        --sword sword.glb --axe axe_l.glb [--clip death] [--json f] [--sample-every E: every Eth weapon vertex is tested
#        against his body -- 4 is j_measure.py's own stride; the default, about 300 per weapon, can miss a thin graze]
#
# The pose is the SHIPPED binding's (the glTF rule, as j_measure.py): the clip, then the layers the state names at
# weight x weight_curve(t) (slerp), un-keyed channels at rest, pieces placed by their own IBMs. Blender is used only for
# the BVH. The search: 1200 blade directions (a Fibonacci sphere); for each, the minimal rotation from the current blade
# onto it about the grip; valid = lowest point >= 0 and 0 of ~300 sampled vertices inside the body; the valid direction
# nearest the current one AND the previous key's choice wins (a smoothness term), else the one with the least inside.
import json, math, os, struct, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("so21_weapon_clamp.py")][0]))
RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(RUNS, 'nb_join', 'scripts')); B = __import__('j_blend')
a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUT, LAYJ = a[0], a[1], a[2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
STATE = opt('--state', 'death'); CLIP = opt('--clip', 'death'); OUTJ = opt('--json')
# --floor-tol m: how far below y 0 a clamped weapon's lowest vertex may sit (first runs: 0.002, contact within 2 mm);
# the conductor's ruling reads 'penetration into the floor (0)', so the shipped clamp runs at 0
FTOL = float(opt('--floor-tol', '0.002'))
LAYERS = [ly for ly in json.load(open(LAYJ)) if STATE in ly.get('states', [])]
MORPHS = dict(grip_R=1.0, grip_L=1.0, helmet_on=1.0, under_battlemage=1.0)

js, b0 = L.load_glb(BODY); bn = bytearray(b0)
nodes = js['nodes']; nid = {n.get('name'): i for i, n in enumerate(nodes)}
parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
rest = {i: (np.array(n.get('translation', [0, 0, 0]), float), np.array(n.get('rotation', [0, 0, 0, 1]), float),
            np.array(n.get('scale', [1, 1, 1]), float)) for i, n in enumerate(nodes)}
anims = {}
for an in js['animations']:
    ch = {}
    for c in an['channels']:
        s = an['samplers'][c['sampler']]
        ch[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, bn, s['input'])[:, 0].astype(float),
                                                          L.read_accessor(js, bn, s['output']).astype(float))
    anims[an['name']] = ch


def samp(tt, vv, t, path):
    if len(tt) == 1 or t <= tt[0]: return vv[0]
    if t >= tt[-1]: return vv[-1]
    k = int(np.searchsorted(tt, t, side='right')) - 1; u = (t - tt[k]) / max(tt[k + 1] - tt[k], 1e-12)
    v0, v1 = vv[k], vv[k + 1]
    if path == 'rotation': return B.slerp(v0, v1, u)                        # glTF LINEAR rotation = slerp
    return (1 - u) * v0 + u * v1


def slerp(p, q, u):
    p = p / np.linalg.norm(p); q = q / np.linalg.norm(q); d = float(np.dot(p, q))
    if d < 0: q = -q; d = -d
    if d > 0.9995: v = p + u * (q - p); return v / np.linalg.norm(v)
    th = math.acos(d); return (math.sin((1 - u) * th) * p + math.sin(u * th) * q) / math.sin(th)


def curve(ly, t):
    if 'weight_curve' not in ly: return 1.0
    ks = ly['weight_curve']['keys']
    if t <= ks[0][0]: return float(ks[0][1])
    for i in range(1, len(ks)):
        if t <= ks[i][0]:
            u = (t - ks[i - 1][0]) / max(ks[i][0] - ks[i - 1][0], 1e-9); u = u * u * (3 - 2 * u)
            return float(ks[i - 1][1] + (ks[i][1] - ks[i - 1][1]) * u)
    return float(ks[-1][1])


def locals_at(clip, t):
    loc = {i: list(rest[i]) for i in range(len(nodes))}
    for (n, p), (tt, vv) in anims[clip].items():
        loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = np.array(samp(tt, vv, t, p), float)
    return loc


def globals_of(loc):
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if parent.get(i) is None else g(parent[i]) @ M
        return G[i]
    for i in range(len(nodes)): g(i)
    return G


def pose_locals(t):
    # the pose the renderer shows: Godot's mixer over the layers (scripts/j_blend.py), not slerp(clip, layer, w)
    loc = locals_at(CLIP, t)
    act = [({nid[bnm] for bnm in ly['bones']}, float(ly.get('weight', 1.0)) * curve(ly, t), locals_at(ly['action'], 0.0)) for ly in LAYERS]
    act = [x for x in act if x[1] > 0]
    return B.blend(lambda i: rest[i], loc, act) if act else loc


# the body mesh (CPU skinning with its morphs) -- as j_measure.py
mnode = next(i for i, nd in enumerate(nodes) if 'mesh' in nd and 'skin' in nd)
sk = js['skins'][nodes[mnode]['skin']]; SJ = sk['joints']
IBM = L.read_accessor(js, bn, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
mesh = js['meshes'][nodes[mnode]['mesh']]; tn = (mesh.get('extras') or {}).get('targetNames', [])
BP, BJ, BW, BT, off = [], [], [], [], 0
for pr in mesh['primitives']:
    at = pr['attributes']; P = L.read_accessor(js, bn, at['POSITION']).astype(float)
    for k, tg in enumerate(pr.get('targets', [])):
        w = MORPHS.get(tn[k] if k < len(tn) else '', 0.0)
        if w and 'POSITION' in tg: P = P + w * L.read_accessor(js, bn, tg['POSITION']).astype(float)
    Jn = L.read_accessor(js, bn, at['JOINTS_0']).astype(int); Wt = L.read_accessor(js, bn, at['WEIGHTS_0']).astype(float)
    BP.append(P); BJ.append(Jn); BW.append(Wt); BT.append(L.read_accessor(js, bn, pr['indices']).astype(np.int64).reshape(-1, 3) + off); off += len(P)
BP = np.concatenate(BP); BJ = np.concatenate(BJ); BW = np.concatenate(BW); BW /= np.maximum(BW.sum(1, keepdims=True), 1e-12)
BT = np.concatenate(BT); BPh = np.hstack([BP, np.ones((len(BP), 1))]); TRIS = [tuple(x) for x in BT.tolist()]
jn = [nodes[j].get('name') for j in SJ]; dom = BJ[np.arange(len(BJ)), np.argmax(BW, axis=1)]
HANDV = {'r': np.nonzero(dom == jn.index('RightHand'))[0], 'l': np.nonzero(dom == jn.index('LeftHand'))[0]}


def skin(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(SJ)]); out = np.zeros((len(BP), 3))
    for c in range(BJ.shape[1]):
        out += BW[:, c:c + 1] * np.einsum('vij,vj->vi', M[BJ[:, c]], BPh)[:, :3]
    return out


def piece(path, bone):
    pj, pb = L.load_glb(path)
    pn = next(i for i, nd in enumerate(pj['nodes']) if 'mesh' in nd and 'skin' in nd)
    psk = pj['skins'][pj['nodes'][pn]['skin']]; names = [pj['nodes'][j].get('name') for j in psk['joints']]
    ibm = L.read_accessor(pj, pb, psk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)[names.index(bone)]
    V = L.read_accessor(pj, pb, pj['meshes'][pj['nodes'][pn]['mesh']]['primitives'][0]['attributes']['POSITION']).astype(float)
    loc = (ibm @ np.hstack([V, np.ones((len(V), 1))]).T).T[:, :3]            # the weapon joint's local frame (its units)
    return dict(bone=bone, local=loc, sample=loc[::int(opt('--sample-every', '0')) or max(1, len(loc) // 300)])


WEAP = {k: piece(opt(f), bn_) for k, f, bn_ in (('r', '--sword', 'weapon_r'), ('l', '--axe', 'weapon_l')) if opt(f)}


def inside(tree, p):
    loc, nrm, fi, dist = tree.find_nearest(Vector(p))
    if loc is None or ((Vector(p) - loc).dot(nrm) > 0 and dist > 1e-4):
        return False
    for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        o = Vector(p); dv = Vector(d); n = 0
        for _ in range(64):
            h = tree.ray_cast(o, dv, 10.0)
            if h[0] is None: break
            n += 1; o = h[0] + dv * 1e-5
        if n % 2 == 0: return False
    return True


def rot_between(u, v):
    u = u / np.linalg.norm(u); v = v / np.linalg.norm(v); c = float(np.clip(u @ v, -1, 1))
    ax = np.cross(u, v); s = float(np.linalg.norm(ax))
    if s < 1e-9: return np.eye(3) if c > 0 else W.axis_angle(np.array([1.0, 0, 0]) if abs(u[0]) < 0.9 else np.array([0, 1.0, 0]), math.pi)
    return W.axis_angle(ax / s, math.atan2(s, c))


def settle(Q, ok, steps=14):
    # the direction grid is ~6 deg coarse, so the first clear grid direction can leave a blade a grid step ABOVE the floor
    # (1.2 cm at the held last frame) or turned further than it must be. Along the chosen turn's own axis: the SMALLEST
    # fraction of the turn that is still clear (bisection; the full turn is clear, so the result always is) -- a blade the
    # floor stops then lies ON it, and the turn is the minimal one on that axis. Returns (Q, the fraction kept).
    ang = math.acos(max(-1, min(1, (np.trace(Q) - 1) / 2)))
    if ang < 1e-6 or ang > 3.1:
        return Q, None
    ax = np.array([Q[2, 1] - Q[1, 2], Q[0, 2] - Q[2, 0], Q[1, 0] - Q[0, 1]]) / (2 * math.sin(ang))
    lo, hi = 0.0, 1.0
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if ok(W.axis_angle(ax, mid * ang)): hi = mid
        else: lo = mid
    return W.axis_angle(ax, hi * ang), round(hi, 4)


def grip_ex(wp, sc):
    # the vertices NOT tested against his body -- j_measure.py's exclusion, exactly, so the clamp and the measure answer
    # the same question: the grip cylinder in the fist (|local y| <= 0.07 m and radial <= 0.06 m). A sphere of 0.07 m
    # about the grip (this script's first rule) tests the cylinder's ends, which sit in his FINGERS -- vertices a finger
    # bone dominates, so the 2 cm hand-vertex rule does not catch them -- and it turned the axe at every key
    ly = wp['sample'][:, 1] * sc; lr = np.hypot(wp['sample'][:, 0], wp['sample'][:, 2]) * sc
    return (np.abs(ly) <= 0.07) & (lr <= 0.06)


N = 1200
gi = np.arange(N) + 0.5; ph = np.arccos(1 - 2 * gi / N); th = math.pi * (1 + 5 ** 0.5) * gi
DIRS = np.stack([np.cos(th) * np.sin(ph), np.cos(ph), np.sin(th) * np.sin(ph)], 1)   # y up
keys = np.unique(np.round(np.concatenate([v[0] for v in anims[CLIP].values()]), 6))
if opt('--hz'):
    keys = np.unique(np.round(np.append(np.arange(0.0, keys[-1], 1.0 / float(opt('--hz'))), keys[-1]), 6))
import hashlib
res = dict(state=STATE, clip=CLIP, body=os.path.basename(BODY), body_sha256=hashlib.sha256(open(BODY, 'rb').read()).hexdigest(), layers_json=LAYJ,
           layers=[ly['name'] for ly in LAYERS], keys=len(keys),
           params=dict(directions=N, tries=int(opt('--tries', '400')), continuity=float(opt('--continuity', '2.0')),
                       rate_deg_per_key=float(opt('--rate', '10')), max_flick_deg=float(opt('--max-flick', '20')), floor_y=0.0, floor_tol_m=FTOL,
                       sample_every=int(opt('--sample-every', '0')) or 'len/300', samples={k: len(v['sample']) for k, v in WEAP.items()}),
           frames=[])
prev = {k: None for k in WEAP}; corr = {k: [] for k in WEAP}
for t in keys:
    loc = pose_locals(float(t)); G = globals_of(loc)
    BV = skin(G); tree = BVHTree.FromPolygons([tuple(v) for v in BV.tolist()], TRIS, all_triangles=True)
    fr = dict(t=round(float(t), 5))
    for k, wp in WEAP.items():
        Gw = G[nid[wp['bone']]]; sc = float(np.linalg.norm(Gw[:3, 0])); R = Gw[:3, :3] / sc; o = Gw[:3, 3]
        P = (R @ (wp['sample'] * sc).T).T + o                                   # world, metres
        low = float(((R @ (wp['local'] * sc).T).T + o)[:, 1].min())
        hv = BV[HANDV[k]]; gx = grip_ex(wp, sc)
        def n_in(Q):
            PP = (Q @ (P - o).T).T + o; n = 0
            for j, p in enumerate(PP):
                if gx[j]: continue                                                     # the grip in the fist
                if np.min(np.sum((hv - p) ** 2, axis=1)) < 0.02 ** 2: continue          # the fist itself
                if inside(tree, p): n += 1
            return n
        def lowest(Q):
            return float(((Q @ (R @ (wp['local'] * sc).T)).T + o)[:, 1].min())
        n0 = n_in(np.eye(3))
        if n0 == 0 and low >= 0.0:
            corr[k].append(np.eye(3)); fr[k] = dict(clamped=False, lowest=round(low, 4), inside=0); prev[k] = R[:, 1]; continue
        Y = R[:, 1]; best = None
        cand = sorted(range(N), key=lambda i: -(float(DIRS[i] @ Y) + (float(opt("--continuity", "2.0")) * float(DIRS[i] @ prev[k]) if prev[k] is not None else 0.0)))
        tried = 0
        for i in cand:
            Q = rot_between(Y, DIRS[i])
            if lowest(Q) < -FTOL: continue
            tried += 1
            n = n_in(Q)
            if best is None or n < best[1]:
                best = (Q, n, i)
            if n == 0 or tried >= int(opt("--tries", "400")): break
        Q, n, i = best if best else (np.eye(3), n0, -1)
        sf = None
        if best is not None and n == 0:
            Q, sf = settle(Q, lambda Qm: lowest(Qm) >= -FTOL and n_in(Qm) == 0)
        corr[k].append(Q); prev[k] = (Q @ Y)
        fr[k] = dict(clamped=True, turn_deg=round(math.degrees(math.acos(max(-1, min(1, (np.trace(Q) - 1) / 2)))), 2),
                     lowest_before=round(low, 4), lowest=round(lowest(Q), 4), inside_before=n0, inside=n, settled=sf)
    res['frames'].append(fr)
    print("[clamp] t %.3f  %s" % (t, {k: fr[k] for k in WEAP}), flush=True)

# SMOOTH the turns over time (a rate-limited envelope, below), then key them: the weapon's local rotation =
# hand^-1 . Q . (hand . mount) -- the corrected world rotation expressed under the hand, the mount's translation kept
def rv_of(Q):
    ang = math.acos(max(-1, min(1, (np.trace(Q) - 1) / 2)))
    if ang < 1e-9: return np.zeros(3)
    ax = np.array([Q[2, 1] - Q[1, 2], Q[0, 2] - Q[2, 0], Q[1, 0] - Q[0, 1]]) / (2 * math.sin(ang)); return ax * ang
def Q_of(v):
    a_ = float(np.linalg.norm(v)); return np.eye(3) if a_ < 1e-12 else W.axis_angle(v / a_, a_)
# SMOOTHING: a rate-limited envelope over the turns (below), then every key re-checked against the floor and his body;
# where the envelope's axis mix gave a violation back, that key keeps its raw turn (listed as `restored`).
def violates(k, Q, t):
    G = globals_of(pose_locals(float(t))); wp = WEAP[k]
    Gw = G[nid[wp['bone']]]; sc = float(np.linalg.norm(Gw[:3, 0])); R = Gw[:3, :3] / sc; o = Gw[:3, 3]
    if float(((Q @ (R @ (wp['local'] * sc).T)).T + o)[:, 1].min()) < -(FTOL + 0.0001): return True
    BV = skin(G); tr = BVHTree.FromPolygons([tuple(v) for v in BV.tolist()], TRIS, all_triangles=True); hv = BV[HANDV[k]]
    P = (Q @ (R @ (wp['sample'] * sc).T)).T + o; gx = grip_ex(wp, sc)
    for j, p in enumerate(P):
        if gx[j] or np.min(np.sum((hv - p) ** 2, axis=1)) < 0.02 ** 2: continue
        if inside(tr, p): return True
    return False
tracks = {}
res['smoothing'] = dict(method='rate-limited envelope: a turn never below what its key requires, never changing faster than rate_deg_per_key per key; a key the envelope leaves violating is re-searched nearest the envelope blade (restored: [t, deg off] taken, or a graze kept when the nearest clear blade is more than max_flick_deg off)', restored={})
for k, wp in WEAP.items():
    V = np.array([rv_of(Q) for Q in corr[k]])
    # a RATE-LIMITED ENVELOPE, not an average: a turn never falls below what a key requires (so no violation is given
    # back), and never changes faster than RATE per key -- an onset becomes a ramp that starts early, as a loosening grip
    RATE = math.radians(float(opt('--rate', '10')))
    mag = np.linalg.norm(V, axis=1); Vs = np.zeros_like(V)
    for i in range(len(V)):
        cand_ = mag - RATE * np.abs(np.arange(len(V)) - i)
        j = int(np.argmax(cand_))
        if cand_[j] > 0 and mag[j] > 0:
            Vs[i] = V[j] / mag[j] * cand_[j]
    restored = []
    for i, t in enumerate(keys):
        # EVERY key the envelope turns is re-checked -- a key the first pass left alone can be turned by its
        # neighbours' ramp (the sword at 1.4333 s was: clear as it stood, 29 vertices inside once the ramp turned it)
        if (np.linalg.norm(V[i]) > 0 or np.linalg.norm(Vs[i]) > 0) and violates(k, Q_of(Vs[i]), t):
            # the envelope's turn is not clear here: search again, ordered by closeness to the ENVELOPE's blade direction: the clear direction nearest to where
            # its neighbours put the blade (restoring the raw turn outright jumped 71 deg in one key)
            G_ = globals_of(pose_locals(float(t))); Gw_ = G_[nid[WEAP[k]['bone']]]; R_ = Gw_[:3, :3] / np.linalg.norm(Gw_[:3, 0]); Y_ = R_[:, 1]
            want = Q_of(Vs[i]) @ Y_
            done_ = False
            for j_ in sorted(range(N), key=lambda j2: -float(DIRS[j2] @ want))[:int(opt('--tries', '400'))]:
                Q_ = rot_between(Y_, DIRS[j_])
                if not violates(k, Q_, t):
                    off_ = math.degrees(math.acos(max(-1, min(1, float(DIRS[j_] @ want)))))
                    if off_ > float(opt('--max-flick', '20')):
                        # the nearest clear blade is far from where its neighbours hold it: taking it would FLICK the blade
                        # that far in one key. A one-key graze reads as nothing at play scale; a flick reads as a twitch.
                        restored.append((round(float(t), 4), 'graze kept: the clear blade is %.1f deg off' % off_)); done_ = True; break
                    # SETTLE back toward the envelope's blade: along the arc from this clear grid direction to `want`,
                    # the nearest point to `want` that is still clear (the grid is ~6 deg coarse)
                    Rarc = rot_between(want, DIRS[j_]); aa = math.acos(max(-1, min(1, (np.trace(Rarc) - 1) / 2)))
                    if 1e-6 < aa < 3.1:
                        axa = np.array([Rarc[2, 1] - Rarc[1, 2], Rarc[0, 2] - Rarc[2, 0], Rarc[1, 0] - Rarc[0, 1]]) / (2 * math.sin(aa))
                        lo_, hi_ = 0.0, 1.0
                        for _ in range(12):
                            mid_ = 0.5 * (lo_ + hi_)
                            if not violates(k, rot_between(Y_, W.axis_angle(axa, mid_ * aa) @ want), t): hi_ = mid_
                            else: lo_ = mid_
                        dset = W.axis_angle(axa, hi_ * aa) @ want; Q_ = rot_between(Y_, dset)
                        off_ = math.degrees(math.acos(max(-1, min(1, float(dset @ want)))))
                    Vs[i] = rv_of(Q_); restored.append((round(float(t), 4), round(off_, 1))); done_ = True; break
            if not done_:
                Vs[i] = V[i]; restored.append((round(float(t), 4), 'raw'))
    res['smoothing']['restored'][k] = restored
    qs = []
    for i, t in enumerate(keys):
        G = globals_of(pose_locals(float(t)))
        hand = G[parent[nid[wp['bone']]]]; Rh = hand[:3, :3] / np.linalg.norm(hand[:3, 0])
        Gw = G[nid[wp['bone']]]; Rw = Gw[:3, :3] / np.linalg.norm(Gw[:3, 0])
        Rl = Rh.T @ Q_of(Vs[i]) @ Rw
        q = np.array(W.m2q(Rl), float)
        if qs and np.dot(q, qs[-1]) < 0: q = -q
        qs.append(q)
    tracks[wp['bone']] = np.array(qs)


def put(data):
    while len(bn) % 4: bn.append(0)
    o_ = len(bn); bn.extend(data); return o_


def acc(arr, typ, mm=False):
    arr = np.ascontiguousarray(arr, np.float32)
    js['bufferViews'].append(dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes))
    ac = dict(bufferView=len(js['bufferViews']) - 1, componentType=5126, count=int(arr.shape[0]), type=typ)
    if mm: ac['min'] = [float(x) for x in np.atleast_1d(arr.min(0))]; ac['max'] = [float(x) for x in np.atleast_1d(arr.max(0))]
    js['accessors'].append(ac); return len(js['accessors']) - 1


an = next(x for x in js['animations'] if x['name'] == CLIP)
ti = acc(keys.reshape(-1, 1), 'SCALAR', True)
an['channels'] = [c for c in an['channels'] if nodes[c['target']['node']].get('name') not in tracks]
for bone, qs in tracks.items():
    an['samplers'].append(dict(input=ti, output=acc(qs, 'VEC4'), interpolation='LINEAR'))
    an['channels'].append(dict(sampler=len(an['samplers']) - 1, target=dict(node=nid[bone], path='rotation')))
while len(bn) % 4: bn.append(0)
js['buffers'][0]['byteLength'] = len(bn)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as f:
    f.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(bn))); f.write(struct.pack('<I4s', len(jb), b'JSON')); f.write(jb)
    f.write(struct.pack('<I4s', len(bn), b'BIN\x00')); f.write(bytes(bn))
res['clamped_keys'] = {k: sum(1 for fr in res['frames'] if fr[k]['clamped']) for k in WEAP}
res['inside_after_max'] = {k: max(fr[k]['inside'] for fr in res['frames']) for k in WEAP}
res['lowest_after_min'] = {k: min(fr[k]['lowest'] for fr in res['frames']) for k in WEAP}
print("[clamp] clamped keys %s; inside after (sampled) max %s; lowest after %s -> %s" % (res['clamped_keys'], res['inside_after_max'], res['lowest_after_min'], OUT))
if OUTJ:
    json.dump(res, open(OUTJ, 'w'), indent=1)
