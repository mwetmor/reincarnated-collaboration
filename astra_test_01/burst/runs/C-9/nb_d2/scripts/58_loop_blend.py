# LOOP BLEND: a loop whose SOURCE is not periodic, made one -- on the source's own key times, its
# source timing restored, the seam cross-faded where the feet slide least.
#
#   python3 scripts/58_loop_blend.py search <body.glb> <clip> --dir x,y,z [--retime f] [--lmin n] [--lmax n] [--json f]
#   python3 scripts/58_loop_blend.py build  <body.glb> <out.glb> <clip>=<a>:<b>:<w>:<mode>:<dx,dy,dz> ... [--retime f] [--json f]
#
# THE CLIPS (N-C9 loop check, coordinator ruling 2026-09-30): strafe_L_armed, strafe_R_armed and
# run_armed are text-to-motion (SMPL-H through 41_retarget_smplh). The t2m FBX keys at 30 fps (60
# frames, 0 .. 1.9667 s); the chain placed those frames 1:1 on Blender's 24 fps timeline, so they
# shipped 1.25x slow (--retime 0.8 restores the source's own clock: every key time x 24/30). And the
# source is NOT periodic: no window on its own frames closes (strafe_L's best 9.99 cm / 25.8 deg), so
# a re-cut cannot make it loop -- the seam has to be BLENDED.
#
# A CANDIDATE is a window [a, b] on the clip's own keys (the loop is b - a intervals; it keeps the
# source's key times, re-timed to start at 0 -- the SOURCE GRID rule), a blend length w (intervals)
# and a mode:
#   pre     the last w intervals cross-fade into the frames BEFORE a (the source's own lead-in):
#               out(k) = blend(src(a+k), src(a+k-L), s(u)),  u = (k-(L-w))/w,  k in [L-w, L]
#   post    the first w intervals cross-fade out of the frames AFTER b (the source's own run-on):
#               out(k) = blend(src(b+k), src(a+k), s(k/w)),  k in [0, w]
#   offset  no frames outside the window (run_armed ships one trimmed cycle): the last w intervals
#           carry a growing correction that takes src(b) onto src(a):  q' = slerp(1, q_a q_b^-1, s) q
# s is smoothstep, so out(L) == out(0) EXACTLY in every mode (the loop closes to the bit) and the
# velocity has no corner at the joins. Rotations slerp per joint in the local frame; the Hips
# translation is first RE-DE-ROOTED over the window (its own first-to-last horizontal line removed,
# the export's rule applied to the window), so the loop stands in place and the cross-fade never has
# to pull the body back across the ground.
#
# THE OBJECTIVE is foot slide, measured the way the scene sees it: the body driven at the loop's
# FOOT-LOCK speed (57_footlock.py's rule since T12_11, the scene's: the stance side is the lower toe
# within 3 cm of its lowest, that side's foot joint's backward velocity, the median over stance
# intervals, sides pooled -- at the loop's keys; T12_10 used s6's bottom-25% rule, kept as
# LOOP_BLEND_RULE=s6 to reproduce its numbers) along --dir; a TOE is planted when it
# is within 3 cm of its lowest and its height changes <= 1 cm (tools/speed_split.gd's rule); its slide
# is its horizontal travel over the interval. Minimised: the worst planted slide INSIDE the blend,
# then the loop's p95. A loop shorter than --lmin or longer than --lmax intervals is not considered.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
G55 = __import__('55_clip_graft')
R_ = __import__('49_recentre')

FEET = ["LeftFoot", "RightFoot"]
TOES = ["LeftToeBase", "RightToeBase"]


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def qslerp(a, b, u):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if np.dot(a, b) < 0:
        b = -b
    return G55.slerp(a, b, u)


def qmul(a, b):
    x1, y1, z1, w1 = a; x2, y2, z2, w2 = b
    return np.array([w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2])


def qinv(q):
    return np.array([-q[0], -q[1], -q[2], q[3]]) / float(np.dot(q, q))


class Clip:
    def __init__(self, js, bin_, name, retime=1.0):
        self.js, self.bin_, self.name = js, bin_, name
        self.an = next(a for a in js['animations'] if a['name'] == name)
        tr = G55.tracks(js, bin_, self.an)
        grids = [t for d in tr.values() for (t, v, i) in d.values() if len(t) > 2]
        g = grids[0]
        for t in grids:
            assert len(t) == len(g) and np.allclose(t, g, atol=1e-5), "%s: multi-key tracks on different grids" % name
        self.times = np.asarray(g, float) * retime
        self.dt = float(np.median(np.diff(self.times)))
        self.multi = {(n, p): np.asarray(v, float) for n, d in tr.items() for p, (t, v, i) in d.items() if len(t) > 2}
        self.const = {}
        for n, d in tr.items():
            for p, (t, v, i) in d.items():
                if len(t) <= 2:
                    # the export's 2-key "constant" tracks carry Blender's float drift (~1e-5 units, 0.1 um):
                    # anything more than 1e-3 units (11 um) is a track that moves, and is refused
                    assert np.allclose(v[0], v[-1], atol=1e-3), "%s: a 2-key track that moves (%s)" % (name, p)
                    self.const[(n, p)] = np.asarray(v[0], float)
        self.nid = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
        self.hips = self.nid['Hips']
        self.n = len(self.times)

    def hip_rd(self, a, b):
        """The Hips translation re-de-rooted over [a, b]: its own first-to-last HORIZONTAL line removed."""
        H = self.multi[(self.hips, 'translation')]
        d = H[b] - H[a]; d = np.array([d[0], 0.0, d[2]])
        L_ = b - a
        return lambda i: H[i] - d * (i - a) / L_

    def frame(self, i, hip):
        f = {k: v[i].copy() for k, v in self.multi.items()}
        f[(self.hips, 'translation')] = hip(i)
        return f

    def loop(self, a, b, w, mode):
        """The loop's frames 0..L (L = b - a): a list of {(node, path): value}."""
        L_ = b - a
        hip = self.hip_rd(a, b)
        out = []
        fa, fb = self.frame(a, hip), self.frame(b, hip)
        for k in range(L_ + 1):
            f = self.frame(a + k, hip)
            if mode == 'pre' and k >= L_ - w:
                s = smooth((k - (L_ - w)) / w)
                f = blend(f, self.frame(a + k - L_, hip), s)
            elif mode == 'post' and k <= w:
                s = smooth(k / w)
                f = blend(self.frame(b + k, hip), f, s)
            elif mode == 'offset' and k >= L_ - w:
                s = smooth((k - (L_ - w)) / w)
                g = {}
                for key, v in f.items():
                    if key[1] == 'rotation':
                        dq = qmul(fa[key], qinv(fb[key]))
                        g[key] = qmul(qslerp(np.array([0, 0, 0, 1.0]), dq, s), v)
                        g[key] /= np.linalg.norm(g[key])
                    else:
                        g[key] = v + s * (fa[key] - fb[key])
                f = g
            out.append(f)
        return out

    def feasible(self, a, b, w, mode):
        L_ = b - a
        if w < 1 or w > L_ // 2:
            return False
        if mode == 'pre':
            return a - w >= 0
        if mode == 'post':
            return b + w <= self.n - 1
        return mode == 'offset'


def blend(f0, f1, s):
    out = {}
    for key, v in f0.items():
        out[key] = qslerp(v, f1[key], s) if key[1] == 'rotation' else (1 - s) * v + s * f1[key]
    return out


def loop_tracks(clip, frames):
    n = len(frames)
    t = np.arange(n) * clip.dt
    trk = {}
    for key in frames[0]:
        vals = np.array([f[key] for f in frames])
        trk.setdefault(key[0], {})[key[1]] = (t, vals, 'LINEAR')
    for key, v in clip.const.items():
        trk.setdefault(key[0], {})[key[1]] = (np.array([0.0, t[-1]]), np.array([v, v]), 'LINEAR')
    return trk, t


def positions(clip, trk, t, names):
    idx = [clip.nid[nm] for nm in names]
    P = []
    for tt in t:
        G = G55.body_world(clip.js, trk, float(tt))
        P.append([G[i][:3, 3] for i in idx])
    return np.array(P)                     # (frames, joints, 3), metres (the Armature carries the scale)


def metrics(P, t, dirv, blend_iv, gait='walk'):
    """P: (frames, 4, 3) for LeftFoot, RightFoot, LeftToeBase, RightToeBase; blend_iv: the interval indices inside
    the blend. The foot-lock speed (s6's definition, the foot joints), then, with the body driven at it along dirv:
      SUPPORT  the lower toe, the same foot at both ends of the interval: its horizontal travel in the world. A
               walking gait always has a support foot, so every interval is judged and a blend cannot score well by
               landing where nothing counts as planted. (The text-to-motion toes never sit at one height through a
               stance -- strafe_L's left toe sinks 5 cm across its stance -- so the scene probe's 3 cm / 1 cm pair
               rule finds 6 pairs in a 50-interval loop; it is reported, PROBE, not used to choose.)
    in mm per key interval (1/30 s at source timing)."""
    dt = np.diff(t)
    vs = []
    if os.environ.get("LOOP_BLEND_RULE") == "s6":
        for j in (0, 1):
            y = P[:, j, 1]; lo, hi = float(y.min()), float(y.max())
            c = y <= lo + 0.25 * (hi - lo)
            for i in range(len(t) - 1):
                if c[i] and c[i + 1]:
                    vs.append(float(-(P[i + 1, j] - P[i, j]) @ dirv / dt[i]))
    else:
        # the scene's rule (57_footlock.py, T12_11): stance side = the lower toe within 3 cm of its lowest
        tlo = (float(P[:, 2, 1].min()), float(P[:, 3, 1].min()))
        for i in range(len(t) - 1):
            k = 0 if P[i, 2, 1] <= P[i, 3, 1] else 1
            if P[i, 2 + k, 1] <= tlo[k] + 0.03:
                vs.append(float(-(P[i + 1, k] - P[i, k]) @ dirv / dt[i]))
    v = float(np.median(vs)) if vs else 0.0
    Wd = P + v * dirv[None, None, :] * t[:, None, None]
    fy = float(min(P[:, 2, 1].min(), P[:, 3, 1].min()))
    low = np.where(P[:, 2, 1] <= P[:, 3, 1], 2, 3)
    sup_in, sup_all, probe = [], [], 0
    for i in range(len(t) - 1):
        if low[i] != low[i + 1]:
            continue
        j = int(low[i]); ha, hb = P[i, j, 1], P[i + 1, j, 1]
        d = Wd[i + 1, j] - Wd[i, j]
        s_ = float(np.hypot(d[0], d[2])) * 1000
        is_probe = ha <= fy + 0.03 and hb <= fy + 0.03 and abs(ha - hb) <= 0.010
        probe += 1 if is_probe else 0
        if gait == 'run' and not is_probe:
            continue                     # RUN: a flight phase has no support foot -- the probe's rule only
        sup_all.append(s_)
        if i in blend_iv:
            sup_in.append(s_)
    out_ = [s_ for s_ in sup_all]
    return dict(footlock_m_s=round(v, 4), support_pairs=len(sup_all), probe_pairs=probe,
                blend_support_max_mm=round(max(sup_in), 2) if sup_in else None,
                blend_support_med_mm=round(float(np.median(sup_in)), 2) if sup_in else None, blend_support_pairs=len(sup_in),
                loop_slide_med_mm=round(float(np.median(out_)), 2) if out_ else None,
                loop_slide_p95_mm=round(float(np.percentile(out_, 95)), 2) if out_ else None,
                loop_slide_max_mm=round(max(out_), 2) if out_ else None,
                blend_intervals=len(blend_iv))


def blend_intervals(L_, w, mode):
    if mode == 'post':
        return set(range(0, w))
    return set(range(L_ - w, L_))


def evaluate(clip, a, b, w, mode, dirv, names=FEET + TOES, gait='walk'):
    frames = clip.loop(a, b, w, mode)
    trk, t = loop_tracks(clip, frames)
    P = positions(clip, trk, t, names)
    m = metrics(P, t, dirv, blend_intervals(b - a, w, mode), gait)
    m.update(a=a, b=b, w=w, mode=mode, L=b - a, seconds=round(float(t[-1]), 4), gait=gait)
    return m


def search(body, name, dirv, retime, lmin, lmax, outj=None, gait='walk'):
    js, bin_ = L.load_glb(body)
    c = Clip(js, bytes(bin_), name, retime)
    lmax = min(lmax, c.n - 1)
    res = []
    for mode in ('pre', 'post', 'offset'):
        for a in range(0, c.n):
            for L_ in range(lmin, lmax + 1):
                b = a + L_
                if b > c.n - 1:
                    break
                for w in (3, 4, 6, 8, 10, 12, 16, 20):
                    if not c.feasible(a, b, w, mode):
                        continue
                    res.append(evaluate(c, a, b, w, mode, dirv, gait=gait))
    # a blend with NO support pairs (the support toe above 5 cm through it) is not scored as slide-free: refused
    res = [r for r in res if r['blend_support_pairs'] > 0 and r['loop_slide_p95_mm'] is not None]
    key = lambda r: (r['blend_support_max_mm'] + 0.5 * r['loop_slide_p95_mm'], r['loop_slide_p95_mm'])
    res.sort(key=key)
    print("%s: %d keys at %.4f s (retime x%.3f); %d candidates (L %d..%d intervals)" % (name, c.n, c.dt, retime, len(res), lmin, lmax))
    for r in res[:12]:
        print("  %-6s a %2d b %2d (L %2d = %.4f s) w %2d | foot-lock %.3f m/s | blend: support slide max %.1f med %.1f mm (%d of %d intervals) | loop support med %.1f p95 %.1f max %.1f mm (%d intervals)"
              % (r['mode'], r['a'], r['b'], r['L'], r['seconds'], r['w'], r['footlock_m_s'], r['blend_support_max_mm'], r['blend_support_med_mm'],
                 r['blend_support_pairs'], r['blend_intervals'], r['loop_slide_med_mm'], r['loop_slide_p95_mm'], r['loop_slide_max_mm'], r['support_pairs']))
    if outj:
        json.dump(dict(clip=name, retime=retime, dir=list(map(float, dirv)), best=res[:40], candidates=len(res)), open(outj, 'w'), indent=1)
    return res


def build(body, out, specs, retime, outj=None, gaits=None):
    js, b0 = L.load_glb(body)
    bin_ = bytearray(b0)
    rep = {}
    for spec in specs:
        name, rest = spec.split('=', 1)
        a, b, w, mode, dd = rest.split(':')
        a, b, w = int(a), int(b), int(w)
        dirv = np.array([float(x) for x in dd.split(',')])
        c = Clip(js, bytes(bin_), name, retime)
        assert c.feasible(a, b, w, mode), spec
        m = evaluate(c, a, b, w, mode, dirv, gait=(gaits or {}).get(name, 'walk'))
        frames = c.loop(a, b, w, mode)
        trk, t = loop_tracks(c, frames)
        # the new animation: every channel of the old one, same targets, the loop's values
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
        ti = acc(t.reshape(-1), "SCALAR")
        t2 = acc(np.array([0.0, t[-1]]), "SCALAR")
        for och in c.an['channels']:
            node, path = och['target']['node'], och['target']['path']
            tt, vv, interp = trk[node][path]
            if len(tt) == 2:
                sm.append({"input": t2, "output": acc(vv, "VEC4" if path == 'rotation' else "VEC3"), "interpolation": "LINEAR"})
            else:
                vv = np.array(vv, float)
                if path == 'rotation':
                    for j in range(1, len(vv)):
                        if np.dot(vv[j], vv[j - 1]) < 0:
                            vv[j] = -vv[j]
                sm.append({"input": ti, "output": acc(vv, "VEC4" if path == 'rotation' else "VEC3"), "interpolation": "LINEAR"})
            ch.append({"sampler": len(sm) - 1, "target": {"node": node, "path": path}})
        js['animations'] = [an for an in js['animations'] if an.get('name') != name]
        js['animations'].append({"name": name, "channels": ch, "samplers": sm})
        m.update(source_keys=[round(float(c.times[a]), 6), round(float(c.times[b]), 6)], keys=len(t), retime=retime,
                 dir=list(map(float, dirv)))
        rep[name] = m
        print("build: %-15s %s a %d b %d w %d -> %d keys, %.4f s | foot-lock %.3f m/s | blend support slide max %s med %s mm | loop support med %s p95 %s max %s mm"
              % (name, mode, a, b, w, len(t), t[-1], m['footlock_m_s'], m['blend_support_max_mm'], m['blend_support_med_mm'],
                 m['loop_slide_med_mm'], m['loop_slide_p95_mm'], m['loop_slide_max_mm']))
    js['buffers'][0]['byteLength'] = len(bin_) + (-len(bin_) % 4)
    R_.write_glb(out, js, bin_)
    res = L.lint(out)
    print("lint %s, %d fails %s" % (res['verdict'], len(res['fails']), res['fails'][:3]))
    if outj:
        json.dump(dict(clips=rep, lint=dict(verdict=res['verdict'], fails=res['fails'])), open(outj, 'w'), indent=1)
    return rep


def before(body, name, dirv, retime=1.0, gait='walk'):
    """The clip AS IT SHIPS, looped the way the scene loops it: frames 0..N-1 and then the wrap, N-1 -> 0."""
    js, bin_ = L.load_glb(body)
    c = Clip(js, bytes(bin_), name, retime)
    hip = lambda i: c.multi[(c.hips, 'translation')][i]
    frames = [c.frame(i, hip) for i in range(c.n)]
    trk, t = loop_tracks(c, frames)
    P = positions(c, trk, t, FEET + TOES)
    # append the wrap: the pose after T is frame 0 again, one key later
    P2 = np.concatenate([P, P[:1]], axis=0)
    t2 = np.concatenate([t, [t[-1] + c.dt]])
    m = metrics(P2, t2, dirv, {len(t2) - 2}, gait)
    m.update(clip=name, keys=c.n, seconds=round(float(t[-1]), 4), retime=retime, gait=gait)
    return m


if __name__ == '__main__':
    a = sys.argv[1:]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    retime = float(opt('--retime', 1.0))
    outj = opt('--json')
    if a[0] == 'search':
        dirv = np.array([float(x) for x in opt('--dir').split(',')])
        search(a[1], a[2], dirv, retime, int(opt('--lmin', 10)), int(opt('--lmax', 999)), outj, opt('--gait', 'walk'))
    elif a[0] == 'before':
        dirv = np.array([float(x) for x in opt('--dir').split(',')])
        r = before(a[1], a[2], dirv, retime, opt('--gait', 'walk'))
        print(json.dumps(r))
    elif a[0] == 'build':
        specs = [x for x in a[3:] if '=' in x and not x.startswith('--')]
        build(a[1], a[2], specs, retime, outj)
