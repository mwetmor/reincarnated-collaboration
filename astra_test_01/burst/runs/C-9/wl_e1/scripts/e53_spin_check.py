# SPIN CHECKS (R-C9-132/133): over every key of a spin clip --
#   grip radius    each fist's horizontal distance from his spin axis (the hips' vertical), m
#   sweep height   each weapon's outer point height (DK: the mace head centre from e12; barbarian: the blade TIP = weapon bone
#                  + tip_along_y along its +Y), and its radius
#   arms cross     the minimum distance between the right-arm and left-arm segments (shoulder->elbow->wrist), m; < 0.06 = crossing
#   penetration    weapon-piece vertices inside the body (nearest body vertex < 1 cm and behind its normal), share
#   python3 e53_spin_check.py <body.glb> <clip> --weapons <piece.glb>:<bone>[:tip_m],... [--H 1.96] [--json f]
import sys, os, json, math, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; BODY, CLIP = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
HT = float(opt('--H', '1.96')); WSPEC = [x.split(':') for x in opt('--weapons', '').split(',') if x]
src = open(os.path.join(HERE, 'e26_cape_poke.py')).read()
m = C.model(BODY); nid = m['nid']; root = [i for i in range(len(m['nodes'])) if m['parent'].get(i) is None][0]
exec(src[src.index('def load('):src.index('B = load(BODY)')])
jb, bb = L.load_glb(BODY); G0, _ = W.globals_(jb); mn = next(i for i, nd in enumerate(jb['nodes']) if 'skin' in nd and 'mesh' in nd)
V0 = W.skin_rest(jb, bb, mn, G0); K = HT / float(np.ptp(V0[:, 1]))
cf = {s: W.hand_points(jb, bb, s + 'Hand', 0.6)[0].mean(0) for s in ('Right', 'Left')}
B = load(BODY); WP = [(load(s[0]), s[1], float(s[2]) if len(s) > 2 else None) for s in WSPEC]
def seg_dist(p1, q1, p2, q2):
    best = 1e9
    for s in np.linspace(0, 1, 21):
        x = p1 + s * (q1 - p1); d = np.min([np.linalg.norm(x - (p2 + u * (q2 - p2))) for u in np.linspace(0, 1, 21)]); best = min(best, d)
    return best
tt = sorted({float(t) for v in m['anims'][CLIP].values() for t in v[0]}); rows = []
for t in tt:
    G = C.globals_at(m, CLIP, t); Gd = {n: G[i] for n, i in nid.items()}
    hip = G[nid['Hips']][:3, 3]; flo = None
    BV, BN = pose(B, G); flo = BV[:, 1].min()
    r = dict(t=round(t, 4))
    for s in ('Right', 'Left'):
        f = (G[nid[s + 'Hand']] @ np.r_[cf[s], 1])[:3]; r[s + '_fist_radius_m'] = round(float(np.linalg.norm((f - hip)[[0, 2]]) * K), 4); r[s + '_fist_height_m'] = round(float((f[1] - flo) * K), 4)
    arm = {s: [G[nid[s + j]][:3, 3] for j in ('Arm', 'ForeArm', 'Hand')] for s in ('Right', 'Left')}
    r['arms_min_dist_m'] = round(float(min(seg_dist(arm['Right'][i], arm['Right'][i + 1], arm['Left'][j], arm['Left'][j + 1]) for i in (0, 1) for j in (0, 1)) * K), 4)
    tb = cKDTree(BV[::2])
    for P, bone, tip in WP:
        WV, _ = pose(P, G); d, i = tb.query(WV[::3]); ins = (d < 0.01 / K) & (((WV[::3] - BV[::2][i]) * BN[::2][i]).sum(1) < 0)
        r['pen_' + bone] = round(float(ins.mean()), 4)
        dom_ = np.array([B['names'][q] for q in B['J'][::2][i][np.arange(len(i)), B['W'][::2][i].argmax(1)]])
        r['pen_' + bone + '_nonhand'] = round(float((ins & ~np.isin(dom_, ['RightHand', 'LeftHand'])).mean()), 4)   # the grip is contact by design
        if ins.any():
            Pi = WV[::3][ins]; bi = i[ins]; jw = B['J'][::2][bi][np.arange(len(bi)), B['W'][::2][bi].argmax(1)]; parts = {}
            for q in jw: parts[B['names'][q]] = parts.get(B['names'][q], 0) + 1
            r['pen_' + bone + '_where'] = dict(radius_m=[round(float(x), 3) for x in np.percentile(np.linalg.norm((Pi - hip)[:, [0, 2]], axis=1) * K, [5, 50, 95])],
                                              height_m=[round(float(x), 3) for x in np.percentile((Pi[:, 1] - flo) * K, [5, 50, 95])],
                                              depth_cm=round(float(np.max(d[ins]) * K * 100), 2), body_bones=dict(sorted(parts.items(), key=lambda x: -x[1])[:4]))
        if tip is not None:
            Mb = G[nid[bone]]; y = Mb[:3, 1] / np.linalg.norm(Mb[:3, 1]); tp = Mb[:3, 3] + y * (tip / K)
        else:
            far = WV[np.argmax(np.linalg.norm((WV - hip)[:, [0, 2]], axis=1))]; tp = far
        r['tip_' + bone + '_radius_m'] = round(float(np.linalg.norm((tp - hip)[[0, 2]]) * K), 4); r['tip_' + bone + '_height_m'] = round(float((tp[1] - flo) * K), 4)
    rows.append(r)
agg = {k: [min(x[k] for x in rows), round(float(np.median([x[k] for x in rows])), 4), max(x[k] for x in rows)] for k in rows[0] if k != 't' and not k.endswith('_where')}
print('where', [x.get('pen_weapon_r_where') for x in rows[:1]])
for k, v in agg.items(): print('%-28s min %.4f  median %.4f  max %.4f' % (k, *v))
if opt('--json'): json.dump(dict(clip=CLIP, height_m=HT, min_med_max=agg, rows=rows), open(opt('--json'), 'w'), indent=1)
