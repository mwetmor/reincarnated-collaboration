# bm_mx STAGE 3 (R-C9-133): the DUAL-WIELD barbarian's measures -- sword on weapon_r (two edges along its +/-Z), axe_l on weapon_l
# (edge +Z), the pieces drawn on the BODY's weapon bones with their own IBMs (as Godot binds by name). Per key of each clip:
#   fistR / fistL     T12's FIST row (bm08's definition): grip offset toward its own side / shoulder half-width, chest frame
#   <w>_bear / <w>_elev   the blade's tip direction (bone +Y): horizontal bearing from his root forward (deg; + = toward his left) and
#                     elevation above horizontal (deg)
#   pen_<w>           share of the blade's vertices inside the BODY (nearest body vertex < 10 cm, behind its normal), fists excluded
#   <w>_<piece>       the same against each gear piece;  cross   sword vertices inside the axe or axe inside the sword (< 2 cm)
#   floor_<w>         the blade's lowest point above the floor (m; the clip is grounded on his feet at 0)
# EDGE per strike (T12 rule, bm08): active swing at >= 50% of the peak head speed, strike frame = head furthest forward of the hips;
#   the sword's cos is |.| (two edges), the axe's is SIGNED (+Z must lead). TTI = the strike frame's time.
#   python3 bm10_dual_measure.py <body.glb> <gear_dir> <p,p..> --clips a,b --strikes clip:sword,clip:axe_l [--swing clip=t0:t1] [--json f]
import sys, os, json, math, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; BODY, GD = a[0], a[1]; PIECES = [p for p in a[2].split(',') if p]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
m = C.model(BODY); nid = m['nid']
WEAP = {'sword': ('weapon_r', False), 'axe_l': ('weapon_l', True)}     # bone, signed edge


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


def inside(MV, PV, PN, lim=0.10):
    d, i = cKDTree(PV).query(MV); return (d < lim) & (((MV - PV[i]) * PN[i]).sum(1) < 0)


def rotn(M):
    R = M[:3, :3]; return R / np.cbrt(np.linalg.det(R))


jb, bb = L.load_glb(BODY); G0, _ = W.globals_(jb)
cR = W.hand_points(jb, bytes(bb), 'RightHand', 0.6)[0].mean(0); cL = W.hand_points(jb, bytes(bb), 'LeftHand', 0.6)[0].mean(0)
B = load(BODY); WP = {w: load(os.path.join(GD, w + '.glb')) for w in WEAP}; GP = {p: load(os.path.join(GD, p + '.glb')) for p in PIECES}
head = {}
for w, (bone, _) in WEAP.items():
    V0, _ = pose(WP[w], G0); M0 = G0[nid[bone]]
    loc = (np.c_[V0, np.ones(len(V0))] @ np.linalg.inv(M0).T)[:, :3] * np.cbrt(abs(np.linalg.det(M0[:3, :3])))
    head[w] = loc[:, 1] > loc[:, 1].max() - 0.25
clips = opt('--clips', '').split(','); strikes = [x.split(':') for x in (opt('--strikes', '') or '').split(',') if ':' in x]
swing = dict((x.split('=')[0], [float(v) for v in x.split('=')[1].split(':')]) for x in (opt('--swing', '') or '').split(',') if '=' in x)
rep = {}
for clip in [c for c in clips if c in m['anims']]:
    tt = sorted({float(t) for v in m['anims'][clip].values() for t in v[0]}); rows = []; prev = {}
    for t in tt:
        G = C.globals_at(m, clip, t); BV, BN = pose(B, G, 3)
        o = G[nid['Spine']][:3, 3]; lat = G[nid['LeftArm']][:3, 3] - G[nid['RightArm']][:3, 3]; half = np.linalg.norm(lat) / 2; lat /= np.linalg.norm(lat)
        fR = (G[nid['RightHand']] @ np.r_[cR, 1])[:3]; fL = (G[nid['LeftHand']] @ np.r_[cL, 1])[:3]
        row = dict(t=round(t, 4), fistR=round(float((G[nid['weapon_r']][:3, 3] - o) @ (-lat) / half), 3), fistL=round(float((G[nid['weapon_l']][:3, 3] - o) @ lat / half), 3))
        WV = {}
        for w, (bone, signed) in WEAP.items():
            V, N = pose(WP[w], G); WV[w] = (V, N); R = rotn(G[nid[bone]]); y = R[:, 1]
            row[w + '_bear'] = round(math.degrees(math.atan2(y[0], y[2])), 1); row[w + '_elev'] = round(math.degrees(math.asin(np.clip(y[1], -1, 1))), 1)
            sub = V[::2]; keep = (np.linalg.norm(sub - fR, axis=1) > 0.08) & (np.linalg.norm(sub - fL, axis=1) > 0.08)
            row['pen_' + w] = round(float((inside(sub, BV, BN) & keep).mean()), 4)
            for p, P in GP.items():
                PV, PN = pose(P, G, 2); row[w + '_' + p] = round(float((inside(sub, PV, PN) & keep).mean()), 4)
            row['floor_' + w] = round(float(V[:, 1].min()), 3)
            hc = V[head[w]].mean(0)
            if w in prev:
                v = (hc - prev[w][1]) / max(t - prev[w][0], 1e-6); vp = v - (v @ y) * y
                row['_v_' + w] = float(np.linalg.norm(v)); row['_c_' + w] = float(R[:, 2] @ vp / max(np.linalg.norm(vp), 1e-9)); row['_w_' + w] = float(np.linalg.norm(vp))
            row['_f_' + w] = float((hc - G[nid['Hips']][:3, 3]) @ np.array([0, 0, 1.0])); prev[w] = (t, hc)
        sv, axv = WV['sword'][0][::2], WV['axe_l'][0][::2]
        ds, _ = cKDTree(WV['axe_l'][0]).query(sv); row['cross'] = round(float((ds < 0.02).mean()), 4)
        rows.append(row)
    agg = {}
    for k in sorted({k for r in rows for k in r if k != 't' and not k.startswith('_')}):
        v = [r[k] for r in rows if r.get(k) is not None]
        if v: agg[k] = [min(v), round(float(np.median(v)), 3), max(v)]
    rep[clip] = dict(min_med_max=agg, keys=len(rows))
    for sc, w in [s for s in strikes if s[0] == clip]:
        signed = WEAP[w][1]; sp_ = np.array([r.get('_v_' + w, 0.0) for r in rows]); ix = list(range(1, len(rows)))
        if clip in swing: ix = [j for j in ix if swing[clip][0] - 1e-4 <= rows[j]['t'] <= swing[clip][1] + 1e-4]
        kp = max(ix, key=lambda j: sp_[j]); lo = hi = kp
        while lo - 1 in ix and sp_[lo - 1] >= 0.5 * sp_[kp]: lo -= 1
        while hi + 1 in ix and sp_[hi + 1] >= 0.5 * sp_[kp]: hi += 1
        js_ = max(range(lo, hi + 1), key=lambda j: rows[j]['_f_' + w])
        c = np.array([rows[j]['_c_' + w] for j in range(lo, hi + 1)]); c = c if signed else np.abs(c); ww = np.array([rows[j]['_w_' + w] for j in range(lo, hi + 1)])
        cs = rows[js_]['_c_' + w] if signed else abs(rows[js_]['_c_' + w])
        e = dict(weapon=w, swing=[rows[lo]['t'], rows[hi]['t']], peak_speed=round(float(sp_[kp]), 2), strike_t=rows[js_]['t'], cos_strike=round(cs, 3),
                 cos_weighted=round(float((c * ww).sum() / ww.sum()), 3), signed=signed)
        e['EDGE'] = 'PASS' if cs >= 0.707 and e['cos_weighted'] >= 0.8 else 'FAIL'; e['TTI_s'] = rows[js_]['t']
        rep[clip].setdefault('edge', []).append(e)
    for r in rows:
        for k in [k for k in r if k.startswith('_')]: r.pop(k)
    rep[clip]['rows'] = rows
    s = {k: agg[k] for k in ('fistR', 'fistL', 'sword_bear', 'sword_elev', 'axe_l_bear', 'axe_l_elev', 'pen_sword', 'pen_axe_l', 'cross', 'floor_sword', 'floor_axe_l') if k in agg}
    gw = {k: agg[k][2] for k in agg if any(k.startswith(w + '_') for w in WEAP) and not k.endswith(('_bear', '_elev')) and agg[k][2] > 0.005}
    print('%-10s' % clip, json.dumps(s), ('gear>0.5%% ' + json.dumps(gw)) if gw else '', ('EDGE ' + json.dumps(rep[clip]['edge'])) if 'edge' in rep[clip] else '')
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
