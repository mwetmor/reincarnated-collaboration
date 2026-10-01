# R-C9-105 variant C (conductor): a VALUE GRADE on the painted atlases -- no paint calls.
#   python3 s43_value_grade.py
# Piece regions in the shared armour atlas are rasterised from each piece GLB's OWN UV triangles (no colour guessing about
# which texel is pelt and which is gold). Then, per region, in HSV on the painted texture:
#   metal (helm, chest, pauldron, girdle, greaves, wrists) -- gold texels only (hue 30-65 deg, sat > 0.28): an S-curve on
#       value about 0.55 (x1.45): darker bronze recesses, brighter gold highlights; a touch more saturation (x1.12).
#       Red straps (hue < 22 or > 335) and dark leather stay as painted.
#   kilt -- deepened toward the sheet's dark tawny brown: value x0.70, hue pulled 6 deg toward red-brown, sat x1.05.
#   wraps -- linen kept, slightly brightened (value x1.05) so the cream reads against the gold greaves.
#   body atlas, skin texels (hue 8-40, sat 0.18-0.65, not copper hair): sat x0.78 (pale, not orange) and an S-curve on value
#       about 0.62 (x1.25) plus +0.03: skin separates from gold by VALUE. Hair, loincloth, shoes untouched.
import json, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/nb_d2/scripts')
L = __import__('21_lint_export')
B = '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/gear_sets/barbarian_gladiator'
SIZE = 2048


def uv_mask(glb):
    js, b = L.load_glb(glb)
    m = np.zeros((SIZE, SIZE), bool)
    from PIL import ImageDraw
    img = Image.new('1', (SIZE, SIZE), 0); d = ImageDraw.Draw(img)
    for mesh in js['meshes']:
        for p in mesh['primitives']:
            uv = L.read_accessor(js, b, p['attributes']['TEXCOORD_0'])
            idx = L.read_accessor(js, b, p['indices']).astype(int).reshape(-1, 3)
            P = uv * SIZE                                  # glTF uv: v down from the top = image row
            for t in idx:
                d.polygon([tuple(P[t[0]]), tuple(P[t[1]]), tuple(P[t[2]])], fill=1)
    return np.array(img, bool)


def rgb2hsv(a):
    mx, mn = a.max(2), a.min(2); d = mx - mn
    h = np.zeros_like(mx)
    r, g, bb = a[..., 0], a[..., 1], a[..., 2]
    nz = d > 1e-6
    hr = nz & (mx == r); hg = nz & (mx == g) & ~hr; hb = nz & ~hr & ~hg
    h[hr] = ((g - bb)[hr] / d[hr]) % 6; h[hg] = ((bb - r)[hg] / d[hg]) + 2; h[hb] = ((r - g)[hb] / d[hb]) + 4
    return h * 60, np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0), mx


def hsv2rgb(h, s, v):
    h = (h % 360) / 60; i = np.floor(h).astype(int) % 6; f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.zeros(h.shape + (3,))
    for k, (r_, g_, b_) in enumerate(((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))):
        m = i == k; out[m] = np.stack([r_[m], g_[m], b_[m]], 1)
    return out


rep = {}
A = np.array(Image.open(B + '/paint/tex_armour_final.png').convert('RGB').resize((SIZE, SIZE)), np.float64) / 255
h, s, v = rgb2hsv(A)
masks = {p: uv_mask(B + '/export/%s.glb' % p) for p in ("helm", "chest", "pauldron", "girdle", "greaves", "wrists", "kilt", "wraps")}
metal = np.zeros((SIZE, SIZE), bool)
for p in ("helm", "chest", "pauldron", "girdle", "greaves", "wrists"):
    metal |= masks[p]
gold = metal & (h > 30) & (h < 65) & (s > 0.28)
v2, s2, h2 = v.copy(), s.copy(), h.copy()
v2[gold] = np.clip(0.55 + 1.45 * (v[gold] - 0.55), 0, 1); s2[gold] = np.clip(s[gold] * 1.12, 0, 1)
kilt = masks["kilt"] & ~metal
v2[kilt] = v[kilt] * 0.70; s2[kilt] = np.clip(s[kilt] * 1.05, 0, 1); h2[kilt] = h[kilt] - 6
wr = masks["wraps"] & ~metal & ~kilt
v2[wr] = np.clip(v[wr] * 1.05, 0, 1)
out = hsv2rgb(h2, s2, v2)
Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(B + '/paint/tex_armour_graded.png')
rep["armour"] = dict(texels=dict(gold=int(gold.sum()), kilt=int(kilt.sum()), wraps=int(wr.sum()),
                                 metal_region=int(metal.sum())),
                     gold_value_curve="0.55 + 1.45*(v-0.55), sat x1.12", kilt="value x0.70, hue -6 deg, sat x1.05", wraps="value x1.05")
Bd = np.array(Image.open(B + '/paint/tex_body_final.png').convert('RGB'), np.float64) / 255
h, s, v = rgb2hsv(Bd)
skin = (h > 8) & (h < 40) & (s > 0.18) & (s < 0.65) & (v > 0.35)
hair = (h < 30) & (s > 0.62) & (v > 0.35)
skin &= ~hair
s2, v2 = s.copy(), v.copy()
s2[skin] = s[skin] * 0.78; v2[skin] = np.clip(0.62 + 1.25 * (v[skin] - 0.62) + 0.03, 0, 1)
out = hsv2rgb(h, s2, v2)
Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(B + '/paint/tex_body_graded.png')
rep["body"] = dict(skin_texels=int(skin.sum()), skin="sat x0.78, value 0.62 + 1.25*(v-0.62) + 0.03; hair, loincloth, shoes untouched")
json.dump(rep, open(B + '/paint/value_grade.json', 'w'), indent=1)
print(json.dumps(rep))
