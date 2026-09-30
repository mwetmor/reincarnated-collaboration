# T12 (c) chop re-source: GRAFT a Meshy library clip onto the body GLB as a new animation -- a
# binary glTF patch, no Blender round trip.
#
#   python3 scripts/55_clip_graft.py graft <body.glb> <out.glb> <name>=<anim.glb>[@<t0>:<t1>] ... [--json f]
#   python3 scripts/55_clip_graft.py compare <body.glb> <clip in the body> <anim.glb>
#
# WHY NOT 33_assemble. The body now carries binary-patched clips and channels (the guard poses,
# idle_guard, the weapon_r channel), and a Blender round trip re-exports all of them -- it has
# already resampled a clip 30 -> 24 fps and reordered the joints once. A new clip is a new
# animation and nothing else, so it is appended and every other byte is kept.
#
# THE RETARGET, per frame, per joint, in WORLD space. The fetched GLB is Meshy's own export of his
# rig, and its node rests are NOT the body's: the body went through the T8 fit (1.85 m) and
# Blender, and the two files' local rest rotations differ by up to ~120 deg for the same bone. What
# they share is the rest POSE -- the same A-pose in the same world. So each joint's rotation AWAY
# FROM REST, measured in world space, is carried across:
#     dW(t)      = R_src_world(t) . R_src_world_rest^-1
#     R_body(t)  = dW(t) . R_body_world_rest            (then back to local under the animated parent)
# The Hips' travel is carried the same way, scaled by the ratio of the two rigs' hip heights.
# `compare` checks the method against a clip the Blender chain already merged (attack_chop from
# axe_chop.glb): the world orientation of every bone, frame for frame where both have keys.
#
# HYGIENE, as 33_assemble applies it: no joint scale tracks (Meshy's Idle shipped a 1.176 Hips
# scale); the clip GROUNDED on its first frame (the lowest foot joint where the rest pose puts it);
# and, a one-shot, RECENTRED so its first frame's hips stand over the rest position (49_recentre's
# rule). Weapon bones get no track (rest: the mount). Optional trim [t0, t1], re-timed to start at 0.
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = __import__('21_lint_export')
R_ = __import__('49_recentre')
W = __import__('52_weapon_bones')

FEET = ["LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase"]


def qn(q):
    q = np.asarray(q, float)
    return q / np.linalg.norm(q)


def slerp(a, b, u):
    a = qn(a); b = qn(b)
    d = float(np.dot(a, b))
    if d < 0:
        b = -b; d = -d
    if d > 0.9995:
        return qn(a + u * (b - a))
    th = math.acos(d)
    return (math.sin((1 - u) * th) * a + math.sin(u * th) * b) / math.sin(th)


def tracks(js, bin_, anim):
    out = {}
    for ch in anim['channels']:
        s = anim['samplers'][ch['sampler']]
        t = L.read_accessor(js, bin_, s['input']).reshape(-1)
        v = L.read_accessor(js, bin_, s['output'])
        out.setdefault(ch['target']['node'], {})[ch['target']['path']] = (t, v, s.get('interpolation', 'LINEAR'))
    return out


def sample(tr, t, path):
    tt, vv, interp = tr
    if t <= tt[0]:
        return vv[0].copy()
    if t >= tt[-1]:
        return vv[-1].copy()
    i = int(np.searchsorted(tt, t, side='right')) - 1
    if interp == 'STEP':
        return vv[i].copy()
    u = (t - tt[i]) / max(tt[i + 1] - tt[i], 1e-12)
    if path == 'rotation':
        return slerp(vv[i], vv[i + 1], u)
    return vv[i] + u * (vv[i + 1] - vv[i])


def local_mats(js, trk, t, skip_scale=False):
    """Every node's local 4x4 at time t (rest where the clip has no track)."""
    M = []
    for i, nd in enumerate(js['nodes']):
        if 'matrix' in nd:
            M.append(W.trs(nd)); continue
        T = np.array(nd.get('translation', [0, 0, 0]), float)
        Rq = np.array(nd.get('rotation', [0, 0, 0, 1]), float)
        S = np.array(nd.get('scale', [1, 1, 1]), float)
        if i in trk:
            if 'translation' in trk[i]: T = sample(trk[i]['translation'], t, 'translation')
            if 'rotation' in trk[i]: Rq = sample(trk[i]['rotation'], t, 'rotation')
            if 'scale' in trk[i] and not skip_scale: S = sample(trk[i]['scale'], t, 'scale')
        m = np.eye(4); m[:3, :3] = W.q2m(qn(Rq)) @ np.diag(S); m[:3, 3] = T
        M.append(m)
    return M


def globals_from(js, M):
    parent = {c: i for i, nd in enumerate(js['nodes']) for c in nd.get('children', [])}
    G = {}

    def g(i):
        if i not in G:
            G[i] = M[i] if parent.get(i) is None else g(parent[i]) @ M[i]
        return G[i]
    for i in range(len(js['nodes'])):
        g(i)
    return G, parent


def rot(m):
    r = m[:3, :3]
    u, _, vt = np.linalg.svd(r)
    q = u @ vt
    if np.linalg.det(q) < 0:
        u[:, -1] *= -1; q = u @ vt
    return q


def joints(js):
    return [js['nodes'][j]['name'] for j in js['skins'][0]['joints']]


def world_rest(js):
    G, parent = globals_from(js, [W.trs(nd) for nd in js['nodes']])
    return G, parent


def retarget(body_js, src_js, src_bin, anim, times, skip_scale=True):
    """Local rotations for the body's joints (and the Hips translation) at each source time."""
    bname = {nd.get('name'): i for i, nd in enumerate(body_js['nodes'])}
    sname = {nd.get('name'): i for i, nd in enumerate(src_js['nodes'])}
    common = [n for n in joints(body_js) if n in sname and n in set(joints(src_js))]
    Gb0, bpar = world_rest(body_js)
    Gs0, _ = world_rest(src_js)
    trk = tracks(src_js, src_bin, anim)
    hips_b, hips_s = bname['Hips'], sname['Hips']
    # the hip-height ratio (world rest, above each rig's lowest rest foot joint)
    def lowest(G, nm):
        return min(G[nm[f]][1, 3] for f in FEET)
    hb = Gb0[hips_b][1, 3] - lowest(Gb0, bname); hs = Gs0[hips_s][1, 3] - lowest(Gs0, sname)
    k = hb / hs
    # hierarchy order over the body's joints
    order = []
    seen = set()
    def visit(i):
        if i in seen: return
        p = bpar.get(i)
        if p is not None and body_js['nodes'][p].get('name') in common: visit(p)
        seen.add(i); order.append(i)
    for n in common: visit(bname[n])
    out = {n: [] for n in common}
    hips_T = []
    for t in times:
        Gs, _ = globals_from(src_js, local_mats(src_js, trk, t, skip_scale))
        Rw = {}
        for i in order:
            n = body_js['nodes'][i]['name']
            dW = rot(Gs[sname[n]]) @ rot(Gs0[sname[n]]).T
            Rw[i] = dW @ rot(Gb0[i])
            p = bpar.get(i)
            Rp = Rw[p] if p in Rw else rot(Gb0[p])
            out[n].append(W.m2q(Rp.T @ Rw[i]))
        # the Hips' travel: the source's world displacement from rest, scaled to the body
        d = (Gs[hips_s][:3, 3] - Gs0[hips_s][:3, 3]) * k
        pb = Gb0[hips_b][:3, 3] + d
        P = Gb0[bpar[hips_b]]
        hips_T.append((np.linalg.inv(P) @ np.append(pb, 1.0))[:3])
    return common, out, np.array(hips_T), k


def body_world(js, trk_local, t):
    """World matrices of the body's nodes for a clip given as {node: {path: (t, v, interp)}}."""
    G, _ = globals_from(js, local_mats(js, trk_local, t))
    return G


def graft(body, out, specs, outj=None):
    js, bin_ = L.load_glb(body)
    bin_ = bytearray(bin_)
    bname = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
    Gb0, bpar = world_rest(js)
    rep = {}
    for spec in specs:
        name, rest = spec.split('=', 1)
        src, t0, t1 = rest, None, None
        if '@' in rest:
            src, win = rest.split('@', 1)
            t0, t1 = [float(x) for x in win.split(':')]
        sjs, sbin = L.load_glb(src)
        anim = sjs['animations'][0]
        st = tracks(sjs, sbin, anim)
        allt = sorted(set(float(x) for tr in st.values() for (tt, _, _) in tr.values() for x in tt))
        a, b = (t0 if t0 is not None else allt[0]), (t1 if t1 is not None else allt[-1])
        times = [x for x in allt if a - 1e-6 <= x <= b + 1e-6]
        common, rots, hipsT, k = retarget(js, sjs, sbin, anim, times)
        times = np.array(times) - times[0]
        # GROUND on the first frame, RECENTRE the first frame's hips over the rest position
        hips = bname['Hips']
        trk_body = {bname[n]: {'rotation': (times, np.array(rots[n]), 'LINEAR')} for n in common}
        trk_body[hips]['translation'] = (times, hipsT, 'LINEAR')
        G = body_world(js, trk_body, 0.0)
        low0 = min(G[bname[f]][1, 3] for f in FEET)
        lowr = min(Gb0[bname[f]][1, 3] for f in FEET)
        dy_w = lowr - low0
        dxz_w = Gb0[hips][:3, 3] - G[hips][:3, 3]
        shift_w = np.array([dxz_w[0], dy_w, dxz_w[2]])
        P = rot(Gb0[bpar[hips]])
        sc = np.cbrt(np.linalg.det(Gb0[bpar[hips]][:3, :3]))
        shift_l = (P.T @ shift_w) / sc
        hipsT = hipsT + shift_l
        # APPEND the animation
        ch, sm = [], []
        def acc(arr, typ):
            arr = np.asarray(arr, np.float32)
            data = arr.tobytes()
            off = W.append(bin_, data)
            js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
            a_ = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
            if typ == "SCALAR":
                a_["min"] = [float(arr.min())]; a_["max"] = [float(arr.max())]
            js['accessors'].append(a_)
            return len(js['accessors']) - 1
        ti = acc(times.reshape(-1), "SCALAR")
        for n in common:
            q = np.array(rots[n])
            for j in range(1, len(q)):
                if np.dot(q[j], q[j - 1]) < 0: q[j] = -q[j]
            sm.append({"input": ti, "output": acc(q, "VEC4"), "interpolation": "LINEAR"})
            ch.append({"sampler": len(sm) - 1, "target": {"node": bname[n], "path": "rotation"}})
        sm.append({"input": ti, "output": acc(hipsT, "VEC3"), "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": hips, "path": "translation"}})
        js['animations'] = [an for an in js['animations'] if an.get('name') != name]
        js['animations'].append({"name": name, "channels": ch, "samplers": sm})
        rep[name] = dict(source=os.path.basename(src), source_anim=anim.get('name'), window=[a, b], keys=len(times),
                         length_s=float(times[-1]), joints=len(common), hip_ratio=float(k),
                         grounded_by_m=float(dy_w), recentred_by_m=[float(dxz_w[0]), float(dxz_w[2])])
        print("graft: %-16s <- %s %s [%.3f, %.3f] s: %d keys, %.3f s, %d joints; hips x%.4f; grounded %+.4f, recentred %+.4f/%+.4f (world units)"
              % (name, os.path.basename(src), anim.get('name'), a, b, len(times), times[-1], len(common), k, dy_w, dxz_w[0], dxz_w[2]))
    js['buffers'][0]['byteLength'] = len(bin_)
    R_.write_glb(out, js, bin_)
    res = L.lint(out)
    print("lint %s, %d fails %s" % (res['verdict'], len(res['fails']), res['fails'][:3]))
    if outj:
        json.dump(dict(clips=rep, lint=dict(verdict=res['verdict'], fails=res['fails'], warns=len(res['warns']))), open(outj, 'w'), indent=1)
    return rep


def compare(body, clip, src):
    """The method against the Blender chain: world orientation of every bone, frame for frame."""
    js, bin_ = L.load_glb(body)
    sjs, sbin = L.load_glb(src)
    an = next(a for a in js['animations'] if a['name'] == clip)
    bt = tracks(js, bin_, an)
    tb = sorted(set(float(x) for tr in bt.values() for (tt, _, _) in tr.values() for x in tt))
    st = tracks(sjs, sbin, sjs['animations'][0])
    ts = sorted(set(float(x) for tr in st.values() for (tt, _, _) in tr.values() for x in tt))
    common_t = [t for t in tb if any(abs(t - u) < 1e-4 for u in ts)]
    common, rots, hipsT, k = retarget(js, sjs, sbin, sjs['animations'][0], common_t)
    bname = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
    errs = {n: [] for n in common}
    for j, t in enumerate(common_t):
        Gb = body_world(js, bt, t)
        mine = {bname[n]: {'rotation': (np.array([0.0]), np.array([rots[n][j]]), 'LINEAR')} for n in common}
        Gm = body_world(js, mine, 0.0)
        for n in common:
            Ra, Rb = rot(Gb[bname[n]]), rot(Gm[bname[n]])
            c = (np.trace(Ra @ Rb.T) - 1) / 2
            errs[n].append(math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    print("compare '%s' (Blender chain) vs the world-space graft of %s: %d common key times" % (clip, os.path.basename(src), len(common_t)))
    worst = 0.0
    for n in common:
        e = np.array(errs[n]); worst = max(worst, e.max())
        print("  %-14s world orientation diff median %6.2f  p95 %6.2f  max %6.2f deg" % (n, np.median(e), np.percentile(e, 95), e.max()))
    print("  worst %.2f deg" % worst)


if __name__ == "__main__":
    a = sys.argv[1:]
    outj = a[a.index('--json') + 1] if '--json' in a else None
    a = [x for i, x in enumerate(a) if x != '--json' and (i == 0 or a[i - 1] != '--json')]
    if a[0] == 'graft':
        graft(a[1], a[2], a[3:], outj)
    elif a[0] == 'compare':
        compare(a[1], a[2], a[3])
    else:
        sys.exit("usage: graft|compare ...")
