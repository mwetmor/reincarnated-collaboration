# R-C9-138: the orb staff GRIPPED and AIMED along her facing, and a calmer idle, as BINARY ACCESSOR PATCHES on the body GLB
# (no Blender round trip: no resample, every clip not named stays byte-identical in its channels).
#
#   python3 r138_02_edit.py <in.glb> <out.glb> <orbstaff.glb> [ops...] [--json rep.json]
# ops (applied in order):
#   copy=<dst>:<src.glb>:<src_clip>      replace/add clip <dst> with <src_clip>'s JOINT channels from another GLB on the
#                                        same body (same node names; the grafted Mixamo idles); weapon bones get no track
#   pitch=<clip>:<bone>:<deg>            pre-rotate <bone>'s WORLD rotation about her lateral axis (+X) by deg at every key
#                                        (+ = lean FORWARD); everything below the bone follows
#   aim=<clip>:<mode>[:<elev>[:<w0>:<w1>:<w2>:<w3>]]
#        mode loop   : the haft (grip -> orb) aimed at her facing (+Z) raised <elev> deg, at every key
#        mode lead   : <elev> if given, else the clip's own orb elevation kept; the azimuth swung to her facing; weight ramps 0 at w0 -> 1 at w1,
#                      held to w2, back to 0 at w3 (seconds) -- casts: the orb LEADS toward the target over the thrust
#      THE GRIP IS NOT EDITED: the haft stays where the fist holds it (weapon_r's own keys, untouched). The HAND turns, and the
#      forearm takes half of the twist about its own axis (the gauntlet covers both): world twist about the forearm axis
#      chosen to bring the haft nearest the target, then the residual swing at the wrist, clamped to MAX_SWING deg.
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); C = __import__('s17_loop_closure')
R_ = __import__('49_recentre')
MAX_SWING = 30.0
MAX_TWIST = 100.0
FA_SHARE = 0.5

a = sys.argv[1:]
IN, OUT, STAFF = a[0], a[1], a[2]
REP = a[a.index('--json') + 1] if '--json' in a else None
ops = [x for i, x in enumerate(a[3:], 3) if '=' in x and not x.startswith('--') and a[i - 1] != '--json']
js, bin_ = L.load_glb(IN); bin_ = bytearray(bin_)
nid = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
parent = {c: i for i, nd in enumerate(js['nodes']) for c in nd.get('children', [])}
rep = {'in': IN, 'ops': [], 'clips': {}}


def acc(arr, typ):
    arr = np.asarray(arr, np.float32); data = arr.tobytes(); off = W.append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    a_ = {"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(arr.shape[0]), "type": typ}
    if typ == "SCALAR": a_["min"] = [float(arr.min())]; a_["max"] = [float(arr.max())]
    js['accessors'].append(a_); return len(js['accessors']) - 1


def anim(name):
    return next((an for an in js['animations'] if an.get('name') == name), None)


def model():
    # a fresh evaluator over the CURRENT js/bin (after earlier ops)
    js['buffers'][0]['byteLength'] = len(bin_)
    tmp = OUT + '.tmp.glb'; R_.write_glb(tmp, js, bin_); m = C.model(tmp); os.remove(tmp); return m


def set_rot_track(an, node, times, quats):
    q = np.array(quats, float)
    for j in range(1, len(q)):
        if np.dot(q[j], q[j - 1]) < 0: q[j] = -q[j]
    ti = acc(np.asarray(times, float).reshape(-1), "SCALAR"); oi = acc(q, "VEC4")
    an['samplers'].append({"input": ti, "output": oi, "interpolation": "LINEAR"})
    si = len(an['samplers']) - 1
    for ch in an['channels']:
        if ch['target']['node'] == node and ch['target']['path'] == 'rotation':
            ch['sampler'] = si; return
    an['channels'].append({"sampler": si, "target": {"node": node, "path": "rotation"}})


def key_times(m, clip):
    return sorted({float(t) for v in m['anims'][clip].values() for t in v[0]})


def rotn(M):
    R = M[:3, :3]; return R / np.linalg.norm(R, axis=0)


def staff_axis_local():
    sj, sb = L.load_glb(STAFF)
    _, A = W.hand_points(sj, sb, 'weapon_r', wmin=-1.0)
    c = A.mean(0); _, _, vt = np.linalg.svd(A - c, full_matrices=False); ax = vt[0]; s = (A - c) @ ax
    def rad(mask):
        Q = A[mask] - c; Q = Q - np.outer(Q @ ax, ax); return float(np.linalg.norm(Q, axis=1).max())
    if rad(s < np.percentile(s, 15)) > rad(s > np.percentile(s, 85)): ax = -ax; s = -s
    return c + ax * s.min(), c + ax * s.max()


BUTT, TIP = staff_axis_local()


def haft_world(G):
    Wm = G[nid['weapon_r']]
    t = (Wm @ np.append(TIP, 1))[:3]; b = (Wm @ np.append(BUTT, 1))[:3]
    v = t - b; return v / np.linalg.norm(v)


def op_copy(dst, src, sclip):
    sj, sb = L.load_glb(src); sb = bytes(sb)
    san = next(an for an in sj['animations'] if an.get('name') == sclip)
    snames = {i: nd.get('name') for i, nd in enumerate(sj['nodes'])}
    new = {"name": dst, "channels": [], "samplers": []}
    for ch in san['channels']:
        nm = snames[ch['target']['node']]
        if nm not in nid or nm.startswith('weapon'): continue
        s = san['samplers'][ch['sampler']]
        tt = L.read_accessor(sj, sb, s['input'])[:, 0]; vv = L.read_accessor(sj, sb, s['output'])
        new['samplers'].append({"input": acc(tt, "SCALAR"), "output": acc(vv, {3: "VEC3", 4: "VEC4"}[vv.shape[1]]),
                                "interpolation": s.get('interpolation', 'LINEAR')})
        new['channels'].append({"sampler": len(new['samplers']) - 1, "target": {"node": nid[nm], "path": ch['target']['path']}})
    js['animations'] = [an for an in js['animations'] if an.get('name') != dst] + [new]
    rep['ops'].append(dict(op='copy', dst=dst, src=os.path.basename(src), clip=sclip, channels=len(new['channels'])))
    print('copy %s <- %s:%s (%d channels)' % (dst, os.path.basename(src), sclip, len(new['channels'])))


def op_pitch(clip, bone, deg):
    m = model(); tt = key_times(m, clip); b = nid[bone]; p = parent[b]
    Rx = W.axis_angle([1, 0, 0], math.radians(deg)); qs = []
    for t in tt:
        G = C.globals_at(m, clip, t)
        Rw = Rx @ rotn(G[b]); qs.append(W.m2q(rotn(G[p]).T @ Rw))
    set_rot_track(anim(clip), b, tt, qs)
    rep['ops'].append(dict(op='pitch', clip=clip, bone=bone, deg=deg, keys=len(tt)))
    print('pitch %s %s %+.1f deg over %d keys' % (clip, bone, deg, len(tt)))


def twist_to(f, a_, t_):
    """the angle about unit f bringing a_ nearest t_"""
    pa = a_ - f * (a_ @ f); pt = t_ - f * (t_ @ f)
    if np.linalg.norm(pa) < 1e-6 or np.linalg.norm(pt) < 1e-6: return 0.0
    pa /= np.linalg.norm(pa); pt /= np.linalg.norm(pt)
    return math.atan2(np.cross(pa, pt) @ f, pa @ pt)


def op_aim(clip, mode, elev=30.0, w=None):
    m = model(); tt = key_times(m, clip)
    fa, hd = nid['RightForeArm'], nid['RightHand']; pf = parent[fa]
    qf, qh, rows = [], [], []
    for t in tt:
        G = C.globals_at(m, clip, t)
        Rfa, Rh = rotn(G[fa]), rotn(G[hd])
        f = G[hd][:3, 3] - G[fa][:3, 3]; f /= np.linalg.norm(f)
        a0 = haft_world(G)
        if mode == 'loop':
            e = math.radians(elev); tgt = np.array([0.0, math.sin(e), math.cos(e)]); wt = 1.0
        else:
            e = math.asin(np.clip(a0[1], -1, 1)) if elev is None else math.radians(elev)
            tgt = np.array([0.0, math.sin(e), math.cos(e)])
            w0, w1, w2, w3 = w
            wt = 0.0 if t <= w0 or t >= w3 else (min(1.0, (t - w0) / max(w1 - w0, 1e-6)) if t < w1 else (1.0 if t <= w2 else max(0.0, 1 - (t - w2) / max(w3 - w2, 1e-6))))
            wt = wt * wt * (3 - 2 * wt)
        th = float(np.clip(twist_to(f, a0, tgt), -math.radians(MAX_TWIST), math.radians(MAX_TWIST))) * wt
        Rt = W.axis_angle(f, th); a1 = Rt @ a0
        sw = W.arc(a1, a1 * (1 - wt) + tgt * wt) if wt > 0 else np.eye(3)
        ang = math.degrees(math.acos(np.clip((np.trace(sw) - 1) / 2, -1, 1)))
        if ang > MAX_SWING:
            ax_ = np.cross(a1, tgt); ax_ /= max(np.linalg.norm(ax_), 1e-9); sw = W.axis_angle(ax_, math.radians(MAX_SWING) * np.sign(ang))
            sw = W.axis_angle(ax_, math.radians(MAX_SWING))
        Rfa2 = W.axis_angle(f, th * FA_SHARE) @ Rfa
        Rh2 = sw @ Rt @ Rh
        qf.append(W.m2q(rotn(G[pf]).T @ Rfa2)); qh.append(W.m2q(Rfa2.T @ Rh2))
        a2 = sw @ a1
        rows.append(dict(t=round(t, 4), w=round(wt, 3), twist=round(math.degrees(th), 1), swing=round(min(ang, MAX_SWING), 1),
                         elev0=round(math.degrees(math.asin(np.clip(a0[1], -1, 1))), 1), az0=round(math.degrees(math.atan2(a0[0], a0[2])), 1),
                         elev1=round(math.degrees(math.asin(np.clip(a2[1], -1, 1))), 1), az1=round(math.degrees(math.atan2(a2[0], a2[2])), 1)))
    an = anim(clip); set_rot_track(an, fa, tt, qf); set_rot_track(an, hd, tt, qh)
    tw = [abs(r['twist']) for r in rows]; sws = [r['swing'] for r in rows]
    rep['clips'][clip] = dict(mode=mode, elev=elev, window=w, keys=len(tt), twist_max=max(tw), twist_med=float(np.median(tw)),
                              swing_max=max(sws), per_key=rows)
    print('aim %-16s %s: twist med %.1f max %.1f deg, swing max %.1f; az %s -> %s' % (
        clip, mode, np.median(tw), max(tw), max(sws), (min(r['az0'] for r in rows), max(r['az0'] for r in rows)),
        (min(r['az1'] for r in rows if r['w'] > 0.99) if any(r['w'] > 0.99 for r in rows) else None,
         max(r['az1'] for r in rows if r['w'] > 0.99) if any(r['w'] > 0.99 for r in rows) else None)))


for o in ops:
    k, v = o.split('=', 1); p = v.split(':')
    if k == 'copy': op_copy(p[0], p[1], p[2])
    elif k == 'pitch': op_pitch(p[0], p[1], float(p[2]))
    elif k == 'aim':
        op_aim(p[0], p[1], float(p[2]) if len(p) > 2 and p[2] != '' else (None if p[1] == 'lead' else 30.0), [float(x) for x in p[3:7]] if len(p) > 3 else None)
js['buffers'][0]['byteLength'] = len(bin_)
R_.write_glb(OUT, js, bin_)
res = L.lint(OUT)
rep['lint'] = dict(verdict=res['verdict'], fails=res['fails'], warns=len(res['warns']))
print('lint %s, %d fails' % (res['verdict'], len(res['fails'])), [f[:90] for f in res['fails']])
if REP: json.dump(rep, open(REP, 'w'), indent=1)
