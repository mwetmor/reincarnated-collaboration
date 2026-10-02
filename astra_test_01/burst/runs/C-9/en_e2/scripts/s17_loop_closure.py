# Does a looping clip close? pose(0) against pose(T), every skin joint, in glTF WORLD metres.
#
#   python3 scripts/s17_loop_closure.py <body.glb> run,walk,idle [--json f]
#
# The instrument behind the run-seam fix (s17_run_cycle.py): the pack's in-figure closure of 35.7
# on run is a pixel measure; this is its source -- how far each joint is from where it started
# when the clip wraps. Pure glTF evaluation (s16's evaluator, copied here because s16 runs its
# CLI on import), so no importer is in the loop it judges.
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')


def model(path):
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
            ch[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, b, s['input'])[:, 0],
                                                              L.read_accessor(js, b, s['output']))
        anims[an.get('name')] = ch
    joints = sorted({j for sk in js.get('skins', []) for j in sk['joints']})
    return dict(nodes=nodes, parent=parent, rest=rest, anims=anims, joints=joints,
                nid={n.get('name'): i for i, n in enumerate(nodes)})


def globals_at(m, clip, t):
    local = {}
    for (n, p), (tt, vv) in m['anims'][clip].items():
        tr, q, s = local.get(n, m['rest'][n])
        i = int(np.searchsorted(tt, t - 1e-6)); i = min(max(i, 0), len(tt) - 1)
        if i > 0 and tt[i] > t and len(tt) > 1:
            a0, a1 = tt[i - 1], tt[i]; w = (t - a0) / max(a1 - a0, 1e-9)
            v0, v1 = vv[i - 1], vv[i]
            if p == 'rotation':
                if np.dot(v0, v1) < 0: v1 = -v1
                v = (1 - w) * v0 + w * v1; v = v / np.linalg.norm(v)
            else:
                v = (1 - w) * v0 + w * v1
        else:
            v = vv[i]
        if p == 'translation': tr = np.array(v, float)
        elif p == 'rotation': q = np.array(v, float)
        elif p == 'scale': s = np.array(v, float)
        local[n] = (tr, q, s)
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = local.get(i, m['rest'][i])
        M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if m['parent'].get(i) is None else g(m['parent'][i]) @ M
        return G[i]
    for i in range(len(m['nodes'])): g(i)
    return G


def rot_deg(A, B):
    Ra = A[:3, :3] / np.linalg.norm(A[:3, :3], axis=0); Rb = B[:3, :3] / np.linalg.norm(B[:3, :3], axis=0)
    c = (np.trace(Ra.T @ Rb) - 1) / 2
    return float(np.degrees(np.arccos(np.clip(c, -1, 1))))


if __name__ == '__main__':
    a = sys.argv[1:]
    m = model(a[0]); clips = a[1].split(",")
    OUTJ = a[a.index('--json') + 1] if '--json' in a else None
    rep = {}
    for c in clips:
        T = float(max(v[0].max() for v in m['anims'][c].values()))
        G0, G1 = globals_at(m, c, 0.0), globals_at(m, c, T)
        d = {m['nodes'][j]['name']: float(np.linalg.norm(G0[j][:3, 3] - G1[j][:3, 3])) for j in m['joints']}
        r = {m['nodes'][j]['name']: rot_deg(G0[j], G1[j]) for j in m['joints']}
        jw, rw = max(d, key=d.get), max(r, key=r.get)
        h = m['nid']['Hips']
        rep[c] = dict(T_s=round(T, 6), joints=len(d), worst_joint=jw, worst_joint_m=round(d[jw], 6),
                      worst_rot_joint=rw, worst_rot_deg=round(r[rw], 4),
                      hips_m=round(float(np.linalg.norm(G0[h][:3, 3] - G1[h][:3, 3])), 6), hips_rot_deg=round(rot_deg(G0[h], G1[h]), 4))
        print("  %-6s T %.4f s: worst joint %s %.4f m, worst rotation %s %.3f deg; hips %.4f m %.3f deg"
              % (c, T, jw, d[jw], rw, r[rw], rep[c]['hips_m'], rep[c]['hips_rot_deg']))
    if OUTJ:
        json.dump(rep, open(OUTJ, 'w'), indent=1)
