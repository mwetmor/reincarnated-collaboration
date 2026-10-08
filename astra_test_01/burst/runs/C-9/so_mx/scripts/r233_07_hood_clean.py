# R-C9-236 (Matt, fix G + "cleaner rim"): the DARK SPECKLE round the hood's face opening is in the TEXTURE, not only the
# pen: her hood was cut from a whole-character bake, and its shell's vertices round the opening (and a scatter elsewhere)
# sample the atlas's HAIR and shadow texels -- dark brown dots on red cloth, which at the play camera read as a ragged
# dark outline round her face (it stays with the pen OFF). Here every hood-shell vertex (primitive 0) whose own texel is
# DARK (5x5 mean luma < DARK) or NOT the cloth (hue outside the reds, or brown) takes the UV of the nearest red-fabric
# vertex of the same shell (R-C9-152's cap rule), so the cloth reads as cloth to its edge. Light texels (the fur trim,
# luma >= LIGHT) are kept. Primitive 1 (the cap) already wears red-fabric UVs; the lining primitives are one texel.
# Geometry, joints and weights untouched; only TEXCOORD_0 of primitive 0 is rewritten (a new accessor).
#   python3 r233_07_hood_clean.py <hood.glb> <out.glb> [--dark 70] [--light 150] [--rim-m 0.06] [--smooth-rim 3] [--smooth-band 0.04,6] [--cap-too] [--report out.json]
import sys, os, io, json, colorsys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
IN, OUT = sys.argv[1], sys.argv[2]
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
DARK, LIGHT = float(arg('--dark', 70)), float(arg('--light', 150))
js, b = L.load_glb(IN); b = bytearray(b)
bv = js['bufferViews'][js['images'][0]['bufferView']]
T = np.asarray(Image.open(io.BytesIO(bytes(b[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]))).convert('RGB')).astype(float)
H, Wd = T.shape[:2]
pr = js['meshes'][0]['primitives'][0]
P = L.read_accessor(js, bytes(b), pr['attributes']['POSITION']); UV = L.read_accessor(js, bytes(b), pr['attributes']['TEXCOORD_0']).astype(np.float32)
px = np.clip((UV[:, 0] % 1) * Wd, 0, Wd - 1).astype(int); py = np.clip((UV[:, 1] % 1) * H, 0, H - 1).astype(int)
acc = np.zeros((len(P), 3))
for dx in (-2, -1, 0, 1, 2):
    for dy in (-2, -1, 0, 1, 2):
        acc += T[np.clip(py + dy, 0, H - 1), np.clip(px + dx, 0, Wd - 1)]
c = acc / 25
lum = 0.2126 * c[:, 0] + 0.7152 * c[:, 1] + 0.0722 * c[:, 2]
hsv = np.array([colorsys.rgb_to_hsv(*(x / 255)) for x in c])
red = (hsv[:, 1] > 0.40) & ((hsv[:, 0] < 0.045) | (hsv[:, 0] > 0.94)) & (lum >= DARK)
redsrc = red.copy()                                   # UV sources: well-lit red cloth only
red = (hsv[:, 1] > 0.35) & ((hsv[:, 0] < 0.06) | (hsv[:, 0] > 0.93)) & (lum >= 0.5 * DARK)   # kept: red cloth incl. its painted shade
light = lum >= LIGHT
bad = ~red & ~light
# ONLY ROUND THE FACE OPENING (--rim-m): the shell's open-edge vertices in front of her head (z > 0, y > 1.40 m,
# |x| < 0.16 m) are the opening's rim; vertices within RIM_M of them are the band cleaned. The rest of the hood keeps
# its painted folds and shading.
RIM_M = float(arg('--rim-m', 0.06))
I = L.read_accessor(js, bytes(b), pr['indices']).astype(int).reshape(-1, 3)
key = np.round(P / 1e-5).astype(np.int64); _, wid = np.unique(key, axis=0, return_inverse=True); wid = wid.ravel()
E = np.sort(np.concatenate([wid[I[:, [0, 1]]], wid[I[:, [1, 2]]], wid[I[:, [2, 0]]]]), 1)
ue, ce = np.unique(E, axis=0, return_counts=True); bset = np.zeros(wid.max() + 1, bool); bset[ue[ce == 1].ravel()] = True
isb = bset[wid] & (P[:, 2] > 0.0) & (P[:, 1] > 1.40) & (np.abs(P[:, 0]) < 0.16)
from scipy.spatial import cKDTree as _K
near = _K(P[isb]).query(P)[0] <= RIM_M
bad = bad & near
src = np.nonzero(redsrc)[0]; dst = np.nonzero(bad)[0]
from scipy.spatial import cKDTree
d, j = cKDTree(P[src]).query(P[dst])
UV2 = UV.copy(); UV2[dst] = UV[src[j]]
# --smooth-rim N: the opening's rim is a RAGGED open edge (a cut from a whole-character mesh), and the screen pen traces
# every jog of it as a zig-zag round her face. N passes of boundary-only Laplacian smoothing (each rim vertex moves half
# way to the mean of its two rim neighbours, coincident vertices moved together); the lining primitives -- built vertex
# for vertex from this shell (r233_05) -- take the same offsets so the lining stays 2.5 mm inside. Bind-space positions
# only; joints, weights and normals untouched.
NS = int(arg('--smooth-rim', 0))
moved = 0
if NS > 0:
    be = ue[ce == 1]
    rimw = set(np.unique(wid[isb]).tolist())
    nb = {}
    for a_, b_ in be:
        if a_ in rimw and b_ in rimw:
            nb.setdefault(a_, []).append(b_); nb.setdefault(b_, []).append(a_)
    Pw = np.zeros((wid.max() + 1, 3)); Pw[wid] = P
    P0w = Pw.copy()
    for _ in range(NS):
        Pn = Pw.copy()
        for v_, ns_ in nb.items():
            if len(ns_) == 2:
                Pn[v_] = 0.5 * Pw[v_] + 0.5 * Pw[ns_].mean(0)
        Pw = Pn
    # --smooth-band M,K: then K passes of Laplacian smoothing over EVERY shell vertex within M of the rim (the brim's
    # crumpled fold, whose every jog the pen draws), each moving half way to the mean of its welded neighbours; the
    # band's own outer edge fades the step to zero so nothing tears where the band meets the untouched shell
    if '--smooth-band' in sys.argv:
        BM, BK = [float(x) for x in arg('--smooth-band', '0.04,6').split(',')]
        dist_w = np.full(wid.max() + 1, 9.0); dist_w[wid] = _K(P[isb]).query(P)[0]
        fw = np.clip(1.0 - dist_w / BM, 0.0, 1.0)
        Ew = np.unique(np.sort(np.concatenate([wid[I[:, [0, 1]]], wid[I[:, [1, 2]]], wid[I[:, [2, 0]]]]), 1), axis=0)
        from scipy.sparse import coo_matrix
        nW = wid.max() + 1
        A = coo_matrix((np.ones(len(Ew) * 2), (np.r_[Ew[:, 0], Ew[:, 1]], np.r_[Ew[:, 1], Ew[:, 0]])), shape=(nW, nW)).tocsr()
        deg = np.asarray(A.sum(1)).ravel(); deg[deg == 0] = 1
        for _ in range(int(BK)):
            M_ = (A @ Pw) / deg[:, None]
            Pw = Pw + (0.5 * fw)[:, None] * (M_ - Pw)
    D = (Pw - P0w)[wid].astype(np.float32)
    moved = int((np.linalg.norm(D, axis=1) > 1e-6).sum())
    def set_pos(prim, delta):
        Q = L.read_accessor(js, bytes(b), prim['attributes']['POSITION']).astype(np.float32) + delta
        rq = np.ascontiguousarray(Q).tobytes(); oq = W.append(b, rq)
        js['bufferViews'].append({"buffer": 0, "byteOffset": oq, "byteLength": len(rq)})
        js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(Q)), "type": "VEC3",
                                "min": Q.min(0).tolist(), "max": Q.max(0).tolist()})
        prim['attributes']['POSITION'] = len(js['accessors']) - 1
    set_pos(pr, D)
    for prim in js['meshes'][0]['primitives'][1:]:
        if js['accessors'][prim['attributes']['POSITION']]['count'] == len(P):
            set_pos(prim, D)           # the shell's lining (same vertex order)
    rim_move = np.linalg.norm(D, axis=1)
# --cap-too: the CAP (primitive 1, R-C9-152) sits on her forehead under the brim, and its vertices wear the nearest
# red-fabric texel of the shell -- including the shell's SHADED reds, a mottled dark band along the top of the opening.
# In the rim band every cap vertex darker than DARK takes the nearest well-lit red-fabric shell UV too.
cap_re = 0
if '--cap-too' in sys.argv:
    cp = js['meshes'][0]['primitives'][1]
    Pc = L.read_accessor(js, bytes(b), cp['attributes']['POSITION']); UVc = L.read_accessor(js, bytes(b), cp['attributes']['TEXCOORD_0']).astype(np.float32)
    qx = np.clip((UVc[:, 0] % 1) * Wd, 0, Wd - 1).astype(int); qy = np.clip((UVc[:, 1] % 1) * H, 0, H - 1).astype(int)
    ac = np.zeros((len(Pc), 3))
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            ac += T[np.clip(qy + dy, 0, H - 1), np.clip(qx + dx, 0, Wd - 1)]
    ac /= 25; lc = 0.2126 * ac[:, 0] + 0.7152 * ac[:, 1] + 0.0722 * ac[:, 2]
    nearc = _K(P[isb]).query(Pc)[0] <= RIM_M
    badc = np.nonzero(nearc & (lc < DARK))[0]
    _, jc = cKDTree(P[src]).query(Pc[badc])
    UVc2 = UVc.copy(); UVc2[badc] = UV[src[jc]]
    rc = np.ascontiguousarray(UVc2).tobytes(); oc = W.append(b, rc)
    js['bufferViews'].append({"buffer": 0, "byteOffset": oc, "byteLength": len(rc)})
    js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(UVc2)), "type": "VEC2"})
    cp['attributes']['TEXCOORD_0'] = len(js['accessors']) - 1
    cap_re = int(len(badc))
raw = np.ascontiguousarray(UV2).tobytes(); o = W.append(b, raw)
js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(raw)})
js['accessors'].append({"bufferView": len(js['bufferViews']) - 1, "componentType": 5126, "count": int(len(UV2)), "type": "VEC2"})
pr['attributes']['TEXCOORD_0'] = len(js['accessors']) - 1
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, b)
rep = {"in": IN, "out": OUT, "dark": DARK, "light": LIGHT, "rim_m": RIM_M, "rim_verts": int(isb.sum()), "band_verts": int(near.sum()), "shell_verts": int(len(P)), "red_fabric": int(red.sum()),
       "light_kept": int(light.sum()), "re_uv": int(bad.sum()), "uv_source_dist_m": {"median": round(float(np.median(d)), 4),
       "p95": round(float(np.percentile(d, 95)), 4), "max": round(float(d.max()), 4)},
       "cap_re_uv": cap_re, "smooth_rim_passes": NS, "rim_verts_moved": moved, "rim_move_max_m": round(float(rim_move.max()), 4) if NS > 0 else 0.0}
print(json.dumps(rep))
if '--report' in sys.argv:
    json.dump(rep, open(arg('--report', ''), 'w'), indent=1)
