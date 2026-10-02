# EN-E3 eyes (the conductor's MENACE note on the gazer): find the painted eyes on the surface, ship them as an EMISSIVE map (costume
# emission, contract 2.2 allows it: steady, no flicker), and write the two eye positions (rest, world) for the runtime glare-flare sprite.
#   python3 scripts/n09b_eyes.py <surface.npz> <tex.png: the TRIPO projection -- the gazer's paint sheet placed no cool-white eye> <out_emissive.png> <out.json> [head_len_m]
# An eye texel: inside the head (the front head_len of the body), pale (lum > 150) and cool (G >= R) -- the pale verdigris-white the
# sheet paints the eye -- and not the ivory horns (warm: R > G). Clustered left/right; each eye's emissive patch is its texels plus a
# 2 px rim, coloured pale verdigris-white.
import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage
NPZ, TEX, OUTE, OUTJ = sys.argv[1:5]; HL = float(sys.argv[5]) if len(sys.argv) > 5 else 0.45
d = np.load(NPZ); P = d['tex_pos']; on = d['tex_tri'] >= 0
A = np.asarray(Image.open(TEX).convert('RGB')).astype(np.float32)
if A.shape[0] != P.shape[0]: A = np.asarray(Image.open(TEX).convert('RGB').resize((P.shape[1], P.shape[0]))).astype(np.float32)
if np.mean(A.mean(2)[on[::-1]] > 3) > np.mean(A.mean(2)[on] > 3): P = P[::-1]; on = on[::-1]
y0 = P[on][:, 1].min()
head = on & (P[..., 1] < y0 + HL)
R, G, B = A[..., 0], A[..., 1], A[..., 2]; lum = A.mean(2)
eye = head & (lum > 150) & (G >= R) & (G - B > -10) & (P[..., 2] > np.quantile(P[head][:, 2], 0.25)) & (np.abs(P[..., 0]) > 0.03)   # not the snout tip
eye = eye & ndimage.binary_dilation(eye, iterations=1, structure=np.ones((3, 3))) & (ndimage.uniform_filter(eye.astype(float), 3) > 0.3)   # drop isolated speckle texels
out = {}
for side, sg in (('L', 1), ('R', -1)):
    m = eye & (P[..., 0] * sg > 0.02)
    lab, n = ndimage.label(m)
    if n == 0: continue
    sizes = ndimage.sum(m, lab, range(1, n + 1)); k = 1 + int(np.argmax(sizes)); mm = lab == k
    out[side] = dict(center_m=[round(float(v), 4) for v in P[mm].mean(0)], texels=int(mm.sum()),
                     extent_m=round(float(np.ptp(P[mm], 0).max()), 4))
    eye = eye & ~(m & ~mm)
# a side the colour test missed (the gazer's right eye is painted darker) is MIRRORED from the found one: the body is symmetric
for a_, b_ in (('L', 'R'), ('R', 'L')):
    if a_ in out and b_ not in out:
        c = list(out[a_]['center_m']); c[0] = -c[0]; out[b_] = dict(center_m=c, texels=0, extent_m=out[a_]['extent_m'], mirrored_from=a_)
# the emissive patch = every surface texel within the eye's radius of its centre (3D), so both eyes get the same disc
eye = np.zeros(on.shape, bool)
for v in out.values():
    eye |= on & (np.linalg.norm(P - np.array(v['center_m']), axis=2) < max(0.6 * v['extent_m'], 0.03))
E = np.zeros(A.shape, np.float32)
rim = ndimage.binary_dilation(eye, iterations=2)
E[rim] = (196, 236, 214); E[eye] = (226, 252, 236)
E = ndimage.gaussian_filter(E, (1.0, 1.0, 0))
Image.fromarray(np.clip(E, 0, 255).astype(np.uint8)).save(OUTE)
json.dump(dict(eyes=out, emissive=OUTE, rule='head, lum>150, G>=R, upper half of the head; largest blob per side'), open(OUTJ, 'w'), indent=1)
print(json.dumps(out))
