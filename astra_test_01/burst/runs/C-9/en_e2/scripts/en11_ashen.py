# EN-E2 ASHEN GRADE (the conductor's note on the female caster, 2026-10-02: "lean her skin slightly more ashen or grey-blue, so she reads
# as possessed rather than living ... a colour grade on the bake is enough; no new sheet"). No paint call.
#   python3 scripts/en11_ashen.py <body.glb> <tex.png> <out.png> [--strength 0.7] [--json f]
# WHERE: skin is found by the body's OWN UVs, not by hue alone (e43 v2's lesson: a hue rule takes the ivory alb too) -- the
# triangles whose vertices are weighted > 0.5 to Head / neck / headfront / head_end / either Hand are rasterised into a UV mask.
# WHAT: inside that mask, WARM skin texels (hue 0-45 deg, saturation 0.06-0.55) that are NOT brass (circlet: hue 25-60 with
# saturation > 0.38) lose most of their warmth: chroma x (1 - s), then a small cool lift toward grey-blue (B +, R -), value kept.
import sys, json, os, colorsys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, TEX, OUT = a[0], a[1], a[2]
S = float(a[a.index('--strength') + 1]) if '--strength' in a else 0.7
js, b = L.load_glb(BODY)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
prim = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
read = lambda i: np.asarray(L.read_accessor(js, b, i))
uv = read(prim['attributes']['TEXCOORD_0']); J = read(prim["attributes"]["JOINTS_0"]).astype(np.int64); Wt = read(prim['attributes']['WEIGHTS_0'])
idx = read(prim["indices"]).astype(np.int64).reshape(-1, 3)
joints = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
want = {joints.index(n) for n in ('Head', 'neck', 'headfront', 'head_end', 'LeftHand', 'RightHand') if n in joints}
w_skin = np.zeros(len(uv))
for k in range(J.shape[1]):
    w_skin += np.where(np.isin(J[:, k], list(want)), Wt[:, k], 0.0)
tri = idx[(w_skin[idx] > 0.5).all(1)]
im = Image.open(TEX).convert('RGB'); Wd, Hd = im.size
mask = Image.new('L', (Wd, Hd), 0); dr = ImageDraw.Draw(mask)
for t in tri:
    dr.polygon([(float(uv[v, 0]) * Wd, float(uv[v, 1]) * Hd) for v in t], fill=255)
m = np.asarray(mask) > 0
x = np.asarray(im).astype(np.float32) / 255
mx, mnv = x.max(2), x.min(2); d = mx - mnv; sat = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
r, g, bb = x[..., 0], x[..., 1], x[..., 2]; h = np.zeros_like(mx); nz = d > 1e-6
hr = nz & (mx == r); hg = nz & (mx == g) & ~hr; hb = nz & ~hr & ~hg
h[hr] = (((g - bb)[hr] / d[hr]) % 6) * 60; h[hg] = (((bb - r)[hg] / d[hg]) + 2) * 60; h[hb] = (((r - g)[hb] / d[hb]) + 4) * 60
brass = (h > 25) & (h < 60) & (sat > 0.38)
warm = ((h < 45) | (h > 340)) & (sat > 0.06) & (sat < 0.55)
sel = m & warm & ~brass
lum = (x @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
y = lum + (x - lum) * (1 - S)                         # warmth out
y = y + np.array([-0.025, 0.0, 0.035], np.float32) * S   # a cool grey-blue lift
out = np.where(sel[..., None], np.clip(y, 0, 1), x)
Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(OUT)
rep = dict(body=BODY, tex=TEX, out=OUT, strength=S, skin_triangles=int(len(tri)), mask_texels=int(m.sum()), graded_texels=int(sel.sum()),
           mean_sat_before=round(float(sat[sel].mean()), 4) if sel.any() else None,
           mean_hue_before=round(float(h[sel].mean()), 1) if sel.any() else None)
print('ASHEN', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
