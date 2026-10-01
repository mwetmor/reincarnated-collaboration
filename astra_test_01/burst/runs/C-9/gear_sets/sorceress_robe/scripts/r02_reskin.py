# R-C9-120: RE-SKIN her long red robe so the hem hangs from the pelvis and swings with the thighs, never with the shins or
# feet (r01: 81% of the bottom-40% weight sat on Leg/Foot/ToeBase, 71% single-bone, 1,128 hard bone flips -> rigid blocks).
#   python3 r02_reskin.py <robe.glb> <body.glb> <out.glb> [--thigh 0.6] [--blend 0.06] [--smooth 8] [--json f]
# Below the hip joints, every vertex gets:   Hips (1 - t) + its own-side UpLeg t,   t = THIGH * s^0.8,
#   s = depth below the hips / (hip - hem) in 0..1 (0 at the hips, THIGH at the hem);
#   left/right by x across the centre line, BLENDED over +-BLEND m so no vertex flips between the thighs at the back seam.
# Within 8 cm under the hips the new weights fade in over the robe's own (the bodice keeps its skin).
# Then a Laplacian smoothing (SMOOTH iterations) over the mesh edges, below the hips only; weights of co-located seam
# duplicates averaged (a UV seam must not open); top 4 influences, normalised. JOINTS_0/WEIGHTS_0 rewritten as a binary
# patch: positions, UVs, texture, skin and inverse binds byte-identical.
import json, sys
import numpy as np
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_robe/scripts')
D = __import__('r01_diagnose')
a = sys.argv[1:]
ROBE, BODY, OUT = a[0], a[1], a[2]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
THIGH, BLEND, SMOOTH = opt('--thigh', 0.6), opt('--blend', 0.06), int(opt('--smooth', 8))
OUTJ = a[a.index('--json') + 1] if '--json' in a else OUT.replace('.glb', '.json')
js, b, ni, jn, P, J, Wt, I = D.load(ROBE)
b = bytearray(b)
nb = len(jn); nv = len(P)
Wd = np.zeros((nv, nb)); np.add.at(Wd, (np.repeat(np.arange(nv), 4), J.ravel()), Wt.ravel())
G = D.node_world(js); nm = {n.get('name'): i for i, n in enumerate(js['nodes'])}
hip_y = 0.5 * (G[nm['LeftUpLeg']][1, 3] + G[nm['RightUpLeg']][1, 3]); mid_x = G[nm['Hips']][0, 3]
hem_y = float(P[:, 1].min())
# v3: --split back[,front] --split_s S -- SPLIT the skirt at the centre line(s) INSIDE the fold, from the hem up to S of the
# hip->hem depth: a vertex below S, on that side of the hips' z, used by faces on BOTH sides of the centre (face centroid x)
# is DUPLICATED for the right-side faces (positions, normals, UVs identical: closed at rest, it opens only in a stride).
# Each half then hangs from its OWN thigh only (no left/right blend across the slit) -- as the gladiator kilt was split.
SPLIT = a[a.index('--split') + 1].split(',') if '--split' in a else []
SPLIT_S = opt('--split_s', 0.3)
side = None
nsplit = {}
if SPLIT:
    assert len(js['meshes'][js['nodes'][ni]['mesh']]['primitives']) == 1
    assert not js['meshes'][js['nodes'][ni]['mesh']]['primitives'][0].get('targets'), 'a split piece with morph targets needs its targets duplicated too'
    zc = G[nm['Hips']][2, 3]
    sv = np.clip((hip_y - P[:, 1]) / (hip_y - hem_y), 0, 1)
    cen = P[I].mean(1); fl = cen[:, 0] > mid_x                      # face on her LEFT
    useL = np.zeros(nv, bool); useR = np.zeros(nv, bool)
    np.logical_or.at(useL, I[fl].ravel(), True); np.logical_or.at(useR, I[~fl].ravel(), True)
    cand = useL & useR & (sv > SPLIT_S) & (np.abs(P[:, 0] - mid_x) < 0.08)
    zone = np.zeros(nv, bool)
    for which in SPLIT:
        zone |= (P[:, 2] < zc) if which == 'back' else (P[:, 2] > zc)
        nsplit[which] = int((cand & ((P[:, 2] < zc) if which == 'back' else (P[:, 2] > zc))).sum())
    cand &= zone
    dup = np.where(cand)[0]; newid = np.full(nv, -1); newid[dup] = nv + np.arange(len(dup))
    I2 = I.copy(); rf = np.where(~fl)[0]
    sub = I2[rf]; m_ = newid[sub] >= 0; sub[m_] = newid[sub][m_]; I2[rf] = sub
    # duplicate every vertex attribute row (binary: new accessors appended)
    prim = js['meshes'][js['nodes'][ni]['mesh']]['primitives'][0]
    for k_, ai in list(prim['attributes'].items()):
        A = L.read_accessor(js, bytes(b), ai); A2 = np.concatenate([A, A[dup]])
        acc = dict(js['accessors'][ai]); data = A2.astype({5126: np.float32, 5121: np.uint8, 5123: np.uint16}[acc['componentType']]).tobytes(); o = W.append(b, data)   # read_accessor returns float64
        js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(data), "target": 34962})
        acc = {kk: vv for kk, vv in acc.items() if kk not in ('bufferView', 'byteOffset', 'count')}
        acc.update(bufferView=len(js['bufferViews']) - 1, count=int(len(A2)))
        js['accessors'].append(acc); prim['attributes'][k_] = len(js['accessors']) - 1
    assert nv + len(dup) < 65536
    data = I2.astype(np.uint16).ravel().tobytes(); o = W.append(b, data)
    js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(data), "target": 34963})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5123, "count": int(I2.size), "type": "SCALAR"})
    prim['indices'] = len(js['accessors']) - 1
    P = np.vstack([P, P[dup]]); Wd = np.vstack([Wd, Wd[dup]]); I = I2; nv = len(P)
    # per vertex: share of its faces on the LEFT (after the split a slit vertex is 1 or 0)
    lc = np.zeros(nv); tc = np.zeros(nv)
    np.add.at(lc, I[fl].ravel(), 1.0); np.add.at(tc, I.ravel(), 1.0)
    side = np.where(tc > 0, lc / np.maximum(tc, 1), 0.5)
    inslit = np.zeros(nv, bool); inslit[dup] = True; inslit[nv - len(dup):] = True
    nsplit['duplicated_verts'] = int(len(dup)); zone2 = np.r_[zone, zone[dup]]
y = P[:, 1]; x = P[:, 0]
s = np.clip((hip_y - y) / (hip_y - hem_y), 0, 1)
# v7: the FRONT may take more thigh than the back (--thigh_front, --exp): a knee swinging forward must carry the cloth in
# front of it or it comes through (r08: +19% body pixels visible with 0.6 all round). Front/back blended over +-0.08 m of
# the hips' z.
THIGH_F = opt('--thigh_front', THIGH); EXP = opt('--exp', 0.8)
zf = np.clip(0.5 + (P[:, 2] - G[nm['Hips']][2, 3]) / 0.16, 0, 1)
EXP_F = opt('--exp_front', EXP)
t = THIGH * (1 - zf) * s ** EXP + THIGH_F * zf * s ** EXP_F
wl = np.clip(0.5 + (x - mid_x) / (2 * BLEND), 0, 1)              # her LEFT is +x
if side is not None:
    # below the slit top, a vertex near the centre in a split zone takes its FACES' side, hard; fading to the blend above
    zz = (np.abs(x - mid_x) < BLEND) & zone2
    h = np.clip((s - SPLIT_S) / 0.05, 0, 1)
    wl = np.where(zz, (1 - h) * wl + h * np.round(side), wl)
new = np.zeros_like(Wd)
new[:, jn.index('Hips')] = 1 - t
new[:, jn.index('LeftUpLeg')] = t * wl
new[:, jn.index('RightUpLeg')] = t * (1 - wl)
# option C (--shin_back S): the BACK of the hem below the knee takes a small own-side SHIN share, ramped smoothly from 0 at
# the knee's depth to S at the hem and faded to 0 toward the front, taken out of the Hips share (the thigh share is kept)
SHIN_B = opt('--shin_back', 0.0)
if SHIN_B > 0:
    kn_y = 0.5 * (G[nm['LeftLeg']][1, 3] + G[nm['RightLeg']][1, 3]); s_k = (hip_y - kn_y) / (hip_y - hem_y)
    sh = SHIN_B * (1 - zf) * np.clip((s - s_k) / (1 - s_k), 0, 1) ** 1.5
    new[:, jn.index('Hips')] -= sh
    new[:, jn.index('LeftLeg')] = sh * wl; new[:, jn.index('RightLeg')] = sh * (1 - wl)
fade = np.clip((hip_y - y) / 0.08, 0, 1)[:, None]
Wn = (1 - fade) * Wd + fade * new
# v2: ABOVE the hips up to STRIP m, the robe's own thigh weight (nearest-point weights off the buttock skin) goes to Hips:
# r03 found the run's stretch at 0.64-0.76 of the robe's height -- that band tearing against the Hips-hung skirt below
STRIP = opt('--strip', 0.0)                                       # v5: 0 (r03: any strip ABOVE the hips worsened the sleeve-hip junction in the casts)
up = (y >= hip_y - 0.0) & (y < hip_y + STRIP)
k = (1 - np.clip((y - hip_y) / max(STRIP, 1e-9), 0, 1))[up]                  # full strip at the hips, none at hip + STRIP
for leg in ('LeftUpLeg', 'RightUpLeg'):
    j = jn.index(leg); moved = Wn[up, j] * k
    Wn[up, j] -= moved; Wn[up, jn.index('Hips')] += moved
below = (y < hip_y + 0.05) | up
# the SLEEVES hang to her hips and their cuffs are fused to the skirt there (one connected surface): a vertex carrying
# ARM weight is left exactly as it was -- no strip, no smoothing -- so the hip band does not smear forearm into pelvis
ARMS = [jn.index(n) for n in jn if any(k in n for k in ("Arm", "Hand", "Shoulder"))]
armv = Wd[:, ARMS].sum(1) > 0.05
Wn[armv] = Wd[armv]
below &= ~armv
e = np.vstack([I[:, [0, 1]], I[:, [1, 2]], I[:, [2, 0]]]); e = np.unique(np.sort(e, 1), axis=0)
deg = np.bincount(e.ravel(), minlength=nv).astype(float)[:, None]
for _ in range(SMOOTH):
    acc = np.zeros_like(Wn); np.add.at(acc, e[:, 0], Wn[e[:, 1]]); np.add.at(acc, e[:, 1], Wn[e[:, 0]])
    sm = 0.5 * Wn + 0.5 * np.where(deg > 0, acc / np.maximum(deg, 1), Wn)
    Wn = np.where(below[:, None], sm, Wn)
# co-located seam duplicates share their weights
key = np.round(P / 1e-5).astype(np.int64)
if side is not None:                                                # a slit's two lips must NOT be re-welded here
    key = np.hstack([key, np.where(zone2 & (s > SPLIT_S), np.round(side).astype(np.int64) + 1, 0)[:, None]])
_, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.ravel()
summ = np.zeros((inv.max() + 1, nb)); np.add.at(summ, inv, Wn); cnt = np.bincount(inv)[:, None]
Wn = summ[inv] / cnt[inv]
legs = [jn.index(n) for n in ((() if SHIN_B > 0 else ("LeftLeg", "RightLeg")) + ("LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase")) if n in jn]
Wn[np.ix_(below & (y < hip_y - 0.02), legs)] = 0.0
top = np.argsort(-Wn, axis=1)[:, :4]
Wt4 = np.take_along_axis(Wn, top, 1); Wt4 = np.where(Wt4 > 0.002, Wt4, 0.0); Wt4 /= np.maximum(Wt4.sum(1, keepdims=True), 1e-9)
J4 = np.where(Wt4 > 0, top, 0)
# write back per primitive (same vertex order as D.load concatenated)
off = 0
for p in js['meshes'][js['nodes'][ni]['mesh']]['primitives']:
    n_ = js['accessors'][p['attributes']['POSITION']]['count']
    jc = js['accessors'][p['attributes']['JOINTS_0']]['componentType']
    jarr = J4[off:off + n_].astype(np.uint16 if jc == 5123 else np.uint8)
    warr = Wt4[off:off + n_].astype(np.float32)
    for k, arr, ct in (('JOINTS_0', jarr, jc), ('WEIGHTS_0', warr, 5126)):
        data = arr.tobytes(); o = W.append(b, data)
        js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(data), "target": 34962})
        js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": ct, "count": int(n_), "type": "VEC4"})
        p['attributes'][k] = len(js['accessors']) - 1
    off += n_
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, bytes(b))
low = ((y - hem_y) / (P[:, 1].max() - hem_y)) < 0.40
share = Wt4[low].sum(0) if False else None
rep = dict(robe=ROBE, out=OUT, split=SPLIT, split_s=SPLIT_S, split_counts=nsplit, strip_above_hips_m=STRIP, thigh_at_hem=THIGH, thigh_front_at_hem=THIGH_F, exp=EXP, exp_front=EXP_F, shin_back_at_hem=SHIN_B, centre_blend_m=BLEND, smooth_iterations=SMOOTH, hip_y=round(float(hip_y), 4),
           hem_y=round(hem_y, 4), seam_clusters=int(inv.max() + 1), verts=int(nv))
json.dump(rep, open(OUTJ, 'w'), indent=1); print("RESKIN", json.dumps(rep))
