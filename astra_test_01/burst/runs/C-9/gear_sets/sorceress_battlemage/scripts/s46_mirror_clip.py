# R-C9-119: MIRROR a clip left<->right on her rig, as a BINARY glTF patch (a new animation appended; every other byte kept).
#   python3 s46_mirror_clip.py <body.glb> <out.glb> <clip> <new_name> [--json f]
# Matt: the book lives in her LEFT hand, so the Fire Ball (thrown by her LEFT hand) is mirrored and the WAND hand throws.
# THE METHOD, in world space (55_clip_graft's frame, independent of bone-axis conventions): for every joint n, its world
# rotation AWAY FROM REST is taken from its mirror m (Left<->Right, _l<->_r) and reflected through the sagittal plane:
#     dW_m(t) = R_m(t) R_m_rest^T,   dW'_n(t) = S dW_m(t) S,   R'_n(t) = dW'_n(t) R_n_rest,   S = diag(-1, 1, 1) (world X)
# then back to local under the mirrored parent. The Hips' world position is reflected about her rest x. Valid when the
# REST pose is symmetric: the worst mirror-pair asymmetry of the rest joints is measured and reported.
import json, os, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
G_ = __import__('55_clip_graft')
a = sys.argv[1:]
BODY, OUT, CLIP, NEW = a[:4]
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '_%s.json' % NEW)
js, bin_ = L.load_glb(BODY); bin_ = bytearray(bin_)
names = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
jn = G_.joints(js)


def mirror(n):
    for x, y in (("Left", "Right"), ("Right", "Left")):
        if n.startswith(x):
            return y + n[len(x):]
    for x, y in (("_l", "_r"), ("_r", "_l")):
        if n.endswith(x):
            return n[:-len(x)] + y
    return n


Gb0, bpar = G_.world_rest(js)
S = np.diag([-1.0, 1.0, 1.0])
hips = names['Hips']
x0 = float(Gb0[hips][0, 3])
asym = max(float(np.linalg.norm(S @ (Gb0[names[n]][:3, 3] - np.array([x0, 0, 0])) + np.array([x0, 0, 0]) - Gb0[names[mirror(n)]][:3, 3]))
           for n in jn if mirror(n) in names)
anim = next(an for an in js['animations'] if an.get('name') == CLIP)
trk = G_.tracks(js, bytes(bin_), anim)
times = sorted(set(float(x) for tr in trk.values() for (tt, _, _) in tr.values() for x in tt))
order = []; seen = set()


def visit(i):
    if i in seen: return
    p = bpar.get(i)
    if p is not None and js['nodes'][p].get('name') in jn: visit(p)
    seen.add(i); order.append(i)


for n in jn:
    visit(names[n])
rots = {n: [] for n in jn}; hipsT = []
P = Gb0[bpar[hips]]; Pi = np.linalg.inv(P)
for t in times:
    G, _ = G_.globals_from(js, G_.local_mats(js, trk, t, True))
    Rw = {}
    for i in order:
        n = js['nodes'][i]['name']; m = names[mirror(n)]
        dW = G_.rot(G[m]) @ G_.rot(Gb0[m]).T
        Rw[i] = (S @ dW @ S) @ G_.rot(Gb0[i])
        p = bpar.get(i)
        Rp = Rw[p] if p in Rw else G_.rot(Gb0[p])
        rots[n].append(W.m2q(Rp.T @ Rw[i]))
    ph = G[hips][:3, 3].copy(); ph[0] = 2 * x0 - ph[0]
    hipsT.append((Pi @ np.append(ph, 1.0))[:3])
times = np.array(times) - times[0]


def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); off = W.append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    a_ = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR":
        a_["min"] = [float(arr.min())]; a_["max"] = [float(arr.max())]
    js['accessors'].append(a_); return len(js['accessors']) - 1


before = json.dumps(js['animations'], sort_keys=True)
ti = acc(times.reshape(-1), "SCALAR"); ch, sm = [], []
for n in jn:
    q = np.array(rots[n])
    for j in range(1, len(q)):
        if np.dot(q[j], q[j - 1]) < 0: q[j] = -q[j]
    sm.append({"input": ti, "output": acc(q, "VEC4"), "interpolation": "LINEAR"})
    ch.append({"sampler": len(sm) - 1, "target": {"node": names[n], "path": "rotation"}})
sm.append({"input": ti, "output": acc(np.array(hipsT), "VEC3"), "interpolation": "LINEAR"})
ch.append({"sampler": len(sm) - 1, "target": {"node": hips, "path": "translation"}})
js['animations'] = [an for an in js['animations'] if an.get('name') != NEW]
js['animations'].append({"name": NEW, "channels": ch, "samplers": sm})
js['buffers'][0]['byteLength'] = len(bin_)
R_.write_glb(OUT, js, bin_)
# verify: the mirrored clip's RIGHT hand at every key equals the source's LEFT hand reflected
js2, b2 = L.load_glb(OUT)
an2 = next(x for x in js2['animations'] if x.get('name') == NEW); tr2 = G_.tracks(js2, b2, an2)
err = 0.0
for t in np.linspace(times[0], times[-1], 12):
    Ga, _ = G_.globals_from(js, G_.local_mats(js, trk, float(t + 0.0) + 0.0, True))
    Gm, _ = G_.globals_from(js2, G_.local_mats(js2, tr2, float(t), True))
    pl = Ga[names['LeftHand']][:3, 3].copy(); pl[0] = 2 * x0 - pl[0]
    err = max(err, float(np.linalg.norm(pl - Gm[names['RightHand']][:3, 3])))
others_same = json.dumps([x for x in js2['animations'] if x.get('name') != NEW], sort_keys=True) == before
rep = dict(body=BODY, out=OUT, clip=CLIP, new=NEW, keys=len(times), length_s=float(times[-1]), joints=len(jn),
           rest_asymmetry_m=round(asym, 5), right_hand_vs_mirrored_left_max_m=round(err, 5), other_clips_identical=others_same)
json.dump(rep, open(OUTJ, 'w'), indent=1); print("MIRROR", json.dumps(rep))
