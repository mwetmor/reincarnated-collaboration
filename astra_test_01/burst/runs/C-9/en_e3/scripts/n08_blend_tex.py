# EN-E3: the shipped texture = the D7 sheet-A bake where sheet A's 19.77-deg cameras SAW the surface face-on, and the Tripo texture
# (itself projected by Tripo from the approved painted model sheet) on the UPWARD-facing surfaces those low cameras only grazed.
#   python3 scripts/n08_blend_tex.py <prep.glb> <surface.npz> <tex_A.png> <out.png> [nz0 nz1]
# Why: on the maw, sheet A's paint of the back came out smeared -- the spurs Astra drew are not where the spur shells are, and at
# 19.77 deg the back is seen at ~20 deg incidence, so ivory spur paint landed across the whole back (measured at the game camera:
# blotches over every top surface). D7's own answer is a sheet B at 52.95 deg; this lane's image cap does not stretch to a second
# paint sheet for every creature, so the top falls back to Tripo's projection of the approved sheet, blended by world normal z.
import io, json, struct, sys
import numpy as np
from PIL import Image
from scipy import ndimage
GLB, NPZ, TA, OUT = sys.argv[1:5]
nz0, nz1 = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (0.30, 0.60)
b = open(GLB, 'rb').read(); n = struct.unpack('<I', b[12:16])[0]; js = json.loads(b[20:20 + n]); off = 20 + n + 8
bv = js['bufferViews'][js['images'][0]['bufferView']]
T0 = Image.open(io.BytesIO(b[off + bv.get('byteOffset', 0): off + bv.get('byteOffset', 0) + bv['byteLength']])).convert('RGB')
A = Image.open(TA).convert('RGB'); S = A.size[0]
T0 = np.asarray(T0.resize(A.size, Image.LANCZOS)).astype(np.float32); A = np.asarray(A).astype(np.float32)
M = np.asarray(Image.open(TA.replace('.png', '_mask.png')).convert('L')).astype(np.float32) / 255.0
d = np.load(NPZ); N = d['tex_nrm']; on = d['tex_tri'] >= 0
# the npz rows run in UV v (bottom-up); the PNG rows run top-down -- align by flipping if the mask agrees better that way
nz = N[..., 2]
if np.mean(on[::-1] == (M > 0.5)) > np.mean(on == (M > 0.5)): nz = nz[::-1]; on = on[::-1]
up = np.clip((nz - nz0) / (nz1 - nz0), 0, 1); up = up * up * (3 - 2 * up)
w = M * (1 - up)
w = ndimage.gaussian_filter(w, 2.0)
s2l = lambda x: np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4); l2s = lambda x: np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)
out = l2s(s2l(A / 255) * w[..., None] + s2l(T0 / 255) * (1 - w[..., None])) * 255
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT)
print(json.dumps(dict(on_mesh_texels=int(on.sum()), share_from_sheetA=round(float((w * on).sum() / on.sum()), 4),
                      share_from_tripo=round(float(((1 - w) * on).sum() / on.sum()), 4), nz_ramp=[nz0, nz1])))
