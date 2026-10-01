# R-C9-119: carry the body's NEW grip morphs onto a worn piece (the gauntlets) as a BINARY patch: each piece vertex moves as
# its NEAREST body vertex moves (world space, rest), so the steel glove closes with the fist instead of the fist closing
# inside an open glove. Both files are read in glTF: world rest = bind (joint world x inverse bind) applied to POSITION.
#   python3 s53_piece_keys.py <body.glb> <piece.glb> <out.glb> <key> [<key> ...]
import json, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_battlemage/scripts')
S28 = None
a = sys.argv[1:]; BODY, PIECE, OUT, KEYS = a[0], a[1], a[2], a[3:]


def node_world(js):
    par = {c: i for i, n in enumerate(js['nodes']) for c in n.get('children', [])}
    loc = [L._trs(n) for n in js['nodes']]; Wm = [None] * len(js['nodes'])
    def w(i):
        if Wm[i] is None: Wm[i] = loc[i] if i not in par else w(par[i]) @ loc[i]
        return Wm[i]
    return [w(i) for i in range(len(js['nodes']))]


def bind(js, b, ni):
    sk = js['skins'][js['nodes'][ni]['skin']]
    ibm = L.read_accessor(js, b, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    return node_world(js)[sk['joints'][0]] @ ibm[0]


jb, bb = L.load_glb(BODY)
nb = next(i for i, n in enumerate(jb['nodes']) if 'mesh' in n and 'skin' in n)
Mb = bind(jb, bb, nb); pr = jb['meshes'][jb['nodes'][nb]['mesh']]['primitives'][0]
names = jb['meshes'][jb['nodes'][nb]['mesh']]['extras']['targetNames']
PB = L.read_accessor(jb, bb, pr['attributes']['POSITION']); BW = PB @ Mb[:3, :3].T + Mb[:3, 3]
dW = {k: L.read_accessor(jb, bb, pr['targets'][names.index(k)]['POSITION']) @ Mb[:3, :3].T for k in KEYS}
tree = cKDTree(BW)
js, b = L.load_glb(PIECE); b = bytearray(b)
rep = dict(piece=PIECE, out=OUT, keys=KEYS, meshes={})
done = set()
for ni, nd in enumerate(js['nodes']):
    if 'mesh' not in nd or 'skin' not in nd or nd['mesh'] in done:
        continue
    done.add(nd['mesh'])
    M = bind(js, bytes(b), ni); Mi = np.linalg.inv(M[:3, :3])
    mesh = js['meshes'][nd['mesh']]
    for p in mesh['primitives']:
        P = L.read_accessor(js, bytes(b), p['attributes']['POSITION']); PW = P @ M[:3, :3].T + M[:3, 3]
        dist, j = tree.query(PW)
        for k in KEYS:
            d = (dW[k][j] @ Mi.T).astype(np.float32)
            data = d.tobytes(); off = W.append(b, data)
            js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
            js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(d)),
                                    "type": "VEC3", "min": d.min(0).tolist(), "max": d.max(0).tolist()})
            p.setdefault('targets', []).append({"POSITION": len(js['accessors']) - 1})
        rep['meshes'].setdefault(mesh.get('name', str(nd['mesh'])), []).append(
            dict(verts=int(len(P)), nearest_median_m=round(float(np.median(dist)), 4), moved={k: int((np.linalg.norm(dW[k][j], axis=1) > 1e-6).sum()) for k in KEYS}))
    nt = len(mesh['primitives'][0].get('targets', []))
    mesh['weights'] = (list(mesh.get('weights', [])) + [0.0] * len(KEYS))[:nt]
    mesh.setdefault('extras', {}).setdefault('targetNames', [])
    mesh['extras']['targetNames'] = mesh['extras']['targetNames'] + KEYS
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, bytes(b))
print(json.dumps(rep))
