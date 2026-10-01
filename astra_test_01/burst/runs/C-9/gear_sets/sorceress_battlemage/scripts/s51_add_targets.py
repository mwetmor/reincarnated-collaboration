# R-C9-119: add morph targets authored in Blender (s50's per-vertex deltas, Blender mesh-local) to a glTF body as a BINARY
# patch -- clips, skin, other targets byte-identical.
#   python3 s51_add_targets.py <body.glb> <deltas.npz> <out.glb> <name> [<name> ...]
# The Blender->glTF vertex-space map is MEASURED, not assumed: each candidate axis map is applied to Blender's basis and
# compared with the glTF POSITION accessor vertex for vertex; the one that matches (max error < 1e-4) is used for the deltas.
import json, os, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, NPZ, OUT, NAMES = a[0], a[1], a[2], a[3:]
D = np.load(NPZ)
js, b = L.load_glb(BODY); b = bytearray(b)
ni = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
mesh = js['meshes'][js['nodes'][ni]['mesh']]
assert len(mesh['primitives']) == 1
prim = mesh['primitives'][0]
P = L.read_accessor(js, bytes(b), prim['attributes']['POSITION'])
Bb = D['basis_blender_local']
assert len(Bb) == len(P), (len(Bb), len(P))
_yup = lambda v: np.stack([v[:, 0], v[:, 2], -v[:, 1]], 1)
# a uniform SCALE is fitted per candidate too: Meshy's rig carries a 0.01 object scale, so Blender's mesh-local is 100x glTF's
def fit(f):
    X = f(Bb); k = float((X * P).sum() / (X * X).sum()); return k
maps0 = {"identity": lambda v: v, "yup": _yup}
ks = {k: fit(f) for k, f in maps0.items()}
maps = {k: (lambda f, kk: (lambda v: kk * f(v)))(f, ks[k]) for k, f in maps0.items()}
errs = {k: float(np.abs(f(Bb) - P).max()) for k, f in maps.items()}
best = min(errs, key=errs.get)
assert errs[best] < 1e-4, errs
before = json.dumps(js['animations'], sort_keys=True)
for nm in NAMES:
    d = maps[best](D[nm]).astype(np.float32)
    data = d.tobytes(); off = W.append(b, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(d)), "type": "VEC3",
                            "min": d.min(0).tolist(), "max": d.max(0).tolist()})
    prim.setdefault('targets', []).append({"POSITION": len(js['accessors']) - 1})
    mesh['weights'] = list(mesh.get('weights', [])) + [0.0]
    mesh.setdefault('extras', {}).setdefault('targetNames', []).append(nm)
js['buffers'][0]['byteLength'] = len(b)
assert json.dumps(js['animations'], sort_keys=True) == before
R_.write_glb(OUT, js, bytes(b))
print(json.dumps(dict(out=OUT, space_map=best, scale=round(ks[best], 6), map_errors=errs, added=NAMES, target_names=mesh['extras']['targetNames'],
                      moved={nm: int((np.linalg.norm(D[nm], axis=1) > 1e-6).sum()) for nm in NAMES})))
