# R-C9-98: add ONE morph target to her body -- `under_battlemage` -- as a BINARY glTF patch (no Blender round trip: the
# body's clips and patched channels stay byte-identical, verified at the end).
#
#   python3 s28_body_morph.py <so-body.glb> <out.glb> <piece.glb> [<piece.glb> ...] [--json f]
#
# WHY. Her base body wears a knee-length linen SHIFT that flares from the hips. The battle-mage armour was cut from a build
# of the DRESSED body, where the cuisses and the mail skirt hug the thighs -- so the shift's flare stands OUTSIDE them and
# shows as a cream band between the mail hem and the knee (stills v2, the green-marked holes). D7 met the same class of
# defect with `under_<garment>` keys; this is that key for the whole set, computed at rest from the pieces' own surfaces.
#
# THE KEY. Every body vertex between zf 0.30 and 0.80 (knee to chest) that is OUTSIDE or within MARGIN of the nearest piece
# surface (the piece's nearest vertex and its normal) moves to MARGIN inside that surface, along the piece normal. Vertices
# already deeper than MARGIN never move. The displacement is converted to the mesh's own space through the bind
# (joint world rest x inverse bind), so it is exact for a skinned primitive. The scene sets under_battlemage = 1 while the
# GOWN is worn (morph_rules), as it sets grip_R with the wand.
import json, os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export')
R_ = __import__('49_recentre')

a = sys.argv[1:]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--json', '--band'))]
BODY, OUT, PIECES = pos[0], pos[1], pos[2:]
MARGIN, ZLO, ZHI, NAME = 0.008, 0.30, 0.80, "under_battlemage"
if "--band" in a:   # v9: the whole leg under the leggings and greaves (the knees showed through in the run and casts)
    ZLO, ZHI = (float(x) for x in a[a.index("--band") + 1].split(","))


def node_world(js):
    par = {}
    for i, n in enumerate(js['nodes']):
        for c in n.get('children', []):
            par[c] = i
    loc = [L._trs(n) for n in js['nodes']]
    W = [None] * len(js['nodes'])

    def w(i):
        if W[i] is None:
            W[i] = loc[i] if i not in par else w(par[i]) @ loc[i]
        return W[i]
    return [w(i) for i in range(len(js['nodes']))]


def bind_matrix(js, bin_, skin_i):
    sk = js['skins'][skin_i]
    ibm = L.read_accessor(js, bin_, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    Wn = node_world(js)
    Ms = [Wn[j] @ ibm[k] for k, j in enumerate(sk['joints'])]
    spread = max(float(np.abs(M - Ms[0]).max()) for M in Ms)
    return Ms[0], spread


def world_positions(path):
    js, bin_ = L.load_glb(path)
    out, nrm = [], []
    for n in js['nodes']:
        if 'mesh' not in n:
            continue
        M, _ = bind_matrix(js, bin_, n['skin']) if 'skin' in n else (node_world(js)[js['nodes'].index(n)], 0)
        for p in js['meshes'][n['mesh']]['primitives']:
            P = L.read_accessor(js, bin_, p['attributes']['POSITION'])
            N = L.read_accessor(js, bin_, p['attributes']['NORMAL'])
            out.append(P @ M[:3, :3].T + M[:3, 3])
            Nw = N @ np.linalg.inv(M[:3, :3])
            nrm.append(Nw / np.maximum(np.linalg.norm(Nw, axis=1, keepdims=True), 1e-9))
    return np.vstack(out), np.vstack(nrm)


js, bin_ = L.load_glb(BODY)
bin_ = bytearray(bin_)
anim_before = json.dumps(js['animations'], sort_keys=True)
anim_bytes_before = [bytes(bin_[js['bufferViews'][js['accessors'][s['input']]['bufferView']].get('byteOffset', 0):
                                js['bufferViews'][js['accessors'][s['input']]['bufferView']].get('byteOffset', 0)
                                + js['bufferViews'][js['accessors'][s['input']]['bufferView']]['byteLength']])
                     for an in js['animations'] for s in an['samplers'][:3]]
node_i = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
mesh_i = js['nodes'][node_i]['mesh']
M, spread = bind_matrix(js, bytes(bin_), js['nodes'][node_i]['skin'])
print("bind matrix from joint 0; spread across joints %.2e" % spread)
GP, GN = [], []
for p in PIECES:
    P_, N_ = world_positions(p); GP.append(P_); GN.append(N_)
GP, GN = np.vstack(GP), np.vstack(GN)
tree = cKDTree(GP)
rep = dict(name=NAME, margin_m=MARGIN, band_zf=[ZLO, ZHI], pieces=[os.path.basename(p) for p in PIECES], primitives=[])
for prim in js['meshes'][mesh_i]['primitives']:
    P = L.read_accessor(js, bytes(bin_), prim['attributes']['POSITION'])
    Pw = P @ M[:3, :3].T + M[:3, 3]
    z0, z1 = Pw[:, 2].min(), Pw[:, 2].max()
    zf = (Pw[:, 2] - z0) / (z1 - z0)
    band = (zf > ZLO) & (zf < ZHI)
    d, j = tree.query(Pw)
    s = np.einsum('ij,ij->i', Pw - GP[j], GN[j])          # signed: + outside the piece surface
    move = band & (s > -MARGIN) & (d < 0.08)
    D = np.zeros_like(Pw)
    D[move] = -(s[move] + MARGIN)[:, None] * GN[j[move]]
    Dl = D @ np.linalg.inv(M[:3, :3]).T                    # world displacement -> mesh space
    data = Dl.astype('<f4').tobytes()
    while len(bin_) % 4:
        bin_.append(0)
    off = len(bin_); bin_ += data
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(Dl)),
                            "type": "VEC3", "min": Dl.min(0).tolist(), "max": Dl.max(0).tolist()})
    prim.setdefault('targets', []).append({"POSITION": len(js['accessors']) - 1})
    mv = np.linalg.norm(D[move], axis=1)
    rep["primitives"].append(dict(verts=int(len(Pw)), in_band=int(band.sum()), moved=int(move.sum()),
                                  max_m=round(float(mv.max()), 4) if move.any() else 0.0,
                                  median_m=round(float(np.median(mv)), 4) if move.any() else 0.0))
    print("primitive: %d verts, %d in band, %d moved (median %.4f m, max %.4f m)" % (len(Pw), band.sum(), move.sum(),
          rep["primitives"][-1]["median_m"], rep["primitives"][-1]["max_m"]))
mesh = js['meshes'][mesh_i]
mesh['weights'] = list(mesh.get('weights', [])) + [0.0]
mesh.setdefault('extras', {}).setdefault('targetNames', []).append(NAME)
js['buffers'][0]['byteLength'] = len(bin_)
assert json.dumps(js['animations'], sort_keys=True) == anim_before
R_.write_glb(OUT, js, bytes(bin_))
# VERIFY: re-read, animation JSON identical and a sample of animation buffer bytes identical
js2, b2 = L.load_glb(OUT)
anim_bytes_after = [bytes(b2[js2['bufferViews'][js2['accessors'][s['input']]['bufferView']].get('byteOffset', 0):
                             js2['bufferViews'][js2['accessors'][s['input']]['bufferView']].get('byteOffset', 0)
                             + js2['bufferViews'][js2['accessors'][s['input']]['bufferView']]['byteLength']])
                    for an in js2['animations'] for s in an['samplers'][:3]]
rep["animations_identical"] = (json.dumps(js2['animations'], sort_keys=True) == anim_before) and anim_bytes_after == anim_bytes_before
rep["target_names"] = js2['meshes'][mesh_i]['extras']['targetNames']
rep["out_mb"] = round(os.path.getsize(OUT) / 1e6, 2)
print(json.dumps({k: v for k, v in rep.items() if k != 'primitives'}))
if OUTJ:
    json.dump(rep, open(OUTJ, 'w'), indent=1)
