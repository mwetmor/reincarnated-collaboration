# R-C9-152 (Matt, on the live R-C9-140 build): "the top of the head and back of the hood have become transparent ... We dont
# want to change the face/front of hair, and we only want to paint over the back of hair with the hood/body armor so the hair
# is worn under the hood".
#
# WHY IT WENT TRANSPARENT (r152_01_hood_holes.py): the hood piece is an OPEN shell -- 67 boundary loops, the largest on the
# crown (1.28 m of open edge at y 1.58-1.69) and round the back of the neck -- because the hood was cut from a model whose
# HAIR was the outer surface there. The hair filled those holes; R-C9-140's hood_hair morph pulled the hair inside her, and the
# holes (and the hood's culled inside, seen through the face opening) read as see-through.
#
# THE FIX, a HOOD CAP: the hair stays exactly as it is (no morph). The hood piece gains a second primitive -- a copy of the
# BACK and TOP hair surface (every hair vertex behind the face-front band, the braid included), pushed OUT along its normal by
# OFFSET_M, skinned with the hair's own weights and textured with the hood's own atlas (each vertex takes the UV of the nearest
# hood vertex). So with the hood worn, the back/top hair is covered by hood fabric and the holes are closed by it; the face and
# the front hair are untouched; take the hood off (G) and the cap goes with it -- the hair is back, unchanged.
#   python3 r152_02_hood_cap.py <body.glb> <hood_in.glb> <hood_out.glb> <hair_mask.npy> [--front-z 0.035] [--offset 0.004]
#                               [--no-braid] [--json rep.json]
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
a = sys.argv[1:]
BODY, HIN, HOUT, MASK = a[0], a[1], a[2], a[3]
opt = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
FRONT_Z = opt('--front-z', 0.035); OFFSET = opt('--offset', 0.004)
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
front = B['P'][:, 2] > FRONT_Z
cap = hair & ~front
if '--no-braid' in a:
    cap &= B['P'][:, 1] > 1.30
tri = B['R']['I']; keep = cap[tri].all(axis=1); T = tri[keep]
used = np.unique(T); remap = -np.ones(len(cap), int); remap[used] = np.arange(len(used))
Pw = B['P'][used] + B['N'][used] * OFFSET
# skin: the hair's own weights, joints renamed into the hood's joint list
jmap = np.array([H['names'].index(n) for n in B['names']])
Jc = jmap[B['R']['JOINTS_0'].astype(int)[used]]; Wc = B['R']['WEIGHTS_0'][used]
Mc = np.einsum('vk,vkij->vij', Wc, H['Mj'][Jc])
Pb = np.array([np.linalg.solve(m, np.append(p, 1.0))[:3] for m, p in zip(Mc, Pw)])
Nb = np.array([np.linalg.solve(m[:3, :3], n) for m, n in zip(Mc, B['N'][used])]); Nb /= np.linalg.norm(Nb, axis=1, keepdims=True)
# UV: the nearest hood vertex's -- among the hood vertices whose own texel is the RED OUTER FABRIC (its lining and hems
# are brown/peach; taking those made the cap read as more hair, measured on the first cut)
from scipy.spatial import cKDTree
import io, colorsys
from PIL import Image
im = hj['images'][hj['textures'][hj['materials'][H['pr'].get('material', 0)]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']]
bv = hj['bufferViews'][im['bufferView']]
TX = np.asarray(Image.open(io.BytesIO(bytes(hb[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]))).convert('RGB')).astype(float) / 255
huv = H['R']['TEXCOORD_0']; th, tw = TX.shape[:2]
col = TX[np.clip(((huv[:, 1] % 1) * th).astype(int), 0, th - 1), np.clip(((huv[:, 0] % 1) * tw).astype(int), 0, tw - 1)]
hsv = np.array([colorsys.rgb_to_hsv(*c) for c in col])
red = ((hsv[:, 0] < 0.05) | (hsv[:, 0] > 0.95)) & (hsv[:, 1] > 0.45) & (hsv[:, 2] > 0.35)
d_, nn = cKDTree(H['P'][red]).query(Pw)
UV = huv[np.nonzero(red)[0][nn]]
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
rep = dict(body=BODY, hood_in=HIN, hood_out=HOUT, front_z=FRONT_Z, offset_m=OFFSET, braid=('--no-braid' not in a),
           hair_verts=int(hair.sum()), front_hair_kept=int((hair & front).sum()), cap_verts=int(len(used)), cap_tris=int(len(T)),
           cap_y=[round(float(Pw[:, 1].min()), 3), round(float(Pw[:, 1].max()), 3)],
           red_fabric_hood_verts=int(red.sum()), uv_source_dist_m=dict(median=round(float(np.median(d_)), 4), p95=round(float(np.percentile(d_, 95)), 4), max=round(float(d_.max()), 4)))
print(json.dumps(rep))
if REP: json.dump(rep, open(REP, 'w'), indent=1)
