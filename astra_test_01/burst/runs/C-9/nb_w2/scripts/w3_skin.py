# The JOIN sword as a weapon_r piece: measured features -> the axe's convention -> skinned into a
# COPY of the T12_5_guard skeleton, sockets named for the JOIN-1 contract.
#
#   python3 scripts/w3_skin.py <raw build.glb> <clean.glb> <template axe.glb> <out.glb>
#        [--overall 0.90] [--blade-thick 0.5] [--json f]
#
# CONVENTION -- the axe's, from 52_weapon_bones (so the mount code is shared, not special-cased):
#   weapon_r local  origin at the GRIP (the fist's feature: the middle of the grip, on its axis),
#                   +Y along the blade to the TIP, +Z toward an EDGE, X = Y x Z (the flat's normal).
# The raw Tripo frame is already long axis +Y (tip up: the thin end), guard along Z, thickness X,
# so the frame is a translation to the grip and a scale -- no rotation is invented here.
# FEATURES are found on the DENSE raw build's width profile (the crossguard is the widest band, the
# grip the narrow band below it, the pommel the widening at the end), then applied to the clean mesh.
# SCALE: --overall sets tip-to-pommel (0.90 m by default); the rest follows from the painted
# proportions (blade/grip 4.82 on the edited sheet), and every dimension is reported.
# BLADE THICKNESS: Tripo reconstructed the edge-on line ~2.5x the painted thickness; --blade-thick
# scales X over the blade only (above the guard, blended over 1 cm) and bends the normals with it.
# SOCKETS (reincarnated-godot docs/join1-sprite-cell-contract-2026-09-29.md 3.2 / 5): `main_grip`
# and `main_tip` (the main hand carries the sword, R-C9-81), child nodes of weapon_r, so a renderer
# reads them as exact attachment positions per frame. `sword_edge` marks the +Z edge for the roll,
# as `axe_edge` does for the axe.
import json, math, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "so_d7", "scripts"))
L = __import__('21_lint_export')
W = __import__('52_weapon_bones')
a = sys.argv[1:]
RAW, CLEAN, TPL, OUT = a[0], a[1], a[2], a[3]
OVERALL = float(a[a.index('--overall') + 1]) if '--overall' in a else 0.90
THIN = float(a[a.index('--blade-thick') + 1]) if '--blade-thick' in a else 1.0
OUTJ = a[a.index('--json') + 1] if '--json' in a else None
ROLL = float(a[a.index('--roll') + 1]) if '--roll' in a else 0.0   # the mount's roll about +Y (w6_roll.py)

# ---- features on the dense raw build ------------------------------------------------------------
rj, rb = L.load_glb(RAW)
PR = L.read_accessor(rj, rb, rj['meshes'][0]['primitives'][0]['attributes']['POSITION'])
y = PR[:, 1]; y0, y1 = float(y.min()), float(y.max()); LR = y1 - y0
NB = 400
idx = np.clip(((y - y0) / LR * NB).astype(int), 0, NB - 1)
wz = np.zeros(NB); tx = np.zeros(NB); cx = np.zeros(NB); cz = np.zeros(NB)
for k in range(NB):
    s = PR[idx == k]
    if len(s) > 3:
        wz[k] = np.percentile(s[:, 2], 99) - np.percentile(s[:, 2], 1)
        tx[k] = np.percentile(s[:, 0], 99) - np.percentile(s[:, 0], 1)
        cx[k] = np.median(s[:, 0]); cz[k] = np.median(s[:, 2])
yc = y0 + (np.arange(NB) + 0.5) / NB * LR
bot, top = wz[:12].mean() + tx[:12].mean(), wz[-12:].mean() + tx[-12:].mean()
assert top < bot, "the thin end (tip) is expected at +Y in the raw frame"
lower = np.arange(NB) < NB // 2
gk = int(np.argmax(np.where(lower, wz, 0)))                          # crossguard: widest, lower half
band = [k for k in range(NB) if abs(k - gk) < 20 and wz[k] > 0.5 * wz[gk]]
g_lo, g_hi = min(band), max(band)
grip_w = float(np.median(wz[max(0, g_lo - 40):g_lo]))
pk = None                                                            # pommel top: from the end up
for k in range(0, g_lo):
    if wz[k] < 1.25 * grip_w and np.all(wz[k:k + 6] < 1.25 * grip_w):
        pk = k; break
grip_lo, grip_hi = yc[pk], yc[g_lo] - 0.5 * LR / NB
gs = (idx >= pk) & (idx < g_lo)
axis_x, axis_z = float(np.median(PR[gs, 0])), float(np.median(PR[gs, 2]))
origin = np.array([axis_x, 0.5 * (grip_lo + grip_hi), axis_z])
S = OVERALL / LR
tip_raw = PR[int(np.argmax(y))]
feat = dict(
    overall_m=round(OVERALL, 4),
    blade_m=round((y1 - (yc[g_hi] + 0.5 * LR / NB)) * S, 4),
    guard_thick_m=round((g_hi - g_lo + 1) * LR / NB * S, 4), guard_span_m=round(float(wz[gk]) * S, 4),
    grip_m=round((grip_hi - grip_lo) * S, 4), grip_width_m=round(grip_w * S, 4),
    pommel_m=round((grip_lo - y0) * S, 4), pommel_width_m=round(float(wz[:pk].max()) * S, 4),
    blade_width_at_guard_m=round(float(wz[g_hi + 3]) * S, 4),
    blade_thick_raw_m=round(float(np.median(tx[g_hi + 5:NB - 20])) * S, 4))
feat["blade_over_grip"] = round(feat["blade_m"] / feat["grip_m"], 3)
feat["blade_thick_m"] = round(feat["blade_thick_raw_m"] * THIN, 4)

# ---- the clean mesh into the local frame ------------------------------------------------------------
cj, cb = L.load_glb(CLEAN)
pr = cj['meshes'][0]['primitives'][0]
P = L.read_accessor(cj, cb, pr['attributes']['POSITION']).astype(float)
N = L.read_accessor(cj, cb, pr['attributes']['NORMAL']).astype(float)
UV = L.read_accessor(cj, cb, pr['attributes']['TEXCOORD_0']).astype(float)
IDX = L.read_accessor(cj, cb, pr['indices']).reshape(-1).astype(np.int64)
Pl = (P - origin) * S                                                 # metres, grip at the origin
if THIN != 1.0:
    y_guard_top = (yc[g_hi] + 0.5 * LR / NB - origin[1]) * S
    f = np.clip((Pl[:, 1] - y_guard_top) / 0.01, 0.0, 1.0)             # 0 at the guard, 1 from 1 cm up
    k = 1.0 + (THIN - 1.0) * f
    Pl[:, 0] *= k
    N[:, 0] /= k; N /= np.linalg.norm(N, axis=1, keepdims=True)
tip_l = (tip_raw - origin) * S
tip_l = np.array([0.0, float(tip_l[1]), 0.0]) if abs(tip_l[0]) + abs(tip_l[2]) < 0.01 else tip_l

# ---- the template: the T12_5_guard axe, same skeleton ----------------------------------------------
js, bn = L.load_glb(TPL)
nodes = js['nodes']
nid = {n.get('name'): i for i, n in enumerate(nodes)}
parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
def local(i):
    n = nodes[i]; M = np.eye(4)
    M[:3, :3] = W.q2m(n.get('rotation', [0, 0, 0, 1])) * np.array(n.get('scale', [1, 1, 1]))
    M[:3, 3] = n.get('translation', [0, 0, 0]); return M
def glob(i):
    M = local(i)
    while i in parent:
        i = parent[i]; M = local(i) @ M
    return M
wr = nid['weapon_r']
if ROLL:
    # THE MOUNT'S ROLL, as 52_weapon_bones --roll makes it: weapon_r's rest rotation post-multiplied by a
    # turn about its own +Y. The sword's local frame keeps the axe's convention (+Z an edge); the roll
    # lives in the mount, in the body (w6_roll.py) and here, so the two rests agree.
    q = np.array(nodes[wr].get('rotation', [0, 0, 0, 1]), float)
    qr = np.array([0.0, math.sin(math.radians(ROLL) / 2), 0.0, math.cos(math.radians(ROLL) / 2)])
    x1, y1_, z1, w1 = q; x2, y2, z2, w2 = qr
    qn = np.array([w1 * x2 + x1 * w2 + y1_ * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1_ * w2 + z1 * x2,
                   w1 * z2 + x1 * y2 - y1_ * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1_ * y2 - z1 * z2])
    nodes[wr]['rotation'] = [float(v) for v in qn / np.linalg.norm(qn)]
GW = glob(wr)
su = float(np.linalg.norm(GW[:3, 0]))                                 # metres per weapon_r unit
RW = GW[:3, :3] / su
Pb = (GW @ np.c_[Pl / su, np.ones(len(Pl))].T).T[:, :3]
Nb = (RW @ N.T).T
skin = js['skins'][0]
jnames = [nodes[j].get('name') for j in skin['joints']]
ji = jnames.index('weapon_r')
IBM_ALL = L.read_accessor(js, bn, skin['inverseBindMatrices']).reshape(-1, 4, 4).copy()
IBM_ALL[ji] = np.linalg.inv(GW).T                       # glTF matrices are column-major
# ---- rebuild the BIN: keep every bufferView the template still needs, new data for the sword ---------
mesh_i = next(i for i, n in enumerate(nodes) if 'mesh' in n)
old_prim = js['meshes'][nodes[mesh_i]['mesh']]['primitives'][0]
drop_acc = set(old_prim['attributes'].values()) | {old_prim['indices']}
img = js['images'][0]
cimg = cj['images'][0]
cbv = cj['bufferViews'][cimg['bufferView']]
jpeg = bytes(cb[cbv.get('byteOffset', 0):cbv.get('byteOffset', 0) + cbv['byteLength']])
keep_bv = {}
new_bin = bytearray()
def put(data):
    while len(new_bin) % 4: new_bin.append(0)
    off = len(new_bin); new_bin.extend(data); return off
views, accs = [], []
for ai, acc in enumerate(js['accessors']):
    if ai in drop_acc:
        accs.append(None); continue
    bv = js['bufferViews'][acc['bufferView']]
    if acc['bufferView'] not in keep_bv:
        data = bytes(bn[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']])
        nbv = {k: v for k, v in bv.items() if k not in ('byteOffset', 'buffer')}
        nbv.update(buffer=0, byteOffset=put(data)); views.append(nbv); keep_bv[acc['bufferView']] = len(views) - 1
    nacc = dict(acc); nacc['bufferView'] = keep_bv[acc['bufferView']]; accs.append(nacc)
def add(arr, ctype, typ, target=None, minmax=False):
    arr = np.ascontiguousarray(arr)
    nbv = dict(buffer=0, byteOffset=put(arr.tobytes()), byteLength=arr.nbytes)
    if target: nbv['target'] = target
    views.append(nbv)
    acc = dict(bufferView=len(views) - 1, componentType=ctype, count=int(arr.shape[0]), type=typ)
    if minmax:
        acc['min'] = [float(v) for v in arr.min(0)]; acc['max'] = [float(v) for v in arr.max(0)]
    accs.append(acc); return len(accs) - 1
nv = len(Pb)
a_pos = add(Pb.astype(np.float32), 5126, 'VEC3', 34962, True)
a_nrm = add(Nb.astype(np.float32), 5126, 'VEC3', 34962)
a_uv = add(UV.astype(np.float32), 5126, 'VEC2', 34962)
a_j = add(np.tile(np.array([ji, 0, 0, 0], np.uint8), (nv, 1)), 5121, 'VEC4', 34962)
a_w = add(np.tile(np.array([1, 0, 0, 0], np.float32), (nv, 1)), 5126, 'VEC4', 34962)
a_i = add(IDX.astype(np.uint16 if nv < 65535 else np.uint32).reshape(-1, 1), 5123 if nv < 65535 else 5125, 'SCALAR', 34963)
# image
views.append(dict(buffer=0, byteOffset=put(jpeg), byteLength=len(jpeg)))
img_bv = len(views) - 1
# compact the accessor list (drop the axe's), remapping every reference
remap, final = {}, []
for i, acc in enumerate(accs):
    if acc is not None:
        remap[i] = len(final); final.append(acc)
js['accessors'] = final
js['bufferViews'] = views
for sk in js['skins']:
    sk['inverseBindMatrices'] = remap[sk['inverseBindMatrices']]
# the weapon_r IBM for the rolled rest: a fresh accessor (the old view may be shared)
views.append(dict(buffer=0, byteOffset=put(IBM_ALL.astype(np.float32).tobytes()), byteLength=IBM_ALL.astype(np.float32).nbytes))
js['accessors'].append(dict(bufferView=len(views) - 1, componentType=5126, count=int(len(IBM_ALL)), type='MAT4'))
js['skins'][0]['inverseBindMatrices'] = len(js['accessors']) - 1
for an in js.get('animations', []):
    for s in an['samplers']:
        s['input'] = remap[s['input']]; s['output'] = remap[s['output']]
js['meshes'] = [dict(name='sword', primitives=[dict(attributes=dict(POSITION=remap[a_pos], NORMAL=remap[a_nrm],
                     TEXCOORD_0=remap[a_uv], JOINTS_0=remap[a_j], WEIGHTS_0=remap[a_w]), indices=remap[a_i],
                     material=old_prim.get('material', 0))])]
nodes[mesh_i]['mesh'] = 0; nodes[mesh_i]['name'] = 'sword'
js['images'] = [dict(bufferView=img_bv, mimeType=cimg.get('mimeType', 'image/jpeg'), name='sword_color')]
js['materials'][0]['name'] = 'sword_material'
# sockets: re-use the axe's marker node as sword_edge (no re-indexing), append main_grip / main_tip
edge_i = nid.get('axe_edge')
blade_mid = 0.5 * (feat['grip_m'] / 2 + feat['guard_thick_m'] + (feat['grip_m'] / 2 + feat['guard_thick_m'] + feat['blade_m']))
if edge_i is not None:
    nodes[edge_i].update(name='sword_edge', translation=[0.0, blade_mid / su, 0.5 * feat['blade_width_at_guard_m'] / su],
                         rotation=[0, 0, 0, 1], scale=[1, 1, 1])
for nm, t in (('main_grip', [0.0, 0.0, 0.0]), ('main_tip', [float(v) / su for v in tip_l])):
    nodes.append(dict(name=nm, translation=[float(v) for v in t]))
    nodes[wr].setdefault('children', []).append(len(nodes) - 1)
js['buffers'] = [dict(byteLength=len(new_bin) + (-len(new_bin) % 4))]
js['asset']['generator'] = 'nb_w2 w3_skin.py (the JOIN sword) on a T12_5_guard template'
while len(new_bin) % 4: new_bin.append(0)
jb = json.dumps(js, separators=(',', ':')).encode(); jb += b' ' * (-len(jb) % 4)
with open(OUT, 'wb') as fo:
    fo.write(struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(jb) + 8 + len(new_bin)))
    fo.write(struct.pack('<I4s', len(jb), b'JSON')); fo.write(jb)
    fo.write(struct.pack('<I4s', len(new_bin), b'BIN\x00')); fo.write(bytes(new_bin))
Lr_ = L.lint(OUT)
rep = dict(features=feat, roll_deg=ROLL, frame="weapon_r local: origin the grip's middle on its axis, +Y to the tip, +Z an edge, X the flat normal",
           metres_per_weapon_r_unit=su, verts=nv, tris=int(len(IDX) // 3), tip_local_m=[round(float(v), 4) for v in tip_l],
           sockets={"main_grip": [0, 0, 0], "main_tip": [round(float(v), 4) for v in tip_l],
                    "sword_edge": [0, round(blade_mid, 4), round(0.5 * feat['blade_width_at_guard_m'], 4)]},
           weapon_r_joint_index=ji, joints=len(jnames), lint=dict(verdict=Lr_['verdict'], fails=Lr_['fails']),
           bytes=os.path.getsize(OUT))
print(json.dumps(rep, indent=1))
if OUTJ:
    json.dump(rep, open(OUTJ, "w"), indent=1)
