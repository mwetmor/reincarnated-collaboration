# EN-E2 round 4, THE WRETCH'S BOG GRADE (the conductor: "a greener-grey bog-mud skin (algae and silt tones on the shins and hands)", a
# grade, no new sheet). On the painted atlas, in CIE Lab, regions from the body's OWN geometry and the frozen region IDs (en17):
#   SKIN+HIDE  every texel that is NOT the lapis sash or brass (en17 region IDs): a* + --da (-7, toward green), b* + --db (+1), L* + --dl (-5)
#   SILT       a smoothstep by REST HEIGHT from the knee (0.30 H) down to the soles: a further a* --sa (-4), b* --sb (+4, algae-olive),
#              L* --sl (-10) at the soles (wet silt)
#   HANDS      the hands' UV mask: a* -4, L* -8 (the same mud on the hands)
#   python3 scripts/en36_bog_grade.py <static.glb> <regions.png> <in.png> <out.png> [--json f]
import json, sys, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = __import__('en16_colourlib'); L = __import__('21_lint_export'); W = __import__('52_weapon_bones')
a = sys.argv[1:]; BODY, REG, IN, OUT = a[:4]
o = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
DA, DB, DL, SA, SB, SL = o('--da', -7), o('--db', 1), o('--dl', -5), o('--sa', -4), o('--sb', 4), o('--sl', -10)
js, b = L.load_glb(BODY); G, _ = W.globals_(js)
mn = next(i for i, n in enumerate(js['nodes']) if 'skin' in n and 'mesh' in n)
pr = js['meshes'][js['nodes'][mn]['mesh']]['primitives'][0]
rd = lambda i: np.asarray(L.read_accessor(js, b, i))
uv = rd(pr['attributes']['TEXCOORD_0']); J = rd(pr['attributes']['JOINTS_0']).astype(int); Wt = rd(pr['attributes']['WEIGHTS_0'])
idx = rd(pr['indices']).astype(int).reshape(-1, 3)
V = W.skin_rest(js, b, mn, G); y = V[:, 1]; y0, H = float(y.min()), float(y.max() - y.min())
names = [js['nodes'][j]['name'] for j in js['skins'][js['nodes'][mn]['skin']]['joints']]
hands = [names.index(n) for n in ('LeftHand', 'RightHand')]
w_hand = sum(np.where(np.isin(J[:, k], hands), Wt[:, k], 0.0) for k in range(J.shape[1]))
im = np.asarray(Image.open(IN).convert('RGB')).astype(float) / 255; S = im.shape[0]
def raster(vals, sel):
    img = Image.new('F', (S, S), -1.0); d = ImageDraw.Draw(img)
    for t in idx[sel]:
        d.polygon([(float(uv[v, 0]) * S, float(uv[v, 1]) * S) for v in t], fill=float(vals[t].mean()))
    return np.asarray(img)
hmap = raster(y, np.ones(len(idx), bool)); used = hmap > -0.5
handm = raster(np.ones(len(y)), (w_hand[idx] > 0.5).all(1)) > 0
ids = np.asarray(Image.open(REG).convert('RGB'))
lapis = (ids[..., 0] == 255) & (ids[..., 1] == 0); brass = (ids[..., 2] == 255) & (ids[..., 0] == 0)
low = used & (hmap < y0 + 0.30 * H)                    # FIX (round 4 look): warm skin of the bare feet classes as 'brass' (en17); no brass below the knee
body = used & ~lapis & (~brass | low)
lab = C.rgb2lab(im); Lc, A_, B_ = lab[..., 0].copy(), lab[..., 1].copy(), lab[..., 2].copy()
A_[body] += DA; B_[body] += DB; Lc[body] = np.clip(Lc[body] + DL, 0, 100)
u = np.clip((y0 + 0.30 * H - hmap) / (0.30 * H), 0, 1); s = (u * u * (3 - 2 * u)) * body
A_ += SA * s; B_ += SB * s; Lc = np.clip(Lc + SL * s, 0, 100)
hm = handm & body; A_[hm] += -4; Lc[hm] = np.clip(Lc[hm] - 8, 0, 100)
out = C.lab2rgb(np.stack([Lc, A_, B_], -1)); out[~used] = im[~used]
Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(OUT)
rep = dict(params=dict(da=DA, db=DB, dl=DL, silt=dict(da=SA, db=SB, dl=SL, from_height_frac=0.30)), texels=dict(body=int(body.sum()), silt_weighted=int((s > 0.05).sum()), hands=int(hm.sum())))
print('BOG', json.dumps(rep))
if '--json' in a: json.dump(rep, open(a[a.index('--json') + 1], 'w'), indent=1)
