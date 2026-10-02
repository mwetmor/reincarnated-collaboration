# bm_mx (R-C9-127) MAUL MEASURES, per key of every armed clip -- e25_carry_measure's instrument for the champion + great maul
# (e25 itself is the dark knight's: it hard-codes his 1.70 -> 1.96 root scale and the wl_* gear names).
#   head_y      the maul head centre's height above the body's lowest vertex (m)
#   face_deg    the angle between the head's LONG axis (its two striking faces, PCA of the head's vertices across the haft) and
#               the head's velocity across the haft (finite difference between keys): 0 = a face leads the swing, 90 = the
#               cheek leads. Read at the attack's CONTACT key (bm_e12_weapon.py's strike t) -- the roll about the haft is set by it.
#   pen_body    e25's proxy, kept for comparability: maul vertices with the nearest body vertex < 1 cm AND behind its normal
#   deep_body   the same with the nearest body vertex < 10 cm (catches a maul vertex well INSIDE the body, which the 1 cm rule
#               cannot: deep inside, the nearest body vertex is farther than 1 cm)
#   deep_<p>    deep rule against every gear piece p (posed by its own skin)
#   FIST EXCLUSION (T12 53_weapon_gate's rule: "fist excluded"): the haft runs INSIDE his closed fists (the rig has no fingers),
#               so pen_* and deep_* are counted on maul vertices more than --fist-r (0.08 m) from both posed fist centroids; the
#               raw counts are kept as raw_pen_body / raw_deep_body.
#   SWING (T12 EDGE rule, N-C9-GUARD-DESIGN-2): active swing = the keys contiguous with the peak head speed at >= 50% of it;
#               |cos(face, velocity across the haft)| speed-weighted over it, and at the key in the swing where the head is
#               furthest forward of the hips; roll_deg = the speed-weighted mean (mod 180) of the signed angle, in weapon_r's
#               frame about the haft, from the face axis to the velocity -- the roll that would put a face on the swing.
#   --swing t0:t1 restricts the active swing to a named window (the BLOW).
#   python3 bm03_maul_measure.py <body.glb> <maul.glb> <gear_dir> <piece,piece,...> [--clips a,b] [--strike work/weapon.json] [--json f]
import sys, os, json, math, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; BODY, MAUL, GD, PIECES = a[0], a[1], a[2], [p for p in a[3].split(',') if p]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
m = C.model(BODY); nid = m['nid']


def load(p):
    js, b = L.load_glb(p); mns = [i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n]
    sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]; ibm = W.mat_list(js, b, sk['inverseBindMatrices'])
    pr = [q for mn in mns for q in js['meshes'][js['nodes'][mn]['mesh']]['primitives']]
    V = np.vstack([L.read_accessor(js, b, q['attributes']['POSITION']) for q in pr]).astype(float)
    J = np.vstack([L.read_accessor(js, b, q['attributes']['JOINTS_0']) for q in pr]).astype(int)
    Wt = np.vstack([L.read_accessor(js, b, q['attributes']['WEIGHTS_0']) for q in pr]).astype(float)
    Nn = np.vstack([L.read_accessor(js, b, q['attributes']['NORMAL']) for q in pr]).astype(float)
    return dict(V=V, J=J, W=Wt / np.maximum(Wt.sum(1, keepdims=True), 1e-9), N=Nn, names=names, ibm=ibm)


def pose(P, G, step=1):
    V = P['V'][::step]; J = P['J'][::step]; Wt = P['W'][::step]; Nn = P['N'][::step]
    out = np.zeros_like(V); on = np.zeros_like(V); Vh = np.c_[V, np.ones(len(V))]
    for k in range(4):
        for jj in np.unique(J[:, k]):
            s = (J[:, k] == jj) & (Wt[:, k] > 0)
            if not s.any(): continue
            M = G[nid[P['names'][jj]]] @ P['ibm'][jj]
            out[s] += (Vh[s] @ M.T)[:, :3] * Wt[s, k:k + 1]; on[s] += (Nn[s] @ M[:3, :3].T) * Wt[s, k:k + 1]
    return out, on / np.maximum(np.linalg.norm(on, axis=1, keepdims=True), 1e-9)


def inside(MV, tree, PV, PN, lim):
    d, i = tree.query(MV); return (d < lim) & (((MV - PV[i]) * PN[i]).sum(1) < 0)


jb_, bb_ = L.load_glb(BODY)
cR = W.hand_points(jb_, bytes(bb_), 'RightHand', 0.6)[0].mean(0); cL = W.hand_points(jb_, bytes(bb_), 'LeftHand', 0.6)[0].mean(0)
FIST_R = float(opt('--fist-r', '0.08'))
B = load(BODY); Mc = load(MAUL); GP = {p: load(os.path.join(GD, p + '.glb')) for p in PIECES}
G0, _ = W.globals_(L.load_glb(BODY)[0]); MV0, _ = pose(Mc, G0); c0 = MV0.mean(0)
_, _, vt = np.linalg.svd(MV0 - c0, full_matrices=False); ax = vt[0]; s = (MV0 - c0) @ ax
wid = lambda lo, hi: np.linalg.norm(((MV0 - c0) - np.outer(s, ax))[(s > lo) & (s < hi)], axis=1).max()
if wid(s.max() - 0.25 * np.ptp(s), s.max()) < wid(s.min(), s.min() + 0.25 * np.ptp(s)): ax = -ax; s = -s
HEAD_FROM = float(opt('--head-from', '1.07')) / 1.30           # the maul's own record: head from 1.07 of 1.30 m
headsel = s > s.min() + HEAD_FROM * np.ptp(s); buttsel = s < s.min() + 0.05 * np.ptp(s)
strike = json.load(open(opt('--strike')))['strike'] if opt('--strike') else None
clips = opt('--clips', 'idle,idle_lean,walk,run,attack,warcry,hit,death').split(',')
rep = {}
for clip in [c for c in clips if c in m['anims']]:
    tt = sorted({float(t) for v in m['anims'][clip].values() for t in v[0]})
    rows, prev = [], None
    for t in tt:
        G = C.globals_at(m, clip, t)
        MV, _ = pose(Mc, G); BV, BN = pose(B, G, 3)
        head = MV[headsel].mean(0); butt = MV[buttsel].mean(0); hd = head - butt; hd /= np.linalg.norm(hd)
        H = MV[headsel] - head; H = H - np.outer(H @ hd, hd); _, _, v2 = np.linalg.svd(H, full_matrices=False); face = v2[0]
        row = dict(t=round(t, 4), head_y=round(float(head[1] - BV[:, 1].min()), 3))
        if prev is not None:
            vel = (head - prev[1]) / max(t - prev[0], 1e-6); vp = vel - (vel @ hd) * hd
            row['speed'] = round(float(np.linalg.norm(vel)), 2)
            row['face_deg'] = round(float(math.degrees(math.acos(min(1.0, abs(float(face @ vp)) / max(np.linalg.norm(vp), 1e-9))))), 1) if np.linalg.norm(vp) > 0.3 else None
        prev = (t, head)
        tb = cKDTree(BV); sub = MV[::2]
        fR = (G[nid['RightHand']] @ np.r_[cR, 1])[:3]; fL = (G[nid['LeftHand']] @ np.r_[cL, 1])[:3]
        keep = (np.linalg.norm(sub - fR, axis=1) > FIST_R) & (np.linalg.norm(sub - fL, axis=1) > FIST_R)
        ib1, ib10 = inside(sub, tb, BV, BN, 0.01), inside(sub, tb, BV, BN, 0.10)
        row['raw_pen_body'] = round(float(ib1.mean()), 4); row['raw_deep_body'] = round(float(ib10.mean()), 4)
        row['pen_body'] = round(float((ib1 & keep).mean()), 4); row['deep_body'] = round(float((ib10 & keep).mean()), 4)
        s_sub = (s - s.min())[::2] * (1.30 / np.ptp(s)); hit_any = ib10 & keep
        Rw = G[nid['weapon_r']][:3, :3]; Rw = Rw / np.cbrt(np.linalg.det(Rw)); row['_face_loc'] = (Rw.T @ face).tolist(); row['_head'] = head.tolist()
        row['_hips'] = G[nid['Hips']][:3, 3].tolist(); row['_hd'] = hd.tolist(); row['_Rw'] = Rw.tolist()
        for p, P in GP.items():
            PV, PN = pose(P, G, 2); ig = inside(sub, cKDTree(PV), PV, PN, 0.10) & keep; row['deep_' + p] = round(float(ig.mean()), 4)
            if ig.any(): row.setdefault('_where', {})[p] = [round(float(s_sub[ig].min()), 2), round(float(s_sub[ig].max()), 2)]
        if hit_any.any(): row.setdefault('_where', {})['body'] = [round(float(s_sub[hit_any].min()), 2), round(float(s_sub[hit_any].max()), 2)]
        if '_where' in row: row['where_m_from_butt'] = row.pop('_where')
        rows.append(row)
    keys = sorted({k for r in rows for k in r if k not in ('t', 'where_m_from_butt') and not k.startswith('_')})
    agg = {}
    for k in keys:
        v = [r[k] for r in rows if r.get(k) is not None]
        if v: agg[k] = [min(v), round(float(np.median(v)), 3), max(v)]
    worst_pen = max(rows, key=lambda r: r['deep_body'])
    rep[clip] = dict(min_med_max=agg, worst_deep_body_t=worst_pen['t'], rows=rows)
    if clip == 'attack' and strike:
        k = min(range(len(rows)), key=lambda i: abs(rows[i]['t'] - strike['t']))
        rep[clip]['contact'] = dict(t=rows[k]['t'], face_deg=rows[k].get('face_deg'), head_y=rows[k]['head_y'],
                                    face_deg_window=[rows[j].get('face_deg') for j in range(max(1, k - 3), min(len(rows), k + 1))])
    if clip == 'attack':
        sp = np.array([r.get('speed', 0.0) for r in rows]); kp = int(np.argmax(sp)); lo = kp; hi = kp
        while lo > 1 and sp[lo - 1] >= 0.5 * sp[kp]: lo -= 1
        while hi < len(rows) - 1 and sp[hi + 1] >= 0.5 * sp[kp]: hi += 1
        if opt('--swing'):     # the BLOW named explicitly (Mixamo slash 3: its rebound after contact is faster than the blow)
            w0, w1 = [float(x) for x in opt('--swing').split(':')]
            ix = [j for j, r in enumerate(rows) if w0 - 1e-4 <= r['t'] <= w1 + 1e-4]; sub_ = sp[ix]; kp = ix[int(np.argmax(sub_))]
            lo = kp; hi = kp
            while lo - 1 in ix and sp[lo - 1] >= 0.5 * sp[kp]: lo -= 1
            while hi + 1 in ix and sp[hi + 1] >= 0.5 * sp[kp]: hi += 1
        cs, ws, angs = [], [], []
        for j in range(max(lo, 1), hi + 1):
            v = (np.array(rows[j]['_head']) - np.array(rows[j - 1]['_head'])) / max(rows[j]['t'] - rows[j - 1]['t'], 1e-6)
            hd = np.array(rows[j]['_hd']); vp = v - (v @ hd) * hd; Rw = np.array(rows[j]['_Rw'])
            fl = np.array(rows[j]['_face_loc']); vl = Rw.T @ vp
            a_f = math.atan2(fl[0], fl[2]); a_v = math.atan2(vl[0], vl[2])         # about weapon_r's +Y (the haft)
            angs.append(math.degrees(a_v - a_f)); ws.append(np.linalg.norm(vp)); cs.append(abs(math.cos(math.radians(angs[-1]))))
        ws = np.array(ws); cos_w = float((np.array(cs) * ws).sum() / ws.sum())
        dbl = np.radians(2 * np.array(angs)); roll = 0.5 * math.degrees(math.atan2((np.sin(dbl) * ws).sum(), (np.cos(dbl) * ws).sum()))
        fw = [float((np.array(rows[j]['_head']) - np.array(rows[j]['_hips'])) @ np.array([0, 0, 1.0])) for j in range(lo, hi + 1)]
        js_ = lo + int(np.argmax(fw)); jj = max(js_, 1)
        rep[clip]['swing'] = dict(keys=[rows[lo]['t'], rows[hi]['t']], peak_speed=round(float(sp[kp]), 2), cos_weighted=round(cos_w, 3),
                                  strike_t=rows[js_]['t'], cos_at_strike=round(cs[jj - max(lo, 1)], 3) if jj - max(lo, 1) < len(cs) else None,
                                  roll_deg=round(roll, 1), signed_angles=[round(x, 1) for x in angs])
        print('SWING', json.dumps(rep[clip]['swing']))
    for r in rows:
        for k in [k for k in r if k.startswith('_')]: r.pop(k)
    print(clip, json.dumps({k: agg[k] for k in agg if k in ('head_y', 'pen_body', 'deep_body') or (k.startswith('deep_') and agg[k][2] > 0)}),
          ('CONTACT ' + json.dumps(rep[clip]['contact'])) if 'contact' in rep[clip] else '')
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
