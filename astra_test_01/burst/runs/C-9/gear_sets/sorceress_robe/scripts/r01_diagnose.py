# R-C9-120: why her long red robe moves "in a blocky fashion". Reads a skinned piece in glTF: rest world positions (bind),
# JOINTS_0/WEIGHTS_0; reports the weight share by bone for the BOTTOM 40% of the robe (by rest height), how many vertices
# are dominated by each bone, how sharp the boundaries are (neighbouring vertices whose dominant bone differs, and the
# weight jump across those edges), and how much weight sits on the shins and feet.
#   python3 r01_diagnose.py <piece.glb> <out.json>
import json, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export')


def node_world(js):
    par = {c: i for i, n in enumerate(js['nodes']) for c in n.get('children', [])}
    loc = [L._trs(n) for n in js['nodes']]; Wm = [None] * len(js['nodes'])
    def w(i):
        if Wm[i] is None: Wm[i] = loc[i] if i not in par else w(par[i]) @ loc[i]
        return Wm[i]
    return [w(i) for i in range(len(js['nodes']))]


def load(path):
    js, b = L.load_glb(path)
    ni = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n and
              max(js['accessors'][p['attributes']['POSITION']]['count'] for p in js['meshes'][n['mesh']]['primitives']) > 500)
    sk = js['skins'][js['nodes'][ni]['skin']]
    ibm = L.read_accessor(js, b, sk['inverseBindMatrices']).reshape(-1, 4, 4).transpose(0, 2, 1)
    M = node_world(js)[sk['joints'][0]] @ ibm[0]
    jn = [js['nodes'][j]['name'] for j in sk['joints']]
    P, J, Wt, I = [], [], [], []
    off = 0
    for p in js['meshes'][js['nodes'][ni]['mesh']]['primitives']:
        pos = L.read_accessor(js, b, p['attributes']['POSITION'])
        P.append(pos @ M[:3, :3].T + M[:3, 3]); J.append(L.read_accessor(js, b, p['attributes']['JOINTS_0']).astype(int))
        Wt.append(L.read_accessor(js, b, p['attributes']['WEIGHTS_0'])); I.append(L.read_accessor(js, b, p['indices']).astype(int).reshape(-1, 3) + off)
        off += len(pos)
    return js, b, ni, jn, np.vstack(P), np.vstack(J), np.vstack(Wt), np.vstack(I)


if __name__ == "__main__":
    PIECE, OUT = sys.argv[1], sys.argv[2]
    js, b, ni, jn, P, J, Wt, I = load(PIECE)
    y = P[:, 1]; y0, y1 = y.min(), y.max(); hf = (y - y0) / (y1 - y0)       # glTF: +Y up
    low = hf < 0.40
    nb = len(jn); share = np.zeros(nb)
    np.add.at(share, J[low].ravel(), Wt[low].ravel()); share /= share.sum()
    dom = J[np.arange(len(J)), Wt.argmax(1)]
    domc = np.bincount(dom[low], minlength=nb)
    e = np.vstack([I[:, [0, 1]], I[:, [1, 2]], I[:, [2, 0]]]); e = np.unique(np.sort(e, 1), axis=0)
    el = e[low[e[:, 0]] & low[e[:, 1]]]
    def wvec(i):
        v = np.zeros((len(i), nb)); np.add.at(v, (np.repeat(np.arange(len(i)), 4), J[i].ravel()), Wt[i].ravel()); return v
    jump = np.abs(wvec(el[:, 0]) - wvec(el[:, 1])).sum(1) / 2
    flip = dom[el[:, 0]] != dom[el[:, 1]]
    leg = [k for k, n in enumerate(jn) if n in ("LeftLeg", "RightLeg", "LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase")]
    rep = dict(piece=PIECE, verts=int(len(P)), bottom40_verts=int(low.sum()), height_m=[round(float(y0), 3), round(float(y1), 3)],
               weight_share_bottom40={jn[k]: round(float(share[k]), 4) for k in np.argsort(-share) if share[k] > 0.001},
               dominant_bone_count_bottom40={jn[k]: int(domc[k]) for k in np.argsort(-domc) if domc[k] > 0},
               shin_foot_weight_share_bottom40=round(float(share[leg].sum()), 4),
               boundary=dict(edges=int(len(el)), edges_where_dominant_bone_flips=int(flip.sum()),
                             mean_weight_jump_on_flip_edges=round(float(jump[flip].mean()), 4) if flip.any() else 0.0,
                             edges_with_jump_over_0_5=int((jump > 0.5).sum()),
                             max_influences=int((Wt > 0.002).sum(1).max()), single_bone_verts_pct=round(100 * float((Wt.max(1) > 0.98)[low].mean()), 2)))
    json.dump(rep, open(OUT, 'w'), indent=1); print(json.dumps(rep, indent=1))
