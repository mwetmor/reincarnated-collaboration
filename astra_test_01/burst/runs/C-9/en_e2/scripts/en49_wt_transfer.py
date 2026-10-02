# EN-E2 round 7: a FREE rig (no Meshy credit) for a new mesh on an EXISTING Meshy skeleton -- weight transfer + joint refit.
# Occasioned by: (1) the conductor's "check the skeleton nemesis's weight transfer onto the revenant skeleton, since that costs
# nothing"; (2) the Mind-Taker (heroine01 boss mesh) blocked at Meshy 25/30 by the ledger's 10-credit reservation (not worked around).
#
#   python3 scripts/en49_wt_transfer.py <template_rigged.glb> <target_prepped.glb> <target_height_m> <out_rigged.glb> [--json r.json] [--k 8]
#
# TEMPLATE = a Meshy-rigged GLB on the wanted skeleton (24 joints, Armature x0.01, skinned mesh 'char1', mesh space 0..1.70 up).
# TARGET   = a 12_prep_rig output (same axes, centred at the origin, height H): rig space = (P + [0, H/2, 0]) x 1.70 / H (measured on
#            the female acolyte and the witch: prepped -> Meshy rigged is exactly that map, same axes).
# WEIGHTS  : inverse-distance blend of the k nearest TEMPLATE vertices' full weight vectors; then a SIDE RULE below the hips (a leg
#            vertex keeps only its own side's leg chain -- a robed template smears L/R between the legs); top 4, renormalised.
#            The rule spares a midline band |lateral| <= --side-gap (default 0.04 mesh units = 4 cm at 1.70): a skirt's centre keeps
#            Meshy's L/R blend (self-test: the rule with no band rewrote 29,470 robe vertices of the witch's own rig).
# JOINTS   : ring refit. For joint j with parent p, the RING is the vertices carrying >= 0.25 of both; the joint moves by
#            (target ring centroid - template ring centroid). No ring -> the parent's move. Global rotations are kept, so the
#            Mixamo graft (rotation-only, rest-aligned) needs nothing new. IBMs are rebuilt from the moved joints.
# The output has the template's node tree, names and skin; the target's geometry, UVs and texture; no animations.
import json, os, sys, struct
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R = __import__('49_recentre')
a = sys.argv[1:]
TPL, TGT, H, OUT = a[0], a[1], float(a[2]), a[3]
JS = a[a.index('--json') + 1] if '--json' in a else None
K = int(a[a.index('--k') + 1]) if '--k' in a else 8
REFIT = a[a.index('--refit') + 1] if '--refit' in a else 'disp'   # disp | ring | none
GAP = float(a[a.index('--side-gap') + 1]) if '--side-gap' in a else 0.04   # mesh units; < 0 = side rule off
js, b = L.load_glb(TPL)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
sk = js['skins'][js['nodes'][mn]['skin']]; joints = sk['joints']; names = [js['nodes'][j]['name'] for j in joints]
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
rd = lambda g, bb, i: np.asarray(L.read_accessor(g, bb, i))
S = rd(js, b, pr['attributes']['POSITION']).astype(float)
SJ = rd(js, b, pr['attributes']['JOINTS_0']).astype(int); SW = rd(js, b, pr['attributes']['WEIGHTS_0']).astype(float)
NJ = len(joints); Sd = np.zeros((len(S), NJ))
for k in range(4): np.add.at(Sd, (np.arange(len(S)), SJ[:, k]), SW[:, k])
IBM = np.array(W.mat_list(js, b, sk['inverseBindMatrices']))
G = W.globals_(js)[0]
M0 = G[joints[0]] @ IBM[0]                                     # mesh space -> world at rest (the same for every joint)
assert all(np.allclose(G[j] @ IBM[k], M0, atol=1e-4) for k, j in enumerate(joints)), 'template is not at its bind pose'
Minv = np.linalg.inv(M0)
pos = np.array([(Minv @ G[j])[:3, 3] for j in joints])         # joint positions in MESH space
parent = {}
for i, n in enumerate(js['nodes']):
    for c in n.get('children', []): parent[c] = i
pj = {k: (joints.index(parent[j]) if parent.get(j) in joints else None) for k, j in enumerate(joints)}
# ---- target
tj, tb = L.load_glb(TGT)
tpr = tj['meshes'][0]['primitives'][0]; ta = tpr['attributes']
T = rd(tj, tb, ta['POSITION']).astype(float); T = (T + [0, H / 2.0, 0]) * (S[:, 1].max() / H)
TN = rd(tj, tb, ta['NORMAL']).astype(np.float32); TUV = rd(tj, tb, ta['TEXCOORD_0']).astype(np.float32)
TI = rd(tj, tb, tpr['indices']).astype(np.uint32).ravel()
timg = tj['images'][0]; bv = tj['bufferViews'][timg['bufferView']]
IMG = bytes(tb[bv.get('byteOffset', 0): bv.get('byteOffset', 0) + bv['byteLength']]); MIME = timg.get('mimeType', 'image/jpeg')
# ---- weights
d, nn = cKDTree(S).query(T, k=K); w = 1.0 / np.maximum(d, 1e-5) ** 2; w /= w.sum(1, keepdims=True)
Td = np.einsum('nk,nkj->nj', w, Sd[nn])
LEFT = [names.index(n) for n in ('LeftUpLeg', 'LeftLeg', 'LeftFoot', 'LeftToeBase')]
RIGHT = [names.index(n) for n in ('RightUpLeg', 'RightLeg', 'RightFoot', 'RightToeBase')]
lat = 0 if abs(pos[LEFT[0], 0] - pos[RIGHT[0], 0]) > abs(pos[LEFT[0], 2] - pos[RIGHT[0], 2]) else 2
lsign = np.sign(pos[LEFT[0], lat] - pos[RIGHT[0], lat]); mid = (pos[LEFT[0], lat] + pos[RIGHT[0], lat]) / 2
hip_y = pos[LEFT[0], 1]
below = (T[:, 1] < hip_y) & (np.abs(T[:, lat] - mid) > GAP) & (GAP >= 0); side = np.sign(T[:, lat] - mid) * lsign      # +1 = left
moved = 0
for sel, kill in ((below & (side > 0), RIGHT), (below & (side < 0), LEFT)):
    moved += int((Td[sel][:, kill].sum(1) > 1e-6).sum()); Td[np.ix_(sel, kill)] = 0
top = np.argsort(-Td, 1)[:, :4]; tw = np.take_along_axis(Td, top, 1); tw /= np.maximum(tw.sum(1, keepdims=True), 1e-9)
# ---- joint refit (rings)
Tdn = np.zeros_like(Td); np.put_along_axis(Tdn, top, tw, 1)
move = {}; rings = {}
for k in range(NJ):
    p = pj[k]
    if p is None: continue
    rs = (Sd[:, k] >= 0.25) & (Sd[:, p] >= 0.25); rt = (Tdn[:, k] >= 0.25) & (Tdn[:, p] >= 0.25)
    rings[names[k]] = (int(rs.sum()), int(rt.sum()))
    if REFIT == 'ring' and rs.sum() >= 30 and rt.sum() >= 30: move[k] = T[rt].mean(0) - S[rs].mean(0)
if REFIT == 'disp':                                            # each joint: the mean (target - nearest template) offset of the
    off = T - S[nn[:, 0]]                                      # target vertices it holds >= 0.5 of (thickness cancels side to side)
    move = {k: off[Tdn[:, k] >= 0.5].mean(0) for k in range(NJ) if (Tdn[:, k] >= 0.5).sum() >= 30}
elif REFIT == 'none':
    move = {k: np.zeros(3) for k in range(NJ)}
order = list(range(NJ))
kids = {k: [c for c in range(NJ) if pj[c] == k] for k in range(NJ)}
if 0 not in move:
    cm = [move[c] for c in kids[0] if c in move]; move[0] = np.mean(cm, 0) if cm else np.zeros(3)
for k in order:                                               # joints listed parent-first in Meshy's skin
    if k not in move: move[k] = move[pj[k]] if pj[k] is not None else np.zeros(3)
newpos = pos + np.array([move[k] for k in range(NJ)])
# ---- rebuild the skeleton: same global rotations, moved origins
Gn = {}
for k, j in enumerate(joints):
    Gj = G[j].copy(); Gj[:3, 3] = (M0 @ np.r_[newpos[k], 1])[:3]; Gn[j] = Gj
for k, j in enumerate(joints):
    par = parent.get(j); Gp = Gn[par] if par in Gn else G[par] if par is not None else np.eye(4)
    Lm = np.linalg.inv(Gp) @ Gn[j]; js['nodes'][j]['translation'] = [float(x) for x in Lm[:3, 3]]
IBMn = np.array([np.linalg.inv(Gn[j]) @ M0 for j in joints])
# ---- fresh binary: target geometry, new skin data, target texture
nb = bytearray(); views = []; accs = []
def add(arr, comp, typ, target=None, minmax=False):
    off = W.append(nb, arr.tobytes()); v = dict(buffer=0, byteOffset=off, byteLength=arr.nbytes)
    if target: v['target'] = target
    views.append(v); acc = dict(bufferView=len(views) - 1, componentType=comp, count=int(arr.shape[0]), type=typ)
    if minmax: acc['min'] = [float(x) for x in arr.min(0)]; acc['max'] = [float(x) for x in arr.max(0)]
    accs.append(acc); return len(accs) - 1
F, U16, U32 = 5126, 5123, 5125
attrs = dict(POSITION=add(T.astype(np.float32), F, 'VEC3', 34962, True), NORMAL=add(TN, F, 'VEC3', 34962),
             TEXCOORD_0=add(TUV, F, 'VEC2', 34962), JOINTS_0=add(top.astype(np.uint8), 5121, 'VEC4', 34962),
             WEIGHTS_0=add(tw.astype(np.float32), F, 'VEC4', 34962))
idx = add(TI, U32, 'SCALAR', 34963)
ibm_acc = add(np.ascontiguousarray(IBMn.transpose(0, 2, 1)).reshape(-1, 16).astype(np.float32), F, 'MAT4')
img_off = W.append(nb, IMG); views.append(dict(buffer=0, byteOffset=img_off, byteLength=len(IMG)))
mesh = js['meshes'][js['nodes'][mn]['mesh']]
mesh['primitives'] = [dict(attributes=attrs, indices=idx, material=pr.get('material', 0), mode=4)]
sk['inverseBindMatrices'] = ibm_acc
js['images'] = [dict(bufferView=len(views) - 1, mimeType=MIME, name='target_tex')]
js['accessors'] = accs; js['bufferViews'] = views; js['buffers'] = [dict(byteLength=len(nb))]
js['animations'] = []                                          # downstream (52, e40b) append to it; en07 then holds only the grafted clips
R.write_glb(OUT, js, nb)
# ---- report
ring_n = {n: v for n, v in rings.items()}
rep = dict(refit=REFIT, template=TPL, target=TGT, target_height_m=H, k=K, side_gap=GAP, verts=len(T), faces=len(TI) // 3,
           nearest_m=dict(p50=float(np.percentile(d[:, 0], 50)), p95=float(np.percentile(d[:, 0], 95)), max=float(d[:, 0].max())),
           side_rule_verts=moved, rings_tpl_tgt=ring_n,
           joint_move_m={names[k]: round(float(np.linalg.norm(move[k])), 4) for k in range(NJ)},
           note='mesh-space units = 1.70 m tall template (Meshy); the export rescales to the target height')
if JS: json.dump(rep, open(JS, 'w'), indent=1)
print('WT_TRANSFER', OUT, 'nearest p50 %.4f p95 %.4f max %.4f' % tuple(rep['nearest_m'].values()), 'side-rule', moved,
      'max joint move %.3f (%s)' % max((v, k) for k, v in rep['joint_move_m'].items()))
