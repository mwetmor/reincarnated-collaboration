# R-C9-138 (Matt): "the wand ... pointing downwards and dropping directly through the palm of the hand" and "the body ... a bit
# too upturned in the idle state". MEASURE the kit of record (ss134f: orb staff R, shield L) in every state, pure glTF
# evaluation (no importer in the loop), glTF world frame: up +Y, her forward +Z (the package's forward_axis).
#
# Per clip, at every key:
#   orb_elev    the staff axis (grip -> orb) elevation above horizontal, deg (+ = orb up, - = orb DOWN)
#   orb_az      its horizontal bearing off her facing (+Z), deg (0 = straight ahead; 180 = behind her)
#   orb_fwd     the axis's component along her facing (cos of the 3D angle; 1 = straight ahead)
#   haft_lat    angle between the haft and the FIST's channel (the hand's thumb-pinky axis, measured off the
#               grip_R morph: the axis about which the fingers curl), deg -- 0 = the haft runs through the closed fist
#   haft_palm   angle between the haft and the PALM NORMAL (the mean curl direction of the grip_R finger tips), deg --
#               0 = the haft goes straight out THROUGH THE PALM (Matt's complaint)
#   off_cm      distance from the fist centre (the gripped hand's verts, morph on) to the haft line, cm
#   torso_pitch Hips -> neck from vertical, + = leaning FORWARD (e30's definition), and chest_pitch Spine01 -> neck
#   python3 r138_01_grip_measure.py <body.glb> <orbstaff.glb> [clips] [--json out]
import sys, os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('s17_loop_closure'); W = __import__('52_weapon_bones'); L = __import__('21_lint_export')

_av = sys.argv[1:]
args = [x for i, x in enumerate(_av) if not x.startswith('--') and not (i > 0 and _av[i - 1] in ('--json', '--weapon'))]
BODY, STAFF = args[0], args[1]
OUT = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
WEAPON = sys.argv[sys.argv.index('--weapon') + 1] if '--weapon' in sys.argv else 'weapon_r'
m = C.model(BODY); nid = m['nid']
js, bb = L.load_glb(BODY)


def read_sparse(js, bb, idx):
    acc = js['accessors'][idx]
    D = L.read_accessor(js, bb, idx) if 'bufferView' in acc else np.zeros((acc['count'], 3))
    sp = acc.get('sparse')
    if sp:
        bvi, bvv = js['bufferViews'][sp['indices']['bufferView']], js['bufferViews'][sp['values']['bufferView']]
        dt = {5125: np.uint32, 5123: np.uint16, 5121: np.uint8}[sp['indices']['componentType']]
        ii = np.frombuffer(bb, dtype=dt, count=sp['count'], offset=bvi.get('byteOffset', 0) + sp['indices'].get('byteOffset', 0))
        vv = np.frombuffer(bb, dtype=np.float32, count=sp['count'] * 3, offset=bvv.get('byteOffset', 0) + sp['values'].get('byteOffset', 0)).reshape(-1, 3)
        D = D.copy(); D[ii.astype(int)] = vv
    return D


def hand_frame(js, bb, hand='RightHand', morph='grip_R'):
    """The fist in the hand's LOCAL frame: centre (morph on), curl direction (palm normal) and channel axis."""
    nd = next(n for n in js['nodes'] if 'skin' in n and 'mesh' in n)
    sk = js['skins'][nd['skin']]; names = [js['nodes'][j]['name'] for j in sk['joints']]
    jh = names.index(hand); ibm = W.mat_list(js, bb, sk['inverseBindMatrices'])[jh]
    mesh = js['meshes'][nd['mesh']]; pr = mesh['primitives'][0]
    V = L.read_accessor(js, bb, pr['attributes']['POSITION'])
    J = L.read_accessor(js, bb, pr['attributes']['JOINTS_0']).astype(int)
    Wt = L.read_accessor(js, bb, pr['attributes']['WEIGHTS_0'])
    w = ((J == jh) * Wt).sum(1); sel = w > 0.5
    ti = mesh['extras']['targetNames'].index(morph)
    D = read_sparse(js, bb, pr['targets'][ti]['POSITION'])
    R = ibm[:3, :3]
    P0 = (np.c_[V[sel], np.ones(sel.sum())] @ ibm.T)[:, :3]
    P1 = (np.c_[V[sel] + D[sel], np.ones(sel.sum())] @ ibm.T)[:, :3]
    d = P1 - P0; mag = np.linalg.norm(d, axis=1)
    mv = mag > np.percentile(mag, 80)                       # the moving finger tips
    # the bone's long axis (+Y in glTF joint convention is wrist -> fingers for this rig; checked below)
    along = P0.mean(0); along = along / np.linalg.norm(along)
    curl = d[mv].mean(0); curl -= along * (curl @ along); curl /= np.linalg.norm(curl)
    chan = np.cross(along, curl); chan /= np.linalg.norm(chan)
    return dict(centre=P1.mean(0), centre_open=P0.mean(0), along=along, palm=curl, channel=chan,
                n=int(sel.sum()), moved_mm=float(mag.max() * 1000))


def staff_axis(path, bone):
    sj, sb = L.load_glb(path)
    _, A = W.hand_points(sj, sb, bone, wmin=-1.0)          # every vertex in the weapon bone's local frame
    c = A.mean(0); _, _, vt = np.linalg.svd(A - c, full_matrices=False); ax = vt[0]
    s = (A - c) @ ax
    # the ORB end is the fat end: compare the cross-section radius in the outer 15% at each end
    def rad(mask):
        Q = A[mask] - c; Q = Q - np.outer(Q @ ax, ax); return float(np.linalg.norm(Q, axis=1).max())
    lo, hi = np.percentile(s, 15), np.percentile(s, 85)
    if rad(s < lo) > rad(s > hi): ax = -ax; s = -s
    tip = c + ax * s.max(); butt = c + ax * s.min()
    return dict(axis=ax, tip=tip, butt=butt, length=float(s.max() - s.min()))


HF = hand_frame(js, bb)
SA = staff_axis(STAFF, WEAPON)
clips = args[2].split(',') if len(args) > 2 else [c for c in m['anims'] if not c.startswith(('mx_', 'staff_', 'book_'))]


def feats(G):
    p = lambda n: G[nid[n]][:3, 3]
    Rw = lambda n: G[nid[n]][:3, :3] / np.linalg.norm(G[nid[n]][:3, :3], axis=0)
    Wm = G[nid[WEAPON]]
    tip = (Wm @ np.append(SA['tip'], 1))[:3]; butt = (Wm @ np.append(SA['butt'], 1))[:3]
    ax = tip - butt; ax /= np.linalg.norm(ax)
    H = G[nid['RightHand']]; Rh = Rw('RightHand')
    fist = (H @ np.append(HF['centre'], 1))[:3]
    lat = Rh @ HF['channel']; palm = Rh @ HF['palm']
    elev = math.degrees(math.asin(np.clip(ax[1], -1, 1)))
    az = math.degrees(math.atan2(ax[0], ax[2]))
    ang = lambda u, v: math.degrees(math.acos(np.clip(abs(u @ v), 0, 1)))
    off = np.linalg.norm(np.cross(fist - butt, ax))
    v = p('neck') - p('Hips'); tp = math.degrees(math.atan2(v[2], v[1]))
    v2 = p('neck') - p('Spine01'); cp = math.degrees(math.atan2(v2[2], v2[1]))
    v3 = p('Spine01') - p('Hips'); pp = math.degrees(math.atan2(v3[2], v3[1]))
    return dict(orb_elev=elev, orb_az=az, orb_fwd=float(ax[2]), haft_lat=ang(ax, lat), haft_palm=ang(ax, palm),
                off_cm=off * 100, torso_pitch=tp, chest_pitch=cp, pelvis_pitch=pp, tip_y=float(tip[1]))


G0, _ = W.globals_(js)
rest = feats({i: G0[i] for i in G0})
out = dict(body=BODY, staff=STAFF, hand_frame={k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in HF.items()},
           staff_axis={k: (v.tolist() if hasattr(v, 'tolist') else v) for k, v in SA.items()}, rest=rest, clips={})
print('fist: n=%d moved %.1f mm; along %s palm %s channel %s' % (HF['n'], HF['moved_mm'], np.round(HF['along'], 3), np.round(HF['palm'], 3), np.round(HF['channel'], 3)))
print('staff: length %.3f m; rest: %s' % (SA['length'], {k: round(v, 1) for k, v in rest.items()}))
KEYS = ['orb_elev', 'orb_az', 'orb_fwd', 'haft_lat', 'haft_palm', 'off_cm', 'torso_pitch', 'chest_pitch', 'pelvis_pitch']
for c in clips:
    if c not in m['anims']: continue
    tt = sorted({float(t) for v in m['anims'][c].values() for t in v[0]})
    F = [feats(C.globals_at(m, c, t)) for t in tt]
    S = {k: dict(med=round(float(np.median([f[k] for f in F])), 2), min=round(float(min(f[k] for f in F)), 2),
                 max=round(float(max(f[k] for f in F)), 2)) for k in KEYS}
    S['keys'] = len(tt); S['per_key'] = [{k: round(f[k], 2) for k in KEYS} | {'t': round(t, 4)} for f, t in zip(F, tt)]
    out['clips'][c] = S
    print('%-16s elev %6.1f [%6.1f,%6.1f] az %6.1f [%6.1f,%6.1f] lat %5.1f [%5.1f,%5.1f] palm %5.1f [%5.1f,%5.1f] off %4.1f cm  pitch %5.1f chest %5.1f pelvis %5.1f' % (
        c, S['orb_elev']['med'], S['orb_elev']['min'], S['orb_elev']['max'], S['orb_az']['med'], S['orb_az']['min'], S['orb_az']['max'],
        S['haft_lat']['med'], S['haft_lat']['min'], S['haft_lat']['max'], S['haft_palm']['med'], S['haft_palm']['min'], S['haft_palm']['max'],
        S['off_cm']['med'], S['torso_pitch']['med'], S['chest_pitch']['med'], S['pelvis_pitch']['med']))
if OUT:
    json.dump(out, open(OUT, 'w'), indent=1)
