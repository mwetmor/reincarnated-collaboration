# R-C9-237 (Matt: "a blown-out bright-white patch on her forehead and eyes"): it is NOT skin -- it is SEE-THROUGH. Fix G takes
# ALL her hair inside while the hood is worn, and on her one-shell body the hair IS the scalp: the forehead/crown triangles
# under the brim went with it, and so did the surface behind the hood's open crown (R-C9-152's 1.28 m of open edge), so
# through the opening the ray reaches the snow (the probe's ID pass: those pixels are no surface of hers at all).
# A SCALP for the hood: the hood piece gains one more primitive, a copy of her HEAD hair surface (hair above 1.40 m, braid
# excluded, the front hair included) pushed IN by OFFSET_M (so the untucked hair would cover it -- but it leaves with the
# hood anyway), skinned with the hair's weights, wearing ONE skin texel of the hood's own atlas (the texel nearest
# --skin RGB among the hood's own atlas texels in the face region). Worn only while the hood is: G takes it off with it.
#   python3 r233_08_scalp.py <body.glb> <hood_in.glb> <hood_out.glb> <hair_mask.npy> <braid_mask.npy> [--offset 0.003]
#                            [--skin 178,134,102] [--brow 1.60] [--center 0,1.58,-0.015] [--radius 0.12] [--on-face 0.008] [--json rep.json]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
a = sys.argv[1:]
BODY, HIN, HOUT, MASK, BRAID = a[0], a[1], a[2], a[3], a[4]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
OFFSET = opt('--offset', 0.003)
SKIN = np.array([float(x) for x in (a[a.index('--skin') + 1] if '--skin' in a else '178,134,102').split(',')]) / 255.0
REP = a[a.index('--json') + 1] if '--json' in a else None


def mesh_world(js, b):
    G, _ = W.globals_(js)
    mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
    sk = js['skins'][js['nodes'][mi]['skin']]; ibm = W.mat_list(js, b, sk['inverseBindMatrices'])
    pr = js['meshes'][js['nodes'][mi]['mesh']]['primitives'][0]
    R = {k: L.read_accessor(js, b, v) for k, v in pr['attributes'].items()}
    R['I'] = L.read_accessor(js, b, pr['indices']).astype(int).reshape(-1, 3)
    J = R['JOINTS_0'].astype(int); Wt = R['WEIGHTS_0']
    Mj = np.array([G[j] @ ibm[k] for k, j in enumerate(sk['joints'])])        # per skin joint: global x IBM
    M = np.einsum('vk,vkij->vij', Wt, Mj[J])                                  # per vertex skin matrix at rest
    P = np.einsum('vij,vj->vi', M, np.c_[R['POSITION'], np.ones(len(J))])[:, :3]
    N = np.einsum('vij,vj->vi', M[:, :3, :3], R['NORMAL']); N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
    names = [js['nodes'][j]['name'] for j in sk['joints']]
    return dict(G=G, mi=mi, sk=sk, ibm=ibm, Mj=Mj, pr=pr, R=R, P=P, N=N, names=names)


bj, bb = L.load_glb(BODY); B = mesh_world(bj, bb)
hj, hb = L.load_glb(HIN); hb = bytearray(hb); H = mesh_world(hj, bytes(hb))
hair = np.load(MASK); assert len(hair) == len(B['P'])
Gn = {n.get('name'): i for i, n in enumerate(bj['nodes'])}
braid = np.load(BRAID)
# the SKULL's hair only: front strands that hang in front of the face below the brow (z > 0.035 m and y < BROW_M) would
# become skin-coloured ribbons across it, so they are left out
BROW_M = opt('--brow', 1.60)
# and ONLY ON THE SKULL: within RADIUS of the skull's centre (y scaled 0.85) -- the long strands that hang OUTSIDE the
# hood at her sides would otherwise come out as skin-coloured ribbons (seen at heading E on the first cut)
CEN = np.array([float(x) for x in (a[a.index('--center') + 1] if '--center' in a else '0,1.58,-0.015').split(',')])
RAD = opt('--radius', 0.12)
rr = np.linalg.norm((B['P'] - CEN) * np.array([1.0, 0.85, 1.0]), axis=1)
cap = hair & ~braid & (B['P'][:, 1] > 1.40) & ~((B['P'][:, 2] > 0.035) & (B['P'][:, 1] < BROW_M)) & (rr < RAD)
# R-C9-237: and every front strand that LIES ON the face (within ON_FACE_M of her face skin): on the one-shell body there
# is no skin under such a strand -- the strand WAS the surface -- so tucking it opened a hole in her face (the white at
# her eyes, the snow seen through). Its scalp copy, skin-coloured and 3 mm in, fills it; strands hanging AWAY from the
# face stay out (they would be skin ribbons)
from scipy.spatial import cKDTree as _KD
ON_FACE_M = opt('--on-face', 0.008)
fskin = (~hair) & (B['P'][:, 1] > 1.45) & (B['P'][:, 1] < 1.67) & (B['P'][:, 2] > 0.03)
onface = hair & ~braid & (B['P'][:, 2] > 0.035) & (_KD(B['P'][fskin]).query(B['P'])[0] < ON_FACE_M)
cap = cap | onface
tri = B['R']['I']; keep = cap[tri].all(axis=1); T = tri[keep]
used = np.unique(T); remap = -np.ones(len(cap), int); remap[used] = np.arange(len(used))
Pw = B['P'][used] - B['N'][used] * OFFSET
# skin: the hair's own weights, joints renamed into the hood's joint list
jmap = np.array([H['names'].index(n) for n in B['names']])
Jc = jmap[B['R']['JOINTS_0'].astype(int)[used]]; Wc = B['R']['WEIGHTS_0'][used]
Mc = np.einsum('vk,vkij->vij', Wc, H['Mj'][Jc])
Pb = np.array([np.linalg.solve(m, np.append(p, 1.0))[:3] for m, p in zip(Mc, Pw)])
Nb = np.array([np.linalg.solve(m[:3, :3], n) for m, n in zip(Mc, B['N'][used])]); Nb /= np.linalg.norm(Nb, axis=1, keepdims=True)
# UV: ONE texel of the hood atlas, the nearest to SKIN in colour (5x5 mean), searched over the whole atlas
import io
from PIL import Image
im = hj['images'][hj['textures'][hj['materials'][H['pr'].get('material', 0)]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']]
bv = hj['bufferViews'][im['bufferView']]
TX = np.asarray(Image.open(io.BytesIO(bytes(hb[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]))).convert('RGB').resize((256, 256), Image.BOX)).astype(float) / 255
dd = np.linalg.norm(TX - SKIN[None, None, :], axis=2); iy, ix = np.unravel_index(int(np.argmin(dd)), dd.shape)
uv0 = np.array([(ix + 0.5) / 256.0, (iy + 0.5) / 256.0], np.float32)
UV = np.tile(uv0, (len(used), 1))
d_ = np.array([float(dd[iy, ix])])
# APPEND the primitive
def acc(arr, typ, ct=5126, target=None, mm=False):
    arr = np.ascontiguousarray(arr); data = arr.tobytes(); off = W.append(hb, data)
    bv = {"buffer": 0, "byteOffset": off, "byteLength": len(data)}
    if target: bv["target"] = target
    hj['bufferViews'].append(bv)
    x = {"bufferView": len(hj['bufferViews']) - 1, "componentType": ct, "count": int(arr.shape[0]), "type": typ}
    if mm: x["min"] = arr.min(0).tolist(); x["max"] = arr.max(0).tolist()
    hj['accessors'].append(x); return len(hj['accessors']) - 1
prim = {"attributes": {"POSITION": acc(Pb.astype(np.float32), "VEC3", target=34962, mm=True),
                       "NORMAL": acc(Nb.astype(np.float32), "VEC3", target=34962),
                       "TEXCOORD_0": acc(UV.astype(np.float32), "VEC2", target=34962),
                       "JOINTS_0": acc(Jc.astype(np.uint16), "VEC4", ct=5123, target=34962),
                       "WEIGHTS_0": acc(Wc.astype(np.float32), "VEC4", target=34962)},
        "indices": acc(remap[T].astype(np.uint32).reshape(-1), "SCALAR", ct=5125, target=34963),
        "material": H['pr'].get('material', 0)}
hm = hj['meshes'][hj['nodes'][H['mi']]['mesh']]
hm['primitives'].append(prim)
hj['buffers'][0]['byteLength'] = len(hb)
R_.write_glb(HOUT, hj, hb)
rep = dict(on_face_m=ON_FACE_M, on_face_verts=int(onface.sum()), body=BODY, hood_in=HIN, hood_out=HOUT, offset_m=OFFSET, scalp_verts=int(len(used)), scalp_tris=int(len(T)),
           scalp_y=[round(float(Pw[:, 1].min()), 3), round(float(Pw[:, 1].max()), 3)], skin_target=(SKIN * 255).round(1).tolist(),
           skin_texel=(TX[iy, ix] * 255).round(1).tolist(), skin_uv=uv0.tolist(), primitives=len(hm['primitives']))
print(json.dumps(rep))
if REP: json.dump(rep, open(REP, 'w'), indent=1)
