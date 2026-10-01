# R-C9-98 variant D: a VALUE GRADE on her painted armour atlas (the champion's s43 method) -- the bake left the steel pale
# (steel value contrast std L 18.2 -> 15.1). Regions from each piece GLB's OWN UVs; within breastplate / gauntlets / legs,
# STEEL texels only (low chroma: sat < 0.22, value > 0.30): an S-curve on value about 0.60 (x1.45) -- dark blue-grey recesses,
# bright edges -- and a slight cool tint (hue -> 215 deg, sat 0.07). Mail (darker, sat < 0.22, value <= 0.30) deepened x0.85.
# Scarlet wool, gold borders, the charcoal gown and the leggings are untouched.
#   python3 s44_steel_grade.py
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export')
S = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/sorceress_battlemage'
SIZE = 2048


def uv_mask(glb):
    js, b = L.load_glb(glb)
    img = Image.new('1', (SIZE, SIZE), 0); d = ImageDraw.Draw(img)
    for mesh in js['meshes']:
        for p in mesh['primitives']:
            uv = L.read_accessor(js, b, p['attributes']['TEXCOORD_0']) * SIZE
            for t in L.read_accessor(js, b, p['indices']).astype(int).reshape(-1, 3):
                d.polygon([tuple(uv[t[0]]), tuple(uv[t[1]]), tuple(uv[t[2]])], fill=1)
    return np.array(img, bool)


def rgb2hsv(a):
    mx, mn = a.max(2), a.min(2); d = mx - mn; h = np.zeros_like(mx)
    r, g, bb = a[..., 0], a[..., 1], a[..., 2]; nz = d > 1e-6
    hr = nz & (mx == r); hg = nz & (mx == g) & ~hr; hb = nz & ~hr & ~hg
    h[hr] = ((g - bb)[hr] / d[hr]) % 6; h[hg] = ((bb - r)[hg] / d[hg]) + 2; h[hb] = ((r - g)[hb] / d[hb]) + 4
    return h * 60, np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0), mx


def hsv2rgb(h, s, v):
    h = (h % 360) / 60; i = np.floor(h).astype(int) % 6; f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f)); out = np.zeros(h.shape + (3,))
    for k, (r_, g_, b_) in enumerate(((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))):
        m = i == k; out[m] = np.stack([r_[m], g_[m], b_[m]], 1)
    return out


A = np.array(Image.open(S + '/paint/tex_armour_final.png').convert('RGB').resize((SIZE, SIZE)), np.float64) / 255
h, s, v = rgb2hsv(A)
reg = np.zeros((SIZE, SIZE), bool)
for p in ("breastplate", "gauntlets", "legs"):
    reg |= uv_mask(S + '/export_v11/%s.glb' % p)
steel = reg & (s < 0.22) & (v > 0.30)
mail = reg & (s < 0.22) & (v <= 0.30)
h2, s2, v2 = h.copy(), s.copy(), v.copy()
v2[steel] = np.clip(0.60 + 1.45 * (v[steel] - 0.60), 0, 1); h2[steel] = 215.0; s2[steel] = np.maximum(s[steel], 0.07)
v2[mail] = v[mail] * 0.85
out = hsv2rgb(h2, s2, v2)
Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(S + '/paint/tex_armour_graded.png')
rep = dict(steel_texels=int(steel.sum()), mail_texels=int(mail.sum()), region_texels=int(reg.sum()),
           steel="value 0.60 + 1.45*(v-0.60), hue 215, sat >= 0.07", mail="value x0.85")
json.dump(rep, open(S + '/paint/steel_grade.json', 'w'), indent=1); print(json.dumps(rep))
