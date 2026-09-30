# SOURCE FIDELITY: does a shipped clip still move like the library clip it came from?
#
#   python3 scripts/56_clip_fidelity.py <shipped.glb> [<clip>=<source.glb>[@t0:t1] ...] [--registry f] [--json f]
#
# With no pairs, every clip the provenance registry (work/clip_sources.json) names is measured.
#
# THE MEASURE -- D7's s16_clip_fidelity.py, with its frame corrected. At every compared time, each
# of 14 joints relative to the hips, expressed in the hips' PHYSICAL frame, over the rest
# hips-to-head length; the error is the largest joint distance, shipped against source. s16 takes
# the joints in the hips' own LOCAL frame, which is only comparable when the two rigs' hips rest
# frames coincide -- true for D7 (her clips were fetched for her own rig) and false for the
# barbarian, whose body went through the T8 fit and Blender: its Hips rest rotation is ~110 deg
# from Meshy's. s16 reads 2.4-2.9 on a world-space graft that reproduces its source. The physical
# frame is the local frame turned by the hips' own rest world rotation:
#     x_j(t) = R_hips_rest_world . (G_hips(t)^-1 . p_j(t))  =  dW_hips(t)^-1 . (p_j(t) - p_hips(t))
# -- the joints as seen by hips that have moved dW away from rest, identical for the same motion on
# any rig with the same rest POSE. The hips' own rotation away from rest is compared too (degrees),
# since removing it is what makes the joint measure blind to root processing.
#
# EXCEPTIONS are named, not tolerated: a registry entry's `edits` lists the intended edits after
# the retarget, and each one says what it excludes -- "wrist_lock" the hands, "trim" is the window
# itself, "deroot"/"recentre"/"reground" touch only the hips' translation, which this measure does
# not see. Everything else must be within LIMIT at every frame.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')

LIMIT = 0.10
JOINTS = ["Spine02", "Head", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand",
          "LeftUpLeg", "LeftLeg", "LeftFoot", "RightUpLeg", "RightLeg", "RightFoot"]
EXCLUDES = {"wrist_lock": ("LeftHand", "RightHand")}
REGISTRY = os.path.join(os.path.dirname(HERE), "work", "clip_sources.json")


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
            ch[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, b, s['input'])[:, 0], L.read_accessor(js, b, s['output']))
        anims[an.get('name')] = ch
    return dict(nodes=nodes, parent=parent, rest=rest, anims=anims, nid={n.get('name'): i for i, n in enumerate(nodes)})


def _sample(tt, vv, t, path):
    i = int(np.searchsorted(tt, t - 1e-6)); i = min(max(i, 0), len(tt) - 1)
    if i > 0 and tt[i] > t and len(tt) > 1:
        a0, a1 = tt[i - 1], tt[i]; w = (t - a0) / max(a1 - a0, 1e-9)
        v0, v1 = vv[i - 1], np.array(vv[i], float)
        if path == 'rotation':
            if np.dot(v0, v1) < 0: v1 = -v1
            v = (1 - w) * v0 + w * v1; return v / np.linalg.norm(v)
        return (1 - w) * v0 + w * v1
    return np.array(vv[i], float)


def globals_at(m, clip, t):
    local = {}
    for (n, p), (tt, vv) in (m['anims'][clip].items() if clip else []):
        tr, q, s = local.get(n, m['rest'][n])
        v = _sample(tt, vv, t, p)
        if p == 'translation': tr = v
        elif p == 'rotation': q = v
        elif p == 'scale': s = v
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


def _rot(M):
    u, _, vt = np.linalg.svd(M[:3, :3]); r = u @ vt
    if np.linalg.det(r) < 0: u[:, -1] *= -1; r = u @ vt
    return r


class Rig:
    def __init__(self, path):
        self.m = model(path)
        G0 = globals_at(self.m, None, 0.0)
        h = self.m['nid']['Hips']
        self.R0 = _rot(G0[h])                                   # the hips' rest world rotation
        self.span = float(np.linalg.norm((np.linalg.inv(G0[h]) @ G0[self.m['nid']['Head']])[:3, 3]))

    def pose(self, clip, t):
        G = globals_at(self.m, clip, t)
        h = self.m['nid']['Hips']
        Hi = np.linalg.inv(G[h])
        x = {j: self.R0 @ (Hi @ G[self.m['nid'][j]])[:3, 3] / self.span for j in JOINTS}
        return x, _rot(G[h]) @ self.R0.T                         # joints, the hips' dW


def fidelity(ship, clip, src, window=None, exclude=()):
    S = ship if isinstance(ship, Rig) else Rig(ship)
    C = src if isinstance(src, Rig) else Rig(src)
    sclip = next(iter(C.m['anims']))
    tsrc = np.concatenate([v[0] for v in C.m['anims'][sclip].values()])
    tshp = np.concatenate([v[0] for v in S.m['anims'][clip].values()])
    shifts = [0.0, float(tsrc.min() - tshp.min())]
    if window is not None:
        # the graft re-times the first source key at or after t0 to 0
        k0 = float(np.min(tsrc[tsrc >= float(window[0]) - 1e-6]))
        shifts = [k0 - float(tshp.min())]
    tt = sorted(set(np.round(tshp, 4)))
    joints = [j for j in JOINTS if j not in exclude]
    best = None
    for sh in shifts:
        rows = []
        for t in tt:
            ts = min(t + sh, float(tsrc.max()))
            a, ha = S.pose(clip, t); b, hb = C.pose(sclip, ts)
            e = {j: float(np.linalg.norm(a[j] - b[j])) for j in joints}
            jw = max(e, key=e.get)
            c = (np.trace(ha @ hb.T) - 1) / 2
            rows.append((float(t), e[jw], jw, math.degrees(math.acos(max(-1.0, min(1.0, c))))))
        med = float(np.median([r[1] for r in rows]))
        if best is None or med < best[1]:
            best = (sh, med, rows)
    sh, med, rows = best
    w = max(rows, key=lambda r: r[1])
    return dict(clip=clip, source=os.path.basename(src if isinstance(src, str) else "?"), source_clip=sclip, time_shift_s=round(sh, 4),
                times=len(rows), err_max=round(w[1], 4), worst_t=round(w[0], 4), worst_joint=w[2], err_median=round(med, 4),
                hips_deg_max=round(max(r[3] for r in rows), 2), excluded=list(exclude), within=bool(w[1] <= LIMIT))


def registry(path=REGISTRY):
    return json.load(open(path)) if os.path.exists(path) else {"clips": {}}


def rest_match(A, B):
    """How far two rigs' REST POSES are apart: the 14 joints in the hips' physical frame over the
    rest hips-to-head. ~0 for a clip fetched for this body's own rig."""
    def pose(R):
        G = globals_at(R.m, None, 0.0); h = R.m['nid']['Hips']; Hi = np.linalg.inv(G[h])
        return {j: R.R0 @ (Hi @ G[R.m['nid'][j]])[:3, 3] / R.span for j in JOINTS}
    a, b = pose(A), pose(B)
    return max(float(np.linalg.norm(a[j] - b[j])) for j in JOINTS)


RIG_TOL = 0.01


def check(ship_glb, reg=None):
    """The lint row: every registry clip present in the GLB, within LIMIT at every frame, its source
    on this body's rig. Statuses: PASS / FAIL / RIG (source on another skeleton) / LEGACY (unused,
    slated for removal; measured for information) / AUTHORED / UNMEASURED (not a GLB, e.g. SMPL-H)."""
    reg = reg if reg is not None else registry()
    S = Rig(ship_glb)
    root = os.path.dirname(HERE)
    out = []
    for clip, e in sorted(reg.get("clips", {}).items()):
        if clip not in S.m['anims']:
            continue
        if not e.get("source"):
            out.append(dict(clip=clip, status="LEGACY" if e.get("status") == "legacy" else "AUTHORED", note=e.get("note", "no library source")))
            continue
        src = os.path.join(root, e["source"])
        if not os.path.exists(src) or not src.endswith(".glb"):
            out.append(dict(clip=clip, status="LEGACY" if e.get("status") == "legacy" else "UNMEASURED",
                            note=e.get("note") or "source %s not a GLB on disk" % e["source"]))
            continue
        C = Rig(src)
        ex = []
        for ed in e.get("edits", []):
            ex += list(EXCLUDES.get(ed, ()))
        r = fidelity(S, clip, C, e.get("window"), tuple(ex))
        r["source"] = e["source"]
        r["rest_match"] = round(rest_match(S, C), 5)
        r["edits"] = e.get("edits", [])
        if e.get("status") == "legacy":
            r["status"] = "LEGACY"; r["note"] = e.get("note", "")
        elif r["rest_match"] > RIG_TOL:
            r["status"] = "RIG"
        else:
            r["status"] = "PASS" if r["within"] else "FAIL"
        out.append(r)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    regp = a[a.index('--registry') + 1] if '--registry' in a else REGISTRY
    ship = a[0]
    pairs = [x for x in a[1:] if '=' in x and not x.startswith('--')]
    res = []
    if pairs:
        S = Rig(ship)
        for p in pairs:
            clip, src = p.split('=', 1)
            win = None
            if '@' in src:
                src, w = src.split('@', 1); win = [float(v) for v in w.split(':')]
            res.append(fidelity(S, clip, src, win))
    else:
        res = check(ship, registry(regp))
    print("source fidelity of %s (joints in the hips' physical frame / rest hips-to-head; limit %.2f)" % (os.path.basename(ship), LIMIT))
    for r in res:
        if 'err_max' not in r:
            print("  %-22s %-10s %s" % (r['clip'], r['status'], r.get('note', '')))
            continue
        print("  %-22s %-4s vs %-20s worst %.4f at %.3f s (%s), median %.4f, hips %.1f deg; shift %+.4f s, %d times%s"
              % (r['clip'], r.get('status', 'PASS' if r['within'] else 'FAIL'), r['source'], r['err_max'], r['worst_t'], r['worst_joint'],
                 r['err_median'], r['hips_deg_max'], r['time_shift_s'], r['times'], (" (excluding %s)" % ",".join(r['excluded'])) if r['excluded'] else ""))
    if outj:
        json.dump(res, open(outj, 'w'), indent=1)
