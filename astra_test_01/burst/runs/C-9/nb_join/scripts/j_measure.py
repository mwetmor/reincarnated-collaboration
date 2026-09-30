# nb_join: the barbarian's JOIN moves MEASURED ON THE SHIPPED BINDING -- the glTF rule, which is Godot's:
# a piece is placed by its OWN inverse bind matrices on the body's joints, and a channel a clip does not key
# sits at its REST. Blender is used ONLY for mathutils' BVH (ray casts); nothing here evaluates a Blender rig,
# because a Blender rig keeps an un-keyed bone at the last action's pose (nb_w2/scripts/w5_measure.py header:
# the sword's edge read 65.74 deg off in idle_guard for exactly that reason).
#
#   blender -b -noaudio --python scripts/j_measure.py -- <body.glb> <out.json> --clips a,b,c [--n 24]
#        [--sword sword.glb] [--axe axe_l.glb] [--morphs grip_R=1,grip_L=1,helmet_on=0]
#        [--layer <clip>=<bone,bone,...>@<pose clip>[:<t>, -1 = the clip's own time]] (repeatable) [--pen-every 4] [--no-pen]
#
# Per clip, per sample time (uniform over [0, T], both ends): for each weapon, the GRIP (the weapon joint's
# origin), its axes X (the flat's normal), Y (blade / haft to the tip) and Z (an edge) in world, the TIP
# (the piece's farthest vertex along +Y), the blade's tilt from vertical; the head, chest and hips joints;
# and PENETRATION: every Nth weapon vertex INSIDE the posed body -- an odd number of crossings along all six
# axis directions (the T12 PEN instrument's rule), after a nearest-surface prune -- the holding fist excluded
# (vertices on the grip, |local y| <= half the grip, and any within 2 cm of a body vertex that hand dominates).
# The body is CPU-skinned in numpy with its morphs (grip_R / grip_L closed by default). World = glTF world,
# metres: +Y up, he faces +Z, his right is -X.
import json, math, os, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath([x for x in sys.argv if x.endswith("j_measure.py")][0]))
RUNS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts"))
sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts"))
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')

a = sys.argv[sys.argv.index('--') + 1:]
BODY, OUT = a[0], a[1]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIPS = [c for c in opt('--clips', '').split(',') if c]
N = int(opt('--n', '24'))
SWORD, AXE = opt('--sword'), opt('--axe')
MORPHS = dict((kv.split('=')[0], float(kv.split('=')[1])) for kv in opt('--morphs', 'grip_R=1,grip_L=1,helmet_on=0').split(','))
EVERY = int(opt('--pen-every', '4'))
NOPEN = '--no-pen' in a
LAYERS = {}                                  # clip -> [layers], applied in order (bottom to top), weight 1
for i, x in enumerate(a):
    if x == '--layer':
        spec = a[i + 1]; clip, rest = spec.split('=', 1); bones, pose = rest.split('@', 1)
        pc, pt = (pose.split(':') + ['0'])[:2]
        LAYERS.setdefault(clip, []).append(dict(bones=bones.split(','), clip=pc, t=float(pt)))


# ---------------------------------------------------------------- the rig: rest, animations, globals
def load(path):
    js, b = L.load_glb(path)
    nodes = js['nodes']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    rest = {i: (np.array(n.get('translation', [0, 0, 0]), float), np.array(n.get('rotation', [0, 0, 0, 1]), float),
                np.array(n.get('scale', [1, 1, 1]), float)) for i, n in enumerate(nodes)}
    anims = {}
    for an in js.get('animations', []):
        ch = {}
        for c in an['channels']:
            s = an['samplers'][c['sampler']]
            ch[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, b, s['input'])[:, 0].astype(float),
                                                              L.read_accessor(js, b, s['output']).astype(float),
                                                              s.get('interpolation', 'LINEAR'))
        anims[an.get('name')] = ch
    return dict(js=js, bin=b, nodes=nodes, parent=parent, rest=rest, anims=anims,
                nid={n.get('name'): i for i, n in enumerate(nodes)})


def samp(tt, vv, interp, t, path):
    if len(tt) == 1 or t <= tt[0]:
        return vv[0]
    if t >= tt[-1]:
        return vv[-1]
    k = int(np.searchsorted(tt, t, side='right')) - 1
    if interp == 'STEP':
        return vv[k]
    u = (t - tt[k]) / max(tt[k + 1] - tt[k], 1e-12); v0, v1 = vv[k], vv[k + 1]
    if path == 'rotation':
        if np.dot(v0, v1) < 0:
            v1 = -v1
        v = (1 - u) * v0 + u * v1
        return v / np.linalg.norm(v)
    return (1 - u) * v0 + u * v1


def locals_at(m, clip, t):
    """every node's local TRS: the clip's keyed channels, REST for everything it does not key (glTF, Godot)"""
    loc = {i: list(m['rest'][i]) for i in range(len(m['nodes']))}
    for (n, p), (tt, vv, ip) in m['anims'][clip].items():
        v = samp(tt, vv, ip, t, p)
        loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = np.array(v, float)
    return loc


def globals_of(m, loc):
    G = {}
    def g(i):
        if i in G:
            return G[i]
        tr, q, s = loc[i]
        M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if m['parent'].get(i) is None else g(m['parent'][i]) @ M
        return G[i]
    for i in range(len(m['nodes'])):
        g(i)
    return G


def pose(m, clip, t):
    loc = locals_at(m, clip, t)
    for ly in LAYERS.get(clip, []):
        pl = locals_at(m, ly['clip'], t if ly['t'] < 0 else ly['t'])      # t < 0: the layer plays at the clip's time
        for bn in ly['bones']:
            loc[m['nid'][bn]] = pl[m['nid'][bn]]
    return globals_of(m, loc)


def clip_len(m, clip):
    return float(max(v[0].max() for v in m['anims'][clip].values()))


# ---------------------------------------------------------------- the body mesh, CPU-skinned with its morphs
body = load(BODY)
js, bb = body['js'], body['bin']
mnode = next(i for i, nd in enumerate(js['nodes']) if 'mesh' in nd and 'skin' in nd)
sk = js['skins'][js['nodes'][mnode]['skin']]
SJ = sk['joints']
IBM = L.read_accessor(js, bb, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
mesh = js['meshes'][js['nodes'][mnode]['mesh']]
tnames = (mesh.get('extras') or {}).get('targetNames', [])
BP, BJ, BW, BT = [], [], [], []
off = 0
for pr in mesh['primitives']:
    at = pr['attributes']
    P = L.read_accessor(js, bb, at['POSITION']).astype(float)
    for k, tg in enumerate(pr.get('targets', [])):
        w = MORPHS.get(tnames[k] if k < len(tnames) else '', 0.0)
        if w and 'POSITION' in tg:
            P = P + w * L.read_accessor(js, bb, tg['POSITION']).astype(float)
    J = L.read_accessor(js, bb, at['JOINTS_0']).astype(int); Wt = L.read_accessor(js, bb, at['WEIGHTS_0']).astype(float)
    if 'JOINTS_1' in at:
        J = np.hstack([J, L.read_accessor(js, bb, at['JOINTS_1']).astype(int)])
        Wt = np.hstack([Wt, L.read_accessor(js, bb, at['WEIGHTS_1']).astype(float)])
    idx = L.read_accessor(js, bb, pr['indices']).astype(np.int64).reshape(-1, 3)
    BP.append(P); BJ.append(J); BW.append(Wt); BT.append(idx + off); off += len(P)
BP = np.concatenate(BP); BJ = np.concatenate(BJ); BW = np.concatenate(BW); BT = np.concatenate(BT)
BW = BW / np.maximum(BW.sum(1, keepdims=True), 1e-12)
BPh = np.hstack([BP, np.ones((len(BP), 1))])
jname = [js['nodes'][j].get('name') for j in SJ]
dom = BJ[np.arange(len(BJ)), np.argmax(BW, axis=1)]
HAND = {'r': np.nonzero(dom == jname.index('RightHand'))[0], 'l': np.nonzero(dom == jname.index('LeftHand'))[0]}
TRIS = [tuple(t) for t in BT.tolist()]


def skin_body(G):
    M = np.stack([G[j] @ IBM[k] for k, j in enumerate(SJ)])                   # (nj,4,4)
    out = np.zeros((len(BP), 3))
    for c in range(BJ.shape[1]):
        out += BW[:, c:c + 1] * np.einsum('vij,vj->vi', M[BJ[:, c]], BPh)[:, :3]
    return out


# ---------------------------------------------------------------- the weapons, placed by their own IBMs
def piece(path, bone):
    pj, pb = L.load_glb(path)
    pn = next(i for i, nd in enumerate(pj['nodes']) if 'mesh' in nd and 'skin' in nd)
    psk = pj['skins'][pj['nodes'][pn]['skin']]
    names = [pj['nodes'][j].get('name') for j in psk['joints']]
    ibm = L.read_accessor(pj, pb, psk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)[names.index(bone)]
    pr = pj['meshes'][pj['nodes'][pn]['mesh']]['primitives'][0]
    V = L.read_accessor(pj, pb, pr['attributes']['POSITION']).astype(float)
    J = L.read_accessor(pj, pb, pr['attributes']['JOINTS_0']).astype(int); Wt = L.read_accessor(pj, pb, pr['attributes']['WEIGHTS_0']).astype(float)
    on = float((Wt * (J == names.index(bone))).sum() / max(Wt.sum(), 1e-12))
    loc = (ibm @ np.hstack([V, np.ones((len(V), 1))]).T).T[:, :3]           # the joint's LOCAL frame (its units)
    return dict(path=path, bone=bone, ibm=ibm, V=np.hstack([V, np.ones((len(V), 1))]), local=loc, weight_on_bone=round(on, 5),
                tip=int(np.argmax(loc[:, 1])))


WEAP = {}
if SWORD:
    WEAP['r'] = piece(SWORD, 'weapon_r')
if AXE:
    WEAP['l'] = piece(AXE, 'weapon_l')


def unit(v):
    return v / np.linalg.norm(v)


def inside(tree, p):
    loc, nrm, fi, dist = tree.find_nearest(Vector(p))
    if loc is None:
        return False
    if (Vector(p) - loc).dot(nrm) > 0 and dist > 1e-4:                         # on the outward side of the nearest face
        return False
    for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        o = Vector(p); dv = Vector(d); n = 0
        for _ in range(64):
            h = tree.ray_cast(o, dv, 10.0)
            if h[0] is None:
                break
            n += 1; o = h[0] + dv * 1e-5
        if n % 2 == 0:
            return False
    return True


# ---------------------------------------------------------------- measure
res = dict(body=os.path.abspath(BODY), weapons={k: dict(path=v['path'], bone=v['bone'], weight_on_bone=v['weight_on_bone']) for k, v in WEAP.items()},
           morphs=MORPHS, layers=LAYERS, convention="glTF world metres: +Y up, he faces +Z, his right is -X", clips={})
nid = body['nid']
for clip in CLIPS:
    T = clip_len(body, clip)
    times = [T * i / (N - 1) for i in range(N)]
    rows = []
    for t in times:
        G = pose(body, clip, t)
        row = dict(t=round(t, 5), joints={b: [round(float(x), 5) for x in G[nid[b]][:3, 3]] for b in ('Hips', 'Spine02', 'Head', 'RightHand', 'LeftHand')},
                   rot={b: [[round(float(x), 5) for x in rr] for rr in (G[nid[b]][:3, :3] / np.linalg.norm(G[nid[b]][:3, :3], axis=0))] for b in ('Hips', 'Head')},
                   weapons={})
        tree = None
        if not NOPEN and WEAP:
            BV = skin_body(G)
            tree = BVHTree.FromPolygons([tuple(v) for v in BV.tolist()], TRIS, all_triangles=True)
        for k, wp in WEAP.items():
            Gw = G[nid[wp['bone']]]
            M = Gw @ wp['ibm']
            R = Gw[:3, :3]; sc = float(np.linalg.norm(R[:, 0])); R = R / sc
            X, Y, Z = R[:, 0], R[:, 1], R[:, 2]
            WV = (M @ wp['V'].T).T[:, :3]
            grip = Gw[:3, 3]; tip = WV[wp['tip']]
            wr = dict(grip=[round(float(x), 5) for x in grip], tip=[round(float(x), 5) for x in tip],
                      X=[round(float(x), 5) for x in X], Y=[round(float(x), 5) for x in Y], Z=[round(float(x), 5) for x in Z],
                      tilt_deg=round(math.degrees(math.acos(max(-1, min(1, float(Y[1]))))), 2))
            if tree is not None:
                ly = wp['local'][:, 1] * sc; lr = np.hypot(wp['local'][:, 0], wp['local'][:, 2]) * sc
                half = 0.07                                                     # half a grip, metres (the sword's is 0.066)
                cand = [i for i in range(0, len(WV), EVERY) if not (abs(ly[i]) <= half and lr[i] <= 0.06)]
                hv = BV[HAND[k]]
                pen, where = 0, []
                for i in cand:
                    if np.min(np.sum((hv - WV[i]) ** 2, axis=1)) < 0.02 ** 2:
                        continue
                    if inside(tree, WV[i]):
                        pen += 1
                        if len(where) < 6:
                            where.append(round(float(ly[i]), 3))
                wr['pen'] = pen; wr['pen_at_local_y_m'] = where; wr['pen_tested'] = len(cand)
            row['weapons'][k] = wr
        rows.append(row)
    pmax = {k: max((r['weapons'][k].get('pen', 0) for r in rows), default=0) for k in WEAP}
    res['clips'][clip] = dict(T=round(T, 5), n=N, rows=rows, pen_max=pmax)
    print("[j_measure] %-18s T %.3f s, %d samples; pen max %s" % (clip, T, N, pmax), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
print("[j_measure] wrote %s" % OUT)
