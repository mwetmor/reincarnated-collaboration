# R-C9-120 option A (CANDIDATE, pending the coordinator's ruling): LEGGINGS on her base body -- texture only. Every texel
# of a LEG face (faces whose vertices are dominated by an UpLeg/Leg bone, between the boot tops and the hips) that reads
# as SKIN (bright, warm, low saturation) is re-coloured to a dark wine cloth, keeping the texel's own shading (luma).
# Geometry, skin, morphs and clips byte-identical; the PNG is swapped in the binary chunk.
#   python3 r11_leggings.py <so-body.glb> <out.glb> [--rgb 0.30,0.12,0.11]
import io, json, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export'); R_ = __import__('49_recentre'); W = __import__('52_weapon_bones')
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_robe/scripts')
D = __import__('r01_diagnose')
a = sys.argv[1:]; BODY, OUT = a[0], a[1]
RGB = np.array([float(v) for v in (a[a.index('--rgb') + 1] if '--rgb' in a else '0.30,0.12,0.11').split(',')])
js, b, ni, jn, P, J, Wt, I = D.load(BODY)
pr = js['meshes'][js['nodes'][ni]['mesh']]['primitives'][0]
UV = L.read_accessor(js, b, pr['attributes']['TEXCOORD_0'])
Wd = np.zeros((len(P), len(jn))); np.add.at(Wd, (np.repeat(np.arange(len(P)), 4), J.ravel()), Wt.ravel())
legs = [jn.index(n) for n in ("LeftUpLeg", "RightUpLeg", "LeftLeg", "RightLeg")]
legv = Wd[:, legs].sum(1) > 0.5
G = D.node_world(js); nm = {n.get('name'): i for i, n in enumerate(js['nodes'])}
hip_y = 0.5 * (G[nm['LeftUpLeg']][1, 3] + G[nm['RightUpLeg']][1, 3])
face = legv[I].all(1) & (P[I][:, :, 1].max(1) < hip_y)
img_i = js['textures'][js['materials'][0]['pbrMetallicRoughness']['baseColorTexture']['index']]['source']
bv = js['bufferViews'][js['images'][img_i]['bufferView']]
im = Image.open(io.BytesIO(bytes(b[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]))).convert('RGB')
Wpx, Hpx = im.size
mask = Image.new('L', im.size, 0); dr = ImageDraw.Draw(mask)
for f in I[face]:
    dr.polygon([(UV[v, 0] * Wpx, UV[v, 1] * Hpx) for v in f], fill=255)
A = np.asarray(im).astype(float) / 255; M = np.asarray(mask) > 0
lum = A @ np.array([0.299, 0.587, 0.114]); mx = A.max(2); mn = A.min(2); sat = (mx - mn) / np.maximum(mx, 1e-6)
skin = M & (lum > 0.45) & (A[..., 0] >= A[..., 1]) & (A[..., 1] >= A[..., 2] - 0.02) & (sat < 0.55)
# grow the skin mask by 2 px inside the leg mask (texel bleed at UV edges)
from scipy.ndimage import binary_dilation
skin = binary_dilation(skin, iterations=2) & binary_dilation(M, iterations=2)
out = A.copy(); shade = (lum / max(np.median(lum[skin]), 1e-6)).clip(0.5, 1.4)[..., None]
out[skin] = (RGB[None, :] * shade[skin]).clip(0, 1)
buf = io.BytesIO(); Image.fromarray((out * 255).round().astype(np.uint8)).save(buf, 'PNG'); data = buf.getvalue()
b = bytearray(b); off = W.append(b, data)
js['bufferViews'].append({"buffer": 0, "byteOffset": off, "byteLength": len(data)})
js['images'][img_i]['bufferView'] = len(js['bufferViews']) - 1
js['buffers'][0]['byteLength'] = len(b)
R_.write_glb(OUT, js, bytes(b))
rep = dict(body=BODY, out=OUT, rgb=RGB.tolist(), leg_faces=int(face.sum()), leg_texels=int(M.sum()), skin_texels_recoloured=int(skin.sum()), texture=im.size)
print(json.dumps(rep)); json.dump(rep, open(OUT.replace('.glb', '.json'), 'w'), indent=1)
Image.fromarray((np.where(skin[..., None], [0, 255, 255], (A * 255)) ).astype(np.uint8)).resize((1024, 1024)).save(OUT.replace('.glb', '_mask.jpg'))
