# VALUE GRADE on the painted body atlas (the champion's s43 / the battlemage's s44 method, no paint calls): the render now that the
# bake is really embedded reads plate L* 31.5 against the sheet's 26.7 (stage J). PLATE texels only -- low chroma (HSV sat < 0.28)
# that are not skin (hue 8-40 with sat > 0.18 excluded) -- get value x --gain (default 0.80) through a gentle S about 0.5 so the
# edges keep their paper highlights; GOLD (hue 30-65, sat > 0.28), the violet cloth and the face are untouched.
#   python3 e43_value_grade.py <tex.png> <out.png> [--gain 0.80] [--json f]
import sys, json, numpy as np
from PIL import Image
a = sys.argv[1:]; SRC, OUT = a[0], a[1]; G = float(a[a.index('--gain') + 1]) if '--gain' in a else 0.80
im = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float32) / 255.0
mx, mn = im.max(2), im.min(2); d = mx - mn; s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
r, g, b = im[..., 0], im[..., 1], im[..., 2]; h = np.zeros_like(mx); nz = d > 1e-6
hr = nz & (mx == r); hg = nz & (mx == g) & ~hr; hb = nz & ~hr & ~hg
h[hr] = (((g - b)[hr] / d[hr]) % 6) * 60; h[hg] = (((b - r)[hg] / d[hg]) + 2) * 60; h[hb] = (((r - g)[hb] / d[hb]) + 4) * 60
# v2: SKIN by the body's own UVs (faces whose vertices are weighted > 0.5 to Head/neck), not by hue -- v1's hue rule took 44% of
# the atlas as 'skin' (the painted plate is warm). GOLD = hue 30-65 with sat > 0.35 and value > 0.45; CLOTH = hue 250-340, sat > 0.12.
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); L = __import__('21_lint_export')
from PIL import ImageDraw
BODY = a[a.index('--body') + 1] if '--body' in a else 'export/wl_body.glb'
js, bb = L.load_glb(BODY); mn_ = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n); sk = js['skins'][0]
nm = [js['nodes'][j]['name'] for j in sk['joints']]; H_, W_ = im.shape[:2]; head = Image.new('L', (W_, H_), 0); dr = ImageDraw.Draw(head)
for pr in js['meshes'][js['nodes'][mn_]['mesh']]['primitives']:
    uv = L.read_accessor(js, bb, pr['attributes']['TEXCOORD_0']); J = L.read_accessor(js, bb, pr['attributes']['JOINTS_0']).astype(int)
    Wt = L.read_accessor(js, bb, pr['attributes']['WEIGHTS_0']); idx = L.read_accessor(js, bb, pr['indices']).astype(int).reshape(-1, 3)
    hw = np.array([sum(Wt[v, k] for k in range(4) if nm[J[v, k]] in ('Head', 'neck', 'head_end', 'headfront')) for v in range(len(uv))]) > 0.5
    for t in idx:
        if hw[t].all(): dr.polygon([(uv[v][0] * W_, uv[v][1] * H_) for v in t], fill=255)
skin = np.asarray(head) > 0
gold = (h >= 30) & (h <= 65) & (s > 0.35) & (mx > 0.45); cloth = (h >= 250) & (h <= 340) & (s > 0.12)
plate = ~skin & ~gold & ~cloth & (mx > 0.04)
k = np.where(plate, G * (1 + 0.15 * (mx - 0.5)), 1.0)[..., None]          # a touch less darkening on the highlights
out = np.clip(im * k, 0, 1)
Image.fromarray((out * 255).astype(np.uint8)).save(OUT)
rep = dict(gain=G, plate_texels_frac=round(float(plate.mean()), 4), skin_frac=round(float(skin.mean()), 4), gold_frac=round(float(gold.mean()), 4), cloth_frac=round(float(cloth.mean()), 4), mean_value_before=round(float(mx[plate].mean()), 4),
           mean_value_after=round(float(out.max(2)[plate].mean()), 4)); print(rep)
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
