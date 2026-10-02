# bm_mx STAGE 2 (R-C9-127/131): the Barrow Viking's T12 measures on a Mixamo clip set -- axe on weapon_r (haft +Y, edge +Z: the
# T12_11 mount), shield on weapon_l (a disc in the hand's Y-Z plane, its FACE toward the hand's +X). Per key of each clip:
#   fistR / fistL  T12's FIST row (attack_lab guard_accept.gd _fist_frac): the grip's sideways offset from his centreline, toward its
#                  own side, over the shoulder half-width, in the chest (Spine) frame. 0 = centre, 1 = the shoulder joint.
#                  T12 aim 0.78 (R-C9-93), Matt later ~1.0 (R-C9-97/107). REPORTED, not failed (53_weapon_gate has no FIST row).
#   shield_face    the shield face's horizontal bearing from his root forward (deg; 0 = square to the front) and |cos| of the face
#                  normal with forward (1 = square on)
#   axe_head_y     the axe head centre's height above his lowest body vertex (m)
#   pen_axe / pen_shield   share of the weapon's vertices INSIDE the body (nearest body vertex < 10 cm and behind its normal), the
#                  fists excluded (vertices within --fist-r of either posed fist centroid: T12's "fist excluded"); vs every gear piece
#                  too (axe_<p>, shield_<p>), and the axe inside the shield (axe_in_shield)
# EDGE (T12 gate check 3, N-C9-GUARD-DESIGN-2) for each strike clip: the active swing = keys contiguous with the peak axe-head speed at
#   >= 50% of it (or --swing clip=t0:t1); the strike frame = the key in the swing where the head is furthest forward of the hips;
#   cos = edge (+Z) . (head velocity across the haft) / |...|, SIGNED (the edge, not the poll, must lead): PASS >= 0.707 at the strike
#   frame AND speed-weighted mean >= 0.8.  TTI = the strike frame's time (T12: <= 0.8 s).
#   python3 bm08_viking_measure.py <body.glb> <axe.glb> <shield.glb> <gear_dir> <p,p..> --clips a,b --strikes a,b [--swing a=t0:t1]
#        [--json f]
import sys, os, json, math, numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')
a = sys.argv[1:]; BODY, AXE, SHIELD, GD = a[0:4]; PIECES = [p for p in a[4].split(',') if p]
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


def inside(MV, PV, PN, lim=0.10):
    d, i = cKDTree(PV).query(MV); return (d < lim) & (((MV - PV[i]) * PN[i]).sum(1) < 0)


def rotn(M):
    R = M[:3, :3]; return R / np.cbrt(np.linalg.det(R))


jb, bb = L.load_glb(BODY)
cR = W.hand_points(jb, bytes(bb), 'RightHand', 0.6)[0].mean(0); cL = W.hand_points(jb, bytes(bb), 'LeftHand', 0.6)[0].mean(0)
FIST_R = float(opt('--fist-r', '0.08'))
B = load(BODY); AX = load(AXE); SH = load(SHIELD); GP = {p: load(os.path.join(GD, p + '.glb')) for p in PIECES}
# the axe head: vertices high on the haft (weapon_r local +Y > 0.55 m), from the rest pose in weapon_r's frame
G0, _ = W.globals_(jb); A0, _ = pose(AX, G0); Rw0 = G0[nid['weapon_r']]
loc = (np.c_[A0, np.ones(len(A0))] @ np.linalg.inv(Rw0).T)[:, :3] * np.cbrt(abs(np.linalg.det(Rw0[:3, :3])))
headsel = loc[:, 1] > float(opt('--head-from', '0.55'))
clips = opt('--clips', '').split(','); strikes = [x for x in opt('--strikes', '').split(',') if x]
swing = dict((x.split('=')[0], [float(v) for v in x.split('=')[1].split(':')]) for x in (opt('--swing', '') or '').split(',') if '=' in x)
rep = {}
for clip in [c for c in clips if c in m['anims']]:
    tt = sorted({float(t) for v in m['anims'][clip].values() for t in v[0]}); rows = []; prev = None
    for t in tt:
        G = C.globals_at(m, clip, t); BV, BN = pose(B, G, 3); ground = BV[:, 1].min()
        AV, _ = pose(AX, G); SV, SN = pose(SH, G, 2)
        root_f = np.array([0, 0, 1.0])
        sp = rotn(G[nid['Spine']]); o = G[nid['Spine']][:3, 3]
        lat = G[nid['LeftArm']][:3, 3] - G[nid['RightArm']][:3, 3]; half = np.linalg.norm(lat) / 2; lat /= np.linalg.norm(lat)
        fr = (G[nid['weapon_r']][:3, 3] - o) @ (-lat) / half; fl = (G[nid['weapon_l']][:3, 3] - o) @ lat / half
        nrm = rotn(G[nid['weapon_l']])[:, 0]; nh = nrm.copy(); nh[1] = 0
        bear = math.degrees(math.atan2(nh[0], nh[2])) if np.linalg.norm(nh) > 1e-6 else None
        head = AV[headsel].mean(0)
        fR = (G[nid['RightHand']] @ np.r_[cR, 1])[:3]; fL = (G[nid['LeftHand']] @ np.r_[cL, 1])[:3]
        ka = (np.linalg.norm(AV[::2] - fR, axis=1) > FIST_R) & (np.linalg.norm(AV[::2] - fL, axis=1) > FIST_R)
        ks = (np.linalg.norm(SV - fL, axis=1) > 0.12)
        row = dict(t=round(t, 4), fistR=round(float(fr), 3), fistL=round(float(fl), 3), shield_bear=round(bear, 1) if bear is not None else None,
                   shield_cos=round(float(abs(nrm @ root_f)), 3), axe_head_y=round(float(head[1] - ground), 3),
                   pen_axe=round(float((inside(AV[::2], BV, BN) & ka).mean()), 4), pen_shield=round(float((inside(SV, BV, BN) & ks).mean()), 4),
                   axe_in_shield=round(float(inside(AV[::2], SV, SN, 0.05).mean()), 4))
        for p, P in GP.items():
            PV, PN = pose(P, G, 2); row['axe_' + p] = round(float((inside(AV[::2], PV, PN) & ka).mean()), 4)
            row['shield_' + p] = round(float((inside(SV, PV, PN) & ks).mean()), 4)
        hd = rotn(G[nid['weapon_r']])[:, 1]; edge = rotn(G[nid['weapon_r']])[:, 2]
        if prev is not None:
            v = (head - prev[1]) / max(t - prev[0], 1e-6); vp = v - (v @ hd) * hd; row['speed'] = round(float(np.linalg.norm(v)), 2)
            row['_cos'] = float(edge @ vp / max(np.linalg.norm(vp), 1e-9)); row['_w'] = float(np.linalg.norm(vp))
        row['_fwd'] = float((head - G[nid['Hips']][:3, 3]) @ root_f)
        prev = (t, head); rows.append(row)
    agg = {}
    for k in sorted({k for r in rows for k in r if k not in ('t',) and not k.startswith('_')}):
        v = [r[k] for r in rows if r.get(k) is not None]
        if v: agg[k] = [min(v), round(float(np.median(v)), 3), max(v)]
    rep[clip] = dict(min_med_max=agg, keys=len(rows))
    if clip in strikes:
        sp_ = np.array([r.get('speed', 0.0) for r in rows]); ix = list(range(1, len(rows)))
        if clip in swing: ix = [j for j in ix if swing[clip][0] - 1e-4 <= rows[j]['t'] <= swing[clip][1] + 1e-4]
        kp = max(ix, key=lambda j: sp_[j]); lo = hi = kp
        while lo - 1 in ix and sp_[lo - 1] >= 0.5 * sp_[kp]: lo -= 1
        while hi + 1 in ix and sp_[hi + 1] >= 0.5 * sp_[kp]: hi += 1
        js_ = max(range(lo, hi + 1), key=lambda j: rows[j]['_fwd'])
        w = np.array([rows[j]['_w'] for j in range(lo, hi + 1)]); c = np.array([rows[j]['_cos'] for j in range(lo, hi + 1)])
        e = dict(swing=[rows[lo]['t'], rows[hi]['t']], peak_speed=round(float(sp_[kp]), 2), strike_t=rows[js_]['t'], cos_strike=round(rows[js_]['_cos'], 3),
                 cos_weighted=round(float((c * w).sum() / w.sum()), 3), tti_s=rows[js_]['t'], head_y_strike=rows[js_]['axe_head_y'])
        e['EDGE'] = 'PASS' if e['cos_strike'] >= 0.707 and e['cos_weighted'] >= 0.8 else 'FAIL'
        e['TTI'] = 'PASS' if e['tti_s'] <= 0.8 else 'FAIL (%.2f s > 0.8)' % e['tti_s']
        rep[clip]['edge'] = e
    for r in rows:
        for k in [k for k in r if k.startswith('_')]: r.pop(k)
    rep[clip]['rows'] = rows
    s = {k: agg[k] for k in ('fistR', 'fistL', 'shield_bear', 'shield_cos', 'pen_axe', 'pen_shield', 'axe_in_shield') if k in agg}
    gw = {k: agg[k][2] for k in agg if (k.startswith('axe_') or k.startswith('shield_')) and k not in s and k not in ('axe_head_y', 'shield_bear', 'shield_cos') and agg[k][2] > 0.005}
    print('%-12s' % clip, json.dumps(s), ('gear>0.5%% %s' % json.dumps(gw)) if gw else '', ('EDGE ' + json.dumps(rep[clip]['edge'])) if 'edge' in rep[clip] else '')
if opt('--json'): json.dump(rep, open(opt('--json'), 'w'), indent=1)
