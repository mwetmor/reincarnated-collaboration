# R-C9-233 step 1: her body for the face-under-the-hood fix, built from the same base as ss152b (work/ss138a_pre.glb).
#   hood_braid (the gear-state morph knight.gd's morph_rules drive while the hood is worn) now ALSO tucks the FRONT STRANDS
#   THAT CROSS HER FACE behind the hood rim: front hair (r140 hair mask, z > 0.035 m) above the chin (y > 1.44 m) and
#   within the face's width, weighted 1 at |x| <= X_IN and fading to 0 at X_OUT -- so the cheek strands beyond the face's
#   edge stay and still frame it (R-C9-233 narrows R-C9-152's "face and front hair untouched" to this). Tucked = pulled
#   into the skull, R-C9-140's method (toward the middle of the vertex's dominant bone), scaled by the weight. The braid
#   part of hood_braid is ss152b's exactly (r152_braid_mask, weight 1). Taking the hood off (G) releases all of it.
#   --lift G,K  ALSO lifts the FACE island of the atlas (r233 class texture, red) -- the painted skin AND the painted hair
#   streaks inside it -- by out = 255 * (in/255)^G * K (default 0.75, 1.12): a lighter face under the hood at every heading
#   and lighting. The new PNG is appended to the buffer and the image re-pointed (the old bytes stay: +~4 MB).
#   --tuck-all  hood_braid takes ALL her hair inside while the hood is worn except the cheek strands that frame the face
#   --lift-head the lift also covers every non-hair head/neck triangle above 1.42 m
#   --clean-brow Y  repaint the non-hair head texels above Y m (the forehead's painted fringe) as her lifted skin
#   python3 r233_04_build.py <base.glb> <out.glb> [--tuck-all] [--lift-head] [--clean-brow 1.60] [--knee 1.15] [--keep-face-surface 0.006] [--lift 0.75,1.12] [--xin 0.060] [--xout 0.080] [--report out.json]
import sys, os, io, json, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones'); R_ = __import__('49_recentre')
WORK = os.path.join(HERE, '..', 'work')
IN, OUT = sys.argv[1], sys.argv[2]
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
X_IN, X_OUT = float(arg('--xin', 0.060)), float(arg('--xout', 0.080))
CHILD = {"Head": "head_end", "neck": "Head", "Spine": "neck", "Spine01": "Spine", "Spine02": "Spine01", "Hips": "Spine02",
         "LeftShoulder": "neck", "RightShoulder": "neck"}
js, b = L.load_glb(IN); b = bytearray(b)
G, _ = W.globals_(js)
mi = next(i for i, n in enumerate(js['nodes']) if 'mesh' in n and 'skin' in n)
mesh = js['meshes'][js['nodes'][mi]['mesh']]; pr = mesh['primitives'][0]
names = mesh.get('extras', {}).get('targetNames', [])
assert 'hood_braid' not in names and 'hood_hair' not in names, names
sk = js['skins'][js['nodes'][mi]['skin']]; jn = [js['nodes'][j]['name'] for j in sk['joints']]
ibm = W.mat_list(js, bytes(b), sk['inverseBindMatrices'])
V = L.read_accessor(js, bytes(b), pr['attributes']['POSITION'])
J = L.read_accessor(js, bytes(b), pr['attributes']['JOINTS_0']).astype(int)
Wt = L.read_accessor(js, bytes(b), pr['attributes']['WEIGHTS_0'])
Vr = W.skin_rest(js, bytes(b), mi, G)                     # rest positions, metres, Y up, +Z her facing
hair = np.load(os.path.join(WORK, 'r140_hair_mask.npy')); braid = np.load(os.path.join(WORK, 'r152_braid_mask.npy'))
assert len(hair) == len(V) == len(braid)
ax = np.abs(Vr[:, 0])
wx = np.clip((X_OUT - ax) / max(X_OUT - X_IN, 1e-6), 0.0, 1.0)
tuck = hair & ~braid & (Vr[:, 2] > 0.035) & (Vr[:, 1] > 1.44) & (wx > 0)
w = np.zeros(len(V)); w[braid] = 1.0; w[tuck] = wx[tuck]
# --tuck-all: EVERY hair vertex under the hood goes in (R-C9-140's hood_hair reach, now that R-C9-152's cap closes the crown),
# EXCEPT the front strands beyond the face's width, which keep framing it (weighted as above)
if '--tuck-all' in sys.argv:
    frame = hair & ~braid & (Vr[:, 2] > 0.035) & (Vr[:, 1] > 1.44)
    w[hair & ~frame] = 1.0
    tuck = tuck | (hair & ~frame & ~braid)
# R-C9-237: hair-CLASSED vertices that ARE her face's surface (r140's island test calls every dark head island hair: her
# brows and eye region are among them) stay where they are. Tucking them opened holes in her face -- the "blown-out
# white" at her eyes was the snow seen through. Test: front (z > 0.035), in the face's height band, and not standing
# more than FACE_TOL in front of the face skin at the same (x, y) (a strand hanging in front stands 1-4 cm off it)
if '--keep-face-surface' in sys.argv:
    from scipy.spatial import cKDTree as _KD2
    FACE_TOL = float(arg('--keep-face-surface', 0.006))
    fsk = (~hair) & (Vr[:, 1] > 1.45) & (Vr[:, 1] < 1.70) & (Vr[:, 2] > 0.03)
    dd2, jj2 = _KD2(Vr[fsk][:, :2]).query(Vr[:, :2])
    zsk = Vr[fsk][jj2, 2]
    onsurf = hair & ~braid & (Vr[:, 2] > 0.035) & (Vr[:, 1] > 1.44) & (Vr[:, 1] < 1.70) & (dd2 < 0.01) & (Vr[:, 2] <= zsk + FACE_TOL)
    w[onsurf] = 0.0
    rep_keep = int(onsurf.sum())
idx = np.nonzero(w > 0)[0]
nid = {n.get('name'): i for i, n in enumerate(js['nodes'])}
D = np.zeros((len(idx), 3))
for k, v in enumerate(idx):
    Mv = sum(Wt[v, c] * (G[sk['joints'][J[v, c]]] @ ibm[J[v, c]]) for c in range(4))
    pw = (Mv @ np.append(V[v], 1))[:3]
    dom = jn[J[v, int(np.argmax(Wt[v]))]]
    a = G[nid[dom]][:3, 3]; c_ = G[nid[CHILD.get(dom, dom)]][:3, 3]
    tgt = a + 0.5 * (c_ - a)
    D[k] = w[v] * np.linalg.solve(Mv[:3, :3], tgt - pw)


def add_sparse(vals):
    ii = idx.astype(np.uint32).tobytes(); vv = np.asarray(vals, np.float32).tobytes()
    oi = W.append(b, ii); js['bufferViews'].append({"buffer": 0, "byteOffset": oi, "byteLength": len(ii)})
    bi = len(js['bufferViews']) - 1
    ov = W.append(b, vv); js['bufferViews'].append({"buffer": 0, "byteOffset": ov, "byteLength": len(vv)})
    bv = len(js['bufferViews']) - 1
    full = np.zeros((len(V), 3), np.float32); full[idx] = vals
    js['accessors'].append({"componentType": 5126, "count": int(len(V)), "type": "VEC3",
                            "min": full.min(0).tolist(), "max": full.max(0).tolist(),
                            "sparse": {"count": int(len(idx)), "indices": {"bufferView": bi, "componentType": 5125},
                                       "values": {"bufferView": bv}}})
    return len(js['accessors']) - 1


for p in mesh['primitives']:
    p.setdefault('targets', []).append({"POSITION": add_sparse(D), "NORMAL": add_sparse(np.zeros_like(D))})
mesh.setdefault('extras', {})['targetNames'] = names + ['hood_braid']
if 'weights' in mesh: mesh['weights'] = list(mesh['weights']) + [0.0]
rep = {"base": IN, "out": OUT, "x_in": X_IN, "x_out": X_OUT, "braid_verts": int(braid.sum()),
       "tuck_verts": int(tuck.sum()), "tuck_full_weight": int((tuck & (wx >= 1)).sum()),
       "front_hair_kept_untucked": int((hair & ~braid & (Vr[:, 2] > 0.035) & ~tuck).sum()),
       "max_delta_bind_units": float(np.linalg.norm(D, axis=1).max())}
if '--lift' in sys.argv:
    g, kk = [float(x) for x in arg('--lift', '0.75,1.12').split(',')]
    im = js['images'][js['textures'][js['materials'][0]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']]
    bvw = js['bufferViews'][im['bufferView']]
    T = Image.open(io.BytesIO(bytes(b[bvw.get('byteOffset', 0):bvw.get('byteOffset', 0) + bvw['byteLength']]))).convert('RGB')
    C = Image.open(os.path.join(WORK, 'r233', 'class.png')).resize(T.size, Image.NEAREST)
    M = np.asarray(C.convert('RGB'))[..., 0] > 128
    if '--lift-head' in sys.argv:
        # ALSO every non-hair triangle of the head and neck above 1.42 m (ears, temples, the neck under the hood: painted
        # dark like the face, and inside the opening)
        from PIL import ImageDraw
        UVb = L.read_accessor(js, bytes(b), pr['attributes']['TEXCOORD_0'])
        IDXb = L.read_accessor(js, bytes(b), pr['indices']).astype(int).reshape(-1, 3)
        Cn = Vr[IDXb].mean(1); sel = (hair[IDXb].sum(1) < 2) & (Cn[:, 1] > 1.42)
        hm = Image.new('L', T.size, 0); dd = ImageDraw.Draw(hm)
        for tri in np.nonzero(sel)[0]:
            uv = UVb[IDXb[tri]] % 1.0
            dd.polygon([(float(u * T.size[0]), float(v * T.size[1])) for u, v in uv], fill=255)
        M = M | (np.asarray(hm) > 127)
    M = np.asarray(Image.fromarray((M * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 127   # the island's gutter too
    A = np.asarray(T).astype(float) / 255.0
    lum0 = float((0.2126 * A[..., 0] + 0.7152 * A[..., 1] + 0.0722 * A[..., 2])[M].mean() * 255)
    A2 = A.copy(); A2[M] = np.clip(np.power(A[M], g) * kk, 0, 1)
    if '--clean-brow' in sys.argv:
        # THE FOREHEAD UNDER THE HOOD RIM: the face island's texels above BROW_Y carry PAINTED hair streaks (the bake
        # projected her fringe onto the skin); with the fringe tucked they read as a dark band under the rim. Repainted
        # as her own lifted skin: every texel of a non-hair head triangle above BROW_Y takes the median lifted skin colour
        # of the face island's light half, its own luminance variation kept at 25%
        from PIL import ImageDraw
        BROW_Y = float(arg('--clean-brow', 1.60))
        UVb = L.read_accessor(js, bytes(b), pr['attributes']['TEXCOORD_0'])
        IDXb = L.read_accessor(js, bytes(b), pr['indices']).astype(int).reshape(-1, 3)
        Cn = Vr[IDXb].mean(1); sel = (hair[IDXb].sum(1) < 2) & (Cn[:, 1] > BROW_Y)
        hm = Image.new('L', T.size, 0); dd = ImageDraw.Draw(hm)
        for tri in np.nonzero(sel)[0]:
            uv = UVb[IDXb[tri]] % 1.0
            dd.polygon([(float(u * T.size[0]), float(v * T.size[1])) for u, v in uv], fill=255)
        Bm = np.asarray(hm.filter(ImageFilter.MaxFilter(5))) > 127
        lumA = 0.2126 * A2[..., 0] + 0.7152 * A2[..., 1] + 0.0722 * A2[..., 2]
        fm = M & ~Bm
        BROW_PCT = float(arg('--brow-pct', 50))     # R-C9-237: 50 = the lifted face's MEDIAN skin (G used the light half's median, which blew out)
        skin = np.median(A2[fm & (lumA >= np.percentile(lumA[fm], BROW_PCT))], axis=0) if BROW_PCT > 0 else np.median(A2[fm], axis=0)
        rel = lumA[Bm] / max(float(np.median(lumA[Bm])), 1e-3)
        A2[Bm] = np.clip(skin[None, :] * (0.75 + 0.25 * rel[:, None]), 0, 1)
        rep_brow = {"brow_y": BROW_Y, "brow_pct": BROW_PCT, "texels": int(Bm.sum()), "skin_rgb": (skin * 255).round(1).tolist()}
    if '--knee' in sys.argv:
        # R-C9-237 (Matt: "a blown-out bright-white patch on her forehead and eyes"): the face island's LIGHT texels -- the
        # painted eye whites and highlights -- are compressed toward its skin: any lifted texel brighter than KNEE x the
        # island's median skin luma is scaled down to it (hue kept), so nothing on the face reads whiter than lit skin
        KNEE = float(arg('--knee', 1.15))
        lumK = 0.2126 * A2[..., 0] + 0.7152 * A2[..., 1] + 0.0722 * A2[..., 2]
        cap_l = KNEE * float(np.median(lumK[M]))
        over = M & (lumK > cap_l)
        A2[over] = A2[over] * (cap_l / lumK[over])[:, None]
        rep_knee = {"knee": KNEE, "cap_luma": round(cap_l * 255, 1), "texels_compressed": int(over.sum())}
    lum1 = float((0.2126 * A2[..., 0] + 0.7152 * A2[..., 1] + 0.0722 * A2[..., 2])[M].mean() * 255)
    buf = io.BytesIO(); Image.fromarray((A2 * 255 + 0.5).astype(np.uint8)).save(buf, 'PNG'); nb = buf.getvalue()
    o = W.append(b, nb); js['bufferViews'].append({"buffer": 0, "byteOffset": o, "byteLength": len(nb)})
    im['bufferView'] = len(js['bufferViews']) - 1
    rep["lift"] = {"gamma": g, "gain": kk, "face_texels": int(M.sum()), "face_albedo_luma": [round(lum0, 1), round(lum1, 1)]}
    if '--clean-brow' in sys.argv:
        rep["clean_brow"] = rep_brow
    if '--knee' in sys.argv:
        rep["knee"] = rep_knee
if '--keep-face-surface' in sys.argv:
    rep["face_surface_hair_kept"] = rep_keep
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, b)
print(json.dumps(rep))
if '--report' in sys.argv:
    json.dump(rep, open(arg('--report', ''), 'w'), indent=1)
