# JOINT LIMITS, a lint row for every move this lane owns (the conductor, on Matt's look at v3, 2026-09-30: "the tilt of
# the blades made the elbow joints bend backwards and it looked really bad"). FAIL on any frame outside the range.
#
#   python3 scripts/j_joint_lint.py <body.glb> [--clips whirlwind,shout,hit,death] [--layers work/layers_moves.json]
#        [--ref idle,walk,run,attack,...] [--json f] [--neg]
#
# THE POSE is the shipped one: the clip at every one of its own keys, the layers its STATE names at weight x
# weight_curve(t), blended by Godot's mixer (scripts/j_blend.py), an un-keyed channel at REST (the glTF rule).
#
# THE MEASURES -- every bone of this rig points down its own +Y (verified: each child sits on its parent's +Y):
#   ELBOW / KNEE: the lower segment's direction in the UPPER bone's own frame. Its angle off the upper's axis is the
#            bend; the bend's direction round that axis is read against the joint's NATURAL flexion direction, LEARNED
#            from the rig's own library clips (--ref: the mean bend direction over their frames bent > 20 deg) -- a
#            hinge bends one way. flexion = bend x cos(phi), lateral = bend x sin(phi). Hyperextension is flexion < 0.
#   WRIST: the hand's rotation off its rest, relative to the forearm, split into a swing (about axes across the bone)
#            and a twist (about it). The swing's FLEXION axis is LEARNED from the library (its principal axis); the
#            other cross axis is deviation. The twist is the forearm's own (pronation / supination): forearm twist plus
#            hand twist, each off rest.
# LIMITS (anatomical, degrees) -- FAIL: elbow flexion -5..150 (no hyperextension past 5); knee flexion -5..155; wrist
#            flexion/extension |.| <= 80, deviation |.| <= 40 (radial ~25, ulnar ~40).
#            INFO only, not failed: hinge LATERAL bend (|.| > 20 elbow, 15 knee) and forearm TWIST (|.| > 90). The first run
#            showed why: the rig's upper-arm bone carries an arbitrary share of the humerus's twist, so a lateral angle in
#            its frame is not anatomical -- Meshy's own run reads 23 deg lateral, the retargeted run_armed 59, the scene
#            drax's guard 38-47 -- while the bend's SIGN (hyperextension) is robust: the v3 whirlwind's right elbow reads
#            -33, the library's least is attack's left elbow at -10 for 2 frames on a strike.
# LEARNED FROM Meshy-native library clips only (--ref): the text-to-motion retargets (--retargets) are reported as
#            controls but not learned from -- their world-space transport onto an A-pose rest bends the hinge planes.
# CONTROL: the --ref library clips are linted with the same rule and reported (natural motion must pass; if it does
# not, the limit or the axis is wrong, not the move). NEGATIVE CONTROL (--neg): a copy of one pose with the right elbow
# bent 20 deg BACKWARD must FAIL.
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RUNS = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(RUNS, "nb_d2", "scripts")); sys.path.insert(0, os.path.join(RUNS, "so_d7", "scripts")); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); B = __import__('j_blend')
a = sys.argv[1:]; BODY = a[0]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CLIPS = opt('--clips', 'whirlwind,shout,hit,death').split(',')
REF = opt('--ref', 'idle,walk,run,attack,walk_armed,idle_armed,block,shield_bash,chop_overhead_92').split(',')
RETARGETS = opt('--retargets', 'run_armed,strafe_L_armed').split(',')   # reported, NOT learned from (see the header)
LAYER_LIST = json.load(open(opt('--layers', os.path.join(ROOT, 'work', 'layers_moves.json'))))
LIM = dict(elbow=dict(flex=(-5, 150), lateral=20), knee=dict(flex=(-5, 155), lateral=15), wrist=dict(flex=80, dev=40, twist=90))
INFO_ONLY = {'lateral', 'forearm twist'}          # reported, not failed: see the header

js, bn = L.load_glb(BODY)
nodes = js['nodes']; parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
nid = {n.get('name'): i for i, n in enumerate(nodes)}
rest = {i: (np.array(n.get('translation', [0, 0, 0]), float), np.array(n.get('rotation', [0, 0, 0, 1]), float),
            np.array(n.get('scale', [1, 1, 1]), float)) for i, n in enumerate(nodes)}
anims = {}
for an in js.get('animations', []):
    ch = {}
    for c in an['channels']:
        s = an['samplers'][c['sampler']]
        ch[(c['target']['node'], c['target']['path'])] = (L.read_accessor(js, bn, s['input'])[:, 0].astype(float),
                                                          L.read_accessor(js, bn, s['output']).astype(float))
    anims[an.get('name')] = ch


def samp(tt, vv, t, path):
    if len(tt) == 1 or t <= tt[0]: return vv[0]
    if t >= tt[-1]: return vv[-1]
    k = int(np.searchsorted(tt, t, side='right')) - 1; u = (t - tt[k]) / max(tt[k + 1] - tt[k], 1e-12)
    return B.slerp(vv[k], vv[k + 1], u) if path == 'rotation' else (1 - u) * vv[k] + u * vv[k + 1]


def locals_at(clip, t):
    loc = {i: list(rest[i]) for i in rest}
    for (n, p), (tt, vv) in anims[clip].items():
        loc[n][{'translation': 0, 'rotation': 1, 'scale': 2}[p]] = np.array(samp(tt, vv, t, p), float)
    return loc


def clip_len(c):
    return float(max(v[0].max() for v in anims[c].values()))


def curve(ly, t):
    if 'weight_curve' not in ly: return 1.0
    ks = ly['weight_curve']['keys']
    if t <= ks[0][0]: return float(ks[0][1])
    for i in range(1, len(ks)):
        if t <= ks[i][0]:
            u = (t - ks[i - 1][0]) / max(ks[i][0] - ks[i - 1][0], 1e-9); u = u * u * (3 - 2 * u)
            return float(ks[i - 1][1] + (ks[i][1] - ks[i - 1][1]) * u)
    return float(ks[-1][1])


def pose_locals(clip, t, layered=True):
    loc = locals_at(clip, t); act = []
    for ly in (LAYER_LIST if layered else []):
        if clip not in ly.get('states', []): continue
        w = float(ly.get('weight', 1.0)) * curve(ly, t)
        if w <= 0: continue
        tm = ly.get('time', 'pose')
        if isinstance(tm, dict):                                       # the hold's contact-phase sync (render_cells.gd / j_measure.py rule)
            tl = ((t / clip_len(clip) - tm['c_base'] + tm['c_layer']) % 1.0) * clip_len(ly['action'])
        else:
            tl = t if tm == 'clip' else 0.0
        act.append(({nid[b] for b in ly['bones']}, w, locals_at(ly['action'], tl)))
    return B.blend(lambda i: rest[i], loc, act) if act else loc


def globals_of(loc):
    G = {}
    def g(i):
        if i in G: return G[i]
        tr, q, s = loc[i]; M = np.eye(4); M[:3, :3] = W.q2m(q) * s; M[:3, 3] = tr
        G[i] = M if parent.get(i) is None else g(parent[i]) @ M
        return G[i]
    for i in loc: g(i)
    return G


def rot(G, i):
    X = G[i][:3, :3]; return X / np.linalg.norm(X, axis=0)


Y = np.array([0.0, 1.0, 0.0])
HINGE = {'elbow_R': ('RightArm', 'RightForeArm', 'RightHand'), 'elbow_L': ('LeftArm', 'LeftForeArm', 'LeftHand'),
         'knee_R': ('RightUpLeg', 'RightLeg', 'RightFoot'), 'knee_L': ('LeftUpLeg', 'LeftLeg', 'LeftFoot')}
WRIST = {'wrist_R': ('RightForeArm', 'RightHand', 'RightArm'), 'wrist_L': ('LeftForeArm', 'LeftHand', 'LeftArm')}


def bend_vec(G, up, mid, lo):
    """the lower segment's direction in the upper bone's frame, with the upper's own axis (its +Y toward the joint)"""
    Ru = rot(G, nid[up]); d = G[nid[lo]][:3, 3] - G[nid[mid]][:3, 3]; d = Ru.T @ (d / np.linalg.norm(d))
    ax = Ru.T @ (G[nid[mid]][:3, 3] - G[nid[up]][:3, 3]); ax = ax / np.linalg.norm(ax)
    return d, ax


def qlocal_off_rest(loc, b):
    q = np.asarray(loc[nid[b]][1], float); q = q / np.linalg.norm(q); r = rest[nid[b]][1] / np.linalg.norm(rest[nid[b]][1])
    return W.q2m(r).T @ W.q2m(q)                                       # the bone's rotation off its rest, in its rest frame


def swing_twist(R):
    """R = swing . twist about +Y; returns (swing rotation vector, twist deg)"""
    y2 = R @ Y; ax = np.cross(Y, y2); s = np.linalg.norm(ax); ang = math.atan2(s, float(Y @ y2))
    sw = np.zeros(3) if s < 1e-9 else ax / s * ang
    Sw = W.axis_angle(ax / s, ang) if s > 1e-9 else np.eye(3)
    Tw = Sw.T @ R; tw = math.degrees(math.atan2(Tw[0, 2] - Tw[2, 0], Tw[0, 0] + Tw[2, 2]))
    return sw, tw


def frames_of(clip):
    tt = sorted({float(t) for (n, p), (ts, vv) in anims[clip].items() for t in ts})
    return tt


# ---- LEARN the natural directions from the library
nat = {k: [] for k in HINGE}; wsw = {k: [] for k in WRIST}
for c in REF:
    if c not in anims: continue
    for t in frames_of(c):
        loc = pose_locals(c, t, layered=False); G = globals_of(loc)
        for k, (u, mm, lo) in HINGE.items():
            d, ax = bend_vec(G, u, mm, lo); dev = d - (d @ ax) * ax
            if math.degrees(math.acos(max(-1, min(1, float(d @ ax))))) > 20: nat[k].append(dev / np.linalg.norm(dev))
        for k, (fa, h, ua) in WRIST.items():
            sw, _ = swing_twist(qlocal_off_rest(loc, h)); wsw[k].append(sw)
NAT = {}
for k, v in nat.items():
    v = np.array(v); mdir = v.mean(0); NAT[k] = dict(dir=mdir / np.linalg.norm(mdir), n=len(v), coherence=round(float(np.linalg.norm(mdir)), 3))
WAX = {}
for k, v in wsw.items():
    v = np.array(v); _, _, Vt = np.linalg.svd(v - 0 * v.mean(0), full_matrices=False)
    f = Vt[0] - (Vt[0] @ Y) * Y; f = f / np.linalg.norm(f); dvx = np.cross(Y, f)
    WAX[k] = dict(flex=f, dev=dvx, n=len(v))


def measure(loc):
    G = globals_of(loc); out = {}
    for k, (u, mm, lo) in HINGE.items():
        d, ax = bend_vec(G, u, mm, lo); th = math.degrees(math.acos(max(-1, min(1, float(d @ ax)))))
        dev = d - (d @ ax) * ax; nd = np.linalg.norm(dev)
        n = NAT[k]['dir'] - (NAT[k]['dir'] @ ax) * ax; n = n / np.linalg.norm(n)
        if nd < 1e-9: phi = 0.0
        else:
            dv = dev / nd; phi = math.atan2(float(np.cross(n, dv) @ ax), float(n @ dv))
        out[k] = dict(flex=th * math.cos(phi), lateral=th * math.sin(phi), bend=th)
    for k, (fa, h, ua) in WRIST.items():
        sw, tw_h = swing_twist(qlocal_off_rest(loc, h)); _, tw_f = swing_twist(qlocal_off_rest(loc, fa))
        out[k] = dict(flex=math.degrees(float(sw @ WAX[k]['flex'])), dev=math.degrees(float(sw @ WAX[k]['dev'])), twist=tw_h + tw_f)
    return out


def fails_of(m_):
    f = []
    for k, v in m_.items():
        if k.startswith('elbow') or k.startswith('knee'):
            lim = LIM['elbow' if k.startswith('elbow') else 'knee']
            if v['flex'] < lim['flex'][0]: f.append((k, 'hyperextension', v['flex']))
            if v['flex'] > lim['flex'][1]: f.append((k, 'over-flexion', v['flex']))
            if abs(v['lateral']) > lim['lateral']: f.append((k, 'lateral', v['lateral']))
        else:
            lim = LIM['wrist']
            if abs(v['flex']) > lim['flex']: f.append((k, 'flexion/extension', v['flex']))
            if abs(v['dev']) > lim['dev']: f.append((k, 'deviation', v['dev']))
            if abs(v['twist']) > lim['twist']: f.append((k, 'forearm twist', v['twist']))
    return f


def hard(f):
    return [x for x in f if x[1] not in INFO_ONLY]


def lint_clip(c, layered=True):
    rows = []; worst = {}
    for t in frames_of(c):
        m_ = measure(pose_locals(c, t, layered)); f0 = fails_of(m_); f = hard(f0)
        rows.append(dict(t=round(t, 4), fails=[dict(joint=a_, what=b_, deg=round(v_, 1)) for a_, b_, v_ in f],
                         info=[dict(joint=a_, what=b_, deg=round(v_, 1)) for a_, b_, v_ in f0 if b_ in INFO_ONLY]))
        for k, v in m_.items():
            for q, x in v.items():
                if q == 'bend': continue
                key = (k, q); cur = worst.get(key)
                score = -x if q == 'flex' and not k.startswith('wrist') else abs(x)   # hinge flexion: worst = least (most extended)
                if cur is None or score > cur[0]: worst[key] = (score, x, t)
    nf = sum(1 for r in rows if r['fails'])
    W_ = {}
    for (k, q), (s, x, t) in sorted(worst.items()):
        W_.setdefault(k, {})[q + ('_min' if q == 'flex' and not k.startswith('wrist') else '_worst')] = dict(deg=round(x, 1), t=round(t, 4))
    for k in HINGE:                                                    # and the hinge's most flexed frame
        mx = max(((measure(pose_locals(c, t, layered))[k]['flex'], t) for t in frames_of(c)[::3]), default=None)
        if mx: W_[k]['flex_max'] = dict(deg=round(mx[0], 1), t=round(mx[1], 4))
    return dict(frames=len(rows), failing_frames=nf, verdict='FAIL' if nf else 'PASS', worst=W_,
                info_frames=sum(1 for r in rows if r['info']),
                fails=[r for r in rows if r['fails']][:12])


rep = dict(instrument="scripts/j_joint_lint.py", body=os.path.basename(BODY), limits_deg=LIM,
           learned=dict(hinge={k: dict(n=v['n'], coherence=v['coherence']) for k, v in NAT.items()},
                        wrist={k: dict(n=v['n']) for k, v in WAX.items()}, from_clips=[c for c in REF if c in anims],
                        axes=dict(wrist={k: dict(flex=[float(x) for x in v['flex']], dev=[float(x) for x in v['dev']]) for k, v in WAX.items()},
                                  hinge={k: [float(x) for x in v['dir']] for k, v in NAT.items()})),
           moves={c: lint_clip(c) for c in CLIPS if c in anims},
           control_library={c: lint_clip(c, layered=False) for c in REF + RETARGETS if c in anims})
if '--neg' in a:
    c = CLIPS[0]; t = frames_of(c)[0]; loc = pose_locals(c, t)
    i = nid['RightForeArm']; G = globals_of(loc); d, ax = bend_vec(G, 'RightArm', 'RightForeArm', 'RightHand')
    th0 = measure(loc)['elbow_R']['flex']
    n = NAT['elbow_R']['dir']; hinge = np.cross(ax, n); hinge = hinge / np.linalg.norm(hinge)
    best = None
    for sgn in (1, -1):                                                # bend 20 deg past straight, backward, about the hinge
        R = W.axis_angle(sgn * hinge, math.radians(th0 + 20.0))
        q = np.array(W.m2q(W.q2m(loc[i][1]) @ R), float); l2 = {k_: list(v_) for k_, v_ in loc.items()}; l2[i] = [loc[i][0], q, loc[i][2]]
        fx = measure(l2)['elbow_R']['flex']
        if best is None or fx < best[0]: best = (fx, l2)
    f = hard(fails_of(measure(best[1])))
    rep['negative_control'] = dict(what="clip %s t %.4f with the right elbow bent past straight about its hinge" % (c, t),
                                   elbow_R_flex=round(best[0], 1), verdict='FAIL' if any(x[0] == 'elbow_R' and x[1] == 'hyperextension' for x in f) else 'PASS (THE ROW IS BLIND)')
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
print("learned hinges:", {k: (v['n'], v['coherence']) for k, v in NAT.items()})
for grp in ('moves', 'control_library'):
    for c, r in rep[grp].items():
        w = r['worst']
        print("%-8s %-22s %-4s %3d/%3d frames fail | elbow min R %6.1f L %6.1f | knee min R %6.1f L %6.1f | wrist flex R %6.1f L %6.1f dev R %6.1f L %6.1f twist R %6.1f L %6.1f"
              % ('MOVE' if grp == 'moves' else 'control', c, r['verdict'], r['failing_frames'], r['frames'],
                 w['elbow_R']['flex_min']['deg'], w['elbow_L']['flex_min']['deg'], w['knee_R']['flex_min']['deg'], w['knee_L']['flex_min']['deg'],
                 w['wrist_R']['flex_worst']['deg'], w['wrist_L']['flex_worst']['deg'], w['wrist_R']['dev_worst']['deg'], w['wrist_L']['dev_worst']['deg'],
                 w['wrist_R']['twist_worst']['deg'], w['wrist_L']['twist_worst']['deg']))
        if r['fails']: print("          first fails:", [(x['t'], [(f['joint'], f['what'], f['deg']) for f in x['fails']]) for x in r['fails'][:3]])
if 'negative_control' in rep: print("NEGATIVE CONTROL:", rep['negative_control'])
