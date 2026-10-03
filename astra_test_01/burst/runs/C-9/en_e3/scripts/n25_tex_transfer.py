# EN-E3: carry a baked texture from one prep of a mesh to another prep of the SAME Tripo build at a different scale (larva 0.9 m <- worm
# 2.8 m). The two preps decimate separately, so their UVs differ and the worm's bake cannot be reused as is; and the paint sheet's cameras
# were laid out for the worm, so baking the sheet straight onto the larva smears it (seen: knobs and segment grooves lost). Here every
# larva texel's surface point is scaled by (dst/src length) -- n04 grounds and centres both preps the same way -- and takes the colour
# of the nearest worm texel (KD tree over the worm's on-mesh texels; the normal must agree within 60 deg, else the next nearest of 8).
#   python3 scripts/n25_tex_transfer.py <surface_dst.npz> <surface_src.npz> <tex_src.png> <scale dst->src> <out.png>
import sys, json, numpy as np
from PIL import Image
from scipy.spatial import cKDTree
SD, SS, TS, K, OUT = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
d = np.load(SD); s = np.load(SS); T = np.asarray(Image.open(TS).convert('RGB'))
md = d['tex_tri'] >= 0; ms = s['tex_tri'] >= 0
Pd = d['tex_pos'][md] * K; Nd = d['tex_nrm'][md]
Ps = s['tex_pos'][ms]; Ns = s['tex_nrm'][ms]; Cs = T[ms] if T.shape[:2] == ms.shape else np.asarray(Image.open(TS).convert('RGB').resize(ms.shape[::-1]))[ms]
tree = cKDTree(Ps); dist, idx = tree.query(Pd, k=8, workers=-1)
ok = np.einsum('nkj,nj->nk', Ns[idx], Nd) > 0.5
first = np.where(ok.any(1), ok.argmax(1), 0)
pick = idx[np.arange(len(idx)), first]
out = np.zeros(md.shape + (3,), np.uint8); out[md] = Cs[pick]
from scipy import ndimage   # pad the UV islands outward (nearest on-mesh texel) so mip levels never pull in black
_, (iy, ix) = ndimage.distance_transform_edt(~md, return_indices=True); out = out[iy, ix]
Image.fromarray(out).save(OUT)
print(json.dumps(dict(texels=int(md.sum()), median_dist_m=round(float(np.median(dist[np.arange(len(idx)), first])), 4),
                      p95_dist_m=round(float(np.quantile(dist[np.arange(len(idx)), first], 0.95)), 4), normal_ok_share=round(float(ok.any(1).mean()), 4))))
