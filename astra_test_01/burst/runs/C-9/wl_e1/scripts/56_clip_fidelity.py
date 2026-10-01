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
EXCLUDES = {"wrist_lock": ("LeftHand", "RightHand"),
            # E1 (drax, 2026-10-01): the two-handed HOLD -- idle/run arms set to the armed walk's held pose (e09_hold.py)
            "head_lift": ("neck", "Head", "head_end", "headfront"),   # E1 stage I: e33 neck/head lift over the idle
            "joint_fix": ("LeftHand", "RightHand", "LeftForeArm", "RightForeArm"),   # E1: 63_joint_fix on keys (wrist deviation cut to 38 deg, elbow to -3)
            "arm_hold": ("LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand", "RightShoulder", "RightArm", "RightForeArm", "RightHand")}
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

# E1 (R-C9-123): a MIXAMO source rests in a T-pose and this body in an A-pose, so joint POSITIONS cannot match (the 55 rule would call
# it 'another rig'). e40b's transfer guarantees bone DIRECTIONS instead; so a registry entry with "retarget": "mixamo_aligned" is
# measured as the worst angle, over the source's own keys (after its window/edits), between each body bone's direction (joint ->
# child, in the WORLD frame relative to the hips' rest-to-now turn) and the source bone's. PASS within DIR_LIMIT_DEG.
DIR_LIMIT_DEG = 6.0
_PAIRS = (("Spine02", "Spine01"), ("Spine01", "Spine"), ("Spine", "neck"), ("neck", "Head"), ("LeftArm", "LeftForeArm"), ("LeftForeArm", "LeftHand"),
          ("RightArm", "RightForeArm"), ("RightForeArm", "RightHand"), ("LeftUpLeg", "LeftLeg"), ("LeftLeg", "LeftFoot"), ("RightUpLeg", "RightLeg"),
          ("RightLeg", "RightFoot"), ("LeftFoot", "LeftToeBase"), ("RightFoot", "RightToeBase"))
def fidelity_dirs(ship, clip, src, window=None, exclude=()):
    S = ship if isinstance(ship, Rig) else Rig(ship); Cc = src if isinstance(src, Rig) else Rig(src)
    sclip = next(iter(Cc.m['anims'])); tsrc = sorted({float(x) for v in Cc.m['anims'][sclip].values() for x in v[0]})
    t0 = window[0] if window else tsrc[0]; t1 = window[1] if window else tsrc[-1]; ts = [x for x in tsrc if t0 - 1e-6 <= x <= t1 + 1e-6]
    worst = (0.0, None, None)
    for t in ts[::2]:
        Gs = globals_at(Cc.m, sclip, t); Gb = globals_at(S.m, clip, t - ts[0])
        for a_, b_ in _PAIRS:
            if a_ in exclude or b_ in exclude: continue
            ds = Gs[Cc.m['nid'][b_]][:3, 3] - Gs[Cc.m['nid'][a_]][:3, 3]; db = Gb[S.m['nid'][b_]][:3, 3] - Gb[S.m['nid'][a_]][:3, 3]
            ang = float(np.degrees(np.arccos(np.clip(np.dot(ds, db) / (np.linalg.norm(ds) * np.linalg.norm(db)), -1, 1))))
            if ang > worst[0]: worst = (ang, round(t - ts[0], 4), a_)
    return dict(clip=clip, times=len(ts), err_max=round(worst[0], 2), worst_t=worst[1], worst_joint=worst[2], err_median=None, hips_deg_max=0.0,
                excluded=list(exclude), within=bool(worst[0] <= DIR_LIMIT_DEG), measure='bone-direction angle (deg), mixamo_aligned')


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
        if e.get("retarget") == "mixamo_aligned":
            r = fidelity_dirs(S, clip, C, e.get("window"), tuple(ex)); r["source"] = e["source"]; r["rest_match"] = None; r["edits"] = e.get("edits", [])
            r["status"] = "PASS" if r["within"] else "FAIL"; out.append(r); continue
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



# LOOP SEAM and SOURCE GRID (N-C9 loop check, 2026-09-30) -- for every registry clip marked "loop": true.
# Found: the D2 Blender merge cut the T8 walk, run and idle on a 24 fps grid from t = 0 while Meshy keys
# at 30 fps from 0.0333 s -- a clamped hold on the first key, and a cut short of (walk) or past (run) the
# source's own cycle. The walk popped 9.96 cm / 11.3 deg at every wrap; the run's first interval moved
# 29% of a normal one (a hitch every cycle). Same defect D2 found in D7's run (collab b3fa2d725).
#   SOURCE GRID  every loop keys on its SOURCE'S OWN key times (its window, re-timed to start at 0) within
#                1e-4 s -- anything else was resampled. The source is the registry's `grid_source` or
#                `source`: a GLB (its sampler inputs) or an FBX (its KeyTime arrays, read here: the t2m
#                clips). NO convenience exceptions (coordinator ruling 2026-09-30): a loop whose source
#                cannot be read, or that names none, FAILS.
#   LOOP SEAM    pose(0) against pose(T) (s17_loop_closure.py's definition: every skin joint, world
#                metres; in place when the scene de-roots it -- net hips travel >= 0.25 m): within
#                SEAM_M and SEAM_DEG. No exceptions either: a source that is not periodic is BLENDED
#                (58_loop_blend.py), not excused.
SEAM_M, SEAM_DEG = 0.005, 1.0
KTIME = 46186158000                  # FBX time units per second


def fbx_key_times(path):
    """The FBX's animation key times (s): the KeyTime array most curves share. Binary FBX only -- each
    KeyTime property is an int64 array ('l'), raw or zlib-deflated."""
    import struct, zlib, re as _re
    b = open(path, 'rb').read()
    if not b.startswith(b'Kaydara FBX Binary'):
        raise ValueError("%s: not a binary FBX" % path)
    by = {}
    for m_ in _re.finditer(b'KeyTime', b):
        q = m_.end()
        if b[q:q + 1] != b'l':
            continue
        n, enc, clen = struct.unpack('<III', b[q + 1:q + 13])
        raw = b[q + 13:q + 13 + clen]
        data = zlib.decompress(raw) if enc == 1 else raw
        t = tuple(np.frombuffer(data, '<i8')[:n].tolist())
        by[t] = by.get(t, 0) + 1
    if not by:
        raise ValueError("%s: no KeyTime arrays" % path)
    best = max(by.items(), key=lambda kv: (kv[1], len(kv[0])))[0]
    return np.array(best, float) / KTIME


def _grid(m, clip):
    by = {}
    for (tt, vv) in m['anims'][clip].values():
        if len(tt) > 2:
            by.setdefault(len(tt), []).append(np.asarray(tt, float))
    return max(by.items(), key=lambda kv: (len(kv[1]), kv[0]))[1][0]


def seam(S, clip):
    """closure (m, deg, joint), first interval / median, the grid, T"""
    m = S.m
    g = _grid(m, clip)
    T = max(float(tt[-1]) for (tt, vv) in m['anims'][clip].values())
    ks = list(g) + ([T] if abs(float(g[-1]) - T) > 1e-4 else [])
    h = m['nid']['Hips']
    js_ = sorted(set(j for j, nd in enumerate(m['nodes']) if nd.get('name') in S.joint_names))
    def pose(t):
        G = globals_at(m, clip, float(t))
        return {j: G[j] for j in js_}, G[h][:3, 3]
    P0, h0 = pose(ks[0]); P1, h1 = pose(ks[-1])
    net = h1 - h0; net[1] = 0.0
    # world positions are metres already (the Armature node carries the scale)
    off = net if np.linalg.norm(net) >= 0.25 else np.zeros(3)
    d = {j: float(np.linalg.norm(P0[j][:3, 3] - (P1[j][:3, 3] - off))) for j in js_}
    def rd(A, B):
        a = _rot(A); b = _rot(B); c = (np.trace(a.T @ b) - 1) / 2
        return math.degrees(math.acos(max(-1.0, min(1.0, c))))
    r = {j: rd(P0[j], P1[j]) for j in js_}
    jw = max(d, key=d.get)
    pp = [pose(t)[0] for t in ks]
    st = [max(float(np.linalg.norm(pp[i][j][:3, 3] - pp[i + 1][j][:3, 3])) for j in js_) for i in range(len(pp) - 1)]
    med = float(np.median(st)) or 1e-9
    return dict(closure_m=round(d[jw], 5), closure_deg=round(max(r.values()), 3), closure_joint=m['nodes'][jw]['name'],
                first_frac=round(st[0] / med, 3), keys=len(ks), T_s=round(T, 4), grid=g)


def seams(ship_glb, reg=None):
    reg = reg if reg is not None else registry()
    S = Rig(ship_glb)
    js, _b = L.load_glb(ship_glb)
    S.joint_names = {js['nodes'][j].get('name') for sk in js.get('skins', []) for j in sk['joints']}
    root = os.path.dirname(HERE)
    out = []
    for clip, e in sorted(reg.get("clips", {}).items()):
        if not e.get("loop") or clip not in S.m['anims']:
            continue
        r = seam(S, clip)
        r['clip'] = clip
        # SOURCE GRID -- the grid source (an authored loop names the clip it is built on), else the source
        gs = e.get("grid_source") or e.get("source")
        src = os.path.join(root, gs) if gs else None
        r['grid_status'] = "NO SOURCE"
        sk = None
        if src and os.path.exists(src):
            if src.endswith(".glb"):
                C = Rig(src)
                sclip = next(iter(C.m['anims']))
                sk = np.array(sorted(set(round(float(x), 6) for (tt, vv) in C.m['anims'][sclip].values() for x in tt)))
            elif src.lower().endswith(".fbx"):
                sk = np.round(fbx_key_times(src), 6)
            else:
                r['grid_status'] = "UNREADABLE"
        elif src:
            r['grid_status'] = "MISSING"
        if sk is not None:
            win = e.get("grid_window") or e.get("window")
            if win:
                sk = sk[(sk >= float(win[0]) - 1e-4) & (sk <= float(win[1]) + 1e-4)]
            want = sk - sk[0]
            g = np.asarray(r['grid'], float)
            ok = len(g) == len(want) and float(np.abs(g - want).max()) <= 1e-4
            r['grid_status'] = "PASS" if ok else "FAIL"
            r['grid_note'] = "%d keys at %.4f s against the source's %d at %.4f s (%s)" % (
                len(g), float(np.median(np.diff(g))), len(want), float(np.median(np.diff(want))), os.path.basename(src))
        r.pop('grid')
        within = r['closure_m'] <= SEAM_M and r['closure_deg'] <= SEAM_DEG
        r['seam_status'] = "PASS" if within else "FAIL"
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
