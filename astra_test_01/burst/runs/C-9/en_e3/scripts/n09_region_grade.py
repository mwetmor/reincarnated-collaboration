# EN-E3 region grade (no new paint): inside a 3D region, take the texel colour back toward the Tripo projection of the APPROVED
# sheet (which carried the right local colour) while keeping the painted texture's ink and hatching (its luminance DETAIL).
#   python3 scripts/n09_region_grade.py <prep.glb> <surface.npz> <tex_in.png> <out.png> <region>
# region crab_legs: outside the shell's rigid-core ellipse and not the claws -- the thin slate legs the paint washed out (the D7
# sheet misregisters on 2-cm shapes, so the bake averaged leg paint with the floor of the plate).
import io, json, struct, sys
import numpy as np
from PIL import Image
from scipy import ndimage
GLB, NPZ, TIN, OUT, REG = sys.argv[1:6]
b = open(GLB, 'rb').read(); n = struct.unpack('<I', b[12:16])[0]; js = json.loads(b[20:20 + n]); off = 20 + n + 8
bv = js['images'][0]['bufferView']; bv = js['bufferViews'][bv]
T0 = Image.open(io.BytesIO(b[off + bv.get('byteOffset', 0): off + bv.get('byteOffset', 0) + bv['byteLength']])).convert('RGB')
A = Image.open(TIN).convert('RGB'); S = A.size[0]
T0 = np.asarray(T0.resize(A.size, Image.LANCZOS)).astype(np.float32); A = np.asarray(A).astype(np.float32)
d = np.load(NPZ); P = d['tex_pos']; on = d['tex_tri'] >= 0
M = np.asarray(Image.open(TIN.replace('T.png', '.png').replace('.png', '_mask.png')).convert('L')) > 127 if False else None
# the npz rows run in UV v (bottom-up) vs the PNG's top-down rows: decide by which orientation puts on-mesh texels where A has colour
lumA = A.mean(2)
if np.mean(lumA[on[::-1]] > 3) > np.mean(lumA[on] > 3): P = P[::-1]; on = on[::-1]
if REG == 'crab_legs':
    rig = json.load(open(GLB.replace('builds/crab_prep.glb', 'export/crab/crab.rig.json')))['landmarks']
    cy = rig['cy']; ex, ey = 0.82, 0.86
    x, y, z = P[..., 0], P[..., 1], P[..., 2]
    core = (x / ex) ** 2 + ((y - cy) / ey) ** 2 < 1.0
    claw = (np.abs(x) < 0.85) & (y < cy - 0.6)
    reg = on & ~core & ~claw & (z > 0.0)
elif REG == 'all':
    # the whole surface (the rimethorn: the paint bake washed the dark slate hide to cream; Tripo's projection of the approved sheet
    # keeps the local colour, the paint keeps its ink and hatching)
    reg = on.copy()
else:
    raise SystemExit('unknown region')
w = ndimage.gaussian_filter(reg.astype(np.float32), 1.5)[..., None]
lA = A.mean(2, keepdims=True); lT = T0.mean(2, keepdims=True)
detail = (lA - ndimage.gaussian_filter(lA[..., 0], 3)[..., None])          # the paint's ink/hatching, high-pass
graded = np.clip(T0 + 0.8 * detail, 0, 255)
out = A * (1 - w) + graded * w
Image.fromarray(out.astype(np.uint8)).save(OUT)
print(json.dumps(dict(region=REG, texels=int(reg.sum()), share_of_mesh=round(float(reg.sum() / on.sum()), 4),
                      mean_lum_before=round(float(lA[reg].mean()), 1), mean_lum_after=round(float(out.mean(2)[reg].mean()), 1),
                      mean_lum_tripo=round(float(lT[reg].mean()), 1))))
