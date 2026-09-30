# Does a shipped clip still MOVE like the Meshy clip it came from?
#
#   python3 scripts/s16_clip_fidelity.py <shipped.glb> <clip>=<source.glb> [...] [--json f]
#
# Asked because the T12 drax found nb_d2's 33_assemble Blender action merge re-framing every
# bone's motion (Q_body = R_body_rest * R_src_rest^-1 * Q_src): joints off by 0.2-0.9 of the
# hips-to-head length against the source. D7's s6_merge moves actions the same way, so the
# same question applies to her.
#
# Measure: at every source key time, every joint's position in the HIPS' own frame (which
# removes whatever the root processing -- de-root, recentre, re-ground -- did to Hips itself),
# divided by the rest hips-to-head length, shipped against source. Pure glTF evaluation, no
# Blender, so no importer can be in the loop that it is judging.
# VALID ONLY WHEN BOTH RIGS SHARE THE HIPS REST FRAME -- true for D7, whose clips were fetched on
# her own rig. Across rigs whose rests differ, hips-LOCAL coordinates of two differently oriented
# hips frames disagree even for a faithful graft (the T12 drax measured 2.4-2.9 on one); the
# rotation-corrected form, x_j = R_hips_rest_world . (G_hips(t)^-1 . p_j), is
# nb_d2/scripts/56_clip_fidelity.py.
import json, sys, os
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
    return dict(nodes=nodes, parent=parent, rest=rest, anims=anims,
                nid={n.get('name'): i for i, n in enumerate(nodes)})


def globals_at(m, clip, t):
    local = {}
    for (n, p), (tt, vv) in (m['anims'][clip].items() if clip else []):
        tr, q, s = local.get(n, m['rest'][n])
        i = int(np.searchsorted(tt, t - 1e-6)); i = min(max(i, 0), len(tt) - 1)
        if i > 0 and tt[i] > t and len(tt) > 1:          # linear between keys
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


JOINTS = ["Spine02", "Head", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand",
          "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot"]
a = sys.argv[1:]
SHIP = a[0]
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
pairs = [x.split("=", 1) for x in a[1:] if "=" in x and not x.startswith("--")]
ms = model(SHIP)
rep = {}
for clip, src in pairs:
    mc = model(src)
    sclip = next(iter(mc['anims']))
    def rel(m, c, t):
        G = globals_at(m, c, t)
        Hi = np.linalg.inv(G[m['nid']['Hips']])
        return {j: (Hi @ G[m['nid'][j]])[:3, 3] for j in JOINTS}
    def span(m):
        # the rest hips-to-head IN THE HIPS' OWN UNITS -- the positions compared are hips-local
        # (a glTF armature at 0.01 scale makes those centimetres). The first version divided
        # hips-local centimetres by a world-metre span and reported walk "4.06 hips-to-head" off
        # at a frame where every joint matched the source to 0.01 units.
        G = globals_at(m, None, 0.0)
        return float(np.linalg.norm((np.linalg.inv(G[m['nid']['Hips']]) @ G[m['nid']['Head']])[:3, 3]))
    hs, hc = span(ms), span(mc)
    tsrc = np.concatenate([v[0] for v in mc['anims'][sclip].values()])
    tshp = np.concatenate([v[0] for v in ms['anims'][clip].values()])
    # the merge resamples to 24 fps and starts every clip at 0; Meshy's keys start one 30 fps
    # frame in. Both alignments are measured and the better one reported, and named.
    shift = float(tsrc.min() - tshp.min())
    tt = sorted(set(np.round(tshp, 4)))
    tt = tt[::max(1, len(tt) // 24)]
    best = None
    for sh in (0.0, shift):
        worst, errs = 0.0, []
        for t in tt:
            A, B = rel(ms, clip, t), rel(mc, sclip, min(t + sh, float(tsrc.max())))
            e = {j: float(np.linalg.norm(A[j] / hs - B[j] / hc)) for j in JOINTS}
            errs.append(max(e.values())); worst = max(worst, max(e.values()))
        if best is None or float(np.median(errs)) < best[2]:
            best = (sh, worst, float(np.median(errs)), errs)
    sh, worst, med, errs = best
    rep[clip] = dict(source=os.path.basename(src), source_clip=sclip, times=len(tt), time_shift_s=round(sh, 4),
                     err_max=round(worst, 4), err_median_of_frame_max=round(med, 4))
    print("  %-14s vs %-12s (shift %+.4f s) joints in the hips frame / hips-to-head: max %.4f, median of per-frame max %.4f (%d times)"
          % (clip, os.path.basename(src), sh, worst, med, len(tt)))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
