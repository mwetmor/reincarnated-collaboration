# E1 the mace on weapon_r: (1) weapon_r's REST becomes the GRIP (origin at the right fist on the haft axis, +Y along the haft
# to the head) in the body AND the piece, IBM to match (the piece is rebound RightHand -> weapon_r); (2) a weapon_r rotation
# channel on every clip that lays the haft through BOTH fists -- the two-handed grip TAKEN FROM EACH CLIP -- pivoting at the
# right fist, with the left fist free to slide along the haft; when the clip's hands part (> 0.85 m) the solve fades out over
# 0.2 m and the mace rides the right hand rigidly (a one-handed moment: hit, death, the shout's arms-wide); (3) the measures:
# left fist position along the haft (must stay on it: 0 .. 0.68 m toward the butt), and the attack's STRIKE-FRAME ASSERT.
#   python3 e12_weapon.py <body.glb> <piece.glb> <out_body.glb> <out_piece.glb> [--json f]
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); C = __import__('s17_loop_closure'); R_ = __import__('49_recentre')
CH = __import__('54_weapon_channel')
a = sys.argv[1:]; BODY, PIECE, OB, OP = a[:4]; OUTJ = a[a.index('--json') + 1] if '--json' in a else None
LEN, RGRIP = 1.45, float(os.environ.get("E1_RGRIP", "0.68")); HEAD_C = LEN - RGRIP - 0.20      # head centre ~0.20 m below the top spike's tip
SEP_FULL, SEP_FADE = 0.85, 0.20
ROOT = os.path.dirname(HERE)
jb, bb = L.load_glb(BODY); bb = bytearray(bb); jp, bp = L.load_glb(PIECE); bp = bytearray(bp)
nb = {n.get('name'): i for i, n in enumerate(jb['nodes'])}; npc = {n.get('name'): i for i, n in enumerate(jp['nodes'])}
Gb, _ = W.globals_(jb); Gp, _ = W.globals_(jp)
Hrest = Gb[nb['RightHand']]
# fist centroids in each hand's local frame (from the body mesh)
cR = W.hand_points(jb, bytes(bb), 'RightHand', 0.6)[0].mean(0); cL = W.hand_points(jb, bytes(bb), 'LeftHand', 0.6)[0].mean(0)
# the piece's vertices at rest -> haft axis, head end
mesh_node = next(i for i, n in enumerate(jp['nodes']) if 'skin' in n and 'mesh' in n)
V = W.skin_rest(jp, bytes(bp), mesh_node, Gp)
c = V.mean(0); _, _, vt = np.linalg.svd((V - c)[::max(1, len(V) // 5000)], full_matrices=False); ax = vt[0]
s = (V - c) @ ax; L0 = s.max() - s.min()
def wid(lo, hi):
    k = (s > lo) & (s < hi); P = (V[k] - c) - np.outer(s[k], ax); return np.linalg.norm(P, axis=1).max()
if wid(s.max() - 0.25 * L0, s.max()) < wid(s.min(), s.min() + 0.25 * L0): ax = -ax
# into RightHand-local
Hi = np.linalg.inv(Hrest)
axl = Hi[:3, :3] @ ax; axl /= np.linalg.norm(axl)
cl = (Hi @ np.r_[c, 1])[:3]
piv = cl + axl * float((cR - cl) @ axl)                        # the fist's foot on the haft axis
fist_off_axis = float(np.linalg.norm(cR - piv)) * float(np.cbrt(np.linalg.det(Hrest[:3, :3])))
x = np.cross(axl, [0, 0, 1.0]); x /= np.linalg.norm(x); z = np.cross(x, axl)
Wm = np.eye(4); Wm[:3, 0], Wm[:3, 1], Wm[:3, 2], Wm[:3, 3] = x, axl, z, piv
def set_mount(js, bin_, G):
    n = {nd.get('name'): i for i, nd in enumerate(js['nodes'])}
    W.set_trs(js['nodes'][n['weapon_r']], Wm)
    js['nodes'][n['weapon_r']]['scale'] = [1.0, 1.0, 1.0]
    sk = js['skins'][0]; names = [js['nodes'][j]['name'] for j in sk['joints']]
    ibm = W.mat_list(js, bytes(bin_), sk['inverseBindMatrices'])
    ibm[names.index('weapon_r')] = np.linalg.inv(G[n['RightHand']] @ Wm)
    data = b''.join(struct.pack('<16f', *M.T.reshape(-1)) for M in ibm); off = W.append(bin_, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": len(ibm), "type": "MAT4"})
    sk['inverseBindMatrices'] = len(js['accessors']) - 1
    return names
set_mount(jb, bb, Gb)
names = set_mount(jp, bp, Gp)
# piece: every vertex RightHand -> weapon_r (weights stay 1.0)
iR, iW = names.index('RightHand'), names.index('weapon_r')
pr = jp['meshes'][jp['nodes'][mesh_node]['mesh']]['primitives'][0]['attributes']
acc = jp['accessors'][pr['JOINTS_0']]; bv = jp['bufferViews'][acc['bufferView']]
base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0); stride = bv.get('byteStride') or 4; nre = 0
for i in range(acc['count']):
    for k in range(4):
        o = base + i * stride + k
        if bp[o] == iR: bp[o] = iW; nre += 1
jp['buffers'][0]['byteLength'] = len(bp) + (-len(bp) % 4); jb['buffers'][0]['byteLength'] = len(bb) + (-len(bb) % 4)
R_.write_glb(OP, jp, bp); R_.write_glb(OB, jb, bb)
# rest check: the piece draws where it did
Gp2, _ = W.globals_(jp); V2 = W.skin_rest(jp, bytes(bp), mesh_node, Gp2); rest_dev = float(np.abs(V2 - V).max())
# (2) channels
m = C.model(BODY); nid = m['nid']; tracks, meas = {}, {}
unit = float(np.cbrt(np.linalg.det(Hrest[:3, :3]))) if False else 1.0
for clip in m['anims']:
    times = sorted({float(t) for (n, p), (tt, vv) in m['anims'][clip].items() if p == 'rotation' for t in tt})
    qs, rows = [], []
    for t in times:
        G = C.globals_at(m, clip, t)
        H = G[nid['RightHand']]; HL = G[nid['LeftHand']]
        R = (H @ np.r_[cR, 1])[:3]; Lf = (HL @ np.r_[cL, 1])[:3]; sep = float(np.linalg.norm(R - Lf))
        Hr = H[:3, :3] / np.cbrt(np.linalg.det(H[:3, :3]))
        h = Hr @ axl; d = (R - Lf) / max(sep, 1e-9)
        w = float(np.clip((SEP_FULL - sep) / SEP_FADE, 0, 1))
        A = W.arc(h, d); ang = math.acos(np.clip((np.trace(A) - 1) / 2, -1, 1))
        Aw = W.axis_angle(np.array([A[2, 1] - A[1, 2], A[0, 2] - A[2, 0], A[1, 0] - A[0, 1]]) if ang > 1e-9 else np.array([0, 1.0, 0]), w * ang) if ang > 1e-9 else np.eye(3)
        Wr = Aw @ Hr @ Wm[:3, :3]
        qs.append(W.m2q(Hr.T @ Wr))
        hd = Wr[:, 1]; Pv = (H @ np.r_[piv, 1])[:3]
        sL = float((Lf - Pv) @ hd)                                     # left fist along the haft (negative = toward the butt)
        offL = float(np.linalg.norm((Lf - Pv) - sL * hd))
        head = Pv + hd * HEAD_C
        rows.append(dict(t=round(t, 4), sep=round(sep, 3), w=round(w, 3), left_along=round(-sL, 3), left_off_axis=round(offL, 3), head=np.round(head, 3).tolist()))
    tracks[clip] = dict(times=times, quats=np.array(qs).tolist()); meas[clip] = rows
json.dump({"weapon_r": tracks}, open(os.path.join(ROOT, 'work', 'weapon_r_tracks.json'), 'w'))
json.dump({"W": Wm.tolist(), "G": np.eye(4).tolist(), "_note": "E1 weapon_r rest = the right fist's grip on the mace haft (e12_weapon.py); no re-seat G (the piece is placed at rest by e10)"},
          open(os.path.join(ROOT, 'work', 'weapon_mount.json'), 'w'), indent=1)
CH.chan(OB, OB, os.path.join(ROOT, 'work', 'weapon_r_tracks.json'), None, replace=True)
# (3) measures + the strike-frame assert
summ = {}
for clip, rows in meas.items():
    two = [r for r in rows if r['w'] >= 0.999]
    summ[clip] = dict(keys=len(rows), two_handed_keys=len(two),
                      left_along_m=[min(r['left_along'] for r in two), max(r['left_along'] for r in two)] if two else None,
                      left_on_haft=all(0.0 <= r['left_along'] <= RGRIP for r in two))
# strike: the attack's contact = the key where the head is lowest after it was highest
STRIKE_CLIP = os.environ.get('E1_STRIKE', 'attack')
if STRIKE_CLIP not in meas:
    json.dump(dict(rows=meas), open(OUTJ, 'w')) if OUTJ else None; sys.exit(0)
ar = meas[STRIKE_CLIP]; hy = np.array([r['head'][1] for r in ar]); top = int(np.argmax(hy)); k = top + int(np.argmin(hy[top:]))
G = C.globals_at(m, STRIKE_CLIP, ar[k]['t']); hips = G[nid['Hips']][:3, 3]; head = np.array(ar[k]['head'])
fwd = np.array([0, 0, 1.0])                                  # the rest forward (Blender -Y = glTF +Z)
hz = head - hips; hz[1] = 0
strike = dict(t=ar[k]['t'], head_height_m=round(float(head[1]), 3), head_from_hips_m=round(float(np.linalg.norm(hz)), 3),
              head_bearing_deg=round(float(math.degrees(math.atan2(hz[0], hz[2]))), 1), two_handed_w=ar[k]['w'])
strike['ASSERT'] = bool(strike['head_height_m'] < 0.9 and strike['head_from_hips_m'] > 0.5 and abs(strike['head_bearing_deg']) < 75)
rep = dict(mount_W=Wm.tolist(), fist_off_axis_m=round(fist_off_axis, 4), piece_rebound=nre, piece_rest_dev=rest_dev, summary=summ, strike=strike)
print(json.dumps(dict(summary=summ, strike=strike, piece_rest_dev=rest_dev, fist_off_axis_m=rep['fist_off_axis_m']), indent=0)[:2500])
if OUTJ: json.dump(dict(rep, rows=meas), open(OUTJ, 'w'), indent=1)
